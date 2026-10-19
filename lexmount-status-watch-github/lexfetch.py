#!/usr/bin/env python3
"""Lexmount Status Watch.

Fetch public status pages through the Lexmount Web Fetch API and generate a
verifiable brief with raw API responses, request IDs, and SHA-256 checksums.

No third-party packages are required.
"""

from __future__ import annotations

import argparse
import csv
import hashlib
import json
import os
import re
import sys
import time
import unicodedata
import urllib.error
import urllib.request
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parent
USER_AGENT = "lexmount-status-watch/1.0"
RETRYABLE_HTTP = {408, 425, 429, 500, 502, 503, 504}

ISSUE_TERMS = [
    "investigating", "identified", "monitoring", "degraded performance",
    "partial outage", "major outage", "minor outage", "elevated error",
    "elevated latency", "error rates", "service disruption", "unavailable",
    "故障", "服务异常", "降级", "中断", "错误率升高", "延迟升高", "无法访问",
]
MAINTENANCE_TERMS = ["maintenance", "scheduled maintenance", "维护", "计划维护"]
OPERATIONAL_TERMS = [
    "all systems operational", "all systems normal", "fully operational", "systems operational",
    "所有系统正常运行", "全部系统正常运行", "运行正常",
]


def utc_now() -> datetime:
    return datetime.now(timezone.utc)


def timestamp_name(dt: datetime | None = None) -> str:
    dt = dt or utc_now()
    return dt.strftime("%Y%m%dT%H%M%SZ")


def compact(value: Any, limit: int = 720) -> str:
    if value is None:
        return ""
    text = unicodedata.normalize("NFKC", str(value))
    text = text.replace("\r", " ").replace("\n", " ")
    text = re.sub(r"\s+", " ", text).strip()
    if len(text) <= limit:
        return text
    return text[: limit - 1].rstrip() + "…"


def load_env(path: Path) -> None:
    """Load a small .env file without overriding existing environment values."""
    if not path.exists():
        return
    for raw in path.read_text(encoding="utf-8-sig").splitlines():
        line = raw.strip()
        if not line or line.startswith("#") or "=" not in line:
            continue
        key, value = line.split("=", 1)
        key = key.strip()
        value = value.strip().strip('"').strip("'")
        if key and key not in os.environ:
            os.environ[key] = value


def read_targets(path: Path) -> list[dict[str, str]]:
    data = json.loads(path.read_text(encoding="utf-8-sig"))
    raw_targets = data.get("targets") if isinstance(data, dict) else data
    if not isinstance(raw_targets, list):
        raise ValueError("targets.json must contain a top-level list or an object with a targets list")

    targets: list[dict[str, str]] = []
    seen: set[str] = set()
    for i, item in enumerate(raw_targets, 1):
        if not isinstance(item, dict):
            raise ValueError(f"target #{i} is not an object")
        target_id = compact(item.get("id"), 80)
        name = compact(item.get("name"), 100)
        url = compact(item.get("url"), 1000)
        if not target_id or not name or not url:
            raise ValueError(f"target #{i} requires id, name, and url")
        if not re.fullmatch(r"[A-Za-z0-9_.-]+", target_id):
            raise ValueError(f"target id {target_id!r} may only contain A-Z a-z 0-9 _ . -")
        if not url.lower().startswith(("http://", "https://")):
            raise ValueError(f"target {target_id!r} must use http/https")
        if target_id in seen:
            raise ValueError(f"duplicate target id: {target_id}")
        seen.add(target_id)
        targets.append({"id": target_id, "name": name, "url": url})
    if not targets:
        raise ValueError("at least one target is required")
    return targets


def classify(result: dict[str, Any]) -> tuple[str, list[str]]:
    """Conservatively classify a status page from extracted text."""
    title = unicodedata.normalize("NFKC", str(result.get("title") or ""))
    description = unicodedata.normalize("NFKC", str(result.get("description") or ""))
    main_text = unicodedata.normalize("NFKC", str(result.get("main_text") or ""))
    combined = " ".join([title, description, main_text])
    low = combined.lower()

    candidates = re.split(r"[\r\n]+|(?<=[。！？.!?])\s+", main_text)
    findings: list[str] = []
    for raw_line in candidates:
        clean = compact(raw_line, 300)
        candidate_low = clean.lower()
        if not clean:
            continue
        issue_hit = any(term in candidate_low or term in clean for term in ISSUE_TERMS)
        maintenance_hit = any(term in candidate_low or term in clean for term in MAINTENANCE_TERMS)
        if issue_hit or maintenance_hit:
            findings.append(clean)
    findings = list(dict.fromkeys(findings))[:8]

    has_issue = any(term in low or term in combined for term in ISSUE_TERMS)
    has_maintenance = any(term in low or term in combined for term in MAINTENANCE_TERMS)
    has_operational = any(term in low or term in combined for term in OPERATIONAL_TERMS)

    # An explicit all-operational banner is stronger than historical incident
    # entries such as "Past Incidents" or legend text on status pages.
    if has_operational:
        return "operational", findings
    if has_issue:
        return "possible_issue", findings
    if has_maintenance:
        return "maintenance", findings
    return "unknown", findings


def post_json(url: str, payload: dict[str, Any], headers: dict[str, str], timeout: int = 45) -> tuple[int, dict[str, Any] | bytes, dict[str, str]]:
    body = json.dumps(payload, ensure_ascii=False, separators=(",", ":")).encode("utf-8")
    req = urllib.request.Request(url=url, data=body, method="POST", headers=headers)
    try:
        with urllib.request.urlopen(req, timeout=timeout) as resp:
            content = resp.read()
            return resp.status, json.loads(content.decode("utf-8")), dict(resp.headers.items())
    except urllib.error.HTTPError as exc:
        content = exc.read()
        try:
            parsed: dict[str, Any] | bytes = json.loads(content.decode("utf-8"))
        except Exception:
            parsed = content
        return exc.code, parsed, dict(exc.headers.items())
    except Exception as exc:
        return 0, {"error": {"code": "client_request_failed", "message": str(exc)}}, {}


def call_lexmount_extract(
    base_url: str,
    target: dict[str, str],
    api_key: str,
    project_id: str,
    include_trace: bool,
    attempts: int,
    timeout: int,
) -> tuple[dict[str, Any], list[dict[str, Any]]]:
    endpoint = base_url.rstrip("/") + "/v1/extract"
    headers = {
        "Content-Type": "application/json",
        "User-Agent": USER_AGENT,
        "X-API-Key": api_key,
        "X-Project-Id": project_id,
    }
    payload: dict[str, Any] = {"extract": {"url": target["url"]}}
    if include_trace:
        payload["trace"] = {"include_steps": True}

    attempts_log: list[dict[str, Any]] = []
    for attempt in range(1, attempts + 1):
        started = utc_now().isoformat().replace("+00:00", "Z")
        status, response, response_headers = post_json(endpoint, payload, headers, timeout)
        finished = utc_now().isoformat().replace("+00:00", "Z")
        request_id = ""
        if isinstance(response, dict):
            request_id = compact(response.get("request_id"), 100)
        if not request_id:
            request_id = compact(response_headers.get("X-Request-ID"), 100)
        if isinstance(response, bytes):
            response = {"raw_response": response.decode("utf-8", errors="replace")}
        attempts_log.append({
            "attempt": attempt,
            "started_at": started,
            "finished_at": finished,
            "http_status": status,
            "request_id": request_id,
        })
        if status == 200:
            return response if isinstance(response, dict) else {"raw_response": response}, attempts_log
        if (status != 0 and status not in RETRYABLE_HTTP) or attempt == attempts:
            return response if isinstance(response, dict) else {"raw_response": response}, attempts_log
        time.sleep(min(8.0, 0.75 * (2 ** (attempt - 1))))
    raise AssertionError("unreachable")


def write_json(path: Path, value: Any) -> None:
    path.write_text(json.dumps(value, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def sha256_file(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as f:
        for block in iter(lambda: f.read(1024 * 1024), b""):
            h.update(block)
    return h.hexdigest()


def render_report(
    out_dir: Path,
    generated_at: str,
    rows: list[dict[str, Any]],
    endpoint: str,
    trace_enabled: bool,
) -> str:
    issue_count = sum(r["status"] in {"possible_issue", "maintenance"} for r in rows)
    unknown_count = sum(r["status"] == "unknown" for r in rows)
    failed_count = sum(not r["ok"] for r in rows)
    lines = [
        "# 服务状态巡检简报",
        "",
        f"- 生成时间：`{generated_at}`",
        f"- 抓取服务：Lexmount Web Fetch `{endpoint}`",
        f"- 目标数量：{len(rows)}",
        f"- 疑似异常/维护：{issue_count}",
        f"- 未知：{unknown_count}",
        f"- API 调用失败：{failed_count}",
        f"- Trace：{'开启' if trace_enabled else '关闭'}",
        "",
        "> 结论由正文关键词保守识别，最终请以各服务商状态页为准。",
        "",
        "## 总览",
        "",
        "| 服务 | 判定 | 目标状态码 | 引擎 | 标题 | 来源 |",
        "|---|---|---:|---|---|---|",
    ]
    for row in rows:
        title = compact(row.get("title"), 80) or "-"
        engine = compact(row.get("engine"), 40) or "-"
        target_status = "-" if row.get("target_status_code") is None else str(row.get("target_status_code"))
        status = row["status"]
        lines.append(
            f"| {row['name']} | `{status}` | {target_status} | `{engine}` | {title} "
            f"| [打开]({row['url']}) |"
        )

    lines.extend(["", "## 详情", ""])
    for row in rows:
        lines.extend([
            f"### {row['name']} — `{row['status']}`",
            "",
            f"- 目标 URL：<{row['url']}>",
            f"- 最终 URL：{row.get('final_url') or '-'}",
            f"- Lexmount request_id：`{row.get('request_id') or '-'}`",
            f"- Lexmount dom_id：`{row.get('dom_id') or '-'}`",
            f"- 目标状态码：{row.get('target_status_code') if row.get('target_status_code') is not None else '-'}",
            f"- 抓取引擎：`{row.get('engine') or '-'}`",
            f"- Raw 文件：`{row.get('raw_relative') or '-'}`",
            f"- 摘要：{compact(row.get('excerpt'), 500) or '-'}",
        ])
        findings = row.get("findings") or []
        if findings:
            lines.append("- 命中的提示：")
            for finding in findings:
                lines.append(f"  - {compact(finding, 260)}")
        else:
            lines.append("- 命中的提示：无")
        if not row["ok"]:
            lines.append(f"- API 错误摘要：`{compact(row.get('error_summary'), 300)}`")
        lines.append("")

    lines.extend([
        "## 核验步骤",
        "",
        "1. 打开本表中的来源 URL，确认服务商当前页面；",
        "2. 打开对应 `raw/*.json`，核对 `request_id`、`result.final_url` 和 `result.title`；",
        "3. 查看 `run_manifest.json` 的调用索引；",
        "4. 使用 `SHA256SUMS.txt` 检查成果文件是否与本次运行一致。",
        "",
    ])
    return "\n".join(lines)


def run(args: argparse.Namespace) -> int:
    env_path = args.env if args.env.is_absolute() else ROOT / args.env
    load_env(env_path)
    targets_path = args.targets if args.targets.is_absolute() else ROOT / args.targets
    targets = read_targets(targets_path)

    if args.only:
        wanted = {x.strip().lower() for x in args.only.split(",") if x.strip()}
        targets = [t for t in targets if t["id"].lower() in wanted]
        if not targets:
            print("No target matched --only", file=sys.stderr)
            return 2

    api_key = os.environ.get("LEXMOUNT_API_KEY", "").strip()
    project_id = os.environ.get("LEXMOUNT_PROJECT_ID", "").strip()
    base_url = os.environ.get("LEXMOUNT_BASE_URL", "https://api.lexmount.cn").strip().rstrip("/")

    if args.dry_run:
        print("DRY-RUN OK")
        print(f"targets={len(targets)}")
        print(f"base_url={base_url}")
        print(f"api_key_present={bool(api_key)}")
        print(f"project_id_present={bool(project_id)}")
        for t in targets:
            print(f"- {t['id']}: {t['name']} <{t['url']}>")
        return 0

    if not api_key or not project_id:
        print("Missing LEXMOUNT_API_KEY or LEXMOUNT_PROJECT_ID.", file=sys.stderr)
        print("Copy .env.example to .env and fill both values.", file=sys.stderr)
        return 2

    generated_at = utc_now().isoformat().replace("+00:00", "Z")
    out_dir = args.out_dir if args.out_dir.is_absolute() else ROOT / args.out_dir
    out_dir = out_dir / f"run-{timestamp_name()}"
    raw_dir = out_dir / "raw"
    raw_dir.mkdir(parents=True, exist_ok=True)

    endpoint = base_url + "/v1/extract"
    rows: list[dict[str, Any]] = []
    calls: list[dict[str, Any]] = []

    for index, target in enumerate(targets, 1):
        print(f"[{index}/{len(targets)}] {target['name']}: {target['url']}")
        response, attempts_log = call_lexmount_extract(
            base_url=base_url,
            target=target,
            api_key=api_key,
            project_id=project_id,
            include_trace=args.trace,
            attempts=args.attempts,
            timeout=args.timeout,
        )
        raw_path = raw_dir / f"{target['id']}.json"
        write_json(raw_path, response)

        result = response.get("result") if isinstance(response.get("result"), dict) else {}
        status, findings = classify(result)
        request_id = compact(response.get("request_id"), 100)
        if not request_id:
            request_id = compact(attempts_log[-1].get("request_id"), 100) if attempts_log else ""
        dom_id = compact(response.get("metadata", {}).get("dom_id") if isinstance(response.get("metadata"), dict) else result.get("dom_id"), 100)
        if not dom_id and isinstance(result.get("dom_id"), str):
            dom_id = compact(result.get("dom_id"), 100)

        error = response.get("error") if isinstance(response.get("error"), dict) else None
        if error:
            error_summary = json.dumps(error, ensure_ascii=False, separators=(",", ":"))
        elif not result:
            error_summary = json.dumps(response, ensure_ascii=False)[:500]
        else:
            error_summary = ""

        raw_relative = raw_path.relative_to(out_dir).as_posix()
        row = {
            "id": target["id"],
            "name": target["name"],
            "url": target["url"],
            "final_url": compact(result.get("final_url"), 1000),
            "title": compact(result.get("title"), 200),
            "excerpt": compact(result.get("main_text"), 500),
            "status": status,
            "findings": findings,
            "engine": compact(result.get("engine"), 40),
            "target_status_code": result.get("status_code"),
            "request_id": request_id,
            "dom_id": dom_id,
            "ok": bool(result),
            "error_summary": error_summary,
            "raw_relative": raw_relative,
            "attempts": attempts_log,
            "generated_at": generated_at,
        }
        rows.append(row)
        calls.append({
            "service_id": target["id"],
            "service_name": target["name"],
            "target_url": target["url"],
            "endpoint": endpoint,
            "http_call_ok": bool(result),
            "request_id": request_id,
            "dom_id": dom_id,
            "engine": row["engine"],
            "target_status_code": row["target_status_code"],
            "raw_file": raw_relative,
            "attempts": attempts_log,
        })
        time.sleep(args.delay)

    report_path = out_dir / "report.md"
    report_path.write_text(render_report(out_dir, generated_at, rows, endpoint, args.trace), encoding="utf-8")

    summary_path = out_dir / "summary.json"
    write_json(summary_path, {
        "generated_at": generated_at,
        "tool": USER_AGENT,
        "endpoint": endpoint,
        "trace_enabled": args.trace,
        "target_count": len(rows),
        "issue_or_maintenance_count": sum(r["status"] in {"possible_issue", "maintenance"} for r in rows),
        "unknown_count": sum(r["status"] == "unknown" for r in rows),
        "api_failure_count": sum(not r["ok"] for r in rows),
        "results": rows,
    })

    csv_path = out_dir / "summary.csv"
    with csv_path.open("w", encoding="utf-8-sig", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=[
            "id", "name", "status", "target_status_code", "engine", "title",
            "final_url", "url", "request_id", "dom_id", "excerpt", "raw_relative",
        ])
        writer.writeheader()
        for r in rows:
            writer.writerow({k: r.get(k, "") for k in writer.fieldnames})

    jsonl_path = out_dir / "summary.jsonl"
    with jsonl_path.open("w", encoding="utf-8") as f:
        for r in rows:
            slim = {k: r.get(k) for k in [
                "generated_at", "id", "name", "url", "final_url", "status",
                "findings", "target_status_code", "engine", "request_id", "dom_id",
                "title", "excerpt", "raw_relative", "ok", "error_summary",
            ]}
            f.write(json.dumps(slim, ensure_ascii=False, separators=(",", ":")) + "\n")

    manifest_path = out_dir / "run_manifest.json"
    write_json(manifest_path, {
        "generated_at": generated_at,
        "tool": USER_AGENT,
        "region_base_url": base_url,
        "endpoint": endpoint,
        "trace_enabled": args.trace,
        "targets_file": str(targets_path),
        "target_count": len(rows),
        "calls": calls,
        "security_note": "No API key or project id is stored in artifacts.",
    })

    hashed = sorted([
        report_path, summary_path, csv_path, jsonl_path, manifest_path,
        *(raw_dir / f"{r['id']}.json" for r in rows),
    ])
    sums_path = out_dir / "SHA256SUMS.txt"
    with sums_path.open("w", encoding="utf-8", newline="\n") as f:
        for p in hashed:
            f.write(f"{sha256_file(p)}  {p.relative_to(out_dir).as_posix()}\n")

    print(f"Artifact directory: {out_dir}")
    print(f"Report: {report_path}")
    print(f"Success: {sum(r['ok'] for r in rows)}/{len(rows)}; possible issues/maintenance: {sum(r['status'] in {'possible_issue','maintenance'} for r in rows)}")
    return 0 if all(r["ok"] for r in rows) else 1


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--env", type=Path, default=ROOT / ".env", help="Path to .env file")
    parser.add_argument("--targets", type=Path, default=ROOT / "targets.json", help="Path to targets JSON")
    parser.add_argument("--out-dir", type=Path, default=ROOT / "artifacts", help="Base artifact directory")
    parser.add_argument("--only", help="Comma-separated target IDs to fetch")
    parser.add_argument("--trace", action="store_true", help="Ask Lexmount to include trace steps")
    parser.add_argument("--delay", type=float, default=0.5, help="Delay between targets in seconds")
    parser.add_argument("--attempts", type=int, default=3, help="Attempts per target for retryable HTTP statuses")
    parser.add_argument("--timeout", type=int, default=45, help="Client timeout in seconds")
    parser.add_argument("--dry-run", action="store_true", help="Validate config and credentials without calling the API")
    return parser.parse_args()


if __name__ == "__main__":
    try:
        raise SystemExit(run(parse_args()))
    except (ValueError, OSError, json.JSONDecodeError) as exc:
        print(f"ERROR: {exc}", file=sys.stderr)
        raise SystemExit(2)





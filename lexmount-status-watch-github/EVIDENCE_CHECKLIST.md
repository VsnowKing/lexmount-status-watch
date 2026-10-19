# 核验清单

提交前逐项检查。

## A. 账号与平台

- [ ] 已通过活动入口登录 Lexmount；
- [ ] 已完成活动报名；
- [ ] 已确认活动截止时间：2026-11-08 23:59（北京时间）；
- [ ] API Key 来自同一个 Lexmount 项目；
- [ ] `LEXMOUNT_PROJECT_ID` 与 API Key 属于同一项目。

## B. 实际运行

- [ ] 已执行 `python .\lexfetch.py --dry-run`，配置校验通过；
- [ ] 已至少完成一次真实 Lexmount Web Fetch 调用；
- [ ] `artifacts/` 下存在本次运行目录；
- [ ] `report.md` 非空；
- [ ] `summary.csv`、`summary.jsonl` 可打开；
- [ ] `run_manifest.json` 可被 JSON 解析；
- [ ] 每个成功目标都有 `raw/*.json`；
- [ ] raw JSON 中存在 `request_id`；
- [ ] 成功结果中尽量能找到 `dom_id`、`engine`、`final_url`。

## C. 材料脱敏

- [ ] 不提交 `.env`；
- [ ] 公开材料中搜索不到真实 API Key；
- [ ] 公开材料中搜索不到真实 Project ID；
- [ ] raw JSON 只包含公开状态页内容；
- [ ] 截图和日志没有个人手机号、身份证、住址等敏感信息。

## D. 文档

- [ ] `README.md` 能让他人复现；
- [ ] `SUBMISSION.md` 的 `[待填]` 已全部替换；
- [ ] 作者名单与实际贡献准确；
- [ ] 如果有旧项目基础，已说明旧基础与新增工作；
- [ ] 局限性已经写明。

## E. 提交

- [ ] 作品链接公开可访问；
- [ ] 压缩包或仓库路径可在另一台设备下载；
- [ ] 已保留本地原始运行目录备份；
- [ ] 提交表单内容与 `SUBMISSION.md` 一致；
- [ ] 截止前保存提交成功页面或提交确认截图。

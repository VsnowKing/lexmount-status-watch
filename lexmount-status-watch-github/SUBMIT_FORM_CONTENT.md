# 提交表单粘贴内容

> 打开提交页并登录后，按表单字段选用下面内容。方括号处先替换成你的真实信息。

## 作品名称

```text
Lexmount Status Watch
```

## 作品简介 / 任务描述

```text
基于 Lexmount Web Fetch API 的公开服务状态页巡检工具。一次读取 GitHub、Cloudflare、Vercel、OpenAI、Stripe、Supabase 的状态页，生成人工可读简报和 CSV/JSONL 结构化摘要，并保留 Lexmount request_id、dom_id、引擎、目标状态码、raw JSON 与 SHA-256 清单，便于核验。
```

## 做法说明

```text
1. targets.json 维护公开状态页清单。
2. lexfetch.py 逐个调用 Lexmount Web Fetch POST /v1/extract，请求头使用 X-API-Key 与 X-Project-Id。
3. 保存每次 API 响应到 raw/*.json。
4. 从 title/description/main_text 保守识别 operational / possible_issue / maintenance / unknown。
5. 汇总生成 report.md、summary.csv、summary.jsonl、run_manifest.json 和 SHA256SUMS.txt。
6. 状态页明确显示 All Systems Operational / Fully Operational 时优先判定为正常，避免被历史事件干扰。
```

## Lexmount 使用说明

```text
使用 Lexmount Web Fetch API：POST https://api.lexmount.cn/v1/extract。
最终运行共 6 个目标、6 次成功调用、0 次失败。
每次结果保留 request_id、final_url、status_code、title、main_text、engine、dom_id。
最终运行 Trace 关闭；未提交 API Key 或 Project ID。
```

## 运行时间

```text
2026-10-19 22:31 左右，北京时间。
```

## 结果摘要

```text
成功抓取 6/6。
正常 4 个：GitHub、Vercel、OpenAI、Supabase。
疑似异常 1 个：Cloudflare，页面显示活跃的 WARP 地理位置错误事件。
未知 1 个：Stripe，该次抓取只返回 Loading...。
API 调用失败 0 个。
```

## 核验方式

```text
1. 打开 report.md 查看每个目标的状态、来源 URL、request_id 和 dom_id。
2. 打开 raw/*.json 核对 request_id、result.final_url、result.title。
3. 查看 run_manifest.json 中的调用索引和 raw 文件映射。
4. 用 SHA256SUMS.txt 校验本次成果文件完整性。
```

## 局限说明

```text
工具是巡检辅助，不是官方可用性结论。当前使用通用正文提取和保守关键词判定；强 JavaScript 渲染页面可能只得到 Loading...，会保守标记为 unknown。工具不处理需要登录、内网或付费合同才能访问的状态。
```

## 需要你补齐的信息

```text
作者 / 团队：
邮箱：
身份 / 学校：
是否组队：
作品链接：
```

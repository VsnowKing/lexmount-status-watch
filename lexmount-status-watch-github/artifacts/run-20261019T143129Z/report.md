# 服务状态巡检简报

- 生成时间：`2026-10-19T14:31:29.741008Z`
- 抓取服务：Lexmount Web Fetch `https://api.lexmount.cn/v1/extract`
- 目标数量：6
- 疑似异常/维护：1
- 未知：1
- API 调用失败：0
- Trace：关闭

> 结论由正文关键词保守识别，最终请以各服务商状态页为准。

## 总览

| 服务 | 判定 | 目标状态码 | 引擎 | 标题 | 来源 |
|---|---|---:|---|---|---|
| GitHub | `operational` | 200 | `lightmount_lite` | GitHub Status | [打开](https://www.githubstatus.com/) |
| Cloudflare | `possible_issue` | 200 | `lightmount_dcl` | Cloudflare Status | [打开](https://www.cloudflarestatus.com/) |
| Vercel | `operational` | 200 | `lightmount_dcl` | Vercel Status | [打开](https://www.vercel-status.com/) |
| OpenAI | `operational` | 200 | `lightmount_lite` | OpenAI Status | [打开](https://status.openai.com/) |
| Stripe | `unknown` | 200 | `lightmount_dcl` | Stripe system status | [打开](https://status.stripe.com/) |
| Supabase | `operational` | 200 | `lightmount_dcl` | Supabase Status | [打开](https://status.supabase.com/) |

## 详情

### GitHub — `operational`

- 目标 URL：<https://www.githubstatus.com/>
- 最终 URL：https://www.githubstatus.com/
- Lexmount request_id：`5437bb83-c674-4a06-b155-a4f74a706854`
- Lexmount dom_id：`846751`
- 目标状态码：200
- 抓取引擎：`lightmount_lite`
- Raw 文件：`raw/github.json`
- 摘要：Overall Status: All Systems Operational Components: - Git Operations: Operational - Webhooks: Operational - Visit www.githubstatus.com for more information: Operational - API Requests: Operational - Issues: Operational - Pull Requests: Operational - Actions: Operational - Packages: Operational - Pages: Operational - Copilot: Operational - Codespaces: Operational - Copilot AI Model Providers: Operational About This Site: Check GitHub Enterprise Cloud status by region: - Australia: au.githubstatu…
- 命中的提示：无

### Cloudflare — `possible_issue`

- 目标 URL：<https://www.cloudflarestatus.com/>
- 最终 URL：https://www.cloudflarestatus.com/
- Lexmount request_id：`5c4fde40-69a2-4071-8e0d-efd6d178e0d4`
- Lexmount dom_id：`846752`
- 目标状态码：200
- 抓取引擎：`lightmount_dcl`
- Raw 文件：`raw/cloudflare.json`
- 摘要：Cloudflare Status Skip to main content Support (opens in new tab) Dashboard (opens in new tab) Local time Showing local times Overview Services & Sites Locations History Cloudflare System Status Subscribe to updates Active incidents Incorrect geo location for some Cloudflare WARP users Identified WARP Identified Recent incidents View All DNS Update Delays Minor Resolved Oct 19, 2026, 11:50 UTC Active maintenance View All No active maintenance View all future maintenance About Us (opens in new t…
- 命中的提示：
  - Cloudflare Status Skip to main content Support (opens in new tab) Dashboard (opens in new tab) Local time Showing local times Overview Services & Sites Locations History Cloudflare System Status Subscribe to updates Active incidents Incorrect geo location for…

### Vercel — `operational`

- 目标 URL：<https://www.vercel-status.com/>
- 最终 URL：https://www.vercel-status.com/
- Lexmount request_id：`3e193cf3-3a33-4bea-8b38-362c668c0e92`
- Lexmount dom_id：`846753`
- 目标状态码：200
- 抓取引擎：`lightmount_dcl`
- Raw 文件：`raw/vercel.json`
- 摘要：Vercel Status Subscribe to Updates Subscribe x Get email notifications whenever Vercel creates , updates or resolves an incident. Email address: Enter OTP: Resend OTP in: seconds Didn't receive the OTP? Resend OTP By subscribing you agree to our Privacy Policy . This site is protected by reCAPTCHA and the Google Privacy Policy and Terms of Service apply. Get text message notifications whenever Vercel creates or resolves an incident. Country code: Afghanistan (+93) Albania (+355) Algeria (+213).…
- 命中的提示：
  - Get incident updates and maintenance status messages in Slack.
  - had a major outage.
  - had a partial outage.
  - Related No incidents or maintenance related to this downtime.
  - Oct 12 , 2026 , 20:11 UTC (6 days ago) Monitoring - The backlog of deployment events has been processed.
  - Oct 12 , 2026 , 14:57 UTC (6 days ago) Identified - We have identified the issue and are working on a fix.
  - Oct 12 , 2026 , 14:08 UTC (7 days ago) Investigating - We've identified an issue where some customers may experience build failures or deployments that fail to start.
  - We are investigating this issue.

### OpenAI — `operational`

- 目标 URL：<https://status.openai.com/>
- 最终 URL：https://status.openai.com/
- Lexmount request_id：`7fc2c4a4-e8be-4716-8088-2d1679be5234`
- Lexmount dom_id：`846754`
- 目标状态码：200
- 抓取引擎：`lightmount_lite`
- Raw 文件：`raw/openai.json`
- 摘要：We’re fully operational. We’re not aware of any issues affecting our systems. System status: - APIs: 14 components, 99.95% uptime - ChatGPT: 16 components, 99.52% uptime - Codex: 4 components, 99.95% uptime - FedRAMP: 1 components, 100% uptime - Ads Platform: 2 components, 99.992% uptime Availability metrics are reported at an aggregate level across all tiers, models and error types. Individual customer availability may vary depending on their subscription tier as well as the specific model and…
- 命中的提示：无

### Stripe — `unknown`

- 目标 URL：<https://status.stripe.com/>
- 最终 URL：https://status.stripe.com/
- Lexmount request_id：`45949b84-fd9d-411d-9941-363496f10ab5`
- Lexmount dom_id：`846755`
- 目标状态码：200
- 抓取引擎：`lightmount_dcl`
- Raw 文件：`raw/stripe.json`
- 摘要：Stripe system status Loading...
- 命中的提示：无

### Supabase — `operational`

- 目标 URL：<https://status.supabase.com/>
- 最终 URL：https://status.supabase.com/
- Lexmount request_id：`29bd8f7b-5688-48a8-af3a-b4727b11099f`
- Lexmount dom_id：`846757`
- 目标状态码：200
- 抓取引擎：`lightmount_dcl`
- Raw 文件：`raw/supabase.json`
- 摘要：Supabase Status Report a problem Subscribe to updates Report a problem Subscribe to updates We’re fully operational Having a supa day. All systems are operational. System status Sep 2026 - Oct 2026 Branching 18 components Branching 18 components ap-east-1 100 % uptime ap-east-1 ap-northeast-1 100 % uptime ap-northeast-1 ap-northeast-2 100 % uptime ap-northeast-2 ap-south-1 100 % uptime ap-south-1 ap-southeast-1 100 % uptime ap-southeast-1 ap-southeast-2 100 % uptime ap-southeast-2 ca-central-1.…
- 命中的提示：无

## 核验步骤

1. 打开本表中的来源 URL，确认服务商当前页面；
2. 打开对应 `raw/*.json`，核对 `request_id`、`result.final_url` 和 `result.title`；
3. 查看 `run_manifest.json` 的调用索引；
4. 使用 `SHA256SUMS.txt` 检查成果文件是否与本次运行一致。

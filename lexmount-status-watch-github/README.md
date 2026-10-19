# Lexmount Status Watch

一个为「Lexmount 云平台真实任务挑战」准备的小型实践作品：
用 Lexmount Web Fetch API 巡检多个公开服务状态页，生成带来源、请求 ID 与原始 API 响应的服务状态简报。

## 为什么做这个

排查「某个依赖是不是挂了」经常要在多个状态页之间来回跳。这个工具把公开状态页巡检变成一次可复现的 API 任务，并保留核验材料：

- 每个目标页面由 Lexmount Web Fetch `/v1/extract` 抓取；
- 保存 `request_id`、`dom_id`、引擎、HTTP 状态、标题和正文摘要；
- 自动识别常见故障、降级、维护提示；
- 输出 Markdown 简报、CSV 摘要、JSONL 摘要和原始响应；
- 生成 SHA-256 清单，方便提交后核对文件未被改动。

## 目录

```text
lexmount-status-watch/
├─ README.md
├─ SUBMISSION.md
├─ PLAN.md
├─ targets.json
├─ lexfetch.py
├─ .env.example
└─ artifacts/
```

## 准备

1. 从 Lexmount 控制台创建 API Key：
   <https://browser.lexmount.cn/settings/api-keys>
2. 复制 `.env.example` 为 `.env`，填入：

```env
LEXMOUNT_API_KEY=your-api-key
LEXMOUNT_PROJECT_ID=your-project-id
LEXMOUNT_BASE_URL=https://api.lexmount.cn
```

不要把 `.env`、API Key 或 Project ID 上传到公开仓库。

## 运行

PowerShell：

```powershell
python .\lexfetch.py --dry-run
python .\lexfetch.py
```

可选参数：

```powershell
# 使用自定义目标清单
python .\lexfetch.py --targets .\targets.json

# 只巡检指定服务
python .\lexfetch.py --only github,cloudflare

# 请求 Lexmount trace，便于排查抓取链路
python .\lexfetch.py --trace
```

2026-10-19 已完成一次真实运行：6 个目标成功 6 个，其中 Cloudflare 识别到活跃事件，Stripe 因页面仅返回 Loading... 标记为 unknown。`artifacts/run-20261019T143129Z/` 保留了最终证据。`artifacts/run-20261019T142940Z/` 是改进判定前的开发运行记录。`artifacts/` 默认不进入 Git，提交时请单独打包需要公开的运行目录。成功后会生成类似下面的目录：

```text
artifacts/run-20261019T123000Z/
├─ report.md
├─ summary.json
├─ summary.csv
├─ summary.jsonl
├─ run_manifest.json
├─ SHA256SUMS.txt
└─ raw/github.json
```

## 输出说明

### report.md

给人阅读的简报，包含：

- 巡检时间；
- 总数、异常数、未知数；
- 每个站点的服务名、状态判定、目标 URL、来源链接；
- Lexmount 返回的目标状态码、引擎、标题；
- 从状态页正文摘要中提取的疑似故障/维护行；
- 对应 raw JSON 文件路径。

### summary.csv / summary.jsonl

便于表格和程序处理。

### run_manifest.json

记录每次调用的：

- 本地时间；
- 服务名；
- 目标 URL；
- HTTP 是否成功；
- Lexmount `request_id`；
- `dom_id`；
- 引擎；
- raw 文件路径。

### SHA256SUMS.txt

对当次报告、摘要、manifest 和 raw JSON 做完整性清单。

## 状态判定

当前只做保守判断：

- `operational`：状态页明确出现 All Systems Operational / Fully Operational / 所有系统正常运行等横幅；该判定优先于历史事件文案；
- `possible_issue`：命中 investigating、identified、monitoring、degraded performance、partial/major/minor outage、elevated error/latency、service disruption、unavailable、故障、服务异常、降级、中断、错误率升高、延迟升高、无法访问等关键词；
- `maintenance`：命中 maintenance、维护；
- `unknown`：内容不足或无法确定。

这不是替代服务商官方公告的结论。简报始终保留来源链接和 raw JSON，读者应回到原始状态页确认。

## 隐私与安全

- 只巡检公开状态页；
- 脚本不会输出或保存 API Key；
- `.env` 已加入 `.gitignore`；
- raw 响应里不主动请求 `raw_dom`，避免保存整页 DOM；
- 如需公开仓库，请先检查 raw JSON 是否包含不想公开的内容。

## 核验方式

1. 打开 `report.md`，检查服务状态和来源 URL；
2. 打开对应 `raw/*.json`，核对 `request.result.title`、`request.result.final_url`、`request_id`；
3. 对比 `run_manifest.json` 中的 `dom_id`；
4. 用 `SHA256SUMS.txt` 校验文件完整性：

```powershell
Get-FileHash -Algorithm SHA256 .\report.md
```

## 后续可扩展

- 增加定时巡检和趋势记录；
- 对每个状态页增加定制解析器；
- 加入历史响应 diff，突出新增事件；
- 将结果发布为静态页面；
- 对失败调用保存脱敏错误与建议。



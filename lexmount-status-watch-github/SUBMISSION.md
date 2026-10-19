# 作品提交草稿

> 本稿基于 2026-10-19 的真实运行结果。提交前只需补齐作者/团队信息和作品链接。

## 基本信息

- **作品名称**：Lexmount Status Watch
- **作品简介**：基于 Lexmount Web Fetch API 的公开服务状态页巡检工具，一次读取多个状态页，生成带来源、原始 API 响应、调用索引和 SHA-256 清单的服务状态简报。
- **作者 / 团队**：[待填]
- **邮箱**：[待填]
- **身份 / 学校**：[待填]
- **是否组队**：[待填；如组队，请列出全部实际作者与分工]
- **作品链接**：[待填：公开仓库 / 云盘 / 可访问压缩包]
- **最终运行时间**：2026-10-19 22:31 左右（北京时间）
- **最终运行目录**：`artifacts/run-20261019T143129Z`

## 任务描述

排查线上依赖是否异常时，经常需要反复打开多个状态页。本作品把这些分散步骤整理成一次可复现的网页任务：

1. 用 `targets.json` 维护公开状态页清单；
2. 用 Lexmount Web Fetch API 抓取并提取页面内容；
3. 保守识别正常、疑似异常、维护和未知；
4. 汇总为 Markdown / CSV / JSONL 简报；
5. 保留 `request_id`、`dom_id`、原始响应和 SHA-256 清单，便于核验。

## Lexmount 云平台的使用

- **使用能力**：Lexmount Web Fetch API。
- **接口**：`POST /v1/extract`
- **入口**：`https://api.lexmount.cn/v1/extract`
- **鉴权方式**：请求头携带 `X-API-Key` 与 `X-Project-Id`。
- **最终运行调用数**：6 个目标，6 次成功返回，0 次失败。
- **最终运行 Trace**：关闭。
- **目标页面**：
  - GitHub Status
  - Cloudflare Status
  - Vercel Status
  - OpenAI Status
  - Stripe Status
  - Supabase Status
- **留证字段**：
  - `request_id`
  - `result.final_url`
  - `result.status_code`
  - `result.title`
  - `result.main_text`
  - `result.engine`
  - `dom_id`

## 成果

- **人工可读简报**：`artifacts/run-20261019T143129Z/report.md`
- **结构化摘要**：`artifacts/run-20261019T143129Z/summary.csv`、`summary.jsonl`
- **调用索引**：`artifacts/run-20261019T143129Z/run_manifest.json`
- **原始响应**：`artifacts/run-20261019T143129Z/raw/*.json`
- **完整性清单**：`artifacts/run-20261019T143129Z/SHA256SUMS.txt`
- **可运行代码**：`lexfetch.py`

## 运行方式

```powershell
# 不调用 API，只检查配置和目标清单
python .\lexfetch.py --dry-run

# 真实调用 Lexmount Web Fetch
python .\lexfetch.py
```

运行前需在本地 `.env` 配置：

```env
LEXMOUNT_API_KEY=your-api-key
LEXMOUNT_PROJECT_ID=your-project-id
LEXMOUNT_BASE_URL=https://api.lexmount.cn
```

公开材料不包含 `.env`，也不包含 API Key 和 Project ID。

## 结果摘要

| 服务 | 判定 | 目标状态码 | 引擎 |
|---|---|---:|---|
| GitHub | `operational` | 200 | `lightmount_lite` |
| Cloudflare | `possible_issue` | 200 | `lightmount_dcl` |
| Vercel | `operational` | 200 | `lightmount_dcl` |
| OpenAI | `operational` | 200 | `lightmount_lite` |
| Stripe | `unknown` | 200 | `lightmount_dcl` |
| Supabase | `operational` | 200 | `lightmount_dcl` |

统计：

- 成功抓取：6 / 6；
- 正常：4；
- 疑似异常：1，Cloudflare 页面显示活跃的 WARP 地理位置错误事件；
- 未知：1，Stripe 页面在该次抓取中只返回 `Loading...`；
- API 调用失败：0。

## 为什么可信

1. 每条状态都有目标 URL，可回到服务商页面复核；
2. 每次调用都有 Lexmount `request_id`；
3. `run_manifest.json` 记录 raw 文件、`dom_id` 和调用索引；
4. `SHA256SUMS.txt` 可证明提交材料与当次运行一致；
5. 脚本使用保守关键词判定，内容不足时标记为 `unknown`，不伪造结论；
6. 状态页明确显示 operational 时，优先采用该横幅，而不是被历史事件干扰。

## 边界与说明

- 工具不是官方可用性结论，只是巡检辅助；
- 当前基于通用正文提取和保守关键词匹配；
- 对强 JavaScript 渲染页面可能拿到 `Loading...`，此时标记为 unknown；
- 状态页文案变化可能影响识别；
- 若某个目标抓取失败，会保留错误并标记为 unknown；
- 不处理需要登录、内网或付费合同才能访问的状态。

## 后续改进

- 为 Stripe 等页面增加浏览器引擎或站点专用解析器；
- 增加定时巡检和历史 diff；
- 对活跃事件和历史事件做时间窗口区分；
- 增加静态页面输出。

## 独立性与原创说明

本作品为本次活动期间创建的新实践。作品选择、目标清单设计、判定规则、脚本和报告结构均为本次新增；未复用其他比赛获奖作品。

## 授权确认

[待填：提交时如页面要求确认官网展示授权，请保留截图或说明。]

## 核验联系人

- 作者：[待填]
- 邮箱：[待填]
- 可核验时间：[待填]

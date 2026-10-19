# 参赛方案：多站点巡检与服务状态简报

## 一、选题

**作品名称**：Lexmount Status Watch  
**选题类型**：多站点巡检助手 / 开发服务状态简报  
**目标**：把分散的服务状态页巡检过程变成一次可复现的网页任务，并保留来源、API 响应与文件完整性清单。

## 二、为什么适合比赛

活动要求作品必须实际使用 Lexmount 云平台完成任务。本方案每轮都会调用 Lexmount Web Fetch API：

- `POST https://api.lexmount.cn/v1/extract`
- 请求头带 `X-API-Key` 和 `X-Project-Id`
- 每个目标站点返回 `request_id`、`final_url`、`title`、`main_text`、`engine`、`dom_id`

这些字段天然适合作为「可核验过程」。

## 三、任务流程

1. **定义目标**
   - `targets.json` 维护服务名、显示名称和公开状态页 URL。
2. **调用 Lexmount**
   - `lexfetch.py` 逐个请求 Lexmount Web Fetch。
   - 保存每次 API 响应为 raw JSON。
3. **生成摘要**
   - 从 `title`、`description`、`main_text` 中保守识别 operational / issue / maintenance。
4. **生成成果**
   - `report.md`：人工可读简报；
   - `summary.csv` / `summary.jsonl`：结构化结果；
   - `run_manifest.json`：请求与响应索引；
   - `SHA256SUMS.txt`：文件完整性清单。
5. **人工复核**
   - 表格中每条结论都可回到来源 URL 和 raw JSON 核验。

## 四、成果形态

提交时可附上：

- 可运行代码；
- 至少一次真实运行生成的 `report.md`；
- `run_manifest.json`；
- 若干个脱敏后的 `raw/*.json`；
- `SHA256SUMS.txt`；
- 运行命令与复现说明。

## 五、时间安排

| 时间 | 工作 |
|---|---|
| Day 1 | 确定选题、整理目标站点、完成脚本 |
| Day 2 | 用 Lexmount API 实际运行至少一轮 |
| Day 3 | 人工检查误判、补充 `SUBMISSION.md` |
| Day 4 | 整理公开仓库 / 压缩包、材料链接和提交表单内容 |
| 截止前 | 检查作品描述、作者、成果链接、核验说明 |

## 六、评委核验要点

- 是否真的使用了 Lexmount 云平台？
  - raw JSON 中应有 Lexmount `request_id`、`engine`、`dom_id` 等字段。
- 是否完成了网页任务？
  - 多个状态页被读取并汇总为简报。
- 结果是否可复核？
  - 每条状态都有来源 URL 和 raw JSON；
  - manifest 记录文件索引；
  - SHA-256 保证提交材料一致。
- 是否有独立价值？
  - 不只是截图，而是可复用的小工具和结构化结果。

## 七、风险与应对

| 风险 | 应对 |
|---|---|
| 状态页改版导致正文摘要不稳定 | 只做保守判定，必要时补充站点专用解析器 |
| 某站点反爬或 Lexmount 抓取失败 | 保留失败响应与错误码；失败站点标记为 `unknown`，不伪造结论 |
| Free 额度不足 | 先用 5-8 个高价值站点；不要反复试跑；必要时减少 trace |
| raw 响应太大 | 不请求 `raw_dom`；只保存 `/v1/extract` 默认结构化结果 |
| 隐私风险 | 不提交 `.env`；公开前检查 raw JSON |

## 八、最小可行版本

只要完成下面四点，就已经能构成一个合格的小实践：

1. 至少 5 个公开服务状态页；
2. 每个页面一次真实 Lexmount Web Fetch 调用；
3. 一份 Markdown 简报；
4. 一份包含 request/dom ID 和 raw 文件索引的 manifest。

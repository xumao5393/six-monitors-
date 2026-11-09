# 十七个监测器 · Seventeen Monitors

十七个开箱即用的静态监测页面：A股+港股、头部 AI 与 Agent、开源 AI、X、义乌小商品、国内 AI 与 Agent，再加 11 个新监测：AI 工具降价、AI 新品上线、AI 副业拆解、跨境爆款、1688/拼多多价格趋势、节日选品日历、热搜热榜聚合、GitHub Trending 日榜、AI 产品热度日榜、AI 大事件、搜索趋势。

全部是**纯静态 HTML**，不需要后端、不需要数据库、不需要账号密码。
打开 `monitors/` 里的任意一个文件（或用任意静态服务器托管），点右上角**刷新**即可拉取最新公开数据——05 义乌页除外，它的按钮是「载入样本」，只重绘已标注的缓存样本，不拉取实时数据；09、10、11、16 页为人工策展/人工录入，按钮同样只载入样本，不拉取实时数据；11 页另有自行录入表单（品名、拿货价、零售价 → 自动算毛利，存本机浏览器）。

> ⚠️ 免责声明：本项目只展示公开数据，不构成投资建议。股票、基金、AI 模型价格与额度以官方公布为准。

> 设计说明（2026-11-09 改版）：每个监测器有独立配色与渐变背景、彩色 KPI 卡、hero「今日看点」栏；图表类型各不相同（折线、散点、彩色条形等）。Chart.js 已随仓库内置（`monitors/chart.umd.min.js`），离线打开也能画图，CDN 仅作替补。

## 总览入口

- `index.html`（仓库根）与 `monitors/index.html`：17 张卡片，每张链到对应监测页，并标明 **实时 / 样本 / 人工**：实时 = 打开即拉公开接口（失败显示未获取或切缓存并标注）；样本 = 缓存样本 / 人工整理值，非实时；人工 = 人工策展 / 人工录入，无实时源，过期会标明。
- 全站响应式：每页含同一段 `@media (max-width:720px)`（header 收窄、h1 18px、KPI 2 列、feed 1 列、卡片横向滚动、表格块级滚动、canvas 200px、header 按钮全宽）。
- 加载态 / 空状态：`refreshAll` 开头设 `aria-busy` + 「正在拉取…」占位；空表统一一行「未获取 / 无匹配」，不编数。
- Chart.js 随仓库内置（`monitors/chart.umd.min.js`），各页用同目录相对路径 `./chart.umd.min.js` 引用，须从 `monitors/` 内打开各页；总览页只链 `monitors/*.html`。

## Actions 快照流水线（.github/workflows/snapshot.yml）

- 已搭建：`.github/workflows/snapshot.yml`（cron `0 */6 * * *`，可手动触发），由 `.github/scripts/snapshot.py` 在 runner 上 curl 各源，写 `monitors/data/*.json` 后 commit；失败时保留上次成功内容并写 `fetched_at` + `ok:false`，不编数。
- 现有快照（2026-11-09 15:54 CST 生成，`ok:true`）：`hot.json`（13 热搜：微博国际版 + 抖音）、`ph.json`（15 Product Hunt RSS）、`trends.json`（17 Google Trends 新版 RSS）、`prices.json`（07 价格：OpenRouter + models.dev 全量）、`oss.json`（03 开源：24 仓 GitHub Core API）。
- 另有 `monitors/data/yiwu-hotwords.json`（05 与 10 共用的义乌购热词，2026-11-09 调研核实值，手工维护，非 Actions 产物）。

## 监测器一览

| # | 文件 | 监测什么 | 主要数据源 |
|---|------|----------|-----------|
| 01 | `monitors/01-a-share-hk.html` | A股+港股：上证、深证成指、创业板、恒生、恒生科技，涨跌家数、板块、AH 溢价 | 腾讯行情（主，逐个代码解析）→ 缓存样本（标注，2026-11-09 14:48 盘中快照）；自选现拉 `qt.gtimg.cn/q=<代码>`（f[1]/f[3]/f[32]，失败显示未获取，6 字头自动补 sh、0/3 字头补 sz）；涨跌家数 / 分时 / AH 溢价标「缓存样本·非实时」；指数部分失败时 badge 为「腾讯实时 + 部分缓存补齐」；新浪行情已移除：直连 403 且无 CORS 头，浏览器不可用 |
| 02 | `monitors/02-top-ai-agents.html` | 头部 AI 模型与 Agent：GPT、Claude、Gemini、Grok、DeepSeek、Qwen、Kimi 等，价格、速度、上下文 | OpenRouter（主，公开目录，无分数）→ 缓存样本（标注）；实时模式画价格条形图（分数不混画），缓存模式才画分数散点（分数=缓存 AA v5）；API 名称经 esc() 转义；「今日变化」KPI 已删；表头排序带 ▲/▼；Agent 对比表标「人工整理·非API」 |
| 03 | `monitors/03-open-source-ai.html` | 开源 AI 项目：周增 Star 第一指标，白名单仓库，分类筛选 | Actions 快照 `monitors/data/oss.json`（主，GitHub Actions 每 6 小时逐仓拉 24 个白名单仓库，history 连续 ≥7 天后给出全站统一 Δ Star）→ 浏览器直连 GitHub Core API 逐仓（替补）→ 缓存样本（标注，2026-11-09 核实）；本机 localStorage 快照差分只作补充；GitHub Search topic:llm 仅在底部「发现」区块，不进主表和 KPI |
| 04 | `monitors/04-x-monitor.html` | X 账号只读监测：粉丝、帖子、互动（输入任意公开账号，不预设任何账号） | FxTwitter `/2/profile/{账号}`（主，用户资料）；VxTwitter 替补已失效：2026-11-09 实测 403 Cloudflare，代码已下线，不再尝试；帖子时间线只走 FxTwitter `/2/profile/{账号}/statuses`；trends24 仅外链（只有 HTML 页面且无 CORS 头，浏览器读不到，不当 API） |
| 05 | `monitors/05-yiwu-small-goods.html` | 义乌小商品：义乌指数、义乌购热词榜、国内外爆款、季节日历 | 义乌购 / 义乌指数官网（无公开 JSON 接口，不可直拉）→ 缓存样本（明确标注，景气指数为 2026年9月样本）；景气分项柱状图已删除（分项数无出处，只有总指数 1554.97 有来源）；热词与 10 共用 `monitors/data/yiwu-hotwords.json`；样本超过 14 天标「已过期」 |
| 06 | `monitors/06-domestic-ai-agents.html` | 国内 AI 与 Agent：豆包、千问、DeepSeek、混元、智谱、Kimi、文心、MiniMax、阶跃等 | OpenRouter（主，公开目录，旗舰白名单 + id 前缀→厂商映射，无分数）→ 缓存样本（标注）；实时模式画价格条形图，缓存模式才画分数散点；榜首 KPI 改为「最便宜国产」（实时价最低者）与「最长上下文」，永不显示「未获取」榜首；Agent 数=5 / 视频模型=6 已移出 KPI，放在「人工整理」区块；API 名称经 esc() 转义；表头排序带 ▲/▼；Agent 对比表标「人工整理·非API」 |
| 07 | `monitors/07-ai-price-drop.html` | AI 工具降价/额度变动：各模型输入/输出价，快照差分标涨跌 | OpenRouter（主）→ models.dev api.json（替补，仅官方渠道价）→ 缓存快照（标注，2026-11-09）；快照差分已实现：按北京时间日期在 localStorage 存每日快照（键 `mon07_price_YYYY-MM-DD`），与最近一份非今日快照比算涨跌（涨价 / 降价 / 基线积累中），无上一份快照时涨/降筛选禁用；models.dev Anthropic id 已按实测改为 `claude-opus-5-5`（连字符）；备注按 id 合并，不按显示名；Actions 另产 `monitors/data/prices.json` 全量价快照 |
| 08 | `monitors/08-ai-new-launches.html` | AI 新品/新功能上线：新模型、新功能、发布时间、卖点 | OpenRouter/models.dev 新增条目 diff（主）→ 厂商博客 RSS → 人工策展缓存（标注，2026-11-09）；类型筛选已删「新功能」option（无该类型策展条目）；Google Blog RSS（blog.google/rss）浏览器可直读（实测 200，CORS 反射 Origin，本页实时拉取最新 5 条）；Anthropic /news/rss.xml 实测 404（改抓 /news HTML 需 Actions）；OpenAI /news/rss.xml 浏览器无 CORS，只能经 Actions 存 JSON 后读；diff 新增列表最多展示 20 条，超出部分折叠展开 |
| 09 | `monitors/09-ai-side-hustle.html` | AI 副业玩法真假拆解：声称收入、可信度评级（可复制/有水分/割韭菜） | 人工策展，非实时抓取；X 搜索整理 + 小红书人工收集互为对照，无实时源；样本超过 30 天标「需重新策展」 |
| 10 | `monitors/10-cross-border-hot.html` | 跨境爆款：人工周更精选 + 趋势信号 | 人工精选 / 缓存样本（标注，2026-11-09）；无稳定免费实时榜单源，不假装实时；热词与 05 共用 `monitors/data/yiwu-hotwords.json`；世界杯信号 KPI（体育用品出口 Q1 28.3 亿元、同比 +12%）有来源脚注（与 05 同一批调研样本值，非海关实时统计）；「数据源状态」改为 <details> 折叠；样本超过 14 天标「已过期」 |
| 11 | `monitors/11-1688-pdd-price.html` | 1688/拼多多价格趋势：拿货价 vs 零售价、毛利差对照表 | 人工录入 + 日期（2026-11-09）；无免费公开接口，不假装实时；可自行录入：表单填品名、拿货价、零售价 → 自动算毛利差（零售 − 拿货），存本机浏览器 localStorage，可删除；条形图改为横向（indexAxis 'y'），长中文标签不再挤压；毛利未扣运费、平台费、退货损耗（红字标注） |
| 12 | `monitors/12-festival-calendar.html` | 节日/季节选品日历：节点、倒计时、该囤品类、配套选题 | 内置静态 JSON（主）→ 历法规则推算备用表（替补，逐条核验）；零依赖；日期一律按 `+08:00` 解析（海外时区倒计时不再差半天）；移动端时间轴改为垂直时间线（.dot/.lbl 不重叠）；七夕已按香港天文台核对（8 月 8 日），无「待复核」标记 |
| 13 | `monitors/13-hot-search.html` | 热搜热榜聚合：微博、抖音、知乎、B 站 Top 榜 | Actions 快照 `monitors/data/hot.json`（主，GitHub Actions 每 6 小时在 runner 上 curl 微博国际版 + 抖音热搜，浏览器直连因 CORS 必然失败，改读同域快照）→ 嵌入式缓存（2026-11-09 15:15 CST curl 实测，超过 12 小时标「已过期」）；Hero 由快照 Top 1 生成，不再写死旧热点；知乎 curl 亦 401，固定「未获取 + 手动链接」；源状态分「curl（服务端）/ 浏览器」两列 |
| 14 | `monitors/14-github-trending.html` | GitHub Trending 日榜：今日新增 Star 最多的开源项目 | GitHub Search API（主，浏览器直连）→ Trending 官方页快照（替补，需 Actions 回填）→ 缓存样本（标注，2026-11-09）；查询窗口为动态近 7 日（`created:>` + 当天 −7 天，不再写死 2026-11-02）；标题为「新建仓库 Star 榜（近 7 日）」，非官方 Trending |
| 15 | `monitors/15-product-hunt.html` | AI 产品热度日榜：Product Hunt 上正在爆红的 AI 产品 | Actions 快照 `monitors/data/ph.json`（主，服务端 curl Product Hunt RSS 存 JSON）→ RSS 直连 + DOMParser 解析（备份，只有解析出条目并渲染才标 live，否则一律「样本+策展」）→ 人工策展样本（标注，2026-11-09）；票数 RSS 不提供，一律「未获取」，不编数；allorigins 已下线（实测超时/500） |
| 16 | `monitors/16-ai-events.html` | AI 大事件/监管动态：封禁、调价、宕机、监管新规 | 人工策展，非实时抓取（2026-11-09）；每条事件双源核实；页头按策展日期算样本年龄，超过 7 天标「已过期·需重策展」；有「载入样本」按钮（与 09 一致）；Actions 快照尚未搭建（status 页与 RSS 需 Actions 抓取存 JSON，本页目前无此层，已明示） |
| 17 | `monitors/17-search-trends.html` | 搜索趋势：关键词 7/30 天涨跌、相关上升词 | Actions 快照 `monitors/data/trends.json`（主，新版 `trends.google.com/trending/rss?geo=US/HK/TW`，旧版 daily RSS 已 404，geo=CN 返回 400 不用）→ trends.google.com 手动打开（替补）→ 人工判断样本表（标注，定性方向，无编造数值）；百度指数无备份源 |

## 备份硬规则（新增 11 个监测同样适用）

每个数据源都必须有备份：主源 → 替补源 → 缓存，三层标注来源与时间，过期标「已过期」。没有备份的源，页面上明确写「无备份」或「无可用备份源」，绝不假装有备用。

## 冗余规则（本项目最重要的一条）

每个数据源都必须有替补：

1. 主源失败 → 自动切换替补源；
2. 替补也失败 → 显示上次缓存数据，并标明 **「上次数据 / 已过期」**；
3. 没有数据时显示 **「未获取」**，绝不编造数字；
4. 每个模块都标明当前来源（主源 / 替补源 / 缓存）和数据时间。

港股免费行情约延迟 15 分钟，页面上已写明，不冒充实时。
北向资金净买额因港交所不再披露实时买卖金额，只报成交额，不编净买额。

## 本地运行

```bash
# 任选其一
python3 -m http.server 8000
# 或
npx serve .
```

然后打开 http://localhost:8000/monitors/01-a-share-hk.html

直接双击 HTML 文件也能打开，但部分公开接口会因 CORS 拒绝 `file://` 请求，
此时页面会如实显示「未获取 / 缓存」，建议用上面的本地服务器方式运行。

## 数据缺口（诚实说明）

- **01 股票**：腾讯行情是唯一真正解析的主源（逐个代码 `v_sh000001` 等精确匹配）；自选现拉 `qt.gtimg.cn/q=<代码>`（f[1]=名称、f[3]=现价、f[32]=涨跌幅%，失败显示未获取）。新浪行情已从代码中移除——实测直连 403 且无 CORS 头，不能当实时替补。腾讯失败即走标注缓存（2026-11-09 14:48 盘中快照），不冒充实时。涨跌家数（725/4483/87）无实时来源，仅作缓存样本标注；分时图 7 个点为缓存示例走势，非实时；三块标题均带「缓存样本·非实时」徽章。
- **02 / 06 AI 模型**：代码里根本没有 model-watch，不要再把它当来源；models.dev `/api/v1/models` 返回 302 已死，但 `models.dev/api.json` 仍活（200，07/08 在用），两者不要混为一谈。实际唯一能通的公开目录是 OpenRouter，且它不给分数——分数列只有缓存样本里才有，实时模式改画价格条形图。缓存样本明确标注；API 返回的模型名经 esc() 转义后才进 innerHTML。
- **03 开源**：主源是 Actions 快照 `monitors/data/oss.json`（GitHub Actions 每 6 小时逐仓拉取 24 个白名单仓库，history 连续 ≥7 天后给出全站统一 Δ Star；第 1 天只有基线，显示「积累中」），替补为浏览器直连 GitHub Core API 逐仓（topic 搜索已弃用，噪声太大），GitHub Search API 仅作底部「发现」。周增 Star（Δ Star）已实现：本机 localStorage 存每日快照，Δ = 当前 − ≥6 天前快照，不足则标明快照天数；第 1 天只有基线，显示「积累中」。未登录 Core API 每小时限 60 次，一次加载 24 次调用，约 2 次满载后会被 403 截断（已优雅处理，保留已加载部分）。缓存样本为 2026-11-09 核实值并标注。
- **04 X**：trends24 不是可用来源——它只有 HTML 页面且不带 CORS 头，浏览器读不到，代码也不解析，只给链接让人手动打开；本页没有自动化的热搜来源。用户资料只走 FxTwitter `/2/profile/{账号}`；VxTwitter 替补已失效（2026-11-09 实测 403 Cloudflare），代码已下线。帖子时间线只有 FxTwitter `/2/profile/{账号}/statuses`。帖子表不展示单帖浏览量。只读，不登录、不发帖、不关注。
- **05 义乌**：义乌购 / 义乌指数官网无公开 JSON 接口，浏览器直接拉取常被拦截；页面用调研核实过的样本作缓存并明确标注「缓存样本」，景气指数 1554.97（+0.55%）明确标注为 **2026年9月样本**，不得当作当前值；景气分项柱状图已删除（分项数无出处）；热词与 10 共用 `monitors/data/yiwu-hotwords.json`；样本超过 14 天标「已过期」。按钮是「载入样本」不是刷新。1688 生意参谋完整数据需商家账号，本项目只呈现公开方法，不伪造后台数据。
- **07 降价**：OpenRouter 与 models.dev api.json 均实测 200 可用（2026-11-09）；models.dev 价格是分渠道价，替补只用官方渠道条目，Qwen/GLM/Seed 在替补模式下显示未获取。涨跌对比靠快照差分：按北京时间日期在 localStorage 存每日快照（`mon07_price_YYYY-MM-DD`），与最近一份非今日快照比算涨跌；首次快照只是基线，需第二次快照才有真涨跌，无上一份快照时涨/降筛选禁用。Anthropic 替补 id 为 `claude-opus-5-5`（连字符，实测存在）。订阅价/免费额度无稳定免费源，一律显示未获取。Actions 另产 `monitors/data/prices.json` 全量价快照。
- **08 新品**：OpenRouter/models.dev 新增条目 diff 可用；Google Blog RSS（blog.google/rss）浏览器可直读（实测 200，CORS 反射 Origin）；Anthropic /news/rss.xml 实测 404（改抓 /news HTML 需 Actions），OpenAI /news/rss.xml 浏览器无 CORS（只能经 Actions 存 JSON 后读）。类型筛选无「新功能」option（无该类型策展条目）。diff 新增列表最多展示 20 条，超出折叠。今日新品数为 0 是如实值，不是缺失。
- **09 副业**：纯人工策展，无实时源；评级是判断不是审计，样本超过 30 天标「需重新策展」。声称收入均为原帖宣称，未验证。
- **10 跨境**：无稳定免费实时榜单源；样本 14 天后标已过期，需重新策展。热词与 05 共用 `monitors/data/yiwu-hotwords.json`。世界杯信号 KPI（体育用品出口 Q1 28.3 亿元、同比 +12%）有来源脚注（与 05 同一批调研样本值，非海关实时统计）。「数据源状态」改为 <details> 折叠。Amazon/Temu/TikTok Shop 实时销量无主源、无备份，本页不提供。
- **11 价格**：样本区间为示例对照，非实测报价；毛利差不含运费、平台费、退货（红字标注）。可自行录入：表单填品名、拿货价、零售价 → 自动算毛利差，存本机浏览器 localStorage，可删除。无免费公开接口，无实时备份。
- **12 日历**：节日日期为固定历法知识，2027 春节 2027-02-06 等已多源核实；七夕已按香港天文台核对（2027-08-08），无「待复核」标记；开学季为惯例窗口、2027 放假调休天数未公布故不写。日期一律按 `+08:00` 解析；移动端时间轴为垂直时间线。
- **13 热榜**：主源为 Actions 快照 `monitors/data/hot.json`（GitHub Actions 每 6 小时在 runner 上 curl 微博国际版 + 抖音热搜；浏览器直连因 CORS 必然失败，改读同域快照）。Hero 由快照 Top 1 生成，不再写死旧热点；缓存超过 12 小时标「已过期」。知乎 curl 亦 401，固定「未获取 + 手动链接」。
- **14 Trending**：GitHub Search API 带 CORS `*`，https 下应可直连；查询窗口为动态近 7 日；Trending 原站 HTML 快照需 Actions 回填，尚未建。Search API 不给单日新增 Star，图表标明为总 Star，非日增。
- **15 Product Hunt**：主源为 Actions 快照 `monitors/data/ph.json`（服务端 curl RSS 存 JSON）；备份为 RSS 直连 + DOMParser 解析，只有解析出条目并渲染才标 live，否则一律「样本+策展」；票数 RSS 不提供，一律「未获取」，不编数；allorigins 已下线（实测超时/500）。
- **16 大事件**：人工策展快照，页头按策展日期算样本年龄，超过 7 天标「已过期·需重策展」；有「载入样本」按钮（与 09 一致）；Actions 快照未建，无自动刷新路径。
- **17 搜索趋势**：主源为 Actions 快照 `monitors/data/trends.json`（新版 `trending/rss?geo=US/HK/TW`；旧版 daily RSS 已 404，geo=CN 返回 400 不用）；趋势图为示意指数（人工设定，非实测），页内三处警告勿当数值引用；百度指数无备份源，页内无百度数据。

## 隐私

本项目不包含任何私人信息：没有密码、邮箱、电话、账号、订单号。
X 监测不预设任何账号，使用者自行输入公开账号。

## 许可

MIT License，见 [LICENSE](LICENSE)。

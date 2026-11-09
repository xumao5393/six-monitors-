# Seventeen Monitors · 十七个监测器

Seventeen ready-to-use static monitoring pages: A-shares + Hong Kong stocks, top AI & Agents, open-source AI, X, Yiwu small commodities, domestic AI & Agents — plus 11 more: AI tool price drops, AI new launches, AI side-hustle teardowns, cross-border hot products, 1688 / Pinduoduo price trends, a festival product calendar, a hot-search aggregator, GitHub Trending daily, Product Hunt daily buzz, AI big events, and search trends.

十七个开箱即用的静态监测页面：A股+港股、头部 AI 与 Agent、开源 AI、X、义乌小商品、国内 AI 与 Agent，再加 11 个新监测：AI 工具降价、AI 新品上线、AI 副业拆解、跨境爆款、1688/拼多多价格趋势、节日选品日历、热搜热榜聚合、GitHub Trending 日榜、AI 产品热度日榜、AI 大事件、搜索趋势。

All pages are **pure static HTML** — no backend, no database, no account or password needed. Open any file under `monitors/` (or serve the folder with any static server) and click **Refresh** (top right) to pull the latest public data — except 05 Yiwu, whose button is “Load sample” and only redraws the labelled cached sample without fetching live data; pages 09, 10, 11 and 16 are hand-curated / hand-entered, so their buttons also only load samples; page 11 additionally has a manual-entry form (product name, wholesale price, retail price → auto gross margin, stored in the browser).

全部是**纯静态 HTML**，不需要后端、不需要数据库、不需要账号密码。
打开 `monitors/` 里的任意一个文件（或用任意静态服务器托管），点右上角**刷新**即可拉取最新公开数据——05 义乌页除外，它的按钮是「载入样本」，只重绘已标注的缓存样本，不拉取实时数据；09、10、11、16 页为人工策展/人工录入，按钮同样只载入样本，不拉取实时数据；11 页另有自行录入表单（品名、拿货价、零售价 → 自动算毛利，存本机浏览器）。

> ⚠️ Disclaimer: this project only shows public data and is not investment advice. Stock, fund, AI model price and quota figures follow official announcements.
> 免责声明：本项目只展示公开数据，不构成投资建议。股票、基金、AI 模型价格与额度以官方公布为准。

> Design (2026-11-09 redesign): each monitor has its own colour scheme and gradient background, coloured KPI cards, and a hero “today’s takeaway” bar; chart types differ per page (line, scatter, coloured bars, …). Chart.js is bundled with the repo (`monitors/chart.umd.min.js`), so charts draw offline; the CDN is only a fallback.
> 设计说明（2026-11-09 改版）：每个监测器有独立配色与渐变背景、彩色 KPI 卡、hero「今日看点」栏；图表类型各不相同（折线、散点、彩色条形等）。Chart.js 已随仓库内置（`monitors/chart.umd.min.js`），离线打开也能画图，CDN 仅作替补。

## Language · 语言

**12 of the 17 monitors are bilingual (Chinese + English)** — marked 🌐 Bilingual on the overview page. Each bilingual page has a prominent toggle button in its header showing the language you would switch to (**🌐 EN** in Chinese mode, **🌐 中文** in English mode): `?lang=en` (or `?lang=zh`) in the URL wins, otherwise the choice saved in `localStorage` (`mon-lang`), default Chinese. All UI chrome is translated (titles, hero, KPI labels, table headers, buttons, badges, footnotes, empty/error states, expiry and sample labels); data values themselves (model names, prices, numbers, dates) stay as-is, and only the surrounding labels are translated. Content that would be useless untranslated (festival names, hotwords, trend keywords, event titles, curated pitches, repo descriptions) is translated too.

**17 个监测器中有 12 个是中英双语**——总览页标为 🌐 Bilingual。每个双语页页眉都有醒目的切换按钮，只显示将要切换到的语言（中文模式下显示 **🌐 EN**，英文模式下显示 **🌐 中文**）：URL 参数 `?lang=en`（或 `?lang=zh`）优先，其次是 `localStorage` 里存的选择（`mon-lang`），默认中文。所有界面文字都翻译（标题、hero、KPI 标签、表头、按钮、徽章、脚注、空态/报错、过期与样本标注）；数据值本身（模型名、价格、数字、日期）保持原样，只翻译周围的标签。离开翻译就没法用的内容（节日名、热词、趋势关键词、事件标题、策展文案、仓库简介）也一并翻译。

**The other 5 monitors are Chinese-only** (marked “Chinese only” on the overview page): 01 A-shares + Hong Kong stocks, 06 domestic AI & Agents, 09 AI side-hustle plays, 11 1688 / Pinduoduo price trends, 13 hot-search aggregator. Their subjects are China-market specific, so the pages stay in Chinese; the overview page still gives each an English title and description.

**其余 5 个监测器仅中文**（总览页标为“Chinese only”）：01 A股+港股、06 国内AI与Agent、09 AI副业玩法、11 1688/拼多多价格趋势、13 热搜热榜聚合。这些主题面向中国市场，页面保持中文；总览页仍为每张卡片提供英文标题与简介。

## Overview · 总览入口

- `index.html` (repo root) and `monitors/index.html`: 17 cards, each linking to its monitor page and labelled **Live / Sample / Curated** — Live = fetches a public API on open (shows “Not available” or falls back to labelled cache on failure); Sample = cached sample / hand-compiled value, not live; Curated = hand-curated / hand-entered, no live source, expiry is labelled. Each card also carries a language badge: 🌐 Bilingual or Chinese only.
- `index.html`（仓库根）与 `monitors/index.html`：17 张卡片，每张链到对应监测页，并标明 **实时 / 样本 / 人工**：实时 = 打开即拉公开接口（失败显示未获取或切缓存并标注）；样本 = 缓存样本 / 人工整理值，非实时；人工 = 人工策展 / 人工录入，无实时源，过期会标明。每张卡片另有语言徽章：🌐 中英双语 或 仅中文。
- Fully responsive: every page includes the same `@media (max-width:720px)` block (narrower header, 18px h1, 2-column KPIs, 1-column feed, horizontally scrolling cards, block-scrolling tables, 200px canvas, full-width header buttons).
- 全站响应式：每页含同一段 `@media (max-width:720px)`（header 收窄、h1 18px、KPI 2 列、feed 1 列、卡片横向滚动、表格块级滚动、canvas 200px、header 按钮全宽）。
- Loading / empty states: `refreshAll` sets `aria-busy` plus a “Loading…” placeholder at the start; empty tables show a single “Not available / No matches” row — never invented numbers.
- 加载态 / 空状态：`refreshAll` 开头设 `aria-busy` + 「正在拉取…」占位；空表统一一行「未获取 / 无匹配」，不编数。
- Chart.js is bundled with the repo (`monitors/chart.umd.min.js`); each page references it by the relative path `./chart.umd.min.js` from inside `monitors/`; the overview pages only link to `monitors/*.html`.
- Chart.js 随仓库内置（`monitors/chart.umd.min.js`），各页用同目录相对路径 `./chart.umd.min.js` 引用，须从 `monitors/` 内打开各页；总览页只链 `monitors/*.html`。

## Actions snapshot pipeline · Actions 快照流水线（.github/workflows/snapshot.yml）

- Built: `.github/workflows/snapshot.yml` (cron `0 */6 * * *`, manually triggerable). `.github/scripts/snapshot.py` curls each source on the runner, writes `monitors/data/*.json`, then commits; on failure it keeps the last good content and writes `fetched_at` + `ok:false` — never invents numbers.
- 已搭建：`.github/workflows/snapshot.yml`（cron `0 */6 * * *`，可手动触发），由 `.github/scripts/snapshot.py` 在 runner 上 curl 各源，写 `monitors/data/*.json` 后 commit；失败时保留上次成功内容并写 `fetched_at` + `ok:false`，不编数。
- Current snapshots (generated 2026-11-09 15:54 CST, `ok:true`): `hot.json` (13 hot search: Weibo international + Douyin), `ph.json` (15 Product Hunt RSS), `trends.json` (17 Google Trends new RSS), `prices.json` (07 prices: OpenRouter + models.dev full list), `oss.json` (03 open source: 24 repos via GitHub Core API).
- 现有快照（2026-11-09 15:54 CST 生成，`ok:true`）：`hot.json`（13 热搜：微博国际版 + 抖音）、`ph.json`（15 Product Hunt RSS）、`trends.json`（17 Google Trends 新版 RSS）、`prices.json`（07 价格：OpenRouter + models.dev 全量）、`oss.json`（03 开源：24 仓 GitHub Core API）。
- Also `monitors/data/yiwu-hotwords.json` (Yiwu hotwords shared by 05 and 10, verified by research on 2026-11-09, hand-maintained, not an Actions product).
- 另有 `monitors/data/yiwu-hotwords.json`（05 与 10 共用的义乌购热词，2026-11-09 调研核实值，手工维护，非 Actions 产物）。

## Monitors · 监测器一览

| # | Monitor 监测器 | Language 语言 | File 文件 | Main data sources 主要数据源 |
|---|---|---|---|---|
| 01 | A-Shares + Hong Kong Stocks · A股+港股监测 | 仅中文 · Chinese only | `monitors/01-a-share-hk.html` | Tencent quotes live (five major indices, per-code parsing) → labelled cached sample (2026-11-09 14:48 intraday snapshot); watchlist pulls `qt.gtimg.cn/q=<code>` live; advancers/decliners, intraday and AH premium are cached samples, not live; Sina quotes removed (direct 403, no CORS headers) |
| 02 | Top AI & Agent Monitor · 头部AI与Agent监测 | 🌐 Bilingual · 中英双语 | `monitors/02-top-ai-agents.html` | OpenRouter (primary, public catalog, no scores) → labelled cached sample; live mode draws a price bar chart (scores never mixed in), cached mode draws the score scatter (scores = cached AA v5); model names escaped via esc(); “today’s change” KPI removed; sortable headers ▲/▼; agent table marked “hand-compiled · not an API” |
| 03 | Open-Source AI Monitor · 开源AI监测 | 🌐 Bilingual · 中英双语 | `monitors/03-open-source-ai.html` | Actions snapshot `monitors/data/oss.json` (primary: GitHub Actions pulls 24 allow-listed repos every 6 h; full-site unified Δ Star once history is ≥7 days) → browser-direct GitHub Core API per repo (backup) → labelled cached sample (verified 2026-11-09); local localStorage snapshot diffs are supplementary only; GitHub Search topic:llm appears only in the bottom “Discover” section, not in the main table or KPIs |
| 04 | X Accounts (read-only) · X账号只读监测 | 🌐 Bilingual · 中英双语 | `monitors/04-x-monitor.html` | FxTwitter `/{handle}` (primary, profile); VxTwitter backup is dead — 403 Cloudflare on 2026-11-09, code removed, no longer tried; post timeline only via FxTwitter `/2/profile/{handle}/statuses`; trends24 is link-only (HTML page, no CORS headers, not readable in the browser, not treated as an API) |
| 05 | Yiwu Small Commodities · 义乌小商品监测 | 🌐 Bilingual · 中英双语 | `monitors/05-yiwu-small-goods.html` | Yiwugo / Yiwu Index official sites (no public JSON API, cannot be pulled directly) → labelled cached sample (business-climate index is a Sep 2026 sample); climate breakdown bar chart removed (only the total index 1554.97 is sourced); hotwords shared with 10 via `monitors/data/yiwu-hotwords.json`; samples older than 14 days marked “Expired” |
| 06 | Domestic AI & Agent Monitor · 国内AI与Agent监测 | 仅中文 · Chinese only | `monitors/06-domestic-ai-agents.html` | OpenRouter (primary, public catalog, flagship allow-list + id-prefix→vendor mapping, no scores) → labelled cached sample; live mode draws a price bar chart, cached mode draws the score scatter; leader KPI changed to “cheapest domestic” (lowest live price) and “longest context”, never showing an “unavailable” leader; agent count = 5 / video models = 6 moved out of KPIs into the “hand-compiled” section; API names escaped via esc(); sortable headers ▲/▼; agent table marked “hand-compiled · not an API” |
| 07 | AI Tool Price Drops & Quotas · AI工具降价/额度监测 | 🌐 Bilingual · 中英双语 | `monitors/07-ai-price-drop.html` | OpenRouter (primary) → models.dev api.json (backup, official-channel prices only) → labelled cached snapshot (2026-11-09); snapshot diff implemented: daily snapshots stored in localStorage by Beijing date (key `mon07_price_YYYY-MM-DD`), compared with the latest non-today snapshot for up/down/baseline; up/down filters disabled with no earlier snapshot; models.dev Anthropic id corrected to `claude-opus-5-5` (hyphenated, verified); notes merged by id, not display name; Actions also produces the full-price snapshot `monitors/data/prices.json` |
| 08 | AI New Launches · AI新品上线监测 | 🌐 Bilingual · 中英双语 | `monitors/08-ai-new-launches.html` | OpenRouter / models.dev new-entry diff (primary) → vendor blog RSS → hand-curated cache (labelled, 2026-11-09); “New feature” type filter option removed (no curated entries of that type); Google Blog RSS (blog.google/rss) readable directly in the browser (tested 200, CORS reflects Origin, fetched live — latest 5); Anthropic /news/rss.xml tested 404 (scraping /news HTML needs Actions); OpenAI /news/rss.xml has no browser CORS (only readable after Actions saves it as JSON); new-diff list shows at most 20 entries, the rest folds away |
| 09 | AI Side-Hustle Plays · AI副业玩法监测 | 仅中文 · Chinese only | `monitors/09-ai-side-hustle.html` | Hand-curated, no live fetching; X search notes cross-checked against Xiaohongshu hand collection, no live source; samples older than 30 days marked “needs re-curation” |
| 10 | Cross-Border Hot Products · 跨境爆款监测 | 🌐 Bilingual · 中英双语 | `monitors/10-cross-border-hot.html` | Hand-picked / cached sample (labelled, 2026-11-09); no stable free live ranking source, not presented as live; hotwords shared with 05 via `monitors/data/yiwu-hotwords.json`; World Cup signal KPI (sports-goods exports Q1 ¥2.83B, +12% YoY) has a source footnote (same research batch as 05, not live customs statistics); “source status” is a <details> fold; samples older than 14 days marked “Expired” |
| 11 | 1688 / Pinduoduo Price Trends · 1688/拼多多价格趋势 | 仅中文 · Chinese only | `monitors/11-1688-pdd-price.html` | Manual entry + dates (2026-11-09); no free public API, not presented as live; self-entry supported: form takes product name, wholesale price, retail price → auto gross-margin difference (retail − wholesale), stored in browser localStorage, deletable; bar chart switched to horizontal (indexAxis 'y') so long Chinese labels no longer squeeze; margin excludes shipping, platform fees and returns (marked in red) |
| 12 | Festival Product Calendar · 节日选品日历 | 🌐 Bilingual · 中英双语 | `monitors/12-festival-calendar.html` | Built-in static JSON (primary) → calendar-rule backup table (backup, verified entry by entry); zero dependencies; all dates parsed as `+08:00` (overseas-timezone countdowns no longer off by half a day); mobile timeline switched to a vertical timeline (.dot/.lbl no longer overlap); Qixi verified against the Hong Kong Observatory (Aug 8), no “pending verification” mark |
| 13 | Hot Search Aggregator · 热搜热榜聚合 | 仅中文 · Chinese only | `monitors/13-hot-search.html` | Actions snapshot `monitors/data/hot.json` (primary: GitHub Actions curls Weibo international + Douyin hot search on the runner every 6 h; browser-direct fetch always fails on CORS, so the page reads the same-origin snapshot) → embedded cache (2026-11-09 15:15 CST curl test, marked “Expired” after 12 h); hero built from the snapshot’s Top 1, no longer hardcoded to an old topic; Zhihu curl also 401, fixed as “Not available + manual link”; source status split into “curl (server) / browser” columns |
| 14 | GitHub Trending Daily · GitHub Trending 日榜 | 🌐 Bilingual · 中英双语 | `monitors/14-github-trending.html` | GitHub Search API (primary, browser-direct) → official Trending page snapshot (backup, needs Actions backfill) → labelled cached sample (2026-11-09); query window is the rolling last 7 days (`created:>` + today − 7 days, no longer hardcoded to 2026-11-02); titled “New-Repo Star Ranking (Last 7 Days)”, not official Trending |
| 15 | Product Hunt Daily Buzz · AI 产品热度日榜 | 🌐 Bilingual · 中英双语 | `monitors/15-product-hunt.html` | Actions snapshot `monitors/data/ph.json` (primary: server curls the Product Hunt RSS into JSON) → direct RSS + DOMParser parsing (backup: marked live only when entries are parsed and rendered, otherwise always “sample + curation”) → hand-curated sample (labelled, 2026-11-09); RSS carries no vote counts, always “Not available”, never invented; allorigins is down (tested timeout/500) |
| 16 | AI Big Events & Regulation · AI大事件 / 监管动态 | 🌐 Bilingual · 中英双语 | `monitors/16-ai-events.html` | Hand-curated, no live fetching (2026-11-09); every event dual-source verified; header computes sample age from the curation date, marked “Expired · needs re-curation” after 7 days; has a “Load sample” button (same as 09); Actions snapshot not built yet (status pages and RSS need Actions to fetch into JSON; this page currently has no such layer, stated openly) |
| 17 | Search Trends Monitor · 搜索趋势监测 | 🌐 Bilingual · 中英双语 | `monitors/17-search-trends.html` | Actions snapshot `monitors/data/trends.json` (primary: new `trends.google.com/trending/rss?geo=US/HK/TW`; old daily RSS is 404, geo=CN returns 400 and is not used) → open trends.google.com manually (backup) → hand-judged sample table (labelled, directional only, no invented numbers); Baidu Index has no backup source, no Baidu data on the page |

## Backup rule · 备份硬规则（新增 11 个监测同样适用）

Every data source must have a backup: primary → backup → cache, with source and time labelled on all three layers and “Expired” marked when stale. A source with no backup says “no backup” or “no usable backup source” on the page — never pretending a backup exists.

每个数据源都必须有备份：主源 → 替补源 → 缓存，三层标注来源与时间，过期标「已过期」。没有备份的源，页面上明确写「无备份」或「无可用备份源」，绝不假装有备用。

## Redundancy rule · 冗余规则（本项目最重要的一条）

Every data source must have a backup:

1. Primary fails → automatically switch to the backup;
2. Backup also fails → show the last cached data, labelled **“last data / expired”**;
3. No data at all → show **“Not available”**, never invent numbers;
4. Every module labels its current source (primary / backup / cache) and data time.

每个数据源都必须有替补：

1. 主源失败 → 自动切换替补源；
2. 替补也失败 → 显示上次缓存数据，并标明 **「上次数据 / 已过期」**；
3. 没有数据时显示 **「未获取」**，绝不编造数字；
4. 每个模块都标明当前来源（主源 / 替补源 / 缓存）和数据时间。

Hong Kong free quotes lag about 15 minutes; the page says so and does not pretend to be real-time.
Northbound net buying is not invented: HKEX no longer discloses real-time buy/sell amounts, so only turnover is reported, not net buying.

港股免费行情约延迟 15 分钟，页面上已写明，不冒充实时。
北向资金净买额因港交所不再披露实时买卖金额，只报成交额，不编净买额。

## Run locally · 本地运行

```bash
# either one / 任选其一
python3 -m http.server 8000
# or / 或
npx serve .
```

Then open http://localhost:8000/monitors/01-a-share-hk.html

然后打开 http://localhost:8000/monitors/01-a-share-hk.html

Double-clicking an HTML file also opens it, but some public APIs refuse `file://` requests over CORS; the page will then honestly show “Not available / cached”, so the local-server way above is recommended.

直接双击 HTML 文件也能打开，但部分公开接口会因 CORS 拒绝 `file://` 请求，
此时页面会如实显示「未获取 / 缓存」，建议用上面的本地服务器方式运行。

## Known data gaps (stated honestly) · 数据缺口（诚实说明）

- **01 Stocks · 股票**：腾讯行情是唯一真正解析的主源（逐个代码 `v_sh000001` 等精确匹配）；自选现拉 `qt.gtimg.cn/q=<代码>`（f[1]=名称、f[3]=现价、f[32]=涨跌幅%，失败显示未获取，6 字头自动补 sh、0/3 字头补 sz）；涨跌家数 / 分时 / AH 溢价标「缓存样本·非实时」；指数部分失败时 badge 为「腾讯实时 + 部分缓存补齐」；新浪行情已移除：直连 403 且无 CORS 头，浏览器不可用。Tencent quotes are the only truly parsed primary source (exact per-code matching, e.g. `v_sh000001`); the watchlist pulls `qt.gtimg.cn/q=<code>` live (f[1]=name, f[3]=price, f[32]=change%, “Not available” on failure, auto-prefix sh for 6xxxxx and sz for 0/3xxxxx). Advancers/decliners (725/4483/87) have no live source and are cached samples only; the intraday chart’s 7 points are a cached example trend, not live; all three section titles carry the “cached sample · not live” badge.
- **02 / 06 AI models · AI 模型**：代码里根本没有 model-watch，不要再把它当来源；models.dev `/api/v1/models` 返回 302 已死，但 `models.dev/api.json` 仍活（200，07/08 在用），两者不要混为一谈。实际唯一能通的公开目录是 OpenRouter，且它不给分数——分数列只有缓存样本里才有，实时模式改画价格条形图。缓存样本明确标注；API 返回的模型名经 esc() 转义后才进 innerHTML。There is no model-watch in the code — do not treat it as a source; models.dev `/api/v1/models` returns 302 (dead), but `models.dev/api.json` is still alive (200, used by 07/08) — do not confuse the two. The only working public catalog is OpenRouter, and it provides no scores — scores exist only in the cached sample, and live mode draws a price bar chart instead. Cached samples are clearly labelled; API-returned model names are escaped via esc() before entering innerHTML.
- **03 Open source · 开源**：主源是 Actions 快照 `monitors/data/oss.json`（GitHub Actions 每 6 小时逐仓拉取 24 个白名单仓库，history 连续 ≥7 天后给出全站统一 Δ Star；第 1 天只有基线，显示「积累中」），替补为浏览器直连 GitHub Core API 逐仓（topic 搜索已弃用，噪声太大），GitHub Search API 仅作底部「发现」。周增 Star（Δ Star）已实现：本机 localStorage 存每日快照，Δ = 当前 − ≥6 天前快照，不足则标明快照天数；第 1 天只有基线，显示「积累中」。未登录 Core API 每小时限 60 次，一次加载 24 次调用，约 2 次满载后会被 403 截断（已优雅处理，保留已加载部分）。缓存样本为 2026-11-09 核实值并标注。Primary source is the Actions snapshot `monitors/data/oss.json` (GitHub Actions pulls 24 allow-listed repos every 6 h; full-site unified Δ Star once history is ≥7 days; day 1 has only a baseline, shown as “Accumulating”); backup is browser-direct GitHub Core API per repo (topic search dropped — too noisy); GitHub Search API is only the bottom “Discover” section. Weekly Δ Star is implemented: localStorage keeps daily snapshots, Δ = now − the snapshot from ≥6 days ago, with the snapshot age stated when insufficient; day 1 shows only a baseline (“Accumulating”). Unauthenticated Core API allows 60 calls/hour; one full load is 24 calls, so about 2 full loads trigger a 403 cutoff (handled gracefully, keeping what loaded). Cached samples are 2026-11-09 verified values, labelled.
- **04 X**：trends24 不是可用来源——它只有 HTML 页面且不带 CORS 头，浏览器读不到，代码也不解析，只给链接让人手动打开；本页没有自动化的热搜来源。用户资料只走 FxTwitter `/2/profile/{账号}`；VxTwitter 替补已失效（2026-11-09 实测 403 Cloudflare），代码已下线。帖子时间线只有 FxTwitter `/2/profile/{账号}/statuses`。帖子表不展示单帖浏览量。只读，不登录、不发帖、不关注。trends24 is not a usable source — it is only an HTML page with no CORS headers, unreadable in the browser; the code does not parse it and only links it for manual opening; this page has no automated hot-search source. Profiles come only from FxTwitter `/2/profile/{handle}`; the VxTwitter backup is dead (403 Cloudflare on 2026-11-09) and its code is removed. Timelines come only from FxTwitter `/2/profile/{handle}/statuses`. The post table does not show per-post view counts. Read-only: no login, no posting, no following.
- **05 Yiwu · 义乌**：义乌购 / 义乌指数官网无公开 JSON 接口，浏览器直接拉取常被拦截；页面用调研核实过的样本作缓存并明确标注「缓存样本」，景气指数 1554.97（+0.55%）明确标注为 **2026年9月样本**，不得当作当前值；景气分项柱状图已删除（分项数无出处）；热词与 10 共用 `monitors/data/yiwu-hotwords.json`；样本超过 14 天标「已过期」。按钮是「载入样本」不是刷新。1688 生意参谋完整数据需商家账号，本项目只呈现公开方法，不伪造后台数据。Yiwugo / Yiwu Index official sites have no public JSON API and browser-direct fetches are often blocked; the page uses research-verified samples as cache, clearly labelled “cached sample”. The climate index 1554.97 (+0.55%) is explicitly a **Sep 2026 sample**, not a current value. The climate breakdown bar chart was removed (no source for the breakdown). Hotwords are shared with 10 via `monitors/data/yiwu-hotwords.json`; samples older than 14 days are marked “Expired”. The button is “Load sample”, not refresh. Full 1688 Business Advisor data needs a merchant account; this project only presents public methods and never fakes backend data.
- **07 Price drops · 降价**：OpenRouter 与 models.dev api.json 均实测 200 可用（2026-11-09）；models.dev 价格是分渠道价，替补只用官方渠道条目，Qwen/GLM/Seed 在替补模式下显示未获取。涨跌对比靠快照差分：按北京时间日期在 localStorage 存每日快照（`mon07_price_YYYY-MM-DD`），与最近一份非今日快照比算涨跌；首次快照只是基线，需第二次快照才有真涨跌，无上一份快照时涨/降筛选禁用。Anthropic 替补 id 为 `claude-opus-5-5`（连字符，实测存在）。订阅价/免费额度无稳定免费源，一律显示未获取。Actions 另产 `monitors/data/prices.json` 全量价快照。OpenRouter and models.dev api.json both tested 200 and usable (2026-11-09); models.dev prices are per-channel, and the backup uses official-channel entries only — Qwen/GLM/Seed show “Not available” in backup mode. Rise/fall comparison uses snapshot diffs: daily snapshots stored in localStorage by Beijing date (`mon07_price_YYYY-MM-DD`), compared with the latest non-today snapshot; the first snapshot is only a baseline, a second snapshot is needed for real rises/falls, and the up/down filters are disabled with no earlier snapshot. The Anthropic backup id is `claude-opus-5-5` (hyphenated, verified to exist). Subscription prices / free quotas have no stable free source and always show “Not available”. Actions also produces the full-price snapshot `monitors/data/prices.json`.
- **08 New launches · 新品**：OpenRouter/models.dev 新增条目 diff 可用；Google Blog RSS（blog.google/rss）浏览器可直读（实测 200，CORS 反射 Origin）；Anthropic /news/rss.xml 实测 404（改抓 /news HTML 需 Actions），OpenAI /news/rss.xml 浏览器无 CORS（只能经 Actions 存 JSON 后读）。类型筛选无「新功能」option（无该类型策展条目）。diff 新增列表最多展示 20 条，超出折叠。今日新品数为 0 是如实值，不是缺失。OpenRouter / models.dev new-entry diff works; Google Blog RSS (blog.google/rss) is directly readable in the browser (tested 200, CORS reflects Origin); Anthropic /news/rss.xml tested 404 (scraping /news HTML needs Actions); OpenAI /news/rss.xml has no browser CORS (only readable after Actions saves it as JSON). The type filter has no “New feature” option (no curated entries of that type). The new-diff list shows at most 20 entries, the rest folds away. A “0 new today” count is an honest value, not a missing one.
- **09 Side hustle · 副业**：纯人工策展，无实时源；评级是判断不是审计，样本超过 30 天标「需重新策展」。声称收入均为原帖宣称，未验证。Pure hand curation, no live source; ratings are judgements, not audits; samples older than 30 days are marked “needs re-curation”. Claimed incomes are as claimed in the original posts, unverified.
- **10 Cross-border · 跨境**：无稳定免费实时榜单源；样本 14 天后标已过期，需重新策展。热词与 05 共用 `monitors/data/yiwu-hotwords.json`。世界杯信号 KPI（体育用品出口 Q1 28.3 亿元、同比 +12%）有来源脚注（与 05 同一批调研样本值，非海关实时统计）。「数据源状态」改为 <details> 折叠。Amazon/Temu/TikTok Shop 实时销量无主源、无备份，本页不提供。No stable free live ranking source; samples are marked expired after 14 days and need re-curation. Hotwords are shared with 05 via `monitors/data/yiwu-hotwords.json`. The World Cup signal KPI (sports-goods exports Q1 ¥2.83B, +12% YoY) has a source footnote (same research batch as 05, not live customs statistics). “Source status” is a <details> fold. Amazon / Temu / TikTok Shop live sales have no primary source and no backup — this page does not provide them.
- **11 Prices · 价格**：样本区间为示例对照，非实测报价；毛利差不含运费、平台费、退货（红字标注）。可自行录入：表单填品名、拿货价、零售价 → 自动算毛利差，存本机浏览器 localStorage，可删除。无免费公开接口，无实时备份。Sample ranges are example comparisons, not measured quotes; gross-margin difference excludes shipping, platform fees and returns (marked in red). Self-entry supported: form takes product name, wholesale price, retail price → auto gross-margin difference, stored in browser localStorage, deletable. No free public API, no live backup.
- **12 Calendar · 日历**：节日日期为固定历法知识，2027 春节 2027-02-06 等已多源核实；七夕已按香港天文台核对（2027-08-08），无「待复核」标记；开学季为惯例窗口、2027 放假调休天数未公布故不写。日期一律按 `+08:00` 解析；移动端时间轴为垂直时间线。Festival dates are fixed calendar knowledge; 2027 Spring Festival 2027-02-06 and others are multi-source verified; Qixi is verified against the Hong Kong Observatory (2027-08-08) with no “pending verification” mark; the back-to-school season is a customary window, and 2027 holiday-adjustment days are not published, so they are not listed. All dates parse as `+08:00`; the mobile timeline is vertical.
- **13 Hot search · 热榜**：主源为 Actions 快照 `monitors/data/hot.json`（GitHub Actions 每 6 小时在 runner 上 curl 微博国际版 + 抖音热搜；浏览器直连因 CORS 必然失败，改读同域快照）。Hero 由快照 Top 1 生成，不再写死旧热点；缓存超过 12 小时标「已过期」。知乎 curl 亦 401，固定「未获取 + 手动链接」。Primary source is the Actions snapshot `monitors/data/hot.json` (GitHub Actions curls Weibo international + Douyin hot search on the runner every 6 h; browser-direct fetch always fails on CORS, so the page reads the same-origin snapshot). The hero is built from the snapshot’s Top 1, no longer hardcoded to an old topic; cache older than 12 hours is marked “Expired”. Zhihu curl also returns 401, fixed as “Not available + manual link”.
- **14 Trending**：GitHub Search API 带 CORS `*`，https 下应可直连；查询窗口为动态近 7 日；Trending 原站 HTML 快照需 Actions 回填，尚未建。Search API 不给单日新增 Star，图表标明为总 Star，非日增。The GitHub Search API carries CORS `*` and should be directly reachable over https; the query window is the rolling last 7 days; the official Trending HTML snapshot needs Actions backfill and is not built yet. The Search API does not provide daily new stars — charts are labelled as total stars, not daily adds.
- **15 Product Hunt**：主源为 Actions 快照 `monitors/data/ph.json`（服务端 curl RSS 存 JSON）；备份为 RSS 直连 + DOMParser 解析，只有解析出条目并渲染才标 live，否则一律「样本+策展」；票数 RSS 不提供，一律「未获取」，不编数；allorigins 已下线（实测超时/500）。Primary source is the Actions snapshot `monitors/data/ph.json` (server curls the RSS into JSON); backup is direct RSS + DOMParser parsing, marked live only when entries are parsed and rendered, otherwise always “sample + curation”; RSS provides no vote counts, always “Not available”, never invented; allorigins is down (tested timeout/500).
- **16 Big events · 大事件**：人工策展快照，页头按策展日期算样本年龄，超过 7 天标「已过期·需重策展」；有「载入样本」按钮（与 09 一致）；Actions 快照未建，无自动刷新路径。Hand-curated snapshot; the header computes sample age from the curation date and marks “Expired · needs re-curation” after 7 days; has a “Load sample” button (same as 09); the Actions snapshot is not built, so there is no automatic refresh path.
- **17 Search trends · 搜索趋势**：主源为 Actions 快照 `monitors/data/trends.json`（新版 `trending/rss?geo=US/HK/TW`；旧版 daily RSS 已 404，geo=CN 返回 400 不用）；趋势图为示意指数（人工设定，非实测），页内三处警告勿当数值引用；百度指数无备份源，页内无百度数据。Primary source is the Actions snapshot `monitors/data/trends.json` (new `trending/rss?geo=US/HK/TW`; the old daily RSS is 404, geo=CN returns 400 and is not used); the trend chart is an illustrative index (hand-set, not measured), with three on-page warnings not to cite it as numbers; Baidu Index has no backup source and no Baidu data appears on the page.

## Privacy · 隐私

This project contains no private information: no passwords, emails, phone numbers, accounts, or order numbers.
The X monitor presets no accounts — users enter a public handle themselves.

本项目不包含任何私人信息：没有密码、邮箱、电话、账号、订单号。
X 监测不预设任何账号，使用者自行输入公开账号。

## License · 许可

MIT License，见 [LICENSE](LICENSE)。

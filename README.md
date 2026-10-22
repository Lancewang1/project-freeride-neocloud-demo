# PROJECT FREERIDE · Neocloud 深度投研 DEMO

公开网页：**https://lancewang1.github.io/project-freeride-neocloud-demo/**

首页完整覆盖需求、业务获取、交付、单位经济/现金、债务时间表和同业估值。每层有数据、来源、分析、验证、结论和投资含义。研究截止2026-10-22；估值采用10/21收盘，财报截至6/30，融资核实到9/22，信用报道到10/21。事件行情序列截至10/20，与估值报价分列。

## 内容

- `index.html`：完整研究首页；`coreweave-deep-dive.md`：文字与图表版。
- `data/deep-research.json`：15条Anthropic公司run-rate观测/重复/回溯/预测、产品与实际收入、六季CRWV数据、同业预测、债务日程、价格和来源哈希。
- `data/deep-analysis.json`：300个事件×股票×基准×窗口结果及60组相关检验，不是300个独立事件。
- `scripts/analyze_deep_case.py`：重算Pearson、Spearman、精确置换p、Holm及留一法。
- `scripts/render_deep_case.py`：从已审核数据重建首页。
- `scripts/refresh_evidence.py`：公开网页采集及待审队列，原文只保存在忽略的本地缓存。
- `references/deep-dive-protocol.md`：探索性检验登记；`references/`含原研报出处、机构框架及审计。
- `dashboard.html`：原数据看板；`case-v1.html`：上一版存档，口径更正以新首页为准。

## 本地重算与更新

依赖：`pip install numpy scipy markdown requests beautifulsoup4`。

1. `python scripts/refresh_evidence.py --scope anthropic`：全官网新闻发现、哈希、候选收入段落；可选`financial`或`all`。
2. 复核实际/预测、公司/产品、所属期/披露时间、下界/点值后更新`data/deep-research.json`。新页面不能未经复核成为历史事件。
3. `python scripts/analyze_deep_case.py`：重算全部预定窗口，不择优发布。
4. `python scripts/render_deep_case.py`：重建首页；叙述结论须与新计算核对，脚本不会自行完成投研判断。
5. `python -m http.server 8000`预览；检查后提交main，由GitHub Pages部署。

本页是已审核快照。网页刷新不会运行爬虫；未安装无人值守定时任务。原始研报PDF、整篇新闻、凭据和本地路径不进入公开仓库。

## 结论与边界

CRWV 2027E收入倍数低于NBIS，但未来资本结构、折旧后利润和稀释决定每股回报。RPO近24个月兑现额增长快于总RPO；Q2现金质量弱于EBITDA。融资表区分实际提款、未提款承诺和9月可转债净额；情景不等于当前现金余额。

Anthropic官网扫描276篇新闻。核心相关检验只有5个官方新高事件、4个增幅配对；CRWV六季构成5个变化配对。结果不支持已验证交易规则。全行业统一RPO分母、Anthropic正式卖方调查共识、下次正式ARR公告日、逐GPU项目数据仍未取得；不制造数据或用不匹配口径替代。

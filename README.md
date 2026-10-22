# PROJECT FREERIDE · Neocloud Research Demo

公开演示：**https://lancewang1.github.io/project-freeride-neocloud-demo/**

首页是一份完整的 **CoreWeave 投资案例**，逐层展示需求、合同、交付、单位经济、现金、信用、股东价值和历史信号检验。每层都有数据、验证、分析、结论、投资含义和证伪条件。原始数据看板保留在 `dashboard.html`。

## 内容

- `index.html`：完整CoreWeave研究案例与交互压力情景，无外部前端依赖。
- `coreweave-case.md` / `data/coreweave-case.json`：文字版与结构化案例。
- `data/coreweave-case-calculations.json`：SEC数值、计算与口径。
- `dashboard.html`：原始数据、覆盖与事件研究看板。
- `data/observations.json`：规范化观测与来源URL。
- `data/event-study.json`：逐事件历史检验、方法及限制。
- `references/`：研究框架、审计、来源书目、数据获取路径。

## 数据与更新

完整案例研究截止2026-10-22，财务期间截至2026-06-30，信用数据为10月15/21日媒体报道，非实时终端报价。旧数据看板采集日期为2026-10-21，各指标实际期间与披露日期分别显示；12/30类指标有部分观测或代理，其余保留明确缺口。网页重新加载不会运行爬虫；维护端完成采集、语义复核和检验后发布新版本。

GitHub Pages 从 `main` 分支根目录部署。无API密钥、无服务器账户、无交易执行功能。原始研究PDF、原始网页存档和本地路径不进入公开仓库。第三方来源内容及权利归其各自所有者，出处不代表其认可本项目。

## 研究边界

框架是研究工具，不是已验证的预测模型。初次NBIS实际ARR增幅与公告后5日相对QQQ回报的6个事件相关系数约−0.37，p约0.50；不能据此宣称正向或负向交易规律。具体时点处理、口径变化、样本缺失和混杂说明见看板与审计。

CoreWeave案例当前结论为条件观察、融资先行。收入增长有报表支持，现金建设需求与信用压力显著；尚未验证完整流动性、项目ROIC和融资后每股估值，不提供伪精确目标价，也不认定已经违约。案例的步骤完整不代表所有投资尽调已经完成。

## 本地预览

直接打开 `index.html`，或运行 `python -m http.server 8000` 后访问 `http://localhost:8000`。

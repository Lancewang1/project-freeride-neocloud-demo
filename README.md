# PROJECT FREERIDE · Neocloud Research Demo

公开演示：**https://lancewang1.github.io/project-freeride-neocloud-demo/**

基于公开数据与有出处的行业研究框架，展示AI算力云关键数据、数据覆盖、历史事件检验与经营传导实验器。

## 内容

- `index.html`：自包含交互看板，无外部前端依赖。
- `data/observations.json`：规范化观测与来源URL。
- `data/event-study.json`：逐事件历史检验、方法及限制。
- `references/`：研究框架、审计、来源书目、数据获取路径。

## 数据与更新

这是已验证数据的公开快照。当前采集日期为2026-10-21，各指标的实际期间和披露日期分别显示。12/30类指标有部分观测或代理，其余保留明确缺口。网页重新加载不会运行爬虫；本地维护端完成采集、语义复核和检验后发布新版本。

GitHub Pages 从 `main` 分支根目录部署。无API密钥、无服务器账户、无交易执行功能。原始研究PDF、原始网页存档和本地路径不进入公开仓库。第三方来源内容及权利归其各自所有者，出处不代表其认可本项目。

## 研究边界

框架是研究工具，不是已验证的预测模型。初次NBIS实际ARR增幅与公告后5日相对QQQ回报的6个事件相关系数约−0.37，p约0.50；不能据此宣称正向或负向交易规律。具体时点处理、口径变化、样本缺失和混杂说明见看板与审计。

## 本地预览

直接打开 `index.html`，或运行 `python -m http.server 8000` 后访问 `http://localhost:8000`。

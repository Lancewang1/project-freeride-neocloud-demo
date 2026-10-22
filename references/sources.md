# 原研报出处、蒸馏映射与阅读记录

本版基于用户提供的4份机构署名PDF；书目、日期及观点均按PDF页内内容记录。本次未向发行机构独立核验版本，也未把研报引用的公司数据全部回溯到原始公告。**可以确认的是出处忠实度与已查看页内容，不是历史预测必然正确。**

所有页码是PDF物理页码，从1起。公开版仅保留研究书目与页码，不提供原研报文件或本地材料路径。

## 原始来源

### S1｜Bernstein｜2026-03-31

**The Neocloud Field Guide: What Differentiates CRWV, IREN, and NBIS?**

作者：Madison Rezaei、Gautam Chhugani及团队。封面日期：2026-03-31；首次发布/页内时间：2026-03-31 04:01 UTC。共24页。

| 对应框架 | 原文位置 | 可定位的英文短锚/标题 |
|---|---|---|
| F1 | p.3–4，Details / Exhibit 2 | foundational differences |
| F2 | p.2–6，Foundational Differences / Exhibits 3–8 | time to market |
| F3 | p.7–9，Commercial Differences / Exhibits 9–14 | on-demand revenue |
| F4 | p.10–11，Financing Considerations / Exhibits 15–21 | Special Purpose Vehicles |
| F8 | p.1–2，Investment Implications | structural concerns |

正文阅读页：1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12；图像核对页：4, 7, 8, 11。

### S2｜Bernstein｜2026-04-21

**China Internet: A primer on AI token economics and inference margins**

作者：Robin Zhu、Charles Gou、Min-Joo Kang。封面日期：2026-04-21；首次发布/页内时间：2026-04-20 20:30 UTC。共23页。

| 对应框架 | 原文位置 | 可定位的英文短锚/标题 |
|---|---|---|
| F5 | p.4–5，Exhibits 2–4; formula in Exhibit 3 | A BACK OF ENVELOPE MODEL FOR REVENUE AND COST PER TOKEN |
| F5 | p.6–8，Workload Mix Matters / Exhibits 5–9 | WORKLOAD MIX MATTERS |
| F5 | p.8–12，GPU cost triangulation / Exhibits 10–17 | educated guesstimates |
| F5 | p.12–13，H1 2026 / Exhibits 18–19 | workload mix headwind |

正文阅读页：1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13；图像核对页：5, 11, 12。

### S3｜Bernstein｜2026-06-12

**Global Internet: A framework for AI model commoditisation, and market segmentation**

作者：Robin Zhu、Mark Shmulik及团队。封面日期：2026-06-12；首次发布/页内时间：2026-06-11 20:30 UTC。共18页。

| 对应框架 | 原文位置 | 可定位的英文短锚/标题 |
|---|---|---|
| F6 | p.4–5，A Mental Model / Exhibit 2 | good enough |
| F6 | p.5–7，Market Segmentation / Exhibits 3–5 | cost per task |
| F6 | p.7–8，R&D / Exhibit 6 | Breadth of R&D focus |

正文阅读页：1, 2, 3, 4, 5, 6, 7, 8；图像核对页：5, 7。

### S4｜Goldman Sachs｜2026-06-22

**Americas Technology: Hardware — Traditional & accelerated servers: An industry primer**

作者：Katherine Murphy、Michael Ng、Zorayda Montemayor。封面日期：2026-06-22；首次发布/页内时间：2026-06-22 16:56 EDT。共30页。

| 对应框架 | 原文位置 | 可定位的英文短锚/标题 |
|---|---|---|
| F7 | p.17–18，Accelerated server unit economics / Exhibit 28 | GPU cost includes HBM pricing |
| F7 | p.19–21，Customer buying patterns / Exhibits 31–36 | Buying patterns |
| F7 | p.22，Services / Exhibit 37 | Attaching services |

正文阅读页：1, 2, 3, 17, 18, 19, 20, 21, 22；图像核对页：18。

## 原文到Skill的具体变换

| 原文内容 | 本版保留 | 本版新增，不能归给机构 |
|---|---|---|
| S1 p.3–4三组十维 | 十维名称、分组与比较逻辑 | 每维必答问题、字段ID、阶段权重建议 |
| S1 p.7–11合同/融资 | 合同类型、backlog脚注、SPV/可转债/预付款差别 | 合同瀑布、逐季资金缺口与双重计数控制 |
| S2 p.5公式、p.11–12敏感性 | 原公式、历史参数及机构估计属性 | Python复算、Anthropic收入到GPU小时的跨报告桥接 |
| S3 p.4–8商品化/分层 | good-enough、任务成本、地区/客户分层、研发方向 | 对Neocloud续租/残值的两方向推导 |
| S4 p.17–22采购与BOM | OEM/ODM/客户类别、全机成本和组件价日期 | GPU cohort资产现金流与采购验证清单 |
| 用户要求Anthropic ARR | 原样纳入M01核心面板 | 数据定义、获取路径、映射边界和优先级 |

## 需要保留的原文冲突与限定

1. **S1杠杆：**p.3/p.4称CRWV净债务/EBITDA约5.9倍，而p.11 Exhibit 21的4Q25点为6.91。口径/期间未解释前不选择一个作为当前事实。两处均已查看，p.4/p.11图像核对。
2. **S1合同汇总：**p.4约47B与p.8的47.4B是不同精度的表述；p.8 NBIS相关条款还包括固定额/潜在backstop、不同年份及“up to”金额。不能直接把表头总额当不可撤销RPO；须回原合同重建。
3. **S1集中度：**p.8是机构估计backlog构成，p.9的IREN项使用当前/预期ARR，不能把这些图表全部标作同一期实际收入集中度。
4. **S2吞吐假设：**p.8/p.11的MiniMax基准为2,300 tok/s，p.12敏感性为3,000 tok/s，p.4/p.13前瞻情景也用3,000。这是场景不同；引用时保留图号，不把它们当三次实测。
5. **S2模态单位：**p.8文字提到4:3但同时给1920×1080换算，两者宽高比不一致。本版不沿用该视频Token换算，只保留“模态影响混合单价”的定性框架。
6. **S2毛利边界：**p.4定义不含训练和公司层费用；p.5的GPU小时成本可包含云服务加价。因此此处毛利不是Neocloud毛利，也不是模型公司净利。
7. **S3市场空间：**p.5正文320B，p.7图中350B/38%，不一致。本版只采用按地区/客户划分可服务市场的方法，不把任一TAM点值写入默认预测。两页图像已核对。
8. **S4 BOM时点：**p.18明确组件价为2025年7月，报告本身是2026年6月。GPU成本含HBM；表下的CPU general server说明与H100表内容也不一致，按具体配置和脚注识别，不靠副标题。

## 补充材料的处理

算力租赁：从业务本质到研究框架20260806.pdf：已阅读提取的主要正文（p.1–10），它包含资本中介/渠道/运营三个层次及若干渠道参数。但可读内容不足以确认作者与机构身份，部分公司使用缩写。因此不将其作为“机构框架”的主出处，不沿用拿卡成本折扣、利用率和融资比例等未经复核数字。其视角只能作为进一步尽调问题。

## 阅读范围说明

沿用先前127文件的清单定位，本次针对上面四份报告重新进行章节阅读与10页关键图像核对，没有宣称全量精读全部资料。音频未用于此版。历史数字只在出处复算/阅读示例中出现；市场面板的最新数值需要后续按截止日采集。

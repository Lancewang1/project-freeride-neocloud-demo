"""Render the research memo and interactive homepage from reviewed public data.
Run: python scripts/analyze_deep_case.py && python scripts/render_deep_case.py
Requires markdown; analysis also needs numpy and scipy.
"""
from pathlib import Path
import json,html,math
import markdown
R=Path(__file__).resolve().parents[1]
D=json.loads((R/'data/deep-research.json').read_text(encoding='utf8'));A=json.loads((R/'data/deep-analysis.json').read_text(encoding='utf8'));Q=D['quarters'];E=html.escape
def ref(key,label=None):return f'[{label or key}]({D["sources"][key]["url"]})'
def table(headers,rows):return '\n|'+'|'.join(headers)+'|\n|'+'|'.join(['---']*len(headers))+'|\n'+''.join('|'+'|'.join(str(v) for v in row)+'|\n' for row in rows)+'\n'
def pct(v):return '—' if v is None else f'{v*100:+.1f}%'
def num(v):return '—' if v is None else f'{v:,.2f}'
def chart(title,labels,series,ylabel='USD B',id=''):
 colors=['#58dfbb','#8faeff','#ffc475','#ff819c'];w=900;h=310;left=65;right=20;top=30;bottom=55
 vals=[v for _,vs in series for v in vs if v is not None];lo=min(0,min(vals));hi=max(vals)*1.12 or 1
 xx=lambda i:left+i*(w-left-right)/max(1,len(labels)-1)
 yy=lambda v:top+(hi-v)/(hi-lo)*(h-top-bottom)
 svg=f'<div class="chart" id="{id}"><h3>{E(title)}</h3><svg viewBox="0 0 {w} {h}" role="img" aria-label="{E(title)}"><text x="5" y="17" fill="#aebdd0" font-size="12">{ylabel}</text>'
 for j in range(5):
  v=lo+(hi-lo)*j/4;y=yy(v);svg+=f'<path d="M{left},{y:.1f}H{w-right}" stroke="#263849"/><text x="{left-8}" y="{y+4:.1f}" text-anchor="end" fill="#aebdd0" font-size="12">{v:.1f}</text>'
 for i,l in enumerate(labels):svg+=f'<text x="{xx(i):.1f}" y="{h-bottom+24}" text-anchor="middle" fill="#aebdd0" font-size="12">{E(l)}</text>'
 for si,(name,vs) in enumerate(series):
  pts=' '.join(f'{xx(i):.1f},{yy(v):.1f}' for i,v in enumerate(vs) if v is not None);c=colors[si%4]
  svg+=f'<polyline points="{pts}" fill="none" stroke="{c}" stroke-width="2" stroke-dasharray="4 3"/>'
  for i,v in enumerate(vs):
   if v is not None:svg+=f'<circle cx="{xx(i):.1f}" cy="{yy(v):.1f}" r="4" fill="{c}"><title>{E(labels[i])} · {E(name)}: {v:.3f}</title></circle>'
  svg+=f'<text x="{left+si*230}" y="{h-5}" fill="{c}" font-size="13">● {E(name)}</text>'
 return svg+'</svg><p class="small">悬停数据点查看数值。虚线仅连接观测，不代表中间日期已有披露。</p></div>'
def statrow(series):
 r=next(x for x in A['summary'] if x['series']==series and x['symbol']=='CRWV' and x['benchmark']=='QQQ' and x['horizon']==5)
 return [series,r['n'],f"{r['pearson']:.2f}",f"{r['rho']:.2f}",f"{r['p']:.3f}",f"{r['p_holm_all']:.3f}",f"{r['leave_one_rho'][0]:.2f} 至 {r['leave_one_rho'][1]:.2f}"]
parts=[]
parts.append('''<div class="eyebrow">PROJECT FREERIDE · 深度投研案例 / 2026-10-22</div>
<h1>CoreWeave：增长很强，<br>股权回报的门槛更高。</h1>
<p class="lead">从终端需求到合同、交付、现金与估值，把“AI需求好”拆成可核查、可计算、可证伪的股票判断。</p>
<div class="hero-grid"><div><small>2027E EV / Sales · 供应商含租赁口径</small><strong>3.04×</strong><span>NBIS 4.00×；期间与资本结构需校正</span></div><div><small>2026Q2 CFO − 递延收入增长贡献</small><strong>−$0.111B</strong><span>经营现金质量弱于收入和EBITDA</span></div><div><small>未来24个月RPO兑现额 · Q2较Q1</small><strong>+19.5%</strong><span>总RPO仅+5.0%，兑现结构改善</span></div></div>

**本版投资判断：[新增] 相对 NBIS 的收入倍数有折价，但尚不能据此判定 CRWV 绝对便宜。** 当前股价依赖交付加速、未来融资可得以及折旧后的利润率恢复。最值得追踪的预期差不是再多一笔订单，而是近端RPO转收入、交付爬坡是否改善现金、以及新增资本由谁承担。

**统一口径：**本文金额默认 **USD B（十亿美元，1B=10亿美元）**；股价/市值采用2026-10-21美股收盘。财务最新为2026-06-30，融资更新到9月22日；不要把6月现金误称为10月现金。实际、管理层预计、媒体报道、研究者情景分别标记。下列机制继承原研报，新增测算和判断均由FREERIDE负责。

<div class="links"><a href="coreweave-deep-dive.md">下载完整文字版</a><a href="data/deep-research.json">下载基础数据</a><a href="data/deep-analysis.json">下载检验结果</a><a href="dashboard.html">原始数据看板</a><a href="case-v1.html">上一版案例存档</a><button onclick="window.print()">打印 / 保存PDF</button></div>
''')
parts.append('<section id="demand">\n\n## 01 · 终端需求：收入规模、增长速度与股价敏感度必须分开\n\n'+ref('framework','框架出处：S2 pp.4–13；S3 pp.4–8')+'；Anthropic指标及以下检验为[用户指定 / 新增]。\n\n')
parts.append('''**结论：需求仍在增长，但“增长率下降、订单流向其他算力商、融资成本上升”可以同时发生。** Anthropic不是CRWV已披露收入的等比例代理。按官方公告，5B→7B→14B→30B→47B是连续扩张；更近期的65B为媒体/研究机构数据。不能用47B停更数据代表当前终端需求，也不能把Q3单季收入16.8B直接拼成公司月末ARR。

### 历史全表：保留本次检索发现的每个全公司数值

覆盖官网 sitemap 的276篇新闻及定向媒体检索；这是**本次检索覆盖内全表，不声称互联网历史披露穷尽**。ARR在此是annualized revenue run-rate，并非严格订阅ARR；用户此前的“IRR”在此按ARR处理。地区收入倍数、客户自己的收入和Claude Code单产品不混入公司序列。

<div class="control"><label>图表时间轴 <select id="anthroAxis"><option value="period">实际所属月份（历史回溯）</option><option value="published">可核查披露日期（市场信息集）</option></select></label></div><div id="anthroChart" class="chart"></div>
''')
parts.append(table(['数据所属期','可核查披露日','Run-rate $B','证据类型','解释 / 来源'],[[a['period'],a['published'] or '未确定',f"{a['value']:g}",a['kind'],a['note']+' '+ref(a['source'],'来源')] for a in D['anthropic']]))
parts.append('### 产品与已确认收入交叉核验\n\n'+table(['Claude Code所属期','Run-rate $B','披露日','来源'],[[a['period'],a['value'],a['published'],ref(a['source'])] for a in D['claude_code']]))
parts.append(table(['期间','全公司已确认收入 $B（媒体/研究机构口径）','证据'],[[a['period'],a['value'],ref(a['source'])] for a in D['anthropic_recognized_revenue_media']]))
parts.append('''10月2日早期报道Q1/Q2为4.73B/11.5B；10月15日CNBC报道约数为4.7B/11.6B，Q3为16.8B。按同一较新报道，Q2 / Q1约增长147%，Q3 / Q2约增长45%，保留两版而不悄悄覆盖。这支持“绝对规模继续增长、增速放缓”，不支持“收入下降”。Q3的16.8B乘4等于67.2B，是**季度平均收入年化**，不能当作9月月末run-rate。47B、65B等门槛数值也不能当成精确实测增幅。

**需求质量与份额传导：**官方4月披露明确包含Google/Broadcom TPU和AWS合作，算力需求未必流向CRWV的NVIDIA GPU。PitchBook/Morningstar援引草案称2025年47%收入经Amazon/Google市场销售，并采用总额法；因此不同模型公司的收入比较还受渠道会计影响。模型收入增长→付费工作负载→单位任务算力→外租比例→CRWV份额→合同收入，每一步都要有独立证据，不能直接把Anthropic增长率乘CRWV收入。

### 市场共识与下一个催化剂

|项目|本次证据|对模型的用途|
|---|---|---|
|Anthropic下一次定期财报/ARR公告|未找到公司确认的固定披露日|显示“未公告”，不能制造倒计时|
|2026年末100B run-rate|9月19日Gulf News转述NYT的报道预期|舆论预期参照，不是多家机构一致预期；现值与预测分开|
|2026年末110B run-rate|10月15日CNBC转述WSJ的投资者预期，较早期100B更高|最新可得预期参照；缺分析师数量/分位数，不能称为正式卖方一致预期|
|拟IPO及公开文件|媒体曾称可能11月；未核实正式上市日|作为触发器监控，不能承诺该月披露|
|CRWV下次财报|数据供应商估计2026-11-09盘后，当前IR新闻列表未确认|标“估计日期”，公布正式时间后替换|

监测办法：每天抓取官网全新闻目录，新增正文中识别公司主体、run-rate、已确认收入和预测词，保存哈希；重复门槛去重，历史回溯保留两条时间轴。未找到可核查的Anthropic券商调查样本/均值/分位数，因此把100B→110B标成**报道中的预期变化**，而不是统计意义的共识修正。CRWV/NBIS/IREN的公开卖方聚合收入预测见第06层。

### 历史上什么时候最敏感？

定义一：公告窗口内**绝对市场模型异常收益**最大；定义二：该反应除以事件前残差波动率×窗口长度平方根。两者回答“当时动了多少”，不是因果弹性。主样本为5个官方新高披露，增长相关只有4组；重复披露、媒体65B、回溯87M/1B/9B不进入主检验。
''')
top=[e for e in A['largest_observed_reaction'] if e['horizon']==5]
parts.append(table(['股票','5日绝对异常反应最大日期','原始收益','QQQ相减','市场模型异常收益','标准化反应'],[[e['symbol'],e['date'],pct(e['raw']),pct(e['excess']),pct(e['car']),f"{e['z']:.2f}σ"] for e in top]))
parts.append('''**解释：**这三个股票的最大反应不在同一天，IREN最大绝对反应甚至为负。若把“敏感”定义为上涨，会遗漏风险事件。2026-04-06同时含TPU合作信息；2026-02-12同时是NBIS财报日；融资、产品、宏观等变量没有被单因素模型隔离。不能把表中日期解释为“市场只因Anthropic ARR而涨跌”。

完整事件、1/5/20日、QQQ/SMH、Pearson与Spearman、置换p值、留一法和全检验Holm校正均可在下面切换。未做ARR日频插值；否则五条新闻会被伪装成数百个独立样本。

<div id="eventExplorer"></div>

**本层决策：**把Anthropic作为需求与客户信用的前导指标，不单独触发买入。若收入增长放缓同时客户算力承诺扩大，优先检查客户资本开支回报与付款保障；若新收入主要由TPU渠道承接，降低其对CRWV收入预测的映射权重。
</section>
''')
parts.append('<section id="contracts">\n\n## 02 · 业务获取：RPO增长、近端兑现与份额\n\n'+ref('framework','框架：S1 pp.7–9，合同可见度与集中度')+'。\n\n')
parts.append(chart('合同存量：RPO 与公司定义 backlog 分列',[q['label'] for q in Q],[('RPO',[q['rpo'] for q in Q]),('Revenue backlog',[q['backlog'] for q in Q]),('预计24个月兑现RPO',[q['rpo_24m'] for q in Q])]))
parts.append(table(['期末','RPO $B','Backlog $B','RPO/Backlog','近24月预计兑现 $B','RPO首次已核查申报日'],[[q['label'],q['rpo'],q['backlog'],f"{q['rpo']/q['backlog']:.1%}",num(q['rpo_24m']),q['rpo_published']] for q in Q]))
parts.append('''**结论：Q2订单增长减速，但合同兑现结构改善。** 2026Q2 RPO环比+5.0%，backlog约+4.6%，弱于Q1的大额签约跳升。可是未来24个月预计兑现占比由36%升至41%，相应金额由35.568B增至42.517B，增加6.949B、约19.5%。这比单看103.7B总额更接近未来两年收入。

**合同瀑布检验：**Q2末RPO103.7 − Q1末98.8 + Q2收入2.575 = 7.475B。这只是“新增及重估的净补充代理”，不是净新签订单：收入不全来自前期RPO、合同修改/变量对价/重分类也会影响结果。Q1同法约40.178B；因此增长确实依赖大单，不能外推每季平滑签约。Q2新闻另称第三季度初新增超过25B净客户承诺，不能加到6月底RPO冒充已报告期末余额。

RPO定义扣除部分预计服务抵扣、交付延迟与转售容量等变量对价；backlog还可包括其他估计金额。2025Q1 RPO仅占backlog56.8%，2026Q2约99.7%，这既可能包含合同可确认程度改善，也提示**RPO增速不全等于客户需求增速**。

来源：'''+ref('crwv10q','2026Q2 10-Q，Note 2 pp.14–15')+'；'+ref('sec2026-03-31','2026Q1 10-Q Note 2')+'；'+ref('sec2025-12-31','2025 10-K Note 2')+'；'+ref('sec2025-09-30','2025Q3 10-Q Note 2')+'；各季度IR新闻链接见交付表。\n\n')
parts.append('''### RPO市场份额：先把分母做对

|公司 / 最近可得口径|金额 $B|为什么不能直接相加为行业RPO|
|---|---:|---|
|CRWV 2026-06-30 ASC606 RPO|103.7|与backlog分列，预计兑现到78个月|
|NBIS 2026Q2股东信 customer commitments|40|客户承诺，非本版已核实的统一RPO定义|
|IREN 2026-06-30 合计|16.6|明确混合ASC606 RPO与ASC842租赁合同价值|

因此不输出“CRWV RPO占全行业64.7%”：它既混了口径，也漏掉Lambda、Fluidstack、Nscale等私人公司和大云供应。**本次不能验证全行业RPO份额，也不能合法地给它做股价相关性。** 可执行替代是固定可比样本的已实现云收入份额，并在取得其他公司同口径RPO后扩展。
'''+ref('nbisq2','NBIS Q2股东信 p.3')+'；'+ref('irenfiling','IREN FY2026 10-K Note 4')+'。\n\n')
shares=[('2025Q4',1.572,.2142),('2026Q1',2.078,.3897),('2026Q2',2.575,.5749)]
parts.append(table(['固定两公司样本','CRWV收入 $B','NBIS AI云收入 $B','CRWV样本收入份额'],[[p,c,n,f'{c/(c+n):.2%}'] for p,c,n in shares]))
parts.append(f'''最新季度加上IREN AI云收入0.0705B，三家公司样本中CRWV占 **{2.575/(2.575+.5749+.0705):.2%}**。两公司固定样本的份额由88.0%降至81.8%：CRWV绝对规模领先，但NBIS增速更快。三公司样本不代表全行业；IREN总收入含挖矿，不混入AI云分母。三个时期不足以识别份额变化与股价的稳定关系。来源：[NBIS Q4股东信](https://assets.nebius.com/assets/e59fb92e-9027-473a-8cac-04f9d2e9ea9a/Shareholder%20Letter%20Q4%202025.pdf)、[NBIS Q1股东信](https://assets.nebius.com/assets/4f7f76ee-aa57-41d9-935b-cac74898469d/Nebius%20SHL_Q1%202026.pdf)、[IREN季度AI收入报道](https://finance.yahoo.com/markets/stocks/articles/iren-4b-contracted-arr-only-034434431.html)，最新NBIS精确值574.9M见Q2股东信p.9。

**历史检验：**RPO增幅 vs 5日市场模型异常收益，n=5、Spearman −0.70、精确p=0.233；backlog为−0.30、p=0.683。均未通过多重检验。RPO使用SEC可核查披露日，可能晚于财报/订单已被市场知悉，因此不是纯粹的订单意外冲击。

**本层决策：**维持规模领先判断，但不赋予“份额持续扩大”的估值溢价。上调近端收入必须同时看到24个月兑现结构与验收；Q3要验证早期新增承诺是否进入期末RPO、是否改变预付款和交付条款。
</section>
''')
parts.append('<section id="delivery">\n\n## 03 · 交付兑现：容量、客户结构与收入拆解\n\n'+ref('framework','框架：S1 pp.5–6，time-to-market')+'。\n\n')
parts.append(chart('季度收入与调整后EBITDA',[q['label'] for q in Q],[('收入',[q['revenue'] for q in Q]),('Adjusted EBITDA',[q['ebitda'] for q in Q])]))
parts.append(table(['季度','收入 $B','环比','Active MW约数','Contracted GW约数','收入年化/期末MW $M','公告'],[[q['label'],num(q['revenue']),pct(q['revenue']/Q[i-1]['revenue']-1) if i else '—',q['active_mw'],q['contracted_gw'],num(q['rev_per_end_mw']),ref(q['source'],'原文')] for i,q in enumerate(Q)]))
parts.append('''**结论：交付速度明显加快，但新容量尚未完整体现在季度收入中。** Q2 active power约1.5GW，较Q1超过1GW的近似基准增加约50%；收入环比增加23.9%。期末容量年化收入强度由约8.31M/MW降到6.87M/MW。若用Q1/Q2期末均值1.25GW粗估平均容量，Q2强度约8.24M/MW，说明**时间权重本身已能解释很大一部分下降**，不能据此宣布租金下降17%。容量数字本身也带“超过/约”的精度限制。

Active MW不是可售GPU数，更不是客户计费GPU小时；合同开始日、验收、不同卡型密度和软件收入都影响换算。要验证租价，需要同一GPU代际与服务配置的实际合同价格，不能把收入/MW代理称为真实GPU租金。

### 收入拆解：用已披露维度，而非编造训练 / 推理占比

|2026Q2维度|金额 $B|占比 / 变化|研究结论|
|---|---:|---|---|
|客户承诺相关收入|约2.524|约98%|按需租价上涨不会立刻重定价全部收入|
|其他收入残差|约0.052|约2%|不直接等同全部spot GPU收入|
|美国|2.389|92.8%；同比+108.1%|扩张仍主要来自美国|
|其他国家|0.186|7.2%；同比+190.6%|海外增速高，绝对贡献较小|
|客户A|约0.927|36%，上年同期71%|最大客户集中度下降，但A标签不能跨文件直接等同Microsoft|
|客户B|约0.670|26%|第二大客户已具系统性重要性|
|客户C|约0.258|10%|前三家合计72%，仍高度集中|
|其余客户|约0.721|28%|收入增长不能归因于单一客户|

以上百分比按披露四舍五入，因此金额为推算近似数。Q2同比增加1.363B，其中美国增加1.241B，贡献约91.0%；海外增加0.122B，贡献约9.0%。客户A上年同期约0.861B、本期约0.927B，增加约0.066B；其余客户合计增加约1.297B，贡献约95%的增长。**按同一份Q2比较表，增长主要来自大客户A以外；集中度改善不等于客户信用风险消失。**

公司报告一个经营分部，未披露训练/推理、GPU代际、单独软件、GPU小时、客户实际净租金的完整收入表；这些维度保留为数据缺口，而不是用总收入替代分析。客户标签文件明确提示不同期间可能代表不同客户，不擅自把A/B/C命名为微软/OpenAI/Meta。

来源：'''+ref('crwv10q','Q2 10-Q Note 2 p.15、Note 15 p.40')+'''。

### 收入共识要求怎样的下半年？

公开聚合2026年收入共识12.87B，减去已实现H1 4.653B，H2必须产生 **8.217B**，平均每季4.109B，较Q2高59.6%。不是Q3和Q4各自必然达到4.109B，而是两季合计的交付门槛。若Q3环比+30%至3.348B，则Q4需4.870B、环比约+45.5%才能满足全年共识。

RPO预计24个月兑现42.517B意味着平均年额21.259B，比2026共识高，提供中期覆盖；但它不是逐年时间表，不能证明2027收入共识26.34B已被完全锁定。

**股价检验：**收入环比增幅与5日异常收益rho=0.60、p=0.350；active MW增幅rho=0.70、p=0.233，n均为5。方向上与交付改善假说一致，证据强度不足以确认稳定交易规律；没有披露前共识就不能把增长率当“超预期幅度”。

**本层决策：**公司兑现能力在增强，但要维持全年收入共识需要显著加速。下一次财报若只有容量增加、没有收入爬坡和现金改善，应下调兑现速度，而非把新增MW全部资本化到目标价。
</section>
''')
parts.append('<section id="economics">\n\n## 04 · 单位经济与现金：高EBITDA为何没有落到股东手里\n\n'+ref('framework','框架：S1 pp.10–11；S2 p.5；S4 pp.17–22')+'。S2是模型客户的Token经济，不直接当云商毛利。\n\n')
parts.append(table(['季度','Adj EBITDA率','Adj EBIT率','D&A $B','CFO $B','现金PP&E $B','CFO−PP&E $B'],[[q['label'],f"{q['ebitda_margin']:.1%}",f"{q['adjusted_ebit']/q['revenue']:.1%}",num(q['da']),num(q['cfo']),num(q['capex']),num(q['fcf'])] for q in Q]))
parts.append(chart('现金创造与建设付款：季度实际值',[q['label'] for q in Q],[('经营现金流',[q['cfo'] for q in Q]),('现金PP&E付款',[q['capex'] for q in Q]),('两者差额',[q['fcf'] for q in Q])]))
parts.append('''### 利润桥：经营杠杆只在部分成本上出现

|每100美元收入对应成本 / 利润|2025Q2|2026Q2|变化含义|
|---|---:|---:|---|
|Cost of revenue|25.8|34.1|机房/电力等直接支出压力增加|
|Technology & infrastructure|55.3|58.5|包含折旧及研发等，设备资本负担尚未摊薄|
|销售费用|3.0|2.3|规模效应改善|
|管理费用|14.4|6.9|规模效应改善|
|GAAP经营利润|1.6|−1.9|收入翻倍未带来GAAP盈利改善|
|调整后EBITDA|62.1|58.6|仍有现金运营贡献，但同比下滑|
|调整后EBIT|16.5|5.0|折旧后收益显著变弱|
|净利息费用|22.0|24.9|债权人吸收更多收入|

Q2同比收入增加1.362B，调整后EBITDA增加约0.757B，增量EBITDA率约55.6%；调整后EBIT却由0.200B降至0.128B，增量EBIT率约 **−5.3%**。Q2调整后EBIT仅覆盖净利息约0.20倍。EBITDA1.510B减去D&A1.393B只剩约0.117B（与调整后EBIT差异主要是收购无形资产调整），再扣净利息0.640B显著为负。**主要矛盾不是没有运营贡献，而是设备消耗与融资成本吃掉贡献。**

“收入−Cost of revenue”的65.9%不能直接称为扣除设备折旧的经济毛利，因为大量折旧列在Technology & infrastructure。这也是平台67%上下毛利数字容易误导的原因。

### 资产寿命与资本效率：先做公司层交叉检验

- 6月底技术设备原值33.823B，净PP&E46.736B，在建工程11.918B。上半年净PP&E较年初增加16.179B，但H1年化调整后EBIT只有0.298B，对年初/期末平均净PP&E约0.77%；这是简化资本效率代理，**不是完整税后ROIC**。
- CRWV技术设备按6年折旧。若以整个33.823B原值做静态、零残值压力演示，改为4年意味着年化折旧约多2.819B。这不是已预测会计调整，实际需按各批次剩余账面值、剩余寿命和残值重算；它显示项目回报对寿命假设非常敏感。
- NBIS也从2026年起将服务器/网络设备寿命由4年延至5年。不能把两家公司调整后EBIT差异全归为软件优势；需要先把cohort折旧与更新资本开支统一。
- 未披露CRWV逐GPU成本、GPU小时租金、有效计费利用率和残值，因此不能声称已经测得真实GPU项目IRR。先看实际现金与会计利润的差额，再建立有合同输入的项目模型。

来源：'''+ref('crwv10q','Q2 10-Q Note 5及MD&A pp.44–47')+'；'+ref('sec2025-12-31','2025 10-K，技术设备6年折旧')+'；'+ref('nbisq2','NBIS股东信 p.10，寿命调整')+'''。

### 现金质量：预付款和营运资金不能当永久利润

|现金桥 $B|2026Q1|2026Q2|解释|
|---|---:|---:|---|
|CFO|2.984|0.679|环比下降77.2%|
|应收账款现金贡献|+1.042|−0.435|回款时点逆转，差额−1.477B|
|应付及应计费用现金贡献|+0.960|−0.656|付款时点逆转，差额−1.616B|
|递延收入现金贡献|+0.575|+0.790|新收款/履约净变化继续支持现金|
|CFO减递延收入贡献|2.409|−0.111|不是“真实CFO”，是预付款依赖敏感性|
|现金PP&E|7.695|6.422|季度付款下降，但仍远高于CFO|
|CFO/现金PP&E|38.8%|10.6%|外部资金依赖加深|

Q1与Q2现金波动主要受应收/应付时点影响，不能把Q1高CFO简单年化。H1 CFO3.663B中，递延收入净贡献1.365B、应收回款贡献0.607B；同时扣掉这两项后为1.691B，仅覆盖现金PP&E约12.0%。这只是**营运资金来源剥离**，不是断言预付款不可持续。

客户现金收款的一阶估算为收入4.653 + 应收释放0.607 + 递延贡献1.365 = 6.625B；还需扣除合同资产增加、非现金合同调整和收购/汇兑影响，故不作为精确收款额进入偿债模型。H1另有9.796B“设备新增相关负债（含OEM融资）”的非现金披露，现金PP&E不等于全部设备投资。应付采购日程也可能形成融资负担。

**检验与决策：**EBITDA率变动、CFO率变动、capex强度变动均未与5日异常收益形成显著关系（完整结果可切换）。本层对估值的约束仍成立：没有覆盖资产消耗、利息和建设现金需求前，不因59% EBITDA率就给予软件公司倍数；优先验证新增容量的折旧后利润、预付款可退条件和后续回款。
</section>
''')
parts.append('<section id="credit">\n\n## 05 · 信用与融资：把现金来源和刚性支出放到同一时间轴\n\n'+ref('framework','框架：S1 pp.10–11，资金与合同匹配')+'。\n\n')
parts.append('''**结论：信用市场压力显著，但最新申报支持的是“融资与流动性依赖”，不是“已违约”。** 6月底公司披露DDTL契约合规，管理层认为现金及借款能力可满足一年义务；这不是对10月偿付状态的保证。10月21日媒体报CDS约1067bp、无担保债收益率约15%，应触发压力预算，而不是直接换算真实破产概率。

### 资金来源时间表：这次核实了实际提款和可转债交割

|日期 / 期间|资金来源 $B|状态|预算处理|
|---|---:|---|---|
|2026-06-30现金及现金等价物|5.524|资产负债表实际|期初可用现金；另有1.380B受限现金，不加进来|
|2026-06-30短期证券|0.015|实际|假设可变现，单独列示|
|2026-06-30未提款承诺|10.014|公司披露|含RCF约2.0B；提款有条件、项目隔离，不等于现金|
|2026-08 DDTL5.5|2.6额度，已提款1.2|10-Q后续事项确认|新额度另计，未提款余额约1.4B；12月提款期结束|
|2026-08 RCF提款|1.2|10-Q后续事项确认|来自6月原额度，不能再加一次额度|
|2026-09-22可转债|本金4.2；净额4.137|8-K确认完成交割|扣capped call 0.5662后净新增约3.5708B，尚未扣其他发行费用|
|持续经营收款|由CFO情景承接|尚无Q3报表|不把收入、预付款、CFO同时相加|

9月融资不再只引用3.7B定价标题：最终含超额配售的本金为4.2B，2.875%票息、2033-04-01到期、2027-04-01开始半年付息，初始转股价97.85美元。初始潜在转股约42.92M股（当前基本股数的7.8%），但有capped call保护、结算选择和条件；现价低于转股价时不能假定债务已消失，也不能一边全额扣债一边全额稀释。

来源：'''+ref('crwv10q','Q2 10-Q Note 10/16、MD&A流动性')+'；'+ref('sec2026-09-22','9月22日8-K，完成交割及资金用途')+'；'+ref('creditnews','10月21日信用市场报道')+'。\n\n### 已签债务与租赁付款日程\n\n')
parts.append(table(['付款期间','6月底存量债务本金 $B','经营租赁付款 $B','融资租赁含息付款 $B'],[[x['year'],x['principal'],x['op_lease'],x['finance_lease']] for x in D['maturities']]))
parts.append('''本金合计35.551B，**净账面债务为35.068B**（相差0.483B未摊销折价/发行成本）；上一版将本金笼统称为账面债务，本版纠正。表中未包括8月新增提款和9月可转债的未来本金；9月42亿美元到2033年到期，不会挤进2027年本金，但增加每年约0.12075B票息。未来债务变动会改变该表。

经营租赁表为已起租租约；另有约35.5B尚未起租的未折现租赁承诺，预计2026–2029年起租，缺逐年完整付款分布，不能直接加到一年偿付额。应付设备款、建设承诺、担保和税项亦需另建到期表。

### 资金缺口测算：实际日程 + 显式假设

下面是**从6月30日出发的研究者预算，不是10月现金余额或公司指引**。采用CFO法：CFO包含现金利息、经营租赁及客户预付款，因此不重复扣租金/利息、不重复加预付款。融资租赁含息付款作为额外储备保守全扣，可能重复包含小额已在CFO中的租赁利息；明确保留这项保守偏差。

2026H2基准用H1的CFO3.663B和现金PP&E14.117B作为机械延续，另留JV及其他付款1.15B、融资费用0.05B。旧额度10.014B、新DDTL额度2.6B按提款比例计入；8月已提款的2.4B包含在这些额度内。加上9月可转债净额3.5708B。**提款率100%时条件期末现金约5.645B；80%时约3.122B；80%提款且现金PP&E再增加25%时约−0.407B。** 基准并不证明即将断流，联合压力显示融资可用性与付款速度很重要。

2027行接续上期余额；默认CFO8B、现金PP&E20B、额外融资20B、其他用途1B均为情景输入；本金6.184B来自已披露日程。2027新增债务的摊还、增量利息和新起租租金需纳入CFO/本金输入，未披露部分不能由本表“自动证明安全”。

<div id="cashModel"></div>

**可执行判断：**仅看55亿美元现金会低估已承诺融资，看155亿美元“流动性”又会高估无条件可用资金。应逐项目核对提款先决条件、担保、现金隔离和客户预付款退款义务。10月底需取得Q3现金及未提款余额才能把这一预算滚到当下；CDS升高时，优先压测80%提款、延迟回款和高价增发，而不是以有RPO为由忽略资金约束。
</section>
''')
parts.append('<section id="valuation">\n\n## 06 · 股东价值：相对贵贱、隐含增长与融资后的每股回报\n\n'+ref('framework','框架：S1 p.2及pp.10–11；估值反推为新增')+'。\n\n### 同期股价、明确预测期间的可比估值\n\n')
parts.append(table(['公司','10/21收盘 $','市值 $B','EV $B（供应商）','第一预测年收入 $B','第二预测年收入 $B','EV/第一年','EV/第二年','两年间增长'],[[p['symbol'],p['price'],p['marketcap'],p['vendor_ev'],p['fy0']+' / '+str(p['rev0']),p['fy1']+' / '+str(p['rev1']),f"{p['ev_sales0']:.2f}×",f"{p['ev_sales1']:.2f}×",pct(p['growth'])] for p in D['peers']]))
parts.append('''CRWV与NBIS均为12月年结，可直接比较同一2027预测年度：CRWV 3.04×、NBIS 4.00×，CRWV折价约24.0%。**这是相对收入倍数便宜，不等于风险调整后便宜。** NBIS预计2027增长约268%，CRWV约105%；负债、预付款、非核心股权和租赁负担也不同。

IREN是6月年结，表中2027财年只到2027年6月，不冒充CRWV的2027日历年；其FY2026收入约81.8%来自挖矿。用集团EV除AI收入会把矿业/地产价值全压到AI业务上。若仅作线性日历化示例，CY2027收入≈(FY2027 2.81 + FY2028 7.41)/2=5.11B，EV/S≈2.53×，但交付高度后置，真实日历化必须用季度预测。因此**不以2.53×对IREN做正式便宜排名**。

公开预测为StockAnalysis展示的S&P Global聚合值：CRWV 40名收入预测分析师、NBIS21名、IREN17名；CRWV/NBIS页面更新10月21日，IREN9月29日。2027预测的独立样本数与完整分歧区间未公开。本表使用公开页面的年度字段，未将NTM forward P/S倒算成日历年预测。各公司GAAP EBIT为负，当前EV/EBIT均不具备“低倍数”含义；供应商TTM EBITDA也不是公司Adjusted EBITDA。
'''+ '；'.join(ref(p['source_stats'],p['symbol']+'统计')+' / '+ref(p['source_forecast'],'预测') for p in D['peers'])+'。\n\n')
parts.append('''### CRWV估值分子的桥：租赁处理会改变“便宜”的幅度

|EV口径，以10/21市值搭配最近报表|计算 $B|2027E EV/Sales|使用限制|
|---|---:|---:|---|
|供应商含租赁近似|80.12|3.04×|三家均先使用同一供应商，仍有会计差异|
|6月底报告口径、排经营租赁|34.10+35.068+0.221−5.524−0.015=63.850|2.42×|保留经营租金为成本；不是10月完整净债务|
|以上加回经营租赁负债|63.850+16.319=80.169|3.04×|与供应商差异为精度/分类；EBITDA比较须配套租金处理|
|只调整已知9月融资费用影响|63.850+4.2−3.5708≈64.479|2.45×|假设净融资款尚未使用；不是当前真实EV|

8月借款在到账瞬间增加现金和债务，对净债务大致中性；其后建设支出、CFO、债务偿还和资本化租赁会改变净债务。不能把4.2B本金全部加债、却忽略融资现金，也不能忽略后续烧钱。

### 现价到底price in多少增长？

先给一个可复算的**条件解**，不是从股价中唯一识别“市场信念”。设一年后目标回报12%、届时股数600M、净债务45B（排经营租赁）、退出EV/EBIT 15×、可持续EBIT率20%。则：

`所需2027收入 = (现价61.82 × 600M × 1.12 + 45B) / (15 × 20%) = 28.848B`

这要求较2026共识12.87B增长约124.1%，比2027共识26.34B再高约9.5%。若收入恰好达到26.34B，则同样条件需要EBIT率约21.9%，或EV/EBIT约16.43×，才达到12%回报。当前季度GAAP EBIT率为−1.9%、调整后约5.0%，所以反推的利润率改善幅度相当大。

再看一个偏乐观口径：用报告期EV63.850B除2027收入26.34B，仅2.42×销售额，看起来便宜；但该比值没有为未来建设融资、股数增加和要求回报支付代价。两者并不矛盾。

<div id="valuationModel"></div>

### 三种经营 / 融资组合对每股价值的影响

以下均为一年后条件值，不是目标价；净债务排经营租赁、EBIT扣经营租金。收入之外的假设是FREERIDE情景，不冒充共识。还需要项目现金流估值交叉验证，避免终值倍数掩盖维护Capex。
''')
scens=[('压力',20,.12,12,55,.65),('共识收入 / 中性资本结构',26.34,.20,15,45,.60),('强交付 / 高利润率',30,.25,18,40,.58)]
parts.append(table(['情景','2027收入 $B','EBIT率','EV/EBIT','净债务 $B','股数 B','一年后每股条件值 $','相对61.82'],[[name,rev,f'{mar:.0%}',mult,nd,sh,f'{max(0,(rev*mar*mult-nd)/sh):.2f}',pct(max(0,(rev*mar*mult-nd)/sh)/61.82-1)] for name,rev,mar,mult,nd,sh in scens]))
parts.append('''**结论：**共识收入+20% EBIT率+15×退出倍数+45B净债务+600M股，条件值约56.70美元，低于现价61.82；在这组假设下并不便宜。上行情景要求交付、利润率、融资和估值四项共同改善。现价是否有吸引力，核心争议是未来EBIT率与资本需求，而非“收入倍数低于NBIS”这一条。

**使我转向更积极的证据：**Q3/Q4交付足以满足8.217B的H2收入门槛；近端RPO兑现继续改善；剔除预付款净贡献后CFO改善；12个月资金表在较低提款率下仍保留缓冲；同口径利润率与资本结构使共识收入情景可以达到要求回报。**使我下调的证据：**验收延期、项目资金无法互用、融资净成本增加、寿命/残值下修或以更大股数弥补资金缺口。
</section>
''')
parts.append('''<section id="audit">

## 检验审计与下次更新：把研究判断与统计证据分开

以下为CRWV、QQQ基准、5日市场模型异常收益。全股票、窗口、基准结果已保存为JSON，事件浏览器可切换。全检验Holm校正避免对多个指标逐个试到显著；p值不是因果概率。
'''+table(['解释变量变化','n','Pearson','Spearman','原始精确p','全检验Holm p','留一法rho范围'],[statrow(x) for x in ['rpo','backlog','revenue','active_mw','ebitda_margin','cash_margin','capex_intensity']])+'''
**方法边界：**事件行情序列截至2026-10-20；估值另用10/21收盘报价。指标增长率和股票收益率做相关，避免趋势水平伪相关；市场模型用事前120至21交易日、至少40条，无法消除行业/公司事件混杂。RPO申报日可能晚于财报；容量约数和会计定义变化影响解释。5条季度变化/4条Anthropic增长样本远不足以估计多变量稳定因子，未做样本外预测。相关性不显著不否定会计约束，但意味着不能声称该指标已被验证为选股信号。

与旧版检验的差别：旧版用下一交易日收盘后漂移；本版依用户要求加入公告反应窗口和事前beta调整，两者研究的问题不同，不能把结果变化当成模型提升。未知公告小时的1日口径实际涵盖公告日及次日，页面明确显示起止日期；它不是可交易回测收益。

### 更新清单与触发条件

|数据|更新动作|何时改变模型|
|---|---|---|
|Anthropic官方收入/媒体新数据|全新闻扫描、主体与实际/预测复核；保留首次来源时间|改变需求情景，不直接按比例上调CRWV|
|CRWV Q3财报|预计11/9，等待IR确认；提取RPO、24月兑现、收入/容量与现金|重估全年12.87B共识实现概率|
|融资与债务|监控8-K，确认到账、费用、capped call、提款条件|更新月度可用现金、净债务和稀释|
|同业与一致预期|保存同日价格和预测版本，统一财年/业务口径|重算相对倍数及反推增长|
|样本增加|使用既定协议加入全部新事件，不根据涨跌挑选|只有样本与样本外证据足够才考虑信号化|

自动化边界：本页是审核后的研究快照，刷新网页不会产生实时抓取；公开脚本重算全部相关性和情景，数据更新仍需采集与语义复核。本次官网全目录采集、SEC和价格抓取已实际执行，成功/失败状态及哈希保存在数据来源清单；原始研报和整篇新闻不公开再分发。

- [探索性检验预登记](references/deep-dive-protocol.md)
- [机构原框架与页码](references/institutional-frameworks.html)
- [原始框架逻辑审计](references/framework-audit.html)
- [重算脚本](https://github.com/Lancewang1/project-freeride-neocloud-demo/tree/main/scripts)
- [完整GitHub仓库](https://github.com/Lancewang1/project-freeride-neocloud-demo)

</section>
''')
text='\n'.join(parts)
(R/'coreweave-deep-dive.md').write_text(text,encoding='utf8')
body=markdown.markdown(text.replace('<section id=', '<section markdown="1" id='),extensions=['tables','fenced_code','md_in_html'])
body=body.replace('<table>','<div class="tablewrap"><table>').replace('</table>','</table></div>')
nav=''.join(f'<a href="#{i}">{label}</a>' for i,label in [('demand','01 终端需求'),('contracts','02 业务获取'),('delivery','03 交付兑现'),('economics','04 经济与现金'),('credit','05 偿付时间表'),('valuation','06 贵贱与隐含增长'),('audit','检验与更新')])
page='<!doctype html><html lang="zh-CN"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>FREERIDE · CoreWeave 深度投研：需求、偿付与隐含增长</title><link rel="stylesheet" href="deep-case.css"></head><body><header><b>PROJECT FREERIDE</b><span>NEOCLOUD / RESEARCH NOTE 02</span></header><div class="shell"><nav>'+nav+'</nav><main>'+body+'</main></div><script id="researchData" type="application/json">'+json.dumps(D,ensure_ascii=False).replace('</','<'+chr(92)+'/')+'</script><script id="analysisData" type="application/json">'+json.dumps(A,ensure_ascii=False).replace('</','<'+chr(92)+'/')+'</script><script src="deep-case.js"></script></body></html>'
(R/'index.html').write_text(page,encoding='utf8')
print('Rendered deep case:',len(text),'characters')

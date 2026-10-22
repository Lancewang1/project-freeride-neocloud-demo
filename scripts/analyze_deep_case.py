"""Reproduce exploratory event analysis from the published normalized data.
Dependencies: numpy, scipy. No credentials or private files.
"""
from pathlib import Path
import json,itertools,bisect,math
import numpy as np
from scipy.stats import spearmanr,pearsonr,rankdata
R=Path(__file__).resolve().parents[1]
D=json.loads((R/'data/deep-research.json').read_text(encoding='utf8'))
prices={s:{x['date']:x['close'] for x in rows} for s,rows in D['prices'].items()}
def reaction(symbol,date,bench,h,after_close=False):
 dates=sorted(set(prices[symbol])&set(prices[bench]));idx=bisect.bisect_left(dates,date)
 if idx>=len(dates):return None
 # Unknown time: prior close to next trading-day close. Known post-close: release close onward.
 anchor=idx if after_close and dates[idx]==date else idx-1
 end=idx+h if dates[idx]==date else idx+h-1
 if anchor<0 or end>=len(dates):return None
 rs=np.array([prices[symbol][dates[i]]/prices[symbol][dates[i-1]]-1 for i in range(1,len(dates))])
 rb=np.array([prices[bench][dates[i]]/prices[bench][dates[i-1]]-1 for i in range(1,len(dates))])
 train_start=max(1,idx-120);train_end=max(1,idx-20)
 x=rb[train_start-1:train_end-1];y=rs[train_start-1:train_end-1]
 raw=prices[symbol][dates[end]]/prices[symbol][dates[anchor]]-1
 br=prices[bench][dates[end]]/prices[bench][dates[anchor]]-1
 out={'symbol':symbol,'date':date,'benchmark':bench,'horizon':h,'anchor':dates[anchor],'exit':dates[end],'raw':raw,'benchmark_return':br,'excess':raw-br,'car':None,'z':None,'beta':None,'training_n':len(x),'window_days':end-anchor}
 if len(x)>=40:
  beta,alpha=np.polyfit(x,y,1);res=y-alpha-beta*x;sigma=np.std(res,ddof=2)
  expected=np.prod(1+alpha+beta*rb[anchor:end])-1
  car=raw-expected
  out.update(car=float(car),z=float(car/(sigma*np.sqrt(end-anchor))) if sigma>0 else None,beta=float(beta),alpha=float(alpha))
 return out
events=[]
primary=[x for x in D['anthropic'] if x['event']]
for j,a in enumerate(primary):
 for s in ['CRWV','NBIS','IREN']:
  for b in ['QQQ','SMH']:
   for h in [1,5,20]:
    v=reaction(s,a['published'],b,h)
    if v:events.append(dict(series='Anthropic',value=a['value'],change=None if j==0 else a['value']/primary[j-1]['value']-1,source=a['source'],**v))
metrics=['rpo','backlog','revenue','active_mw','ebitda_margin','cash_margin','capex_intensity']
for metric in metrics:
 for j,q in enumerate(D['quarters']):
  if j==0:continue
  prev=D['quarters'][j-1][metric];change=q[metric]-prev if metric.endswith('margin') or metric=='capex_intensity' else q[metric]/prev-1
  date=q['rpo_published'] if metric=='rpo' else q['published']
  for b in ['QQQ','SMH']:
   for h in [1,5,20]:
    v=reaction('CRWV',date,b,h,metric!='rpo')
    if v:events.append(dict(series=metric,value=q[metric],change=change,source='facts' if metric=='rpo' else q['source'],**v))
def stats(rows):
 xy=[(x['change'],x['car']) for x in rows if x['change'] is not None and x['car'] is not None]
 if len(xy)<4:return {'n':len(xy),'rho':None,'pearson':None,'p':None}
 x,y=map(np.array,zip(*xy));rho=float(spearmanr(x,y).statistic);pear=float(pearsonr(x,y).statistic)
 xr=rankdata(x);yr=rankdata(y);xr=(xr-xr.mean())/np.linalg.norm(xr-xr.mean());yr=(yr-yr.mean())/np.linalg.norm(yr-yr.mean())
 dist=np.array([np.dot(xr,v) for v in itertools.permutations(yr)])
 p=float(np.mean(np.abs(dist)>=abs(rho)-1e-10))
 loo=[float(spearmanr(np.delete(x,i),np.delete(y,i)).statistic) for i in range(len(x))]
 return {'n':len(x),'rho':rho,'pearson':pear,'p':p,'leave_one_rho':[min(loo),max(loo)],'mean_car':float(y.mean())}
summary=[]
for series in ['Anthropic']+metrics:
 for s in (['CRWV','NBIS','IREN'] if series=='Anthropic' else ['CRWV']):
  for b in ['QQQ','SMH']:
   for h in [1,5,20]:
    st=stats([v for v in events if v['series']==series and v['symbol']==s and v['benchmark']==b and v['horizon']==h])
    summary.append(dict(series=series,symbol=s,benchmark=b,horizon=h,**st))
for series in ['Anthropic']+metrics:
 rows=sorted([r for r in summary if r['series']==series and r['p'] is not None],key=lambda r:r['p']);last=0
 for i,row in enumerate(rows):last=max(last,min(1,row['p']*(len(rows)-i)));row['p_holm']=last
# A second correction across all planned tests avoids giving seven quarterly metrics separate chances.
rows=sorted([r for r in summary if r['p'] is not None],key=lambda r:r['p']);last=0
for i,row in enumerate(rows):last=max(last,min(1,row['p']*(len(rows)-i)));row['p_holm_all']=last
top=[]
for s in ['CRWV','NBIS','IREN']:
 for h in [1,5,20]:
  vals=[e for e in events if e['series']=='Anthropic' and e['symbol']==s and e['benchmark']=='QQQ' and e['car'] is not None and e['horizon']==h]
  if vals:top.append(max(vals,key=lambda e:abs(e['car'])))
result={'method':'references/deep-dive-protocol.md','events':events,'summary':summary,'largest_observed_reaction':top,'limitations':['Five official new-high events; four growth pairs. Threshold growth is not exact growth.','Price reaction includes co-announced financing, partnerships and earnings; not a causal estimate.','Unknown publication hours use wide reaction windows, not tradable drift.','RPO first confirmed SEC release may follow prior earnings/backlog disclosure.','No out-of-sample or contemporaneous consensus surprises; current webpage reconstruction.']}
(R/'data/deep-analysis.json').write_text(json.dumps(result,ensure_ascii=False,indent=2,allow_nan=False),encoding='utf8')
for x in top:
 if x['horizon']==5:print(x['symbol'],x['date'],'CAR',round(x['car']*100,2),'z',round(x['z'],2))
for x in summary:
 if x['benchmark']=='QQQ' and x['horizon']==5:print(x['series'],x['symbol'],x['n'],round(x['rho'],3),round(x['p'],3),round(x['p_holm_all'],3))

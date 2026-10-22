"""Refresh public evidence into an ignored local cache; never auto-promote values.
Requires requests and beautifulsoup4. Publisher originals stay out of git.
"""
from pathlib import Path
import argparse,json,hashlib,datetime,concurrent.futures,re
import xml.etree.ElementTree as ET
import requests
from bs4 import BeautifulSoup
R=Path(__file__).resolve().parents[1]
def main():
 p=argparse.ArgumentParser();p.add_argument('--scope',choices=['anthropic','financial','all'],default='anthropic');args=p.parse_args()
 cache=R/'.research-cache';cache.mkdir(exist_ok=True)
 old=json.loads((R/'data/deep-research.json').read_text(encoding='utf8'))['sources'];known={v['url']:v.get('sha256') for v in old.values()};urls=set()
 if args.scope in ['anthropic','all']:
  r=requests.get('https://www.anthropic.com/sitemap.xml',timeout=30);r.raise_for_status()
  urls.update(x.text for x in ET.fromstring(r.content).iter() if x.tag.endswith('loc') and '/news/' in (x.text or ''))
 if args.scope in ['financial','all']:
  urls.update(v['url'] for v in old.values() if any(k in v['url'] for k in ['companyfacts/','stockanalysis.com/stocks/','finance/chart/']))
  urls.add('https://investors.coreweave.com/feed/PressRelease.svc/GetPressReleaseList?LanguageId=1&pageSize=100&pageNumber=0')
 def fetch(u):
  item={'url':u,'retrieved_at':datetime.datetime.now(datetime.timezone.utc).isoformat()}
  try:
   r=requests.get(u,timeout=35,headers={'User-Agent':'Mozilla/5.0 FREERIDE public research'});item['status']=r.status_code;r.raise_for_status()
   digest=hashlib.sha256(r.content).hexdigest();item['sha256']=digest;item['changed']=known.get(u)!=digest;(cache/(digest+'.raw')).write_bytes(r.content)
   if 'anthropic.com/news/' in u:
    text=BeautifulSoup(r.content,'html.parser').get_text(' ',strip=True)
    item['candidate_passages']=re.findall(r'.{0,90}(?:run.rate|annualized revenue|revenue.{0,30}billion).{0,180}',text,re.I)
    item['requires_review']=bool(item['candidate_passages']) and item['changed']
  except Exception as e:item['error']=str(e)
  return item
 results=list(concurrent.futures.ThreadPoolExecutor(6).map(fetch,sorted(urls)))
 (cache/'latest-review.json').write_text(json.dumps(results,indent=2,ensure_ascii=False),encoding='utf8')
 print(json.dumps({'fetched':len(results),'errors':sum('error' in r for r in results),'review_candidates':sum(r.get('requires_review',False) for r in results),'output':'.research-cache/latest-review.json'}))
if __name__=='__main__':main()

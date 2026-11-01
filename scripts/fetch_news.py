import json,re,html,urllib.request,xml.etree.ElementTree as ET
from email.utils import parsedate_to_datetime
B='https://news.google.com/rss'
F=[('en','top',B+'?hl=en-IN&gl=IN&ceid=IN:en'),('en','india',B+'/headlines/section/geo/India?hl=en-IN&gl=IN&ceid=IN:en'),('en','world',B+'/headlines/section/topic/WORLD?hl=en-IN&gl=IN&ceid=IN:en'),('en','politics',B+'/search?q=politics+india&hl=en-IN&gl=IN&ceid=IN:en'),('hi','top',B+'?hl=hi&gl=IN&ceid=IN:hi')]
def strip(t):return re.sub(r'\s+',' ',html.unescape(re.sub(r'<[^>]+>',' ',t or ''))).strip()
out={}
for lang,topic,u in F:
  try:
    x=ET.fromstring(urllib.request.urlopen(urllib.request.Request(u,headers={'User-Agent':'Mozilla/5.0'}),timeout=20).read())
  except Exception as e:print(u,e);continue
  for i in x.iter('item'):
    src=i.findtext('source') or '';t=re.sub(r' - [^-]+$','',i.findtext('title') or '')
    if not t or t in out:continue
    try:d=parsedate_to_datetime(i.findtext('pubDate')).isoformat()
    except Exception:continue
    sm=strip(i.findtext('description')).replace(t,'').replace(src,'').strip()
    out[t]=dict(title=t,source=src,summary=sm,link=i.findtext('link'),pubDate=d,lang=lang,topic=topic)
it=sorted(out.values(),key=lambda a:a['pubDate'],reverse=True)
hi=[a for a in it if a['lang']=='hi'][:15];en=[a for a in it if a['lang']=='en'][:60-len(hi)]
res=sorted(en+hi,key=lambda a:a['pubDate'],reverse=True)
if res:open('news.json','w').write(json.dumps(res,ensure_ascii=False,indent=0))

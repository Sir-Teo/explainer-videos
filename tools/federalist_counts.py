"""Build explainer/stats/data/federalist_counts.json from Project Gutenberg's *The Federalist Papers* (ebook 18).

    curl -sSL -o fed.txt https://www.gutenberg.org/cache/epub/18/pg18.txt
    python tools/federalist_counts.py fed.txt explainer/stats/data/federalist_counts.json

For each of the 85 papers: its number, the author line Gutenberg prints, the number of words in the body, and the
counts of Mosteller & Wallace's 70 function words plus some of their marker words.  Part 19 of *Statistics, Built*
uses it; the Museum (``museum.federalist()``) applies the standard attribution (12 disputed papers: 49-58, 62, 63).
"""
import re, json, sys
txt=open(sys.argv[1], encoding='utf-8').read()
end=txt.find('*** END OF THE PROJECT GUTENBERG')
txt=txt[:end]
parts=re.split(r'\nTHE FEDERALIST\.\s*\n', txt)[1:]
roman={'I':1,'V':5,'X':10,'L':50,'C':100}
def r2i(s):
    t=0
    for a,b in zip(s, s[1:]+' '):
        v=roman[a]; t+= -v if b!=' ' and roman.get(b,0)>v else v
    return t
FW=("a all also an and any are as at be been but by can do down even every for from had has have her his if in into is it its "
    "may more must my no not now of on one only or our shall should so some such than that the their then there things this to up "
    "upon was were what when which who will with would your").split()
EXTRA="whilst while although though enough both always commonly consequently considerable according apt direction innovation language vigor kind matter particularly probability work".split()
papers=[]
for p in parts:
    m=re.match(r'\s*No\.\s*([IVXLC]+)\.', p)
    if not m: continue
    num=r2i(m.group(1))
    am=re.search(r'\n(HAMILTON AND MADISON|HAMILTON OR MADISON|MADISON, with HAMILTON|HAMILTON|MADISON|JAY)\s*\n', p[:800])
    author=am.group(1) if am else '?'
    body=p[am.end():] if am else p
    words=re.findall(r"[a-z]+", body.lower())
    cnt={w:0 for w in FW+EXTRA}
    for w in words:
        if w in cnt: cnt[w]+=1
    papers.append({"no":num,"author":author,"n_words":len(words),"counts":cnt})
seen={}
for p in papers:
    seen.setdefault(p["no"],[]).append(p)
out=[v[0] for k,v in sorted(seen.items())]
print(len(papers), len(out), sorted(set(p['author'] for p in out)))
from collections import Counter; print(Counter(p['author'] for p in out))
print([p['no'] for p in out if p['author']=='HAMILTON OR MADISON'], [p['no'] for p in out if 'AND' in p['author']], [p['no'] for p in out if p['author']=='JAY'])
json.dump({"function_words":FW,"extra_words":EXTRA,"papers":out}, open(sys.argv[2],'w'))

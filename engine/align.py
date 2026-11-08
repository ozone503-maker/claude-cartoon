import json,re,sys
# usage: align.py silfile end transcriptfile out.json
sil=[tuple(map(float,l.split())) for l in open(sys.argv[1])]; END=float(sys.argv[2])
txt=open(sys.argv[3]).read().replace('—',' — ')
sp=[];t=0.0
for a,b in sil:
    if a>t: sp.append((t,a))
    t=b
if t<END: sp.append((t,END))
toks=txt.split()
ph=[];cur=[]
for x in toks:
    if x=='—':
        if cur: ph.append(cur);cur=[]
        continue
    cur.append(x)
    if re.search(r'[,.?!:]$',x): ph.append(cur);cur=[]
if cur: ph.append(cur)
cl=lambda ws:sum(len(re.sub(r'[^A-Za-z0-9]','',w))+1.5 for w in ws)
C=[cl(p) for p in ph]; D=[b-a for a,b in sp]
rate=sum(D)/sum(C)
M,N=len(sp),len(ph); INF=1e18
f=[[INF]*(N+1) for _ in range(M+1)]; bk=[[None]*(N+1) for _ in range(M+1)]; f[0][0]=0
for i in range(M):
    for j in range(N):
        if f[i][j]>=INF: continue
        for di in range(1,4):
            for dj in range(1,6):
                if i+di>M or j+dj>N: continue
                d=sum(D[i:i+di]); c=sum(C[j:j+dj])*rate
                cost=f[i][j]+(d-c)**2/max(c,.3)+0.04*(di-1)+0.02*(dj-1)
                if cost<f[i+di][j+dj]: f[i+di][j+dj]=cost; bk[i+di][j+dj]=(i,j)
i,j=M,N; groups=[]
while (i,j)!=(0,0):
    pi,pj=bk[i][j]; groups.append((pi,i,pj,j)); i,j=pi,pj
groups.reverse()
words=[]
for si,se,pi,pe in groups:
    ivs=sp[si:se]; ws=[w for p in ph[pi:pe] for w in p]
    tot=sum(b-a for a,b in ivs); W=cl(ws); acc=0
    for w in ws:
        pos=acc/W*tot; acc+=cl([w])
        for a,b in ivs:
            if pos<=b-a+1e-9: words.append([w,round(a+pos,2)]); break
            pos-=b-a
json.dump(words,open(sys.argv[4],'w'))
for si,se,pi,pe in groups: print(round(sp[si][0],2),' '.join(w for p in ph[pi:pe] for w in p))

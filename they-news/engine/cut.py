from PIL import Image; import numpy as np, glob, os
from scipy import ndimage as nd
import os
HERE=os.path.dirname(os.path.abspath(__file__))
SRC=os.path.join(HERE,'..','..','art','they-live'); OUT=os.path.join(HERE,'..','cuts'); os.makedirs(OUT, exist_ok=True)
def cells(a):
    H,W=a.shape[:2]; lum=a.mean(2); out=[]
    for r in range(2):
        for c in range(4):
            x0,x1=int(c*W/4),int((c+1)*W/4); y0,y1=int(r*H/2),int((r+1)*H/2)
            dk=lum[y0:y1,x0:x1]<70
            rows=np.where(dk.mean(1)>.55)[0]; cols=np.where(dk.mean(0)>.55)[0]
            hh,ww=dk.shape
            top=max([v for v in rows if v<hh*.25],default=0); bot=min([v for v in rows if v>hh*.75],default=hh-1)
            lef=max([v for v in cols if v<ww*.25],default=0); rig=min([v for v in cols if v>ww*.75],default=ww-1)
            out.append((x0+lef,y0+top,x0+rig,y0+bot))
    return out
for f in sorted(g for g in glob.glob(SRC+'/*.webp') if 'redo' not in g):
    name=os.path.basename(f)[:-5]; im=Image.open(f).convert('RGB'); a=np.asarray(im)
    base=int(name.split('-')[-2])
    for k,(x0,y0,x1,y1) in enumerate(cells(a)):
        n=base+k; ins=12
        crop=a[y0+ins:y1-ins,x0+ins:x1-ins]
        tag=name.rsplit('-',2)[0]
        if not tag.startswith('fullbody'):
            Image.fromarray(crop).save(f'{OUT}/{tag}-{n:02d}.png'); continue
        # cutout: background = similar to corner color, connected to edges
        ring=np.concatenate([crop[:6].reshape(-1,3),crop[-6:].reshape(-1,3),crop[:,:6].reshape(-1,3),crop[:,-6:].reshape(-1,3)])
        bg=np.median(ring,0)
        d=np.abs(crop.astype(int)-bg).max(2); cand=d<22
        lab,_=nd.label(cand); edge=set(np.unique(np.concatenate([lab[0],lab[-1],lab[:,0],lab[:,-1]])))-{0}
        bgm=np.isin(lab,list(edge)); fg=~bgm
        fg=nd.binary_opening(fg,iterations=1); fg=nd.binary_fill_holes(fg)
        if '-man' in tag:
            tight=np.abs(crop.astype(int)-bg).max(2)<10; lt,_=nd.label(tight)
            sz=nd.sum(tight,lt,range(1,lt.max()+1)); fg&=~np.isin(lt,[i+1 for i,v in enumerate(sz) if v>400])
        if '-man' in tag or '-woman' in tag:
            hh=crop.shape[0]; lum=crop.mean(2); sat=crop.max(2).astype(int)-crop.min(2)
            light=(lum>150)&(sat<25); light[:int(hh*0.55)]=False
            l2,_=nd.label(light); s2=nd.sum(light,l2,range(1,l2.max()+1)); fg&=~np.isin(l2,[i+1 for i,v in enumerate(s2) if v>120])
        lab2,nl=nd.label(fg)
        if nl>1:
            sz=nd.sum(fg,lab2,range(1,nl+1)); keep=[i+1 for i,s in enumerate(sz) if s>0.15*sz.max()]; fg=np.isin(lab2,keep)
        al=(nd.gaussian_filter(fg.astype(float),0.7)*255).astype(np.uint8)
        rgba=np.dstack([crop,al]); ys,xs=np.where(fg)
        rgba=rgba[ys.min():ys.max()+1,xs.min():xs.max()+1]
        Image.fromarray(rgba).save(f'{OUT}/{tag}-{n:02d}.png')
print(len(os.listdir(OUT)))

import sys; sys.path.insert(0,'/home/claude/claude-cartoon/they-news/engine')
from engine import *
S=1080; rng=np.random.default_rng(7)
# color world (left) and bw world (right)
col=Image.new('RGB',(S,S),(28,40,66)); d=ImageDraw.Draw(col)
for r in range(900,0,-30): d.ellipse((300-r,380-r,300+r,380+r),fill=(int(28+(900-r)*.06),int(40+(900-r)*.05),int(66+(900-r)*.07)))
bw=Image.new('RGB',(S,S),(30,30,30)); bd=ImageDraw.Draw(bw)
for k in range(0,S*2,26): bd.line((k,0,k-S,S),fill=(48,48,48),width=10)
# jessie face huge, full bleed
src=load('jessie-cool-glasses-lowered-05').convert('RGBA'); s_=min(src.size)
src=src.crop(((src.width-s_)//2,(src.height-s_)//2,(src.width+s_)//2,(src.height+s_)//2)).resize((900,900),Image.LANCZOS)
# remove light grey bg of portrait
arr=np.array(src).astype(np.int16); bgc=np.array([215,213,209]); dist=np.abs(arr[:,:,:3]-bgc).sum(2); dist[arr[:,:,:3].min(2)>245]=0
from scipy import ndimage
mask=(dist<45); lab,n=ndimage.label(mask); edge=set(lab[0,:].tolist())|set(lab[:,0].tolist())|set(lab[:,-1].tolist()); edge.discard(0)
bgm=np.isin(lab,list(edge)); alpha=np.where(bgm,0,255).astype(np.uint8)
src.putalpha(Image.fromarray(alpha).filter(ImageFilter.GaussianBlur(1.2)))
# alien
a=load('fullbody-alien-man-10'); a=a.crop(a.getbbox()); a=a.crop((0,0,a.width,int(a.height*.5)))
sc=820/a.height; a=a.resize((int(a.width*sc),int(a.height*sc)),Image.LANCZOS)
a=Image.merge('RGBA',(*to_bw(a.convert('RGB')).split(),a.split()[3]))
bw.paste(a,(S-a.width+120,90),a)
# diagonal split
m=Image.new('L',(S,S),0); ImageDraw.Draw(m).polygon([(0,0),(700,0),(520,S),(0,S)],fill=255)
im=bw.copy(); im.paste(col,(0,0),m)
im.paste(src,(-170,60),src)
# halftone
ht=Image.new('RGBA',(S,S),(0,0,0,0)); hd=ImageDraw.Draw(ht)
for y in range(0,S,8):
    off=(y//8%2)*4
    for x in range(0,S+8,8):
        r=1+2.2*(y/S); hd.ellipse((x+off-r,y-r,x+off+r,y+r),fill=(0,0,0,55))
im.paste(ht,(0,0),ht)
# split line
d=ImageDraw.Draw(im); d.line((700,0,520,S),fill=(240,236,225),width=10); d.line((712,0,532,S),fill=(0,0,0),width=6)
# vignette
v=Image.new('L',(S,S),0); ImageDraw.Draw(v).ellipse((-200,-200,S+200,S+200),fill=255); v=v.filter(ImageFilter.GaussianBlur(120))
im=Image.composite(im,Image.new('RGB',(S,S),(0,0,0)),v)
# word blocks, staggered and tilted
words=["PUT","ON","THE","GLASSES"]; f=F(ANTON,118)
x=40; y=800
for i,w in enumerate(words):
    tw=ImageDraw.Draw(im).textlength(w,font=f); pw,ph=int(tw+44),150
    blk=Image.new('RGBA',(pw+24,ph+24),(0,0,0,0)); bd2=ImageDraw.Draw(blk)
    bd2.rectangle((14,16,pw+14,ph+16),fill=(0,0,0,140)); bd2.rectangle((4,4,pw+4,ph+4),fill=(8,8,8),outline=(245,240,225),width=5)
    bd2.text((4+pw/2,4+ph/2),w,font=f,fill=(255,255,255),anchor='mm')
    blk=blk.rotate([-3,2,-2,3][i],resample=Image.BICUBIC,expand=True)
    im.paste(blk,(int(x),int(y+[0,14,-6,8][i])),blk); x+=pw-2
# grain
g=(np.random.default_rng(1).normal(0,9,(S,S,1))).astype(np.int16)
arr=np.clip(np.array(im).astype(np.int16)+g,0,255).astype(np.uint8); im=Image.fromarray(arr)
im.save('tue night put on the glasses logo.png'); im.resize((540,540)).save('/tmp/l9.jpg')

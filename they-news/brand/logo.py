import sys; sys.path.insert(0,'/home/claude/claude-cartoon/they-news/engine')
from engine import *
S=1080
def build(jpose, apose, seed, out):
    bg = Image.new('RGB',(S,S),(14,14,16)); d=ImageDraw.Draw(bg)
    for i,x in enumerate(range(0,S,120)): d.rectangle((x,0,x+115,S),fill=(30,30,34) if i%2 else (24,24,28))
    cone=Image.new('L',(S,S),0); ImageDraw.Draw(cone).polygon([(470,0),(610,0),(900,S),(180,S)],fill=50)
    bg.paste((230,230,240),(0,0),cone.filter(ImageFilter.GaussianBlur(40)))
    ht=Image.new('RGBA',(S,S),(0,0,0,0)); hd=ImageDraw.Draw(ht)
    for y in range(0,S,9):
        off=(y//9%2)*4.5
        for x in range(0,S+9,9): hd.ellipse((x+off-1.6,y-1.6,x+off+1.6,y+1.6),fill=(0,0,0,45))
    bg.paste(ht,(0,0),ht)
    # alien upper body, right
    a=load(apose); a=a.transpose(Image.FLIP_LEFT_RIGHT)
    bb=a.getbbox(); a=a.crop((bb[0],bb[1],bb[2],bb[1]+int((bb[3]-bb[1])*.5))); sc=760/a.height; a=a.resize((int(a.width*sc),int(a.height*sc)),Image.LANCZOS)
    a=Image.merge('RGBA',(*to_bw(a.convert('RGB')).split(),a.split()[3]))
    al=np.array(a.split()[3]).astype(np.float32); n=180; al[-n:]*=np.linspace(1,0,n)[:,None]; a.putalpha(Image.fromarray(al.astype(np.uint8)))
    bg.paste(a,(S-a.width+30, 60),a)
    # jessie circle left
    r=215; cx,cy=350,380
    src=load(jpose).convert('RGB'); s_=min(src.size)
    src=src.crop(((src.width-s_)//2,(src.height-s_)//2,(src.width+s_)//2,(src.height+s_)//2))
    face=src.resize((int(2*r*1.08),)*2,Image.LANCZOS); off=(face.width-2*r)//2; face=face.crop((off,off-6,off+2*r,off+2*r-6))
    m=Image.new('L',(2*r,2*r),0); ImageDraw.Draw(m).ellipse((0,0,2*r-1,2*r-1),fill=255)
    d=ImageDraw.Draw(bg)
    d.ellipse((cx-r-30,cy-r-20,cx+r+30,cy+r+40),fill=(0,0,0)); d.ellipse((cx-r-16,cy-r-16,cx+r+16,cy+r+16),fill=(245,240,225)); d.ellipse((cx-r-6,cy-r-6,cx+r+6,cy+r+6),fill=(0,0,0))
    bg.paste(face,(cx-r,cy-r),m)
    # ransom text
    rng=np.random.default_rng(seed); rows=[["PUT","ON"],["THE","GLASSES"]]; y=650
    for ri,row in enumerate(rows):
        ps=[piece(w,rng,False,.9 if ri==0 else .92) for w in row]
        rw=sum(p.width-10 for p in ps); x=(S-rw)//2; rh=max(p.height for p in ps)
        for p in ps: bg.paste(p,(int(x),int(y+(rh-p.height)/2)),p); x+=p.width-10
        y+=rh-18
    # fade alien bottom into text area
    bg.save(out,quality=95)
build('jessie-cool-glasses-worn-01','fullbody-alien-man-14',11,'tue night put on the glasses logo.png')

# build.py spec.json  -> builds page html + mixed audio for an episode
import json,re,sys,base64,subprocess,numpy as np,wave
S=json.load(open(sys.argv[1])); D=S['dir']
words=json.load(open(f"{D}/words.json"))
# caption lines from chunk spec: [first_word_index, emotion, kicker]
lines=[]
for n,(i0,e,k) in enumerate(S['chunks']):
    i1=S['chunks'][n+1][0] if n+1<len(S['chunks']) else len(words)
    ws=words[i0:i1]; lines.append(dict(at=ws[0][1] if n else 0,e=e,k=k,w=ws))
vend=S['voice_end']; SPON=round(vend+0.3,2); SPON2=round(SPON+2.5,2); END=round(SPON+5.0,2); TOTAL=round(END+4.6,2)
# ---- audio mix
SR=44100
with wave.open(f"{D}/voice.wav") as w: v=np.frombuffer(w.readframes(w.getnframes()),np.int16).astype(np.float32)/32768
mix=np.zeros(int(TOTAL*SR),np.float32); mix[:len(v)]+=v
rng=np.random.default_rng(7)
def lp(x,a):
    y=np.zeros_like(x); s=0.0; a=np.broadcast_to(a,x.shape)
    for i in range(len(x)): s+=a[i]*(x[i]-s); y[i]=s
    return y
def whoosh(d=.45,g=.12):
    n=int(d*SR); t=np.linspace(0,1,n); x=rng.standard_normal(n).astype(np.float32); y=lp(x,0.02+0.25*t); y-=lp(y,0.01); y*=np.sin(np.pi*t)**1.6
    return y/np.abs(y).max()*g
def clunk(g=.45):
    t=np.arange(int(.35*SR))/SR; y=np.sin(2*np.pi*95*t)*np.exp(-t*14)+.5*np.sin(2*np.pi*190*t)*np.exp(-t*22); return y/np.abs(y).max()*g
def bell(f,d):
    t=np.arange(int(d*SR))/SR; return (np.sin(2*np.pi*f*t)+.5*np.sin(2*np.pi*2.76*f*t)*np.exp(-t*6))*np.exp(-t*4.5)
def ding(g=.3):
    a=bell(1568,.9);b=bell(2093,1.0);y=np.zeros(int(1.2*SR));y[:len(a)]+=a;o=int(.13*SR);y[o:o+len(b)]+=b;return y/np.abs(y).max()*g
def pop(g=.22,f=880):
    t=np.arange(int(.12*SR))/SR; y=np.sin(2*np.pi*(f+f*2*t/.12)*t)*np.exp(-t*40); return y/np.abs(y).max()*g
def tick(g=.25):
    n=int(.012*SR); y=rng.standard_normal(n)*np.exp(-np.arange(n)/60); y=y-lp(y,0.3); return y/np.abs(y).max()*g
FX=dict(whoosh=whoosh,clunk=clunk,ding=ding,pop=pop,tick=tick)
def put(t,s):
    i=int(t*SR); mix[i:i+len(s)]+=s[:len(mix)-i]
st=S['sting']; put(st[0]-0.02,whoosh(.55,.2)); [put(st[0]+0.25+k*.33,tick()) for k in range(6)]
for x in S['V']:
    if x.get('c') and x['at']>0: put(x['at']-0.12,whoosh())
for name,t,*a in S.get('fx',[]): put(t,FX[name](*a))
put(SPON-0.1,whoosh(.6,.2)); put(END-0.1,whoosh(.5,.16)); put(END+0.1,tick(.3)); put(END+0.4,tick(.3))
pk=np.abs(mix).max(); mix/=max(1,pk/0.97)
with wave.open(f"{D}/mix.wav",'wb') as w: w.setnchannels(1);w.setsampwidth(2);w.setframerate(SR);w.writeframes((mix*32767).astype(np.int16).tobytes())
subprocess.run(['ffmpeg','-v','error','-y','-i',f"{D}/mix.wav",'-b:a','96k',f"{D}/mix.mp3"],check=True)
# ---- page
s=open(S['template']).read()
mp3=base64.b64encode(open(f"{D}/mix.mp3",'rb').read()).decode()
s=re.sub(r'(<audio id="vo" preload="auto" src="data:audio/mpeg;base64,)[^"]*"',lambda m:m.group(1)+mp3+'"',s)
used=sorted({x['c'] for x in S['V'] if x.get('c')})
imgs=''.join(f'<img alt="" data-c="{n}" src="data:image/jpeg;base64,{base64.b64encode(open(f"cuts/{n}.jpg","rb").read()).decode()}">' for n in used)
s=re.sub(r'<div class="cut" id="cut">.*?</div>',lambda m:'<div class="cut" id="cut">'+imgs+'</div>',s,count=1,flags=re.S)
s=re.sub(r'const LINES=.*?;\n',lambda m:'const LINES='+json.dumps(lines)+';\n',s,count=1,flags=re.S)
s=re.sub(r'const V=\[.*?\];',lambda m:'const V='+json.dumps(S['V'])+';',s,count=1,flags=re.S)
s=re.sub(r'const STING=\[[^\]]*\], SPON=[0-9.]+, SPON2=[0-9.]+, END=[0-9.]+;',f'const STING={json.dumps(st)}, SPON={SPON}, SPON2={SPON2}, END={END};',s)
s=re.sub(r'(<div class="ov open" id="open">.*?<div class="ep">)[^<]*(</div>)',lambda m:m.group(1)+S['ep_title']+m.group(2),s,count=1,flags=re.S)
open(S['out'],'w').write(s)
json.dump(dict(total=TOTAL),open(f"{D}/meta.json",'w'))
print('total',TOTAL,'lines',len(lines),'cuts',len(used),'kb',len(s)//1024)

import subprocess,numpy as np,sys
V=sys.argv[1]; OUT=sys.argv[2]; AUD=sys.argv[3] if len(sys.argv)>3 else 'am/mix.mp3'
W,H=720,1296; FS=W*H*3; DUR=float(sys.argv[4]) if len(sys.argv)>4 else 71.5; FPS=30
def frames():
    pr=subprocess.Popen(['ffmpeg','-v','error','-i',V,'-f','rawvideo','-pix_fmt','rgb24','-'],stdout=subprocess.PIPE)
    while True:
        b=pr.stdout.read(FS)
        if len(b)<FS: break
        f=np.frombuffer(b,np.uint8).reshape(H,W,3)
        row=f[1288]; cw=W/16
        v=0
        for k in range(16):
            if row[int(cw*k+cw/2)].mean()>128: v|=1<<k
        yield ((v-1)/100 if 0<v<60000 else None), f
enc=subprocess.Popen(['ffmpeg','-v','error','-y','-f','rawvideo','-pix_fmt','rgb24','-s',f'{W}x1280','-r',str(FPS),'-i','-','-i',AUD,
 '-vf','scale=1080:1920:flags=lanczos','-c:v','libx264','-preset','veryfast','-crf','19','-pix_fmt','yuv420p','-profile:v','high','-c:a','aac','-b:a','160k','-shortest','-movflags','+faststart',OUT],stdin=subprocess.PIPE)
g=frames(); cur=None; nxt=next(g); n=0; got=[]
for i in range(int(DUR*FPS)):
    T=i/FPS
    while nxt is not None and (nxt[0] is None or nxt[0]<=T+0.02):
        if nxt[0] is not None: cur=nxt; got.append(nxt[0])
        nxt=next(g,None)
    if cur is None: cur=nxt
    enc.stdin.write(np.ascontiguousarray(cur[1][:1280]).tobytes()); n+=1
enc.stdin.close(); enc.wait()
d=np.diff(got); print('frames',n,'decoded',len(got),'first',got[:3],'max gap',round(d.max(),3) if len(d) else None,'last',got[-1])

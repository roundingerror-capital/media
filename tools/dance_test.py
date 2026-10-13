import os, sys, math, subprocess, numpy as np, wave
sys.path.insert(0,os.path.dirname(os.path.abspath(__file__)))
from PIL import Image, ImageDraw
from make_reel import W,H,FPS,archivo,mono,fit,fade,blend
M=72; LIME="#C8F03C"; INK="#F2F2EE"; MUT="#9A9A94"; LINE="#262626"
BPM=112; BEAT=60/BPM; END=10.0
SP={n:Image.open(os.path.join(os.path.dirname(os.path.abspath(__file__)),'sprites',f'{n}_sprite_1x.png')).convert('RGBA') for n in ('theo','penny')}
def sprite(n,scale,flip=False,sq=1.0):
    s=SP[n]; w,h=s.width*scale,s.height*scale
    im=s.resize((w,h),Image.NEAREST)
    if flip: im=im.transpose(Image.FLIP_LEFT_RIGHT)
    if sq!=1.0: im=im.resize((int(w/sq**0.5),int(h*sq)),Image.NEAREST)
    return im
rng=np.random.default_rng(3); CONF=[(rng.uniform(0,W),rng.uniform(-H,0),rng.uniform(260,520),rng.uniform(0,6.28),rng.choice([LIME,INK,"#5BC0F0"])) for _ in range(70)]
def frame(t):
    img=Image.new("RGB",(W,H),"#000000"); d=ImageDraw.Draw(img)
    b=(t/BEAT); ph=b%1; beat=int(b)
    # confetti after 1.5s
    if t>1.5:
        for x,y0,v,p,c in CONF:
            y=y0+(t-1.5)*v
            if 0<y<1700: xx=x+math.sin(t*3+p)*30; d.rectangle([xx,y,xx+12,y+12],fill=c)
    # header
    d.text((M,120),"≈ Rounding Error",font=archivo(40,110,800),fill=INK,anchor="ls")
    d.text((W-M,120),"BEHIND THE SCENES",font=mono(24),fill=MUT,anchor="rs")
    d.line([(M,150),(W-M,150)],fill=LINE,width=2)
    a=fade(t,0.1,0.5)
    f=fit("Testing the workflow.",W-2*M,110,wdth=110,wght=900)
    d.text((M,330),"Testing the",font=f,fill=blend(INK,a),anchor="ls")
    d.text((M,330+int(f.size*1.05)),"workflow.",font=f,fill=blend(LIME,a),anchor="ls")
    steps=["Penny makes it","The boss approves it","Metricool posts it","You watch it"]
    for i,sx in enumerate(steps):
        sa=fade(t,1.2+i*0.9,1.5+i*0.9)
        if sa>0:
            y=640+i*70
            d.text((M,y),("✓ " if t>1.5+i*0.9+0.5 else "· ")+sx,font=mono(38,True),fill=blend(LIME if i==3 else INK,sa),anchor="ls")
    # dancers: hop on beat, sway, flip every 2 beats
    hop=abs(math.sin(ph*math.pi))*90
    sq=1.0-0.12*max(0,math.cos(ph*math.pi*2))*(1 if ph<0.15 or ph>0.85 else 0)
    sway=math.sin(b*math.pi)*40
    for n,xc,off in (("theo",W*0.30,0.0),("penny",W*0.70,0.5)):
        p2=(b+off)%1; hp=abs(math.sin(p2*math.pi))*90
        im=sprite(n,9,flip=((beat+(1 if off else 0))//2)%2==1,sq=1.0-0.10*(1-abs(math.sin(p2*math.pi))))
        x=int(xc-im.width/2+ (sway if n=="theo" else -sway)); y=int(1620-im.height-hp)
        # shadow
        sw=int(im.width*0.7*(1-hp/250)); d.ellipse([xc-sw/2,1615,xc+sw/2,1640],fill="#1a1a1a")
        img.paste(im,(x,y),im)
    # bubbles
    if 6.2<t<9.6:
        txt="It works!" if t<8 else "Like + follow!"
        fb=mono(34,True); tw=int(fb.getlength(txt)); bx=W//2-tw//2-22; by=1080
        d.rectangle([bx,by,bx+tw+44,by+70],fill=INK); d.rectangle([bx+4,by+4,bx+tw+40,by+66],outline="#1A1A1A",width=4)
        d.text((W//2,by+48),txt,font=fb,fill="#000000",anchor="ms")
    # secret message (the boss's note, 2026-10-13): faint line all video + a 3-frame flash near the end
    d.text((W//2,1690),"I like Fried Chicken",font=mono(20),fill="#141414",anchor="ms")
    if 9.70<=t<9.80:
        d.rectangle([0,860,W,1000],fill="#000000")
        d.text((W//2,955),"I like Fried Chicken",font=archivo(72,110,900),fill=LIME,anchor="ms")
    d.line([(M,1720),(W-M,1720)],fill=LINE,width=2)
    d.text((M,1768),"A TEST POST · NOT ADVICE",font=mono(22),fill=MUT,anchor="ls")
    d.text((M,1806),"@ROUNDINGERROR.CAPITAL",font=mono(22),fill=MUT,anchor="ls")
    return img
def track(path):
    SR=44100; N=int(SR*(END+0.5)); out=np.zeros(N); t_=lambda n: np.arange(n)/SR
    def add(sig,at):
        i=int(at*SR); j=min(N,i+len(sig)); out[i:j]+=sig[:j-i]
    def kick():
        n=int(.3*SR); t=t_(n); f=50+100*np.exp(-t*30); return np.sin(2*np.pi*np.cumsum(f)/SR)*np.exp(-t*9)*0.9
    def clap():
        n=int(.2*SR); t=t_(n); return np.random.randn(n)*np.exp(-t*22)*0.35
    def hat():
        n=int(.04*SR); t=t_(n); x=np.diff(np.concatenate([[0],np.random.randn(n)])); return x*np.exp(-t*90)*0.1
    def pluck(f,l):
        n=int(l*SR); t=t_(n); return (np.sin(2*np.pi*f*t)+0.4*np.sin(4*np.pi*f*t))*np.exp(-t*6)*0.16
    def bass(f,l):
        n=int(l*SR); t=t_(n); return (np.sign(np.sin(2*np.pi*f*t))*0.3+np.sin(2*np.pi*f*t)*0.5)*np.minimum(1,t*200)*np.exp(-t*3)*0.33
    mel=[659.3,784.0,880.0,784.0,659.3,587.3,659.3,0]; bl=[82.41,82.41,110.0,98.0]
    for k in range(int(END/BEAT)):
        t0=k*BEAT; add(kick(),t0)
        if k%2==1: add(clap(),t0)
        add(hat(),t0+BEAT/2)
        add(bass(bl[(k//2)%4],BEAT*0.9),t0)
        if k>=4: f=mel[k%8]; 
        if k>=4 and f: add(pluck(f,BEAT*0.8),t0+BEAT/2)
    fo=int(1.0*SR); out[-fo:]*=np.linspace(1,0,fo); out=out/np.max(np.abs(out))*0.6
    data=(np.stack([out,out],1)*32767).astype(np.int16)
    w=wave.open(path,'wb'); w.setnchannels(2); w.setsampwidth(2); w.setframerate(SR); w.writeframes(data.tobytes()); w.close()
if __name__=="__main__":
    if len(sys.argv)>1 and sys.argv[1]=="stills":
        ts=[0.6,2.2,4.0,6.5,8.5]; sh=Image.new("RGB",(len(ts)*270,480))
        for i,s in enumerate(ts): sh.paste(frame(s).resize((270,480)),(i*270,0))
        sh.save('contact.png'); sys.exit()
    track('track.wav')
    p=subprocess.Popen(["ffmpeg","-y","-loglevel","error","-f","rawvideo","-pix_fmt","rgb24","-s",f"{W}x{H}","-r",str(FPS),"-i","-","-i","track.wav","-map","0:v","-map","1:a","-c:v","libx264","-pix_fmt","yuv420p","-preset","medium","-crf","18","-c:a","aac","-b:a","192k","-af","loudnorm=I=-14:TP=-1.5","-shortest","-movflags","+faststart","workflow_test_v2.mp4"],stdin=subprocess.PIPE)
    for i in range(int(END*FPS)): p.stdin.write(frame(i/FPS).tobytes())
    p.stdin.close(); p.wait(); print("done")

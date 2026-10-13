import os, sys, math, subprocess
sys.path.insert(0,os.path.dirname(os.path.abspath(__file__))); sys.path.insert(0,'.')
from PIL import Image, ImageDraw
from make_reel import W,H,FPS,archivo,mono,fit,fade,blend
M=72; LIME="#C8F03C"; INK="#F2F2EE"; MUT="#9A9A94"; FAINT="#6E6E69"; LINE="#262626"; LOSS="#FF8A5B"
END=20.0
def ease(x): x=max(0,min(1,x)); return 1-(1-x)**3
from specs import SPECS
KEY=sys.argv[1]; S=SPECS[KEY]
SP=Image.open(os.path.join(os.path.dirname(os.path.abspath(__file__)),'sprites','theo_sprite_1x.png')).convert('RGBA'); SPX=5
SPB=SP.resize((SP.width*SPX,SP.height*SPX),Image.NEAREST)
def theo(img,d,t,line):
    bob=SPX if int(t*2)%2 else 0; hop=0
    for h0 in (0.5,4.0,15.6):
        x=(t-h0)/0.45
        if 0<=x<=1: hop=int(math.sin(x*math.pi)*7)*SPX
    x0=W-M-SPB.width+6; y0=1700-SPB.height-bob-hop; img.paste(SPB,(x0,y0),SPB)
    if line:
        f=mono(30,True); tw=int(f.getlength(line)); bw,bh=tw+40,66; bx=x0-bw-14; by=y0+40
        d.rectangle([bx,by,bx+bw,by+bh],fill=INK); d.rectangle([bx+4,by+4,bx+bw-5,by+bh-5],outline="#1A1A1A",width=4)
        d.polygon([(bx+bw,by+22),(bx+bw+16,by+33),(bx+bw,by+44)],fill=INK); d.text((bx+20,by+45),line,font=f,fill="#000000",anchor="ls")
def chrome(d):
    d.text((M,120),"≈ Rounding Error",font=archivo(40,110,800),fill=INK,anchor="ls")
    d.text((W-M,120),f"TRADE #{S['n']} · RECEIPT",font=mono(24),fill=MUT,anchor="rs")
    d.line([(M,150),(W-M,150)],fill=LINE,width=2); d.line([(M,1720),(W-M,1720)],fill=LINE,width=2)
    d.text((M,1768),"REAL TRADE · REAL MONEY · NOT ADVICE",font=mono(22),fill=MUT,anchor="ls")
    d.text((M,1806),"@ROUNDINGERROR.CAPITAL",font=mono(22),fill=MUT,anchor="ls")
def frame(t):
    img=Image.new("RGB",(W,H),"#000000"); d=ImageDraw.Draw(img); line=None
    # scene 1: hook + $270 count (0-6.2)
    a=fade(t,0.1,0.4)*(1-fade(t,6.0,6.3))
    if a>0:
        d.text((M,300),"NEW FILL · "+S["when"],font=mono(30,True),fill=blend(LIME,a),anchor="ls")
        h1,h2=S["headline"]; f=fit(max(h1,h2,key=len),W-2*M,128,wdth=110,wght=900)
        d.text((M,460),h1,font=f,fill=blend(INK,a),anchor="ls")
        d.text((M,460+int(f.size*1.05)),h2,font=f,fill=blend(LIME,a*fade(t,0.4,0.8)),anchor="ls")
        p=ease((t-1.4)/1.4); v=int(round(S['amt']*p))
        if t>1.3:
            k=1+0.12*ease((t-2.8)/0.4)
            d.text((M,950),f"${v}",font=archivo(int(230*k),110,900),fill=blend(LIME,a),anchor="ls")
            d.text((M,1020),S["amt_line"],font=mono(34,True),fill=blend(INK,a*fade(t,2.8,3.2)),anchor="ls")
        b=fade(t,3.8,4.2)*a
        if b>0:
            d.rectangle([M,1100,W-M,1250],outline=blend(LIME,b),width=4)
            d.text((M+30,1160),S["er"][0],font=mono(28,True),fill=blend(LIME,b),anchor="ls")
            d.text((M+30,1212),S["er"][1],font=fit_m(S["er"][1],W-2*M-60,30),fill=blend(INK,b),anchor="ls")
        line="Like + follow!" if t<3.0 else f"Trade #{S['n']}."
    # scene 2: receipt rows (6.3-12.6)
    a=fade(t,6.3,6.6)*(1-fade(t,12.4,12.7))
    if a>0:
        d.text((M,300),"THE RECEIPT",font=mono(30,True),fill=blend(MUT,a),anchor="ls")
        d.text((M,390),S["title"],font=fit(S["title"],W-2*M,70,wdth=110,wght=900),fill=blend(INK,a),anchor="ls")
        rows=S["short_rows"]
        y=520
        for i,(k,v) in enumerate(rows):
            ra=fade(t,6.8+i*0.55,7.1+i*0.55)*a
            if ra<=0: y+=150; continue
            hl=k in S["short_hl"]
            sc=1+(0.15*ease((t-7.1-i*0.55)/0.4) if hl else 0)
            d.text((M,y),k,font=mono(28,True),fill=blend(MUT,ra),anchor="ls")
            d.text((W-M,y+62),v,font=archivo(int(56*sc),105,900),fill=blend(LIME if hl else INK,ra),anchor="rs")
            d.line([(M,y+90),(W-M,y+90)],fill=blend(LINE,ra),width=2); y+=150
        line="Read it all." if t>10.2 else None
    # scene 3: how it ends + tally (12.7-17.2)
    a=fade(t,12.7,13.0)*(1-fade(t,17.0,17.3))
    if a>0:
        d.text((M,300),"HOW IT ENDS",font=mono(30,True),fill=blend(MUT,a),anchor="ls")
        d.text((M,400),"Two endings. Both planned.",font=fit("Two endings. Both planned.",W-2*M,96,wdth=110,wght=900),fill=blend(INK,a),anchor="ls")
        for i,(hh,tt) in enumerate(S["outcomes"]):
            ra=fade(t,13.1+i*0.5,13.4+i*0.5)*a; y=480+i*230
            d.rectangle([M,y,W-M,y+190],outline=blend(LIME if i==0 else LINE,ra),width=4 if i==0 else 2)
            d.text((M+30,y+66),hh,font=fit_m(hh,W-2*M-60,30),fill=blend(LIME if i==0 else INK,ra),anchor="ls")
            d.text((M+30,y+136),tt,font=fit(tt,W-2*M-60,34,wdth=100,wght=600),fill=blend(INK,ra),anchor="ls")
        ta=fade(t,14.6,15.0)*a
        d.text((M,1060),"RUNNING TOTAL",font=mono(28,True),fill=blend(MUT,ta),anchor="ls")
        for i,(k,v) in enumerate(zip(("TRADES","COLLECTED","LOSSES"),S["tot"])):
            x=(M,M+230,M+660)[i]; sc=1+0.15*ease((t-15.0-i*0.2)/0.4)
            d.text((x,1190),v,font=archivo(int(100*sc),105,900),fill=blend(LIME,ta),anchor="ls")
            d.text((x,1240),k,font=mono(26,True),fill=blend(INK,ta),anchor="ls")
        line="Holding to expiry." if t>15.4 else None
    # scene 4: CTA (17.3-20)
    a=fade(t,17.3,17.6)
    if a>0:
        f=fit("Follow for every receipt.",W-2*M,96,wdth=110,wght=900)
        d.text((M,700),"Follow for",font=f,fill=blend(INK,a),anchor="ls"); d.text((M,700+int(f.size*1.05)),"every receipt.",font=f,fill=blend(LIME,a),anchor="ls")
        d.text((M,960),"Wins and losses. Every trade.",font=mono(34,True),fill=blend(MUT,a),anchor="ls")
        line=S["bye"]
    theo(img,d,t,line); chrome(d)
    return img
def fit_m(txt,maxw,start):
    s=start
    while s>14 and mono(s).getlength(txt)>maxw: s-=1
    return mono(s)
if __name__=="__main__":
    if len(sys.argv)>2 and sys.argv[2]=="stills":
        ts=[1.0,3.5,5.0,10.5,16.0,18.5]; sh=Image.new("RGB",(len(ts)*270,480))
        for i,s in enumerate(ts): sh.paste(frame(s).resize((270,480)),(i*270,0))
        sh.save(f'{KEY}_short_contact.png'); frame(10.5).save(f'{KEY}_short_cover.png'); sys.exit()
    out=f"RoundingError_Trade{S['n']}_{S['tk']}_Short.mp4"
    p=subprocess.Popen(["ffmpeg","-y","-loglevel","error","-f","rawvideo","-pix_fmt","rgb24","-s",f"{W}x{H}","-r",str(FPS),"-i","-","-c:v","libx264","-pix_fmt","yuv420p","-preset","medium","-crf","18","-movflags","+faststart",out],stdin=subprocess.PIPE)
    for i in range(int(END*FPS)): p.stdin.write(frame(i/FPS).tobytes())
    p.stdin.close(); p.wait(); print("done")

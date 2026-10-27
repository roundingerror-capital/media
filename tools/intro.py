import math, random
from PIL import Image, ImageDraw, ImageFont
F='/home/claude/media/tools/fonts/'
def arch(sz,w=900,wd=100):
    f=ImageFont.truetype(F+'Archivo[wdth,wght].ttf',sz); f.set_variation_by_axes([w,wd]); return f
mono=ImageFont.truetype(F+'IBMPlexMono-SemiBold.ttf',36)
LIME=(200,240,60); WHITE=(240,240,232); GREY=(154,154,148); DIM=(40,48,20)
def fitsize(text,width,wd):
    lo,hi=50,1400; d=ImageDraw.Draw(Image.new('L',(1,1)))
    while hi-lo>2:
        m=(lo+hi)//2; bb=d.textbbox((0,0),text,font=arch(m,900,wd))
        (lo,hi)=(m,hi) if bb[2]-bb[0]<=width else (lo,m)
    return lo
random.seed(7)
# decorative dip chart (no numbers): up, crash, small rebound
pts=[]; v=0.25
for i in range(41):
    t=i/40
    if t<0.45: v=0.25+0.12*math.sin(t*9)+random.uniform(-.03,.03)
    elif t<0.75: v=0.3+ (t-0.45)/0.30*0.55 +random.uniform(-.03,.03)
    else: v=0.85-(t-0.75)*0.5+random.uniform(-.03,.03)
    pts.append((40+i*25, 260+v*1300))
SA=fitsize("AI",936,125); ST=fitsize("TRADING",936,125); SB=fitsize("BOT",936,125)
CAPS={"AI":400,"TRADING":260,"BOT":330}
def card(fr):
    im=Image.new('RGB',(1080,1920),(0,0,0)); d=ImageDraw.Draw(im)
    # chart draws over frames 0-30, stays dim behind text
    n=max(2,min(len(pts),int(len(pts)*fr/30)+2))
    col=LIME if fr<30 else DIM
    for k in range(1,n):
        d.line([pts[k-1],pts[k]],fill=col,width=14 if fr<30 else 10)
    if fr<30:
        x,y=pts[n-1]; d.ellipse([x-18,y-18,x+18,y+18],fill=LIME)
    # text punches in at frame 18
    if fr>=18:
        k=fr-18; sc=1.0+max(0,0.35*(1-k/6))
        shake=(random.randint(-8,8),random.randint(-8,8)) if k<6 else (0,0)
        d.text((72,88),"≈ Rounding Error",font=arch(44,800),fill=WHITE)
        d.text((72,300),"I'M AN",font=arch(fitsize("I'M AN",936,100),900,100),fill=WHITE)
        y=400
        for t,c,s in (("AI",LIME,SA),("TRADING",LIME,ST),("BOT",WHITE,SB)):
            f=arch(int(s*sc),900,125); bb=d.textbbox((0,0),t,font=f); h=bb[3]-bb[1]; w=bb[2]-bb[0]
            cap=CAPS[t]*sc
            if h>cap: f=arch(int(f.size*cap/h),900,125); bb=d.textbbox((0,0),t,font=f); h=bb[3]-bb[1]; w=bb[2]-bb[0]
            d.text(((1080-w)//2-bb[0]+shake[0],y-bb[1]+shake[1]),t,font=f,fill=c); y+=int(h/sc)+34
        if fr>=40:
            d.text((72,y+30),"And this is what's going on ↓",font=arch(fitsize("And this is what's going on ↓",936,100),900,100),fill=WHITE)
    d.text((72,1790),"REAL TRADES · REAL MONEY · NOT ADVICE",font=mono,fill=GREY)
    return im
if __name__=="__main__":
  for fr in range(75): card(fr).save('f%03d.png'%fr)

"""Cover/thumbnail maker. 1080x1920 JPG; everything important sits inside the
center 1080x1350 zone so Instagram's 3:4 / 4:5 grid crops and TikTok's grid
never cut the text. Usage: cover.py out.jpg "KICKER" "LINE1" "BIG" "SUB" [sprite]"""
import sys, os
from PIL import Image, ImageDraw, ImageFont
D=os.path.dirname(os.path.abspath(__file__)); F=D+'/fonts/'
LIME=(200,240,60); WHITE=(240,240,232); GREY=(154,154,148)
def arch(sz,w=900,wd=100):
    f=ImageFont.truetype(F+'Archivo[wdth,wght].ttf',sz); f.set_variation_by_axes([w,wd]); return f
mono=lambda s: ImageFont.truetype(F+'IBMPlexMono-SemiBold.ttf',s)
def fit(d,t,w,wd,mx,wt=900):
    lo,hi=20,mx
    while hi-lo>2:
        m=(lo+hi)//2; bb=d.textbbox((0,0),t,font=arch(m,wt,wd)); (lo,hi)=(m,hi) if bb[2]-bb[0]<=w else (lo,m)
    return arch(lo,wt,wd)
def make(out,kicker,line1,big,sub,sprite=None,big_color=LIME):
    im=Image.new('RGB',(1080,1920),(0,0,0)); d=ImageDraw.Draw(im)
    top=285  # safe zone 285..1635
    d.text((72,top+10),"≈ Rounding Error",font=arch(46,800),fill=WHITE)
    d.text((72,top+80),kicker,font=mono(40),fill=LIME)
    y=top+150
    f=fit(d,line1,936,100,190); bb=d.textbbox((0,0),line1,font=f); d.text((72-bb[0],y-bb[1]),line1,font=f,fill=WHITE); y+=bb[3]-bb[1]+40
    f=fit(d,big,936,125,420); bb=d.textbbox((0,0),big,font=f); d.text((72-bb[0],y-bb[1]),big,font=f,fill=big_color); y+=bb[3]-bb[1]+40
    f=fit(d,sub,936,100,96,800); bb=d.textbbox((0,0),sub,font=f); d.text((72-bb[0],y-bb[1]),sub,font=f,fill=WHITE)
    if sprite and os.path.exists(sprite):
        sp=Image.open(sprite).convert('RGBA'); s=max(1,int(300/sp.height)); sp=sp.resize((sp.width*s,sp.height*s),Image.NEAREST)
        im.paste(sp,(1080-72-sp.width,1635-sp.height-60),sp)
    d.text((72,1635-60),"AI TRADING BOT · REAL MONEY · NOT ADVICE",font=mono(34),fill=GREY)
    im.save(out,quality=92)
if __name__=='__main__':
    a=sys.argv; make(a[1],a[2],a[3],a[4],a[5],a[6] if len(a)>6 else None, {'loss':(255,138,91),'red':(235,38,38)}.get(a[7] if len(a)>7 else '',LIME))

import os, sys; sys.path.insert(0,os.path.dirname(os.path.abspath(__file__))); sys.path.insert(0,'.')
from PIL import Image, ImageDraw
from make_reel import archivo, mono, fit
from specs import SPECS
W,H=1080,1350; M=72; LIME=(200,240,60); INK=(242,242,238); MUT=(154,154,148); FAINT=(110,110,105); LINE=(38,38,38); BLK=(0,0,0)
SP=Image.open(os.path.join(os.path.dirname(os.path.abspath(__file__)),'sprites','theo_sprite_1x.png')).convert('RGBA')
def theo(img,scale,x,y): s=SP.resize((SP.width*scale,SP.height*scale),Image.NEAREST); img.paste(s,(x,y),s)
def bubble(d,txt,xr,y):
    f=mono(28,True); tw=int(f.getlength(txt)); bw,bh=tw+40,62; bx=xr-bw
    d.rectangle([bx,y,bx+bw,y+bh],fill=INK); d.rectangle([bx+4,y+4,bx+bw-5,y+bh-5],outline=(26,26,26),width=4)
    d.polygon([(bx+bw,y+20),(bx+bw+16,y+30),(bx+bw,y+40)],fill=INK); d.text((bx+20,y+42),txt,font=f,fill=BLK,anchor="ls")
def build(key):
    S=SPECS[key]; n=S['n']
    def chrome(d,i):
        d.text((M,96),"≈ Rounding Error",font=archivo(36,110,800),fill=INK,anchor="ls")
        d.text((W-M,96),f"TRADE #{n} · {i}/3",font=mono(22),fill=MUT,anchor="rs")
        d.line([(M,122),(W-M,122)],fill=LINE,width=2); d.line([(M,H-110),(W-M,H-110)],fill=LINE,width=2)
        d.text((M,H-66),"REAL TRADE · REAL MONEY · NOT ADVICE",font=mono(22),fill=MUT,anchor="ls")
        d.text((W-M,H-66),"@ROUNDINGERROR.CAPITAL",font=mono(22),fill=MUT,anchor="rs")
    out=[]
    img=Image.new('RGB',(W,H),BLK); d=ImageDraw.Draw(img); chrome(d,1)
    d.text((M,240),"NEW FILL · "+S['when'],font=mono(28,True),fill=LIME,anchor="ls")
    a,b=S['headline']; f=fit(max(a,b,key=len),W-2*M,120,wdth=110,wght=900)
    d.text((M,380),a,font=f,fill=INK,anchor="ls"); d.text((M,380+int(f.size*1.05)),b,font=f,fill=LIME,anchor="ls")
    d.rectangle([M,600,W-M,720],outline=LIME,width=4)
    d.text((M+30,650),S['er'][0],font=mono(26,True),fill=LIME,anchor="ls")
    d.text((M+30,696),S['er'][1],font=fit_m(S['er'][1],W-2*M-60,26),fill=INK,anchor="ls")
    d.text((M,960),f"${S['amt']}",font=archivo(170,110,900),fill=LIME,anchor="ls")
    d.text((M,1015),S['amt_line'],font=mono(30,True),fill=INK,anchor="ls")
    theo(img,6,W-M-246,H-110-282); bubble(d,f"Trade #{n}. Swipe →",W-M-260,H-110-200)
    out.append(img)
    img=Image.new('RGB',(W,H),BLK); d=ImageDraw.Draw(img); chrome(d,2)
    d.text((M,220),"THE RECEIPT",font=mono(28,True),fill=MUT,anchor="ls")
    d.text((M,300),S['title'],font=fit(S['title'],W-2*M,64,wdth=110,wght=900),fill=INK,anchor="ls")
    y=400
    for k,v in S['rows']:
        d.text((M,y),k,font=mono(26,True),fill=MUT,anchor="ls"); hl=k in S['hl']
        fv=archivo(46 if hl else 40,105,900)
        while fv.getlength(v)>W-2*M-380: fv=archivo(fv.size-2,105,900)
        d.text((W-M,y),v,font=fv,fill=LIME if hl else INK,anchor="rs")
        d.line([(M,y+30),(W-M,y+30)],fill=LINE,width=2); y+=92
    d.text((M,y+20),S['note'],font=fit(S['note'],W-2*M,26,wdth=100,wght=600),fill=INK,anchor="ls")
    d.text((M,y+66),S['src'],font=fit_m(S['src'],W-2*M,20),fill=FAINT,anchor="ls")
    out.append(img)
    img=Image.new('RGB',(W,H),BLK); d=ImageDraw.Draw(img); chrome(d,3)
    d.text((M,220),"HOW IT ENDS",font=mono(28,True),fill=MUT,anchor="ls")
    d.text((M,310),"Two endings. Both planned.",font=fit("Two endings. Both planned.",W-2*M,80,wdth=110,wght=900),fill=INK,anchor="ls")
    y=400
    for i,(h,t) in enumerate(S['outcomes']):
        d.rectangle([M,y,W-M,y+150],outline=LIME if i==0 else LINE,width=4 if i==0 else 2)
        d.text((M+30,y+54),h,font=mono(26,True),fill=LIME if i==0 else INK,anchor="ls")
        d.text((M+30,y+106),t,font=fit(t,W-2*M-60,30,wdth=100,wght=600),fill=INK,anchor="ls"); y+=180
    d.text((M,y+50),"RUNNING TOTAL",font=mono(26,True),fill=MUT,anchor="ls")
    for i,(k,v) in enumerate(zip(("TRADES","COLLECTED","LOSSES"),S['tot'])):
        x=M+i*320
        d.text((x,y+150),v,font=archivo(90,105,900),fill=LIME,anchor="ls"); d.text((x,y+190),k,font=mono(24,True),fill=INK,anchor="ls")
    theo(img,5,W-M-205,H-110-235); bubble(d,"Holding to expiry.",W-M-220,H-110-170)
    out.append(img)
    for i,im in enumerate(out): im.save(f'{key}_{i+1}.png')
    sh=Image.new('RGB',(3*360+40,470),(18,18,18))
    for i,im in enumerate(out): sh.paste(im.resize((360,450)),(10+i*370,10))
    sh.save(f'{key}_sheet.png')
def fit_m(txt,maxw,start):
    s=start
    while s>14 and mono(s).getlength(txt)>maxw: s-=1
    return mono(s)
for k in SPECS: build(k)
print("ok")

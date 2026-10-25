import numpy as np, wave, sys
def make(path,dur,bpm,root,seed,mel_shift=0,cold=0.0):
    """cold > 0: a cold open of that many seconds comes first (impact + alarm); the riser/drop and groove shift by it."""
    sr=44100; beat=60/bpm; N=int(sr*dur); out=np.zeros(N); rng=np.random.default_rng(seed)
    def add(sig,t):
        i=int(t*sr); 
        if i>=N: return
        e=min(N,i+len(sig)); out[i:e]+=sig[:e-i]
    def kick():
        t=np.arange(int(.35*sr))/sr; f=50+120*np.exp(-t*30); return np.sin(2*np.pi*np.cumsum(f)/sr)*np.exp(-t*7)
    def snare():
        t=np.arange(int(.2*sr))/sr; return (rng.standard_normal(len(t))*0.5+np.sin(2*np.pi*190*t)*0.3)*np.exp(-t*18)
    def hat(o=False):
        t=np.arange(int((.12 if o else .04)*sr))/sr; n=np.diff(rng.standard_normal(len(t)),prepend=0); return n*np.exp(-t*(25 if o else 90))*0.18
    def bass(f,l):
        t=np.arange(int(l*sr))/sr; s=np.sin(2*np.pi*f*t)+0.3*np.sin(2*np.pi*f*2*t); return np.tanh(s*2)*0.35*np.minimum(1,(l-t)*20)
    def lead(f,l):
        t=np.arange(int(l*sr))/sr; return (np.sign(np.sin(2*np.pi*f*t))*0.5+np.sin(2*np.pi*f*2.005*t)*0.3)*0.09*np.exp(-t*3)
    if cold:
        t=np.arange(int(1.6*sr))/sr; add(np.sin(2*np.pi*(30+80*np.exp(-t*3))*t)*np.exp(-t*1.5)*1.2+rng.standard_normal(len(t))*np.exp(-t*6)*0.5,0.1)  # impact
        t=np.arange(int((cold-0.2)*sr))/sr; f=900+250*np.sign(np.sin(2*np.pi*3*t)); add(np.sign(np.sin(2*np.pi*np.cumsum(f)/sr))*0.07,0.15)  # alarm
    o=cold
    t=np.arange(int(0.6*sr))/sr; add(rng.standard_normal(len(t))*np.linspace(0,0.25,len(t)),o)
    add(kick()*1.3,0.6+o); add(rng.standard_normal(int(.5*sr))*np.exp(-np.arange(int(.5*sr))/sr*8)*0.4,0.6+o)
    semis=[0,0,-4,-2]; roots=[root*2**(s/12) for s in semis]
    scale=[0,3,5,7,10,12,15]; mel=[root*8*2**(scale[(i*3+mel_shift)%7]/12) for i in range(8)]
    b=0; t0=0.6+o
    while t0+b*beat<dur:
        tt=t0+b*beat; bar=int(b//4)%4
        if b%4==0 or b%8==6: add(kick(),tt)
        if b%8==7: add(kick(),tt+beat/2)
        if b%4 in (1,3) and tt>2.4+o: add(snare(),tt)
        for k in range(2 if tt<2.4+o else 4): add(hat(k==3 and b%2==1),tt+k*beat/(2 if tt<2.4+o else 4))
        if b%2==0: add(bass(roots[bar],beat*1.8),tt)
        if tt>2.5+o and b%2==0: add(lead(mel[(b//2)%8],beat*0.9),tt+beat/2)
        b+=1
    fade=np.ones(N); fade[-int(.8*sr):]=np.linspace(1,0,int(.8*sr)); out*=fade
    out=out/np.max(np.abs(out))*0.89
    data=(np.stack([out,out],1)*32767).astype('<i2')
    w=wave.open(path,'wb'); w.setnchannels(2); w.setsampwidth(2); w.setframerate(sr); w.writeframes(data.tobytes()); w.close()
if __name__=='__main__':
    make(sys.argv[1],float(sys.argv[2]),float(sys.argv[3]),float(sys.argv[4]),int(sys.argv[5]),int(sys.argv[6]))

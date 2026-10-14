import numpy as np,wave
from pathlib import Path
sr=44100; dur=39.; n=int(sr*dur); t=np.arange(n)/sr;rng=np.random.default_rng(314)
a=np.zeros((n,2),np.float64)
def put(start,sig,pan=0):
 i=int(start*sr);j=min(n,i+len(sig));sig=sig[:j-i];a[i:j,0]+=sig*(1-pan*.35);a[i:j,1]+=sig*(1+pan*.35)
def tone(f,d,vol=.1,decay=3):
 u=np.arange(int(sr*d))/sr;env=np.minimum(u/.012,1)*np.exp(-u*decay)
 return vol*env*(np.sin(2*np.pi*f*u)+.24*np.sin(2*np.pi*f*2*u)+.1*np.sin(2*np.pi*f*3.01*u))
# low sustained tension: D minor, slow evolving upper partials
for f,v in [(36.708,.045),(73.416,.023),(110,.014),(155.56,.008)]:
 sig=np.sin(2*np.pi*f*t+0.18*np.sin(t*.6))*v*(.7+.3*np.sin(t*.31)**2)
 sig*=np.minimum(t/2,1)*np.minimum((39-t)/3,1)
 a[:,0]+=sig;a[:,1]+=np.roll(sig,53)
# restrained ostinato; grows after cast reveal
notes=[146.83,220,293.66,174.61,146.83,220,311.13,220]
for k,start in enumerate(np.arange(1,32,.3)):
 v=.028 if start<11 else .046
 put(start,tone(notes[k%8],1.2,v,6),(-1)**k*.65)
 if k%2==0:
  u=np.arange(int(.3*sr))/sr
  kick=np.sin(2*np.pi*(44*u+8*(1-np.exp(-u*22))))*np.exp(-u*17)*.13
  put(start,kick)
 if k%4==2:
  u=np.arange(int(.12*sr))/sr;noise=rng.normal(0,1,len(u));noise-=np.roll(noise,1)
  put(start,noise*np.exp(-u*48)*.011,.3)
# camera edits, identity match pulses
for start in [0,2.8,5,7.4,9,11,12.1,13.2,14.3,15.4,16.5,19,21.3,23.6,26.5,27,29.5,34]:
 u=np.arange(int(.09*sr))/sr
 put(start,rng.normal(0,1,len(u))*np.exp(-u*65)*.055)
 put(start+.035,tone(1320,.09,.025,35),.25)
# ominous deep impacts at three turning points
for start in [5,19,27,34]:
 u=np.arange(int(3.8*sr))/sr
 hit=np.sin(2*np.pi*(36*u+4*(1-np.exp(-u*5))))*.24*np.exp(-u*1.8)
 hit+=rng.normal(0,1,len(u))*.022*np.exp(-u*7)
 put(start,hit)
# final sparse two-note unresolved figure
put(34.3,tone(146.83,4,.08,.7),-.2);put(35.2,tone(155.56,3.8,.055,.8),.2)
a*=np.minimum(t/.07,1)[:,None]*np.clip((39-t)/1.6,0,1)[:,None]
a=np.tanh(a*1.35)*.86
p=Path(__file__).resolve().parents[1] / 'assets/score.wav'
with wave.open(str(p),'wb') as w:w.setnchannels(2);w.setsampwidth(2);w.setframerate(sr);w.writeframes((a*32767).astype('<i2').tobytes())
print(p, 'peak',round(float(np.max(np.abs(a))),3))

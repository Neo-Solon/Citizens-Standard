"""
Calibrate the compound-jump model to all six Lian moments + held-out, at high N.
Mechanism validated; now tune jump magnitude/persistence so the HIGH-debt tail
comes down to +2% while preserving the low-debt reversal=25% the jump class gives.
Search keeps top-5, verifies at N=10000.
"""
import random
H=28
def series(d0,years,P):
    mu_c,sd_c,lam0,lam1,Jmag,Jsd,pp0,pp1=P
    lam=min(0.6,max(0.0,lam0+lam1*max(0.0,d0-0.40)))
    pp =min(0.85,max(0.0,pp0+pp1*max(0.0,d0-0.40)))
    out=[]; in_jump=False
    for _ in range(years):
        if in_jump: in_jump=random.random()<pp
        if not in_jump: in_jump=random.random()<lam
        out.append(random.gauss(Jmag,Jsd) if in_jump else random.gauss(mu_c,sd_c))
    return out
def has_ep(v,sign,start=0):
    run=0
    for i in range(start,len(v)):
        ok=(v[i]<0) if sign<0 else (v[i]>0)
        run=run+1 if ok else 0
        if run>=2: return True,i
    return False,len(v)
def metrics(P,N):
    def sev(d0):
        a=sorted(sum(series(d0,5,P))/5 for _ in range(N)); return a[int(.5*N)],a[int(.9*N)]
    def rev(d0):
        h=v=0
        for _ in range(N):
            s=series(d0,H,P); nf,ne=has_ep(s,-1,0)
            if not nf: continue
            v+=1; pf,_=has_ep(s,+1,ne+1); h+=pf
        return h/max(1,v)
    p50_40,p90_40=sev(0.40); p50_120,p90_120=sev(1.20)
    return (p50_40,p90_40,p50_120,p90_120,rev(0.45),rev(1.00))
def loss(m):
    p50_40,p90_40,p50_120,p90_120,rl,rh=m
    Lsev=(p90_40)**2*1.5+(p90_120-0.02)**2*1.5+(p50_40+0.012)**2+((p50_120-p50_40)-0.008)**2*1.5
    Lrev=(rl-0.25)**2*3+(max(0,0.76-rh))**2*3
    return Lsev*1e4+Lrev*10
random.seed(303)
cands=[]
for _ in range(420):
    P=(random.uniform(-0.015,-0.011),random.uniform(0.003,0.006),
       random.uniform(0.03,0.09),       # lam0 low-debt jump rate
       random.uniform(0.10,0.30),       # lam1
       random.uniform(0.030,0.055),     # Jmag (smaller than 6% to tame high-debt tail)
       random.uniform(0.008,0.020),
       random.uniform(0.05,0.20),       # pp0 low-debt persistence (keep low -> isolated)
       random.uniform(0.30,0.55))       # pp1 high-debt clustering
    m=metrics(P,3000); cands.append((loss(m),P))
cands.sort(key=lambda x:x[0])
print("JUMP MODEL CALIBRATION -- top-5 verified at N=10,000:\n")
print(f"  {'#':>2}{'sev90@40':>10}{'sev90@120':>11}{'med@40':>9}{'medrise':>9}{'rev45':>8}{'rev100':>8}{'pass':>6}")
best=None
for i,P in enumerate([P for _,P in cands[:5]],1):
    random.seed(88); m=metrics(P,10000)
    p50_40,p90_40,p50_120,p90_120,rl,rh=m
    sev_ok=abs(p90_40)<0.006 and abs(p90_120-0.02)<0.006 and abs(p50_40+0.012)<0.006 and abs((p50_120-p50_40)-0.008)<0.007
    rev_ok=0.18<=rl<=0.33 and rh>=0.73
    ok=sev_ok and rev_ok
    print(f"  {i:>2}{100*p90_40:>9.2f}%{100*p90_120:>10.2f}%{100*p50_40:>8.2f}%"
          f"{100*(p50_120-p50_40):>8.2f}%{100*rl:>7.0f}%{100*rh:>7.0f}%{str(ok):>6}")
    if best is None or loss(m)<loss(best[2]): best=(ok,P,m)
ok,P,m=best
random.seed(7); t=n=0
for _ in range(3000):
    for x in series(0.60,10,P): t+=1;n+=(x<0)
ns=n/t
print(f"\nBEST: all-six pass={ok}, held-out neg-share={100*ns:.0f}% (>50)")
keys=['mu_c','sd_c','lam0','lam1','Jmag','Jsd','pp0','pp1']
print("  "+"  ".join(f"{k}={v:+.4f}" for k,v in zip(keys,P)))
if ok and ns>0.5:
    import json
    d=dict(zip(keys,P)); d['H']=H; d['model']='compound_jump'
    json.dump(d,open('/home/claude/dsa_locked.json','w'))
    print("  *** JUMP MODEL CENTERS ALL 6 + held-out at high N -> saved dsa_locked.json ***")
else:
    print("  close; one tight refine pass if needed")

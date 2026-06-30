import random
random.seed(8888)
M=4500; MR=4500; H=28
def series(d0,years,P):
    mu_c,sd_c,h0,h1,m0,m1,sd_s,e0,e1=P
    h=min(0.7,max(0.0,h0+h1*max(0.0,d0-0.40))); ms=m0+m1*max(0.0,d0-0.40)
    ex=max(0.15,e0-e1*max(0.0,d0-0.40))
    regime="stress" if random.random()<h/(h+ex) else "calm"; out=[]
    for _ in range(years):
        if regime=="calm":
            if random.random()<h: regime="stress"
        else:
            if random.random()>ex: regime="calm"
        out.append(random.gauss(mu_c,sd_c) if regime=="calm" else random.gauss(ms,sd_s))
    return out
def has_ep(v,sign,start=0):
    run=0
    for i in range(start,len(v)):
        ok=(v[i]<0) if sign<0 else (v[i]>0)
        run=run+1 if ok else 0
        if run>=2: return True,i
    return False,len(v)
def rev(d0,P):
    h=v_=0
    for _ in range(MR):
        s=series(d0,H,P); nf,ne=has_ep(s,-1,0)
        if not nf: continue
        v_+=1; pf,_=has_ep(s,+1,ne+1); h+=pf
    return h/max(1,v_)
def sev(d0,P):
    a=[sum(series(d0,5,P))/5 for _ in range(M)]; a.sort(); return a[int(.5*M)],a[int(.9*M)]
def negshare(d0,P):
    t=n=0
    for _ in range(1000):
        for x in series(d0,10,P): t+=1;n+=(x<0)
    return n/t
def evaluate(P):
    p50_40,p90_40=sev(0.40,P); p50_120,p90_120=sev(1.20,P)
    rl=rev(0.45,P); rh=rev(1.00,P)
    Lsev=(p90_40)**2*2.0+(p90_120-0.02)**2+(p50_40+0.012)**2+((p50_120-p50_40)-0.008)**2*2.0
    Lrev=(rl-0.25)**2*2.0+(max(0,0.76-rh))**2*3.0
    return Lsev*1e4+Lrev*10,(p50_40,p90_40,p50_120,p90_120,rl,rh)
# nudge h0 up (lift sev90@40 toward 0), trim m1 (medrise toward 0.8); rest near final
best=None
for _ in range(500):
    P=(random.uniform(-0.0126,-0.0116),random.uniform(0.0060,0.0070),
       random.uniform(0.030,0.050),random.uniform(0.44,0.54),   # h0 up
       random.uniform(0.013,0.018),random.uniform(0.007,0.011), # m1 down
       random.uniform(0.030,0.036),random.uniform(0.52,0.60),
       random.uniform(0.33,0.40))
    L,st=evaluate(P)
    if best is None or L<best[0]: best=(L,P,st)
L,P,st=best
mu_c,sd_c,h0,h1,m0,m1,sd_s,e0,e1=P
p50_40,p90_40,p50_120,p90_120,rl,rh=st
ns=negshare(0.60,P)
print(f"FINAL FIT v2, H={H}")
print(f"  sev90@40%  {100*p90_40:+.2f}% (0.0)   sev90@120% {100*p90_120:+.2f}% (+2.0)")
print(f"  med@40%    {100*p50_40:+.2f}% (-1.2)  medrise    {100*(p50_120-p50_40):+.2f}% (+0.8)")
print(f"  rev@45%    {100*rl:.0f}% (~25)        rev@100%   {100*rh:.0f}% (>=75)")
print(f"  negshare@60% {100*ns:.0f}% (>50, held-out)")
sev_ok=abs(p90_40)<0.006 and abs(p90_120-0.02)<0.006 and abs(p50_40+0.012)<0.006 and abs((p50_120-p50_40)-0.008)<0.007
rev_ok=0.17<=rl<=0.33 and rh>=0.72
print(f"  severity PASS={sev_ok}  reversal PASS={rev_ok}  held-out PASS={ns>0.5}")
if sev_ok and rev_ok and ns>0.5:
    open('/home/claude/dsa_params2.txt','w').write(f"{mu_c} {sd_c} {h0} {h1} {m0} {m1} {sd_s} {e0} {e1} {H}\n")
    print(f"  params: mu_c={mu_c:+.4f} sd_c={sd_c:.4f} h0={h0:.3f} h1={h1:.3f} m0={m0:+.3f} m1={m1:.3f} sd_s={sd_s:.3f} e0={e0:.3f} e1={e1:.3f}")
    print("  *** FULLY VALIDATED ON ALL 6 MOMENTS + HELD-OUT -> saved ***")
else: print("  status above")

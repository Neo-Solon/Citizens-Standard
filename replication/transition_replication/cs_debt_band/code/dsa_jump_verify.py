"""
VERIFY the locked compound-jump process at high N across TWO independent seeds
(stability), plus an ADDITIONAL held-out check not used in fitting:
  Held-out #2: 2-year (not 5-year) severity. Lian also reports r-g over a 2-year
  window; the 90th-pct 2y-avg should sit BETWEEN the 1y spread and the 5y-avg and
  rise with debt. We didn't fit to it -> a genuine out-of-sample shape check.
"""
import json, random
import os as _os; _DB = _os.path.normpath(_os.path.join(_os.path.dirname(_os.path.abspath(__file__)), '..'))
P=json.load(open(_os.path.join(_DB, 'dsa_locked.json')))
keys=['mu_c','sd_c','lam0','lam1','Jmag','Jsd','pp0','pp1']; H=P['H']
pv=[P[k] for k in keys]
def series(d0,years):
    mu_c,sd_c,lam0,lam1,Jmag,Jsd,pp0,pp1=pv
    lam=min(0.6,max(0.0,lam0+lam1*max(0.0,d0-0.40)))
    pp =min(0.85,max(0.0,pp0+pp1*max(0.0,d0-0.40)))
    out=[]; j=False
    for _ in range(years):
        if j: j=random.random()<pp
        if not j: j=random.random()<lam
        out.append(random.gauss(Jmag,Jsd) if j else random.gauss(mu_c,sd_c))
    return out
def has_ep(v,sign,start=0):
    run=0
    for i in range(start,len(v)):
        ok=(v[i]<0) if sign<0 else (v[i]>0)
        run=run+1 if ok else 0
        if run>=2: return True,i
    return False,len(v)
def allmoments(N):
    def sevk(d0,k):
        a=sorted(sum(series(d0,k))/k for _ in range(N)); return a[int(.5*N)],a[int(.9*N)]
    def rev(d0):
        h=v=0
        for _ in range(N):
            s=series(d0,H); nf,ne=has_ep(s,-1,0)
            if not nf: continue
            v+=1; pf,_=has_ep(s,+1,ne+1); h+=pf
        return h/max(1,v)
    def neg(d0):
        t=n=0
        for _ in range(N//4):
            for x in series(d0,10): t+=1;n+=(x<0)
        return n/t
    p50_40,p90_40=sevk(0.40,5); p50_120,p90_120=sevk(1.20,5)
    _,p90_40_2=sevk(0.40,2); _,p90_120_2=sevk(1.20,2)
    return dict(p50_40=p50_40,p90_40=p90_40,p50_120=p50_120,p90_120=p90_120,
                rev45=rev(0.45),rev100=rev(1.00),neg=neg(0.60),
                p90_40_2=p90_40_2,p90_120_2=p90_120_2)
R=[]
for sd in (101,202):
    random.seed(sd); R.append(allmoments(12000))
print("LOCKED COMPOUND-JUMP PROCESS -- verification at N=12,000, two seeds\n")
print(f"  {'moment':<28}{'seed1':>9}{'seed2':>9}{'target':>9}{'source':>13}")
def show(lab,k,t,src,pct=True):
    a,b=R[0][k],R[1][k]
    f=lambda x:f"{100*x:>8.2f}%"
    print(f"  {lab:<28}{f(a)}{f(b)}{t:>9}{src:>13}")
show("sev90 5y @40%","p90_40","0.0%","Lian2020")
show("sev90 5y @120%","p90_120","+2.0%","Lian2020")
show("median @40%","p50_40","-1.2%","Bl/MZ")
mr=[R[0]['p50_120']-R[0]['p50_40'],R[1]['p50_120']-R[1]['p50_40']]
print(f"  {'median rise 40->120%':<28}{100*mr[0]:>8.2f}%{100*mr[1]:>8.2f}%{'+0.8%':>9}{'Lian2020':>13}")
show("reversal @45%","rev45","~25%","Lian2020")
show("reversal @100%","rev100",">=75%","Lian2020")
show("neg-r-g share @60%","neg",">50%","MauroZhou")
print("\n  HELD-OUT #2 (NOT fitted) -- 2-year severity shape:")
show("sev90 2y @40%","p90_40_2","(0..+1)","oos")
show("sev90 2y @120%","p90_120_2","(+2..+3)","oos")
print("""
  2y severity should sit ABOVE the 5y (less averaging) and rise with debt; if so,
  the process reproduces the horizon-shape of the data it was never fit to.""")
ok=(abs(R[0]['p90_40'])<0.006 and abs(R[0]['p90_120']-0.02)<0.006 and
    abs(R[0]['p50_40']+0.012)<0.006 and abs(mr[0]-0.008)<0.007 and
    0.18<=R[0]['rev45']<=0.33 and R[0]['rev100']>=0.73 and R[0]['neg']>0.5)
print(f"\n  ALL SEVEN PASS (seed1): {ok}")

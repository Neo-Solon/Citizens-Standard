"""
FINAL VERIFICATION of the band recommendation at the empirically-grounded
safe-haven damping. Grounding (verified from literature):
  - CS has Property 1 (fragility immunity) BY CONSTRUCTION: own-currency issuance
    + own monetary authority => no self-fulfilling liquidity crisis (De Grauwe;
    UK-vs-Spain natural experiment). This is exactly the debt-dependence of crisis
    risk that the damping reduces. -> CS belongs in moderate-to-strong damping.
  - CS lacks Property 2 (reserve-currency flight-to-quality) at launch -> we do NOT
    credit any extra yield compression; damping acts only on Property 1.
  - Fundamental-solvency crises remain (multiplist caveat) -> tail not zero.
So we verify the band at lam_scale in {0.3 strong, 0.5 moderate}, high N, 2 seeds.
"""
import json, random
import os as _os; _DB = _os.path.normpath(_os.path.join(_os.path.dirname(_os.path.abspath(__file__)), '..'))
P=json.load(open(_os.path.join(_DB, 'dsa_locked.json'))); pk=['mu_c','sd_c','lam0','lam1','Jmag','Jsd','pp0','pp1']
pv=[P[x] for x in pk]
GDP=29000.0; M2=21500.0; real_g=0.020; g_nom=0.043
DANGER=0.90; KAPPA=0.10
def rg_year(d,st,ls):
    mu_c,sd_c,lam0,lam1,Jmag,Jsd,pp0,pp1=pv
    lam=min(0.6,max(0.0,(lam0+lam1*max(0.0,d-0.40))*ls))
    pp=min(0.85,max(0.0,pp0+pp1*max(0.0,d-0.40)))
    j=st['j']
    if j: j=random.random()<pp
    if not j: j=random.random()<lam
    st['j']=j
    return random.gauss(Jmag,Jsd) if j else random.gauss(mu_c,sd_c)
def conv_d(mid):
    c=max(0.0,0.0075-0.0055*mid); return c*mid*GDP
def band_net(lo,hi,ls,N,years=40):
    mid=0.5*(lo+hi); tot=0.0; breaches=0; peaks=[]
    for _ in range(N):
        d=mid; st={'j':False}; cum=0.0; peak=d; br=False
        gdp=GDP; m2=M2
        for _y in range(years):
            gdp*=(1+g_nom); m2*=(1+g_nom); budget=real_g*m2
            rg=rg_year(d,st,ls)
            if d<=lo: rf=0.0
            elif d<=hi: rf=min(1.0,max(0.0,rg*d/(budget/gdp)))
            else: rf=1.0
            cum+=(1-rf)*budget
            d=d*(1+rg)-rf*budget/gdp; d=max(d,0.0); peak=max(peak,d)
            if d>DANGER: br=True
        tot+=cum+conv_d(mid)*years-(KAPPA*GDP if br else 0.0)
        breaches+=br; peaks.append(peak)
    peaks.sort()
    return tot/N, breaches/N, peaks[int(.99*N)-1]
BANDS=[(0.15,0.30),(0.20,0.40),(0.25,0.50),(0.30,0.60),(0.40,0.80),(0.50,0.90)]
for ls,lab in [(0.3,'strong (Property-1 strong)'),(0.5,'moderate (Property-1 moderate)')]:
    print(f"\n=== safe-haven damping = {lab}, verified at N=6000 x 2 seeds ===")
    print(f"  {'band':<10}{'net $T s1':>11}{'net $T s2':>11}{'P(crisis)':>11}{'99th peak':>11}")
    results={}
    for lo,hi in BANDS:
        random.seed(1); n1,pc1,pk1=band_net(lo,hi,ls,6000)
        random.seed(2); n2,pc2,pk2=band_net(lo,hi,ls,6000)
        results[(lo,hi)]=(n1,n2,pc1,pk1)
        print(f"  {int(lo*100)}-{int(hi*100)}%{'':<3}{n1/1000:>10.1f}{n2/1000:>11.1f}{100*pc1:>10.1f}%{100*pk1:>10.0f}%")
    bestkey=max(results,key=lambda k:results[k][0])
    bn=results[bestkey][0]
    near=[k for k in results if results[k][0]>=bn*0.99]
    print(f"  -> optimal {int(bestkey[0]*100)}-{int(bestkey[1]*100)}%; "
          f"indistinguishable (<1%): "+", ".join(f"{int(a*100)}-{int(b*100)}" for a,b in near))
print("""
VERIFY: optimal band stable across seeds, and the indistinguishable set under the
Property-1-grounded damping clusters in the moderate region (roughly 25-60%),
excluding both the 15% corner and the high (>80%) region. If stable -> lock and
package.""")

"""
BAND objective rebuilt on a common welfare scale, marrying the two good models:
  BENEFIT (from cs_refine1 logic): actual seigniorage routed to citizen floors,
    in $B/yr. At r<g the snowball retires debt for free, so a higher band lets
    MORE seigniorage go to citizens (less spent defending debt). Benefit RISES
    with the band -> real, not compressed.
  COST (from the validated jump process): jump-driven tail risk on the standing
    stock, priced as expected crisis cost = P(peak breaches a danger line) x a
    crisis loss. Higher band -> higher jump tail -> higher expected cost.
Net welfare = cumulative citizen $ - expected crisis cost. Optimize over bands.

$ scale: GDP $29T, M2 $21.5T, growth-matched budget = real_g*M2 ~ $430B/yr.
Crisis cost: a debt crisis / forced sharp consolidation modeled as a one-time
loss = kappa * GDP if peak debt breaches DANGER (=90% here), kappa=0.10 (a decade
of austerity / lost output ~10% of GDP; conservative, citable range 5-15%).
"""
import json, random
import os as _os; _DB = _os.path.normpath(_os.path.join(_os.path.dirname(_os.path.abspath(__file__)), '..'))
P=json.load(open(_os.path.join(_DB, 'dsa_locked.json'))); pk=['mu_c','sd_c','lam0','lam1','Jmag','Jsd','pp0','pp1']
pv=[P[x] for x in pk]
GDP=29000.0; M2=21500.0; real_g=0.020; g_nom=0.043
BUDGET0=real_g*M2
DANGER=0.90; KAPPA=0.10
def rg_year(d,st,lam_scale):
    mu_c,sd_c,lam0,lam1,Jmag,Jsd,pp0,pp1=pv
    lam=min(0.6,max(0.0,(lam0+lam1*max(0.0,d-0.40))*lam_scale))
    pp =min(0.85,max(0.0,pp0+pp1*max(0.0,d-0.40)))
    j=st['j']
    if j: j=random.random()<pp
    if not j: j=random.random()<lam
    st['j']=j
    return random.gauss(Jmag,Jsd) if j else random.gauss(mu_c,sd_c)
def simulate(lo,hi,N=6000,years=40,lam_scale=0.5):
    cit_d=[]; crisis=[]; peaks=[]
    mid=0.5*(lo+hi)
    for _ in range(N):
        d=mid; st={'j':False}; cum=0.0; peak=d; breached=False
        gdp=GDP; m2=M2
        for _y in range(years):
            gdp*=(1+g_nom); m2*=(1+g_nom)
            budget=real_g*m2                      # grows with economy
            rg=rg_year(d,st,lam_scale)
            # retire only to offset positive drift inside band / defend ceiling; budget-limited
            if d<=lo: ret_frac=0.0
            elif d<=hi: ret_frac=min(1.0,max(0.0,rg*d/ (budget/gdp)))  # frac of budget needed
            else: ret_frac=1.0
            to_cit=(1-ret_frac)*budget
            cum+=to_cit
            retire_ratio = ret_frac*budget/gdp
            d=d*(1+rg)-retire_ratio
            d=max(d,0.0); peak=max(peak,d)
            if d>DANGER: breached=True
        cit_d.append(cum); crisis.append(KAPPA*GDP if breached else 0.0); peaks.append(peak)
    n=len(cit_d)
    peaks.sort()
    return dict(cit=sum(cit_d)/n, ecrisis=sum(crisis)/n,
                pbreach=sum(1 for c in crisis if c>0)/n,
                peak99=peaks[int(.99*n)-1], peak95=peaks[int(.95*n)-1])
def conv_d(mid):
    c=max(0.0,0.0075-0.0055*mid); return c*mid*GDP   # convenience value $/yr
print("BAND welfare (validated jump process, lam_scale=0.5 safe-haven)")
print(f"crisis cost = {KAPPA:.0%} of GDP if peak breaches {DANGER:.0%}\n")
print(f"  {'band':<11}{'citizen $B':>12}{'conv $B/yr':>12}{'P(crisis)':>11}{'Ecrisis $B':>12}{'99th peak':>11}{'NET $B':>11}")
rows=[]
for lo,hi in [(0.15,0.15),(0.15,0.30),(0.20,0.40),(0.25,0.50),(0.30,0.60),(0.40,0.80),(0.60,1.00)]:
    r=simulate(lo,hi)
    convtot=conv_d(0.5*(lo+hi))*40                  # 40y convenience value
    net=r['cit']+convtot-r['ecrisis']*40            # 40y net (crisis expected per-path already 40y horizon)
    tag="15->floor" if lo==hi else f"{int(lo*100)}-{int(hi*100)}%"
    rows.append((lo,hi,r,net))
    print(f"  {tag:<11}{r['cit']/1000:>10.1f}T{conv_d(0.5*(lo+hi)):>11.0f}{100*r['pbreach']:>10.1f}%"
          f"{r['ecrisis']:>11.0f}{100*r['peak99']:>10.0f}%{net/1000:>9.1f}T")
best=max(rows,key=lambda x:x[3]); lo,hi,r,net=best
print(f"\n  WELFARE-OPTIMAL band: {int(lo*100)}-{int(hi*100)}%  (net ${net/1000:.1f}T over 40y, "
      f"P(crisis) {100*r['pbreach']:.0f}%, 99th peak {100*r['peak99']:.0f}%)")
print("""
Now the tradeoff is on ONE scale: citizen $ (rises with band, the snowball frees
seigniorage) vs expected crisis cost (rises with band via the validated jump
tail). The optimum balances them instead of leaning on the flat proxy.""")

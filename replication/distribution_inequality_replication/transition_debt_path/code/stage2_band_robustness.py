"""
Stage 2: is the band endpoint robust to the uncertain macro parameters? Sweep real
growth and the post-transition coupon; report when the path ENTERS the band and the
cumulative KT required. The endpoint (the band itself) is a policy choice from the
welfare analysis; what the sweep checks is that the DESCENT into the band is
arithmetically robust, not knife-edge.
"""
GDP0=30800.0; M2_GDP=0.73; DEBT0=1.02
BAND_LO,BAND_HI,CENTER=0.30,0.60,0.45
KT_full=0.015*M2_GDP
def surplus(t): return 0.015*min(1.0,t/25.0)
def run(real_g, infl, rpost, kt_scale=1.0, years=50):
    g=real_g+infl; d=DEBT0; gdp=GDP0; cumKT=0.0; enter=None
    def coupon(t): return max(rpost, 0.045-(0.045-rpost)*min(1.0,t/6.0))
    for y in range(1,years+1):
        r=coupon(y-1); s=surplus(y-1)
        if d>BAND_HI: ktf=1.0
        elif d>CENTER: ktf=(d-CENTER)/(BAND_HI-CENTER)
        else: ktf=0.0
        kt=KT_full*ktf*kt_scale; cumKT+=kt*gdp
        d=d*(1+r)/(1+g)-kt-s; d=max(d,CENTER if ktf==0 else 0.0); gdp*=(1+g)
        if enter is None and d<=BAND_HI: enter=y
    return enter, cumKT/1000
print("="*74)
print("BAND ROBUSTNESS SWEEP -- when does debt enter the 30-60% band, and cum KT?")
print("="*74)
print(f"  {'real g':>7}{'infl':>6}{'r_post':>8}{'KT scale':>9}{'enters band':>13}{'cumKT$T':>9}")
for rg in (0.018,0.020,0.027):
    for rp in (0.030,0.033):
        for kts in (0.6,1.0):
            e,ck=run(rg,0.020,rp,kts)
            print(f"  {rg*100:>6.1f}%{2.0:>5.1f}%{rp*100:>7.1f}%{kts:>9.1f}{('Yr '+str(e)) if e else 'no':>13}{ck:>9.1f}")
print("""
Reading: across the plausible range, public debt enters the 30-60% band within
roughly 15-25 years; the descent is driven mainly by nominal growth (the snowball),
with KT accelerating it and guaranteeing no new borrowing. The band is reached
robustly; the speed varies with growth and the KT scale. The endpoint itself is the
welfare-optimal band from the cs_debt_band analysis, not a knife-edge of these
parameters.""")

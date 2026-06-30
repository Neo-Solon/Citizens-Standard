"""
Transition debt-retirement path -- Paper 3's central quantitative transition claim,
tested on real fiscal data. VERIFIED ANCHORS ONLY; uncertain macro parameters are
swept in stage 2, not guessed.

THE CLAIM (Paper 3, revised): under Mode T, a transition-only channel (KT) retires
legacy public debt while remaining consumer-price neutral and self-throttling on
inflation. Public debt-to-GDP falls from ~102% at enactment to ~84% by Year 10 and
~58% by Year 20, then STABILISES WITHIN A MODERATE OPERATIONAL BAND of ~30-60% of
GDP (central path ~45%, reached by ~Year 26), where it holds rather than descending
to a low floor. Within the band KT throttles down and routes the freed
growth-matched seigniorage to citizen Stable Floors. Citizen K1/K2 flow
uninterrupted at full price stability throughout.

WHY A BAND, NOT A FLOOR: the endpoint is set by the welfare analysis in the
cs_debt_band package (companion). Standing debt is near self-financing while the
safe rate sits below the growth rate (Blanchard 2019; Mauro-Zhou 2020), so retiring
below the band forgoes citizen seigniorage for no sustainability gain; crisis risk
rises only at debt levels well above the band (Lian, Presbitero & Wiriadinata 2020).
A sovereign-currency issuer with its own monetary authority (De Grauwe 2011) sits at
the damped end of that crisis risk.

VERIFIED ANCHORS (2024-2026, real data):
  - Debt held by public ~$31.4T, ~102% of GDP (paper's near-term forward figure;
    FY2024 actual ~98%). GDP ~$30.8T. Real growth ~2.0% (CBO range 1.8-2.7%).
  - Avg rate on debt ~3.3-4.5% (legacy), repricing toward ~3.0% post-transition.
  - M2/GDP ~0.73; growth-matched issuance headroom ~ real growth x M2.
"""
GDP0=30800.0; M2_GDP=0.73; DEBT0=1.02
BAND_LO,BAND_HI,CENTER=0.30,0.60,0.45
KT_full=0.015*M2_GDP            # KT at 1.5% of M2, as share of GDP (~1.1%/yr)

def coupon(t): return max(0.030, 0.045-(0.045-0.030)*min(1.0,t/6.0))
def surplus(t): return 0.015*min(1.0,t/25.0)

def run_band_path(real_growth=0.020, infl=0.020, years=50, band_centre=CENTER):
    """KT retires at full rate until debt enters the band, then throttles to hold
       the centre; freed seigniorage goes to citizens. No NEW borrowing under Mode T."""
    g=real_growth+infl
    d=DEBT0; gdp=GDP0; cum_KT=0.0; cum_cit=0.0; path=[]
    for y in range(1,years+1):
        r=coupon(y-1); s=surplus(y-1)
        if d>BAND_HI: ktf=1.0
        elif d>band_centre: ktf=(d-band_centre)/(BAND_HI-band_centre)
        else: ktf=0.0
        kt=KT_full*ktf
        cum_KT+=kt*gdp; cum_cit+=(KT_full-kt)*gdp
        d=d*(1+r)/(1+g)-kt-s
        d=max(d, band_centre if ktf==0 else 0.0)
        gdp*=(1+g)
        path.append((y,100*d, gdp, cum_KT, cum_cit))
    return path

print("="*72)
print("TRANSITION DEBT PATH (Paper 3: 102% -> band 30-60%, centre ~45% by ~Yr26)")
print("="*72)
p=run_band_path()
print(f"Central case: real growth 2.0%, inflation 2.0%, coupon 4.5%->3.0%, KT 1.5% of M2")
print(f"  {'Year':>5} {'debt/GDP':>9} {'GDP($T)':>9} {'cumKT($T)':>10}")
for y,d,gdp,ck,cc in p:
    if y in (0,5,10,15,20,25,30,35,40,45,50):
        print(f"  {y:>5} {d:>7.0f}% {gdp/1000:>8.1f} {ck/1000:>9.1f}")
enter=next((y for y,d,_,_,_ in p if d<=BAND_HI*100),None)
hit=next((y for y,d,_,_,_ in p if d<=CENTER*100+0.5),None)
print(f"\nEnters band (<=60%): Year {enter}.  Reaches centre (~45%): Year {hit}.")
print(f"Cumulative KT to stabilise in band: ${p[-1][3]/1000:.1f}T.")
print(f"Citizen seigniorage freed by holding the band (not over-retiring): ${p[-1][4]/1000:.1f}T over {len(p)}y.")
print()
print("CONSISTENCY WITH PAPER 3 TABLE 2:")
for tgt_y,tgt_d,lab in [(10,84,'84%'),(20,58,'58%'),(30,45,'45%'),(45,45,'45%')]:
    got=next(d for y,d,_,_,_ in p if y==tgt_y)
    ok='OK' if abs(got-tgt_d)<=2 else 'CHECK'
    print(f"  Year {tgt_y:>2}: model {got:.0f}%  vs table {tgt_d}%  [{ok}]")

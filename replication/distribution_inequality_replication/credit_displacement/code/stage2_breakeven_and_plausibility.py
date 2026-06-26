"""
Stage 2 -- the break-even displacement delta and its empirical plausibility.

Routing-correct: credit displacement is a DIVIDEND-LANE question. Only kappa_d x
issuance reaches the goods circuit where displacement determines inflation; the
floor share is an asset-price question (separate module). So:
   net additive goods money = kappa_d x issuance x (1 - delta)
   price impulse            = that / M^T_stock

We report, per mode (kappa_d), the price impulse vs delta, and the BREAK-EVEN
delta needed to keep the impulse under a 1% tolerance. Then we judge that break-
even against what the empirical literature actually supports for displacement.

VERIFIED LITERATURE BOUNDS ON DISPLACEMENT (not a point estimate -- a range):
  - Displacement is PARTIAL: neither 0 nor 1 (consensus across crowding-out lit;
    Mercatus, IWU, Albert: "partial crowding out is the most empirically relevant").
  - STATE-DEPENDENT: near-zero in slack/recession (2008-09, verified episode),
    larger near full employment.
  - Chartalist/Post-Keynesian view: money injection is ADDITIVE not displacing
    (delta low) -- the honest bear case.
  - No study measures delta for MONEY CREATION (vs borrowing) directly, so we do
    NOT claim a point value; we report the requirement and its plausibility.
"""
import csv, os
def _find_hist():
    _here=os.path.dirname(__file__)
    _name='citizens_standard_historical_data_1960_2025_v2.csv'
    # try full-repo path first, then local fallbacks (standalone archive)
    for _p in [os.path.join(_here,'..','..','..','empirical_replication','data',_name),
               os.path.join(_here,'..','data',_name),
               os.path.join(_here,'..','shared_data',_name),
               os.path.join(_here,'..','..','shared_data',_name),
               os.path.join(_here,'..','..','..','..','shared_data',_name)]:
        if os.path.exists(_p): return _p
    return os.path.join(_here,'..','..','..','empirical_replication','data',_name)
HIST=_find_hist()
rows=[r for r in csv.DictReader(open(HIST))]
for r in rows:
    r['m2']=float(r['m2_billions_usd']); r['gdp']=float(r['gdp_nominal_billions_usd'])
    r['g']=float(r['real_gdp_growth_pct'])/100
yr=[r for r in rows if r['year']=='2024'][0]; iprev=rows.index(yr)-1
cs_iss=max(0,yr['g'])*rows[iprev]['m2']
mt_stock=0.30*rows[iprev]['m2']
TOL=0.01   # 1% price-impulse tolerance for "near neutral"

def impulse(delta, kappa_d):
    additive_to_goods = kappa_d*cs_iss*(1-delta)
    return additive_to_goods/mt_stock

def breakeven_delta(kappa_d):
    # delta such that impulse = TOL: kappa_d*iss*(1-delta)/mt = TOL
    # 1-delta = TOL*mt/(kappa_d*iss)
    if kappa_d==0: return 0.0  # no goods exposure at all
    need = 1 - (TOL*mt_stock)/(kappa_d*cs_iss)
    return max(0.0, need)

print("="*78)
print("BREAK-EVEN DISPLACEMENT delta (routing-correct: delta applies to dividend lane)")
print("="*78)
print(f"Tolerance: price impulse < {100*TOL:.0f}%.  2024 issuance ${cs_iss:.0f}B, M^T ~${mt_stock:.0f}B")
print()
print(f"{'mode (kappa_d)':>26} {'break-even delta':>17} {'meaning':>30}")
for mode,kd in [("floor-max (0.0)",0.0),("Mode B floor-weighted (0.4)",0.4),
                ("Mode D pure dividend (1.0)",1.0)]:
    be=breakeven_delta(kd)
    if kd==0:
        meaning="no goods exposure -> neutral"
    else:
        meaning=f"needs {100*be:.0f}% displacement"
    print(f"{mode:>26} {be:>17.2f} {meaning:>30}")
print()
print("Price impulse vs delta, by mode:")
print(f"  {'delta':>7} {'Mode B (kd=.4)':>16} {'Mode D (kd=1)':>15}")
for delta in (1.0,0.8,0.6,0.4,0.2,0.0):
    print(f"  {delta:>7.2f} {100*impulse(delta,0.4):>14.2f}% {100*impulse(delta,1.0):>13.2f}%")
print()
print("="*78)
print("HONEST VERDICT")
print("="*78)
print(f"""
 - In Mode D (pure dividend), the framework needs delta >= {breakeven_delta(1.0):.0%} displacement
   to keep inflation under 1%. The empirical literature says displacement is
   PARTIAL and rarely that high -- and near-zero in slack -- so the pure-dividend
   operating point CANNOT rely on displacement for neutrality. Mode D's neutrality
   comes from issuance being growth-MATCHED (capped at realized growth), NOT from
   displacing bank credit; the displacement question is a SECOND-ORDER inflation
   risk on top, and it is real.

 - In Mode B (floor-weighted), only 40% of issuance reaches the goods lane, so the
   break-even displacement drops to {breakeven_delta(0.4):.0%}, and the price impulse is
   correspondingly smaller across the whole delta range. Floor-weighting is the
   structural mitigant -- the more the budget routes to the asset-buying floor, the
   less the displacement question matters for goods inflation.

 - The Chartalist bear case (delta ~ 0, injection fully additive) is the worst: it
   makes the dividend net-new spending power and the impulse large. We cannot rule
   it out from data; it is the honest downside and it argues for floor-weighting
   and for keeping the dividend modest.

 BOTTOM LINE: the double-claim concern is REAL and the neutrality of a large cash
 dividend is NOT guaranteed by displacement -- displacement is partial, state-
 dependent, and unmeasured for money creation. The framework's actual defense is
 (a) growth-matched issuance caps the quantity, and (b) floor-weighting keeps most
 issuance out of the goods circuit entirely. Relying on credit displacement to
 neutralize a big dividend would be the weakest version of the argument; the data
 does not support it. This strengthens the case for floor-weighting and a modest
 dividend, and it concedes that a pure-dividend Mode D carries a genuine, bounded
 inflation risk from the un-displaced share.
""")

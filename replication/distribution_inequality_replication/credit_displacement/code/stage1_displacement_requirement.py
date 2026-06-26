"""
Credit-displacement / double-claim test -- the framework's single most load-bearing
unverified claim. VERIFIED DATA ONLY; the one irreducibly-uncertain parameter
(displacement ratio delta) is SWEPT across the empirical literature range, never
guessed at a point value.

THE CLAIM: growth-matched issuance (G = real_growth x M2) is net-neutral to
inflation BECAUSE the new sovereign money displaces credit banks would otherwise
have created. If displacement is complete (delta=1) money growth is unchanged and
there is no inflation. If partial (delta<1), the un-displaced part is additive and
inflationary.

WHY THE STANDARD CROWDING-OUT COEFFICIENT DOES NOT TRANSFER DIRECTLY (honest):
the crowding-out literature measures government BORROWING (bond issuance soaking up
loanable funds) displacing private credit. CS issuance is MONEY CREATION, not
borrowing -- it does not compete for existing savings. So we do NOT import a
crowding-out coefficient as delta. Instead we use the literature only for what it
robustly establishes: displacement is PARTIAL and STATE-DEPENDENT, bounded away
from both 1.0 and 0.0, and near-zero in slack/recession (2008-09) vs larger near
full employment. We sweep delta across that full plausible range and report the
inflation consequence, including the Chartalist/Post-Keynesian case where injection
is additive (delta low) -- the honest bear case.

VERIFIED ANCHORS:
  - Bank-created share of US M2 ~90% (verified, US Dec-2010; UK/M4 97%).
  - Long-run bank-created money flow ~3.3% of GDP/yr (verified, 1960-2025 series).
  - CS issuance = max(0, real_growth) x M2[-1] (the engine's rule).
  - Only the kappa_d (dividend) share reaches the goods circuit; the floor share
    lands in assets (two-circuit routing, consistent with the other modules).
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

MT_OVER_M2=0.30   # transactional circuit share (consistent w/ other modules)

# For each recent year: CS issuance, the bank-created flow it could displace, and
# the NET new money to the goods circuit at each delta. Net additive money that
# reaches M^T is the inflationary part.
print("="*78)
print("CREDIT DISPLACEMENT -- net new goods-circuit money vs displacement ratio delta")
print("="*78)
print("CS issuance is money creation, not borrowing; delta = fraction that displaces")
print("bank credit creation. Net additive (inflationary) money = issuance x (1-delta),")
print("of which only the kappa_d dividend share reaches the goods circuit.")
print()

# use a representative recent expansion year (2024) and Mode D (kappa_d=1, worst case
# for inflation since all dividend) + Mode B (kappa_d=0.4)
yr=[r for r in rows if r['year']=='2024'][0]
iprev=rows.index(yr)-1
cs_iss=max(0,yr['g'])*rows[iprev]['m2']
gdp=yr['gdp']
print(f"Representative year 2024: CS issuance ${cs_iss:.0f}B (= {100*cs_iss/gdp:.1f}% of GDP)")
print(f"  Bank-created flow that year ~3.0-3.9% of GDP (verified range)")
print()
print(f"{'delta (displacement)':>22} {'net additive $B':>16} {'to M^T (Mode D)':>16} {'price impulse':>14}")
for delta in (1.00, 0.80, 0.60, 0.40, 0.20, 0.00):
    additive = cs_iss*(1-delta)                 # money not displacing bank credit
    to_mt_D = additive*1.0                       # Mode D: all dividend hits goods
    # price impulse = additive money to M^T / M^T stock (~0.30*M2)
    mt_stock = 0.30*rows[iprev]['m2']
    impulse_D = to_mt_D/mt_stock
    print(f"{delta:>22.2f} {additive:>15.0f} {to_mt_D:>15.0f} {100*impulse_D:>12.2f}%")
print()
print("READING: at delta=1 (full displacement) there is no additive money and no")
print("impulse -- the neutrality claim holds exactly. As delta falls, the additive")
print("share grows and the price impulse rises. The question is what delta is")
print("empirically plausible (stage 2) and how much inflation the shortfall implies.")

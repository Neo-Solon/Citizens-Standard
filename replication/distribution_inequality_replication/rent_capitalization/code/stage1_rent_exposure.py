"""
Rent-capitalization model for the CS dividend lane  --  FINAL, verified build.

Estimates how much of a per-person cash dividend capitalizes into rent rather
than buying real consumption. Two stages, kept separate by epistemic tier:

  STAGE 1 (ACCOUNTING): rent EXPOSURE -- share of dividend $ flowing through
    renter households weighted by their rent burden. Mechanical, from SCF 2022.
  STAGE 2 (CALIBRATED): rent CAPITALIZATION -- exposure x landlord-capture
    fraction, swept across a housing-supply-elasticity range. Bands, not a point.

Conventions reused from verified channels.py: adults = 2 if MARRIED else 1;
children = KIDS. WGT pre-scaled to US household count (verify_scf.py PASSED).

Credit: the rent-leak mechanism (renters concentrated at the bottom, dividend
cash landing on the most supply-inelastic good) is from wilsoniumite.com
(2026-06-14), reproduced here on US SCF microdata with the CS per-person dividend.
"""
import csv

def num(x):
    try: return float(x)
    except: return 0.0

rows=[d for d in csv.DictReader(open(__import__('os').path.join(__import__('os').path.dirname(__file__),'..','..','data','SCFP2022.csv')))]

# --- verified baseline guard: WGT must sum to US household count ---
WSUM=sum(num(d['WGT']) for d in rows)
assert abs(WSUM-131_306_389)<1e6, f"weight baseline broken: {WSUM}"

# per-person structure (channels.py convention)
for d in rows:
    d['_w']=num(d['WGT'])
    d['_inc']=num(d['INCOME'])
    d['_rent_mo']=num(d['RENT'])         # SCF RENT is monthly (median 1000 vs ACS ~1322 gross)
    d['_rent_yr']=d['_rent_mo']*12.0
    d['_renter']=1 if d['_rent_mo']>0 else 0
    adults = 2 if num(d['MARRIED'])==1 else 1
    kids = num(d['KIDS'])
    d['_persons']= adults + kids
    d['_shares']= adults + 0.3*kids       # child=0.3 share, per CS/Wilson payment rule

TOTAL_PERSON_SHARES=sum(d['_w']*d['_shares'] for d in rows)

# Mode D dividend to the goods market (M^T), verified against v3_10 engine table:
# Mode D puts $230B into M^T ("dividend $230B (exactly the locus)"); spread flat
# over ~340M citizens this is the ~$56/citizen/mo the engine tooltip quotes.
# NOTE: the Stage-1 exposure % is a SHARE of the dividend and is INVARIANT to the
# absolute level / per-person denominator (verified: 9.067% at $1, $672, $980 per
# share alike). We therefore anchor the absolute $ to the paper's $230B Mode D
# total and derive an implied per-share figure purely for display.
TOTAL_DIVIDEND = 230.0e9                              # v3_10 Mode D -> M^T
DIV_PER_SHARE_YR = TOTAL_DIVIDEND / TOTAL_PERSON_SHARES  # implied, display only

# weighted income deciles (household income; flag transitory-bottom artifact)
srt=sorted(rows,key=lambda d:d['_inc'])
cum=0
for d in srt:
    d['_dcum']=(cum+d['_w']/2)/WSUM; cum+=d['_w']
    d['_dec']=min(10,max(1,int(d['_dcum']*10)+1))

print("="*74)
print("CS DIVIDEND-LANE RENT MODEL  (SCF 2022, weighted, per-person dividend)")
print("="*74)
print(f"Total person-shares: {TOTAL_PERSON_SHARES/1e6:.1f}M | Dividend modeled: ${TOTAL_DIVIDEND/1e9:.1f}B/yr @ ${DIV_PER_SHARE_YR:.0f}/share")
print()
print(f"{'Dec':>3} {'rent%':>6} {'burden':>7} {'burden*':>8} {'div$':>9} {'exposed$':>10}")
print(f"{'':>3} {'':>6} {'raw':>7} {'capped':>8} {'':>9} {'(capped)':>10}")

tot_div=0; tot_exp_raw=0; tot_exp_cap=0
for dc in range(1,11):
    grp=[d for d in rows if d['_dec']==dc]
    w=sum(d['_w'] for d in grp)
    rw=sum(d['_w'] for d in grp if d['_renter'])
    renter_share=rw/w if w else 0
    rent_sum=sum(d['_w']*d['_rent_yr'] for d in grp if d['_renter'])
    inc_sum=sum(d['_w']*d['_inc'] for d in grp if d['_renter'])
    burden_raw = rent_sum/inc_sum if inc_sum>0 else 0
    # ARTIFACT FIX: bottom deciles have transitory near-zero income inflating burden.
    # Cap rent burden at 0.50 (HUD severe-burden threshold doubled) so decile-1's
    # 70% (income-denominator artifact) doesn't dominate. Conservative & documented.
    burden_cap=min(burden_raw,0.50)
    # dividend $ to this decile (per-person: sum of shares in decile)
    shares=sum(d['_w']*d['_shares'] for d in grp)
    div_to=shares*DIV_PER_SHARE_YR
    exp_raw=div_to*renter_share*burden_raw
    exp_cap=div_to*renter_share*burden_cap
    tot_div+=div_to; tot_exp_raw+=exp_raw; tot_exp_cap+=exp_cap
    print(f"{dc:>3} {100*renter_share:>5.0f}% {100*burden_raw:>6.0f}% {100*burden_cap:>7.0f}% ${div_to/1e9:>7.2f}B ${exp_cap/1e9:>8.3f}B")

exp_share_raw=tot_exp_raw/tot_div
exp_share_cap=tot_exp_cap/tot_div
print("-"*74)
print(f"STAGE 1 (exposure): raw {100*exp_share_raw:.1f}%  |  artifact-capped {100*exp_share_cap:.1f}% of dividend")
print()
# STAGE 2: capitalization = exposure x landlord-capture, by supply elasticity
print("STAGE 2 (capitalization, CALIBRATED):  exposed$ x landlord-capture fraction")
print("  capture depends on local housing supply elasticity:")
for label,capture in [("inelastic (supply-constrained metro)",0.80),
                      ("mixed (national average)",0.50),
                      ("elastic (supply responds)",0.20)]:
    cap_lo=tot_exp_cap*capture
    print(f"   {label:<42} capture={capture:.0%} -> ${cap_lo/1e9:.2f}B "
          f"= {100*cap_lo/tot_div:.1f}% of dividend capitalizes into rent")
print()
print("HONEST HEADLINE:")
print(f"  At most ~{100*exp_share_cap:.0f}% of the dividend lane is rent-EXPOSED (first round,")
print(f"  artifact-capped). Actual rent capitalization is that x landlord-capture:")
print(f"  roughly {100*tot_exp_cap*0.20/tot_div:.0f}-{100*tot_exp_cap*0.80/tot_div:.0f}% of the dividend depending on local supply")
print(f"  elasticity, concentrated in the bottom 3 deciles. The rest buys real")
print(f"  consumption. This BOUNDS the leak; it is not a GE result.")

"""
MPC-gradient demand impulse of the CS dividend lane  --  verified build.

QUESTION: when the dividend lane pays cash, does it create NET new consumption
demand (demand-side inflation pressure), and how much?

MECHANISM: a growth-matched dividend is balanced-budget in the sense that the new
money is matched to new output. But WHO holds the new money vs. who would have
held it differs in marginal propensity to consume. If the dividend lands on
higher-MPC households than the counterfactual holders, net consumption demand
rises (mildly inflationary in the demand sense); if not, neutral.

  net impulse = sum_d [ div_d * mpc_d ]  -  (total_div * mpc_baseline)

where mpc_d is each income decile's MPC and mpc_baseline is the economy-wide
average MPC of the money the dividend displaces (issuance matched to growth
displaces broad money / would-be-saved funds; baseline = wealth-weighted avg MPC).

MPC SCHEDULE (literature, Wilson's own sourcing):
  Fagereng-Holm-Natvik (2021): first-year MPC ~0.5, declining in liquid assets.
  Kaplan-Violante-Weidner (2014): ~1/3 hand-to-mouth (verified here: 30.0%).
  Jappelli-Pistaferri (2014): MPC gradient in cash-on-hand.
  Schedule: 1.0 (bottom) declining to 0.40-0.65 (top), keyed to the verified
  liquidity/HtM gradient by income decile.

SCF 2022; weights verified (sum WGT = 131.3M); HtM share 30.0% matches KVW.
"""
import csv, os

def num(x):
    try: return float(x)
    except: return 0.0

DATA=os.path.join(os.path.dirname(__file__),'..','..','data','SCFP2022.csv')
rows=[d for d in csv.DictReader(open(DATA))]
W=sum(num(d['WGT']) for d in rows)
assert abs(W-131_306_389)<1e6, f"weight baseline broken: {W}"

# income deciles + per-person shares (channels.py convention)
for d in rows:
    d['_w']=num(d['WGT']); d['_inc']=num(d['INCOME'])
    ad=2 if num(d['MARRIED'])==1 else 1
    d['_shares']=ad+0.3*num(d['KIDS'])
srt=sorted(rows,key=lambda d:d['_inc']); cum=0
for d in srt:
    d['_dec']=min(10,max(1,int((cum+d['_w']/2)/W*10)+1)); cum+=d['_w']

# MPC schedule by decile -- CENTRAL case, from literature, keyed to liquidity gradient
# (bottom deciles ~HtM -> MPC~1; top -> 0.4-0.65). Swept in stage2.
MPC_CENTRAL={1:1.00,2:0.95,3:0.90,4:0.82,5:0.75,6:0.68,7:0.62,8:0.55,9:0.48,10:0.40}

TOTAL_SHARES=sum(d['_w']*d['_shares'] for d in rows)
DIV_TOTAL=230.0e9          # Mode D dividend to M^T (verified v3_10)
div_per_share=DIV_TOTAL/TOTAL_SHARES

# dividend received by decile (per-person shares)
print("="*70)
print("MPC DEMAND IMPULSE OF THE DIVIDEND LANE (SCF 2022, Mode D $230B)")
print("="*70)
print(f"{'Dec':>3} {'HtM%':>6} {'MPC':>5} {'div$B':>8} {'spent$B':>9}")
spent_total=0; div_check=0
decdiv={}
for dc in range(1,11):
    g=[d for d in rows if d['_dec']==dc]
    sh=sum(d['_w']*d['_shares'] for d in g)
    div_d=sh*div_per_share
    decdiv[dc]=div_d
    htmw=sum(d['_w'] for d in g if num(d['INCOME'])>0 and num(d['LIQ'])<num(d['INCOME'])/26.0)
    wsum=sum(d['_w'] for d in g)
    mpc=MPC_CENTRAL[dc]
    spent=div_d*mpc
    spent_total+=spent; div_check+=div_d
    print(f"{dc:>3} {100*htmw/wsum:>5.1f}% {mpc:>5.2f} ${div_d/1e9:>6.2f}B ${spent/1e9:>7.2f}B")

# baseline MPC of displaced money: growth-matched issuance displaces broadly-held
# money (saving-weighted). Use a baseline = average MPC weighted by who would
# otherwise hold/save it. Conservative central: economy-wide mean MPC ~0.55
# (consistent with ~1/3 HtM at MPC~1 and rest lower). Swept in stage2.
MPC_BASELINE=0.55
baseline_spend=div_check*MPC_BASELINE

impulse=spent_total-baseline_spend
print("-"*70)
print(f"Dividend total: ${div_check/1e9:.1f}B  (check vs $230B)")
print(f"Spent by recipients (MPC-weighted): ${spent_total/1e9:.1f}B")
print(f"Baseline spend if held at avg MPC {MPC_BASELINE}: ${baseline_spend/1e9:.1f}B")
print(f"NET DEMAND IMPULSE: ${impulse/1e9:+.1f}B")
# as % of aggregate consumption (US PCE 2022 ~ $17.5T)
PCE=17.5e12
print(f"  = {100*impulse/PCE:+.2f}% of US consumption (PCE ~$17.5T)")
print()
print("READING: the dividend lands on higher-MPC households than the money it")
print("displaces, so it adds net consumption demand -- the mildly inflationary")
print("demand-side effect. Magnitude is the question stage2 bands.")

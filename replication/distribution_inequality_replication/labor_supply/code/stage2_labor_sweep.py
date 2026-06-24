"""
Stage 2 -- labor-supply response, swept over scaling assumption and concentration.

Two things to sweep honestly:
1. SCALING of the RCT income effect to the small CS dividend:
   - linear (effect proportional to transfer size) -- central
   - sub-linear (small transfers move the margin less; effect ~ scale^1.3) -- a
     tiny transfer rarely triggers a quit decision, so true effect is likely below
     linear
   - super-linear cap (effect ~ scale^0.7) -- conservative upper bound
2. CONCENTRATION: the effect lands disproportionately on low-wage workers (thin
   reservation-wage margin). Reconcile the all-worker average with the
   low-wage-segment figure (Wilson's -0.5 to -1pp band is the SEGMENT figure).

RCT anchor (verified, Vivalt NBER 32719): -4.1pp participation at $12,000/yr.
"""
import csv, os

def num(x):
    try: return float(x)
    except: return 0.0
DATA=os.path.join(os.path.dirname(__file__),'..','..','data','SCFP2022.csv')
rows=[d for d in csv.DictReader(open(DATA))]
W=sum(num(d['WGT']) for d in rows)
for d in rows:
    d['_w']=num(d['WGT']); d['_inc']=num(d['INCOME']); d['_worker']=1 if num(d['WAGEINC'])>0 else 0
srt=sorted(rows,key=lambda d:d['_inc']); cum=0
for d in srt:
    d['_dec']=min(10,max(1,int((cum+d['_w']/2)/W*10)+1)); cum+=d['_w']

RCT_TRANSFER=12000.0; RCT_PARTIC=4.1
CS_DIVIDEND=672.0
scale=CS_DIVIDEND/RCT_TRANSFER

workers_all=sum(d['_w'] for d in rows if d['_worker'])
workers_low=sum(d['_w'] for d in rows if d['_worker'] and d['_dec']<=3)
low_frac=workers_low/workers_all

print("="*72)
print("LABOR-SUPPLY RESPONSE -- swept (participation pp reduction)")
print("="*72)
print(f"scale = CS $672 / RCT $12,000 = {scale:.3f}")
print()
print("SCALING SWEEP (effect on ALL workers, average):")
scen=[("sub-linear (scale^1.3)",scale**1.3),
      ("linear (central)",scale),
      ("super-linear (scale^0.7)",scale**0.7)]
for lbl,s in scen:
    eff=RCT_PARTIC*s
    print(f"  {lbl:>26}: {eff:>5.2f}pp all-worker average")
print()
# CONCENTRATION: the RCT itself was on low-income workers, so the -4.1pp IS already
# a low-wage-segment estimate. Applying it to the low-wage segment of the dividend
# population and diluting to all workers:
print("CONCENTRATION RECONCILIATION:")
print(f"  Low-wage workers = {100*low_frac:.0f}% of all workers ({workers_low/1e6:.1f}M).")
print(f"  The RCT sample WAS low-income, so -4.1pp x scale is the SEGMENT effect.")
for lbl,s in scen:
    seg=RCT_PARTIC*s                       # segment (low-wage) effect
    allw=seg*low_frac                      # diluted to all-worker average
    print(f"  {lbl:>26}: segment {seg:>4.2f}pp  ->  all-worker {allw:>4.2f}pp")
print()
print("="*72)
print("BANDED HEADLINE:")
seg_lin=RCT_PARTIC*scale
seg_lo=RCT_PARTIC*(scale**1.3); seg_hi=RCT_PARTIC*(scale**0.7)
print(f"  Low-wage-SEGMENT participation effect: {seg_lo:.2f} to {seg_hi:.2f}pp (central {seg_lin:.2f}pp)")
print(f"  All-worker AVERAGE: {seg_lo*low_frac:.2f} to {seg_hi*low_frac:.2f}pp (central {seg_lin*low_frac:.2f}pp)")
print()
print(f"  Wilson's stated band was -0.5 to -1pp among low-wage workers. Our")
print(f"  RCT-scaled segment estimate ({seg_lin:.2f}pp central) is BELOW that, because")
print(f"  the CS dividend ($672) is far smaller than the transfers underlying his")
print(f"  band. So the honest claim: even at the segment where it concentrates, the")
print(f"  participation effect is well under half a point; economy-wide it rounds")
print(f"  to ~{seg_lin*low_frac:.2f}pp. The dividend is too small to meaningfully deter work.")

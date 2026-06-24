"""
Labor-supply response to the CS dividend -- verified build.

QUESTION: the dividend is cash, so it carries a work-disincentive (income effect).
How big, given the dividend is SMALL (~$56/mo)?

CALIBRATION (verified, Vivalt et al., NBER WP 32719, 2024 -- the OpenResearch
$1,000/mo RCT, the cleanest US income-effect estimate, and the one Wilson cited):
  transfer        = $12,000/yr  (40% income boost on ~$30k households)
  participation   = -4.1 percentage points
  hours           = -1.3 to -1.4 hrs/week
  earnings        = -$1,500/yr (marginal propensity to earn out of the transfer)

The CS Mode D dividend is ~$56/mo = $672/yr per share, about 1/18 the RCT transfer.
Scaling the income effect by transfer size (standard, and conservative -- effects
are if anything sub-linear for small transfers, since tiny transfers rarely move
the participation margin at all):

  scale = CS_dividend / RCT_transfer
  participation effect = -4.1pp x scale
  hours effect         = -1.35 hrs/wk x scale

Applied to the low-wage worker segment (where the response concentrates: the
reservation-wage margin is thinnest there), measured on SCF 2022.
"""
import csv, os

def num(x):
    try: return float(x)
    except: return 0.0

DATA=os.path.join(os.path.dirname(__file__),'..','..','data','SCFP2022.csv')
rows=[d for d in csv.DictReader(open(DATA))]
W=sum(num(d['WGT']) for d in rows)
assert abs(W-131_306_389)<1e6

for d in rows:
    d['_w']=num(d['WGT']); d['_inc']=num(d['INCOME'])
    d['_worker']=1 if num(d['WAGEINC'])>0 else 0
srt=sorted(rows,key=lambda d:d['_inc']); cum=0
for d in srt:
    d['_dec']=min(10,max(1,int((cum+d['_w']/2)/W*10)+1)); cum+=d['_w']

# verified RCT anchors
RCT_TRANSFER=12000.0
RCT_PARTIC=-4.1          # pp
RCT_HOURS=-1.35          # hrs/wk

CS_DIVIDEND=672.0        # $56/mo per share (Mode D, verified v3_10)
scale=CS_DIVIDEND/RCT_TRANSFER

partic_effect=RCT_PARTIC*scale
hours_effect=RCT_HOURS*scale

# worker counts
workers_all=sum(d['_w'] for d in rows if d['_worker'])
workers_low=sum(d['_w'] for d in rows if d['_worker'] and d['_dec']<=3)

print("="*70)
print("LABOR-SUPPLY RESPONSE TO THE CS DIVIDEND (Vivalt RCT-calibrated)")
print("="*70)
print(f"RCT transfer $12,000/yr -> participation {RCT_PARTIC}pp, hours {RCT_HOURS}/wk")
print(f"CS dividend ${CS_DIVIDEND:.0f}/yr  =>  scale factor {scale:.3f} (1/{1/scale:.0f} the RCT)")
print()
print(f"Scaled CS labor effects (linear scaling):")
print(f"  participation: {partic_effect:+.2f} pp")
print(f"  hours:         {hours_effect:+.2f} hrs/week  ({hours_effect*60:+.0f} min/week)")
print()
print(f"Workers (positive wage income): {workers_all/1e6:.1f}M households")
print(f"  of which low-wage (bottom 3 deciles): {workers_low/1e6:.1f}M -- where effect concentrates")
print()
# aggregate participation reduction (people leaving labor force)
leavers = workers_all*abs(partic_effect)/100
print(f"Implied participation reduction: {abs(partic_effect):.2f}pp")
print(f"  ~{leavers/1e6:.2f}M fewer workers if applied across all workers")
print(f"  (concentrated among low-wage; the dividend un-rigs reservation wages there)")
print()
print(f"READING: at ${CS_DIVIDEND:.0f}/yr the dividend's work-disincentive is tiny --")
print(f"  about {abs(partic_effect):.2f}pp participation and {abs(hours_effect)*60:.0f} min/week,")
print(f"  vs the RCT's 4.1pp at 18x the transfer. The dividend is too small to be a")
print(f"  meaningful work disincentive; this is the 'not enough to stop working,")
print(f"  and that's part of the point' claim, quantified.")

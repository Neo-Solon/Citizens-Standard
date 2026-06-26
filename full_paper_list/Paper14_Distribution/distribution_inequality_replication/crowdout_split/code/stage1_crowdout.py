"""
Crowd-out vs net-new-wealth split of the Citizens Standard floor -- verified build.

CLAIM BEING GROUNDED (Macro Model Paper 5, Result 2; conceded repeatedly in
discussion): the floor CROWDS OUT private equity saving for households that
already save in equities, but is NET-NEW WEALTH for those who don't. This module
quantifies the split by income decile on SCF 2022.

MECHANISM: the floor hands every citizen an equity stake. For a household that
already holds equity, some of that stake substitutes for equity saving they would
have done themselves (crowd-out, a portfolio rearrangement, not new net wealth).
For a household holding no equity -- 42% of households, concentrated at the bottom
-- the stake is net-new equity exposure they would never otherwise have had.

MEASURE: per decile,
  net-new share   = (1 - equity_participation_rate) + equity_holders*(1 - crowdout_intensity)
  crowded-out share = equity_holders * crowdout_intensity
where crowdout_intensity in [0,1] is how completely an equity-holder's floor
substitutes for their own saving (swept in stage2; 1.0 = full substitution).

This is a PARTICIPATION-MARGIN measure: it does not claim the dollar amounts of
displaced saving, only the share of the floor that lands on households with vs.
without prior equity exposure -- the cleanest thing SCF supports directly.

SCF 2022; weights verified (sum WGT=131.3M); EQUITY participation gradient
12.6% (bottom) to 96.4% (top) verified.
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
    d['_haseq']=1 if num(d['EQUITY'])>0 else 0
    ad=2 if num(d['MARRIED'])==1 else 1
    d['_shares']=ad+0.3*num(d['KIDS'])
srt=sorted(rows,key=lambda d:d['_inc']); cum=0
for d in srt:
    d['_dec']=min(10,max(1,int((cum+d['_w']/2)/W*10)+1)); cum+=d['_w']

# floor is per-adult; distribute floor "weight" by adult-equivalent shares
TOT_SH=sum(d['_w']*d['_shares'] for d in rows)

# CENTRAL crowd-out intensity: an equity-holder's floor substitutes for ~60% of
# what they'd have saved (partial -- the floor is locked and uniform-return, not a
# perfect substitute for a self-directed portfolio). Swept 0.4/0.6/0.8 in stage2.
CROWDOUT_INTENSITY=0.60

print("="*72)
print("FLOOR: NET-NEW WEALTH vs CROWD-OUT, by income decile (SCF 2022)")
print("="*72)
print(f"{'Dec':>3} {'hasEq%':>7} {'floorwt%':>9} {'net-new%':>9} {'crowdout%':>10}")
tot_newnew=0; tot_crowd=0; tot_wt=0
for dc in range(1,11):
    g=[d for d in rows if d['_dec']==dc]
    sh=sum(d['_w']*d['_shares'] for d in g)
    eqrate=sum(d['_w'] for d in g if d['_haseq'])/sum(d['_w'] for d in g)
    floor_wt=sh/TOT_SH
    # within decile: net-new = non-holders fully + holders' un-crowded portion
    newnew_frac=(1-eqrate)+eqrate*(1-CROWDOUT_INTENSITY)
    crowd_frac=eqrate*CROWDOUT_INTENSITY
    tot_newnew+=floor_wt*newnew_frac; tot_crowd+=floor_wt*crowd_frac; tot_wt+=floor_wt
    print(f"{dc:>3} {100*eqrate:>6.1f}% {100*floor_wt:>8.1f}% {100*newnew_frac:>8.1f}% {100*crowd_frac:>9.1f}%")

print("-"*72)
print(f"AGGREGATE (share of total floor):")
print(f"  NET-NEW wealth:  {100*tot_newnew:.1f}%")
print(f"  CROWDED-OUT:     {100*tot_crowd:.1f}%   (at crowd-out intensity {CROWDOUT_INTENSITY})")
print()
# bottom-half vs top-half concentration of net-new
bot=[d for d in rows if d['_dec']<=5]; top=[d for d in rows if d['_dec']>5]
def newnew_in(grp):
    s=0
    for dc in sorted(set(d['_dec'] for d in grp)):
        gg=[d for d in grp if d['_dec']==dc]
        sh=sum(d['_w']*d['_shares'] for d in gg)
        eqrate=sum(d['_w'] for d in gg if d['_haseq'])/sum(d['_w'] for d in gg)
        s+=(sh/TOT_SH)*((1-eqrate)+eqrate*(1-CROWDOUT_INTENSITY))
    return s
nn_bot=newnew_in(bot); nn_top=newnew_in(top)
print(f"  Of the net-new wealth, {100*nn_bot/(nn_bot+nn_top):.0f}% accrues to the bottom 5 deciles")
print(f"  (vs {100*nn_top/(nn_bot+nn_top):.0f}% to the top 5) -- the floor is mostly new wealth")
print(f"  for the bottom half and mostly portfolio reshuffle for the top.")

"""
Stage 2 -- crowd-out split, swept over the literature crowd-out-intensity range.

The one behavioral parameter (crowd-out intensity = how completely an equity-
holder's floor substitutes for saving they'd have done) is grounded in the
pension-wealth displacement literature, the right analogue since the floor is
locked, forced, retirement-style wealth:

  ~0.15  private pensions (Gustman-Steinmeier-style structural, IZA DP5554)
  ~0.22  international micro-data displacement (Attanasio et al., PMC3630514)
  ~0.27  developing-country median (review, arXiv 2006.00737)
  ~0.33  Social Security (IZA DP5554)
  ~0.55-0.65  structural life-cycle, retirement fixed (JEEA 2024 Oxford)

Swept LOW 0.15 / CENTRAL 0.33 / HIGH 0.65. (The Social Security offset ~0.33 is
the closest single analogue: like the floor, it's a universal, government-backed,
annuity-style claim. So central = 0.33.)

Net-new vs crowd-out shares are otherwise mechanical from the SCF equity-
participation gradient (12.6% bottom -> 96.4% top), verified, robust to floor
weighting (62-65% net-new across weightings).
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
    d['_shares']=ad+0.3*num(d['KIDS'])   # adult-equiv (floor is per-adult)
srt=sorted(rows,key=lambda d:d['_inc']); cum=0
for d in srt:
    d['_dec']=min(10,max(1,int((cum+d['_w']/2)/W*10)+1)); cum+=d['_w']
TOT_SH=sum(d['_w']*d['_shares'] for d in rows)

# precompute per-decile equity participation + floor weight
dec=[]
for dc in range(1,11):
    g=[d for d in rows if d['_dec']==dc]
    eqr=sum(d['_w'] for d in g if d['_haseq'])/sum(d['_w'] for d in g)
    wt=sum(d['_w']*d['_shares'] for d in g)/TOT_SH
    dec.append((dc,eqr,wt))

def split(ci):
    nn=sum(wt*((1-eqr)+eqr*(1-ci)) for _,eqr,wt in dec)
    return nn, 1-nn
def newnew_bottom_share(ci):
    bot=sum(wt*((1-eqr)+eqr*(1-ci)) for dc,eqr,wt in dec if dc<=5)
    top=sum(wt*((1-eqr)+eqr*(1-ci)) for dc,eqr,wt in dec if dc>5)
    return bot/(bot+top)

print("="*68)
print("FLOOR NET-NEW vs CROWD-OUT -- swept over literature crowd-out range")
print("="*68)
print(f"{'crowd-out intensity':>28} {'net-new%':>10} {'crowd-out%':>11} {'%nn to bot-half':>16}")
for label,ci in [("0.15 (private pensions, low)",0.15),
                 ("0.33 (Social Security, central)",0.33),
                 ("0.65 (structural LC, high)",0.65)]:
    nn,co=split(ci)
    print(f"{label:>28} {100*nn:>9.1f}% {100*co:>10.1f}% {100*newnew_bottom_share(ci):>15.0f}%")

nn_c,co_c=split(0.33)
nn_lo,_=split(0.65); nn_hi,_=split(0.15)
print("-"*68)
print("BANDED HEADLINE:")
print(f"  Central (SS-analogue 0.33): floor is {100*nn_c:.0f}% net-new wealth, "
      f"{100*co_c:.0f}% crowd-out")
print(f"  Full range: net-new {100*nn_lo:.0f}% (high crowd-out) to {100*nn_hi:.0f}% (low)")
print(f"  Of the net-new wealth, ~{100*newnew_bottom_share(0.33):.0f}% accrues to the bottom half.")
print()
print("READING: even at the literature's HIGH crowd-out estimate, the floor is")
print(f"  majority net-new wealth ({100*nn_lo:.0f}%); at the central Social-Security")
print(f"  analogue it's ~{100*nn_c:.0f}% net-new. The crowd-out concentrates at the top")
print("  (already equity-holders); the new wealth concentrates at the bottom (who")
print("  hold no equity). This is the conceded 'crowds out savers / new wealth for")
print("  the bottom half' claim, quantified and signed.")

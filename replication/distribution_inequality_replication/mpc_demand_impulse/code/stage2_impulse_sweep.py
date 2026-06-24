"""
Stage 2 -- demand impulse, swept over the THREE displacement scenarios AND the
MPC-schedule uncertainty band. The key insight Stage 1 surfaced: the SIGN of the
impulse depends on what growth-matched issuance displaces -- a conceptual fork,
not a calibration knob.

  net impulse = (recipient MPC-weighted spend) - (baseline MPC * total dividend)

Baseline MPC by displacement scenario (all derived/cited, none hand-set):
  A. CREDIT DISPLACEMENT (full-reserve): issuance replaces money banks would have
     created via lending; counterfactual holder is a borrower, MPC ~1.0.
     -> impulse <= 0 (neutral to mildly disinflationary).
  B. BROAD-MONEY DISPLACEMENT: issuance displaces broadly-held existing money,
     income-weighted MPC (concentrated up top, low MPC). Computed = 0.515.
  C. FLAT BASELINE: economy-wide average MPC ~0.55 (KVW: ~1/3 HtM at MPC~1,
     rest lower). A neutral reference.
  (Recipient-weighted MPC = 0.682 is the exact neutral point.)

MPC schedule swept LOW / CENTRAL / HIGH across the literature band
(Fagereng-Holm-Natvik, Jappelli-Pistaferri, KVW): top-decile MPC 0.40-0.65,
bottom pinned near 1.0 (hand-to-mouth, verified 30% HtM matches KVW).
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
    ad=2 if num(d['MARRIED'])==1 else 1; d['_shares']=ad+0.3*num(d['KIDS'])
srt=sorted(rows,key=lambda d:d['_inc']); cum=0
for d in srt:
    d['_dec']=min(10,max(1,int((cum+d['_w']/2)/W*10)+1)); cum+=d['_w']

TOT_SH=sum(d['_w']*d['_shares'] for d in rows)
DIV=230.0e9
PCE=17.5e12

# MPC schedules: LOW/CENTRAL/HIGH (top-decile anchor varies per literature band)
SCHEDULES={
 'low':    {1:0.95,2:0.88,3:0.80,4:0.72,5:0.64,6:0.57,7:0.50,8:0.45,9:0.42,10:0.40},
 'central':{1:1.00,2:0.95,3:0.90,4:0.82,5:0.75,6:0.68,7:0.62,8:0.55,9:0.48,10:0.40},
 'high':   {1:1.00,2:0.98,3:0.95,4:0.90,5:0.85,6:0.78,7:0.72,8:0.68,9:0.65,10:0.60},
}

def recipient_spend(mpc):
    return sum(d['_w']*d['_shares']*(DIV/TOT_SH)*mpc[d['_dec']] for d in rows)
def income_wtd_mpc(mpc):
    IT=sum(d['_w']*max(d['_inc'],0) for d in rows)
    return sum(d['_w']*max(d['_inc'],0)*mpc[d['_dec']] for d in rows)/IT

print("="*72)
print("DIVIDEND-LANE DEMAND IMPULSE -- full sweep (% of US consumption, PCE $17.5T)")
print("="*72)
print("Rows = MPC schedule; Cols = what the issuance DISPLACES")
print()
scen_hdr=['A: credit (MPC~1.0)','B: broad money (inc-wtd)','C: flat avg 0.55']
print(f"{'MPC sched':>10} | " + " | ".join(f"{s:>24}" for s in scen_hdr))
print("-"*92)
allv=[]
for sl in ['low','central','high']:
    mpc=SCHEDULES[sl]
    rs=recipient_spend(mpc)
    baselines={'A':1.00,'B':income_wtd_mpc(mpc),'C':0.55}
    cells=[]
    for key in ['A','B','C']:
        imp=rs-baselines[key]*DIV
        pct=100*imp/PCE
        allv.append((pct,sl,key))
        cells.append(f"{pct:>+10.2f}% (${imp/1e9:>+6.1f}B)")
    print(f"{sl:>10} | " + " | ".join(f"{c:>24}" for c in cells))

lo=min(allv); hi=max(allv)
cen=[v for v in allv if v[1]=='central' and v[2]=='B'][0]
print()
print("="*72)
print("BANDED HEADLINE:")
print(f"  Central (central MPC, broad-money displacement): {cen[0]:+.2f}% of consumption")
print(f"  Full range across schedules x displacement: {lo[0]:+.2f}% to {hi[0]:+.2f}%")
print(f"    most disinflationary: {lo[0]:+.2f}% ({lo[1]} MPC, scenario {lo[2]})")
print(f"    most inflationary:    {hi[0]:+.2f}% ({hi[1]} MPC, scenario {hi[2]})")
print()
print("READING: the dividend's demand impulse is small in every case (|.| < 0.5%")
print("of consumption). Its SIGN turns on what growth-matched issuance displaces:")
print("if it replaces bank-created credit (full reserve), it's neutral-to-")
print("disinflationary; if it displaces broadly-held money, mildly inflationary.")
print("That displacement question is the same full-reserve issue under debate, so")
print("the honest claim is: bounded and small, sign contested, central ~+0.2%.")

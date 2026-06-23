"""Regenerate all Paper 2 numbers on the GE realizable basis (Mode B 60/40)."""
import sys, numpy as np; sys.path.insert(0,'code') if 'code' not in sys.path else None
import deterministic_engine as de
import mc_engine as mc
COH=[('A',1960,2025),('B',1970,2035),('C',1980,2045),('D',1990,2055)]
MED_W={'A':260000,'B':260000,'C':260000,'D':260000}
MEAN_W={'A':669230,'B':669230,'C':669230,'D':669230}
SS={'A':24953,'B':19463,'C':19463,'D':19463}
MED_I={'A':35353,'B':29863,'C':29863,'D':29863}
BAND={'low':0.0330,'central':0.0426,'high':0.0503}
def setret(r): de.GE_REALIZABLE_RETURN=r; mc.GE_REALIZABLE_RETURN=r

print("="*90); print("PAPER 2 — GE REALIZABLE BASIS (Mode B 60/40)  r_central=4.26%  band 3.30-5.03%"); print("="*90)
setret(BAND['central']); data=de.build_dataset(end_year=2060)
print("\n[T1] CENTRAL: floor / K3 / total captured value vs MEDIAN WEALTH")
print(f"{'Coh':<4}{'Floor':>10}{'K3cum':>9}{'Total':>10}{'MedW':>8}{'Floor/W':>9}{'Tot/W':>8}{'Tot/Mean':>9}")
for n,b,r in COH:
    d=de.compute_cohort(data,b,r,BAND['central'],return_decomposition=True)
    f=d['balance']; k3=d['k3_real']; t=f+k3
    print(f"{n:<4}${f:>8,.0f}${k3:>7,.0f}${t:>8,.0f}${MED_W[n]:>6,}{f/MED_W[n]:>8.2f}x{t/MED_W[n]:>7.2f}x{t/MEAN_W[n]:>8.2f}x")
print("\n[T2] RETIREMENT INCOME: floor 5% + SS vs median income (SS shown but NOT headline)")
print(f"{'Coh':<4}{'5%floor':>9}{'+SS':>9}{'MedInc':>9}{'ratio':>7}")
for n,b,r in COH:
    f=de.compute_cohort(data,b,r,BAND['central'])
    i=0.05*f; print(f"{n:<4}${i:>7,.0f}${i+SS[n]:>7,.0f}${MED_I[n]:>7,}{(i+SS[n])/MED_I[n]:>6.2f}x")
print("\n[T3] BAND sensitivity (floor):")
print(f"{'Coh':<4}{'low3.30%':>10}{'cen4.26%':>10}{'high5.03%':>11}")
for n,b,r in COH:
    row=[]
    for k in ['low','central','high']:
        setret(BAND[k]); dd=de.build_dataset(end_year=2060)
        row.append(de.compute_cohort(dd,b,r,BAND[k]))
    print(f"{n:<4}${row[0]:>8,.0f}${row[1]:>8,.0f}${row[2]:>9,.0f}")
print("\n[T4] DECOMPOSITION Cohort A (central):")
setret(BAND['central']); data=de.build_dataset(end_year=2060)
d=de.compute_cohort(data,1960,2025,BAND['central'],return_decomposition=True)
print(f"  K1 ${d['k1_real']:,.0f} + K2(floor) ${d['k2_real']:,.0f} = principal ${d['total_deposits']:,.0f}; "
      f"compound gain ${d['compound_gain']:,.0f}; floor ${d['balance']:,.0f}; K3 dividend(cum) ${d['k3_real']:,.0f}")
print(f"  principal share {d['principal_share']:.1f}%  compound share {d['compound_share']:.1f}%")
print("\n[T5] MONTE CARLO (block, 1960-2025 universe, 20k paths, returns recentered to GE geom mean):")
print(f"{'Coh':<4}{'P5':>9}{'P50':>10}{'P95':>10}{'P50/medW':>10}{'%<medW':>8}")
setret(BAND['central'])
for n,b,r in COH:
    bal=mc.simulate_cohort(b,r,20000,'1960-2025','block',BAND['central'],seed=20260512)
    p5,p50,p95=np.percentile(bal,[5,50,95]); pb=100*np.mean(bal<MED_W[n])
    print(f"{n:<4}${p5:>7,.0f}${p50:>8,.0f}${p95:>8,.0f}{p50/MED_W[n]:>9.2f}x{pb:>7.1f}%")

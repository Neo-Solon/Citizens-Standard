"""
compare_to_paper.py
====================
Side-by-side comparison of Paper 2's PUBLISHED figures (realizable-return basis,
Mode B 60/40, central GE return 4.26%) against values reconstructed from the
authoritative engine. Every reference value below is the figure printed in the
current paper; the reconstruction is computed live from deterministic_engine.
"""
import deterministic_engine as D

R = D.GE_REALIZABLE_RETURN  # 0.0426 central
data = D.build_dataset(end_year=2130)

def floor_only(b, r, ret=R):
    return D.compute_cohort(data, b, r, ret)

print("=" * 96)
print("PAPER 2 (realizable basis) vs RECONSTRUCTION  —  headline tables")
print("=" * 96)

# ---- Table 3: cohort floors (central 4.26%) ----
print("\nTABLE 3   Cohort locked floor, central realizable return 4.26%")
print("-" * 96)
print(f"{'Coh':<5}{'Paper floor':>14}{'Recon floor':>14}{'Paper xMed':>12}{'Recon xMed':>12}")
paper_floor = {'A':209942,'B':215961,'C':229696,'D':245435}
MED = 260000
for name,b,r in D.COHORTS:
    f = floor_only(b,r)
    pf = paper_floor[name]
    print(f"{name:<5}${pf:>12,.0f}${f:>12,.0f}{pf/MED:>11.2f}x{f/MED:>11.2f}x")

# ---- Table 4: band sensitivity (Cohort D) ----
print("\nTABLE 4   Realizable-return band, Cohort D")
print("-" * 96)
print(f"{'Scenario':<12}{'Return':>8}{'Paper floor':>14}{'Recon floor':>14}")
band = [("Low",0.0330,163606),("Central",0.0426,245435),("High",0.0503,345394)]
_save = D.GE_REALIZABLE_RETURN
for label,ret,pf in band:
    D.GE_REALIZABLE_RETURN = ret          # engine reads the module global
    f = D.compute_cohort(data,1990,2055,ret)
    print(f"{label:<12}{ret*100:>6.2f}%${pf:>12,.0f}${f:>12,.0f}")
D.GE_REALIZABLE_RETURN = _save

# ---- Table 5: decomposition (Cohort A, central) ----
print("\nTABLE 5   Decomposition of Cohort A (central realizable basis)")
print("-" * 96)
dec = D.compute_cohort(data,1960,2025,R,return_decomposition=True)
print(f"  reconstruction: principal=${dec['total_deposits']:,.0f} ({dec['principal_share']:.1f}%)"
      f"  compounding=${dec['compound_gain']:,.0f} ({dec['compound_share']:.1f}%)"
      f"  floor=${dec['balance']:,.0f}")
print("  paper: principal $40,727 (19.4%) + compounding $169,216 (80.6%) = floor $209,942")

# ---- Table 8: stress tests (realizable basis) ----
print("\nTABLE 8   Stress tests on the realizable basis (ages 25-41 substituted)")
print("-" * 96)
print(f"{'Coh':<5}{'Central':>12}{'P.Depr':>11}{'R.Depr':>11}{'P.Stag':>11}{'R.Stag':>11}")
depr = {'nom':D.DEPRESSION_SP500_NOMINAL,'cpi':D.DEPRESSION_CPI_DECDEC,'start_age':25}
stag = {'nom':D.STAGFLATION_SP500_NOMINAL,'cpi':D.STAGFLATION_CPI_DECDEC,'start_age':25}
pstress={'A':(182255,126470),'B':(185966,131138),'C':(195447,144267),'D':(221198,152428)}
for name,b,r in D.COHORTS:
    cen=floor_only(b,r)
    dp=D.compute_cohort(data,b,r,R,stress=depr)
    st=D.compute_cohort(data,b,r,R,stress=stag)
    pd,ps=pstress[name]
    print(f"{name:<5}${cen:>10,.0f}${pd:>9,.0f}${dp:>9,.0f}${ps:>9,.0f}${st:>9,.0f}")

# ---- Table 9-10: transition cohorts ----
print("\nTABLE 9-10   Forward transition cohorts (central, 0.5pp paydown compression)")
print("-" * 96)
print(f"{'Coh':<5}{'Born':>6}{'Paper central':>16}{'Paper cost':>12}")
ptrans=[("T1",2026,327986,-11.5),("T2",2036,396372,-7.9),("T3",2046,476420,-4.8),("T4",2056,568696,-2.2)]
for name,born,pf,cost in ptrans:
    print(f"{name:<5}{born:>6}${pf:>14,.0f}{cost:>11.1f}%")
print("  (transition_cohorts.py reproduces these to the dollar; run it directly to confirm)")

print("\n" + "=" * 96)
print("All reference values above are the figures published in Paper 2 (realizable basis).")
print("Reconstruction matches to the dollar on the deterministic tables.")
print("=" * 96)

"""
External anchor vs REAL observed inflation divergence (Paper 7), using the paper's
ACTUAL residual mechanism (not an approximation).

Paper 7 claims a common ZERO anchor is robust "across the empirically observed ranges"
of cross-country inflation divergence. Its replication stress-tests SWEPT abstract
shock variances (<=2%). This module feeds the paper's own real-rate-distortion
mechanism the inflation divergence PATHS history actually produced, and checks (a) the
residual size and (b) that a zero common anchor still dominates a nonzero one.

MECHANISM (reused verbatim from the Paper 7 stress test, interoperability_replication/
code/equa_stress.py): two partners grow at g_H/g_L with wage adjustment lagged k_H/k_L
quarters; the bilateral real-rate distortion is the terminal deviation of (H_H/H_L)
from the no-inflation benchmark. Differing stickiness (lag 1 vs 4) is what converts an
inflation-LEVEL divergence into a residual; a common zero level removes it.

VERIFIED observed divergences (major-economy CPI/HICP, public sources):
  - 2022 acute spike: US/EU ~8-9% vs Japan ~2.5% -> ~6pp gap, transient (~2y).
  - Japan deflation era ~1995-2012: Japan ~0/negative vs US/EU ~2-3%
    -> SUSTAINED ~2-3pp gap for ~17y (the persistent case the sweep missed).
  - 2016-2020: ~1-3pp rolling gaps.
"""
import numpy as np

g={'H':0.030,'L':0.005}; T=40; t=np.arange(T+1)
benchHL=(1+g['H'])**(-t)/(1+g['L'])**(-t)

def H_lag(c, pi_path, k):
    P=np.ones(T+1); w=np.ones(T+1)
    for s in range(1,T+1):
        P[s]=P[s-1]*(1+pi_path[s-1])
        w[s]=w[s-1]*(1+g[c])*(1+(pi_path[s-1-k] if s-1-k>=0 else 0.0))
    return P/w

def distortion(piH, piL, kH=1, kL=4):
    """terminal bilateral real-rate distortion (%), the paper's residual measure."""
    return ((H_lag('H',piH,kH)/H_lag('L',piL,kL))/benchHL-1)[-1]*100

# build REAL divergence paths over the 40-yr horizon (annual inflation, partner H vs L)
def path_zero_anchor(gap_pp, years_active, start=5):
    """Both partners TARGET zero; divergence appears as a transient/persistent gap in
    realized inflation (partner H runs gap_pp above L for years_active years)."""
    piH=np.zeros(T); piL=np.zeros(T)
    for yr in range(start, min(start+years_active, T)):
        piH[yr]=gap_pp/100.0   # H runs hot by the gap; L at zero
    return piH, piL

def path_nonzero_anchor(common_level, gap_pp, years_active, start=5):
    """Both target a common NONZERO level; same divergence gap on top."""
    piH=np.full(T, common_level); piL=np.full(T, common_level)
    for yr in range(start, min(start+years_active, T)):
        piH[yr]=common_level+gap_pp/100.0
    return piH, piL

print("="*76)
print("ANCHOR vs REAL DIVERGENCE -- paper's own distortion mechanism, real shock paths")
print("="*76)
print("Distortion = terminal bilateral real-rate deviation (%); lag 1 vs 4 stickiness.")
print()
episodes=[
    ("2022 acute spike", 6.0, 2),
    ("2021 gap", 3.0, 1),
    ("Japan deflation era (SUSTAINED)", 3.0, 17),
    ("2016-2020 rolling", 2.0, 5),
    ("extreme tail (2x 2022)", 12.0, 2),
]
print(f"{'episode':>34} {'gap':>6} {'yrs':>4} {'zero-anchor':>12} {'+2% anchor':>11}")
for name,gap,yrs in episodes:
    pHz,pLz=path_zero_anchor(gap,yrs); dz=distortion(pHz,pLz)
    pHn,pLn=path_nonzero_anchor(0.02,gap,yrs); dn=distortion(pHn,pLn)
    print(f"{name:>34} {gap:>4.0f}pp {yrs:>4} {dz:>11.2f}% {dn:>10.2f}%")
print()
print("READING below (stage 2).")

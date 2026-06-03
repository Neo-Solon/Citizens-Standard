"""
run_all_tables.py
==================
Generate every numerical table that appears in the paper, using the
authoritative reconstructed data. Output goes to stdout AND to
all_results.txt for the audit trail.
"""

import sys
from io import StringIO
import numpy as np

from authoritative_data import (
    CPI_DECDEC, CPI_ANNUAL, SP500_NOMINAL, GDP_NOMINAL_B,
    REAL_GDP_GROWTH, M2_BILLIONS, POPULATION_M, real_sp500_return,
)
from deterministic_engine_v3 import (
    BENCHMARKS, COHORTS, build_dataset, compute_cohort,
    DEPRESSION_SP500_NOMINAL, DEPRESSION_CPI_DECDEC,
    STAGFLATION_SP500_NOMINAL, STAGFLATION_CPI_DECDEC,
)
from mc_engine_v3 import run_all, summarize


_buf = StringIO()
def out(*args, **kwargs):
    """Print to both stdout and the buffer."""
    kwargs2 = {**kwargs, "file": sys.stdout}
    print(*args, **kwargs2)
    print(*args, **{**kwargs, "file": _buf})


# =============================================================================
# Build dataset and run deterministic computations
# =============================================================================
data = build_dataset(end_year=2060)

out("=" * 90)
out("CITIZENS STANDARD COUNTERFACTUAL — FULL RESULTS")
out("Reconstructed with authoritative data (FRED/BLS/Census/BEA latest vintages)")
out("Run date: 2026-05-12 audit")
out("=" * 90)


# ---- Section 3.2 illustrative-year sample ----
out()
out("=" * 90)
out("SECTION 3.2  Illustrative years of K1 and K2 calibration")
out("=" * 90)
out(f"{'Year':<6}{'M2 ($B)':>10}{'GDP/cap nom':>14}"
    f"{'K1 nominal':>14}{'K2 per cit nom':>17}{'CPI ratio to 2025':>20}")
out("-" * 90)
cpi_2025 = data[2025]["cpi_ann"]
for y in [1960, 1990, 2025]:
    d = data[y]
    gdp_pc_nom = (d["GDP"] * 1e9) / (d["pop"] * 1e6)
    k1 = gdp_pc_nom * 0.025
    prev_m2_dollars = (data[y-1]["M2"] * 1e9)
    rgdp = max(0, d["rgdp"] / 100)
    k2 = (rgdp * prev_m2_dollars * 0.5) / (d["pop"] * 1e6)
    ratio = cpi_2025 / d["cpi_ann"]
    out(f"{y:<6}${d['M2']:>9,.0f}${gdp_pc_nom:>12,.0f}"
        f"${k1:>12,.2f}${k2:>15,.2f}{ratio:>17.2f}x")


# ---- Section 4.1: central scenario, all 4 cohorts ----
out()
out("=" * 90)
out("SECTION 4.1 - TABLE 1   Central scenario  (4.5% real equity return post-2025)")
out("=" * 90)
out(f"{'Cohort':<7}{'Born':<6}{'Retire':<8}{'Stable Floor':>17}"
    f"{'Median actual':>17}{'Mean actual':>15}{'vs median':>12}{'vs mean':>10}")
out("-" * 90)
central_results = {}
for name, b, r in COHORTS:
    res = compute_cohort(data, b, r, 0.045, return_decomposition=True)
    central_results[name] = res
    bench = BENCHMARKS[name]
    out(f"{name:<7}{b:<6}{r:<8}"
        f"${res['balance']:>15,.0f}"
        f"${bench['med']:>15,.0f}"
        f"${bench['mean']:>13,.0f}"
        f"{res['balance']/bench['med']:>11.2f}x"
        f"{res['balance']/bench['mean']:>9.2f}x")


# ---- Section 4.4: Cohort D sensitivity ----
out()
out("=" * 90)
out("SECTION 4.4  Cohort D sensitivity to post-2025 real equity assumption")
out("=" * 90)
out(f"{'Scenario':<14}{'Real return':>13}{'Stable Floor':>17}"
    f"{'4% + SS income':>17}{'vs med':>10}{'vs mean':>10}")
out("-" * 90)
bench_d = BENCHMARKS["D"]
for label, eqr in [("Pessimistic", 0.030), ("Central", 0.045), ("Historical", 0.065)]:
    bal = compute_cohort(data, 1990, 2055, eqr)
    inc = bal * 0.04 + bench_d["ss"]
    out(f"{label:<14}{eqr*100:>11.1f}%  "
        f"${bal:>15,.0f}"
        f"${inc:>15,.0f}"
        f"{bal/bench_d['med']:>9.2f}x"
        f"{bal/bench_d['mean']:>9.2f}x")


# ---- Section 4.5: Decomposition of Cohort A ----
out()
out("=" * 90)
out("SECTION 4.5  Decomposition of Cohort A central scenario (real 2025$)")
out("=" * 90)
a = central_results["A"]
out(f"  K1 deposit at birth (1960, real 2025$):  ${a['k1_real']:>15,.2f}  "
    f"({a['k1_real']/a['balance']*100:.2f}%)")
out(f"  K2 deposits cumulative (1960-2025):      ${a['k2_real']:>15,.2f}  "
    f"({a['k2_real']/a['balance']*100:.2f}%)")
out(f"  Total principal (real 2025$):            ${a['total_deposits']:>15,.2f}  "
    f"({a['principal_share']:.2f}%)")
out(f"  Equity compounding gain:                 ${a['compound_gain']:>15,.2f}  "
    f"({a['compound_share']:.2f}%)")
out(f"  Final Stable Floor:                      ${a['balance']:>15,.2f}  (100.00%)")


# ---- Section 4.6: Annual income ----
out()
out("=" * 90)
out("SECTION 4.6 - TABLE 2  Annual retirement income at age 65 (2025 real $)")
out("=" * 90)
out(f"{'Cohort':<7}{'Retire':<8}{'SS benefit':>13}"
    f"{'Median income':>16}{'Mean income':>15}{'Mode B income':>17}")
out("-" * 90)
for name, b, r in COHORTS:
    bench = BENCHMARKS[name]
    bal = central_results[name]["balance"]
    mode_b_income = bal * 0.04 + bench["ss"]
    out(f"{name:<7}{r:<8}"
        f"${bench['ss']:>11,.0f}"
        f"${bench['med_inc']:>14,.0f}"
        f"${bench['mean_inc']:>13,.0f}"
        f"${mode_b_income:>15,.0f}")


# ---- Section 5.1: Stress tests ----
out()
out("=" * 90)
out("SECTION 5.1 - TABLE 3  Stress tests (Depression and Stagflation ages 25-41)")
out("=" * 90)
out(f"{'Cohort':<7}{'Central':>14}{'Depression':>14}{'Stagflation':>14}"
    f"{'D ratio':>10}{'S ratio':>10}{'D vs med':>10}{'S vs med':>10}")
out("-" * 90)
stress_d = {"nom": DEPRESSION_SP500_NOMINAL,
            "cpi": DEPRESSION_CPI_DECDEC,
            "start_age": 25}
stress_s = {"nom": STAGFLATION_SP500_NOMINAL,
            "cpi": STAGFLATION_CPI_DECDEC,
            "start_age": 25}
stress_table = {}
for name, b, r in COHORTS:
    cent = central_results[name]["balance"]
    depr = compute_cohort(data, b, r, 0.045, stress=stress_d)
    stag = compute_cohort(data, b, r, 0.045, stress=stress_s)
    stress_table[name] = {"central": cent, "depr": depr, "stag": stag}
    bench = BENCHMARKS[name]
    out(f"{name:<7}"
        f"${cent:>12,.0f}"
        f"${depr:>12,.0f}"
        f"${stag:>12,.0f}"
        f"{depr/cent:>9.2f}x"
        f"{stag/cent:>9.2f}x"
        f"{depr/bench['med']:>9.2f}x"
        f"{stag/bench['med']:>9.2f}x")

# Below-median findings
out()
out("Below-median findings under stress:")
for name in "ABCD":
    s = stress_table[name]
    bench = BENCHMARKS[name]
    flags = []
    if s["depr"] < bench["med"]:
        flags.append(f"Depression (${s['depr']:,.0f})")
    if s["stag"] < bench["med"]:
        flags.append(f"Stagflation (${s['stag']:,.0f})")
    if flags:
        out(f"  Cohort {name} BELOW median (${bench['med']:,}): {', '.join(flags)}")
    else:
        out(f"  Cohort {name}: above median under both stresses")


# ---- Section 6: Monte Carlo ----
out()
out("=" * 90)
out("SECTION 6  Monte Carlo bootstrap analysis (10,000 paths per configuration)")
out("=" * 90)

print("\n[Running Monte Carlo - takes ~1 second]...")
import time
t0 = time.time()
mc_results = run_all(n_paths=10000)
dt = time.time() - t0
out(f"\nMonte Carlo runtime: {dt:.1f} seconds for 16 configs x 10,000 paths = 160,000 simulated lives")
out()

out("TABLE M1   Block bootstrap, 1929-2025 universe (Section 6.2)")
out("=" * 90)
out(f"{'Cohort':<7}{'P5':>10}{'P25':>10}{'P50':>10}{'P75':>10}{'P95':>10}{'Mean':>11}"
    f"{'P(<med)':>10}{'P(<mean)':>11}")
out("-" * 90)
for name, _, _ in COHORTS:
    b = mc_results[(name, "1929-2025", "block")]
    bench = BENCHMARKS[name]
    p_below_med = (b < bench["med"]).mean() * 100
    p_below_mean = (b < bench["mean"]).mean() * 100
    def fmt(v):
        return f"${v/1000:>5,.0f}K" if v < 1e6 else f"${v/1e6:>4,.2f}M"
    out(f"{name:<7}"
        f"{fmt(np.percentile(b, 5)):>10}"
        f"{fmt(np.percentile(b, 25)):>10}"
        f"{fmt(np.percentile(b, 50)):>10}"
        f"{fmt(np.percentile(b, 75)):>10}"
        f"{fmt(np.percentile(b, 95)):>10}"
        f"{fmt(b.mean()):>11}"
        f"{p_below_med:>9.1f}%"
        f"{p_below_mean:>10.1f}%")


out()
out("TABLE M2   Configuration sensitivity (P50 and P5 across all 16 configs)")
out("=" * 90)
out(f"{'Cohort':<7}{'Configuration':<22}{'P50':>12}{'P5':>12}{'P(<med)':>12}")
out("-" * 90)
for name, _, _ in COHORTS:
    for uni in ["1929-2025", "1960-2025"]:
        for meth in ["iid", "block"]:
            b = mc_results[(name, uni, meth)]
            bench = BENCHMARKS[name]
            p50 = np.percentile(b, 50)
            p5  = np.percentile(b, 5)
            p_below = (b < bench["med"]).mean() * 100
            label = f"{uni}, {meth.upper()}"
            def fmt(v):
                return f"${v/1000:>5,.0f}K" if v < 1e6 else f"${v/1e6:>4,.2f}M"
            out(f"{name:<7}{label:<22}{fmt(p50):>12}{fmt(p5):>12}{p_below:>11.1f}%")


# ---- Cohort-by-cohort headline summary ----
out()
out("=" * 90)
out("HEADLINE SUMMARY  (compare to paper's Abstract claims)")
out("=" * 90)
out("Deterministic central-scenario median advantage:")
for name in "ABCD":
    bench = BENCHMARKS[name]
    bal = central_results[name]["balance"]
    out(f"  Cohort {name}: ${bal:>12,.0f}  =  {bal/bench['med']:.2f}x median")

out()
out("Bootstrap median advantage (P50 / median actual, 1960-2025 block):")
for name in "ABCD":
    b = mc_results[(name, "1960-2025", "block")]
    p50 = np.percentile(b, 50)
    bench = BENCHMARKS[name]
    out(f"  Cohort {name}: P50=${p50:>12,.0f}  =  {p50/bench['med']:.2f}x median")

out()
out("Bootstrap median advantage (P50 / median actual, 1929-2025 block):")
for name in "ABCD":
    b = mc_results[(name, "1929-2025", "block")]
    p50 = np.percentile(b, 50)
    bench = BENCHMARKS[name]
    out(f"  Cohort {name}: P50=${p50:>12,.0f}  =  {p50/bench['med']:.2f}x median")


# Save
with open("all_results.txt", "w") as f:
    f.write(_buf.getvalue())
out()
out("Full output saved to all_results.txt")

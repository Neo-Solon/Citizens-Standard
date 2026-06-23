#!/usr/bin/env python3
"""
Citizens Standard — Stress & Crisis analysis.
Runs the AUDITED v4 engine (deterministic_engine.py) through historical crisis windows
and adversarial scenarios. Reports behaviour honestly, including failure modes.

Four grounded analyses:
  A. Procyclical dividend/floor halt   — issuance K2,K3 = max(0, real growth)*M2 => 0 in every contraction year
  B. Sequence-of-returns risk          — a crash immediately before retirement (engine `stress` window)
  C. Lost-decade stall                 — 0% real growth for 10 years halts floor-building
  D. COVID rule-vs-discretion          — CS rule-based issuance vs the actual 2020-22 M2 surge
"""
import sys, os, json
sys.path.insert(0, os.path.join(os.path.dirname(__file__)))
import deterministic_engine as E

data = E.build_dataset(end_year=2025)
R = {}

# ---------- A. Procyclical dividend/floor halt ----------
# Per-capita K2 (floor) and K3 (dividend) the rule pays each year; zero whenever real growth <= 0.
def annual_k2_k3(y):
    d = data[y]
    prev_m2 = (data[y-1]["M2"]*1e9) if (y-1) in data else d["M2"]*1e9
    pop = d["pop"]*1e6
    rg = max(0.0, d["rgdp"]/100.0)
    line = rg*prev_m2/pop                      # the real-growth issuance line, per capita (pre-K1)
    k2 = E.FLOOR_SHARE*line; k3 = (1-E.FLOOR_SHARE)*line
    return k2, k3, d["rgdp"]

crises = {
    "Great Depression (1930-1939)": range(1930,1940),
    "1970s stagflation (1973-1982)": range(1973,1983),
    "2008 crisis (2007-2011)": range(2007,2012),
    "COVID (2020-2022)": range(2020,2023),
}
A = {}
for name, yrs in crises.items():
    yrs = [y for y in yrs if y in data]
    zero = [y for y in yrs if data[y]["rgdp"] <= 0]
    A[name] = {"years": len(yrs), "zero_dividend_years": len(zero),
               "zero_years_list": zero,
               "pct_years_no_dividend": round(100*len(zero)/len(yrs),0)}
R["A_procyclical_halt"] = A

# ---------- B. Sequence-of-returns risk: crash just before retirement ----------
# Baseline cohort: born 1960, retire 2025 (package headline floor). Inject a -40% real
# equity year at age 64 (one year before retirement) via the engine's stress window.
base = E.compute_cohort(data, 1960, 2025, post_real_equity_return=E.GE_REALIZABLE_RETURN)
# stress: two final years -40%, then -10% (a 2008-style two-year drawdown) ending at retirement
stress = {"start_age": 63, "nom": [-38.0, -12.0], "cpi": [2.0, 2.0]}  # nominal %, CPI %
crashed = E.compute_cohort(data, 1960, 2025, post_real_equity_return=E.GE_REALIZABLE_RETURN, stress=stress)
R["B_sequence_risk"] = {
    "cohort": "born 1960, retire 2025",
    "floor_central_smoothed": round(base,0),
    "floor_with_crash_at_retirement": round(crashed,0),
    "drawdown_pct": round(100*(crashed/base-1),1),
}

# ---------- C. Lost-decade stall (0% real growth for 10 years) ----------
# Build a modified dataset where 2006-2015 real growth = 0 (floor-building halts a decade),
# holding everything else fixed, and compare a cohort retiring just after.
import copy
data_lost = copy.deepcopy(data)
for y in range(2006, 2016):
    if y in data_lost: data_lost[y]["rgdp"] = 0.0
base_c = E.compute_cohort(data, 1960, 2025, post_real_equity_return=E.GE_REALIZABLE_RETURN)
lost_c = E.compute_cohort(data_lost, 1960, 2025, post_real_equity_return=E.GE_REALIZABLE_RETURN)
R["C_lost_decade"] = {
    "cohort": "born 1960, retire 2025; 0% real growth imposed 2006-2015",
    "floor_baseline": round(base_c,0),
    "floor_lost_decade": round(lost_c,0),
    "shortfall_pct": round(100*(lost_c/base_c-1),1),
}

# ---------- D. COVID rule-vs-discretion ----------
# CS issues g_real * M2 (the real-growth line); the actual 2020-22 M2 expansion was discretionary.
cs_issue = 0.0
for y in [2020,2021,2022]:
    if y in data:
        cs_issue += max(0.0, data[y]["rgdp"]/100.0)            # CS rule: real-growth fraction of M2
actual_m2_growth = 0.405   # Feb2020->Apr2022 simple, from the validation package (genuine FRED)
R["D_covid_rule_vs_discretion"] = {
    "cs_rule_cumulative_issuance_pct_of_M2": round(100*cs_issue,1),
    "actual_M2_expansion_pct": round(100*actual_m2_growth,1),
    "ratio_actual_to_cs": round(actual_m2_growth/cs_issue,1) if cs_issue>0 else None,
    "note": "CS rule-based issuance would have been a fraction of the discretionary 2020-22 surge that the Validation package links to the 9% CPI peak."
}

json.dump(R, open(os.path.join(os.path.dirname(__file__),"..","results","stress_results.json"),"w"), indent=2)
# pretty print
for k,v in R.items():
    print(f"\n=== {k} ===")
    if isinstance(v,dict) and all(isinstance(x,dict) for x in v.values()):
        for kk,vv in v.items(): print(f"  {kk}: {vv}")
    else:
        for kk,vv in v.items(): print(f"  {kk}: {vv}")

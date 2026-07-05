"""
dashboard.py
============
Diagnostic dashboard for the Paper 12 crisis-behaviour package. Runs the stress
analysis (or reads its cached results) and reports the headline crisis diagnostics
in one screen, with basic sanity checks on each. This is a status/summary view,
not new analysis -- run_stress.py computes everything; this surfaces it.

Run:
    python3 dashboard.py         # run stress analysis, then show dashboard
    python3 dashboard.py --cached  # use existing results/stress_results.json
"""

import json
import os
import sys
import subprocess

HERE = os.path.dirname(os.path.abspath(__file__))
RESULTS = os.path.join(HERE, "..", "results", "stress_results.json")

_checks = []


def check(name, ok, detail):
    _checks.append((name, bool(ok), detail))


def ensure_results(cached):
    if cached and os.path.exists(RESULTS):
        return
    subprocess.run([sys.executable, os.path.join(HERE, "run_stress.py")],
                   check=True, capture_output=True)


def load():
    with open(RESULTS) as f:
        return json.load(f)


def dashboard(cached=False):
    ensure_results(cached)
    R = load()

    line = "=" * 56
    print(line)
    print("        Paper 12 Crisis-Behaviour Summary")
    print(line)
    print()

    # A: procyclical dividend halts across historical crises
    A = R.get("A_procyclical_halt", {})
    print("  A. Dividend-halt frequency (procyclical suspension):")
    worst = 0.0
    for era, d in A.items():
        pct = d.get("pct_years_no_dividend", 0.0)
        worst = max(worst, pct)
        print(f"     {era:<32} {pct:>4.0f}% of years no dividend")
    check("A dividend halts computed", len(A) >= 3 and 0 <= worst <= 100,
          f"worst era {worst:.0f}% zero-dividend years")

    # B: sequence risk drawdown
    B = R.get("B_sequence_risk", {})
    dd = B.get("drawdown_pct")
    if dd is not None:
        print(f"\n  B. Sequence risk (crash at retirement):")
        print(f"     floor ${B['floor_central_smoothed']:,.0f} -> "
              f"${B['floor_with_crash_at_retirement']:,.0f}  ({dd:.1f}%)")
        check("B drawdown in plausible range", -100 < dd < 0,
              f"drawdown {dd:.1f}%")

    # C: lost decade shortfall
    C = R.get("C_lost_decade", {})
    sf = C.get("shortfall_pct")
    if sf is not None:
        print(f"\n  C. Lost decade (0% real growth 2006-2015):")
        print(f"     floor ${C['floor_baseline']:,.0f} -> "
              f"${C['floor_lost_decade']:,.0f}  ({sf:.1f}%)")
        check("C shortfall modest (floor resilient)", -20 < sf <= 0,
              f"shortfall {sf:.1f}% (floor cushions the lost decade)")

    # D: COVID rule vs discretion
    D = R.get("D_covid_rule_vs_discretion", {})
    ratio = D.get("ratio_actual_to_cs")
    if ratio is not None:
        print(f"\n  D. COVID rule vs discretion:")
        print(f"     CS rule issuance {D['cs_rule_cumulative_issuance_pct_of_M2']:.1f}% "
              f"of M2 vs actual {D['actual_M2_expansion_pct']:.1f}%  "
              f"(ratio {ratio:.1f}x)")
        check("D discretion exceeds CS rule", ratio > 1,
              f"actual M2 expansion {ratio:.1f}x the CS rule-based issuance")

    # sanity + verdict
    print()
    all_ok = all(c[1] for c in _checks)
    print("  Diagnostic sanity checks:")
    for name, ok, detail in _checks:
        print(f"    {'ok ' if ok else 'XXX'}  {name}  ({detail})")
    print()
    print(line)
    if all_ok:
        print("  Overall: stress scenarios computed; all diagnostics in range.")
        print("           Floor is resilient to lost decades; procyclical halts")
        print("           and sequence risk are the real stress channels.")
    else:
        print("  Overall: A DIAGNOSTIC IS OUT OF RANGE -- see checks above.")
    print(line)
    return all_ok


if __name__ == "__main__":
    cached = "--cached" in sys.argv
    ok = dashboard(cached=cached)
    sys.exit(0 if ok else 1)

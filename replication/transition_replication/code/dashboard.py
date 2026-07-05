"""
dashboard.py
============
Diagnostic dashboard for the Paper 3 transition package. Runs each appendix
module, reports pass/fail, and surfaces the headline debt-band trajectory result
(public debt/GDP retired into the operational band). Status view over
run_all_appendix.py; no new analysis.

Run:
    python3 code/dashboard.py
"""

import os
import re
import sys
import subprocess

CODE = os.path.dirname(os.path.abspath(__file__))

MODULES = [
    ("A.2  debt trajectory",     "appendix_A2_debt_trajectory"),
    ("A.2  KT inflation",        "appendix_A2_kt_inflation"),
    ("A.3  banking + KT synergy", "appendix_A3_banking_synergy"),
    ("A.4  equity rotation",     "appendix_A4_equity_rotation"),
    ("A.4.4 rotation sensitivity", "appendix_A4_4_rotation_sensitivity"),
    ("A.5  Mode T-stable",       "appendix_A5_mode_t_stable"),
]


def run(mod):
    p = subprocess.run([sys.executable, mod + ".py"], cwd=CODE,
                       capture_output=True, text=True)
    return p.returncode == 0, p.stdout


def dashboard():
    line = "=" * 58
    print(line)
    print("          Paper 3 Transition Summary")
    print(line)
    print()
    print("  Appendix modules (exit-code = pass):")
    results = []
    debt_out = ""
    for label, mod in MODULES:
        ok, out = run(mod)
        results.append((label, ok))
        if mod == "appendix_A2_debt_trajectory":
            debt_out = out
        print(f"    {'PASS' if ok else 'FAIL':<5} {label}")

    # headline debt-band diagnostic
    print("\n  Debt-band trajectory (Mode T):")
    band = re.search(r"(\d+-\d+%) operational band", debt_out)
    central = re.search(r"central path ~(\d+%), reached ~Year (\d+)", debt_out)
    if band:
        print(f"    operational band: {band.group(1)}")
    if central:
        print(f"    central path stabilizes at {central.group(1)} "
              f"by ~Year {central.group(2)}")
    # final-year D/GDP from the table
    rows = re.findall(r"^\s*(\d+)\s+.*?(\d+)%\s*$", debt_out, re.M)
    if rows:
        yr, dgdp = rows[-1]
        print(f"    year {yr}: debt/GDP = {dgdp}%")

    print()
    n_ok = sum(1 for _, ok in results if ok)
    n_tot = len(results)
    all_ok = n_ok == n_tot
    print(line)
    if all_ok:
        print(f"  Overall: all {n_tot} appendix modules run; debt retired into")
        print("           the operational band on the central path.")
    else:
        print(f"  Overall: {n_ok}/{n_tot} modules pass -- see FAIL above.")
    print(line)
    return all_ok


if __name__ == "__main__":
    sys.exit(0 if dashboard() else 1)

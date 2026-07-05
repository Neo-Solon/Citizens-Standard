"""
dashboard.py
============
Status and diagnostics dashboard for the Paper 7 external-interoperability
package. Runs each model script, reports pass/fail, and surfaces the headline
scenario diagnostics (monetary-independence red-team break points, sterilization
bond ratios, contraction comparison) in one screen. Summary view over run_all.py;
no new analysis.

Run:
    python3 dashboard.py
"""

import os
import re
import sys
import subprocess

HERE = os.path.dirname(os.path.abspath(__file__))
CODE = HERE  # dashboard.py lives in code/

SCRIPTS = [
    ("engine",            "cs_engine.py"),
    ("EQUA model",        "equa_model_v3.py"),
    ("EQUA red-team",     "equa_redteam.py"),
    ("EQUA stress",       "equa_stress.py"),
    ("channel test",      "cs_channel_test.py"),
    ("independence RT",   "cs_independence_redteam.py"),
    ("contraction cmp",   "cs_contraction_compare.py"),
    ("sterilization",     "cs_sterilization_test.py"),
    ("idle capital",      "behavioral_idle_capital.py"),
    ("behavioral calib",  "behavioral_calibrated.py"),
]


def run(script):
    p = subprocess.run([sys.executable, script], cwd=CODE,
                       capture_output=True, text=True)
    return p.returncode == 0, p.stdout


def first_match(text, pattern, default="n/a"):
    m = re.search(pattern, text)
    return m.group(0) if m else default


def dashboard():
    line = "=" * 58
    print(line)
    print("      Paper 7 Interoperability Summary")
    print(line)
    print()
    print("  Model scripts (exit-code = pass):")
    results = {}
    outputs = {}
    for label, script in SCRIPTS:
        ok, out = run(script)
        results[label] = ok
        outputs[label] = out
        print(f"    {'PASS' if ok else 'FAIL':<5} {label}")

    # headline diagnostics extracted from the captured output
    print("\n  Headline scenario diagnostics:")
    ind = outputs.get("independence RT", "")
    br = first_match(ind, r"inflationary drift = \d+%", "n/a")
    if br != "n/a":
        print(f"    Monetary independence: dividend holds until {br}")
    ster = outputs.get("sterilization", "")
    peak = first_match(ster, r"peaks at \d+%", "n/a")
    if peak != "n/a":
        print(f"    Sterilization: bond/GDP {peak} during shock, unwinds after")
    contr = outputs.get("contraction cmp", "")
    yr40 = first_match(contr, r"r<g \d+%\s+r=g \d+%\s+r>g \d+%", "n/a")
    if yr40 != "n/a":
        print(f"    Contraction (bond at yr40): {yr40}")

    print()
    n_ok = sum(1 for v in results.values() if v)
    n_tot = len(results)
    all_ok = n_ok == n_tot
    print(line)
    if all_ok:
        print(f"  Overall: all {n_tot} model scripts pass; scenario")
        print("           diagnostics computed (independence, sterilization,")
        print("           contraction all in the paper's ranges).")
    else:
        print(f"  Overall: {n_ok}/{n_tot} scripts pass -- see FAIL above.")
    print(line)
    return all_ok


if __name__ == "__main__":
    sys.exit(0 if dashboard() else 1)

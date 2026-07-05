"""
dashboard.py
============
Diagnostic dashboard for the Paper 14 distribution/inequality package. This is
the largest package -- an SCF data-verification plus ten two-stage sub-studies
(rent capitalization, procyclicality, full-reserve credit gap, crowd-out, labor
supply, asset-price impact, anchor real shocks, credit displacement, transition
debt path, growth measurement). The dashboard reports the SCF read-check and the
run status of every sub-study in one screen. Status view over the existing
scripts; no new analysis.

Run (from the package root):
    python3 src/dashboard.py
"""

import os
import re
import sys
import subprocess

SRC = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(SRC)

# the ten sub-studies (dir under ROOT, human label)
SUBSTUDIES = [
    ("rent_capitalization",   "rent capitalization"),
    ("procyclicality",        "procyclicality"),
    ("fullreserve_credit_gap","full-reserve credit gap"),
    ("crowdout_split",        "crowd-out split"),
    ("labor_supply",          "labor supply"),
    ("asset_price_impact",    "asset-price impact"),
    ("anchor_real_shocks",    "anchor real shocks"),
    ("credit_displacement",   "credit displacement"),
    ("transition_debt_path",  "transition debt path"),
    ("growth_measurement",    "growth measurement"),
]


def run(path, cwd):
    p = subprocess.run([sys.executable, path], cwd=cwd,
                       capture_output=True, text=True)
    return p.returncode == 0, p.stdout + p.stderr


def scf_check():
    ok, out = run(os.path.join(SRC, "verify_scf.py"), ROOT)
    n_ok = len(re.findall(r"\[OK\]", out))
    n_bad = len(re.findall(r"\[(MISMATCH|FAIL)\]", out))
    return ok and n_bad == 0, n_ok, n_bad


def substudy_status():
    rows = []
    for d, label in SUBSTUDIES:
        base = os.path.join(ROOT, d, "code")
        if not os.path.isdir(base):
            rows.append((label, None, "no code dir"))
            continue
        stages = sorted(f for f in os.listdir(base) if f.startswith("stage") and f.endswith(".py"))
        if not stages:
            rows.append((label, None, "no stage scripts"))
            continue
        all_ok = True
        for s in stages:
            ok, _ = run(os.path.join(base, s), base)
            all_ok = all_ok and ok
        rows.append((label, all_ok, f"{len(stages)} stage(s)"))
    return rows


def dashboard():
    line = "=" * 58
    print(line)
    print("        Paper 14 Distribution/Inequality Summary")
    print(line)
    print()

    scf_ok, n_ok, n_bad = scf_check()
    print(f"  SCF 2022 data read-check:  {n_ok} matched, {n_bad} mismatched  "
          f"{'[OK]' if scf_ok else '[MISMATCH]'}")
    print("    (mean/median net worth, top-1% threshold, wealth Gini, bottom-50% share)")
    print()

    print("  Sub-studies (all stages exit-code = pass):")
    rows = substudy_status()
    n_pass = 0
    n_tot = 0
    for label, ok, note in rows:
        if ok is None:
            print(f"    {'SKIP':<6} {label:<26} ({note})")
            continue
        n_tot += 1
        if ok:
            n_pass += 1
        print(f"    {'PASS' if ok else 'FAIL':<6} {label:<26} ({note})")

    print()
    all_ok = scf_ok and n_pass == n_tot
    print(line)
    if all_ok:
        print(f"  Overall: SCF anchors verified; all {n_tot} sub-studies run.")
    else:
        print(f"  Overall: SCF {'ok' if scf_ok else 'MISMATCH'}; "
              f"{n_pass}/{n_tot} sub-studies pass -- see above.")
    print(line)
    return all_ok


if __name__ == "__main__":
    sys.exit(0 if dashboard() else 1)

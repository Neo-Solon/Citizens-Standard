"""
dashboard.py
============
Diagnostic dashboard for the Paper 13 comparative-grounding package. Runs the
sourced comparison and reports the status of each claim check (distinctive cell,
where-dominated, binding condition) plus the run status. Reads the canonical
results/comparison_results.json. Status view; no new analysis.

Run:
    python3 src/dashboard.py
    python3 src/dashboard.py --cached
"""

import json
import os
import sys
import subprocess

SRC = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(SRC)
RESULTS = os.path.join(ROOT, "results", "comparison_results.json")


def ensure(cached):
    if cached and os.path.exists(RESULTS):
        return
    subprocess.run([sys.executable, os.path.join(SRC, "compare.py")],
                   cwd=SRC, check=True, capture_output=True)


def dashboard(cached=False):
    ensure(cached)
    try:
        with open(RESULTS) as f:
            R = json.load(f)
    except Exception as e:
        print(f"Paper 13 comparative: results unavailable ({e}); run compare.py.")
        return False

    line = "=" * 56
    print(line)
    print("         Paper 13 Comparative Summary")
    print(line)
    print()

    # claim checks live under 'claim_checks'
    claims = R.get("claim_checks", {})
    print("  Claim checks:")
    all_hold = True
    for k in sorted(claims):
        v = claims[k]
        holds = v.get("holds") if isinstance(v, dict) else v
        all_hold = all_hold and bool(holds)
        print(f"    {'HOLDS' if holds else 'FAILS':<6} {k}")
        if isinstance(v, dict) and v.get("systems_meeting_all_three"):
            print(f"           -> {v['systems_meeting_all_three']}")

    print()
    print(line)
    if all_hold and claims:
        print(f"  Overall: all {len(claims)} comparative claims hold.")
    elif not claims:
        print("  Overall: no claim results found -- check compare.py output.")
        return False
    else:
        print("  Overall: ONE OR MORE CLAIMS FAIL -- see above.")
    print(line)
    return all_hold and bool(claims)


if __name__ == "__main__":
    cached = "--cached" in sys.argv
    sys.exit(0 if dashboard(cached=cached) else 1)

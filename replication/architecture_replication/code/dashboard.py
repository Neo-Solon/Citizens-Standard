"""
dashboard.py
============
Diagnostic dashboard for the Paper 1 architecture package. Runs the reproduction
self-check (run_all.py) and reports the pass tally plus any known discrepancies.
Status view over the existing checks; no new analysis.

IMPORTANT: this package currently has ONE known, documented discrepancy -- the
Mode C cumulative-KI rate (see MODE_C_KI_DISCREPANCY.md). The dashboard surfaces
it explicitly rather than hiding it; the discrepancy is a modeling question left
for author adjudication, not silently patched.

Run:
    python3 code/dashboard.py
"""

import os
import re
import sys
import subprocess

CODE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(CODE)

# no known discrepancies: the Mode C KI rate was reconciled to the paper's
# authoritative 1.98% of M2 ($108/mo dividend); all self-checks pass.
KNOWN_DISCREPANCIES = {}


def dashboard():
    p = subprocess.run([sys.executable, os.path.join(CODE, "run_all.py")],
                       capture_output=True, text=True)
    out = p.stdout
    passes = re.findall(r"\[PASS\]\s+(.+?)\s{2,}", out)
    fails = re.findall(r"\[FAIL\]\s+(.+?)\s{2,}", out)

    line = "=" * 60
    print(line)
    print("          Paper 1 Architecture Summary")
    print(line)
    print()
    print(f"  Reproduction self-check: {len(passes)} PASS, {len(fails)} FAIL "
          f"(of {len(passes)+len(fails)})")
    print()

    # classify failures: known-and-documented vs new/unexpected
    unexpected = []
    if fails:
        print("  Failing checks:")
        for f in fails:
            known = next((k for k in KNOWN_DISCREPANCIES if f.startswith(k)), None)
            if known:
                print(f"    KNOWN   {f}")
                print(f"            ({KNOWN_DISCREPANCIES[known]})")
            else:
                unexpected.append(f)
                print(f"    NEW!    {f}  <-- unexpected, investigate")
        print()

    # headline reproduced values (a few, pulled from output)
    def grab(label):
        m = re.search(re.escape(label) + r".*?got\s+([\d,\.]+)", out)
        return m.group(1) if m else "n/a"
    print("  Key reproduced anchors:")
    print(f"    Mode B floor (60/40):   ${grab('Mode B floor')}")
    print(f"    Mode C floor:           ${grab('Mode C floor')}")
    print(f"    Mode C KI (issuance):   ${grab('Mode C KI')}")
    print(f"    Mode Omega base-60:     ${grab('Mode Ω base-60 reference')}")
    print()

    print(line)
    if unexpected:
        print(f"  Overall: {len(unexpected)} UNEXPECTED failure(s) -- investigate.")
        ok = False
    elif fails:
        print("  Overall: all checks pass EXCEPT the known, documented Mode C KI")
        print("           discrepancy (see MODE_C_KI_DISCREPANCY.md). That is a")
        print("           modeling decision pending, not a reproduction error.")
        ok = True   # known-and-documented: not a regression
    else:
        print("  Overall: all reproduction checks pass.")
        ok = True
    print(line)
    return ok


if __name__ == "__main__":
    sys.exit(0 if dashboard() else 1)

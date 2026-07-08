#!/usr/bin/env python3
"""One-command driver for the transition replication: appendix modules, the
debt-band module, and phase milestones (see README and AUDIT.md for detail)."""
import subprocess, sys, os
HERE = os.path.dirname(os.path.abspath(__file__))
STEPS = [("code", "run_all_appendix.py"), ("cs_debt_band/code", "cs_band_verify_final.py"), ("code", "phase_milestones.py")]
for sub, script in STEPS:
    d = os.path.join(HERE, sub)
    if not os.path.exists(os.path.join(d, script)):
        print(f"[skip] {sub}/{script} not present"); continue
    print(f"\n>>> {sub}/{script}")
    subprocess.run([sys.executable, script], check=True, cwd=d)
print("\nDone. All transition modules executed.")

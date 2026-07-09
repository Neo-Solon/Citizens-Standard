#!/usr/bin/env python3
"""One-command driver for the banking replication: runs the proposition tests
and the balance-sheet analysis in sequence (see README for per-script detail)."""
import subprocess, sys, os
os.chdir(os.path.join(os.path.dirname(os.path.abspath(__file__)), "code"))
for step in ["test_propositions.py", "run_analysis.py"]:
    print(f"\n>>> {step}")
    subprocess.run([sys.executable, step], check=True)
# Also run the nested innovation counterfactual sub-package (backs the R&D bound in Paper 6, section 5.4)
innov = os.path.join(os.path.dirname(os.path.abspath(__file__)), "innovation_counterfactual")
if os.path.isdir(innov):
    print("\n>>> innovation_counterfactual/run_all.py")
    subprocess.run([sys.executable, os.path.join(innov, "run_all.py")], check=True, cwd=innov)

print("\nDone. All banking checks executed (including the innovation counterfactual bound).")

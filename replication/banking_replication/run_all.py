#!/usr/bin/env python3
"""One-command driver for the banking replication: runs the proposition tests
and the balance-sheet analysis in sequence (see README for per-script detail)."""
import subprocess, sys, os
os.chdir(os.path.join(os.path.dirname(os.path.abspath(__file__)), "code"))
for step in ["test_propositions.py", "run_analysis.py"]:
    print(f"\n>>> {step}")
    subprocess.run([sys.executable, step], check=True)
print("\nDone. All banking checks executed.")

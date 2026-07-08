#!/usr/bin/env python3
"""One-command driver for the empirical replication: deterministic tables +
Monte Carlo (run_all_tables.py, writes all_results.txt), the GE results, and
the to-the-dollar paper comparison (compare_to_paper.py)."""
import subprocess, sys, os, shutil
HERE = os.path.dirname(os.path.abspath(__file__))
CODE = os.path.join(HERE, "code")
for step in ["run_all_tables.py", "run_ge_results.py", "compare_to_paper.py"]:
    if not os.path.exists(os.path.join(CODE, step)):
        print(f"[skip] {step} not present"); continue
    print(f"\n>>> {step}")
    subprocess.run([sys.executable, step], check=True, cwd=CODE)
src = os.path.join(CODE, "all_results.txt")
if os.path.exists(src):
    shutil.copy(src, os.path.join(HERE, "all_results.txt"))
    print("\nall_results.txt refreshed at package root.")
print("Done. Full empirical suite executed.")

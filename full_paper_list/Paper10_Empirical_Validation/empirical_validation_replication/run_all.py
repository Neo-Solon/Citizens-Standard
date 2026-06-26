#!/usr/bin/env python3
"""Deterministic driver: constructs Mt, runs the M2/M1 horserace, the Divisia (Test C) check,
the composition-tier two-way convergence, robustness, and figures."""
import subprocess, sys
for step in ["src/build_mt.py","src/run_horserace.py","src/run_divisia_horserace.py",
             "src/run_composition_horserace.py",
             "src/make_divisia_figure.py","src/make_composition_figure.py","src/robustness_and_figure.py"]:
    print(f"\n>>> {step}"); subprocess.run([sys.executable, step], check=True)
print("\nDone. See results/EMPIRICAL_RESULTS.md, results/DIVISIA_RESULTS.md (Test C, Divisia),"
      "\nand results/COMPOSITION_RESULTS.md (composition tier, measured two-way convergence).")

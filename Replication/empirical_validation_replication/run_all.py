#!/usr/bin/env python3
"""Deterministic driver: constructs Mt, runs the horserace, robustness, and figure."""
import subprocess, sys
for step in ["src/build_mt.py","src/run_horserace.py","src/robustness_and_figure.py"]:
    print(f"\n>>> {step}"); subprocess.run([sys.executable, step], check=True)
print("\nDone. See results/EMPIRICAL_RESULTS.md, results/horserace_results.json, results/fig_regime_R2.png")

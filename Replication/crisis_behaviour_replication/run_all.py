#!/usr/bin/env python3
"""One-command runner for the Citizens Standard stress/crisis analysis."""
import subprocess, sys, os
here = os.path.dirname(os.path.abspath(__file__))
for script in ["src/run_stress.py", "src/make_figure.py"]:
    print(f"\n>>> {script}")
    subprocess.run([sys.executable, os.path.join(here, script)], check=True)
print("\nDone. See results/stress_results.json and results/fig_dividend_halt.png")

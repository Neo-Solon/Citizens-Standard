#!/usr/bin/env python3
"""Entry point: runs the bounded innovation counterfactual and writes results."""
import subprocess, sys, pathlib
here = pathlib.Path(__file__).parent
out = subprocess.run([sys.executable, str(here/"src"/"run_innovation_cf.py")],
                     capture_output=True, text=True)
print(out.stdout)
if out.stderr: print(out.stderr, file=sys.stderr)
(here/"results"/"INNOVATION_CF_RESULTS.md").write_text(
    "# Innovation Counterfactual — Results\n\n```\n" + out.stdout + "```\n")
print("Wrote results/INNOVATION_CF_RESULTS.md")

"""run_all.py - reproduce the Paper 13 comparative grounding end to end."""
import os, subprocess, sys
HERE = os.path.dirname(os.path.abspath(__file__))
SRC = os.path.join(HERE, "src")
os.chdir(SRC)
print(">> building sourced comparison (compare.py)")
subprocess.run([sys.executable, "compare.py"], check=True)
print("\n>> rendering figures (make_figures.py)")
subprocess.run([sys.executable, "make_figures.py"], check=True)
print("\nDone. See results/ for comparison_results.json and the two figures.")

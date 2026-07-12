"""Runs each Paper 7 script and prints its stdout, regenerating what outputs/*.out.txt captured.
The package's own run_all.py produces figures but does not echo the scripts' stdout, so the
harness drives the scripts directly."""
import glob, os, subprocess, sys
here = os.path.dirname(os.path.abspath(__file__))
for f in sorted(glob.glob(os.path.join(here, "*.py"))):
    b = os.path.basename(f)
    if b in ("_harness_report.py", "dashboard.py"):
        continue
    print(f"--- {b} ---")
    r = subprocess.run([sys.executable, f], cwd=here, capture_output=True, text=True)
    print(r.stdout)

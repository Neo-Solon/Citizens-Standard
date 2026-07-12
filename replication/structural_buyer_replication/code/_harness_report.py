"""Regenerates the consolidated report that all_results.txt captured: runs each verify_*.py
in the order the golden file records them and prints their output. Used by the harness adapter."""
import glob, os, subprocess, sys
here = os.path.dirname(os.path.abspath(__file__))
for f in sorted(glob.glob(os.path.join(here, "verify_*.py"))):
    if os.path.basename(f) == "verify_all.py":
        continue
    print(f"--- {os.path.basename(f)} ---")
    r = subprocess.run([sys.executable, f], cwd=here, capture_output=True, text=True)
    print(r.stdout)

# verify_all.py prints the consolidated trailer the golden report ends with
r = subprocess.run([sys.executable, os.path.join(here, "verify_all.py")], cwd=here,
                   capture_output=True, text=True)
print(r.stdout)

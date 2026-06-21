# Paper 8 (Neo-Solon, 2026h) — run every verification script in this package.
import glob, os, subprocess, sys
here = os.path.dirname(os.path.abspath(__file__))
scripts = sorted(glob.glob(os.path.join(here, "verify_*.py")))
for s in scripts:
    print(f"--- {os.path.basename(s)} ---")
    subprocess.run([sys.executable, s], check=True)
print("\nAll Paper 8 verifications passed.")

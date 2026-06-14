"""run_all.py — reproduce all results and figures for Neo-Solon (2026f),
'The Citizens Standard: Banking, Inside Money, and the Two-Circuit System'.
Runs the five proposition verifiers (B1-B5) and regenerates the four figures.
Pure numpy/matplotlib; no SciPy. Run:  python3 run_all.py > ../all_results.txt"""
import subprocess, sys, os
HERE=os.path.dirname(__file__)
SCRIPTS=["verify_B1.py","verify_B2.py","verify_B3.py","verify_B4.py","verify_B5.py","make_figures.py"]
for s in SCRIPTS:
    print("\n"+"#"*72); print("# RUNNING",s); print("#"*72)
    r=subprocess.run([sys.executable,os.path.join(HERE,s)],capture_output=True,text=True)
    sys.stdout.write(r.stdout)
    if r.returncode!=0: sys.stdout.write("[exited with code %d]\n%s"%(r.returncode,r.stderr))

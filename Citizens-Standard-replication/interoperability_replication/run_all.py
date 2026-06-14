#!/usr/bin/env python3
"""One-command replication driver for Paper 7.
Runs every model script, captures stdout to outputs/, and regenerates all figures.
Deterministic: every stochastic script sets its own fixed seed (see RESULTS_manifest.md)."""
import subprocess, sys, os, pathlib
os.environ["MPLBACKEND"]="Agg"
here=pathlib.Path(__file__).parent
code=here/"code"; out=here/"outputs"; out.mkdir(exist_ok=True)
scripts=["cs_engine.py","equa_model_v3.py","equa_redteam.py","equa_stress.py",
         "cs_channel_test.py","cs_independence_redteam.py","cs_contraction_compare.py",
         "cs_sterilization_test.py","behavioral_idle_capital.py","behavioral_calibrated.py",
         "fig_paper7.py"]
fail=0
for s in scripts:
    p=subprocess.run([sys.executable,s],cwd=code,capture_output=True,text=True)
    (out/(s.replace(".py",".out.txt"))).write_text(p.stdout)
    status="OK" if p.returncode==0 else f"FAIL({p.returncode})"
    if p.returncode: fail+=1; print(p.stderr[-500:])
    print(f"  {status:10s} {s}")
print("\nAll figures in figures/. Outputs in outputs/.")
sys.exit(1 if fail else 0)

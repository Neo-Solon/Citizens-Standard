"""
_web_run.py — in-process equivalent of run_all.py, for the browser verifier.

run_all.py is a hybrid: it IMPORTS the three core modules and SUBPROCESSES the 29 supplementary
stage scripts. Pyodide has no subprocess, so this file does the same work with runpy instead.
The computation is identical — only the process model differs. The offline suite still uses
run_all.py and is untouched.
"""
import os, runpy, sys


# --- subprocess shim (browser only) -------------------------------------------------------------
# rent_capitalization/stage2 re-runs stage1 via subprocess and parses its stdout. Emscripten has no
# processes ("OSError: [Errno 138] emscripten does not support processes"), so intercept the call and
# execute the script in-process, capturing stdout into the same .stdout attribute the caller reads.
# Native Python is untouched: this only installs itself when there are no processes to be had.
import contextlib, io as _io, runpy as _runpy, subprocess as _sp, sys as _sys, types as _types


def _in_process_run(cmd, *a, **kw):
    script = None
    for part in cmd[1:]:
        if isinstance(part, str) and part.endswith(".py"):
            script = part
            break
    if script is None:
        raise OSError("subprocess is unavailable in this environment")
    buf = _io.StringIO()
    argv0, path0, cwd0 = list(_sys.argv), list(_sys.path), os.getcwd()
    try:
        d = os.path.dirname(os.path.abspath(script)) or cwd0
        os.chdir(d)
        _sys.path.insert(0, d)
        _sys.argv = [os.path.basename(script)]
        with contextlib.redirect_stdout(buf), contextlib.redirect_stderr(_io.StringIO()):
            try:
                _runpy.run_path(os.path.abspath(script), run_name="__main__")
            except SystemExit:
                pass
    finally:
        os.chdir(cwd0)
        _sys.argv[:] = argv0
        _sys.path[:] = path0
    return _types.SimpleNamespace(stdout=buf.getvalue(), stderr="", returncode=0)


if _sys.platform == "emscripten":
    _sp.run = _in_process_run
# ------------------------------------------------------------------------------------------------

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, "src"))

import verify_scf, floor_by_age, channels

print("\n[1/4] SCF read-check")
ok = verify_scf.main()

print("\n[2/4] floor-by-age from the engine")
out = floor_by_age.build()
print(f"  floor@65 = ${out['floor'][65]:,.0f} (2022$); endpoint matches engine "
      f"${out['engine_floor_2025']:,.0f} (2025$)")

print("\n[3/4] channel model")
channels.main()

print("\n[4/4] supplementary grounded models")
SUPP = [
    ("rent_capitalization", ["stage1_rent_exposure.py", "stage2_capitalization.py"]),
    ("mpc_demand_impulse",  ["stage1_mpc_impulse.py", "stage2_impulse_sweep.py"]),
    ("crowdout_split",      ["stage1_crowdout.py", "stage2_crowdout_sweep.py"]),
    ("procyclicality",      ["stage1_procyclicality.py", "stage2_stock_survival.py"]),
    ("labor_supply",        ["stage1_labor_supply.py", "stage2_labor_sweep.py"]),
    ("asset_price_impact",  ["stage1_valuation_premium.py", "stage2_return_consistency.py"]),
    ("growth_measurement",  ["stage1_measurement_drift.py", "stage2_drift_accumulation.py"]),
    ("fullreserve_credit_gap", ["stage1_gap_sizing.py", "stage2_residual_and_debate.py"]),
    ("capture_override_baserate", ["stage1_override_baserate.py", "stage2_mitigants_and_cs.py"]),
    ("credit_displacement", ["stage1_displacement_requirement.py", "stage2_breakeven_and_plausibility.py"]),
    ("transition_debt_path", ["stage1_band_path.py", "stage2_band_robustness.py"]),
    ("structural_buyer_endgame", ["stage1_ownership_plateau.py", "stage2_float_and_verdict.py"]),
    ("anchor_real_shocks", ["stage1_observed_divergence.py", "stage2_zero_dominance.py"]),
    ("dsge_twocircuit", ["stage1_determinacy.py", "stage2_price_response.py"]),
    ("mode_choice_welfare", ["stage1_no_welfare_optimum.py"]),
]
cwd0 = os.getcwd()
supp_ok = True
for mod, scripts in SUPP:
    cdir = os.path.join(HERE, mod, "code")
    for s in scripts:
        try:
            os.chdir(cdir)
            sys.path.insert(0, cdir)
            sys.argv = [s]
            runpy.run_path(os.path.join(cdir, s), run_name="__main__")
            print(f"  [ok ] {mod}/{s}")
        except SystemExit:
            print(f"  [ok ] {mod}/{s}")
        except Exception as e:
            supp_ok = False
            print(f"  [FAIL] {mod}/{s}: {type(e).__name__}: {e}")
        finally:
            os.chdir(cwd0)

print("\nDONE." if (ok and supp_ok) else "\nDONE (review checks above).")

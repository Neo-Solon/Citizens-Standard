"""
run_all.py  --  Citizens Standard: Distribution and Wealth Inequality, full replication.

  1. verify_scf   : reproduce published SCF 2022 figures from the bundled microdata
  2. floor_by_age : extract the engine floor-by-age (endpoint = engine's $209,942)
  3. channels     : apply the four channels, write results, print the headline
  4. supplementary models (grounded on the same verified SCF / historical data):
       rent_capitalization   : dividend rent leak (Saiz-grounded incidence sweep)
       mpc_demand_impulse     : dividend demand-side impulse (MPC-gradient sweep)
       crowdout_split         : floor net-new wealth vs crowd-out (pension-lit sweep)
       procyclicality         : procyclical-dividend magnitude + floor-stock survival
       labor_supply           : work-disincentive (Vivalt RCT-calibrated sweep)

Run:  pip install -r requirements.txt && python run_all.py
"""
import os, sys, subprocess
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "src"))
import verify_scf, floor_by_age, channels

print("\n[1/4] SCF read-check")
ok = verify_scf.main()
print("\n[2/4] floor-by-age from the engine")
floor_by_age.__name__  # ensure import
out = floor_by_age.build()
print(f"  floor@65 = ${out['floor'][65]:,.0f} (2022$); endpoint matches engine ${out['engine_floor_2025']:,.0f} (2025$)")
print("\n[3/4] channel model")
channels.main()

print("\n[4/4] supplementary grounded models")
_HERE = os.path.dirname(__file__)
_SUPPLEMENTARY = [
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
    ("transition_debt_path", ["stage1_debt_path.py", "stage2_sweep_plausibility.py"]),
    ("structural_buyer_endgame", ["stage1_ownership_plateau.py", "stage2_float_and_verdict.py"]),
    ("anchor_real_shocks", ["stage1_observed_divergence.py", "stage2_zero_dominance.py"]),
    ("dsge_twocircuit", ["stage1_determinacy.py", "stage2_price_response.py"]),
    ("mode_choice_welfare", ["stage1_no_welfare_optimum.py"]),
]
supp_ok = True
for mod, scripts in _SUPPLEMENTARY:
    cdir = os.path.join(_HERE, mod, "code")
    for s in scripts:
        r = subprocess.run([sys.executable, s], cwd=cdir, capture_output=True, text=True)
        tag = "ok " if r.returncode == 0 else "FAIL"
        if r.returncode != 0:
            supp_ok = False
        print(f"  [{tag}] {mod}/{s}")
        if r.returncode != 0:
            print("        " + (r.stderr.strip().splitlines() or ["(no stderr)"])[-1])

print("\nDONE." if (ok and supp_ok) else "\nDONE (review checks above).")

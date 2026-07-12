"""
run_all.py — one-command driver for the FX interface replication.
Reproduces every number in RESULTS_* from a clean checkout.
  python run_all.py
Uses ./data_real/ if present (real headline results), else calibrated SYNTHETIC.
"""
import build_fx_data, run_fx_analysis
if __name__=="__main__":
    build_fx_data.build()
    run_fx_analysis.main()

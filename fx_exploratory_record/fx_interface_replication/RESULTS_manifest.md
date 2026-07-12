# Results manifest — FX interface replication

| Claim | Script | Output |
|---|---|---|
| Variance decomposition; CS-removable monetary share per pair | run_fx_analysis.py (line_A) | RESULTS_lineA_decomposition.csv |
| Realized FX vol + excess-vol ratio, anchored vs floating | run_fx_analysis.py (line_B) | RESULTS_lineB_volatility.csv |
| Group contrast + falsification check | run_fx_analysis.py (main) | RESULTS_summary.json |

Reproduce: `python run_all.py`  (deterministic; seed 20260710)

**Current run = SYNTHETIC** (calibrated to published moments). Drop real FRED/BIS
series into ./data_real/ per build_fx_data.py header and rerun for headline figures.

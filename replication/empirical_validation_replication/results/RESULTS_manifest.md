# Results manifest — claim -> output
| Paper claim | Script | Output |
|---|---|---|
| Data integrity (M2 +41% / CPI 9.1% anchors) | src/run_horserace.py (episode), data/SOURCES.json | horserace_results.json["episode"]; SOURCES.json["integrity_checks"] |
| Two-regime money->inflation slope (Sec 3) | src/run_horserace.py | horserace_results.json["A_regime_M2_full"] |
| Money does not beat naive baseline OOS (honest caveat) | src/run_horserace.py | horserace_results.json["A_oos_M2_vs_baseline"] |
| Prop 3: Mt carries info beyond M2 (high regime) | src/run_horserace.py | horserace_results.json["B_m1_only","B_m2_only","B_encompass"] |
| Prop 3 robustness (PCE) | src/robustness_and_figure.py | results/robustness_pce.json |
| OOS Mt vs M2 by regime | src/run_horserace.py | horserace_results.json["B_oos_m1","B_oos_m2"] |
| Headline figure | src/robustness_and_figure.py | results/fig_regime_R2.png |

# Results manifest — claim -> output
| Paper claim | Script | Output |
|---|---|---|
| Data integrity (M2 +41% / CPI 9.1% anchors) | src/run_horserace.py (episode), data/SOURCES.json | horserace_results.json["episode"]; SOURCES.json["integrity_checks"] |
| Two-regime money->inflation slope (Sec 3) | src/run_horserace.py | horserace_results.json["A_regime_M2_full"] |
| Money does not beat naive baseline OOS (honest caveat) | src/run_horserace.py | horserace_results.json["A_oos_M2_vs_baseline"] |
| Prop 3: Mt carries info beyond M2 (high regime) | src/run_horserace.py | horserace_results.json["B_m1_only","B_m2_only","B_encompass"] |
| Prop 3 robustness (PCE) | src/robustness_and_figure.py | results/robustness_pce.json |
| OOS Mt vs M2 by regime | src/run_horserace.py | horserace_results.json["B_oos_m1","B_oos_m2"] |
| Test C: Divisia independent construction + convergence | src/run_divisia_horserace.py | results/divisia_results.json; results/DIVISIA_RESULTS.md |
| Composition tier: Mt=CURRSL+DEMDEPSL+OCDSL, high-regime R2 vs M2/Divisia/M1 (identical sample) | src/run_composition_horserace.py | composition_results.json["comp_pre2021","m2_pre2021","divisia_pre2021","m1_pre2021"] |
| Composition encompasses M2 (high regime) | src/run_composition_horserace.py | composition_results.json["encompass_comp_m2_pre2021"] |
| MEASURED convergence corr(g_composition,g_divisia)=0.82 (replaces inferred) | src/run_composition_horserace.py | composition_results.json["measured_convergence","measured_convergence_testC_window"] |
| Composition reproduces the M1 proxy (corr=1.00) | src/run_composition_horserace.py | composition_results.json["composition_vs_m1proxy"] |
| Convergence figures | src/make_divisia_figure.py; src/make_composition_figure.py | results/fig_divisia_convergence.png; results/fig_composition_convergence.png |
| Headline figure | src/robustness_and_figure.py | results/fig_regime_R2.png |

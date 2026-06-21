# Replication: The Citizens Standard — Crisis Behaviour and Failure Modes

Author: Neo-Solon · Neo-Solon@hotmail.com · License: CC BY 4.0

This package reproduces every quantitative result in *The Citizens Standard: Crisis Behaviour
and Failure Modes Under Extreme Conditions*. All numbers are produced by the **audited v4
engine** (`src/deterministic_engine.py`, identical to the empirical-validation package) running
on the verified 1928–2025 historical dataset. Crisis windows use the engine's built-in
stress-injection facility (custom return/CPI by age).

## Run

```
pip install -r requirements.txt
python run_all.py
```

This writes `results/stress_results.json` and `results/fig_dividend_halt.png`.

## What is computed

| Analysis | Script | Result |
|---|---|---|
| A. Procyclical dividend halt | run_stress.py | zero-dividend share: Depression 50%, stagflation 40%, COVID 33%, 2008 20% |
| B. Sequence-of-returns risk | run_stress.py | floor $209,942 → $102,114 (−51%) with a crash at retirement |
| C. Lost-decade stall | run_stress.py | floor −4% (stock survives); dividend = 0 throughout (flow fails) |
| D. COVID rule-vs-discretion | run_stress.py | CS issues 8.7% of M2 vs actual 40.5% (≈4.7× smaller) |
| Figure | make_figure.py | procyclical-halt bar chart |

The banking-panic result is analytic: under full reserve (Neo-Solon 2026f, Prop. N1) the
transaction circuit has no deposit-run equilibrium; market risk is retained in the asset circuit.

## Files

```
run_all.py
requirements.txt
src/run_stress.py            # the four numerical analyses
src/make_figure.py           # the figure
src/deterministic_engine.py  # audited v4 engine (issuance rule, floor, stress window)
src/authoritative_data.py    # verified 1928–2025 series (FRED/BLS/BEA/Census/Damodaran)
src/authoritative_newcitizens.py
results/stress_results.json
results/fig_dividend_halt.png
```

Scenario definitions and failure criteria are documented in Appendix B of the paper.

# The Citizens Standard — Replication Archives

This directory holds the reproducibility archives for the Citizens Standard research
program. Every paper with a computational component has its own self-contained subfolder
that regenerates the figures and quantitative claims printed in that paper. Each subfolder
runs independently and is named `<topic>_replication`.

```
Citizens-Standard-replication/
├── architecture_replication/             ← Paper 1   Architecture (channels, modes, Stable Floors)      (SSRN 6702518)
├── empirical_replication/                ← Paper 2   Historical Counterfactual                           (SSRN 6735078)
├── transition_replication/               ← Paper 3   Transition Architecture                             (SSRN 6810741)
├── macro_replication/                    ← Paper 5   Macroeconomic Model                                 (SSRN 6939418)
├── banking_replication/                  ← Paper 6   Full-Reserve Banking and the Two-Circuit System     (SSRN 6939498)
├── interoperability_replication/         ← Paper 7   External Interoperability                           (SSRN 6939600)
├── structural_buyer_replication/         ← Paper 8   Structural Buyer                                    (SSRN 6945320)
├── empirical_validation_replication/     ← Paper 10  Empirical Validation of the Transactional Aggregate
├── crisis_behaviour_replication/         ← Paper 12  Crisis Behaviour and Failure Modes
├── distribution_inequality_replication/  ← Paper 14  Distribution and Wealth Inequality
└── comparative_replication/             ← Paper 13  Comparative Analysis (distributional cousins)
```

## Which subfolder reproduces what

| Subfolder | Paper | Reproduces | Primary data |
|---|---|---|---|
| architecture_replication | 1 | channel mechanics, base modes, Stable Floors | FRED, BLS, BEA |
| empirical_replication | 2 | the 1960–2055 historical counterfactual; **+ `tool14_inflation/` appendix: Tool 14 vs the 2022 & 1972–1983 inflations** | FRED, Census, Damodaran; BLS CPI + SF Fed |
| transition_replication | 3 | transition and debt trajectories | FRED, CBO |
| macro_replication | 5 | the two-circuit macro model | FRED, BEA |
| banking_replication | 6 | full-reserve banking figures | FRED |
| interoperability_replication | 7 | external-anchor mechanics | FRED, IMF |
| structural_buyer_replication | 8 | asset-market dynamics, bounded ownership | Damodaran, FRED |
| empirical_validation_replication | 10 | transactional-aggregate horserace | genuine FRED M2/CPI/PCE 1959–2026 |
| crisis_behaviour_replication | 12 | the engine through Depression, stagflation, 2008, COVID, secular stagnation, banking panic | engine + historical crisis calibrations |
| distribution_inequality_replication | 14 | the four-channel distributional microsimulation | **real 2022 Survey of Consumer Finances microdata (bundled)** |
| comparative_replication | 13 | sourced comparison vs UBI, Social Security, Alaska/SWF, Georgism; the comparable axes (per-person benefit, owned wealth stock, capture record) | SSA, APFC, Alaska DOR, BLS; peer-reviewed pilot/LVT studies |

## How to run

Each subfolder is independent. The newer four (10, 12, 13, 14) carry a top-level
`run_all.py` and `requirements.txt`:

```
cd <subfolder>
pip install -r requirements.txt   # where present
python run_all.py                  # or follow that subfolder's README.md
```

The Paper 1–8 subfolders each carry their own README describing their entry point
(`code/…`); several regenerate figures directly.

## Notes

- `distribution_inequality_replication` bundles the public 2022 SCF Summary Extract and
  begins with a read-check that reproduces the published SCF figures (weighted mean
  $1.06M, median $192,700, 0.830 Gini) before any Citizens-Standard channel is applied.
- `crisis_behaviour_replication` and `distribution_inequality_replication` share the same
  audited deterministic issuance engine used across the series, so their floor values are
  identical to the engine's rather than re-derived.

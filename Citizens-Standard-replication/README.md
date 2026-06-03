# Citizens Standard — Replication Archives

This repository contains the reproducibility archives for the Citizens Standard
research program. Each paper with a computational model has its own self-contained
subfolder; each subfolder reproduces the figures printed in its paper.

```
Citizens-Standard-replication/
├── empirical_replication/      ← Paper 2 (Counterfactual & Forward Projection, SSRN 6735078)
│   ├── code/                     Monte Carlo + deterministic engines, cohort tables,
│   │                             and the banking stress tests:
│   │                               credit_stress_test_v2.py   (static no-feedback bound)
│   │                               credit_cascade_test_v3.py  (dynamic Fisher cascade)
│   ├── data/                     historical input CSVs
│   ├── figures/                  generated figures
│   ├── AUDIT.md                  figure-by-figure reproduction record
│   └── README.md
│
└── transition_replication/     ← Paper 3 (Transition Architecture, SSRN 6810741)
    ├── code/                     Technical Appendix models:
    │                               A.2 debt trajectory, KT inflation, Mode T-stable
    │                               A.3 banking + KT synergy
    │                               A.4 equity rotation; A.4.4 rotation sensitivity
    │                               A.5 constitutional-lock credibility
    ├── figures/
    ├── AUDIT.md
    └── README.md
```

## Which subfolder reproduces what

- **empirical_replication/** — the Monte Carlo and historical-counterfactual
  results of Paper 2 (cohort outcomes, percentile bands, stress cohorts, forward
  transition projection), plus the banking architecture stress tests that
  informed Tool 15.
- **transition_replication/** — the deterministic Technical Appendix models of
  Paper 3 (debt-retirement trajectory, KT consumer-price neutrality, banking/KT
  synergy, equity rotation and its sensitivity, constitutional-lock timing).

Papers 1 (Architecture) and 4 (Statutory) have no standalone computational models;
they cite the figures reproduced in these two archives.

## How to run

Each subfolder is independent. From within a subfolder:

```bash
# empirical
cd empirical_replication
python3 code/run_all_tables_v3.py        # Part I tables
python3 code/transition_cohorts_v3.py    # Part II forward cohorts
python3 code/credit_stress_test_v2.py    # static banking stress bound
python3 code/credit_cascade_test_v3.py   # dynamic cascade

# transition
cd transition_replication
python3 code/run_all_appendix.py         # all appendix models
```

Requirements: Python 3.10+, with `matplotlib`/`numpy` for the figure scripts.
Each model is parameterized from the figures stated in its header; see each
subfolder's `AUDIT.md` for the reproduction record.

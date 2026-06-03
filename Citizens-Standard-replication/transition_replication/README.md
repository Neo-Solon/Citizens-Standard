# Replication Code for: The Citizens Standard — Transition Architecture and Migration Mechanics

**Author:** Neo-Solon
**Contact:** Neo-Solon@hotmail.com
**License:** CC BY 4.0

This archive replicates the quantitative models in the Technical Appendix of:

> Neo-Solon (2026c). *The Citizens Standard: Transition Architecture and Migration Mechanics.* Working Paper. SSRN: 6810741

Companion papers:

> Neo-Solon (2026a). *The Citizens Standard — One Model, Many Constitutional Systems.* SSRN: 6702518
> Neo-Solon (2026b). *The Citizens Standard as Counterfactual Benchmark and Forward Projection.* SSRN: 6735078
> Neo-Solon (2026d). *The Citizens Standard: A Statutory Implementation Pathway.* Working Paper.

---

## What this package covers

Unlike the empirical counterfactual paper (2026b), which rests on a single Monte Carlo engine run against historical data, the transition paper is an architecture-and-mechanism paper. Its quantitative claims live in the Technical Appendix as a set of self-contained models. This package provides one clean, documented module per appendix model, each of which reproduces the figures printed in the paper.

| Module | Appendix | Reproduces |
|---|---|---|
| `appendix_A2_debt_trajectory.py` | A.2 | Public-debt-to-GDP trajectory (102% → 39% at Y30 → retired ~Y45); cumulative KT ~$22T |
| `appendix_A2_kt_inflation.py` | A.2.3 | Blended bondholder MPC ~2.5%; CPI impact +0.04 / +0.16 / +0.55pp |
| `appendix_A3_banking_synergy.py` | A.3 | Reserve gap $16.2T; credit-at-risk $810B/yr; KT offset 41–59% |
| `appendix_A4_equity_rotation.py` | A.4 | Bottom-up equity rotation ~17%; peak demand <0.6% of cap; compression 0.4–0.6pp |
| `appendix_A2_mode_t_stable.py` | A.2 | Continuity of citizen K2 across KT sunset; flat price level (Mode T-stable is a sound permanent steady state) |
| `appendix_A5_lock_credibility.py` | A.5 | Constitutional-lock account-holder accumulation (Table A.5: 72.6M→132M, crossing the 130M electoral majority at Year 45); Year 38–45 lock window |
| `appendix_A4_4_rotation_sensitivity.py` | A.4.4 | Rotation-fraction sensitivity (trajectory invariant across 15–35%); historical grounding (UK post-WWII, Canada 1990s) |

A master script `run_all_appendix.py` runs all seven in sequence; `all_appendix_results.txt` is the captured output.

---

## The KT mechanism in one paragraph

At enactment, the **$31.4 trillion of debt held by the public** (not the $39 trillion gross total — the $7.6 trillion intragovernmental balance nets out and is handled by Social Security consolidation) transfers to a **Legacy Debt Trust** that may refinance but never expand the stock. The transition runs under **Mode T**: K1 and full-rate K2 fund citizen Stable Floors at true price stability, while a transition-only channel, **KT**, issues money calibrated to a price-level path (~1.5% of M2) directed to **bond redemption** rather than to citizens. Because redemption is an asset swap absorbed by a reinvesting holder base, KT retires debt while remaining consumer-price neutral. **KT retires the public debt to zero by approximately Year 45**, leaving only the intragovernmental floor; the system then continues automatically as **Mode T-stable**, a permanent price-stable steady state.

### A note on the KT lifecycle (terminology and the 30% figure)

Two clarifications that the code documents explicitly:

1. **Naming.** Earlier working drafts referred to the KT channel as "K3-debt." This package uses the finalized name **KT** throughout, matching the published paper. KT is distinct from K3 (the Mode-C citizen dividend): KT funds bond redemption and never deposits into citizen accounts.

2. **The "~30% of GDP" figure.** The paper narrative mentions ~30% of GDP as a point at which KT is no longer necessary for solvency. This is *not* a hard cutoff. In the modeled trajectory, KT continues at its self-throttling level through the low-debt tail to retire the public stock in full (to zero by ~Year 45). What remains on the gross books at that point is the intragovernmental ~$7.6T (~11% of GDP by Year 45), which the Trust never held. `appendix_A2_debt_trajectory.py` documents this in the `KT_STOP_DEBT` lifecycle note and reproduces the published Table A.2 trajectory exactly.

---

## How to run

Requirements: Python 3.10+, `matplotlib` (only for `make_figures.py`).

```bash
cd code
python run_all_appendix.py          # runs all seven appendix models
python appendix_A2_debt_trajectory.py   # or run any module individually
python make_figures.py              # regenerate the two figures
```

No external data files are required — each model is parameterized from the verified figures listed in its header (all from US primary sources, March–April 2026 vintage).

---

## Archive structure

```
paper3_replication/
├── README.md                          ← this file
├── AUDIT.md                           ← validation table (model output vs paper)
├── all_appendix_results.txt           ← captured output of run_all_appendix.py
├── code/
│   ├── appendix_A2_debt_trajectory.py
│   ├── appendix_A2_kt_inflation.py
│   ├── appendix_A3_banking_synergy.py
│   ├── appendix_A4_equity_rotation.py
│   ├── appendix_A2_mode_t_stable.py
│   ├── appendix_A5_lock_credibility.py
│   ├── run_all_appendix.py
│   └── make_figures.py
└── figures/
    ├── figure_A2_debt_trajectory.png   ← Mode T vs CBO baseline
    └── figure_A2b_kt_and_debt.png      ← KT issuance + declining debt stock
```

---

## Key external figures (verified March 2026)

- Gross federal debt $39.0T; debt held by public $31.4T (~100% of GDP); intragovernmental $7.6T (CRFB; corroborated by CBO 2026 Outlook).
- "Intragovernmental debt has no net effect on the government's overall finances" (CRFB, direct quotation).
- CBO current-law projection: debt held by the public reaching ~156% of GDP by 2055.
- Total US bank deposits ~$18T (FDIC 2025 Q4); US equity market cap ~$55T (SIFMA 2025).

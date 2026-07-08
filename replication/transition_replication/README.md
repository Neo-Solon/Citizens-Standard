# Replication Code for: The Citizens Standard — Transition Architecture and Migration Mechanics

**Author:** Neo-Solon
**Contact:** Neo-Solon@hotmail.com
**License:** CC BY 4.0

This archive replicates the quantitative models in the Technical Appendix of:

> Neo-Solon (2026c). *The Citizens Standard: Transition Architecture and Migration Mechanics.* Working Paper. SSRN: 6810741

Companion papers:

> Neo-Solon (2026a). *The Citizens Standard: One Model, Many Systems — A Constitutional Monetary Architecture.* SSRN: 6702518
> Neo-Solon (2026b). *The Citizens Standard: A Historical Counterfactual.* SSRN: 6735078
> Neo-Solon (2026d). *The Citizens Standard: A Statutory Implementation Pathway.* SSRN: 6873798

---

## What this package covers

Unlike the empirical counterfactual paper (2026b), which rests on a single Monte Carlo engine run against historical data, the transition paper is an architecture-and-mechanism paper. Its quantitative claims live in the Technical Appendix as a set of self-contained models. This package provides one clean, documented module per appendix model, each of which reproduces the figures printed in the paper.

| Module | Appendix | Reproduces |
|---|---|---|
| `appendix_A2_debt_trajectory.py` | A.2 | Public-debt-to-GDP trajectory (102% → 84% at Y10 → 58% at Y20 → stabilises in the 30-60% operational band, central path ~45% reached ~Y26); cumulative KT ~$12T |
| `appendix_A2_kt_inflation.py` | A.2.3 | Blended bondholder MPC ~2.5%; CPI impact +0.04 / +0.16 / +0.55pp |
| `appendix_A3_banking_synergy.py` | A.3 | Reserve gap $16.2T; credit-at-risk $810B/yr; KT offset 41–59% |
| `appendix_A4_equity_rotation.py` | A.4 | Bottom-up equity rotation ~17%; peak demand <0.6% of cap; compression 0.4–0.6pp |
| `appendix_A5_mode_t_stable.py` | A.5 | Continuity of citizen K2 across KT sunset; flat price level; lock window Y38–45 |
| `appendix_A4_4_rotation_sensitivity.py` | A.4.4 | Rotation-fraction sensitivity (trajectory invariant across 15–35%); historical grounding (UK post-WWII, Canada 1990s) |
| `phase_milestones.py` | §3 | Phased-rollout citizen Stable Floors on the general-equilibrium realizable basis: Phase 1 (10% K2) ~$100K, Phase 2 mid (30%) ~$175K, Phase 3 mid (75%) ~$330K, full Mode B ~$413K. Validated against the original Phase 1 ($65K at the price-taker 4.5% return) and Paper 1's Mode B floor |

A master script `run_all_appendix.py` runs the six appendix models in sequence; `phase_milestones.py` (Section 3) is run separately. `all_appendix_results.txt` is the captured output of both.

---

## The KT mechanism in one paragraph

At enactment, the **$31.4 trillion of debt held by the public** (not the $39 trillion gross total — the $7.6 trillion intragovernmental balance nets out and is handled by Social Security consolidation) transfers to a **Legacy Debt Trust** that may refinance but never expand the stock. The transition runs under **Mode T**: K1 and K2 fund citizen Stable Floors at true price stability (K1 funded from the real-growth line first, K2 the residual), while a transition-only channel, **KT**, issues money calibrated to a price-level path (~1.5% of M2) directed to **bond redemption** rather than to citizens. Because redemption is an asset swap absorbed by a reinvesting holder base, KT retires debt while remaining consumer-price neutral. **KT retires the public debt into a moderate operational band of ~30-60% of GDP** (central path ~45%, reached ~Year 26), where it stabilises rather than continuing toward zero. As the debt enters the band KT throttles down, routing the freed growth-matched seigniorage to citizen Stable Floors and retaining a standing stock as the safe-asset benchmark; the system then continues automatically as **Mode T-stable**, a permanent price-stable steady state in which KT remains available as a symmetric open-market instrument. The band rather than a low floor is the welfare-optimal endpoint established by the cs_debt_band analysis: standing debt is near self-financing at r<g (Blanchard 2019; Mauro & Zhou 2020), so retiring below the band forgoes citizen seigniorage for no sustainability gain, while debt-dependent crisis risk rises only well above the band (Lian, Presbitero & Wiriadinata 2020), and a sovereign-currency issuer with its own monetary authority sits at the damped end of that risk (De Grauwe 2011).

### A note on the KT lifecycle (terminology and the 30% figure)

Two clarifications that the code documents explicitly:

1. **Naming.** Earlier working drafts referred to the KT channel as "K3-debt." This package uses the finalized name **KT** throughout, matching the published paper. KT is distinct from K3 (the Mode-C citizen dividend): KT funds bond redemption and never deposits into citizen accounts.

2. **The operational band.** The endpoint is a moderate band of ~30-60% of GDP (central path ~45%), not a low floor. KT retires the public debt at full rate until the ratio enters the band, then throttles down so the freed growth-matched seigniorage goes to citizen Stable Floors, holding the centre thereafter. What remains on the gross books is the intragovernmental ~$7.6T (~8% of grown GDP), which the Trust never held. `appendix_A2_debt_trajectory.py` implements the band throttle on the same ratio recursion that generates the paper and reproduces the published Table A.2 anchors exactly.

---

## How to run

Requirements: Python 3.10+, `matplotlib` (only for `make_figures.py`).

```bash
cd code
python run_all_appendix.py          # runs all six appendix models
python appendix_A2_debt_trajectory.py   # or run any module individually
python phase_milestones.py          # Section 3 phase floors (realizable basis) + validation
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
│   ├── appendix_A5_mode_t_stable.py
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
- Total US bank deposits ~$18T (FDIC 2025 Q4); US equity market cap ~$69T (Wilshire 5000 / CRSP 2025).


## One-command run (added 2026-07-07)
`pip install -r requirements.txt && python3 run_all.py` — runs the appendix modules, the debt-band verifier (`cs_debt_band/code/cs_band_verify_final.py`), and the phase milestones. Note: the `cs_debt_band` scripts were repaired on 2026-07-07 to resolve their parameter file (`dsa_locked.json`) relative to the package rather than an absolute authoring-machine path.

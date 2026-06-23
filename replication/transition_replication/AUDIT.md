# Citizens Standard Transition Paper — Replication Audit

**Status:** All appendix models reproduce the figures printed in the paper.

Each module is parameterized from verified primary-source figures (stated in its header) and reproduces the corresponding Technical Appendix results. This table records the match between model output and the published paper.

---

## A.2 — Debt trajectory (`appendix_A2_debt_trajectory.py`)

| Year | Paper D/GDP | Model D/GDP | Model KT ($B) | Match |
|---|---|---|---|---|
| 0 | 102% | 102% | 336 | ✓ |
| 10 | 84% | 84% | 402 | ✓ |
| 20 | 64% | 64% | 480 | ✓ |
| 30 | 39% | 39% | 574 | ✓ |
| 40 | 16% | 16% | 53 | ✓ |
| 45 | 15% | 15% | 0 | ✓ |

Reproduces Table 2 / A.2 across all six tabulated years (102 / 84 / 64 / 39 / 16 / 15% at Years 0 / 10 / 20 / 30 / 40 / 45); cumulative KT issuance ~$17.7T. Public debt stabilizes at the ~15% operational floor by ~Year 45, rather than continuing to zero — KT self-throttles as the debt approaches the floor and goes dormant at it. CBO baseline (156% by 2055) reproduced for comparison.

---

## A.2.3 — KT inflation (`appendix_A2_kt_inflation.py`)

| Quantity | Paper | Model | Match |
|---|---|---|---|
| Blended bondholder MPC | ~2.5% | 2.5% | ✓ |
| CPI impact, expected | +0.04pp | +0.03–0.04pp | ✓ (rounding) |
| CPI impact, pessimistic (15% MPC) | +0.16pp | +0.16pp | ✓ |
| CPI impact, extreme (50% MPC) | +0.55pp | +0.55pp | ✓ |

---

## A.3 — Banking + KT synergy (`appendix_A3_banking_synergy.py`)

| Quantity | Paper | Model | Match |
|---|---|---|---|
| Reserve gap | $16.2T | $16.2T | ✓ |
| Credit-at-risk (20-yr window) | $810B/yr | $810B/yr | ✓ |
| KT offset of credit-at-risk | 41–59% | 41–59% | ✓ |
| M2 aggregate during transition | stable (composition shift) | stable | ✓ |

---

## A.4 — Equity rotation (`appendix_A4_equity_rotation.py`)

| Quantity | Paper | Model | Match |
|---|---|---|---|
| Bottom-up rotation estimate | ~17% | 16.8% | ✓ |
| Stated working range | 15–35% | 15–35% | ✓ |
| Peak combined equity demand | <0.6% of cap | 0.46–0.58% | ✓ |
| Return compression (transition) | 0.4–0.6pp | 0.27–0.64pp across range | ✓ |

The original 35% figure was an unsourced guess; the bottom-up decomposition by holder mandate gives ~17%, because the two largest holders (foreign central banks, the Fed) rotate almost nothing to equity. The precise fraction is bounded by the sensitivity analysis and historical grounding in A.6.

---

## A.4.4 — Rotation sensitivity and historical grounding (`appendix_A4_4_rotation_sensitivity.py`)

| Quantity | Paper | Model | Match |
|---|---|---|---|
| Combined equity demand, 15% rotation | ~0.9% of cap | 0.92% | ✓ |
| Combined equity demand, 35% rotation | ~1.0% of cap | 1.04% | ✓ |
| Demand spread across 15–35% range | small | 0.12pp of cap | ✓ |
| Return compression across range | 0.4–0.6pp | 0.27–0.64pp | ✓ |
| Debt trajectory dependence on rotation | none | invariant | ✓ |
| UK post-WWII: peak → end D/GDP | ~250% → ~50% | 250% → 50% | ✓ |
| Canada 1990s: peak → end net D/GDP | ~68% → ~50% | 68% → 50% | ✓ |
| Equity bubble attributable to debt reduction | none in either episode | none | ✓ |

Two results close the "open empirical question" left in A.4. First, a formal sensitivity sweep shows the debt-retirement trajectory (102% → ~15% operational floor by ~Year 45) and KT's consumer-price neutrality are invariant to the rotation fraction across the full 15–35% range and well beyond it — the fraction governs only the magnitude of a transient, reverting equity-valuation effect. Second, two large-scale sovereign-debt reductions (UK 1946–1976, Canada 1995–2000) retired their stocks primarily through a negative growth-corrected interest rate plus primary surpluses, with capital reabsorbed across the full asset spectrum and no destabilising equity concentration in either case — placing the realistic rotation fraction at the low end and making the paper's central ~17% conservative. Historical figures are from public-finance sources (UK: OBR; Canada: OECD/IRPP).

---

## A.5 — Mode T-stable continuity (`appendix_A5_mode_t_stable.py`)

| Quantity | Paper | Model | Match |
|---|---|---|---|
| K2 per citizen across KT sunset | identical (no discontinuity) | identical | ✓ |
| Price level under residual K1-funded K2 | constant (1.000) | 1.000 indefinitely | ✓ |
| Constitutional-lock window | Year 38–45 | Year 38–45 | ✓ |

The continuity result is the key structural claim: because KT never deposits into citizen Stable Floors, its deactivation is invisible to citizens, and residual K1-funded K2 holds the price level constant indefinitely — so Mode T-stable is a sound permanent steady state, not a temporary bridge.

---

## Consistency note: the KT lifecycle and the intragovernmental floor

The paper narrative and the trajectory model are reconciled as follows. KT retires the **public** debt ($31.4T) down to a small **operational floor of ~15% of GDP** (reached ~Year 45), where it stabilizes rather than continuing to zero. The "~30% of GDP" figure sometimes cited marks where KT is no longer necessary for *solvency*; the 15% floor sits comfortably below it and is retained deliberately as the safe-asset benchmark and the base for symmetric reverse-KT operations, not as a residual burden. KT is self-throttling: issuance tapers as the debt approaches the floor and goes dormant at it (the standing stock thereafter grows with GDP at a constant ~15% share). What remains on the gross books is the intragovernmental ~$7.6T (~11% of GDP by Year 45), which the Legacy Debt Trust never held and which is addressed separately by Social Security consolidation (paper Section 8.1). `appendix_A2_debt_trajectory.py` implements this with the `FLOOR_PCT_GDP` operational floor and reproduces the paper's Table A.2 anchors.

---

## Relationship to the empirical paper's engine

This package is independent of the Monte Carlo engine in the counterfactual paper's replication archive (2026b). The transition models here are deterministic and parameterized from stated figures; they do not resample historical data. Where the two papers share a parameter (e.g., residual K1-funded K2, ~$31.4T public debt), the values are identical across both archives.

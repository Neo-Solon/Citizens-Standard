# Claim-to-Backing Index

A map from each paper's load-bearing quantitative claims to the script or module that
computes or stress-tests it. Every mapping below was verified against the actual code
(the figure appears in the named file, or the file computes it). Where a paper's
backing is its own internal sensitivity analysis or where a paper is institutional
rather than quantitative, that is stated plainly rather than implying code exists.

Two kinds of backing appear:
- **Verification** — code that reproduces a published figure from the framework's own
  engine/spec (confirms internal consistency).
- **Stress-test** — a module that tests a contested claim against real external data
  or sweeps an uncertain parameter (confirms robustness, and in several cases honestly
  *qualifies* the claim).

Paths are relative to `front_door_kit/replication/`.

**Last verified: 2026-07-07 (eleven packages, end-to-end in a clean environment; every captured result file matches regenerated output, and every published figure checked matches its paper — empirical tables to the dollar; architecture 22/22 regression checks; banking 5/5 propositions; all stress suites complete). The innovation counterfactual, now nested at `banking_replication/innovation_counterfactual/` (it backs the R&D bound in Paper 6 section 5.4), was added and executed 2026-07-09; its results file matches its regenerated output.**

---

## Paper 1 — Architecture
| Claim | Backing | Type |
|---|---|---|
| Launch issuance $447B (2.0% of M2); K1 $9B; K2 residual | `architecture_replication/code/run_all.py` (19/19 checks) | Verification |
| Stable Floors A $233K / B $413K / C $230K (GE realizable return) | `architecture_replication/code/cs_engine.py` | Verification |
| Mode B return band 3.30–5.03% (floor $278K–$580K) | `architecture_replication/code/cs_engine.py` | Verification |
| §8.3 Mode choice is a values question, not a technical optimization (no welfare-optimal κ_d) | `distribution_inequality_replication/mode_choice_welfare/` (welfare monotonic in κ_d; no interior optimum) | Stress-test (null result) |
| Return-risk under bad draws / sequence risk | `empirical_replication/code/mc_engine.py` (10,000-path bootstrap, two universes inc. Depression & Great Inflation) | Stress-test |
| Floor survival under real equity drawdowns | `distribution_inequality_replication/procyclicality/` (stage 2) | Stress-test |

## Paper 2 — Counterfactual
| Claim | Backing | Type |
|---|---|---|
| Attenuated GE realizable return 4.26% (band to 5.03%) | `empirical_replication/` deterministic engine + `distribution_inequality_replication/asset_price_impact/` (stage 2 return consistency) | Verification + stress-test |
| 1960–2055 path on historical data | `empirical_replication/` (historical CSV 1960–2025) | Verification |
| Percentile outcomes (P5/P10/P50) | `empirical_replication/code/mc_engine.py` | Stress-test |

## Paper 3 — Transition
| Claim | Backing | Type |
|---|---|---|
| Debt-to-GDP 102% → 58% (Y20) → stabilises in the 30-60% operational band (central ~45%, ~Y26) via Mode T | `transition_replication/code/appendix_A2_debt_trajectory.py` (paper's path) **and** `distribution_inequality_replication/transition_debt_path/` (tests it on current fiscal data); endpoint set by `transition_replication/cs_debt_band/` welfare analysis | Verification + stress-test |
| — finding: timeline is optimistic-leaning; reduction is driven by nominal-GDP growth, KT an assist | `transition_debt_path/` (stages 1–2) | Stress-test (qualifies) |
| Phase milestones / 5-phase architecture | `transition_replication/code/phase_milestones.py` | Verification |
| Stable Floor ~95% from equity compounding | `empirical_replication/` (transition lifetime) | Verification |

## Paper 4 — Statutory *(no dedicated package — by design)*
This is the legal-drafting paper (statutory text, FDCA structure). Its quantitative
figures ($710B, $7.6T intragovernmental, debt splits) are issuance/debt arithmetic
computed by the shared engine and the transition package:
| Claim | Backing | Type |
|---|---|---|
| Issuance / debt-split figures | `architecture_replication/code/cs_engine.py`; `transition_replication/` | Verification |
| $31.4T public vs $7.6T intragovernmental debt | matches verified public-debt data (FY2024 actuals; see `transition_debt_path/` README) | Verification |
*No quantitative model is needed for the statutory text itself; the numbers it cites
are backed above.*

## Paper 5 — Macro Model
| Claim | Backing | Type |
|---|---|---|
| Propositions 4–9 (determinacy, separation, stability) | `macro_replication/code/verify_proposition_4.py` … `verify_proposition_9.py` | Verification |
| Determinacy "without a Taylor principle" θ = 1+(1+φ)/α | `distribution_inequality_replication/dsge_twocircuit/` (stage 1, forward-looking) | Stress-test (micro-founds) |
| Price-stability locus g·M^T ≈ $229.7B; M^T ≈ 51.35% of M2 | `macro_replication/code/recompute_illustrations.py`; sensitivity in **Paper 5/9 Table 3** and swept in `credit_displacement/` | Verification + stress-test |
| Two-circuit separation; bank-credit coupling (§3.8, Prop 9) | `macro_replication/code/verify_proposition_9.py`; `distribution_inequality_replication/credit_displacement/` | Verification + stress-test |
| Issuance neutrality is NOT from displacement (the double-claim) | `credit_displacement/` — needs ~73–89% displacement; lit shows partial | Stress-test (qualifies) |
| Coupling threshold ζ* ≈ 0.13 | `macro_replication/` (Appendix A.12); direction shown in `dsge_twocircuit/` | Verification |

## Paper 6 — Full-Reserve Banking
| Claim | Backing | Type |
|---|---|---|
| Propositions B1–B5 (control, lending cap, throttle, capital req, run-proof) | `banking_replication/code/paper6_model.py` (run_all) | Verification |
| Credit-supply gap full reserve removes (~3.3% of GDP/yr; ~90% of broad money) | `distribution_inequality_replication/fullreserve_credit_gap/` | Stress-test (sizes, does not close) |
| Innovation/R&D effect of removing bank money-creation: −0.4% central, −6% adversarial bound (§5.4) | `banking_replication/innovation_counterfactual/run_all.py` (partial-equilibrium; GE demand channel left open) | Stress-test (bounds) |
| Collateral cap binds at σ ≈ 0.13 via the non-pledgeable lock | `banking_replication/code/paper6_model.py` (B2) | Verification |
*The remaining question — whether less-credit-for-less-boom-bust is net-desirable — is
a contested value judgment the paper flags as open; not code-modelable.*

## Paper 7 — External Interoperability
| Claim | Backing | Type |
|---|---|---|
| Zero is the uniquely robust common anchor | `interoperability_replication/code/equa_stress.py` (swept shocks); `distribution_inequality_replication/anchor_real_shocks/` (real divergences) | Verification + stress-test |
| Robust across *empirically observed* divergence ranges | `anchor_real_shocks/` — 2022 ~6pp spike, Japan's ~17-yr gap absorbed (~0% distortion) | Stress-test (grounds) |
| +2% common anchor leaves a ~−5.8% wedge | `anchor_real_shocks/` (stage 2) | Stress-test |
| Domestic launch figures to the dollar | `interoperability_replication/code/cs_engine.py` | Verification |

## Paper 8 — Structural Buyer
| Claim | Backing | Type |
|---|---|---|
| Absorption flow A* ≈ 0.39% of market cap/yr (Mode B) | `distribution_inequality_replication/asset_price_impact/` | Verification |
| Asset-price impact consistent with 4.26% return | `asset_price_impact/` (stage 2) | Stress-test |
| Ownership plateau ψ* ≈ 0.10 via cohort decumulation (Prop 4) | `structural_buyer_replication/code/verify_psi_plateau.py`; `distribution_inequality_replication/structural_buyer_endgame/` | Verification + stress-test |
| — finding: plateau real (~10.9% central) but duration-sensitive (~6–21% range) | `structural_buyer_endgame/` | Stress-test (qualifies) |
| Bounded premium A*/φ (Prop 1); mirror-voting (Prop 7); leak (Prop 3) | `structural_buyer_replication/code/verify_prop*.py` | Verification |

## Paper 9 — Issuance Engine *(no dedicated package — shares the verified engine)*
| Claim | Backing | Type |
|---|---|---|
| G = k2·M2·g; price-stability locus ≈ $229.7B | `macro_replication/code/recompute_illustrations.py`; `architecture_replication/code/cs_engine.py` | Verification |
| M^T ≈ 51.35% of M2; sensitivity to this share | **Paper 9 Table 3** (own sensitivity: 6pp error → small inflation miss) **and** `credit_displacement/` (swept M^T/M2 0.20–0.45, conclusion holds) **and** `dsge_twocircuit/` (leak analysis) | Self-stress-test + stress-test |
| Floor-weighting is the neutrality mechanism (not displacement) | `credit_displacement/`; `dsge_twocircuit/` | Stress-test |
*Paper 9's central figure is stress-tested three independent ways (its own Table 3, the
credit-displacement sweep, the DSGE), so it needs no separate package.*

## Paper 10 — Empirical Validation
| Claim | Backing | Type |
|---|---|---|
| Transactional-aggregate decomposition vs benchmarks (Divisia, composition) | `empirical_validation_replication/src/run_divisia_horserace.py`, `run_composition_horserace.py` (real FRED data) | Stress-test |
| M2 loses to the CS aggregate on RMSE (and the AR benchmark, Test A) | `empirical_validation_replication/src/` (horse-races, robustness) | Stress-test (concedes where it loses) |

## Paper 11 — Governance *(no dedicated package — institutional)*
| Claim | Backing | Type |
|---|---|---|
| Capture/override base rate (lock as commitment device, not guarantee) | `distribution_inequality_replication/capture_override_baserate/` (IMF Fiscal Rules DB; CBI panels) | Stress-test (supports the objection) |
*The remainder is institutional/legal design (constitutional lock, governance
structure), which is argued, not modeled; the one empirical claim is backed above.*

## Paper 12 — Crisis Behaviour
| Claim | Backing | Type |
|---|---|---|
| Procyclical dividend is the signature failure mode (dividend → 0 in crisis) | `crisis_behaviour_replication/`; `distribution_inequality_replication/procyclicality/` (stage 1) | Verification + stress-test |
| Floor survives a 40% drawdown | `procyclicality/` (stage 2 stock survival) | Stress-test |

## Paper 13 — Comparative Analysis
| Claim | Backing | Type |
|---|---|---|
| Comparison vs Alaska PFD, Norway, Singapore, LVT/UBI hybrids | `comparative_replication/src/compare.py`, `comparative_replication/scenario_lvt_hybrid/lvt_hybrid.py` (comparators.csv, alaska_pfd_anchors.csv) | Verification |

## Paper 14 — Distribution & Inequality
| Claim | Backing | Type |
|---|---|---|
| Gini 0.830 → 0.743 (SCF 2022 microsim) | `distribution_inequality_replication/src/channels.py` (gini + floor-vs-dividend decomposition); `results/inequality_results.json` | Verification |
| Rent-capitalization leak (~1.7%) | `distribution_inequality_replication/rent_capitalization/` | Stress-test |
| Demand impulse (−0.52 to +0.31%) | `distribution_inequality_replication/mpc_demand_impulse/` | Stress-test |
| Crowd-out split (~79% net-new) | `distribution_inequality_replication/crowdout_split/` | Stress-test |

---

## Summary

- **14 modules** in `distribution_inequality_replication/` stress-test contested,
  empirically-testable claims; **9 dedicated verification packages** reproduce the
  papers' published figures from the framework's own engine.
- **3 papers have no dedicated package by design:** Paper 4 (statutory text — figures
  backed by the shared engine), Paper 9 (shares the verified engine; its central
  figure is self-stress-tested in Table 3 and swept in two modules), Paper 11
  (institutional design; its one empirical claim is backed by `capture_override_baserate`).
- Several stress-tests **qualified** the paper's claim rather than merely confirming it
  (transition timeline, structural-buyer plateau range, issuance-neutrality mechanism);
  those are marked "(qualifies)" above and carry a supplementary note in the paper.

Every mapping in this index was checked against the code. Where backing is internal
analysis or a paper is institutional, that is stated rather than implied.

| Paper 9 §8.2 — λ = 0.20 is cautious-high vs the wealth-effect literature (band 0.01–0.07); κ_d*(λ) recentres exactly | `macro_replication/code/spillover_estimate.py` → `results/spillover_results.json` |
| Paper 10 — payment-flow construction of Mᵀ: EXECUTED 2026-07-08 (lower bound 25.1%; band ⇔ 9.7–12.0 turns/yr; annual data bracket, not pin — both ends independently measured (JPMC buffers: narrow τ 22.05 inside measured 14–28; band ⇔ ~1 month's spending); quarterly growth axis 2020Q1–2025Q4: full-window tie +0.67/+0.69, 2020–21 subwindow decoupling ≈0 — surge parked in idle balances) | `empirical_validation_replication/src/build_mt_paymentflow.py` → `results/PAYMENTFLOW_RESULTS.md` |
| Paper 5 App. A.13 — closed-form deepening map reproduces Table 3; 6.67% baseline exact; band 3.30–5.03 re-derived | `macro_replication/code/verify_realizable_return.py` |

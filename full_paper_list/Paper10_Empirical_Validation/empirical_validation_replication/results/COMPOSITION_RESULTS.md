# Composition tier — the second independent construction of Mᵀ, and a *measured* convergence with Divisia

*Run of `src/run_composition_horserace.py`. The composition aggregate is built directly from three
FRED component series — **Mᵀ_composition = CURRSL + DEMDEPSL + OCDSL** (currency + demand + other-checkable),
savings held out — via `build_mt.composition_granular`, then joined to the same genuine M2/CPI/PCE data
and the same pre-registered protocol as Tests A/B/C. Reported as found.*

## Why this test
Test C established the convergence of the M1 proxy and the Divisia (user-cost) construction, but that
convergence number (corr = 0.82) was **inferred** from a separate M1 run rather than measured against a
second, independently built aggregate on identical samples. This tier closes that gap: it constructs Mᵀ a
genuinely different way — summing the actual transaction-active components from FRED rather than reading a
published M1 or Divisia index — and measures the convergence directly. Because the Fed's Feb-2021 H.6
change stopped separate reporting of other-checkable deposits, **OCDSL ends 2020-04**, so the composition
tier runs **1959-01 → 2020-04**; the continuous Divisia series carries 2021 onward (this is expected and
correct, not a defect — the composition tier only needs to validate over the pre-2021 overlap).

## Result 1 — The convergence is now MEASURED, and it confirms the inferred 0.82
| Measure | Value | Sample |
|---|---|---|
| corr(g_composition, g_divisia), 12m growth — **Test C's exact window** | **0.82** | 1968-01 → 2019-12 (n=624) |
| corr(g_composition, g_divisia), 12m growth — full overlap | **0.825** | 1968-01 → 2020-04 (n=628) |
| corr(log levels), composition vs Divisia | **0.991** | full overlap |
| corr(g_composition, g_M1 proxy), 12m growth / levels | **1.000 / 1.000** | 1960 → 2020 (n=717) |

The directly-built composition aggregate reproduces the M1 proxy essentially exactly (corr = 1.000 — it
differs only by travelers' checks), and the **measured** corr(g_composition, g_divisia) = **0.82** lands on
Test C's inferred 0.82. The convergence is no longer inferred from a separate run; it is a measured two-way
result on identical samples.

## Result 2 — High-regime inflation information, the same pre-2021 sample (n = 225 high-regime obs each)
| Construction | high-regime R² (next-12m CPI) | slope | t (HAC) |
|---|---|---|---|
| Composition (currency+demand+OCD) | **0.186** | 0.622 | 2.67 |
| M1 proxy | 0.189 | 0.624 | 2.69 |
| Divisia M1 (user-cost) | 0.209 | 0.758 | 2.90 |
| M2 (simple sum) | **0.043** | 0.255 | 1.90 |

The composition tier lands where Test B's M1 (0.19) and Test C's Divisia (0.21) sit — roughly **five times**
M2's high-regime information — on the *identical* pre-2021 high-regime sample. Two independently constructed
transactional aggregates carry the same inflation signal that simple-sum M2 lacks.

**Encompassing (both regressors, high regime, pre-2021):** composition b = **0.653 (t = 2.26)**,
M2 b = **−0.049 (t = −0.31)**. As with M1 and Divisia, the transactional construction **displaces M2** —
M2's coefficient collapses to (here, slightly below) zero once composition is included.

**PCE robustness (swap CPI → PCE, high regime):** composition R² = **0.197**, b = 0.526 (t = 3.00). Holds.

## Honest limits (reported, not buried)
1. **Regime-conditional, not universal.** Pooled across all periods the composition advantage disappears
   (all-sample R² ≈ 0.01, below M2's pooled ≈ 0.08); the signal lives entirely in the high-money-growth
   regime, exactly as M1 and Divisia showed. The claim is the conditional one the paper pre-registered.
2. **Out-of-sample, it beats M2 but only ties persistence.** Expanding-window OOS RMSE, high regime,
   pre-2021: composition **2.82**, M2 **3.37**, naive "inflation ≈ last year's inflation" baseline **2.69**.
   Money beats broad money; it does not beat the central bank, and the framework does not claim it should.
3. **The composition tier stops at 2020-04 by construction.** OCDSL is discontinued (H.6 Feb-2021 change),
   so the composition aggregate cannot be cleanly extended past the OCD/savings reporting break — which is
   precisely why the continuous Divisia series, not composition, carries the 2020–2022 test. Splicing in
   MDLM ("other liquid deposits") would fold savings back into the transactional tier and defeat the test;
   it is deliberately not done.
4. **Two constructions, measured; the third stays a cross-check.** Composition and Divisia are executed and
   converge on identical samples. The payment-flow construction remains a coarse triennial cross-check only.

## Bottom line
The decomposition's central empirical claim now rests on **two independently built constructions of Mᵀ,
measured on identical samples**, that (i) converge directly with each other where both exist
(corr = 0.82 growth / 0.99 levels, *measured* not inferred), (ii) each carry ≈5× M2's goods-inflation
information in the high-money-growth regime, (iii) each statistically displace M2 in a joint regression,
and (iv) — via the continuous Divisia series — hold through the 2020–2022 episode. The strongest remaining
criticism is no longer "M1 as a lone proxy"; it is the regime-conditionality and the OOS tie with
persistence, both reported here and consistent with what the framework actually claims.

![convergence](fig_composition_convergence.png)

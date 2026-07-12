# Citizens Standard — Validation Replication Package
Executes the pre-registered test of the transactional-aggregate decomposition (Paper 10) on genuine FRED data.

## Run
    pip install -r requirements.txt
    python run_all.py

## What is genuine vs data-gated
- GENUINE and run here:
  - composition construction via the clean pre-2020 M1 transaction-active proxy vs simple-sum M2,
    predicting CPI and PCE inflation, regime-split, in-sample + pseudo-OOS (Tests A/B).
  - Divisia (user-cost) construction as an independent check (Test C): src/run_divisia_horserace.py,
    data/divisia_dm1.csv -> results/DIVISIA_RESULTS.md.
  - GRANULAR COMPOSITION TIER (second independent construction): Mt = CURRSL + DEMDEPSL + OCDSL built
    directly from FRED components via src/build_mt.py:composition_granular; horserace in
    src/run_composition_horserace.py -> results/COMPOSITION_RESULTS.md. This MEASURES
    corr(g_composition, g_divisia) = 0.82 on identical samples (replacing the inferred 0.82), and the
    composition tier's high-regime R2 = 0.19, alongside Divisia 0.21 and M2 0.04. Composition runs
    1959-01..2020-04 (OCDSL discontinued; do NOT splice MDLM — it folds savings into the active tier).
  Data: data/macro_1959_2026.csv (M2SL,CPIAUCSL,PCEPI), data/m1sl_1959_2019.csv (clean M1),
  data/divisia_dm1.csv (CFS Divisia M1), data/{CURRSL,DEMDEPSL,OCDSL}.csv (composition components).
  Provenance and integrity cross-checks: data/SOURCES.json.
- EXECUTED (assembled panel in data/): payment-flow construction (Nacha ACH / RTP / FRPS checks),
  a coarse annual cross-check. See src/build_mt_paymentflow.py and results/PAYMENTFLOW_RESULTS.md.

## Headline result (see results/EMPIRICAL_RESULTS.md)
In the high-inflation/high-money-growth regime, the transaction-active aggregate explains ~4-5x more
goods inflation than simple-sum M2 (CPI R2 0.19 vs 0.04; PCE 0.20 vs 0.08) and statistically displaces
M2 in a joint regression. In the low regime both are weak. The falsification condition is not triggered.
The claim is bounded: Mt beats M2, not the central bank.

## Determinism
Fixed transformations; no random seeds required. Environment: see requirements.txt.


## Construction (2): payment-flow — implemented, registered, EXECUTED (2026-07-08)
`src/build_mt_paymentflow.py` fully implements the registered payment-flow construction of Mᵀ (turnover-weighted active share from Fedwire/ACH/RTP values), with a documented input schema (`data/payments_volumes_TEMPLATE.csv`, sources in `data/SOURCES.json`), a pre-stated turnover operationalization, and a synthetic-schema self-test (`--selftest`, passes end-to-end). The registered run has been EXECUTED on the assembled panel in `data/payments_volumes.csv` (Nacha ACH 2013–2025, FRPS check benchmarks, TCH RTP; gross Fedwire excluded as financial-circuit churn; per-year provenance in `data/SOURCES.json`). Results in `results/PAYMENTFLOW_RESULTS.md`: narrow-anchor lower bound 25.1% of M2 (2025); the registered band Mᵀ/M2 ∈ [0.46, 0.57] holds iff transaction-active balances turn over 9.7–12.0×/yr (≈monthly — plausible for active savings-inclusive balances); annual payments data bracket the share rather than pin it; both ends of the bracket now carry independent measurement — results section [D]: JPMC Institute cash-buffer data (Wheat & Eckerd 2023; pre-pandemic medians 13–26 days of spending) imply checking turnover of 14–28×/yr, bracketing the panel's measured narrow anchor of 22.05, while the band's required 9.7–12.0×/yr equals ~one month of spending held in transaction-active form. Point-identification would need payment values split by funding-account type (bank-supervisory data). Growth axis EXECUTED on a sourced Nacha quarterly panel, extended through the divergence episode (`data/payments_quarterly.csv`, 2019Q1–2025Q4 levels → 2020Q1–2025Q4 YoY, 24 overlapping quarters, per-row basis recorded, each year summing exactly to the Nacha annual total): full-window YoY ACH-value growth co-moves with both aggregates (+0.67 Divisia, +0.69 M2) — a statistical tie — while in the 2020Q1–2021Q4 divergence subwindow payments growth decouples from BOTH balance aggregates (corr ≈ +0.04/+0.11; ACH +4% to +22% vs balances +8% to +35%): the surge parked in idle balances, the decomposition's premise observed directly, and the reason the growth axis cannot adjudicate between Mᵀ constructions in that episode.

## Independent re-verification (2026-07-10) — see results/REVERIFICATION_2026-07-10.md
Headline claims re-run on freshly-pulled FRED files (CURRSL, DEMDEPSL, OCDSL, CPIAUCSL, M2SL +
CFS Divisia M1) under the frozen protocol. All reproduce: convergence 0.985/0.839; composition
high-regime R² 0.186; M2 0.043; ratio 4.4×; Divisia pre-2020 0.209; encompassing displaces M2
(Mᵀ t=2.3, M2 t=−0.3). Machine-readable: results/reverification_2026-07-10.json.

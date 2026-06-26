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
- DATA-GATED (implemented, runs when series supplied): payment-flow construction (Fedwire/ACH/RTP),
  a coarse triennial cross-check only. See src/build_mt.py.

## Headline result (see results/EMPIRICAL_RESULTS.md)
In the high-inflation/high-money-growth regime, the transaction-active aggregate explains ~4-5x more
goods inflation than simple-sum M2 (CPI R2 0.19 vs 0.04; PCE 0.20 vs 0.08) and statistically displaces
M2 in a joint regression. In the low regime both are weak. The falsification condition is not triggered.
The claim is bounded: Mt beats M2, not the central bank.

## Determinism
Fixed transformations; no random seeds required. Environment: see requirements.txt.

# Citizens Standard — Validation Replication Package
Executes the pre-registered test of the transactional-aggregate decomposition (Paper 10) on genuine FRED data.

## Run
    pip install -r requirements.txt
    python run_all.py

## What is genuine vs data-gated
- GENUINE and run here: composition construction via the clean pre-2020 M1 transaction-active proxy,
  vs simple-sum M2, predicting CPI and PCE inflation, regime-split, in-sample + pseudo-OOS.
  Data: data/macro_1959_2026.csv (M2SL,CPIAUCSL,PCEPI) and data/m1sl_1959_2019.csv (clean M1).
  Provenance and integrity cross-checks: data/SOURCES.json.
- DATA-GATED (implemented, runs when series supplied): granular composition splice (FRED components),
  payment-flow construction (Fedwire/ACH/RTP), Divisia construction (CFS). See src/build_mt.py.

## Headline result (see results/EMPIRICAL_RESULTS.md)
In the high-inflation/high-money-growth regime, the transaction-active aggregate explains ~4-5x more
goods inflation than simple-sum M2 (CPI R2 0.19 vs 0.04; PCE 0.20 vs 0.08) and statistically displaces
M2 in a joint regression. In the low regime both are weak. The falsification condition is not triggered.
The claim is bounded: Mt beats M2, not the central bank.

## Determinism
Fixed transformations; no random seeds required. Environment: see requirements.txt.

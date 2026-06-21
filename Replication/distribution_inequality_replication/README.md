# Citizens Standard — Distribution and Wealth Inequality (replication)

Replication for *The Citizens Standard: Distribution and Wealth Inequality* (Neo-Solon, 2026).
A microsimulation of the architecture's distributional effect, **seeded from the real 2022
Survey of Consumer Finances household records**, not a synthetic distribution.

## Run

```
pip install -r requirements.txt
python run_all.py
```

`run_all.py` executes three stages:

1. **`src/verify_scf.py`** — reproduces the published SCF 2022 figures from the bundled
   microdata (weighted mean $1.06M, median $192,700, top-1% threshold, 0.830 Gini). This is
   the read-check: if it passes, the baseline is real and correctly weighted.
2. **`src/floor_by_age.py`** — extracts the issuance engine's locked-floor accumulation by
   age (and the reinvested K3 dividend), deflated to 2022 dollars. The endpoint reproduces the
   engine's canonical $209,942 retirement floor exactly.
3. **`src/channels.py`** — applies the four channels to the real distribution and writes
   `results/inequality_results.json`.

## The four channels

| Channel | What | Grounding |
|---|---|---|
| Floor | engine floor-by-age, per adult | issuance engine (deterministic); robust headline |
| Dividend | reinvested K3 | engine; upper bound (mostly consumption) |
| Return compression | bounded top-return haircut over a generation | gradient: Fagereng et al. 2020; mechanism: Gabaix & Koijen 2021; magnitude bounded by the structural-buyer paper (2026h) |
| Bequest | near-universal inheritance; persistence argument | Nekoei & Seim 2023; Elinder et al. 2018 (registry causal evidence) |

## Headline (reproduced by the code)

- Wealth Gini 0.830 → 0.743; P10 $450 → ~$64,800; bottom-50% share 2.2% → 6.7%;
  zero/negative net worth 7.9% → 1.5%; top-1% share 35.1% → 30.4% (mostly mechanical).
- Decomposition: ~74% of the Gini reduction is the floor lifting the bottom.
- Return compression trims the top-1% share by ~1.5–4.3pp over a generation (bounded, secondary).
- Bequest: households able to bequeath >$25k rise 76% → ~99%; the floor's locked, uniform-return
  structure makes inheritance's (otherwise short-lived) equalising effect permanent.
- Consistency with the structural buyer: the floor is 19% principal (the bounded purchase flow)
  + 81% compounding, so the aggregate is consistent with the 6–12% ownership ceiling.

## Data

`data/SCFP2022.csv` — 2022 Survey of Consumer Finances, Summary Extract Public Data
(Federal Reserve Board, released 2023). Public-use data; 4,595 families × 5 implicates.
Cite: Board of Governors of the Federal Reserve System, *Survey of Consumer Finances*, 2022.

## Code

`src/deterministic_engine.py` (+ `authoritative_data.py`, `authoritative_newcitizens.py`) is the
issuance engine used by the rest of the series; the floor channel calls it directly so the floor
values are identical to the engine's, not re-derived.

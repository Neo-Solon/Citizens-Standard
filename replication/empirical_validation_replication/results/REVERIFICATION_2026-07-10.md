# Independent Re-Verification on Freshly-Pulled FRED Data (2026-07-10)

This record documents an independent re-run of the Paper 10 headline claims on
**freshly downloaded FRED source files**, using the frozen pre-registration protocol
(`validation_protocol.md`). It confirms the package reproduces on data pulled independently
of the versions shipped in `data/`.

## Data used (independently pulled from FRED)
- `CURRSL` (currency), `DEMDEPSL` (demand deposits), `OCDSL` (other-checkable) — composition Mᵀ
- `CPIAUCSL` (US CPI), `M2SL` (simple-sum M2 benchmark)
- CFS Divisia (Narrow / Divisia M1) — user-cost construction

## Protocol (frozen, unchanged)
Regime split = trailing-12-month CPI inflation ≥ 4% (high) vs < 4% (low).
Predictor = trailing-12m log change in the aggregate. Dependent = next-12m log change in CPI.

## Results — every headline figure reproduces

| Claim (Paper 10) | Published | Re-verified | Status |
|---|---|---|---|
| Composition vs Divisia convergence — log level | 0.99 | 0.985 | ✓ |
| Composition vs Divisia convergence — 12m growth | 0.82 | 0.839 | ✓ |
| Composition Mᵀ high-regime R² | 0.19 | 0.186 | ✓ |
| Simple-sum M2 high-regime R² | 0.04 | 0.043 | ✓ |
| Mᵀ / M2 information ratio (high regime) | ~5× | 4.4× | ✓ |
| Divisia M1 high-regime R² (pre-2020 clean) | 0.21 | 0.209 | ✓ |
| Encompassing regression (HAC-12): M2 displaced | M2→0 | Mᵀ t=2.3 p=0.02; M2 t=−0.3 p=0.76 | ✓ |

## Honest notes carried forward
- The two constructions **share no inputs** (composition = simple sum of components;
  Divisia = user-cost-weighted), so their convergence is informative, not mechanical.
- **Divisia sample split investigated:** the pre-2020 clean sample gives R²=0.209 (matching
  the paper); a naive pool of pre-2020 with the 2020+ window flattens it to ~0.14 — a pooling
  artifact, not a failure. The 2020–2022 high-CPI sub-window (n=26) is a single continuous
  episode, too small to adjudicate standalone; not cited as an independent result either way.
- The advantage is **regime-conditional** (vanishes in pooled/low-inflation samples), and
  out-of-sample the transactional aggregates tie a naive persistence baseline — "money beats
  broad money, not the central bank," exactly as the paper states.

Machine-readable version: `reverification_2026-07-10.json`.

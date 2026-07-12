# The CS-to-Fractional-World FX Interface — Replication Package (v0, foundation)

This is the **first** of the CS-to-fractional-world models: how a Citizens Standard
currency behaves on the foreign-exchange market against ordinary floating-fiat currencies.
It is the foundation the other three layers (trade/competitiveness, capital-flow/adoption,
reserve-currency dynamics) build on.

## What it answers

The audio's and the papers' honest gap: *how does a CS economy trade with today's normal
fractional-reserve, floating-fx world?* At the FX level, the mechanics are ordinary — a CS
currency exchanges on conventional FX markets like any currency. The **question this package
makes empirical** is whether its rule-fixed, low-variance inflation anchor makes its exchange
rate **behave differently** — specifically, more stably — than a comparable floating fiat.

## Method (two pre-registered lines — see validation_protocol.md)

- **Line A — variance decomposition.** Decompose real bilateral-rate variance into
  inflation-differential (PPP), interest-differential (UIP/carry), and residual (risk/noise).
  The CS anchor fixes its own inflation by rule and runs no discretionary carry, so it removes
  the **CS-side monetary share**. We measure that share.
- **Line B — anchored-vs-floating natural experiment.** Real currencies with a rule-fixed
  nominal anchor (currency boards, hard pegs, credibly low-inflation regimes) are the closest
  existing analogue. Compare their realized FX volatility to freely-floating currencies.

**Bracketing, not pinning.** A CS currency is not a peg (it floats nominally while anchoring
inflation). Hard pegs are the *low-volatility bracket*, floating inflation-targeters the *high*
bracket; CS sits between. The package reports the bracket and places CS inside it — it does not
claim CS equals any single observed currency.

## Falsification (fixed in advance)

The CS FX-stability claim fails if **(F1)** the CS-removable monetary variance share is
negligible (<10%), or **(F2)** anchored currencies do not show lower excess volatility than
floating ones. Either result would be reported honestly.

## Status of the numbers  ⚠️ READ THIS

**The current results are computed on a SYNTHETIC panel** whose moments are *calibrated to
published real-world figures* (see SYNTH_MOMENTS in build_fx_data.py). This proves the pipeline
end-to-end and produces real, interpretable output — but the **headline figures are not yet the
real-data figures.**

To produce the real, citable results:
1. Pull the FRED/BIS series listed in the header of `build_fx_data.py` (exact series IDs given).
2. Drop them as CSVs into `./data_real/`.
3. `python run_all.py` — the pre-registered protocol runs unchanged on real data.

Because the protocol is **frozen before** the real data is fitted (Appendix-E discipline),
running it on real data is a clean confirmatory test, not a specification search.

## What the synthetic run already demonstrates (method validation)

- The decomposition and volatility machinery work and are deterministic (seed 20260710).
- The bracket logic shows up correctly: hard-peg analogues (HKD, SAR, AED) show very low
  FX volatility and low excess-vol; the *soft* analogue (CHF — low-inflation but freely
  floating) correctly shows HIGH excess volatility. That contrast is the point: inflation-
  anchoring **plus** rule-based credibility is what suppresses FX variance, and the model
  surfaces the distinction rather than hiding it.
- On calibrated moments the claim survives both falsification conditions (mean CS-removable
  share ~28%, anchored excess-vol below floating). **These specific numbers will move on real
  data** — treat them as a working demonstration, not the final result.

## Honest limits (standing)

- **No CS currency exists.** This bounds CS behavior by real analogues; it is not an
  observation of a CS currency. The evidence is a bracket, not a point forecast.
- **Pegs understate CS FX variance** (CS floats nominally). Reported as the low bracket only.
- **Reserve-currency / safe-haven status is out of scope** — that is the separate deferred
  question (Paper 3), and a later layer of this program.
- **Regime choice is endogenous** — anchored countries differ systematically; the bracket
  logic mitigates but does not eliminate this.

## Files
- `validation_protocol.md` — the pre-registered protocol (frozen before estimation)
- `build_fx_data.py` — data assembly (real loader + calibrated synthetic; exact series IDs)
- `run_fx_analysis.py` — Line A, Line B, falsification
- `run_all.py` — one-command driver
- `RESULTS_*.csv/.json` — outputs
- `RESULTS_manifest.md` — claim → script → output map
- `requirements.txt` — pinned deps

## Next layers (this program, in order)
1. **FX interface** — this package.
2. Trade / competitiveness (real exchange rate, zero-inflation CS vs inflating partners).
3. Capital-flow / adoption dynamics (one-by-one adoption, first-mover, contagion).
4. Reserve-currency dynamics (the deferred Paper 3 safe-haven question).

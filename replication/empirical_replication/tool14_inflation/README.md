# Replication: Tool 14 vs. Real Inflations — a structural counterfactual

**Author:** Neo-Solon · **Contact:** Neo-Solon@hotmail.com · **License:** CC BY 4.0

**Home paper.** This is the inflation-counterfactual appendix to *The Citizens
Standard as Counterfactual Benchmark and Forward Projection: An Empirical Analysis
of an Alternative US Monetary Architecture* (Neo-Solon 2026, SSRN 6735078) — the
empirical/historical-counterfactual paper, and the package this folder lives in.

**Cited mechanism.** The transmission it relies on is proven in the companion
theory paper, *A Macroeconomic Model of a Two-Circuit Monetary System* (Neo-Solon
2026e, SSRN 6939418): specifically **Proposition 6** (the linearized two-circuit
system, KI self-correction vs the KI-off unit root). `structural_run.py` drives
the episodes through that proposition's own system, parameters verbatim; this
appendix does not re-derive the theory, it takes it to data.

Formalizes the interactive engine's "Tool 14 vs. real inflations" demonstration
into a reproducible, empirically grounded counterfactual for two well-documented
US inflations — the 2021–2023 surge and the 1972–1983 Great Inflation / Volcker
disinflation. It is a **counterfactual, not a forecast**, and it does not claim
the framework could prevent a supply shock.

## Two counterfactuals, kept separate

These answer different questions and must not be blended:

* **Prevention (managed-throughout) — the headline.** If the framework had been
  the system all along, how high would inflation have gotten? Its rule-bound
  issuance never creates the demand/monetary component and KI→0 is automatic, so
  only the supply share passes through; Tool 14 then shaves what remains.
* **Response (drop-in) — the honest, conservative secondary.** Given inflation is
  already at the peak (the old system made it), how fast can the framework bring
  it down? Only Tool 14 acts, at its real capacity (~2.2pp/yr). This is
  deliberately **slower** than an aggressive rate shock.

## What is and is not fitted

* **Actual** paths are raw BLS CPI-U (12-month change) — not modeled.
* **2022 demand share** is the **SF Fed (Shapiro) published monthly decomposition**
  (headline PCE, year-over-year, Figure 3 chart CSV), applied month by month — not
  a parameter we chose. Grounding it in the data actually *raised* the framework's
  2022 peak versus an earlier judgment-call share, because the realized demand
  share at the June 2022 peak was only ~38%.
* **1980 demand share** predates the SF Fed series (which begins 1998), so it
  falls back to the Federal Reserve's own attribution of the Great Inflation to
  excessive money growth — a literature attribution, disclosed as such, carried as
  a band (0.55–0.80).
* **Framework parameters** (anchor, anchor+3pp trigger, 3%-of-M2/yr Tool 14
  ceiling, unit quantity-theoretic pass-through) come from the architecture/macro
  papers and the KT appendix, identical across both episodes (see the
  out-of-sample check in `sensitivity.py`).

## Headline results

| | 2022 surge | 1980 / Great Inflation |
|---|---|---|
| Window | Jan 2021 – Dec 2023 | Jan 1972 – Jun 1983 (full build-up) |
| Actual peak (BLS) | 9.1% (Jun 2022) | 14.8% (Mar 1980) |
| Demand share | SF Fed monthly (~0.38 at peak) | Fed attribution (0.70 central) |
| Prevention peak — structural | ~6.0% | ~5.1% |
| Prevention peak — +Tool 14 | ~4.6% | ~4.0% |
| Prevention-peak band | 4.1%–4.6% | 3.8%–4.1% |
| Months above 4% — framework vs actual | 9 vs 25 | 0 vs 117 |
| Response (Tool 14 only) by window-end | 5.8% vs actual 3.4% | 7.7% vs actual 2.6% |
| **Structural cross-check (Prop 6)** | **4.1%** (vs 4.6% reduced form) | **3.4%** (vs 4.0% reduced form) |
| Conventional policy rate | 0.1%→5.3% | ~19% |
| Conventional real cost | mortgages 3.2%→7.1% | 10.8% unemployment; sacrifice ratio ~2.5 |

## Structural cross-validation (the model's own transmission)

The headline numbers above come from a transparent reduced form. As a check,
`structural_run.py` drives the *same* episodes through the framework's proven
transmission — the linearized two-circuit system of Proposition 6 in the macro
paper, parameters verbatim — by backing out the price shocks that reproduce the
actual inflation under the status quo (KI off, unit root) and then running those
same shocks through the framework (KI on, plus Tool 14).

* **Both episodes cross-validate.** The proven KI self-correction and the static
  demand-share reduced form independently land within ~1pp of each other —
  structural 4.1% vs reduced-form 4.6% for 2022, structural 3.4% vs reduced-form
  4.0% for 1980 — far below the actual 9.1% / 14.8%. Two independent mechanisms
  agree, so the counterfactual is both model-generated and hand-reproducible.
* **1980 required the full window.** Fed the 1972–1983 build-up from 3.3%, the
  framework self-corrects each oil-shock and monetary impulse before it compounds,
  so the Great Inflation never forms (structural prevention peak 3.4%). On the
  narrow 1979–1983 window the same model instead measures a *drop-in* at 11%+,
  which KI can only unwind slowly — the response path, not prevention. The
  distinction is real and the appendix states it: prevention needs the framework
  present through the build-up, which is the whole point of a monetary system.

This is the honest state: both 2022 and 1980 prevention are now validated under
the framework's own proven transmission, agreeing with the transparent reduced
form to within ~1pp.



1. **Prevention is primary.** Most of the gap between framework and actual comes
   from never creating the demand component (the structural baseline), not from
   the active surcharge. Tool 14's marginal effect on the peak is a secondary
   shave (6.0→4.6 in 2022; 5.1→4.0 in 1980). The framework's primary inflation
   defense is its issuance rule, not an emergency tool.
2. **No interest-rate channel.** The framework disinflates by retiring money, so
   none of the mortgage shock (2022) or the recession and 10.8% unemployment
   (1980) that the conventional cure imposed.
3. **NOT faster disinflation.** The response path is explicit about this: Tool 14
   at ~2.2pp/yr is *slower* than an aggressive rate shock (the 2022 Fed cut CPI
   ~6pp/yr; Volcker faster still in 1982). The trade is no collateral damage, not
   speed. Claiming otherwise — as a naive drop-in reading would — is an overclaim
   this module deliberately refuses.

## Caveats

* Counterfactual, not a forecast.
* The framework cannot stop a supply shock; the residual bump is exactly that.
* The SF Fed series is PCE; we borrow the demand *fraction* and apply it to the
  CPI excess (a disclosed, standard approximation). 1980 lacks the series.
* The response path is conservative — it ignores that on takeover the framework
  would also halt the old system's ongoing accommodation, which would help.
* The quantity-theoretic pass-through is deliberately simple (unit, on the demand
  share); a full New-Keynesian transmission is left to the macro model proper.

## Files

```
code/data.py             BLS series, SF Fed monthly demand share, constants (all cited)
code/tool14_engine.py    prevention + response mechanisms (mechanical triggers)
code/run_counterfactual.py   headline tables  ->  results.txt
code/structural_run.py   SAME counterfactual via the macro paper's Proposition 6
                         transmission (cross-validates the reduced form)
code/sensitivity.py      demand-share / capacity / trigger sweeps + out-of-sample
code/make_figures.py     figures/figure_T14_{2022,1980}.png
data/*.csv               the BLS series and the SF Fed demand-share series
AUDIT.md                 provenance of every number
```

Run: `cd code && python run_counterfactual.py && python sensitivity.py && python make_figures.py`

## References

* U.S. BLS. CPI-U, all items, U.S. city average, 12-month change (CUUR0000SA0).
* Shapiro, A. H. (2022b). "How Much Do Supply and Demand Drive Inflation?"
  *FRBSF Economic Letter* 2022-15. Data: FRBSF "Supply- and Demand-Driven PCE
  Inflation," Figure 3 (YoY headline) chart CSV.
* Federal Reserve History. "The Great Inflation"; "Recession of 1981-82."
* Goodfriend, M., King, R. G. (2005). "The Incredible Volcker Disinflation,"
  *J. Monetary Economics* 52(5). (Sacrifice ratio.)
* Freddie Mac. Primary Mortgage Market Survey, 30-year fixed, 2022.

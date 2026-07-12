# FX Interface — Pre-Registered Validation Protocol

**Frozen before estimation.** This document fixes the hypotheses, the constructions,
the country/pair selection rules, the metrics, and the falsification condition **before**
any data is fitted. Reporting a post-hoc specification search would forfeit the credibility
this exercise is meant to establish (same discipline as the empirical-validation paper's
Appendix E).

---

## The question

How does a Citizens Standard (CS) currency — one whose inflation is anchored near zero
by rule, with low variance, issued by a rule not by discretion — behave on the foreign
exchange market against ordinary floating-fiat currencies?

No CS currency exists. This is therefore a **calibrated-analogue** exercise: we bound the
likely FX behavior of a CS currency using **real currencies that share its key structural
feature** (a rule-fixed, low-variance nominal anchor meeting a floating counterpart), and
we **size** the mechanism by decomposing the variance of real floating-vs-floating rates
into the component a CS anchor would remove.

The claim is bounded and stated in advance: **not** that a CS currency would be maximally
stable, but that removing one side's monetary-surprise variance (by rule-anchoring its
inflation) removes an identifiable, quantifiable share of bilateral exchange-rate variance,
and that real anchored-vs-floating pairs exhibit **lower excess FX volatility** than
comparable floating-vs-floating pairs.

---

## Two independent lines of evidence (pre-specified)

### Line A — Variance decomposition (sizes the effect)
For real floating/floating pairs, decompose the variance of the change in the nominal
bilateral rate into:
  1. an **inflation-differential (PPP)** component,
  2. an **interest-differential (UIP/carry)** component,
  3. a **residual** (risk / safe-haven / noise).

A CS currency fixes its own inflation by rule (component 1's CS-side term → a constant)
and has no discretionary policy rate to run carry against (component 2's CS-side term
structurally muted). The **pre-registered quantity** is the share of bilateral-rate
variance attributable to the CS-side monetary terms — i.e., the variance a CS anchor
would plausibly remove. Reported as a range across pairs, not a point.

### Line B — Anchored-vs-floating natural experiment (bounds CS behavior)
Real currencies with a **rule-fixed nominal anchor** (hard pegs, currency boards, and
credibly low-variance-inflation regimes) are the closest existing analogue to a CS
currency meeting the floating world. Compare realized FX volatility of:
  - **Anchored group:** e.g. HKD (currency board), DKK (ERM-II hard band), BGN (board),
    Gulf pegs (SAR/AED), CHF (low-variance-inflation float) — each vs USD and vs EUR.
  - **Floating group:** e.g. GBP, JPY, AUD, CAD, SEK, NOK, KRW, MXN — each vs USD and vs EUR.

Pre-registered comparison: **realized annualized volatility of monthly log-returns**, and
the **excess-volatility ratio** (realized FX vol / inflation-differential vol). The
hypothesis is that the anchored group shows lower excess volatility.

**Bracketing, not pinning.** A CS currency is *not* a peg — it floats nominally while
anchoring inflation. So pegs are the **low-volatility bracket** (they fix the nominal rate
outright) and credible inflation-targeters are the **high-volatility bracket** (they anchor
inflation but let the rate float). CS sits **between**: it anchors inflation like a good
targeter but with rule-based, lower-variance credibility. The protocol reports the whole
bracket and places CS inside it rather than claiming a single number.

---

## Selection rules (fixed in advance, to prevent cherry-picking)

- **Pairs:** every currency in the anchored and floating lists above, each quoted against
  both USD and EUR, over the common maximum sample for which all inputs exist.
- **Sample:** monthly, longest common window where FX + CPI + policy-rate series co-exist
  for the pair; regime classification from Ilzetzki–Reinhart–Rogoff (IRR) and IMF AREAER.
- **Exclusions fixed in advance:** drop any pair-month during a documented regime break
  (peg abandonment, board suspension) using the IRR coarse classification; these are
  reported separately, not silently dropped.
- **No pair is added or removed after seeing its volatility.**

---

## Metrics (fixed)

1. Realized annualized volatility of monthly log FX returns, per pair.
2. Excess-volatility ratio = realized FX vol ÷ inflation-differential vol.
3. Variance shares (Line A): PPP / UIP / residual, per pair, via the pre-specified
   regression + variance-attribution below.
4. Group contrast: anchored vs floating, on (1) and (2), with a simple difference-in-means
   and a rank test — no fancier estimator that could be tuned.

---

## Falsification condition (decidable, fixed in advance)

The CS FX-stability claim is **empirically empty** if **either**:
  (F1) the CS-side monetary variance share in Line A is negligible (< ~10% of bilateral
       rate variance on average) — i.e., anchoring inflation removes almost nothing; **or**
  (F2) the anchored group does **not** show lower excess volatility than the floating group
       in Line B (difference ≤ 0 or not distinguishable).

If either fires, the honest report is that FX stability is **not** a demonstrable CS
advantage, and the audio/paper must say so.

---

## Honest limits (stated up front, not discovered late)

- **No CS instance:** this bounds CS behavior by analogy; it is not an observation of a CS
  currency. The strongest available evidence is a bracket, not a point forecast.
- **Pegs are an imperfect analogue:** CS floats nominally, so hard pegs *understate* CS FX
  variance and *overstate* its rigidity. Reported as the low bracket, not as "CS behaves
  like a peg."
- **Reserve-currency status is out of scope here** (it's the separate, deferred question);
  this package models the *interface mechanics*, not safe-haven flows earned over decades.
- **Endogeneity:** anchored regimes are chosen, not random; countries that peg may differ
  systematically. Reported as a confound, addressed only by the bracket logic, not claimed
  away.

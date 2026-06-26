# Anchor Robustness vs Real Observed Divergence (Paper 7)

Tests Paper 7's claim that a common ZERO anchor is robust "across the empirically
observed ranges" of cross-country inflation divergence — but where the paper's own
replication swept *abstract* shock variances (<=2%), this module feeds the paper's
own real-rate-distortion mechanism the inflation divergences history *actually*
produced.

## Result (vindicates Paper 7 against real shocks, with one honest boundary)

1. **The zero anchor absorbs every transient real divergence.** Using the paper's own
   distortion mechanism (reused verbatim from the interoperability replication's
   `equa_stress.py`), the terminal bilateral real-rate distortion is ~0% for the 2022
   ~6pp spike, the 2021 gap, and even Japan's ~17-year deflation gap — because
   transient deviations around a common zero re-converge. This is stronger than the
   original test, which could only show robustness to assumed shocks <=2%; the real
   divergences are larger and the anchor still absorbs them.

2. **A common positive anchor (+2%) leaves a structural ~-5.77% wedge** regardless of
   the divergence — confirming the paper's "only zero is fully robust" result against
   real magnitudes (the deflation-buffer asymmetry).

3. **The honest boundary:** robustness is to *transient* divergence, not to a
   *permanent* level split. If a partner abandons the anchor and runs +k pp forever,
   the residual is ~+k% — proportional and real. So the anchor's robustness rests on
   the *commitment holding* (a governance property), not on immunity to any
   divergence. Real history is the transient kind; a permanent unilateral exit is the
   failure mode, and it is the same capture/override risk catalogued for the domestic
   rule.

## Verified divergence anchors (major-economy CPI/HICP, public sources)
- 2022 acute spike: US/EU ~8–9% vs Japan ~2.5% → ~6pp gap, transient (~2y).
- 2021: EU 2.9% vs Japan -0.2% → ~3pp.
- Japan deflation era ~1995–2012: ~2–3pp sustained for ~17 years.
- 2016–2020: ~1–3pp rolling gaps.

## Method / honesty notes
- The distortion mechanism is the paper's own (lag-1 vs lag-4 wage stickiness; terminal
  deviation of the bilateral real-rate ratio from the no-inflation benchmark), applied
  directly to the real divergence paths rather than approximated.
- Transient episodes are modeled as gaps that revert to the common anchor (consistent
  with the historical record, where these divergences closed). The permanent-split
  case is shown separately as the genuine failure mode.
- Reduced-form, two-partner, deterministic; not a multilateral GE model.

## Reproduce
```
cd code
python3 stage1_observed_divergence.py
python3 stage2_zero_dominance.py
```

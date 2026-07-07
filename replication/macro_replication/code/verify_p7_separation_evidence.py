"""
verify_p7_separation_evidence.py
--------------------------------
P7's determinacy rests on TWO empirical premises:
  (a) alpha > 0  (Cagan money-demand sign) -- robustly established, already cited.
  (b) circuit SEPARATION -- transactional money carries the consumer-price signal
      while broad (asset-heavy) money does not. THIS is the distinctive premise and
      it is the one Paper 5 does not yet connect to evidence.

This module pulls the RELEVANT results from the Paper 10 validation horserace
(empirical_validation_replication) and states EXACTLY what they do and do not
support for premise (b), so the paper's claim matches the data.

It does not re-run the horserace (that lives in Paper 10); it records the finding
so P7's empirical basis is documented in one place, honestly.
"""

# Numbers as produced by empirical_validation_replication/src/run_composition_horserace.py
# (US, FRED, pre-2021 sample where the transaction-active composition aggregate is defined;
#  high regime = trailing CPI >= 4%; 12m horizon; HAC; PCE cross-check.)
EVIDENCE = {
    "in_sample_high_regime": {
        "composition (currency+demand+OCD)": {"R2": 0.186, "t": 2.67},
        "M1":                                 {"R2": 0.189, "t": 2.69},
        "Divisia (user-cost)":                {"R2": 0.209, "t": 2.90},
        "M2 (broad)":                         {"R2": 0.043, "t": 1.90},
    },
    "encompassing_high_regime (composition + M2 together)": {
        "composition": {"t": 2.26, "verdict": "significant -- carries the signal"},
        "M2":          {"t": -0.31, "verdict": "insignificant -- drops out"},
    },
    "PCE_cross_check_high_regime": {
        "composition": {"R2": 0.197, "t": 3.00},
    },
    "out_of_sample_high_regime": {
        "composition_rmse": 2.82, "persistence_baseline_rmse": 2.69,
        "verdict": "does NOT beat naive persistence OOS",
    },
    "measured_convergence": {
        "corr_growth_composition_vs_divisia": 0.825,
        "corr_level_composition_vs_DM1": 0.991,
    },
}

def summarize():
    print("="*70)
    print("P7 SEPARATION PREMISE — what the Paper 10 horserace supports")
    print("="*70)
    print("""
  SUPPORTS premise (b) IN-SAMPLE, high-inflation regime:
    - Transactional aggregates (composition, M1, Divisia) carry a significant
      consumer-price signal: R^2 ~ 0.19-0.21, t ~ 2.7-2.9.
    - Broad M2 does NOT: R^2 ~ 0.04, t ~ 1.9 (weak).
    - DECISIVE for separation: in the encompassing regression (composition + M2
      jointly), composition stays significant (t=2.26) and M2 DROPS OUT (t=-0.31).
      i.e. once transaction money is in, broad money adds nothing to consumer-price
      prediction -- exactly the two-circuit claim.
    - Robust to PCE as the price index (t=3.00).

  DOES NOT SUPPORT (honest limit):
    - Out-of-sample, the transactional aggregate does NOT beat a naive persistence
      baseline (RMSE 2.82 vs 2.69). The separation signal is IN-SAMPLE structural,
      not an OOS forecasting edge.

  READING FOR P7:
    P7 assumes asset-circuit money does not chase consumer goods (separation up to
    the coupling threshold). The horserace gives DIRECT in-sample evidence for the
    consumer-price side of that split: transaction money carries the price signal,
    broad/asset-heavy money does not. This is empirical support for P7's premise
    (b), stated at its honest strength -- in-sample and regime-dependent, not an
    out-of-sample law. The paper should cite it as SUPPORTING, not PROVING.
""")
    return EVIDENCE

if __name__ == "__main__":
    summarize()

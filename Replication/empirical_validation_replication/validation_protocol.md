# Pre-Registration Protocol — Validation of the Transactional Aggregate
Frozen before estimation. Matches Paper 10, Appendix E. Deviations, if any, are reported as deviations.

1. Mt constructions: (1) composition [active = currency + demand + other-checkable; savings held idle
   across the May-2020 redefinition]; (2) payment-flow [turnover-weighted active share, Fedwire/ACH/RTP];
   (3) user-cost/Divisia [CFS transaction-tier sub-aggregate]. The locus-back-solved route is excluded.
2. Dependent variable: next-12-month log change in CPIAUCSL (primary) and PCEPI (robustness).
3. Predictor: trailing 12-month log change in the money aggregate.
4. Benchmarks: simple-sum M2; CFS Divisia M2; expectations/Phillips-curve baseline.
5. Regime split: high if trailing 12-month CPI inflation >= 4%, else low.
6. Evaluation: in-sample R2 and HAC(12) slopes; expanding-window pseudo-OOS RMSE from 1975,
   reported separately by regime; baseline = naive inflation-persistence (next-12m infl = trailing 12m infl).
7. Falsification: if independently-measured Mt adds no goods-inflation information beyond M2 across all
   available constructions out-of-sample, the decomposition has no empirical content.

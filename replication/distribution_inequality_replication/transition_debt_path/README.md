# Transition Debt Path -- replication (Paper 3, Section 4.1 & 4.1.1)

Reproduces Paper 3's transition trajectory: under Mode T the KT channel retires
legacy public debt from ~102% of GDP into a moderate operational band of ~30-60%
of GDP (central path ~45%, reached ~Year 26), where it stabilises rather than
descending to a low floor. Within the band KT throttles down and routes the freed
growth-matched seigniorage to citizen Stable Floors.

## The endpoint is a band, set by welfare analysis
The descent is ordinary debt dynamics (nominal growth + KT + a phasing primary
surplus). The *endpoint* -- a band, not a low floor -- is the welfare-optimal
result of the companion cs_debt_band analysis: standing debt is near self-financing
while the safe rate sits below the growth rate (Blanchard 2019; Mauro & Zhou 2020),
so retiring below the band forgoes citizen seigniorage for no sustainability gain,
while debt-dependent crisis risk rises only well above the band (Lian, Presbitero &
Wiriadinata 2020), and a sovereign-currency issuer with its own monetary authority
sits at the damped end of that risk (De Grauwe 2011). Full validated analysis lives
in the cs_debt_band package.

## Files
- code/stage1_band_path.py -- the central trajectory; reproduces Paper 3 Table 2
  (Year 10 = 84%, Year 20 = 58%, Year 30 = 45%, holds at 45%) exactly.
- code/stage2_band_robustness.py -- sweeps growth, post-transition coupon, and KT
  scale; shows the band is entered robustly (~17-26 years) across the plausible
  range, not knife-edge.
- output/ -- saved results of both stages.

## Anchors (verified, 2024-2026)
Debt held by public ~$31.4T (~102% of GDP); GDP ~$30.8T; real growth ~2.0%
(CBO 1.8-2.7%); coupon repricing 4.5% -> ~3.0%; M2/GDP ~0.73; KT at 1.5% of M2.

## Reproduce
    python3 code/stage1_band_path.py
    python3 code/stage2_band_robustness.py

## Key results
- Central path matches Paper 3 Table 2 exactly.
- Cumulative KT to stabilise in the band ~$12T (less than a retire-to-floor path,
  because less debt is retired); the difference is delivered to citizen Stable
  Floors instead.
- Band reached within ~17-26 years across all plausible macro assumptions.

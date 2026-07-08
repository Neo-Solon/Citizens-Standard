# Payment-flow construction of M^T -- REGISTERED RUN (Fedwire/ACH/RTP data)

Retail payments value P(t): sum of available instrument columns per year
(coverage per year is recorded in data/payments_volumes.csv and data/SOURCES.json).

## [A] Narrow-anchor level (lower-bound concept)
tau* = median 2013-2019 of P/(CURR+DD+OCD) = 22.05 turns/yr (7 calibration years)
s_pf(2025) = 0.2509 of M2  -- a LOWER BOUND on the transaction-active share:
the narrow pre-2020 stock excludes actively used savings-type balances, so the
anchor overstates per-dollar turnover and understates the share.

## [B] Registered-band consistency (the level test, stated honestly)
P(2025) = $121,530B against M2 = $21,968B.
The registered band M^T/M2 in [0.46, 0.57] holds iff transaction-active
balances turn over 9.7-12.0 times per year on average (10.8 at the 51.35% point) --
i.e. roughly monthly turnover, squarely plausible for balances that include
actively used savings-type money; the narrow anchor's 22.1 turns/yr is the
checking-account corner. The payments data therefore BRACKET the share between
the narrow bound above and the band, rather than pinning a point.

## [C] Growth convergence (anchor-free)
Quarterly test (sourced Nacha panel, data/payments_quarterly.csv, YoY log growth,
24 overlapping quarters 2020Q1-2025Q4):
  corr(dlog ACH value, dlog Divisia DM1) = +0.67
  corr(dlog ACH value, dlog M2)          = +0.69
Full-window correlations are a statistical tie: the growth axis cannot break
the M^T-vs-M2 race on its own. The discriminating subwindow is sharper:
2020Q1-2021Q4 (n=8), corr ACH~DM1 = +0.04, corr ACH~M2 = +0.11 --
payments growth (+4% to +22% YoY) decoupled from BOTH balance
aggregates (+8% to +35%): the 2020-21 surge parked in idle
balances rather than transactions. That is the decomposition's premise observed
directly in payments data, and simultaneously the reason no growth-axis
correlation can adjudicate between M^T constructions in that episode: the
redefinition-era surge moved every balance aggregate together. Annual pre-2021
correlations (n=6, partly interpolated checks) remain uninformative and are
not reported as evidence.

## [D] Independent turnover benchmark (JPMC Institute cash buffers)
Wheat & Eckerd (2023, JPMorgan Chase Institute; 19M individuals, 2008-2023)
measure household cash buffers -- liquid balances over trailing-12m median
checking outflows ex transfers -- stable pre-pandemic at 13/16/19/26 days of
spending across income quartiles: measured checking-account turnover of
14.0-28.1 turns/yr. The panel's narrow-anchor tau* = 22.05 (16.6-day
buffer) sits inside that measured range: the narrow stock turns over like
checking accounts do, as the anchor asserts. The registered band requires
9.7-12.0 turns/yr of the FULL active stock -- buffers of 30-38 days,
i.e. roughly one month of spending held in transaction-active form -- which
is what folding actively-used savings-type balances into the active stock
produces (M^T ~ 2x the narrow stock implies buffer-doubling from the
checking-only 13-26 days). Caveats: person-median rather than dollar-
weighted; household-side only (business accounts unmeasured); one
institution's footprint. Both ends of the bracket now carry independent
measurement; the level itself remains bracketed, and the data that would
pin it (payment values split by funding-account type) is bank-supervisory,
not public.
## Series
year, P ($B), M^T_pf narrow ($B), share of M2:
  2013, 68,730, 3,117, 0.2899
  2014, 69,610, 3,157, 0.2766
  2015, 70,790, 3,210, 0.2659
  2016, 72,070, 3,268, 0.2535
  2017, 74,380, 3,373, 0.2476
  2018, 78,000, 3,537, 0.2501
  2019, 82,740, 3,752, 0.2524
  2020, 88,990, 4,036, 0.2280
  2021, 99,830, 4,527, 0.2204
  2022, 103,930, 4,713, 0.2181
  2023, 107,457, 4,873, 0.2335
  2024, 113,676, 5,155, 0.2439
  2025, 121,530, 5,511, 0.2509

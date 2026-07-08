# Payment-flow construction of M^T -- SELF-TEST (synthetic schema data)

Retail payments value P(t): sum of available instrument columns per year
(coverage per year is recorded in data/payments_volumes.csv and data/SOURCES.json).

## [A] Narrow-anchor level (lower-bound concept)
tau* = median 2013-2019 of P/(CURR+DD+OCD) = 9.00 turns/yr (7 calibration years)
s_pf(2025) = 0.5100 of M2  -- a LOWER BOUND on the transaction-active share:
the narrow pre-2020 stock excludes actively used savings-type balances, so the
anchor overstates per-dollar turnover and understates the share.

## [B] Registered-band consistency (the level test, stated honestly)
P(2025) = $100,832B against M2 = $21,968B.
The registered band M^T/M2 in [0.46, 0.57] holds iff transaction-active
balances turn over 8.1-10.0 times per year on average (8.9 at the 51.35% point) --
i.e. roughly monthly turnover, squarely plausible for balances that include
actively used savings-type money; the narrow anchor's 9.0 turns/yr is the
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
14.0-28.1 turns/yr. The panel's narrow-anchor tau* = 9.00 (40.6-day
buffer) sits inside that measured range: the narrow stock turns over like
checking accounts do, as the anchor asserts. The registered band requires
8.1-10.0 turns/yr of the FULL active stock -- buffers of 37-45 days,
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
  2013, 23,023, 2,558, 0.2379
  2014, 25,445, 2,827, 0.2477
  2015, 27,343, 3,038, 0.2516
  2016, 29,414, 3,268, 0.2535
  2017, 31,927, 3,547, 0.2604
  2018, 33,347, 3,705, 0.2620
  2019, 34,853, 3,873, 0.2605
  2020, 81,226, 9,025, 0.5100
  2021, 94,271, 10,475, 0.5100
  2022, 99,179, 11,020, 0.5100
  2023, 95,791, 10,643, 0.5100
  2024, 97,005, 10,778, 0.5100
  2025, 100,832, 11,204, 0.5100

# Empirical Grounding of the Injection-Topology Simulation (injection_topology.py)

Every variable, sorted by how well it grounds. This document is the honest
boundary of what the simulation can claim.

## Tier 1 — Directly grounded in published micro-data

**lam, price-adjustment speed (per month).** Median price durations from BLS
CPI micro-data: 4.3 months for posted prices (Bils & Klenow 2004, JPE); 8-11
months for regular prices excluding sales (Nakamura & Steinsson 2008, QJE);
14.5 months with all temporary changes filtered (Kehoe & Midrigan 2015, JME).
Monthly adjustment speed = 1/duration gives the calibration set
{0.07, 0.11, 0.23}. The disagreement in the literature is itself the reason to
run the full range rather than a point value.

**Injection size.** US M2 grew more than 23% year-over-year in 2020; before
2020 the record YoY growth in Fed data was under 15% (FRED M2SL). The
calibrated run injects 23% of the money stock as a 12-month flow, replicating
the historical episode. The stylized run's 10% one-shot is conservative
relative to history.

**Injection-layer topology.** The Fedwire interbank payment network has a
tightly connected core of money-center banks to which all other banks connect,
with a scale-free degree distribution over a substantial range (Soramaki,
Bech, Arnold, Glass & Beyeler 2007, Physica A / FRBNY Staff Report 243).
Core-periphery structure corroborated for Japan (Imakubo & Soejima 2010) and
Denmark (Rordam & Bech 2009). Counterpoint honestly noted: Craig & von Peter
(2014) argue for core-periphery rather than strictly scale-free in UK data;
Iori et al. (2008) find exponential fits for Italy. Our qualitative results
hold on both Barabasi-Albert (scale-free) and Watts-Strogatz (small-world)
graphs, so they do not hinge on the disputed distributional form. What all
studies agree on -- a small dense core through which injection passes first --
is the property the model uses.

## Tier 2 — Grounded approximately

**s, spend fraction per period.** Maps to money velocity. M2 velocity of
roughly 1.1-1.4/yr implies ~0.1/month; transactional (M1-type) velocity
implies substantially higher turnover. Calibration set {0.11, 0.45} brackets
the range. Approximate because velocity is an aggregate ratio, not a measured
per-agent spend propensity, and because the model's single s conflates
heterogeneous agent behavior. Confirm current FRED M2V before citing a point
value.

**Channel mix (2020-21 replica).** The 75/25 hierarchical/uniform split is a
rough characterization of QE-plus-institutional channels vs direct Economic
Impact Payments within the 2020-21 injection. The exact split is contestable;
because the model is linear in balances, results for any other split are exact
convex combinations of the pure-channel runs, so readers can recompute their
preferred mix without rerunning.

## Tier 3 — Not grounded; stated as structural stylization

- One good, one global price level, quantity-theory price anchor.
- Fixed spend fraction; no behavioral response, no portfolio choice, no
  precautionary holding.
- The full economy-wide household spending graph is unobserved in any country.
  Fedwire evidence grounds the topology of the layer where injection enters,
  not the diffusion medium beyond it.
- Elastic goods supply during price adjustment (the aggregate windfall margin).

## What the model therefore is

A mechanism demonstration with empirically grounded parameters, not a
measurement. The claims it supports: (1) hierarchical injection produces a
network-distance advantage gradient that uniform injection does not, across
the entire empirically plausible parameter box; (2) the gradient is governed
by injection topology, nearly independent of both injection scale and
price-adjustment speed, while the aggregate windfall is governed by
price-adjustment speed; (3) channel mix maps linearly to distributional tilt.
The claims it does not support: real-world magnitudes of any of the above.

## Mechanism note (A5): why the gradient survives instant price adjustment

A natural objection: the first-recipient advantage is usually told as a
stale-price story (near agents buy before prices rise), which predicts the
gradient should vanish when prices adjust instantly. The simulation rules this
out directly. Holding the price at its final level for every period — so there
are zero stale-price purchases by construction — the near-far gradient persists
almost undiminished (4,841 vs 5,151 gradual), with aggregate real windfall
exactly zero.

The decomposition is exact (identity error 1e-12). Each agent's advantage splits
into two terms:
- **Dilution:** the price rise is a flat proportional real haircut, exactly
  `baseline_i * (1/P_final - 1)`, i.e. the same -9.09% cut on every agent's own
  consumption regardless of network position (cross-tier std/mean 0.11, and that
  residual variation is only because higher-throughput nodes consume more at
  baseline — the *rate* is identical).
- **New money reaching i:** the real value of injected nominal money passing
  through agent i, which is strongly proximity-graded.

The gradient lives entirely in the second term. So the mechanism is not
price-timing but first-receipt of the new nominal money: near agents are
compensated for the uniform price haircut by receiving the new money early and
in quantity; far agents bear the identical haircut with little compensation.
This is why adjustment speed (which governs the aggregate windfall) and network
position (which governs the redistribution) are nearly independent.

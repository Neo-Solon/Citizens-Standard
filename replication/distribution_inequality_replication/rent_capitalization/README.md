# Rent-Capitalization of the Dividend Lane

How much of a per-person cash dividend capitalizes into **rent** (a transfer to
landlords) rather than buying real consumption? This is the empirical answer to
the recurring "won't a cash floor just push up rents?" objection.

The estimate is built in two stages, kept on separate epistemic tiers so the
mechanical part and the calibrated part are never blurred.

## Result (headline)

| Stage | Quantity | Value |
|-------|----------|-------|
| 1 (accounting) | dividend **exposed** to rent, first round | ~9% of the dividend |
| 2 (calibrated, full sweep) | dividend that **capitalizes** into rent | central ~1.7%, full range 0.5%–4.6% |

Anchored to the v3_10 engine's Mode D figure ($230B to the transactional circuit
Mᵀ): central estimate **~$3.9B/yr** capitalizing into rent, full range
**$1.2B–$10.6B/yr** across the joint elasticity sweep. Even at the worst corner
(elastic demand into supply-constrained housing) the leak stays **under 5% of the
dividend**; the central case is ~2%. The conclusion that the leak is bounded and
small therefore survives the full sweep rather than resting on a single parameter
choice.

The Stage-1 exposure share is **invariant** to the absolute dividend level and the
per-person denominator (verified: 9.067% whether the dividend is $1, $672, or $980
per share), so the result is a clean distributional share.

So roughly **2% of the dividend lane leaks into rent** at the US
population-weighted housing-supply elasticity, concentrated in the bottom three
income deciles. The remaining ~98% buys real consumption (or, in floor-weighted
modes, builds the equity floor). This **bounds** the leak; it is a first-round,
partial-equilibrium figure, not a general-equilibrium result.

## Method

### Stage 1 — rent exposure (`code/stage1_rent_exposure.py`)
Mechanical, from the 2022 Survey of Consumer Finances summary extract
(`../../data/SCFP2022.csv`). For each weighted household:
- renter status and monthly `RENT` (SCF RENT is monthly; weighted median $1,000
  vs. ACS 2022 median gross rent ~$1,322 confirms monthly, the gap being
  contract-vs-gross rent),
- per-person dividend shares using the **same convention as the verified
  `channels.py`**: adults = 2 if `MARRIED` else 1, each child = 0.3 share,
- rent burden (rent / income) by income decile, **capped at 0.50** to neutralise
  the known SCF artifact whereby the bottom income decile mixes the persistently
  poor with the transitorily poor consuming above income (Wilson flags the same
  artifact in his piece). Capping moves the total only 9.8% to 9.1%, so the
  result is not artifact-driven.

Exposure = dividend-$ to each decile x renter share x (capped) rent burden,
summed. The weighting baseline is guarded by an assertion that `sum(WGT)` equals
the published US household count (131,306,389); the parent module's
`verify_scf.py` independently reproduces published SCF mean/median net worth and
the wealth Gini, so the baseline is sound.

### Stage 2 — capitalization (`code/stage2_capitalization.py`)
Converts exposure into an actual rent increase using the standard incidence
share

    capture = eps_d / (eps_d + eps_s)

evaluated over a **full 3×3 sweep of both elasticities** across their cited
literature ranges, so every figure carries an uncertainty band (calibrated tier):

- `eps_d` = price elasticity of housing demand, low-income renters, swept
  **0.15 / 0.40 / 0.62** (Ihlanfeldt 1982 low-income range 0.14–0.62, via the HUD
  rental-subsidy literature review; DiPasquale-Wheaton 1996 give ~0.78 for 25–34s,
  above this band). The dividend's renters are bottom-decile-concentrated, so the
  low-income demand range is the correct one.
- `eps_s` = local housing **supply** elasticity from **Saiz (2010), QJE**, swept
  **0.60 / 1.75 / 2.45**: population-weighted US average 1.75, avg-regulated-metro
  IQR 1.25–2.45, constrained metros <1.0 (Chicago), severely land-constrained
  lower.

The sweep reports the central case (εd 0.40, εs 1.75), the full corner-to-corner
range, and the worst corner. The constrained-vs-elastic ordering matches the
independent finding (Hilber; Howard-style) that housing subsidies in inelastic
areas are absorbed into rents while elastic areas absorb them into units.

## Caveats (do not drop these)
- **First-round, partial equilibrium.** No migration, no dividend-induced
  household formation, no multi-year supply response. Each of those generally
  pushes the long-run leak *below* the first-round figure, so the central ~2% is
  closer to an upper bound on the steady leak than a point prediction.
- **Both elasticities are now swept** across their cited literature ranges, so the
  result is reported as a band rather than a point; the conclusion holds across
  the entire grid. The one remaining single assumption is the *form* of the
  incidence relation (capture = εd/(εd+εs)), the standard partial-equilibrium
  result.
- **Per-person proxy.** Adults = 2-if-married is the channels.py convention, not
  a household roster; fine for incidence shares, approximate at the margin.

## Credit
The mechanism modeled here -- renters concentrated at the bottom of the
distribution, so a flat cash dividend's largest first-round flow lands on the
most supply-inelastic good (housing) before any landlord reprices -- is from
**wilsoniumite** (wilsoniumite.com, "Labor pressures causing market distortion
and a minimally invasive solution," 2026-06-14), where it is found on Finnish
HBS and US CE consumption microdata. This module reproduces the qualitative
finding independently on US SCF wealth microdata with the Citizens Standard
per-person dividend, and is the empirical basis for pairing the dividend with a
land-value tax sized to intercept the capitalized slice.

## Reproduce
```
cd code
python3 stage1_rent_exposure.py     # Stage 1 exposure table
python3 stage2_capitalization.py    # Stage 2 grounded capitalization
```

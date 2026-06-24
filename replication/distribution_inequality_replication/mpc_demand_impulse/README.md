# Demand Impulse of the Dividend Lane (MPC Gradient)

Does the cash dividend lane create **net new consumption demand** (demand-side
inflation pressure), and how much? This is the demand-side counterpart to the
rent-capitalization module, and the empirical answer to the recurring "won't
handing out cash be inflationary?" objection.

## Result (headline)

The demand impulse is **small in every scenario** (always under 0.5% of US
consumption in magnitude), but its **sign depends on what growth-matched issuance
displaces** -- a conceptual fork, not a calibration choice:

| MPC schedule | A: credit displacement (MPC~1.0) | B: broad-money displacement | C: flat avg (0.55) |
|---|---|---|---|
| low  | -0.52% | +0.17% | +0.07% |
| central | **-0.42%** | **+0.22%** | +0.17% |
| high | -0.28% | +0.15% | +0.31% |

- **Central estimate: +0.22% of consumption** (central MPC schedule, broad-money displacement).
- **Full range: -0.52% to +0.31%** of US consumption (PCE ~$17.5T).

**Interpretation.** If growth-matched issuance *replaces money that banks would
otherwise create through lending* (the full-reserve story), it displaces ~MPC-1.0
borrowers and the dividend is **neutral-to-mildly-disinflationary**. If it
displaces *broadly-held existing money* (concentrated at the top, low MPC), the
dividend shifts spending power toward higher-MPC households and is **mildly
inflationary (~+0.2%)**. Either way the magnitude is central-bank-trivial. The
displacement question is the same full-reserve / double-claim issue under debate,
so the honest claim is: **bounded and small, central ~+0.2%, sign contested.**

This brackets Wilson's VAT-UBI demand impulse (+0.3 to +0.5%); his is purely
positive because his VAT is explicitly redistributive (savers -> spenders),
whereas growth-matched issuance carries the extra credit-displacement channel
that can flip the sign -- a genuine difference between the two designs.

## Method

### Stage 1 (`code/stage1_mpc_impulse.py`)
Builds the MPC gradient from SCF 2022 and computes the impulse for the central
case. Net impulse = (recipient MPC-weighted spend) - (baseline MPC x dividend).

### Stage 2 (`code/stage2_impulse_sweep.py`)
Full sweep over **two axes**:
- **MPC schedule** (low / central / high) across the literature band: top-decile
  MPC 0.40-0.65, bottom pinned near 1.0 (hand-to-mouth). Sources:
  Fagereng-Holm-Natvik (2021, first-year MPC ~0.5 declining in liquid assets),
  Jappelli-Pistaferri (2014, MPC gradient in cash-on-hand), Kaplan-Violante-
  Weidner (2014, ~1/3 hand-to-mouth).
- **Displacement scenario** (A credit / B broad-money / C flat) for the baseline
  MPC of the money the dividend displaces. Baseline B (income-weighted MPC) and
  the neutral point (recipient-weighted MPC = 0.682) are *computed from the data*,
  not assumed.

## Verification
- Weight baseline guarded by assertion (sum WGT = 131,306,389); parent module's
  `verify_scf.py` reproduces published SCF figures.
- **Hand-to-mouth share computed at 30.0%**, matching Kaplan-Violante-Weidner's
  ~1/3 benchmark -- an independent check that the SCF liquidity gradient (used to
  shape the MPC schedule) is being read correctly. HtM share falls monotonically
  from 44% (bottom decile) to 11% (top), median liquid assets rise $600 ->
  $280,000, exactly the canonical MPC-heterogeneity structure.
- Dividend total reconciles to the verified v3_10 Mode D figure ($230B to Mᵀ).
- Per-person shares use the channels.py convention (adults = 2 if married,
  child = 0.3).

## Caveats
- **Impact-period, partial equilibrium.** First-round spending, no multiplier, no
  monetary-policy offset. The text notes the offset is central-bank-trivial.
- **The MPC schedule is shaped by the liquidity gradient, not estimated
  household-by-household.** The literature band is swept; the *shape* (declining in
  income) is the robust feature.
- **The displacement scenario is the load-bearing judgment**, and it is left
  explicitly as a fork rather than resolved, because resolving it is the contested
  full-reserve question -- not something this module can settle.

## Credit
The MPC-asymmetry demand-impulse framing (moving money toward higher-MPC
households adds net consumption demand; the effect is small and bounded) follows
**wilsoniumite** (wilsoniumite.com, 2026-06-14), who models it on Finnish/US
consumption microdata. This module computes the analogue for the Citizens
Standard dividend on US SCF data, and adds the credit-displacement channel
specific to issuance (vs. VAT) funding, which is what allows the sign to flip.

## Reproduce
```
cd code
python3 stage1_mpc_impulse.py
python3 stage2_impulse_sweep.py
```

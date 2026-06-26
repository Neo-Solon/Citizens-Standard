# Two-Circuit New Keynesian DSGE

Writes the Citizens Standard two-circuit system in the standard macro language so its
central claims can be evaluated and attacked on those terms. Calibrated to **textbook
values** (Gali 2015 / Smets-Wouters), not to flatter.

## What it tests

- **C1 Determinacy (rigorous).** Does the growth-matched issuance rule yield a unique
  stable rational-expectations equilibrium? Solved by the standard Blanchard-Kahn
  eigenvalue count on the micro-founded forward-looking block.
- **C2 Price stability (validated mapping).** How large is the inflation/price response
  to an issuance shock as a function of floor-weighting (kappa_d) and the asset->goods
  leak (lambda)?

## Results

**C1: determinacy without a Taylor principle — reproduced.** The Citizens Standard
does *not* use an interest-rate rule; its anchor is a quantity/price-path rule (KI
sets transactional money so the price level tracks a target path). With the standard
forward-looking Cagan money-demand block, the explosive root is theta = 1 + (1+phi)/alpha,
which exceeds 1 for *every* money-demand semi-elasticity alpha>0 and *every* gap
response phi>=0 — so the price level is determinate even with a passive gap response.
This reproduces Paper 5's "determinacy without a Taylor principle": the money-supply
anchor pins the level each period, where an interest-rate rule would need phi>1 (the
Fisherian root). The two-jump-variable system (price level + asset circuit) is
determinate at low asset<->consumer coupling and loses determinacy as coupling grows;
the module shows this direction qualitatively but does **not** reproduce the paper's
exact ~0.13 threshold (that needs the paper's full two-block specification, Appendix
A.12) and is not tuned to it.

**C2: price stability — regime-dependent, validated against the quantity-theoretic
limit.** Price impulse of a 1pp-of-M2 issuance shock:

| kappa_d \ leak | 0.03 | 0.10 | 0.20 |
|---|---|---|---|
| 0.0 (floor-max) | 0.10% | 0.33% | 0.67% |
| 0.4 | 1.39% | 1.53% | 1.73% |
| 1.0 (pure dividend) | 3.33% | 3.33% | 3.33% |

Floor-weighting keeps the impulse small (conditional on low leak); a large cash
dividend is not price-neutral (3.33%); the leak is the load-bearing parameter.

## The honest headline: convergence

Three independent methods — the analytic propositions (Paper 5), the data-grounded
`credit_displacement` module, and this DSGE — locate the **same boundary**:
floor-weighting plus circuit separation give price stability; a large dividend or a
high leak break it. Agreement across methods is stronger than any one alone.

## Method and scope

- **The rigorous content is the determinacy result** theta = 1+(1+phi)/alpha > 1,
  which reproduces Paper 5's "determinacy without a Taylor principle" on the
  framework's price-level-anchor rule. The Citizens Standard uses a quantity/price-path
  rule, not a Taylor-type interest-rate rule; the determinacy is supplied by the
  money-supply anchor pinning the price level each period, where an interest-rate rule
  would require phi_pi>1.
- **The exact coupling threshold (~0.13) is not reproduced** by the stylized 2x2 here
  and is not tuned to it; only the qualitative direction (determinacy lost as coupling
  grows) is shown. The exact value comes from the paper's full two-block system.
- **C2 is the model's validated long-run quantity-theoretic property** (price level
  pinned by transactional money), not a full short-run perturbation IRF. A validation
  gate checks the pure-dividend limit against the quantity-theoretic benchmark
  S / (M^T/M2); it is in the code and must pass or the grid is not reported.
- Calibration is textbook throughout; the leak is swept from the framework bound (0.03)
  to 0.20; nothing is tuned to produce a result.

## Reproduce
```
cd code
python3 stage1_determinacy.py
python3 stage2_price_response.py   # includes the validation gate
```

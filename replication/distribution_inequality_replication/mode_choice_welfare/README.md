# mode_choice_welfare — backs Paper 1 §13.3 (Mode Selection as Constitutional Choice)

Tests whether a welfare-optimal Mode (optimal dividend/floor split κ_d) exists. Paper 1 §13.3
holds that Mode choice is a values question, not a technical optimization. This module shows
that quantitatively: the social-welfare function is **monotonic in κ_d**, so the formal
optimum is bang-bang (a corner, or the inflation ceiling), never an interior point. There is
no welfare-optimal Mode to compute — which is the formal basis for assigning the choice to a
supermajority vote.

Run: `python3 code/stage1_no_welfare_optimum.py`

## Inputs (verified / cited)
- Realizable return by configuration, from the architecture model: 5.4% at the floor-only
  split (κ_d=0, Modes A/C), 4.3% at Mode B's 60/40 (κ_d=0.4). Linear within [0,0.4]:
  r_e(κ_d) = 0.054 − 0.0275·κ_d. Raising κ_d lowers both the locked share and its return.
- MPC schedule by decile — the Model's own, literature-keyed (Fagereng-Holm-Natvik first-year
  MPC ~0.5; Kaplan-Violante-Weidner ~1/3 hand-to-mouth).
- Liquidity-constrained share ~0.37 (Federal Reserve SHED 2024: 37% of adults could not cover
  a $400 emergency with cash). Discount rates and horizon swept.

## Method and finding
Per $1 of issuance at split κ_d, a household consumes its MPC of the spendable part now and
reinvests the rest; the locked part compounds at r_e(κ_d) and is discounted at the household's
rate. Social welfare sums over deciles with marginal-utility weights higher for the
liquidity-constrained. Maximizing over κ_d yields a corner solution that tracks the cap
(0.6→0.8→1.0 as the cap is raised) — confirming the welfare function has no interior maximum.

## What the result means
- The dial trades **immediate liquidity** (a larger spendable dividend) against **compounding
  ownership** (a larger locked stake earning a higher return), bounded above by the inflation
  ceiling. Neither side dominates on welfare grounds.
- Because no Mode is welfare-optimal, the choice is a constitutional values decision (Paper 1
  §13.3), properly left to a supermajority vote rather than a technocratic calculation.
- Decision support for that vote, not an optimum: a polity wanting the dividend to reach those
  who cannot self-insure can set κ_d near its liquidity-constrained share (~0.37 nationally;
  Mode B's 0.40 sits near it), and may favor a Mode whose κ_d rises countercyclically.

## Scope
This module establishes a null result (no interior optimum). It deliberately does not assert a
unique optimal split; a sharper optimum would require within-group diminishing-marginal-utility
assumptions that available data do not pin down.

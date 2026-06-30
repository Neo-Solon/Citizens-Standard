# Demurrage backstop for Mode A (Paper 1, Section 4.5)

Empirically-grounded analysis of demurrage as a conditional velocity stabilizer for
the deflation-targeting Mode A. Supports Section 4.5 of the Architecture paper.

Run:
    python3 code/demurrage_modeA.py     # full model: problem, offset, leakage, design
    python3 code/demurrage_verify.py    # expectations channel + trigger reconciliation
    python3 code/demurrage_verify2.py   # external validation + sensitivity + neutrality

## Result
Mild productivity deflation (Mode A's ~1.9%) is benign: velocity falls ~1%, no
intervention needed (Atkeson-Kehoe 2004; Bordo-Landon-Lane-Redish 2004). The hoarding
risk is the tail where deflation expectations un-anchor or a confidence shock hits
(the 1930s dynamic, driven by risk premia/uncertainty, not the price decline). For
that tail, KI cannot help (issuing money would destroy the deflation target), so a
demurrage backstop is the fitting tool: a small carrying charge (~2%, far below the
8-12% historical scrips) on transactional balances only (Floors exempt), revenue
recycled equally per capita (price path preserved, net-neutral).

## Verified
- Reproduces the historical benign-vs-spiral split with one money-demand elasticity.
- Robust across the elasticity range 0.3-0.6 (Lucas 2000; Benati et al. 2021).
- Leakage ceiling grounded at the transactional liquidity premium ~2-4% national
  scale (Keynes' evasion objection); the ~2% Mode-A offset sits inside it.
- Revenue-neutral by construction.

## Honest residuals
- The model characterizes demurrage's RESPONSE to a velocity collapse, not the origin
  of the collapse (the confidence shock is an exogenous input).
- In a deep expectations spiral the needed offset (~5%) exceeds the leakage ceiling,
  so demurrage is a partial damper there, not a standalone clamp.

## Sources
Atkeson & Kehoe 2004 (AER 94(2)); Bordo, Landon-Lane & Redish 2004 (NBER 10329);
Lucas 2000 (Econometrica 68(2)); Benati, Lucas, Nicolini & Weber 2021 (JME 117);
Anderson, Bordo & Duca 2016 (NBER 22100, velocity in crises); Worgl 1932 and
Chiemgauer demurrage experiments.

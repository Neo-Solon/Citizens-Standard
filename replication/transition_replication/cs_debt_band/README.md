# CS Debt Band -- validated stochastic DSA and the band recommendation

This package contains the full, verified analysis behind the CS debt-policy
revision: from "retire to a 15% floor" to "hold a moderate ~30-60% band."

Read CS_Debt_Band_Design_Note.md first. It is the complete write-up with the
result, the four grounded links, the verification tables, the empirical
safe-haven grounding, the recommendation, and an honest residuals ledger.

## What is validated
A compound-jump stochastic process for the interest-growth differential (r-g),
calibrated to and reproducing SIX published moments + one held-out moment, stable
across seeds at N=12,000. Parameters in dsa_locked.json. Sources: Blanchard 2019,
Mauro-Zhou 2020, Lian et al. 2020, Krishnamurthy-Vissing-Jorgensen 2012 (+ StL Fed
2025), De Grauwe 2011.

## Layout
- CS_Debt_Band_Design_Note.md  -- the write-up (start here)
- dsa_locked.json              -- locked, validated process parameters
- code/                        -- all runnable modules (reproducible from inputs)
- output/                      -- saved outputs of the key runs
- verification/                -- the diagnostic scripts (horizon + calm-persistence)
                                  that established WHY the Gaussian family failed

## Reproduce
  python3 code/dsa_jump_verify.py        # verify the process (all moments, 2 seeds)
  python3 code/cs_band_verify_final.py   # verify the band at grounded damping

## Honest status
- All six calibration moments + held-out reproduced and seed-stable.
- One anchor (median r-g @40%) is ~0.15pp shy, in the conservative direction.
- The low-debt reversal frequency is matchable only by the jump model class; this
  was a finding (five Gaussian fixes failed at high N), documented in the note.
- The band optimum is a SHALLOW maximum -> the deliverable is a moderate RANGE
  (~30-60%), robust across the safe-haven damping, not a single point.

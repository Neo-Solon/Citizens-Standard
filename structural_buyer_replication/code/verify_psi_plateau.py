# Paper 8 (2026h) Appendix A.6 — numerical verification of psi* = c*dur
# Confirms both decumulation models, consistency with calibration, the limit, and growth sensitivity.
import numpy as np
c, dur = 0.008, 30
# Model 1: constant hazard 1/dur
S=0.0
for _ in range(2000): S=S*(1-1/dur)+c
assert abs(S-c*dur)<1e-3, S
# Model 2: fixed-duration cohort
assert abs(sum(c for _ in range(dur))-c*dur)<1e-9
# base & high-deposit
assert abs(c*dur-0.24)<5e-3
assert abs(0.015*30-0.45)<5e-3
# growth sensitivity (value-share interpretation): psi* = c*annuity(g,dur) <= c*dur
for g in (0.0,0.02,0.05):
    ann = dur if g==0 else (1-(1+g)**(-dur))/g
    assert c*ann <= c*dur + 1e-12
print("Appendix A.6 verification PASSED: psi* = c*dur (both models); base=0.24, high=0.45; conservative under growth.")

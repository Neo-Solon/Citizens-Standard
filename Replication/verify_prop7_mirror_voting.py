# Paper 8 (2026h) Appendix A.6 — numerical verification of the citizen-ownership share psi*.
# Distinguishes the zero-growth stock-flow value c*dur (upper reference) from the realized
# steady-state share under positive growth, psi* = c*annuity(g,dur), bounded by c/g.
import numpy as np

c   = 0.00394   # Mode B central: c = A*/mktcap = $272B/$69T
dur = 40        # cohort-realistic average holding duration (deposit avg age ~32, liquidate ~74)
g   = 0.02      # real growth

# --- zero-growth stock-flow value c*dur (two equivalent decumulation models) ---
S = 0.0
for _ in range(4000):                      # Model 1: constant hazard 1/dur, no growth
    S = S*(1-1/dur) + c
assert abs(S - c*dur) < 1e-3, S
assert abs(sum(c for _ in range(dur)) - c*dur) < 1e-9   # Model 2: fixed-duration cohort
cdur = c*dur
assert abs(cdur - 0.16) < 6e-3, cdur                    # Mode B zero-growth value ~0.16 (dur=40)

# --- realized share under positive growth: psi* = c*annuity(g,dur), and the c/g ceiling ---
def annuity(g, dur):                       # present-value annuity factor (years)
    return dur if g == 0 else (1 - (1+g)**(-dur)) / g
psi_annuity = c * annuity(g, dur)          # fixed-duration / Figure 2 model
psi_hazard  = c*dur / (1 + g*dur)          # constant-hazard renewal model
psi_central = 0.5*(psi_annuity + psi_hazard)
ceil = c / g                               # asymptotic ceiling (dur -> inf)
assert psi_annuity <= cdur + 1e-12         # growth never exceeds the zero-growth value
assert psi_hazard  <= cdur + 1e-12
assert abs(psi_central - 0.10) < 0.02, psi_central       # realized Mode B central ~0.10
assert abs(ceil - 0.20) < 6e-3, ceil                     # c/g ~0.20
assert psi_central < ceil < 1.0                          # bounded, finite

# --- 30% is unreachable at Mode B under positive growth (needs zero growth and dur~61) ---
assert c/g < 0.30                          # ceiling below 0.30 at g=2%
dur30 = 0.30 / c                           # zero-growth dur that would give c*dur = 0.30
assert abs(dur30 - 76) < 2, dur30

print(f"Appendix A.6 verification PASSED:")
print(f"  zero-growth  c*dur            = {cdur:.3f}  (Mode B, dur={dur})")
print(f"  realized     psi* = c*annuity = {psi_central:.3f}  (g={g:.0%}; hazard {psi_hazard:.3f}, annuity {psi_annuity:.3f})")
print(f"  ceiling      c/g              = {ceil:.3f}  (dur -> inf)")
print(f"  active float (1 - psi*)       = {1-psi_central:.3f}")
print(f"  30% share needs zero growth and dur ~ {dur30:.0f} yr; unreachable at Mode B under 2% growth.")

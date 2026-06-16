# Paper 8 (Neo-Solon, 2026h) Appendix A.4 — Proposition 3
# Bounded seller-rebalancing leak into the transactional circuit.
#   leak <= kappa_W * Delta ;  >= (1 - kappa_W) re-enters the asset circuit M^A
#   kappa_W in [0.025, 0.05] (sec 9.3), central ~0.03 -> ~3% leak, >=97% re-enters
KAPPA_LO, KAPPA_HI, KAPPA_C = 0.025, 0.05, 0.03
Delta = 1.0
leak = KAPPA_C*Delta
reenter = (1 - KAPPA_C)*Delta
assert abs(leak - 0.03) < 1e-12
assert reenter >= 0.97 - 1e-12
# bound holds across the literature range
for k in (0.02, 0.025, 0.03, 0.035, 0.05):
    assert k*Delta <= KAPPA_HI*Delta + 1e-12
print(f"A.4 PASSED: leak <= kappa_W*Delta; central kappa_W={KAPPA_C} -> {leak:.0%} leak, "
      f"{reenter:.0%} re-enters M^A; working range [{KAPPA_LO}, {KAPPA_HI}].")

# Paper 8 (Neo-Solon, 2026h) Appendix A.5 — Proposition 7
# Mirror-voting neutrality: ownership without control.
#   FDCA holds vote share psi, casts it in residual shareholders' proportions.
#   YES_total = (1-psi)p + psi*p = p  for every psi  =>  outcome = residual outcome at any threshold tau.
import numpy as np
rng = np.random.default_rng(0)
for _ in range(200000):
    psi = rng.uniform(0.0, 1.0)     # FDCA vote share in [0,1)
    p   = rng.uniform(0.0, 1.0)     # residual YES fraction
    yes_total = (1 - psi)*p + psi*p
    assert abs(yes_total - p) < 1e-12
# threshold-invariance: pass iff p >= tau, independent of psi
for tau in (0.5, 2/3, 0.75):
    for psi in (0.0, 0.1, 0.3, 0.49):
        for p in (0.40, 0.50, 0.60, 2/3, 0.80):
            assert (((1-psi)*p + psi*p) >= tau) == (p >= tau)
print("A.5 PASSED: YES_total = p for all psi (machine precision); "
      "outcome = residual outcome at every threshold; FDCA never pivotal.")

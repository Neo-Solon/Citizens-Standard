# Paper 8 (Neo-Solon, 2026h) Appendix A.2 — Proposition 1
# Bounded valuation fixed point and stability band.
#   Q_{t+1} = (1 - theta*phi) Q_t + theta(A* + phi*Q_baseline)
#   premium Q* - Q_baseline = A*/phi (finite for all finite A*, phi>0)
#   converges iff 0 < theta*phi < 2
# Illustrative calibration (the paper's magnitudes are illustrations, not calibrations).
import numpy as np

def fixed_point(A, phi, theta, Qb=1.0, T=200000):
    Q = Qb
    for _ in range(T):
        Q = (1 - theta*phi)*Q + theta*(A + phi*Qb)
    return Q

A, phi, theta, Qb = 0.45, 0.5, 1.0, 1.0          # A* in $T/yr-equivalent flow units
prem_closed = A/phi
prem_sim = fixed_point(A, phi, theta, Qb) - Qb
assert abs(prem_sim - prem_closed) < 1e-9, (prem_sim, prem_closed)

# Stability band: |1 - theta*phi| < 1  <=>  0 < theta*phi < 2
conv = lambda tp: abs(1 - tp) < 1
for tp in (0.5, 1.0, 1.5):
    assert conv(tp), tp
assert not conv(2.5)

# Premium strictly decreasing in phi:  d/dphi (A/phi) = -A/phi^2 < 0
phis = np.array([0.25, 0.5, 1.0, 2.0])
assert np.all(np.diff(A/phis) < 0)

print(f"A.2 PASSED: premium = A*/phi = {prem_closed:.4f} (sim {prem_sim:.4f}); "
      f"stable for theta*phi in (0,2), divergent at 2.5; premium decreasing in phi.")

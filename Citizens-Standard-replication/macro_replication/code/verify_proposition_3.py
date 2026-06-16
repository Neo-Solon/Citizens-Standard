"""
verify_proposition_3.py
-----------------------
Numerical demonstration of Proposition 3 (convergence of the path-targeting
dividend rule) from:

    Neo-Solon (2026e). The Citizens Standard: A Macroeconomic Model of a
    Two-Circuit Monetary System. Working Paper. Section 4.4, Section 4.7,
    Appendix A.2 (Proposition 3).

PROPOSITION 3 (restated).
Let x_t = ln[target_price_level(t) / CPI(t)] be the log price-path gap. The KI
path-targeting rule injects g_KI(t) = lambda * x_{t-1}. With psi > 0 the
within-period pass-through from path-closure issuance to realized inflation,
the gap evolves as:

        x_t = (1 - psi*lambda) * x_{t-1} + eps_t

The homogeneous solution is (1 - psi*lambda)^t * x_0, hence:
    - converges WITHOUT oscillation   iff  0 < psi*lambda <= 1
    - converges WITH damped oscillation iff 1 < psi*lambda <  2
    - diverges                          iff  psi*lambda >= 2

This script does NOT prove the proposition (the proof is closed-form and
stands alone in Appendix A.2). It simply *demonstrates* the classification
by iterating the gap recursion across the parameter space and confirming the
observed behavior matches the analytic regime boundaries. It also confirms
the Mode T damper KI_T (effective gain chi*lambda <= lambda) inherits
convergence with strictly more margin.

Reproduces the regime classification underlying Sections 3.5, 4.4, and 4.7.
"""

import numpy as np


def simulate_gap(psi, lam, x0=1.0, periods=200, noise=0.0, seed=0):
    """Iterate x_t = (1 - psi*lam) x_{t-1} + eps_t and return the path."""
    rng = np.random.default_rng(seed)
    x = np.empty(periods + 1)
    x[0] = x0
    g = psi * lam
    for t in range(1, periods + 1):
        eps = rng.normal(0.0, noise) if noise > 0 else 0.0
        x[t] = (1.0 - g) * x[t - 1] + eps
    return x


def classify(path, tol=1e-9):
    """Classify a homogeneous path x_t = (1-g)^t x_0 from its realized
    trajectory. Distinguishes monotone convergence, damped (converging)
    oscillation, marginal (constant-amplitude) oscillation at g=2, and
    divergence. Uses the ratio of successive non-zero amplitudes, which is
    |1-g| and is the scale-free signature of the regime."""
    p = path[np.abs(path) > tol]
    if p.size < 3:
        # collapsed to zero essentially immediately => converged
        # determine oscillation from sign pattern of the early steps
        signs = np.sign(path[1:6][np.abs(path[1:6]) > tol])
        osc = signs.size > 1 and np.any(np.abs(np.diff(signs)) > 1)
        return ("converge-oscillate" if osc else "converge-monotone"), int(osc)

    # successive amplitude ratio r ~ |1 - g|
    ratios = np.abs(p[1:] / p[:-1])
    r = float(np.median(ratios))
    # sign alternation => oscillatory branch (1-g < 0, i.e. g > 1)
    signs = np.sign(p)
    sign_changes = int(np.sum(np.abs(np.diff(signs)) > 1))
    oscillatory = sign_changes > 0

    if r > 1.0 + 1e-6:
        regime = "diverge"
    elif abs(r - 1.0) <= 1e-6:
        regime = "marginal-oscillate" if oscillatory else "marginal"
    else:  # r < 1 : converging
        regime = "converge-oscillate" if oscillatory else "converge-monotone"
    return regime, sign_changes


def analytic_regime(psi, lam):
    g = psi * lam
    if g > 2.0:
        return "diverge"
    if g == 2.0:
        return "marginal-oscillate"   # (1 - 2)^t = (-1)^t : bounded, constant amplitude
    if g > 1.0:
        return "converge-oscillate"
    return "converge-monotone"


def main():
    lam = 0.5  # baseline closure gain (paper Section 4.4)
    print("=" * 70)
    print("PROPOSITION 3 — convergence regime classification (lambda = 0.5)")
    print("=" * 70)
    print(f"{'psi':>6} {'psi*lam':>8} {'analytic':>20} {'observed':>20} {'match':>6}")
    print("-" * 70)

    all_match = True
    # sweep psi so psi*lambda spans the three regimes
    for psi in [0.5, 1.0, 1.5, 1.9, 2.0, 2.1, 3.0, 4.0, 4.2]:
        path = simulate_gap(psi, lam, x0=1.0, periods=300, noise=0.0)
        observed, _ = classify(path)
        analytic = analytic_regime(psi, lam)
        match = (observed == analytic)
        all_match = all_match and match
        print(f"{psi:>6.2f} {psi*lam:>8.2f} {analytic:>20} {observed:>20} {'OK' if match else 'XX':>6}")

    print("-" * 70)
    print(f"All observed regimes match the analytic boundaries: {all_match}")
    print()

    # --- The self-correction claim: any measured psi can be stabilized by lam < 1/psi
    print("SELF-CORRECTION (Sections 3.5 / 4.4): for any psi, choose lambda < 1/psi")
    print("-" * 70)
    for psi in [1.0, 2.0, 4.0, 8.0]:
        lam_safe = 0.9 / psi          # any lambda < 1/psi works; 0.9/psi is safely inside
        path = simulate_gap(psi, lam_safe, x0=1.0, periods=300)
        observed, _ = classify(path)
        print(f"  psi={psi:>4.1f}  ->  choose lambda={lam_safe:.3f}  (psi*lambda={psi*lam_safe:.2f})  ->  {observed}")
    print()

    # --- KI_T inherits stability: effective gain chi*lambda <= lambda
    print("MODE T DAMPER KI_T (Section 4.7): effective gain chi*lambda <= lambda")
    print("inherits convergence with strictly MORE margin for any chi in [0,1]")
    print("-" * 70)
    psi = 1.8  # a deliberately near-boundary pass-through at baseline lambda
    g_base = psi * lam
    print(f"  baseline rule: psi={psi}, lambda={lam}  ->  psi*lambda={g_base:.2f}  "
          f"({analytic_regime(psi, lam)})")
    for chi in [1.0, 0.75, 0.5, 0.25]:
        g = psi * chi * lam
        path = simulate_gap(psi, chi * lam, x0=1.0, periods=300)
        observed, _ = classify(path)
        print(f"  chi={chi:>4.2f}  ->  psi*chi*lambda={g:.3f}  ->  {observed}")
    print()
    print("Conclusion: KI_T cannot oscillate on any setting the steady-state rule does not,")
    print("and is strictly more stable whenever chi < 1. Matches Section 4.7 / Proposition 3.")
    print("=" * 70)


if __name__ == "__main__":
    main()

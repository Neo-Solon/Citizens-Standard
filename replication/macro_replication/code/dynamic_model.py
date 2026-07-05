"""
dynamic_model.py
================
Calibrated (not estimated) dynamic model for the Citizens Standard, simulating
the linearized system that Paper 5 writes down in Appendix A.9:

    s_t = A s_{t-1} + e_t,   s = (x, y_tilde, v)'   [price gap, output gap, asset gap]

    A = [[1 - psi*lam,  kappa,   lambda_leak],
         [-gamma,       phi_y,   0          ],
         [0,            0,       phi_v      ]]

This is a *calibrated* exercise: parameters are set from Paper 5's baseline and
the sourced literature, NOT estimated on data. Estimation is deliberately avoided
because the Citizens Standard has never operated -- fitting the system to
fractional-reserve data and assuming the parameters carry over is exactly the
Lucas critique. What a calibrated model CAN show, and what the static propositions
cannot, is that the results survive general-equilibrium dynamics: the price path
is determinate, the two circuits stay separated, and shocks are contained -- across
the admissible parameter space, not just at one baseline.

Three exercises:
  1. VALIDATION      -- reproduce Paper 5's stated baseline eigenvalues (0.12, 0.68, 0.90).
  2. IMPULSE RESPONSES -- report the numeric IRFs to price, demand, and asset shocks.
  3. DYNAMIC ROBUSTNESS -- randomized draws over admissible parameters; confirm
                          stability and bounded asset->price pass-through hold, and
                          report the pass rate for the determinacy/separation region.

Run:  python3 dynamic_model.py
"""

import random
import numpy as np

# ---------------------------------------------------------------------------
# Paper 5 baseline calibration (Appendix A.5 / A.9)
# ---------------------------------------------------------------------------
PSI_LAM   = 0.90   # path-targeting feedback root component (1 - psi*lam is the price-gap own-root)
KAPPA     = 0.08   # output-gap push into the price gap
GAMMA     = 0.15   # price-gap cooling of the output gap
PHI_Y     = 0.70   # output-gap persistence
PHI_V     = 0.90   # asset-valuation-gap persistence
LAMBDA_LEAK = 0.03 # structural asset -> consumer-price leak
OMEGA_F   = 0.15   # acyclical floor-income share (cushions demand shocks)


def A_matrix(psi_lam=PSI_LAM, kappa=KAPPA, gamma=GAMMA, phi_y=PHI_Y,
             phi_v=PHI_V, leak=LAMBDA_LEAK):
    """The linearized transition matrix from Paper 5 A.9."""
    return np.array([
        [1.0 - psi_lam, kappa,  leak ],
        [-gamma,        phi_y,  0.0  ],
        [0.0,           0.0,    phi_v],
    ])


def eigenvalues(**kw):
    return sorted(np.abs(np.linalg.eigvals(A_matrix(**kw))))


def impulse_response(shock, T=24, omega_f=OMEGA_F, **kw):
    """Simulate s_t = A s_{t-1} for a unit shock at t=0.
    shock: dict with any of 'pi' (price), 'y' (demand), 'v' (asset)."""
    A = A_matrix(**kw)
    s = np.array([
        shock.get("pi", 0.0),
        (1.0 - omega_f) * shock.get("y", 0.0),   # floor cushions demand shocks
        shock.get("v", 0.0),
    ])
    path = [s.copy()]
    for _ in range(T):
        s = A @ s
        path.append(s.copy())
    return np.array(path)   # shape (T+1, 3): columns are (x, y_tilde, v)


# ---------------------------------------------------------------------------
# 1. VALIDATION against Paper 5's stated eigenvalues
# ---------------------------------------------------------------------------
def validation():
    ev = eigenvalues()
    stated = [0.12, 0.68, 0.90]
    match = all(abs(a - b) < 0.02 for a, b in zip(ev, stated))
    print("1. VALIDATION (reproduce Paper 5 A.9 baseline eigenvalues)")
    print(f"   computed |eigenvalues| = {[round(float(e),2) for e in ev]}")
    print(f"   paper states           = {stated}")
    print(f"   -> {'MATCH' if match else 'MISMATCH'}; system stable (all < 1): {all(e < 1 for e in ev)}")
    return match


# ---------------------------------------------------------------------------
# 2. IMPULSE RESPONSES (numeric, not just a figure)
# ---------------------------------------------------------------------------
def impulse_responses():
    print("2. IMPULSE RESPONSES (unit shock; peak and half-life of the price gap x)")
    scenarios = [
        ("price shock e_pi",  {"pi": 1.0}),
        ("demand shock e_y",  {"y": 1.0}),
        ("asset shock e_v",   {"v": 1.0}),
    ]
    for name, shk in scenarios:
        irf = impulse_response(shk, T=40)
        x = irf[:, 0]                       # price-gap path
        peak = x[np.argmax(np.abs(x))]
        # half-life: first t where |x| falls below half its peak magnitude
        pk = np.abs(peak)
        hl = next((t for t in range(len(x)) if abs(x[t]) <= pk / 2 and t > 0), None)
        # steady-state pass-through for the asset shock: bounded by leak/(psi*lam)
        ss = x[-1]
        print(f"   {name:<18} price-gap peak = {peak:+.3f}, "
              f"half-life = {hl if hl is not None else '>40'}y, settles -> {ss:+.4f}")
    # the key separation result: asset shock reaches prices only through the leak
    irf_v = impulse_response({"v": 1.0}, T=200)
    peak_x_from_v = np.max(np.abs(irf_v[:, 0]))
    bound = LAMBDA_LEAK / PSI_LAM
    print(f"   asset->price pass-through: peak |x| from a unit asset shock = "
          f"{peak_x_from_v:.4f}  (bound leak/psi*lam = {bound:.4f})")
    return peak_x_from_v <= bound + 1e-6


# ---------------------------------------------------------------------------
# 3. DYNAMIC ROBUSTNESS (randomized over admissible parameters)
# ---------------------------------------------------------------------------
def admissible(rng):
    return dict(
        psi_lam=rng.uniform(0.60, 0.98),   # feedback strength (stable region)
        kappa=rng.uniform(0.0, 0.20),      # output->price push
        gamma=rng.uniform(0.0, 0.40),      # price->output cooling
        phi_y=rng.uniform(0.40, 0.90),     # output persistence
        phi_v=rng.uniform(0.70, 0.98),     # asset persistence
        leak=rng.uniform(0.01, 0.08),      # structural leak
    )


def dynamic_robustness(n=10000, seed=20260705):
    rng = random.Random(seed)
    stable = 0            # all |eigenvalues| < 1 (determinate, non-explosive)
    separated = 0         # asset->price pass-through bounded (circuits stay separate)
    both = 0
    for _ in range(n):
        p = admissible(rng)
        ev = eigenvalues(**p)
        is_stable = all(e < 1.0 - 1e-12 for e in ev)
        # asset->price steady-state pass-through bound: leak/(psi*lam) should stay small
        passthrough = p["leak"] / p["psi_lam"]
        is_separated = passthrough < 0.13         # below the coupling threshold zeta*
        stable += is_stable
        separated += is_separated
        both += (is_stable and is_separated)
    print(f"3. DYNAMIC ROBUSTNESS ({n:,} admissible calibrations, seed {seed})")
    print(f"   stable (determinate, all eig < 1):        {stable:>6}/{n} ({stable/n:.1%})")
    print(f"   circuits separated (pass-through < zeta*): {separated:>6}/{n} ({separated/n:.1%})")
    print(f"   both simultaneously:                       {both:>6}/{n} ({both/n:.1%})")
    return stable, separated, both, n


if __name__ == "__main__":
    print("=" * 70)
    print("CITIZENS STANDARD -- CALIBRATED DYNAMIC MODEL (Paper 5 A.9)")
    print("  calibrated, not estimated (see module docstring for why).")
    print("=" * 70)
    v_ok = validation()
    print()
    sep_ok = impulse_responses()
    print()
    stable, separated, both, n = dynamic_robustness()
    print("=" * 70)
    print(f"validation {'OK' if v_ok else 'FAILED'}; "
          f"baseline separation {'bounded' if sep_ok else 'UNBOUNDED'}; "
          f"stability holds in {stable}/{n} admissible draws.")
    import sys
    sys.exit(0 if (v_ok and sep_ok) else 1)

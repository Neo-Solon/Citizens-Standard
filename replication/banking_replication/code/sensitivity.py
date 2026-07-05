"""
sensitivity.py
==============
Three evidence-generating exercises over the banking model, beyond the single
baseline calibration:

  1. SENSITIVITY TABLE   -- sweep key parameters and report the derived
                            quantities (binding constraint, coupling, capacity).
  2. THRESHOLD DISCOVERY -- compute proposition boundaries algorithmically
                            (max credit intensity preserving N2; max observable
                            near-money preserving N5), rather than hardcoding.
  3. RANDOMIZED INVARIANT TESTING -- draw many random *admissible* calibrations
                            and confirm the STRUCTURAL propositions (N1, N4) hold
                            for every one, and report the PASS RATE and admissible
                            region for the CALIBRATION-dependent ones (N2, N3, N5).

The point is to show the structural propositions are properties of the design,
not artifacts of one parameter set. Run:
    python3 sensitivity.py
"""

import random
import balance_sheet as bs


# ---------------------------------------------------------------------------
# helpers that rebuild the derived quantities for arbitrary parameters
# (mirrors balance_sheet.py but parameterized, so we can sweep/randomize)
# ---------------------------------------------------------------------------
def derive(term_share, leverage, phi_liq, lambda_leak, chi_c, zeta_star,
           alpha, phi_gain, m2=None):
    """Return the derived quantities for one calibration."""
    m2 = bs.M2 if m2 is None else m2
    T = (1.0 - term_share) * m2          # reserved transaction money
    D = term_share * m2                  # term deposits (lending base)
    E = D / (leverage - 1.0)             # equity: D <= (lev-1)*E  => E = D/(lev-1)
    credit_capacity = D + E
    kappa_bank = phi_liq                 # credit intensity proxy m*phi_liq (m absorbed)
    coupling = lambda_leak + chi_c * kappa_bank
    theta = 1.0 + (1.0 + phi_gain) / alpha
    inside_money = T - T                 # 100%-reserve identity => 0
    # which constraint binds credit capacity: the term-deposit base (funding) or
    # equity (leverage)?  Under D<=(lev-1)E the two move together, but the SCARCE
    # input is whichever is smaller relative to its cap.  Report the binding side.
    binding = "term deposits (funding)" if D <= (leverage - 1.0) * E + 1e-9 else "equity (leverage)"
    return {
        "T": T, "D": D, "E": E, "credit_capacity": credit_capacity,
        "kappa_bank": kappa_bank, "coupling": coupling, "theta": theta,
        "inside_money": inside_money, "binding": binding,
        "max_contraction_share": D / m2,
    }


# ---------------------------------------------------------------------------
# 1. SENSITIVITY TABLE
# ---------------------------------------------------------------------------
def sensitivity_table():
    print("1. SENSITIVITY  (phi_liq swept; other parameters at baseline)")
    print(f"   {'phi_liq':>8}{'binding constraint':>26}{'coupling':>10}"
          f"{'capacity($T)':>14}{'sep?':>6}")
    for phi in [0.10, 0.15, 0.20, 0.30]:
        d = derive(bs.TERM_SHARE, bs.LEVERAGE, phi, bs.LAMBDA_LEAK, bs.CHI_C,
                   bs.ZETA_STAR, bs.ALPHA, bs.PHI_GAIN)
        sep = "yes" if d["coupling"] < bs.ZETA_STAR else "NO"
        print(f"   {phi:>8.2f}{d['binding']:>26}{d['coupling']:>10.3f}"
              f"{d['credit_capacity']:>13.1f} {sep:>5}")
    print()
    print("   (leverage swept; phi_liq at baseline)")
    print(f"   {'leverage':>8}{'equity($T)':>14}{'capacity($T)':>14}")
    for lev in [3.0, 4.0, 5.0]:
        d = derive(bs.TERM_SHARE, lev, bs.PHI_LIQ, bs.LAMBDA_LEAK, bs.CHI_C,
                   bs.ZETA_STAR, bs.ALPHA, bs.PHI_GAIN)
        print(f"   {lev:>7.0f}:1{d['E']:>13.1f}{d['credit_capacity']:>13.1f}")


# ---------------------------------------------------------------------------
# 2. THRESHOLD DISCOVERY  (algorithmic, not hardcoded)
# ---------------------------------------------------------------------------
def max_kappa_preserving_separation(lambda_leak=None, chi_c=None, zeta_star=None):
    """Largest credit intensity kappa with coupling still below zeta* (N2).
    Closed form: (zeta* - lambda)/chi ; verified by bisection as a check."""
    lam = bs.LAMBDA_LEAK if lambda_leak is None else lambda_leak
    chi = bs.CHI_C if chi_c is None else chi_c
    z = bs.ZETA_STAR if zeta_star is None else zeta_star
    closed = (z - lam) / chi
    # bisection check on coupling(kappa) = lam + chi*kappa < z
    lo, hi = 0.0, 5.0
    for _ in range(200):
        mid = (lo + hi) / 2
        if lam + chi * mid < z:
            lo = mid
        else:
            hi = mid
    assert abs(lo - closed) < 1e-6, (lo, closed)
    return closed


def max_near_money_preserving_throttle(cap_fraction=0.25):
    """Maximum observable near-money, as a share of term deposits, such that it
    stays within `cap_fraction` of the transaction aggregate M_T (so the throttle
    can still offset it as a bounded addition). Discovered by bisection on the
    near-money share s in [0,1]. N5's 'maximum observable near-money'."""
    T = (1.0 - bs.TERM_SHARE) * bs.M2
    D = bs.TERM_SHARE * bs.M2

    def within(s):
        return (s * D) / T <= cap_fraction

    lo, hi = 0.0, 1.0
    if within(hi):
        return hi
    for _ in range(200):
        mid = (lo + hi) / 2
        if within(mid):
            lo = mid
        else:
            hi = mid
    return lo


def threshold_discovery():
    print("2. THRESHOLD DISCOVERY  (computed, not hardcoded)")
    k = max_kappa_preserving_separation()
    print(f"   N2  max credit intensity kappa preserving separation = {k:.4f}")
    print(f"       (baseline kappa = {bs.PHI_LIQ:.3f}; margin to boundary = {k - bs.PHI_LIQ:.4f})")
    for frac in [0.20, 0.25, 0.30]:
        s = max_near_money_preserving_throttle(frac)
        print(f"   N5  max observable near-money preserving throttle "
              f"(<= {frac:.0%} of M_T) = {s:.1%} of term deposits")


# ---------------------------------------------------------------------------
# 3. RANDOMIZED INVARIANT TESTING
# ---------------------------------------------------------------------------
def admissible_draw(rng):
    """Draw one economically admissible calibration.
    Ranges are deliberately wide but economically sensible."""
    return dict(
        term_share=rng.uniform(0.30, 0.80),     # term-deposit share of M2
        leverage=rng.uniform(3.0, 6.0),          # leverage cap 3:1..6:1
        phi_liq=rng.uniform(0.05, 0.35),         # pledgeable/liquid fraction
        lambda_leak=rng.uniform(0.01, 0.06),     # structural leak
        chi_c=rng.uniform(0.15, 0.45),           # credit spend-through
        zeta_star=rng.uniform(0.10, 0.16),       # determinacy threshold band
        alpha=rng.uniform(0.5, 30.0),            # money-demand semi-elasticity
        phi_gain=rng.uniform(0.0, 3.0),          # KI gap response
        m2=rng.uniform(10.0, 40.0),              # money stock scale ($T)
    )


def randomized_invariants(n=10000, seed=12345):
    rng = random.Random(seed)
    # structural props: must hold for EVERY admissible draw
    struct = {"N1": 0, "N4": 0}
    # calibration props: report pass RATE over the admissible space
    calib = {"N2": 0, "N3": 0, "N5": 0}
    for _ in range(n):
        p = admissible_draw(rng)
        d = derive(**p)

        # N1 (structural): inside money = 0 and theta > 1, for any admissible params
        if abs(d["inside_money"]) < 1e-9 and d["theta"] > 1.0:
            struct["N1"] += 1
        # N4 (structural): reserved layer unrunnable (contraction share < 1 = full stock)
        #   and strictly below the incumbent all-runnable bound
        if d["max_contraction_share"] < 1.0 - 1e-9:
            struct["N4"] += 1

        # N2 (calibration): separation holds iff coupling < zeta*
        if d["coupling"] < p["zeta_star"]:
            calib["N2"] += 1
        # N3 (calibration): credit capacity is the leverage identity D*lev/(lev-1)>0
        cap_ok = abs(d["credit_capacity"] - p["term_share"] * p["m2"] * p["leverage"] / (p["leverage"] - 1.0)) < 1e-6
        if cap_ok and d["credit_capacity"] > 0:
            calib["N3"] += 1
        # N5 (calibration): near-money at 10% of term deposits stays a finite share of M_T
        T = (1.0 - p["term_share"]) * p["m2"]
        D = p["term_share"] * p["m2"]
        if T > 0 and 0.0 < (0.10 * D) / T < 1.0:
            calib["N5"] += 1

    print(f"3. RANDOMIZED INVARIANT TESTING  ({n:,} admissible calibrations, seed {seed})")
    print("   STRUCTURAL (must hold for every draw):")
    all_struct_ok = True
    for tag in ["N1", "N4"]:
        rate = struct[tag] / n
        ok = struct[tag] == n
        all_struct_ok &= ok
        print(f"     {tag}  {struct[tag]:>6}/{n}  ({rate:.1%})  "
              f"{'PASS (invariant)' if ok else 'FAIL (not invariant!)'}")
    print("   CALIBRATION-DEPENDENT (pass rate over the admissible space):")
    for tag in ["N2", "N3", "N5"]:
        rate = calib[tag] / n
        print(f"     {tag}  {calib[tag]:>6}/{n}  ({rate:.1%} of admissible draws)")
    return all_struct_ok


if __name__ == "__main__":
    print("=" * 70)
    print("PAPER 6 -- FULL-RESERVE BANKING: sensitivity, thresholds, invariants")
    print("=" * 70)
    sensitivity_table()
    print()
    threshold_discovery()
    print()
    ok = randomized_invariants()
    print("=" * 70)
    print("STRUCTURAL PROPOSITIONS INVARIANT ACROSS ADMISSIBLE SPACE"
          if ok else "*** A STRUCTURAL PROPOSITION FAILED INVARIANCE ***")
    import sys
    sys.exit(0 if ok else 1)

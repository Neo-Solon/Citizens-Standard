"""
explore.py
==========
An EXPLORATION interface for the Citizens Standard banking model, turning the
replication package from a verification tool (does the baseline hold?) into a
research tool (where is the boundary? what if a parameter moves?).

Two capabilities:

  1. DISCOVER  -- compute the model's boundary quantities algorithmically, as
                 publishable numbers rather than pass/fail checks:
                   * maximum term-deposit share preserving an adequate M_o
                   * maximum credit intensity preserving circuit separation (N2)
                   * maximum observable near-money preserving controllability (N5)

  2. WHAT-IF   -- answer parametric questions by re-deriving the model:
                   * what_if(collateral=2.0)    -> doubles pledgeable fraction
                   * what_if(liquidity=0.5)     -> halves liquid share
                   * stability_boundary(param)  -> where a proposition flips

All quantities are derived from balance_sheet.py, so the exploration inherits the
same accounting mechanism the propositions are tested against. Boundaries are found
by bisection; the model is analytic, so these are exact to tolerance.

Usage:
    python3 explore.py                      # full discovery report
    python3 explore.py --what-if collateral=2.0
    python3 explore.py --boundary chi_c     # trace where N2 separation flips
"""

import sys
import balance_sheet as bs


TOL = 1e-7


# ---------------------------------------------------------------------------
# derived quantities for an arbitrary calibration (parameterized balance sheet)
# ---------------------------------------------------------------------------
def derive(term_share=None, leverage=None, phi_liq=None, lambda_leak=None,
           chi_c=None, zeta_star=None, m2=None):
    term_share = bs.TERM_SHARE if term_share is None else term_share
    leverage   = bs.LEVERAGE   if leverage   is None else leverage
    phi_liq    = bs.PHI_LIQ    if phi_liq    is None else phi_liq
    lambda_leak= bs.LAMBDA_LEAK if lambda_leak is None else lambda_leak
    chi_c      = bs.CHI_C      if chi_c      is None else chi_c
    zeta_star  = bs.ZETA_STAR  if zeta_star  is None else zeta_star
    m2         = bs.M2         if m2         is None else m2

    T = (1.0 - term_share) * m2               # transaction money (M_o)
    D = term_share * m2                        # term deposits
    E = D / (leverage - 1.0)
    kappa = phi_liq                            # credit intensity proxy
    coupling = lambda_leak + chi_c * kappa
    return dict(T=T, D=D, E=E, credit_capacity=D + E, kappa=kappa,
                coupling=coupling, zeta_star=zeta_star, separated=coupling < zeta_star,
                m_o_share=T / m2)


# ---------------------------------------------------------------------------
# 1. BOUNDARY DISCOVERY (bisection)
# ---------------------------------------------------------------------------
def _bisect(predicate, lo, hi, iters=200):
    """Largest x in [lo,hi] with predicate(x) True (predicate True->False monotone)."""
    if not predicate(lo):
        return None
    if predicate(hi):
        return hi
    for _ in range(iters):
        mid = (lo + hi) / 2
        if predicate(mid):
            lo = mid
        else:
            hi = mid
    return lo


def max_term_share(min_m_o_fraction=0.25):
    """Maximum term-deposit share such that transaction money M_o stays at least
    `min_m_o_fraction` of M2 (the 'maximum allowable transactional-deposit split').
    Closed form: 1 - min_m_o_fraction; bisection confirms."""
    return _bisect(lambda ts: derive(term_share=ts)["m_o_share"] >= min_m_o_fraction,
                   0.0, 0.999)


def max_credit_intensity():
    """Maximum credit intensity (phi_liq) preserving circuit separation (N2)."""
    return _bisect(lambda k: derive(phi_liq=k)["separated"], 0.0, 5.0)


def max_near_money(cap_fraction=0.25):
    """Maximum observable near-money (as share of term deposits) before it exceeds
    `cap_fraction` of the transaction aggregate M_T -- N5's controllability limit."""
    d = derive()
    return _bisect(lambda s: (s * d["D"]) / d["T"] <= cap_fraction, 0.0, 1.0)


def discover():
    print("BOUNDARY DISCOVERY (computed, publishable quantities)")
    print("-" * 60)
    ts = max_term_share(0.25)
    print(f"  Maximum transactional (term-deposit) share")
    print(f"    keeping M_o >= 25% of M2:                 {ts:.3f}")
    k = max_credit_intensity()
    print(f"  Maximum credit intensity (phi_liq)")
    print(f"    preserving circuit separation (N2):        {k:.3f}")
    print(f"    (baseline {bs.PHI_LIQ:.3f}; headroom {k - bs.PHI_LIQ:.3f})")
    for frac in (0.25, 0.30):
        nm = max_near_money(frac)
        print(f"  Maximum observable near-money")
        print(f"    before it exceeds {frac:.0%} of M_T (N5):     {nm:.1%} of term deposits")


# ---------------------------------------------------------------------------
# 2. WHAT-IF QUERIES
# ---------------------------------------------------------------------------
def what_if(collateral=1.0, liquidity=1.0, leverage_mult=1.0, verbose=True):
    """Re-derive the model under multiplicative shocks to key inputs.
      collateral    : multiplier on pledgeable fraction phi_liq (credit intensity)
      liquidity     : multiplier on the liquid share (also phi_liq here)
      leverage_mult : multiplier on the leverage cap
    Returns the derived dict; prints a before/after summary."""
    base = derive()
    phi_new = min(1.0, bs.PHI_LIQ * collateral * liquidity)
    lev_new = bs.LEVERAGE * leverage_mult
    new = derive(phi_liq=phi_new, leverage=lev_new)
    if verbose:
        print(f"WHAT-IF  collateral x{collateral}, liquidity x{liquidity}, "
              f"leverage x{leverage_mult}")
        print(f"    phi_liq:  {bs.PHI_LIQ:.3f} -> {phi_new:.3f}")
        print(f"    coupling: {base['coupling']:.3f} -> {new['coupling']:.3f}  "
              f"(zeta* = {new['zeta_star']:.2f})")
        print(f"    separation: {'holds' if base['separated'] else 'FAILS'} -> "
              f"{'holds' if new['separated'] else 'FAILS'}")
        print(f"    credit capacity: ${base['credit_capacity']:.1f}T -> "
              f"${new['credit_capacity']:.1f}T")
    return new


def stability_boundary(param, lo=0.0, hi=1.0):
    """Find the critical value of `param` at which circuit separation (N2) flips.
    param in {'phi_liq','chi_c','lambda_leak'}. Returns the threshold or None if
    separation holds/fails across the whole range."""
    def sep(x):
        return derive(**{param: x})["separated"]
    if sep(lo) == sep(hi):
        return None   # no flip in range
    for _ in range(200):
        mid = (lo + hi) / 2
        if sep(mid) == sep(lo):
            lo = mid
        else:
            hi = mid
    return (lo + hi) / 2


# ---------------------------------------------------------------------------
# CLI
# ---------------------------------------------------------------------------
def _parse_kv(arg):
    k, v = arg.split("=")
    return k, float(v)


if __name__ == "__main__":
    args = sys.argv[1:]
    if not args:
        print("=" * 60)
        print("CITIZENS STANDARD BANKING -- EXPLORATION")
        print("=" * 60)
        discover()
        print()
        print("EXAMPLE WHAT-IF QUERIES")
        print("-" * 60)
        what_if(collateral=2.0)
        print()
        what_if(liquidity=0.5)
        print()
        b = stability_boundary("chi_c", 0.0, 1.0)
        print(f"STABILITY BOUNDARY: circuit separation (N2) flips when "
              f"chi_c = {b:.3f}" if b else "no flip over chi_c in [0,1]")
        b2 = stability_boundary("phi_liq", 0.0, 1.0)
        print(f"                    circuit separation (N2) flips when "
              f"phi_liq = {b2:.3f}" if b2 else "")
        sys.exit(0)

    if args[0] == "--what-if" and len(args) > 1:
        params = dict(_parse_kv(a) for a in args[1:])
        what_if(**params)
    elif args[0] == "--boundary" and len(args) > 1:
        b = stability_boundary(args[1], 0.0, 1.0)
        print(f"separation flips at {args[1]} = {b:.4f}" if b
              else f"no separation flip over {args[1]} in [0,1]")
    elif args[0] == "--discover":
        discover()
    else:
        print(__doc__)

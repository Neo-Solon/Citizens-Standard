"""
spillover_estimate.py
=====================
Empirical anchoring of the asset-to-goods spillover lambda (Paper 9, Sec 8.2 --
the "20% spillover"). lambda is the fraction of each year's new asset-circuit
(locked Stable Floor) issuance that leaks into goods demand: operationally, the
marginal propensity to consume (MPC) out of newly accrued, locked, unrealized
equity wealth.

This module upgrades lambda from "calibrated" toward "estimated" in three steps:
 1. assemble the named empirical wealth-effect literature into an implied band
    for MPC out of equity/housing wealth, by liquidity/realization status;
 2. locate the framework's lambda = 0.20 against that band (a deliberate
    cautious-HIGH choice: it overstates, never understates, inflation risk);
 3. report the locus-exact dividend share kappa_d*(lambda) at each estimate,
    since kappa_d is the free instrument that recentres the split if measured
    lambda differs from 0.20 (Paper 9, Table 4 logic, solved exactly).

Sources (annual MPC per dollar of wealth unless noted):
  Poterba (2000, J. Econ. Perspectives survey), stock wealth ...... 0.02-0.05
  Case, Quigley & Shiller (2005; 2013), housing (upper ref.) ...... 0.03-0.05
  Mian, Rao & Sufi (2013, QJE), housing net-worth shock ........... 0.05-0.07
  Chodorow-Reich, Nenov & Simsek (2021, AER), stock (~2yr) ........ 0.028-0.032
  Di Maggio, Kermani & Majlesi (2020, J. Finance, Swedish registry)
      unrealized capital gains, median household .................. ~0.05
      top-of-distribution holders ................................. ~0.01
  Baker, Nagel & Wurgler (2007), dividends (paid-out income) ...... 0.35-0.75
      (relevant to the K3 dividend channel, which reaches M^T at ~1.0
       by construction -- NOT to the locked floor)

The Stable Floor is locked and unrealizable by construction (no withdrawal, no
collateralization before retirement), which places the floor-relevant MPC at or
below the UNREALIZED-gains estimates above.
"""
import json
import os

M2, MT_SHARE, G = 22366.0, 0.5135, 0.02      # $B, transactional share, real growth
BUDGET = G * M2                               # $447.3B full growth budget
K1 = 9.0                                      # $B citizenship deposits

lit = [
    ("Poterba (2000, JEP survey), stock wealth",               0.020, 0.050),
    ("Case-Quigley-Shiller (2005/2013), housing (upper ref)",  0.030, 0.050),
    ("Mian-Rao-Sufi (2013, QJE), housing net worth",           0.050, 0.070),
    ("Chodorow-Reich-Nenov-Simsek (2021, AER), stock",         0.028, 0.032),
    ("Di Maggio-Kermani-Majlesi (2020, JF), unrealized gains", 0.010, 0.050),
]
lo = min(a for _, a, _ in lit)
hi = max(b for _, _, b in lit)


def inject(lam, kappa=0.40):
    """Money reaching M^T: the K3 dividend plus the lambda leak of everything
    routed to the asset circuit (K1 + locked K2)."""
    R = BUDGET - K1
    div = kappa * R
    return div + lam * (BUDGET - div)


def drift_at(lam, kappa=0.40):
    return (inject(lam, kappa) - G * MT_SHARE * M2) / (MT_SHARE * M2)


def kappa_star(lam):
    """Dividend share that puts the injection exactly on the locus g*M^T."""
    R = BUDGET - K1
    locus = G * MT_SHARE * M2
    return (locus - lam * BUDGET) / (R * (1.0 - lam))


if __name__ == "__main__":
    print("=" * 82)
    print("ASSET-TO-GOODS SPILLOVER lambda -- empirical anchoring (Paper 9, Sec 8.2)")
    print("=" * 82)

    print("\n[1] Literature band, MPC out of equity/housing wealth (annual, per $):")
    for name, a, b in lit:
        print(f"    {name:<55} {a:.3f}-{b:.3f}")
    print(f"    pooled band: {lo:.2f}-{hi:.2f}   |   framework lambda = 0.20 "
          f"({0.20/hi:.1f}x-{0.20/lo:.0f}x the literature range)")
    print("    -> 0.20 is cautious-HIGH: it overstates the leak, hence overstates")
    print("       inflation risk. A measured spillover below 0.20 makes the fixed")
    print("       60/40 split mildly deflationary, never inflationary.")

    print("\n[2] Mode B drift at the fixed 60/40 split, by lambda:")
    for lam in [lo, 0.05, hi, 0.20, 0.30]:
        print(f"    lambda={lam:.2f}: drift = {drift_at(lam)*100:+.2f}%/yr")
    # sanity: reproduce Paper 9 Table 4 rows (10/20/30%) to ~5bp
    assert abs(drift_at(0.20)) < 0.001
    assert abs(drift_at(0.10) - (-0.0021)) < 0.0006
    assert abs(drift_at(0.30) - (+0.0027)) < 0.0006

    print("\n[3] Locus-exact dividend share kappa_d*(lambda) -- the recentering instrument:")
    rows = []
    for lam in [lo, 0.05, hi, 0.20]:
        ks = kappa_star(lam)
        rows.append({"lambda": lam, "kappa_star": round(ks, 4)})
        tag = "the published 60/40 split" if abs(lam - 0.20) < 1e-9 else "recentred split at this estimate"
        print(f"    lambda={lam:.2f}: kappa_d* = {ks*100:.1f}%   ({tag})")
    print("    At literature-point spillovers the locus-exact dividend share rises")
    print("    toward roughly 49-52% (floor share falls correspondingly). Direction and")
    print("    magnitude match Paper 9 Table 4: the spillover sets a calibration,")
    print("    not an outcome.")

    out = {
        "literature_band": {"low": lo, "high": hi, "sources": [n for n, _, _ in lit]},
        "framework_lambda": 0.20,
        "assessment": "cautious-high; ~3x-10x the literature point for locked, unrealized holdings",
        "drift_at_60_40_by_lambda": {f"{l:.3f}": round(drift_at(l), 5)
                                     for l in [lo, 0.05, hi, 0.20, 0.30]},
        "kappa_star_by_lambda": rows,
    }
    here = os.path.dirname(os.path.abspath(__file__))
    res = os.path.normpath(os.path.join(here, "..", "results"))
    os.makedirs(res, exist_ok=True)
    with open(os.path.join(res, "spillover_results.json"), "w") as f:
        json.dump(out, f, indent=1)
    print(f"\nSaved {os.path.join(res, 'spillover_results.json')}")

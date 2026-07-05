"""
test_propositions.py
====================
Automated proposition tests for Paper 6, "Full-Reserve Banking and the
Two-Circuit System." Mirrors the verify_prop convention of the Paper 1 and
Paper 8 replication packages: each banking proposition N1-N5 is checked against
quantities *derived from an explicit two-account balance sheet* (balance_sheet.py),
not against hardcoded restatements of the claim. A proposition therefore fails
if the underlying accounting mechanism is wrong, not merely if a constant is
mistyped.

Run to validate the paper after any change:
    python3 test_propositions.py
Prints one PASS/FAIL line per proposition; exits non-zero on any failure.
"""

import sys
import balance_sheet as bs

TOL = 1e-9
_results = []


def check(tag, kind, title, condition, detail):
    # kind: "structural" (identity; holds for any admissible parameters) or
    #       "calibration" (PASS or magnitude depends on the calibrated values)
    _results.append((tag, bool(condition), kind, title, detail))


inc = bs.incumbent()
cs = bs.citizens_standard()

# N1 (complete monetary control): inside money DERIVED = T - reserves_held from
#    the 100%-reserve identity; must be zero and M_T = M_o; theta>1 applies to M_o.
theta = bs.determinacy_root()
check("N1", "structural", "complete monetary control",
      (abs(cs["inside_money"]) < 1e-6)
      and (abs(cs["money_stock"] - cs["transaction_money"]) < TOL)
      and (theta > 1.0 + TOL)
      and (inc["inside_share"] > 0.5),
      f"inside money derived = ${cs['inside_money']:.3f}T (incumbent {inc['inside_share']:.2f} of stock); "
      f"M_T = M_o = ${cs['money_stock']:.1f}T; theta = {theta:.2f} > 1")

# N2 (separation survives bank credit): coupling = lambda + chi*kappa; DERIVED
#    across the credit-intensity range, and must FAIL past the derived ceiling.
kappa_baseline = 0.075
ceiling = bs.separation_kappa_ceiling()
coupling_baseline = bs.asset_consumer_coupling(kappa_baseline)
holds_below = all(bs.asset_consumer_coupling(k) < bs.ZETA_STAR
                  for k in [0.0, 0.05, 0.075, 0.10])
fails_above = bs.asset_consumer_coupling(ceiling + 0.05) >= bs.ZETA_STAR
check("N2", "calibration", "separation survives bank credit",
      (coupling_baseline < bs.ZETA_STAR - TOL) and holds_below and fails_above
      and (kappa_baseline < ceiling - TOL),
      f"coupling(kappa={kappa_baseline}) = {coupling_baseline:.3f} < zeta* = {bs.ZETA_STAR}; "
      f"holds for kappa < ceiling = {ceiling:.3f}, fails above it")

# N2 sensitivity: separation is robust across a wide credit-intensity range,
# flipping to FAIL only past the derived ceiling. Reported for referees.
_n2_sweep = []
for k in [0.05, 0.10, 0.15, 0.20, 0.30, 0.34]:
    c = bs.asset_consumer_coupling(k)
    _n2_sweep.append((k, c, c < bs.ZETA_STAR))

# N3 (credit supply): L <= D + E, D <= 3E => capacity = D*4/3. DERIVED from D,E.
D, E, cap = cs["term_deposits"], cs["equity"], cs["credit_capacity"]
check("N3", "calibration", "credit supply under full reserve",
      (abs(cap - D * bs.LEVERAGE / 3.0) < 1e-6)
      and (D / E <= 3.0 + TOL)
      and (17.5 < cap < 18.5),
      f"D = ${D:.1f}T, E = ${E:.1f}T, capacity = D*4/3 = ${cap:.1f}T "
      f"(leverage {D/E:.0f}:1 within 4:1)")

# N4 (run-proof): runnable money DERIVED = 0 (reserved layer unrunnable); max
#    contraction bounded by term share, strictly below incumbent runnable stock.
check("N4", "structural", "run-proof payments",
      (abs(cs["runnable_money"]) < TOL)
      and (cs["max_money_contraction_share"] < inc["runnable_share_of_money"] - TOL)
      and (abs(cs["max_money_contraction_share"] - bs.TERM_SHARE) < 1e-6),
      f"runnable transaction money = ${cs['runnable_money']:.3f}T; max contraction "
      f"{cs['max_money_contraction_share']:.0%} (term share) vs incumbent "
      f"{inc['runnable_share_of_money']:.0%} of money stock")

# N5 (near-money boundary): near-money enters the throttled aggregate M_T and is
#    finite/offsettable when observable -- DERIVED against the actual T base.
T = cs["transaction_money"]
near_fracs = [0.05, 0.10, 0.20]
enters_and_finite = []
for s in near_fracs:
    nm = s * cs["term_deposits"]
    share_of_txn = nm / T
    enters_and_finite.append(0.0 < share_of_txn < 1.0)
check("N5", "calibration", "near-money boundary is bounded and conditional",
      all(enters_and_finite) and (T > 0),
      f"near-money at {near_fracs} of term deposits adds "
      f"{[round(s*cs['term_deposits']/T,2) for s in near_fracs]} of M_T; "
      f"enters the throttled aggregate when observable (conditional, not abolished)")


def _print_group(kind, heading):
    print(heading)
    for tag, ok, k, title, detail in _results:
        if k != kind:
            continue
        status = "PASS" if ok else "FAIL"
        print(f"  {status}  {tag}  ({title})")
        print(f"          {detail}")


if __name__ == "__main__":
    print("=" * 70)
    print("PAPER 6 -- FULL-RESERVE BANKING: automated proposition tests")
    print("  claims derived from balance_sheet.py, not asserted.")
    print("  Structural = identity, holds for any admissible parameters.")
    print("  Calibration = PASS or magnitude depends on the calibrated values.")
    print("=" * 70)

    _print_group("structural",
                 "STRUCTURAL (unchanged if parameters change):")
    _print_group("calibration",
                 "\nCALIBRATION-DEPENDENT (contingent on the calibrated values):")

    # N2 sensitivity analysis
    print("\nN2 sensitivity -- separation coupling vs credit intensity kappa:")
    print(f"  threshold zeta* = {bs.ZETA_STAR};  ceiling kappa = "
          f"{bs.separation_kappa_ceiling():.3f}")
    for k, c, ok in _n2_sweep:
        print(f"    kappa = {k:.2f}  ->  coupling = {c:.3f}  {'PASS' if ok else 'FAIL'}")

    all_pass = all(ok for _, ok, _, _, _ in _results)
    print("=" * 70)
    print(("ALL PROPOSITIONS PASS" if all_pass else "SOME PROPOSITIONS FAILED")
          + f"  ({sum(1 for _, ok, _, _, _ in _results if ok)}/{len(_results)})")
    sys.exit(0 if all_pass else 1)

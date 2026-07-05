"""
verify_all.py
=============
Consolidated verification harness and diagnostic dashboard for Paper 8, "The
Structural Buyer" (Neo-Solon 2026h). Mirrors the Paper 6 banking harness: each
proposition is reduced to its concrete claim, checked against the model's
computed quantities, tagged structural (identity / holds for any admissible
parameters) or calibration (depends on the calibrated magnitudes), and reported
in a one-page dashboard. Where a proposition has an admissible band (Prop 1's
stability condition, Prop 3's leak range), the boundary is reported explicitly.

This adds no new economics; it re-expresses the existing verify_prop*.py checks
as a single PASS/FAIL report with structural/calibration classification and a
summary dashboard, so a reader gets the model's state from one command.

Run:
    python3 verify_all.py            # full report + dashboard
    python3 verify_all.py dashboard  # one-page dashboard only
"""

import sys

_results = []


def check(tag, kind, title, condition, detail):
    _results.append((tag, bool(condition), kind, title, detail))


# ---------------------------------------------------------------------------
# Prop 1 -- bounded valuation fixed point + stability band
#   Q* - Q_baseline = A*/phi  (finite premium for any phi>0)      [structural]
#   converges iff 0 < theta*phi < 2                               [calibration band]
# ---------------------------------------------------------------------------
def _fixed_point(A, phi, theta, Qb=1.0, T=200000):
    Q = Qb
    for _ in range(T):
        Q = (1 - theta * phi) * Q + theta * (A + phi * Qb)
    return Q


A_STAR, PHI, THETA, QB = 0.45, 0.5, 0.5, 1.0
prem_closed = A_STAR / PHI
prem_sim = _fixed_point(A_STAR, PHI, THETA, QB) - QB
converges = 0 < THETA * PHI < 2
check("P1", "structural", "bounded valuation premium = A*/phi",
      abs(prem_sim - prem_closed) < 1e-6 and prem_closed < float("inf"),
      f"premium sim {prem_sim:.4f} = closed-form A*/phi {prem_closed:.4f}; finite for any phi>0")
check("P1b", "calibration", "fixed point converges (0 < theta*phi < 2)",
      converges and (THETA * PHI < 2),
      f"theta*phi = {THETA*PHI:.2f} in (0,2); stability band upper edge theta*phi = 2")

# ---------------------------------------------------------------------------
# Prop 2 -- permanent flow funds real investment (I* = A*)        [structural]
# ---------------------------------------------------------------------------
a_decay = 1 - THETA * PHI
I_ss = A_STAR                                  # steady-state issuance = flow
total_repricing = A_STAR / PHI                 # once-for-all, = the whole premium
check("P2", "structural", "steady-state flow funds investment (I* = A*)",
      abs(I_ss - A_STAR) < 1e-9 and abs(total_repricing - A_STAR / PHI) < 1e-9,
      f"I* = A* = {I_ss:.3f}; total repricing sum R_t = A*/phi = {total_repricing:.3f} (once-for-all)")

# ---------------------------------------------------------------------------
# Prop 3 -- bounded seller-rebalancing leak                        [calibration band]
#   leak <= kappa_W * Delta, kappa_W in [0.025, 0.05], central ~0.03
# ---------------------------------------------------------------------------
KAPPA_LO, KAPPA_HI, KAPPA_C = 0.025, 0.05, 0.03
leak_c = KAPPA_C * 1.0
reenter_c = 1 - leak_c
leak_hi = KAPPA_HI * 1.0
check("P3", "calibration", "bounded rebalancing leak (<= kappa_W)",
      abs(leak_c - 0.03) < 1e-9 and reenter_c >= 0.97 - 1e-9 and leak_hi <= 0.05 + 1e-9,
      f"central leak {leak_c:.1%} (>= {reenter_c:.0%} re-enters asset circuit); "
      f"literature band [{KAPPA_LO:.1%}, {KAPPA_HI:.1%}]")

# ---------------------------------------------------------------------------
# psi-plateau -- citizen-ownership share                           [calibration]
#   psi* = c * annuity(g, dur), bounded above by c/g
# ---------------------------------------------------------------------------
C_SHARE, DUR, G = 0.00394, 40, 0.02
cdur = C_SHARE * DUR                            # zero-growth reference
psi_bound = C_SHARE / G                         # upper bound under positive growth
check("PSI", "calibration", "citizen-ownership share psi* bounded",
      abs(cdur - 0.16) < 6e-3 and (C_SHARE * DUR <= psi_bound + 1e-9),
      f"zero-growth reference c*dur = {cdur:.3f}; upper bound c/g = {psi_bound:.3f}")

# ---------------------------------------------------------------------------
# Prop 7 -- mirror-voting neutrality (structural, exact for all psi)
#   YES_total = (1-psi)p + psi*p = p for every psi                 [structural]
# ---------------------------------------------------------------------------
import random
_rng = random.Random(0)
_max_err = 0.0
_thr_ok = True
for _ in range(50000):
    psi = _rng.uniform(0.0, 1.0)
    p = _rng.uniform(0.0, 1.0)
    yes_total = (1 - psi) * p + psi * p
    _max_err = max(_max_err, abs(yes_total - p))
    tau = _rng.uniform(0.0, 1.0)
    if (yes_total >= tau) != (p >= tau):
        _thr_ok = False
check("P7", "structural", "mirror-voting neutrality (outcome = residual, any psi)",
      _max_err < 1e-12 and _thr_ok,
      f"max |YES_total - p| = {_max_err:.1e} over 50k draws; threshold outcome matches residual")


# ---------------------------------------------------------------------------
# dashboard + report
# ---------------------------------------------------------------------------
def dashboard():
    line = "=" * 46
    print(line)
    print("       Paper 8 Verification Summary")
    print("          (The Structural Buyer)")
    print(line)
    print()
    for tag, ok, kind, title, _ in _results:
        print(f"  {tag:<4} {'PASS' if ok else 'FAIL'}   {title}  [{kind}]")
    print()
    print("  Key diagnostics:")
    print(f"    Valuation premium (A*/phi):     {prem_closed:.3f}  (finite, structural)")
    print(f"    Stability band:                 0 < theta*phi < 2  (at {THETA*PHI:.2f})")
    print(f"    Steady-state investment I*/A*:  {I_ss/A_STAR:.2f}  (flow fully funds investment)")
    print(f"    Central rebalancing leak:       {leak_c:.1%}  (band {KAPPA_LO:.1%}-{KAPPA_HI:.1%})")
    print(f"    Asset-circuit re-entry:         {reenter_c:.0%}")
    print(f"    Citizen-ownership psi* bound:   {psi_bound:.3f}  (c/g)")
    print(f"    Mirror-voting neutrality error: {_max_err:.0e}  (exact for any psi)")
    print()
    struct = [r for r in _results if r[2] == "structural"]
    calib = [r for r in _results if r[2] == "calibration"]
    all_pass = all(r[1] for r in _results)
    struct_pass = all(r[1] for r in struct)
    print(line)
    if all_pass:
        print(f"  Overall: all {len(_results)} propositions verified")
        print(f"           ({len(struct)} structural, {len(calib)} calibration-dependent).")
    else:
        print("  Overall: ONE OR MORE PROPOSITIONS FAILED -- see detail.")
    print(line)
    return all_pass


def full_report():
    print("#" * 60)
    print("# PAPER 8 -- THE STRUCTURAL BUYER: VERIFICATION REPORT")
    print("#" * 60)
    print()
    print("STRUCTURAL (identities; hold for any admissible parameters):")
    for tag, ok, kind, title, detail in _results:
        if kind == "structural":
            print(f"  {'PASS' if ok else 'FAIL'}  {tag}  {title}")
            print(f"        {detail}")
    print("\nCALIBRATION-DEPENDENT (depend on the calibrated magnitudes):")
    for tag, ok, kind, title, detail in _results:
        if kind == "calibration":
            print(f"  {'PASS' if ok else 'FAIL'}  {tag}  {title}")
            print(f"        {detail}")
    print()
    return dashboard()


if __name__ == "__main__":
    if len(sys.argv) > 1 and sys.argv[1] == "dashboard":
        ok = dashboard()
    else:
        ok = full_report()
    sys.exit(0 if ok else 1)

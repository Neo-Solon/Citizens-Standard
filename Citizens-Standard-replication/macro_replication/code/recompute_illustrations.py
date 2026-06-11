"""
recompute_illustrations.py
--------------------------
Recomputes the two worked illustrative magnitude bounds in:

    Neo-Solon (2026e). The Citizens Standard: A Macroeconomic Model of a
    Two-Circuit Monetary System. Working Paper.
        Section 3.2a  — illustrative magnitude of the consumer-price leak
        Section 6.5   — illustrative magnitude of the structural-buyer premium

These are explicitly *worked illustrations, not calibrations* (the paper says
so). This script exists only so a reader does not have to trust the arithmetic:
it reproduces every number printed in Sections 3.2a and 6.5 from the inputs
stated in those sections. All inputs are anchored to the architectural paper
(Neo-Solon 2026a) or bracketed within the stated plausible bands.
"""

# ---------------------------------------------------------------------------
# SECTION 3.2a — consumer-price leak
#   Leak = kappa_W * (Delta / mu_star) * (1 - s_t)
# ---------------------------------------------------------------------------
M2 = 22_366.0          # $B, anchored (Neo-Solon 2026a, A.1)
DELTA_B = 455.0        # $B, Mode B annual issuance (Neo-Solon 2026a, Section 5.1)
DELTA_A = 80.0         # $B, Mode A annual issuance (Neo-Solon 2026a, Table 2)


def leak(delta, kappa_w, mu_star, s_t):
    return kappa_w * (delta / mu_star) * (1.0 - s_t)


def pct_m2(x):
    return 100.0 * x / M2


def section_3_2a():
    print("=" * 70)
    print("SECTION 3.2a — illustrative consumer-price leak")
    print("  Leak = kappa_W * (Delta / mu*) * (1 - s_t)")
    print("=" * 70)

    # Central case: kappa_W = 0.03, mu* = 0.15, s_t = 0 (launch, worst case)
    lk_b = leak(DELTA_B, 0.03, 0.15, 0.0)
    print(f"Mode B central (kappa_W=0.03, mu*=0.15, s_t=0):")
    print(f"   leak = ${lk_b:,.0f}B  =  {pct_m2(lk_b):.2f}% of M2   [paper: ~$91B, 0.41%]")

    # Full band: low end (0.02, 0.25) and high end (0.05, 0.10)
    lk_lo = leak(DELTA_B, 0.02, 0.25, 0.0)
    lk_hi = leak(DELTA_B, 0.05, 0.10, 0.0)
    print(f"Mode B band: ${lk_lo:,.0f}B - ${lk_hi:,.0f}B "
          f"= {pct_m2(lk_lo):.2f}% - {pct_m2(lk_hi):.2f}% of M2   "
          f"[paper: $36B-$228B, 0.16%-1.02%]")

    # Mode A central
    lk_a = leak(DELTA_A, 0.03, 0.15, 0.0)
    print(f"Mode A central: ${lk_a:,.0f}B = {pct_m2(lk_a):.2f}% of M2   "
          f"[paper: ~$16B, 0.07%]")

    # Decline as floors mature (central case, varying s_t)
    print("\nDecline of the leak as the locked-float share s_t rises (Mode B central):")
    for s in [0.0, 0.25, 0.50, 0.75, 0.90]:
        lk = leak(DELTA_B, 0.03, 0.15, s)
        print(f"   s_t={s:>4.2f}  ->  {pct_m2(lk):.2f}% of M2")
    print("   [paper: 0.41 / 0.31 / 0.20 / 0.10 / 0.04 %]")
    print()


# ---------------------------------------------------------------------------
# SECTION 6.5 — structural-buyer valuation premium
#   A* = gross - L_t ;   premium = A* / phi  (against capitalization)
# ---------------------------------------------------------------------------
GROSS = 455.0          # $B/yr gross FDCA equity purchase (Neo-Solon 2026a)
CAP = 55_000.0         # $B total US equity capitalization (order of magnitude)


def net_absorption(gross, drawdown_frac):
    return gross * (1.0 - drawdown_frac)


def section_6_5():
    print("=" * 70)
    print("SECTION 6.5 — illustrative structural-buyer valuation premium")
    print("  A* = gross - L_t ;  premium (level) = (A*/CAP) / phi")
    print("=" * 70)

    print("Net absorption A* as drawdown L_t ramps up:")
    for dd in [0.40, 0.60, 0.90]:
        a_star = net_absorption(GROSS, dd)
        print(f"   L_t={dd:>4.0%}  ->  A* = ${a_star:,.0f}B/yr = {100*a_star/CAP:.2f}% of cap")
    print("   [paper: $273B/0.50% , $182B/0.33% , $45B/0.08%]")

    # Premium at mid drawdown (A* ~ $182B, 0.33% of cap) across supply elasticity phi
    a_mid = net_absorption(GROSS, 0.60)
    base_pct = 100.0 * a_mid / CAP
    print(f"\nValuation premium at mid drawdown (A*=${a_mid:,.0f}B, {base_pct:.2f}% of cap):")
    for phi in [0.5, 1.0, 2.0]:
        premium = base_pct / phi
        print(f"   phi={phi:>4.1f}  ->  premium = {premium:.2f}% of valuation level")
    print("   [paper: 0.66% / 0.33% / 0.17%]")
    print()


if __name__ == "__main__":
    section_3_2a()
    section_6_5()
    print("All illustrative magnitudes reproduce the figures printed in")
    print("Sections 3.2a and 6.5 of Neo-Solon (2026e).")

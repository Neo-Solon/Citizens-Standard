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
DELTA_B = 272.0        # $B, Mode B asset-circuit injection = FDCA purchase = K1 + 0.6*K2
                       # (Mode B 60/40). The 40% K3 dividend (~$175B) goes straight to the
                       # goods circuit (Section 4.3 channel), so it is NOT an asset-circuit leak.
                       # Full growth-issuance line remains K1+K2 = $447B.
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
    print(f"   leak = ${lk_b:,.0f}B  =  {pct_m2(lk_b):.2f}% of M2   [paper: ~$54B, 0.24%]")

    # Full band: low end (0.02, 0.25) and high end (0.05, 0.10)
    lk_lo = leak(DELTA_B, 0.02, 0.25, 0.0)
    lk_hi = leak(DELTA_B, 0.05, 0.10, 0.0)
    print(f"Mode B band: ${lk_lo:,.0f}B - ${lk_hi:,.0f}B "
          f"= {pct_m2(lk_lo):.2f}% - {pct_m2(lk_hi):.2f}% of M2   "
          f"[paper: $22B-$136B, 0.10%-0.61%]")

    # Mode A central
    lk_a = leak(DELTA_A, 0.03, 0.15, 0.0)
    print(f"Mode A central: ${lk_a:,.0f}B = {pct_m2(lk_a):.2f}% of M2   "
          f"[paper: ~$16B, 0.07%]")

    # Decline as floors mature (central case, varying s_t)
    print("\nDecline of the leak as the locked-float share s_t rises (Mode B central):")
    for s in [0.0, 0.25, 0.50, 0.75, 0.90]:
        lk = leak(DELTA_B, 0.03, 0.15, s)
        print(f"   s_t={s:>4.2f}  ->  {pct_m2(lk):.2f}% of M2")
    print("   [paper: 0.24 / 0.18 / 0.12 / 0.06 / 0.02 %]")
    print()


# ---------------------------------------------------------------------------
# SECTION 6.5 — structural-buyer valuation premium
#   A* = gross - L_t ;   premium = A* / phi  (against capitalization)
# ---------------------------------------------------------------------------
GROSS = 272.0          # $B/yr gross FDCA equity purchase under Mode B 60/40 = K1 + 0.6*K2
                       # (the 40% K3 dividend is not absorbed into equity). Full line = $447B.
CAP = 69_000.0         # $B total US equity capitalization (order of magnitude)


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
    print("   [paper: $163B/0.24% , $109B/0.16% , $27B/0.04%]")

    # Premium at mid drawdown (A* ~ $109B, 0.16% of cap) across supply elasticity phi
    a_mid = net_absorption(GROSS, 0.60)
    base_pct = 100.0 * a_mid / CAP
    print(f"\nValuation premium at mid drawdown (A*=${a_mid:,.0f}B, {base_pct:.2f}% of cap):")
    for phi in [0.5, 1.0, 2.0]:
        premium = base_pct / phi
        print(f"   phi={phi:>4.1f}  ->  premium = {premium:.2f}% of valuation level")
    print("   [paper: 0.32% / 0.16% / 0.08%]")
    print()




# ---------------------------------------------------------------------------
# GENERAL FORMULA — structural-buyer flow as a share of the index market
#   A jurisdiction recovers its own figure from observable aggregates plus the
#   one policy lever kappa_d; no need to re-derive K1/K2 by hand.
#
#   Budget partition (Neo-Solon 2026e, 4.3):
#       K1_agg + K2_agg + K3_agg = g_r * M2          (the one growth-matched line)
#       K3_agg = kappa_d * (g_r*M2 - K1_agg)         (consumer dividend)
#       K2_agg = (1-kappa_d) * (g_r*M2 - K1_agg)     (locked floor)
#   Structural-buyer (FDCA) equity flow = K1_agg + K2_agg:
#       A* = (1 - kappa_d) * g_r * M2 + kappa_d * K1_agg
#   As a share of the domestic index capitalization M_index:
#       f  = A* / M_index
#   Since K1_agg << K2_agg, the working approximation is:
#       f ~= (1 - kappa_d) * g_r * (M2 / M_index)
# ---------------------------------------------------------------------------
G_R      = 0.02          # real-growth issuance peg
K1_AGG   = 9.0           # $B aggregate citizenship endowment (Neo-Solon 2026a)
KAPPA_D  = 0.40          # Mode B consumer-dividend share (the 60/40 split)


def sb_flow(kappa_d, g_r=G_R, m2=M2, m_index=CAP, k1_agg=K1_AGG):
    """Structural-buyer equity flow as a share of the index market."""
    a_star = (1.0 - kappa_d) * g_r * m2 + kappa_d * k1_agg
    return a_star, 100.0 * a_star / m_index


def section_general():
    print("=" * 70)
    print("GENERAL FORMULA — structural-buyer flow f = A*/M_index")
    print("  A* = (1-kappa_d)*g_r*M2 + kappa_d*K1_agg ;  f ~= (1-kappa_d)*g_r*(M2/M_index)")
    print("=" * 70)
    print(f"  inputs: g_r={G_R:.0%}, M2=${M2:,.0f}B, M_index=${CAP:,.0f}B, K1_agg=${K1_AGG:.0f}B")
    for kd in [0.0, 0.40, 0.60]:
        a, fpct = sb_flow(kd)
        approx = 100.0 * (1 - kd) * G_R * M2 / CAP
        print(f"  kappa_d={kd:.2f}:  A*=${a:,.0f}B  ->  f={fpct:.2f}% of index   (approx no-K1: {approx:.2f}%)")
    print("  [paper: kappa_d=0 -> 0.65% ; 0.40 -> 0.39% ; 0.60 -> 0.27%]")

    # Transactional-circuit (goods) injection under Mode B 60/40 = spillover + dividend
    print("\n  Transactional-circuit injection under Mode B (kappa_d=0.40):")
    spill = leak(DELTA_B, 0.03, 0.15, 0.0)                 # asset-circuit spillover (3.2a)
    k3    = KAPPA_D * (G_R * M2 - K1_AGG)                  # dividend paid into goods circuit
    total = spill + k3
    print(f"     asset-circuit spillover (leak) : ${spill:,.1f}B  = {pct_m2(spill):.2f}% of M2")
    print(f"     K3 dividend (direct to goods)  : ${k3:,.1f}B  = {pct_m2(k3):.2f}% of M2")
    print(f"     total transactional injection  : ${total:,.1f}B  = {pct_m2(total):.2f}% of M2")
    print(f"     [paper: $54.4B/0.24% + $175.3B/0.78% = $229.7B/1.03% of M2; bounded by price-stability locus]")
    print()

if __name__ == "__main__":
    section_3_2a()
    section_6_5()
    section_general()
    print("All illustrative magnitudes reproduce the figures printed in")
    print("Sections 3.2a and 6.5 of Neo-Solon (2026e).")

"""
appendix_A2_debt_trajectory.py
==============================
Replicates Technical Appendix A.2 of the transition paper:
the sovereign-debt transition model and the public-debt-to-GDP trajectory.

Companion to:
  Neo-Solon (2026c). The Citizens Standard: Transition Architecture and
  Migration Mechanics. SSRN 6810741. Technical Appendix A.2.

MECHANISM (paper Section 4.1 / Appendix A.2):
  - The relevant debt is the $31.4T held by the public (102% of GDP), NOT
    the $39T gross total. The $7.6T intragovernmental debt nets out (CRFB).
  - A Legacy Debt Trust refinances the public debt but never expands it.
  - As legacy coupons (~4.5%) roll into refinanced ones (~1.5% real yield),
    the average coupon reprices toward 1.5% by Year 6.
  - The transition-only KT channel issues money calibrated to a price-level
    path (~1.5% of M2/yr) directed to bond redemption (an asset swap),
    operating alongside a primary surplus that phases in to 1.5% of GDP.
  - Public debt is retired by approximately Year 45.

NOTE ON TERMINOLOGY: earlier working drafts called the KT channel "K3-debt."
This module uses the finalized name KT throughout, matching the published paper.
"""

# ── Verified parameters (US data, March-April 2026 vintage) ──
GDP_0        = 30.762e12   # nominal US GDP, BEA April 2026
M2_0         = 22.4e12     # M2, FRED M2SL
DEBT_PUBLIC  = 31.4e12     # debt held by the public, US Treasury / CRFB 2026
DEBT_GROSS   = 39.0e12     # gross federal debt (for reference)
DEBT_INTRAGOV= 7.6e12      # intragovernmental (nets out, per CRFB)

RATE_LEGACY  = 0.045       # legacy average coupon
RATE_NEW     = 0.015       # post-rollover real yield under price stability
ROLLOVER_YRS = 6           # years for average coupon to reprice
G_NOM        = 0.018       # Mode T nominal growth (real growth, price stable)
KT_PCT_M2    = 0.015       # KT calibration: ~1.5% of M2 per year
KT_STOP_DEBT = 2.0e12      # KT operates until the PUBLIC stock is cleared to ~$2T

# NOTE on the KT lifecycle:
#   KT retires the PUBLIC debt to zero (by ~Year 45). It operates while a
#   meaningful public stock remains (here, debt > ~$2T). The narrative "~30%
#   of GDP sunset" marks the point at which KT is no longer strictly necessary
#   for solvency, but the channel continues through the low-debt tail to fully
#   clear the public stock. What remains on the gross books is the ~$7.6T
#   intragovernmental debt — which the Trust never touched (it nets out and is
#   handled by Social Security consolidation, paper Section 8.1). In other
#   words, the mechanism pays the public debt down exactly to the
#   intragovernmental floor (~11% of GDP by Year 45) and stops.


def avg_coupon(yr):
    """Average coupon repricing as the Legacy Trust refinances its stock."""
    legacy_share = max(0.0, 1.0 - yr / ROLLOVER_YRS)
    return legacy_share * RATE_LEGACY + (1 - legacy_share) * RATE_NEW


def primary_surplus_pct(yr):
    """Balanced-budget primary surplus, phasing in to 1.5% of GDP over 25 yrs."""
    if yr < 5:
        return 0.0
    if yr < 15:
        return 0.005
    if yr < 25:
        return 0.010
    return 0.015


def run_trajectory(debt_0=DEBT_PUBLIC, use_kt=True, kt_pct_m2=KT_PCT_M2,
                   k2_diversion=0.0, k2_divert_from_year=20, horizon=70):
    """
    Project the debt trajectory year by year.

    debt_0:        starting debt stock (public debt by default)
    use_kt:        whether the KT channel operates
    kt_pct_m2:     KT issuance as a fraction of M2 per year
    k2_diversion:  optional fraction of K2 diverted to the Trust (default 0;
                   the paper recommends 0 — KT does the work, not citizen K2)
    Returns a list of annual dicts and the first year debt reaches ~0.
    """
    debt = debt_0
    gdp = GDP_0
    m2 = M2_0
    rows = []
    retired_year = None

    for yr in range(horizon + 1):
        coupon = avg_coupon(yr)
        interest = debt * coupon
        surplus = gdp * primary_surplus_pct(yr)

        d_gdp = debt / gdp
        # KT operates while a meaningful public stock remains (cleared to ~$2T).
        # See the KT lifecycle note above: the channel runs through the low-debt
        # tail to fully retire the public debt, leaving the intragovernmental floor.
        kt = m2 * kt_pct_m2 if (use_kt and debt > KT_STOP_DEBT) else 0.0

        # Optional K2 diversion (not recommended; included for sensitivity)
        k2_div = 0.0
        if k2_diversion > 0 and yr >= k2_divert_from_year:
            k2_agg = G_NOM * m2 * (1 - 0.022)  # residual K2 aggregate (K1 funded from the line first)
            k2_div = k2_agg * k2_diversion

        total_available = surplus + kt + k2_div
        principal_retired = max(0.0, total_available - interest)

        rows.append({
            "year": yr,
            "coupon": coupon,
            "interest": interest,
            "surplus": surplus,
            "kt": kt,
            "k2_div": k2_div,
            "principal_retired": principal_retired,
            "debt": debt,
            "gdp": gdp,
            "d_gdp": d_gdp,
        })

        debt = max(0.0, debt - principal_retired)
        if debt <= 1e12 and retired_year is None:
            retired_year = yr
        gdp *= (1 + G_NOM)
        m2 *= (1 + G_NOM)

    return rows, retired_year


def cumulative_kt(rows):
    return sum(r["kt"] for r in rows)


if __name__ == "__main__":
    print("=" * 78)
    print("APPENDIX A.2 — PUBLIC-DEBT-TO-GDP TRAJECTORY UNDER MODE T")
    print("=" * 78)
    print(f"Public debt: ${DEBT_PUBLIC/1e12:.1f}T ({DEBT_PUBLIC/GDP_0*100:.0f}% of GDP); "
          f"gross ${DEBT_GROSS/1e12:.0f}T; intragov ${DEBT_INTRAGOV/1e12:.1f}T (nets out)")
    print(f"KT calibration: {KT_PCT_M2*100:.1f}% of M2/yr; retires public debt to zero (~Year 45),")
    print(f"leaving the ~${DEBT_INTRAGOV/1e12:.1f}T intragovernmental floor (handled by SS consolidation)")
    print()

    rows, retired = run_trajectory()
    print(f"{'Year':<6}{'Coupon':<9}{'KT ($B)':<10}{'Surplus($B)':<13}"
          f"{'Interest($B)':<14}{'Debt ($T)':<12}{'D/GDP':<8}")
    print("-" * 78)
    for yr in [0, 10, 20, 30, 40, 45]:
        r = rows[yr]
        print(f"{yr:<6}{r['coupon']*100:>5.2f}%   ${r['kt']/1e9:>6.0f}    "
              f"${r['surplus']/1e9:>8.0f}    ${r['interest']/1e9:>9.0f}     "
              f"${r['debt']/1e12:>7.1f}     {r['d_gdp']*100:>5.0f}%")
    print()
    print(f"Public debt retired by: Year {retired}")
    print(f"Cumulative KT issuance:  ${cumulative_kt(rows)/1e12:.1f}T")
    print(f"(remainder retired by primary surplus and nominal output growth)")
    print()
    print("vs CBO March 2025 projection: 156% of GDP by 2055 under current law.")

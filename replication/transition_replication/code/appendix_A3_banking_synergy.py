"""
appendix_A3_banking_synergy.py
==============================
Replicates Technical Appendix A.3 of the transition paper (Neo-Solon, 2026c):
the banking-separation / credit-stability model and its synergy with KT.

CLAIMS:
  - Full-reserve transition does not shrink M2; it shifts composition from
    inside money (bank-created) to outside money (sovereign). The KT base
    (1.5% of M2) is therefore stable.
  - Full-reserve conversion removes bank money-creation capacity (~$810B/yr
    credit-at-risk over a 20-year window). KT injects sovereign money during
    the same window, offsetting an estimated 41-59% of that credit-at-risk,
    on top of the Transition Lending Facility's 12-38% coverage.
"""

DEPOSITS = 18.0e12          # total US bank deposits (FDIC 2025 Q4)
RR_CURRENT = 0.10           # current effective reserve ratio
RR_TARGET = 1.00            # full reserve
RESERVE_GAP = DEPOSITS * (RR_TARGET - RR_CURRENT)   # ~$16.2T
CONVERSION_YEARS = 20
CREDIT_AT_RISK = RESERVE_GAP / CONVERSION_YEARS     # ~$810B/yr

M2_0 = 22.4e12
G_NOM = 0.018
KT_PCT_M2 = 0.015
# Domestic share of KT that becomes outside money in the US system
# (foreign central banks ~30% hold proceeds abroad).
DOMESTIC_SHARE = 0.70


def m2_composition(years=range(0, 46, 5)):
    """M2 total grows; inside/outside composition shifts over the 20-yr window
    (Phase 3 of the transition, modeled here as Years 20-40)."""
    rows = []
    for yr in years:
        if yr < 20:
            inside_share = 0.80
            note = "Pre-banking-transition"
        elif yr <= 40:
            progress = (yr - 20) / 20
            inside_share = 0.80 * (1 - progress)
            note = f"Converting ({progress*100:.0f}% done)"
        else:
            inside_share = 0.0
            note = "Full reserve complete"
        m2 = M2_0 * (1 + G_NOM) ** yr
        rows.append({
            "year": yr,
            "m2": m2,
            "inside": m2 * inside_share,
            "outside": m2 * (1 - inside_share),
            "kt": m2 * KT_PCT_M2,
            "note": note,
        })
    return rows


def kt_offset(years=range(20, 41, 5)):
    """Fraction of annual credit-at-risk offset by domestic KT injection
    during the Years 20-40 banking-transition overlap."""
    rows = []
    for yr in years:
        m2 = M2_0 * (1 + G_NOM) ** yr
        domestic_injection = m2 * KT_PCT_M2 * DOMESTIC_SHARE
        rows.append((yr, CREDIT_AT_RISK, domestic_injection,
                     domestic_injection / CREDIT_AT_RISK * 100))
    return rows


if __name__ == "__main__":
    print("=" * 78)
    print("APPENDIX A.3 — BANKING SEPARATION AND KT SYNERGY")
    print("=" * 78)
    print(f"Total deposits: ${DEPOSITS/1e12:.0f}T | reserve gap: ${RESERVE_GAP/1e12:.1f}T "
          f"| credit-at-risk: ${CREDIT_AT_RISK/1e9:.0f}B/yr over {CONVERSION_YEARS}yr")
    print()
    print("M2 composition through the transition (total grows; inside -> outside):")
    print(f"{'Year':<6}{'M2 ($T)':<10}{'Inside ($T)':<13}{'Outside ($T)':<14}{'KT ($B)':<10}{'Note'}")
    print("-" * 78)
    for r in m2_composition():
        print(f"{r['year']:<6}{r['m2']/1e12:>6.1f}    {r['inside']/1e12:>7.1f}      "
              f"{r['outside']/1e12:>7.1f}       {r['kt']/1e9:>5.0f}     {r['note']}")
    print()
    print("KT offset of credit-at-risk (Years 20-40 overlap):")
    print(f"{'Year':<6}{'Credit-at-risk ($B)':<22}{'Domestic KT ($B)':<20}{'Offset'}")
    print("-" * 64)
    offsets = []
    for yr, car, inj, pct in kt_offset():
        offsets.append(pct)
        print(f"{yr:<6}${car/1e9:>6.0f}              ${inj/1e9:>6.0f}              {pct:.0f}%")
    print()
    print(f"KT offsets {min(offsets):.0f}-{max(offsets):.0f}% of annual credit-at-risk,")
    print("complementary to the Transition Lending Facility's 12-38% coverage.")
    print("The two mechanisms are complementary: KT supplies outside-money creation")
    print("precisely as full-reserve conversion removes inside-money creation.")

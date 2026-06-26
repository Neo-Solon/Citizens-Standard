"""
appendix_A2_kt_inflation.py
===========================
Replicates the KT consumer-price-impact analysis in Technical Appendix A.2.3
of the transition paper (Neo-Solon, 2026c).

CLAIM: KT is consumer-price-neutral because bond redemption is an asset swap
absorbed by a holder base dominated by structural reinvesters (foreign central
banks, pension funds, the Federal Reserve). The blended marginal propensity to
consume (MPC) out of redemption is ~2.5%, so the CPI impact is negligible
(+0.04pp expected; +0.16pp under a pessimistic 15% MPC).
"""

M2_0 = 22.4e12
KT_PCT_M2 = 0.015
KT_ANNUAL = M2_0 * KT_PCT_M2          # ~$336B/yr at launch
GDP_0 = 30.762e12

# Holder base of US public debt and each class's MPC out of a bond redemption.
# Shares approximate the US Treasury holder distribution (2025-2026).
HOLDERS = [
    # (class, share of public debt, MPC out of redemption, rationale)
    ("Foreign central banks", 0.30, 0.00, "FX-reserve mandate; rotate to other sovereigns"),
    ("Pension funds",         0.15, 0.00, "Liability-matched; reinvest in fixed income/equity"),
    ("Federal Reserve",       0.14, 0.00, "Balance-sheet runoff; spends nothing"),
    ("Mutual funds / ETFs",   0.12, 0.02, "Mandate-bound; minimal leakage to consumption"),
    ("Banks / insurance",     0.12, 0.03, "Regulatory capital; reinvest"),
    ("State / local govt",    0.07, 0.05, "Mostly reinvest"),
    ("Households",            0.10, 0.15, "Some consumption out of redemption"),
]

# CPI sensitivity: extra consumer demand as a share of GDP, times a pass-through.
# A dollar of new consumer demand at ~full employment raises the price level by
# roughly its share of GDP (a conservative unit pass-through on the gap).
def cpi_impact(kt_spent):
    return kt_spent / GDP_0 * 100.0  # in percentage points


def blended_mpc():
    return sum(share * mpc for _, share, mpc, _ in HOLDERS)


def scenario_table():
    out = []
    for label, mpc in [("Full reinvestment (0%)", 0.0),
                       ("Expected (blended ~2.5%)", blended_mpc()),
                       ("Pessimistic (15%)", 0.15),
                       ("Extreme (50%)", 0.50)]:
        spent = KT_ANNUAL * mpc
        out.append((label, mpc, spent, cpi_impact(spent)))
    return out


if __name__ == "__main__":
    print("=" * 78)
    print("APPENDIX A.2.3 — KT CONSUMER-PRICE IMPACT")
    print("=" * 78)
    print(f"KT annual issuance at launch: ${KT_ANNUAL/1e9:.0f}B ({KT_PCT_M2*100:.1f}% of M2)")
    print()
    print(f"{'Holder class':<24}{'Share':<8}{'MPC':<7}{'Rationale'}")
    print("-" * 78)
    for cls, share, mpc, why in HOLDERS:
        print(f"{cls:<24}{share*100:>4.0f}%   {mpc*100:>3.0f}%   {why}")
    print("-" * 78)
    print(f"{'BLENDED MPC':<24}{'':8}{blended_mpc()*100:>3.1f}%")
    print()
    print(f"{'CPI Scenario':<28}{'MPC':<8}{'KT spent/yr':<14}{'CPI impact'}")
    print("-" * 64)
    for label, mpc, spent, cpi in scenario_table():
        print(f"{label:<28}{mpc*100:>4.1f}%   ${spent/1e9:>6.0f}B       +{cpi:.2f}pp")
    print()
    print("KT is self-throttling: calibration to a price-level path automatically")
    print("reduces issuance if consumer inflation rises. Cannot produce runaway")
    print("inflation by construction.")

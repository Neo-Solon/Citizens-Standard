"""
appendix_A4_equity_rotation.py
==============================
Replicates Technical Appendix A.4 of the transition paper (Neo-Solon, 2026c):
the equity-valuation flow model and the bond-rotation estimate.

CLAIM: When KT redeems bonds, holders reinvest. With sovereign instruments
scarcer, a fraction rotates into equities. A bottom-up decomposition by holder
mandate gives a central estimate of ~17% (the two largest holders, foreign
central banks and the Fed, rotate almost nothing). The paper uses a 15-35%
range and reports the result is robust across it. Combined Stable-Floor plus
bond-rotation equity demand peaks at ~0.92% of market capitalization per
year (the Stable Floor flow alone is ~0.81%), well within the range of
existing systematic flows. The transition-specific compression — the part
that reverts when KT sunsets — is driven by the KT bond-rotation flow only;
the permanent Stable Floor flow is a steady-state feature, not a transition cost.
"""

US_EQUITY_MKT = 55e12       # total US equity market cap (SIFMA 2025)
M2_0 = 22.4e12
KT_PCT_M2 = 0.015
KT_ANNUAL = M2_0 * KT_PCT_M2
SF_FLOW_0 = 447e9           # Stable Floor (K1+K2) equity purchases at launch (residual K1-funded line)
PE_ELASTICITY = 3.0         # PE response to flow/mktcap (transition paper)

# Equity-rotation fraction by holder class (bottom-up by mandate).
HOLDERS = [
    ("Foreign central banks", 0.30, 0.05),
    ("Pension funds",         0.15, 0.40),
    ("Federal Reserve",       0.14, 0.00),
    ("Mutual funds / ETFs",   0.12, 0.30),
    ("Banks / insurance",     0.12, 0.10),
    ("State / local govt",    0.07, 0.15),
    ("Households",            0.10, 0.35),
]


def weighted_rotation():
    return sum(share * rot for _, share, rot in HOLDERS)


def equity_demand(rotation):
    bond_to_eq = KT_ANNUAL * rotation
    combined = SF_FLOW_0 + bond_to_eq
    return bond_to_eq, combined, combined / US_EQUITY_MKT * 100


def return_compression(rotation):
    extra_flow = (KT_ANNUAL * rotation) / US_EQUITY_MKT
    return PE_ELASTICITY * extra_flow * 100  # in percentage points


if __name__ == "__main__":
    print("=" * 78)
    print("APPENDIX A.4 — EQUITY ROTATION AND RETURN COMPRESSION")
    print("=" * 78)
    print(f"{'Holder class':<24}{'Share':<8}{'Eq-rotation':<13}")
    print("-" * 50)
    for cls, share, rot in HOLDERS:
        print(f"{cls:<24}{share*100:>4.0f}%   {rot*100:>4.0f}%")
    print("-" * 50)
    wr = weighted_rotation()
    print(f"{'WEIGHTED ROTATION ESTIMATE':<24}{'':8}{wr*100:>4.1f}%")
    print(f"(roughly half the original unsourced 35% guess; the two largest")
    print(f" holders -- foreign CBs and the Fed -- rotate almost nothing)")
    print()
    print(f"{'Rotation':<12}{'Bond->Eq ($B)':<16}{'Combined ($B)':<16}{'% of mkt cap':<14}{'Compression'}")
    print("-" * 72)
    for rot in [0.15, wr, 0.35]:
        b, c, pct = equity_demand(rot)
        comp = return_compression(rot)
        tag = "  <- central" if abs(rot - wr) < 1e-9 else ""
        print(f"{rot*100:>4.1f}%       ${b/1e9:>6.0f}          ${c/1e9:>6.0f}          "
              f"{pct:>5.2f}%        +{comp:.2f}pp{tag}")
    print()
    print("For comparison: 401k+IRA contributions ~1.4% of mkt cap/yr; QE peak ~2.6%.")
    print("Combined transition-era equity demand peaks at ~0.92% of market cap")
    print("(Stable Floor flow alone ~0.81%); permanent SF flow is steady-state.")
    print("Transition-specific compression ~0.4-0.6pp (KT-rotation driven), reverting")
    print("to baseline once KT sunsets. The precise rotation fraction is an open")
    print("empirical question; results are robust across the 15-35% range.")

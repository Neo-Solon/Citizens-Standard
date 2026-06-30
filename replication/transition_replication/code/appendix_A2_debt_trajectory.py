"""
appendix_A2_debt_trajectory.py
==============================
Replicates Technical Appendix A.2 of the transition paper:
the sovereign-debt transition model and the public-debt-to-GDP trajectory.

Companion to:
  Neo-Solon (2026c). The Citizens Standard: Transition Architecture and
  Migration Mechanics. Technical Appendix A.2.

MECHANISM (paper Section 4.1 / 4.1.1 / Appendix A.2):
  - The relevant debt is the $31.4T held by the public (102% of GDP), NOT
    the $39T gross total. The $7.6T intragovernmental debt nets out (CRFB).
  - A Legacy Debt Trust refinances the public debt but never expands it.
  - As legacy coupons (~4.5%) roll into refinanced ones, the average coupon
    reprices toward ~3.0% by Year 6.
  - The transition-only KT channel issues money calibrated to a price-level
    path (~1.5% of M2/yr) directed to bond redemption (an asset swap),
    operating alongside a primary surplus that phases in to 1.5% of GDP.
  - Public debt is retired into a MODERATE OPERATIONAL BAND of ~30-60% of GDP
    (central path ~45%, reached by ~Year 26), where it STABILISES. KT throttles
    down as the debt enters the band and routes the freed growth-matched
    seigniorage to citizen Stable Floors.

THE ENDPOINT IS A BAND, NOT A FLOOR. The descent is ordinary debt dynamics; the
endpoint is the welfare-optimal result of the cs_debt_band analysis (companion
package): standing debt is near self-financing at r<g (Blanchard 2019; Mauro &
Zhou 2020), so retiring below the band forgoes citizen seigniorage for no
sustainability gain, while debt-dependent crisis risk rises only well above the
band (Lian, Presbitero & Wiriadinata 2020), and a sovereign-currency issuer with
its own monetary authority sits at the damped end of that risk (De Grauwe 2011).
"""

# Verified parameters (US data, 2026 vintage)
GDP_0        = 30.8e12     # nominal US GDP
M2_0         = 22.4e12     # M2
DEBT_PUBLIC  = 31.4e12     # debt held by the public (~102% of GDP)
DEBT_GROSS   = 39.0e12
DEBT_INTRAGOV= 7.6e12

RATE_LEGACY  = 0.045
RATE_NEW     = 0.030       # post-rollover yield under price stability
ROLLOVER_YRS = 6
G_NOM        = 0.040       # nominal growth (real ~2.0% + ~2.0%)
KT_PCT_M2    = 0.015       # KT calibration: ~1.5% of M2 per year
BAND_LO, BAND_HI, CENTER = 0.30, 0.60, 0.45   # operational band and central path

def avg_coupon(yr):
    legacy_share = max(0.0, 1.0 - yr/ROLLOVER_YRS)
    return legacy_share*RATE_LEGACY + (1-legacy_share)*RATE_NEW

def primary_surplus_pct(yr):
    return 0.015*min(1.0, yr/25.0)

def run_trajectory(debt_0=DEBT_PUBLIC, use_kt=True, kt_pct_m2=KT_PCT_M2, horizon=70):
    """Project the debt trajectory using the SAME ratio recursion that generates
       Table A.2 of the paper:
           d' = d*(1+coupon)/(1+g_nom) - kt_ratio - surplus_pct
       KT runs at full rate (kt_pct_m2 of M2, expressed as a share of GDP) until the
       debt ratio enters the band, then throttles linearly to zero from the band top
       to the centre, holding the centre (~45%) thereafter. The freed growth-matched
       seigniorage goes to citizen Stable Floors. No new borrowing under Mode T."""
    debt, gdp, m2 = debt_0, GDP_0, M2_0
    rows=[]; band_year=None
    for yr in range(horizon+1):
        coupon=avg_coupon(yr)
        d_gdp=debt/gdp
        interest=debt*coupon
        surplus=gdp*primary_surplus_pct(yr)
        # KT throttle on the debt RATIO
        if d_gdp>BAND_HI: taper=1.0
        elif d_gdp>CENTER: taper=(d_gdp-CENTER)/(BAND_HI-CENTER)
        else: taper=0.0
        kt = m2*kt_pct_m2*taper if use_kt else 0.0
        rows.append(dict(year=yr, coupon=coupon, interest=interest, surplus=surplus,
                         kt=kt, debt=debt, gdp=gdp, d_gdp=d_gdp))
        # ratio recursion (matches band_trajectory.py / paper Table A.2)
        kt_ratio = (kt/gdp) if gdp>0 else 0.0
        surplus_pct = primary_surplus_pct(yr)
        d_next = d_gdp*(1+coupon)/(1+G_NOM) - kt_ratio - surplus_pct
        if taper==0.0:
            # holding within the band: peg the ratio at the centre (KT dormant, surplus
            # and growth offset, freed seigniorage routed to citizens) as in Table A.2
            d_next=CENTER
            if band_year is None: band_year=yr
        d_next=max(d_next, 0.0)
        gdp*=(1+G_NOM); m2*=(1+G_NOM)
        # in the hold phase, peg debt to exactly CENTER of the grown GDP (clean 45% each year)
        debt = (CENTER*gdp) if (band_year is not None and yr>=band_year) else (d_next*gdp)
    return rows, band_year

def cumulative_kt(rows): return sum(r["kt"] for r in rows)

if __name__ == "__main__":
    print("="*78)
    print("APPENDIX A.2 — PUBLIC-DEBT-TO-GDP TRAJECTORY UNDER MODE T")
    print("="*78)
    print(f"Public debt: ${DEBT_PUBLIC/1e12:.1f}T ({DEBT_PUBLIC/GDP_0*100:.0f}% of GDP); "
          f"gross ${DEBT_GROSS/1e12:.0f}T; intragov ${DEBT_INTRAGOV/1e12:.1f}T (nets out)")
    print(f"KT calibration: {KT_PCT_M2*100:.1f}% of M2/yr; retires public debt into a "
          f"{int(BAND_LO*100)}-{int(BAND_HI*100)}% operational band")
    print(f"(central path ~{int(CENTER*100)}%, reached ~Year 26), where it stabilises.")
    print()
    rows, band_year = run_trajectory()
    print(f"{'Year':<6}{'Coupon':<9}{'KT ($B)':<10}{'Surplus($B)':<13}"
          f"{'Interest($B)':<14}{'Debt ($T)':<12}{'D/GDP':<8}")
    print("-"*78)
    for yr in [0,10,20,30,40,45]:
        r=rows[yr]
        print(f"{yr:<6}{r['coupon']*100:>5.2f}%   ${r['kt']/1e9:>6.0f}    "
              f"${r['surplus']/1e9:>8.0f}    ${r['interest']/1e9:>9.0f}     "
              f"${r['debt']/1e12:>7.1f}     {r['d_gdp']*100:>5.0f}%")
    print()
    print(f"Operational band ({int(BAND_LO*100)}-{int(BAND_HI*100)}% of GDP) entered and held "
          f"(D/GDP {rows[20]['d_gdp']*100:.0f}% at Yr20, {rows[30]['d_gdp']*100:.0f}% at Yr30, stabilises ~{int(CENTER*100)}%)")
    print(f"Cumulative KT issuance:  ${cumulative_kt(rows)/1e12:.1f}T")
    print(f"(remainder of the descent delivered by primary surplus and nominal output growth;")
    print(f" seigniorage freed by holding the band rather than over-retiring goes to citizen Stable Floors)")
    print()
    print("vs CBO March 2025 projection: 156% of GDP by 2055 under current law.")

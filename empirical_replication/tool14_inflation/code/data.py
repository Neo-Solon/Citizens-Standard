"""
data.py
=======
Empirically grounded inputs for the Tool 14 inflation counterfactual
(Technical Appendix to the macro / counterfactual paper, Neo-Solon 2026).

EVERY number in this file is sourced. See AUDIT.md for full provenance.
Nothing here is fitted to make the framework look good; the actual inflation
series are raw BLS data and the demand/supply split is taken from a published
Federal Reserve decomposition, NOT tuned.

Primary sources
---------------
* Actual CPI ............ U.S. BLS, CPI-U, All items, U.S. city average,
                         12-month change, not seasonally adjusted (BLS series
                         CUUR0000SA0). Retrieved via BLS / usinflationcalculator
                         monthly tables.
* Demand/supply split .. Shapiro, Adam Hale (2022b), "How Much Do Supply and
                         Demand Drive Inflation?" FRBSF Economic Letter 2022-15
                         (June 21, 2022); and the SF Fed "Supply- and
                         Demand-Driven PCE Inflation" data page.
* 1980 attribution ..... Federal Reserve History, "The Great Inflation"
                         (origins: "policies that allowed excessive growth in
                         the supply of money"); Federal Reserve History,
                         "Recession of 1981-82".
* Policy-cost facts .... Fed funds: Federal Reserve History / Bankrate.
                         Unemployment: U.S. BLS (10.8%, Nov-Dec 1982).
                         Mortgages: Freddie Mac PMMS (30-yr fixed,
                         3.22% Jan 2022 -> 7.08% Oct 2022).
                         Sacrifice ratio ~2.5: standard Volcker-disinflation
                         estimate (Goodfriend-King 2005 and successors).
"""

# ----------------------------------------------------------------------------
# 1. ACTUAL CPI-U, 12-month % change, NOT seasonally adjusted (BLS).
#    These are raw data, used only to define the shock and the actual path.
# ----------------------------------------------------------------------------

# 2021-2023 surge. 36 months, Jan 2021 .. Dec 2023.
CPI_2022 = [
    1.4, 1.7, 2.6, 4.2, 5.0, 5.4, 5.4, 5.3, 5.4, 6.2, 6.8, 7.0,   # 2021
    7.5, 7.9, 8.5, 8.3, 8.6, 9.1, 8.5, 8.3, 8.2, 7.7, 7.1, 6.5,   # 2022 (peak 9.1, Jun)
    6.4, 6.0, 5.0, 4.9, 4.0, 3.0, 3.2, 3.7, 3.7, 3.2, 3.1, 3.4,   # 2023
]
START_2022 = "Jan 2021"

# 1972-1983 Great Inflation through Volcker. 138 months, Jan 1972 .. Jun 1983.
# Computed as 12-month % change directly from the BLS CPI-U monthly index
# (1982-84=100, Table 24): so the framework can experience the BUILD-UP from
# low inflation (3.3% in 1972) through both oil shocks to the 14.8% peak (Mar
# 1980) -- which is what lets the structural model test PREVENTION, not just a
# drop-in. Anchors: 3.3% Jan 1972, 12.3% Dec 1974, 14.8% Mar 1980, 2.6% Jun 1983.
CPI_1980 = [
    3.3,3.5,3.5,3.5,3.2,2.7,2.9,2.9,3.2,3.4,3.7,3.4,          # 1972
    3.6,3.9,4.6,5.1,5.5,6.0,5.7,7.4,7.4,7.8,8.3,8.7,          # 1973
    9.4,10.0,10.4,10.1,10.7,10.9,11.5,10.9,11.9,12.1,12.2,12.3,  # 1974 (oil shock I)
    11.8,11.2,10.3,10.2,9.5,9.4,9.7,8.6,7.9,7.4,7.4,6.9,      # 1975
    6.7,6.3,6.1,6.0,6.2,6.0,5.4,5.7,5.5,5.5,4.9,4.9,          # 1976
    5.2,5.9,6.4,7.0,6.7,6.9,6.8,6.6,6.6,6.4,6.7,6.7,          # 1977
    6.8,6.4,6.6,6.5,7.0,7.4,7.7,7.8,8.3,8.9,8.9,9.0,          # 1978
    9.3,9.9,10.1,10.5,10.9,10.9,11.3,11.8,12.2,12.1,12.6,13.3,  # 1979 (oil shock II)
    13.9,14.2,14.8,14.7,14.4,14.4,13.1,12.9,12.6,12.8,12.6,12.5,  # 1980 (peak 14.8, Mar)
    11.8,11.4,10.5,10.0,9.8,9.6,10.8,10.8,11.0,10.1,9.6,8.9,  # 1981
    8.4,7.6,6.8,6.5,6.7,7.1,6.4,5.9,5.0,5.1,4.6,3.8,          # 1982 (Volcker crush)
    3.7,3.5,3.6,3.9,3.5,2.6,                                  # 1983 H1
]
START_1980 = "Jan 1972"

# ----------------------------------------------------------------------------
# 2. DEMAND / SUPPLY DECOMPOSITION (the share the framework can vs cannot damp).
#
#    The framework's rule-bound issuance never creates a demand/monetary surge,
#    and Tool 14 actively retires money; so it removes the DEMAND-driven share
#    of an inflation. It cannot stop a SUPPLY shock (energy, supply chains).
#
#    2022 now uses the ACTUAL published monthly decomposition (no judgment call).
#    1980 predates the series (begins 1998), so it falls back to the literature
#    attribution band, disclosed as such.
# ----------------------------------------------------------------------------

# SF Fed (Shapiro) monthly YoY decomposition of HEADLINE PCE inflation, in pp.
# Source: FRBSF "Supply- and Demand-Driven PCE Inflation", Figure 3 (12-month
# headline), downloaded chart CSV (supply-demand-pce-headline-yoy-chart-3.csv).
# Keyed by month_index in CPI_2022 (0 = Jan 2021). Series begins 2021m3 (idx 2);
# idx 0-1 are near-anchor and inherit idx 2. Tuple = (demand, ambiguous, supply).
SFFED_2022 = {
    2:(0.16,1.22,1.34),  3:(1.10,1.31,1.31),  4:(1.36,1.33,1.44),  5:(1.54,1.24,1.58),
    6:(1.58,1.30,1.64),  7:(1.65,1.19,1.79),  8:(1.61,1.34,1.82),  9:(1.94,1.48,1.94),
   10:(2.26,1.47,2.20), 11:(2.22,1.39,2.53), 12:(2.13,1.27,2.85), 13:(2.36,1.07,3.09),
   14:(2.62,1.05,3.22), 15:(2.47,1.08,3.10), 16:(2.67,0.98,3.10), 17:(2.72,1.09,3.36),
   18:(2.81,0.82,3.08), 19:(2.84,0.86,2.90), 20:(2.84,0.68,3.10), 21:(2.77,0.64,3.01),
   22:(2.51,0.59,2.90), 23:(2.22,0.59,2.69), 24:(2.53,0.44,2.53), 25:(2.35,0.41,2.43),
   26:(1.84,0.42,2.19), 27:(1.94,0.35,2.19), 28:(1.63,0.24,2.13), 29:(1.56,0.18,1.55),
   30:(1.31,0.50,1.59), 31:(1.36,0.46,1.61), 32:(1.44,0.58,1.42), 33:(1.26,0.45,1.31),
   34:(1.18,0.47,1.12), 35:(1.32,0.40,1.05),
}

def demand_share_2022(month_index, ambiguous_weight=0.0):
    """Removable (demand-driven) fraction from SF Fed data, month by month.
    ambiguous_weight allocates the 'ambiguous' bucket: 0.0 = demand only
    (most conservative; highest framework peak), 1.0 = all ambiguous removable."""
    rec = SFFED_2022.get(month_index, SFFED_2022[2])
    dem, amb, sup = rec
    total = dem + amb + sup
    return (dem + ambiguous_weight * amb) / total if total > 0 else 0.0

# 1980: no SF Fed series. Federal Reserve History attributes the Great Inflation
# primarily to excessive money growth, so the framework-removable share is high.
# This is a literature attribution, NOT a category decomposition -- disclosed.
DEMAND_SHARE_1980 = {"low": 0.55, "central": 0.70, "high": 0.80}

# ----------------------------------------------------------------------------
# 3. FRAMEWORK CONSTANTS (from the architecture/macro papers; not tuned here).
# ----------------------------------------------------------------------------
ANCHOR_CPI      = 1.0     # near-zero price-stability anchor (Mode B ~0-2%); pp
TRIGGER_OVER    = 3.0     # Tool 14 fires when CPI > anchor + 3pp (paper trigger)
M2_LEVEL        = 22.4e12 # USD, M2 at framework launch scale (matches kt appendix)
GDP_LEVEL       = 30.762e12  # USD (matches kt appendix)
TOOL14_CAP_PCT  = 0.03    # Tool 14 ceiling: retire up to 3% of M2 per year
# Quantity-theoretic pass-through: a dollar of demand withdrawn lowers the price
# level by ~its share of GDP (the same unit pass-through used in the KT
# consumer-price appendix, appendix_A2_kt_inflation.py).
PASS_THROUGH    = 1.0

# Tool 14's maximum annual CPI pull, in percentage points, from retiring money:
#   (cap * M2) / GDP * pass_through * 100
TOOL14_MAX_PULL_PP = TOOL14_CAP_PCT * M2_LEVEL / GDP_LEVEL * PASS_THROUGH * 100.0
# ~2.18pp/yr of additional disinflation capacity at launch scale.

# ----------------------------------------------------------------------------
# 4. POLICY-COST FACTS (the conventional cure, for the contrast; all sourced).
# ----------------------------------------------------------------------------
POLICY = {
    "2022": {
        "actual_peak": 9.1, "peak_when": "Jun 2022",
        "ffr": "0.1% -> 5.3%", "ffr_note": "7 hikes; first only after CPI passed 8%",
        "cost": "30-yr mortgage 3.2% -> 7.1%", "cost_note": "Freddie Mac PMMS, 2022",
        "lag": "first hike Mar 2022, after CPI already 8%+",
    },
    "1980": {
        "actual_peak": 14.8, "peak_when": "Mar 1980",
        "ffr": "~19%", "ffr_note": "Fed funds peak, Jun 1981",
        "cost": "10.8% unemployment", "cost_note": "BLS, Nov-Dec 1982",
        "lag": "stop-go: eased in 1980, re-tightened 1981",
        "sacrifice_ratio": 2.5,  # unemployment-point-years per point of disinflation
    },
}

EPISODES = {
    "2022": {"cpi": CPI_2022, "start": START_2022, "share_mode": "data",
             "share_fn": demand_share_2022, "demand_band": DEMAND_SHARE_1980},  # band fallback unused for 2022
    "1980": {"cpi": CPI_1980, "start": START_1980, "share_mode": "literature",
             "demand": DEMAND_SHARE_1980},
}

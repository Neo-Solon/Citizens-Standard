"""
authoritative_newcitizens.py
============================
Annual U.S. *new-citizen* counts used to calibrate the residual K2 channel.

The Citizens Standard issues new base money each year up to the real-growth
"line":  K1_agg + K2_agg = g_r * M2.  K1 is the per-citizen citizenship deposit
(2.5% of GDP per capita) paid to every new citizen; K2 is the *residual* growth
budget after K1, spread across the whole population.  Computing the residual
therefore requires the annual count of new citizens = births + naturalizations.

Sources
-------
Births (calendar year, final counts):
    National Center for Health Statistics (NCHS), National Vital Statistics
    System, natality files. 1960-2024. 2007 is the modern peak (4,316,233);
    2024 final = 3,628,934. Pre-1972 from the 50% sample, scaled to totals.

Naturalizations (fiscal year):
    DHS Office of Homeland Security Statistics (OHSS) / USCIS, Yearbook of
    Immigration Statistics and Annual Flow Reports. Anchor years below; gap
    years linearly interpolated. Cross-checks: FY2024 = 818,500; FY2023 =
    878,460; FY2022 = 969,380; 2008 peak = 1,046,539; 2020 trough = 628,260;
    official 2010-2019 mean = 730,100 (this series' 2010-2019 mean = 729k).

Naturalization age adjustment
-----------------------------
Naturalized citizens receive the citizenship deposit pro-rated to the years
remaining to the compounding horizon, per the framework rule K1_nat = K1 *
(65 - a)/65.  Mean naturalization age ~34 (OHSS), giving a factor (65-34)/65.
Births receive the full deposit (a = 0).
"""

from authoritative_data import POPULATION_M

# ---- Births, thousands (NCHS NVSS, calendar year) ----
BIRTHS_THOUSANDS = {
    1960: 4258, 1961: 4268, 1962: 4167, 1963: 4098, 1964: 4027, 1965: 3760,
    1966: 3606, 1967: 3521, 1968: 3502, 1969: 3600, 1970: 3731, 1971: 3556,
    1972: 3258, 1973: 3137, 1974: 3160, 1975: 3144, 1976: 3168, 1977: 3327,
    1978: 3333, 1979: 3494, 1980: 3612, 1981: 3629, 1982: 3681, 1983: 3639,
    1984: 3669, 1985: 3761, 1986: 3757, 1987: 3809, 1988: 3910, 1989: 4041,
    1990: 4158, 1991: 4111, 1992: 4065, 1993: 4000, 1994: 3953, 1995: 3900,
    1996: 3891, 1997: 3881, 1998: 3942, 1999: 3959, 2000: 4059, 2001: 4026,
    2002: 4022, 2003: 4090, 2004: 4112, 2005: 4138, 2006: 4266, 2007: 4316,
    2008: 4248, 2009: 4131, 2010: 3999, 2011: 3954, 2012: 3953, 2013: 3932,
    2014: 3988, 2015: 3978, 2016: 3946, 2017: 3856, 2018: 3792, 2019: 3748,
    2020: 3614, 2021: 3664, 2022: 3667, 2023: 3596, 2024: 3629,
}

# ---- Naturalizations, thousands (DHS/OHSS/USCIS, fiscal year). Anchors; gaps interpolated. ----
NATURALIZATIONS_ANCHOR_THOUSANDS = {
    1960: 119, 1965: 105, 1970: 110, 1975: 142, 1980: 165, 1985: 244,
    1990: 270, 1995: 488, 1996: 1041, 1997: 598, 1998: 463, 1999: 837,
    2000: 888, 2001: 613, 2002: 573, 2003: 463, 2004: 537, 2005: 604,
    2006: 702, 2007: 660, 2008: 1047, 2009: 744, 2010: 620, 2011: 694,
    2012: 758, 2013: 779, 2014: 654, 2015: 730, 2016: 753, 2017: 707,
    2018: 762, 2019: 834, 2020: 625, 2021: 814, 2022: 969, 2023: 880,
    2024: 819,
}

NATURALIZATION_MEAN_AGE = 34          # OHSS; pro-rate factor = (65 - age)/65
COMPOUNDING_HORIZON     = 65
DATA_LAST_YEAR          = 2024


def naturalizations_thousands(year):
    """Naturalizations (thousands) with linear interpolation on gap years."""
    y = min(year, DATA_LAST_YEAR)
    a = NATURALIZATIONS_ANCHOR_THOUSANDS
    if y in a:
        return float(a[y])
    ks = sorted(a)
    lo = max(k for k in ks if k < y)
    hi = min(k for k in ks if k > y)
    f = (y - lo) / (hi - lo)
    return a[lo] + f * (a[hi] - a[lo])


def new_citizens(year):
    """Gross new citizens (persons) = births + naturalizations.

    For projection years (> DATA_LAST_YEAR) the gross new-citizen RATE is held
    at its last observed value and applied to the projected population, so the
    count tracks population growth in the forward scenario.
    """
    if year <= DATA_LAST_YEAR:
        b = BIRTHS_THOUSANDS.get(year, BIRTHS_THOUSANDS[DATA_LAST_YEAR])
        return (b + naturalizations_thousands(year)) * 1000.0
    rate = new_citizens(DATA_LAST_YEAR) / (POPULATION_M[DATA_LAST_YEAR] * 1e6)
    return rate * (POPULATION_M.get(year, POPULATION_M[DATA_LAST_YEAR]) * 1e6)


def _deposit_weighted_new_citizens(year):
    """Births at full deposit + naturalizations pro-rated by (65 - age)/65."""
    prorate = (COMPOUNDING_HORIZON - NATURALIZATION_MEAN_AGE) / COMPOUNDING_HORIZON
    if year <= DATA_LAST_YEAR:
        b = BIRTHS_THOUSANDS.get(year, BIRTHS_THOUSANDS[DATA_LAST_YEAR]) * 1000.0
        n = naturalizations_thousands(year) * 1000.0
        return b + n * prorate
    # forward: hold the deposit-weighted rate at its last observed value
    b = BIRTHS_THOUSANDS[DATA_LAST_YEAR] * 1000.0
    n = naturalizations_thousands(DATA_LAST_YEAR) * 1000.0
    rate = (b + n * prorate) / (POPULATION_M[DATA_LAST_YEAR] * 1e6)
    return rate * (POPULATION_M.get(year, POPULATION_M[DATA_LAST_YEAR]) * 1e6)


def k1_residual_deduction_per_capita(year, gdp_pc_nom_dollars, pop_persons, k1_fraction):
    """Per-citizen reduction applied to K2 so that K1_agg + K2_agg = g_r * M2.

    = (deposit-weighted new citizens * K1 deposit) / population
    where K1 deposit = gdp_pc * k1_fraction.  Births full, naturalizations
    pro-rated by (65 - mean_age)/65.
    """
    k1_agg = _deposit_weighted_new_citizens(year) * gdp_pc_nom_dollars * k1_fraction
    return k1_agg / pop_persons

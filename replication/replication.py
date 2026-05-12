"""
replication.py
==============
Replication code for:

  Neo-Solon (2026). "The Citizens Standard as Counterfactual Benchmark:
  Empirical Analysis of an Alternative US Monetary Architecture, 1960–2055."
  SSRN Working Paper. https://papers.ssrn.com/sol3/papers.cfm?abstract_id=6735078

Produces all figures reported in Tables 1, 2, 3, and Section 4.5.

DATA SOURCES (all public, no API key required)
-----------------------------------------------
S&P 500 nominal total returns 1960–2024:
  Damodaran, Aswath. "Historical Returns on Stocks, Bonds and Bills: 1928–2024."
  NYU Stern, January 2026.
  https://pages.stern.nyu.edu/~adamodar/New_Home_Page/datafile/histretSP.html

S&P 500 total return 2025: +17.9%
  Bloomberg / RBC Wealth Management, January 2026.

CPI-U (Dec-Dec, all items):
  Bureau of Labor Statistics. 2024: 2.9%, 2025: 2.7%.
  https://www.bls.gov/cpi/

Nominal GDP (GDPA series):
  Bureau of Economic Analysis / FRED. 2025: $30,762.1B.
  https://fred.stlouisfed.org/series/GDPA

M2 money supply (M2SL series, annual averages):
  Federal Reserve Bank of St. Louis / FRED.
  https://fred.stlouisfed.org/series/M2SL

Population (mid-year estimates):
  US Census Bureau.
  https://www.census.gov/programs-surveys/popest.html

Retirement account benchmarks:
  Federal Reserve Board. Survey of Consumer Finances, 2022.
  Age cohort 65-74, retirement account balances.
  Adjusted for DB pension wealth per BLS Employee Benefits Survey.

Social Security benefits:
  SSA. 2025 Annual Report of the Board of Trustees.
  Full benefits assumed for cohorts retiring before 2034 trust fund depletion;
  23% reduction for cohorts retiring 2034+.

METHODOLOGY
-----------
1. K1 = 2.5% of GDP per capita at birth year (nominal dollars)
2. K2 = max(0, nominal GDP growth rate - CPI rate) * prior-year M2 * 0.5 / population
   (i.e., half of real GDP growth times prior-year M2, per living citizen)
3. All nominal deposits deflated to December 2025 purchasing power using the
   Dec-Dec CPI chain BEFORE compounding. This ensures all Stable Floor balances
   are directly comparable to 2025 retirement-account balances.
4. Compounding: real return = (1 + nominal S&P return) / (1 + CPI rate) - 1
   Applied year-by-year to the real (2025$) running balance.
5. Post-2025 projected years use central scenario: 4.5% real return.
   Pessimistic: 3.0% real. Historical: 6.5% real.
6. Post-2025 GDP projected at 4.0% nominal growth (CBO LT Budget Outlook 2025).
   Post-2025 M2 projected at 4.5% nominal growth.
   Post-2025 population at 0.4% annual growth.
   Post-2025 CPI at 2.5% (Fed target).

STRESS TEST METHODOLOGY
-----------------------
Depression sequence: S&P 500 nominal returns 1929–1945 (Damodaran) substituted
  for ages 25–41 of each cohort's working life.
  Depression CPI from BLS historical tables.

Stagflation sequence: S&P 500 nominal returns 1966–1982 (Damodaran) substituted
  for ages 25–41 of each cohort's working life.
  Stagflation CPI from BLS historical tables.

USAGE
-----
  python replication.py

Prints all tables to stdout. No external dependencies required.
Python 3.7+ only.
"""

# ── Data ──────────────────────────────────────────────────────────────────

# S&P 500 nominal total returns (%) — Damodaran Jan 2026 + Bloomberg 2025
SP_NOM = {
    1960: 0.34,  1961: 26.64, 1962: -8.81, 1963: 22.61, 1964: 16.42,
    1965: 12.40, 1966: -9.97, 1967: 23.80, 1968: 10.81, 1969: -8.24,
    1970:  3.56, 1971: 14.22, 1972: 18.76, 1973:-14.31, 1974:-25.90,
    1975: 37.00, 1976: 23.83, 1977: -6.98, 1978:  6.51, 1979: 18.52,
    1980: 31.74, 1981: -4.70, 1982: 20.42, 1983: 22.34, 1984:  6.15,
    1985: 31.24, 1986: 18.49, 1987:  5.81, 1988: 16.54, 1989: 31.48,
    1990: -3.06, 1991: 30.23, 1992:  7.49, 1993:  9.97, 1994:  1.33,
    1995: 37.20, 1996: 22.68, 1997: 33.10, 1998: 28.34, 1999: 20.89,
    2000: -9.03, 2001:-11.85, 2002:-21.97, 2003: 28.36, 2004: 10.74,
    2005:  4.83, 2006: 15.61, 2007:  5.48, 2008:-36.55, 2009: 25.94,
    2010: 14.82, 2011:  2.10, 2012: 15.89, 2013: 32.15, 2014: 13.52,
    2015:  1.38, 2016: 11.77, 2017: 21.61, 2018: -4.23, 2019: 31.33,
    2020: 18.02, 2021: 28.47, 2022:-18.17, 2023: 26.06, 2024: 25.00,
    2025: 17.78,  # Damodaran NYU Stern, Jan 5, 2026 release (Bloomberg 17.9, RBC 17.9)
}

# CPI-U Dec-Dec annual % — BLS
CPI_PCT = {
    1960: 1.46, 1961: 1.07, 1962: 1.20, 1963: 1.24, 1964: 1.28,
    1965: 1.59, 1966: 2.86, 1967: 3.09, 1968: 4.19, 1969: 5.46,
    1970: 5.72, 1971: 4.38, 1972: 3.21, 1973: 6.16, 1974:11.03,
    1975: 9.14, 1976: 5.76, 1977: 6.50, 1978: 7.62, 1979:11.22,
    1980:13.58, 1981:10.35, 1982: 6.16, 1983: 3.22, 1984: 4.30,
    1985: 3.56, 1986: 1.86, 1987: 3.65, 1988: 4.14, 1989: 4.82,
    1990: 5.40, 1991: 4.21, 1992: 3.01, 1993: 2.99, 1994: 2.56,
    1995: 2.83, 1996: 2.95, 1997: 2.29, 1998: 1.56, 1999: 2.21,
    2000: 3.36, 2001: 2.85, 2002: 1.58, 2003: 2.28, 2004: 2.66,
    2005: 3.39, 2006: 3.24, 2007: 2.85, 2008: 3.84, 2009:-0.36,
    2010: 1.64, 2011: 3.16, 2012: 2.07, 2013: 1.46, 2014: 1.62,
    2015: 0.12, 2016: 1.26, 2017: 2.13, 2018: 2.44, 2019: 1.81,
    2020: 1.23, 2021: 4.70, 2022: 8.00, 2023: 4.12, 2024: 2.90,
    2025: 2.70,  # BLS Dec 2025 release
}

# Nominal GDP ($B) — BEA / FRED GDPA
GDP_NOM = {
    1960:  543.3, 1961:  563.3, 1962:  605.1, 1963:  638.6, 1964:  685.8,
    1965:  743.7, 1966:  815.0, 1967:  861.7, 1968:  942.5, 1969: 1019.9,
    1970: 1075.9, 1971: 1167.8, 1972: 1282.4, 1973: 1428.5, 1974: 1549.2,
    1975: 1688.9, 1976: 1877.6, 1977: 2086.0, 1978: 2356.6, 1979: 2632.1,
    1980: 2862.5, 1981: 3211.0, 1982: 3345.0, 1983: 3638.1, 1984: 4040.7,
    1985: 4346.7, 1986: 4590.2, 1987: 4870.2, 1988: 5252.6, 1989: 5657.7,
    1990: 5979.6, 1991: 6174.0, 1992: 6539.3, 1993: 6878.7, 1994: 7308.8,
    1995: 7664.1, 1996: 8100.2, 1997: 8608.5, 1998: 9089.2, 1999: 9660.6,
    2000:10284.8, 2001:10621.8, 2002:10977.5, 2003:11510.7, 2004:12274.9,
    2005:13093.7, 2006:13855.9, 2007:14477.6, 2008:14718.6, 2009:14418.7,
    2010:14964.4, 2011:15517.9, 2012:16155.3, 2013:16691.5, 2014:17393.1,
    2015:18036.6, 2016:18715.0, 2017:19519.4, 2018:20580.2, 2019:21380.0,
    2020:21060.5, 2021:23315.1, 2022:25723.0, 2023:27357.8, 2024:29175.5,
    2025:30762.1,  # BEA advance estimate, April 2026
}

# M2 money supply ($B, annual averages) — FRED M2SL
M2 = {
    1959:  297, 1960:  312, 1961:  335, 1962:  363, 1963:  393,
    1964:  424, 1965:  459, 1966:  480, 1967:  524, 1968:  567,
    1969:  589, 1970:  628, 1971:  712, 1972:  805, 1973:  861,
    1974:  908, 1975: 1016, 1976: 1152, 1977: 1270, 1978: 1366,
    1979: 1474, 1980: 1599, 1981: 1755, 1982: 1910, 1983: 2127,
    1984: 2310, 1985: 2497, 1986: 2733, 1987: 2832, 1988: 2994,
    1989: 3159, 1990: 3277, 1991: 3380, 1992: 3432, 1993: 3478,
    1994: 3499, 1995: 3641, 1996: 3824, 1997: 4035, 1998: 4379,
    1999: 4644, 2000: 4921, 2001: 5437, 2002: 5785, 2003: 6065,
    2004: 6394, 2005: 6664, 2006: 7103, 2007: 7456, 2008: 8166,
    2009: 8498, 2010: 8800, 2011: 9643, 2012:10454, 2013:10994,
    2014:11683, 2015:12340, 2016:13208, 2017:13845, 2018:14413,
    2019:15326, 2020:19154, 2021:21637, 2022:21514, 2023:20766,
    2024:21340, 2025:22442,
}

# Population (millions, mid-year) — Census Bureau
POP = {
    1960:180.7, 1961:183.7, 1962:186.5, 1963:189.2, 1964:191.9,
    1965:194.3, 1966:196.6, 1967:198.7, 1968:200.7, 1969:202.7,
    1970:205.1, 1971:207.7, 1972:209.9, 1973:211.9, 1974:213.9,
    1975:216.0, 1976:218.0, 1977:220.2, 1978:222.6, 1979:225.1,
    1980:227.7, 1981:229.9, 1982:232.2, 1983:234.3, 1984:236.4,
    1985:238.5, 1986:240.7, 1987:243.0, 1988:245.0, 1989:247.3,
    1990:249.6, 1991:252.2, 1992:255.0, 1993:257.8, 1994:260.3,
    1995:262.8, 1996:265.2, 1997:267.8, 1998:270.2, 1999:272.7,
    2000:282.2, 2001:285.0, 2002:287.8, 2003:290.1, 2004:292.9,
    2005:295.5, 2006:298.4, 2007:301.2, 2008:304.1, 2009:306.8,
    2010:309.3, 2011:311.7, 2012:314.2, 2013:316.5, 2014:318.9,
    2015:321.4, 2016:323.1, 2017:325.1, 2018:327.2, 2019:329.5,
    2020:331.5, 2021:332.0, 2022:333.3, 2023:335.9, 2024:337.9,
    2025:342.0,
}

# Adverse return sequences for stress tests
# Source: Damodaran Jan 2026 for S&P nominal; BLS historical for CPI

# Great Depression: 1929–1945 (17 years)
DEPRESSION_SP  = [-8.30,-25.12,-43.84,-8.64,49.98,-1.19,46.74,31.94,
                  -35.34,29.28,-1.10,-10.67,-12.77,19.17,25.06,19.03,35.82]
DEPRESSION_CPI = [-0.2,-6.4,-9.3,-10.3,0.8,1.5,3.0,1.4,2.9,-2.8,
                   0.0,0.7,5.0,10.9,6.1,1.7,2.3]

# Stagflation: 1966–1982 (17 years)
STAGFLATION_SP  = [-9.97,23.80,10.81,-8.24,3.56,14.22,18.76,-14.31,-25.90,
                   37.00,23.83,-6.98,6.51,18.52,31.74,-4.70,20.42]
STAGFLATION_CPI = [2.86,3.09,4.19,5.46,5.72,4.38,3.21,6.16,11.03,
                   9.14,5.76,6.50,7.62,11.22,13.58,10.35,6.16]

# BEA chain-weighted real GDP growth (%) — BEA NIPA Table 1.1.1
# Source: https://fred.stlouisfed.org/series/A191RP1A027NBEA
REAL_GDP_GROWTH = {
    1960: 2.57, 1961: 2.31, 1962: 6.10, 1963: 4.40, 1964: 5.80,
    1965: 6.49, 1966: 6.59, 1967: 2.46, 1968: 4.85, 1969: 3.09,
    1970: 0.17, 1971: 3.28, 1972: 5.27, 1973: 5.65, 1974:-0.54,
    1975:-0.21, 1976: 5.39, 1977: 4.62, 1978: 5.56, 1979: 3.17,
    1980:-0.26, 1981: 2.55, 1982:-1.92, 1983: 4.63, 1984: 7.24,
    1985: 4.17, 1986: 3.46, 1987: 3.46, 1988: 4.18, 1989: 3.68,
    1990: 1.88, 1991:-0.11, 1992: 3.56, 1993: 2.74, 1994: 4.04,
    1995: 2.72, 1996: 3.80, 1997: 4.49, 1998: 4.45, 1999: 4.74,
    2000: 4.09, 2001: 0.97, 2002: 1.75, 2003: 2.85, 2004: 3.90,
    2005: 3.33, 2006: 2.86, 2007: 1.99, 2008:-0.14, 2009:-2.60,
    2010: 2.71, 2011: 1.55, 2012: 2.25, 2013: 1.84, 2014: 2.53,
    2015: 3.08, 2016: 1.71, 2017: 2.33, 2018: 2.99, 2019: 2.29,
    2020:-2.77, 2021: 5.95, 2022: 1.99, 2023: 2.54, 2024: 2.82,
    2025: 2.00,  # CBO estimate
}

# Post-2025 projection assumptions (CBO Long-Term Budget Outlook 2025)
POST_GDP_GROWTH = 0.040   # 4.0% nominal
POST_M2_GROWTH  = 0.045   # 4.5% nominal
POST_POP_GROWTH = 0.004   # 0.4% annual
POST_CPI        = 2.5     # Fed target %
POST_REAL_GDP   = 1.8     # CBO long-run real GDP growth %

# ── Dataset builder ────────────────────────────────────────────────────────

def build_dataset():
    """Extend all series to 2060 using post-2025 projections."""
    gdp  = dict(GDP_NOM)
    m2   = dict(M2)
    pop  = dict(POP)
    cpi  = dict(CPI_PCT)
    sp   = dict(SP_NOM)

    for y in range(2026, 2061):
        gdp[y] = gdp[y-1] * (1 + POST_GDP_GROWTH)
        m2[y]  = m2[y-1]  * (1 + POST_M2_GROWTH)
        pop[y] = pop[y-1] * (1 + POST_POP_GROWTH)
        cpi[y] = POST_CPI
        # sp[y] intentionally left absent for post-2025 (uses post_real_rate)

    return gdp, m2, pop, cpi, sp


def build_cpi_index(cpi):
    """Build cumulative CPI index (base = Jan 1960 = 100)."""
    idx = {}
    level = 100.0
    for y in range(1960, 2061):
        level *= (1 + cpi[y] / 100)
        idx[y] = level
    return idx


# ── Core computation ───────────────────────────────────────────────────────

def compute_cohort(birth_year, retire_year, post_real_rate,
                   stress_seq=None):
    """
    Compute Mode B Stable Floor for one cohort.

    Parameters
    ----------
    birth_year      : int   — year citizen is born (K1 deposited)
    retire_year     : int   — year citizen turns 65
    post_real_rate  : float — real return % for years after 2025
    stress_seq      : dict or None
        If provided: {'sp': [...], 'cpi': [...], 'start_age': int}
        Substitutes adverse nominal SP and CPI for ages start_age to
        start_age + len(sp) - 1.

    Returns
    -------
    dict with keys: balance, total_dep, k1_real, k2_real, annual_rows
    """
    gdp, m2, pop, cpi, sp = build_dataset()
    cpi_idx  = build_cpi_index(cpi)
    cpi_2025 = cpi_idx[2025]

    balance    = 0.0
    total_dep  = 0.0
    k1_real    = 0.0
    k2_real    = 0.0
    annual_rows = []

    for y in range(birth_year, retire_year + 1):
        age = y - birth_year

        # ── Deposits ──
        gdp_y   = gdp[y]
        pop_y   = pop[y] * 1e6          # persons
        gdp_pc  = (gdp_y * 1e9) / pop_y

        k1_nom  = gdp_pc * 0.025 if age == 0 else 0.0

        prev_m2  = m2.get(y - 1, m2[y]) * 1e9  # convert $B → $
        cpi_rate = cpi[y] / 100
        # Use BEA chain-weighted real GDP growth directly (authoritative)
        if y in REAL_GDP_GROWTH:
            real_gdp_growth = max(0.0, REAL_GDP_GROWTH[y] / 100)
        else:
            real_gdp_growth = max(0.0, POST_REAL_GDP / 100)
        k2_nom  = (real_gdp_growth * prev_m2 * 0.5) / pop_y

        dep_nom  = k1_nom + k2_nom
        cpi_mult = cpi_2025 / cpi_idx[y]
        dep_real = dep_nom * cpi_mult

        total_dep += dep_real
        if age == 0:
            k1_real += dep_real
        else:
            k2_real += dep_real

        # ── Real return ──
        if stress_seq and (stress_seq['start_age'] <= age <
                           stress_seq['start_age'] + len(stress_seq['sp'])):
            si      = age - stress_seq['start_age']
            nom_ret = stress_seq['sp'][si]  / 100
            s_cpi   = stress_seq['cpi'][si] / 100
            real_ret = (1 + nom_ret) / (1 + s_cpi) - 1
        elif y <= 2025:
            nom_ret  = sp.get(y, 0.0) / 100
            real_ret = (1 + nom_ret) / (1 + cpi_rate) - 1
        else:
            real_ret = post_real_rate / 100

        balance = (balance + dep_real) * (1 + real_ret)

        annual_rows.append({
            'year': y, 'age': age,
            'gdp_nom': round(gdp_y, 1),
            'pop_m':   round(pop[y], 1),
            'k1_nom':  round(k1_nom, 2),
            'k2_nom':  round(k2_nom, 2),
            'dep_real_2025': round(dep_real, 2),
            'real_ret_pct':  round(real_ret * 100, 2),
            'balance_2025':  round(balance, 2),
        })

    return {
        'balance':     round(balance, 0),
        'total_dep':   round(total_dep, 0),
        'k1_real':     round(k1_real, 0),
        'k2_real':     round(k2_real, 0),
        'comp_gain':   round(balance - total_dep, 0),
        'annual_rows': annual_rows,
    }


# ── Benchmarks ─────────────────────────────────────────────────────────────

BENCHMARKS = {
    'A': {'med': 260000, 'mean': 669230, 'ss': 24953,
          'med_inc': 35353,  'mean_inc': 51722},
    'B': {'med': 240000, 'mean': 649230, 'ss': 19214,
          'med_inc': 28814,  'mean_inc': 45183},
    'C': {'med': 220000, 'mean': 629230, 'ss': 19214,
          'med_inc': 28014,  'mean_inc': 44383},
    'D': {'med': 210000, 'mean': 619230, 'ss': 19214,
          'med_inc': 27614,  'mean_inc': 43983},
}

COHORTS = [
    {'label': 'A', 'born': 1960, 'retire': 2025},
    {'label': 'B', 'born': 1970, 'retire': 2035},
    {'label': 'C', 'born': 1980, 'retire': 2045},
    {'label': 'D', 'born': 1990, 'retire': 2055},
]

DEPRESSION  = {'sp': DEPRESSION_SP,  'cpi': DEPRESSION_CPI,  'start_age': 25}
STAGFLATION = {'sp': STAGFLATION_SP, 'cpi': STAGFLATION_CPI, 'start_age': 25}


# ── Output helpers ─────────────────────────────────────────────────────────

def fmt(v):
    return f"${v:,.0f}"

def fmtx(v, b):
    return f"{v/b:.1f}×"

def sep(char='-', width=110):
    print(char * width)

def header(title):
    sep('=')
    print(f"  {title}")
    sep('=')


# ── Main ───────────────────────────────────────────────────────────────────

def main():
    print()
    print("Citizens Standard — Mode B Replication Script")
    print("Neo-Solon (2026) | SSRN: https://papers.ssrn.com/sol3/papers.cfm?abstract_id=6735078")
    print()

    # ── Table 1: Central scenario, all four cohorts ────────────────────────
    header("TABLE 1  Cohort outcomes — central scenario (4.5% real post-2025)")
    print(f"{'Cohort':<8} {'Born':<6} {'Retire':<8} "
          f"{'Stable Floor':>14} {'Median actual':>14} {'Mean actual':>12} "
          f"{'vs median':>10} {'vs mean':>10}")
    sep()

    central_results = {}
    for c in COHORTS:
        r = compute_cohort(c['born'], c['retire'], 4.5)
        central_results[c['label']] = r
        b = BENCHMARKS[c['label']]
        print(f"{c['label']:<8} {c['born']:<6} {c['retire']:<8} "
              f"{fmt(r['balance']):>14} {fmt(b['med']):>14} "
              f"{fmt(b['mean']):>12} "
              f"{fmtx(r['balance'], b['med']):>10} "
              f"{fmtx(r['balance'], b['mean']):>10}")
    print()

    # ── Table 2: Annual retirement income ─────────────────────────────────
    header("TABLE 2  Annual retirement income at age 65 — central scenario (2025 real $)")
    print(f"{'Cohort':<8} {'Retire':<8} {'SS benefit':>12} "
          f"{'Median income':>14} {'Mean income':>12} {'Mode B income':>14}")
    sep()

    for c in COHORTS:
        r = central_results[c['label']]
        b = BENCHMARKS[c['label']]
        mode_b_income = round(r['balance'] * 0.04) + b['ss']
        print(f"{c['label']:<8} {c['retire']:<8} {fmt(b['ss']):>12} "
              f"{fmt(b['med_inc']):>14} {fmt(b['mean_inc']):>12} "
              f"{fmt(mode_b_income):>14}")
    print()

    # ── Section 4.4: Cohort D three scenarios ─────────────────────────────
    header("SECTION 4.4  Cohort D sensitivity — three return scenarios")
    print(f"{'Scenario':<14} {'Post-2025 real':>15} {'Stable Floor':>14} "
          f"{'Annual income':>14} {'vs median':>10} {'vs mean':>10}")
    sep()

    d_bench = BENCHMARKS['D']
    for label, rate in [('Pessimistic', 3.0), ('Central', 4.5), ('Historical', 6.5)]:
        r = compute_cohort(1990, 2055, rate)
        inc = round(r['balance'] * 0.04) + d_bench['ss']
        print(f"{label:<14} {rate:>14.1f}% {fmt(r['balance']):>14} "
              f"{fmt(inc):>14} "
              f"{fmtx(r['balance'], d_bench['med']):>10} "
              f"{fmtx(r['balance'], d_bench['mean']):>10}")
    print()

    # ── Section 4.5: Decomposition — Cohort A ─────────────────────────────
    header("SECTION 4.5  Decomposition — Cohort A (born 1960, retire 2025)")
    r = central_results['A']
    total = r['balance']
    print(f"  K1 deposit at birth (1960, real 2025$):   {fmt(r['k1_real']):>14}  "
          f"({r['k1_real']/total*100:.2f}%)")
    print(f"  K2 deposits cumulative (real 2025$):       {fmt(r['k2_real']):>14}  "
          f"({r['k2_real']/total*100:.1f}%)")
    print(f"  Total principal (real 2025$):              {fmt(r['total_dep']):>14}  "
          f"({r['total_dep']/total*100:.1f}%)")
    print(f"  Equity compounding gain:                   {fmt(r['comp_gain']):>14}  "
          f"({r['comp_gain']/total*100:.1f}%)")
    print(f"  Final Stable Floor:                        {fmt(total):>14}  (100%)")
    print()

    # ── Table 3: Stress tests ──────────────────────────────────────────────
    header("TABLE 3  Stress tests — Depression and Stagflation sequences (ages 25–41)")
    print(f"{'Cohort':<8} {'Central':>12} {'Depression':>12} {'Stagflation':>12} "
          f"{'Depr/Cent':>10} {'Stag/Cent':>10} "
          f"{'Depr vs med':>12} {'Stag vs med':>12}")
    sep()

    for c in COHORTS:
        cent = central_results[c['label']]['balance']
        depr = compute_cohort(c['born'], c['retire'], 4.5, DEPRESSION)['balance']
        stag = compute_cohort(c['born'], c['retire'], 4.5, STAGFLATION)['balance']
        med  = BENCHMARKS[c['label']]['med']
        d_flag = '✓' if depr >= med else '✗'
        s_flag = '✓' if stag >= med else '✓'
        print(f"{c['label']:<8} {fmt(cent):>12} {fmt(depr):>12} {fmt(stag):>12} "
              f"{depr/cent:>9.2f}× {stag/cent:>9.2f}× "
              f"{fmtx(depr,med):>10} {d_flag}  "
              f"{fmtx(stag,med):>8} {s_flag}")
    print()

    # ── Cohort A annual detail (first and last 10 years + key years) ───────
    header("COHORT A  Annual detail — selected years (full trail in annual_rows)")
    rows = central_results['A']['annual_rows']
    snap = {1960,1965,1970,1975,1980,1985,1990,1995,2000,2005,2010,2015,2020,2025}
    print(f"{'Year':<6} {'Age':<5} {'GDP $B':>9} {'Pop M':>7} "
          f"{'K1 nom':>10} {'K2 nom':>10} "
          f"{'Dep real':>11} {'Real ret%':>10} {'Balance 2025$':>15}")
    sep()
    for row in rows:
        if row['year'] in snap:
            print(f"{row['year']:<6} {row['age']:<5} {row['gdp_nom']:>9.1f} "
                  f"{row['pop_m']:>7.1f} "
                  f"${row['k1_nom']:>9,.0f} ${row['k2_nom']:>9,.0f} "
                  f"${row['dep_real_2025']:>9,.0f} "
                  f"{row['real_ret_pct']:>9.1f}% "
                  f"${row['balance_2025']:>13,.0f}")
    print()

    sep('=')
    print("  All figures in 2025 purchasing power unless otherwise noted.")
    print("  Methodology: deposits deflated to 2025$ using Dec-Dec CPI chain,")
    print("  then compounded at real returns throughout (Fisher equation).")
    print("  Post-2025 central scenario: 4.5% real. GDP: 4.0% nominal growth.")
    print("  M2: 4.5% nominal growth. Pop: 0.4%/yr. CPI: 2.5% (CBO baseline).")
    sep('=')
    print()


if __name__ == '__main__':
    main()

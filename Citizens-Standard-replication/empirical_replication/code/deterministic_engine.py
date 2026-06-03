"""
deterministic_engine.py
========================
Single-path Mode B Stable Floor computation using authoritative data.

This is the engine for Sections 3, 4, and 5 of the paper. The Monte Carlo
engine in mc_engine.py reuses the same per-year accounting; only the
(return, CPI, real-GDP-growth) triple is randomized there.
"""

from authoritative_data import (
    CPI_DECDEC, CPI_ANNUAL, SP500_NOMINAL, GDP_NOMINAL_B,
    REAL_GDP_GROWTH, M2_BILLIONS, POPULATION_M, real_sp500_return,
)


# Post-2025 projection assumptions (CBO Long-Term Budget Outlook 2025).
POST_REAL_GDP_GROWTH_PCT = 1.8
POST_M2_NOMINAL_GR_PCT   = 4.5
POST_POPULATION_GR_PCT   = 0.4
POST_CPI_PCT             = 2.5
POST_GDP_NOMINAL_GR_PCT  = 4.0

# Methodology constants from the paper.
K1_FRACTION = 0.025  # 2.5% of GDP per capita at birth
K2_FRACTION = 0.5    # half of real GDP growth times prior-year M2 per citizen

# ----- Reference benchmarks (SCF 2022 + DB pension adjustments) -----
BENCHMARKS = {
    "A": {"med": 260000, "mean": 669230, "ss": 24953,
          "med_inc": 35353,  "mean_inc": 51722},
    "B": {"med": 240000, "mean": 649230, "ss": 19214,
          "med_inc": 28814,  "mean_inc": 45183},
    "C": {"med": 220000, "mean": 629230, "ss": 19214,
          "med_inc": 28014,  "mean_inc": 44383},
    "D": {"med": 210000, "mean": 619230, "ss": 19214,
          "med_inc": 27614,  "mean_inc": 43983},
}

COHORTS = [
    ("A", 1960, 2025),
    ("B", 1970, 2035),
    ("C", 1980, 2045),
    ("D", 1990, 2055),
]

# ----- Stress sequences (Damodaran + BLS) -----
DEPRESSION_SP500_NOMINAL = [
    -8.30, -25.12, -43.84, -8.64, 49.98, -1.19, 46.74, 31.94,
    -35.34, 29.28, -1.10, -10.67, -12.77, 19.17, 25.06, 19.03, 35.82,
]
DEPRESSION_CPI_DECDEC = [
    0.6, -6.4, -9.3, -10.3, 0.8, 1.5, 3.0, 1.4, 2.9, -2.8,
    0.0, 0.7, 9.9, 9.0, 3.0, 2.3, 2.2,
]  # 1929-1945 Dec-Dec from BLS

STAGFLATION_SP500_NOMINAL = [
    -9.97, 23.80, 10.81, -8.24, 3.56, 14.22, 18.76, -14.31, -25.90,
    37.00, 23.83, -6.98, 6.51, 18.52, 31.74, -4.70, 20.42,
]
STAGFLATION_CPI_DECDEC = [
    3.5, 3.0, 4.7, 6.2, 5.6, 3.3, 3.4, 8.7, 12.3,
    6.9, 4.9, 6.7, 9.0, 13.3, 12.5, 8.9, 3.8,
]  # 1966-1982 Dec-Dec from BLS (authoritative)


# =============================================================================
# Data construction (combine historical + projection)
# =============================================================================

def build_dataset(end_year=2060):
    """
    Return dict keyed by year with M2 ($B), GDP ($B), pop (M), cpi_decdec_pct,
    real_gdp_growth_pct, sp500_nominal_pct, sp500_real (decimal), cpi_annual.
    Extends post-2025 by post-projection constants.
    """
    data = {}
    for y in range(1928, 2026):
        if y not in M2_BILLIONS or y not in GDP_NOMINAL_B or y not in POPULATION_M:
            continue
        data[y] = {
            "M2":         M2_BILLIONS[y],
            "GDP":        GDP_NOMINAL_B[y],
            "pop":        POPULATION_M[y],
            "cpi_decdec": CPI_DECDEC[y],
            "cpi_ann":    CPI_ANNUAL[y],
            "rgdp":       REAL_GDP_GROWTH.get(y, 0.0),
            "sp_nom":     SP500_NOMINAL[y],
            "sp_real":    real_sp500_return(y) if y in CPI_DECDEC else None,
        }

    for y in range(2026, end_year + 1):
        prev = data[y - 1]
        data[y] = {
            "M2":         prev["M2"]  * (1 + POST_M2_NOMINAL_GR_PCT  / 100),
            "GDP":        prev["GDP"] * (1 + POST_GDP_NOMINAL_GR_PCT / 100),
            "pop":        prev["pop"] * (1 + POST_POPULATION_GR_PCT  / 100),
            "cpi_decdec": POST_CPI_PCT,
            "cpi_ann":    prev["cpi_ann"] * (1 + POST_CPI_PCT / 100),
            "rgdp":       POST_REAL_GDP_GROWTH_PCT,
            "sp_nom":     None,
            "sp_real":    None,
        }
    return data


# =============================================================================
# Single-path computation
# =============================================================================

def compute_cohort(
    data,
    birth_year,
    retire_year,
    post_real_equity_return,
    stress=None,
    return_decomposition=False,
):
    """
    Compute Mode B Stable Floor at retirement, in 2025 real dollars.

    Methodology:
      * K1 = 2.5% of GDP per capita at birth year (nominal).
      * K2 = 0.5 * max(0, real GDP growth) * M2[y-1] / pop[y]  (nominal).
      * Both deflated to 2025$ via the annual CPI ratio.
      * Real return per year = Fisher from S&P nominal and CPI Dec-Dec,
        except in stress windows (override) or post-2025 (constant scenario).
      * Deposit-then-compound: deposit credited at start of year, earns
        that year's return.
    """
    cpi_2025 = data[2025]["cpi_ann"]

    def deflate(nominal_amount, year):
        return nominal_amount * (cpi_2025 / data[year]["cpi_ann"])

    balance       = 0.0
    k1_real_total = 0.0
    k2_real_total = 0.0

    for y in range(birth_year, retire_year + 1):
        age = y - birth_year
        d   = data[y]

        # ---- Deposits ----
        gdp_pc_nom_dollars = (d["GDP"] * 1e9) / (d["pop"] * 1e6)
        k1_nom = gdp_pc_nom_dollars * K1_FRACTION if y == birth_year else 0.0

        prev_m2_dollars = (data[y - 1]["M2"] * 1e9) if (y - 1) in data else d["M2"] * 1e9
        rgdp_clamped = max(0.0, d["rgdp"] / 100.0)
        k2_nom = (rgdp_clamped * prev_m2_dollars * K2_FRACTION) / (d["pop"] * 1e6)

        k1_real = deflate(k1_nom, y)
        k2_real = deflate(k2_nom, y)
        k1_real_total += k1_real
        k2_real_total += k2_real

        # ---- Real return for the year ----
        if stress is not None:
            s_start = stress.get("start_age", 25)
            s_len   = len(stress["nom"])
            if s_start <= age < s_start + s_len:
                i = age - s_start
                real_ret = (
                    (1 + stress["nom"][i] / 100.0)
                    / (1 + stress["cpi"][i] / 100.0)
                    - 1.0
                )
            elif y <= 2025:
                real_ret = d["sp_real"]
            else:
                real_ret = post_real_equity_return
        elif y <= 2025:
            real_ret = d["sp_real"]
        else:
            real_ret = post_real_equity_return

        balance = (balance + k1_real + k2_real) * (1 + real_ret)

    if return_decomposition:
        total_dep = k1_real_total + k2_real_total
        return {
            "balance":         balance,
            "k1_real":         k1_real_total,
            "k2_real":         k2_real_total,
            "total_deposits":  total_dep,
            "compound_gain":   balance - total_dep,
            "principal_share": total_dep / balance * 100 if balance else 0,
            "compound_share":  (balance - total_dep) / balance * 100 if balance else 0,
        }
    return balance


if __name__ == "__main__":
    data = build_dataset(end_year=2060)
    for name, b, r in COHORTS:
        bal = compute_cohort(data, b, r, 0.045)
        bench = BENCHMARKS[name]
        print(f"{name}: born {b}, retires {r}, "
              f"Stable Floor = ${bal:>12,.0f}  "
              f"({bal/bench['med']:.1f}x med, {bal/bench['mean']:.1f}x mean)")

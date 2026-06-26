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
from authoritative_newcitizens import k1_residual_deduction_per_capita


# Post-2025 projection assumptions (CBO Long-Term Budget Outlook 2025).
POST_REAL_GDP_GROWTH_PCT = 1.8
POST_M2_NOMINAL_GR_PCT   = 4.5
POST_POPULATION_GR_PCT   = 0.4
POST_CPI_PCT             = 2.5
POST_GDP_NOMINAL_GR_PCT  = 4.0

# Methodology constants from the paper.
K1_FRACTION = 0.025  # 2.5% of GDP per capita at birth
K2_FRACTION = 1.0    # share of the real-growth line allocated to K2 before the K1 residual
# Residual calibration: K2_agg = g_r*M2 - K1_agg, so that total new money equals
# the real-growth line (zero drift in growth years). K1_agg is funded first from
# the line; K2 receives the remainder. Set False to recover the legacy full-rate
# convention (K2 = g_r*M2 with K1 issued on top, ~0.04% overshoot).
K2_RESIDUAL = True

# --- GE realizable basis / Mode B 60-40 (Neo-Solon 2026a, Section 6.7) ---
# At universal scale the citizen floors deepen the aggregate capital stock, so the
# realized price-taker S&P return is not available: the floor earns the general-
# equilibrium realizable return on capital. When GE_REALIZABLE_RETURN is not None
# the with-program counterfactual compounds at that return for ALL years (not the
# realized historical returns, which were a price-taker outcome). FLOOR_SHARE splits
# the post-K1 residual: the locked floor (K2) takes FLOOR_SHARE, the standing K3
# citizen dividend takes the remainder.
GE_REALIZABLE_RETURN = 0.0426   # Mode B central GE return; alpha/delta band 0.0330-0.0503
FLOOR_SHARE = 0.60              # Mode B 60/40: 60% of the residual builds the floor
# The K3 dividend is paid as LIQUID CASH, not into the tax-advantaged locked floor.
# If a citizen voluntarily reinvests it in a taxable brokerage account it compounds
# at an AFTER-TAX rate (long-term capital-gains and dividend tax drag), below the
# floor's locked tax-free rate. K3_REINVEST_RATE sets that after-tax real return for
# the illustrative "if reinvested" upper case; None means the dividend is held as cash.
K3_REINVEST_RATE = 0.034        # ~0.9pp tax drag on a 4.26% buy-and-hold equity return

# ----- Reference benchmarks (SCF 2022 + DB pension adjustments) -----
# Single constant SCF-2022 benchmark (age 65-74, DB-adjusted) applied to ALL cohorts:
# the best available empirical anchor, held constant in real 2025 dollars (US median
# retirement wealth has been roughly flat in real terms). Floor-to-benchmark ratios
# therefore rise across cohorts only because the framework's deposits scale with the
# economy, not because the yardstick moves. SS = full $24,953 for cohort A (retires
# pre-2032); cohorts B-D retire after OASI depletion and take the 22% cut (x0.78 =
# $19,463) per the 2026 SSA Trustees Report. med_inc/mean_inc hold the non-SS (asset-
# draw) component constant and apply the same 22% SS cut to the embedded SS portion.
BENCHMARKS = {
    "A": {"med": 260000, "mean": 669230, "ss": 24953,
          "med_inc": 35353,  "mean_inc": 51722},
    "B": {"med": 260000, "mean": 669230, "ss": 19463,
          "med_inc": 29863,  "mean_inc": 46232},
    "C": {"med": 260000, "mean": 669230, "ss": 19463,
          "med_inc": 29863,  "mean_inc": 46232},
    "D": {"med": 260000, "mean": 669230, "ss": 19463,
          "med_inc": 29863,  "mean_inc": 46232},
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
      * K2 = max(0, real GDP growth) * M2[y-1] / pop[y], less the per-citizen
        K1 residual when K2_RESIDUAL (so K1_agg + K2_agg = the real-growth line).
        The K1 residual draws on the deposit-weighted new-citizen count (births
        full, naturalizations pro-rated by (65-age)/65).
      * Both deflated to 2025$ via the annual CPI ratio.
      * Real return per year = Fisher from S&P nominal and CPI Dec-Dec,
        except in stress windows (override) or post-2025 (constant scenario).
      * Deposit-then-compound: deposit credited at start of year, earns
        that year's return.
      * In contraction years real growth <= 0 so K2 = 0; K1 still flows,
        a small counter-cyclical injection (the line is not clawed back).
    """
    cpi_2025 = data[2025]["cpi_ann"]

    def deflate(nominal_amount, year):
        return nominal_amount * (cpi_2025 / data[year]["cpi_ann"])

    balance       = 0.0
    k1_real_total = 0.0
    k2_real_total = 0.0
    k3_real_total = 0.0
    k3_invested_balance = 0.0   # K3 dividend voluntarily reinvested at after-tax rate

    for y in range(birth_year, retire_year + 1):
        age = y - birth_year
        d   = data[y]

        # ---- Deposits ----
        gdp_pc_nom_dollars = (d["GDP"] * 1e9) / (d["pop"] * 1e6)
        k1_nom = gdp_pc_nom_dollars * K1_FRACTION if y == birth_year else 0.0

        prev_m2_dollars = (data[y - 1]["M2"] * 1e9) if (y - 1) in data else d["M2"] * 1e9
        rgdp_clamped = max(0.0, d["rgdp"] / 100.0)
        pop_persons = d["pop"] * 1e6
        k2_nom = (rgdp_clamped * prev_m2_dollars * K2_FRACTION) / pop_persons
        if K2_RESIDUAL:
            # Fund K1 first from the real-growth line; K2 gets the remainder.
            # When K2 is already 0 (contraction year) there is nothing to net
            # against, so K1 flows on top (counter-cyclical), and K2 stays 0.
            deduction = k1_residual_deduction_per_capita(
                y, gdp_pc_nom_dollars, pop_persons, K1_FRACTION
            )
            k2_nom = max(0.0, k2_nom - deduction)

        # Mode B 60/40: split the post-K1 residual into the locked floor (K2)
        # and the standing K3 citizen dividend.
        k3_nom = (1.0 - FLOOR_SHARE) * k2_nom
        k2_nom = FLOOR_SHARE * k2_nom

        k1_real = deflate(k1_nom, y)
        k2_real = deflate(k2_nom, y)
        k3_real = deflate(k3_nom, y)
        k1_real_total += k1_real
        k2_real_total += k2_real
        k3_real_total += k3_real

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
            elif GE_REALIZABLE_RETURN is not None:
                real_ret = GE_REALIZABLE_RETURN
            elif y <= 2025:
                real_ret = d["sp_real"]
            else:
                real_ret = post_real_equity_return
        elif GE_REALIZABLE_RETURN is not None:
            real_ret = GE_REALIZABLE_RETURN
        elif y <= 2025:
            real_ret = d["sp_real"]
        else:
            real_ret = post_real_equity_return

        balance = (balance + k1_real + k2_real) * (1 + real_ret)
        # Illustrative voluntary reinvestment of the liquid K3 dividend in a taxable
        # account: compounds at the after-tax rate, not the floor's locked rate.
        reinvest_ret = K3_REINVEST_RATE if K3_REINVEST_RATE is not None else real_ret
        k3_invested_balance = (k3_invested_balance + k3_real) * (1 + reinvest_ret)

    if return_decomposition:
        total_dep = k1_real_total + k2_real_total
        return {
            "balance":         balance,
            "k1_real":         k1_real_total,
            "k2_real":         k2_real_total,
            "k3_real":         k3_real_total,
            "k3_invested":     k3_invested_balance,
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

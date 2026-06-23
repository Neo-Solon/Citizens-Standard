"""
transition_cohorts.py
========================
Part II of the v3 paper: forward transition-cohort projections.

These are FORWARD PROJECTIONS, not historical reconstructions. Cohorts born
2026/2036/2046/2056 accumulate full-rate K2 from birth to age 65, with a
return-compression haircut applied during the debt-paydown window (2026-2071)
to reflect the systematic-demand effect described in the transition paper
(Neo-Solon, 2026c, Section 4.3).

Unlike Part I (which uses actual historical returns through 2025), these
cohorts accumulate entirely post-2025 and therefore use ASSUMED returns:
pessimistic 3.0%, central 4.5%, optimistic 6.5% real.
"""

from deterministic_engine import build_dataset, K1_FRACTION, K2_FRACTION, K2_RESIDUAL, FLOOR_SHARE
from authoritative_newcitizens import k1_residual_deduction_per_capita

# Forward transition cohorts: (label, birth_year, retire_year)
TRANSITION_COHORTS = [
    ("T1", 2026, 2091),
    ("T2", 2036, 2101),
    ("T3", 2046, 2111),
    ("T4", 2056, 2121),
]

# Debt-paydown window over which return compression applies.
PAYDOWN_END_YEAR = 2071
# Central compression estimate (transition paper reports 0.4-0.6pp range; KT-rotation driven).
COMPRESSION_PP = 0.005

RETURN_SCENARIOS = {"pessimistic": 0.0330, "central": 0.0426, "optimistic": 0.0503}  # GE Mode B band


def compute_transition_cohort(data, birth, retire, base_return,
                              compression_pp=COMPRESSION_PP,
                              paydown_end=PAYDOWN_END_YEAR):
    """
    Compute a forward transition cohort's Stable Floor in 2025 real dollars.

    Identical per-year accounting to deterministic_engine.compute_cohort,
    except: (a) all post-2025 returns are the assumed base_return, and
    (b) during the paydown window [birth..paydown_end] the return is reduced
    by compression_pp.
    """
    cpi_2025 = data[2025]["cpi_ann"]

    def deflate(nominal, year):
        return nominal * (cpi_2025 / data[year]["cpi_ann"])

    balance = 0.0
    for y in range(birth, retire + 1):
        d = data[y]
        gdp_pc_nom = (d["GDP"] * 1e9) / (d["pop"] * 1e6)
        k1_nom = gdp_pc_nom * K1_FRACTION if y == birth else 0.0
        prev_m2 = (data[y - 1]["M2"] * 1e9) if (y - 1) in data else d["M2"] * 1e9
        rgdp = max(0.0, d["rgdp"] / 100.0)
        pop_persons = d["pop"] * 1e6
        k2_nom = (rgdp * prev_m2 * K2_FRACTION) / pop_persons
        if K2_RESIDUAL:
            k2_nom = max(0.0, k2_nom - k1_residual_deduction_per_capita(
                y, gdp_pc_nom, pop_persons, K1_FRACTION))

        k1_real = deflate(k1_nom, y)
        k2_real = FLOOR_SHARE * deflate(k2_nom, y)   # Mode B 60/40 floor share

        if y <= 2025:
            real_ret = d["sp_real"]
        else:
            real_ret = base_return - (compression_pp if y <= paydown_end else 0.0)

        balance = (balance + k1_real + k2_real) * (1 + real_ret)
    return balance


def run_transition_tables(data=None):
    if data is None:
        data = build_dataset(end_year=2125)
    results = {}
    for name, b, r in TRANSITION_COHORTS:
        results[name] = {}
        for scen, ret in RETURN_SCENARIOS.items():
            results[name][scen] = compute_transition_cohort(data, b, r, ret)
        # No-compression central for transition-cost calc
        results[name]["central_no_compression"] = compute_transition_cohort(
            data, b, r, RETURN_SCENARIOS["central"], compression_pp=0.0)
    return results


if __name__ == "__main__":
    data = build_dataset(end_year=2125)
    res = run_transition_tables(data)
    print("Forward transition cohorts (full-rate K2, 0.5pp paydown compression)")
    print(f"{'Cohort':<8}{'Born':<6}{'Pessim':<14}{'Central':<14}{'Optimistic':<14}{'Cost'}")
    for name, b, r in TRANSITION_COHORTS:
        rr = res[name]
        cost = (rr["central_no_compression"] - rr["central"]) / rr["central_no_compression"] * 100
        print(f"{name:<8}{b:<6}${rr['pessimistic']:>11,.0f}  ${rr['central']:>11,.0f}  "
              f"${rr['optimistic']:>11,.0f}  -{cost:.1f}%")

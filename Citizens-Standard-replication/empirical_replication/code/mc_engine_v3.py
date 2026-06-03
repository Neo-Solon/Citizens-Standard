"""
mc_engine.py
============
Monte Carlo bootstrap engine for the Citizens Standard Mode B Stable Floor.

Resamples the historical joint (real_return, CPI_decdec, real_GDP_growth)
distribution and applies Mode B's K1/K2 deposit formula path by path. M2,
nominal GDP, and population follow their deterministic historical (and
post-2025 projected) trajectories; only the (return, CPI, real-GDP-growth)
triple is randomized. This matches Section 6 of the paper.

Two universes:
  * 1929-2025: 97 joint observations (includes Depression and Great Inflation)
  * 1960-2025: 66 joint observations (the observed window for Sections 3-5)

Two methods:
  * IID bootstrap: each year independently sampled from the universe
  * Block bootstrap (5-yr moving blocks): preserves within-block sequencing

10,000 paths per (cohort, universe, method) configuration.
"""

import numpy as np

from authoritative_data import (
    CPI_DECDEC, CPI_ANNUAL, SP500_NOMINAL, GDP_NOMINAL_B,
    REAL_GDP_GROWTH, M2_BILLIONS, POPULATION_M, real_sp500_return,
)
from deterministic_engine_v3 import (
    K1_FRACTION, K2_FRACTION,
    POST_M2_NOMINAL_GR_PCT, POST_GDP_NOMINAL_GR_PCT,
    POST_POPULATION_GR_PCT, POST_CPI_PCT, POST_REAL_GDP_GROWTH_PCT,
    BENCHMARKS, COHORTS, build_dataset,
)


# =============================================================================
# Build the joint universe arrays
# =============================================================================

def build_universe(start_year, end_year):
    """
    Return (returns, cpi_pct, rgdp_pct) np.float64 arrays for years in
    [start_year, end_year] that have all three data points.
    """
    rets, cpis, rgdps = [], [], []
    for y in range(start_year, end_year + 1):
        if y not in CPI_DECDEC or y not in SP500_NOMINAL or y not in REAL_GDP_GROWTH:
            continue
        rets.append(real_sp500_return(y))
        cpis.append(CPI_DECDEC[y])
        rgdps.append(REAL_GDP_GROWTH[y])
    return np.array(rets), np.array(cpis), np.array(rgdps)


UNIVERSES = {
    "1929-2025": build_universe(1929, 2025),
    "1960-2025": build_universe(1960, 2025),
}


# =============================================================================
# Resampling
# =============================================================================

def sample_iid(n_years, n_paths, universe, rng):
    """Return (n_paths, n_years) arrays of indices into universe arrays."""
    n_uni = len(universe[0])
    return rng.integers(0, n_uni, size=(n_paths, n_years))


def sample_block(n_years, n_paths, universe, rng, block_size=5):
    """
    Moving block bootstrap with circular wraparound. Block size 5 preserves
    serial correlation that drives sequence-of-returns risk while keeping the
    bootstrap distribution from collapsing onto a handful of historical
    regimes.
    """
    n_uni = len(universe[0])
    n_blocks = (n_years + block_size - 1) // block_size  # ceiling
    # Random starting positions for each block
    starts = rng.integers(0, n_uni, size=(n_paths, n_blocks))
    # Build the block_size-wide offset, then add to starts
    offsets = np.arange(block_size).reshape(1, 1, block_size)
    full = (starts[:, :, None] + offsets) % n_uni              # (P, B, K)
    full = full.reshape(n_paths, n_blocks * block_size)
    return full[:, :n_years]


# =============================================================================
# Vectorized cohort simulator
# =============================================================================

def simulate_cohort(birth_year, retire_year, n_paths, universe_name,
                    method, post_real_eq, seed, block_size=5):
    """
    Return np.ndarray of shape (n_paths,) with Stable Floor at retirement
    in 2025-real dollars (deflated by path-specific cumulative CPI).

    Per Section 6.1 of the paper: the bootstrap draws an independent sequence
    of annual (return, CPI Dec-Dec, real GDP growth) triples FROM THE
    HISTORICAL UNIVERSE FOR EVERY YEAR of the cohort's working life, including
    post-2025 years. This characterizes total accumulation-phase uncertainty
    under random sequencing of historical conditions.

    M2 nominal, nominal GDP, and population follow their deterministic
    historical (and projected post-2025) trajectories. Randomizing M2 directly
    would introduce monetary-regime variation that the framework's
    constitutional design is intended to bound rather than characterize.

    `post_real_eq` is retained for backward compatibility but is not used when
    randomizing every year. To recover the deterministic central scenario, use
    deterministic_engine.compute_cohort() directly.
    """
    rng = np.random.default_rng(seed)
    ret_uni, cpi_uni, rgdp_uni = UNIVERSES[universe_name]

    # Build deterministic trajectories for M2, GDP, population.
    det = build_dataset(end_year=max(retire_year, 2025) + 1)

    years = list(range(birth_year, retire_year + 1))
    n_years = len(years)

    # ---- Draw bootstrap indices for ALL years ----
    if method == "iid":
        idx = sample_iid(n_years, n_paths, (ret_uni, cpi_uni, rgdp_uni), rng)
    elif method == "block":
        idx = sample_block(n_years, n_paths, (ret_uni, cpi_uni, rgdp_uni),
                           rng, block_size)
    else:
        raise ValueError(method)

    drawn_returns  = ret_uni[idx]            # (P, n_years) real returns
    drawn_cpi_pct  = cpi_uni[idx]            # (P, n_years) CPI Dec-Dec %
    drawn_rgdp_pct = rgdp_uni[idx]           # (P, n_years) real GDP growth %

    # ---- Per-path cumulative CPI level (indexed to 1.0 at start of birth) ----
    cpi_factor = 1.0 + drawn_cpi_pct / 100.0
    cpi_level  = np.cumprod(cpi_factor, axis=1)             # (P, n_years)

    # The 2025-index within each path:
    #   for cohort A (born 1960, retire 2025): index = 65 (last year)
    #   for cohort D (born 1990, retire 2055): index = 35
    idx_2025 = 2025 - birth_year
    cpi_2025_path = cpi_level[:, idx_2025]                  # (P,)
    deflator = cpi_2025_path[:, None] / cpi_level           # (P, n_years)

    # ---- Compute K1+K2 deposits per year per path ----
    deposits_real = np.zeros((n_paths, n_years))
    for i, y in enumerate(years):
        d_year = det[y]
        prev_y = y - 1
        prev_M2_dollars = (det[prev_y]["M2"] * 1e9) if prev_y in det else d_year["M2"] * 1e9
        pop_persons = d_year["pop"] * 1e6
        gdp_pc_dollars = (d_year["GDP"] * 1e9) / pop_persons

        k1_nom = gdp_pc_dollars * K1_FRACTION if i == 0 else 0.0

        rgdp_year = np.maximum(0.0, drawn_rgdp_pct[:, i] / 100.0)  # (P,)
        k2_nom_per_path = (rgdp_year * prev_M2_dollars * K2_FRACTION) / pop_persons
        nominal_deposit = k1_nom + k2_nom_per_path
        deposits_real[:, i] = nominal_deposit * deflator[:, i]

    # ---- Compound at the path-drawn real returns ----
    balance = np.zeros(n_paths)
    for i in range(n_years):
        balance = (balance + deposits_real[:, i]) * (1.0 + drawn_returns[:, i])

    return balance


# =============================================================================
# Configuration runner
# =============================================================================

def run_all(n_paths=10000, base_seed=20260512, post_real_eq=0.045):
    """
    Run all 16 configurations: 4 cohorts x 2 universes x 2 methods.
    Returns dict[(cohort_name, universe, method)] = np.ndarray.
    """
    results = {}
    config_id = 0
    for cohort_name, birth, retire in COHORTS:
        for universe in ["1929-2025", "1960-2025"]:
            for method in ["iid", "block"]:
                seed = base_seed + config_id
                balances = simulate_cohort(
                    birth, retire, n_paths, universe, method,
                    post_real_eq, seed,
                )
                results[(cohort_name, universe, method)] = balances
                config_id += 1
    return results


def summarize(results):
    """Return list of dicts with summary statistics per configuration."""
    summary = []
    for (cohort, universe, method), bal in results.items():
        bench = BENCHMARKS[cohort]
        summary.append({
            "cohort":      cohort,
            "universe":    universe,
            "method":      method,
            "n_paths":     len(bal),
            "P5":          np.percentile(bal,  5),
            "P25":         np.percentile(bal, 25),
            "P50":         np.percentile(bal, 50),
            "P75":         np.percentile(bal, 75),
            "P95":         np.percentile(bal, 95),
            "mean":        bal.mean(),
            "p_below_med": (bal < bench["med"]).mean()  * 100,
            "p_below_mean":(bal < bench["mean"]).mean() * 100,
        })
    return summary


if __name__ == "__main__":
    import time
    t0 = time.time()
    print("Running 16 configurations x 10,000 paths each...")
    results = run_all(n_paths=10000)
    dt = time.time() - t0
    print(f"Done in {dt:.1f}s.\n")

    summary = summarize(results)
    fmt = lambda v: f"${v/1000:>6,.0f}K" if v < 1e6 else f"${v/1e6:>5,.2f}M"
    print(f"{'Cohort':<7}{'Universe':<11}{'Method':<7}"
          f"{'P5':>10}{'P25':>10}{'P50':>10}{'P75':>10}{'P95':>10}{'Mean':>10}"
          f"{'<med':>7}{'<mean':>8}")
    print("-" * 110)
    for s in summary:
        print(f"{s['cohort']:<7}{s['universe']:<11}{s['method']:<7}"
              f"{fmt(s['P5']):>10}{fmt(s['P25']):>10}{fmt(s['P50']):>10}"
              f"{fmt(s['P75']):>10}{fmt(s['P95']):>10}{fmt(s['mean']):>10}"
              f"{s['p_below_med']:>6.1f}%{s['p_below_mean']:>7.1f}%")

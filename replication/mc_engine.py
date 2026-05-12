"""
Monte Carlo engine for v7 — uses the corrected CSV.

Implements the same methodology as v6 (1929-2025 and 1960-2025 universes,
IID and block bootstrap, 10,000 paths per config, joint resampling of
(return, CPI, real_gdp_growth) triples) but using the CORRECTED
sp500_real_total_return_pct column from the CSV.

For the 1929-2025 universe, the years 1929-1959 are inlined here from
Damodaran/BLS/BEA historical sources, since the CSV only covers 1960-2025.
"""
import csv
import numpy as np

# ── Load 1960-2025 from CSV ───────────────────────────────────────────────
PATH = "citizens_standard_historical_data_1960_2025.csv"
CSV_DATA = {}
with open(PATH) as f:
    for row in csv.DictReader(f):
        y = int(row["year"])
        CSV_DATA[y] = {
            "M2":   float(row["m2_billions_usd"]) * 1e9,
            "GDP":  float(row["gdp_nominal_billions_usd"]) * 1e9,
            "pop":  float(row["population_millions"]) * 1e6,
            "CPI":  float(row["cpi_u_index_1982_84_eq_100"]),
            "eqR":  float(row["sp500_real_total_return_pct"]) / 100.0,
            "rgdp": float(row["real_gdp_growth_pct"]) / 100.0,
            "cpi_pct": float(row["cpi_decdec_pct"]) / 100.0,
        }

# ── 1929-1959 pre-CSV data (Damodaran nominal + BLS CPI + BEA real GDP) ────
# These are used ONLY for the 1929-2025 bootstrap universe; the deterministic
# Cohort A calculation starts at 1960 and is unaffected.
# Real return = Fisher-deflated: (1+nominal)/(1+cpi)-1
PRE_1960_NOM_RETURN = {
    1929: -0.0830, 1930: -0.2512, 1931: -0.4384, 1932: -0.0864, 1933: 0.4998,
    1934: -0.0119, 1935: 0.4674,  1936: 0.3194,  1937: -0.3534, 1938: 0.2928,
    1939: -0.0110, 1940: -0.1067, 1941: -0.1277, 1942: 0.1917, 1943: 0.2506,
    1944: 0.1903,  1945: 0.3582,  1946: -0.0843, 1947: 0.0520, 1948: 0.0570,
    1949: 0.1830,  1950: 0.3081,  1951: 0.2368,  1952: 0.1815, 1953: -0.0121,
    1954: 0.5256,  1955: 0.3260,  1956: 0.0744,  1957: -0.1046, 1958: 0.4372,
    1959: 0.1206,
}
PRE_1960_CPI_PCT = {
    1929: 0.002, 1930: -0.064, 1931: -0.093, 1932: -0.103, 1933: 0.008,
    1934: 0.015, 1935: 0.030,  1936: 0.014,  1937: 0.029,  1938: -0.028,
    1939: 0.000, 1940: 0.007,  1941: 0.050,  1942: 0.109,  1943: 0.061,
    1944: 0.017, 1945: 0.023,  1946: 0.183,  1947: 0.090,  1948: 0.027,
    1949: -0.018, 1950: 0.057, 1951: 0.060,  1952: 0.008,  1953: 0.007,
    1954: -0.007, 1955: 0.004, 1956: 0.029,  1957: 0.030,  1958: 0.018,
    1959: 0.015,
}
PRE_1960_REAL_GDP = {  # BEA chain-weighted real GDP growth, %
    1929: 6.4, 1930: -8.5, 1931: -6.4, 1932: -12.9, 1933: -1.3, 1934: 10.8,
    1935: 8.9, 1936: 12.9, 1937: 5.1,  1938: -3.3,  1939: 8.0,  1940: 8.8,
    1941: 17.7, 1942: 18.9, 1943: 17.0, 1944: 8.0,  1945: -1.0, 1946: -11.6,
    1947: -1.1, 1948: 4.1,  1949: -0.5, 1950: 8.7,  1951: 8.0,  1952: 4.1,
    1953: 4.7, 1954: -0.6, 1955: 7.1,  1956: 2.1,  1957: 2.1,  1958: -0.7,
    1959: 6.9,
}

def build_universe(start, end):
    """Return list of (real_return, cpi_pct, real_gdp_growth) tuples."""
    triples = []
    for y in range(start, end+1):
        if y in CSV_DATA:
            d = CSV_DATA[y]
            triples.append((d["eqR"], d["cpi_pct"], d["rgdp"]))
        else:
            nom = PRE_1960_NOM_RETURN[y]
            cpi = PRE_1960_CPI_PCT[y]
            real = (1+nom)/(1+cpi) - 1
            rgdp = PRE_1960_REAL_GDP[y] / 100.0
            triples.append((real, cpi, rgdp))
    return np.array(triples)  # shape (N, 3)

UNIVERSE_FULL = build_universe(1929, 2025)
UNIVERSE_60   = build_universe(1960, 2025)

# ── Project deterministic M2/GDP/pop/CPI ──────────────────────────────────
# We do NOT randomize these; only the (return, cpi, rgdp) triple
# determines stochastic outcomes year-by-year for K2 and balance growth.
PROJ = {}
for y in range(2026, 2056):
    p = CSV_DATA[y-1] if y-1 == 2025 else PROJ[y-1]
    PROJ[y] = {
        "M2":  p["M2"]*1.045,
        "GDP": p["GDP"]*1.040,
        "pop": p["pop"]*1.004,
        "CPI": p["CPI"]*1.025,
    }

CPI_2025 = CSV_DATA[2025]["CPI"]

def get_year_macros(y):
    """Return (M2_prev_year, pop, CPI, GDP) for year y, drawing on CSV/PROJ."""
    if y in CSV_DATA:
        d = CSV_DATA[y]
        prev_m2 = CSV_DATA[y-1]["M2"] if y-1 in CSV_DATA else d["M2"]
        return prev_m2, d["pop"], d["CPI"], d["GDP"]
    else:
        d = PROJ[y]
        prev = CSV_DATA[2025] if y-1 == 2025 else PROJ[y-1]
        return prev["M2"], d["pop"], d["CPI"], d["GDP"]


def simulate_cohort(birth, retire, universe, n_paths, method="block", block_size=5, seed=0):
    """
    Run Monte Carlo simulation for a cohort.

    universe: array of (real_return, cpi_pct, rgdp) triples to resample from
    method:   'iid' or 'block'
    n_paths:  number of bootstrap paths

    Returns:  np.array of final balances, length n_paths
    """
    rng = np.random.default_rng(seed)
    years = retire - birth + 1
    N = len(universe)
    balances = np.zeros(n_paths)

    for path in range(n_paths):
        # Generate the bootstrap year-index sequence
        if method == "iid":
            indices = rng.integers(0, N, size=years)
        elif method == "block":
            # Moving block bootstrap: pick start positions, take blocks of block_size
            n_blocks = (years + block_size - 1) // block_size
            starts = rng.integers(0, N - block_size + 1, size=n_blocks)
            indices = np.concatenate([np.arange(s, s+block_size) for s in starts])[:years]
        else:
            raise ValueError(method)

        bal = 0.0
        for i, age in enumerate(range(years)):
            y = birth + age
            prev_m2, pop, cpi, gdp = get_year_macros(y)
            gdp_pc = gdp / pop
            # K1 only at birth
            k1_nom = gdp_pc * 0.025 if age == 0 else 0.0
            # K2: use *resampled* real GDP growth, but the M2 base is the
            # deterministic historical M2 — this preserves the K2 = f(rgdp,M2)
            # mechanism while randomizing the rgdp driver.
            real_ret, _cpi_draw, rgdp_draw = universe[indices[i]]
            rgdp_eff = max(0.0, rgdp_draw)
            k2_nom = (rgdp_eff * prev_m2 * 0.5) / pop
            # Deflate nominal deposits to 2025$ using the deterministic CPI
            # path (we don't randomize the price level, only the growth rate)
            k1r = k1_nom * (CPI_2025 / cpi)
            k2r = k2_nom * (CPI_2025 / cpi)
            bal = (bal + k1r + k2r) * (1 + real_ret)
        balances[path] = bal

    return balances


if __name__ == "__main__":
    import json, time
    cohorts = [("A",1960,2025),("B",1970,2035),("C",1980,2045),("D",1990,2055)]
    MEDIAN = {"A":260000,"B":240000,"C":220000,"D":210000}
    MEAN   = {"A":669230,"B":649230,"C":629230,"D":619230}

    universes = {"1929-2025": UNIVERSE_FULL, "1960-2025": UNIVERSE_60}
    methods = ["iid", "block"]

    all_results = {}
    t0 = time.time()
    for uname, U in universes.items():
        for m in methods:
            for cname, b, r in cohorts:
                seed = hash((uname, m, cname)) & 0xffffffff
                bals = simulate_cohort(b, r, U, n_paths=10000, method=m, seed=seed)
                key = f"{cname}_{uname}_{m}"
                all_results[key] = {
                    "P5": float(np.percentile(bals, 5)),
                    "P25": float(np.percentile(bals, 25)),
                    "P50": float(np.percentile(bals, 50)),
                    "P75": float(np.percentile(bals, 75)),
                    "P95": float(np.percentile(bals, 95)),
                    "mean": float(np.mean(bals)),
                    "p_below_median": float(np.mean(bals < MEDIAN[cname])),
                    "p_below_mean":   float(np.mean(bals < MEAN[cname])),
                }
                # Save raw distributions for figure generation
                np.save(f"/home/claude/p2/mc_{key}.npy", bals)
    elapsed = time.time() - t0
    print(f"Elapsed: {elapsed:.1f}s")

    # Write JSON summary
    with open("/home/claude/p2/mc_results.json", "w") as f:
        json.dump(all_results, f, indent=2)

    # Print key table M1: 1929-2025 block bootstrap
    print("\n=== TABLE M1: 1929-2025 universe, block bootstrap ===")
    print(f"{'Cohort':<8}{'P5':>8}{'P25':>8}{'P50':>8}{'P75':>8}{'P95':>8}{'Mean':>8}{'P<med':>8}{'P<mean':>9}")
    for cname, _, _ in cohorts:
        k = f"{cname}_1929-2025_block"
        r = all_results[k]
        print(f"{cname:<8}${r['P5']/1000:>5.0f}K ${r['P25']/1000:>5.0f}K ${r['P50']/1000:>5.0f}K "
              f"${r['P75']/1000:>5.0f}K ${r['P95']/1000:>5.0f}K ${r['mean']/1000:>5.0f}K "
              f"{r['p_below_median']*100:>5.1f}%  {r['p_below_mean']*100:>5.1f}%")

    # Print Table M2: configuration sensitivity
    print("\n=== TABLE M2: All configurations ===")
    print(f"{'Cohort':<8}{'Configuration':<20}{'P50':>10}{'P5':>10}{'P<med':>10}")
    for cname, _, _ in cohorts:
        for uname in ["1929-2025","1960-2025"]:
            for m in ["iid","block"]:
                k = f"{cname}_{uname}_{m}"
                r = all_results[k]
                print(f"{cname:<8}{uname+', '+m.upper():<20}${r['P50']/1000:>8.0f}K "
                      f"${r['P5']/1000:>8.0f}K {r['p_below_median']*100:>8.1f}%")

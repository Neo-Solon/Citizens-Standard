"""
Definitive computation under Paper 2's stated methodology, using the
PURE BEA chain-weighted real GDP growth series (FRED A191RP1A027NBEA).

This replaces the CSV's hybrid real_gdp_growth_pct column with the
authoritative BEA series that Section 2.2 of the paper commits to.
All other inputs (M2, GDP nominal, population, CPI, S&P real returns)
come from the CSV and are unchanged.
"""
import csv

# ── Load CSV for the five non-disputed columns ────────────────────────────
PATH = "citizens_standard_historical_data_1960_2025.csv"
DATA = {}
with open(PATH) as f:
    for row in csv.DictReader(f):
        y = int(row["year"])
        DATA[y] = {
            "M2":   float(row["m2_billions_usd"]) * 1e9,
            "GDP":  float(row["gdp_nominal_billions_usd"]) * 1e9,
            "pop":  float(row["population_millions"]) * 1e6,
            "CPI":  float(row["cpi_u_index_1982_84_eq_100"]),
            "eqR":  float(row["sp500_real_total_return_pct"]) / 100.0,
        }

# ── PURE BEA chain-weighted real GDP growth (FRED A191RP1A027NBEA) ────────
# Source: BEA NIPA Table 1.1.1, "Percent Change from Preceding Period in
# Real Gross Domestic Product." This is the authoritative series the paper
# commits to in Section 2.2.
REAL_GDP_GROWTH_BEA = {
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
    2025: 2.00,
}
# Inject into DATA
for y, v in REAL_GDP_GROWTH_BEA.items():
    DATA[y]["rgdp"] = v / 100.0

# ── Project DATA forward to 2055 (CBO baseline) ───────────────────────────
POST_REAL_GDP = 0.018      # 1.8% real GDP growth
POST_M2_NOM   = 0.045      # 4.5% nominal M2 growth
POST_POP      = 0.004      # 0.4% population growth
POST_CPI_PCT  = 2.5        # 2.5% Dec-Dec CPI inflation
POST_GDP_NOM  = 0.040      # 4.0% nominal GDP growth

for y in range(2026, 2056):
    prev = DATA[y-1]
    DATA[y] = {
        "M2":   prev["M2"]  * (1 + POST_M2_NOM),
        "GDP":  prev["GDP"] * (1 + POST_GDP_NOM),
        "pop":  prev["pop"] * (1 + POST_POP),
        "CPI":  prev["CPI"] * (1 + POST_CPI_PCT/100.0),
        "eqR":  None,
        "rgdp": POST_REAL_GDP,
    }

CPI_2025 = DATA[2025]["CPI"]
def to_2025(nominal, year):
    return nominal * (CPI_2025 / DATA[year]["CPI"])

# ── Stress sequences ──────────────────────────────────────────────────────
DEPR_NOM = [-8.30, -25.12, -43.84, -8.64, 49.98, -1.19, 46.74, 31.94,
            -35.34, 29.28, -1.10, -10.67, -12.77, 19.17, 25.06, 19.03, 35.82]
DEPR_CPI = [-0.2, -6.4, -9.3, -10.3, 0.8, 1.5, 3.0, 1.4, 2.9, -2.8,
             0.0, 0.7, 5.0, 10.9, 6.1, 1.7, 2.3]
STAG_NOM = [-9.97, 23.80, 10.81, -8.24, 3.56, 14.22, 18.76, -14.31, -25.90,
             37.00, 23.83, -6.98, 6.51, 18.52, 31.74, -4.70, 20.42]
STAG_CPI = [2.86, 3.09, 4.19, 5.46, 5.72, 4.38, 3.21, 6.16, 11.03,
             9.14, 5.76, 6.50, 7.62, 11.22, 13.58, 10.35, 6.16]


def compute(birth, retire, post_real_eq, stress=None, return_decomp=False):
    """
    Returns either final balance, or full decomposition dict if return_decomp=True.
    Methodology:
      - K1 = 2.5% of GDP per capita at birth year
      - K2 = 0.5 × max(0, BEA real GDP growth) × M2[y-1] / pop[y]
      - Each year's deposits deflated to 2025$ via CPI ratio
      - Compound at S&P real return (or stress override, or post-2025 scenario)
      - Convention: deposit at start of year, earn that year's return
    """
    if stress:
        s_nom = stress["nom"]
        s_cpi = stress["cpi"]
        s_start = stress.get("start_age", 25)
        s_len   = stress.get("len", 17)

    balance = 0.0
    k1_real_total = 0.0
    k2_real_total = 0.0

    for y in range(birth, retire + 1):
        age = y - birth
        d = DATA[y]
        gdp_pc = d["GDP"] / d["pop"]

        k1_nom = gdp_pc * 0.025 if y == birth else 0.0
        prev_m2 = DATA[y-1]["M2"] if y > birth else d["M2"]
        rgdp = max(0.0, d["rgdp"])
        k2_nom = (rgdp * prev_m2 * 0.5) / d["pop"]

        k1_real = to_2025(k1_nom, y)
        k2_real = to_2025(k2_nom, y)
        k1_real_total += k1_real
        k2_real_total += k2_real

        # Real return for year
        if stress and s_start <= age < s_start + s_len:
            i = age - s_start
            eq = (1 + s_nom[i]/100) / (1 + s_cpi[i]/100) - 1
        elif y <= 2025:
            eq = d["eqR"]
        else:
            eq = post_real_eq

        balance = (balance + k1_real + k2_real) * (1 + eq)

    if return_decomp:
        total_dep = k1_real_total + k2_real_total
        return {
            "balance": balance,
            "k1_real": k1_real_total,
            "k2_real": k2_real_total,
            "deposits": total_dep,
            "gain": balance - total_dep,
            "principal_share": total_dep / balance * 100,
            "compound_share": (balance - total_dep) / balance * 100,
        }
    return balance


# ── Reference benchmarks ──────────────────────────────────────────────────
MEDIAN = {"A": 260000, "B": 240000, "C": 220000, "D": 210000}
MEAN   = {"A": 669230, "B": 649230, "C": 629230, "D": 619230}
SS     = {"A": 24953,  "B": 19214,  "C": 19214,  "D": 19214}

cohorts = [("A", 1960, 2025), ("B", 1970, 2035),
           ("C", 1980, 2045), ("D", 1990, 2055)]


# ── Table 1: Central scenario ─────────────────────────────────────────────
print("=" * 82)
print("TABLE 1 — CENTRAL SCENARIO (4.5% real equity post-2025)")
print("Pure BEA chain-weighted real GDP growth")
print("=" * 82)
print(f"{'Cohort':<7}{'Born':<6}{'Retires':<9}{'Floor (2025$)':>17}{'vs Median':>12}{'vs Mean':>11}")
print("-" * 82)

central = {}
for name, b, r in cohorts:
    res = compute(b, r, post_real_eq=0.045, return_decomp=True)
    central[name] = res
    bal = res["balance"]
    print(f"{name:<7}{b:<6}{r:<9}${bal:>15,.0f}{bal/MEDIAN[name]:>11.1f}×{bal/MEAN[name]:>10.1f}×")

print()
print("=" * 82)
print("TABLE 2 — ANNUAL INCOME (4% withdrawal + Social Security)")
print("=" * 82)
print(f"{'Cohort':<7}{'CS income':>14}{'Med actual':>14}{'Mean actual':>14}")
print("-" * 82)
for name, _, _ in cohorts:
    bal = central[name]["balance"]
    cs_inc   = bal * 0.04 + SS[name]
    med_inc  = MEDIAN[name] * 0.04 + SS[name]
    mean_inc = MEAN[name]   * 0.04 + SS[name]
    print(f"{name:<7}${cs_inc:>12,.0f}${med_inc:>12,.0f}${mean_inc:>12,.0f}")

print()
print("=" * 82)
print("COHORT D — THREE SCENARIOS (Section 4.4)")
print("=" * 82)
print(f"{'Scenario':<22}{'Real return':>13}{'Floor (2025$)':>18}{'vs Med':>10}{'vs Mean':>10}")
print("-" * 82)
for label, eqr in [("Pessimistic", 0.030), ("Central", 0.045), ("Historical", 0.065)]:
    bal = compute(1990, 2055, post_real_eq=eqr)
    print(f"{label:<22}{eqr*100:>11.1f}%  ${bal:>15,.0f}{bal/MEDIAN['D']:>9.1f}×{bal/MEAN['D']:>9.1f}×")

print()
print("=" * 82)
print("SECTION 4.5 DECOMPOSITION — Cohort A central")
print("=" * 82)
A = central["A"]
print(f"  K1 at birth (real 2025$):    ${A['k1_real']:>12,.2f}")
print(f"  K2 cumulative (real 2025$):  ${A['k2_real']:>12,.2f}")
print(f"  Total deposits:              ${A['deposits']:>12,.2f}  ({A['principal_share']:.1f}%)")
print(f"  Compound gain:               ${A['gain']:>12,.2f}  ({A['compound_share']:.1f}%)")
print(f"  Final Stable Floor:          ${A['balance']:>12,.2f}")

print()
print("=" * 82)
print("TABLE 3 — STRESS TESTS (Depression / Stagflation, ages 25-41)")
print("=" * 82)
print(f"{'Cohort':<7}{'Central':>14}{'Depression':>14}{'Stagflation':>14}"
      f"{'D ratio':>10}{'S ratio':>10}{'D vs Med':>11}{'S vs Med':>11}")
print("-" * 82)

stress_results = {}
for name, b, r in cohorts:
    cent = central[name]["balance"]
    depr = compute(b, r, 0.045, stress={"nom": DEPR_NOM, "cpi": DEPR_CPI})
    stag = compute(b, r, 0.045, stress={"nom": STAG_NOM, "cpi": STAG_CPI})
    stress_results[name] = {"cent": cent, "depr": depr, "stag": stag}
    print(f"{name:<7}${cent:>12,.0f}${depr:>12,.0f}${stag:>12,.0f}"
          f"{depr/cent:>9.2f}×{stag/cent:>9.2f}×"
          f"{depr/MEDIAN[name]:>10.1f}×{stag/MEDIAN[name]:>10.1f}×")

print()
print("=" * 82)
print("BELOW-MEDIAN FINDINGS")
print("=" * 82)
for name in ["A", "B", "C", "D"]:
    r = stress_results[name]
    flags = []
    if r["depr"] < MEDIAN[name]: flags.append(f"Depression (${r['depr']:,.0f})")
    if r["stag"] < MEDIAN[name]: flags.append(f"Stagflation (${r['stag']:,.0f})")
    if flags:
        print(f"  Cohort {name}: BELOW median (${MEDIAN[name]:,}) under: {', '.join(flags)}")
    else:
        print(f"  Cohort {name}: above median under both stress scenarios")

print()
depr_ratios = [stress_results[c]["depr"]/stress_results[c]["cent"]*100 for c in "ABCD"]
stag_ratios = [stress_results[c]["stag"]/stress_results[c]["cent"]*100 for c in "ABCD"]
print(f"Depression retention range: {min(depr_ratios):.0f}%–{max(depr_ratios):.0f}%")
print(f"Stagflation retention range: {min(stag_ratios):.0f}%–{max(stag_ratios):.0f}%")

print()
print("=" * 82)
print("ABSTRACT HEADLINE RANGE (central, Mode B vs median)")
print("=" * 82)
ratios = [central[c]["balance"]/MEDIAN[c] for c in "ABCD"]
print(f"  Mode B beats median by {min(ratios):.1f}× to {max(ratios):.1f}×")

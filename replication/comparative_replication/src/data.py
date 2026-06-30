"""
data.py - Sourced figures for the Paper 13 comparative grounding.

Every number below carries a `src` tag that resolves to a full citation in
AUDIT.md. Nothing here is invented: each value is either (a) a published figure
from a primary source (SSA, APFC, Alaska DOR, BLS, peer-reviewed studies), or
(b) a figure computed elsewhere in this replication suite (the Citizens Standard
column is imported from architecture_replication, not re-derived here).

Design note (read before using these numbers):
Paper 13 is a POSITIONING paper, not a head-to-head horse-race (see its Section 7).
The systems differ in KIND - Georgism is a funding base, not a distribution; Social
Security is contributory retirement income, not a universal working-age flow; the
Citizens Standard is theoretical, with no operating record. So the comparable axes
below (annual per-person benefit, owned wealth stock per person, track record,
capture history) are computed ONLY where the comparison is meaningful, and every
"not comparable / differs in kind" case is flagged explicitly rather than forced
onto a single ranking. The grounding backs each claim with real figures; it does
NOT manufacture a single winner.
"""

from dataclasses import dataclass, field
from typing import Optional


@dataclass
class Figure:
    value: object
    unit: str
    src: str            # resolves to AUDIT.md
    note: str = ""


# ---------------------------------------------------------------------------
# 1. SOVEREIGN WEALTH FUND / ALASKA PERMANENT FUND  (maturity: PROVEN)
# ---------------------------------------------------------------------------
ALASKA = {
    "funding": Figure("resource rents (oil/mineral royalties)", "category", "APFC-2024",
                      ">=25% of mineral royalties constitutionally dedicated"),
    "builds": Figure("wealth stock + annual dividend", "category", "APFC-2024"),
    "coverage": Figure("universal among residents", "category", "DOR-PFD",
                       "1 full calendar year residency; ~600-640k recipients"),
    "price_brake": Figure(False, "bool", "structural", "no inflation-control mechanism"),
    "maturity": Figure("proven", "category", "WIKI-APF", "43rd dividend year in 2024"),

    # hard numbers
    "fund_value_usd": Figure(85.1e9, "USD", "APFC-2025",
                             "$85.1B as of 30 Jun 2025 (APFC 2025 Annual Report); $86.3B at 31 Dec 2025"),
    "fund_value_2019_usd": Figure(64e9, "USD", "WIKI-APF", "2019 reference point"),
    "recipients": Figure(640000, "people", "DOR-PFD-2024", "~600-640k eligible Alaskans"),
    "dividend_2024_usd": Figure(1702.0, "USD/yr", "DOR-PFD-2024",
                                "$1,403.83 base + $298.17 energy relief (HB268)"),
    "dividend_2023_usd": Figure(1312.0, "USD/yr", "AKPUB-2024"),
    "dividend_2025_usd": Figure(1000.0, "USD/yr", "DOR-PFD-2025"),
    "dividend_min_usd": Figure(331.29, "USD/yr", "WIKI-APF", "1984, lowest ever"),
    "dividend_max_usd": Figure(3284.0, "USD/yr", "WIKI-APF", "2022, highest ever"),
    "dividend_avg_usd": Figure(1600.0, "USD/yr", "WIKI-APF",
                               "long-run average per resident, 2019 dollars"),

    # capture-resistance (the cautionary case named on the paper's axis)
    "capture": Figure("corpus constitutionally protected; earnings are general-fund money",
                      "category", "WIKI-APF",
                      "statutory dividend formula not followed since 2016 (POMV politics)"),

    # empirical effects (answers 'does an unconditional transfer kill work / harm')
    "employment_effect": Figure("no effect on full-time employment; +1.8pp part-time",
                                "finding", "JONES-MARION-2018", "NBER, synthetic control"),
    "poverty_effect": Figure("reduced Alaskans below poverty line by 20-40%",
                             "finding", "BERMAN-2024", "Poverty & Public Policy"),
}

# Documented anchor points of the PFD series (NOT a fabricated full series).
# The complete year-by-year history is published at pfd.alaska.gov; we encode the
# sourced anchors and use the published long-run average for the comparison.
ALASKA_PFD_ANCHORS = [
    # year, nominal USD, source-tag
    (1982, 1000.00, "DOR-PFD"),     # first dividend
    (1984,  331.29, "WIKI-APF"),    # lowest ever
    (2008, 2069.00, "WIKI-APF"),    # +$1,200 Palin resource rebate that year was separate
    (2015, 2072.00, "WIKI-APF"),    # pre-cap peak era
    (2016, 1022.00, "WIKI-APF"),    # first capped year (Walker veto) -> capture begins
    (2022, 3284.00, "WIKI-APF"),    # highest ever
    (2023, 1312.00, "AKPUB-2024"),
    (2024, 1702.00, "DOR-PFD-2024"),
    (2025, 1000.00, "DOR-PFD-2025"),
]

# ---------------------------------------------------------------------------
# 2. SOCIAL SECURITY  (maturity: PROVEN)
# ---------------------------------------------------------------------------
SOCIAL_SECURITY = {
    "funding": Figure("payroll tax, pay-as-you-go", "category", "SSA-TR-2024",
                      "91.2% of revenue from payroll tax (2024)"),
    "builds": Figure("income flow, no property right", "category", "FLEMMING-1960",
                     "Flemming v. Nestor, 363 U.S. 603 (1960): no accrued property right"),
    "coverage": Figure("contributory", "category", "SSA-TR-2024",
                       "~68M beneficiaries; tied to covered earnings history"),
    "price_brake": Figure(False, "bool", "structural", "COLA indexes benefits TO inflation; no control of it"),
    "maturity": Figure("proven", "category", "SSA-TR-2024", "since 1935; national scale"),

    "beneficiaries": Figure(68e6, "people", "SSA-2024"),
    "replacement_rate_medium": Figure(0.40, "fraction", "SSA-OACT",
                                      "~40% of pre-retirement earnings, medium earner"),
    "avg_benefit_usd_mo": Figure(1900.0, "USD/mo", "SSA-2024", "approx. retired-worker average"),
    "oasi_depletion_year": Figure(2033, "year", "SSA-TR-2024",
                                  "OASI reserves depleted; combined OASDI ~2034-2035"),
    "payable_at_depletion": Figure(0.77, "fraction", "CBO-2024",
                                   "~77% of scheduled payable -> ~23% cut at depletion"),
    "actuarial_deficit_pct_payroll": Figure(3.82, "pct", "SSA-TR-2025",
                                            "75-year deficit, 2025 report"),
    "unfunded_obligation_usd": Figure(22.6e12, "USD", "SSA-TR-2024",
                                      "present-value unfunded obligation through 2098"),
}

# ---------------------------------------------------------------------------
# 3. UNIVERSAL BASIC INCOME  (maturity: PILOTS ONLY)
# ---------------------------------------------------------------------------
UBI = {
    "funding": Figure("general taxation", "category", "YANG-FD",
                      "Yang 'Freedom Dividend' proposed a VAT"),
    "builds": Figure("income flow", "category", "structural", "no owned, compounding stock"),
    "coverage": Figure("universal (proposed)", "category", "YANG-FD"),
    "price_brake": Figure(False, "bool", "structural"),
    "maturity": Figure("pilots", "category", "WIKI-UBI",
                       "no permanent national UBI; many city/region pilots"),

    "canonical_monthly_usd": Figure(1000.0, "USD/mo", "YANG-FD",
                                    "$1,000/mo per adult, the canonical US proposal"),
    "us_adults": Figure(258e6, "people", "CENSUS", "approx. 18+ population, used for gross-cost calc"),
    # pilots
    "stockton_amount_usd_mo": Figure(500.0, "USD/mo", "SEED-2021", "125 residents, 24 months"),
    "stockton_employment": Figure("full-time employment 28%->40% vs control 32%->37%",
                                  "finding", "SEED-2021"),
    "finland_amount_eur_mo": Figure(560.0, "EUR/mo", "KELA-FIN", "2,000 unemployed, 2017-18"),
    "finland_employment": Figure("mild positive employment effect; higher wellbeing",
                                "finding", "KELA-FIN"),
    "ontario_outcome": Figure("3-yr pilot cancelled after 1 yr on cost grounds",
                             "finding", "WIKI-UBI"),
}

# ---------------------------------------------------------------------------
# 4. GEORGISM / LAND-VALUE TAX  (maturity: PARTIAL; FUNDING SOURCE ONLY)
# ---------------------------------------------------------------------------
GEORGISM = {
    "funding": Figure("land rents", "category", "GEORGE-1879"),
    "builds": Figure("funding source only (no distribution)", "category", "structural",
                     "an LVT raises revenue; it does not itself distribute a benefit"),
    "coverage": Figure("n/a", "category", "structural"),
    "price_brake": Figure(False, "bool", "structural"),
    "maturity": Figure("partial", "category", "WIKI-LVT",
                       "Estonia, Pennsylvania split-rate, Denmark; no national single-tax"),

    "us_lvt_revenue_low_usd": Figure(1.1e12, "USD/yr", "LEP-2019",
                                     "national 100% LVT, low estimate"),
    "us_lvt_revenue_high_usd": Figure(3.36e12, "USD/yr", "LEP-2019",
                                      "national 100% LVT, high estimate (25-76% of govt spending)"),
    "deadweight_loss": Figure(0.0, "approx", "NIELSSON-LVT",
                              "~zero; land supply inelastic. Empirically null effect on development"),
    "efficiency_status": Figure("most efficient major tax base ('least bad tax', Friedman)",
                               "finding", "WIKI-LVT", "accepted since Smith/Ricardo; Arnott-Stiglitz 1979"),
}

# ---------------------------------------------------------------------------
# 5. CITIZENS STANDARD  (maturity: THEORETICAL)
# Figures IMPORTED from architecture_replication (not re-derived here).
# ---------------------------------------------------------------------------
CITIZENS_STANDARD = {
    "funding": Figure("growth-tied money issuance (self-financing)", "category", "CS-ARCH",
                      "not tax-dependent; issuance base scales with nominal growth"),
    "builds": Figure("wealth stock + dividend", "category", "CS-ARCH",
                     "locked, compounding, owned, bequeathable floor"),
    "coverage": Figure("universal", "category", "CS-ARCH"),
    "price_brake": Figure(True, "bool", "CS-MACRO",
                          "Tool 14 / KI inflation-gap stabilizer (Prop 6, Neo-Solon 2026e)"),
    "maturity": Figure("theoretical", "category", "structural", "no operating record"),

    "gdp_per_capita_usd": Figure(90000.0, "USD", "CS-ARCH", "model base"),
    # owned wealth stock at age 65 (real launch-year $), per person, by mode
    "floor_modeA_usd": Figure(233000.0, "USD", "CS-ARCH", "Mode A, GE realizable 5.4%"),
    "floor_modeB_usd": Figure(413000.0, "USD", "CS-ARCH", "Mode B, GE 4.3%, 60/40 split"),
    "floor_modeC_usd": Figure(232000.0, "USD", "CS-ARCH", "Mode C, GE 5.4%"),
    "floor_vs_median": Figure("0.81x-0.94x median on locked floor alone",
                             "ratio", "CS-EMPIRICAL", "Neo-Solon 2026b, Paper 2"),
    # annual dividend, per person, by mode
    "dividend_modeB_usd_yr": Figure(516.0, "USD/yr", "CS-ARCH", "$42.7/mo, Mode B 60/40"),
    "dividend_modeC_usd_yr": Figure(1293.0, "USD/yr", "CS-ARCH", "$108/mo, Mode C (KI $443B/342M, 1.98% of M2)"),
    # the honest vulnerability (named in the paper's Claim 4)
    "capture": Figure("issuance base disappears in contraction; procyclical dividend halts in downturns",
                     "category", "CS-CRISIS",
                     "Neo-Solon 2026l: 50% zero-dividend years in a Depression-class slump"),
}

SYSTEMS = {
    "UBI": UBI,
    "Social Security": SOCIAL_SECURITY,
    "SWF / Alaska": ALASKA,
    "Georgism (LVT)": GEORGISM,
    "Citizens Standard": CITIZENS_STANDARD,
}

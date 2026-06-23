# AUDIT — Paper 13 comparative grounding

Every figure in `src/data.py` carries a `src` tag. This file resolves each tag to
a primary source (or, where only a secondary summary was available, says so
explicitly). Nothing in the package is asserted without a tag here.

Principle followed: the systems compared differ in kind, so the package quantifies
only the axes that are genuinely comparable and flags every "differs in kind" cell
rather than forcing a single ranking. This honours Paper 13's Section 7, which
states the paper argues from structure, not a head-to-head empirical horse-race.

## Alaska Permanent Fund / sovereign wealth fund

| Tag | Source |
|---|---|
| DOR-PFD, DOR-PFD-2024, DOR-PFD-2025 | State of Alaska, Dept. of Revenue — Permanent Fund Dividend Division. 2024 PFD = $1,702 ($1,403.83 base + $298.17 energy relief, HB 268); 2025 PFD = $1,000. pfd.alaska.gov (full year-by-year history: pfd.alaska.gov/Division-Info/summary-of-dividend-applications-payments). |
| APFC-2024, APFC-2025, APFC-PERF | Alaska Permanent Fund Corporation. Total fund value **$85.1B as of 30 June 2025** (APFC 2025 Annual Report, "49 Forward"); $86.3B as of 31 Dec 2025 (2026 Mid-FY Review). Constitutionally, ≥25% of mineral royalties are dedicated to the Principal; the Earnings Reserve is spendable by simple legislative majority. apfc.org/2025-annual-report/ ; apfc.org/performance/ |
| WIKI-APF | "Alaska Permanent Fund," Wikipedia (accessed 2026): lowest dividend $331.29 (1984), highest $3,284 (2022); fund ~$64B (2019); long-run average ~$1,600/yr per resident in 2019 dollars; corpus constitutionally protected, earnings are general-fund money. Used for anchor points and ranges; primary series at pfd.alaska.gov. |
| AKPUB-2024 | Alaska Public Media, "Alaska Permanent Fund Dividend for 2024 is $1,702" (Sep 2024): 2023 PFD $1,312; >600k eligible. alaskapublic.org |
| JONES-MARION-2018 | Jones, D. & Marinescu, I. (2018). *The Labor Market Impacts of Universal and Permanent Cash Transfers: Evidence from the Alaska Permanent Fund.* NBER WP 24312. Finding: no effect on full-time employment; +1.8pp (17%) part-time. |
| BERMAN-2024 | 2024 study in *Poverty & Public Policy* (as summarized in the Alaska Permanent Fund Wikipedia entry): the dividend reduced the number of Alaskans below the US poverty threshold by 20–40%. Secondary summary; primary to be cited from the journal on final typeset. |

## Social Security

| Tag | Source |
|---|---|
| SSA-TR-2024 | *2024 OASDI Trustees Report* and Summary. ssa.gov/oact/trsum/ ; ssa.gov/oact/TRSUM/2024/. Payroll tax = 91.2% of revenue (2024); OASI reserve depletion 2033; combined OASDI ~2034–2035; present-value unfunded obligation ~$22.6T through 2098. |
| SSA-TR-2025 | 2025 Trustees Report, as summarized by the Center for Retirement Research (crr.bc.edu) and CRS (congress.gov/crs-product/IF13045): 75-year actuarial deficit 3.82% of taxable payroll. |
| SSA-2024 | SSA press release, May 2024 (ssa.gov/news): ~67–68M beneficiaries; benefits paid ~$1.38T (2023). |
| SSA-OACT | SSA Office of the Chief Actuary — replacement rate ~40% of pre-retirement earnings for a medium (average) earner (standard OACT figure). |
| CBO-2024 | CBO, *2024 Long-Term Projections for Social Security* (cbo.gov/publication/60679): at depletion (FY2034 combined), revenues ≈ 77% of scheduled outlays → ~23% benefit cut. |
| FLEMMING-1960 | *Flemming v. Nestor*, 363 U.S. 603 (1960): Social Security confers no accrued property right; benefits can be altered by Congress. (Also in Paper 13 references.) |

## Universal basic income

| Tag | Source |
|---|---|
| YANG-FD | A. Yang, 2020 "Freedom Dividend": $1,000/mo per adult, VAT-funded. The canonical US national UBI proposal. |
| CENSUS | US Census Bureau — ~258M adults (18+); used only for the gross-cost arithmetic (258M × $12,000 ≈ $3.1T/yr gross). |
| SEED-2021 | West, S. et al. (2021), Stockton Economic Empowerment Demonstration (SEED) preliminary analysis: $500/mo, 125 residents, 24 months; full-time employment 28%→40% (vs control 32%→37%); improved financial/physical/mental wellbeing. |
| KELA-FIN | Kela (Finland), basic income experiment 2017–2018 final results: €560/mo, 2,000 unemployed; mild positive employment effect; higher reported wellbeing, autonomy, security. |
| WIKI-UBI | "Universal basic income" / "Universal basic income pilots," Wikipedia (accessed 2026): no permanent national UBI; Ontario 3-year pilot cancelled after ~1 year on cost grounds. |

## Georgism / land-value tax

| Tag | Source |
|---|---|
| GEORGE-1879 | George, H. (1879). *Progress and Poverty.* (Paper 13 references.) |
| LEP-2019 | Economic Possibility / LEP, *Land Value Tax* policy report (2019 estimate): a national 100% LVT would raise ~$1.1T–$3.36T/yr (≈25–76% of total government spending). economicpossibility.org |
| WIKI-LVT | "Land value tax," Wikipedia (accessed 2026): land's inelastic supply means an LVT creates no deadweight loss ("least bad tax," Friedman; accepted since Smith/Ricardo). Estonia levies a state LVT funding municipalities (0.1–2.5%). |
| NIELSSON-LVT | Nielsson, U. (working paper), *The Incidence and Efficiency of Land Value Taxation*: empirically, higher land taxes show null effects on development → no efficiency cost. (See also Arnott & Stiglitz 1979, Henry George Theorem, in Paper 13 refs.) |

## Citizens Standard (imported, not re-derived here)

| Tag | Source |
|---|---|
| CS-ARCH | `architecture_replication/` (this suite) — Neo-Solon 2026a (Paper 1). GDP/capita $90,000; Stable-Floor balances at age 65 on the GE realizable return: Mode A ≈ $233K, Mode B ≈ $413K (60/40), Mode C ≈ $232K; dividends Mode B ≈ $43/mo ($516/yr), Mode C ≈ $199/mo ($2,388/yr). |
| CS-MACRO | `macro_replication/` — Neo-Solon 2026e (Paper 5), Proposition 6: the KI / Tool 14 inflation-gap stabilizer (the built-in price brake). |
| CS-EMPIRICAL | `empirical_replication/` — Neo-Solon 2026b (Paper 2): the locked floor universalizes ≈0.81×–0.94× the median household on the floor alone. |
| CS-CRISIS | `crisis_behaviour_replication/` — Neo-Solon 2026l (Paper 12): the dividend is procyclical and halts in downturns (≈50% zero-dividend years in a Depression-class slump); the issuance base contracts in a slump. The documented CS vulnerability behind Claim 4. |

## "structural" tag
Cells tagged `structural` are definitional properties of the system (e.g. UBI builds
a flow, not an owned stock; an LVT is a funding source that distributes nothing by
itself), not empirical measurements, and need no external source.

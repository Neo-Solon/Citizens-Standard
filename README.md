# The Citizens Standard — Interactive Engine

> **Build your own monetary system.** Interactive companion to *The Citizens Standard* — adjust the K1, K2, K3 issuance channels and see how a citizen retires under your rules vs. seven alternative frameworks.

A working tool for the constitutional monetary architecture introduced in *The Citizens Standard* ([SSRN link](https://papers.ssrn.com/sol3/papers.cfm?abstract_id=5575160)). Tune the framework's three issuance dials, watch the projection update live, and compare side-by-side against the Federal Reserve status quo, the Chicago Plan, Friedman's k-percent rule, Bitcoin, the Alaska Permanent Fund Dividend, tax-funded UBI, and Modern Monetary Theory. 

## The three Modes

The framework offers three reference configurations for the K1 / K2 / K3 issuance channels:

| Mode | K1 (citizenship) | K2 (growth) | K3 (dividend) | Result |
|------|------------------|-------------|---------------|--------|
| **A** | 2.5% of GDP per capita | 12.5% of real growth | 0% | Pure stable-floor wealth building |
| **B** | 2.5% of GDP per capita | 12.5% of real growth | 0.25% of M2 monthly | Wealth + small monthly dividend |
| **C** | 2.5% of GDP per capita | 12.5% of real growth | 0.50% of M2 monthly | Wealth + larger dividend, more inflation pressure |

Or build a **Custom** mode by adjusting any slider — the engine recalculates everything live.

## What's in this repo

| File | Purpose |
|------|---------|
| `Citizens_Standard_Builder.html` | Standalone web engine. Sliders, charts, comparison view. Open in any browser. |
| `Citizens_Standard_Builder.xlsx` | Six-sheet spreadsheet: Inputs, Projection, Summary, Comparison, Mode Presets, How It Works. |
| `replication/` | Empirical replication materials for Paper 2 (the counterfactual benchmark study). |
| `README.md` | This file. |

## Quick start

**Run the web engine.** Download `Citizens_Standard_Builder.html` and double-click it. It opens in your default browser. Adjust any slider; everything recalculates live. No installation, no server, works offline after first load.

**Open the spreadsheet.** Download `Citizens_Standard_Builder.xlsx` and open it in Excel, Numbers, LibreOffice Calc, or Google Sheets. Edit only the yellow cells; everything else recalculates from formulas.

**Run the empirical replication.** See `replication/README.md`.

## What you can adjust in the Engine

The engine exposes every variable the framework actually depends on:

- **Issuance channels** — K1, K2, K3 percentages
- **Macro environment** — real GDP growth, population growth, equity return, CPI inflation
- **Launch conditions** — M2 money supply, nominal GDP, population, projection horizon
- **Comparison settings** — personal savings rate, working-life span, Social Security replacement rate, UBI proposal level, MMT jobs guarantee wage

## Outputs

For your representative cohort (born at year 0, projected to the horizon you set):

- Stable Floor at horizon (real dollars, in launch-year purchasing power)
- Annual real income at retirement (at the 4% safe withdrawal rate)
- K3 monthly dividend per citizen
- Total annual issuance as percent of M2 and percent of GDP
- Year-by-year trajectories for M2, GDP, population, CPI, and the cohort's wealth

## Comparison tab

Side-by-side comparison of eight monetary systems under identical economic assumptions:

1. **Citizens Standard** — your current configuration
2. **Fed status quo** — personal savings + Social Security
3. **Chicago Plan** — 100% reserve banking + personal savings
4. **Friedman k-rule** — fixed money growth + personal savings
5. **Bitcoin / fixed-supply** — savings vehicle, no inflation response
6. **Alaska PFD-style** — sovereign wealth dividend at user-set level
7. **UBI** — tax-funded universal basic income
8. **MMT + jobs guarantee** — federal employment at $15/hr

Each shows what it structurally delivers to a representative citizen: locked wealth, lifetime cash transfers, annual retirement income, funding source, rules-based or not.

## Why this exists

The Citizens Standard makes a structural claim: that locked, rules-based citizen wealth and modest monthly dividends, funded entirely by seigniorage rather than taxation, can deliver retirement security comparable to or better than the existing patchwork — without expanding tax burdens. The engine lets you test that claim against your own assumptions, and against seven competing frameworks running on the same numbers. If Fed status quo wins on retirement income under a particular setting, the engine shows it. The engine doesn't hide the tension; it foregrounds it.

- Real-time Discussion: https://discord.gg/hFyzcXV54

## Honest caveats

- K3 modeled as a flat percent of M2, not the Citizens Standard's full price-level path targeting formula. Launch-year values match; dynamic self-correction does not.
- Equity return is treated as nominal — for real returns, set CPI to 0.
- Single-cohort projection — does not model multiple overlapping generations.
- Fed status quo comparison uses real-world median data (Vanguard 2025, SSA 2026) rather than theoretical maximums.

## Citation

> Neo-Solon. *The Citizens Standard: A Constitutional Monetary Architecture with Mode-Selectable Inflation Regimes*. SSRN, 2026. Interactive companion engine: github.com/Neo-Solon/Citizens-Standard.

## License

Open-source. Free to share, embed, modify, or adapt. Attribution to the paper appreciated.

## Built from

*The Citizens Standard*, Triple-Mode Edition (2026), by Neo-Solon. Pen name in homage to the Athenian reformer of 594 BC, whose reforms are referenced in the paper's conclusion as conceptual antecedent.

---

*If you find an error in the model, want to add a comparator, or have ideas for additional features, open an issue.*

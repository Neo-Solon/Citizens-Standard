# The Citizens Standard — Interactive Engine

> Build your own monetary system. Adjust K1, K2, K3 issuance channels and see how a citizen retires under your rules — then compare against Fed status quo, Chicago Plan, Friedman's k-rule, Bitcoin, Alaska PFD, UBI, and MMT.

Companion tool to *The Citizens Standard: A Constitutional Monetary Architecture with Mode-Selectable Inflation Regimes* by Neo-Solon (https://papers.ssrn.com/sol3/papers.cfm?abstract_id=6702518)

---

## What this is

The Citizens Standard is a constitutional monetary framework that replaces discretionary central banking with formula-bounded, citizen-anchored monetary creation distributed equally to all verified citizens at issuance. The framework defines two pools — a circulating money pool and a Stable Floor of locked, individually owned equity — and three issuance channels:

- **K1** — citizenship endowment, issued once at each new-citizen event
- **K2** — growth dividend, issued annually as a share of real economic growth
- **K3** — citizen dividend, issued monthly (active in Mode C only) calibrated by price-level path targeting

The framework is designed around a single architectural Model that hosts three constitutionally selectable Modes:

| Mode | Target | K3 active | Per-citizen Stable Floor at 65 |
|------|--------|-----------|-------------------------------|
| **A** — Deflation | ~−1.6% annual | No | ~$1.7M (real) |
| **B** — Stable | 0% annual | No | ~$2.6M (real) |
| **C** — Inflation | ~+2.0% annual | Yes (~$208/mo at launch) | ~$145K (real) + dividends |

Mode selection is a Tier 2 constitutional choice requiring a 67% supermajority and 90-day deliberation. Modes do not auto-rotate.

## What this engine does

Two interactive tools that let anyone tune the framework's parameters and see the consequences in real time:

1. **`Citizens_Standard_Engine.html`** — a single-file web application with sliders, charts, and a side-by-side comparison view. Open it in any browser. No installation. No server. Works offline after the first load.
2. **`Citizens_Standard_Engine.xlsx`** — a six-sheet Excel/Google Sheets model with 1,000+ live formulas, color-coded inputs, a 65-year projection sheet, and a comparison sheet. Drop it into Google Drive and "Open with Google Sheets" for sharing.

Both tools use the same underlying single-cohort projection model, so you can switch between them or use one for exploration and the other for documentation.

## Quick start

**Run the web engine.** Download `Citizens_Standard_Engine.html` and double-click it. It opens in your default browser. Adjust any slider; everything recalculates live.

**Open the spreadsheet.** Download `Citizens_Standard_Engine.xlsx` and open it in Excel, Numbers, LibreOffice Calc, or Google Sheets. Edit only the yellow cells; everything else recalculates from formulas.

## What you can adjust

The engine exposes every variable the framework actually depends on:

**Issuance channels** — K1, K2, K3 percentages

**Macro environment** — real GDP growth, population growth, equity return assumption, CPI inflation rate

**Launch conditions** — M2 money supply, nominal GDP, population, projection horizon

**Comparison settings** — personal savings rate, working-life span, Social Security replacement rate, UBI proposal level, MMT jobs guarantee wage

Three preset Modes (A, B, C) load the paper's reference configurations with one click. A Custom mode is automatically selected as soon as you adjust any slider away from a preset.

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

Each is shown for what it structurally delivers to a representative citizen (locked wealth, lifetime cash transfers, annual retirement income, funding source, rules-based or not).

## Methodology

Single-cohort projection: tracks one citizen born at year 0. K1 deposited once at birth; K2 deposited annually; K3 (when active) distributed monthly. Stable Floor compounds at the equity return rate. Real values deflate by CPI index. Each year, M2 expands by total issuance, GDP grows at real growth × CPI, and population grows at the pop-growth rate.

### Honest caveats

- K3 modeled as a flat percent of M2, not the paper's full price-level path targeting formula. Launch-year values match; dynamic self-correction does not.
- Equity return is treated as nominal — for real returns, set CPI to 0.
- Births are computed as population × pop-growth rate. Real demographics are more complex; this is a proxy.
- Personal savings is treated as a level annuity at year-1 income times savings rate. Real wage growth would make wealth slightly higher.
- The paper's full simulation includes stochastic returns, mode transitions, sequence-of-returns risk, and emergency tools. This engine is for intuition, not policy calibration.
- Running the engine at the paper's three preset configs reproduces ~65–80 percent of paper-stated values for Modes A and B and roughly 100 percent for Mode C. Structural ranking and relative magnitudes are correct.

## Why this exists

Monetary outcomes are properly the subject of constitutional politics rather than committee discretion. The paper's central claim is structural: a single architectural Model can host coherent inflation, stable, and deflationary regimes while preserving equal per-citizen distribution and rules-based issuance. This engine lets readers verify the claim themselves rather than trust the tables.

It also exists to surface the framework's failure modes. The interactive comparison makes the tradeoffs concrete — Citizens Standard delivers more locked wealth than systems with no retirement architecture, but Fed status quo wins on annual retirement income if you assume Social Security keeps paying current benefits. The engine doesn't hide the tension; it foregrounds it.

## Files

| File | Purpose |
|------|---------|
| `Citizens_Standard_Engine.html` | Standalone web engine. Sliders, charts, comparison view. |
| `Citizens_Standard_Engine.xlsx` | Six-sheet spreadsheet: Inputs, Projection, Summary, Comparison, Mode Presets, How It Works. |
| `README.md` | This file. |

## Embedding in your own work

The HTML file is self-contained and free to embed, host, share, or adapt. If you host it (GitHub Pages, Netlify Drop, your own domain), please link back to the SSRN paper so readers can find the source.

For academic citation:

> Neo-Solon. *The Citizens Standard: A Constitutional Monetary Architecture with Mode-Selectable Inflation Regimes*. SSRN Solon, Neo, The Citizens Standard: A Constitutional Monetary Architecture with Mode-Selectable Inflation Regimes (May 03, 2026). Available at SSRN: https://ssrn.com/abstract=6702518 or http://dx.doi.org/10.2139/ssrn.6702518, 2026. Interactive companion engine: https://github.com/Neo-Solon/Citizens-Standard

## License

Open-source. Free to share, embed, modify, or adapt. Attribution to the paper appreciated but not required.

## Built from

*The Citizens Standard*, Triple-Mode Edition (May 2026), by Neo-Solon. Pen name in homage to the Athenian reformer of 594 BC, whose reforms are referenced in the paper's conclusion as conceptual antecedent.

---

*If you find an error in the model, want to add a comparator, or have ideas for additional features, open an issue.*

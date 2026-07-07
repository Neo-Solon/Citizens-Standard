# Citizens Standard: Turkey Calibration Note

Turkey is a monetary sovereign (the TCMB issues the lira), a standard unilateral calibration mechanically. It is the most cautionary emerging-market fit in the set, and deliberately included for that reason: a **high-inflation regime** (CPI ~31%, down from a peak of ~86% in 2022) with a history of severe lira depreciation. This makes Turkey a revealing stress case for a money-quantity framework, precisely the kind of economy the design is meant to discipline, but it also means the realizable-return estimate must be handled with the heaviest caution in the set.

**Status:** macro block primary-sourced (TCMB, TurkStat, Borsa Istanbul). Inflation regime flagged as the dominant caveat (§3).

------------------------------------------------------------------------

## 1. Macro parameters (engine units: ₺ trillion)

| Parameter                 | Value                      | Reference  | Source                                               |
|---------------------------|----------------------------|------------|------------------------------------------------------|
| Broad money **M2**        | **≈ ₺26.4 T**              | early 2026 | TCMB (monthly money & banking statistics)            |
| Transaction-active **M1** | **≈ ₺10.6 T**              | Jan 2026   | TCMB (currency + demand deposits)                    |
| **M^T / M2 ratio**        | **≈ 40%**                  | \-         | constructed (see §2), M1/M2 ≈ 10.6/26.4              |
| Nominal **GDP**           | **≈ ₺68 T**                | 2025       | TurkStat (~US\$1.35T)                                |
| Real trend growth **g**   | **≈ 3.2%**                 | 2024-25    | TurkStat / World Bank (solid real growth)            |
| **Population**            | **≈ 86.1 M**               | Dec 2025   | TurkStat (86,092,168; growth ~0.5%)                  |
| Equity **market cap**     | **≈ ₺20.5 T ≈ 30% of GDP** | 2024-25    | Borsa Istanbul / CEIC (shallow, EM)                  |
| Inflation                 | **~31%**                   | early 2026 | TurkStat (down from ~86% peak in 2022; disinflating) |

Turkey combines solid real growth (~3.2%) with very high inflation (~31%) and a policy rate above 40%, an unusual pairing. The nominal figures move fast: broad money and GDP both roughly double on a multi-year horizon in nominal terms, so any snapshot must be read at its stated date. The lira has depreciated dramatically over the past decade, which is the central fact behind the return treatment in §3.

------------------------------------------------------------------------

## 2. Transaction-active share (M^T / M2): low, and why

The TCMB's M1 = currency in circulation + demand deposits, the transaction-active measure. M2 = M1 + time deposits + money-market funds.

    M^T (Turkey) = M1 ≈ ₺10.6 T
    M2           ≈ ₺26.4 T
    M^T / M2     ≈ 40%

**At ~40%, Turkey's transaction-active share is the low end of the set** (developed set 50-80%; India and Korea ~28-30%; Mexico ~50%). This is a direct consequence of the high-rate environment: with time-deposit rates above 50%, households and firms hold an unusually large share of money in interest-bearing term deposits rather than in transaction balances. The low ratio is economically meaningful, not a data artifact, it is what a high-inflation, high-rate regime does to money composition, and it is exactly the kind of distortion the framework's transaction-active anchor is designed to measure.

------------------------------------------------------------------------

## 3. Realizable return: two paths that diverge sharply (heaviest EM caution)

### Path 1: Production function

Turkey's labour share is ~0.55 → alpha ≈ 0.45, with a capital-output ratio ~2.8 → production-function baseline ~7.0% → **~4.5% realizable** on the production side alone. On paper this looks like a healthy mid-set figure.

### Path 2: Historical realised returns

Here the picture changes completely. Turkish equity has produced strong *nominal* returns but poor **real and USD** returns: the lira's sustained depreciation has eroded most of the nominal gains for any investor measuring in constant purchasing power or dollars. Long-run real returns have been low and extraordinarily volatile, among the weakest risk-adjusted records of any sizeable market. The shallow market (~30% of GDP) and the ongoing 31% inflation compound the caution.

### Resolution: weight the realized history heavily

Turkey's two paths **diverge more sharply than any other country in the set**: the production function says ~4.5% but the realized real/USD history says materially less, with severe volatility. Anchoring on the production-function figure would ignore precisely the currency and inflation risk that defines the Turkish experience. The central realizable is therefore set at the low end, **4.0% (Mode B), band 3.0-5.2%**, close to the realized-history path, with the production-function figure retained only as the top of the band. This is the honest call, and the divergence itself is the finding: for an economy with Turkey's inflation and currency record, the realized history must dominate a favourable production estimate.

------------------------------------------------------------------------

## 4. Broad citizen ownership under Mode Ω

Running Turkey in Mode Ω produces a citizen market-ownership share **elevated relative to the US**, for the same structural reason as the other shallow-market EMs: a small equity market (~30% of GDP) means the structural-buyer flow is large relative to market size, pushing the ownership ceiling up. Turkey's solid growth (g ~3.2%) enlarges the growth-funded budget somewhat, working in the same direction.

The ceiling is set by the flow-to-growth ratio **c / g**, reported as the true output of the design rather than tuned to a target. The honest framing holds: **in shallower markets citizens can end up owning a larger share than the US ~10%, and Turkey's ~30%-of-GDP market is one of those cases**. The heavy caveat here is not on the ownership arithmetic but on the return band feeding it, which is deliberately conservative for the reasons in §3.

------------------------------------------------------------------------

## 5. Engine values

Currency ₺. M^T share 40%. Defaults: M2 ₺26.4T, GDP ₺68T, pop 86.1M, market cap ₺20.5T. Real growth 3.2%, pop growth 0.5%. Realizable band 3.0 / 4.0 / 5.2 / 6.3 / 6.3. Mode B return 4.0%.

------------------------------------------------------------------------

## 6. Audit checklist

- \[ \] Confirm M1 and M2 at a common date from the TCMB money & banking statistics (fast-moving nominal figures)
- \[ \] Confirm nominal GDP to the printed TurkStat figure (annual, current prices)
- \[ \] Confirm Borsa Istanbul domestic market cap at a stated date (the ~30%-of-GDP ratio feeds §4)
- \[ \] Return: the 4.0% central is a deliberate weighting toward realized real/USD equity history over the production-function figure (~4.5%); pin to a Turkish equity real-return series in constant terms
- \[ \] Inflation regime: re-confirm current CPI; the ~40% M^T/M2 share tracks the high-rate environment and will shift as rates normalize


[back to top ↑](#top)

<div id="uk" class="section note">


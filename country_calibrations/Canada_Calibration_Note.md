# Citizens Standard: Canada Calibration Note

**Purpose.** Re-parameterise the CS engine to Canada using primary-source data, to the same
standard as the US and UK calibrations. Every figure traces to a named primary source
(Bank of Canada, Statistics Canada, TMX). Canada is structurally the *cleanest* non-US case:
it uses M2 as the broad aggregate (directly comparable to the US, unlike the UK's M4), and
M1+ as the transaction-active measure.

**Status:** macro block complete and primary-sourced. Realizable return via the same
two-path method as the UK. For audit before/after wiring into the engine.

---

## 1. Macro parameters (all primary-sourced)

| Parameter | Canada value | Reference | Primary source |
|---|---|---|---|
| Broad money **M2** | **C$2,817 bn** | Apr 2026 | Bank of Canada, M2 series |
| Transaction-active **M1+** | **C$1,734 bn** | Dec 2025 | Bank of Canada (currency + all chequable deposits) |
| **M^T / M2 ratio** | **≈ 61.5%** | - | constructed (see §2) |
| Nominal **GDP** | **≈ C$3.2 T** | 2025 | US$2.32T (StatCan/IMF) × ~1.38 USD/CAD; cross-checks vs M2/GDP |
| Real trend growth **g** | **≈ 1.7%** | 2025 | Statistics Canada (real GDP +1.7% in 2025) |
| **Population** | **41.47 M** | Jan 2026 | Statistics Canada (41,472,081; note: first annual decline since 1867) |
| Equity **market cap** (domestic) | **≈ 193% of GDP ≈ C$6.2 T** | Dec 2025 | TMX market cap ÷ StatCan GDP (CEIC); domestically-listed |
| Federal **debt** | **≈ 41% of GDP** | Mar 2025 | Dept of Finance (federal accumulated deficit; total-govt net debt higher) |

Notes:
- M2 and M1+ are one month apart (Apr 2026 / Dec 2025); ratio is stable, but same-date
  figures from the BoC E1 table are preferred for the published note.
- GDP is derived (USD × FX) and cross-checked; the StatCan nominal-CAD annual figure would
  confirm to the decimal. The ~C$3.2T value is consistent with M2 at ~88% of GDP.
- Market cap at ~193% of GDP is high (resource-heavy large-cap market), well above the US
  (~2.2×) only in that both exceed GDP, and far above the UK (~0.97×).

---

## 2. Construction of the transaction-active share (M^T / M2)

Canada is cleaner than the UK here. The Bank of Canada publishes **M1+** with an explicit
definition that is exactly the M^T construct:

> **M1+ (gross)** = currency outside banks + personal and non-personal chequable deposits at
> chartered banks + all chequable deposits at trust and mortgage loan companies, credit unions
> and caisses populaires., Bank of Canada, monetary aggregate definitions.

Chequable = on-demand transactable = the transaction-active property M^T captures.

    M^T (Canada) = M1+ = C$1,734 bn
    M2           = C$2,817 bn
    M^T / M2     = 61.5%

**Finding:** Canada's transaction-active share (~61.5%) sits between the US (51.35%) and the
UK (69.7%). This is economically sensible and confirms the share is genuinely country-specific,
not importable. The Canadian price-stability locus recomputes on 61.5%.

---

## 3. Realizable return (two-path method, same as UK)

### Path 1: Production function (matched to Paper 5's Solow construct)
Canada is capital-intensive and resource-heavy, implying a capital share slightly above the US.
Literature places the Canadian labour share around 0.60-0.62, so **alpha_CA ≈ 0.38**. Holding
the K/Y construct matched to Paper 5 (3.0):

    r0(CA) = alpha_CA / (K/Y) - delta = 0.38 / 3.0 - 0.05 = 7.67%   (baseline; US 6.67%)

Attenuated by the same r→g compression Paper 5 uses (×0.639):

    realizable (Mode B) ≈ 4.90%

### Path 2: Historical realised returns (independent)
Dimson-Marsh-Staunton database (Canada is one of the 125-year continuous markets): Canadian
long-run real equity return is on the order of **~5.6% real (1900-2024)**, close to the world
5.2% and slightly above the UK. (To pin to the printed DMS Canada page figure on final audit.)

### Reconciliation
Realizable ~4.90% sits just below listed equity ~5.6%, the same consistent relationship found
for the US (4.26% vs ~6.5%) and UK (4.68% vs 5.3%): the broad attenuated floor return lands
just under levered listed equity. **Canada realizable return (Mode B) ≈ 4.90%, band ~4.5-5.2%.**

---

## 4. Engine changes (US → UK → Canada)

| Engine input | US | UK | Canada |
|---|---|---|---|
| Currency | $ | £ | C$ |
| Broad money | $22.4T (M2) | £3.27T (M4) | C$2.82T (M2) |
| M^T share | 51.35% | 69.7% | 61.5% |
| GDP | $30.8T | £3.04T | C$3.2T |
| Population | 342M | 69.5M | 41.5M |
| Market cap | $69T (~2.2×) | £2.96T (~0.97×) | C$6.2T (~1.93×) |
| Real growth | 2.0% | 1.2% | 1.7% |
| Baseline return | 6.67% | 7.33% | 7.67% |
| Realizable (Mode B) | 4.26% | 4.68% | 4.90% (band 4.5-5.2%) |
| Govt debt | ~102% | ~95% | ~41% federal |

---

## 5. Audit checklist

- [ ] M2 and M1+ pulled at a common date from BoC E1 table
- [ ] Nominal CAD GDP confirmed against StatCan annual figure (vs the USD×FX derivation)
- [ ] Market cap confirmed on domestically-listed basis at a stated date
- [ ] Labour share / alpha_CA confirmed to a printed StatCan or OECD figure (currently ~0.62 from literature)
- [ ] DMS Canada equity return confirmed to the printed country-page figure (~5.6%)
- [ ] Return: two-path central 4.90% + band 4.5-5.2%

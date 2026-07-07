# Citizens Standard: Saudi Arabia Calibration Note

Saudi Arabia is the most qualified fit in the set, and is included with two caveats stated plainly rather than buried. First, the riyal is **hard-pegged to the US dollar** (SAR 3.75, unchanged since 1986), so Saudi Arabia is not a free-floating monetary sovereign in the way the other calibrations are: SAMA's policy rate follows the US Federal Reserve by necessity, and the peg constrains independent control of the domestic money quantity. Second, the headline equity market is **dominated by the state**, one company (Aramco) and government-related entities account for the bulk of it, so the tradeable, citizen-accessible market is far smaller than the headline suggests. Both points bear directly on the framework's premises and are handled below.

**Status:** macro block primary-sourced (SAMA, GASTAT, Tadawul). Peg and market- concentration caveats foregrounded (§0 and §4).

------------------------------------------------------------------------

## 0. The peg caveat (read first)

The Citizens Standard assumes a country issues its own free-floating currency and can control the quantity of its transaction-active money. Saudi Arabia's dollar peg is a genuine departure from that premise. Under the peg, a large citizens-dividend money injection would create pressure on the exchange rate (capital would tend to flow out, testing the 3.75 parity) unless it were sterilized or matched by reserve movements. SAMA holds ample reserves (net foreign assets ~US\$415bn, ~15 months of imports), so the peg is credible and defensible, but the constraint is real: **Saudi Arabia could run the CS levers on its domestic money base only to the extent the peg allows, and a full-strength dividend would be in tension with the peg**. The calibration is presented as a what-if for a pegged economy, not as a claim that the mechanism operates as freely as it does for a floating sovereign. This is the honest seam, and it is surfaced rather than hidden.

------------------------------------------------------------------------

## 1. Macro parameters (engine units: SR trillion)

| Parameter                                   | Value                      | Reference | Source                                          |
|---------------------------------------------|----------------------------|-----------|-------------------------------------------------|
| Broad money **M2**                          | **≈ SR2.9 T**              | 2025      | SAMA (M3 SR3.12T; M2 excludes some quasi-money) |
| Transaction-active **M1**                   | **≈ SR1.65 T**             | 2025      | SAMA (currency + demand deposits ~46.5% of M3)  |
| **M^T / M2 ratio**                          | **≈ 57%**                  | \-        | constructed (see §2), M1/M2                     |
| Nominal **GDP**                             | **≈ SR4.79 T**             | 2025      | GASTAT (~US\$1.275T; rebased +14% May 2025)     |
| Real trend growth **g**                     | **≈ 4.5%**                 | 2025      | GASTAT (oil-driven, volatile; −0.8% in 2024)    |
| **Population**                              | **≈ 33.5 M**               | 2025      | GASTAT (large expat share ~42%; growth ~1.5%)   |
| Equity **market cap** (free-float-adjusted) | **≈ SR1.9 T ≈ 40% of GDP** | 2024-25   | Tadawul, ex-Aramco/GRE (see §4; headline ~210%) |
| Inflation                                   | **~2.0-2.3%**              | 2025      | GASTAT (low, anchored by the dollar peg)        |

Saudi Arabia has strong but oil-cyclical real growth (4.5% in 2025, but −0.8% in 2024 on OPEC+ production cuts) and very low, peg-anchored inflation (~2%). The economy is concentrated: the hydrocarbon complex is ~35-40% of GDP on a broad definition, and Vision-2030 diversification is under way but incomplete.

------------------------------------------------------------------------

## 2. Transaction-active share (M^T / M2): mid-range

SAMA's M1 = currency outside banks + demand deposits, the transaction-active measure. M2 = M1 + time and savings deposits; M3 adds other quasi-monetary deposits.

    M^T (Saudi Arabia) = M1 ≈ SR1.65 T
    M2                 ≈ SR2.9 T
    M^T / M2           ≈ 57%

**At ~57%, Saudi Arabia sits mid-range** (developed set 50-80%; India and Korea ~28-30%; Mexico ~50%). Demand deposits are the largest single component of Saudi broad money, giving a transaction-active share a little above Mexico's. This is a clean primary-sourced ratio; the peg caveat in §0 concerns money-quantity *control*, not the composition measured here.

------------------------------------------------------------------------

## 3. Realizable return: production-function baseline, oil and concentration caution

### Path 1: Production function

Saudi Arabia's capital share is high (a capital- and resource-intensive economy) → alpha ≈ 0.50, capital-output ratio ~3.2 → production-function baseline ~6.2% → **~4.5% realizable**.

### Path 2: Historical realised returns and the peg

Tadawul's long-run real returns have been modest and oil-cyclical. One axis actually works in Saudi Arabia's favour relative to other EMs: **the dollar peg removes currency risk**, a Saudi return in riyals is, by construction, a return in dollars, unlike Turkey or Mexico where FX depreciation erodes realized returns. But this is offset by heavy oil-cyclicality and by the market- concentration problem in §4: the freely tradeable market is small and dominated by a few state-linked names.

### Resolution: mid-single-digit, with concentration rather than currency the binding caution

The central realizable is set at **4.5% (Mode B), band 3.5-5.5%**. Currency risk is low (the peg), so the downward adjustment here is driven not by FX (as in Turkey/Mexico) but by oil- cyclicality and the shallow, state-dominated free float. The high band assumes Vision-2030 diversification broadens the tradeable market; the low band assumes continued oil dependence and concentration. This is the honest call for a pegged, oil-concentrated economy.

------------------------------------------------------------------------

## 4. Broad citizen ownership under Mode Ω, and the free-float adjustment

The headline Tadawul market cap is very large, on the order of **210% of GDP (~US\$2.7T)**. Taken at face value this would make Saudi Arabia look like a deep-market case where citizen ownership barely moves. That would be misleading. Roughly **67% of the exchange is Aramco alone, and government-related entities (the sovereign fund PIF and pension fund GOSI) hold ~64% of total market value**; foreign investors hold only ~4%. The freely tradeable, citizen-accessible market is therefore far smaller, on the order of **~40% of GDP once Aramco and the state blocks are stripped out**. The engine uses this free-float-adjusted figure (~SR1.9T), not the headline, because the ownership mechanism concerns shares citizens can actually acquire.

On the adjusted market, Saudi Arabia behaves like a moderate-to-shallow-market case: the structural-buyer flow is meaningful relative to the tradeable float, so the citizen ownership share comes out **above the US ~10%**. As always this is the true output of the design, not a target, and it rests on the free-float adjustment above, which is the load-bearing honesty in this calibration.

------------------------------------------------------------------------

## 5. Engine values

Currency SR. M^T share 57%. Defaults: M2 SR2.9T, GDP SR4.79T, pop 33.5M, market cap SR1.9T (free-float-adjusted). Real growth 4.5%, pop growth 1.5%. Realizable band 3.5 / 4.5 / 5.5 / 6.9 / 6.9. Mode B return 4.5%.

------------------------------------------------------------------------

## 6. Audit checklist

- \[ \] **Peg:** confirm the calibration is read as a pegged-economy what-if (§0); a full-strength dividend is in tension with the 3.75 parity
- \[ \] Confirm M1 and M2 (or M3 components) at a common date from the SAMA monthly bulletin
- \[ \] Confirm nominal GDP to the printed GASTAT figure (rebased series, current prices)
- \[ \] **Market cap:** confirm the free-float-adjusted figure ex-Aramco/GRE (~40% of GDP), not the ~210% headline; this is the load-bearing input for §4
- \[ \] Return: the 4.5% central reflects low FX risk (peg) offset by oil-cyclicality and concentration; pin to a Tadawul real total-return series


[back to top ↑](#top)

<div id="south-korea" class="section note">


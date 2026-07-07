# Citizens Standard: Norway Calibration Note

Norway is a monetary sovereign (Norges Bank issues the krone), a standard unilateral calibration.
Norway is conceptually interesting for CS: it already runs the world's largest sovereign wealth
fund (GPFG, NOK 19.7T, more than 3x GDP), a real "structural buyer" operating at global scale, 
though invested abroad rather than domestically as CS would direct.

**Status:** macro block primary-sourced (Norges Bank, Statistics Norway, IMF). One soft spot: the
transaction-active M1 level is not cleanly pinned (see §2 and audit checklist).

---

## 1. Macro parameters (engine units: NOK trillions)

| Parameter | Value | Reference | Source |
|---|---|---|---|
| Broad money **M2/M3** | **NOK 3.57 T** | Apr 2026 | Norges Bank / Statistics Norway |
| Transaction-active **M1** | **~NOK 2.2 T (estimated)** | - | see §2, NOT cleanly pinned |
| **M^T / broad ratio** | **≈ 62% (provisional)** | - | flagged for confirmation |
| Nominal **GDP** | **≈ NOK 5.3 T** | 2025 | Statistics Norway (~US$493bn) |
| Real trend growth **g** | **≈ 1.8%** | 2025-26 | IMF |
| **Population** | **5.65 M** | 2025 | Statistics Norway |
| Equity **market cap** | **≈ 75% of GDP ≈ NOK 4.0 T** | 2025 | Euronext Oslo (domestic) |
| Government **debt** | **≈ 43% of GDP** | 2024 | IMF (and enormous net assets via GPFG) |

The sovereign wealth fund context matters: Norway's fiscal position is uniquely strong (budget
surplus ~14-16% of GDP including petroleum), so the "affordability" framing of CS looks very
different here than for a debtor nation.

---

## 2. Transaction-active share: provisional, flagged

Norway's broad money (M2) is NOK 3.57T (Norges Bank). The transaction-active M1 (currency +
transaction deposits) was NOT cleanly sourced at a current level in this pass; the engine uses a
provisional M^T/broad ratio of **0.62**, consistent with the Nordic/European cluster (UK 70%,
Eurozone 66%, Switzerland 63%). This is the one genuinely unconfirmed input in the Norway block
and is flagged in the audit checklist. It should be replaced with the actual Norges Bank M1 level
before the Norway figures are treated as final.

---

## 3. Realizable return

Norwegian labour share ~0.58 → alpha ≈ 0.42 → production-function ~5.75% realizable. But DMS Norway
real equity is ~4.3% (moderate; oil-cycle volatility, smaller market). The paths diverge somewhat
(like a milder Japan), so the central estimate leans toward the historical: **4.8% (Mode B),
band 3.7-5.6%**.

---

## 4. Engine values

Currency NOK. M^T share 0.62 (provisional). Defaults: broad NOK 3.57T, GDP NOK 5.3T, pop 5.65M,
market cap NOK 4.0T. Realizable band 3.7 / 4.8 / 5.6 / 6.0 / 7.4. Mode B return 4.8%.

---

## 5. Audit checklist

- [ ] **PIN THE M1 LEVEL** from Norges Bank and recompute M^T/broad (currently provisional 0.62)
- [ ] Confirm broad money aggregate choice (M2 vs M3) and level at a stated date
- [ ] Confirm Euronext Oslo domestic market cap at a stated date
- [ ] Return: DMS Norway equity figure pinned to the printed DMS country page (~4.3%)
- [ ] Consider a note on the GPFG as a real-world analogue to the CS structural buyer

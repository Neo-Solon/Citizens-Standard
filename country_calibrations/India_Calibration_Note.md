# Citizens Standard: India Calibration Note

India is a monetary sovereign (RBI issues the rupee), a standard unilateral calibration
mechanically. But as the first genuine emerging market in the set, it differs from the
developed-economy calibrations in two ways that are flagged honestly below: a low
transaction-active share (term-deposit-heavy savings) and a high-but-volatile equity return.

**Status:** macro block primary-sourced (RBI, MoSPI, NSE, IMF).

---

## 1. Macro parameters (engine units: ₹ trillion)

| Parameter | Value | Reference | Source |
|---|---|---|---|
| Broad money **M3** | **₹281.4 T** | Jul 2025 | Reserve Bank of India |
| Transaction-active **M1** | **₹80.6 T** | early 2026 | RBI (currency + demand deposits + other deposits with RBI) |
| **M^T / M3 ratio** | **≈ 28%** | - | constructed (see §2), LOW, like Korea but for a different reason |
| Nominal **GDP** | **≈ ₹330.7 T** | 2024-25 | MoSPI (~US$4.1T) |
| Real trend growth **g** | **≈ 6.5%** | 2025-26 | IMF / RBI (fastest in the set by far) |
| **Population** | **≈ 1,476 M (1.48 bn)** | 2025 | UN / Census (world's most populous) |
| Equity **market cap** | **≈ ₹438.9 T ≈ 133% of GDP** | Dec 2024 | NSE (US$5.13T; 5th-largest exchange) |
| Government **debt** | **≈ 80% of GDP** | 2025 | IMF (general government) |
| Inflation | **~2-4% (within RBI band)** | 2025 | RBI, notably benign for an EM |

India is the fastest-growing economy in the set (~6.5% real), which is why the real-growth slider
range was widened to accommodate it. Its equity market is now the world's 5th-largest by cap.

---

## 2. Transaction-active share (M^T / M3): low, and why

RBI's M1 (narrow money) = currency with the public + demand deposits + other deposits with RBI, 
the transaction-active measure. M3 = M1 + net time deposits.

    M^T (India) = M1 = ₹80.6 T
    M3          = ₹281.4 T
    M^T / M3    ≈ 28%

**This is low (developed set is 50-80%), and it is a genuine structural feature, not an error.**
Time deposits are 74.6% of India's M3, Indians hold most of their money in fixed/term deposits
rather than transaction accounts, reflecting a high-savings culture and attractive term-deposit
rates. This is the same *category* of low-ratio situation as South Korea (30%), though the cause
differs (Korea's broad M2 definition vs India's term-deposit-heavy holdings). Flagged so the low
share is understood as real rather than a data slip.

---

## 3. Realizable return: high but volatile (EM caution applied)

### Path 1: Production function
India's labour share is lower than the developed set (~0.52; large informal/agricultural sector,
high capital share in the formal economy) → alpha ≈ 0.48 → production-function baseline ~11% →
~7.0% realizable. That is the highest production-function figure in the entire set.

### Path 2: Historical realised returns
Indian equity (Sensex/Nifty) has delivered strong long-run real returns, roughly 6.5-7% real over
recent decades, among the best-performing markets globally, but with substantially higher
volatility than developed markets (currency risk, EM drawdowns, valuation swings).

### Resolution: conservative despite both paths pointing high
Both paths point to an above-average return, and a naive reading would place India at the top of
the set (~7%). But emerging-market equity returns carry materially higher volatility and drawdown
risk than the developed markets, and the CS structural-buyer mechanism should not be calibrated to
the top of a volatile EM range. The central realizable is therefore set **conservatively at 5.5%
(Mode B), band 4.2-6.4%**, above the developed set (reflecting genuinely higher growth and
returns) but well below the ~7% production-function figure, to respect EM volatility. This is the
honest middle: India's returns are real and high, but their variance argues against anchoring on
the peak.

---

## 4. Broad citizen ownership under Mode Ω (higher here, and honestly so)

Running India in Mode Ω produces a citizen market-ownership share of ~47% (structural-buyer
flow ~3.74% of market cap per year; active tradable float ~53%). This is far above the US figure
(~10% realized, ~20% ceiling), and it is a real result, not a calibration slip.

The ownership ceiling is set by the flow-to-growth ratio **c / g**, not by a fixed percentage.
India pushes both terms: it is the fastest grower in the set (g ~6.5%, enlarging the growth-funded
budget) and has a low transaction-active share (M^T/M3 ~28%, so more of the budget routes to the
asset/floor circuit), against an equity market that, while the 5th-largest globally, is not large
enough to dilute that flow. High flow into a proportionally smaller market gives a high c/g ceiling
(~57%) and a realized share near 47%.

This is reported as the true output of the design. Mode Ω solves for price stability; it is not
tuned to hold ownership down to a target, and it should not be. The honest framing is therefore
country-dependent: **in the US the structural buyer settles near a tenth of the market, but in
shallower or faster-growing economies citizens can end up owning a much larger share, up toward
half in India’s case.** The bound that matters is still load-bearing (ownership stays well inside
the 100% that feasibility forbids, and the majority of the market remains freely traded), but the
specific share is a function of the economy, not a universal ~10%.

---

## 5. Engine values

Currency ₹. M^T share 28%. Defaults: M3 ₹281.4T, GDP ₹330.7T, pop 1,476M, market cap ₹438.9T.
Real growth 6.5%, pop growth 0.9%. Realizable band 4.2 / 5.5 / 6.4 / 6.9 / 8.5. Mode B return 5.5%.

---

## 6. Audit checklist

- [ ] Confirm M1 and M3 at a common date from the RBI Weekly Statistical Supplement
- [ ] Confirm nominal GDP to the printed MoSPI annual figure (new 2022-23 base series)
- [ ] Confirm NSE (or NSE+BSE combined) market cap at a stated date
- [ ] Return: pin to an India equity-return series (e.g. Nifty total-return real); the 5.5% central
      is a deliberate EM-volatility discount to the ~7% production-function figure, not a sourced point
- [ ] Population growth: confirm current annual rate (~0.9%, decelerating)

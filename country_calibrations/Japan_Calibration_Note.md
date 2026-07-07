# Citizens Standard: Japan Calibration Note

Japan is a monetary sovereign (BoJ issues the yen), so it can implement CS unilaterally, 
a standard calibration like the UK and Canada. But Japan is the case where the two return
paths diverge most, and that divergence is handled explicitly below.

**Status:** macro block complete and primary-sourced (BoJ, MoF, Statistics Bureau, IMF).
Return anchored on historical (DMS) rather than production-function, with reasoning shown.

---

## 1. Macro parameters (all primary-sourced)

| Parameter | Japan value | Reference | Primary source |
|---|---|---|---|
| Broad money **M3** | **¥1,586 T** | 2024 | Bank of Japan (fuller coverage incl. Japan Post Bank) |
| Transaction-active **M1** | **¥1,103 T** | May 2026 | Bank of Japan (currency + demand deposits) |
| **M^T / M3 ratio** | **≈ 69.5%** | - | constructed (see §2) |
| Nominal **GDP** | **≈ ¥600 T** | 2025 | Ministry of Finance (~US$4.0T) |
| Real trend growth **g** | **≈ 1.0%** | 2025 | IMF (recovering, above potential H1 2025); exiting deflation |
| **Population** | **123.05 M** | 2025 census | Statistics Bureau (record 2.5% fall from 2020) |
| Equity **market cap** (TSE) | **≈ ¥1,200 T ≈ 200% of GDP** | 2025 | Ministry of Finance / Japan Exchange Group |
| Government **debt** | **≈ 230% of GDP** | 2025 | IMF (highest among advanced economies) |

Notes:
- **M3, not M2, is the broad aggregate.** Japan's M2 (¥1,298T) excludes Japan Post Bank, a
  huge deposit-taker; M3 includes it, giving fuller coverage (same logic as ECB M3 / UK M4).
  Using M2 would give an implausibly high M^T share (~85%); M3 gives the comparable 69.5%.
- Debt at ~230% is the highest of any country in the set, but Japan holds most of it
  domestically and has a large net international investment position, so it is sustainable
  in a way headline debt-to-GDP understates.

---

## 2. Transaction-active share (M^T / M3)

BoJ's M1 is a textbook transaction-active measure:

> **M1 = currency in circulation + deposit money** (demand deposits: current, ordinary,
> savings, deposits at notice)., Bank of Japan, Money Stock Statistics.

    M^T (Japan) = M1 = ¥1,103 T
    M3          = ¥1,586 T
    M^T / M3    = 69.5%

Close to the UK (69.7%) and Eurozone (65.5%); above the US (51.35%). Japan's high cash/deposit
holdings (households hold ~¥1.1 quadrillion in cash and deposits) make the transaction-active
core a large fraction of broad money.

---

## 3. Realizable return: the divergence case (handled explicitly)

Japan is where the two independent return paths DISAGREE, and the disagreement is itself
informative.

### Path 1: Production function
Japan's capital share is high and rising: productivity rose 18% (2000-2024) while real
compensation per worker *fell* 4% (ILO/OECD), and unit profits have outpaced unit labour costs.
That implies alpha_JP ≈ 0.42 (labour share ~0.58). Mechanically:

    r0(JP) = 0.42/3.0 - 0.05 = 9.00%  ->  ~5.75% realizable (Mode B)

### Path 2: Historical realised returns
Japan's long-run real equity return in the DMS database is among the LOWEST of any developed
market: **~4.0-4.5% real (1900-2024)**, reflecting WWII capital destruction and the post-1990
"Lost Decades" of deflation and weak corporate governance.

### Resolution: historical anchor wins (and why)
The paths diverge by ~1.5 percentage points, the widest gap of any country in the set. The
production-function path OVERSTATES the realizable return for Japan, because Japan's high notional
capital share has historically NOT translated into shareholder returns (poor capital allocation,
cross-holdings, deflation). The honest central estimate anchors on the historical path:

    **Japan realizable return (Mode B) ≈ 4.2%, band 3.2-4.9%.**

This coincidentally lands near the US 4.3%, but for the OPPOSITE reason: the US has a moderate
capital share and moderate equity returns, while Japan has a high capital share whose returns
leak away before reaching shareholders. Recent governance reform (TSE's book-value campaign,
rising ROE) may lift future returns toward the production-function figure, so the band's upper
end (4.9%) captures that upside; the central estimate stays conservative.

---

## 4. Engine values

Currency ¥. M^T share 69.5%. Defaults: M3 ¥1,586T, GDP ¥600T, pop 123M, market cap ¥1,200T.
Realizable band 3.2 / 4.2 / 4.9 / 5.3 / 6.5. Mode B return 4.2%.

---

## 5. Audit checklist

- [ ] Confirm M1 and M3 at a common date from the BoJ Money Stock Statistics
- [ ] Confirm nominal GDP to the printed Cabinet Office annual figure (vs the ~¥600T round)
- [ ] Confirm TSE market cap on a domestically-listed basis at a stated date
- [ ] Return: DMS Japan equity figure pinned to the printed DMS country page (~4.0-4.5%)
- [ ] Revisit the return upward if TSE governance reforms durably lift ROE/equity returns

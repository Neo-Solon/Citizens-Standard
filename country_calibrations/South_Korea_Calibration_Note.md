# Citizens Standard: South Korea Calibration Note

South Korea is a monetary sovereign (Bank of Korea issues the won), a standard unilateral
calibration. Its distinctive feature is an unusually broad M2 definition that makes its
transaction-active share the lowest in the set; this is flagged, not smoothed over.

**Status:** macro block primary-sourced (Bank of Korea, Korea Exchange, Statistics Korea, IMF).

---

## 1. Macro parameters

| Parameter | Value | Reference | Source |
|---|---|---|---|
| Broad money **M2** | **₩4,472 T** | Oct 2025 | Bank of Korea |
| Transaction-active **M1** | **₩1,357 T** | Feb 2026 | Bank of Korea (cash + demand + instant-access) |
| **M^T / M2 ratio** | **≈ 30.3%** | - | constructed (see §2), the LOW outlier of the set |
| Nominal **GDP** | **≈ ₩2,560 T** | 2025 | Bank of Korea (~US$1.87T) |
| Real trend growth **g** | **≈ 1.8%** | 2025 | Bank of Korea / IMF |
| **Population** | **51.6 M** | 2025 | Statistics Korea |
| Equity **market cap** | **≈ 149.6% of GDP ≈ ₩3,830 T** | Dec 2025 | Korea Exchange (KOSPI+KOSDAQ) / CEIC |
| Government **debt** | **≈ 50% of GDP** | 2025 | IMF (low among the set) |

---

## 2. Transaction-active share (M^T / M2): the low outlier, explained

    M^T (Korea) = M1 = ₩1,357 T
    M2          = ₩4,472 T
    M^T / M2    = 30.3%

**This is genuinely low (US 51%, others 60-70%), and the reason is a definition quirk, not a
real difference in transactional money.** The IMF has repeatedly urged Korea to revise its M2:
Korea's M2 includes ETFs, mutual-fund beneficiary certificates, and other market instruments
that the US, Europe, and Japan exclude. That inflates the M2 denominator. Excluding those, the
BoK's own "adjusted" M2 growth is materially lower, and the implied M^T share would be higher
(closer to ~40%). The BoK began publishing a securities-excluded M2 series from Nov 2025.

**Recommendation:** the 30.3% figure is defensible as the headline-M2 ratio, but a fairer
cross-country comparison would use the securities-excluded M2 (raising M^T/M2 toward ~38-42%).
Flagged in the audit checklist; the engine uses 30.3% as the sourced headline value with this
caveat noted.

---

## 3. Realizable return

Korea's labour share ~0.60 → alpha ≈ 0.40 → production-function baseline 8.33% → ~5.32%
realizable. But Korea has long traded at a "Korea discount" (low P/E, governance/chaebol
concerns), so realized equity returns have lagged the production-function implication, 
though recent "value-up" governance reforms are narrowing it. Central estimate splits the
difference at **~4.7% (Mode B), band 3.6-5.5%**, with the upper end capturing reform upside.
(DMS Korea equity history is shorter than the 125-year markets; treated as literature-grounded.)

---

## 4. Engine values

Currency ₩. M^T share 30.3%. Defaults: M2 ₩4,472T, GDP ₩2,560T, pop 51.6M, market cap ₩3,830T.
Realizable band 3.6 / 4.7 / 5.5 / 5.9 / 7.3. Mode B return 4.7%.

---

## 5. Audit checklist

- [ ] Recompute M^T/M2 on the securities-EXCLUDED M2 (BoK new series from Nov 2025) for comparability
- [ ] Confirm M1 and M2 at a common date
- [ ] Confirm market cap (KOSPI+KOSDAQ) and GDP at stated dates
- [ ] Return: pin to a Korea equity-return series; revisit upward if value-up reforms hold

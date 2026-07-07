# Citizens Standard: Switzerland Calibration Note

Switzerland is a monetary sovereign (SNB issues the franc), a standard unilateral calibration.
Distinctive features: the highest equity-market-cap-to-GDP ratio in the set (~201%), a very
strong currency, a zero policy rate (post negative-rate era), and very low public debt.

**Status:** macro block primary-sourced (SNB, SECO, SIX Swiss Exchange, FSO, IMF).

---

## 1. Macro parameters (engine units: CHF trillions)

| Parameter | Value | Reference | Source |
|---|---|---|---|
| Broad money **M3** | **CHF 1.211 T** | Dec 2025 | Swiss National Bank |
| Transaction-active **M1** | **CHF 0.766 T** | Apr 2026 | SNB (currency + sight deposits) |
| **M^T / M3 ratio** | **≈ 63.3%** | - | constructed (see §2) |
| Nominal **GDP** | **≈ CHF 0.80 T** | 2025 | SECO (~US$0.9T nominal) |
| Real trend growth **g** | **≈ 1.3%** | 2025 | SECO / SNB |
| **Population** | **9.0 M** | 2025 | Federal Statistical Office |
| Equity **market cap** (SIX) | **≈ 201% of GDP ≈ CHF 1.61 T** | Dec 2025 | SIX Swiss Exchange / CEIC |
| Government **debt** | **≈ 30% of GDP** | 2025 | very low (debt brake); AAA-rated |

Note: Switzerland's market cap is dominated by a few global giants (Nestlé, Roche, Novartis),
so the ~201% ratio partly reflects that these multinationals are large relative to the small
domestic economy. Genuine, but worth remembering when comparing to bank-based economies.

---

## 2. Transaction-active share (M^T / M3)

    M^T (Switzerland) = M1 = CHF 0.766 T   (currency + sight deposits)
    M3                = CHF 1.211 T
    M^T / M3          = 63.3%

In line with the UK/Eurozone/Japan cluster (63-70%); comfortably above the US.

---

## 3. Realizable return: both paths moderate and agreeing

Swiss labour share ~0.62 → alpha ≈ 0.38 → production-function baseline 7.67% → ~4.90% realizable.
DMS Swiss real equity is ~4.4% (1900-2024): solid, defensive, low-volatility, with the strong
franc a drag on nominal returns but real returns respectable. Both paths land in the mid-4s, so
the central realizable is set at **4.6% (Mode B), band 3.5-5.3%**, squarely between the two.
A defensible, low-drama calibration.

---

## 4. Engine values

Currency CHF. M^T share 63.3%. Defaults: M3 CHF 1.211T, GDP CHF 0.80T, pop 9.0M, market cap CHF 1.61T.
Realizable band 3.5 / 4.6 / 5.3 / 5.8 / 7.1. Mode B return 4.6%.

---

## 5. Audit checklist

- [ ] Confirm M1 and M3 at a common date from the SNB data portal (monetary aggregates cube)
- [ ] Confirm nominal GDP in CHF (SECO) at a stated date; keep market-cap ratio internally consistent
- [ ] Confirm SIX total market cap / GDP ratio at a stated date
- [ ] Return: DMS Switzerland equity figure pinned to the printed DMS country page (~4.4%)

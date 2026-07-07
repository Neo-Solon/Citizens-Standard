# Citizens Standard: Eurozone Calibration Note (Boundary Case)

**This is not a standard country calibration. It is the framework's own boundary case.**
The UK and Canada are monetary sovereigns: each controls its own currency issuance, so each
can implement CS unilaterally. The Eurozone cannot be treated the same way, and the reason is
central to the framework, not incidental to it.

---

## 0. The prerequisite (read this first)

CS requires a **monetary sovereign**, an entity that controls issuance of the currency it
distributes. In the euro area, no single member state has this. Germany, France, Italy, and the
rest ceded monetary sovereignty to the **ECB** when they adopted the euro. This is exactly the
fragility Paper 3 identifies via De Grauwe (2011): euro members borrow and operate in a currency
they do not individually issue.

The consequence for CS is precise:

1. **A single member cannot implement CS alone.** Germany cannot run citizen-issuance in euros, 
   it does not control the euro. It would have to either leave the euro (regaining sovereignty)
   or persuade the whole union.
2. **The bloc can implement CS, but only as a bloc.** If the euro-area members collectively agree
   to unified ECB citizen-issuance, then the union as a whole *is* the monetary sovereign the
   framework requires, and the mechanism works at euro-area scale.
3. **The barrier is political, not economic or mechanical.** The money plumbing is arguably the
   cleanest of any region (the ECB publishes M1/M2/M3 with excellent detail). What is missing is
   the political integration to authorize union-level citizen-issuance.

**The engine entry therefore models the euro area AS IF the bloc had agreed to implement CS
collectively.** It is a "what the numbers would be if the political prerequisite were met" case,
not a claim that any single European government could switch this on. The engine must show this
caveat whenever the Eurozone is selected, or it misrepresents the framework's own stated
prerequisite.

---

## 1. Macro parameters (ECB / Eurostat primary; euro area, NOT EU-27)

**Scope note:** all figures are for the **euro area** (the ~20 members using the euro), not the
EU-27. The EU-27 has ~449M people and ~EUR 17.9T GDP; the euro area is smaller. Mixing them
would be an error.

| Parameter | Euro area value | Reference | Primary source |
|---|---|---|---|
| Broad money **M3** | **EUR 17.2 T** | Nov 2025 | ECB (headline broad aggregate) |
| Transaction-active **M1** | **EUR 11.27 T** | Apr 2026 | ECB (currency in circulation + overnight deposits) |
| **M^T / M3 ratio** | **≈ 65.5%** | - | constructed (see §2) |
| Nominal **GDP** | **≈ EUR 15.9 T** | 2025 | ECB (external debt EUR 17.00T = 107% GDP → 15.9T) |
| Real trend growth **g** | **≈ 1.4%** | 2025 | ECB Dec-2025 projection (Statista 1.2%) |
| **Population** | **≈ 349 M** | 2025 | Eurostat (euro area; distinct from EU-27 449M) |
| Equity **market cap** | **≈ 68% of GDP ≈ EUR 10.8 T** | 2025 | Eurostat/Wikipedia (bank-based economy; US is 170%) |
| Government **debt** | **≈ 88% of GDP** | 2025 | Maastricht euro-area average |

**Structural note:** the euro-area listed-equity market is small relative to GDP (~68%) because
Europe is **bank-based**, not market-based (EU bank assets ≈ 300% of GDP vs 85% in the US). This
materially lowers the structural-buyer flow as a share of the equity market and is a genuine
euro-area feature, not an artifact.

---

## 2. Transaction-active share (M^T / M3)

The ECB's M1 is a textbook transaction-active measure:

> **M1 (narrow money)** = currency in circulation (banknotes and coins) + overnight deposits.
>, ECB, monetary aggregate definitions.

Overnight deposits = immediately spendable = the M^T property.

    M^T (euro area) = M1 = EUR 11.27 T
    M3              = EUR 17.2 T
    M^T / M3        = 65.5%

The euro-area share (~65.5%) is high, close to the UK (69.7%), and well above the US (51.35%).
Broad M3 includes marketable instruments (repos, MMF shares, short debt securities) that most
households never transact in, so the transaction-active core is a large fraction. The share is
genuinely euro-area-specific; the US and UK values are not imported.

---

## 3. Realizable return (two-path, same method)

### Path 1: Production function (matched to Paper 5)
Euro-area labour share is sourced directly, NOT copied from the UK. Eurostat reports
compensation of employees at 48.6% of GDP (2025, unadjusted), and the ECB's *adjusted* wage
share (corrected for self-employed, over gross value added) at ~0.615. That adjusted figure is
the right basis, and it is slightly LOWER than the UK's 0.63, so the euro-area capital share is
slightly higher: **alpha_EA ≈ 0.385** (vs UK 0.37). Holding K/Y = 3.0:

    r0(EA) = 0.385/3.0 - 0.05 = 7.83%  (baseline)  ->  ~5.00% realizable (Mode B)

The euro area is therefore NOT identical to the UK (a natural question, since both have ~0.6x
labour shares): UK baseline 7.33% / realizable 4.68%; euro-area baseline 7.83% / realizable 5.00%.
The small gap is real and traces to the sourced labour-share difference.

### Path 2: Historical realised returns
DMS pan-European / Germany + France long-run real equity ≈ 4.5-5.0%, lower than the UK (5.3%)
and US (~6.5%), consistent with continental Europe's lower historical equity returns and the
World Wars' capital destruction in the DMS record.

### Reconciliation (honest note on the tightest fit of the four)
Realizable ~5.00% sits at the TOP of the euro-area historical equity range (~4.5-5.0%), rather
than comfortably below it as in the US, UK, and Canada cases. The two paths are still close and
consistent, but the euro-area reconciliation has the least slack of the four calibrations. This
is flagged rather than hidden: the production-function path and the historical path agree to
within their uncertainty, but a conservative reading would place the euro-area realizable return
slightly lower (toward 4.6-4.8%) to preserve the broad-below-equity ordering. **Euro-area
realizable return (Mode B) ≈ 5.00%, band 3.8-5.8%, with a conservative alternative ~4.7%.**

---

## 4. Engine changes (adds € as a fourth entry)

| Engine input | US | UK | Canada | Eurozone |
|---|---|---|---|---|
| Currency | $ | £ | C$ | € |
| Broad money | $22.4T (M2) | £3.27T (M4) | C$2.82T (M2) | €17.2T (M3) |
| M^T share | 51.35% | 69.7% | 61.5% | 65.5% |
| GDP | $30.8T | £3.04T | C$3.2T | €15.9T |
| Population | 342M | 69.5M | 41.5M | 349M |
| Market cap | $69T (~2.2×) | £2.96T (~0.97×) | C$6.2T (~1.93×) | €10.8T (~0.68×) |
| Real growth | 2.0% | 1.2% | 1.7% | 1.4% |
| Realizable (Mode B) | 4.26% | 4.68% | 4.90% | 5.00% |
| Govt debt | ~102% | ~95% | ~41% | ~88% |
| **Sovereign?** | yes | yes | yes | **only as a bloc (see §0)** |

The Eurozone entry carries a visible caveat in the engine noting the political prerequisite.

---

## 5. Audit checklist

- [ ] Confirm M1 and M3 at a common date from the ECB Data Portal (BSI series)
- [ ] Confirm euro-area (not EU-27) population and market cap at stated dates
- [ ] Confirm the euro-area listed-equity/GDP ratio (~68%) against an ECB/FESE figure
- [ ] Return: two-path central 4.68% + band; DMS Europe equity cross-check to the printed figure
- [ ] Caveat text (§0) displayed in the engine whenever Eurozone is selected

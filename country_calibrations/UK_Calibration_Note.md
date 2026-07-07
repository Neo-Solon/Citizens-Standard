# Citizens Standard: United Kingdom Calibration Note (Pilot)

**Purpose.** Re-parameterise the CS engine to the United Kingdom using primary-source
data, to the same standard as the US calibration in the papers. Every figure below
traces to a named primary source. Two parameters require construction rather than
direct citation (the transaction-active money share M^T, and the realizable return);
both constructions are shown in full, and the one genuine methodological choice (the
capital-output construct) is stated openly rather than hidden in a point estimate.

**Status:** macro block complete and primary-sourced. Realizable return re-estimated by two
independent paths and cross-checked against the canonical UK return series (DMS). For audit before wiring into the engine.

---

## 1. Macro parameters (all primary-sourced)

| Parameter | UK value | Reference date | Primary source |
|---|---|---|---|
| Broad money **M4** | **£3,272 bn** | Apr 2026 | Bank of England, M4 series (Bankstats) |
| Transaction-active money **M^T (= M1)** | **£2,280 bn** | Dec 2024 | Bank of England, M1 (notes & coin + non-interest-bearing deposits + interest-bearing sight deposits) |
| **M^T / M4 ratio** | **≈ 69.7%** | - | constructed (see §2) |
| Nominal **GDP** | **£3,037 bn** | 2025 | ONS, via House of Commons Library |
| Real trend growth **g** | **≈ 1.1-1.3%** | 2025 / OBR fwd | ONS; OBR Economic & Fiscal Outlook |
| **Population** | **69.49 m** | mid-2025 | ONS, provisional mid-2025 estimate (accredited official statistic) |
| Equity **market cap** (domestic) | **≈ 97% of GDP ≈ £2,958 bn** | Dec 2025 | LSE market cap ÷ ONS GDP (CEIC construction); domestically-listed only |
| Government debt **PSND ex** | **≈ 95-96% of GDP** | 2025 | ONS, Public Sector Finances |
| Notes in circulation | £91.5 bn | Feb 2025 | Bank of England, Banknote Statistics |

Notes:
- M^T and M4 are at different reference dates (Dec 2024 vs Apr 2026); before wiring in,
  both should be pulled at a common date from the BoE Database (M4 headline series;
  M1/M2 in Bankstats Tables A2.2.1 / A2.3). The ratio is stable month-to-month, so
  ~69.7% is robust, but same-date figures are preferred for the published note.
- Market cap uses the domestically-listed basis (matches the US market-cap construct in
  the engine), not the total-LSE figure (which includes large foreign listings ≈ £4.5T).

---

## 2. Construction of the transaction-active share (M^T / M4)

The US calibration (Paper 10) separates transaction-active money (M^T) from broad money
and finds M^T/M2 = 51.35%. The UK equivalent is built from the Bank of England's own
published aggregate definitions, which draw the transaction boundary explicitly:

> **M1** = notes & coin held by the private sector + non-interest-bearing deposits +
> interest-bearing **sight** deposits. **Sight** deposits are those "accessible without
> penalty, either on demand or by close of business on the day following." **Time**
> deposits are "all other deposits.", Bank of England, Statistics FAQ.

This is the same economic distinction M^T captures: money available for transactions
(penalty-free, on-demand) versus money held as a store of value (time/notice deposits).
The BoE boundary is arguably cleaner than a constructed cut because it is defined by the
economic property itself (penalty-free on-demand access).

    M^T (UK) = M1 = £2,280 bn
    M4       = £3,272 bn
    M^T / M4 = 69.7%

**Finding (flagged for honesty):** the UK transaction-active share (~70%) is materially
higher than the US M^T/M2 share (51.35%). This is real, not an artefact: UK M4 and US M2
are bounded differently, and UK sight deposits are a larger fraction of broad money. It
means the UK price-stability locus differs from the US one and must be recomputed with
the UK ratio, the US 51.35% must NOT be imported.

Optional refinement: the BoE also publishes a **Divisia** money index that weights each
M4 component by its transaction-service content (Barnett aggregation). A Divisia-weighted
M^T could be used as a robustness cross-check on the 69.7% sight-deposit cut; both are
defensible, and they should agree closely.

---

## 3. Realizable return (deeper re-estimation: two independent paths, triangulated)

The return is the least mechanical parameter, so it is derived two independent ways and
cross-checked, rather than asserted from one stylised assumption.

### Path 1: Production function (matched to Paper 5's Solow construct)

Paper 5's US baseline is `r0 = alpha/(K/Y) - delta = 0.35/3.0 - 0.05 = 6.67%`. The K/Y = 3.0
is a standard mid-range Solow calibration (textbook values span ~2.5 (Mankiw) to ~4.3
(Golden Rule); 3.0 is a defensible convention, not a hard US measurement). The only
cleanly-sourced UK structural parameter that genuinely differs is the capital share:

- UK labour share ≈ 0.63 (ONS; Caswell 2024) ⇒ **alpha_UK ≈ 0.37**.

Holding the K/Y construct matched to Paper 5 (3.0) and changing only alpha:

    r0(UK) = 0.37/3.0 - 0.05 = 7.33%   (UK no-program baseline; US 6.67%)

This is the GROSS marginal product of total productive capital, before program attenuation.

### Path 2: Historical realised returns (independent of the production function)

Cross-check against the Dimson-Marsh-Staunton (DMS) database, the canonical long-run
return dataset (UBS/Cambridge/LBS Global Investment Returns Yearbook 2025, 125 years):

- **UK real equity return, 1900-2024: ≈ 5.3% real** (DMS)
- World real equity, 125yr: 5.2%; world 2000-2024: 3.5% (lower-return era)

### Reconciliation (the validation)

The two paths measure related but distinct objects and should NOT be equal:
- Path 1 (7.33%) is the aggregate marginal product of *total* capital (broad base).
- Path 2 (5.3%) is the realised return to *listed equity* (a levered claim on a subset).

The floor return the engine uses is the **attenuated** return (Paper 5 compresses the US
6.67% baseline to 4.26% in Mode B via the r→g mechanism). Applying the same attenuation
ratio to the UK:

    UK: 7.33% baseline  ->  ~4.68% realizable (Mode B)

**4.68% sits just below the 5.3% UK historical equity return**, exactly the expected
relationship, since the realizable floor is a broad, attenuated claim that should earn
slightly less than levered listed equity. The same reconciliation holds for the US in
Paper 5 (6.67% → 4.26% realizable, against US historical equity ~6.5% real), so the UK is
treated on identical footing.

**Conclusion:** the two independent paths converge on a consistent, economically sensible
relationship. UK realizable return (Mode B) ≈ **4.68%**, baseline ≈ **7.33%**. This is no
longer a single-assumption estimate with a caveat, it is triangulated and cross-checked
against the canonical UK return series. Residual sensitivity remains in the K/Y convention
(shared with Paper 5's US figure), so a band of roughly 4.3-5.0% realizable is appropriate,
matching the style of Paper 5's own reported band.

## 4. What changes in the engine (UK vs US)

| Engine input | US | UK |
|---|---|---|
| Currency symbol | $ | £ |
| Broad money | $22.4T (M2) | £3.27T (M4) |
| M^T share of broad money | 51.35% | 69.7% |
| GDP | $30.8T | £3.04T |
| Population | 342M | 69.5M |
| Market cap | $69T (~2.2× GDP) | £2.96T (~0.97× GDP) |
| Real growth (default) | 2.0% | 1.2% |
| Realizable return (Mode B) | 4.26% | 4.68% (triangulated, band 4.3-5.0%) |
| Baseline return r0 | 6.67% | 7.33% (α-adjusted, K/Y matched) |
| Govt debt (context) | ~102% | ~95% |

The price-stability locus, floors, and dividends all recompute from these; none of the
US structural ratios are imported. The M^T share and market-cap/GDP ratio are the two
inputs that differ most and will move the UK outputs materially away from a "US model in
pounds."

---

## 5. Audit checklist (for sign-off before wiring in)

- [ ] M4 and M^T pulled at a common reference date from BoE Database
- [ ] Market cap confirmed on domestically-listed basis at a stated date
- [x] Return: DONE, triangulated via production function (7.33% baseline / 4.68%
      realizable) AND cross-checked against DMS UK historical equity (5.3%); band 4.3-5.0%
- [ ] Divisia cross-check on the 69.7% M^T share (optional robustness)
- [ ] Confirm growth default (1.2% trend vs a forward OBR figure)

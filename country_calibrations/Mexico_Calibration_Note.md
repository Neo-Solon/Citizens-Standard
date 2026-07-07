# Citizens Standard: Mexico Calibration Note

Mexico is a monetary sovereign (Banco de México issues the peso), a standard unilateral calibration mechanically. As an emerging market (like India), it is flagged honestly on two fronts: a shallow equity market (~28% of GDP) and a realizable-return estimate where the two estimation paths genuinely *diverge*, resolved conservatively toward the weaker realized history rather than the more favourable production-function figure.

**Status:** macro block primary-sourced (Banxico, INEGI, SHCP, BMV).

------------------------------------------------------------------------

## 1. Macro parameters (engine units: Mex\$ trillion)

| Parameter                 | Value                         | Reference  | Source                                              |
|---------------------------|-------------------------------|------------|-----------------------------------------------------|
| Broad money **M2**        | **Mex\$16.5 T**               | Mar 2026   | Banco de México (Agregados Monetarios)              |
| Transaction-active **M1** | **≈ Mex\$8.25 T**             | early 2026 | Banxico (currency + immediate-demand deposits)      |
| **M^T / M2 ratio**        | **≈ 50%**                     | \-         | constructed (see §2), M1/M2 ≈ 8.25/16.5             |
| Nominal **GDP**           | **≈ Mex\$35.5 T**             | Mar 2026   | INEGI / SHCP (~US\$2.03T)                           |
| Real trend growth **g**   | **≈ 1.8%**                    | 2025-26    | INEGI (2025 weak ~0.6-0.8%); Banxico 2026 proj 1.6% |
| **Population**            | **≈ 130.8 M**                 | Jan 2026   | INEGI / CONAPO / UN (10th most populous)            |
| Equity **market cap**     | **≈ Mex\$9.9 T ≈ 28% of GDP** | 2025       | BMV / CEIC (US\$508bn; shallow, EM feature)         |
| Government **debt**       | **≈ 50% of GDP**              | Apr 2026   | SHCP (SHRFSP, broadest measure; 18.6T MXN)          |
| Inflation                 | **~3.5-4%**                   | 2025-26    | Banxico (near the upper target band)                |

Mexico is a mid-growth economy (~1.8% real trend, weaker in 2025 at ~0.6-0.8%), with a peso that has seen repeated historical crises. Its equity market, while liquid, is small relative to GDP (~28%), which matters for the ownership arithmetic in §4.

------------------------------------------------------------------------

## 2. Transaction-active share (M^T / M2): mid-range

Banxico's M1 = banknotes and coins held by the public + immediate-demand deposits, the transaction-active measure. M2 = M1 + resident time deposits, debt mutual-fund shares, and repo creditors.

    M^T (Mexico) = M1 ≈ Mex$8.25 T
    M2           ≈ Mex$16.5 T
    M^T / M2     ≈ 50%

**At ~50%, Mexico sits mid-range** (developed set is 50-80%; India and Korea are ~28-30%). Roughly half of Mexican broad money is held in transaction-active form and half in term/savings instruments, a balance typical of a middle-income economy with a sizeable but not dominant term-deposit segment. No adjustment flag is needed on this figure; it is a clean primary-sourced ratio.

------------------------------------------------------------------------

## 3. Realizable return: two paths that diverge (EM caution applied)

### Path 1: Production function

Mexico's labour share is ~0.56 (a large informal sector, moderate formal capital share) → alpha ≈ 0.44 → production-function baseline ~9.8% → **~6.2% realizable**. That is a solid mid-set figure, below India's ~7.0% but comfortably above the developed floor.

### Path 2: Historical realised returns

Mexican equity (IPC / Bolsa) has delivered materially weaker long-run real returns than India, roughly **~4.5% real** and among the lower emerging markets in the DMS dataset, with high volatility driven by repeated peso crises (1976, 1982, 1994) and persistent currency risk. The shallow market (~28% of GDP) compounds the caution.

### Resolution: weight the weaker realized path

Unlike India, where both paths pointed high and agreed, Mexico's two paths **diverge**: the production function says ~6.2% but the realized equity history says ~4.5%. When a structural-buyer mechanism must pick one, anchoring on the more favourable production-function number would ignore a century of actual Mexican equity experience. The central realizable is therefore set **conservatively at 4.7% (Mode B), band 3.7-5.7%**, close to the realized-history path, with the production-function figure retained only as the top of the band. This is the honest call: the divergence itself is the finding, and where a production estimate and a realized history disagree for an EM, the realized history plus currency risk should dominate.

------------------------------------------------------------------------

## 4. Broad citizen ownership under Mode Ω

Running Mexico in Mode Ω produces a citizen market-ownership share that is **elevated relative to the US**, for the same structural reason as India: a shallow equity market (~28% of GDP) means the structural-buyer flow is large relative to market size, pushing the ownership ceiling up.

The ceiling is set by the flow-to-growth ratio **c / g**, not a fixed percentage. Mexico's moderate growth (g ~1.8%) gives a smaller growth-funded budget than India's, so the ownership share lands below India's ~47% but still above the developed set: the shallow market is the dominant term. As with every country, this is reported as the true output of the design, not tuned to a target. The honest framing holds: **in shallower markets citizens can end up owning a larger share than the US ~10%, and Mexico's ~28%-of-GDP market makes it one of those cases**, though its slower growth keeps the share below India's.

------------------------------------------------------------------------

## 5. Engine values

Currency Mex\$. M^T share 50%. Defaults: M2 Mex\$16.5T, GDP Mex\$35.5T, pop 130.8M, market cap Mex\$9.9T. Real growth 1.8%, pop growth 0.6%. Realizable band 3.7 / 4.7 / 5.7 / 7.2 / 7.2. Mode B return 4.7%.

------------------------------------------------------------------------

## 6. Audit checklist

- \[ \] Confirm M1 and M2 at a common date from the Banxico Agregados Monetarios release
- \[ \] Confirm nominal GDP to the printed INEGI/SHCP figure (seasonally-adjusted annualized)
- \[ \] Confirm BMV domestic market cap at a stated date (the ~28%-of-GDP ratio is the load-bearing input for §4)
- \[ \] Return: the 4.7% central is a deliberate weighting toward realized IPC/Bolsa history (~4.5%) over the production-function figure (~6.2%); pin to a Mexican equity total-return real series
- \[ \] Population growth: confirm current annual rate (~0.6%, decelerating)


[back to top ↑](#top)

<div id="norway" class="section note">


# Supplementary record — the liquidation flow `L_t`

**Status:** postdates the published papers. Not yet in Paper 5 or Paper 1.
**Verified by:** `replication/liquidation_flow_replication` (runs in the one-push suite and in the
browser verifier under Paper 5). 181/181 published values reproduce.

---

## The gap

Paper 5 (Macro Model) §3.3 puts the price level on the transactional circuit:

> `P_t = M^T_t · V / Y_t` — price stability requires `M^T` to grow with `Y`.

and names the channel that feeds it:

> *"The transactional circuit is fed by **the liquidation flow L_t** — the conversion of matured
> floor balances into spendable income — and by wages. The issuance rule and the liquidation flow
> are **jointly calibrated** so that M^T tracks Y."*

Paper 1 (Architecture) makes it a hard ceiling:

> *"K3 shares the spendable budget with KI and the Stable Floor liquidation flow, so
> **K3 + KI + liquidation must remain within the Y-matched expansion of the circulating pool**."*

**`L_t` is never given a number in any of the fourteen papers.** Paper 5 §3.5 states the exposure
plainly:

> *"Today's liquidation flow `L_t` is set by floors accumulated decades earlier; it cannot be
> changed by adjusting issuance now… Pure Mode B (KI = 0) is price-stable in steady state … but
> has weak short-run stabilization, **relying on `L_t` being on-target by balanced-growth
> construction**."*

It was assumed on-target. It is not.

## The result

| | |
|---|---|
| `L_t` at launch | **$0B** — no floor has matured |
| Launch injection (K3 + spillover) | **$230.1B** vs a required **$229.7B** — on the locus, exactly as Paper 5 claims |
| Circulating-pool ceiling first breached | **2048** |
| Peak implied goods inflation | **+1.60%** (2100) |
| κ_d must reach zero by | **2087**, and go negative after |
| μ = M^T/M2 | **0.513 → past 1.0** (the asset circuit drains) |

The launch calibration is **correct**. It is a *launch* property. `K3` was sized to fill the
**entire** Y-matched expansion at a moment when `L_t = 0`; as floors mature, `L_t` lands on top of
a budget that is already full.

**This is not an `r > g` artifact.** The breach survives `r = g` (2053) and `r < g` (2054);
`r > g` only amplifies it. It survives every parameter varied — `w` ∈ [3%, 6%], `r` across the
Macro §6.7 band [3.30%, 5.03%], and κ_d ∈ {0, 0.40, 0.60}.

## Why this vindicates Paper 5 rather than refuting it

§3.5 already argues, qualitatively:

> *"This is a structural argument — straight from the two-pool accounting — for why the framework
> needs the KI channel and the adaptive Mode Λ as genuine control instruments, not merely
> distributional choices."*

That is exactly what the computed `L_t` shows. §3.5 reasoned to the right conclusion without the
magnitude. This supplies the magnitude — and the schedule.

## What the framework's own code already had

`replication/empirical_replication/code/demographic_flow_model.py`:

```python
wd[retire:] = w * floor[retire:]
ret_consumption = wd[retire:].sum()
net_abs = issuance - ret_consumption
```

`ret_consumption` **is** `L_t`. It is used only for Paper 8's asset-price question (does the FDCA
remain a net buyer?) and never pointed at the price level.

## Accounting note — why it went unmeasured

`K1`, `K2`, `K3` are **new money**: they raise `M2`. `L_t` is **not** — a retiree sells equity to a
buyer paying with **existing** money. `L_t` is a **transfer from M^A to M^T**, leaving `M2`
unchanged.

It therefore cannot appear in any quantity-of-money check. But it lands squarely on
`P = M^T · V / Y`.

## Data

* Mortality — SSA [Period Life Table](https://www.ssa.gov/oact/STATS/table4c6.html), real `l_x` by
  single year of age. Replaces the framework model's hard "everyone dies at 85."
* Validation — the stable population reproduces the published US **65+ share: 17.5% modelled vs
  18.0% actual** ([Census](https://www.census.gov/data/tables/time-series/demo/popest/2020s-national-detail.html)).
* μ — measured from the framework's own `M^A` construction (`two_circuit_supplementary_record/MA_series.csv`,
  FRED). It ranges **0.23–0.50** historically; the engine hardcodes **0.5135**.

Every other parameter is the framework's own, unchanged — including `w = 4%`, which is the default
in the framework's own `demographic_flow_model.py`.

## Open — needs adversarial review before it enters the papers

The `M^A → M^T` transfer accounting is the load-bearing step. It should be attacked by someone
motivated to break it before this is written into Paper 5.

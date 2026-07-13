# The liquidation flow `L_t`, computed

> **Status: SUPPLEMENTARY — this postdates the published papers.**
> It is not in Paper 5 or Paper 1 yet. It is kept as a *separate* package, deliberately, rather
> than folded into `macro_replication`: that package's contract is to reproduce **Paper 5 as
> published**, and this finding is not in Paper 5. Folding it in would corrupt that contract and
> imply the paper already contained it. Once it is written into Paper 5 — after adversarial
> review of the `M^A → M^T` accounting — it should be merged into `macro_replication` and this
> package retired.

Supplementary to **Paper 5 — A Macroeconomic Model** (§3.3, §3.5) and
**Paper 1 — Architecture** ("Two bounds on κ_d").

## What this answers

Paper 5 defines the price level on the transactional circuit:

> `P_t = M^T_t · V / Y_t` — so price stability requires `M^T` to grow with `Y`.

and states that `M^T` is fed by **the liquidation flow `L_t`** — "the conversion of matured floor
balances into spendable income" — with:

> "The issuance rule and the liquidation flow are **jointly calibrated** so that M^T tracks Y."

Paper 1 turns that into a hard constraint:

> "K3 shares the spendable budget with KI and the Stable Floor liquidation flow, so
> **K3 + KI + liquidation must remain within the Y-matched expansion of the circulating pool**."

**`L_t` is never given a number in any of the 14 papers.** Paper 5 §3.5 concedes the exposure:

> "Pure Mode B (KI = 0) is price-stable in steady state … but has weak short-run stabilization,
> **relying on `L_t` being on-target by balanced-growth construction**."

This package computes it.

## Result

| | |
|---|---|
| `L_t` at launch | **$0B** — no floor has matured |
| Launch injection (K3 + spillover) | $230B against a required $230B — **on the locus**, as the paper says |
| Constraint first breached | **2048** |
| Peak implied goods inflation | **+1.60%** (2100) |
| κ_d must reach zero by | **2087**, and go negative after |

The launch calibration is correct. It is a *launch* property. `K3` was sized to fill the **entire**
Y-matched expansion at a moment when `L_t = 0`; as floors mature, `L_t` lands on top of a budget
that is already full.

**This is not an r > g artifact.** The breach survives `r = g` (2053) and `r < g` (2054); `r > g`
only amplifies it. It survives every parameter variation tested.

## What is new vs. the framework's existing code

`replication/empirical_replication/code/demographic_flow_model.py` **already computes this
quantity**:

```python
wd[retire:] = w * floor[retire:]
ret_consumption = wd[retire:].sum()
net_abs = issuance - ret_consumption
```

`ret_consumption` *is* `L_t`. It is used only for Paper 8's asset-price question (does the FDCA
remain a net buyer?) and is never pointed at the price level. This package points it there.

Two inputs are upgraded to real data:

* **mortality** — the SSA period life table (real `l_x`, single year of age) replaces the
  framework model's hard "everyone dies at 85".
* **μ = M^T/M2** — measured from the framework's own `M^A` construction (FRED savings + small
  time deposits, `two_circuit_supplementary_record/MA_series.csv`), which shows μ ranging
  **0.23–0.50** historically, not the constant 0.5135 the engine hardcodes.

Every other parameter is the framework's own, unchanged.

## Accounting note (why this went unmeasured)

`K1`, `K2`, `K3` are **new money** and raise `M2`. `L_t` is **not**: a retiree sells equity to a
buyer paying with **existing** money. `L_t` is a **transfer from M^A to M^T** — it leaves `M2`
unchanged.

So it can never show up in a quantity-of-money check. But it lands squarely on `P = M^T · V / Y`.

## Run

```
python code/run_all.py
```

## Sources

* SSA, [Actuarial Life Table (Period Life Table)](https://www.ssa.gov/oact/STATS/table4c6.html)
* US Census Bureau, [National Population by Characteristics](https://www.census.gov/data/tables/time-series/demo/popest/2020s-national-detail.html) — validation target (65+ share)
* FRED — `M2SL`, `WSAVNS`/`MDLM`, `STDSL` (via the repo's own `two_circuit_supplementary_record`)

## Before this enters the papers

The load-bearing step is the **`M^A → M^T` transfer accounting**: that a retiree's equity sale is
funded with *existing* money (so `M2` is unchanged) but moves that money into the transactional
circuit (so `M^T` rises). Everything downstream follows from it.

It should be attacked by someone motivated to break it before Paper 5 is amended and reissued.

# How the engine works — the issuance channels

*A guided walk through the one piece that unlocks the rest of the framework: how K1, K2, K3, and KI are calculated, why inflation is an output rather than a dial, and why every channel can be set to zero.*

---

## The one idea to hold onto

There is a single pot of new money each year, and it is tied to one thing: how much the real economy grew. Everything else — the channels, the modes, the dividend, the floor — is just **how big you make that pot, and where you send it.** Inflation is never something you dial in. It falls out of where the money lands.

If you hold only that, the whole console reads cleanly: it's a control surface for sizing and routing one growth-tied budget, nothing more.

The base numbers (US calibration, all adjustable in the engine):

- **M2 ≈ $22.4T** — broad money.
- **Real growth g ≈ 2%** — how fast real output expands.
- **Mᵀ ≈ $11.5T** — the *transactional* slice of M2 (the share that actually moves goods prices). It's 51.35% of M2. This is the number that matters for inflation, and almost nobody separates it out — that separation is the whole trick.

Two derived anchors everything sits against:

- **g × M2 ≈ $447B** — the *full* growth budget (money growing in step with the whole stock).
- **g × Mᵀ ≈ $230B** — the *price-stability locus*: new money reaching the transactional circuit at exactly this rate holds goods prices flat. This is the leash.

---

## The two pools (this is the part that's easy to miss)

Money created by the system lands in one of two circuits, and they behave completely differently:

- **The transactional circuit (Mᵀ)** — money people spend. Anything that lands here pushes on goods prices.
- **The asset circuit (Mᵃ)** — money locked into the citizen savings floor (equity, held). It buys assets, not groceries, so it does *not* push goods prices — except for a small, modelled leakage (spillover ≈ 20% of what's locked).

So the same dollar of new money is inflationary or not **depending only on which pool it lands in.** A dollar paid out as a spendable dividend hits Mᵀ. A dollar locked into the floor sits in Mᵃ and is nearly inert on prices. Hold that, and the modes stop looking like magic.

---

## The four channels, and how each is calculated

Every year the engine computes these in order:

**K1 — Citizenship.** A one-time endowment into the floor for each *new* citizen.

```
K1 = k1  ×  (GDP / population)  ×  (new citizens that year)
```

`k1` is a percentage of GDP-per-capita (default 2.5%). It's paid first, off the top of the budget. Set `k1 = 0` and no citizenship endowment is created.

**K2 — Growth rate.** The throttle on the size of the whole growth budget.

```
Growth budget  =  k2  ×  M2  ×  g
```

`k2` is the share of the growth-matched budget you actually issue. At `k2 = 100%` the budget is the full $447B; at `k2 = 17.5%` it's about $78B; at `k2 = 0` there is no budget at all. **This single dial sets how much new money exists.** (K1 is then subtracted from it; whatever's left is the residual that gets split below.)

**K3 — the dividend share (κ_d).** This one is not a spigot — it's a *router*, and that's the most common point of confusion. It splits the residual budget between the two pools:

```
Dividend (to Mᵀ, spendable)  =  κ_d        ×  residual budget
Floor    (to Mᵃ, locked)     =  (1 − κ_d)  ×  residual budget
```

The two shares **always sum to 100%.** Moving the dividend up moves the floor down by the identical dollars — *the total money issued does not change.* So K3 is price-relevant (it decides how much lands in Mᵀ) but it is **not** a way to create more money. κ_d = 0 is all-floor; κ_d = 100% is all-dividend.

**KI — the inflation gap.** The only channel that issues money *above* the growth line.

```
KI  =  ki  ×  M2
```

This is additive — it's not carved out of the growth budget, it's piled on top, and it lands in Mᵀ. It is the **only** channel that deliberately creates inflation. Set `ki = 0` and there is no above-line issuance. (Mode C uses it to fund a visible monthly dividend at the cost of ~2% inflation.)

---

## Inflation is the output

Once the channels are set, the engine doesn't *ask* for an inflation rate — it computes one:

```
inflation  =  ( dividend  +  KI  +  floor spillover )  /  Mᵀ   −   g
                └──────── money reaching Mᵀ ────────┘
```

In words: take everything that actually reaches the transactional circuit, express it as a rate against Mᵀ, and subtract real growth. If money reaches Mᵀ at exactly the growth rate, the two cancel and **prices are flat.** Below it, deflation. Above it, inflation. The floor (K2/Mᵃ) barely appears, because locked money isn't chasing goods.

That's why the modes land where they do — and you can check each by hand:

| Mode | k1 | k2 | κ_d (K3) | KI | What reaches Mᵀ | Inflation |
|---|---|---|---|---|---|---|
| **A** deflation | 2.5% | 17.5% | 0% | 0 | only floor spillover (~$16B) | **−1.86%** |
| **B** stable | 2.5% | 100% | 40% | 0 | dividend $176B + spillover ~$54B ≈ $230B | **0%** |
| **C** inflation | 2.5% | 17.5% | 0% | 1.98% | KI $443B (= ~$108/citizen·mo) | **+2.0%** |
| **D** pure dividend | 0 | 51.35% | 100% | 0 | dividend $230B (exactly the locus) | **0%** |

Mode B and Mode D reach price stability by completely different routes — B locks 60% and pays 40%, D locks nothing and pays it all — yet both put about $230B into Mᵀ, which is the locus. That's the design working: the leash is on the transactional circuit, and there's more than one way to sit on it.

---

## The point: every channel can be zero

Here is the thing worth showing anyone who hears "this is just printing money."

Set **k1 = 0, k2 = 0, KI = 0.** (K3 is then moot — there's no budget to route.) Walk it through the formulas above and every term is zero: no citizenship endowment, no growth budget, no floor, no dividend, no inflation-gap issuance. **The system creates exactly zero new money.** It is not a printing press with the dial stuck on "more." Zero is one of its settings.

And the consequence is the opposite of what the fear assumes. With no new money and a real economy still growing ~2%, the same money stretches over more goods, so the inflation formula gives:

```
inflation  =  0 / Mᵀ  −  g  =  −2%
```

A dollar *gains* about 2% a year. Zero issuance is the hard-money / fixed-supply corner — the gold-standard outcome — and the engine contains it as a limiting case. Mode A (mild deflation) is just a step in from there; Mode B/D (stability) a few steps further; Mode C (mild inflation) one step past stable. **The framework isn't inflationary or deflationary by nature. It spans the whole range, and the dials decide — including all the way down to creating nothing at all.**

That is what defuses the printing-money objection: the zero setting itself. And even at zero, the citizen comes out ahead of today, because it is today's dollar that quietly loses 2-3% a year — not this one.

---

## Index versus dividend: ownership or income

The K3 router decides more than "locked or spendable." It decides whether a citizen's share of the new money becomes **ownership** or **income** — two different things with two different fates.

- **The floor (the index side).** The `(1 − κ_d)` share that stays locked isn't held as cash. It's used to **buy equity in the domestic market index**, and held. That makes each citizen a part-owner of the country's productive capital: it compounds with the market, it's *wealth*, and because it sits in the asset circuit it barely touches goods prices. This is the **structural buyer** — the system standing in the market every year, buying the index on citizens' behalf.

- **The dividend (the income side).** The `κ_d` share is paid out as **spendable cash**. It's *income* — consumed, hitting the transactional circuit, gone once spent. It builds no stake.

So κ_d isn't just a price dial. It's the choice between handing people *a slice of the market* and handing them *a cheque*. Mode B leans to ownership (60% floor); Mode A is almost pure ownership; Mode D is pure cheque — 100% dividend, **no index bought at all** (A* = 0).

## How the floor buys the index — measured against total market cap

The index purchases are sized and tracked directly against the whole market. Three numbers do it:

**A\* — the structural-buyer flow.** The dollars going into the index each year:
```
A*  =  K1 endowment  +  (1 − κ_d) × growth budget
```
This *is* the floor money — citizenship endowments plus the locked share of the budget.

**c — the flow as a share of the market.** A* measured against total index market cap:
```
c  =  A*  /  market cap
```
At the default $69T market, Mode B's A* ≈ $272B is **c ≈ 0.39% of the entire market, per year** — the annual bite the structural buyer takes.

**ψ\* — realized citizen ownership.** Buying c% a year and holding for `dur` years doesn't simply stack to c × dur, because the market is also growing *and* citizens eventually draw their floors down. The realized share is a growth-discounted accumulation:
```
ψ*  =  c × annuity(g, dur),     annuity(g, dur) = (1 − (1+g)^−dur) / g
```
At the defaults (40-year hold, 2% growth), Mode B settles near **ψ* ≈ 10%** of the index owned by citizens collectively — leaving **~90% as tradable private float** (`1 − ψ*`). The engine brackets this between two decumulation models and shows the band.

And the ceiling is the key line: no matter how long the hold, ψ* cannot run past **c / g** (here ≈ 20%). Ownership *asymptotes* — it does not compound without limit.

## "If we didn't bound it" — why citizens don't end up owning everything

*(The question below is the one a sharp reader asks first: what happens if the structural buyer is not bounded.)*

This is the real tension in a permanent buyer, and it is worth being explicit about, because a sharp reader goes straight to it: **if the system buys a slice of the index every year, forever, doesn't it eventually own the whole thing?**

If nothing bounded it, yes. Naive accumulation — c × duration, with no growth-discounting and no draw-down — would climb past any level, and at the extreme a fully-captured floor would imply owning *more than 100%* of the market, which is impossible. That impossibility isn't waved away; it's the hinge of the feasibility argument (the structural-buyer paper's feasibility analysis, and the ownership-feasibility figure in the macroeconomic model, where naive full capture crosses 100% while the recalibrated design sits safely below).

Three things bound it, and all three are in the engine:

1. **The c/g ceiling.** Because the market grows at g while the buyer adds c, ownership asymptotes to c/g and stops — at the calibrated flow it never approaches 100%.
2. **Decumulation.** Floors aren't held forever; citizens draw them down in retirement, recycling shares back into the tradable float. That's why realized ψ* (≈10%) sits well below even the no-draw-down upper bound, c × dur.
3. **Return attenuation.** As citizens own more of the capital stock, the marginal return on it falls toward g. That feedback makes ever-larger ownership self-limiting instead of self-reinforcing.

The net: ψ* settles at a feasible share — meaningful ownership for citizens, with the large majority of the market still privately held and freely traded. The structural buyer is a **bounded** buyer by construction. If it weren't, the design wouldn't be feasible — which is exactly why the bound is load-bearing, not a footnote.

---

*Everything above is exactly what the engine computes, line for line. The rigor behind each number — the Mᵀ separation, the 20% spillover, the price-stability locus, the realizable returns, the bounded ownership share — is set out in the architecture paper (the mechanical design), the macroeconomic model, and the structural-buyer paper. But the mechanics themselves are just this: one growth-tied budget; four dials that size it and route it between a spendable dividend and a bounded, index-buying floor; with inflation and ownership both read off the back.*

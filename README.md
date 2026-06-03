# The Citizens Standard — Interactive Engine

An interactive model of **The Citizens Standard**, a constitutional monetary architecture that replaces central-bank discretion with three rules-based money-issuance channels and distributes every newly created dollar equally to all citizens.

Open `Citizens_Standard_Engine.html` in any browser. No build step, no dependencies, no server — everything runs client-side.

## What it does

The engine projects one citizen's lifetime outcome under the framework and compares it to what people actually retire with today. You set the three issuance channels and the macro assumptions; it shows:

- the **Stable Floor** — the locked, equity-invested capital account every citizen accrues — at the end of the horizon;
- the **implied inflation** the configuration produces (derived from the channels, not assumed);
- a side-by-side **comparison** against median and average US retirement outcomes and seven alternative monetary/transfer systems;
- **stress tests** against historical bad sequences (Great Depression, 1970s stagflation, 2000s lost decade).

## The three issuance channels

Three rules, no discretion. Each is a slider.

- **K1 — Citizenship dividend.** A one-time deposit at birth equal to 2.5% of GDP per capita, paid into the citizen's Stable Floor.
- **K2 — Growth channel.** New money matched to real economic growth: `capture% × real growth × M2` (on prior-year M2). At 100% capture, the money supply grows at exactly the real output rate — the definition of price stability. Below 100%, money grows slower than output and the price level falls.
- **K3 — Citizen dividend.** A flat percentage of M2 issued each year and paid out as a monthly cash dividend. This is the only channel that pushes total issuance *above* real growth, so it is the only source of inflation.

## The three modes

The mode buttons are presets over those channels. Defaults: 2% real growth, 0.5% population growth, 6.5% real equity return (Shiller long-run), 65-year horizon, and $22.7T M2 / $30.7T GDP / 342M population at launch.

| Mode | K2 | K3 | Implied inflation | Stable Floor at 65 | Character |
|------|-----|-----|-------------------|--------------------|-----------|
| **A — Rising real wages** | 12.5% | 0 | ≈ −1.7% (deflation) | ≈ $360K | Smallest floor, but every dollar of cash and wages gains ~+217% real purchasing power over a lifetime |
| **B — Stable prices** | 100% | 0 | ≈ 0% | ≈ $1.87M | Full-rate issuance; largest locked floor; price-neutral |
| **C — Monthly dividend** | 12.5% | 4% | ≈ +2.3% (inflation) | ≈ $358K | Same floor as A, plus a ~$230/month citizen dividend; mild inflation erodes cash |

Move any slider and the mode switches to **Custom**.

Two properties the engine is built to make obvious:

**1. Inflation is derived, not dialed.** It equals total new money (issuance ÷ M2) minus real growth. K1 and K2 can at most match real growth (Mode B → price stability) or fall short of it (Mode A → deflation). Only K3 lifts issuance above real growth, so only K3 creates inflation. Raise the K3 slider and watch the implied-inflation readout climb; set K2 to 100% with K3 at zero and it sits at zero.

**2. The Stable Floor is inflation-neutral.** It is invested in equities — a real asset earning a real return — so its real value does not move with the price level. That is why raising K3 (which only changes inflation and funds the dividend) leaves the K1+K2-funded floor unchanged. Modes A and C therefore share the same floor; what differs is whether the "extra" arrives as deflationary purchasing-power gains (A) or as a monthly dividend (C). Mode A's payoff is not a bigger floor — it is that money held *outside* the floor gains value.

## The comparison

The **vs real outcomes** tab pits the configured cohort against eight reference points: the Fed status quo (median 401(k) + Social Security), the Chicago Plan, Friedman's k-rule, Bitcoin / fixed supply, an Alaska PFD-style dividend, a tax-funded UBI, and an MMT jobs guarantee. Scenarios let you swap the median 401(k) for the average, or apply the projected ~23% Social Security trust-depletion cut.

Three fair-comparison rules are built in:

- **Social Security is in every row.** None of these proposals — the Citizens Standard included — abolishes SS, so crediting only some systems with it would distort the result. Every row carries the same SS benefit; the differences reflect what each system adds on top.
- **Transfer figures are face-value.** UBI and Alaska-style dividends are shown without netting out the inflation those transfers would themselves generate. The Citizens Standard dividend is already in real terms (its inflation is derived here).
- **A jobs guarantee is a wage floor, not retirement wealth.** The MMT row does not count lifetime wages as an accumulated stock, since workers earn wages under every system.

## Tabs

- **Stable Floor growth** — the account balance over the horizon.
- **M2 trajectory** — the money-supply path.
- **K1 / K2 / K3 over time** — issuance by channel.
- **vs real outcomes** — the comparison above.
- **Inflation paths** — the derived Citizens Standard rate vs each system's price-level behavior.
- **Stress test** — outcomes if a historical bad sequence strikes during the working life.

## What this is *not*

The engine is for building intuition, not for policy calibration. Specifically:

- It is a **forward projection** of one hypothetical cohort under constant macro assumptions — not the empirical historical reconstruction in Paper 2, which produces the ≈$1.32M Mode B figure from the actual earliest cohort.
- Inflation is a **quantity-theory approximation** (issuance minus real growth), not the full price-level-targeting formula in the papers; K3 is modeled as a flat percentage of M2.
- It models the three **base** modes only. The full framework also defines **Mode Ω** (an adaptive mode that shifts targets with conditions) and **Mode T** (the transition mode with the KT debt-retirement channel), which are covered in the papers.
- Equity returns use a single base-case real rate except on the Stress tab; the main projection does not model sequence-of-returns risk, mode transitions, or emergency tools.

## The papers

This engine accompanies the four-paper Citizens Standard series by **Neo-Solon**:

1. **Architecture** — the constitutional framework and the K1/K2/K3 and mode system.
2. **Empirical / Counterfactual** — the historical reconstruction and Stable Floor results.
3. **Transition** — moving from the current system, including debt retirement.
4. **Statutory** — model legislative text.

*Available on SSRN — add links here.*

## License

Open-source and free to share, embed, or adapt.

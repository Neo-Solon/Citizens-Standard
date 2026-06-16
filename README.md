# The Citizens Standard — Interactive Engine

An interactive model of **The Citizens Standard**, a constitutional monetary architecture that replaces central-bank discretion with four rules-based money-issuance channels and distributes every newly created dollar equally to all citizens.

Open `Citizens_Standard_Engine.html` in any browser, or go to https://neo-solon.github.io/Citizens-Standard/Citizens_Standard_Engine.html. No build step, no dependencies, no server — everything runs client-side.

## What it does

The engine projects one citizen's lifetime outcome under the framework and compares it to what people actually retire with today. You set the four issuance channels and the macro assumptions; it shows:

- the **Stable Floor** — the locked, equity-invested capital account every citizen accrues — at the end of the horizon;
- the **implied inflation** the configuration produces (derived from the channels, not assumed);
- a side-by-side **comparison** against median and average US retirement outcomes and seven alternative monetary/transfer systems;
- **stress tests** against historical bad sequences (Great Depression, 1970s stagflation, 2000s lost decade).

## The four issuance channels

Four rules, no discretion. Each is a slider.

- **K1 — Citizenship dividend.** A one-time deposit at birth equal to 2.5% of GDP per capita, paid into the citizen's Stable Floor.
- **K2 — Growth channel.** New money matched to real economic growth: `capture% × real growth × M2` (on prior-year M2). At 100% capture, the money supply grows at exactly the real output rate — the definition of price stability. Below 100%, money grows slower than output and the price level falls.
- **K3 — Citizen dividend (κ_d split).** A price-neutral *reallocation* of the K2 growth budget: the κ_d split sets how much of that budget locks into Stable Floors versus pays out as a monthly cash dividend. It moves money between locked and spendable without changing the total, so it does not move the price level.
- **KI — Inflation-gap channel.** A flat percentage of M2 issued *above* the growth line. This is the only channel that pushes total issuance above real growth, so it is the only source of inflation — and the channel that funds the Mode C monthly dividend.

## The three modes

The mode buttons are presets over those channels. Defaults: 2% real growth, 0.5% population growth, 6.5% real equity return (Shiller long-run), 65-year horizon, and $22.4T M2 / $30.8T GDP / 342M population at launch.

| Mode | K2 | KI | Implied inflation | Character |
|------|-----|-----|-------------------|-----------|
| **A — Rising real wages** | 12.5% | off | ≈ −1.6% (deflation) | Smallest floor, but every dollar of cash and wages gains real purchasing power over a lifetime |
| **B — Stable prices** | 100% | off | ≈ 0% | Full-rate issuance; largest locked floor; price-neutral |
| **C — Modest inflation** | 100% | 2% | ≈ +2.0% (inflation) | Same floor as B, plus a KI-funded monthly dividend; mild inflation erodes cash held outside the floor |

Each mode's **Stable Floor at 65** is computed live by the engine from the macro assumptions above — open it for the current figure under each mode rather than relying on a cached number here. Move any slider and the mode switches to **Custom**. (The κ_d split between K2 and K3 is available in every mode and is price-neutral.)

Two properties the engine is built to make obvious:

**1. Inflation is derived, not dialed.** It equals total new money (issuance ÷ M2) minus real growth. K1 and K2 can at most match real growth (Mode B → price stability) or fall short of it (Mode A → deflation), and the κ_d split (K3) only reallocates — so none of them move the price level. Only **KI** lifts issuance above real growth, so only KI creates inflation. Raise the KI slider and watch the implied-inflation readout climb; set K2 to 100% with KI off and it sits at zero.

**2. The Stable Floor is inflation-neutral.** It is invested in equities — a real asset earning a real return — so its real value does not move with the price level. That is why turning on **KI** (which changes inflation and funds the dividend) leaves the K1+K2-funded floor unchanged. Modes B and C therefore share the same floor; what differs is that Mode C runs a positive inflation gap whose issuance arrives as a monthly dividend, while Mode B holds the price level flat. Mode A's payoff is not a bigger floor — it is that money held *outside* the floor gains value as prices fall.

## The comparison

The **vs real outcomes** tab pits the configured cohort against eight reference points: the Fed status quo (median 401(k) + Social Security), the Chicago Plan, Friedman's k-rule, Bitcoin / fixed supply, an Alaska PFD-style dividend, a tax-funded UBI, and an MMT jobs guarantee. Scenarios let you swap the median 401(k) for the average, or apply the projected ~23% Social Security trust-depletion cut.

Three fair-comparison rules are built in:

- **Social Security is in every row.** None of these proposals — the Citizens Standard included — abolishes SS, so crediting only some systems with it would distort the result. Every row carries the same SS benefit; the differences reflect what each system adds on top.
- **Transfer figures are face-value.** UBI and Alaska-style dividends are shown without netting out the inflation those transfers would themselves generate. The Citizens Standard dividend is already in real terms (its inflation is derived here).
- **A jobs guarantee is a wage floor, not retirement wealth.** The MMT row does not count lifetime wages as an accumulated stock, since workers earn wages under every system.

## Tabs

- **Stable Floor growth** — the account balance over the horizon.
- **M2 trajectory** — the money-supply path.
- **K1 / K2 / K3 / KI over time** — issuance by channel.
- **vs real outcomes** — the comparison above.
- **Inflation paths** — the derived Citizens Standard rate vs each system's price-level behavior.
- **Stress test** — outcomes if a historical bad sequence strikes during the working life.

## What this is *not*

The engine is for building intuition, not for policy calibration. Specifically:

- It is a **forward projection** of one hypothetical cohort under constant macro assumptions — not the empirical historical reconstruction in Paper 2, whose deterministic Mode B anchor (~$1.3M) comes from the actual earliest cohort.
- Inflation is a **quantity-theory approximation** (issuance minus real growth), not the full price-level-targeting formula in the papers; KI is modeled as a flat percentage of M2 issued above the growth line.
- It models the three **base** modes only. The full framework also defines **Mode Ω** (an adaptive mode that shifts targets with conditions) and **Mode T** (the transition mode with the KT debt-retirement channel), which are covered in the papers.
- Equity returns use a single base-case real rate except on the Stress tab; the main projection does not model sequence-of-returns risk, mode transitions, or emergency tools.

## The papers

This engine accompanies the eight-paper Citizens Standard series by **Neo-Solon** (replication archives in this repository under `Citizens-Standard-replication/`). The papers are the figures of record; where the engine's illustrative defaults differ from the calibrated values in the papers, the papers govern.

1. **Architecture** — the constitutional framework and the K1/K2/K3/KI and mode system. *(SSRN 6702518)*
2. **Counterfactual / Empirical** — the historical reconstruction and Stable Floor results. *(SSRN 6735078)*
3. **Transition** — moving from the current system, including debt retirement. *(SSRN 6810741)*
4. **Statutory** — model legislative text. *(SSRN 6873798)*
5. **Macroeconomic Model** — the dynamic model and determinacy results. *(SSRN 6939418)*
6. **Full-Reserve Banking and the Two-Circuit System** — inside money, intermediation, and payment-credit separation. *(SSRN 6939498)*
7. **External Interoperability** — the EQUA-class settlement layer and common anchor. *(SSRN 6939600)*
8. **Structural Buyer** — the structural-buyer mechanism. *(SSRN 6945320)*

## License

Open-source and free to share, embed, or adapt.

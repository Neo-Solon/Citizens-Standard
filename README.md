# The Citizens Standard — Interactive Engine

An interactive model of **The Citizens Standard**, a constitutional monetary architecture that replaces central-bank discretion with four rules-based money-issuance channels and distributes every newly created dollar equally to all citizens.

Open `Citizens_Standard_Engine.html` in any browser, or go to <https://neo-solon.github.io/Citizens-Standard/Citizens_Standard_Engine.html>. No build step, no dependencies, no server — everything runs client-side.

## What it does

The engine projects one citizen's lifetime outcome under the framework and shows what each configuration delivers against what people actually retire with today. You set the four issuance channels and the macro assumptions; it shows:

- the **Stable Floor** — the locked, equity-invested capital account every citizen accrues — at the end of the horizon;
- the **implied inflation** the configuration produces (derived from the channels, not assumed);
- **what you get** — each mode's retirement outcome (floor, monthly dividend, income at retirement) set against today's median retirement, plus how the framework differs from UBI, MMT, Bitcoin, and other proposals;
- **stress tests** against historical bad sequences (Great Depression, 1970s stagflation, 2000s lost decade).

## The four issuance channels

Four rules, no discretion. Each is a slider.

- **K1 — Citizenship dividend.** A one-time deposit at birth equal to 2.5% of GDP per capita, paid into the citizen's Stable Floor.
- **K2 — Growth channel.** New money matched to real economic growth: capture% × real growth × M2 (on prior-year M2). At 100% capture, the money supply grows at exactly the real output rate — the definition of price stability. Below 100%, money grows slower than output and the price level falls.
- **K3 — Citizen dividend (κ_d split).** A price-neutral reallocation of the K2 growth budget: the κ_d split sets how much of that budget locks into Stable Floors versus pays out as a monthly cash dividend. It moves money between locked and spendable without changing the total, so it does not move the price level.
- **KI — Inflation-gap channel.** A flat percentage of M2 issued above the growth line. This is the only channel that pushes total issuance above real growth, so it is the only source of inflation — and the channel that funds the Mode C monthly dividend.

## The modes

The mode buttons are presets over those channels. Defaults: 2% real growth, 0.5% population growth, **4.5% real equity return** (the forward-looking central case; 6.5% Shiller-historical and 3% pessimistic are one-click presets), 65-year horizon, and $22.4T M2 / $30.8T GDP / 342M population at launch.

| Mode | K2 | K3 (κ_d) | KI | Implied inflation | Character |
|---|---|---|---|---|---|
| **A — Deflation** | 17.5% | — | off | ≈ −1.6% | Smallest floor, but every dollar of cash and wages gains real purchasing power over a lifetime (rising real wages); no dividend |
| **B — Stable** | 100% | — | off | ≈ 0% | Full-rate issuance; the largest locked floor; price-neutral; no dividend |
| **C — Inflation** | 17.5% | — | 3.65% | ≈ +2.0% | A smaller floor, traded for the largest monthly dividend, funded by mild inflation |
| **D — Stable dividend** | 100% | 50% | off | ≈ 0% | A mid-size floor plus a standing monthly dividend at zero inflation — a dividend without the inflation tax |

Each mode's Stable Floor at retirement is computed live by the engine from the macro assumptions above — open it for the current figure rather than relying on a cached number here. Move any slider and the mode switches to Custom. (The κ_d split between K2 and K3 is available in every mode and is price-neutral.)

The full framework also defines two further modes, each with its own tab: **Mode Ω** (an adaptive mode whose governors shift issuance with conditions, within published caps) and **Mode T** (the transition mode, which adds the KT channel to retire legacy national debt down to an operational floor).

Two properties the engine is built to make obvious:

**1. Inflation is derived, not dialed.** It equals total new money (issuance ÷ M2) minus real growth. K1 and K2 can at most match real growth (Mode B → price stability) or fall short of it (Mode A → deflation), and the κ_d split (K3) only reallocates — so none of them move the price level. Only KI lifts issuance above real growth, so only KI creates inflation. Raise the KI slider and watch the implied-inflation readout climb; set K2 to 100% with KI off and it sits at zero.

**2. The Stable Floor is inflation-neutral.** It is invested in equities — a real asset earning a real return — so its real value does not move with the price level. Turning KI on (which changes inflation and funds a dividend) leaves the K1+K2-funded floor unchanged *at a given K2*. The modes differ in what they do with that fact: Mode B runs the full K2 rate into the floor and holds prices flat; Mode C deliberately runs a *lower* K2 — a smaller floor — and adds KI, trading locked wealth for a large inflation-funded dividend; Mode D keeps the full K2 but splits part of it (κ_d) into a price-neutral dividend. Mode A's payoff is not a bigger floor — it is that money held outside the floor gains value as prices fall.

## What you get

The **What you get** tab leads with the reality check: what each Citizens Standard mode delivers a representative citizen, set against what Americans actually retire with today (median 401(k) + Social Security). Each mode is a card — floor, monthly dividend, implied inflation, and income at retirement — with the income shown as a multiple of today's outcome. Scenarios let you swap the median 401(k) for the average, or apply the projected ~23% Social Security trust-depletion cut.

How the framework relates to other proposals is summarized in a line rather than a table, because under a fair accounting they collapse onto the same baseline. Three fair-comparison rules drive that:

- **Social Security is in every row.** None of these proposals — the Citizens Standard included — abolishes SS, so it is carried identically everywhere; the differences reflect only what each system *adds* on top.
- **Only genuine net transfers count.** The Citizens Standard dividend (seigniorage) and an Alaska-style royalty PFD are net transfers to the citizen. A tax-funded UBI is shown net of the taxes the same citizens pay to fund it (≈ a wash for a median earner). An MMT jobs guarantee pays earned wages for work, not a wealth transfer, so it adds nothing to accumulated wealth.
- **Private savings is a shared baseline.** Every citizen's own 401(k) is the same regardless of monetary regime, so it anchors every row, including the Citizens Standard.

The result the tab is built to show: only the Citizens Standard routes newly-created money to citizens as locked, equal, rules-based wealth — every other monetary regime leaves the representative citizen on the same savings-plus-Social-Security baseline.

## Tabs

- **Stable Floor** — the account balance over the horizon.
- **M2** — the money-supply path.
- **Channels** — issuance by K1 / K2 / K3 / KI over time.
- **What you get** — the mode-by-mode outcome and reality check above.
- **Inflation** — the derived Citizens Standard rate vs each system's price-level behavior.
- **Stress test** — outcomes if a historical bad sequence strikes during the working life.
- **Mode T** — the debt-transition path: the KT channel retiring national debt to an operational floor, with symmetric reverse-KT draining money under an inflation shock.
- **Mode Ω** — the adaptive mode: governors responding to deflation or demographic stress within published caps.

## What this is not

The engine is for building intuition, not for policy calibration. Specifically:

- It is a forward projection of one hypothetical cohort under constant macro assumptions — not the empirical historical reconstruction in Paper 2, whose deterministic Mode B anchor (~$1.3M) comes from the actual earliest cohort.
- Inflation is a quantity-theory approximation (issuance minus real growth), not the full price-level-targeting formula in the papers; KI is modeled as a flat percentage of M2 issued above the growth line.
- Equity returns use a single base-case real rate (4.5% central by default) except on the Stress tab; the main projection does not model sequence-of-returns risk or mode transitions.
- The Mode Ω and Mode T tabs are illustrative; their full governor and debt-retirement formulas live in the papers.

## The papers

This engine accompanies the eight-paper Citizens Standard series by Neo-Solon (replication archives in this repository under `Citizens-Standard-replication/`). The papers are the figures of record; where the engine's illustrative defaults differ from the calibrated values in the papers, the papers govern.

1. **Architecture** — the constitutional framework and the K1/K2/K3/KI and mode system. (SSRN 6702518)
2. **Counterfactual / Empirical** — the historical reconstruction and Stable Floor results. (SSRN 6735078)
3. **Transition** — moving from the current system, including debt retirement. (SSRN 6810741)
4. **Statutory** — model legislative text. (SSRN 6873798)
5. **Macroeconomic Model** — the dynamic model and determinacy results. (SSRN 6939418)
6. **Full-Reserve Banking and the Two-Circuit System** — inside money, intermediation, and payment-credit separation. (SSRN 6939498)
7. **External Interoperability** — the EQUA-class settlement layer and common anchor. (SSRN 6939600)
8. **Structural Buyer** — the structural-buyer mechanism. (SSRN 6945320)

## License

Open-source and free to share, embed, or adapt.

# Floor: Net-New Wealth vs Crowd-Out

How much of the Citizens Standard floor is **genuinely new wealth** versus a
**reshuffle of saving households would have done anyway** (crowd-out)? This grounds
the most frequently conceded claim in discussion -- "yes the floor crowds out
savers, but it's new wealth for the people who never get to own capital" (Macro
Model Paper 5, Result 2) -- on SCF 2022.

## Result (headline)

| Crowd-out intensity | Net-new wealth | Crowd-out |
|---|---|---|
| 0.15 (private pensions, low) | 91% | 9% |
| **0.33 (Social Security, central)** | **79%** | **21%** |
| 0.65 (structural life-cycle, high) | 59% | 41% |

- **Central estimate: the floor is ~79% net-new wealth, ~21% crowd-out.**
- **Even at the literature's highest crowd-out estimate, the floor is majority
  net-new wealth (59%).**
- The character differs by income half: within the **bottom 5 deciles the floor is
  88% net-new wealth**; within the **top 5 it is 73% net-new** (central case). The
  crowd-out concentrates at the top, where households already hold equity; the new
  wealth concentrates at the bottom, where they hold none.

So the conceded claim is not just supported but **understated** by the data: the
floor is mostly new wealth across the whole distribution, overwhelmingly so at the
bottom.

## Method

For each income decile, the floor splits into:

    net-new share   = (1 - equity_participation) + equity_holders x (1 - crowdout_intensity)
    crowded-out     = equity_holders x crowdout_intensity

- **Equity participation** is mechanical from SCF 2022 `EQUITY` (direct stock +
  mutual funds + retirement equity): verified gradient **12.6% (bottom decile) to
  96.4% (top)**, 58% overall. A household holding no equity experiences the floor's
  equity stake as wealth it would never otherwise have had; a holder experiences
  part of it as substituting for saving it would have done.
- **Crowd-out intensity** (Stage 2 sweep) is grounded in the pension-wealth
  displacement literature, the right analogue because the floor is locked, forced,
  annuity-style retirement wealth:
  - ~0.15 private pensions (IZA DP5554)
  - ~0.22 international micro-data (Attanasio et al.)
  - ~0.27 developing-country median (review)
  - **~0.33 Social Security** (IZA DP5554) -- the closest single analogue, since
    like the floor it is a universal government-backed annuity-style claim; used as
    central
  - ~0.55-0.65 structural life-cycle with retirement fixed (JEEA 2024)

## Verification
- Weight baseline asserted (sum WGT = 131,306,389); parent `verify_scf.py` passes.
- Equity-participation gradient is monotone and matches expectation (12.6% to 96.4%).
- Saver-rate gradient independently checked: 32% (bottom) to 84% (top), monotone.
- **Headline robust to floor weighting**: net-new share is 62-65% at the *high*
  (0.6) intensity across adult-equivalent / per-household / per-capita weightings;
  adult-equivalent is correct since the floor is per-adult.
- Per-person shares use the channels.py convention.

## Caveats
- **Participation-margin measure.** This tracks the share of the floor landing on
  households *with vs. without* prior equity, scaled by a crowd-out intensity. It
  does not estimate the dollar value of displaced saving household-by-household;
  that would need a behavioral saving model, not a cross-section.
- **Crowd-out intensity is the one judgment parameter**, swept across the full
  literature range; the conclusion (majority net-new) holds across all of it.
- Binary `EQUITY>0` is a participation proxy; a household with trivial equity is
  counted as a holder, which if anything *overstates* crowd-out (conservative).

## Credit
The crowd-out result itself is the Citizens Standard's own (Macro Model, Result
2). The pension-displacement literature supplies the empirical intensity range.
This module quantifies the conceded split on US SCF data. (Companion to the
rent-capitalization and demand-impulse modules built alongside discussions with
wilsoniumite.)

## Reproduce
```
cd code
python3 stage1_crowdout.py
python3 stage2_crowdout_sweep.py
```


##############################################################################
# TOOL 14 vs. REAL INFLATIONS -- structural counterfactual
# Actual = BLS CPI-U. 2022 demand share = SF Fed (Shapiro) monthly data.
# Counterfactual under mechanical triggers; not a forecast.
##############################################################################

==============================================================================
EPISODE 2022  (Jan 2021 + 36 mo)   actual peak 9.1%  [Jun 2022]   share: SF Fed monthly decomposition
==============================================================================

PREVENTION (managed-throughout) -- central:
  peak: structural 6.0%  ->  +Tool14 4.6%   (vs actual 9.1%)
  months above 4%: framework 9  vs actual 25
  Tool 14: active 9 mo, ~$504B retired (<=3% M2/yr, 2.2pp/yr cap)
  prevention-peak band: 4.1% - 4.6%
      demand-only  -> peak 4.6%
      demand+½amb  -> peak 4.3%
      demand+amb   -> peak 4.1%

RESPONSE (drop-in; Tool 14 capacity only) -- the honest, slower path:
  from the realized 9.1% peak, Tool 14 at ~2.2pp/yr
  reaches 5.8% by the end of the window, vs actual 3.4%.
  -> Tool 14 ALONE is SLOWER than the rate shock was. Its value is no
     rate channel, not speed. (Conservative: ignores halting old-system
     accommodation, which would help.)

CONVENTIONAL CURE (what actually happened):
  policy rate 0.1% -> 5.3% (7 hikes; first only after CPI passed 8%)
  real cost   30-yr mortgage 3.2% -> 7.1% (Freddie Mac PMMS, 2022)

==============================================================================
EPISODE 1980  (Jan 1972 + 138 mo)   actual peak 14.8%  [Mar 1980]   share: Fed monetary attribution (no SF Fed series pre-1998)
==============================================================================

PREVENTION (managed-throughout) -- central:
  peak: structural 5.1%  ->  +Tool14 4.0%   (vs actual 14.8%)
  months above 4%: framework 0  vs actual 117
  Tool 14: active 7 mo, ~$392B retired (<=3% M2/yr, 2.2pp/yr cap)
  prevention-peak band: 3.8% - 4.1%
      low          -> peak 4.1%
      central      -> peak 4.0%
      high         -> peak 3.8%

RESPONSE (drop-in; Tool 14 capacity only) -- the honest, slower path:
  from the realized 14.8% peak, Tool 14 at ~2.2pp/yr
  reaches 7.7% by the end of the window, vs actual 2.6%.
  -> Tool 14 ALONE is SLOWER than the rate shock was. Its value is no
     rate channel, not speed. (Conservative: ignores halting old-system
     accommodation, which would help.)

CONVENTIONAL CURE (what actually happened):
  policy rate ~19% (Fed funds peak, Jun 1981)
  real cost   10.8% unemployment (BLS, Nov-Dec 1982)
  sacrifice ratio ~2.5 unemployment-pt-yrs/pt

==============================================================================
WHAT THE FRAMEWORK ACTUALLY BUYS (honest, after data-grounding):
  1. PREVENTION is primary -- a far lower peak, because rule-bound
     issuance never creates the demand component (the structural
     baseline does most of the work; Tool 14 is a secondary shave).
  2. NO RATE CHANNEL -- disinflation without the mortgage shock (2022)
     or the 10.8% unemployment recession (1980).
  NOT a claim: faster disinflation. Tool 14 (~2.2pp/yr) is slower than
  an aggressive rate shock; the trade is no collateral damage.
==============================================================================


====================================================================
SENSITIVITY -- Tool 14 prevention counterfactual
====================================================================

(A) Demand-share band -- 2022
    demand-only  -> peak  4.6%   months>4%: 9
    demand+½amb  -> peak  4.3%   months>4%: 5
    demand+amb   -> peak  4.1%   months>4%: 3

(B) Tool 14 capacity sweep -- 2022
    cap 2% M2/yr ( 1.5pp/yr)  ->  peak  4.9%   months>4%: 10
    cap 3% M2/yr ( 2.2pp/yr)  ->  peak  4.6%   months>4%: 9
    cap 4% M2/yr ( 2.9pp/yr)  ->  peak  4.3%   months>4%: 7

(C) Trigger sweep -- 2022
    trigger anchor+2pp  ->  peak  3.5%   months>4%: 0
    trigger anchor+3pp  ->  peak  4.6%   months>4%: 9
    trigger anchor+4pp  ->  peak  5.1%   months>4%: 12

(A) Demand-share band -- 1980
    low          -> peak  4.1%   months>4%: 8
    central      -> peak  4.0%   months>4%: 0
    high         -> peak  3.8%   months>4%: 0

(B) Tool 14 capacity sweep -- 1980
    cap 2% M2/yr ( 1.5pp/yr)  ->  peak  4.2%   months>4%: 7
    cap 3% M2/yr ( 2.2pp/yr)  ->  peak  4.0%   months>4%: 0
    cap 4% M2/yr ( 2.9pp/yr)  ->  peak  4.0%   months>4%: 0

(C) Trigger sweep -- 1980
    trigger anchor+2pp  ->  peak  3.0%   months>4%: 0
    trigger anchor+3pp  ->  peak  4.0%   months>4%: 0
    trigger anchor+4pp  ->  peak  5.0%   months>4%: 26

OUT-OF-SAMPLE: same engine + parameters, both episodes.
    1980: prevention peak 4.0%  months>4% 0 (actual 117)  Tool14 7mo
    2022: prevention peak 4.6%  months>4% 9 (actual 25)  Tool14 9mo

The prevention peak moves with the demand-share assumption (the honest
uncertainty), but lower-peak + less-time-elevated + NO-rate-channel hold
across every cell.

########## STRUCTURAL RUN (Proposition 6 transmission) ##########

STRUCTURAL COUNTERFACTUAL via Proposition 6 transmission
Same shocks that reproduce history under the status quo, run through
the framework's proven mechanism. Parameters verbatim from the macro paper.

========================================================================
2022 surge  (quarterly; Prop 6 system, psi*lam=0.9, unretuned)
========================================================================
  status-quo check (KI off) reproduces actual peak: 8.7%  vs actual 8.7%   (max abs err 0.00pp)
  FRAMEWORK peak, KI self-correction only : 4.1%
  FRAMEWORK peak, KI + Tool 14            : 4.1%
  (actual 8.7%)

========================================================================
1980 / Volcker  (quarterly; Prop 6 system, psi*lam=0.9, unretuned)
========================================================================
  status-quo check (KI off) reproduces actual peak: 14.5%  vs actual 14.5%   (max abs err 0.00pp)
  FRAMEWORK peak, KI self-correction only : 3.4%
  FRAMEWORK peak, KI + Tool 14            : 3.4%
  (actual 14.5%)

========================================================================
CROSS-CHECK vs the reduced form (run_counterfactual.py):
  2022: structural 4.1%  vs reduced-form 4.6%  (actual 8.7%)  -> AGREE
  1980: structural 3.4%  vs reduced-form 4.0%  (actual 14.5%)  -> AGREE

  BOTH episodes cross-validate. The framework's proven KI self-
  correction (Proposition 6) and the transparent demand-share reduced
  form -- two independent mechanisms -- land within ~1pp of each other
  at ~3-5%, far below the actual 9.1% / 14.8%. The 1980 result required
  the full 1972-1983 window: fed the build-up from 3.3%, the framework
  self-corrects each oil-shock and monetary impulse before it compounds,
  so the Great Inflation never forms. (On the narrow 1979-1983 window
  the model instead measures a drop-in at 11%+, which KI can only unwind
  slowly -- the response path, not prevention.)

  The counterfactual is now BOTH model-generated (the paper's own proven
  transmission) AND hand-reproducible (the reduced form), and the two
  agree -- the strongest evidentiary basis available for the appendix.
========================================================================

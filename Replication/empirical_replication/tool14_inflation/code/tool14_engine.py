"""
tool14_engine.py
================
Structural framework response to a historical inflation shock. Paper-grade
mechanism (not the interactive engine's reduced form). Two DISTINCT
counterfactuals, kept separate because they answer different questions:

  PREVENTION (managed-throughout)  -- the headline.
    "If the framework had been the system all along, how high would inflation
    have gotten?" The rule-bound issuance never creates the DEMAND-driven share
    and KI->0 is automatic, so only the supply share passes through; Tool 14
    then shaves what remains:
        structural[t] = anchor + (1 - demand_share[t]) * (actual[t] - anchor)
    demand_share[t] is the SF Fed monthly decomposition for 2022 (not fitted);
    for 1980 it is the Fed's monetary attribution (no SF Fed series pre-1998).

  RESPONSE (drop-in)  -- the honest, conservative secondary.
    "Given inflation is ALREADY at the peak (the old system made it), how fast
    can the framework bring it down?" Only Tool 14 acts, at its real capacity
    (~2.2pp/yr). This is deliberately SLOWER than an aggressive rate shock --
    Tool 14 is not a fast-disinflation tool. Its value is no rate channel, not
    speed. (Conservative: ignores that the framework would also halt the old
    system's ongoing accommodation, which would disinflate somewhat faster.)

What the framework actually buys, then, is (1) a far lower peak via prevention,
and (2) disinflation with NO interest-rate channel -- no mortgage shock, no
engineered recession -- NOT faster disinflation than rate hikes.
"""

from data import (ANCHOR_CPI, TRIGGER_OVER, TOOL14_MAX_PULL_PP,
                  TOOL14_CAP_PCT, M2_LEVEL)

MONTHLY_PULL = TOOL14_MAX_PULL_PP / 12.0   # pp of disinflation per active month


def _share_series(actual, share):
    """`share` may be a float (constant) or callable(month_index)->float."""
    if callable(share):
        return [share(t) for t in range(len(actual))]
    return [float(share)] * len(actual)


def structural_path(actual, share):
    """Prevention baseline: only the non-demand (supply) share passes through."""
    sh = _share_series(actual, share)
    return [ANCHOR_CPI + (1.0 - sh[t]) * max(0.0, actual[t] - ANCHOR_CPI)
            for t in range(len(actual))]


def prevention_path(actual, share):
    """Structural baseline + cumulative, self-throttling Tool 14 shave.
    Returns (path, struct, months_active, money_retired_usd)."""
    struct = structural_path(actual, share)
    trig = ANCHOR_CPI + TRIGGER_OVER
    out, active, cum = [], 0, 0.0
    for s in struct:
        eff = s - cum
        if eff > trig:
            cum += MONTHLY_PULL
            active += 1
            eff = s - cum
        out.append(max(ANCHOR_CPI, eff))
    retired = active * (TOOL14_CAP_PCT * M2_LEVEL / 12.0)
    return out, struct, active, retired


def response_path(actual):
    """Drop-in: track the realized rise to the peak, then disinflate ONLY at
    Tool 14's capacity (~2.2pp/yr). Honestly slower than the actual recovery."""
    pk = actual.index(max(actual))
    out = list(actual[:pk + 1])
    cur = actual[pk]
    for _ in range(pk + 1, len(actual)):
        cur = max(ANCHOR_CPI, cur - MONTHLY_PULL)
        out.append(cur)
    return out


def _months_above(path, level):
    return sum(1 for v in path if v > level)


def summarize(actual, share, elevated=4.0):
    prev, struct, active, retired = prevention_path(actual, share)
    resp = response_path(actual)
    return {
        "actual_peak":      max(actual),
        "struct_peak":      max(struct),
        "prevention_peak":  max(prev),
        "response_peak":    max(resp),
        "actual_above":     _months_above(actual, elevated),
        "prevention_above": _months_above(prev, elevated),
        "response_end":     resp[-1],
        "actual_end":       actual[-1],
        "months_active":    active,
        "money_retired_b":  retired / 1e9,
        "prevention": prev, "struct": struct, "response": resp,
    }

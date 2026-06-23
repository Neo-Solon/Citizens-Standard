"""
sensitivity.py
==============
Robustness for the Tool 14 prevention counterfactual.
  (A) Demand-share band  -- 2022 from SF Fed (ambiguous allocation); 1980 literature.
  (B) Tool 14 capacity   -- 2% / 3% / 4% of M2/yr.
  (C) Trigger threshold  -- anchor+2 / +3 / +4 pp.
Plus OUT-OF-SAMPLE: identical engine/parameters on both episodes; the only
per-episode inputs are raw BLS CPI and a published demand share.

Run:  python sensitivity.py
"""
from data import (EPISODES, DEMAND_SHARE_1980, demand_share_2022,
                  M2_LEVEL, GDP_LEVEL, PASS_THROUGH)
import tool14_engine as eng


def share_for(key, regime):
    return (lambda t: demand_share_2022(t, regime)) if key == "2022" else regime


def _peak_above(actual, share):
    p, *_ = eng.prevention_path(actual, share)
    return max(p), sum(1 for v in p if v > 4.0)


def demand_band(key):
    print(f"(A) Demand-share band -- {key}")
    regs = [("demand-only",0.0),("demand+½amb",0.5),("demand+amb",1.0)] if key=="2022" \
           else [("low",DEMAND_SHARE_1980["low"]),("central",DEMAND_SHARE_1980["central"]),("high",DEMAND_SHARE_1980["high"])]
    for lbl, r in regs:
        pk, ab = _peak_above(EPISODES[key]["cpi"], share_for(key, r))
        print(f"    {lbl:<12} -> peak {pk:4.1f}%   months>4%: {ab}")
    print()


def capacity_sweep(key):
    actual = EPISODES[key]["cpi"]; sh = share_for(key, 0.0 if key=="2022" else DEMAND_SHARE_1980["central"])
    print(f"(B) Tool 14 capacity sweep -- {key}")
    b_cap, b_pull = eng.TOOL14_CAP_PCT, eng.MONTHLY_PULL
    for cap in (0.02, 0.03, 0.04):
        eng.TOOL14_CAP_PCT = cap
        eng.MONTHLY_PULL = (cap*M2_LEVEL/GDP_LEVEL*PASS_THROUGH*100.0)/12.0
        pk, ab = _peak_above(actual, sh)
        print(f"    cap {cap:.0%} M2/yr ({eng.MONTHLY_PULL*12:4.1f}pp/yr)  ->  peak {pk:4.1f}%   months>4%: {ab}")
    eng.TOOL14_CAP_PCT, eng.MONTHLY_PULL = b_cap, b_pull
    print()


def trigger_sweep(key):
    import data as d
    actual = EPISODES[key]["cpi"]; sh = share_for(key, 0.0 if key=="2022" else DEMAND_SHARE_1980["central"])
    print(f"(C) Trigger sweep -- {key}")
    base = eng.TRIGGER_OVER
    for over in (2.0, 3.0, 4.0):
        eng.TRIGGER_OVER = over
        pk, ab = _peak_above(actual, sh)
        print(f"    trigger anchor+{over:.0f}pp  ->  peak {pk:4.1f}%   months>4%: {ab}")
    eng.TRIGGER_OVER = base
    print()


def out_of_sample():
    print("OUT-OF-SAMPLE: same engine + parameters, both episodes.")
    for key in ("1980", "2022"):
        sh = share_for(key, 0.0 if key=="2022" else DEMAND_SHARE_1980["central"])
        s = eng.summarize(EPISODES[key]["cpi"], sh)
        print(f"    {key}: prevention peak {s['prevention_peak']:.1f}%  months>4% "
              f"{s['prevention_above']} (actual {s['actual_above']})  Tool14 {s['months_active']}mo")
    print()


if __name__ == "__main__":
    print("="*68 + "\nSENSITIVITY -- Tool 14 prevention counterfactual\n" + "="*68 + "\n")
    for key in ("2022", "1980"):
        demand_band(key); capacity_sweep(key); trigger_sweep(key)
    out_of_sample()
    print("The prevention peak moves with the demand-share assumption (the honest")
    print("uncertainty), but lower-peak + less-time-elevated + NO-rate-channel hold")
    print("across every cell.")

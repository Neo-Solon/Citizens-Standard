"""
run_counterfactual.py
=====================
Tool 14 inflation counterfactual, both episodes, both counterfactuals
(prevention / response), with the data-driven demand share for 2022 and the
sensitivity band. Reproduces every headline number in the paper's Tool 14
section. Deterministic.

Run:  python run_counterfactual.py
"""

from data import (EPISODES, POLICY, TOOL14_MAX_PULL_PP, demand_share_2022,
                  DEMAND_SHARE_1980)
from tool14_engine import summarize, response_path, _months_above, prevention_path


def share_for(key, regime):
    """2022 regime = ambiguous_weight (0/0.5/1.0); 1980 regime = constant share."""
    if key == "2022":
        return lambda t: demand_share_2022(t, regime)
    return regime


def bands(key):
    if key == "2022":
        return [("demand-only", 0.0), ("demand+½amb", 0.5), ("demand+amb", 1.0)]
    return [("low", DEMAND_SHARE_1980["low"]),
            ("central", DEMAND_SHARE_1980["central"]),
            ("high", DEMAND_SHARE_1980["high"])]


def central_regime(key):
    return 0.0 if key == "2022" else DEMAND_SHARE_1980["central"]


def episode_block(key):
    ep = EPISODES[key]; actual = ep["cpi"]; pol = POLICY[key]
    print("=" * 78)
    src = "SF Fed monthly decomposition" if key == "2022" else "Fed monetary attribution (no SF Fed series pre-1998)"
    print(f"EPISODE {key}  ({ep['start']} + {len(actual)} mo)   actual peak "
          f"{max(actual):.1f}%  [{pol['peak_when']}]   share: {src}")
    print("=" * 78)

    cen = summarize(actual, share_for(key, central_regime(key)))
    print(f"\nPREVENTION (managed-throughout) -- central:")
    print(f"  peak: structural {cen['struct_peak']:.1f}%  ->  +Tool14 "
          f"{cen['prevention_peak']:.1f}%   (vs actual {cen['actual_peak']:.1f}%)")
    print(f"  months above 4%: framework {cen['prevention_above']}  vs actual {cen['actual_above']}")
    # Robustness: sweep the elevated-inflation threshold so 4% is not load-bearing.
    # Both counts are computed directly from the real BLS CPI-U actual path and the
    # framework prevention path (no threshold is fitted or chosen to flatter).
    _prev_path, _, _, _ = prevention_path(actual, share_for(key, central_regime(key)))
    print(f"  months-above-threshold sweep (framework vs actual BLS CPI-U):")
    for _thr in (3.0, 3.5, 4.0, 4.5, 5.0):
        _fw = _months_above(_prev_path, _thr)
        _ac = _months_above(actual, _thr)
        print(f"      above {_thr:>3.1f}%:  framework {_fw:>2}  vs actual {_ac:>2}"
              f"   ({_ac - _fw:+d} mo fewer under the framework)")
    print(f"  Tool 14: active {cen['months_active']} mo, ~${cen['money_retired_b']:.0f}B retired "
          f"(<=3% M2/yr, {TOOL14_MAX_PULL_PP:.1f}pp/yr cap)")

    peaks = [(lbl, summarize(actual, share_for(key, r))["prevention_peak"]) for lbl, r in bands(key)]
    lo, hi = min(p for _, p in peaks), max(p for _, p in peaks)
    print(f"  prevention-peak band: {lo:.1f}% - {hi:.1f}%")
    for lbl, p in peaks:
        print(f"      {lbl:<12} -> peak {p:.1f}%")

    resp = response_path(actual)
    print(f"\nRESPONSE (drop-in; Tool 14 capacity only) -- the honest, slower path:")
    print(f"  from the realized {max(actual):.1f}% peak, Tool 14 at ~{TOOL14_MAX_PULL_PP:.1f}pp/yr")
    print(f"  reaches {resp[-1]:.1f}% by the end of the window, vs actual {actual[-1]:.1f}%.")
    print(f"  -> Tool 14 ALONE is SLOWER than the rate shock was. Its value is no")
    print(f"     rate channel, not speed. (Conservative: ignores halting old-system")
    print(f"     accommodation, which would help.)")

    print(f"\nCONVENTIONAL CURE (what actually happened):")
    print(f"  policy rate {pol['ffr']} ({pol['ffr_note']})")
    print(f"  real cost   {pol['cost']} ({pol['cost_note']})")
    if "sacrifice_ratio" in pol:
        print(f"  sacrifice ratio ~{pol['sacrifice_ratio']} unemployment-pt-yrs/pt")
    print()


def main():
    print("\n" + "#" * 78)
    print("# TOOL 14 vs. REAL INFLATIONS -- structural counterfactual")
    print("# Actual = BLS CPI-U. 2022 demand share = SF Fed (Shapiro) monthly data.")
    print("# Counterfactual under mechanical triggers; not a forecast.")
    print("#" * 78 + "\n")
    for key in ("2022", "1980"):
        episode_block(key)
    print("=" * 78)
    print("WHAT THE FRAMEWORK ACTUALLY BUYS (honest, after data-grounding):")
    print("  1. PREVENTION is primary -- a far lower peak, because rule-bound")
    print("     issuance never creates the demand component (the structural")
    print("     baseline does most of the work; Tool 14 is a secondary shave).")
    print("  2. NO RATE CHANNEL -- disinflation without the mortgage shock (2022)")
    print("     or the 10.8% unemployment recession (1980).")
    print("  NOT a claim: faster disinflation. Tool 14 (~2.2pp/yr) is slower than")
    print("  an aggressive rate shock; the trade is no collateral damage.")
    print("=" * 78)


if __name__ == "__main__":
    main()

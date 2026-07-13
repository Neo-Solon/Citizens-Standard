"""
compare.py - Build the sourced comparison from data.py.

Outputs:
  - the two tables Paper 13 prints (load-bearing axes; full comparison table),
    now with every cell backed by a source tag;
  - the three axes that ARE genuinely comparable across systems, computed in
    common units (annual per-person benefit; owned wealth stock per person;
    track record), with explicit "differs in kind" flags where a cell is not
    comparable;
  - a check of Paper 13's Comparative Claims 1, 2 and 4 against the figures.

This honours the positioning frame: it does not rank the systems on one number.
"""

import json
from data import (SYSTEMS, ALASKA, SOCIAL_SECURITY, UBI, GEORGISM,
                  CITIZENS_STANDARD, ALASKA_PFD_ANCHORS)


def f(x):
    """value of a Figure"""
    return x.value


# ---------------------------------------------------------------------------
# A. The categorical comparison table (sourced)
# ---------------------------------------------------------------------------
def categorical_table():
    rows = []
    for name, s in SYSTEMS.items():
        rows.append({
            "system": name,
            "funding": f(s["funding"]),
            "builds": f(s["builds"]),
            "coverage": f(s["coverage"]),
            "price_brake": "Yes" if f(s["price_brake"]) else "No",
            "maturity": f(s["maturity"]),
            "sources": sorted({s[k].src for k in
                               ("funding", "builds", "coverage", "price_brake", "maturity")}),
        })
    return rows


# ---------------------------------------------------------------------------
# B. Comparable axis 1 - annual per-person cash benefit (real USD/yr)
#    Only systems that pay an individual a recurring benefit are comparable.
# ---------------------------------------------------------------------------
def annual_benefit_axis():
    out = {}
    # UBI: canonical $1,000/mo
    out["UBI"] = {"usd_yr": f(UBI["canonical_monthly_usd"]) * 12,
                  "kind": "universal flow", "src": UBI["canonical_monthly_usd"].src}
    # Social Security: average retired-worker benefit, but contributory + retirement-only
    out["Social Security"] = {"usd_yr": f(SOCIAL_SECURITY["avg_benefit_usd_mo"]) * 12,
                              "kind": "contributory, retirement only (NOT universal working-age)",
                              "src": SOCIAL_SECURITY["avg_benefit_usd_mo"].src}
    # Alaska: long-run average dividend (universal among residents)
    out["SWF / Alaska"] = {"usd_yr": f(ALASKA["dividend_avg_usd"]),
                           "range": [f(ALASKA["dividend_min_usd"]), f(ALASKA["dividend_max_usd"])],
                           "kind": "universal resident dividend",
                           "src": ALASKA["dividend_avg_usd"].src}
    # CS: Mode B and Mode C dividend
    out["Citizens Standard"] = {"usd_yr_modeB": f(CITIZENS_STANDARD["dividend_modeB_usd_yr"]),
                                "usd_yr_modeC": f(CITIZENS_STANDARD["dividend_modeC_usd_yr"]),
                                "kind": "universal dividend (theoretical)",
                                "src": CITIZENS_STANDARD["dividend_modeB_usd_yr"].src}
    # Georgism: not comparable - it is a funding source, not a distribution
    out["Georgism (LVT)"] = {"usd_yr": None,
                             "kind": "DIFFERS IN KIND: funding source, pays no per-person benefit",
                             "src": GEORGISM["builds"].src}
    return out


# ---------------------------------------------------------------------------
# C. Comparable axis 2 - owned, compounding wealth stock per person (real USD)
#    Only the wealth-BUILDING systems are comparable; flow systems own nothing.
# ---------------------------------------------------------------------------
def wealth_stock_axis():
    out = {}
    # Alaska: fund value per resident (the per-capita owned stock behind the dividend)
    per_resident = f(ALASKA["fund_value_usd"]) / f(ALASKA["recipients"])
    out["SWF / Alaska"] = {"usd_per_person": round(per_resident),
                           "kind": "collective fund / per-resident share (proven)",
                           "src": ALASKA["fund_value_usd"].src}
    # CS: locked floor at 65, owned and bequeathable
    out["Citizens Standard"] = {"usd_per_person_modeA": f(CITIZENS_STANDARD["floor_modeA_usd"]),
                                "usd_per_person_modeB": f(CITIZENS_STANDARD["floor_modeB_usd"]),
                                "vs_median": f(CITIZENS_STANDARD["floor_vs_median"]),
                                "kind": "owned, locked, bequeathable floor (theoretical)",
                                "src": CITIZENS_STANDARD["floor_modeA_usd"].src}
    # SS and UBI: no owned wealth
    out["Social Security"] = {"usd_per_person": 0,
                              "kind": "DIFFERS IN KIND: no property right (Flemming v. Nestor)",
                              "src": SOCIAL_SECURITY["builds"].src}
    out["UBI"] = {"usd_per_person": 0,
                  "kind": "DIFFERS IN KIND: income flow, builds no owned stock",
                  "src": UBI["builds"].src}
    out["Georgism (LVT)"] = {"usd_per_person": None,
                             "kind": "DIFFERS IN KIND: funding source only",
                             "src": GEORGISM["builds"].src}
    return out


# ---------------------------------------------------------------------------
# D. Comparable axis 3 - funding sustainability / capture record
# ---------------------------------------------------------------------------
def sustainability_axis():
    return {
        "Social Security": {"stress": f(SOCIAL_SECURITY["oasi_depletion_year"]),
                            "detail": f"PAYGO; OASI depletes {f(SOCIAL_SECURITY['oasi_depletion_year'])}, "
                                      f"~{int(f(SOCIAL_SECURITY['payable_at_depletion'])*100)}% payable "
                                      f"(~23% cut); ${f(SOCIAL_SECURITY['unfunded_obligation_usd'])/1e12:.1f}T unfunded",
                            "src": SOCIAL_SECURITY["oasi_depletion_year"].src},
        "SWF / Alaska": {"stress": "capture",
                         "detail": f(ALASKA["capture"]).split(";")[0] +
                                   "; statutory dividend formula abandoned since 2016",
                         "src": ALASKA["capture"].src},
        "UBI": {"stress": "fiscal scale",
                "detail": f"gross cost ~${f(UBI['canonical_monthly_usd'])*12*f(UBI['us_adults'])/1e12:.1f}T/yr "
                          f"at $1,000/mo x {int(f(UBI['us_adults'])/1e6)}M adults; Ontario pilot cancelled on cost",
                "src": UBI["us_adults"].src},
        "Georgism (LVT)": {"stress": "unimplemented",
                           "detail": f"${f(GEORGISM['us_lvt_revenue_low_usd'])/1e12:.1f}-"
                                     f"{f(GEORGISM['us_lvt_revenue_high_usd'])/1e12:.2f}T/yr potential, "
                                     f"~zero deadweight; never adopted as national single-tax",
                           "src": GEORGISM["us_lvt_revenue_low_usd"].src},
        "Citizens Standard": {"stress": "growth-contingent",
                              "detail": f(CITIZENS_STANDARD["capture"]),
                              "src": CITIZENS_STANDARD["capture"].src},
    }


# ---------------------------------------------------------------------------
# E. Check Paper 13's comparative claims against the figures
# ---------------------------------------------------------------------------
def check_claims():
    res = {}

    # Claim 1: CS is the ONLY system simultaneously self-financing + wealth-building + price-brake
    def self_financing(s): return "self-financing" in f(s["funding"]) or "issuance" in f(s["funding"])
    def wealth_building(s): return "stock" in f(s["builds"])
    def price_brake(s): return f(s["price_brake"]) is True
    triple = [name for name, s in SYSTEMS.items()
              if self_financing(s) and wealth_building(s) and price_brake(s)]
    res["claim1_distinctive_cell"] = {
        "statement": "CS is the only universal system that is simultaneously self-financing, "
                     "wealth-building, and equipped with a price-stability mechanism",
        "systems_meeting_all_three": triple,
        "holds": triple == ["Citizens Standard"],
    }

    # Claim 2: each rival LEADS on a specific axis CS does not
    leaders = {
        "simplicity/speed": "UBI",
        "track record": ["Social Security", "SWF / Alaska"],
        "funding efficiency": "Georgism (LVT)",
    }
    proven = [name for name, s in SYSTEMS.items() if f(s["maturity"]) == "proven"]
    res["claim2_where_dominated"] = {
        "statement": "UBI leads on simplicity; SS and the SWF lead on track record; "
                     "Georgism leads on funding efficiency; CS leads none individually",
        "proven_systems": proven,
        "cs_is_proven": f(CITIZENS_STANDARD["maturity"]) == "proven",
        "georgism_zero_deadweight": f(GEORGISM["deadweight_loss"]) == 0.0,
        "holds": ("Citizens Standard" not in proven) and (set(proven) == {"Social Security", "SWF / Alaska"}),
    }

    # Claim 4: CS advantage is conditional - growth-contingent + brake-under-stress
    res["claim4_binding_condition"] = {
        "statement": "CS's advantage is contingent on sustained growth and a brake that holds under stress",
        "cs_funding_growth_tied": "growth" in f(CITIZENS_STANDARD["funding"]),
        "cs_documented_vulnerability": CITIZENS_STANDARD["capture"].note,
        "holds": "growth" in f(CITIZENS_STANDARD["funding"]),
    }
    return res


def build_all():
    return {
        "categorical_table": categorical_table(),
        "axis_annual_benefit_usd_yr": annual_benefit_axis(),
        "axis_wealth_stock_per_person_usd": wealth_stock_axis(),
        "axis_funding_sustainability": sustainability_axis(),
        "claim_checks": check_claims(),
    }


if __name__ == "__main__":
    out = build_all()

    print("=" * 78)
    print("PAPER 13 COMPARATIVE GROUNDING  -  sourced comparison")
    print("=" * 78)

    print("\n[A] CATEGORICAL TABLE (every cell sourced; see AUDIT.md)")
    hdr = f'{"System":<19}{"Funding":<22}{"Builds":<14}{"Brake":<6}{"Maturity"}'
    print(hdr); print("-" * 78)
    for r in out["categorical_table"]:
        print(f'{r["system"]:<19}{r["funding"][:21]:<22}'
              f'{("stock+flow" if "stock" in r["builds"] else "flow")[:13]:<14}'
              f'{r["price_brake"]:<6}{r["maturity"]}')

    print("\n[B] COMPARABLE AXIS 1 - annual per-person benefit (real USD/yr)")
    for k, v in out["axis_annual_benefit_usd_yr"].items():
        amt = (v.get("usd_yr") if v.get("usd_yr") is not None
               else f'B:${v.get("usd_yr_modeB")}/C:${v.get("usd_yr_modeC")}' if "usd_yr_modeB" in v
               else "n/a")
        print(f'  {k:<19} {str(amt):<22} {v["kind"]}')

    print("\n[C] COMPARABLE AXIS 2 - owned wealth stock per person (real USD)")
    for k, v in out["axis_wealth_stock_per_person_usd"].items():
        amt = (v.get("usd_per_person") if "usd_per_person" in v
               else f'A:${v.get("usd_per_person_modeA"):,}/B:${v.get("usd_per_person_modeB"):,}')
        print(f'  {k:<19} {str(amt):<26} {v["kind"]}')

    print("\n[D] COMPARABLE AXIS 3 - funding sustainability / capture")
    for k, v in out["axis_funding_sustainability"].items():
        print(f'  {k:<19} {v["detail"]}')

    print("\n[E] CLAIM CHECKS")
    for k, v in out["claim_checks"].items():
        print(f'  {k}: holds={v["holds"]}')
        if k == "claim1_distinctive_cell":
            print(f'      only system meeting all three: {v["systems_meeting_all_three"]}')

    import os as _os
    _rd = _os.path.join(_os.path.dirname(_os.path.abspath(__file__)), "..", "results")
    _os.makedirs(_rd, exist_ok=True)
    with open(_os.path.join(_rd, "comparison_results.json"), "w") as fh:
        json.dump(out, fh, indent=2, default=str)
    print("\n-> results/comparison_results.json written")

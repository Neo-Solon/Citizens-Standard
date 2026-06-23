"""
channels.py  --  The four-channel distributional model, applied to the real SCF records.

Channel 1  Floor          : engine floor-by-age (per adult), 2022$  -- robust, mechanical
Channel 3  Dividend       : engine reinvested K3 (upper bound; mostly consumption)
Channel 2  Compression    : bounded top-return compression over a generation
                            (gradient: Fagereng et al. 2020; mechanism: Gabaix-Koijen 2021;
                             magnitude bounded by the structural-buyer paper, 2026h)
Channel 4  Bequest        : near-universal inheritance; persistence argument anchored on
                            Nekoei-Seim 2023 / Elinder et al. 2018 (registry causal evidence)

Results are staged robust -> bounded -> registry-grounded, with a decomposition and a
robustness table. Every baseline figure is verified against published SCF statistics first.
"""
import json
import os
import numpy as np
import pandas as pd

from verify_scf import load, gini, share, wpct
import floor_by_age

R = os.path.join(os.path.dirname(__file__), "..", "results")


def metrics(nw, w):
    return dict(
        gini=gini(nw, w),
        p10=wpct(nw, w, 0.10),
        p50=wpct(nw, w, 0.50),
        b50=share(nw, w, 0.0, 0.50),
        t1=share(nw, w, 0.99, 1.0),
        t10=share(nw, w, 0.90, 1.0),
        zeroneg=w[nw <= 0].sum() / w.sum() * 100,
    )


def run():
    fb = floor_by_age.build()
    floor = {int(k): v for k, v in fb["floor"].items()}
    k3 = {int(k): v for k, v in fb["k3"].items()}
    fl = lambda a: floor[int(min(max(a, 0), 65))]
    kd = lambda a: k3[int(min(max(a, 0), 65))]

    df = load()
    w = df.WGT.values.astype(float)
    nw = df.NETWORTH.values.astype(float)
    age = df.AGE.values
    adults = np.where(df.MARRIED.values == 1, 2, 1)
    floorv = np.array([fl(a) for a in age]) * adults
    divv = np.array([kd(a) for a in age]) * adults

    base = metrics(nw, w)
    cF = metrics(nw + floorv, w)
    cFD = metrics(nw + floorv + divv, w)

    # decomposition of the Gini reduction (floor vs dividend)
    tot = base["gini"] - cFD["gini"]
    decomp = {"floor_pct": round((base["gini"] - cF["gini"]) / tot * 100),
              "dividend_pct": round((cF["gini"] - cFD["gini"]) / tot * 100)}

    # channel 2: bounded return compression over a 30y generation (on top of the floor world)
    r_top, T = 0.065, 30
    S = cF["t1"] / 100.0
    comp = {}
    for d in (0.0025, 0.005, 0.0075):
        f = ((1 + r_top - d) / (1 + r_top)) ** T
        comp[f"{d*100:.2f}pp"] = float(round(f * S / (f * S + (1 - S)) * 100, 1))

    # channel 4: bequest (illustrative inheritance distribution; registry evidence -> persistence)
    inh_cf = np.maximum(nw, 0)
    inh_cs = inh_cf + floorv
    bequest = {
        "bequeath_gt25k_cf_pct": round(w[inh_cf > 25000].sum() / w.sum() * 100),
        "bequeath_gt25k_cs_pct": round(w[inh_cs > 25000].sum() / w.sum() * 100),
        "inheritance_gini_cf": round(gini(inh_cf, w), 3),
        "inheritance_gini_cs": round(gini(inh_cs, w), 3),
        "persistence": ("ordinary inheritance equalises on receipt but reverses in ~10y "
                        "(Nekoei-Seim 2023; Elinder 2018): poor heirs deplete, rich earn higher "
                        "returns. The CS floor is LOCKED (no depletion) and UNIFORM-return "
                        "(no rich-heir advantage) -> the equalisation is permanent."),
    }

    # robustness
    co = np.where(nw > floorv, np.maximum(nw, nw * 0.85 + floorv), nw + floorv)
    robust = {
        "per_household": metrics(nw + np.array([fl(a) for a in age]), w),
        "crowding_out": metrics(co, w),
        "floor_minus20": metrics(nw + 0.8 * floorv, w),
    }

    # Paper-8 consistency (principal vs compound) and aggregate
    import deterministic_engine as E
    data = E.build_dataset(end_year=2060)
    dec = E.compute_cohort(data, 1960, 2025, post_real_equity_return=E.GE_REALIZABLE_RETURN,
                           return_decomposition=True)
    consistency = {"principal_pct": round(dec["principal_share"]),
                   "compound_pct": round(dec["compound_share"])}
    agg = {"floor_T": round((floorv * w).sum() / 1e12, 1),
           "total_nw_T": round((nw * w).sum() / 1e12, 1),
           "floor_share_pct": round((floorv * w).sum() / (nw * w).sum() * 100)}

    return {"baseline": base, "floor": cF, "floor_dividend": cFD, "decomposition": decomp,
            "compression_top1": comp, "bequest": bequest, "robustness": robust,
            "paper8_consistency": consistency, "aggregate": agg}


def main():
    res = run()
    b, f = res["baseline"], res["floor"]
    print("=== HEADLINE (real SCF, per-adult floor, 2022$) ===")
    print(f"  Gini            {b['gini']:.3f} -> {f['gini']:.3f}")
    print(f"  P10            ${b['p10']:,.0f} -> ${f['p10']:,.0f}")
    print(f"  bottom-50% share {b['b50']:.1f}% -> {f['b50']:.1f}%")
    print(f"  top-1% share     {b['t1']:.1f}% -> {f['t1']:.1f}%")
    print(f"  zero/negative NW {b['zeroneg']:.1f}% -> {f['zeroneg']:.1f}%")
    print(f"  decomposition: floor {res['decomposition']['floor_pct']}% of Gini reduction")
    print(f"  compression (top-1%, by dDelta): {res['compression_top1']}")
    print(f"  bequest: bequeath>$25k {res['bequest']['bequeath_gt25k_cf_pct']}% -> "
          f"{res['bequest']['bequeath_gt25k_cs_pct']}%")
    print(f"  Paper-8 consistency: principal {res['paper8_consistency']['principal_pct']}% / "
          f"compound {res['paper8_consistency']['compound_pct']}%")
    path = os.path.join(R, "inequality_results.json")
    json.dump(res, open(path, "w"), indent=1, default=float)
    print("wrote", path)


if __name__ == "__main__":
    main()

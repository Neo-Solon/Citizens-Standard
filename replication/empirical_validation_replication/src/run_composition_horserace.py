#!/usr/bin/env python3
"""
Composition tier — the granular composition construction of Mt, run as a MEASURED
two-way convergence check against the Divisia (user-cost) construction (Test C).

Mt_composition = CURRSL + DEMDEPSL + OCDSL  (currency + demand + other-checkable),
built by build_mt.composition_granular from the three FRED component series. Savings is
held OUT (idle tier), so this is the clean transaction-active aggregate. OCDSL is
discontinued after 2020-04 (FRED H.6 Feb-2021 change stopped separate OCD reporting), so the
composition tier runs ~1959 -> 2020-04; the continuous Divisia series carries 2021 onward.

Purpose of this script (the second, independent, NON-inferred construction):
  (1) replace the INFERRED corr(g_M1, g_divisia) = 0.82 from Test C with a DIRECTLY MEASURED
      corr(g_composition, g_divisia) on the identical overlap, and
  (2) report the composition tier's high-regime R^2 on the SAME pre-2021 sample as M2 and Divisia
      (should land near the M1 proxy's 0.19 and Divisia's 0.21).

Same pre-registered protocol as Tests A/B/C (regime >= 4% trailing CPI, 12m horizon, HAC,
expanding-window pseudo-OOS vs a persistence baseline). Reported AS FOUND, including
non-convergence if that is what the data show.
"""
import pandas as pd, numpy as np, json, os, sys
sys.path.insert(0, os.path.join(os.path.dirname(__file__)))
from run_horserace import ols_hac, reg_table, oos_rmse, HORIZON
from build_mt import composition_granular

PRE2021 = "2020-12-01"   # composition is defined only through 2020-04 (OCDSL ends); mask is pre-2021

def _read_fred(fn, col):
    """Read a FRED default-format CSV (observation_date,<col>) into a monthly Series indexed by date."""
    s = pd.read_csv(f"data/{fn}", parse_dates=["observation_date"]).set_index("observation_date")[col]
    s.index.name = "date"
    return s.sort_index()

def load():
    m  = pd.read_csv("data/macro_1959_2026.csv", parse_dates=["date"]).set_index("date").sort_index()
    m1 = pd.read_csv("data/m1sl_1959_2019.csv", parse_dates=["date"]).set_index("date").sort_index()
    dv = pd.read_csv("data/divisia_dm1.csv",    parse_dates=["date"]).set_index("date").sort_index()
    # Build Mt_composition = currency + demand + OCD from the three FRED component series.
    components = {
        "CURRSL":   _read_fred("CURRSL.csv",   "CURRSL"),
        "DEMDEPSL": _read_fred("DEMDEPSL.csv", "DEMDEPSL"),
        "OCDSL":    _read_fred("OCDSL.csv",    "OCDSL"),
    }
    comp = composition_granular(components).rename("MT_COMP")   # raises if a key is missing
    # composition_granular adds with fill_value=0, so it would silently CONTINUE past OCDSL's end
    # (treating OCD as 0 -> an artificial cliff in May-2020 and a currency+demand-only tail).
    # Truncate to the true common window of all three components (OCDSL ends 2020-04): the
    # composition tier genuinely stops here; the continuous Divisia series carries 2021 onward.
    ocd_last = components["OCDSL"].dropna().index.max()
    comp = comp.loc[:ocd_last]
    df = m.join(m1, how="left").join(dv, how="left").join(comp, how="left")
    df["g_m2"]          = 100*np.log(df["M2SL"]).diff(12)
    df["g_m1"]          = 100*np.log(df["M1SL"]).diff(12)
    df["g_divisia"]     = 100*np.log(df["DM1"]).diff(12)
    df["g_composition"] = 100*np.log(df["MT_COMP"]).diff(12)
    df["pi_trail"]      = 100*np.log(df["CPIAUCSL"]).diff(12)
    df["pi_fwd"]        = 100*np.log(df["CPIAUCSL"]).shift(-HORIZON) - 100*np.log(df["CPIAUCSL"])
    df["pi_fwd_pce"]    = 100*np.log(df["PCEPI"]).shift(-HORIZON)    - 100*np.log(df["PCEPI"])
    df["regime"]        = np.where(df["pi_trail"] >= 4.0, "high", "low")
    return df

def main():
    df = load(); R = {}
    pre = df.index <= pd.Timestamp(PRE2021)   # composition's own NaNs make this == its native window

    # ---- Three-way horserace on the IDENTICAL pre-2021 sample (composition / M2 / Divisia / M1) ----
    R["comp_pre2021"]    = reg_table(df, ["g_composition"], "piF~g_composition (currency+demand+OCD, pre-2021)", sample_mask=pre)
    R["m2_pre2021"]      = reg_table(df, ["g_m2"],          "piF~g_m2 (pre-2021)",        sample_mask=pre)
    R["divisia_pre2021"] = reg_table(df, ["g_divisia"],     "piF~g_divisia (pre-2021)",   sample_mask=pre)
    R["m1_pre2021"]      = reg_table(df, ["g_m1"],          "piF~g_m1 (pre-2021)",        sample_mask=pre)

    # ---- Encompassing: does the composition aggregate drive M2 out, as M1 and Divisia did? ----
    R["encompass_comp_m2_pre2021"] = reg_table(df, ["g_composition","g_m2"], "piF~g_composition+g_m2 (pre-2021)", sample_mask=pre)

    # ---- PCE robustness (swap the inflation measure), composition, pre-2021 ----
    dpce = df[pre].dropna(subset=["pi_fwd_pce","g_composition"]).copy()
    dpce["pi_fwd"] = dpce["pi_fwd_pce"]
    R["comp_pce_pre2021"] = reg_table(dpce, ["g_composition"], "piF(PCE)~g_composition (pre-2021)")

    # ---- Pseudo-OOS, composition vs M2, pre-2021, vs persistence baseline ----
    R["oos_composition_pre2021"] = oos_rmse(df, ["g_composition"], sample_end=PRE2021)
    R["oos_m2_pre2021"]          = oos_rmse(df, ["g_m2"],          sample_end=PRE2021)

    # ---- MEASURED convergence: composition vs Divisia on the identical overlap (replaces inferred 0.82) ----
    ov = df.dropna(subset=["g_composition","g_divisia"])   # full composition-Divisia overlap (ends 2020-04)
    R["measured_convergence"] = {
        "corr_g_composition_g_divisia": round(float(ov["g_composition"].corr(ov["g_divisia"])), 3),
        "corr_level_COMP_DM1":          round(float(np.log(ov["MT_COMP"]).corr(np.log(ov["DM1"]))), 3),
        "overlap_start": str(ov.index.min().date()),
        "overlap_end":   str(ov.index.max().date()),
        "n": int(len(ov)),
        "note": "DIRECTLY MEASURED 12m-growth corr of composition (currency+demand+OCD) vs user-cost (Divisia) Mt on the full identical overlap; this replaces the inferred 0.82",
    }
    # Same correlation restricted to the EXACT window Test C used for its inferred 0.82 (<= 2019-12),
    # so the "inferred 0.82 -> measured" replacement is on identical footing.
    ovc = ov[ov.index <= "2019-12-01"]
    R["measured_convergence_testC_window"] = {
        "corr_g_composition_g_divisia": round(float(ovc["g_composition"].corr(ovc["g_divisia"])), 3),
        "corr_level_COMP_DM1":          round(float(np.log(ovc["MT_COMP"]).corr(np.log(ovc["DM1"]))), 3),
        "overlap_start": str(ovc.index.min().date()),
        "overlap_end":   str(ovc.index.max().date()),
        "n": int(len(ovc)),
        "note": "same measure on Test C's exact 1968-2019 window; directly comparable to the inferred corr(g_M1,g_divisia)=0.82",
    }

    # ---- Sanity: composition vs the M1 proxy (should be ~1; composition == M1 pre-2020 by definition) ----
    ov2 = df.dropna(subset=["g_composition","g_m1"]); ov2 = ov2[ov2.index <= PRE2021]
    R["composition_vs_m1proxy"] = {
        "corr_g_composition_g_m1": round(float(ov2["g_composition"].corr(ov2["g_m1"])), 3),
        "corr_level_COMP_M1":      round(float(np.log(ov2["MT_COMP"]).corr(np.log(ov2["M1SL"]))), 3),
        "n": int(len(ov2)),
        "note": "composition = currency+demand+OCD; the M1 proxy (M1SL) adds only travelers' checks, so the two are near-identical pre-2020 — confirms the composition tier reproduces the M1 proxy directly",
    }

    # ---- composition availability window ----
    cv = df["MT_COMP"].dropna()
    R["composition_window"] = {"start": str(cv.index.min().date()), "end": str(cv.index.max().date()), "n": int(len(cv))}

    json.dump(R, open("results/composition_results.json","w"), indent=2)
    for k, v in R.items():
        print(f"\n=== {k} ===")
        if isinstance(v, list):
            for r in v: print("  ", r)
        else:
            print("  ", v)

if __name__ == "__main__":
    main()

#!/usr/bin/env python3
"""
Test C — the Divisia construction of Mt, run as an INDEPENDENT check on Test B's M1 proxy.

Divisia M1 (CFS, Barnett) weights monetary components by user cost rather than summing them,
so it is a genuinely different construction from the composition (M1) tier. Two things it can do
that clean M1 cannot:
  (1) it is continuous across the May-2020 redefinition, so it reaches the 2020-2022 episode;
  (2) if it agrees with M1 where both exist (pre-2020) and carries the same inflation signal,
      that is the independent-construction convergence the referee asked for.

Same pre-registered protocol as Tests A/B (regime >=4% trailing CPI, 12m horizon, HAC, OOS).
Reported honestly, including any regime where Divisia does NOT beat M2.
"""
import pandas as pd, numpy as np, json, os, sys
sys.path.insert(0, os.path.join(os.path.dirname(__file__)))
from run_horserace import ols_hac, reg_table, oos_rmse, HORIZON

def load():
    m  = pd.read_csv("data/macro_1959_2026.csv", parse_dates=["date"]).set_index("date").sort_index()
    m1 = pd.read_csv("data/m1sl_1959_2019.csv", parse_dates=["date"]).set_index("date").sort_index()
    dv = pd.read_csv("data/divisia_dm1.csv", parse_dates=["date"]).set_index("date").sort_index()
    df = m.join(m1, how="left").join(dv, how="left")
    df["g_m2"]      = 100*np.log(df["M2SL"]).diff(12)
    df["g_m1"]      = 100*np.log(df["M1SL"]).diff(12)
    df["g_divisia"] = 100*np.log(df["DM1"]).diff(12)
    df["pi_trail"]  = 100*np.log(df["CPIAUCSL"]).diff(12)
    df["pi_fwd"]    = 100*np.log(df["CPIAUCSL"]).shift(-HORIZON) - 100*np.log(df["CPIAUCSL"])
    df["pi_fwd_pce"]= 100*np.log(df["PCEPI"]).shift(-HORIZON) - 100*np.log(df["PCEPI"])
    df["regime"]    = np.where(df["pi_trail"] >= 4.0, "high", "low")
    return df

def main():
    df = load(); R={}
    # ---- C1: Divisia vs M2, FULL sample incl 2020-22 (the period clean M1 can't reach) ----
    R["C1_divisia_full"] = reg_table(df, ["g_divisia"], "piF~g_divisia (1968-2026, incl 2020-22)")
    R["C1_m2_full"]      = reg_table(df, ["g_m2"],      "piF~g_m2 (1968-2026)")
    # ---- C2: Divisia vs M2, clean pre-2020 (direct comparison to Test B's M1 numbers) ----
    pre = df.index <= pd.Timestamp("2019-12-01")
    R["C2_divisia_pre2020"] = reg_table(df, ["g_divisia"], "piF~g_divisia (pre-2020)", sample_mask=pre)
    # ---- C3: encompassing — does Divisia drive M2 out, like M1 did? (high regime, full sample) ----
    R["C3_encompass_full"]  = reg_table(df, ["g_divisia","g_m2"], "piF~g_divisia+g_m2 (full)")
    # ---- PCE robustness (swap the inflation measure), high regime, full ----
    dpce = df.dropna(subset=["pi_fwd_pce","g_divisia"]).copy()
    dpce["pi_fwd"]=dpce["pi_fwd_pce"]
    R["C_pce_divisia_full"] = reg_table(dpce, ["g_divisia"], "piF(PCE)~g_divisia (full)")
    # ---- C4: pseudo-OOS, Divisia vs M2, full sample ----
    R["C4_oos_divisia"] = oos_rmse(df, ["g_divisia"])
    R["C4_oos_m2"]      = oos_rmse(df, ["g_m2"])
    # ---- CONVERGENCE: do the two independent constructions move together where both exist? ----
    ov = df.dropna(subset=["g_m1","g_divisia"])
    ov = ov[ov.index <= "2019-12-01"]
    R["convergence_pre2020"] = {
        "corr_g_m1_g_divisia": round(float(ov["g_m1"].corr(ov["g_divisia"])),3),
        "corr_level_M1_DM1":   round(float(np.log(df.loc[ov.index,"M1SL"]).corr(np.log(df.loc[ov.index,"DM1"]))),3),
        "n": int(len(ov)),
        "note": "12m-growth correlation of the composition (M1) and user-cost (Divisia) constructions, 1968-2019"
    }
    json.dump(R, open("results/divisia_results.json","w"), indent=2)
    for k,v in R.items():
        print(f"\n=== {k} ===")
        if isinstance(v,list):
            for r in v: print("  ",r)
        else: print("  ",v)

if __name__=="__main__":
    main()

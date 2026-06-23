#!/usr/bin/env python3
"""
Citizens Standard — Validation replication: empirical horserace.
Runs the two pre-registered tests on genuine FRED data:
  Test A  two-regime money->inflation (M2), full sample 1959-2026 (incl. 2020-22)
  Test B  narrow(M1, transaction-active proxy) vs broad(M2) info content, clean pre-2020 sample
All claims are reported honestly: slopes, R2, and pseudo-out-of-sample RMSE, by regime.
"""
import pandas as pd, numpy as np, json
import statsmodels.api as sm

HORIZON = 12          # predict inflation over next 12 months
REGIME_THRESHOLD = 4.0  # trailing 12m CPI inflation (%) splitting high/low regime  [pre-registered]
OOS_START = "1975-01" # expanding-window OOS evaluation start

def load():
    m = pd.read_csv("data/macro_1959_2026.csv", parse_dates=["date"]).set_index("date").sort_index()
    m1 = pd.read_csv("data/m1sl_1959_2019.csv", parse_dates=["date"]).set_index("date").sort_index()
    df = m.join(m1, how="left")
    # growth rates (12m log %, annual)
    df["g_m2"] = 100*np.log(df["M2SL"]).diff(12)
    df["g_m1"] = 100*np.log(df["M1SL"]).diff(12)
    # trailing & forward CPI inflation (12m log %)
    df["pi_trail"] = 100*np.log(df["CPIAUCSL"]).diff(12)
    df["pi_fwd"]   = 100*np.log(df["CPIAUCSL"]).shift(-HORIZON) - 100*np.log(df["CPIAUCSL"])
    df["regime"]   = np.where(df["pi_trail"] >= REGIME_THRESHOLD, "high", "low")
    return df

def ols_hac(y, X):
    X = sm.add_constant(X)
    return sm.OLS(y, X, missing="drop").fit(cov_type="HAC", cov_kwds={"maxlags":HORIZON})

def reg_table(df, xcols, label, sample_mask=None):
    out=[]
    d = df if sample_mask is None else df[sample_mask]
    for name, sub in [("all", d), ("high", d[d.regime=="high"]), ("low", d[d.regime=="low"])]:
        s = sub.dropna(subset=["pi_fwd"]+xcols)
        if len(s) < 30:
            out.append({"model":label,"regime":name,"n":len(s),"note":"insufficient"}); continue
        m = ols_hac(s["pi_fwd"], s[xcols])
        row={"model":label,"regime":name,"n":int(len(s)),"R2":round(m.rsquared,3)}
        for c in xcols:
            row[f"b_{c}"]=round(m.params[c],3); row[f"t_{c}"]=round(m.tvalues[c],2)
        out.append(row)
    return out

def oos_rmse(df, xcols, sample_end=None):
    """Expanding-window pseudo-OOS: at each t (with pi_fwd observed), fit on history, predict, by regime."""
    d = df.copy()
    if sample_end: d = d[d.index <= sample_end]
    d = d.dropna(subset=["pi_fwd","pi_trail"]+xcols)
    d = d[d.index >= "1962-01-01"]
    idx = d.index
    start = pd.Timestamp(OOS_START)
    errs = {"high":[], "low":[]}; base_errs={"high":[],"low":[]}
    for t in idx[idx>=start]:
        train = d[d.index < t]
        if len(train) < 60: continue
        Xtr = sm.add_constant(train[xcols]); ytr = train["pi_fwd"]
        try: m = sm.OLS(ytr, Xtr).fit()
        except Exception: continue
        xt = d.loc[[t], xcols]; xt = sm.add_constant(xt, has_constant="add")
        # align columns
        xt = xt.reindex(columns=Xtr.columns, fill_value=1.0)
        pred = float(m.predict(xt).iloc[0])
        # baseline: random-walk-in-inflation (forecast next-12m infl = trailing 12m infl)
        base = float(d.loc[t,"pi_trail"])
        actual = float(d.loc[t,"pi_fwd"]); reg = d.loc[t,"regime"]
        errs[reg].append((pred-actual)**2); base_errs[reg].append((base-actual)**2)
    res={}
    for r in ["high","low"]:
        if errs[r]:
            res[r]={"rmse_model":round(np.sqrt(np.mean(errs[r])),3),
                    "rmse_baseline":round(np.sqrt(np.mean(base_errs[r])),3),
                    "n":len(errs[r])}
    return res

def main():
    df = load()
    R={}
    # ---------- TEST A: two-regime, M2, full sample ----------
    R["A_regime_M2_full"]   = reg_table(df, ["g_m2"], "piF~g_m2 (1959-2026)")
    R["A_oos_M2_vs_baseline"]= oos_rmse(df, ["g_m2"])
    # ---------- TEST B: narrow vs broad, clean pre-2020 ----------
    pre = df.index <= pd.Timestamp("2019-09-01")
    R["B_m1_only"]   = reg_table(df, ["g_m1"], "piF~g_m1 (1960-2019)", sample_mask=pre)
    R["B_m2_only"]   = reg_table(df, ["g_m2"], "piF~g_m2 (1960-2019)", sample_mask=pre)
    R["B_encompass"] = reg_table(df, ["g_m1","g_m2"], "piF~g_m1+g_m2 (1960-2019)", sample_mask=pre)
    R["B_oos_m1"]    = oos_rmse(df, ["g_m1"], sample_end="2019-09-01")
    R["B_oos_m2"]    = oos_rmse(df, ["g_m2"], sample_end="2019-09-01")
    # episode descriptive (genuine)
    m2=df["M2SL"]
    R["episode"]={"M2_pct_Feb2020_Apr2022":round(100*(m2.loc['2022-04-01']/m2.loc['2020-02-01']-1),1),
                  "CPI_YoY_Jun2022":round(100*(df['CPIAUCSL'].loc['2022-06-01']/df['CPIAUCSL'].loc['2021-06-01']-1),1)}
    json.dump(R, open("results/horserace_results.json","w"), indent=2)
    # pretty print
    def show(key):
        print(f"\n=== {key} ===")
        v=R[key]
        if isinstance(v,list):
            for r in v: print("  ",r)
        else: print("  ",v)
    for k in ["A_regime_M2_full","A_oos_M2_vs_baseline","B_m1_only","B_m2_only","B_encompass","B_oos_m1","B_oos_m2","episode"]:
        show(k)

if __name__=="__main__":
    main()

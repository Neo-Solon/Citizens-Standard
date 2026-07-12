"""
Two-circuit (transactional vs asset) replication package.

Exposes run(data_dir, refresh) -> {"passed": bool, "summary": str, "detail": {...}}
so the top-level run_all.py can execute it and report pass/fail.

Standalone use (academics): `python run.py` prints the full detail.

What it checks (against the bundled snapshot):
  1. Clean dollar MA series builds and coheres: MA + MT tracks M2 to a stable ~4-5% gap.
  2. The two circuits are distinct: Divisia-M1 vs M2 growth correlation is well below 1.0.
  3. Japan narrow-vs-broad horserace reproduces (broad wins; low-inflation regime caveat).
These are the confirmatory checks from the 2026-07 two-circuit supplementary record.
"""
import numpy as np
import pandas as pd
from pathlib import Path


def _load(data_dir, fname, col):
    d = pd.read_csv(Path(data_dir) / fname)
    d = d.rename(columns={d.columns[0]: "date", d.columns[-1]: col})
    d["date"] = pd.to_datetime(d["date"])
    return d[["date", col]]


def run(data_dir, refresh=False):
    detail = {}
    checks = []

    # ---- 1. build clean dollar MA and coherence-check MA+MT vs M2 ----
    wsav = _load(data_dir, "WSAVNS.csv", "WSAVNS")
    mdlm = _load(data_dir, "MDLM.csv", "MDLM")
    std = _load(data_dir, "STDSL.csv", "STDSL")
    curr = _load(data_dir, "CURRSL.csv", "CURR")
    dem = _load(data_dir, "DEMDEPSL.csv", "DEM")
    m2 = _load(data_dir, "M2SL.csv", "M2")

    wsav["ym"] = wsav["date"].dt.to_period("M")
    wm = wsav.groupby("ym")["WSAVNS"].mean().reset_index()
    wm["date"] = wm["ym"].dt.to_timestamp(); wm = wm[["date", "WSAVNS"]]
    w_mar = wm[wm["date"] == "2020-03-01"]["WSAVNS"].values[0]
    w_apr = wm[wm["date"] == "2020-04-01"]["WSAVNS"].values[0]
    m_may = mdlm[mdlm["date"] == "2020-05-01"]["MDLM"].values[0]
    splice = m_may / (w_apr * (w_apr / w_mar))
    wm["SAV"] = wm["WSAVNS"] * splice
    pre = wm[wm["date"] < "2020-05-01"][["date", "SAV"]]
    post = mdlm[mdlm["date"] >= "2020-05-01"].rename(columns={"MDLM": "SAV"})
    sav = pd.concat([pre, post]).sort_values("date")
    ma = sav.merge(std, on="date"); ma["MA"] = ma["SAV"] + ma["STDSL"]

    coh = ma.merge(curr, on="date").merge(dem, on="date").merge(m2, on="date")
    coh["MT"] = coh["CURR"] + coh["DEM"]
    coh["gap"] = (coh["MA"] + coh["MT"] - coh["M2"]) / coh["M2"] * 100
    gap_window = coh[(coh["date"] >= "2020-02-01") & (coh["date"] <= "2023-06-01")]["gap"]
    gap_ok = (gap_window.abs().between(2, 9).mean() > 0.8)  # stable few-percent gap
    detail["splice_factor"] = round(splice, 3)
    detail["coherence_gap_mean_pct"] = round(gap_window.mean(), 2)
    checks.append(("MA coherence (MA+MT ~ M2, stable gap)", gap_ok))

    # ---- 2. circuits distinct: Divisia-M1 vs M2 growth correlation ----
    dv = _load(data_dir, "divisia_dm1.csv", "DM1")
    d = dv.merge(m2, on="date").sort_values("date")
    d["dm1_g"] = d["DM1"].pct_change(12) * 100
    d["m2_g"] = d["M2"].pct_change(12) * 100
    dd = d.dropna(subset=["dm1_g", "m2_g"])
    corr = dd["dm1_g"].corr(dd["m2_g"])
    detail["divisia_vs_m2_growth_corr"] = round(corr, 3)
    checks.append(("circuits distinct (corr < 0.9)", corr < 0.9))

    # ---- 3. Japan narrow-vs-broad horserace ----
    nm = _load(data_dir, "MANMM101JPM189S.csv", "NM")
    bm = _load(data_dir, "MABMM301JPM189S.csv", "BM")
    cpi = _load(data_dir, "JPNCPIALLMINMEI.csv", "CPI")
    j = nm.merge(bm, on="date").merge(cpi, on="date").sort_values("date")
    j["nm_g"] = j["NM"].pct_change(12) * 100
    j["bm_g"] = j["BM"].pct_change(12) * 100
    j["infl_fwd"] = j["CPI"].pct_change(12).shift(-12) * 100
    j = j.dropna(subset=["nm_g", "bm_g", "infl_fwd"])
    ann = j.iloc[::12, :]
    r2n = np.corrcoef(ann["nm_g"], ann["infl_fwd"])[0, 1] ** 2
    r2b = np.corrcoef(ann["bm_g"], ann["infl_fwd"])[0, 1] ** 2
    detail["japan_narrow_R2"] = round(r2n, 3)
    detail["japan_broad_R2"] = round(r2b, 3)
    checks.append(("Japan: broad out-predicts narrow", r2b > r2n))

    passed = all(ok for _, ok in checks)
    summary = f"MA gap {detail['coherence_gap_mean_pct']}%, corr {detail['divisia_vs_m2_growth_corr']}, JP broad>{r2b>r2n and 'narrow' or '?'}"
    return {"passed": passed, "summary": summary, "detail": detail, "checks": checks}


if __name__ == "__main__":
    import json, sys
    data_dir = Path(__file__).resolve().parents[2] / "data"
    out = run(data_dir)
    print(json.dumps(out["detail"], indent=2))
    for name, ok in out["checks"]:
        print(("  PASS " if ok else "  FAIL ") + name)
    print("\nRESULT:", "PASS" if out["passed"] else "FAIL")
    sys.exit(0 if out["passed"] else 1)

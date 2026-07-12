"""
run_fx_analysis.py — the two pre-registered lines of evidence + falsification check.

Line A: decompose bilateral-rate variance into PPP / UIP / residual, and report the
        CS-removable monetary share (PPP + UIP systematic part).
Line B: compare realized FX volatility and excess-vol ratio, anchored vs floating group.
Falsification: F1 (monetary share < 10%) or F2 (anchored not lower) -> claim fails.

Runs on panel.csv from build_fx_data.py (real or synth). All outputs stamped with source.
"""
import numpy as np, pandas as pd, json, os

def annualize_vol(monthly_logret):
    return monthly_logret.std()*np.sqrt(12)

def line_A_decomposition(df):
    """For each currency, regress fx_logret on infl_diff and rate_diff; variance shares."""
    out=[]
    for cur,g in df.groupby("currency"):
        y=g.fx_logret.values
        X=np.column_stack([np.ones(len(g)), g.infl_diff.values, g.rate_diff.values])
        # OLS
        beta,_,_,_=np.linalg.lstsq(X,y,rcond=None)
        yhat=X@beta
        ppp_part = beta[1]*g.infl_diff.values
        uip_part = beta[2]*g.rate_diff.values
        resid = y - yhat
        var_total=y.var()
        # variance attribution (cov-based, sums to total)
        def share(comp): return np.cov(comp,y)[0,1]/var_total if var_total>0 else 0.0
        s_ppp=share(ppp_part); s_uip=share(uip_part); s_res=1-s_ppp-s_uip
        out.append(dict(currency=cur, regime=g.regime.iloc[0],
                        share_ppp=s_ppp, share_uip=s_uip, share_resid=s_res,
                        cs_removable=s_ppp+s_uip))  # the monetary share a CS anchor mutes
    return pd.DataFrame(out)

def line_B_volatility(df):
    out=[]
    for cur,g in df.groupby("currency"):
        fxvol=annualize_vol(g.fx_logret)
        infvol=annualize_vol(g.infl_diff)
        excess = fxvol/infvol if infvol>0 else np.nan
        out.append(dict(currency=cur, regime=g.regime.iloc[0],
                        fx_vol=fxvol, infl_vol=infvol, excess_vol_ratio=excess))
    return pd.DataFrame(out)

def group_contrast(volB):
    a=volB[volB.regime=="anchored"]; f=volB[volB.regime=="floating"]
    return dict(
        anchored_fx_vol_mean=a.fx_vol.mean(), floating_fx_vol_mean=f.fx_vol.mean(),
        anchored_excess_mean=a.excess_vol_ratio.mean(), floating_excess_mean=f.excess_vol_ratio.mean(),
        fx_vol_diff=f.fx_vol.mean()-a.fx_vol.mean(),
        excess_diff=f.excess_vol_ratio.mean()-a.excess_vol_ratio.mean(),
    )

def falsification(decompA, contrast):
    monetary_share = decompA.cs_removable.mean()
    F1 = monetary_share < 0.10                      # anchoring removes almost nothing
    F2 = contrast["excess_diff"] <= 0               # anchored NOT lower excess vol
    return dict(mean_monetary_share=monetary_share, F1_triggered=bool(F1),
                F2_triggered=bool(F2), claim_survives=bool(not F1 and not F2))

def main():
    if not os.path.exists("panel.csv"):
        import build_fx_data; build_fx_data.build()
    df=pd.read_csv("panel.csv")
    src = "SYNTHETIC (calibrated)" if os.path.exists("panel_meta.json") else "REAL"
    try:
        meta=json.load(open("panel_meta.json")); src=meta.get("source",src)
    except Exception: pass

    A=line_A_decomposition(df)
    B=line_B_volatility(df)
    C=group_contrast(B)
    F=falsification(A,C)

    print("="*70)
    print(f"FX INTERFACE ANALYSIS   |   data source: {src}")
    print("="*70)
    print("\n--- LINE A: variance decomposition (CS-removable monetary share) ---")
    print(A.round(3).to_string(index=False))
    print(f"\n  mean CS-removable (PPP+UIP) share across pairs: {A.cs_removable.mean():.1%}")

    print("\n--- LINE B: realized FX volatility, anchored vs floating ---")
    print(B.round(3).to_string(index=False))
    print("\n  group means:")
    print(f"    anchored  FX vol {C['anchored_fx_vol_mean']:.3f}   excess {C['anchored_excess_mean']:.2f}")
    print(f"    floating  FX vol {C['floating_fx_vol_mean']:.3f}   excess {C['floating_excess_mean']:.2f}")
    print(f"    difference (floating - anchored): FX vol {C['fx_vol_diff']:.3f}, excess {C['excess_diff']:.2f}")

    print("\n--- FALSIFICATION CHECK ---")
    print(f"    F1 (monetary share < 10%): {'TRIGGERED' if F['F1_triggered'] else 'not triggered'}")
    print(f"    F2 (anchored not lower):   {'TRIGGERED' if F['F2_triggered'] else 'not triggered'}")
    print(f"    => claim survives: {F['claim_survives']}")

    # save results
    A.to_csv("RESULTS_lineA_decomposition.csv", index=False)
    B.to_csv("RESULTS_lineB_volatility.csv", index=False)
    json.dump(dict(source=src, contrast=C, falsification=F),
              open("RESULTS_summary.json","w"), indent=2, default=float)
    print("\n[saved] RESULTS_lineA_decomposition.csv, RESULTS_lineB_volatility.csv, RESULTS_summary.json")

if __name__=="__main__":
    main()

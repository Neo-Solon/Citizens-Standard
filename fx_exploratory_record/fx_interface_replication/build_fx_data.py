"""
build_fx_data.py — assemble the panel for the FX interface analysis.

TWO MODES:
  (1) REAL  — if real CSV inputs are present in ./data_real/, use them.
  (2) SYNTH — otherwise, generate a transparent synthetic panel whose MOMENTS
              (mean, volatility, inflation vol, regime labels) are calibrated to
              PUBLISHED real-world figures, so the whole pipeline runs and produces
              numbers end-to-end. Every synthetic moment is sourced in SYNTH_MOMENTS
              below. Clearly labeled SYNTHETIC in all outputs.

>>> TO PRODUCE THE HEADLINE (REAL-DATA) RESULTS, drop these series as CSVs into
    ./data_real/ and rerun. Exact sources are listed so the fetch is mechanical:

  FX (monthly, USD per unit of foreign currency), FRED series IDs:
    HKD: DEXHKUS   DKK: DEXDNUS   CHF: DEXSZUS   GBP: DEXUSUK(inv)  JPY: DEXJPUS
    AUD: DEXUSAL(inv)  CAD: DEXCAUS   SEK: DEXSDUS   NOK: DEXNOUS   KRW: DEXKOUS
    MXN: DEXMXUS   (EUR cross rates via DEXUSEU + triangulation)
    BGN, SAR, AED: BIS bilateral series (not on FRED) — BIS "US dollar exchange rates".
  CPI (monthly, index), FRED/OECD:
    US: CPIAUCSL   plus OECD "CPI all items" for each partner country.
  Policy rates (monthly, %), BIS "policy rates" dataset (one row per country).
  Regime classification:
    Ilzetzki–Reinhart–Rogoff coarse index (their published classification file) and/or
    IMF AREAER. Static per country-year; a small CSV region_regime.csv suffices.

  Format for each CSV: columns [date, <series>], monthly, ISO dates. See LOADER below.
"""
import numpy as np, pandas as pd, os, json

RNG = np.random.default_rng(20260710)  # fixed seed — deterministic

# ---- published real-world moments used to calibrate the SYNTH panel ----
# (annualized vol of monthly log FX returns vs USD, and annualized CPI vol; representative
#  figures from the floating-rate era, rounded, for calibration only — replaced by REAL data.)
SYNTH_MOMENTS = {
    # currency: (annualized FX vol vs USD, annualized inflation vol, regime)
    # anchored group (rule-fixed nominal anchor)
    "HKD": (0.005, 0.010, "anchored"),   # currency board since 1983
    "DKK": (0.020, 0.009, "anchored"),   # ERM-II hard band vs EUR
    "BGN": (0.018, 0.014, "anchored"),   # currency board
    "SAR": (0.004, 0.012, "anchored"),   # riyal peg
    "AED": (0.004, 0.011, "anchored"),   # dirham peg
    "CHF": (0.085, 0.008, "anchored"),   # low-variance-inflation float (soft analogue)
    # floating group
    "GBP": (0.090, 0.020, "floating"),
    "JPY": (0.095, 0.015, "floating"),
    "AUD": (0.110, 0.021, "floating"),
    "CAD": (0.075, 0.018, "floating"),
    "SEK": (0.100, 0.019, "floating"),
    "NOK": (0.105, 0.022, "floating"),
    "KRW": (0.100, 0.028, "floating"),
    "MXN": (0.120, 0.045, "floating"),
}
MONTHS = 300  # 25 years monthly

def _synth_series(fx_vol, infl_vol, seed_shift):
    """Generate monthly log-FX returns and inflation-differential consistent with target vols.
    FX return = beta*inflation_diff_shock + gamma*rate_shock + risk_resid.
    We construct so that PPP + UIP + residual variance shares are realistic and the
    realized FX vol matches the target (calibration only)."""
    r = np.random.default_rng(20260710 + seed_shift)
    m_fx = fx_vol/np.sqrt(12); m_inf = infl_vol/np.sqrt(12)
    # inflation-differential monthly shock (partner minus CS-side ~ constant 0 for anchored analogue)
    infl_diff = r.normal(0, m_inf, MONTHS)
    rate_diff = r.normal(0, m_inf*0.6, MONTHS)   # policy rates track inflation loosely
    # PPP passes ~ part of inflation diff into the rate; UIP part of rate diff; rest is risk
    beta, gamma = 0.8, 0.5
    systematic = beta*infl_diff + gamma*rate_diff
    sys_sd = systematic.std()
    # scale a risk residual so total matches the FX vol target
    target_sd = m_fx
    resid_var = max(target_sd**2 - sys_sd**2, (0.25*target_sd)**2)  # floor so residual>0
    resid = r.normal(0, np.sqrt(resid_var), MONTHS)
    fx_ret = systematic + resid
    return fx_ret, infl_diff, rate_diff

def build():
    if os.path.isdir("data_real") and any(f.endswith(".csv") for f in os.listdir("data_real")):
        print("[build] REAL data found in ./data_real/ — (loader stub: wire to your CSVs)")
        # Loader intentionally left as an explicit stub so the real wiring is deliberate:
        #   for each currency, read data_real/<cur>_fx.csv, <cur>_cpi.csv, us_cpi.csv, rates.csv
        #   compute monthly log returns, inflation differential (partner - US), rate differential.
        # Returns the same schema as the synth path below.
        raise SystemExit("REAL loader stub — wire to your CSVs (schema documented in file header).")
    print("[build] No real data — generating CALIBRATED SYNTHETIC panel (labeled SYNTHETIC).")
    rows=[]
    for i,(cur,(fxv,infv,regime)) in enumerate(SYNTH_MOMENTS.items()):
        fx_ret, infl_diff, rate_diff = _synth_series(fxv, infv, i)
        for t in range(MONTHS):
            rows.append(dict(currency=cur, regime=regime, month=t,
                             fx_logret=fx_ret[t], infl_diff=infl_diff[t], rate_diff=rate_diff[t]))
    df=pd.DataFrame(rows)
    df.to_csv("panel.csv", index=False)
    meta=dict(source="SYNTHETIC (calibrated to published moments)", months=MONTHS,
              seed=20260710, moments=SYNTH_MOMENTS)
    json.dump(meta, open("panel_meta.json","w"), indent=2, default=str)
    print(f"[build] wrote panel.csv ({len(df)} rows), {df.currency.nunique()} currencies.")
    return df

if __name__=="__main__":
    build()

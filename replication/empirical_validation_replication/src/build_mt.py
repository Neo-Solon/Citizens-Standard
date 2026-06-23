#!/usr/bin/env python3
"""
build_mt.py — construct the transactional aggregate M-transaction (Mt) three independent ways.

Construction 1 (composition): transaction-active money = currency + demand + other-checkable.
  - In this package it is operationalized by M1 for the pre-May-2020 window, where M1 == the
    active tier by definition (currency + demand + OCD) and no reclassification has occurred.
  - The granular post-2020 version (holding savings in the IDLE tier across the redefinition)
    is implemented in `composition_granular` and runs when the component series are supplied.
Construction 2 (payment-flow): turnover-weighted active share from Fedwire/ACH/RTP volumes.   [data-gated]
Construction 3 (user-cost/Divisia): CFS Divisia transaction-tier sub-aggregate.                [data-gated]

The constructions share NO input with the CS price-stability locus (non-circular, paper Prop. 4).
The locus-back-solved route is intentionally NOT implemented.
"""
import pandas as pd, numpy as np

# ---------- Construction 1: composition ----------
def composition_m1proxy(macro_csv="data/macro_1959_2026.csv", m1_csv="data/m1sl_1959_2019.csv"):
    """Clean pre-2020 transaction-active aggregate = M1 (currency+demand+OCD). Returns monthly Mt level."""
    m1 = pd.read_csv(m1_csv, parse_dates=["date"]).set_index("date")["M1SL"]
    return m1.rename("Mt_composition")

def composition_granular(components: dict, redefinition="2020-05-01"):
    """
    Full composition construction with the May-2020 splice.
    components: dict of monthly Series keyed by FRED id:
       active : CURRSL (currency), DEMDEPSL (demand deposits), OCDSL (other checkable)
       idle   : SAVINGSL (savings), STDSL (small time), RMFSL/retail MMF
    Mt = currency + demand + OCD, with savings ALWAYS in the idle tier even after the
    May-2020 reclassification moved it into M1. This keeps Mt continuous across the break.
    """
    req=["CURRSL","DEMDEPSL","OCDSL"]
    missing=[c for c in req if c not in components]
    if missing:
        raise ValueError(f"composition_granular needs {missing}; supply the FRED component series to run.")
    active = components["CURRSL"].add(components["DEMDEPSL"],fill_value=0).add(components["OCDSL"],fill_value=0)
    return active.rename("Mt_composition_granular")

# ---------- Construction 2: payment-flow (data-gated) ----------
def payment_flow(m2: pd.Series, flows: dict|None=None):
    """
    Turnover-weighted active share of M2 from payment volumes.
    flows: {'FEDWIRE': Series, 'ACH': Series, 'RTP': Series} of monthly $ transfer volumes.
    Mt = M2 * w_active, where w_active is the share of M2 implied by payment turnover.
    Returns None (with an explanatory note) when the flow series are not supplied.
    """
    if not flows:
        return None  # requires Fedwire/ACH/RTP monthly volumes (Federal Reserve Payments Study / Fedwire stats)
    turnover = sum(flows.values())
    w = (turnover/turnover.rolling(12).mean())  # normalized turnover proxy
    w = (w/w.max()).clip(0,1)
    return (m2*w).rename("Mt_paymentflow")

# ---------- Construction 3: user-cost / Divisia (data-gated) ----------
def divisia_transaction_tier(divisia_components: dict|None=None):
    """
    Transaction-tier Divisia sub-aggregate using CFS user-cost weights.
    divisia_components: CFS Divisia component quantities and user costs.
    Returns None when CFS Divisia data are not supplied (centerforfinancialstability.org/amfm).
    """
    if not divisia_components:
        return None
    # Divisia growth = sum_i w_i * dlog(q_i), w_i = expenditure share in user cost (transaction tier only)
    q = divisia_components["quantities"]; uc = divisia_components["user_costs"]
    exp = q*uc; w = exp.div(exp.sum(axis=1),axis=0)
    dlog = np.log(q).diff()
    g = (w.shift(1)*dlog).sum(axis=1)
    return (100*g).rename("Mt_divisia_growth")

if __name__=="__main__":
    mt = composition_m1proxy()
    print("Mt (composition, M1 proxy):", mt.dropna().index.min().date(),"→",mt.dropna().index.max().date(),
          "| last", round(float(mt.dropna().iloc[-1]),1))
    print("payment_flow:", "available" if payment_flow(pd.Series(dtype=float),None) is not None else "data-gated (needs Fedwire/ACH/RTP)")
    print("divisia:", "available" if divisia_transaction_tier(None) is not None else "data-gated (needs CFS Divisia)")

def divisia_dm1_index(csv="data/divisia_dm1.csv"):
    """Load the CFS Divisia M1 index (user-cost aggregate). This IS the construction-3 output,
    computed by CFS the proper way (user-cost weights), so we use their published index directly
    rather than re-deriving it. Returns the monthly level (index, base 100 @ 1967)."""
    import pandas as pd
    d = pd.read_csv(csv, parse_dates=["date"]).set_index("date")["DM1"]
    return d.rename("Mt_divisia")

#!/usr/bin/env python3
"""Robustness (PCE inflation) + figure for the narrow-vs-broad result."""
import pandas as pd, numpy as np, json
# statsmodels is the source of truth offline and in CI. It has C extensions and is NOT in the
# Pyodide distribution, so in the browser we fall back to hac_ols -- a pure-numpy drop-in that
# reproduces the OLS/HAC results to machine precision (see hac_ols.py).
try:
    import statsmodels.api as sm
except ImportError:                     # Pyodide / no statsmodels
    import hac_ols as sm
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

H=12; THR=4.0
def load():
    m=pd.read_csv("data/macro_1959_2026.csv",parse_dates=["date"]).set_index("date").sort_index()
    m1=pd.read_csv("data/m1sl_1959_2019.csv",parse_dates=["date"]).set_index("date").sort_index()
    df=m.join(m1,how="left")
    df["g_m2"]=100*np.log(df["M2SL"]).diff(12)
    df["g_m1"]=100*np.log(df["M1SL"]).diff(12)
    df["pi_trail"]=100*np.log(df["CPIAUCSL"]).diff(12)
    df["regime"]=np.where(df["pi_trail"]>=THR,"high","low")
    df["cpi_fwd"]=100*np.log(df["CPIAUCSL"]).shift(-H)-100*np.log(df["CPIAUCSL"])
    df["pce_fwd"]=100*np.log(df["PCEPI"]).shift(-H)-100*np.log(df["PCEPI"])
    return df

def r2(y,X):
    s=pd.concat([y,X],axis=1).dropna()
    if len(s)<30: return None,len(s)
    m=sm.OLS(s.iloc[:,0],sm.add_constant(s.iloc[:,1:])).fit()
    return round(m.rsquared,3),len(s)

df=load()
pre=df[df.index<=pd.Timestamp("2019-09-01")]
table={}
for dep in ["cpi_fwd","pce_fwd"]:
    for reg in ["high","low"]:
        d=pre[pre.regime==reg]
        r_m1,n=r2(d[dep],d[["g_m1"]]); r_m2,_=r2(d[dep],d[["g_m2"]])
        table[f"{dep}_{reg}"]={"R2_M1":r_m1,"R2_M2":r_m2,"n":n}
json.dump(table,open("results/robustness_pce.json","w"),indent=2)
print(json.dumps(table,indent=2))

# figure: in-sample R2 by regime, M1(active proxy) vs M2(broad), CPI
labels=["High-inflation regime\n(trailing CPI \u2265 4%)","Low-inflation regime\n(trailing CPI < 4%)"]
r_m1=[table["cpi_fwd_high"]["R2_M1"],table["cpi_fwd_low"]["R2_M1"]]
r_m2=[table["cpi_fwd_high"]["R2_M2"],table["cpi_fwd_low"]["R2_M2"]]
x=np.arange(2); w=0.36
fig,ax=plt.subplots(figsize=(7.2,4.3))
b1=ax.bar(x-w/2,r_m1,w,label="M\u1D40 proxy (M1, transaction-active)",color="#2E6F9E")
b2=ax.bar(x+w/2,r_m2,w,label="Simple-sum M2 (broad)",color="#B0B7BF")
ax.set_ylabel("Out-of-12-month CPI inflation explained (R\u00B2)")
ax.set_title("Transaction-active money carries the goods-inflation signal\nin the high-inflation regime (US monthly, 1960\u20132019)")
ax.set_xticks(x); ax.set_xticklabels(labels); ax.legend(frameon=False,fontsize=9)
for b in list(b1)+list(b2):
    ax.text(b.get_x()+b.get_width()/2,b.get_height()+0.004,f"{b.get_height():.2f}",ha="center",fontsize=9)
ax.spines[["top","right"]].set_visible(False); ax.set_ylim(0,0.23)
plt.tight_layout(); plt.savefig("results/fig_regime_R2.png",dpi=140); print("figure saved")

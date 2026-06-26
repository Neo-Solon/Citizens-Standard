"""
Publication figures for Paper 7. Self-contained: recomputes the headline series
from the same formulas used in cs_engine.py and equa_model_v3.py so each figure
is independently reproducible. Saves PNGs to ../figures/.
"""
import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

NAVY="#1f3864"; BLUE="#2e75b6"; GOLD="#c08a1e"; RED="#a23b3b"; GREY="#888888"
plt.rcParams.update({"font.family":"DejaVu Sans","font.size":11,"axes.titlesize":11,"axes.spines.top":False,"axes.spines.right":False})

# ---- shared CS launch calibration ----
M2=22366.0; g_r=0.02; K1_agg=9.0
growth_budget=g_r*M2
kd=0.5
K3=kd*(growth_budget-K1_agg)

# ===== Fig A.1: dividend by inflation regime — CS vs bundled =====
fig,ax=plt.subplots(figsize=(7,4))
regimes=["Mode A\n(-1.6%)","Mode B\n(0%)","Mode C\n(+2%)","(+3%)"]
cs=[K3,K3,K3,K3]
bundled=[np.nan,0.0,0.02*M2,0.03*M2]   # bundled: only above-line issuance; deflation N/A
x=np.arange(len(regimes)); w=0.38
ax.bar(x-w/2,cs,w,label="Citizens Standard (K3, growth-funded)",color=BLUE)
ax.bar(x+w/2,bundled,w,label="Bundled system (inflation-funded)",color=GOLD)
ax.set_xticks(x); ax.set_xticklabels(regimes)
ax.set_ylabel("Annual citizen dividend ($B)")
ax.set_title("Holding zero costs nothing on the dividend")
for xi,v in zip(x-w/2,cs): ax.text(xi,v+10,f"${v:.0f}B",ha="center",fontsize=9,color=NAVY)
for xi,v in zip(x+w/2,bundled):
    if not np.isnan(v): ax.text(xi,v+10,f"${v:.0f}B",ha="center",fontsize=9,color=GOLD)
ax.legend(frameon=False,fontsize=9,loc="upper left")
fig.tight_layout(); fig.savefig("../figures/fig_A1_dividend.png",dpi=150); plt.close(fig)

# ===== EQUA machinery (relative-PPP layer; realistic wage lag) =====
T=40; t=np.arange(T+1); g={'H':0.030,'L':0.005}
benchHL=(1+g['H'])**(-t)/(1+g['L'])**(-t)
def H_lag(c,pi_path,k):
    P=np.ones(T+1); w=np.ones(T+1)
    for s in range(1,T+1):
        P[s]=P[s-1]*(1+pi_path[s-1])
        w[s]=w[s-1]*(1+g[c])*(1+(pi_path[s-1-k] if s-1-k>=0 else 0.0))
    return P/w
def dist(piH,piL,kH,kL): return ((H_lag('H',piH,kH)/H_lag('L',piL,kL))/benchHL-1)[-1]*100

# ===== Fig A.2: distortion vs common anchor level (heterogeneous stickiness 1 vs 4) =====
levels=np.array([0.0,0.005,0.01,0.015,0.02,0.025,0.03])
d=[dist(np.full(T,L),np.full(T,L),1,4) for L in levels]
fig,ax=plt.subplots(figsize=(7,4))
ax.axhline(0,color=GREY,lw=0.8)
ax.plot(levels*100,d,"o-",color=NAVY,lw=2)
ax.annotate("common zero:\ndistortion = 0",(0,0),xytext=(0.4,-3.2),fontsize=9,color=BLUE,
            arrowprops=dict(arrowstyle="->",color=BLUE))
ax.annotate(f"common +3%:\n{d[-1]:.1f}%",(3,d[-1]),xytext=(1.7,d[-1]+1.2),fontsize=9,color=RED,
            arrowprops=dict(arrowstyle="->",color=RED))
ax.set_xlabel("Common anchor level (% inflation)"); ax.set_ylabel("Bilateral real-rate distortion (%)")
ax.set_title("Only a common zero removes the distortion (heterogeneous stickiness)")
fig.tight_layout(); fig.savefig("../figures/fig_A2_anchor_level.png",dpi=150); plt.close(fig)

# ===== Fig A.3: cumulative excess price level over 40y, corridor+3% vs zero, by baseline =====
def excess(level,base):
    # excess price level of a +level economy vs a baseline-drift economy over 40y
    return ((1+level)**40/(1+base)**40-1)*100
bases=[("vs 0%",0.0),("vs -1%",-0.01),("vs -2%",-0.02)]
corr=[excess(0.03,b) for _,b in bases]; zero=[excess(0.0,b) for _,b in bases]
x=np.arange(len(bases)); w=0.38
fig,ax=plt.subplots(figsize=(7,4))
ax.bar(x-w/2,corr,w,label="corridor +3%",color=GOLD)
ax.bar(x+w/2,zero,w,label="common zero",color=BLUE)
ax.set_xticks(x); ax.set_xticklabels([b[0] for b in bases]); ax.set_ylabel("Excess price level over 40y (%)")
ax.set_title("Cost of a positive anchor: cumulative excess price level")
for xi,v in zip(x-w/2,corr): ax.text(xi,v+8,f"+{v:.0f}%",ha="center",fontsize=9,color=GOLD)
for xi,v in zip(x+w/2,zero): ax.text(xi,v+8,f"+{v:.0f}%",ha="center",fontsize=9,color=NAVY)
ax.legend(frameon=False,fontsize=9); fig.tight_layout(); fig.savefig("../figures/fig_A3_cost.png",dpi=150); plt.close(fig)

# ===== Fig A.4: contraction — bond sterilization stock vs retired surcharge =====
yrs=np.arange(0,41); drift=0.03; gdp_g=0.03
def bond_stock(r):
    b=np.zeros(len(yrs))
    for i in range(1,len(yrs)):
        b[i]=b[i-1]*(1+r)/(1+gdp_g)+drift   # withdraw drift*GDP each yr, financed by interest-bearing debt
    return b*100
fig,ax=plt.subplots(figsize=(7,4))
ax.plot(yrs,bond_stock(0.01),color=BLUE,lw=2,label="bond sterilization, r<g (1%)")
ax.plot(yrs,bond_stock(0.03),color=GOLD,lw=2,label="bond sterilization, r=g (3%)")
ax.plot(yrs,bond_stock(0.05),color=RED,lw=2,label="bond sterilization, r>g (5%)")
ax.axhline(0,color=NAVY,lw=2,ls="--",label="retired surcharge (no stock; bounded drag)")
ax.set_xlabel("Year"); ax.set_ylabel("Accumulated sterilization stock (% of GDP)")
ax.set_title("Retiring money vs sterilizing it")
ax.legend(frameon=False,fontsize=8.5,loc="upper left"); fig.tight_layout()
fig.savefig("../figures/fig_A4_contraction.png",dpi=150); plt.close(fig)

print("figures written:")
for f in ["fig_A1_dividend","fig_A2_anchor_level","fig_A3_cost","fig_A4_contraction"]:
    print(f"  ../figures/{f}.png")
print(f"\nkey values: K3 dividend ${K3:.0f}B (flat); growth budget ${growth_budget:.0f}B; "
      f"+3% distortion {d[-1]:.1f}%; corridor cost vs 0% +{corr[0]:.0f}%")

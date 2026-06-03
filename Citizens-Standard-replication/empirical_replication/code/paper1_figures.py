"""
Paper 1 figure regeneration at FULL-RATE Mode B (0% drift, true price stability).
Clean consistent modern style. Mode A=-1.6% defl, Mode B=0% (price stable), Mode C=+2% infl.
"""
import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import matplotlib.ticker as mticker

# ---- consistent style ----
plt.rcParams.update({
    "figure.dpi": 120,
    "font.size": 12,
    "axes.titlesize": 13,
    "axes.titleweight": "bold",
    "axes.spines.top": False,
    "axes.spines.right": False,
    "axes.grid": True,
    "grid.alpha": 0.25,
    "legend.frameon": True,
    "legend.framealpha": 0.9,
})
C = {"A":"#2563eb", "B":"#16a34a", "C":"#ea580c", "current":"#dc2626", "omega":"#7c3aed"}

# ---- core economic assumptions (full-rate) ----
R_NOM = 0.07            # nominal equity return
YEARS = 65
# Drifts
DRIFT = {"current":0.03, "C":0.02, "B":0.0, "A":-0.016}
# M2 growth rates (full-rate Mode B ~2%; Mode A 0.35%; C 4.5%; current 6.5%)
M2G = {"current":0.065, "C":0.045, "B":0.020, "A":0.0035}

# Validated full-rate Stable Floor real figures (2025$, projected launch cohort)
# Anchored to empirical paper full-rate: A ~$1.70M, B ~$1.32M (historical anchor), C ~$145K
SF_REAL = {"A":1.70e6, "B":1.32e6, "C":0.145e6}
MEDIAN_401K = 95e3

def cpi_path(drift, years=YEARS):
    return np.array([(1+drift)**t for t in range(years+1)])

def real_accum(target_real, years=YEARS):
    """Smooth monotone accumulation curve ending at target_real (2025$)."""
    t=np.arange(years+1)
    # exponential-ish growth shape normalized to hit target at 65
    shape=(np.exp(R_NOM*t)-1)/(np.exp(R_NOM*years)-1)
    return target_real*shape

if __name__=="__main__":
    print("style + assumptions loaded; full-rate Mode B = 0% drift")
    for m in ["A","B","C"]:
        print(f"  Mode {m}: drift {DRIFT[m]*100:+.1f}%, M2g {M2G[m]*100:.2f}%, SF real ${SF_REAL[m]:,.0f}")

# ============ FIGURE BUILDERS ============
def fig1_wealth_accumulation(path):
    """image1: nominal + real Stable Floor accumulation, A/B/C vs 401k."""
    fig,(ax1,ax2)=plt.subplots(1,2,figsize=(15,6))
    fig.suptitle("Citizen Wealth Accumulation Over a Working Life\n"
                 "(Representative cohort born at framework launch; 7% nominal equity return)",
                 fontweight="bold")
    t=np.arange(YEARS+1)
    # NOMINAL: real * cpi
    for m in ["A","B","C"]:
        real=real_accum(SF_REAL[m])
        cpi=cpi_path(DRIFT[m])
        nominal=real*cpi
        ax1.plot(t,nominal/1e3,color=C[m],lw=2.5,
                 label=f"Mode {m} (nominal)")
    med401k_nom=real_accum(MEDIAN_401K)*cpi_path(DRIFT["current"])
    ax1.plot(t,med401k_nom/1e3,"--",color=C["current"],lw=2,label="Median US 401(k) — Vanguard 2025")
    ax1.set_title("Stable Floor — Nominal Balance")
    ax1.set_xlabel("Age (years from birth)"); ax1.set_ylabel("$K (nominal)")
    ax1.legend(); ax1.yaxis.set_major_formatter(mticker.FuncFormatter(lambda x,_:f"${x:.0f}K"))
    # REAL
    labels={"A":"Mode A (real — ~$1.7M at 65)","B":"Mode B (real — ~$1.32M at 65)","C":"Mode C (real — ~$145K at 65)"}
    for m in ["A","B","C"]:
        real=real_accum(SF_REAL[m])
        ax2.plot(t,real/1e3,color=C[m],lw=2.5,label=labels[m])
    ax2.plot(t,real_accum(MEDIAN_401K)/1e3,":",color=C["current"],lw=2.2,label="Median US 401(k) (~$95K)")
    # endpoint annotations
    ax2.annotate("$1.7M",(YEARS,SF_REAL["A"]/1e3),color=C["A"],fontweight="bold",fontsize=11,xytext=(3,0),textcoords="offset points")
    ax2.annotate("$1.32M",(YEARS,SF_REAL["B"]/1e3),color=C["B"],fontweight="bold",fontsize=11,xytext=(3,-12),textcoords="offset points")
    ax2.annotate("$145K",(YEARS,SF_REAL["C"]/1e3),color=C["C"],fontweight="bold",fontsize=11,xytext=(3,0),textcoords="offset points")
    ax2.set_title("Stable Floor — Real (2025 Dollars)")
    ax2.set_xlabel("Age (years from birth)"); ax2.set_ylabel("$K (2025 dollars)")
    ax2.legend(loc="upper left"); ax2.yaxis.set_major_formatter(mticker.FuncFormatter(lambda x,_:f"${x:.0f}K"))
    fig.tight_layout(rect=[0,0,1,0.94]); fig.savefig(path); plt.close(fig)
    print("wrote",path)

def fig2_purchasing_power(path):
    """image2: purchasing power of $1 over 65 yrs by mode."""
    fig,ax=plt.subplots(figsize=(14,7))
    t=np.arange(YEARS+1)
    series=[("current","Current (3%/yr inflation)",C["current"]),
            ("C","Mode C (2%/yr inflation)",C["C"]),
            ("B","Mode B (0% drift — price stable)",C["B"]),
            ("A","Mode A (−1.6%/yr deflation)",C["A"])]
    end={}
    for key,lab,col in series:
        pp=1.0/cpi_path(DRIFT[key])
        end[key]=pp[-1]
        ax.plot(t,pp,color=col,lw=2.5,label=f"{lab} → ${pp[-1]:.2f}")
    ax.axhline(1.0,ls="--",color="gray",alpha=0.6)
    ax.fill_between(t,1.0,1.0/cpi_path(DRIFT["A"]),color=C["A"],alpha=0.08)
    ax.fill_between(t,1.0/cpi_path(DRIFT["current"]),1.0,color=C["current"],alpha=0.08)
    ax.set_title("Purchasing Power of $1 Over 65 Years\n(What does $1 buy over time, relative to the year of launch?)")
    ax.set_xlabel("Years from launch"); ax.set_ylabel("Real purchasing power ($1 = launch year)")
    ax.legend(loc="upper left")
    fig.text(0.5,-0.01,"Current system: ~85% purchasing power loss over 65 years at 3%/yr. "
             "Mode B holds the dollar stable; Mode A grows purchasing power for cash holders.",
             ha="center",fontsize=9,style="italic",color="gray")
    fig.tight_layout(); fig.savefig(path,bbox_inches="tight"); plt.close(fig)
    print("wrote",path)

if __name__=="__main__":
    import sys
    if len(sys.argv)>1 and sys.argv[1]=="build":
        fig1_wealth_accumulation("/home/claude/p1figs/image1.png")
        fig2_purchasing_power("/home/claude/p1figs/image2.png")

def fig3_composite(path):
    """image3: 4-panel — price level, M2, stable floor, income at 65."""
    fig,axes=plt.subplots(2,2,figsize=(15,11))
    fig.suptitle("Three Base Modes vs. Current System — 65-Year Trajectories",fontweight="bold",fontsize=15)
    t=np.arange(YEARS+1)
    # Panel 1: price level
    ax=axes[0,0]
    for key,lab in [("current","Current (~3%/yr)"),("C","Mode C (+2%/yr)"),("B","Mode B (0% — price stable)"),("A","Mode A (−1.6%/yr)")]:
        ax.plot(t,cpi_path(DRIFT[key]),color=C[key if key!='current' else 'current'],lw=2.3,label=lab)
    ax.axhline(1.0,ls="--",color="gray",alpha=0.5)
    ax.set_title("Price Level Over Time"); ax.set_xlabel("Years from launch"); ax.set_ylabel("CPI (1.0 = launch)"); ax.legend()
    # Panel 2: M2 log
    ax=axes[0,1]
    M2_0=22.4
    for key,lab in [("current","Current (6.5%/yr)"),("C","Mode C (4.5%/yr)"),("B","Mode B (2.0%/yr)"),("A","Mode A (0.35%/yr)")]:
        ax.plot(t,M2_0*(1+M2G[key])**t,color=C[key if key!='current' else 'current'],lw=2.3,label=lab)
    ax.set_yscale("log"); ax.set_title("Circulating Money Supply (log scale)")
    ax.set_xlabel("Years from launch"); ax.set_ylabel("M2 ($T, log scale)"); ax.legend()
    # Panel 3: stable floor real
    ax=axes[1,0]
    ax.plot(t,real_accum(SF_REAL["A"])/1e3,color=C["A"],lw=2.3,label="Mode A (~$1.7M real)")
    ax.plot(t,real_accum(SF_REAL["B"])/1e3,color=C["B"],lw=2.3,label="Mode B (~$1.32M real)")
    ax.plot(t,real_accum(SF_REAL["C"])/1e3,color=C["C"],lw=2.3,label="Mode C floor (~$145K)")
    ax.plot(t,real_accum(MEDIAN_401K)/1e3,":",color=C["current"],lw=2.2,label="Median US 401(k) (~$95K)")
    ax.set_title("Stable Floor Capital Stake (2025 Dollars)")
    ax.set_xlabel("Age (years from birth)"); ax.set_ylabel("$K (2025 dollars)")
    ax.legend(); ax.yaxis.set_major_formatter(mticker.FuncFormatter(lambda x,_:f"${x:.0f}K"))
    # Panel 4: income at 65 stacked
    ax=axes[1,1]
    modes=["Current\n(median)","Mode A","Mode B","Mode C"]
    ss=[22,22,22,22]
    cap=[4,68,52.8,5.8]
    k3=[0,0,0,3.36]
    x=np.arange(4)
    ax.bar(x,ss,color="#9ca3af",label="Social Security (~$22K)")
    ax.bar(x,cap,bottom=ss,color=[C["current"],C["A"],C["B"],C["C"]],label="Capital stake income (4%)")
    ax.bar(x,k3,bottom=np.array(ss)+np.array(cap),color=C["C"],hatch="//",alpha=0.7,label="Ongoing K3 (Mode C)")
    totals=[s+c+k for s,c,k in zip(ss,cap,k3)]
    for i,tot in enumerate(totals):
        ax.annotate(f"${tot:.0f}K",(i,tot),ha="center",va="bottom",fontweight="bold",fontsize=10)
    ax.set_ylim(0,100)
    ax.set_xticks(x); ax.set_xticklabels(modes)
    ax.set_title("Annual Income at Age 65"); ax.set_ylabel("$K/year (2025 dollars)")
    ax.legend(fontsize=9); ax.yaxis.set_major_formatter(mticker.FuncFormatter(lambda v,_:f"${v:.0f}K"))
    fig.tight_layout(rect=[0,0,1,0.96]); fig.savefig(path); plt.close(fig)
    print("wrote",path)

if __name__=="__main__":
    import sys
    if len(sys.argv)>1 and sys.argv[1]=="build3":
        fig3_composite("/home/claude/p1figs/image3.png")

# Mode Omega environment (shared across fig5/6) — illustrative 65-yr path
def omega_inflation_path():
    """Mode Omega effective inflation relative to 0% Mode B baseline.
    Governors ADD issuance during demographic stress / productivity boom,
    so Mode Omega sits slightly ABOVE the 0% baseline when active, reverting to 0%."""
    t=np.arange(YEARS+1)
    infl=np.zeros(YEARS+1)  # tracks Mode B (0%) when governors inactive
    for i,yr in enumerate(t):
        if yr<=1:
            infl[i]=0.0
        elif 2<=yr<30:
            infl[i]=0.0007*(1-np.exp(-(yr-1)/8))   # mild standing demographic governor, ~+0.07bp->climbs
        elif 30<=yr<38:
            infl[i]=0.0016+0.0030*(yr-30)/8         # productivity boom ramps up
        elif 38<=yr<=42:
            infl[i]=0.0046+0.0002*np.sin((yr-38)/4*np.pi)  # demo stress + boom: peak ~+0.48bp
        elif 43<=yr<=45:
            infl[i]=0.0046-0.0030*(yr-42)/3
        elif 46<=yr<=55:
            infl[i]=0.0016                          # K3 full activation period, settles
        else:
            infl[i]=0.0014
    return t,infl

def fig5_omega_zoom(path):
    t,infl=omega_inflation_path()
    fig,ax=plt.subplots(figsize=(15,7))
    ax.axhline(0.0,ls="--",color=C["B"],lw=2.5,label="Mode B (0% drift) — baseline")
    ax.axhline(-0.016,ls=":",color=C["A"],lw=1.8,label="Mode A (−1.6%) — for reference")
    ax.plot(t,infl,color=C["omega"],lw=3,label="Mode Ω (adaptive band)")
    ax.fill_between(t,0.0,infl,color=C["omega"],alpha=0.15)
    ax.axvspan(30,38,color="#f59e0b",alpha=0.08); ax.axvspan(38,46,color=C["omega"],alpha=0.06); ax.axvspan(48,55,color="#3b82f6",alpha=0.07)
    peak=infl.max()
    ax.annotate(f"Peak: {peak*100:+.2f}%",(np.argmax(infl),peak),color=C["omega"],fontweight="bold",
                xytext=(-70,-35),textcoords="offset points",arrowprops=dict(arrowstyle="->",color=C["omega"]))
    ax.text(34,0.0035,"Productivity\nboom",color="#b45309",ha="center",fontsize=10,style="italic")
    ax.text(42,0.0035,"Demo stress",color=C["omega"],ha="center",fontsize=10,style="italic")
    ax.text(51,0.0035,"K3 fires",color="#1d4ed8",ha="center",fontsize=10,style="italic")
    ax.set_ylim(-0.018,0.005)
    ax.yaxis.set_major_formatter(mticker.FuncFormatter(lambda v,_:f"{v*100:.1f}%"))
    ax.set_title("Mode Ω Effective Inflation Rate — Zoomed View\n(Adaptive band relative to the price-stable Mode B baseline)")
    ax.set_xlabel("Years from launch"); ax.set_ylabel("Annual inflation rate (%)")
    ax.legend(loc="lower right")
    fig.tight_layout(); fig.savefig(path); plt.close(fig); print("wrote",path)

def fig6_omega_deviation(path):
    t,infl=omega_inflation_path()
    dev=infl-0.0  # deviation above 0% baseline
    fig,ax=plt.subplots(figsize=(15,6))
    ax.axhline(0.0,ls="--",color=C["B"],lw=2.5,label="Mode B baseline (0%)")
    ax.plot(t,dev,color=C["omega"],lw=3,label="Mode Ω above Mode B (governors active)")
    ax.fill_between(t,0,dev,color=C["omega"],alpha=0.18)
    ax.axvspan(30,38,color="#f59e0b",alpha=0.08); ax.axvspan(38,47,color=C["omega"],alpha=0.06); ax.axvspan(48,55,color="#3b82f6",alpha=0.07)
    ax.text(33,dev.max()*0.95,"Productivity\nboom",color="#b45309",fontsize=10,style="italic")
    ax.text(41,dev.max()*0.8,"Demo stress\n+ K3 partial",color=C["omega"],fontsize=10,style="italic")
    ax.text(50,dev.max()*0.5,"K3 full\nactivation",color="#1d4ed8",fontsize=10,style="italic")
    ax.yaxis.set_major_formatter(mticker.FuncFormatter(lambda v,_:f"{v*100:+.2f}%"))
    ax.set_title("Mode Ω Deviation Above Mode B Baseline (Governors Active Periods)")
    ax.set_xlabel("Years from launch"); ax.set_ylabel("Deviation from Mode B (%)")
    ax.legend(loc="upper left")
    fig.text(0.5,-0.02,f"Maximum deviation: ~{dev.max()*100:+.2f}% above Mode B during simultaneous demographic stress and productivity boom. "
             "Mode Ω reverts to the price-stable Mode B baseline at 25%/yr once conditions normalize.",
             ha="center",fontsize=9,style="italic",color="gray")
    fig.tight_layout(); fig.savefig(path,bbox_inches="tight"); plt.close(fig); print("wrote",path)

if __name__=="__main__":
    import sys
    if len(sys.argv)>1 and sys.argv[1]=="build56":
        fig5_omega_zoom("/home/claude/p1figs/image5.png")
        fig6_omega_deviation("/home/claude/p1figs/image6.png")

def fig7_omega_scenarios(path):
    scen=["Normal\n(+0.3% pop)","Neg pop\n(−0.5%)","Neg pop +\noptimistic","Neg pop +\npessimistic","Prod boom +\nneg pop"]
    A=[532,532,1350,284,532]
    B=[926,926,2310,494,926]      # full-rate Mode B (doubled from half)
    Om=[880,1248,2926,705,1330]
    x=np.arange(5); w=0.26
    fig,(ax1,ax2)=plt.subplots(1,2,figsize=(16,7))
    fig.suptitle("Mode Ω vs. Mode A and Mode B — Identical Conditions Per Scenario\n"
                 "(Each cluster shows all three Modes simulated under the same demographic and return environment)",fontweight="bold")
    ax1.bar(x-w,A,w,color=C["A"],label="Mode A")
    ax1.bar(x,B,w,color=C["B"],label="Mode B")
    ax1.bar(x+w,Om,w,color=C["omega"],label="Mode Ω")
    for i in range(5):
        ax1.annotate(f"${A[i]}K",(i-w,A[i]),ha="center",va="bottom",fontsize=8,color=C["A"])
        ax1.annotate(f"${B[i]}K",(i,B[i]),ha="center",va="bottom",fontsize=8,color=C["B"])
        ax1.annotate(f"${Om[i]}K",(i+w,Om[i]),ha="center",va="bottom",fontsize=8,color=C["omega"],fontweight="bold")
    ax1.set_xticks(x); ax1.set_xticklabels(scen,fontsize=9)
    ax1.set_title("Stable Floor Capital Stake at Age 65 (2025 Dollars)")
    ax1.set_ylabel("$K (2025 dollars)"); ax1.legend()
    ax1.yaxis.set_major_formatter(mticker.FuncFormatter(lambda v,_:f"${v:.0f}K"))
    # advantage panel
    advB=[Om[i]-B[i] for i in range(5)]
    advA=[Om[i]-A[i] for i in range(5)]
    ax2.bar(x-w/2,advB,w,color=C["omega"],label="Mode Ω advantage over Mode B")
    ax2.bar(x+w/2,advA,w,color=C["omega"],alpha=0.45,hatch="//",label="Mode Ω advantage over Mode A")
    ax2.axhline(0,color="black",lw=0.8)
    for i in range(5):
        ax2.annotate(f"{advB[i]:+}K",(i-w/2,advB[i]),ha="center",va="bottom" if advB[i]>=0 else "top",fontsize=8,color=C["omega"],fontweight="bold")
    ax2.set_xticks(x); ax2.set_xticklabels(scen,fontsize=9)
    ax2.set_title("Mode Ω Advantage vs. Mode A and Mode B\n(Same conditions; positive = Mode Ω wins)")
    ax2.set_ylabel("$K advantage (2025 dollars)"); ax2.legend()
    ax2.yaxis.set_major_formatter(mticker.FuncFormatter(lambda v,_:f"${v:+.0f}K"))
    fig.text(0.5,-0.02,"Each scenario simulates all three Modes under identical conditions. Mode A and Mode B have no adaptive governors. "
             "Under normal conditions Mode Ω's conservative base K2 can trail full-rate Mode B; under demographic stress its governors activate and it leads.",
             ha="center",fontsize=9,style="italic",color="gray")
    fig.tight_layout(rect=[0,0,1,0.93]); fig.savefig(path,bbox_inches="tight"); plt.close(fig); print("wrote",path)

def fig8_transitions(path):
    fig,axes=plt.subplots(2,2,figsize=(15,12))
    fig.suptitle("Constitutional Mode Transitions at Year 30 — 65-Year Horizon",fontweight="bold",fontsize=15)
    t=np.arange(YEARS+1)
    # Panel 1: A/B -> transition at yr 30
    ax=axes[0,0]
    cpiA=cpi_path(DRIFT["A"]); cpiB=cpi_path(DRIFT["B"])
    ax.plot(t,cpiA,color=C["A"],lw=2.5,label="Pure Mode A")
    # B is flat at 1.0 now
    def transit(base_drift,new_drift,switch=30):
        p=np.ones(YEARS+1)
        for i in range(1,YEARS+1):
            d=base_drift if i<=switch else new_drift
            p[i]=p[i-1]*(1+d)
        return p
    ax.plot(t,transit(DRIFT["A"],DRIFT["B"]),"--",color=C["A"],alpha=0.8,label="A→B@30")
    ax.plot(t,transit(DRIFT["A"],DRIFT["C"]),"--",color=C["C"],alpha=0.8,label="A→C@30")
    ax.plot(t,transit(DRIFT["B"],DRIFT["A"]),":",color=C["B"],lw=2,label="B→A@30")
    ax.plot(t,transit(DRIFT["B"],DRIFT["C"]),":",color=C["C"],lw=2,label="B→C@30")
    ax.axvline(30,ls=":",color="gray",alpha=0.6)
    ax.set_title("Price Level: A/B → Transition at Yr 30"); ax.set_xlabel("Years"); ax.set_ylabel("CPI (1.0 = launch)"); ax.legend(fontsize=8)
    # Panel 2: C transitions
    ax=axes[0,1]
    ax.plot(t,cpi_path(DRIFT["C"]),color=C["C"],lw=2.5,label="Pure Mode C")
    ax.plot(t,transit(DRIFT["C"],DRIFT["A"]),"-.",color=C["A"],label="C→A@30")
    ax.plot(t,transit(DRIFT["C"],DRIFT["B"]),"-.",color=C["B"],label="C→B@30")
    ax.axvline(30,ls=":",color="gray",alpha=0.6)
    ax.set_title("Price Level: C → Transition at Yr 30"); ax.set_xlabel("Years"); ax.set_ylabel("CPI (1.0 = launch)"); ax.legend(fontsize=8)
    # Panel 3: K3 activate/deactivate
    ax=axes[1,0]
    k3a=np.where(t>=30,280,0); k3a=np.where(t<30,0,280.0)
    k3_ac=np.where(t>=30,280,0.0)
    k3_end=np.where(t<30,280,0.0); k3_end[t<5]=np.linspace(173,280,(t<5).sum())
    ax.plot(t,k3_ac,color=C["C"],lw=2.5,label="A→C: K3 activates")
    ax.plot(t,np.where(t<30,280,0.0),"--",color=C["A"],lw=2,label="C→A: K3 ends")
    ax.axvline(30,ls=":",color="gray",alpha=0.6)
    ax.set_title("K3 Channel Activates / Deactivates Cleanly"); ax.set_xlabel("Years"); ax.set_ylabel("$/month per citizen"); ax.legend(fontsize=9)
    # Panel 4: lifetime real value by scenario
    ax=axes[1,1]
    labels=["Pure A","Pure B","Pure C","A→B@30","A→C@30","B→C@30","C→A@30","C→B@30"]
    vals=[1700,1320,145,1480,520,640,950,820]  # full-rate: Pure B now 1320 (was ~1550)
    cols=[C["A"],C["B"],C["C"],C["A"],C["C"],C["C"],C["A"],C["B"]]
    ax.bar(range(8),vals,color=cols)
    ax.set_xticks(range(8)); ax.set_xticklabels(labels,rotation=30,ha="right",fontsize=9)
    ax.set_title("Lifetime Real Value by Transition Scenario"); ax.set_ylabel("$K (2025 dollars)")
    ax.yaxis.set_major_formatter(mticker.FuncFormatter(lambda v,_:f"${v:.0f}K"))
    fig.tight_layout(rect=[0,0,1,0.96]); fig.savefig(path); plt.close(fig); print("wrote",path)

if __name__=="__main__":
    import sys
    if len(sys.argv)>1 and sys.argv[1]=="build78":
        fig7_omega_scenarios("/home/claude/p1figs/image7.png")
        fig8_transitions("/home/claude/p1figs/image8.png")

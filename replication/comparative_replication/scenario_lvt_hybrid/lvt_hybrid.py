#!/usr/bin/env python3
"""
ILLUSTRATIVE SCENARIO — a worked Georgist-LVT / Citizens-Standard hybrid.

This is NOT part of the audited comparative replication. It rests on EXTERNAL, CONTESTED
estimates of US land rent (the conservative-to-aggressive spread is ~4x), so its outputs are
scenario illustrations, not measured results, and must not be read with the confidence of the
Paper-13 comparison tables. All inputs are stated with sources; the contested ones are flagged.

Produces five exhibits (figures/*.png) and prints the key magnitudes:
  1. Land-rent dividend potential vs the CS monetary dividend.
  2. Capitalization: the dividend rides the rent FLOW; the land PRICE collapses.
  3. The Mode-D hybrid that drops the equity buyer (and the wealth-stock tradeoff).
  4. Transition glide: a multi-decade phase-in; full reserve roughly halves the safe time.
  5. Land interaction: LVT and CS do not fight over land; LVT plugs CS's land leak.

Sources for inputs:
  - US land value ~$23T in 2009 (BEA, Larson 2015); Case (Lincoln Inst.) $34.7T (2005, developed+ag);
    grown through the 2012-2022 housing run -> ~$48T central (STATED ASSUMPTION, not a measured 2026 figure).
  - Land rent: Lincoln Inst. (Barker) ~13.6% of personal income; Georgist sources 20-40% of GDP (contested).
    Here the central rent is derived internally as R = i * land_value (capitalization identity), which is
    deliberately conservative and sidesteps the aggressive claims.
  - Land discount yield i ~5% (Baa-based, per Barker); current Baa ~6%; carried as a 4-6% assumption.
  - Real-estate sector ~2.5-3% of the broad US equity index (S&P DJI / GICS, 2026).
  - Real estate loans ~$5.76T of ~$12.5T total US bank loans = ~45% (FRED H.8, REALLN, Dec 2025).
  - CS monetary dividend $516-$1,293/person/yr; locked wealth floor $233k-$413k/person (Paper 13, verified).
  - CS buys a broad equity index in Modes A/B/C (build floors); Mode D (k_d=100%) buys NO index
    (engine presets; macro paper "buys no equity at all, A*=0"). Verified.
"""
import os, numpy as np
import matplotlib; matplotlib.use("Agg")
import matplotlib.pyplot as plt

HERE = os.path.dirname(os.path.abspath(__file__))
FIG  = os.path.join(HERE, "figures"); os.makedirs(FIG, exist_ok=True)
INK="#10161C"; AMBER="#E6A93E"; TEAL="#3FAE92"; DIM="#9AA3AE"; LAND="#8C6E4A"; RED="#C0563B"; SLATE="#5B6B7B"

# ---- shared anchors ----
POP=335e6; GDP=29.0e12; PI=24.0e12
i=0.05; LANDV0=48e12; R=i*LANDV0                 # internally-consistent fundamental rent ~ $2.4T (~8.3% GDP)
CS_div_lo, CS_div_hi = 516, 1293
CS_floor_lo, CS_floor_hi = 233000, 413000

def banner(t): print("\n"+"="*72+"\n"+t+"\n"+"="*72)

# ============ 1. land-rent dividend potential vs CS monetary dividend ============
banner("1. Land-rent dividend potential (LVT layer) vs CS monetary dividend")
KAP=0.70
scen={"conservative (4% yield on $40T land)":0.04*40e12,
      "central (Lincoln/Barker 13.6% personal income)":0.136*PI,
      "aggressive (Georgist ~20% of GDP)":0.20*GDP}
for k,v in scen.items():
    cap=v*KAP
    print(f"  {k:50s}: captured ${cap/1e12:.2f}T -> ${cap/POP:,.0f}/person/yr if fully distributed")
print(f"  CS monetary dividend (issuance): ${CS_div_lo:,}-${CS_div_hi:,}/person/yr "
      f"-> LVT layer is the larger, more efficient base.")

fig,ax=plt.subplots(figsize=(9,4.6))
labels=["conservative\n(~5.5% GDP)","central\n(13.6% pers.inc.)","aggressive\n(~20% GDP)"]
land=[scen[list(scen)[j]]*KAP/POP for j in range(3)]
ax.bar(range(3),land,0.6,color=LAND,label="land-rent dividend (LVT, 100% distributed)")
ax.bar(range(3),[CS_div_hi]*3,0.6,bottom=land,color=TEAL,label="CS monetary dividend (Mode D, top of range)")
for j,lv in enumerate(land):
    ax.text(j,lv/2,f"${lv:,.0f}",ha="center",va="center",color="white",fontsize=8.5)
    ax.text(j,lv+CS_div_hi+250,f"${lv+CS_div_hi:,.0f}",ha="center",fontsize=9,fontweight="bold",color=INK)
ax.set_xticks(range(3)); ax.set_xticklabels(labels,fontsize=8.5)
ax.set_ylabel("$ per person / year"); ax.set_title("1. Mode D hybrid: two dividend flows, no equity buyer",fontsize=10.5,color=INK)
ax.legend(fontsize=8,frameon=False,loc="upper left"); ax.spines[["top","right"]].set_visible(False)
fig.tight_layout(); fig.savefig(f"{FIG}/fig1_hybrid_dividend.png",dpi=140); plt.close(fig)

# ============ 2. capitalization ============
banner("2. Capitalization: dividend rides the rent flow; land price collapses")
tau=np.linspace(0,0.25,300); cap=tau/(i+tau); price=i/(i+tau); div=R*cap/POP; destroyed=LANDV0*(1-price)
for t in [0.02,0.05,0.10,0.20]:
    print(f"  LVT {t:.0%}: captures {t/(i+t):.0%} of rent, land price -> {i/(i+t):.0%} of pre-tax, "
          f"dividend ${R*(t/(i+t))/POP:,.0f}/person, land value destroyed ${LANDV0*(1-i/(i+t))/1e12:.0f}T")
fig,(a,b)=plt.subplots(1,2,figsize=(11,4.5))
a.plot(tau*100,cap*100,color=LAND,lw=2.2,label="rent captured (% of rent)")
a.plot(tau*100,price*100,color=RED,lw=2.2,ls="--",label="land price (% of pre-tax)")
a.set_xlabel("LVT rate on land value (%/yr)"); a.set_ylabel("%"); a.set_ylim(0,100)
a.set_title("2a. Revenue robust, land price collapses",fontsize=10,color=INK); a.legend(fontsize=8.3,frameon=False)
a.spines[["top","right"]].set_visible(False)
b2=b.twinx(); b.plot(tau*100,div,color=TEAL,lw=2.4); b2.plot(tau*100,destroyed/1e12,color=RED,lw=1.8,ls="--")
b.axhspan(CS_div_lo,CS_div_hi,color=DIM,alpha=0.16)
b.set_xlabel("LVT rate (%/yr)"); b.set_ylabel("dividend $/person/yr",color=TEAL)
b2.set_ylabel("land value destroyed $T",color=RED); b.set_ylim(0,6500); b2.set_ylim(0,45)
b.set_title("2b. Steady-state dividend vs transition shock",fontsize=10,color=INK)
b.spines[["top"]].set_visible(False); b2.spines[["top"]].set_visible(False)
fig.tight_layout(); fig.savefig(f"{FIG}/fig2_capitalization.png",dpi=140); plt.close(fig)

# ============ 3. transition glide ============
banner("3. Transition: a multi-decade glide; full reserve halves the safe time")
TAU_STAR=0.10; floor=i/(i+TAU_STAR)
def glide(d):
    T=int(np.ceil(np.log(floor)/np.log(1-d))); t=np.arange(0,T+1)
    return t, LANDV0*(1-d)**t, (1-(1-d)**t)*R/POP, T
for d,lab in [(0.02,"very gentle"),(0.03,"normal housing cycle"),(0.05,"brisk"),(0.07,"sharp-but-orderly")]:
    print(f"  {d:.0%}/yr land-price decline -> {int(np.ceil(np.log(floor)/np.log(1-d)))} years to full {TAU_STAR:.0%} LVT ({lab})")
print("  Fractional reserve tolerates ~2-3%/yr (money-contraction risk) -> ~30-50 yr;")
print("  CS full reserve tolerates ~5-7%/yr (credit losses only) -> ~15-21 yr. Roughly HALVES the safe time.")
fig,(a,b)=plt.subplots(1,2,figsize=(11.2,4.5))
for d,col,lab in [(0.05,TEAL,"CS full reserve 5%/yr"),(0.03,RED,"fractional reserve 3%/yr")]:
    t,V,dv,T=glide(d); a.plot(t,V/1e12,color=col,lw=2.2,label=f"{lab} (~{T} yr)")
a.set_xlabel("years into phase-in"); a.set_ylabel("US land value ($T)"); a.set_ylim(0,50)
a.set_title("3a. Land-price glide: full reserve halves the transition",fontsize=10,color=INK)
a.legend(fontsize=8.2,frameon=False); a.spines[["top","right"]].set_visible(False)
t,V,dv,T=glide(0.05); b2=b.twinx(); b.plot(t,dv,color=TEAL,lw=2.4); b2.plot(t,V/1e12,color=LAND,lw=1.8,ls="--")
b.axhspan(CS_div_lo,CS_div_hi,color=DIM,alpha=0.16)
b.set_xlabel("years (5%/yr glide)"); b.set_ylabel("dividend $/person/yr",color=TEAL); b2.set_ylabel("land value $T",color=LAND)
b.set_ylim(0,5500); b2.set_ylim(0,50); b.set_title("3b. Dividend phases up as land glides down",fontsize=10,color=INK)
b.spines[["top"]].set_visible(False); b2.spines[["top"]].set_visible(False)
fig.tight_layout(); fig.savefig(f"{FIG}/fig3_transition.png",dpi=140); plt.close(fig)

# ============ 4. land interaction ============
banner("4. Land interaction: LVT and CS do not fight over land")
alpha=0.7; dr=0.005
def land_index(d,t): return 100.0*(R/((i-alpha*d)+t))/(R/i)
base,cs,lvt,hyb,modeD = land_index(0,0),land_index(dr,0),land_index(0,TAU_STAR),land_index(dr,TAU_STAR),land_index(0,TAU_STAR)
print(f"  baseline {base:.0f} | CS alone {cs:.1f} (+{cs-base:.1f}% land LEAK) | LVT alone {lvt:.0f} | "
      f"hybrid {hyb:.1f} | Mode D {modeD:.0f}")
print(f"  LVT plugs ~{100*(1-(hyb-lvt)/(cs-base)):.0f}% of the land leak CS alone would create. REIT overlap ~1.5% of US land (Mode D removes it).")
fig,ax=plt.subplots(figsize=(8.6,4.7))
labs=["baseline","CS floor modes\n(equity bid)","LVT alone","Hybrid\n(floor + LVT)","Mode D\n(no equity bid)"]
vals=[base,cs,lvt,hyb,modeD]; cols=[DIM,RED,LAND,TEAL,"#2E7D5B"]
bb=ax.bar(labs,vals,color=cols,edgecolor=INK,lw=0.6,width=0.62)
for r,v in zip(bb,vals): ax.text(r.get_x()+r.get_width()/2,v+1.5,f"{v:.0f}",ha="center",fontsize=9.5,fontweight="bold",color=INK)
ax.axhline(100,color=DIM,ls=":",lw=1); ax.set_ylabel("US land price index (baseline=100)"); ax.set_ylim(0,135)
ax.set_title("4. LVT and CS are self-reinforcing on land (LVT plugs CS's land leak)",fontsize=10,color=INK)
ax.spines[["top","right"]].set_visible(False)
fig.tight_layout(); fig.savefig(f"{FIG}/fig4_land_interaction.png",dpi=140); plt.close(fig)

banner("DONE — figures in figures/. SCENARIO ONLY: contested land-rent inputs; not audited replication.")

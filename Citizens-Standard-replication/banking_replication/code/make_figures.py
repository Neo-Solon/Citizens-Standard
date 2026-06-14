import numpy as np, os
import matplotlib; matplotlib.use("Agg")
import matplotlib.pyplot as plt
INK="#1a1a2e"; WARM="#b0413e"; GOLD="#c08a2e"; GREEN="#3a6b4f"; GREY="#8a8a8a"; BLUE="#2E74B5"
plt.rcParams.update({"font.family":"serif","font.size":10,"axes.edgecolor":INK,"axes.linewidth":0.8})
def style(ax):
    for a in np.atleast_1d(ax).ravel():
        a.spines["top"].set_visible(False); a.spines["right"].set_visible(False); a.tick_params(labelsize=8.5)
OUT=os.path.join(os.path.dirname(__file__),"..","figures")

# ---------- Figure B1: effective transactional money & KI offset ----------
fig,ax=plt.subplots(1,2,figsize=(11,4.3))
D=np.linspace(0,2.4,200); d_T=0.5; Mstar=1.0
Mo=np.clip(Mstar-d_T*D,0,None); MT=Mo+d_T*D
a=ax[0]
a.plot(D,Mo,lw=2,color=BLUE,label="outside money $M_o$ (KI-set)")
a.plot(D,d_T*D,lw=2,color=GOLD,label="inside transactional $d_T D$")
a.plot(D,np.minimum(MT,Mstar),lw=2.4,color=INK,label="effective $M_T$ (on target)")
sat=Mstar/d_T
a.axvline(sat,color=WARM,ls="--",lw=1); a.text(sat-0.02,0.2,"KI saturates\n$d_T D=M^*$",color=WARM,fontsize=7.4,ha="right")
a.fill_between(D,0,1.05,where=(D>sat),color=WARM,alpha=.07)
a.set_xlim(0,2.4); a.set_ylim(0,1.25); a.set_xlabel("inside deposits $D$"); a.set_ylabel("money (target units)")
a.set_title("(a)  KI offsets inside money to hold $M_T$ on target",fontsize=10.5,color=INK,loc="left")
a.legend(fontsize=7.6,loc="upper left",frameon=False)
b=ax[1]
t=np.arange(24)
gap_total=0.6*0.85**t                                  # KI targets total M_T -> gap closes
gap_outside=0.6*0.85**t+0.04*np.cumsum(np.ones_like(t))*0.5  # KI ignores inside -> drift
b.plot(t,gap_total,lw=2.2,color=INK,label="KI targets total $M_T$")
b.plot(t,gap_outside,lw=2.0,color=WARM,ls="--",label="KI targets outside only")
b.axhline(0,color=GREY,lw=.6)
b.set_xlim(0,23); b.set_xlabel("periods"); b.set_ylabel("price-path gap")
b.set_title("(b)  Determinacy carries over only if KI targets the total",fontsize=10.5,color=INK,loc="left")
b.legend(fontsize=7.8,loc="upper right",frameon=False)
style(ax); fig.suptitle("B1 — The price level is set by total (outside + inside) transactional money",fontsize=11.5,color=INK,y=1.02)
fig.tight_layout(); fig.savefig(f"{OUT}/figure_B1_inside_money.png",dpi=200,bbox_inches="tight",facecolor="white"); plt.close(fig)

# ---------- Figure B2: bounded inside-money multiplier ----------
fig,ax=plt.subplots(1,2,figsize=(11,4.3))
k=0.08;rho=0.10;m=0.50;phi=0.15;E=0.10;Rb=0.12;W=4.0
caps={"capital\n$E/k$":E/k,"reserves\n$R_b/\\rho$":Rb/rho,"collateral\n$m\\,\\phi_{liq}W$":m*phi*W}
a=ax[0]; names=list(caps); vals=[caps[n] for n in names]; cols=[GREY,GREY,WARM]
a.bar(names,vals,color=cols,alpha=.85,width=.6)
a.axhline(min(vals),color=WARM,ls="--",lw=1); a.text(2.1,min(vals)+0.03,"binding (lock)",color=WARM,fontsize=7.6,ha="right")
a.set_ylabel("max lending $L$ (units of $M_o$)"); a.set_ylim(0,1.4)
a.set_title("(a)  Non-pledgeable floors make collateral bind",fontsize=10.5,color=INK,loc="left")
b=ax[1]; phis=np.linspace(0.05,1.0,200); Lmax=np.minimum(np.minimum(E/k,Rb/rho),m*phis*W); sigma=d_T*Lmax/(1+d_T*Lmax)
b.plot(phis,sigma,lw=2.2,color=INK)
b.axvline(0.15,color=GREEN,ls="--",lw=1); b.plot(0.15,d_T*min(E/k,Rb/rho,m*0.15*W)/(1+d_T*min(E/k,Rb/rho,m*0.15*W)),'o',color=GREEN,ms=7)
b.text(0.17,0.10,"locked\n$\\phi_{liq}\\approx0.15$\n$\\sigma\\approx0.13$",color=GREEN,fontsize=7.4)
b.set_xlim(0.05,1.0); b.set_ylim(0,0.5); b.set_xlabel("pledgeable fraction $\\phi_{liq}$"); b.set_ylabel("inside transactional share $\\sigma$")
b.set_title("(b)  Inside-money share is small and bounded",fontsize=10.5,color=INK,loc="left")
style(ax); fig.suptitle("B2 — Bank inside-money creation is bounded; the locked floors are the binding constraint",fontsize=11.3,color=INK,y=1.02)
fig.tight_layout(); fig.savefig(f"{OUT}/figure_B2_multiplier_bound.png",dpi=200,bbox_inches="tight",facecolor="white"); plt.close(fig)

# ---------- Figure B3/B4: KI controllability & macroprudential rule ----------
fig,ax=plt.subplots(1,2,figsize=(11,4.3))
a=ax[0]; beta=np.linspace(0.0,0.6,200); Dctrl=(1-beta)*Mstar/d_T
a.plot(beta,Dctrl,lw=2.2,color=INK)
a.fill_between(beta,0,Dctrl,color=GREEN,alpha=.10); a.fill_between(beta,Dctrl,4,color=WARM,alpha=.07)
a.text(0.30,0.6,"KI controllable",color=GREEN,fontsize=8.5); a.text(0.06,3.3,"KI saturates",color=WARM,fontsize=8.5)
a.plot(0.25,(1-0.25)/d_T,'o',color=BLUE,ms=7); a.text(0.27,1.7,"baseline buffer\n25%",color=BLUE,fontsize=7.4)
a.set_xlim(0,0.6); a.set_ylim(0,4); a.set_xlabel("shock-response buffer $\\beta$"); a.set_ylabel("max inside deposits $D$")
a.set_title("(a)  KI controllability frontier",fontsize=10.5,color=INK,loc="left")
b=ax[1]; Dc=(1-0.25)*Mstar/d_T; Es=np.linspace(0.02,0.20,200); kmin=Es/Dc
b.plot(Es,kmin,lw=2.2,color=BLUE)
b.fill_between(Es,kmin,0.16,color=GREEN,alpha=.10); b.fill_between(Es,0,kmin,color=WARM,alpha=.07)
b.text(0.12,0.11,"capital requirement\nkeeps KI in control",color=GREEN,fontsize=7.8)
b.text(0.13,0.018,"too lax",color=WARM,fontsize=8)
b.set_xlim(0.02,0.20); b.set_ylim(0,0.16); b.set_xlabel("bank equity $E$ (units of $M_o$)"); b.set_ylabel("required capital ratio $k$")
b.set_title("(b)  Macroprudential design rule  $k\\geq E/D^{ctrl}$",fontsize=10.5,color=INK,loc="left")
style(ax); fig.suptitle("B3–B4 — KI stays in control iff inside money is capped; the cap maps to a capital requirement",fontsize=11.0,color=INK,y=1.02)
fig.tight_layout(); fig.savefig(f"{OUT}/figure_B3B4_controllability.png",dpi=200,bbox_inches="tight",facecolor="white"); plt.close(fig)

# ---------- Figure B5: run-proof floor ----------
fig,ax=plt.subplots(1,2,figsize=(11,4.3))
a=ax[0]
a.bar(["Citizens Standard\n(locked floors)","conventional\n(all claims runnable)"],[1-phi,0.0],bottom=[phi,0],color=GREEN,alpha=.8,width=.55,label="run-proof (locked)")
a.bar(["Citizens Standard\n(locked floors)","conventional\n(all claims runnable)"],[phi,1.0],color=WARM,alpha=.7,width=.55,label="runnable (liquid)")
a.set_ylabel("share of citizen wealth"); a.set_ylim(0,1.05)
a.set_title("(a)  Most wealth is run-proof under the lock",fontsize=10.5,color=INK,loc="left")
a.legend(fontsize=7.8,loc="center right",frameon=False)
b=ax[1]; phis=np.linspace(0.0,1.0,200)
LOLR=d_T*np.minimum(np.minimum(E/k,Rb/rho),m*phis*W)
b.plot(phis,LOLR,lw=2.2,color=INK)
b.axvline(0.15,color=GREEN,ls="--",lw=1); b.plot(0.15,d_T*min(E/k,Rb/rho,m*0.15*W),'o',color=GREEN,ms=7)
b.text(0.17,0.05,"locked baseline\nLOLR need ≈0.15",color=GREEN,fontsize=7.4)
b.set_xlim(0,1.0); b.set_ylim(0,0.6); b.set_xlabel("pledgeable fraction $\\phi_{liq}$"); b.set_ylabel("max LOLR need (outside money)")
b.set_title("(b)  Run severity / LOLR need scales with liquid share",fontsize=10.5,color=INK,loc="left")
style(ax); fig.suptitle("B5 — Locked floors are run-proof: systemic run severity and LOLR need scale only with the small liquid share",fontsize=10.8,color=INK,y=1.02)
fig.tight_layout(); fig.savefig(f"{OUT}/figure_B5_runproof_floor.png",dpi=200,bbox_inches="tight",facecolor="white"); plt.close(fig)
print("wrote 4 figure files (B1,B2,B3-4,B5)")

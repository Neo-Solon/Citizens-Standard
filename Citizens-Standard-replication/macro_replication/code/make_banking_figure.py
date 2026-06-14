"""
make_banking_figure.py
----------------------
Reproduces figure_P9_banking_separation.png for Section 3.8 / Proposition 9 /
Appendix A.12 of Neo-Solon (2026e): separation region, the critical-LTV/lock
relation, and the two-safeguard eigenvalue plot.
"""
import numpy as np, os
import matplotlib; matplotlib.use("Agg")
import matplotlib.pyplot as plt
INK="#1a1a2e"; WARM="#b0413e"; GOLD="#c08a2e"; GREEN="#3a6b4f"; GREY="#8a8a8a"
r=0.045; a=1/(1+r); theta=1+(1+0.5)/4.0
lam=0.03; chi_c=0.30; zstar=0.127; kbc=(zstar-lam)/chi_c
def nexp(z,b):
    M=np.array([[theta,-z],[-b/a,1/a]]); return np.sum(np.abs(np.linalg.eigvals(M))>1+1e-12)
plt.rcParams.update({"font.family":"serif","font.size":10,"axes.edgecolor":INK,"axes.linewidth":0.8})
fig,ax=plt.subplots(1,3,figsize=(15,4.6))

# (a) separation region in (credit intensity, spend-through)
a0=ax[0]; kb=np.linspace(0,0.6,300)
chic_b=(zstar-lam)/np.maximum(kb,1e-6)        # boundary chi_c*kb=zstar-lam
a0.fill_between(kb,0,np.minimum(chic_b,1.0),color=GREEN,alpha=.10)
a0.plot(kb,np.clip(chic_b,0,1.0),lw=2,color=INK)
a0.text(0.07,0.18,"separation intact\n($\\lambda+\\chi_c\\,m\\phi_{liq}<\\zeta^*$)",fontsize=8,color=GREEN)
a0.text(0.40,0.62,"circuits re-mix",fontsize=8.5,color=WARM)
a0.plot(0.075,0.30,'o',color=GREEN,ms=8,zorder=5); a0.annotate("locked\nbaseline",(0.075,0.30),(0.13,0.42),fontsize=7.6,color=GREEN,arrowprops=dict(arrowstyle="->",color=GREEN,lw=.8))
a0.plot(0.50,0.30,'s',color=WARM,ms=8,zorder=5); a0.annotate("no-lock\n($\\phi_{liq}=1$)",(0.50,0.30),(0.40,0.12),fontsize=7.6,color=WARM,arrowprops=dict(arrowstyle="->",color=WARM,lw=.8))
a0.set_xlim(0,0.6); a0.set_ylim(0,1.0)
a0.set_xlabel(r"credit intensity  $\kappa_{bank}=m\,\phi_{liq}$"); a0.set_ylabel(r"consumption spend-through  $\chi_c$")
a0.set_title("(a)  Where bank credit keeps the circuits separate",fontsize=11,color=INK,loc="left")

# (b) critical LTV vs liquid fraction (the lock)
b=ax[1]; phi=np.linspace(0.05,1.0,300); mstar=kbc/phi
b.plot(phi,mstar,lw=2.2,color=INK)
b.axhspan(0,1,color=GREY,alpha=.08); b.axhline(1,color=GREY,lw=.8,ls=":")
b.fill_between(phi,np.minimum(mstar,1.0),1.0,where=(mstar<1.0),color=WARM,alpha=.10)
b.text(0.55,0.45,"separation breaks\n(feasible LTV $\\geq m^*$)",fontsize=7.8,color=WARM)
b.text(0.12,2.6,"no feasible LTV\nbreaks separation",fontsize=7.8,color=GREEN)
b.axvline(0.15,color=GREEN,lw=.9,ls="--"); b.plot(0.15,kbc/0.15,'o',color=GREEN,ms=7)
b.text(0.165,2.9,"locked\n$\\phi_{liq}\\approx0.15$",fontsize=7.4,color=GREEN)
b.axvline(1.0,color=WARM,lw=.9,ls="--"); b.plot(1.0,kbc,'s',color=WARM,ms=7)
b.text(0.80,0.55,"no lock\n$m^*=%.2f$"%kbc,fontsize=7.4,color=WARM)
b.set_xlim(0.05,1.0); b.set_ylim(0,3.5)
b.set_xlabel(r"pledgeable (liquid) fraction  $\phi_{liq}$"); b.set_ylabel(r"critical loan-to-value  $m^*$")
b.set_title("(b)  The lock is decisive: locked floors aren't pledgeable",fontsize=11,color=INK,loc="left")

# (c) two safeguards: eigenvalue vs credit intensity
c=ax[2]; kbs=np.linspace(0,2.0,400)
def smalleig(z,bb):
    M=np.array([[theta,-z],[-bb/a,1/a]]); return sorted(np.abs(np.linalg.eigvals(M)))[0]
cons=[smalleig(lam+chi_c*k, lam+chi_c*k) for k in kbs]      # accelerator on (symmetric)
sbuy=[smalleig(lam+chi_c*k, lam) for k in kbs]              # accelerator damped
c.plot(kbs,cons,lw=1.9,color=WARM,label="accelerator on (conservative)")
c.plot(kbs,sbuy,lw=1.9,color=GREEN,label="structural buyer damps accelerator")
c.axhline(1,color=GREY,lw=1.0,ls=":")
c.axvline(0.075,color=INK,lw=.9,ls="--"); c.text(0.10,0.955,"locked\nbaseline\n0.075",fontsize=7.0,color=INK)
c.plot(kbc,1,'o',color=WARM,ms=6); c.text(kbc-0.02,1.006,"%.2f"%kbc,fontsize=7.2,color=WARM,ha="right")
c.plot(1.694,1,'o',color=GREEN,ms=6); c.text(1.694,1.006,"1.69",fontsize=7.2,color=GREEN)
c.set_xlim(0,2.0); c.set_ylim(0.93,1.06)
c.set_xlabel(r"credit intensity  $\kappa_{bank}=m\,\phi_{liq}$"); c.set_ylabel("smaller eigenvalue modulus")
c.set_title("(c)  Two independent safeguards on separation",fontsize=11,color=INK,loc="left")
c.legend(fontsize=7.4,loc="lower left",frameon=False)

for a_ in ax:
    a_.spines["top"].set_visible(False); a_.spines["right"].set_visible(False); a_.tick_params(labelsize=8.5)
fig.suptitle("Bank credit and circuit separation: locked floors are non-pledgeable, so endogenous lending cannot re-mix "
             "the transactional and asset circuits at any feasible loan-to-value",fontsize=11.3,color=INK,y=1.02)
fig.tight_layout()
fig.savefig(os.path.join(os.path.dirname(__file__),"..","figures","figure_P9_banking_separation.png"),dpi=200,bbox_inches="tight",facecolor="white")
print("wrote figure_P9_banking_separation.png; kappa_bank*=%.3f"%kbc)

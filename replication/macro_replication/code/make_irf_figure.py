"""
make_irf_figure.py
------------------
Reproduces figure_P6_irf.png — the three-panel impulse-response figure for
Section 7.6 / Proposition 6 / Appendix A.9 of Neo-Solon (2026e):
  (a) demand shock with vs without the floor cushion,
  (b) cost-push shock with vs without KI,
  (c) asset-circuit shock and consumer-price containment.
"""
import numpy as np
import os
import matplotlib; matplotlib.use("Agg")
import matplotlib.pyplot as plt
INK="#1a1a2e"; WARM="#b0413e"; GOLD="#c08a2e"; GREEN="#3a6b4f"; GREY="#8a8a8a"
psiLam=0.9; kappa=0.08; gamma=0.15; phi_y=0.7; phi_v=0.9; leak=0.03
def A(pl): return np.array([[1-pl,kappa,leak],[-gamma,phi_y,0],[0,0,phi_v]])
def irf(shock,T=24,pl=psiLam,omegaF=0.0):
    M=A(pl); s=np.array([shock.get('pi',0.0),(1-omegaF)*shock.get('y',0.0),shock.get('v',0.0)])
    out=[]
    for _ in range(T): out.append(s.copy()); s=M@s
    return np.array(out)
plt.rcParams.update({"font.family":"serif","font.size":10,"axes.edgecolor":INK,"axes.linewidth":0.8})
fig,ax=plt.subplots(1,3,figsize=(15,4.6)); T=24; t=np.arange(T)

# (a) demand shock: floor cushions output; prices stay anchored
a=ax[0]
a.plot(t,irf({'y':-1},omegaF=0.0)[:,1],lw=2.0,color=WARM,label=r"output, no floor ($\omega_F=0$)")
a.plot(t,irf({'y':-1},omegaF=0.15)[:,1],lw=2.0,color=GREEN,label=r"output, floor cushion ($\omega_F=0.15$)")
a.plot(t,irf({'y':-1},omegaF=0.15)[:,0],lw=1.6,color=INK,ls="--",label="price-path gap (KI anchors)")
a.axhline(0,color=GREY,lw=.7)
a.annotate("trough −15%",(3,-0.85),xytext=(7,-0.6),fontsize=8,color=GREEN,
           arrowprops=dict(arrowstyle="->",color=GREEN,lw=0.8))
a.set_xlim(0,T-1); a.set_xlabel("periods after shock"); a.set_ylabel("deviation")
a.set_title("(a)  Demand collapse — floor cushions",fontsize=11,color=INK,loc="left")
a.legend(fontsize=7.6,loc="lower right",frameon=False)

# (b) cost-push: KI returns the gap; no-KI persists
b=ax[1]
b.plot(t,irf({'pi':1},pl=0.9)[:,0],lw=2.0,color=GREEN,label=r"with KI ($\psi\lambda=0.9$)")
b.plot(t,irf({'pi':1},pl=0.0)[:,0],lw=2.0,color=WARM,label=r"no KI ($\psi\lambda=0$, unit root)")
b.axhline(0,color=GREY,lw=.7)
b.set_xlim(0,T-1); b.set_ylim(-0.1,1.05); b.set_xlabel("periods after shock"); b.set_ylabel("price-path gap  $x_t$")
b.set_title("(b)  Cost-push — KI self-corrects",fontsize=11,color=INK,loc="left")
b.legend(fontsize=7.8,loc="upper right",frameon=False)

# (c) asset shock: consumer prices contained
c=ax[2]; sim=irf({'v':1})
c.plot(t,sim[:,2],lw=2.0,color=GOLD,label="asset valuation  $v_t$")
c.plot(t,sim[:,0],lw=2.0,color=INK,label="consumer price-path gap  $x_t$")
c.axhline(0,color=GREY,lw=.7)
c.annotate(r"contained $\leq\lambda_{\rm leak}/\psi\lambda\approx3\%$",(2,0.03),xytext=(6,0.30),
           fontsize=8,color=INK,arrowprops=dict(arrowstyle="->",color=INK,lw=0.8))
c.set_xlim(0,T-1); c.set_ylim(-0.05,1.05); c.set_xlabel("periods after shock"); c.set_ylabel("deviation")
c.set_title("(c)  Asset shock — two-circuit containment",fontsize=11,color=INK,loc="left")
c.legend(fontsize=7.8,loc="upper right",frameon=False)

for a_ in ax:
    a_.spines["top"].set_visible(False); a_.spines["right"].set_visible(False); a_.tick_params(labelsize=8.5)
fig.suptitle("Impulse responses of the linearized two-circuit system: the floor cushions demand, KI self-corrects "
             "cost-push, and the asset circuit is contained",fontsize=11.5,color=INK,y=1.02)
fig.tight_layout()
fig.savefig(os.path.join(os.path.dirname(__file__),"..","figures","figure_P6_irf.png"),dpi=200,bbox_inches="tight",facecolor="white")
print("wrote figure_P6_irf.png")

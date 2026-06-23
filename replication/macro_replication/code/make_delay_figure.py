"""
make_delay_figure.py
--------------------
Reproduces figure_P5_delay_feedback.png — the three-panel delay-feedback figure
for Section 3.6 / Proposition 5 / Appendix A.8 of Neo-Solon (2026e):
  (a) the stability region collapsing toward the small-gain box as delay d grows,
  (b) the slowest-mode damping vanishing like |ln lamL|/d at fixed gain,
  (c) impulse responses: feedforward schedule vs delayed feedback.
"""
import numpy as np
import os
import matplotlib; matplotlib.use("Agg")
import matplotlib.pyplot as plt
INK="#1a1a2e"; WARM="#b0413e"; GOLD="#c08a2e"; GREEN="#3a6b4f"; GREY="#8a8a8a"
def maxroot(a,lamL,d):
    c=[0.0]*(d+1); c[0]=1.0; c[1]=-a; c[d]=lamL
    return max(abs(r) for r in np.roots(c))
plt.rcParams.update({"font.family":"serif","font.size":10,"axes.edgecolor":INK,"axes.linewidth":0.8})
fig,ax=plt.subplots(1,3,figsize=(15,4.6))

# (a) stability region in (a, lamL) collapsing toward the small-gain triangle
A=np.linspace(-0.6,1.0,90); LL=np.linspace(0,1.5,90)
AA,LLg=np.meshgrid(A,LL)
cols={1:GOLD,2:GREEN,8:WARM,32:INK}
for d,c in cols.items():
    Z=np.empty_like(AA)
    for i in range(AA.shape[0]):
        for j in range(AA.shape[1]):
            Z[i,j]=maxroot(AA[i,j],LLg[i,j],d)
    ax[0].contour(AA,LLg,Z,levels=[1.0],colors=[c],linewidths=1.8)
    ax[0].plot([],[],color=c,lw=1.8,label="d = %d"%d)
# small-gain triangle |a|+|lamL|<1
xt=np.linspace(-1,1,50); ax[0].plot(xt,1-np.abs(xt),color=GREY,ls=":",lw=1.2)
ax[0].fill_between(xt,0,1-np.abs(xt),color=GREY,alpha=.10)
ax[0].text(0.0,0.30,"small-gain box\n$|1{-}\\psi\\lambda|+|\\lambda_L|<1$\n(stable for all $d$)",
           ha="center",fontsize=7.4,color="#5a5a5a")
ax[0].plot(0.1,0,marker="^",color=INK,ms=7); ax[0].text(0.13,0.04,"baseline\n$\\psi\\lambda=0.90$",fontsize=7.2,color=INK)
ax[0].set_xlim(-0.6,1.0); ax[0].set_ylim(0,1.5)
ax[0].set_xlabel(r"fast-loop pole  $a=1-\psi\lambda$"); ax[0].set_ylabel(r"slow-lever feedback gain  $\lambda_L$")
ax[0].set_title("(a)  Stable region collapses with delay",fontsize=11,color=INK,loc="left")
ax[0].legend(fontsize=7.8,loc="upper right",frameon=False,title="delay (steps)")

# (b) vanishing damping at fixed lamL as delay grows
a=0.10; lamL=0.5; ds=np.arange(1,61)
damp=[1-maxroot(a,lamL,int(d)) for d in ds]
ax[1].plot(ds,damp,lw=2.0,color=WARM,label=r"slowest-mode damping $1-\max|z|$")
ax[1].plot(ds,np.abs(np.log(lamL))/ds,ls="--",lw=1.4,color=INK,label=r"$|\ln\lambda_L|/d$ asymptote")
for dd in (10,40):
    ax[1].axvline(dd,color=GREY,ls=":",lw=.9); ax[1].text(dd+0.6,0.45,"d=%d"%dd,fontsize=7.2,color=GREY,rotation=90,va="top")
ax[1].set_xlim(1,60); ax[1].set_ylim(0,0.55)
ax[1].set_xlabel(r"slow-lever delay  $d$ (steps)"); ax[1].set_ylabel("damping of the loop")
ax[1].set_title(r"(b)  Damping vanishes as $1/d$  ($\lambda_L=0.5$)",fontsize=11,color=INK,loc="left")
ax[1].legend(fontsize=8,loc="upper right",frameon=False)

# (c) impulse response: feedforward (schedule) vs delayed feedback
def irf(a,lamL,d,T=60):
    x=np.zeros(T); x[0]=1.0
    for t in range(1,T):
        x[t]=a*x[t-1]-(lamL*x[t-d] if t-d>=0 else 0.0)
    return x
T=60; t=np.arange(T)
ax[2].plot(t,irf(a,0.0,10,T),lw=2.0,color=GREEN,label="feedforward schedule (no feedback pole)")
ax[2].plot(t,irf(a,0.5,10,T),lw=2.0,color=WARM,label=r"delayed feedback ($d=10,\ \lambda_L=0.5$)")
ax[2].axhline(0,color=GREY,lw=.7)
ax[2].set_xlim(0,T-1); ax[2].set_xlabel("steps after a unit price-path shock"); ax[2].set_ylabel("price-path gap  $x_t$")
ax[2].set_title("(c)  Feedforward keeps the clean decay",fontsize=11,color=INK,loc="left")
ax[2].legend(fontsize=7.8,loc="upper right",frameon=False)

for a_ in ax:
    a_.spines["top"].set_visible(False); a_.spines["right"].set_visible(False); a_.tick_params(labelsize=8.5)
fig.suptitle("Why the slow liquidation lever is feedforward, not feedback: delayed feedback adds $d{-}1$ poles "
             "whose damping vanishes with the delay",fontsize=11.5,color=INK,y=1.02)
fig.tight_layout()
fig.savefig(os.path.join(os.path.dirname(__file__),"..","figures","figure_P5_delay_feedback.png"),dpi=200,bbox_inches="tight",facecolor="white")
print("wrote figure_P5_delay_feedback.png")

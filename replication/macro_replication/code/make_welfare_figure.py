"""
make_welfare_figure.py
----------------------
Reproduces figure_P8_welfare_dividend.png for Section 5.6 / Proposition 8 /
Appendix A.11 of Neo-Solon (2026e): welfare vs dividend share by patience,
the optimal-share schedule kappa*(R) with corners, and the envelope decomposition.
"""
import numpy as np, os
import matplotlib; matplotlib.use("Agg")
import matplotlib.pyplot as plt
INK="#1a1a2e"; WARM="#b0413e"; GOLD="#c08a2e"; GREEN="#3a6b4f"; GREY="#8a8a8a"
nu=0.5; chi=1.0; G=0.20; r=0.045
def labor(b,wedge=0.0):
    lo,hi=1e-6,5.0
    for _ in range(80):
        h=0.5*(lo+hi)
        if chi*h**(1/nu) < (1.0-wedge)/(h+b): lo=h
        else: hi=h
    return 0.5*(lo+hi)
def c1(k,wedge=0.0): return labor(k*G,wedge)+k*G
def c2(k): return 1.0+(1-k)*G*(1+r)
def W(k,beta,Om,wedge=0.0):
    h=labor(k*G,wedge); return np.log(h+k*G)-chi*h**(1+1/nu)/(1+1/nu)+beta*Om*np.log(c2(k))
def kstar(beta,Om,wedge=0.0):
    ks=np.linspace(0,1,4001); return ks[int(np.argmax([W(k,beta,Om,wedge) for k in ks]))]
Rcorner=c2(0)/c1(0)

plt.rcParams.update({"font.family":"serif","font.size":10,"axes.edgecolor":INK,"axes.linewidth":0.8})
fig,ax=plt.subplots(1,3,figsize=(15,4.6))
ks=np.linspace(0,1,400)

# (a) W(kappa) for several patience beta
a=ax[0]
for beta,c,lab in [(0.80,GOLD,"0.80 (impatient)"),(0.90,INK,"0.90 (baseline)"),(1.00,GREEN,"1.00"),(1.16,WARM,"1.16 (≈corner)")]:
    w=np.array([W(k,beta,1.0) for k in ks]); w=w-w.max()
    a.plot(ks,w,lw=1.9,color=c,label=r"$\beta=$%s"%lab)
    ks_=kstar(beta,1.0); a.plot(ks_,0,'o',color=c,ms=5)
a.set_xlim(0,1); a.set_ylim(-0.02,0.004)
a.set_xlabel(r"dividend share  $\kappa_d$"); a.set_ylabel("welfare (normalised to peak)")
a.set_title("(a)  Welfare-optimal $\\kappa_d$ shifts with patience",fontsize=11,color=INK,loc="left")
a.legend(fontsize=7.6,loc="lower center",frameon=False,title="patience",title_fontsize=7.6)

# (b) kappa*(R) master schedule
b=ax[1]; Rs=np.linspace(0.7,1.35,260); kk=[]
for R in Rs:
    beta=R/(1+r); kk.append(kstar(beta,1.0))
b.plot(Rs,kk,lw=2.2,color=INK)
b.axvspan(Rcorner,1.35,color=WARM,alpha=.08)
b.axhline(0,color=GREY,lw=.6); b.axhline(1,color=GREY,lw=.6,ls=":")
b.plot(0.9405,0.795,'o',color=GREEN,ms=7,zorder=5)
b.annotate("baseline\n$R=0.94,\\ \\kappa_d^*=0.80$",(0.9405,0.795),(0.74,0.45),fontsize=7.6,color=GREEN,
           arrowprops=dict(arrowstyle="->",color=GREEN,lw=.8))
b.axvline(Rcorner,color=WARM,lw=.9,ls="--")
b.text(Rcorner+0.005,0.55,"wealth-max corner\n$\\kappa_d^*=0$ needs $R\\geq%.2f$"%Rcorner,fontsize=7.4,color=WARM)
b.text(0.73,0.93,"pay-out corner $\\kappa_d^*=1$",fontsize=7.2,color=GREY)
b.set_xlim(0.7,1.35); b.set_ylim(-0.05,1.08)
b.set_xlabel(r"retention premium  $R=\beta\,\Omega\,(1+r)$"); b.set_ylabel(r"optimal dividend share  $\kappa_d^*$")
b.set_title("(b)  The optimal share falls as retention is rewarded",fontsize=11,color=INK,loc="left")

# (c) envelope: labor term ~0 without a wedge; first-order with one
c=ax[2]
def dW(k,beta,Om,wedge=0.0,e=1e-6): return (W(k+e,beta,Om,wedge)-W(k-e,beta,Om,wedge))/(2*e)
beta=0.90
tot=np.array([dW(k,beta,1.0,0.0) for k in ks])
timing=np.array([G/c1(k)-beta*1.0*G*(1+r)/c2(k) for k in ks])
laborterm=tot-timing
c.plot(ks,timing,lw=1.9,color=INK,label="consumption-timing term")
c.plot(ks,laborterm,lw=1.9,color=GOLD,label="labour term (no wedge)")
totw=np.array([dW(k,beta,1.0,0.20) for k in ks])
c.plot(ks,totw,lw=1.6,color=WARM,ls="--",label="total with 20% labour wedge")
c.axhline(0,color=GREY,lw=.6)
k0=kstar(beta,1.0); kw=kstar(beta,1.0,0.20)
c.plot(k0,0,'o',color=INK,ms=6); c.plot(kw,0,'s',color=WARM,ms=5)
c.annotate("$\\kappa_d^*$",(k0,0),(k0-0.13,0.012),fontsize=9,color=INK)
c.set_xlim(0,1); c.set_ylim(-0.05,0.05)
c.set_xlabel(r"dividend share  $\kappa_d$"); c.set_ylabel(r"marginal welfare $dW/d\kappa_d$")
c.set_title("(c)  Labour distortion is second-order (envelope)",fontsize=11,color=INK,loc="left")
c.legend(fontsize=7.2,loc="upper right",frameon=False)

for a_ in ax:
    a_.spines["top"].set_visible(False); a_.spines["right"].set_visible(False); a_.tick_params(labelsize=8.5)
fig.suptitle("The welfare-optimal consumer dividend: $\\kappa_d=0$ maximises wealth, but the welfare optimum is interior "
             "unless retention is very strongly rewarded",fontsize=11.5,color=INK,y=1.02)
fig.tight_layout()
fig.savefig(os.path.join(os.path.dirname(__file__),"..","figures","figure_P8_welfare_dividend.png"),dpi=200,bbox_inches="tight",facecolor="white")
print("wrote figure_P8_welfare_dividend.png; baseline kappa*=%.3f corner R=%.3f"%(kstar(0.90,1.0),Rcorner))

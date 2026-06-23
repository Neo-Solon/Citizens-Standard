"""
make_forward_figure.py
----------------------
Reproduces figure_P7_forward_determinacy.png for Section 3.7 / Proposition 7 /
Appendix A.10 of Neo-Solon (2026e): (a) determinacy frontier money-rule vs
interest-rate rule, (b) unique path vs sunspot fan, (c) two-circuit BK count
vs asset-consumer coupling.
"""
import numpy as np
import os
import matplotlib; matplotlib.use("Agg")
import matplotlib.pyplot as plt
INK="#1a1a2e"; WARM="#b0413e"; GOLD="#c08a2e"; GREEN="#3a6b4f"; GREY="#8a8a8a"
# precise two-circuit determinacy threshold
r=0.045; a=1/(1+r); alpha=4.0; phi=0.5; theta=1+(1+phi)/alpha
def nexp(c):
    M=np.array([[theta,-c],[-c/a,1/a]]); return np.sum(np.abs(np.linalg.eigvals(M))>1+1e-12)
lo,hi=0.0,0.5
for _ in range(60):
    m=0.5*(lo+hi)
    if nexp(m)==2: lo=m
    else: hi=m
thr=0.5*(lo+hi); print("two-circuit determinacy threshold coupling = %.3f"%thr)

plt.rcParams.update({"font.family":"serif","font.size":10,"axes.edgecolor":INK,"axes.linewidth":0.8})
fig,ax=plt.subplots(1,3,figsize=(15,4.6))

# (a) determinacy frontier: explosive root vs policy gain
a0=ax[0]; phis=np.linspace(0,2.5,200)
for al,c in [(0.5,GREEN),(2.0,INK),(4.0,GOLD)]:
    a0.plot(phis,1+(1+phis)/al,lw=1.8,color=c,label=r"money rule, $\alpha=%.1f$"%al)
a0.plot(phis,phis,lw=2.0,color=WARM,ls="--",label="interest-rate rule (root $=\\phi$)")
a0.axhline(1,color=GREY,lw=1.0,ls=":")
a0.fill_between(phis,1,8,color=GREY,alpha=.06)
a0.text(1.7,6.6,"determinate\n(root outside unit circle)",fontsize=7.6,color="#5a5a5a",ha="center")
a0.axvline(1.0,color=WARM,lw=.8,ls=":"); a0.text(1.03,0.2,"Taylor\nthreshold",fontsize=7.0,color=WARM)
a0.set_xlim(0,2.5); a0.set_ylim(0,8)
a0.set_xlabel(r"policy gap response  $\phi$"); a0.set_ylabel(r"explosive root")
a0.set_title("(a)  Money anchor is determinate for all $\\phi$",fontsize=11,color=INK,loc="left")
a0.legend(fontsize=7.4,loc="upper left",frameon=False)

# (b) uniqueness vs sunspot fan
b=ax[1]; T=30; t=np.arange(T); rng=np.random.default_rng(7)
# determinate money rule: unique bounded fundamental path (AR(1) fundamental shock, forward-solved)
rho=0.6; th=1+(1+0.5)/4.0
xf=np.zeros(T)
# forward solution to E x_{t+1}=th x_t - eps_t with AR(1) eps: x_t = eps_t/(th-rho)
eps=np.zeros(T); eps[0]=1.0
for k in range(1,T): eps[k]=rho*eps[k-1]
xf=eps/(th-rho)
b.plot(t,xf,lw=2.4,color=INK,label="money anchor: unique path",zorder=5)
# indeterminate passive interest rule phi=0.5: fan of sunspot equilibria
for i in range(6):
    xs=np.zeros(T)
    for k in range(1,T): xs[k]=0.5*xs[k-1]+rng.normal(0,0.12)
    b.plot(t,xs,lw=1.0,color=WARM,alpha=.55)
b.plot([],[],lw=1.0,color=WARM,alpha=.7,label="passive rate rule: sunspot fan")
b.axhline(0,color=GREY,lw=.6)
b.set_xlim(0,T-1); b.set_xlabel("periods after a fundamental shock"); b.set_ylabel(r"price gap  $x_t$")
b.set_title("(b)  Determinacy vs self-fulfilling beliefs",fontsize=11,color=INK,loc="left")
b.legend(fontsize=7.8,loc="upper right",frameon=False)

# (c) two-circuit BK count vs coupling
c=ax[2]; cs=np.linspace(0,0.30,200)
e1=[];e2=[]
for cc in cs:
    M=np.array([[theta,-cc],[-cc/a,1/a]]); ev=sorted(np.abs(np.linalg.eigvals(M)))
    e1.append(ev[0]); e2.append(ev[1])
c.plot(cs,e2,lw=1.8,color=INK,label="larger |eigenvalue|")
c.plot(cs,e1,lw=1.8,color=GOLD,label="smaller |eigenvalue|")
c.axhline(1,color=GREY,lw=1.0,ls=":")
c.axvspan(0,thr,color=GREEN,alpha=.10); c.axvspan(thr,0.30,color=WARM,alpha=.08)
c.text(thr/2,1.02,"determinate\n(2 jumps, 2 explosive)",fontsize=7.0,color=GREEN,ha="center")
c.text((thr+0.30)/2,0.90,"indeterminate",fontsize=7.4,color=WARM,ha="center")
c.axvline(0.03,color=INK,ls=":",lw=.9); c.text(0.035,1.30,"paper leak\n≈0.03",fontsize=7.0,color=INK)
c.axvline(thr,color=GREY,lw=.8); c.text(thr+0.004,1.34,"threshold\n≈%.2f"%thr,fontsize=7.0,color=GREY)
c.set_xlim(0,0.30); c.set_ylim(0.82,1.45)
c.set_xlabel(r"asset$\leftrightarrow$consumer coupling"); c.set_ylabel("eigenvalue modulus")
c.set_title("(c)  Circuit separation secures determinacy",fontsize=11,color=INK,loc="left")
c.legend(fontsize=7.6,loc="upper left",frameon=False)

for a_ in ax:
    a_.spines["top"].set_visible(False); a_.spines["right"].set_visible(False); a_.tick_params(labelsize=8.5)
fig.suptitle("Forward-looking determinacy: the money-quantity anchor pins a unique rational-expectations price path "
             "without a Taylor principle",fontsize=11.5,color=INK,y=1.02)
fig.tight_layout()
fig.savefig(os.path.join(os.path.dirname(__file__),"..","figures","figure_P7_forward_determinacy.png"),dpi=200,bbox_inches="tight",facecolor="white")
print("wrote figure_P7_forward_determinacy.png")

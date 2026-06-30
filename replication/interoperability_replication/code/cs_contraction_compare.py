"""
Contraction redesign: bond sterilization (carries r<g) vs graduated surcharge (carry-free).
Shows CS escapes the carry condition by RETIRING money via surcharge rather than absorbing it
into an interest-bearing stock. Converged independently with PCM Ch.7's graduated Inflationary Surcharge.
"""
import numpy as np, matplotlib.pyplot as plt
import os
_FIGDIR = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "figures"); os.makedirs(_FIGDIR, exist_ok=True)
g=0.03; delta=0.02; T=40; t=np.arange(T+1)
def bond(r):
    b=np.zeros(T+1)
    for i in range(1,T+1): b[i]=b[i-1]*(1+r)/(1+g)+delta
    return b*100
b_lo, b_eq, b_hi = bond(0.01), bond(0.03), bond(0.05)
surch_stock=np.zeros(T+1)            # money retired each period -> no liability accumulates
surch_drag=np.full(T+1,delta*100)    # bounded annual withdrawal (% GDP), constant for constant drift

plt.rcParams.update({'font.size':10,'axes.grid':True,'grid.alpha':.25,'figure.dpi':150})
fig,(a1,a2)=plt.subplots(1,2,figsize=(11,4.6))
fig.suptitle("Contraction without the carry condition: retire money, don't sterilize it",fontsize=12,fontweight='bold')

a1.plot(t,b_lo,color='#3a8a4a',lw=2.4,label='r < g (1% vs 3%): converges')
a1.plot(t,b_eq,color='#d4781f',lw=2.2,label='r = g: grows linearly')
a1.plot(t,b_hi,color='#c0392b',lw=2.4,label='r > g (5% vs 3%): diverges')
a1.set_title("Bond sterilization — an interest-bearing stock"); a1.set_xlabel("years of persistent 2%/yr drift"); a1.set_ylabel("sterilization stock (% GDP)"); a1.set_ylim(0,140); a1.legend(fontsize=8)
a1.text(.5,-.32,"Absorbing money into interest-bearing debt makes the stock compound. It only stays finite if r < g — the carry condition.",transform=a1.transAxes,ha='center',fontsize=8,style='italic')

a2.plot(t,b_hi,color='#c0392b',lw=2.0,ls='--',label='bond stock if sterilized (r>g) — avoided')
a2.plot(t,surch_stock,color='#3a8a4a',lw=2.6,label='surcharge liability (money retired): 0')
a2.plot(t,surch_drag,color='#2c6e9e',lw=2.2,ls=':',label='surcharge annual drag (bounded)')
a2.set_title("Graduated surcharge — money retired, no stock"); a2.set_xlabel("years of persistent 2%/yr drift"); a2.set_ylabel("% GDP"); a2.set_ylim(0,140); a2.legend(fontsize=8)
a2.text(.5,-.32,"Retiring money leaves no interest-bearing stock, so nothing compounds and r<g never arises. The cost is a bounded annual drag.",transform=a2.transAxes,ha='center',fontsize=8,style='italic')

fig.tight_layout(rect=[0,0.04,1,0.95]); fig.savefig(os.path.join(_FIGDIR,"cs_contraction_compare.png"),bbox_inches='tight',facecolor='white')
print("bond stock at yr40: r<g %.0f%%  r=g %.0f%%  r>g %.0f%%"%(b_lo[-1],b_eq[-1],b_hi[-1]))
print("surcharge liability at yr40: %.0f%% (money retired); annual drag constant at %.0f%% GDP"%(surch_stock[-1],surch_drag[-1]))
print("saved cs_contraction_compare.png")

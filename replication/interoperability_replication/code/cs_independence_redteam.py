"""
Red-team the load-bearing assumption: are KI (inflation thermostat) and the growth-line stream
(dividend) really INDEPENDENT? Try to find configurations where holding the anchor must lean on
the dividend, breaking 'holding zero is free.'
"""
import numpy as np, matplotlib.pyplot as plt
import os
_FIGDIR = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "figures"); os.makedirs(_FIGDIR, exist_ok=True)
g=0.03; kd=0.5; base=kd*g   # base real dividend per period (normalized reference)

# ---------- BREAK A: the withdrawal asymmetry (the real threat) ----------
# KI can ADD money freely & independently. To DISINFLATE it must SUBTRACT money, which needs a real
# withdrawal instrument (bonds/tax) with capacity w_max. Beyond w_max the only lever left is cutting
# the dividend -> the streams couple. A member with INFLATIONARY drift delta must withdraw delta to hold 0.
delta=np.linspace(-0.03,0.08,221)          # natural drift: <0 deflationary (CS design case), >0 inflationary
def divA(delta,w_max):
    withdraw_needed=np.maximum(0.0,delta)               # only inflationary drift needs withdrawal
    excess=np.maximum(0.0,withdraw_needed-w_max)        # beyond KI's independent capacity
    return base-excess                                  # excess must come out of the dividend
print("BREAK A — withdrawal asymmetry:")
for w in (0.03,0.06):
    d=divA(delta,w); brk=delta[np.argmax(d<base-1e-9)]
    print(f"  w_max={w*100:.0f}%: dividend stays full until inflationary drift = {brk*100:.0f}%, then it pays for the anchor.")
print("  -> Independence is ASYMMETRIC: free when KI ADDS (deflationary drift, the CS design case),")
print("     broken when KI must SUBTRACT beyond its withdrawal capacity (inflationary drift/shock).")

# ---------- BREAK B: shared issuance ceiling ----------
# If total issuance is capped at C, the growth-line (g) and KI (pi*) compete for the same envelope.
pis=np.linspace(0,0.04,201); C=0.04
def divB(pis,C): return base*np.minimum(g,np.maximum(0.0,C-pis))/g   # KI takes priority to hold anchor; dividend gets the rest
dB=divB(pis,C); brkB=pis[np.argmax(dB<base-1e-9)]
print(f"\nBREAK B — shared issuance ceiling (C={C*100:.0f}%): dividend full until pi*={brkB*100:.0f}%, then the corridor crowds it.")
print("  -> This bites the CORRIDOR, not zero: a positive anchor competes with the dividend under a cap; zero leaves max room.")

# ---------- BREAK C: inflation isn't perfectly real-neutral ----------
# If inflation carries a (convex) real cost, the real growth that funds the dividend shrinks with |pi*|.
cost_a=20.0
def divC(pis): return base*(1-cost_a*pis**2)
print(f"\nBREAK C — real cost of inflation (a={cost_a:.0f}): real dividend at pi*=0/+3% = {divC(np.array([0]))[0]/base:.3f} / {divC(np.array([0.03]))[0]/base:.3f} of base.")
print("  -> 'Dividend independent of pi*' is only approximate; the dividend is MAXIMIZED at zero. Also reinforces zero.")

print("\nVERDICT: one real break (A), two that reinforce zero (B,C).")
print("  The decoupling holds in CS's design regime (deflationary drift, anchor held by ADDING money).")
print("  It fails only when holding the anchor requires net CONTRACTION beyond KI's independent withdrawal")
print("  instrument. Fix: the spec must NAME that instrument (bond/tax sterilization) so KI never has to")
print("  reach into the dividend. With it, independence holds both directions; without it, only upward.")

# ---------- figure ----------
plt.rcParams.update({'font.size':10,'axes.grid':True,'grid.alpha':.25,'figure.dpi':150})
fig,ax=plt.subplots(2,2,figsize=(11,8))
fig.suptitle("Red-team: when do KI and the growth-line dividend stop being independent?",fontsize=12,fontweight='bold')
G,R,O,B='#3a8a4a','#c0392b','#d4781f','#2c6fa6'

a=ax[0,0]
a.axvspan(-0.03,0,color=G,alpha=0.08); a.axvspan(0,0.08,color=R,alpha=0.06)
a.plot(delta*100,divA(delta,0.03)/base,color=R,lw=2.5,label='withdrawal capacity 3%')
a.plot(delta*100,divA(delta,0.06)/base,color=O,lw=2,ls='--',label='withdrawal capacity 6%')
a.axvline(0,color='#999',lw=.8); a.set_title("BREAK A: dividend vs natural drift (holding anchor=0)"); a.set_xlabel("natural drift  \u2190 deflationary | inflationary \u2192  (%)"); a.set_ylabel("real dividend / base"); a.legend(fontsize=8)
a.text(.5,-.32,"Free while KI ADDS (green). Once it must SUBTRACT past capacity (red), the anchor is paid from the dividend.",transform=a.transAxes,ha='center',fontsize=8,style='italic')

a=ax[0,1]
a.plot(pis*100,dB/base,color=B,lw=2.5)
a.axvline(brkB*100,color='#999',lw=.8,ls=':'); a.set_title("BREAK B: shared issuance ceiling"); a.set_xlabel("inflation setpoint pi* (%)"); a.set_ylabel("real dividend / base")
a.text(.5,-.32,"Under a total-issuance cap, a positive corridor crowds the dividend; zero leaves the most room.",transform=a.transAxes,ha='center',fontsize=8,style='italic')

a=ax[1,0]
pp=np.linspace(-0.04,0.04,201)
a.plot(pp*100,divC(pp)/base,color=B,lw=2.5); a.axvline(0,color='#999',lw=.8)
a.set_title("BREAK C: inflation not perfectly real-neutral"); a.set_xlabel("inflation setpoint pi* (%)"); a.set_ylabel("real dividend / base")
a.text(.5,-.32,"If inflation has a real cost, the dividend peaks at zero. 'Independent of pi*' is only approximate.",transform=a.transAxes,ha='center',fontsize=8,style='italic')

a=ax[1,1]; a.axis('off')
a.text(0.5,0.95,"VERDICT",ha='center',fontweight='bold',fontsize=12,transform=a.transAxes)
txt=("Independence is ASYMMETRIC.\n\n"
     "Upward (KI adds money):\n  always independent of the dividend.\n  This is CS's design regime\n  (productivity-driven deflation).\n\n"
     "Downward (KI withdraws money):\n  independent only up to KI's own\n  withdrawal capacity. Beyond it,\n  holding the anchor cuts the dividend.\n\n"
     "FIX: give KI a named independent\ncontractionary instrument (bond/tax\nsterilization). With it, the setpoint\nclaim holds both directions.\n\n"
     "Breaks B & C bite the CORRIDOR,\nnot zero \u2014 they reinforce the anchor.")
a.text(0.04,0.86,txt,ha='left',va='top',fontsize=9.5,transform=a.transAxes,linespacing=1.25)

fig.tight_layout(rect=[0,0.02,1,0.96]); fig.savefig(os.path.join(_FIGDIR,"cs_independence_redteam.png"),bbox_inches='tight',facecolor='white')
print("\nsaved cs_independence_redteam.png")

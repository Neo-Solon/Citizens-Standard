"""
Test Davide's behavioral claim: does zero inflation increase IDLE/speculative capital, and does
mild inflation push capital toward PRODUCTIVE use? Built fairly to reveal the CONDITION under which
he's right, then compare inflation against a targeted carrying cost.

Reduced-form portfolio allocation across {cash, speculative store, productive}. Agents allocate by a
logit over after-cost real 'attractiveness' (real return + liquidity/safety premium). Illustrative
parameters; the model shows DIRECTIONS and the crux, not calibrated magnitudes.

Load-bearing assumptions (stated honestly):
  (1) Speculative stores (real estate, commodities, gold, equities) HEDGE inflation -> hedge factor h.
  (2) Productive claims are real (a claim on output), broadly inflation-neutral.
  (3) The targeted carrying cost can exempt working cash and fall on speculative/idle stores.
"""
import numpy as np, matplotlib.pyplot as plt
r_p, r_s = 0.06, 0.01          # real returns: productive (illiquid/risky), speculative (low, "produces little")
lam_c, lam_s, lam_p = 0.035, 0.045, 0.0   # liquidity/safety premia: cash, speculative store (preferred safe hedge), productive
sig = 0.02                      # allocation sensitivity

def shares(pi, h=1.0, tau_c=0.0, tau_s=0.0):
    real_c = -pi - tau_c
    real_s = r_s - (1-h)*pi - tau_s     # h=1 perfect inflation hedge; h=0 erodes like cash
    real_p = r_p
    u = np.array([real_c+lam_c, real_s+lam_s, real_p+lam_p])
    e = np.exp(u/sig); return e/e.sum()  # [cash, speculative, productive]

A  = shares(0.00)                       # baseline: zero inflation
B  = shares(0.03, h=1.0)                # mild inflation, speculative HEDGES it (realistic)
B0 = shares(0.03, h=0.0)                # mild inflation, NO hedge available (Davide's implicit world)
C  = shares(0.00, tau_c=0.03, tau_s=0.03)  # zero inflation + targeted carrying cost on idle (cash+spec), NOT productive

lab=["cash","speculative","productive"]
def show(n,s): print(f"  {n:32}: cash {s[0]:.3f}  spec {s[1]:.3f}  prod {s[2]:.3f}")
print("ALLOCATIONS:")
show("A baseline (pi=0)", A); show("B inflation 3% (hedged, real)", B)
show("B0 inflation 3% (NO hedge)", B0); show("C zero + targeted idle-cost", C)
print(f"\nPRODUCTIVE share:  baseline {A[2]:.3f}")
print(f"  inflation, hedges exist  -> {B[2]:.3f}  (+{(B[2]-A[2])*100:.1f} pts)  <- the realistic case")
print(f"  inflation, NO hedge      -> {B0[2]:.3f}  (+{(B0[2]-A[2])*100:.1f} pts)  <- Davide's mechanism works here")
print(f"  targeted carrying cost   -> {C[2]:.3f}  (+{(C[2]-A[2])*100:.1f} pts)  <- works regardless of hedges")
print(f"\nWhere does capital fleeing cash go under inflation (hedged)? "
      f"spec +{(B[1]-A[1])*100:.1f} pts vs prod +{(B[2]-A[2])*100:.1f} pts  -> much of it goes to the speculative hedge.")

# incidence: who bears the cost
saver  ={'cash':0.70,'spec':0.20,'prod':0.10,'W':1.0}    # low wealth, cash-heavy
rentier={'cash':0.10,'spec':0.50,'prod':0.40,'W':10.0}   # high wealth, hedge-heavy
def infl_burden(a,pi): return pi*a['cash']                # only cash erodes (spec hedged, prod real); per unit wealth
def targ_burden(a,tau): return tau*a['spec']              # targeted on speculative store; working cash exempt
pi,tau=0.03,0.03
print("\nINCIDENCE (share of own wealth taxed per year):")
print(f"  inflation:  saver {infl_burden(saver,pi)*100:.2f}%   rentier {infl_burden(rentier,pi)*100:.2f}%   -> REGRESSIVE (saver pays {infl_burden(saver,pi)/infl_burden(rentier,pi):.1f}x the rate)")
print(f"  targeted :  saver {targ_burden(saver,tau)*100:.2f}%   rentier {targ_burden(rentier,tau)*100:.2f}%   -> PROGRESSIVE (rentier pays {targ_burden(rentier,tau)/targ_burden(saver,tau):.1f}x the rate)")

# ---------------- figure ----------------
plt.rcParams.update({'font.size':10,'axes.grid':True,'grid.alpha':.25,'figure.dpi':150})
fig,ax=plt.subplots(2,2,figsize=(11,8.4))
fig.suptitle("Does zero inflation idle capital? A portfolio test of Davide's behavioral question",fontsize=12,fontweight='bold')
CASH,SPEC,PROD='#6b7280','#d4781f','#3a8a4a'; R='#c0392b'

a=ax[0,0]
pis=np.linspace(0,0.05,51)
a.plot(pis*100,[shares(p,h=1.0)[2] for p in pis],color=PROD,lw=2.6,label='speculative stores HEDGE inflation (realistic)')
a.plot(pis*100,[shares(p,h=0.0)[2] for p in pis],color=PROD,lw=2.2,ls='--',label='NO hedge available (Davide\'s implicit world)')
a.set_title("Productive share vs inflation"); a.set_xlabel("inflation (%)"); a.set_ylabel("productive share"); a.legend(fontsize=7.8)
a.text(.5,-.30,"Inflation drives capital to productive use ONLY if idle wealth can't hedge. With hedges, it barely moves.",transform=a.transAxes,ha='center',fontsize=8,style='italic')

a=ax[0,1]
X=np.arange(3); w=0.6; data=np.array([A,B,C])
a.bar(X,data[:,0],w,color=CASH,label='cash (idle)')
a.bar(X,data[:,1],w,bottom=data[:,0],color=SPEC,label='speculative (idle/rentier)')
a.bar(X,data[:,2],w,bottom=data[:,0]+data[:,1],color=PROD,label='productive')
a.set_xticks(X); a.set_xticklabels(["zero infl.","inflation 3%\n(hedged)","zero + targeted\nidle cost"]); a.set_title("Where the money sits"); a.legend(fontsize=7.5,loc='lower center',ncol=3)
a.text(.5,-.30,"Inflation moves cash into the speculative hedge as much as productive. The targeted cost moves both idle forms to productive.",transform=a.transAxes,ha='center',fontsize=8,style='italic')

a=ax[1,0]
costs=np.linspace(0,0.05,51)
a.plot(costs*100,[shares(c,h=1.0)[2] for c in costs],color=R,lw=2.4,label='inflation (realistic, hedged)')
a.plot(costs*100,[shares(0.0,tau_c=c,tau_s=c)[2] for c in costs],color=PROD,lw=2.6,label='targeted idle-carrying cost')
a.set_title("Productive deployment per unit of 'holding cost'"); a.set_xlabel("cost imposed (%)"); a.set_ylabel("productive share"); a.legend(fontsize=8)
a.text(.5,-.30,"For the same cost of holding idle, the targeted instrument delivers far more productive deployment.",transform=a.transAxes,ha='center',fontsize=8,style='italic')

a=ax[1,1]
grp=np.arange(2); w=0.36
infl=[infl_burden(saver,pi)*100, infl_burden(rentier,pi)*100]
targ=[targ_burden(saver,tau)*100, targ_burden(rentier,tau)*100]
a.bar(grp-w/2,infl,w,color=R,label='inflation')
a.bar(grp+w/2,targ,w,color=PROD,label='targeted on speculative')
a.set_xticks(grp); a.set_xticklabels(["saver\n(cash-heavy)","rentier\n(hedge-heavy)"]); a.set_ylabel("% of own wealth taxed / yr"); a.set_title("Who bears the cost"); a.legend(fontsize=8)
a.text(.5,-.30,"Inflation taxes the saver and spares the rentier (regressive). The targeted cost flips it (progressive).",transform=a.transAxes,ha='center',fontsize=8,style='italic')

fig.tight_layout(rect=[0,0.02,1,0.96]); fig.savefig("behavioral_idle_capital.png",bbox_inches='tight',facecolor='white')
print("\nsaved behavioral_idle_capital.png")

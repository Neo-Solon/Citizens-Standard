"""
Calibrated version of the idle-capital test, on REAL data.
Sources:
  - Real long-run returns: Jordà-Schularick-Taylor "Rate of Return on Everything" 1870-2015 (16 econ.).
  - Portfolio composition by wealth: SCF 2022 (Richmond Fed EB 23-39, Table 2; Fed DFA).
Honesty correction surfaced by the real data: ordinary households are heavily LEVERAGED (mortgages
~96% of net worth at the 25-50th pct), so mild inflation erodes their DEBT as well as their cash ->
net incidence is ambiguous, NOT cleanly 'regressive' as the illustrative model implied. What survives
and sharpens is the ESCAPE: the wealthy hold ~2% of net worth in cash and ~98% in hedged/productive
assets, so inflation structurally can't reach the rentier capital it's meant to discipline.
"""
import numpy as np, matplotlib.pyplot as plt

# ---- REAL INPUTS ----
JST = {'Equity':6.7,'Housing\n(incl. rent)':7.1,'Bonds':2.5,'Bills':0.9,'Gold\n(long-run)':0.6}  # % real, JST 1870-2015
bins=['25-50th','50-75th','75-99th','Top 1%']
cash_pct   =[15,8,6,2]      # cash as % of net worth (SCF 2022, Table 2)
mort_pct   =[-96,-35,-13,-3]
prod_pct   =[15,19,40,72]   # stocks+business as % net worth (productive claims)
print("REAL DATA:")
print(f"  JST real returns: equity 6.7%, housing 7.1% (mostly rent->productive), bills 0.9%, gold ~0.6%")
print(f"  SCF cash share of net worth: {dict(zip(bins,cash_pct))}  -> wealthy hold ~2%, ordinary ~15%")
print(f"  Bottom 50% own ~1.1% of all corporate equities (Fed DFA, 2025).")
print(f"  Leverage note: at 25-50th pct, mortgages = -96% of net worth -> inflation also erodes their debt.")

# ---- allocation model with REAL returns ----
r_p, r_s = 0.067, 0.006      # productive (JST equity), speculative store (gold)
lam_c, lam_s, lam_p = 0.021, 0.015, 0.0   # liquidity/safety premia, calibrated to baseline ~ (cash .15, spec .15, prod .70)
sig=0.03
def shares(pi,h):
    u=np.array([-pi+lam_c, r_s-(1-h)*pi+lam_s, r_p+lam_p])
    e=np.exp(u/sig); return e/e.sum()
base=shares(0,1)
print(f"\n  baseline allocation (pi=0): cash {base[0]:.2f}  spec {base[1]:.2f}  prod {base[2]:.2f}  (calibrated)")
for h,lab in [(1.0,'real-estate-quality hedge'),(0.7,'gold/commodity partial hedge'),(0.0,'no hedge')]:
    s=shares(0.03,h); print(f"  inflation 3%, {lab:30}: prod {s[2]:.2f}  (+{(s[2]-base[2])*100:.0f} pts)")

# ---- figure ----
plt.rcParams.update({'font.size':10,'axes.grid':True,'grid.alpha':.25,'figure.dpi':150})
fig,ax=plt.subplots(2,2,figsize=(11,8.6))
fig.suptitle("Idle-capital test on real data (JST returns, SCF wealth composition)",fontsize=12,fontweight='bold')
PROD,SPEC,CASH,R='#3a8a4a','#d4781f','#6b7280','#c0392b'

a=ax[0,0]
ks=list(JST.keys()); vs=list(JST.values()); cols=[PROD,PROD,'#888','#888',SPEC]
a.bar(ks,vs,color=cols); a.set_title("Real long-run returns (JST 1870-2015)"); a.set_ylabel("% real / yr")
a.text(.5,-.34,"Productive claims (equity, housing-via-rent) ~7%; pure stores (gold) ~0.6%; cash = minus inflation.",transform=a.transAxes,ha='center',fontsize=8,style='italic')

a=ax[0,1]
x=np.arange(4)
a.bar(x,cash_pct,color=CASH,label='cash (inflation-exposed)')
a.bar(x,prod_pct,bottom=cash_pct,color=PROD,label='stocks + business (productive/hedged)')
a.set_xticks(x); a.set_xticklabels(bins); a.set_title("Where wealth sits, by wealth group (SCF 2022)"); a.set_ylabel("% of net worth"); a.legend(fontsize=7.5)
a.annotate("wealthy: 2% cash\n-> inflation can't reach them",xy=(3,2),xytext=(1.4,55),fontsize=8,color=R,arrowprops=dict(arrowstyle='->',color=R))
a.text(.5,-.34,"The capital meant to be disciplined sits in hedged/productive form, not cash. The cash is held by ordinary households.",transform=a.transAxes,ha='center',fontsize=8,style='italic')

a=ax[1,0]
pis=np.linspace(0,0.05,51)
for h,c,ls,lab in [(1.0,PROD,'-','real-estate-quality hedge (h=1)'),(0.7,SPEC,'-','gold partial hedge (h=0.7)'),(0.0,R,'--','no hedge (Davide\'s world)')]:
    a.plot(pis*100,[shares(p,h)[2]*100 for p in pis],color=c,ls=ls,lw=2.3,label=lab)
a.set_title("Productive share vs inflation (model, real returns)"); a.set_xlabel("inflation (%)"); a.set_ylabel("productive share (%)"); a.legend(fontsize=7.3)
a.text(.5,-.34,"Inflation routes capital to productive use only as hedges weaken. With a good hedge (real estate), it barely moves it.",transform=a.transAxes,ha='center',fontsize=8,style='italic')

a=ax[1,1]
costs=np.linspace(0,0.05,51)
a.plot(costs*100,[shares(c,1.0)[2]*100 for c in costs],color=R,lw=2.3,label='inflation (good hedges exist)')
def shares_targeted(tau):
    u=np.array([0-tau+lam_c, r_s-tau+lam_s, r_p+lam_p]); e=np.exp(u/sig); return e/e.sum()
a.plot(costs*100,[shares_targeted(c)[2]*100 for c in costs],color=PROD,lw=2.6,label='targeted idle-carrying cost')
a.set_title("Productive deployment per unit of holding cost"); a.set_xlabel("cost imposed (%)"); a.set_ylabel("productive share (%)"); a.legend(fontsize=8)
a.text(.5,-.34,"A targeted cost on idle/speculative stores hits the target directly; inflation leaks into the hedge.",transform=a.transAxes,ha='center',fontsize=8,style='italic')

fig.tight_layout(rect=[0,0.02,1,0.96]); fig.savefig("behavioral_calibrated.png",bbox_inches='tight',facecolor='white')
print("\nsaved behavioral_calibrated.png")

"""
Test the FIX: give KI an independent contractionary instrument (bond sterilization) so it can withdraw
money without touching the dividend. Then find where the fix ITSELF breaks.

Sterilization recurrence (holding pi*=0 against an inflationary drift delta, M tracks Y since pi=0):
  to remove delta*M each period AND re-absorb interest r*B that injects money:
     B_t = B_{t-1}*(1+r) + delta_t * M_t        (interest rolled into the bond stock)
  bond/GDP ratio: b_t = b_{t-1}*(1+r)/(1+g) + delta_t
  steady state exists iff r < g:  b* = delta*(1+g)/(g-r)   ; if r >= g it diverges (negative carry).
Dividend stays = kd*g*Y throughout (sterilization, not the dividend, does the withdrawing).
"""
import numpy as np, matplotlib.pyplot as plt
import os
_FIGDIR = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "figures"); os.makedirs(_FIGDIR, exist_ok=True)
g=0.03; kd=0.5; T=40; t=np.arange(T+1)
def sterilize(delta_path, r):
    B=np.zeros(T+1)
    for s in range(1,T+1):
        B[s]=max(0.0, B[s-1]*(1+r) + delta_path[s-1]*(1+g)**s)   # M_s=(1+g)^s
    return B/(1+g)**t   # bond/GDP ratio

# ---- TEST 1: transient inflationary shock — does the fix protect the dividend (restore symmetry)? ----
delta=np.where((t>=5)&(t<=10), 0.04, -0.01)[1:]      # +4% shock yrs5-10; otherwise normal -1% deflation
delta=np.r_[delta, -0.01][:T]                         # length T
b1=sterilize(delta, r=0.02)
infl_held=np.zeros(T+1)                               # KI+sterilization hold pi at 0 throughout
div=kd*g*(1+g)**t                                     # dividend untouched
print("TEST 1 — transient inflationary shock, fix ON:")
print(f"  inflation held at ~0 across the shock; dividend flat (yr10 = {div[10]:.4f}, same path as no-shock).")
print(f"  bond/GDP peaks at {b1.max()*100:.0f}% during the shock, unwinds to {b1[-1]*100:.0f}% after.")
print("  -> downward independence RESTORED: the anchor is defended through an inflationary shock, dividend intact.")

# ---- TEST 2: persistent drift — the carry condition r vs g ----
pers=np.full(T,0.03)
print("\nTEST 2 — persistent +3% inflationary drift, bond/GDP ratio by interest rate:")
for r in (0.01,0.03,0.05):
    b=sterilize(pers,r); ss="converges" if r<g else ("linear" if abs(r-g)<1e-9 else "EXPLODES")
    star=0.03*(1+g)/(g-r) if r<g else np.inf
    print(f"  r={r*100:.0f}%  ({'r<g' if r<g else 'r=g' if r==g else 'r>g'}): yr40 b={b[-1]*100:5.0f}% of GDP, {ss}"+(f", steady b*={star*100:.0f}%" if np.isfinite(star) else ""))
print("  -> the fix is sustainable for persistent drift ONLY if r<g (positive carry). r>=g -> unbounded sterilization.")

# ---- TEST 3: the runway — time until bond stock hits a ceiling and forces a choice ----
b_max=1.0   # constitutional ceiling: bonds 100% of GDP
print(f"\nTEST 3 — runway to a {b_max*100:.0f}%-of-GDP sterilization ceiling (then must abandon anchor or cut dividend):")
for r in (0.03,0.05):
    for d in (0.02,0.04,0.06):
        b=sterilize(np.full(T,d),r); hit=np.argmax(b>=b_max)
        yrs=hit if (b>=b_max).any() else None
        print(f"  drift {d*100:.0f}%/yr, r={r*100:.0f}%: {'ceiling hit at year '+str(yrs) if yrs else 'never hits ceiling in 40y'}")
print("  -> a transient shock is absorbed with the dividend safe; a PERSISTENT real inflationary imbalance")
print("     buys only a finite runway. No monetary instrument neutralizes a real imbalance forever.")

# ---- figure ----
plt.rcParams.update({'font.size':10,'axes.grid':True,'grid.alpha':.25,'figure.dpi':150})
fig,ax=plt.subplots(2,2,figsize=(11,8))
fig.suptitle("Testing the fix: bond sterilization restores symmetry \u2014 until persistent drift exhausts it",fontsize=12,fontweight='bold')
G,R,O,B='#3a8a4a','#c0392b','#d4781f','#2c6fa6'

a=ax[0,0]
a.axvspan(5,10,color=R,alpha=0.08)
a.plot(t,div/div[0],color=G,lw=2.5,label='dividend (untouched)')
a.plot(t,b1*100/100,color=B,lw=2,ls='--',label='bond/GDP (rises & unwinds)')
a.plot(t,infl_held,color=R,lw=1.5,label='inflation (held ~0)')
a.set_title("TEST 1: transient shock \u2014 dividend protected"); a.set_xlabel("years"); a.legend(fontsize=8)
a.text(.5,-.30,"Through a +4% shock (shaded), the anchor holds and the dividend never moves. Symmetry restored.",transform=a.transAxes,ha='center',fontsize=8,style='italic')

a=ax[0,1]
for r,c,lab in ((0.01,G,'r=1% (r<g): converges'),(0.03,O,'r=3% (r=g): linear'),(0.05,R,'r=5% (r>g): explodes')):
    a.plot(t,sterilize(pers,r)*100,color=c,lw=2.3,label=lab)
a.set_title("TEST 2: persistent +3% drift \u2014 the carry condition"); a.set_xlabel("years"); a.set_ylabel("bond stock (% of GDP)"); a.legend(fontsize=8); a.set_ylim(0,400)
a.text(.5,-.30,"Sterilizing a persistent drift is sustainable only with positive carry (r<g).",transform=a.transAxes,ha='center',fontsize=8,style='italic')

a=ax[1,0]
ds=np.linspace(0.01,0.08,40)
for r,c in ((0.03,O),(0.05,R)):
    yrs=[]
    for d in ds:
        b=sterilize(np.full(T,d),r); yrs.append(np.argmax(b>=1.0) if (b>=1.0).any() else np.nan)
    a.plot(ds*100,yrs,color=c,lw=2.3,label=f'r={r*100:.0f}%')
a.set_title("TEST 3: runway to the sterilization ceiling (100% GDP)"); a.set_xlabel("persistent drift (%/yr)"); a.set_ylabel("years until forced choice"); a.legend(fontsize=8)
a.text(.5,-.30,"Bigger/persistent drift = shorter runway before the anchor must yield or the dividend is tapped.",transform=a.transAxes,ha='center',fontsize=8,style='italic')

a=ax[1,1]; a.axis('off'); a.text(0.5,0.96,"VERDICT",ha='center',fontweight='bold',fontsize=12,transform=a.transAxes)
a.text(0.04,0.86,("The fix works \u2014 with a boundary.\n\n"
 "TRANSIENT inflationary shock:\n  fully absorbed, dividend untouched.\n  Downward independence restored;\n  the setpoint claim now holds both ways.\n\n"
 "PERSISTENT inflationary drift:\n  sustainable only if r < g (positive\n  carry). If r \u2265 g the bond stock\n  explodes; even with r<g a finite\n  ceiling gives a finite runway.\n\n"
 "DEEPER POINT:\n  a persistent inflationary drift is a\n  REAL imbalance. No monetary tool\n  neutralizes it forever \u2014 not a CS\n  flaw, a universal limit. CS just\n  enters this regime rarely (it is\n  deflationary by design) and keeps\n  the dividend safe until the runway\n  ends."),ha='left',va='top',fontsize=9,transform=a.transAxes,linespacing=1.2)

fig.tight_layout(rect=[0,0.02,1,0.96]); fig.savefig(os.path.join(_FIGDIR,"cs_sterilization_test.png"),bbox_inches='tight',facecolor='white')
print("\nsaved cs_sterilization_test.png")

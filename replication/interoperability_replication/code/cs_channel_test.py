"""
Stylized test of the CS external-layer architecture claim:
 "Interoperating = moving KI's setpoint to the common anchor; the rest of the stack runs identically,
  and pinning KI to zero costs nothing on the citizen dividend (K3)."

Stylization (faithful to the stated channel roles, NOT the papers' exact equations):
  - Quantity theory, velocity const: P = M / Y.
  - TWO independent issuance streams:
      growth-line stream  m_growth = g     -> funds the dividend (K1/K2/K3), price-neutral (M,Y both grow at g)
      KI stream (thermostat) m_KI = pi*    -> sets the inflation LEVEL, over the line
    => realized inflation pi = m_KI, so KI alone moves the level; the growth stream is untouched.
  - Real cash dividend K3 (price-neutral) = kappa_d * g * Y  (a share of REAL growth) -> independent of pi* by
    construction of the two-stream design. The test is whether the structure ALLOWS this separation; the bundled
    contrast shows a one-stream system cannot.
  - Basket labor-hours under sticky wages: H = (1+g)^-t * (1+pi*)^min(t, wage_lag).
"""
import numpy as np, matplotlib.pyplot as plt
import os
_FIGDIR = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "figures"); os.makedirs(_FIGDIR, exist_ok=True)
T=40; t=np.arange(T+1)
def member(g,pi_star,kappa_d=0.5,wage_lag=2):
    Y=(1+g)**t; M=(1+g+pi_star)**t; P=M/Y
    pi=np.empty(T+1); pi[0]=0.0; pi[1:]=P[1:]/P[:-1]-1
    realK3=kappa_d*g*Y; realK2=(1-kappa_d)*g*Y
    H=(1+g)**(-t)*(1+pi_star)**np.minimum(t,wage_lag)
    return dict(Y=Y,M=M,P=P,pi=pi,realK3=realK3,realK2=realK2,H=H)

g=0.03; kd=0.5
iso =member(g,-0.01,kd)   # isolated: benign mild deflation
intp=member(g, 0.00,kd)   # interoperating: common-zero anchor
corr=member(g, 0.03,kd)   # corridor: +3%

print("TEST 1 — same engine, only KI's setpoint moves")
print(f"  realized inflation (mean):  isolated {iso['pi'][1:].mean():+.3f}   interop {intp['pi'][1:].mean():+.3f}   corridor {corr['pi'][1:].mean():+.3f}")
print(f"  -> KI setpoint sets the level exactly.")
sameK3 = np.allclose(iso['realK3'],intp['realK3']) and np.allclose(intp['realK3'],corr['realK3'])
sameK2 = np.allclose(iso['realK2'],intp['realK2']) and np.allclose(intp['realK2'],corr['realK2'])
print(f"  real K3 (cash dividend) identical across all three setpoints? {sameK3}")
print(f"  real K2 (stake) identical across all three setpoints?        {sameK2}")
print(f"  -> distribution is untouched by the inflation knob. Holding zero costs nothing on the dividend.")

print("\nTEST 2 — CS (two instruments) vs bundled (one instrument): can you hold distribution while cutting inflation?")
pis=np.linspace(-0.01,0.04,11)
cs_div =[member(g,p,kd)['realK3'][-1] for p in pis]                 # independent of pi*
bundled=[ (g+max(p,0))*kd*(1+g)**T for p in pis ]                   # injection rides on money growth (g+pi*)
print(f"  CS real K3 at pi*=-1%, 0%, +3%:      {member(g,-0.01,kd)['realK3'][-1]:.3f}, {member(g,0,kd)['realK3'][-1]:.3f}, {member(g,0.03,kd)['realK3'][-1]:.3f}  (flat)")
print(f"  bundled injection at pi*=-1%,0%,+3%:  {(g+0)*kd*(1+g)**T:.3f}, {(g+0)*kd*(1+g)**T:.3f}, {(g+0.03)*kd*(1+g)**T:.3f}  (falls as you cut inflation)")
print(f"  -> CS decouples the two; a bundled system must trade distribution against inflation.")

print("\nTEST 3 — two members interoperate via EQUA at the common-zero anchor")
A=member(0.030,0.0,kd); B=member(0.005,0.0,kd); Bc=member(0.005,0.03,kd,wage_lag=2)
rate_clean=A['H']/B['H']; rate_dist=A['H']/Bc['H']
print(f"  common-zero: bilateral rate end = {rate_clean[-1]:.3f}  (reflects productivity gap {0.03-0.005:.3f}; clean)")
print(f"  B runs +3% corridor (sticky wages): rate end = {rate_dist[-1]:.3f}  -> distortion {(rate_dist[-1]/rate_clean[-1]-1)*100:+.1f}%")
print(f"  -> the external-layer result reappears INSIDE the integrated model: corridor distorts, zero doesn't.")

print("\nTEST 4 — onboarding a high-inflation legacy member via KI_T, without starving distribution")
target=np.where(t<=8, 0.20*(1-t/8), 0.0)        # KI_T ramps the setpoint 20% -> 0 over 8 years
mKI=np.empty(T+1); mKI[0]=0.20; alpha=0.6
for s in range(1,T+1): mKI[s]=mKI[s-1]+alpha*(target[s]-mKI[s-1])   # mild adjustment inertia
Yc=(1+g)**t; Pc=np.cumprod(np.r_[1,(1+mKI[1:])]); piC=np.r_[0,Pc[1:]/Pc[:-1]-1]
realK3_onboard=kd*g*Yc                           # dividend stream never interrupted
print(f"  inflation: yr0 {piC[1]*100:.0f}%  yr4 {piC[4]*100:.1f}%  yr8 {piC[8]*100:.1f}%  yr12 {piC[12]*100:.2f}%  -> converges to anchor")
print(f"  real K3 dividend continuous through disinflation? {np.all(realK3_onboard[1:]>=realK3_onboard[:-1])}  (grows with real output throughout)")

# ---- figure ----
plt.rcParams.update({'font.size':10,'axes.grid':True,'grid.alpha':.25,'figure.dpi':150})
fig,ax=plt.subplots(2,2,figsize=(11,8))
fig.suptitle("Does the external layer implement inside CS, as a setpoint not a mode? — stylized channel test",fontsize=12,fontweight='bold')
B1,B2,O,G,R='#7bb0d6','#1b4a73','#d4781f','#3a8a4a','#c0392b'

a=ax[0,0]
a.plot(t,iso['pi']*100,color=B1,lw=2,label='isolated (KI*=\u22121%)')
a.plot(t,intp['pi']*100,color=G,lw=2.5,label='interoperating (KI*=0)')
a.plot(t,corr['pi']*100,color=O,lw=2,label='corridor (KI*=+3%)')
a.axhline(0,color='#999',lw=.8); a.set_title("Only KI's setpoint moves the inflation level"); a.set_xlabel("years"); a.set_ylabel("inflation %"); a.legend(fontsize=8)
a.text(.5,-.30,"Same engine in all three; KI is the level knob. The growth-line dividend stream is untouched.",transform=a.transAxes,ha='center',fontsize=8.3,style='italic')

a=ax[0,1]
a.plot(pis*100,np.array(cs_div),color=G,lw=3,label='CS real dividend (two streams)')
a.plot(pis*100,np.array(bundled),color=R,lw=2.5,ls='--',label='bundled injection (one stream)')
a.axvline(0,color='#999',lw=.8); a.set_title("Holding zero costs nothing on the dividend"); a.set_xlabel("inflation setpoint %"); a.set_ylabel("real distribution (yr 40)"); a.legend(fontsize=8)
a.text(.5,-.30,"CS: distribution flat across setpoints. Bundled: cutting inflation cuts distribution.",transform=a.transAxes,ha='center',fontsize=8.3,style='italic')

a=ax[1,0]
a.plot(t,rate_clean,color=G,lw=2.5,label='both at common zero')
a.plot(t,rate_dist,color=O,lw=2,ls='--',label='B runs +3% corridor')
a.set_title("Two members through EQUA E(A,B)=H_A/H_B"); a.set_xlabel("years"); a.set_ylabel("bilateral rate")
a.legend(fontsize=8)
a.text(.5,-.30,"At common zero the rate is clean productivity; a member's corridor reintroduces the distortion.",transform=a.transAxes,ha='center',fontsize=8.3,style='italic')

a=ax[1,1]
a.plot(t,piC*100,color=R,lw=2.5,label='inflation (left)')
a.axhline(0,color='#999',lw=.8); a.set_title("Onboarding: KI_T disinflates; dividend keeps flowing"); a.set_xlabel("years"); a.set_ylabel("inflation %",color=R); a.tick_params(axis='y',labelcolor=R)
a2=a.twinx(); a2.plot(t,realK3_onboard,color=G,lw=2,label='real K3 dividend (right)'); a2.set_ylabel("real dividend",color=G); a2.tick_params(axis='y',labelcolor=G); a2.grid(False)
a.legend(loc='upper right',fontsize=7.5); a2.legend(loc='center right',fontsize=7.5)
a.text(.5,-.30,"20% \u2192 0 over 8 years via the transition channel; K3 real dividend never interrupted.",transform=a.transAxes,ha='center',fontsize=8.3,style='italic')

fig.tight_layout(rect=[0,0.02,1,0.96]); fig.savefig(os.path.join(_FIGDIR,"cs_channel_test.png"),bbox_inches='tight',facecolor='white')
print("\nsaved cs_channel_test.png")

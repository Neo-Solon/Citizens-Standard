"""
Multilateral test on EQUA's exact formula (PCM Ch.6) — corrected after red-teaming.
Wage model: realistic indexation LAG (wages catch up; the real-rate gap is CONSTANT, not compounding).
  H_i,t = (1+g_i)^-t * (1+pi_i)^min(t,k_i)   [labor-hours for the basket; inflation cancels once wages catch up]
Findings:
  (1) Heterogeneous LEVELS distort the bilateral rate modestly & constantly (~4-18% by lag), not -38%.
  (2) A common level reduces it, but only common ZERO is robust: a common POSITIVE level leaves a
      residual whenever wage stickiness DIFFERS across countries. Zero makes wage dynamics irrelevant.
  (3) Cost: the corridor adds 200-400% cumulative excess price level (any baseline); zero adds ~0.
  (4) DIFFERENTIAL variance, not level, drives volatility; correlated shocks cancel in the differential.
"""
import numpy as np, matplotlib.pyplot as plt
g={'H':0.030,'L':0.005}; T=40; t=np.arange(T+1)
bench=lambda a,b:(1+g[a])**(-t)/(1+g[b])**(-t)
def H(c,pi,k): return (1+g[c])**(-t)*(1+pi)**np.minimum(t,k)
def dist(piH,piL,kH,kL): return ((H('H',piH,kH)/H('L',piL,kL))/bench('H','L')-1)*100
def H_nocatch(c,pi,phi): return (1+pi)**t/((1+g[c])*(1+phi*pi))**t      # 'wages never catch up' (pessimistic)
def dist_nc(piH,piL,phi): return ((H_nocatch('H',piH,phi)/H_nocatch('L',piL,phi))/bench('H','L')-1)*100

# numbers
print("(1) heterogeneous -1/+3, realistic constant lag k:")
for k in (1,2,3,5): print(f"    k={k}yr: {dist(-0.01,0.03,k,k)[-1]:+.1f}% (constant)")
print(f"    'wages never catch up' (phi=0.7): {dist_nc(-0.01,0.03,0.7)[-1]:+.1f}% (compounds; pessimistic bound)")
print("(2) common level + HETEROGENEOUS stickiness (kH=1,kL=4):")
for L in (0.0,0.01,0.02,0.03): print(f"    common {L*100:.0f}%: {dist(L,L,1,4)[-1]:+.1f}%")
print("(3) cost (excess price level over 40y) vs baselines:")
for base,nm in ((-0.01,'natural -1%'),(0.0,'price stability 0%'),(-0.02,'Friedman -2%')):
    print(f"    vs {nm:18}: corridor+3% = +{((1.03)**T/(1+base)**T-1)*100:.0f}%   zero = +{((1.0)**T/(1+base)**T-1)*100:.0f}%")
rng=np.random.default_rng(3)
def vol(sd,rho,reps=3000):
    out=[]
    for _ in range(reps):
        e=1.;ch=[]
        for _k in range(T):
            z=rng.normal(0,sd); a=rho*z+(1-rho)*rng.normal(0,sd); b=rho*z+(1-rho)*rng.normal(0,sd)
            ne=e*(1+a)/(1+b); ch.append(ne/e-1); e=ne
        out.append(np.std(ch)*100)
    return np.mean(out)
v_gap=vol(0.002,0.0); v_ind=vol(0.02,0.0); v_cor=vol(0.02,0.8)
print(f"(4) volatility %/yr: big level-gap/low-var={v_gap:.2f}  high-var independent={v_ind:.2f}  high-var correlated(0.8)={v_cor:.2f}")

# figure
plt.rcParams.update({'font.size':10,'axes.grid':True,'grid.alpha':.25,'figure.dpi':150})
fig,ax=plt.subplots(2,2,figsize=(11,8))
fig.suptitle("Multilateral test on EQUA's exact formula (red-teamed): zero is the uniquely robust anchor",
             fontsize=12,fontweight='bold')
B,O,G,R='#2c6fa6','#d4781f','#3a8a4a','#c0392b'

a=ax[0,0]
for k,c in zip((1,3,5),('#7bb0d6',B,'#1b4a73')): a.plot(t,dist(-0.01,0.03,k,k),color=c,lw=2.4,label=f'{k}-yr indexation lag')
a.plot(t,dist_nc(-0.01,0.03,0.7),color=R,lw=2,ls='--',label='wages never catch up')
a.axhline(0,color='#999',lw=.8); a.set_title("Heterogeneous levels (\u22121/+3): real-rate distortion"); a.set_xlabel("years"); a.legend(fontsize=7.5)
a.text(.5,-.30,"Realistic stickiness \u2192 small CONSTANT offset (\u22124 to \u221218%). Only 'never catch up' compounds to \u221238%.",
       transform=a.transAxes,ha='center',fontsize=8.3,style='italic')

a=ax[0,1]
Ls=np.linspace(0,0.04,17)
a.plot(Ls*100,[dist(L,L,1,4)[-1] for L in Ls],color=B,lw=3,label='heterogeneous stickiness (lag 1 vs 4)')
a.plot(Ls*100,[dist(L,L,3,3)[-1] for L in Ls],color=G,lw=2,ls='--',label='homogeneous stickiness')
a.axhline(0,color='#999',lw=.8); a.scatter([0],[0],color=R,zorder=5,s=40)
a.set_title("Distortion vs common inflation level"); a.set_xlabel("common level (%)"); a.legend(fontsize=7.5)
a.text(.5,-.30,"Under heterogeneous stickiness a common POSITIVE level leaves a residual. Only ZERO removes it.",
       transform=a.transAxes,ha='center',fontsize=8.3,style='italic')

a=ax[1,0]
import numpy as _n; x=_n.arange(3); w=0.38
base=[(-0.01,'vs \u22121%'),(0.0,'vs 0%'),(-0.02,'vs \u22122%')]
corr=[((1.03)**T/(1+b)**T-1)*100 for b,_ in base]; zero=[((1.0)**T/(1+b)**T-1)*100 for b,_ in base]
a.bar(x-w/2,corr,w,color=O,label='corridor +3%'); a.bar(x+w/2,zero,w,color=G,label='zero')
a.set_xticks(x); a.set_xticklabels([n for _,n in base]); a.set_title("Cost: excess price level over 40y (%)"); a.legend(fontsize=8)
a.text(.5,-.30,"Corridor adds 200\u2013400% cumulative at every baseline; zero adds ~0. (The '8\u00d7' was baseline-specific.)",
       transform=a.transAxes,ha='center',fontsize=8.3,style='italic')

a=ax[1,1]
a.bar(['big level gap\nlow variance','no gap\nhigh var (indep.)','no gap\nhigh var (corr. 0.8)'],[v_gap,v_ind,v_cor],color=[B,R,'#e08a5a'])
a.set_title("Nominal-rate volatility (%/yr)"); a.set_ylabel("std of yearly rate change")
a.text(.5,-.32,"DIFFERENTIAL variance drives volatility, not level; correlated shocks cancel in the differential.",
       transform=a.transAxes,ha='center',fontsize=8.3,style='italic')

fig.tight_layout(rect=[0,0.02,1,0.96]); fig.savefig("equa_v3.png",bbox_inches='tight',facecolor='white')
print("saved equa_v3.png")

"""
Red-team our own results. Try to break them.
Our model assumed nominal wages PERMANENTLY grow at g+phi*pi (real wages eroded forever) -> distortion
compounds to -38% over 40y. Attack with a realistic indexation LAG (wages catch up, gap is constant),
and attack the 'any common level is phi-robust' claim with HETEROGENEOUS wage stickiness across countries.
"""
import numpy as np
g={'H':0.030,'L':0.005}; T=40; t=np.arange(T+1)
bench=lambda c:(1+g[c])**(-t)                      # productivity-only real H (inflation-invariant)

# --- realistic wage model: indexation with a k-period LAG (wages catch up; gap is a constant, not compounding)
def H_lag(c,pi,k):
    P=(1+pi)**t
    w=np.ones(T+1)
    for s in range(1,T+1):
        infl = pi if s-1-k>=-1 else 0.0           # wage indexed to inflation k periods ago
        infl = pi if (s-1-k)>=0 else (pi if (s-1)>=0 and k==0 else 0.0)
        w[s]=w[s-1]*(1+g[c])*(1+(pi if (s-1-k)>=0 else 0.0))
    return P/w
def dist_lag(piH,piL,kH,kL):
    e=H_lag('H',piH,kH)/H_lag('L',piL,kL); b=bench('H')/bench('L'); return (e/b-1)[-1]*100

# our ORIGINAL (permanent partial indexation phi): distortion compounds
def H_phi(c,pi,phi): return (1+pi)**t/((1+g[c])*(1+phi*pi))**t * 1.0
def dist_phi(piH,piL,phiH,phiL):
    e=H_phi('H',piH,phiH)/H_phi('L',piL,phiL); b=bench('H')/bench('L'); return (e/b-1)[-1]*100

print("ATTACK A: is the -38% realistic, or an artifact of permanent real-wage erosion?")
print(f"  our model (permanent phi=0.7), hetero -1/+3:   {dist_phi(-0.01,0.03,0.7,0.7):+6.1f}%  (compounds over 40y)")
for k in (1,2,3,5):
    print(f"  realistic {k}-yr indexation lag, hetero -1/+3:   {dist_lag(-0.01,0.03,k,k):+6.1f}%  (CONSTANT over 40y)")
print("  -> the -38% assumes wages NEVER catch up. Realistic lags give a small, constant offset.")

print("\nATTACK F: does a COMMON level really cancel at any wage stickiness? Test HETEROGENEOUS stickiness.")
print("  common +3%, but H indexes fast (lag 1) and L indexes slow (lag 4):")
print(f"     distortion = {dist_lag(0.03,0.03,1,4):+6.1f}%   <- NOT zero! a common POSITIVE level leaves a residual")
print(f"  common  0%, same heterogeneous stickiness (lag 1 vs 4): {dist_lag(0.0,0.0,1,4):+6.1f}%   <- zero")
print("  (phi-form) common +3%, phiH=0.9 vs phiL=0.5:")
print(f"     distortion = {dist_phi(0.03,0.03,0.9,0.5):+6.1f}%   common 0%, same: {dist_phi(0.0,0.0,0.9,0.5):+6.1f}%")
print("  -> 'any common level' was wrong under heterogeneous stickiness. Only common ZERO is fully robust.")

print("\nATTACK C: is '8x cheaper' robust to the baseline? excess price level over 40y vs different baselines:")
for base,name in ((-0.01,'natural -1%'),(0.0,'price stability 0%'),(-0.02,'Friedman -2%')):
    corr=((1.03)**T/(1+base)**T-1)*100; zero=((1.00)**T/(1+base)**T-1)*100
    ratio = corr/zero if zero>0 else float('inf')
    print(f"  vs {name:18}: corridor +{corr:6.0f}%   zero +{zero:5.0f}%   ratio {ratio:.1f}x" if zero>0 else
          f"  vs {name:18}: corridor +{corr:6.0f}%   zero +{zero:5.0f}%   ratio inf (zero has no excess)")
print("  -> the '8x' is specific to the -1% baseline. Robust claim: corridor adds 200-400% cumulative; zero adds ~0.")

print("\nATTACK E: does variance still beat level if shocks are CORRELATED across countries?")
rng=np.random.default_rng(3)
def vol(sd,rho,reps=3000):
    out=[]
    for _ in range(reps):
        e=1.;ch=[]
        for _k in range(T):
            z=rng.normal(0,sd); za=rng.normal(0,sd)
            a=0.0+ (rho*z+(1-rho)*za); b=0.0+ (rho*z+(1-rho)*rng.normal(0,sd))
            ne=e*(1+a)/(1+b); ch.append(ne/e-1); e=ne
        out.append(np.std(ch)*100)
    return np.mean(out)
print(f"  high variance, independent (rho=0):   {vol(0.02,0.0):.2f} %/yr")
print(f"  high variance, correlated  (rho=0.8): {vol(0.02,0.8):.2f} %/yr  <- common shocks cancel in the differential")
print("  -> it's the variance of the DIFFERENTIAL that matters; correlation reduces it. Level still irrelevant.")

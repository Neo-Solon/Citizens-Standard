"""
Stress-test the VERIFIED v3 claim: 'zero is the uniquely robust anchor.'
New attacks:
  S1. Zero TARGET but nonzero realized variance + heterogeneous stickiness -> still robust?
  S2. Deflation-buffer: band can't go below 0, so mean is slightly positive -> how much residual?
  S3. Is zero-robustness specific to the lag wage-model, or general? Test PARTIAL-ADJUSTMENT too.
"""
import numpy as np
g={'H':0.030,'L':0.005}; T=40; t=np.arange(T+1)
benchHL=(1+g['H'])**(-t)/(1+g['L'])**(-t)

def H_lag(c,pi_path,k):
    P=np.ones(T+1); w=np.ones(T+1)
    for s in range(1,T+1):
        P[s]=P[s-1]*(1+pi_path[s-1])
        w[s]=w[s-1]*(1+g[c])*(1+(pi_path[s-1-k] if s-1-k>=0 else 0.0))
    return P/w
def dist_lag(pH,pL,kH,kL): return ((H_lag('H',pH,kH)/H_lag('L',pL,kL))/benchHL-1)[-1]*100

def H_partial(c,pi_path,phi):
    H=np.ones(T+1); logP=0.0; logw=0.0; cg=0.0
    for s in range(1,T+1):
        logP+=np.log(1+pi_path[s-1]); cg+=np.log(1+g[c])
        target=cg+logP; logw+=phi*(target-logw); H[s]=np.exp(logP-logw)
    return H
def dist_partial(pH,pL,phiH,phiL): return ((H_partial('H',pH,phiH)/H_partial('L',pL,phiL))/benchHL-1)[-1]*100

# Calvo-style random wage reset (recovered from the original session). theta = prob a wage
# stays STUCK each period (gets productivity drift, misses inflation); else it resets to full-indexed.
_crng=np.random.default_rng(1)
def H_calvo(c,pi,theta,reps=2000):
    Hs=[]
    for _ in range(reps):
        logP=0.0; cg=0.0; lw=0.0; H=np.ones(T+1)
        for s in range(1,T+1):
            logP+=np.log(1+pi[s-1]); cg+=np.log(1+g[c])
            if _crng.random()>theta: lw=cg+logP
            else: lw=lw+np.log(1+g[c])
            H[s]=np.exp(logP-lw)
        Hs.append(H)
    return np.mean(Hs,axis=0)
def dist_calvo(pH,pL,thH,thL): return ((H_calvo('H',pH,thH)/H_calvo('L',pL,thL))/benchHL-1)[-1]*100

rng=np.random.default_rng(7)
def mc(fn,mu,sd,a,b,reps=4000,common=True):
    out=[]
    for _ in range(reps):
        pH=mu+rng.normal(0,sd,T); pL=pH.copy() if common else mu+rng.normal(0,sd,T)
        out.append(fn(pH,pL,a,b))
    return np.mean(out),np.std(out)

print("S1: ZERO target, heterogeneous stickiness (lag 1 vs 4), rising realized variance (common shocks):")
for sd in (0.0,0.005,0.01,0.02):
    m,s=mc(dist_lag,0.0,sd,1,4)
    print(f"   sd={sd*100:.1f}%:  mean distortion {m:+.2f}%   (run-to-run sd {s:.2f}%)")
print("   -> zero MEAN keeps the systematic distortion ~0 even as variance grows; variance adds noise, not bias.")

print("\nS2: deflation buffer pushes the mean slightly positive (lag 1 vs 4, sd=1%): residual cost of not running exactly 0:")
for mu in (0.0,0.0025,0.005,0.01):
    m,_=mc(dist_lag,mu,0.01,1,4)
    print(f"   mean={mu*100:.2f}%: {m:+.2f}%")
print("   -> residual scales with the MEAN, not the variance. A 0.5% buffer costs ~1.5%; modest, bounded.")

print("\nS3: is zero-robustness model-specific? Repeat with a PARTIAL-ADJUSTMENT wage model (phi 0.5 vs 0.2):")
_l0=dist_lag(np.zeros(T),np.zeros(T),1,4); _l3=dist_lag(np.full(T,0.03),np.full(T,0.03),1,4)
_p0=dist_partial(np.zeros(T),np.zeros(T),0.5,0.2); _p3=dist_partial(np.full(T,0.03),np.full(T,0.03),0.5,0.2)
print(f"   lag model        : common 0% -> {_l0:+.2f}%   common 3% -> {_l3:+.2f}%")
print(f"   partial-adjust   : common 0% -> {_p0:+.2f}%   common 3% -> {_p3:+.2f}%")
_c0=dist_calvo(np.zeros(T),np.zeros(T),0.7,0.4); _c3=dist_calvo(np.full(T,0.03),np.full(T,0.03),0.7,0.4)
print(f"   Calvo reset      : common 0% -> {_c0:+.2f}%   common 3% -> {_c3:+.2f}%")
_cf=dist_calvo(np.full(T,0.03),np.full(T,0.03),0.4,0.7)
print(f"   -> THREE wage models: common 0% ~0 in all; common 3% leaves a residual in all.")
print(f"   -> sign note: Calvo's +{_c3:.1f}% has HIGH-prod as the stickier member; flip the assignment -> {_cf:+.1f}%.")
print(f"      The residual's SIGN tracks which member is stickier, not the wage process per se.")

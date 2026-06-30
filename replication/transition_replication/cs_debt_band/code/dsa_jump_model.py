"""
NEW MODEL CLASS: compound-jump, not Gaussian-regime.
  - baseline r-g: TIGHT negative Gaussian N(mu_c, sd_c) with sd_c SMALL, so a
    normal year is essentially never positive (kills spurious reversals).
  - JUMPS: rare large POSITIVE spikes. Arrival hazard lam(d). At low debt a jump
    is a single isolated year (no 2yr runs -> low reversal). At high debt jumps
    PERSIST/cluster (prob p_persist(d)) -> multi-year positive episodes -> high
    reversal. Jump magnitude large (lifts the 5y-avg tail without making positive
    years common).
This separates SEVERITY (jump magnitude) from REVERSAL FREQUENCY (jump
persistence) structurally, which the Gaussian model could not. Test the mechanism
DIRECTLY at clean parameters before any calibration.
"""
import random
H=28
def series(d0,years,P):
    mu_c,sd_c,lam0,lam1,Jmag,Jsd,pp0,pp1=P
    lam=min(0.6,max(0.0,lam0+lam1*max(0.0,d0-0.40)))     # jump arrival hazard
    pp =min(0.85,max(0.0,pp0+pp1*max(0.0,d0-0.40)))      # jump persistence (cluster) w/ debt
    out=[]; in_jump=False
    for _ in range(years):
        if in_jump:
            in_jump = random.random()<pp                  # persist?
        if not in_jump:
            in_jump = random.random()<lam                 # new jump?
        if in_jump:
            out.append(random.gauss(Jmag,Jsd))            # large positive spike
        else:
            out.append(random.gauss(mu_c,sd_c))           # tight negative baseline
    return out
def has_ep(v,sign,start=0):
    run=0
    for i in range(start,len(v)):
        ok=(v[i]<0) if sign<0 else (v[i]>0)
        run=run+1 if ok else 0
        if run>=2: return True,i
    return False,len(v)
def sev(d0,P,N=8000):
    a=sorted(sum(series(d0,5,P))/5 for _ in range(N)); return a[int(.5*N)],a[int(.9*N)]
def rev(d0,P,N=8000):
    h=v=0
    for _ in range(N):
        s=series(d0,H,P); nf,ne=has_ep(s,-1,0)
        if not nf: continue
        v+=1; pf,_=has_ep(s,+1,ne+1); h+=pf
    return h/max(1,v)
def negshare(d0,P,N=2500):
    t=n=0
    for _ in range(N):
        for x in series(d0,10,P): t+=1;n+=(x<0)
    return n/t

# CLEAN hand-set parameters to test the mechanism (not a search):
# tight baseline; rare single jumps at low debt; clustered jumps at high debt
P=(-0.013, 0.004,        # mu_c, sd_c (TIGHT)
   0.05, 0.30,           # lam0, lam1 (jump hazard: 0.05 low-debt -> ~0.29 @120%)
   0.060, 0.015,         # Jmag, Jsd (large +6% spike)
   0.10, 0.55)           # pp0, pp1 (persistence: 0.10 low-debt -> ~0.54 @120%)
print("CLEAN JUMP MODEL -- direct mechanism test (hand-set, no search)\n")
for d in (0.40,0.45,0.60,1.00,1.20):
    s50,s90=sev(d,P)
    print(f"  debt={int(d*100):>3}%:  5y-avg median {100*s50:+.2f}%  90th {100*s90:+.2f}%")
print()
rl=rev(0.45,P); rh=rev(1.00,P); ns=negshare(0.60,P)
s40m,s40=sev(0.40,P); s120m,s120=sev(1.20,P)
print("  KEY MOMENTS vs targets:")
print(f"    sev90@40%   {100*s40:+.2f}%   (target  0.0%)")
print(f"    sev90@120%  {100*s120:+.2f}%   (target +2.0%)")
print(f"    median@40%  {100*s40m:+.2f}%   (target -1.2%)")
print(f"    medrise     {100*(s120m-s40m):+.2f}%   (target +0.8%)")
print(f"    reversal@45% {100*rl:.0f}%    (target ~25%)")
print(f"    reversal@100% {100*rh:.0f}%   (target >=75%)")
print(f"    negshare@60% {100*ns:.0f}%   (target >50%)")
print(f"""
  Mechanism check: does the jump model finally get reversal@45% near 25% WHILE
  sev90@40% reaches ~0? If yes, the jump class is the right model and we calibrate
  it. If reversal@45% is still high, the Gaussian-era contradiction was not about
  model class.""")

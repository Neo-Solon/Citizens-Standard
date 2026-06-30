"""
DIAGNOSE the low-debt reversal mismatch BEFORE adding any parameter.
Hypothesis: the absolute reversal probability depends on the observation HORIZON
H, which I fixed at 40y arbitrarily. Lian's reversal is measured over a finite
window. If a shorter H makes rev_low ~25% while rev_high stays high, the mismatch
was horizon mis-specification, not a missing 4th element.

Severity (a 5y-average metric) is INDEPENDENT of H, so it stays put regardless.
Sweep H, watch rev@45% and rev@100%.
"""
import random
random.seed(2024)
MR=6000
# representative parameter set from the v9/v10 family (good reversal structure)
mu_c,sd_c,h0,h1,m0,m1,sd_s,e0,e1 = -0.0123,0.0061,0.010,0.50,0.015,0.016,0.032,0.57,0.39
def series(d0,years):
    h=min(0.7,max(0.0,h0+h1*max(0.0,d0-0.40))); ms=m0+m1*max(0.0,d0-0.40)
    ex=max(0.15,e0-e1*max(0.0,d0-0.40))
    regime="stress" if random.random()<h/(h+ex) else "calm"; out=[]
    for _ in range(years):
        if regime=="calm":
            if random.random()<h: regime="stress"
        else:
            if random.random()>ex: regime="calm"
        out.append(random.gauss(mu_c,sd_c) if regime=="calm" else random.gauss(ms,sd_s))
    return out
def has_ep(v,sign,start=0):
    run=0
    for i in range(start,len(v)):
        ok=(v[i]<0) if sign<0 else (v[i]>0)
        run=run+1 if ok else 0
        if run>=2: return True,i
    return False,len(v)
def rev_H(d0,H):
    hits=valid=0
    for _ in range(MR):
        v=series(d0,H); nf,ne=has_ep(v,-1,0)
        if not nf: continue
        valid+=1; pf,_=has_ep(v,+1,ne+1); hits+=pf
    return hits/max(1,valid)

print("Reversal probability vs observation horizon H (same fixed parameters)")
print(f"  {'H (years)':>10}{'rev@45% (~25)':>16}{'rev@100% (>75)':>16}{'gap hi-lo':>12}")
for H in (5,8,10,12,15,20,30,40):
    rl=rev_H(0.45,H); rh=rev_H(1.00,H)
    print(f"  {H:>10}{100*rl:>15.0f}%{100*rh:>15.0f}%{100*(rh-rl):>11.0f}")
print("""
If rev@45% crosses ~25% at some modest H while rev@100% stays >=75%, the earlier
mismatch was HORIZON, not a missing 4th element. That is the academically correct
fix: pin H to Lian's measurement window rather than inflate the model.""")

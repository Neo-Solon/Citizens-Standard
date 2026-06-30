"""
VERIFY the one untested hypothesis: is low-debt reversal high because my CALM
state is i.i.d. noise rather than a DURABLE regime? Diagnostic: directly vary a
calm-persistence parameter 'phi' = extra probability that, having had a negative
year, the next year is also forced negative (financial-repression momentum),
applied ONLY at low debt and fading with debt. Watch reversal_low and severity.
If phi pulls reversal_low 40%->25% while sev90@40 stays ~0, THAT is the mechanism.
"""
import random
H=28
# fixed reasonable base params; vary only phi0 (low-debt calm momentum)
BASE=dict(mu_c=-0.0122, sd_c=0.0090, h0=0.030, h1=0.50, m0=0.020, m1=0.0,
          sd_s=0.030, e0=0.55, e1=0.40)
def series(d0,years,phi0,phi1):
    p=BASE
    h=min(0.75,max(0.0,p['h0']+p['h1']*max(0.0,d0-0.40))); ms=p['m0']+p['m1']*max(0.0,d0-0.40)
    ex=max(0.18,min(0.92,p['e0']-p['e1']*max(0.0,d0-0.40)))
    phi=max(0.0,phi0-phi1*max(0.0,d0-0.40))     # calm momentum, strong@low debt
    regime="stress" if random.random()<h/(h+ex) else "calm"; out=[]; prev_neg=True
    for _ in range(years):
        if regime=="calm":
            if random.random()<h: regime="stress"
        else:
            if random.random()>ex: regime="calm"
        if regime=="calm":
            v=random.gauss(p['mu_c'],p['sd_c'])
            # financial-repression momentum: if last year was negative, with prob phi
            # force this calm draw to stay negative (resample to <0)
            if prev_neg and random.random()<phi and v>0:
                v=-abs(random.gauss(p['mu_c'],p['sd_c']))
        else:
            v=random.gauss(ms,p['sd_s'])
        out.append(v); prev_neg=(v<0)
    return out
def has_ep(v,sign,start=0):
    run=0
    for i in range(start,len(v)):
        ok=(v[i]<0) if sign<0 else (v[i]>0)
        run=run+1 if ok else 0
        if run>=2: return True,i
    return False,len(v)
def rev(d0,phi0,phi1,N=8000):
    h=v=0
    for _ in range(N):
        s=series(d0,H,phi0,phi1); nf,ne=has_ep(s,-1,0)
        if not nf: continue
        v+=1; pf,_=has_ep(s,+1,ne+1); h+=pf
    return h/max(1,v)
def sev(d0,phi0,phi1,N=8000):
    a=sorted(sum(series(d0,5,phi0,phi1))/5 for _ in range(N)); return a[int(.5*N)],a[int(.9*N)]

print("Diagnostic: vary low-debt calm momentum phi0 (phi1=0.6 fades it by high debt)\n")
print(f"  {'phi0':>6}{'rev@45%':>10}{'rev@100%':>11}{'sev90@40':>11}{'sev90@120':>12}")
for phi0 in (0.0,0.3,0.5,0.7,0.85):
    rl=rev(0.45,phi0,0.6); rh=rev(1.00,phi0,0.6)
    s40m,s40=sev(0.40,phi0,0.6); s120m,s120=sev(1.20,phi0,0.6)
    print(f"  {phi0:>6.2f}{100*rl:>9.0f}%{100*rh:>10.0f}%{100*s40:>10.2f}%{100*s120:>11.2f}%")
print("""
If reversal@45% falls toward ~25% as phi0 rises while reversal@100% stays >=75%
and sev90@40 stays near 0, the missing structure is low-debt CALM PERSISTENCE
(financial-repression momentum) -- a real, citable mechanism (Reinhart-Sbrancia
financial repression; Mauro-Zhou persistence). That becomes the principled 4th
element, earned by diagnosis.""")

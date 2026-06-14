"""
verify_proposition_9.py
-----------------------
Reproduces Proposition 9 (Section 3.8 / Appendix A.12) of Neo-Solon (2026e):
robustness of circuit separation to endogenous bank credit. Banks lend against
PLEDGEABLE asset wealth only; locked floors are non-pledgeable, so credit
intensity kappa_bank = m*phi_liq (m=LTV, phi_liq=liquid fraction). A share chi_c
of new credit is spent into the transactional circuit, adding an asset->consumer
coupling chi_c*kappa_bank to the structural leak. Separation = Prop 7 determinacy:
both eigenvalues of M=[[theta,-zeta],[-b/a,1/a]] outside the unit circle.
Parts: (i) coupling under locked vs pledgeable collateral; (ii) conservative
critical intensity; (iii) the lock is decisive (critical LTV); (iv) structural
buyer damps the accelerator (second margin). numpy only.
"""
import numpy as np
r=0.045; a=1/(1+r); theta=1+(1+0.5)/4.0
lam=0.03; chi_c=0.30; zstar=0.127
def nexp(zeta,b):
    M=np.array([[theta,-zeta],[-b/a,1/a]]); return int(np.sum(np.abs(np.linalg.eigvals(M))>1+1e-12))
def sep_conservative(kb):  ze=lam+chi_c*kb; return nexp(ze,ze)==2          # accelerator on (symmetric)
def sep_structural(kb):    ze=lam+chi_c*kb; return nexp(ze,lam)==2          # accelerator damped

def part1():
    print("="*70); print("PART 1 — bank-credit coupling: locked vs pledgeable collateral  [Prop 9(i)]"); print("="*70)
    rows=[("locked baseline",0.15,0.50),("NO-LOCK counterfactual",1.00,0.50)]
    ok=True
    for tag,phi,m in rows:
        kb=phi*m; ze=lam+chi_c*kb
        print("  %-22s phi_liq=%.2f m=%.2f kappa_bank=%.3f zeta_tot=%.3f | sep(conservative)=%s sep(structural)=%s"%(
              tag,phi,m,kb,ze,sep_conservative(kb),sep_structural(kb)))
    ok = sep_conservative(0.075) and (not sep_conservative(0.50)) and sep_structural(0.50)
    print("  [locked safe under both; no-lock breaks conservative, saved only by structural buyer]:", ok); return ok

def part2():
    print("="*70); print("PART 2 — conservative critical credit intensity  [Prop 9(ii)]"); print("="*70)
    kbc=(zstar-lam)/chi_c
    lo,hi=0.0,1.0
    for _ in range(60):
        mid=.5*(lo+hi)
        if sep_conservative(mid): lo=mid
        else: hi=mid
    num=.5*(lo+hi)
    print("  analytic kappa_bank* = (zstar-lam)/chi_c = %.3f ; numeric = %.3f"%(kbc,num))
    print("  [paper: separation iff m*phi_liq < ~0.32]")
    return abs(kbc-0.323)<0.01 and abs(num-kbc)<0.01

def part3():
    print("="*70); print("PART 3 — the lock is decisive: critical LTV m*=kappa*/phi_liq  [Prop 9(iii)]"); print("="*70)
    kbc=(zstar-lam)/chi_c; ok=True
    for phi in (0.10,0.15,0.25,0.50,1.00):
        ms=kbc/phi
        tag="(no feasible LTV)" if ms>1 else "(breaks at LTV>=%.2f)"%ms
        print("  phi_liq=%.2f : m* = %.2f  %s"%(phi,ms,tag))
    print("  locked (phi_liq=0.15): m*=%.2f (>1) ; no-lock (phi_liq=1): m*=%.2f (ordinary)"%(kbc/0.15,kbc/1.0))
    return (kbc/0.15>1) and (kbc/1.0<0.5)

def part4():
    print("="*70); print("PART 4 — structural buyer damps accelerator (2nd margin)  [Prop 9(iv)]"); print("="*70)
    lo,hi=0.0,3.0
    for _ in range(60):
        mid=.5*(lo+hi)
        if sep_structural(mid): lo=mid
        else: hi=mid
    ks=.5*(lo+hi)
    print("  damped-accelerator critical intensity kappa_bank* = %.3f (vs 0.32 conservative)"%ks)
    print("  baseline kappa_bank=0.075 inside both bounds:", sep_conservative(0.075) and sep_structural(0.075))
    return ks>1.0

def main():
    a,b,c,d=part1(),part2(),part3(),part4()
    print("="*70); print("All Proposition 9 claims reproduced:", bool(a and b and c and d)); print("="*70)

if __name__=="__main__": main()

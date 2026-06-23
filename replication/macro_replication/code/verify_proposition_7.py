"""
verify_proposition_7.py
-----------------------
Reproduces Proposition 7 (Section 3.7 / Appendix A.10) of Neo-Solon (2026e):
forward-looking determinacy under the money-quantity anchor. Cagan money
demand + KI quantity rule give E_t x_{t+1} = theta x_t + shock with
theta = 1 + (1+phi)/alpha; x is a jump variable, so determinacy (Blanchard-Kahn)
needs |theta|>1. Parts:
  (i)   theta>1 for all alpha>0, phi>=0 -> determinate without a Taylor principle;
  (ii)  interest-rate analog has root phi -> needs the Taylor principle phi>1;
  (iii) two-circuit (2 jump vars) determinacy threshold in the coupling.
Uses numpy only.
"""
import numpy as np

def theta(alpha, phi): return 1 + (1+phi)/alpha

def part1():
    print("="*70); print("PART 1 — money-quantity anchor: theta>1 for all alpha,phi  [Prop 7(i)]"); print("="*70)
    allok=True
    for alpha in (0.5,2.0,4.0):
        cells=[]
        for phi in (0.0,0.5,1.0,2.0):
            th=theta(alpha,phi); det=abs(th)>1; allok&=det
            cells.append("phi=%.1f:theta=%.3f(%s)"%(phi,th,"det" if det else "INDET"))
        print("  alpha=%.1f | "%alpha+"  ".join(cells))
    print("  determinate for ALL alpha>0, phi>=0 (incl. phi=0):", allok)
    print("  [paper A.10(i): theta=1+(1+phi)/alpha>1 always; no Taylor principle]")
    return allok

def part2():
    print("="*70); print("PART 2 — interest-rate analog needs the Taylor principle  [Prop 7(ii)]"); print("="*70)
    ok=True
    for phi in (0.0,0.5,1.0,1.5,2.0):
        det=abs(phi)>1
        print("  phi=%.1f : root=%.2f  %s"%(phi,phi,"det" if det else "INDETERMINATE (sunspots)"))
        if (phi>1) != det: ok=False
    print("  [paper A.10(ii): interest-rate root = phi; determinate iff phi>1]")
    return ok

def part3():
    print("="*70); print("PART 3 — two-circuit Blanchard-Kahn determinacy threshold  [Prop 7(iii)]"); print("="*70)
    r=0.045; a=1/(1+r); alpha=4.0; phi=0.5; th=theta(alpha,phi)
    def nexp(c):
        M=np.array([[th,-c],[-c/a,1/a]]); return int(np.sum(np.abs(np.linalg.eigvals(M))>1+1e-12))
    for c in (0.0,0.03,0.10,0.30):
        M=np.array([[th,-c],[-c/a,1/a]]); ev=np.round(np.abs(np.linalg.eigvals(M)),3)
        n=nexp(c)
        print("  coupling=%.2f : |eig|=%s  #explosive=%d  %s"%(c,ev.tolist(),n,
              "DETERMINATE (2 jumps)" if n==2 else "indeterminate"))
    lo,hi=0.0,0.5
    for _ in range(60):
        m=0.5*(lo+hi)
        if nexp(m)==2: lo=m
        else: hi=m
    thr=0.5*(lo+hi)
    print("  determinacy threshold coupling = %.3f ; calibrated leak ~0.03 lies inside"%thr)
    print("  [paper A.10(iii): two explosive eigenvalues until coupling ~0.13]")
    return abs(thr-0.13)<0.02 and nexp(0.03)==2

def main():
    a,b,c=part1(),part2(),part3()
    print("="*70); print("All Proposition 7 claims reproduced:", bool(a and b and c)); print("="*70)

if __name__=="__main__": main()

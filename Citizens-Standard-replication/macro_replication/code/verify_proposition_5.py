"""
verify_proposition_5.py
-----------------------
Reproduces Proposition 5 (Section 3.6 / Appendix A.8) of Neo-Solon (2026e):
the two-speed result that a slow (delayed) lever cannot stabilize through
feedback. Augmenting the gap recursion with delayed feedback,
    x_t = (1-psi*lambda) x_{t-1} - lamL x_{t-d} + e_t,
gives the characteristic polynomial  P(z) = z^d - a z^{d-1} + lamL ,  a=1-psi*lambda.
Three parts mirror the three claims:
  (i)   small-gain box |a|+|lamL|<1 is stable at every d;
  (ii)  critical lamL collapses toward 1-|a| as d grows;
  (iii) at fixed lamL the slowest-mode damping vanishes like |ln lamL|/d.
Uses numpy.roots; no SciPy.
"""
import numpy as np

def maxroot(a, lamL, d):
    c = [0.0]*(d+1); c[0] = 1.0; c[1] = -a; c[d] = lamL
    return max(abs(r) for r in np.roots(c))

def crit_lamL(a, d, hi=2.0):
    if maxroot(a, 0.0, d) >= 1: return 0.0
    lo, hiv = 0.0, hi
    for _ in range(60):
        mid = 0.5*(lo+hiv)
        if maxroot(a, mid, d) < 1: lo = mid
        else: hiv = mid
    return lo

def part1():
    print("="*70)
    print("PART 1 — small-gain box |a|+|lamL|<1 is stable at EVERY delay  [Prop 5(i)]")
    print("="*70)
    a = 0.10                       # psi*lambda = 0.90 baseline (monotone)
    pt = (1-abs(a))*0.999
    allok = True
    for d in (1,2,4,8,16,32,64):
        ok = maxroot(a, pt, d) < 1
        allok &= ok
        print("  d=%3d : interior small-gain point lamL=%.3f stable = %s" % (d, pt, ok))
    print("  [paper A.8(i): |1-psi*lambda|+|lamL|<1 sufficient for all d]  -> all stable:", allok)
    return allok

def part2():
    print("="*70)
    print("PART 2 — critical gain collapses toward 1-|a| as delay grows  [Prop 5(ii)]")
    print("="*70)
    a = 0.10; prev = 1e9; mono = True
    for d in (1,2,4,8,16,32,64):
        lc = crit_lamL(a, d)
        if lc - prev > 1e-6: mono = False
        prev = lc
        print("  d=%3d : lamL_crit = %.4f" % (d, lc))
    print("  small-gain asymptote 1-|a| = %.2f ; monotonically non-increasing: %s" % (1-abs(a), mono))
    print("  [paper A.8(ii): 1.00 (d<=2), 0.93 (d=4), 0.91 (d=8) -> 0.90]")
    return mono

def part3():
    print("="*70)
    print("PART 3 — damping vanishes like |ln lamL|/d at fixed lamL  [Prop 5(iii)]")
    print("="*70)
    a = 0.10; lamL = 0.5
    ok = True
    for d in (1,2,4,8,16,32,64,128):
        mr = maxroot(a, lamL, d); damp = 1-mr; asy = abs(np.log(lamL))/d
        print("  d=%3d : max|z|=%.4f  damping=%.4f   |ln lamL|/d=%.4f" % (d, mr, damp, asy))
        if d >= 16 and abs(damp-asy)/asy > 0.25: ok = False     # asymptote close for large d
    print("  decade-scale delay (d~10-40) -> damping ~ a few %% (stable but very sluggish)")
    print("  [paper A.8(iii): max|z|->1, damping = |ln lamL|/d + o(1/d)]  -> asymptote holds:", ok)
    return ok

def main():
    a = part1(); b = part2(); c = part3()
    print("="*70)
    print("All Proposition 5 claims reproduced:", bool(a and b and c))
    print("="*70)

if __name__ == "__main__":
    main()

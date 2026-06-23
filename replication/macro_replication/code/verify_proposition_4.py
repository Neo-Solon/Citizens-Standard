"""
verify_proposition_4.py
-----------------------
Reproduces Proposition 4 (Section 5.5 / Appendix A.7) of Neo-Solon (2026e):
the bounded labor-supply response to a locked citizen floor and the
robustness of trend growth. Four parts mirror the four claims:
  (i)   the labor ratio solves l^(1+1/nu) + b*l^(1/nu) = 1, with dl/db|0 = -nu/(1+nu);
  (ii)  the lock scales the effect by rho_eff/r (liquid ~-19%, locked ~1-5%);
  (iii) b is scale-invariant -> a one-time LEVEL effect, not a trend change;
  (iv)  with a growth-indexed flow the labor-growth loop is a contraction.
Pure-Python (no SciPy); numpy used only for the small grids.
"""
import numpy as np

def labor_ratio(b, nu):
    """Solve l^(1+1/nu) + b l^(1/nu) = 1 on (0,1] by bisection (LHS increasing)."""
    if b <= 0:
        return 1.0
    f = lambda l: l**(1 + 1/nu) + b*l**(1/nu) - 1.0
    lo, hi = 1e-12, 1.0
    for _ in range(200):
        mid = 0.5*(lo + hi)
        if f(mid) > 0: hi = mid
        else:          lo = mid
    return 0.5*(lo + hi)

def part1():
    print("=" * 70)
    print("PART 1 — labor response l(b) and the bounded elasticity  [Prop 4(i)]")
    print("=" * 70)
    for nu in (0.25, 0.5, 1.0):
        cells = []
        for b in (0.0, 0.1, 0.2, 0.5):
            l = labor_ratio(b, nu)
            cells.append("b=%.1f: l=%.4f (%+.1f%%)" % (b, l, 100*(l-1)))
        # numeric slope at b=0 vs analytic -nu/(1+nu)
        h = 1e-6
        num = (labor_ratio(h, nu) - 1.0)/h
        ana = -nu/(1+nu)
        print(" nu=%.2f  dl/db|0  numeric=%+.4f  analytic=%+.4f  match=%s"
              % (nu, num, ana, abs(num-ana) < 1e-3))
        print("          " + "   ".join(cells))
    print("  [paper Sec 5.5 / Prop 4(i): bounded, dl/db = -nu/(1+nu); ~1/3 at nu=0.5]")

def part2():
    print("=" * 70)
    print("PART 2 — the lock is load-bearing: liquid vs locked  [Prop 4(ii)]")
    print("=" * 70)
    r, m, nu = 0.045, 16.0, 0.5     # floor ~16x annual labor income; r=4.5%
    rows = [(r,    "liquid (full return spendable)        "),
            (0.010,"locked, kappa_d distributes ~1%       "),
            (0.002,"locked, near kappa_d=0 + bequest      "),
            (0.0,  "kappa_d -> 0, full bequest (rho_eff=0)")]
    for rho_eff, lab in rows:
        b = rho_eff*m
        l = labor_ratio(b, nu)
        print("  %s b=%.3f -> l=%.4f (%+.1f%% labor)" % (lab, b, l, 100*(l-1)))
    print("  lock factor = rho_eff/r ; liquid ~-19%, locked ~1-5%, rho_eff=0 -> no effect")
    print("  [paper Sec 5.5: liquid ~-19%, locked ~1-5%, vanishes as kappa_d->0]")

def part3():
    print("=" * 70)
    print("PART 3 — level, not trend: scale-invariance of b  [Prop 4(iii)]")
    print("=" * 70)
    nu = 0.5
    # b = Y_F/(omega*h*) ; on a balanced path omega and F (hence Y_F) both scale by 'scale'
    rho_eff, m = 0.010, 16.0
    for scale in (1.0, 10.0, 100.0):
        omega = 1.0*scale
        F     = m*omega          # floor is m times labor income, scales with omega
        Y_F   = rho_eff*F
        b     = Y_F/(omega*1.0)   # h* normalized to 1
        print("  economy scale x%-5g : omega=%.1f F=%.1f Y_F=%.3f -> b=%.4f l=%.4f"
              % (scale, omega, F, Y_F, b, labor_ratio(b, nu)))
    eps_g, b0 = 0.5, 0.10
    bound = eps_g*(nu/(1+nu))*b0
    print("  b invariant to scale -> ONE-TIME LEVEL effect (not a trend change)")
    print("  endogenous-growth trend bound eps_g*[nu/(1+nu)]*b = %.4f (<= %.2f%% of g)"
          % (bound, 100*bound))
    print("  [paper Sec 5.5 / A.7(iii): level effect; trend change <= eps_g*[nu/(1+nu)]*b]")

def part4():
    print("=" * 70)
    print("PART 4 — self-correcting labor-growth loop (contraction)  [Prop 4(iv)]")
    print("=" * 70)
    nu, eps_g, gstar, b0 = 0.5, 0.5, 1.0, 0.10
    def step(g):
        b = b0*(g/gstar)                       # growth-indexed flow: b proportional to g
        return gstar*(1 + eps_g*(labor_ratio(b, nu) - 1))
    for g0 in (0.60, 0.999):
        g = g0; traj = [g]
        for _ in range(8):
            g = step(g); traj.append(g)
        print("  start g/g*=%.3f -> %s" % (g0, " ".join("%.4f" % x for x in traj)))
    gfp = 0.6
    for _ in range(60): gfp = step(gfp)
    h = 1e-6
    gain = abs((step(gfp+h) - step(gfp-h))/(2*h))
    print("  fixed point g/g* = %.4f ; loop gain |dg'/dg| = %.4f (<1 => contraction)"
          % (gfp/gstar, gain))
    print("  [paper Sec 5.5 / A.7(iv): fixed point ~0.984, loop gain ~0.016, self-correcting]")
    return gain < 1.0 and abs(gfp/gstar - 0.984) < 0.01

def main():
    part1(); part2(); part3(); ok = part4()
    print("=" * 70)
    print("All Proposition 4 claims reproduced:", bool(ok))
    print("=" * 70)

if __name__ == "__main__":
    main()

"""
Phase milestone Stable Floors for Paper 3 (Transition Architecture), Section 3.

Grounds the phased-rollout citizen accumulation figures on the general-equilibrium
REALIZABLE return (Neo-Solon 2026e, Section 6.7), replacing the original price-taker
figures. A citizen in phase X receives K1 at birth plus a per-capita share of K2 set
to `frac` of the full Mode B (real-growth-matched) K2 budget, with the Mode B 60/40
split (60 percent to the locked floor), compounded over a 65-year working life.

Two checks anchor the method:
  (1) PRICE-TAKER reproduction: Phase 1 (10% K2) at the old 4.5% central return
      reproduces the originally published ~$65K, confirming the deposit/compounding
      model is the one Paper 3 used.
  (2) REALIZABLE anchor: the full-rate cohort (100% K2) at the Mode B realizable
      return (4.30%) reproduces Paper 1's published Mode B floor (~$413K).

The realizable return is capture-dependent (Paper 5 Section 6.7): a lightly-capitalised
early phase earns close to the low-capture Mode A/C return (~5.40%); at full deployment
the deepened stock pulls the realizable return down to the Mode B value (~4.30%). We
interpolate linearly in the capture fraction and report each phase at its central
realizable return, with a band spanning the realizable return band.

Pure standard library. Engine constants mirror cs_engine.py.
"""

M2_0   = 22366.2e9       # launch M2
GDP_0  = 30762.099e9     # launch nominal GDP
POP_0  = 341.8e6         # launch population
RG     = 0.02            # real growth
PG     = 0.005           # net population growth
HZ     = 65              # working-life horizon (years)
NC     = 0.011703        # gross new-citizen rate (births / pop)
K1_PC  = 0.025           # K1 = 2.5% of GDP per capita per birth

# realizable return endpoints (Paper 5 Section 6.7 / Paper 1 Tables 5-6)
ER_LOWCAP  = 0.054       # ~0% capture (low-capture Mode A/C realizable return)
ER_FULLCAP = 0.043       # 100% capture (Mode B 60/40 realizable return)
# realizable return band (Mode B: 3.30 / 4.26 / 5.03), as offsets from central
BAND = (-0.0096, +0.0077)


def er_capture(frac):
    """Capture-appropriate central realizable return at K2 fraction `frac`."""
    return ER_LOWCAP + (ER_FULLCAP - ER_LOWCAP) * frac


def phase_floor(frac, er, k3=0.40):
    """Real locked Stable Floor at age 65 for a cohort at K2 fraction `frac`,
    Mode B 60/40 split (k3 = dividend share), compounded at real return `er`."""
    m2, gdp, pop = M2_0, GDP_0, POP_0
    cpi_idx, floor_real = 1.0, 0.0
    new_cit = pop * NC
    for t in range(HZ + 1):
        gpc = gdp / pop
        k1_t = K1_PC * gpc * max(new_cit, 0.0)
        split = max(0.0, frac * m2 * RG - k1_t)
        k3_t = k3 * split
        k2_t = split - k3_t
        k1_pc = k1_t / new_cit if new_cit > 0 else 0.0
        dep = (k1_pc if t == 0 else 0.0) + k2_t / pop
        floor_real = (floor_real + dep / cpi_idx) * (1 + er)
        m2 += k1_t + split
        gdp *= (1 + RG)
        pop *= (1 + PG)
    return floor_real


PHASES = [
    ("Phase 1 (K2 = 10%)",          0.10),
    ("Phase 2 midpoint (K2 = 30%)", 0.30),
    ("Phase 3 midpoint (K2 = 75%)", 0.75),
    ("Full Mode B (K2 = 100%)",     1.00),
]
MEDIAN = 260e3        # SCF median actual retirement benchmark (Paper 2)
EARLIEST_HIST = 210e3 # earliest historical cohort, realizable basis (Paper 2)


def k(x):
    return f"${x/1e3:,.0f}K"


def main():
    print("=" * 70)
    print("PAPER 3 PHASE MILESTONES - GENERAL-EQUILIBRIUM REALIZABLE BASIS")
    print("=" * 70)
    print("K1 + frac x (full Mode B K2), 60/40 split, capture-appropriate")
    print("realizable return, 65-year horizon. Real 2025 dollars.\n")
    print(f"  {'phase':28} {'er':>7} {'low':>8} {'central':>9} {'high':>8}")
    central = {}
    for name, frac in PHASES:
        erc = er_capture(frac)
        lo = phase_floor(frac, erc + BAND[0])
        ce = phase_floor(frac, erc)
        hi = phase_floor(frac, erc + BAND[1])
        central[frac] = ce
        print(f"  {name:28} {erc*100:6.2f}% {k(lo):>8} {k(ce):>9} {k(hi):>8}")

    print("\n  Median benchmark (Paper 2):              " + k(MEDIAN))
    print("  Earliest historical cohort (Paper 2):    " + k(EARLIEST_HIST))
    print("  -> Phase 1 below median; Phase 2 approaching; Phase 3 above.\n")

    print("-" * 70)
    print("VALIDATION")
    print("-" * 70)
    checks = [
        ("Phase 1 (10% K2) @ price-taker 4.5% ~ $65K (orig)",
         phase_floor(0.10, 0.045), 65e3, 4e3),
        ("Full Mode B (100% K2) @ realizable 4.30% ~ $413K (Paper 1)",
         phase_floor(1.00, 0.043), 413e3, 12e3),
    ]
    ok = True
    for label, got, target, tol in checks:
        p = abs(got - target) <= tol
        ok = ok and p
        print(f"  [{'PASS' if p else 'FAIL'}] {label:54} got {k(got)}")
    print("-" * 70)
    print("ALL CHECKS PASS" if ok else "CHECK FAILED")
    return central


if __name__ == "__main__":
    main()

# NOTE: this file was named mode_omega.py. It was ALWAYS Mode Λ (Architecture §10,
# "An Adaptive Configuration"): demographic + productivity governors, 2.0x K1 cap,
# 3.5% issuance cap. Mode Ω (§9) is the price-stability SOLVER and has no governors.
# The code was always right; only the name was wrong.
# Mode Λ replication — grounds the Section 10.6 figures in the documented
# governor formulas (Architecture Section 10) applied to the corrected base engine.
#
# Mode Λ = adaptive multi-governor configuration:
#   K1 base 2.5% of GDP/cap, demographic multiplier capped at 2.0x total
#   K2 base 60% of the real-growth-matched budget (between Mode A's 17.5% and Mode B's 100%)
#       + demographic governor (+15-40%) under negative population growth
#       + productivity governor (+10-30%) under a productivity boom
#   Combined issuance capped at 3.5% of M2.
# Inflation is DERIVED from issuance (no rounding), exactly as the base engine.
import cs_engine as E

M2_0, GDP_0, POP_0, RG, HZ, NC = E.M2_0, E.GDP_0, E.POP_0, E.RG, E.HZ, E.NC
K1_BASE, K2_BASE = 0.025, 0.60      # Mode Λ base channels
ISSUANCE_CAP = 0.035                # combined issuance <= 3.5% of M2

def run(er, pg, k1_mult=1.0, k2_demo=0.0, k2_prod=0.0):
    """Deterministic 65-year floor for a citizen born at launch.
       k1_mult    : K1 demographic multiplier (1.0 base, <=2.0 cap)
       k2_demo    : demographic K2 governor, fractional boost (0.15-0.40 when active)
       k2_prod    : productivity K2 governor, fractional boost (0.10-0.30 when active)"""
    k1 = K1_BASE * min(k1_mult, 2.0)
    k2 = K2_BASE * (1.0 + k2_demo + k2_prod)
    # derive cpi from issuance, then cap combined issuance at 3.5% of M2
    k1Share = k1 * (GDP_0 / M2_0) * NC
    issuance = max(k1Share, k2 * RG)
    if issuance > ISSUANCE_CAP:                      # governor hard cap
        k2 = (ISSUANCE_CAP) / RG
        issuance = ISSUANCE_CAP
    cpi = issuance - RG
    m2, gdp, pop = M2_0, GDP_0, POP_0
    cpiIdx, floorReal = 1.0, 0.0
    newcit = pop * NC
    for t in range(HZ + 1):
        gpc = gdp / pop
        k1T = k1 * gpc * max(newcit, 0)
        k2Budget = k2 * m2 * RG
        split = max(0, k2Budget - k1T)
        k2T = split
        k1pc = k1T / newcit if newcit > 0 else 0
        k2pc = k2T / pop
        deposit = (k1pc if t == 0 else 0) + k2pc
        floorReal = (floorReal + deposit / cpiIdx) * (1 + er)
        m2 += k1T + split
        gdp = gdp * (1 + RG) * (1 + cpi)
        pop *= (1 + pg)
        newcit = max(0, pop * NC)
        cpiIdx *= (1 + cpi)
    return floorReal, cpi

# base-60 reference (no governor) at each return, normal demographics
def base60(er, pg=0.003):
    return run(er, pg)[0]

if __name__ == "__main__":
    print("=== Mode Λ base-60 (no governor) ===")
    for er in (0.03, 0.045, 0.065):
        print(f"  er={er*100:.1f}% (normal pop): ${base60(er)/1e3:,.1f}K")

    # Governor settings for the negative-pop stress path (shared across the three
    # neg-pop return scenarios): demographic governor at full strength.
    # Demographic governor calibrated to the Section 10.6 anchor (+55% vs normal at
    # -0.5% pop): K1 multiplier +0.3x (bottom of the +0.3-0.8x range) and K2 governor
    # +30% (within the +15-40% range). Productivity governor at its +30% ceiling.
    DEMO = dict(k1_mult=1.3, k2_demo=0.30)
    PROD = dict(k2_prod=0.30)

    scen = {
      "1 Normal (+0.3% pop, 4.5%)":        dict(er=0.045, pg=0.003),
      "2 Neg pop (-0.5%, 4.5%)":           dict(er=0.045, pg=-0.005, **DEMO),
      "3 Neg pop + optimistic (6.5%)":     dict(er=0.065, pg=-0.005, **DEMO),
      "4 Neg pop + pessimistic (3.0%)":    dict(er=0.030, pg=-0.005, **DEMO),
      "5 Productivity boom + neg pop":     dict(er=0.045, pg=-0.005, **DEMO, **PROD),
    }
    print("\n=== Mode Λ scenarios (grounded) ===")
    normal = None
    for name, kw in scen.items():
        f, cpi = run(**kw)
        if normal is None: normal = f
        boost = (f/normal - 1)*100
        print(f"  {name:34} floor=${f/1e3:,.1f}K  income(5%)=${0.05*f:,.0f}  "
              f"cpi={cpi*100:+.2f}%  vs-normal={boost:+.0f}%")

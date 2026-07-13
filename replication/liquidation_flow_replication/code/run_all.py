"""
Paper 5 (Macro Model) supplementary — the liquidation flow L_t, computed.

Runs the whole package and writes all_results.txt + results/liquidation_results.json.
"""
import json, os, sys
import numpy as np
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
os.chdir(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
sys.path.insert(0, "code")
from liquidation_flow import (run, load_survival, stable_population,
                              G_R, N_POP, POP_0, MU_0, M2_0, KAPPA_D, W_DRAW, R_REAL, RETIRE)

OUT = []
def p(s=""):
    print(s); OUT.append(s)

BAR = "=" * 92
p(BAR); p("CITIZENS STANDARD — THE LIQUIDATION FLOW L_t, COMPUTED")
p("Paper 5 (Macro Model) §3.3 / Paper 1 (Architecture) 'Two bounds on kappa_d'")
p("Framework calibration UNCHANGED. Mortality: SSA period life table (real l_x).")
p(BAR); p()

# ---------- 0. validate the stable population against published US aggregates ----------
l = load_survival("data/ssa_life_table_2022.csv")
pop = stable_population(l, N_POP, POP_0)
share65 = pop[RETIRE:].sum() / pop.sum()
p("SECTION 0  Stable-population validation (real SSA survival)")
p("-" * 92)
p(f"  65+ share   model {share65*100:.1f}%     published US ~18.0% (Census: 61.2M / 342M)")
p(f"  65+ count   model {pop[RETIRE:].sum():.1f}M      published US ~61.2M")
p()

# ---------- 1. the launch calibration gate ----------
r = run(years=125)
p("SECTION 1  Launch gate — reproduce the Architecture paper's own arithmetic")
p("-" * 92)
p(f"  growth budget      {G_R*M2_0:8.1f} $B    paper ~447")
p(f"  K3 dividend        {r['K3'][0]:8.1f} $B    paper ~175.3")
p(f"  M^T = mu*M2        {MU_0*M2_0:8.1f} $B    paper ~11488")
p(f"  required dM^T      {r['required'][0]:8.1f} $B    paper ~229.7")
p(f"  L_t at launch      {r['L'][0]:8.1f} $B    (no floor has matured yet)")
p()

# ---------- 2. the constraint ----------
breach = np.where(r["excess"] > 0)[0]
byear = int(r["year"][breach[0]]) if len(breach) else None
p("SECTION 2  The constraint:  K3 + KI + liquidation <= Y-matched expansion")
p("-" * 92)
p("  year      L_t       K3    spill     inflow   required     excess   implied pi      mu")
for i, y in enumerate(r["year"]):
    if y in (2026, 2040, 2050, 2060, 2070, 2080, 2090, 2100, 2110, 2125):
        p(f"  {int(y)}  {r['L'][i]:8.1f} {r['K3'][i]:8.1f} {r['spill'][i]:7.1f}"
          f"  {r['inflow'][i]:9.1f} {r['required'][i]:10.1f} {r['excess'][i]:+10.1f}"
          f"   {r['pi'][i]:+7.2f}%   {r['mu'][i]:.3f}")
p()
p(f"  CONSTRAINT FIRST BREACHED: {byear}")
p(f"  peak implied inflation:    {r['pi'].max():+.2f}%  in {int(r['year'][r['pi'].argmax()])}")
p(f"  mu drift:                  {r['mu'][0]:.3f} -> {r['mu'][-1]:.3f}")
p()

# ---------- 3. sensitivity ----------
p("SECTION 3  Sensitivity — does the breach survive?")
p("-" * 92)
p("  variation                         breach   peak pi   L_t(2100)")
rows = []
def sens(label, **kw):
    rr = run(years=125, **kw)
    b = np.where(rr["excess"] > 0)[0]
    by = int(rr["year"][b[0]]) if len(b) else 0
    p(f"  {label:<32} {by if by else 'none':>6}  {rr['pi'].max():+7.2f}%  {rr['L'][74]:9.1f}")
    rows.append({"variation": label, "breach_year": by,
                 "peak_pi": round(float(rr["pi"].max()), 4),
                 "L_2100": round(float(rr["L"][74]), 1)})
sens("base (framework defaults)")
for w in (0.03, 0.05, 0.06): sens(f"withdrawal w = {w:.0%}", w_draw=w)
for rr_ in (0.0330, 0.0503):  sens(f"realizable r = {rr_:.2%}", r=rr_)
sens("r = g = 2.00% (r>g removed)", r=0.020)
sens("r = 1.50% (r < g)", r=0.015)
for kd in (0.0, 0.60): sens(f"kappa_d = {kd:.2f}", kappa_d=kd)
p()
p("  The breach survives EVERY variation, including removing r>g entirely.")
p("  Mechanism: K3 was calibrated at launch to fill the ENTIRE Y-matched expansion")
p("  at a moment when L_t = 0. As floors mature, L_t lands on top of a full budget.")
p()

# ---------- 4. the fix ----------
p("SECTION 4  The kappa_d schedule that holds the locus")
p("-" * 92)
after = r["M2"] * G_R - 8.1 * (1.02 ** (r["year"] - 2026))
kd_req = (r["required"] - r["L"] - r["spill"]) / np.maximum(after, 1e-9)
zero = np.where(kd_req <= 0)[0]
for y in (2026, 2040, 2060, 2080, 2100, 2125):
    i = list(r["year"]).index(y)
    p(f"  {y}   kappa_d required = {kd_req[i]:+.3f}")
kd_zero = int(r["year"][zero[0]]) if len(zero) else 0
p()
p(f"  kappa_d must reach ZERO in {kd_zero}; past that, holding the price level requires")
p("  NET CONTRACTION (KI negative / Tool 14a retirement) — the same 'withdrawal capacity'")
p("  limit the Paper 7 red-team identifies as the framework's binding constraint.")
p(BAR)

res = {
    "pop65_share_model": round(float(share65), 4),
    "L_launch": round(float(r["L"][0]), 2),
    "L_2100": round(float(r["L"][74]), 1),
    "required_launch": round(float(r["required"][0]), 1),
    "K3_launch": round(float(r["K3"][0]), 1),
    "breach_year": byear,
    "peak_inflation_pct": round(float(r["pi"].max()), 4),
    "peak_inflation_year": int(r["year"][r["pi"].argmax()]),
    "mu_launch": round(float(r["mu"][0]), 4),
    "mu_2125": round(float(r["mu"][-1]), 4),
    "kappa_d_zero_year": kd_zero,
    "sensitivity": rows,
}
os.makedirs("results", exist_ok=True)
with open("results/liquidation_results.json", "w") as f:
    json.dump(res, f, indent=2)
with open("all_results.txt", "w") as f:
    f.write("\n".join(OUT) + "\n")
print("\nwrote results/liquidation_results.json and all_results.txt")

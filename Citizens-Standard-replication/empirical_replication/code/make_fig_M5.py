"""Figure M5 — Forward transition cohorts (Part II projection)."""
import numpy as np, matplotlib
matplotlib.use("Agg"); import matplotlib.pyplot as plt
from transition_cohorts_v3 import run_transition_tables, TRANSITION_COHORTS
from deterministic_engine_v3 import build_dataset

data = build_dataset(end_year=2125)
res = run_transition_tables(data)

cohorts = [c[0] for c in TRANSITION_COHORTS]
births = [c[1] for c in TRANSITION_COHORTS]
pess = [res[c]["pessimistic"] for c in cohorts]
cent = [res[c]["central"] for c in cohorts]
opt  = [res[c]["optimistic"] for c in cohorts]
cost = [(res[c]["central_no_compression"]-res[c]["central"])/res[c]["central_no_compression"]*100 for c in cohorts]

fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(14, 6))
fig.suptitle("Figure M5. Forward transition cohorts (Part II) — a forward projection, not a historical reconstruction\n"
             "Full-rate K2; 0.5pp return compression during the 2026-2071 paydown window",
             fontsize=12, fontweight="bold")

x = np.arange(len(cohorts))
w = 0.25
ax1.bar(x-w, pess, w, label="Pessimistic (3.0% real)", color="#c0504d")
ax1.bar(x,   cent, w, label="Central (4.5% real)", color="#4f81bd")
ax1.bar(x+w, opt,  w, label="Optimistic (6.5% real)", color="#9bbb59")
ax1.set_xticks(x); ax1.set_xticklabels([f"{c}\n(born {b})" for c,b in zip(cohorts,births)])
ax1.set_ylabel("Projected Stable Floor at age 65 (2025 real $)")
ax1.set_title("Projected Stable Floor by return scenario")
ax1.legend(); ax1.yaxis.set_major_formatter(plt.FuncFormatter(lambda v,_: f"${v/1e6:.1f}M"))
ax1.grid(axis="y", alpha=0.3)

ax2.bar(x, cost, 0.5, color="#8064a2")
ax2.set_xticks(x); ax2.set_xticklabels([f"{c}\n(born {b})" for c,b in zip(cohorts,births)])
ax2.set_ylabel("Transition cost (% reduction, central scenario)")
ax2.set_title("Cost of the transition to citizens\n(return compression during paydown window)")
for i,v in enumerate(cost): ax2.text(i, v+0.2, f"-{v:.1f}%", ha="center", fontsize=10)
ax2.grid(axis="y", alpha=0.3)

plt.tight_layout(rect=[0,0,1,0.94])
plt.savefig("/home/claude/repl/replication/figures_v3/figure_M5_transition_cohorts_v3.png", dpi=120)
print("wrote figure_M5_transition_cohorts_v3.png")

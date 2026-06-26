"""Generate figures for the Paper 3 appendix replication package."""
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from appendix_A2_debt_trajectory import run_trajectory

import os
FIG_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "figures")
os.makedirs(FIG_DIR, exist_ok=True)

# Figure 1: debt trajectory vs CBO baseline
rows, floor_year = run_trajectory()
years = [r["year"] for r in rows if r["year"] <= 50]
dgdp = [r["d_gdp"]*100 for r in rows if r["year"] <= 50]

fig, ax = plt.subplots(figsize=(11, 6))
ax.plot(years, dgdp, lw=2.5, color="#4f81bd", label="Citizens Standard (Mode T + KT)")
# CBO baseline rising to 156% by ~2055 (Year 30 from a 2026 enactment ≈ 2056)
cbo_years = [0, 10, 20, 30]
cbo_vals = [102, 118, 135, 156]
ax.plot(cbo_years, cbo_vals, lw=2.5, color="#c0504d", ls="--", label="CBO current-law baseline")
ax.axhline(15, color="#7f7f7f", lw=1.0, ls=":", label="Operational floor (~15% of GDP)")
ax.annotate("Stabilizes at ~15% of GDP\n(operational floor)",
            xy=(42, 15), xytext=(25, 40),
            arrowprops=dict(arrowstyle="->", color="#333"), fontsize=10)
ax.set_xlabel("Years from enactment")
ax.set_ylabel("Debt held by the public (% of GDP)")
ax.set_title("Public debt-to-GDP under Mode T versus the CBO current-law baseline\n"
             "Legacy Debt Trust + KT channel (1.5% of M2), primary surplus phasing to 1.5% of GDP",
             fontsize=11, fontweight="bold")
ax.legend(loc='upper left'); ax.grid(alpha=0.3); ax.set_ylim(0, 165)
plt.tight_layout()
plt.savefig(f"{FIG_DIR}/figure_A2_debt_trajectory.png", dpi=120)
print("wrote figure_A2_debt_trajectory.png")

# Figure 2: KT issuance and remaining debt over time
fig, ax1 = plt.subplots(figsize=(11, 6))
yrs = [r["year"] for r in rows if r["year"] <= 50]
debt = [r["debt"]/1e12 for r in rows if r["year"] <= 50]
kt = [r["kt"]/1e9 for r in rows if r["year"] <= 50]
ax1.bar(yrs, kt, color="#9bbb59", alpha=0.7, label="KT issuance ($B, left)")
ax1.set_xlabel("Years from enactment"); ax1.set_ylabel("KT issuance ($B/yr)")
ax2 = ax1.twinx()
ax2.plot(yrs, debt, lw=2.5, color="#4f81bd", label="Public debt ($T, right)")
ax2.set_ylabel("Public debt stock ($T)")
ax1.set_title("KT issuance and the declining public debt stock\n"
              "KT retires the public debt to the ~15% operational floor, then self-extinguishes",
              fontsize=11, fontweight="bold")
ax1.legend(loc="upper right"); ax2.legend(loc="center right")
ax1.grid(alpha=0.3)
plt.tight_layout()
plt.savefig(f"{FIG_DIR}/figure_A2b_kt_and_debt.png", dpi=120)
print("wrote figure_A2b_kt_and_debt.png")

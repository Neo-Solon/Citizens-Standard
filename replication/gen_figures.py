"""Generate all figures for v7 PDF."""
import csv, json
import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches

# ── Reload data for Figure 1 (trajectory) ─────────────────────────────────
PATH = "citizens_standard_historical_data_1960_2025.csv"
DATA = {}
with open(PATH) as f:
    for row in csv.DictReader(f):
        y = int(row["year"])
        DATA[y] = {
            "M2":   float(row["m2_billions_usd"]) * 1e9,
            "GDP":  float(row["gdp_nominal_billions_usd"]) * 1e9,
            "pop":  float(row["population_millions"]) * 1e6,
            "CPI":  float(row["cpi_u_index_1982_84_eq_100"]),
            "eqR":  float(row["sp500_real_total_return_pct"]) / 100.0,
            "rgdp": float(row["real_gdp_growth_pct"]) / 100.0,
        }
for y in range(2026, 2056):
    p = DATA[y-1]
    DATA[y] = {"M2":p["M2"]*1.045,"GDP":p["GDP"]*1.040,"pop":p["pop"]*1.004,
               "CPI":p["CPI"]*1.025,"eqR":None,"rgdp":0.018}

CPI_2025 = DATA[2025]["CPI"]
def to_2025(n,y): return n*(CPI_2025/DATA[y]["CPI"])

DEPR_NOM = [-8.30,-25.12,-43.84,-8.64,49.98,-1.19,46.74,31.94,-35.34,29.28,
            -1.10,-10.67,-12.77,19.17,25.06,19.03,35.82]
DEPR_CPI = [-0.2,-6.4,-9.3,-10.3,0.8,1.5,3.0,1.4,2.9,-2.8,0.0,0.7,5.0,10.9,6.1,1.7,2.3]
STAG_NOM = [-9.97,23.80,10.81,-8.24,3.56,14.22,18.76,-14.31,-25.90,37.00,23.83,
            -6.98,6.51,18.52,31.74,-4.70,20.42]
STAG_CPI = [2.86,3.09,4.19,5.46,5.72,4.38,3.21,6.16,11.03,9.14,5.76,6.50,7.62,
            11.22,13.58,10.35,6.16]

def trajectory(birth, retire, post_eq=0.045, stress=None):
    s_start, s_len = 25, 17
    bal = 0.0
    ages, bals = [], []
    for y in range(birth, retire+1):
        age = y-birth
        d = DATA[y]
        gpc = d["GDP"]/d["pop"]
        k1 = gpc*0.025 if y==birth else 0.0
        prev_m2 = DATA[y-1]["M2"] if y>birth else d["M2"]
        rgdp = max(0.0, d["rgdp"])
        k2 = (rgdp*prev_m2*0.5)/d["pop"]
        k1r = to_2025(k1,y); k2r = to_2025(k2,y)
        if stress and s_start <= age < s_start+s_len:
            i = age-s_start
            eq = (1+stress["nom"][i]/100)/(1+stress["cpi"][i]/100)-1
        elif y <= 2025:
            eq = d["eqR"]
        else:
            eq = post_eq
        bal = (bal+k1r+k2r)*(1+eq)
        ages.append(age); bals.append(bal/1000)
    return ages, bals

# ── Figure 1: Trajectories ────────────────────────────────────────────────
cohorts = [("A",1960,2025,260),("B",1970,2035,240),("C",1980,2045,220),("D",1990,2055,210)]
fig, axes = plt.subplots(2, 2, figsize=(11, 8))
fig.suptitle("Figure 1. Stable Floor accumulation trajectories by cohort over 65 working-life years\n"
             "Central path vs. stress scenarios; median actual benchmark for context",
             fontsize=10)
for (name, b, r, med), ax in zip(cohorts, axes.flat):
    a_c, v_c = trajectory(b, r, 0.045)
    a_d, v_d = trajectory(b, r, 0.045, stress={"nom":DEPR_NOM,"cpi":DEPR_CPI})
    a_s, v_s = trajectory(b, r, 0.045, stress={"nom":STAG_NOM,"cpi":STAG_CPI})
    ax.plot(a_c, v_c, "-", color="#1f6feb", lw=2, label="Central (historical / 4.5% real projected)")
    ax.plot(a_d, v_d, "--", color="#fb8500", lw=1.5, label="Depression stress (1929-45 at ages 25-41)")
    ax.plot(a_s, v_s, ":", color="#7c3aed", lw=1.5, label="Stagflation stress (1966-82 at ages 25-41)")
    ax.axhline(med, ls="-.", color="#d6336c", lw=1, label=f"Median actual + DB benchmark (${med}K)")
    ax.axvspan(25, 42, color="gray", alpha=0.1)
    ax.annotate(f"${v_c[-1]:.0f}K", (a_c[-1], v_c[-1]), fontsize=8, color="#1f6feb",
                xytext=(2,2), textcoords="offset points")
    ax.annotate(f"${v_d[-1]:.0f}K", (a_d[-1], v_d[-1]), fontsize=8, color="#fb8500",
                xytext=(2,-10), textcoords="offset points")
    ax.annotate(f"${v_s[-1]:.0f}K", (a_s[-1], v_s[-1]), fontsize=8, color="#7c3aed",
                xytext=(2,-20), textcoords="offset points")
    ax.set_title(f"Cohort {name} (born {b}, retire {r})", fontsize=10)
    ax.set_xlabel("Age (years)", fontsize=8)
    ax.set_ylabel("Stable Floor (2025$ thousands)", fontsize=8)
    ax.tick_params(labelsize=7)
    ax.legend(loc="upper left", fontsize=6.5, framealpha=0.85)
    ax.grid(True, alpha=0.25, linestyle=":")
plt.tight_layout(rect=[0, 0, 1, 0.96])
plt.savefig("/home/claude/p2/fig1_trajectories.png", dpi=150, bbox_inches="tight")
plt.close()
print("Figure 1 saved.")

# ── Load MC results ───────────────────────────────────────────────────────
with open("/home/claude/p2/mc_results.json") as f:
    MC = json.load(f)

def load_dist(cohort, universe, method):
    return np.load(f"/home/claude/p2/mc_{cohort}_{universe}_{method}.npy")

# Deterministic central scenario values (from simulator)
DETERMINISTIC = {"A":680319, "B":704320, "C":692430, "D":459265}
MEDIAN = {"A":260000,"B":240000,"C":220000,"D":210000}

# ── Figure M1: Distribution histograms 1929-2025 universe ─────────────────
fig, axes = plt.subplots(2, 2, figsize=(11, 8))
fig.suptitle("Figure M1. Monte Carlo distribution of Mode B Stable Floor at retirement\n"
             "10,000 paths per cohort, full joint resampling from 1929-2025 historical universe",
             fontsize=10)
cohort_meta = [("A",1960,2025),("B",1970,2035),("C",1980,2045),("D",1990,2055)]
for (cname, b, r), ax in zip(cohort_meta, axes.flat):
    iid_bals = load_dist(cname, "1929-2025", "iid") / 1000
    blk_bals = load_dist(cname, "1929-2025", "block") / 1000
    # Cap at 99th percentile for plotting
    cap = np.percentile(np.concatenate([iid_bals, blk_bals]), 99)
    iid_plot = iid_bals[iid_bals <= cap]
    blk_plot = blk_bals[blk_bals <= cap]
    bins = np.linspace(0, cap, 60)
    ax.hist(iid_plot, bins=bins, density=True, alpha=0.55, color="#1f77b4",
            label="IID bootstrap", edgecolor="#1f77b4", lw=0.3)
    ax.hist(blk_plot, bins=bins, density=True, alpha=0.55, color="#bf8e3c",
            label="Block bootstrap (5-yr)", edgecolor="#bf8e3c", lw=0.3)
    ax.axvline(MEDIAN[cname]/1000, color="#d6336c", ls="--", lw=1.5,
               label=f"Median actual + DB (${MEDIAN[cname]//1000}K)")
    ax.axvline(DETERMINISTIC[cname]/1000, color="#2ca02c", ls=":", lw=1.5,
               label=f"Deterministic central (${DETERMINISTIC[cname]//1000}K)")
    blk_p50 = MC[f"{cname}_1929-2025_block"]["P50"]/1000
    ax.axvline(blk_p50, color="#ff7f0e", ls="-", lw=1,
               label=f"Block P50 (${blk_p50:.0f}K)")
    ax.set_title(f"Cohort {cname} (born {b}, retire {r})", fontsize=10)
    ax.set_xlabel("Stable Floor at age 65 (2025$ thousands)", fontsize=8)
    ax.set_ylabel("Density", fontsize=8)
    ax.tick_params(labelsize=7)
    ax.legend(loc="upper right", fontsize=6.5, framealpha=0.85)
    ax.grid(True, alpha=0.25, linestyle=":")
plt.tight_layout(rect=[0,0,1,0.96])
plt.savefig("/home/claude/p2/figM1_hist.png", dpi=150, bbox_inches="tight")
plt.close()
print("Figure M1 saved.")

# ── Figure M2: Percentile bands box plot ──────────────────────────────────
fig, ax = plt.subplots(figsize=(10, 6))
fig.suptitle("Figure M2. Monte Carlo percentile bands by cohort vs. deterministic central figures\n"
             "Block bootstrap (5-yr blocks), 1929-2025 universe, 10,000 paths", fontsize=10)
cs = list("ABCD")
positions = list(range(len(cs)))
for i, cname in enumerate(cs):
    bals = load_dist(cname, "1929-2025", "block") / 1000
    p5 = np.percentile(bals, 5)
    p25 = np.percentile(bals, 25)
    p50 = np.percentile(bals, 50)
    p75 = np.percentile(bals, 75)
    p95 = np.percentile(bals, 95)
    # IQR box
    ax.bar(i, p75-p25, bottom=p25, width=0.55, color="#fdbb84",
           edgecolor="#d04a02", lw=0.8, alpha=0.85,
           label="IQR (P25-P75)" if i==0 else "")
    # Whiskers
    ax.plot([i, i], [p5, p25], color="#444", lw=1)
    ax.plot([i, i], [p75, p95], color="#444", lw=1)
    ax.plot([i-0.15, i+0.15], [p5, p5], color="#444", lw=1)
    ax.plot([i-0.15, i+0.15], [p95, p95], color="#444", lw=1)
    # P50 black circle
    ax.scatter([i], [p50], s=80, color="black", zorder=5,
               label="MC P50 (block bootstrap)" if i==0 else "")
    # Deterministic green diamond
    ax.scatter([i], [DETERMINISTIC[cname]/1000], marker="D", s=100, color="#2ca02c",
               zorder=5, label="Deterministic central" if i==0 else "")
    # Median actual red square
    ax.scatter([i], [MEDIAN[cname]/1000], marker="s", s=80, color="#d6336c",
               zorder=5, label="Median actual + DB pension" if i==0 else "")
ax.set_xticks(positions)
ax.set_xticklabels([f"Cohort {c}\n(born {1960+10*i})" for i, c in enumerate(cs)], fontsize=9)
ax.set_ylabel("Stable Floor at age 65 (2025$ thousands)", fontsize=9)
ax.tick_params(axis="y", labelsize=8)
ax.legend(loc="upper left", fontsize=8, framealpha=0.9)
ax.grid(True, alpha=0.25, linestyle=":", axis="y")
plt.tight_layout(rect=[0,0,1,0.94])
plt.savefig("/home/claude/p2/figM2_percentiles.png", dpi=150, bbox_inches="tight")
plt.close()
print("Figure M2 saved.")

# ── Figure M3: P(<median) bar chart ───────────────────────────────────────
fig, ax = plt.subplots(figsize=(10, 6))
fig.suptitle("Figure M3. Probability Mode B falls below median actual retirement outcome\n"
             "Across cohorts and bootstrap configurations", fontsize=10)
configs = [("1929-2025","iid"),("1929-2025","block"),("1960-2025","iid"),("1960-2025","block")]
config_labels = ["1929-2025, IID","1929-2025, Block","1960-2025, IID","1960-2025, Block"]
colors = ["#1f77b4","#bf8e3c","#2ca02c","#fdb462"]
hatches = ["//","","\\\\",""]
x = np.arange(4)
width = 0.18
for i, ((u, m), lbl, col, hatch) in enumerate(zip(configs, config_labels, colors, hatches)):
    vals = [MC[f"{c}_{u}_{m}"]["p_below_median"]*100 for c in cs]
    bars = ax.bar(x + (i-1.5)*width, vals, width, label=lbl, color=col, hatch=hatch,
                  edgecolor="black", linewidth=0.6, alpha=0.9)
    for bar, v in zip(bars, vals):
        ax.annotate(f"{v:.1f}%", (bar.get_x()+bar.get_width()/2, v),
                    ha="center", va="bottom", fontsize=7)
ax.set_xticks(x)
ax.set_xticklabels([f"Cohort {c}" for c in cs], fontsize=9)
ax.set_ylabel("P(Mode B Stable Floor < median actual retirement wealth)", fontsize=8)
ax.tick_params(axis="y", labelsize=8)
ax.legend(loc="upper right", fontsize=8, framealpha=0.9)
ax.grid(True, alpha=0.25, linestyle=":", axis="y")
ax.set_ylim(0, max([MC[f"A_{u}_{m}"]["p_below_median"]*100 for u,m in configs])*1.15)
plt.tight_layout(rect=[0,0,1,0.94])
plt.savefig("/home/claude/p2/figM3_pbelow.png", dpi=150, bbox_inches="tight")
plt.close()
print("Figure M3 saved.")

# ── Figure M4: P50 + P5 dual panel ────────────────────────────────────────
fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(12, 5))
fig.suptitle("Figure M4. Sensitivity of Mode B Stable Floor to bootstrap configuration\n"
             "P50 (central tendency, left) and P5 (adverse tail, right) across 4 configurations",
             fontsize=10)
for i, ((u, m), lbl, col, hatch) in enumerate(zip(configs, config_labels, colors, hatches)):
    p50_vals = [MC[f"{c}_{u}_{m}"]["P50"]/1000 for c in cs]
    p5_vals = [MC[f"{c}_{u}_{m}"]["P5"]/1000 for c in cs]
    ax1.bar(x + (i-1.5)*width, p50_vals, width, label=lbl, color=col, hatch=hatch,
            edgecolor="black", linewidth=0.6, alpha=0.9)
    ax2.bar(x + (i-1.5)*width, p5_vals, width, label=lbl, color=col, hatch=hatch,
            edgecolor="black", linewidth=0.6, alpha=0.9)
# Deterministic green diamonds on left
for i, c in enumerate(cs):
    ax1.scatter([i], [DETERMINISTIC[c]/1000], marker="D", s=100, color="#2ca02c",
                zorder=5, edgecolor="black", linewidth=0.5,
                label="Deterministic central" if i==0 else "")
# Median actual red dashed on right
for i, c in enumerate(cs):
    ax2.hlines(MEDIAN[c]/1000, i-0.35, i+0.35, color="#d6336c", linestyle="--", lw=2,
               label="Median actual + DB" if i==0 else "")
ax1.set_xticks(x); ax1.set_xticklabels([f"Cohort {c}" for c in cs], fontsize=9)
ax2.set_xticks(x); ax2.set_xticklabels([f"Cohort {c}" for c in cs], fontsize=9)
ax1.set_ylabel("P50 Stable Floor at age 65 (2025$ thousands)", fontsize=8)
ax2.set_ylabel("P5 (5th percentile) Stable Floor at age 65 (2025$ thousands)", fontsize=8)
ax1.set_title("Median (P50) outcome by configuration", fontsize=9)
ax2.set_title("Adverse-tail (P5) outcome by configuration", fontsize=9)
ax1.tick_params(labelsize=7); ax2.tick_params(labelsize=7)
ax1.legend(loc="upper left", fontsize=7, framealpha=0.9)
ax2.legend(loc="upper left", fontsize=7, framealpha=0.9)
ax1.grid(True, alpha=0.25, linestyle=":", axis="y")
ax2.grid(True, alpha=0.25, linestyle=":", axis="y")
plt.tight_layout(rect=[0,0,1,0.94])
plt.savefig("/home/claude/p2/figM4_sensitivity.png", dpi=150, bbox_inches="tight")
plt.close()
print("Figure M4 saved.")

print("\nAll figures generated.")

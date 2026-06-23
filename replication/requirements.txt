"""Two-panel figure: (A) the two Mt constructions track; (B) high-regime inflation-info, M2 vs both constructions."""
import matplotlib; matplotlib.use("Agg")
import matplotlib.pyplot as plt
import pandas as pd, numpy as np

INK="#10161C"; AMBER="#E6A93E"; TEAL="#3FAE92"; DIM="#9AA3AE"; RED="#C0563B"

m  = pd.read_csv("data/macro_1959_2026.csv", parse_dates=["date"]).set_index("date")
m1 = pd.read_csv("data/m1sl_1959_2019.csv", parse_dates=["date"]).set_index("date")
dv = pd.read_csv("data/divisia_dm1.csv", parse_dates=["date"]).set_index("date")
g_m1 = 100*np.log(m1["M1SL"]).diff(12)
g_dv = 100*np.log(dv["DM1"]).diff(12)

fig, (axA, axB) = plt.subplots(1, 2, figsize=(11, 4.3), gridspec_kw={"width_ratios":[1.6,1]})

# Panel A: the two constructions, 12m growth
axA.plot(g_dv.index, g_dv, color=AMBER, lw=1.4, label="Divisia M1 (user-cost)")
axA.plot(g_m1.index, g_m1, color=TEAL, lw=1.2, ls="--", label="M1 (composition)")
axA.axvspan(pd.Timestamp("2019-12-01"), g_dv.index.max(), color="#1b2530", alpha=0.5)
axA.text(pd.Timestamp("2021-02-01"), axA.get_ylim()[1]*0.86, "clean M1\nends 2019", fontsize=7.5, color=DIM, ha="center")
axA.axhline(0, color=DIM, lw=0.5)
axA.set_title("Two independent constructions of M\u1d40 (12-month growth)", fontsize=10.5, color=INK)
axA.set_ylabel("% per year"); axA.legend(fontsize=8.5, frameon=False, loc="upper left")
axA.text(0.98,0.04,"corr = 0.82 (growth), 0.99 (levels), 1968\u20132019",transform=axA.transAxes,
         ha="right",fontsize=8,color=DIM,style="italic")
axA.spines[["top","right"]].set_visible(False)

# Panel B: high-regime R2 (pre-2020, apples-to-apples) — both constructions vs M2
labels=["M2\n(simple sum)","M1\n(composition)","Divisia M1\n(user-cost)"]
vals=[0.043, 0.189, 0.209]; cols=[DIM, TEAL, AMBER]
bars=axB.bar(labels, vals, color=cols, edgecolor=INK, lw=0.6)
for b,v in zip(bars,vals):
    axB.text(b.get_x()+b.get_width()/2, v+0.006, f"{v:.2f}", ha="center", fontsize=9.5, color=INK)
axB.set_title("High-regime inflation information (R\u00b2)", fontsize=10.5, color=INK)
axB.set_ylabel("R\u00b2, next-12m CPI"); axB.set_ylim(0,0.26)
axB.text(0.5,0.93,"both constructions \u2248 5\u00d7 M2;\nand they agree with each other",transform=axB.transAxes,
         ha="center",fontsize=8,color=DIM,style="italic")
axB.spines[["top","right"]].set_visible(False)

plt.tight_layout()
fig.savefig("results/fig_divisia_convergence.png", dpi=140)
print("wrote results/fig_divisia_convergence.png")

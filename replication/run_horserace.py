"""Composition-tier figure: (A) the directly-built composition aggregate vs Divisia track
(MEASURED convergence, not inferred); (B) high-regime inflation-info R2 for all four series."""
import matplotlib; matplotlib.use("Agg")
import matplotlib.pyplot as plt
import pandas as pd, numpy as np, json, os, sys
sys.path.insert(0, os.path.join(os.path.dirname(__file__)))
from build_mt import composition_granular

INK="#10161C"; AMBER="#E6A93E"; TEAL="#3FAE92"; DIM="#9AA3AE"; SLATE="#5B6B7B"

def _read_fred(fn, col):
    s = pd.read_csv(f"data/{fn}", parse_dates=["observation_date"]).set_index("observation_date")[col]
    s.index.name="date"; return s.sort_index()

# Build the composition aggregate directly from FRED components, truncated to OCDSL's true end.
comp_components = {k: _read_fred(f"{k}.csv", k) for k in ["CURRSL","DEMDEPSL","OCDSL"]}
comp = composition_granular(comp_components)
comp = comp.loc[: comp_components["OCDSL"].dropna().index.max()]   # ends 2020-04
dv   = pd.read_csv("data/divisia_dm1.csv", parse_dates=["date"]).set_index("date")["DM1"]

g_comp = 100*np.log(comp).diff(12)
g_dv   = 100*np.log(dv).diff(12)

# measured correlation on the identical overlap (read back from results for consistency)
res = json.load(open("results/composition_results.json"))
corr_g = res["measured_convergence"]["corr_g_composition_g_divisia"]
corr_l = res["measured_convergence"]["corr_level_COMP_DM1"]

fig, (axA, axB) = plt.subplots(1, 2, figsize=(11, 4.3), gridspec_kw={"width_ratios":[1.6,1]})

# Panel A — the two constructions, 12m growth (composition is the MEASURED line, not inferred from M1)
axA.plot(g_dv.index, g_dv, color=AMBER, lw=1.4, label="Divisia M1 (user-cost)")
axA.plot(g_comp.index, g_comp, color=TEAL, lw=1.2, ls="--", label="Composition (currency+demand+OCD)")
axA.axvspan(pd.Timestamp("2020-04-01"), g_dv.index.max(), color="#1b2530", alpha=0.5)
axA.text(pd.Timestamp("2023-04-01"), axA.get_ylim()[1]*0.86, "composition ends\nApr 2020 (OCDSL)", fontsize=7.5, color=DIM, ha="center")
axA.axhline(0, color=DIM, lw=0.5)
axA.set_title("Two independent constructions of M\u1d40 (12-month growth)", fontsize=10.5, color=INK)
axA.set_ylabel("% per year"); axA.legend(fontsize=8.5, frameon=False, loc="upper left")
axA.text(0.98,0.04,f"measured corr = {corr_g:.2f} (growth), {corr_l:.2f} (levels), 1968\u20132020",
         transform=axA.transAxes, ha="right", fontsize=8, color=DIM, style="italic")
axA.spines[["top","right"]].set_visible(False)

# Panel B — high-regime R2 (pre-2021, identical sample): M2 vs the two transactional constructions + M1
def hi_r2(key): return [r for r in res[key] if r.get("regime")=="high"][0]["R2"]
labels=["M2\n(simple sum)","Composition\n(curr+dem+OCD)","M1\n(proxy)","Divisia M1\n(user-cost)"]
vals=[hi_r2("m2_pre2021"), hi_r2("comp_pre2021"), hi_r2("m1_pre2021"), hi_r2("divisia_pre2021")]
cols=[DIM, TEAL, SLATE, AMBER]
bars=axB.bar(labels, vals, color=cols, edgecolor=INK, lw=0.6)
for b,v in zip(bars,vals):
    axB.text(b.get_x()+b.get_width()/2, v+0.006, f"{v:.2f}", ha="center", fontsize=9.5, color=INK)
axB.set_title("High-regime inflation information (R\u00b2)", fontsize=10.5, color=INK)
axB.set_ylabel("R\u00b2, next-12m CPI"); axB.set_ylim(0,0.26)
axB.text(0.5,0.93,"both transactional constructions \u2248 5\u00d7 M2;\nand they agree with each other",transform=axB.transAxes,
         ha="center",fontsize=8,color=DIM,style="italic")
axB.tick_params(axis="x", labelsize=7.5)
axB.spines[["top","right"]].set_visible(False)

plt.tight_layout()
fig.savefig("results/fig_composition_convergence.png", dpi=140)
print("wrote results/fig_composition_convergence.png  | measured corr g/l =", corr_g, corr_l, "| R2:", dict(zip(['M2','comp','M1','Div'],vals)))

#!/usr/bin/env python3
"""Figure: share of crisis years in which the CS dividend pays zero (procyclical halt)."""
import json, os
import matplotlib; matplotlib.use("Agg")
import matplotlib.pyplot as plt

here = os.path.dirname(__file__)
R = json.load(open(os.path.join(here,"..","results","stress_results.json")))
A = R["A_procyclical_halt"]
labels = ["Great\nDepression","1970s\nstagflation","COVID\n2020-22","2008\ncrisis"]
keys = ["Great Depression (1930-1939)","1970s stagflation (1973-1982)","COVID (2020-2022)","2008 crisis (2007-2011)"]
vals = [A[k]["pct_years_no_dividend"] for k in keys]

fig, ax = plt.subplots(figsize=(7.2,4.2))
bars = ax.bar(labels, vals, color=["#9E2B25","#C06A1F","#C06A1F","#2E6F9E"], width=0.62)
ax.set_ylabel("Share of crisis years paying\nzero dividend (%)")
ax.set_title("The Citizens Standard dividend is procyclical:\nit halts in every contraction (issuance = max(0, real growth) \u00D7 M2)")
ax.set_ylim(0,60)
for b,v in zip(bars,vals):
    ax.text(b.get_x()+b.get_width()/2, b.get_height()+1.2, f"{int(v)}%", ha="center", fontsize=10)
ax.spines[["top","right"]].set_visible(False)
plt.tight_layout(); plt.savefig(os.path.join(here,"..","results","fig_dividend_halt.png"), dpi=140)
print("figure saved")

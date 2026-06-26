"""Paper 1 — Figures 4, A.2, A.3 (grounded).

These three figures previously had no generator in the package. This script
reproduces them from the corrected engine and the grounded Mode Omega
calibration, so they stay consistent with cs_engine / mode_omega / the HTML
engine. Output PNGs match the embedded image dimensions (dpi=120).

  Figure 4   -> fig4_omega_governors.png   (image4.png; 1575x1277)
  Figure A.2 -> figA2_rotation.png         (image9.png; 1784x1038)
  Figure A.3 -> figA3_midcrisis.png        (image10.png; 1684x1197)

Grounded anchors used here:
  Mode A deflation  -1.65%/yr (cs_engine derived; appreciation 2.95x)
  Mode A floor ~$233K   Mode C floor ~$230K   Mode C lifetime ~$492K (+$262K KI)  [GE realizable basis]
  Mode C KI         $199/mo at launch
  Demographic governor: K1 x1.30, K2 capture 0.60 -> 0.78 (+30%)
  Productivity governor: K2 capture -> 0.96 (+30% more), 25%/yr reversion
  KI soft floor: conditional, triggers only if deflation would exceed -1.2%
"""
import sys, os
sys.path.insert(0, os.path.dirname(__file__))
import matplotlib; matplotlib.use("Agg")
import matplotlib.pyplot as plt
import matplotlib.ticker as mticker
import numpy as np
from cs_engine import simulate, RG

plt.rcParams.update({
    "font.family": "serif", "font.serif": ["DejaVu Serif"],
    "axes.edgecolor": "#555", "axes.linewidth": 0.8, "axes.grid": True,
    "axes.axisbelow": True, "grid.color": "#dddddd", "grid.linewidth": 0.6,
    "font.size": 11, "axes.titlesize": 12, "axes.titleweight": "bold",
})
OUT = os.path.join(os.path.dirname(__file__), "..", "figures")
os.makedirs(OUT, exist_ok=True)
CA, CC = "#2a8f8f", "#ba7517"          # Mode A / Mode C accents (match make_figA3)
C_POP, C_PROD = "#2563eb", "#e8a23d"   # environment lines
C_K1, C_K2, C_KI = "#7c3aed", "#10b981", "#d97706"
HZ = 65


# ---- Grounded Mode Omega governor path (ported from the corrected HTML omegaGovernors) ----
def omega_governor_path():
    """65-yr illustrative environment + the governor response it triggers.
    K1 multiplier -> 1.30x, K2 capture 0.60 -> 0.78 (+30%) under demographic
    stress, -> 0.96 with the productivity governor; conditional KI only when
    deflation would exceed -1.2%. Matches Citizens_Standard_Engine.html."""
    t = np.arange(HZ + 1)
    pop = np.where(t <= 25, 0.5 - 0.04 * t,
          np.where(t <= 45, -0.5, -0.5 + 0.03 * (t - 45)))      # +0.5% -> -0.5% -> recover
    prod = np.where((t >= 30) & (t <= 45),
                    1.8 + 2.7 * np.where((t >= 30) & (t <= 45),
                                         1 - np.abs(t - 37.5) / 7.5, 0), 1.8)  # boom peak ~4.5%
    k1m, k2m, ki, defl = [], [], [], []
    for tt in t:
        m, cap, k = 1.0, 0.60, 0.0
        demo = tt >= 18                                  # net pop growth crosses below +0.2% ~yr18
        if demo:
            r = min(1.0, max(0.0, (tt - 18) / 20))
            m = 1.0 + 0.30 * r                           # K1 -> 1.30x
            cap = 0.60 + 0.18 * r                         # K2 capture -> 0.78 (+30% of base)
        if 30 <= tt <= 45:                               # productivity governor, reverts 25%/yr after
            b = 0.18 * min(1.0, (tt - 30) / 3)
            cap = min(1.0, cap + b)
        elif tt > 45:
            cap = min(1.0, cap + 0.18 * (0.75 ** (tt - 45)))
        # illustrative late-period deflation stress -> conditional KI soft floor at -1.2%
        d = 0.80 + (0.80 * max(0.0, (tt - 46) / 6) if tt >= 46 else 0.0)   # -0.80% base deepening late
        d = min(d, 1.60)
        if d > 1.20:
            k = 0.40 * min(1.0, (tt - 48) / 2)           # KI activates as the soft floor
        k1m.append(m); k2m.append(cap / 0.60); ki.append(max(0.0, k)); defl.append(-d)
    return t, pop, prod, np.array(k1m), np.array(k2m), np.array(ki), np.array(defl)


def fig4_omega_governors(path):
    t, pop, prod, k1m, k2m, ki, defl = omega_governor_path()
    fig, ax = plt.subplots(3, 1, figsize=(13.125, 10.64), dpi=120)
    fig.suptitle("Mode \u03a9 \u2014 How the Governors Respond to Conditions Over Time\n"
                 "(Illustrative 65-year environment: aging population, mid-century productivity boom, "
                 "late-period deflation)", fontsize=13, fontweight="bold")
    # Panel 1 — environment
    a = ax[0]; a.set_title("The Environment \u2014 What the Governors Observe")
    a.plot(t, pop, color=C_POP, lw=2.2, label="Population growth (%)")
    a.axhline(0.0, ls="--", color="#999", lw=0.9); a.axhline(0.2, ls=":", color="#bbb", lw=0.8)
    a.set_ylabel("Population growth (%)", color=C_POP); a.tick_params(axis="y", labelcolor=C_POP)
    a.axvspan(30, 45, color=C_PROD, alpha=0.10); a.axvspan(48, 55, color=C_POP, alpha=0.07)
    a2 = a.twinx(); a2.plot(t, prod, color=C_PROD, lw=2.2, label="Productivity index growth (%)")
    a2.set_ylabel("Productivity growth (%)", color=C_PROD); a2.tick_params(axis="y", labelcolor=C_PROD)
    a2.grid(False); a.text(37.5, pop.min(), "Productivity\nboom", color="#b45309", ha="center",
                           va="bottom", fontsize=9, style="italic")
    l1, lb1 = a.get_legend_handles_labels(); l2, lb2 = a2.get_legend_handles_labels()
    a.legend(l1 + l2, lb1 + lb2, loc="lower left", frameon=False, fontsize=9)
    # Panel 2 — adaptive multipliers (grounded calibration)
    b = ax[1]; b.set_title("The Response \u2014 Adaptive Multipliers Activate and Revert (25%/yr)")
    b.axhline(1.0, ls="--", color="#999", lw=1.0, label="Base (1.0\u00d7, no governor)")
    b.axhline(2.0, ls=":", color="#cc8888", lw=0.9)
    b.plot(t, k1m, color=C_K1, lw=2.4, label="K1 governor multiplier (\u21921.30\u00d7)")
    b.plot(t, k2m, color=C_K2, lw=2.4, label="K2 governor multiplier (\u21921.30\u00d7; 1.60\u00d7 in boom)")
    b.fill_between(t, 1.0, k1m, color=C_K1, alpha=0.10); b.fill_between(t, 1.0, k2m, color=C_K2, alpha=0.10)
    b.axvspan(30, 45, color=C_PROD, alpha=0.10); b.axvspan(48, 55, color=C_POP, alpha=0.07)
    b.set_ylabel("Multiplier (\u00d7 base issuance)"); b.set_ylim(0.9, 2.15)
    b.legend(loc="upper left", frameon=False, fontsize=9)
    # Panel 3 — conditional KI safety valve
    c = ax[2]; c.set_title("The Safety Valve \u2014 Conditional KI Activates Only Under Stress")
    c.plot(t, ki, color=C_KI, lw=2.4, drawstyle="steps-mid", label="KI conditional stream (% of M2)")
    c.fill_between(t, 0, ki, step="mid", color=C_KI, alpha=0.18)
    c.axhline(0.40, ls=":", color="#cc5555", lw=0.9)
    c.text(8, 0.43, "KI trigger: deflation > 1.2%", color="#cc5555", fontsize=8.5)
    c.set_ylabel("KI issuance (% of M2)", color=C_KI); c.tick_params(axis="y", labelcolor=C_KI)
    c.set_ylim(0, 0.7); c.axvspan(48, 55, color=C_POP, alpha=0.07)
    c2 = c.twinx(); c2.plot(t, -defl, color="#cc3333", lw=1.8, ls="--", label="Deflation rate (%)")
    c2.set_ylabel("Deflation rate (%)", color="#cc3333"); c2.tick_params(axis="y", labelcolor="#cc3333")
    c2.set_ylim(0, 2.0); c2.grid(False)
    c.text(50.5, 0.62, "KI activates\n(deflation > 1.2%)", color="#b45309", ha="center", fontsize=9,
           fontweight="bold")
    c.set_xlabel("Years from launch")
    fig.text(0.5, 0.005,
             "Every governor is formula-driven: it reads published data (dependency ratio, population "
             "growth, productivity index, CPI) and adjusts issuance automatically.\nNo committee judgment "
             "is involved \u2014 the multipliers rise when conditions warrant and revert to baseline at "
             "25% per year once conditions normalize.",
             ha="center", fontsize=9, style="italic", color="gray")
    for a_ in ax: a_.set_xlim(0, HZ)
    fig.tight_layout(rect=[0, 0.02, 1, 0.95]); fig.savefig(path, dpi=120); plt.close(fig)


def figA2_rotation(path):
    """Mode A <-> Mode C every 30 years over 200 years. Mode A deflates at the
    grounded -1.65%/yr; Mode C inflates at +2%/yr. CPI sawtooth + inflation-rate."""
    A_ = simulate("A"); driftA = A_[1]["cpiIdx"]/A_[0]["cpiIdx"] - 1   # -0.0165 (engine-derived)
    driftC = +0.02
    T = 200; t = np.arange(T + 1)
    cpi = np.empty(T + 1); cpi[0] = 1.0
    infl = np.empty(T + 1)
    for i in range(T + 1):
        modeA = (i // 30) % 2 == 0       # A for yrs 0-30, C for 30-60, ...
        infl[i] = driftA if modeA else driftC
        if i > 0:
            cpi[i] = cpi[i - 1] * (1 + infl[i])
    fig, ax = plt.subplots(2, 1, figsize=(14.87, 8.65), dpi=120)
    fig.suptitle("Generational Mode Rotation \u2014 Mode A \u2194 Mode C Every 30 Years (200-Year Horizon)",
                 fontsize=13, fontweight="bold")

    def shade(a):
        for k in range(0, T, 30):
            modeA = (k // 30) % 2 == 0
            a.axvspan(k, min(k + 30, T), color=(CA if modeA else CC), alpha=0.10)

    a = ax[0]; a.set_title("Price Level \u2014 Sawtooth Pattern")
    shade(a); a.plot(t, cpi, color="#333", lw=2.2)
    a.axhline(1.0, ls="--", color="#999", lw=0.9)
    a.set_ylabel("CPI (1.0 = launch)")
    from matplotlib.patches import Patch
    a.legend(handles=[Patch(facecolor=CA, alpha=0.3, label="Mode A (deflationary)"),
                      Patch(facecolor=CC, alpha=0.3, label="Mode C (inflationary)")],
             loc="upper left", frameon=False, fontsize=10)
    b = ax[1]; b.set_title("Annual Inflation Rate \u2014 Each Mode Hits Its Target Within Window")
    shade(b); b.plot(t, infl * 100, color="#333", lw=2.0)
    b.axhline(0.0, ls="--", color="#999", lw=0.9)
    b.axhline(driftA * 100, ls=":", color=CA, lw=1.0); b.axhline(driftC * 100, ls=":", color=CC, lw=1.0)
    b.set_ylabel("Inflation rate (%)"); b.set_xlabel("Years from launch")
    b.yaxis.set_major_formatter(mticker.FuncFormatter(lambda v, _: f"{v:.1f}"))
    for a_ in ax: a_.set_xlim(0, T)
    fig.tight_layout(rect=[0, 0, 1, 0.96]); fig.savefig(path, dpi=120); plt.close(fig)


def figA3_midcrisis(path):
    """Mid-crisis A->C switch at yr27. Floor/CPI from the corrected engine;
    grounded lifetime bars on the GE realizable basis ($233K stay; $230K + $262K KI = $492K switch)."""
    A = simulate("A", 0.054); ages = list(range(66))   # GE realizable return for Mode A
    floor = [y["floorReal"] / 1e3 for y in A]
    cpiA = [y["cpiIdx"] for y in A]
    sw = 27
    cpiSwitch = [cpiA[t] if t <= sw else cpiA[sw] * (1.02) ** (t - sw) for t in ages]
    kiSwitch = [0 if t < sw else min(236, 199 + 199 * 0.015 * (t - sw)) for t in ages]
    fig, ax = plt.subplots(2, 2, figsize=(14.04, 9.98), dpi=120)
    fig.suptitle("Mid-Crisis Mode Transition \u2014 Recession at Years 25\u201326, Mode Change at Year 27",
                 fontsize=13, fontweight="bold")
    ax[0, 0].axvspan(25, 26, color="#e8b3b3", alpha=0.5)
    ax[0, 0].plot(ages, cpiA, color=CA, lw=2, label="Stay in Mode A")
    ax[0, 0].plot(ages, cpiSwitch, color=CC, lw=2, ls="--", label="Switch to Mode C at yr 27")
    ax[0, 0].set_title("Price level (CPI index, 1.0 = launch)"); ax[0, 0].set_xlabel("Years")
    ax[0, 0].set_xlim(0, 65); ax[0, 0].legend(frameon=False, fontsize=10)
    ax[0, 1].axvspan(25, 26, color="#e8b3b3", alpha=0.5)
    ax[0, 1].plot(ages, kiSwitch, color=CC, lw=2, label="Switch: KI dividend (real $/mo)")
    ax[0, 1].plot(ages, [0] * 66, color=CA, lw=2, label="Stay: KI = 0")
    ax[0, 1].set_title("KI citizen dividend ($/month, real)"); ax[0, 1].set_xlabel("Years")
    ax[0, 1].set_xlim(0, 65); ax[0, 1].legend(frameon=False, fontsize=10)
    ax[1, 0].axvspan(25, 26, color="#e8b3b3", alpha=0.5)
    ax[1, 0].plot(ages, floor, color="#444", lw=2.4, label="Locked real floor (A and C nearly identical)")
    ax[1, 0].set_title("Locked Stable Floor (real, $K)"); ax[1, 0].set_xlabel("Age (years from birth)")
    ax[1, 0].set_ylabel("$K (2025)"); ax[1, 0].set_xlim(0, 65); ax[1, 0].set_ylim(0, 280)
    ax[1, 0].legend(frameon=False, fontsize=9.5, loc="upper left")
    ax[1, 0].annotate("stay ~$233K, switch ~$230K\n\u2014 the floor barely moves",
                      (65, floor[-1]), xytext=(-10, -38), textcoords="offset points",
                      ha="right", fontsize=9.5, color="#444")
    labels = ["Stay\nMode A", "Switch A\u2192C\nat yr 27"]; x = np.arange(2); w = 0.36
    lockfloor = [233, 230]; total = [233, 492]
    ax[1, 1].bar(x - w / 2, lockfloor, w, color="#9aa0a6", label="Locked floor only")
    ax[1, 1].bar(x + w / 2, total, w, color=CC, label="Total real value (+KI)")
    ax[1, 1].set_title("Total real captured value at age 65"); ax[1, 1].set_ylabel("$K (2025)")
    ax[1, 1].set_xticks(x); ax[1, 1].set_xticklabels(labels); ax[1, 1].set_ylim(0, 560)
    ax[1, 1].legend(frameon=False, fontsize=10)
    for xi, (lf, tv) in enumerate(zip(lockfloor, total)):
        ax[1, 1].annotate(f"${lf}K", (xi - w / 2, lf), xytext=(0, 3), textcoords="offset points",
                          ha="center", fontsize=9.5)
        ax[1, 1].annotate(f"${tv}K", (xi + w / 2, tv), xytext=(0, 3), textcoords="offset points",
                          ha="center", fontsize=9.5, fontweight="bold", color=CC)
    fig.tight_layout(rect=[0, 0, 1, 0.97]); fig.savefig(path, dpi=120); plt.close(fig)


if __name__ == "__main__":
    from PIL import Image
    jobs = [(fig4_omega_governors, "fig4_omega_governors.png"),
            (figA2_rotation, "figA2_rotation.png"),
            (figA3_midcrisis, "figA3_midcrisis.png")]
    for fn, name in jobs:
        p = os.path.join(OUT, name); fn(p)
        print(f"wrote {name}  {Image.open(p).size}")

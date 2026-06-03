"""
compare_to_paper.py
====================
Side-by-side comparison of the paper's published figures vs. our
reconstructed values using authoritative data.
"""

print("=" * 100)
print("PAPER vs RECONSTRUCTION  —  All headline tables")
print("=" * 100)

# ========================================================================
# Table 1: central scenario
# ========================================================================
print()
print("SECTION 4.1 / TABLE 1   Central scenario (4.5% real post-2025)")
print("-" * 100)
print(f"{'Cohort':<8}{'Paper Floor':>14}{'New Floor':>14}{'Delta $':>11}{'Delta %':>10}"
      f"{'Paper x med':>14}{'New x med':>12}{'Paper x mean':>15}{'New x mean':>13}")
print("-" * 100)
data = [
    # paper_floor, new_floor, paper_med, new_med, paper_mean, new_mean
    ("A", 680322, 690943, 2.6, 2.66, 1.0, 1.03),
    ("B", 704322, 723667, 2.9, 3.02, 1.1, 1.11),
    ("C", 692432, 712528, 3.1, 3.24, 1.1, 1.13),
    ("D", 459266, 467634, 2.2, 2.23, 0.7, 0.76),
]
for row in data:
    c, pf, nf, pm, nm, pmn, nmn = row
    delta = nf - pf
    pct = 100 * delta / pf
    print(f"{c:<8}${pf:>12,.0f}${nf:>12,.0f}${delta:>9,.0f}{pct:>9.2f}%"
          f"{pm:>13.2f}x{nm:>11.2f}x{pmn:>14.2f}x{nmn:>12.2f}x")

# ========================================================================
# Section 4.5 decomposition (Cohort A)
# ========================================================================
print()
print("SECTION 4.5   Decomposition of Cohort A (real 2025$)")
print("-" * 100)
print(f"{'Component':<32}{'Paper':>18}{'New':>18}{'Paper share':>15}{'New share':>13}")
print("-" * 100)
decomp = [
    ("K1 deposit at birth (1960)",     815,    816.05,  0.12,  0.12),
    ("K2 cumulative (1960-2025)",      33319, 33951.78, 4.90,  4.91),
    ("Total principal",                34134, 34767.83, 5.02,  5.03),
    ("Equity compounding gain",        646188, 656174.74, 94.98, 94.97),
    ("Final Stable Floor",             680322, 690943.0, 100.0, 100.0),
]
for name, p, n, ps, ns in decomp:
    print(f"{name:<32}${p:>16,.2f}${n:>16,.2f}{ps:>13.2f}%{ns:>11.2f}%")

# ========================================================================
# Table 3: stress tests
# ========================================================================
print()
print("SECTION 5.1 / TABLE 3   Stress tests")
print("-" * 100)
print(f"{'Cohort':<8}{'Paper Depr':>14}{'New Depr':>13}"
      f"{'Paper Stag':>14}{'New Stag':>13}"
      f"{'Paper D/cent':>15}{'New D/cent':>13}"
      f"{'Paper S/cent':>15}{'New S/cent':>13}")
print("-" * 100)
stress = [
    ("A", 248329, 248427, 171316, 173446, 0.37, 0.36, 0.25, 0.25),
    ("B", 516128, 522631, 345231, 353843, 0.73, 0.72, 0.49, 0.49),
    ("C", 309040, 320038, 217508, 227427, 0.45, 0.45, 0.31, 0.32),
    ("D", 236593, 240775, 161129, 165096, 0.52, 0.51, 0.35, 0.35),
]
for c, pd, nd, ps, ns, pdc, ndc, psc, nsc in stress:
    print(f"{c:<8}${pd:>12,.0f}${nd:>11,.0f}${ps:>12,.0f}${ns:>11,.0f}"
          f"{pdc:>14.2f}x{ndc:>12.2f}x{psc:>14.2f}x{nsc:>12.2f}x")

# Below-median findings
print()
print("Below-median findings under stress:")
print("  Paper Section 5.1:  A below median under both Depression AND Stagflation,")
print("                      C marginally below median under Stagflation,")
print("                      D below median under Stagflation,")
print("                      B above both medians")
print("  New:                A below median under both Depression AND Stagflation (matches),")
print("                      B above both medians (matches),")
print("                      C now ABOVE median under both (paper had C marginally below under Stag),")
print("                      D below median under Stagflation (matches)")

# ========================================================================
# Monte Carlo Section 6
# ========================================================================
print()
print("SECTION 6 / TABLE M1   Block bootstrap, 1929-2025 universe (10,000 paths)")
print("-" * 100)
print(f"{'Cohort':<8}{'Paper P5':>11}{'New P5':>11}"
      f"{'Paper P50':>12}{'New P50':>11}{'Paper Mean':>13}{'New Mean':>12}"
      f"{'Paper P<med':>13}{'New P<med':>12}")
print("-" * 100)
def fmt(v): return f"${v/1000:>4,.0f}K" if v < 1e6 else f"${v/1e6:>3,.2f}M"
mc = [
    ("A",  82000,  80000,   501000,  485000,   860000,  857000, 27.7, 28.3),
    ("B", 110000, 109000,   655000,  669000,  1160000, 1200000, 18.1, 17.9),
    ("C", 145000, 142000,   862000,  882000,  1650000, 1650000, 10.6, 10.7),
    ("D", 183000, 173000,  1010000, 1030000,  1880000, 1910000,  6.8,  7.5),
]
for c, pp5, np5, pp50, np50, pm, nm, ppm, npm in mc:
    print(f"{c:<8}{fmt(pp5):>11}{fmt(np5):>11}{fmt(pp50):>12}{fmt(np50):>11}"
          f"{fmt(pm):>13}{fmt(nm):>12}{ppm:>12.1f}%{npm:>11.1f}%")

# ========================================================================
# Headline range comparison
# ========================================================================
print()
print("HEADLINE / ABSTRACT  —  median advantage range")
print("-" * 100)
print(f"{'Statistic':<55}{'Paper':>20}{'New':>20}")
print("-" * 100)
print(f"{'Deterministic central, vs median (range across cohorts)':<55}"
      f"{'2.2x - 3.1x':>20}{'2.23x - 3.24x':>20}")
print(f"{'Bootstrap P50, 1960-2025 universe':<55}"
      f"{'2.0x - 4.4x':>20}{'1.98x - 4.56x':>20}")
print(f"{'Bootstrap P50, 1929-2025 universe':<55}"
      f"{'1.9x - 4.8x':>20}{'1.87x - 4.88x':>20}")
print(f"{'P(<median) range across configs':<55}"
      f"{'6% - 28%':>20}{'5.3% - 28.8%':>20}")
print()
print("Bottom line: all paper headline ranges hold up under reconstruction,")
print("with small refinements (~3% upward shift in deterministic values from")
print("corrected GDP/real-GDP vintage; MC distributions very close to paper).")

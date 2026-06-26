"""
Stage 2 -- rent CAPITALIZATION, fully swept (calibrated tier).

Converts Stage-1 rent EXPOSURE into an actual rent increase via the standard
incidence share

    capture = eps_d / (eps_d + eps_s)

and reports a full uncertainty band by sweeping BOTH elasticities across their
literature ranges, rather than evaluating at single points.

PARAMETER RANGES (all from cited sources):
  eps_d  price elasticity of housing DEMAND, low-income renters:
         Ihlanfeldt (1982) 0.14-0.62 for low-income; DiPasquale-Wheaton (1996)
         ~0.78 for 25-34s. Swept 0.15 (low) / 0.40 (central) / 0.62 (high),
         staying within the low-income band (the dividend's renters are
         bottom-decile concentrated, so the low-income range is the right one).
  eps_s  housing SUPPLY elasticity, Saiz (2010) QJE:
         population-weighted US average 1.75; avg-regulated-metro IQR 1.25-2.45;
         constrained metros <1.0 (Chicago); severely land-constrained lower.
         Swept 0.60 (constrained) / 1.75 (US pop-weighted) / 2.45 (elastic p90).

Stage-1 exposure is carried forward live (and is invariant to dividend level).
Sources fully cited in ../README.md.
"""
import subprocess, re, os

_stage1 = os.path.join(os.path.dirname(__file__), "stage1_rent_exposure.py")
out = subprocess.run(["python3", _stage1], capture_output=True, text=True).stdout
exp_pct = float(re.search(r"artifact-capped ([\d.]+)% of dividend", out).group(1))/100
div_b   = float(re.search(r"Dividend modeled: \$([\d.]+)B", out).group(1))
EXPOSED = exp_pct*div_b*1e9
DIV     = div_b*1e9

print(f"Stage-1 carried forward: exposure {exp_pct*100:.1f}% of ${div_b:.1f}B "
      f"= ${EXPOSED/1e9:.2f}B exposed (invariant to dividend level)")
print()

# --- parameter grids (labelled, from cited ranges) ---
eps_d_grid = [("low (Ihlanfeldt floor)",0.15),
              ("central",0.40),
              ("high (Ihlanfeldt ceiling)",0.62)]
eps_s_grid = [("constrained metro (<1, Saiz)",0.60),
              ("US pop-weighted (Saiz 1.75)",1.75),
              ("elastic p90 (Saiz)",2.45)]

def capture(ed,es): return ed/(ed+es)

# --- full 3x3 sweep grid: capitalization as % of dividend ---
print("FULL SWEEP -- rent capitalization as % of dividend  (capture = eps_d/(eps_d+eps_s))")
print()
hdr = f"{'eps_d \\\\ eps_s':>26} | " + " | ".join(f"{lbl.split('(')[0].strip()[:14]:>14}" for lbl,_ in eps_s_grid)
print(hdr); print("-"*len(hdr))
allvals=[]
for dl,ed in eps_d_grid:
    cells=[]
    for sl,es in eps_s_grid:
        pct=100*EXPOSED*capture(ed,es)/DIV
        allvals.append((pct,ed,es,dl,sl))
        cells.append(f"{pct:>13.1f}%")
    print(f"{dl[:26]:>26} | " + " | ".join(cells))

lo=min(allvals); hi=max(allvals); 
# central = central eps_d (0.40) x pop-weighted eps_s (1.75)
central=[v for v in allvals if abs(v[1]-0.40)<1e-9 and abs(v[2]-1.75)<1e-9][0]
print()
print("="*70)
print("BANDED HEADLINE (full sweep):")
print(f"  Central (eps_d 0.40, Saiz 1.75):  {central[0]:.1f}% of dividend  (${EXPOSED*capture(0.40,1.75)/1e9:.2f}B/yr)")
print(f"  Full range across both elasticities: {lo[0]:.1f}% to {hi[0]:.1f}% of dividend")
print(f"    floor  {lo[0]:.1f}%  at eps_d={lo[1]}, eps_s={lo[2]} ({lo[3]}, {lo[4]})")
print(f"    ceiling {hi[0]:.1f}% at eps_d={hi[1]}, eps_s={hi[2]} ({hi[3]}, {hi[4]})")
print(f"  In dollars (Mode D ${div_b:.0f}B): ${EXPOSED*capture(lo[1],lo[2])/1e9:.2f}B to "
      f"${EXPOSED*capture(hi[1],hi[2])/1e9:.2f}B/yr capitalizing into rent.")
print()
print("READING: even at the worst corner (elastic demand into constrained supply),")
print(f"  the dividend's rent leak stays under {hi[0]:.0f}% of the dividend; the central")
print(f"  estimate is ~{central[0]:.0f}%. The leak is bounded and small; the rest buys")
print("  real consumption. First-round partial equilibrium; long-run supply response,")
print("  migration, and household formation push it lower (see README caveats).")

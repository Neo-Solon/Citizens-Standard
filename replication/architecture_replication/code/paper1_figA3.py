"""Paper 1 Figure A.3 (mid-crisis Mode A->C transition) — GE realizable basis.
Thin wrapper matching the provenance note in Appendix A.4; delegates to the
figA3_midcrisis builder so the figure is reproducible by the documented filename."""
import os
from paper1_extra_figures import figA3_midcrisis
FIGDIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'figures')
if __name__ == "__main__":
    out = os.path.join(FIGDIR, "figA3_midcrisis.png")
    figA3_midcrisis(out)
    print("wrote", os.path.relpath(out, os.path.dirname(__file__)))

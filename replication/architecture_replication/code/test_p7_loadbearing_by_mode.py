"""Does P7's load-bearing role vary BY MODE? Test each mode against BOTH
components of P7: (a) determinacy [unique price path], (b) circuit separation
[KI hits M^T not M2]."""
import sys; sys.path.insert(0,'.')
import cs_engine as E

M2=22366.2e9; MT_over_M2=0.514; RG=0.02

def sep_dependency(mode):
    """Does the mode's inflation NUMBER depend on circuit separation?
    Only binds if ki>0 (KI is the thing that could be mis-attributed to M2 vs M^T)."""
    p=E.PRESETS[mode]; ki=p['ki']
    if ki==0:
        return False, "ki=0: no KI channel, separation dependency is VACUOUS"
    infl_sep = ki/MT_over_M2 - RG      # on M^T
    infl_nosep = ki - RG               # on all M2
    return abs(infl_sep-infl_nosep)>0.005, f"ki>0: {infl_sep*100:+.2f}% (M^T) vs {infl_nosep*100:+.2f}% (M2)"

def det_dependency(mode):
    """Does the mode's REGIME CLAIM depend on determinacy?
    Any mode that TARGETS a rate and claims to DELIVER it needs the target to be
    the unique equilibrium. All three target a distinct rate, so all three need it
    for the 'we deliver the selected regime' claim to be non-empty."""
    p=E.PRESETS[mode]
    target={'A':'deflation ~-1.6%','B':'price stability 0%','C':'inflation +2%'}[mode]
    # every mode makes a delivery claim -> all depend on determinacy for that claim
    return True, f"targets {target}; delivery claim needs uniqueness"

print("="*70)
print("P7 LOAD-BEARING BY MODE")
print("="*70)
print(f"  {'mode':<6}{'DETERMINACY dep':<22}{'SEPARATION dep':<28}")
print("  "+"-"*62)
for m in 'ABC':
    d,dnote=det_dependency(m)
    s,snote=sep_dependency(m)
    print(f"  {m:<6}{('YES' if d else 'no'):<22}{('YES' if s else 'no'):<28}")
    print(f"        det: {dnote}")
    print(f"        sep: {snote}")
print()
print("="*70)
print("READING")
print("="*70)
print("""
  DETERMINACY (P7 part 1): load-bearing in ALL THREE modes. Every mode targets a
    distinct rate and claims the constitution DELIVERS it; that delivery claim is
    empty without uniqueness. Even Mode A (deflation) and Mode B (0%) need the
    targeted rate to be the unique equilibrium, not just an announced one.

  SEPARATION (P7 part 2): load-bearing ONLY in Mode C (and any ki>0 mode). Modes
    A and B have ki=0 -- no inflation channel to mis-attribute -- so the 'KI hits
    M^T not M2' dependency is VACUOUS for them. Mode B's 0% comes from k2=1
    (issuance=growth), which needs no separation argument at all.

  => The answer is nuanced:
     - The DETERMINACY half of P7 is load-bearing under ALL modes.
     - The SEPARATION half is load-bearing ONLY under Mode C (the inflationary mode).
     So 'only load-bearing under certain modes' is TRUE for the separation half,
     but the determinacy half is universal across modes.
""")

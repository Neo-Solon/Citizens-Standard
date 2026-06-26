"""
Capture / fig-leaf risk -- empirical override base rate of formal monetary and
fiscal commitment rules. Honest build: we go in expecting this to show the risk
is REAL, and we let the data say so. We do NOT model "probability THIS rule fails"
(no such parameter exists); we report how often COMPARABLE rules have actually been
overridden, suspended, or reversed -- the closest measurable analogue to the
fig-leaf objection.

This module's purpose is to GROUND the capture objection, not to defend against it.
If the data says the risk is substantial, that is the finding.

VERIFIED EMPIRICAL ANCHORS:

A. Fiscal rules (IMF Fiscal Rules Database, 1985-2024, ~100+ countries):
   - 2020 (COVID): ~90% of countries breached deficit-rule limits.
   - Normal times (2014-2019): ~60% of advanced economies and ~40% of EMDEs failed
     to comply with DEBT rules; ~20% (AE) / ~40% (EMDE) breached DEFICIT limits.
   - By 2024, two-thirds of fiscal rules include escape clauses (2x the 2000 share);
     escape-clause use jumped from ~5% (GFC) to widespread (COVID).
   - Deviations are "highly persistent" and "very difficult to reverse."

B. Central-bank independence (the closer monetary analogue):
   - IMF WP 2026/040: of 132 governor transitions (28 countries, 2000-2024),
     38% were POLITICALLY MOTIVATED; ~50% in emerging markets.
   - Romelli CBI dataset (1950-2023): of 370 legislative reforms, 91 (~25%) were
     REVERSALS of independence.
   - "Strong legal protections are no guarantee against political interference"
     (de jure independence != de facto).
"""

print("="*74)
print("CAPTURE / FIG-LEAF RISK -- empirical override base rate of commitment rules")
print("="*74)
print("Purpose: GROUND the capture objection in data, not defend against it.")
print()

print("A. FISCAL RULES (IMF Fiscal Rules Database, 1985-2024)")
fiscal=[
 ("Deficit-rule breach, 2020 (COVID crisis)", 90),
 ("Debt-rule non-compliance, advanced econ, 2014-2019 (normal times)", 60),
 ("Debt-rule non-compliance, EMDEs, 2014-2019", 40),
 ("Deficit-rule breach, EMDEs, 2014-2019 (normal times)", 40),
 ("Deficit-rule breach, advanced econ, 2014-2019", 20),
 ("Fiscal rules with built-in escape clauses by 2024", 67),
]
for lbl,pct in fiscal:
    print(f"   {pct:>3}%  {lbl}")
print()
print("B. CENTRAL-BANK INDEPENDENCE (closer monetary analogue)")
cbi=[
 ("Governor transitions politically motivated, 2000-2024 (all)", 38),
 ("Governor transitions politically motivated, emerging markets", 50),
 ("CBI legislative reforms that REVERSED independence, 1950-2023", 25),
]
for lbl,pct in cbi:
    print(f"   {pct:>3}%  {lbl}")
print()
print("-"*74)
print("READING (honest):")
print(" The fig-leaf risk is NOT hypothetical. Formal monetary/fiscal commitment")
print(" rules are overridden, suspended, or reversed at high and measurable rates:")
print("  - in CRISIS, override is near-universal (~90% breached deficit rules in 2020);")
print("  - even in NORMAL times, 20-60% non-compliance is typical;")
print("  - ~38% of central-bank leadership changes are politically motivated, ~50%")
print("    in emerging markets; ~25% of CBI reforms walk independence BACK;")
print("  - overrides are persistent and hard to reverse, and escape clauses are")
print("    increasingly built INTO the rules (two-thirds by 2024).")
print()
print(" CONCLUSION: the objection is empirically correct. A written issuance rule")
print(" should be expected to face override pressure, and historically comparable")
print(" rules yield to it often, especially under crisis -- exactly the mechanism")
print(" the objection names. This is a REAL, substantial risk, not a solved one.")

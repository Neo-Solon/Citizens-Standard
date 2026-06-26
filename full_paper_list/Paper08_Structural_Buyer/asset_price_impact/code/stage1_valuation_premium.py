"""
Asset-price impact of the floor lane -- verified build.

Grounds the floor-lane asset-price-pressure concession ("you bid up the assets you
buy", the reason Paper 2 uses an attenuated 4.26% return) by combining Paper 8's
verified absorption flow with the empirical price-impact literature.

TWO SEPARATE, SEPARATELY-CITED FACTS (deliberately NOT fused into a single derived
number, because the demand-side multiplier and the supply-side issuance response
are different parameters):

  FACT 1 (short-run price impact, demand side). Gabaix-Koijen (2021, NBER 28967)
  find a flow of $1 into equities raises aggregate value by ~$M, M central 5,
  range 3-8; microstructure dissent (Bouchaud 2021) puts M near order-unity (~1).
  The floor's verified flow (Paper 8) is f = 0.39%/yr (Mode B) to 0.65%/yr
  (floor-max, kappa_d=0). So one year's buying lifts valuations by f*M.

  FACT 2 (long-run premium, supply side). Paper 8 Prop 1 bounds the premium at
  A*/phi, where phi is the equity-SUPPLY response (firms issuing into the premium).
  GK does NOT measure phi; it is a separate empirical question. Paper 8's
  illustrative phi=0.5 gives a 0.78% premium. A weaker supply response (smaller
  phi) yields a larger premium. We report Paper 8's bound and flag phi as the
  load-bearing, unmeasured-here parameter -- we do NOT derive phi from M.

The honest synthesis: the SHORT-RUN impulse is small-to-moderate and directly
citable; the LONG-RUN premium is bounded by Paper 8's mechanism but its size turns
on a supply response neither paper nor GK pins down. This is a stress-test of the
attenuated-return assumption, not a refutation or a proof.
"""

F_MODE_B = 0.0039   # verified Paper 8, kappa_d=0.4
F_KD0    = 0.0065   # verified Paper 8, kappa_d=0
M_GRID = [("order-unity (Bouchaud)",1.0),
          ("GK central",5.0),
          ("GK high",8.0)]

print("="*74)
print("FLOOR-LANE ASSET-PRICE IMPACT")
print("="*74)
print(f"Verified absorption flow (Paper 8): {100*F_MODE_B:.2f}%/yr Mode B, "
      f"{100*F_KD0:.2f}%/yr floor-max")
print()
print("FACT 1 -- short-run valuation impulse from one year's flow = f x M (GK):")
print(f"    {'multiplier M':>26} {'Mode B':>9} {'floor-max':>10}")
for lbl,M in M_GRID:
    print(f"    {lbl:>26} {100*F_MODE_B*M:>8.1f}% {100*F_KD0*M:>9.1f}%")
print("    (demand-side price impact before any equity-supply response)")
print()
print("FACT 2 -- long-run bounded premium (Paper 8 Prop 1, A*/phi):")
print(f"    at illustrative phi=0.5: premium = {100*F_MODE_B/0.5:.2f}% (Mode B)")
print(f"    premium scales as 1/phi; a weaker supply response raises it.")
print(f"    phi is NOT measured by GK and is the load-bearing open parameter.")
print()
# benchmark: the floor buys LESS than corporate buybacks already do (Paper 8)
BUYBACK=0.015
print(f"BENCHMARK (Paper 8): corporate buybacks average ~{100*BUYBACK:.1f}%/yr of cap,")
print(f"  ~{BUYBACK/F_MODE_B:.1f}x the floor's Mode B flow. The market already absorbs a")
print(f"  larger structural bid than the floor introduces; the floor is not")
print(f"  unprecedented in magnitude, though it is permanent and rule-bound.")

"""
Stage 2 -- is the floor's own asset-price impact CONSISTENT with the attenuated
4.26% return Paper 2 already uses?

Logic: Paper 2 does not claim the historical price-taker equity return (~6.5-7%
real total return). It attenuates to 4.26% real (band 3.30-5.03) precisely because
the floor is a permanent structural buyer that bids up the assets it accumulates.
So the question is whether the price impact implied by the flow x multiplier is
in the same ballpark as the attenuation Paper 2 already took.

  historical real equity total return (long-run)   ~ 6.5%  (band 6.0-7.0)
  Paper 2 attenuated return (Mode B central)        = 4.26% (band 3.30-5.03)
  => attenuation already taken                       ~ 2.2pp (band ~1-3.7pp)

A persistent structural bid raises the valuation LEVEL (a one-time-ish premium,
not a permanent return drag once the premium stabilises). The return drag is the
premium amortised over the holding/accumulation horizon, plus the lower forward
return implied by buying at elevated valuations. We bound it by the SHORT-RUN
annual impulse (f x M) treated as an annual headwind to the realised return, swept
over the multiplier range, and compare to the 2.2pp attenuation already taken.
"""
F_MODE_B=0.0039
HIST_RETURN=0.065
ATTEN_RETURN=0.0426
ATTEN_TAKEN=HIST_RETURN-ATTEN_RETURN   # ~2.2pp

M_GRID=[("order-unity (Bouchaud)",1.0),("GK central",5.0),("GK high",8.0)]

print("="*72)
print("CONSISTENCY OF FLOOR PRICE-IMPACT WITH THE 4.26% ATTENUATED RETURN")
print("="*72)
print(f"  Historical real equity total return   ~ {100*HIST_RETURN:.1f}%")
print(f"  Paper 2 attenuated return (Mode B)      = {100*ATTEN_RETURN:.2f}%")
print(f"  Attenuation already taken               ~ {100*ATTEN_TAKEN:.1f}pp")
print()
print("  Floor's own valuation impulse (f x M) as an annual return headwind:")
print(f"    {'multiplier M':>26} {'impulse/yr':>11} {'vs 2.2pp taken':>16}")
for lbl,M in M_GRID:
    imp=F_MODE_B*M
    verdict="within" if imp<=ATTEN_TAKEN else "EXCEEDS"
    print(f"    {lbl:>26} {100*imp:>10.1f}% {verdict:>16}")
print()
print("READING:")
print(f"  At order-unity (M=1) and GK-central (M=5), the floor's annual valuation")
print(f"  impulse ({100*F_MODE_B*1:.1f}-{100*F_MODE_B*5:.1f}%) is at or below the ~2.2pp")
print(f"  attenuation Paper 2 already took -- so the attenuated return is consistent")
print(f"  with, even conservative relative to, the floor's own price impact.")
print(f"  Only at the GK-HIGH multiplier (M=8, {100*F_MODE_B*8:.1f}%) does the one-year")
print(f"  impulse exceed the attenuation -- but that is the impulse from a single")
print(f"  year's flow, not a permanent annual drag (the premium stabilises via")
print(f"  Paper 8's bounded fixed point), so it is an upper-corner caution, not a")
print(f"  standing contradiction.")
print()
print("HONEST BOTTOM LINE: the 4.26% attenuation is broadly CONSISTENT with the")
print("floor's empirical price impact across most of the multiplier range. The")
print("inelastic-markets evidence (GK) pushes toward the conservative end of the")
print("return band (3.30-5.03) rather than refuting it; the high-M corner is a")
print("genuine caution worth stating, not a refutation. The buyback benchmark")
print("(floor flow ~1/4 of buyback flow the market already absorbs) is the main")
print("reason the impact is bounded in practice.")

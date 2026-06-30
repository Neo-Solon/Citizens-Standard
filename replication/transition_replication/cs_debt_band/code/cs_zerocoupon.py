"""
Price the FORM of the CS standing stock at the band central path (~45% of GDP):
interest-bearing (coupon) vs non-interest-bearing (the zero limit). Get the section's
numbers right, including the subtlety that a safe asset earns a CONVENIENCE YIELD
the issuer can capture as seigniorage by NOT paying it out.
"""
GDP=29000.0
S=0.45*GDP                      # band central stock, $B
# Convenience yield: ~70bp historical (KVJ) at modest supply; ~36bp at today's high
# supply (StL Fed). A ~45% band is LOWER supply than today, so c sits toward the
# higher (scarcer-asset) end. Show a range.
print("FORM OF THE STANDING STOCK at the ~45%-of-GDP band\n")
print(f"  Stock S = ${S:,.0f}B (45% of ${GDP:,.0f}B GDP)\n")
print("  A safe public liability earns a CONVENIENCE YIELD: holders accept a")
print("  financial return BELOW the otherwise-fair rate because they value its")
print("  safety, liquidity, and collateral function. The issuer can either PAY")
print("  that out (coupon -> transfer to holders) or CAPTURE it (low/zero coupon")
print("  -> seigniorage to the public).\n")
print(f"  {'instrument':<26}{'pays holders':>14}{'public captures':>17}")
for label, coupon, c in [
    ("conventional coupon bond", 0.030, 0.0060),   # pays 3%, convenience ~60bp
    ("zero-coupon bill",          0.015, 0.0060),   # discount ~1.5%, half the transfer
    ("non-interest-bearing (limit)",0.000, 0.0060), # money-like: zero financial yield
]:
    transfer = coupon*S
    captured = c*S                      # convenience captured as cheaper-than-fair funding
    # at the zero limit the public also captures the coupon it would have paid
    public = captured + (0.030-coupon)*S
    print(f"  {label:<26}{transfer/GDP*100:>12.2f}% {public/GDP*100:>15.2f}% of GDP")
print(f"""
  Reading:
  - The convenience value (collateral, repo, benchmark pricing, safe store) is a
    function of the STOCK, ~{0.0060*S/GDP*100:.2f}% of GDP/yr here, and the public earns it as
    cheaper-than-fair funding whether or not a coupon is paid.
  - The coupon is a PURE TRANSFER to holders: at 3% on a 45% stock it is
    {0.030*S/GDP*100:.2f}% of GDP/yr handed to bondholders (who skew wealthy) for no
    public benefit the convenience value does not already provide.
  - Holding the stock at the non-interest-bearing limit captures the full value
    as public seigniorage and removes the transfer. This is the same pool that
    funds citizen Stable Floors.
  WHAT THE ZERO LIMIT LOSES: a traded BENCHMARK YIELD CURVE. The financial system
  prices other assets off a coupon sovereign curve; a fully non-interest-bearing
  stock supplies safety and collateral but not that benchmark. So retain a THIN
  coupon tranche for the benchmark function; hold the BULK non-interest-bearing.
  CONDITIONAL (state it): convenience yield c SHRINKS as engineered-stable money
  absorbs safe-asset demand. The more completely stable CS money becomes the safe
  store, the smaller c, and the more the standing stock can shrink toward money
  itself -- which is the point at which CS and a debt-free public-money system
  (PCM) converge.
""")

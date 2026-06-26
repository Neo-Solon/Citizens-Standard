"""
Growth-measurement error -> issuance drift -> price drift. Verified build.

CLAIM GROUNDED: "issuance matched to real growth" is only as tight as real-time
growth MEASUREMENT. Issuance set to measured g_hat while truth is g leaks the
error (g_hat - g) as price drift -- but ONLY the share routed to the goods circuit
M^T does (the floor-bound share lands in the asset circuit and does not move CPI,
the same two-lane logic as the rent and demand-impulse modules).

EMPIRICAL ANCHOR (verified, BEA Survey of Current Business 2024/2026): real GDP
growth updates between the advance (30-day) and third (90-day) estimates averaged
0.52pp over 2000-2024, trending lower. Treated as mean-zero measurement error,
sigma ~ 0.52/0.8 ~ 0.65pp.

ROUTING: a growth error e (pp) -> mis-issuance e% of M2. The share hitting the
transactional circuit is kappa_d (the dividend routing); that share over M^T
(~0.30*M2) is the price drift. Floor-bound mis-issuance (1-kappa_d) lands in the
asset circuit (a tiny extra asset-price wobble, not CPI). One-year passthrough
assumed 100% (conservative; overstates).
"""
MEAN_ABS_REVISION=0.52
SIGMA=MEAN_ABS_REVISION/0.8     # ~0.65pp
MT_OVER_M2=0.30

print("="*72)
print("GROWTH-MEASUREMENT ERROR -> PRICE DRIFT  (routing-aware)")
print("="*72)
print(f"Anchor: BEA advance->third revision avg {MEAN_ABS_REVISION}pp -> sigma ~{SIGMA:.2f}pp")
print()
print("One-year price drift from a typical measurement error, by dividend routing:")
print(f"  (only the kappa_d share hits the goods circuit; floor share is asset-side)")
print(f"    {'mode':>22} {'kappa_d':>8} {'to M^T':>8} {'price drift':>12}")
for mode,kd in [("Mode B (floor-weighted)",0.4),
                ("Mode D (pure dividend)",1.0),
                ("floor-max (kappa_d=0)",0.0)]:
    to_mt=SIGMA*kd
    drift=to_mt/100/MT_OVER_M2
    print(f"    {mode:>22} {kd:>8.1f} {to_mt:>6.2f}% {100*drift:>10.2f}%")
print()
print(f"  Typical (Mode B) one-year drift: ~{SIGMA*0.4/100/MT_OVER_M2*100:.2f}%")
print(f"  Worst case (Mode D) one-year drift: ~{SIGMA*1.0/100/MT_OVER_M2*100:.2f}%")
print()
print("This is the drift from ONE year's error before the engine re-matches as the")
print("estimate is revised. Stage 2 simulates the multi-year accumulation.")

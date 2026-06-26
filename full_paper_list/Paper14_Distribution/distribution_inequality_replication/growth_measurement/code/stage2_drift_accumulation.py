"""
Stage 2 -- multi-year accumulation of measurement-error price drift, swept over
dividend routing (kappa_d), error persistence, and a possible systematic bias.

The key question: revision NOISE (mean-reverting) vs systematic BIAS (persistent
over/under-measurement). Noise washes out as the engine re-matches on revised data;
bias accumulates. We simulate 40 years.

Anchor: sigma ~0.65pp (BEA). Residual-after-revision ~20% of the measurement error
(the third estimate corrects most of the advance error; benchmark residual small).
"""
import statistics, random
SIGMA=0.65; MT_OVER_M2=0.30; RESIDUAL=0.20

def simulate(kappa_d, serial_corr, bias_pp, years=40, trials=4000):
    out=[]
    for _ in range(trials):
        cum=0; prev=0
        for _ in range(years):
            noise = serial_corr*prev + (1-serial_corr)*random.gauss(0,SIGMA)
            prev=noise
            e = noise + bias_pp                      # measurement error = noise + bias
            persistent = RESIDUAL*e                  # what survives revision
            to_mt = persistent*kappa_d               # only dividend share hits goods
            cum += to_mt/100/MT_OVER_M2
        out.append(cum)
    return out

print("="*74)
print("40-YEAR CUMULATIVE PRICE DRIFT FROM MEASUREMENT ERROR (swept)")
print("="*74)
random.seed(1)
print(f"{'scenario':>44} {'median':>8} {'5th-95th':>16}")
scenarios=[
 ("Mode B, noise only (uncorrelated)",0.4,0.0,0.0),
 ("Mode B, noise (serially correlated 0.5)",0.4,0.5,0.0),
 ("Mode D, noise only",1.0,0.0,0.0),
 ("Mode B, +0.2pp systematic BIAS",0.4,0.0,0.2),
 ("Mode D, +0.2pp systematic BIAS",1.0,0.0,0.2),
]
for lbl,kd,sc,bias in scenarios:
    d=simulate(kd,sc,bias); d.sort()
    med=statistics.median(d); lo=d[int(0.05*len(d))]; hi=d[int(0.95*len(d))]
    print(f"{lbl:>44} {100*med:>+7.1f}% {100*lo:>+6.1f}% to {100*hi:>+5.1f}%")
print("-"*74)
print("READING:")
print(" - Noise (mean-reverting revision error) WASHES OUT: 40-yr median drift ~0%,")
print("   bounded spread, because the engine re-matches as estimates are revised and")
print("   most of each year's error is corrected.")
print(" - A systematic measurement BIAS does NOT wash out: a persistent +0.2pp")
print("   over-measurement accumulates to a few percent of price level over 40 years,")
print("   larger in Mode D than Mode B (more of it reaches the goods circuit).")
print(" - HONEST BOTTOM LINE: the matching rule is robust to revision NOISE (the")
print("   thing BEA data actually shows), but exposed to a persistent measurement")
print("   BIAS. That is a data-quality / institutional dependency (keep the growth")
print("   estimate unbiased), not a flaw in the rule. Running floor-weighted (low")
print("   kappa_d) further shrinks the exposure, since less reaches the goods market.")

# Architecture Replication — Paper 1

Reproduces the quantitative claims in **Paper 1, *The Citizens Standard: Architecture*** (SSRN 6702518): the launch-year issuance channels, the Mode A/B/C/D Stable Floors, implied inflation by mode, and the Mode C/D dividends.

The base-Mode floors are **derived**, not stored. `run_all.py` calls the same deterministic engine (`cs_engine.py`) that backs the interactive HTML engine, on the **general-equilibrium realizable return** by Mode (Neo-Solon 2026e §6.7: Mode A/C ~5.4%, Mode B ~4.3% with the 60/40 split), so the repository's tool and its founding paper agree. The Mode Ω Table 8 scenario floors are the one exception: they additionally embed the capture→return feedback solved in the macro model and are used in Figure 6 as published values, not re-derived here.

## Run

```bash
cd code
python3 run_all.py        # prints the derivation + a 15-check regression vs the paper
python3 paper1_figures.py  # regenerates the Paper 1 figures into ../figures/
python3 paper1_extra_figures.py  # Appendix A.2/A.3 figures
python3 paper1_figA3.py    # Appendix A.3 (mid-crisis) by its documented filename
```

`run_all.py` needs only the Python standard library. `paper1_figures.py` needs `numpy` and `matplotlib`.

## What it reproduces

| Output | Paper 1 reference |
|---|---|
| K1 = $2,250 per new citizen (2.5% × GDP/cap) | §5.1, Appendix A |
| Mode B total issuance $447B (2.0% of M2); K2 the residual | §5.2, Table A |
| Mode A K2 = $77B (12.5% × g_r × GDP) | §5.1, Appendix A |
| Mode C KI = $816B (3.65% of M2) → ~$199/citizen/mo | §5.3 |
| Stable Floors A $233K / B $413K / C $230K (GE realizable return) | Tables 5, 6; Figure 3 |
| Mode B return band: $278K (3.30%) / $580K (5.03%) | §5.1; Paper 5 §6.7 |
| Mode C cumulative KI $262K; lifetime $492K | §5.3, Table 5 |
| Implied inflation −1.6% / 0% / +2% / 0% | Table 6, §5 |

All targets are checked automatically; see `all_results.txt` for the captured run (19/19 PASS).

## Two notes on the calibration

**K2 base (12.5% vs 17.5%).** Paper 1 states Mode A's capture as **12.5% of real GDP growth** (`0.125 × g_r × GDP = $77B`). The interactive engine's K2 slider is expressed on the **M2 base** (`capture × g_r × M2`), where the same policy reads as **≈17.5%**, because GDP ≈ 1.38 × M2 at launch. Both yield the same ~$77B issuance, the same −1.6% drift, and the same ~$233K floor. The dollar outcomes are identical; only the denominator differs.

**K1 aggregate.** The Stable Floor is insensitive to how the real-growth-matched budget is split between K1 and K2 in Modes A/B (both deposit into the locked floor), so the floors here are exact regardless of the new-citizen count. The deterministic engine funds K1 on the net 0.5% population-growth basis (~1.7M/yr); Paper 1's §5.2 prose quotes the K1 aggregate on a gross new-citizen basis (~4M/yr → ~$9B), with K2 the residual to the $447B line. Either basis lands on the same total issuance and the same floors.

## Files

```
architecture_replication/
├── README.md
├── all_results.txt              ← captured run_all.py output (19/19 PASS)
├── code/
│   ├── run_all.py               ← derivation + regression vs Paper 1
│   ├── cs_engine.py             ← deterministic engine (port of the HTML engine's simulate())
│   ├── mode_omega.py            ← Mode Ω governor model (simple-engine reference)
│   ├── switch_calc.py           ← GE mode-switch lifetime values (Appendix A.1)
│   ├── paper1_figures.py        ← regenerates the Paper 1 figures into ../figures/
│   ├── paper1_extra_figures.py  ← Appendix A.2 / A.3 figures
│   └── paper1_figA3.py          ← Appendix A.3 (mid-crisis), documented filename
└── figures/                     ← written by paper1_figures.py
    ├── modes_vs_current.png          ← Paper 1, Figure 1
    ├── purchasing_power.png          ← Paper 1, Figure 2
    ├── stable_floor_accumulation.png ← Paper 1, Figure 3
    ├── mode_omega_inflation.png      ← Paper 1, Figure 7a
    ├── mode_omega_deviation.png      ← Paper 1, Figure 7b
    ├── mode_omega_scenarios.png      ← Paper 1, Figure 6 (Table 8)
    └── mode_transitions.png          ← Paper 1, Appendix A.1
```

Canonical macro inputs (GDP, M2, population) are sourced and dated in `../empirical_replication/code/authoritative_data.py` (FRED M2SL, BEA GDPA, Census Vintage 2025).

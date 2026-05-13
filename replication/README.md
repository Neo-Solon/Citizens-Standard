# Citizens Standard Counterfactual — SSRN/Mendeley Submission Guide

This document explains which files go where when uploading to SSRN, including the Mendeley Data supplementary materials section.

## What is SSRN's Mendeley section?

SSRN (Social Science Research Network) is owned by Elsevier, and SSRN paper submissions can include a "Supplementary Files" or "Data" section that connects to Mendeley Data (also Elsevier-owned). Mendeley Data hosts the **replication materials** that let other researchers re-run your analysis, while the SSRN paper page hosts the **paper itself**.

Conceptually:
- **SSRN main paper page** = the PDF (or DOCX) of the working paper
- **SSRN Supplementary Files / Mendeley Data link** = the replication bundle (code, data, figures)

## Upload plan

### To the main SSRN paper page

Upload **one file** as the primary paper:

| File | Role | Recommendation |
|---|---|---|
| `Citizens_Standard_Counterfactual_v1.pdf` | Primary paper PDF | ✅ Upload as the main document |
| `Citizens_Standard_Counterfactual_v1.docx` | Editable Word version | Optional — SSRN accepts both; PDF is standard |

SSRN displays one document as the canonical paper view. The PDF renders consistently across all browsers and is the convention for working papers. Use the DOCX only if SSRN asks for an editable version during review.

### To SSRN's Supplementary Files / Mendeley Data

Bundle the **replication materials** as a single ZIP archive (or upload individually if SSRN allows). The Mendeley/Supplementary section is the right home for everything a researcher needs to re-run your analysis:

| File | What it is | Why include |
|---|---|---|
| `authoritative_data.py` | All historical data (1928–2025) in Python dicts | Source of truth for every number |
| `deterministic_engine.py` | Builds dataset and computes cohorts (Sections 3–5) | Implements the K1/K2 formulas |
| `mc_engine.py` | Monte Carlo bootstrap engine (Section 6) | Implements the bootstrap analysis |
| `mc_plots.py` | Generates Figures M1–M4 | Reproduces the paper's figures |
| `run_all_tables.py` | Runs all paper tables in one shot | Produces `all_results.txt` for verification |
| `build_csv.py` | Exports the dataset as CSV | Convenience for non-Python users |
| `compare_to_paper.py` | Side-by-side check of paper claims vs. reconstruction | Audit trail |
| `citizens_standard_historical_data_1960_2025_v2.csv` | Main paper dataset (66 rows) | Human-readable data |
| `citizens_standard_historical_data_1928_2025_full.csv` | Extended dataset for MC (97 rows) | Human-readable data |
| `figure_M1_distributions.png` | MC distribution plot | Paper figure |
| `figure_M2_percentile_bands.png` | MC percentile bands plot | Paper figure |
| `figure_M3_p_below_median.png` | P(<median) bar chart | Paper figure |
| `figure_M4_p50_p5_sensitivity.png` | Configuration sensitivity | Paper figure |
| `all_results.txt` | Full text output of every table in the paper | One-glance verification |
| `AUDIT.md` | Data audit summary with primary-source verification | Reviewer trust |
| `README.md` | This file | Submission guide |

## Recommended bundle structure

```
citizens-standard-replication.zip
├── README.md                    (or rename this file)
├── AUDIT.md
├── all_results.txt              ← one-glance verification of every paper number
├── data/
│   ├── citizens_standard_historical_data_1960_2025_v2.csv
│   └── citizens_standard_historical_data_1928_2025_full.csv
├── code/
│   ├── authoritative_data.py
│   ├── deterministic_engine.py
│   ├── mc_engine.py
│   ├── mc_plots.py
│   ├── run_all_tables.py
│   ├── build_csv.py
│   └── compare_to_paper.py
└── figures/
    ├── figure_M1_distributions.png
    ├── figure_M2_percentile_bands.png
    ├── figure_M3_p_below_median.png
    └── figure_M4_p50_p5_sensitivity.png
```

If SSRN doesn't accept directories inside a single ZIP, flatten everything into one folder.

## Running the replication

Requirements: Python 3.8+ with numpy and matplotlib.

```bash
# Reproduce all paper tables
python3 run_all_tables.py > all_results.txt

# Regenerate figures
python3 mc_plots.py

# Export the dataset as CSV
python3 build_csv.py
```

Runtime: ~1 second for the full 16-configuration Monte Carlo grid (4 cohorts × 2 universes × 2 methods × 10,000 paths) on a modern single core. Random seeds are fixed for reproducibility.

## What NOT to upload

- Working drafts or scratch files
- Intermediate working files (`build_paper_v1.js`, etc.)
- Personal notes or scratch files
- The HTML render or any browser caches

## Suggested SSRN abstract field

The paper's existing abstract already runs about 400 words and includes the headline ranges (2.21×–3.21× deterministic, 1.96×–4.52× bootstrap P50). It is suitable for the SSRN abstract field as-is — copy from the PDF or DOCX directly.

## Suggested SSRN keywords

- Monetary policy
- Retirement security
- Counterfactual analysis
- Monte Carlo simulation
- Survey of Consumer Finances
- Sequence-of-returns risk
- Citizens Standard
- Universal basic capital

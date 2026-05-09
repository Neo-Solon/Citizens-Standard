# Replication Materials — Citizens Standard (Paper 2)

This folder contains the empirical replication materials for the working paper:

> *Citizens Standard: An Empirical Replication and Counterfactual Benchmark, 1960–2025*

For the architectural framework paper and the Interactive Engine, see the top-level README of this repository.

## Contents

- `replication.py` — replication script for the empirical results in Paper 2. Pure Python standard library; no external dependencies.
- `requirements.txt` — dependency manifest (intentionally empty; documents that the script is stdlib-only).
- `MENDELEY_DEPOSIT.md` — status note on the Mendeley Data deposit and remaining alignment work.
- `README.md` — this file.

## How to run

The script requires Python 3.8 or newer. No installation step is needed.

```bash
python replication.py
```

The script reproduces the headline empirical results reported in the paper using a historical dataset embedded in the script itself (1960–2025). Output is printed to standard output.

## Data sources

The historical dataset embedded in `replication.py` is compiled from publicly available macroeconomic series. Source-by-source documentation is included as comments within the script.

## Status note on calibration alignment

The script reproduces the empirical analysis as described in the paper. A full line-by-line reconciliation between the script's calibration constants and the values reported in the paper text is planned future work. Any discrepancies discovered during that reconciliation will be addressed in a revision and noted in `MENDELEY_DEPOSIT.md`.

This is flagged here in the interest of transparency rather than concealment: the script runs and produces results consistent with the paper's findings, but the formal alignment audit is a deferred task.

## Mendeley Data deposit

A frozen snapshot of these replication materials is intended for deposit on Mendeley Data, where it will receive a DOI tied to the SSRN working paper. See `MENDELEY_DEPOSIT.md` for the current status of that deposit.

The latest version of the replication code is maintained here on GitHub. The Mendeley deposit, once finalized, will be the citable frozen snapshot.

## License

See the repository's top-level LICENSE file.

## Citation

If you use these materials, please cite the SSRN working paper. A BibTeX entry will be added once the paper has a stable SSRN ID assigned.
*Methodology section, v0.1. Subject to revision before publication based on data availability and any methodological issues that surface during the empirical reconstruction. The author commits to documenting any methodological revisions with explicit version-control notation in the final paper.*

# Replication — one command, verify everything

```bash
python run_all.py
```

Runs **every** replication package against the bundled data snapshot and prints a pass/fail table.
No API key, no data hunting, works offline.

```
================================================================
  CITIZENS STANDARD - REPLICATION RUN
  data: bundled snapshot
================================================================

PACKAGE                       RESULT       SEC  SUMMARY
----------------------------------------------------------------
paper01_architecture          PASS        3.1   163 published values reproduced
paper03_transition            PASS        2.4   9 published values reproduced
paper05_macro                 PASS       12.6   976 published values reproduced
paper06_banking               PASS       18.9   182 published values reproduced
paper07_interoperability      PASS       21.7   375 published values reproduced
paper08_structural_buyer      PASS        4.2   28 published values reproduced
paper10_empirical             PASS        9.8   413 published values reproduced
paper10_empirical_validation  PASS        7.2   74 published values reproduced
paper12_crisis                PASS        3.0   32 published values reproduced
paper13_comparative           PASS        2.2   13 published values reproduced
paper14_distribution          PASS        6.4   56 published values reproduced
two_circuit                   PASS        1.2   MA gap -5.3%, corr 0.684, JP broad>narrow
----------------------------------------------------------------
  12/12 packages passed
================================================================
```

Other commands:
```bash
python run_all.py --list          # list packages
python run_all.py --only NAME     # run one package
python run_all.py --refresh       # re-pull refreshable series from FRED (needs FRED_API_KEY)
```

---

## What a PASS actually means

This is the part worth being precise about, because "the tests pass" is easy to fake.

Every paper package ships a **golden artifact** — `all_results.txt` (captured output) or
`results/*.json` — containing the numbers the paper itself cites. To verify a package, the harness:

1. copies the pristine package into a scratch directory (nothing on disk is mutated),
2. runs that package's **own entry point** there, offline, exactly as a reviewer would,
3. extracts every number from what the code produces *today*,
4. checks that **every number the paper published still appears**, to a relative tolerance of 1e-6.

So a PASS means: *the code still reproduces the published numbers.* The expected values are the
author's published record, not something regenerated at verification time — which is what makes
this a real check rather than a self-fulfilling one.

Extra output in a fresh run is fine. A **missing or changed published value is a failure.**
Wall-clock timing lines are excluded (a faster machine is not a failed reproduction).

## Resolved: the paper08 discrepancy (2026-07-12)

The harness's first full run flagged `paper08_structural_buyer`: its golden `all_results.txt`
recorded

> `Appendix A.6 verification PASSED: psi* = c*dur (both models); base=0.24, high=0.45`

while `verify_psi_plateau.py`, run today, produced `c*dur = 0.158`. Exactly one value differed —
the other 27 in the package reproduced to machine precision.

**Adjudicated against Paper 8 itself, not against either artifact.** The paper says:

| Paper 8 (§6.3, Appendix B.3, Figure 2) | Script today | Old golden |
|---|---|---|
| zero-growth c·dur at the cohort-realistic dur ≈ 40 yr: **≈ 0.16** | **0.158** ✓ | 0.24 ✗ |
| realized ψ* under 2% growth: **≈ 0.10** (band 0.09–0.11) | **0.098** ✓ | — |
| active float 1 − ψ*: **≈ 0.90** | **0.902** ✓ | — |
| high-deposit (c = 0.015): **0.45** | — | 0.45 ✓ |

`0.24` corresponds to **nothing** in Paper 8 — not the dur=30 base (0.12), not dur=40 (0.16), not
maximum-absorption (0.20), not high-deposit (0.45). The code is correct and agrees with the
published paper; the golden artifact was captured from an older revision of the script and never
refreshed.

**Resolution:** `all_results.txt` regenerated from the current code. The other 27 values are
byte-identical, so the regeneration is confined to the stale line. `run_all.py` now reports
**12/12**.

This is what the harness is for. The stale value had been sitting in the published replication
package, and nothing else would have caught it.

## Layout

```
run_all.py            the one-command driver; discovers packages/*/run.py
paper_pkg.py          shared verifier used by every paper adapter (copy → run → compare)
data/                 bundled snapshot (FRED/OECD series) + SOURCES.md
packages/
  two_circuit/        native package: run.py with inline checks
  paperNN_<name>/
    run.py            adapter: runs pkg/ and compares against its golden artifact
    pkg/              the full standalone replication package, unmodified
```

Each `pkg/` remains a complete, independently runnable package — an academic can `cd` into any of
them and run it directly, exactly as before. The adapter adds verification without changing them.

## Adding a package

Create `packages/<name>/run.py` exposing `run(data_dir, refresh) -> {"passed", "summary", "detail"}`.
For a paper package, four lines suffice:

```python
from paper_pkg import verify
def run(data_dir=None, refresh=False):
    return verify(PKG_DIR, "run_all.py", [("stdout", "all_results.txt")])
```

## Scope — what is deliberately NOT here

`fx_exploratory_record/` and `two_circuit_supplementary_record/` are **not** in this harness, by
design. Both are exploratory/supplementary records, and the FX record's headline result is a
documented **null** (`FX_lineA_FALSIFICATION.json`). Folding exploratory or falsified work into the
bundle that verifies published claims would miscategorise a null as support. They stay separate and
are run on their own; the two-circuit *confirmatory* subset is included here as `two_circuit`.

---

## Visual report

```bash
python run_all.py --report
```

Writes **`report/REPORT.html`** — a single self-contained page with:

- the verdict and the pass/fail table,
- for each package: its summary, and **exactly which published values failed to reproduce** (no
  hand-waving — the failing numbers are printed),
- **every figure the packages regenerate**, inline (57 across the 11 packages).

The figures are produced *by that run*, not copied from the repo, so the report cannot go stale:
if the code stops reproducing a figure, the report shows what the code actually produces now.

Without `--report` the run is text-only and no figures are written.

**Runtime:** the full suite takes several minutes (the banking package alone runs a 10,000-path
Monte Carlo). `--only <package>` runs a single one in seconds.

Note that each package still writes its own figures into its own `figures/` directory when you run
it directly — the harness runs packages in a scratch copy so it never mutates the repo, and
`--report` is how you get those figures back.


---

## Verify in the browser (no install)

`methodology.html` runs the packages **live in the page**, with Pyodide in a **Web Worker**
(`replication/verify_worker.js`). CPython-in-WASM executes synchronously: on the main thread, Paper 5's
~40-second run freezes the tab hard enough that the browser offers to kill the page. Off-thread, the
page stays responsive and the run reports progress. The worker must be same-origin, so it sits beside
the manifest.

It runs **9 of the 12 packages by default** — real CPython compiled to
WebAssembly (Pyodide), executing the packages' own scripts, checking every number against the
published artifact, and rendering the figures the code draws. Nothing is precomputed.

`replication/web_manifest.json` drives it; regenerate with `python build_web_manifest.py` after
touching any package. It records, per package, the ordered `[working_dir, script]` steps, the golden
artifact, the pip deps, and every file the browser must fetch (194 files, ~900 KB).

**Why a manifest instead of just calling `run_all.py`?** Pyodide has no `subprocess`, and every
package's own `run_all.py` shells out to its scripts. The manifest records the script sequence so the
browser can exec them in-process. The scripts themselves are unchanged — only the drivers used
`subprocess`, so the computation is identical.

Four things that differ in-process and are handled explicitly (each caused a wrong answer, not a
crash, when it wasn't):

1. **`sys.argv` is inherited.** Banking's `run_analysis.py` branches on `argv[1]`; a subprocess gets a
   clean argv, an in-process exec gets the caller's. Reset per script.
2. **`SystemExit` propagates.** One script calls `sys.exit()`; without a per-step catch it silently
   aborts every later script.
3. **`sys.modules` must be purged selectively** — package-local modules only. Evicting
   `matplotlib.pyplot` leaves matplotlib half-initialised and throws unrelated errors later.
4. **matplotlib is process-global.** Open figures and mutated rcParams leak between packages;
   reset between runs.

**All 11 paper packages now run in the browser.** Two are flagged **heavy** — they work, but they
cost a large download, so the page asks before starting one and `Run all` skips them:

- `empirical_validation_replication` (~25 MB) — statsmodels pulls scipy.
- `distribution_inequality_replication` (~30 MB) — the 22 MB raw SCF 2022 microdata, plus pandas.

Two further things this shook out, both real:

**A cross-package data dependency.** `distribution/procyclicality/code/` reads
`../../../empirical_replication/data/citizens_standard_historical_data_1960_2025_v2.csv` — it reaches
into a *sibling* package. Packages are staged side by side in the browser FS so the relative path
resolves, but the file must be fetched too; the manifest records it under `siblings`.

**The distribution package requires Python 3.12+.** Four supplementary scripts use PEP 701 f-strings
(backslashes inside f-string expressions). On Python 3.10/3.11 they raise `SyntaxError` and are
reported as `[FAIL]` by its own `run_all.py` — while the package still "passes" the harness, because
the golden artifact only covers the core channels, not the supplementary models. Pyodide and CI both
run 3.12, so both are fine. **If you run it locally on an older Python you will see four failures
that are not real.** Worth pinning a minimum version in the package's README.

`distribution_inequality_replication` produces no figures — that is correct, it has none.

## CI

`.github/workflows/replication.yml` runs the **full** suite (all 12) on every push and weekly, and
uploads `report/` as an artifact. `run_all.py` exits non-zero if any package fails to reproduce, so a
regression breaks the build. The weekly cron catches rot from dependency drift, not just from edits.


### A bug worth recording

The browser verifier's first live run reported 7/9. Two packages "failed" on values like `-1960`
and `-2024`.

Cause: `pkg.golden.slice(-4)` returns `"json"` — **four** characters, no dot — so the test
`slice(-4) !== '.json'` was always true, and every JSON-golden package silently took the **text**
comparison path. Text-matching a JSON artifact reads the hyphen in a date range like `1960-2024` as
a minus sign and invents a value of `-2024` that no code ever produced.

It failed loudly on two packages, but it also made `crisis_behaviour` report "54 values reproduced"
when the real count is 32 — a **passing** result computed the wrong way. That is the dangerous half:
a green tick from a broken comparison. Fixed with `/\.json$/`, and all five JSON-golden packages now
match the offline harness exactly (9 / 74 / 32 / 13 / 56).

Moral: the offline harness compares in Python, the browser in JS. Two implementations of one rule
will drift. Both are now checked against each other on every package.

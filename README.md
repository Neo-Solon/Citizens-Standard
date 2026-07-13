# The Citizens Standard

**A constitutional monetary architecture with mode-selectable inflation regimes.**

Fourteen papers, an interactive engine, and a replication suite where **every quantitative claim
in the papers is reproduced by code you can run yourself** — offline, in CI, or in your browser
without installing anything.

**→ [citizensstandard.org](https://citizensstandard.org)**

---

## What it is

A rules-based monetary framework that replaces central-bank discretion with four constitutionally
bounded issuance channels. Every dollar of new money is distributed equally to all citizens, split
between locked citizen equity (the **Stable Floor**) and spendable dividends.

| Channel | What it does |
|---|---|
| **K1** | Citizenship endowment — 2.5% of GDP per capita, issued once per new citizen |
| **K2** | Growth dividend — issued annually against real growth, into locked floors |
| **K3** | Citizen dividend — the κ_d share of the same budget, paid as spendable cash |
| **KI** | Inflation-gap channel — the **only** channel that moves the price level |

K3 is carved *from* the K2 budget, not added to it: raising the dividend lowers the floor by the
same dollars, and total issuance is unchanged. That is what makes the split price-neutral.

## The Modes

A single architecture hosts several constitutionally selectable regimes. Mode selection is a Tier-2
choice requiring a supermajority and a deliberation period — it does not rotate automatically.

| Mode | | Paper 1 |
|---|---|---|
| **A** | Mild deflation — holdings gain purchasing power | |
| **B** | The full-rate 60/40 split (the reference configuration) | |
| **C** | Modest ~2% inflation, KI active | |
| **D** | Pure dividend — builds no floor | |
| **Ω** | **Price stability**, solved per economy | §9 |
| **Λ** | **Adaptive** — demographic and productivity governors | §10 |
| **0** | Zero-issuance — the hard-money corner | |

On the general-equilibrium **realizable** basis (Macro Model §6.7 — the attenuated marginal product
of the capital stock the deposit itself deepens, *not* an exogenous market return), the per-citizen
Stable Floor at 65 lands at roughly **$233K (Mode A)**, **$413K (Mode B)**, **$230K (Mode C)**, at a
4.26% central realizable return within a 3.30–5.03% band.

These are **not** multiples of what people retire with today. On the realizable basis the floor
lands near the median actual US retirement outcome. The structural claim is not that it is bigger —
it is that **every** citizen receives a compounding equity stake where today they receive nothing.

## Verify it yourself

Every number in the papers is backed by code. Three ways to check, in increasing order of effort:

**1. In your browser, no install.** [Papers & data](https://citizensstandard.org/papers.html) and
[Methodology](https://citizensstandard.org/methodology.html) run the replication packages live via
Pyodide (CPython compiled to WebAssembly). Pick a paper, press Run, watch it reproduce.

**2. Offline, one command.**

```bash
cd replication
python run_all.py            # all 12 packages, pass/fail table
python run_all.py --report   # + an HTML report with every figure
```

Exits non-zero if *any* package fails to reproduce.

**3. CI.** `.github/workflows/replication.yml` runs the full suite on every push and weekly — so
dependency drift gets caught, not just our own edits.

## Layout

```
papers/                     14 papers (PDF + DOCX)
replication/                12 packages, one per paper + supplementary
  run_all.py                the one-push verifier
  paper_pkg.py              copy → run → compare against the published golden
  web_manifest.json         drives the in-browser verifier
*.html                      the 8-page site
fx_exploratory_record/      exploratory, unverified
two_circuit_supplementary_record/
```

Each package ships a **golden artifact** — the exact figures the paper cites. Verification is
containment, not eyeballing: the runner's output must contain every published value.

## Known gaps, stated plainly

- **Paper 10 (Empirical Validation)** *used to* be un-runnable in the browser — it needs
  `statsmodels`, which has C extensions and is not in the Pyodide distribution. Resolved:
  `src/hac_ols.py` is a pure-numpy drop-in for the only two things the package used from
  statsmodels (OLS, and OLS with Newey–West HAC errors). It reproduces statsmodels to machine
  precision, and the package's output is **byte-identical** with and without it. All 12 packages
  now run in the browser.
- **Papers 4 and 11** are argument, not computation — nothing to replicate. **Paper 9** has no
  package of its own, but its numbers are computed elsewhere: its technical appendix maps every
  reported quantity to the script that produces it.
- **The liquidation flow `L_t`** — defined in Macro §3.3 and never given a number in any paper — is
  now computed in `replication/liquidation_flow_replication`. It finds the circulating-pool ceiling
  breached from ~2048 under a fixed κ_d. **This postdates the papers and is not yet in them.** It is
  flagged as supplementary and awaits adversarial review.

## Citation

The Citizens Standard is a **fourteen-paper series**, not a single paper. The letters are the ones
the papers use to cite each other.

**Published on SSRN:**

| | Paper | SSRN |
|---|---|---|
| **2026a** | One Model, Many Systems — A Constitutional Monetary Architecture | [6702518](https://papers.ssrn.com/sol3/papers.cfm?abstract_id=6702518) |
| **2026b** | A Historical Counterfactual, 1960–2055 | [6735078](https://papers.ssrn.com/sol3/papers.cfm?abstract_id=6735078) |
| **2026c** | Transition Architecture and Migration Mechanics | [6810741](https://papers.ssrn.com/sol3/papers.cfm?abstract_id=6810741) |
| **2026e** | A Macroeconomic Model of a Two-Circuit Monetary System | [6939418](https://papers.ssrn.com/sol3/papers.cfm?abstract_id=6939418) |
| **2026f** | Full-Reserve Banking and the Dual-Circuit System | [6939498](https://papers.ssrn.com/sol3/papers.cfm?abstract_id=6939498) |
| **2026g** | External Interoperability and the Common Anchor | [6939600](https://papers.ssrn.com/sol3/papers.cfm?abstract_id=6939600) |
| **2026h** | The Structural Buyer — Asset-Market Dynamics, Price Discovery, and Universal Ownership | [6945320](https://papers.ssrn.com/sol3/papers.cfm?abstract_id=6945320) |

**Submitted, under review:**

| | Paper | SSRN |
|---|---|---|
| **2026d** | Constitutional Vulnerability of a Rules-Based Monetary Statute | [7115018](https://papers.ssrn.com/sol3/papers.cfm?abstract_id=7115018) |
| **2026i** | Bounded Citizen Ownership and the Transactional-Money Locus | [7114938](https://papers.ssrn.com/sol3/papers.cfm?abstract_id=7114938) |

**Submitted, awaiting release:** Empirical Validation (2026j), Governance (2026k), Crisis Behaviour
(2026l), Comparative Analysis (2026m), Distribution & Inequality (2026n).

All fourteen — published or not — are in [`papers/`](papers/) as PDF and DOCX, on
[citizensstandard.org](https://citizensstandard.org/papers.html), and every quantitative claim in
them is reproduced by the code in [`replication/`](replication/).

**To cite the architecture (the entry point):**

> Neo-Solon (2026a). *The Citizens Standard: One Model, Many Systems — A Constitutional Monetary
> Architecture.* Working Paper. SSRN: <https://ssrn.com/abstract=6702518>

**To cite the series:**

> Neo-Solon (2026). *The Citizens Standard.* Fourteen-paper series with full replication code.
> <https://github.com/Neo-Solon/Citizens-Standard>

## Licence

Open source. Free to share, embed, modify, adapt. Attribution appreciated, not required.

*If you find an error in the model, want to add a comparator, or can break one of the results —
open an issue. The replication suite exists precisely so that you can.*

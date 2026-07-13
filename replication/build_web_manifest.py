#!/usr/bin/env python3
"""
build_web_manifest.py — generates web_manifest.json, which drives the in-browser verifier on
methodology.html.

The browser runs CPython via Pyodide (WASM). Two constraints follow, and the manifest exists to
satisfy them:

  1. **No subprocess.** Each package's own run_all.py shells out to its scripts, which Pyodide
     cannot do. So the manifest records the ORDERED SCRIPT LIST directly, and the browser execs
     each script in-process. The scripts themselves are pure Python — only the drivers used
     subprocess — so nothing about the computation changes.
  2. **No filesystem.** Every file a package needs must be fetched over HTTP and written into
     Pyodide's virtual FS first. So the manifest lists every file, with its path relative to
     the repo root.

Regenerate after touching any package:  python build_web_manifest.py
"""
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parent

# pkg -> (cwd relative to package root, ordered scripts, golden artifact, pypi deps)
# pkg -> (ordered [working_dir, script] pairs, golden artifact, pypi deps)
# The working dir is per-script, matching exactly what each package's own run_all.py does with
# subprocess cwd= / os.chdir(). Get this wrong and scripts fail on relative data paths or imports.
SPEC = {
    # run_all.py is the analysis itself; the figure scripts are separate and its runner never
    # calls them. Added here so the browser actually draws the paper's figures.
    "architecture_replication":     ([["code", "run_all.py"], ["code", "paper1_figures.py"],
                                      ["code", "paper1_figA3.py"], ["code", "paper1_extra_figures.py"]],
                                     "all_results.txt", ["numpy", "matplotlib"]),
    "structural_buyer_replication": ([["code", s] for s in
                                      ["verify_prop1_premium.py", "verify_prop2_investment.py",
                                       "verify_prop3_leak.py", "verify_prop7_mirror_voting.py",
                                       "verify_psi_plateau.py", "verify_all.py",
                                       "make_figures.py"]],
                                     "all_results.txt", ["numpy", "matplotlib"]),
    "crisis_behaviour_replication": ([[".", "src/run_stress.py"], [".", "src/make_figure.py"]],
                                     "results/stress_results.json", ["matplotlib"]),
    "comparative_replication":      ([["src", "compare.py"], ["src", "make_figures.py"]],
                                     "results/comparison_results.json", ["matplotlib"]),
    # --- HEAVY: runnable, but they cost a large download. Flagged, never auto-run. ---
    # run_all.py mixes imports with subprocess; web_run.py is the in-process equivalent.
    # NOTE: no leading underscore — GitHub Pages runs Jekyll, which refuses to publish "_*" files.
    # Paper 5 supplementary: the liquidation flow L_t, which Macro §3.3 defines and no paper
    # ever gives a number. Depends only on numpy (SSA life table is a bundled CSV).
    "liquidation_flow_replication": ([["code", "run_all.py"]],
                                     "all_results.txt", ["numpy"]),
    "distribution_inequality_replication": ([[".", "web_run.py"]],
                                     "results/inequality_results.json",
                                     ["numpy", "pandas", "matplotlib"]),
    "transition_replication":       ([["code", "run_all_appendix.py"],
                                      ["cs_debt_band/code", "cs_band_verify_final.py"],
                                      ["code", "phase_milestones.py"], ["code", "make_figures.py"]],
                                     "cs_debt_band/dsa_locked.json", ["numpy", "matplotlib"]),
    # banking's golden report also covers the nested innovation counterfactual, which its
    # run_all.py shells out to — so the browser must run that script directly too.
    "banking_replication":          ([["code", "test_propositions.py"], ["code", "run_analysis.py"],
                                      ["innovation_counterfactual", "src/run_innovation_cf.py"],
                                      ["code", "make_figures.py"]],
                                     "all_results.txt", ["numpy", "matplotlib"]),
    "empirical_replication":        ([["code", s] for s in
                                      ["run_all_tables.py", "run_ge_results.py", "compare_to_paper.py",
                                       "make_fig_M5.py"]],
                                     "all_results.txt", ["numpy", "matplotlib"]),
    "interoperability_replication": ([["code", s] for s in
                                      ["cs_engine.py", "equa_model_v3.py", "equa_redteam.py",
                                       "equa_stress.py", "cs_channel_test.py",
                                       "cs_independence_redteam.py", "cs_contraction_compare.py",
                                       "cs_sterilization_test.py", "behavioral_idle_capital.py",
                                       "behavioral_calibrated.py", "fig_paper7.py"]],
                                     "outputs/", ["numpy", "matplotlib"]),
    # macro's golden report covers ALL 20 scripts its run_all.py drives, figure scripts included
    # (several of them print values that appear in all_results.txt).
    "macro_replication":            ([["code", s] for s in
                                      ["verify_proposition_3.py", "verify_proposition_3prime.py",
                                       "verify_proposition_4.py", "verify_proposition_5.py",
                                       "verify_proposition_6.py", "verify_proposition_7.py",
                                       "verify_proposition_8.py", "verify_proposition_9.py",
                                       "verify_realizable_return.py", "spillover_estimate.py",
                                       "recompute_illustrations.py", "make_figure.py",
                                       "make_determinacy_figure.py", "make_labor_figure.py",
                                       "make_delay_figure.py", "make_irf_figure.py",
                                       "dynamic_model.py", "make_forward_figure.py",
                                       "make_welfare_figure.py", "make_banking_figure.py"]],
                                     "all_results.txt", ["numpy", "matplotlib", "sympy"]),
}

# No package is treated as "heavy" any more. Paper 14 does pull the 22 MB raw SCF microdata, but
# labelling that up front reads as a warning not to bother — and the fetch counter and elapsed clock
# already show it working. Let the progress do the talking; don't editorialise the cost.
HEAVY = {}

# Some scripts reach into a SIBLING package's data (distribution/procyclicality reads
# empirical_replication's historical CSV via ../../../). Packages are staged side by side in the
# browser FS, so the relative path resolves — but the file has to be fetched too.
SIBLING_FILES = {
    "distribution_inequality_replication": [
        "empirical_replication/data/citizens_standard_historical_data_1960_2025_v2.csv",
    ],
}
EXCLUDED = {
    # VERIFIED against the Pyodide v0.26.4 lock file: it ships pandas, scipy and sympy, but NOT
    # statsmodels — and statsmodels has C extensions, so micropip cannot install it at runtime.
    # There is no way to run this package in the browser today.
    "empirical_validation_replication":
        "needs statsmodels, which is not in the Pyodide distribution and cannot be installed at "
        "runtime (it has C extensions). Runs in the offline suite and in CI.",
}

TITLES = {
    "architecture_replication": "Paper 1 — Architecture",
    "structural_buyer_replication": "Paper 8 — The Structural Buyer",
    "crisis_behaviour_replication": "Paper 12 — Crisis Behaviour",
    "comparative_replication": "Paper 13 — Comparative Analysis",
    "transition_replication": "Paper 3 — Transition",
    "banking_replication": "Paper 6 — Full-Reserve Banking",
    "empirical_replication": "Paper 2 — Historical Counterfactual",
    "interoperability_replication": "Paper 7 — External Interoperability",
    "macro_replication": "Paper 5 — Macroeconomic Model",
    "distribution_inequality_replication": "Paper 14 — Distribution & Inequality",
    "liquidation_flow_replication": "Paper 5 — The Liquidation Flow L\u209c (supplementary)",
    "empirical_validation_replication": "Paper 10 — Empirical Validation",
}

# Paper number per package — drives both the manifest order and the dropdown on methodology.html.
PAPER_NO = {
    "architecture_replication": 1,
    "transition_replication": 3,
    "macro_replication": 5,
    "liquidation_flow_replication": 5,
    "banking_replication": 6,
    "interoperability_replication": 7,
    "structural_buyer_replication": 8,
    "empirical_replication": 2,
    "empirical_validation_replication": 10,
    "crisis_behaviour_replication": 12,
    "comparative_replication": 13,
    "distribution_inequality_replication": 14,
}

# Largest file the browser will fetch. Paper 14's raw SCF 2022 microdata is 22 MB and is REQUIRED —
# the package cannot run without it. Nothing else in the tree comes close.
MAX_FETCH_BYTES = 25_000_000

SKIP_DIRS = {"figures", "results", "outputs", "report"}          # regenerated by the run
JUNK_DIRS = {"__pycache__"}


def golden_files(pkg, golden):
    """The published artifact(s) we compare against. These live in results/ or outputs/, which are
    excluded from the input set (the run REGENERATES them) — so they must be fetched separately."""
    base = ROOT / pkg
    if golden.endswith("/"):
        return sorted(p.relative_to(base).as_posix() for p in (base / golden).iterdir() if p.is_file())
    return [golden]


def out_dirs(pkg):
    """Directories the scripts write into. Pyodide's FS starts empty — without these, a script
    doing open('results/x.json','w') fails with ENOENT."""
    base = ROOT / pkg
    dirs = set()
    for d in SKIP_DIRS:
        for p in base.rglob(d):
            if p.is_dir():
                dirs.add(p.relative_to(base).as_posix())
    dirs = {d for d in dirs if "__pycache__" not in d}
    return sorted(dirs)


def files_for(pkg):
    """Every file the package needs in the browser's virtual FS, minus regenerable output."""
    base = ROOT / pkg
    out = []
    for p in sorted(base.rglob("*")):
        if not p.is_file():
            continue
        rel = p.relative_to(base)
        if any(part in SKIP_DIRS | JUNK_DIRS for part in rel.parts[:-1]):
            continue           # figures/results/outputs are REGENERATED by the run
        if p.suffix in {".png", ".pdf", ".docx"}:
            continue
        if p.name.startswith("_harness"):
            continue           # offline-harness helper; the browser runs the scripts directly
        # A single global cap. This used to be "25 MB if the package is HEAVY, else 3 MB" — so when
        # HEAVY was emptied, the exemption vanished with it and the 22 MB SCF microdata silently
        # dropped out of the fetch list. A cosmetic change quietly broke the data.
        if p.stat().st_size > MAX_FETCH_BYTES:
            continue
        out.append(rel.as_posix())
    return out


def main():
    pkgs = []
    for pkg in sorted(SPEC, key=lambda k: (PAPER_NO[k], k)):
        steps, golden, deps = SPEC[pkg]
        files = files_for(pkg)
        gfiles = golden_files(pkg, golden)
        rec_heavy = HEAVY.get(pkg)
        pkgs.append({
            "id": pkg,
            "paper": PAPER_NO[pkg],
            "title": TITLES[pkg],
            "heavy": bool(rec_heavy),
            "heavyMB": rec_heavy["mb"] if rec_heavy else 0,
            "heavyWhy": rec_heavy["why"] if rec_heavy else "",
            "siblings": SIBLING_FILES.get(pkg, []),
            "steps": steps,
            "golden": golden,
            "goldenFiles": gfiles,
            "mkdirs": out_dirs(pkg),
            "deps": deps,
            "files": files,
            "bytes": sum((ROOT / pkg / f).stat().st_size for f in files),
        })
    manifest = {
        "note": "Drives the in-browser verifier on methodology.html. Regenerate with build_web_manifest.py.",
        "noCode": [
            {"paper": 4,  "title": "Paper 4 — Statutory"},
            {"paper": 9,  "title": "Paper 9 — Issuance Engine"},
            {"paper": 11, "title": "Paper 11 — Governance"},
        ],
        "base": "replication",
        "packages": pkgs,
        "excluded": [{"id": k, "title": TITLES[k], "reason": v}
                     for k, v in sorted(EXCLUDED.items(), key=lambda kv: PAPER_NO[kv[0]])],
        "pythonNote": "Four supplementary scripts in the distribution package use PEP 701 f-strings "
                      "and need Python 3.12+. Pyodide and CI both run 3.12; older local Pythons "
                      "will report SyntaxError on those four.",
    }
    (ROOT / "web_manifest.json").write_text(json.dumps(manifest, indent=1))
    tot = sum(p["bytes"] for p in pkgs)
    print(f"web_manifest.json: {len(pkgs)} browser-runnable packages, "
          f"{sum(len(p['files']) for p in pkgs)} files, {tot/1024:.0f} KB total")
    for p in pkgs:
        print(f"  {p['id']:36s} {len(p['files']):3d} files  {p['bytes']/1024:6.0f} KB  {','.join(p['deps'])}")
    print(f"  excluded: {', '.join(EXCLUDED)}")


if __name__ == "__main__":
    main()

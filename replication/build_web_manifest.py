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
    "architecture_replication":     ([["code", "run_all.py"]],
                                     "all_results.txt", ["numpy", "matplotlib"]),
    "structural_buyer_replication": ([["code", s] for s in
                                      ["verify_prop1_premium.py", "verify_prop2_investment.py",
                                       "verify_prop3_leak.py", "verify_prop7_mirror_voting.py",
                                       "verify_psi_plateau.py", "verify_all.py"]],
                                     "all_results.txt", ["numpy", "matplotlib"]),
    "crisis_behaviour_replication": ([[".", "src/run_stress.py"], [".", "src/make_figure.py"]],
                                     "results/stress_results.json", ["matplotlib"]),
    "comparative_replication":      ([["src", "compare.py"], ["src", "make_figures.py"]],
                                     "results/comparison_results.json", ["matplotlib"]),
    "transition_replication":       ([["code", "run_all_appendix.py"],
                                      ["cs_debt_band/code", "cs_band_verify_final.py"],
                                      ["code", "phase_milestones.py"]],
                                     "cs_debt_band/dsa_locked.json", ["numpy", "matplotlib"]),
    # banking's golden report also covers the nested innovation counterfactual, which its
    # run_all.py shells out to — so the browser must run that script directly too.
    "banking_replication":          ([["code", "test_propositions.py"], ["code", "run_analysis.py"],
                                      ["innovation_counterfactual", "src/run_innovation_cf.py"]],
                                     "all_results.txt", ["numpy", "matplotlib"]),
    "empirical_replication":        ([["code", s] for s in
                                      ["run_all_tables.py", "run_ge_results.py", "compare_to_paper.py"]],
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

# Deliberately NOT browser-runnable — stated on the page rather than quietly omitted.
EXCLUDED = {
    "distribution_inequality_replication":
        "needs the 22 MB raw SCF 2022 microdata file — too large to pull into a browser tab",
    "empirical_validation_replication":
        "needs statsmodels, which pulls scipy (~25 MB of extra WASM) into the page",
}

TITLES = {
    "architecture_replication": "Paper 1 — Architecture",
    "structural_buyer_replication": "Paper 8 — The Structural Buyer",
    "crisis_behaviour_replication": "Paper 12 — Crisis Behaviour",
    "comparative_replication": "Paper 13 — Comparative Analysis",
    "transition_replication": "Paper 3 — Transition",
    "banking_replication": "Paper 6 — Full-Reserve Banking",
    "empirical_replication": "Paper 10 — Historical Counterfactual",
    "interoperability_replication": "Paper 7 — External Interoperability",
    "macro_replication": "Paper 5 — Macroeconomic Model",
    "distribution_inequality_replication": "Paper 14 — Distribution & Inequality",
    "empirical_validation_replication": "Paper 10 — Empirical Validation",
}

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
        if p.stat().st_size > 3_000_000:
            continue
        out.append(rel.as_posix())
    return out


def main():
    pkgs = []
    for pkg, (steps, golden, deps) in SPEC.items():
        files = files_for(pkg)
        gfiles = golden_files(pkg, golden)
        pkgs.append({
            "id": pkg,
            "title": TITLES[pkg],
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
        "base": "replication",
        "packages": pkgs,
        "excluded": [{"id": k, "title": TITLES[k], "reason": v} for k, v in EXCLUDED.items()],
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

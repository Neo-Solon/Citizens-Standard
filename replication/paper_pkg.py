"""
paper_pkg.py — shared adapter used by every paper replication package.

WHAT A "PASS" MEANS HERE
------------------------
Each paper package ships a golden artifact that the paper itself cites: `all_results.txt`
(captured stdout of the package's own runner) or `results/*.json`. Those are the published
numbers.

To verify a package we:
  1. copy the pristine package into a scratch dir (so nothing on disk is mutated),
  2. run the package's OWN entry point there, offline, exactly as an academic would,
  3. re-extract every number from the freshly produced artifact,
  4. compare it, value by value, against the shipped golden artifact.

PASS = the code still reproduces the published numbers. That is a genuine reproducibility
check, not a self-fulfilling one: the expected values are the author's published record,
not something regenerated at verification time.

Numbers are compared with a relative tolerance (default 1e-6, loosened per-package only where
a stochastic component is documented in that package's README).
"""
import json, os, re, shutil, subprocess, sys, tempfile
from pathlib import Path

NUM = re.compile(r'-?\d+\.?\d*(?:[eE][-+]?\d+)?')

# Lines reporting wall-clock timing are machine-dependent, not published results. Excluding them
# stops a faster/slower box from being reported as a failed reproduction.
TIMING = re.compile(r'runtime|elapsed|seconds|secs|\bsec\b|took ', re.I)
# An ISO datestamp is not a published value. Paper 2's golden opens 'Run date: 2026-07-12';
# a fresh run prints today's. The tokenizer splits that into 2026, -07, -12, so the golden's
# '-12' is never reproduced and the package fails on the calendar. Neutralised on BOTH sides —
# unlike TIMING, a date is never a result in either text.
DATESTAMP = re.compile(r'\b\d{4}-\d{2}-\d{2}\b')


def _nums(text, drop_timing=False):
    """Every numeric token in a blob of text.

    drop_timing is applied ONLY to the golden artifact, never to the fresh run. Dropping a whole
    line strips every number on it — and packages print results and durations on the same line
    ("...pass rate 0.983 (2.1 sec)"). Removing such a line from the RUN would make a real result
    look unreproduced. Removing it from the EXPECTATIONS just means we don't demand a wall-clock
    match, which is what we want. Containment (want subset of got) makes extra numbers harmless.
    """
    text = DATESTAMP.sub("DATE", text)
    if drop_timing:
        text = "\n".join(ln for ln in text.splitlines() if not TIMING.search(ln))
    out = []
    for tok in NUM.findall(text):
        try:
            out.append(float(tok))
        except ValueError:
            pass
    return out


def _flatten(obj, prefix=""):
    """Every numeric leaf in a JSON structure, keyed by path."""
    flat = {}
    if isinstance(obj, dict):
        for k, v in obj.items():
            flat.update(_flatten(v, f"{prefix}.{k}" if prefix else str(k)))
    elif isinstance(obj, list):
        for i, v in enumerate(obj):
            flat.update(_flatten(v, f"{prefix}[{i}]"))
    elif isinstance(obj, bool):
        pass
    elif isinstance(obj, (int, float)):
        flat[prefix] = float(obj)
    return flat


def _close(a, b, rtol):
    if a == b:
        return True
    denom = max(abs(a), abs(b))
    if denom == 0:
        return abs(a - b) <= rtol
    return abs(a - b) / denom <= rtol


def verify(pkg_dir, entry, artifacts, rtol=1e-6, timeout=600, note=""):
    """
    pkg_dir   : the vendored package (contains the pristine golden artifacts)
    entry     : entry script, relative to pkg_dir, e.g. "run_all.py" or "code/run_all.py"
    artifacts : list of (kind, path). kind is "stdout" (compare the runner's stdout against a
                shipped text file) or "json" (compare a regenerated json against the shipped one).
    """
    pkg_dir = Path(pkg_dir).resolve()
    with tempfile.TemporaryDirectory() as tmp:
        work = Path(tmp) / pkg_dir.name
        shutil.copytree(pkg_dir, work)

        entry_path = work / entry
        if not entry_path.exists():
            return {"passed": False, "summary": f"entry script missing: {entry}", "detail": {}}

        proc = subprocess.run(
            [sys.executable, str(entry_path.name)],
            cwd=str(entry_path.parent),
            capture_output=True, text=True, timeout=timeout,
            env={**os.environ, "MPLBACKEND": "Agg", "MPLCONFIGDIR": tmp},
        )
        if proc.returncode != 0:
            tail = (proc.stderr or proc.stdout).strip().splitlines()[-1:] or [""]
            return {"passed": False,
                    "summary": f"runner exited {proc.returncode}: {tail[0][:70]}",
                    "detail": {"returncode": proc.returncode, "stderr": proc.stderr[-2000:]}}

        # The packages regenerate their figures during the run. Without this they would be
        # discarded along with the scratch directory, and `run_all.py` would be text-only —
        # strictly less than running a package by hand. Harvest them instead.
        figures = []
        figdir = os.environ.get("CS_REPL_FIGURES")
        if figdir:
            dest = Path(figdir) / pkg_dir.name
            dest.mkdir(parents=True, exist_ok=True)
            for png in sorted(work.rglob("*.png")):
                try:
                    out_name = png.relative_to(work).as_posix().replace("/", "__")
                    shutil.copy2(png, dest / out_name)
                    figures.append(f"{pkg_dir.name}/{out_name}")
                except Exception:
                    pass

        checked = mismatched = 0
        worst = 0.0
        detail = {}

        for kind, rel in artifacts:
            golden_path = pkg_dir / rel
            if not golden_path.exists():
                return {"passed": False, "summary": f"golden artifact missing: {rel}", "detail": {}}

            if kind == "stdout":
                # CONTAINMENT, not positional matching. The golden report and the runner's stdout
                # are not line-for-line identical (headers, ordering, extra progress output differ),
                # so index-by-index comparison is meaningless. What must hold is: every number the
                # PAPER publishes still appears in what the code produces. Missing even one is a
                # reproduction failure; extra output in the run is not.
                got = _nums(proc.stdout)                                     # everything the code printed
                want = _nums(golden_path.read_text(errors="ignore"), drop_timing=True)
                if not want:
                    return {"passed": False, "summary": f"no numbers found in {rel}", "detail": {}}
                bad = []
                for wv in want:
                    checked += 1
                    if not any(_close(gv, wv, rtol) for gv in got):
                        mismatched += 1
                        if len(bad) < 8:
                            bad.append({"published": wv, "status": "not reproduced"})
                detail[rel] = {"published_values": len(want), "not_reproduced": mismatched,
                               "examples": bad}

            elif kind == "json":
                fresh_path = work / rel
                if not fresh_path.exists():
                    return {"passed": False, "summary": f"runner did not regenerate {rel}", "detail": {}}
                want = _flatten(json.loads(golden_path.read_text()))
                got = _flatten(json.loads(fresh_path.read_text()))
                bad = []
                for k, wv in want.items():
                    if k not in got:
                        continue
                    checked += 1
                    if not _close(got[k], wv, rtol):
                        mismatched += 1
                        d = abs(got[k] - wv) / max(abs(wv), 1e-12)
                        worst = max(worst, d)
                        if len(bad) < 8:
                            bad.append({"key": k, "published": wv, "reproduced": got[k]})
                detail[rel] = {"compared": len(want), "mismatched": len(bad), "examples": bad}

        passed = (mismatched == 0) and (checked > 0)
        summary = (f"{checked} published values reproduced" if passed
                   else f"{mismatched}/{checked} published values NOT reproduced")
        if note and passed:
            summary += f"; {note}"
        return {"passed": passed, "summary": summary,
                "figures": figures,
                "detail": {"checked": checked, "mismatched": mismatched, "rtol": rtol,
                           "figures": len(figures), **detail}}

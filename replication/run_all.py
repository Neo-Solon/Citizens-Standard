#!/usr/bin/env python3
"""
Citizens Standard - Replication Runner (one-command, run-all)
=============================================================
Two ways to use this repo:

  ACADEMICS / REVIEWERS: each package under packages/ is a standalone, inspectable
    replication with its own script, data, and notes. Read and run them individually.

  EVERYONE ELSE: run this file. It executes every package in sequence against the
    bundled data snapshot and prints a clean pass/fail table.

Data model (Option C - bundled snapshot + optional refresh):
  * By DEFAULT, packages read the bundled CSV snapshot in data/. This works offline,
    with no API key, and reproduces the exact published figures. Discontinued FRED
    series (e.g. WSAVNS, OCDSL) exist ONLY as bundled snapshots and cannot be refreshed.
  * With --refresh, refreshable series are re-pulled live from FRED (needs a free
    FRED_API_KEY env var). Discontinued series stay on the snapshot automatically.
    Note: live data may differ slightly from published figures due to FRED revisions.

Usage:
  python run_all.py                 # run everything on the bundled snapshot (recommended)
  python run_all.py --refresh       # re-pull refreshable series from FRED first
  python run_all.py --only two_circuit   # run a single package by name
  python run_all.py --list          # list available packages
  python run_all.py --report        # ALSO write report/REPORT.html: the pass/fail table plus
                                    #   every figure the packages regenerate, in one page you can
                                    #   open in a browser. Nothing is hand-copied — the figures are
                                    #   produced by this run, so the report cannot go stale.
"""
import argparse, importlib.util, json, os, sys, time, traceback
from pathlib import Path

ROOT = Path(__file__).resolve().parent
PKG_DIR = ROOT / "packages"
DATA_DIR = ROOT / "data"


def discover_packages():
    """Each package is a subdir of packages/ containing a run.py exposing run()->dict."""
    pkgs = []
    if not PKG_DIR.exists():
        return pkgs
    for p in sorted(PKG_DIR.iterdir()):
        if p.is_dir() and (p / "run.py").exists():
            pkgs.append(p.name)
    return pkgs


def load_run(pkg_name):
    run_py = PKG_DIR / pkg_name / "run.py"
    spec = importlib.util.spec_from_file_location(f"pkg_{pkg_name}", run_py)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    if not hasattr(mod, "run"):
        raise AttributeError(f"{pkg_name}/run.py must define run(data_dir, refresh) -> dict")
    return mod.run


def maybe_refresh(refresh):
    """If --refresh, call the shared fetcher to update refreshable series into data/.
    Discontinued series are skipped automatically (see data/SOURCES.md)."""
    if not refresh:
        return
    fetch = ROOT / "fetch_data.py"
    if not fetch.exists():
        print("  [refresh] fetch_data.py not found; using bundled snapshot.")
        return
    key = os.environ.get("FRED_API_KEY")
    if not key:
        print("  [refresh] FRED_API_KEY not set; using bundled snapshot instead.")
        return
    print("  [refresh] pulling refreshable series from FRED ...")
    spec = importlib.util.spec_from_file_location("fetch_data", fetch)
    fmod = importlib.util.module_from_spec(spec); spec.loader.exec_module(fmod)
    fmod.refresh_all(DATA_DIR, key)


def main():
    ap = argparse.ArgumentParser(description="Citizens Standard replication runner")
    ap.add_argument("--refresh", action="store_true", help="re-pull refreshable series from FRED first")
    ap.add_argument("--only", metavar="PKG", help="run a single package by name")
    ap.add_argument("--list", action="store_true", help="list packages and exit")
    ap.add_argument("--report", action="store_true",
                    help="write report/REPORT.html with the results table and every regenerated figure")
    args = ap.parse_args()

    pkgs = discover_packages()
    if args.list:
        print("Available packages:")
        for p in pkgs:
            print("  -", p)
        return 0
    if args.only:
        if args.only not in pkgs:
            print(f"Unknown package '{args.only}'. Available: {', '.join(pkgs)}")
            return 2
        pkgs = [args.only]

    # If a visual report is wanted, tell the verifier where to harvest regenerated figures.
    report_dir = ROOT / "report"
    if args.report:
        import shutil as _sh
        if report_dir.exists():
            _sh.rmtree(report_dir)
        (report_dir / "figures").mkdir(parents=True, exist_ok=True)
        os.environ["CS_REPL_FIGURES"] = str(report_dir / "figures")
    else:
        os.environ.pop("CS_REPL_FIGURES", None)

    maybe_refresh(args.refresh)

    print("\n" + "=" * 64)
    print("  CITIZENS STANDARD - REPLICATION RUN")
    print("  data:", "LIVE (refreshed)" if args.refresh else "bundled snapshot")
    print("=" * 64)

    results = []
    for name in pkgs:
        t0 = time.time()
        try:
            run = load_run(name)
            out = run(DATA_DIR, args.refresh)
            ok = bool(out.get("passed", False))
            results.append((name, ok, out.get("summary", ""), time.time() - t0, None,
                            out.get("figures", []), out.get("detail", {})))
        except Exception as e:
            results.append((name, False, "", time.time() - t0, traceback.format_exc(), [], {}))

    # report
    print("\n{:<26} {:<8} {:>7}  {}".format("PACKAGE", "RESULT", "SEC", "SUMMARY"))
    print("-" * 64)
    npass = 0
    for name, ok, summary, dt, err, figs, det in results:
        tag = "PASS" if ok else "FAIL"
        if ok:
            npass += 1
        print("{:<26} {:<8} {:>6.1f}  {}".format(name, tag, dt, summary[:80]))
        if err:
            print("    " + err.strip().splitlines()[-1])
    print("-" * 64)
    print(f"  {npass}/{len(results)} packages passed")
    print("=" * 64 + "\n")

    if args.report:
        write_report(report_dir, results, npass, args.refresh)
        print(f"  visual report: {report_dir / 'REPORT.html'}")
        nfig = sum(len(r[5]) for r in results)
        print(f"  {nfig} figures regenerated by this run\n")

    return 0 if npass == len(results) else 1


def write_report(report_dir, results, npass, refreshed):
    """One self-contained page: the verdict, the table, and every figure this run regenerated."""
    import html as _h
    from datetime import datetime, timezone

    total = len(results)
    ok_all = npass == total
    rows, sections = [], []

    for name, ok, summary, dt, err, figs, det in results:
        tag = "PASS" if ok else "FAIL"
        cls = "pass" if ok else "fail"
        rows.append(
            f'<tr><td><a href="#{_h.escape(name)}">{_h.escape(name)}</a></td>'
            f'<td class="{cls}">{tag}</td><td class="num">{dt:.1f}s</td>'
            f'<td class="num">{len(figs)}</td><td>{_h.escape(summary)}</td></tr>'
        )

        body = [f'<h2 id="{_h.escape(name)}">{_h.escape(name)} '
                f'<span class="tag {cls}">{tag}</span></h2>',
                f'<p class="sum">{_h.escape(summary)}</p>']

        if err:
            body.append(f'<pre class="err">{_h.escape(err.strip()[-1500:])}</pre>')

        # show exactly which published values failed to reproduce — no hand-waving
        for k, v in det.items():
            if isinstance(v, dict) and v.get("examples"):
                body.append(f'<p class="sub">Not reproduced, from <code>{_h.escape(str(k))}</code>:</p>')
                body.append('<pre class="err">' +
                            _h.escape(json.dumps(v["examples"], indent=2)) + '</pre>')

        if figs:
            body.append('<div class="figs">' + "".join(
                f'<figure><img src="figures/{_h.escape(f)}" loading="lazy">'
                f'<figcaption>{_h.escape(f.split("/", 1)[-1])}</figcaption></figure>'
                for f in figs) + '</div>')
        else:
            body.append('<p class="sub">No figures produced by this package.</p>')
        sections.append("\n".join(body))

    stamp = datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M UTC")
    verdict = (f"{npass}/{total} packages passed" if ok_all
               else f"{npass}/{total} packages passed \u2014 {total - npass} FAILED")

    doc = f"""<!doctype html><meta charset="utf-8">
<title>Citizens Standard \u2014 replication report</title>
<style>
  :root {{ --ink:#10161C; --panel:#18212B; --line:#27313C; --text:#ECE7DB; --dim:#9AA3AE;
           --pass:#5FBE93; --fail:#E0685A; --amber:#E6A93E; }}
  * {{ box-sizing:border-box }}
  body {{ margin:0; padding:34px 22px 80px; background:var(--ink); color:var(--text);
         font:15px/1.6 system-ui,-apple-system,Segoe UI,Roboto,sans-serif; }}
  .wrap {{ max-width:1080px; margin:0 auto }}
  h1 {{ font-size:1.5rem; margin:0 0 4px }}
  .meta {{ color:var(--dim); font-size:.85rem; margin:0 0 22px }}
  .verdict {{ font-weight:700; font-size:1.1rem; padding:12px 16px; border-radius:8px;
              border:1px solid {'var(--pass)' if ok_all else 'var(--fail)'};
              background:{'rgba(95,190,147,.10)' if ok_all else 'rgba(224,104,90,.10)'};
              color:{'var(--pass)' if ok_all else 'var(--fail)'}; margin-bottom:8px }}
  .note {{ color:var(--dim); font-size:.86rem; margin:0 0 26px; max-width:78ch }}
  table {{ width:100%; border-collapse:collapse; margin-bottom:34px; font-size:.9rem }}
  th,td {{ text-align:left; padding:8px 10px; border-bottom:1px solid var(--line) }}
  th {{ color:var(--dim); font-weight:600; text-transform:uppercase; font-size:.72rem;
        letter-spacing:.07em }}
  td.num {{ text-align:right; font-variant-numeric:tabular-nums; color:var(--dim) }}
  a {{ color:var(--amber); text-decoration:none }} a:hover {{ text-decoration:underline }}
  .pass {{ color:var(--pass); font-weight:700 }} .fail {{ color:var(--fail); font-weight:700 }}
  .tag {{ font-size:.7rem; padding:2px 8px; border-radius:20px; vertical-align:middle }}
  .tag.pass {{ background:rgba(95,190,147,.14) }} .tag.fail {{ background:rgba(224,104,90,.14) }}
  h2 {{ font-size:1.05rem; margin:30px 0 4px; padding-top:18px; border-top:1px solid var(--line) }}
  .sum {{ color:var(--dim); margin:0 0 12px; font-size:.9rem }}
  .sub {{ color:var(--dim); font-size:.82rem; margin:10px 0 4px }}
  pre.err {{ background:var(--panel); border:1px solid var(--fail); border-left-width:3px;
             border-radius:6px; padding:10px 12px; overflow-x:auto; font-size:.78rem;
             color:var(--text) }}
  .figs {{ display:grid; grid-template-columns:repeat(auto-fill,minmax(300px,1fr)); gap:14px }}
  figure {{ margin:0; background:var(--panel); border:1px solid var(--line); border-radius:8px;
            padding:8px }}
  figure img {{ width:100%; height:auto; display:block; border-radius:4px; background:#fff }}
  figcaption {{ color:var(--dim); font-size:.72rem; margin-top:6px; word-break:break-all }}
</style>
<div class="wrap">
  <h1>Citizens Standard \u2014 replication report</h1>
  <p class="meta">{stamp} \u00b7 data: {"LIVE (refreshed from FRED)" if refreshed else "bundled snapshot"}</p>
  <div class="verdict">{_h.escape(verdict)}</div>
  <p class="note">
    A <b>PASS</b> means the package's own code, run offline just now, still reproduces every number
    the paper published \u2014 the expected values come from each package's shipped golden artifact,
    not from this run. Every figure below was regenerated by this run, so nothing here can go stale.
  </p>
  <table>
    <tr><th>Package</th><th>Result</th><th>Time</th><th>Figures</th><th>Summary</th></tr>
    {"".join(rows)}
  </table>
  {"".join(sections)}
</div>"""
    (report_dir / "REPORT.html").write_text(doc, encoding="utf-8")


if __name__ == "__main__":
    sys.exit(main())

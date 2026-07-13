/*
 * verify_worker.js — runs the replication packages off the main thread.
 *
 * Pyodide is CPython compiled to WebAssembly, and it executes SYNCHRONOUSLY. Run it on the page's
 * thread and the tab locks solid for the duration — Paper 5 takes ~40 seconds, long enough for the
 * browser to offer to kill the page. So it runs here, in a worker: the page stays responsive, the
 * terminal keeps painting, and the user can scroll, cancel, or leave.
 *
 * Protocol
 *   in : {cmd:'run', base, pkg}     pkg is one entry from replication/web_manifest.json
 *        {cmd:'cancel'}
 *   out: {type:'status',  msg}
 *        {type:'stage',   done, total}
 *        {type:'result',  raw, golden}   raw = JSON from run_package(); golden = published artifacts
 *        {type:'error',   msg}
 */

const PYODIDE = 'https://cdn.jsdelivr.net/pyodide/v0.26.4/full/';

let py = null;
let driverLoaded = false;

function post(type, extra) {
  self.postMessage(Object.assign({ type: type }, extra || {}));
}

/*
 * The Python driver. Identical in behaviour to the offline harness (replication/paper_pkg.py):
 * exec each script in-process, capture stdout, hand back figures and regenerated artifacts.
 *
 * Pyodide has no subprocess, and every package's own run_all.py shells out to its scripts — so the
 * manifest records the script sequence and we exec them directly. The scripts are unchanged; only
 * the process model differs. Four things bite when you do that, and each is handled below.
 */
const DRIVER = `
import base64, contextlib, glob, io, json, os, runpy, sys

def run_package(root, steps):
    # Imported here, not at module scope: loadPackage() for a package's deps runs before each call,
    # so a top-level import would execute before anything was loaded.
    import matplotlib
    matplotlib.use("Agg")

    buf = io.StringIO()
    cwd0 = os.getcwd()
    path0 = list(sys.path)
    argv0 = list(sys.argv)
    mods0 = set(sys.modules)
    err = None
    try:
        with contextlib.redirect_stdout(buf), contextlib.redirect_stderr(io.StringIO()):
            for d, script in steps:
                wd = root if d == "." else os.path.join(root, d)
                os.chdir(wd)
                sys.path.insert(0, wd)
                # (1) Scripts branch on sys.argv — one package's runner takes a mode argument. A
                #     subprocess gets a clean argv; an in-process exec inherits the caller's.
                sys.argv = [os.path.basename(script)]
                try:
                    runpy.run_path(os.path.join(wd, script), run_name="__main__")
                except SystemExit:
                    # (2) sys.exit() in one script must not abort the remaining steps.
                    pass
    except Exception as e:
        err = "%s: %s" % (type(e).__name__, e)
    finally:
        os.chdir(cwd0)
        sys.path[:] = path0
        sys.argv[:] = argv0
        # (3) Evict only the PACKAGE's modules. Purging library modules (matplotlib.pyplot!) leaves
        #     the library half-initialised and throws unrelated errors in the next package.
        for m in list(set(sys.modules) - mods0):
            f = getattr(sys.modules.get(m), "__file__", None) or ""
            if f.startswith(root):
                sys.modules.pop(m, None)
        # (4) matplotlib is process-global: open figures and mutated rcParams leak between packages.
        import matplotlib.pyplot as plt
        plt.close("all"); matplotlib.rcdefaults(); matplotlib.use("Agg")

    figs = []
    for p in sorted(glob.glob(os.path.join(root, "**", "*.png"), recursive=True)):
        with open(p, "rb") as fh:
            figs.append({"name": os.path.relpath(p, root),
                         "b64": base64.b64encode(fh.read()).decode()})
    regen = {}
    for p in glob.glob(os.path.join(root, "**", "*.json"), recursive=True):
        try:
            regen[os.path.relpath(p, root)] = open(p).read()
        except Exception:
            pass
    return json.dumps({"stdout": buf.getvalue(), "figures": figs,
                       "regenerated": regen, "error": err})
`;

async function boot() {
  if (py) return py;
  post('status', { msg: 'loading Python (WebAssembly)…' });
  importScripts(PYODIDE + 'pyodide.js');
  py = await loadPyodide({ indexURL: PYODIDE });
  return py;
}

function mkdirTree(path) {
  try { py.FS.mkdirTree(path); } catch (e) { /* already exists */ }
}

async function stage(base, pkg) {
  const root = '/w/' + pkg.id;
  mkdirTree(root);
  (pkg.mkdirs || []).forEach(function (d) { mkdirTree(root + '/' + d); });

  // Some scripts read a SIBLING package's data via ../../../ (distribution/procyclicality reads
  // empirical_replication's historical CSV). Packages are staged side by side under /w/, so the
  // relative path resolves — but the file still has to be fetched.
  for (const sp of (pkg.siblings || [])) {
    const r = await fetch(base + sp, { cache: 'no-cache' });
    if (!r.ok) { post('status', { msg: 'warning: sibling file missing: ' + sp }); continue; }
    const buf = new Uint8Array(await r.arrayBuffer());
    mkdirTree('/w/' + sp.slice(0, sp.lastIndexOf('/')));
    py.FS.writeFile('/w/' + sp, buf);
  }

  const all = pkg.files.concat(pkg.goldenFiles);
  const golden = {};
  const warnings = [];
  let bytes = 0;
  for (let i = 0; i < all.length; i++) {
    const rel = all[i];
    const r = await fetch(base + pkg.id + '/' + rel, { cache: 'no-cache' });
    if (!r.ok) {
      // Don't kill the whole package for one absent file — report it, keep going. If it was
      // genuinely needed, the script that needs it fails loudly a moment later.
      warnings.push('could not fetch ' + rel + ' (HTTP ' + r.status + ')');
      continue;
    }
    const buf = new Uint8Array(await r.arrayBuffer());
    const slash = rel.lastIndexOf('/');
    mkdirTree(slash > 0 ? root + '/' + rel.slice(0, slash) : root);
    py.FS.writeFile(root + '/' + rel, buf);

    // Stash the PUBLISHED artifact now — the run overwrites results/*.json in place.
    if (pkg.goldenFiles.indexOf(rel) >= 0) {
      golden[rel] = new TextDecoder().decode(buf);
    }
    bytes += buf.length;
    if (i % 5 === 0 || i === all.length - 1) {
      post('stage', { done: i + 1, total: all.length, bytes: bytes });
    }
  }
  return { golden, warnings };
}

self.onmessage = async function (e) {
  const msg = e.data || {};
  if (msg.cmd !== 'run') return;
  const { base, pkg } = msg;

  try {
    await boot();

    post('status', { msg: 'loading ' + pkg.deps.join(', ') + '…' });
    try {
      // Must precede the driver: run_package() imports matplotlib on entry.
      await py.loadPackage(pkg.deps);
    } catch (depErr) {
      throw new Error('could not load ' + pkg.deps.join(', ') + ' — ' +
                      ((depErr && depErr.message) || depErr) +
                      '. (Not every PyPI package exists in the Pyodide distribution.)');
    }

    if (!driverLoaded) { await py.runPythonAsync(DRIVER); driverLoaded = true; }

    post('status', { msg: 'fetching ' + (pkg.files.length + pkg.goldenFiles.length) + ' files…' });
    const staged = await stage(base, pkg);
    staged.warnings.forEach(function (w) { post('status', { msg: 'warning: ' + w, warn: true }); });

    post('status', { msg: 'running ' + pkg.title + '…', running: true });
    py.globals.set('_root', '/w/' + pkg.id);
    py.globals.set('_steps', py.toPy(pkg.steps));
    const raw = await py.runPythonAsync('run_package(_root, [list(s) for s in _steps])');

    post('result', { raw: raw, golden: staged.golden, warnings: staged.warnings });
  } catch (err) {
    post('error', { msg: (err && err.message) ? err.message : String(err) });
  }
};

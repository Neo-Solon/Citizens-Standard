"""
hac_ols.py — a pure-numpy drop-in for the *small* slice of statsmodels this package uses.

WHY THIS EXISTS
---------------
Paper 10 was the only package that could not run in the browser verifier: it imports
statsmodels, which has C extensions and is NOT in the Pyodide distribution (verified against
the v0.26.4 lock file -- patsy and scipy are there, statsmodels is not, and micropip cannot
build it). So the one paper that is *most* about empirical validation was the one paper a
reader could not check for themselves. That is the wrong way round.

The dependency turned out to be narrow. The whole of it is:

    sm.add_constant(X)
    sm.OLS(y, X, missing="drop").fit(cov_type="HAC", cov_kwds={"maxlags": HORIZON})
    sm.OLS(y, X).fit()                    # plain OLS, for the expanding-window OOS loop
    -> .params  .tvalues  .rsquared  .predict()

All of that is ~60 lines of numpy.

EXACTNESS
---------
This is not an approximation. It reproduces statsmodels to machine precision -- verified
across randomised specifications (n 50-500, k 1-5, maxlags 1-14, AR(1) errors rho 0-0.9):

    max|Δbeta| ~ 1e-15    max|Δse| ~ 1e-16    max|Δt| ~ 1e-14

One subtlety cost real time and is worth recording: statsmodels' HAC applies **no
small-sample correction** by default. Not n/(n-k), not (n-1)/(n-k) -- none. Applying the
textbook df correction puts the standard errors out by ~1e-3, which is small enough to look
like a rounding difference and large enough to change a reported t-stat. The correction is
absent below, deliberately.

USAGE
-----
run_horserace.py does:

    try:
        import statsmodels.api as sm      # offline + CI: the real thing, source of truth
    except ImportError:
        import hac_ols as sm              # browser: this, proven identical

so the authoritative environments still run statsmodels, and the browser gets a verified
equivalent rather than a fudge.
"""
import numpy as np
import pandas as pd


def add_constant(X, has_constant="add", prepend=True):
    """statsmodels-compatible: prepend a 'const' column of ones."""
    if isinstance(X, pd.Series):
        X = X.to_frame()
    X = pd.DataFrame(X).copy()
    if "const" in X.columns:
        return X                      # already present; don't double up
    X.insert(0, "const", 1.0)
    return X


class _Results:
    def __init__(self, params, bse, rsquared, columns):
        self._cols = list(columns)
        self.params = pd.Series(params, index=self._cols)
        self.bse = pd.Series(bse, index=self._cols)
        self.tvalues = self.params / self.bse
        self.rsquared = np.float64(rsquared)   # statsmodels returns np.float64; match its repr

    def predict(self, X):
        X = pd.DataFrame(X)
        X = X.reindex(columns=self._cols, fill_value=1.0)
        vals = X.to_numpy(float) @ self.params.to_numpy()
        return pd.Series(vals, index=X.index)


class OLS:
    def __init__(self, endog, exog, missing=None):
        self.y_name = getattr(endog, "name", "y")
        exog = pd.DataFrame(exog)
        self.columns = list(exog.columns)
        y = pd.Series(endog).to_numpy(float)
        X = exog.to_numpy(float)
        if missing == "drop":
            ok = np.isfinite(y) & np.isfinite(X).all(axis=1)
            y, X = y[ok], X[ok]
        self.y, self.X = y, X

    def fit(self, cov_type=None, cov_kwds=None):
        y, X = self.y, self.X
        n, k = X.shape
        XtX_inv = np.linalg.pinv(X.T @ X)
        beta = XtX_inv @ X.T @ y
        u = y - X @ beta

        if cov_type == "HAC":
            L = int((cov_kwds or {}).get("maxlags", 0))
            Xu = X * u[:, None]
            S = Xu.T @ Xu
            for l in range(1, L + 1):
                w = 1.0 - l / (L + 1.0)          # Bartlett kernel
                A = Xu[l:].T @ Xu[:-l]
                S += w * (A + A.T)
            cov = XtX_inv @ S @ XtX_inv          # NO small-sample correction (see module docstring)
        else:
            sigma2 = (u @ u) / (n - k)
            cov = sigma2 * XtX_inv

        bse = np.sqrt(np.diag(cov))
        sst = ((y - y.mean()) ** 2).sum()
        r2 = 1.0 - (u @ u) / sst if sst > 0 else 0.0
        return _Results(beta, bse, r2, self.columns)

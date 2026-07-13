# Replication: The Citizens Standard — Comparative Analysis (Paper 13)

Author: Neo-Solon · Neo-Solon@hotmail.com · License: CC BY 4.0

This package empirically grounds *The Citizens Standard: Comparison with Alternative Monetary and Distributional Systems*
(Neo-Solon, 2026m; SSRN 6973338). It backs every cell of the paper's comparison
table and every comparative claim with a sourced, real-world figure, and computes
the axes that are genuinely comparable across systems.

## What this package does — and deliberately does not do

Paper 13 is a **positioning paper**. Its own Section 7 states that it argues from
the structure of each system, **not** from a head-to-head empirical horse-race,
"which most of these alternatives have never run against one another on comparable
data." This package respects that frame:

- It **sources every categorical cell** (funding, what it builds, coverage, price
  brake, maturity) to a primary reference — see `AUDIT.md`.
- It **computes the axes that ARE comparable** in common units: annual per-person
  cash benefit, owned wealth stock per person, and funding sustainability / capture.
- It **flags every "differs in kind" case** explicitly (Georgism is a funding base,
  not a distribution; Social Security is contributory retirement income, not a
  universal working-age flow; the Citizens Standard is theoretical, with no
  operating record). It does **not** collapse the systems into a single winner.

The comparators are the distributional cousins (UBI, Social Security, the sovereign
wealth fund / Alaska model, Georgism). Full-reserve banking, CBDC and MMT are
treated by the paper as adjacent-not-rival and are not scored here.

## Run

```
pip install -r requirements.txt
python run_all.py
```

This writes `results/comparison_results.json`, `results/fig_annual_benefit.png`,
and `results/fig_wealth_stock.png`, and prints the sourced tables and claim checks.

## Layout

```
src/data.py          every figure, each with a src tag resolving to AUDIT.md
src/compare.py       sourced tables + comparable axes + checks of Claims 1,2,4
src/make_figures.py  the two figures
data/comparators.csv, data/alaska_pfd_anchors.csv   sourced inputs
results/             json, figures, results.txt
AUDIT.md             full citation for every source tag
```

## What the grounding establishes

- **Claim 1 (the distinctive cell) holds in the data**: of the five systems, the
  Citizens Standard is the only one simultaneously self-financing, wealth-building,
  and equipped with a price-stability mechanism (`claim1` check = True).
- **Claim 2 (where it is dominated) holds**: Social Security and the Alaska fund are
  the only "proven" systems; Georgism's funding base carries ~zero deadweight loss;
  the Citizens Standard leads no single axis (it is theoretical).
- **Claim 4 (the binding condition) holds**: the Citizens Standard's funding is
  growth-tied and its dividend is procyclical (Paper 12), so its advantage is
  conditional, exactly as the paper concedes.
- On the **comparable numbers**: the Citizens Standard's *dividend* is modest
  (~$516–$2,388/yr, in the range of Alaska's ~$1,600, well below a UBI-scale flow),
  while its *owned wealth stock* (~$233K–$413K/person) is the distinctive feature —
  alongside Alaska (~$133K/resident) and against $0 owned stock under UBI and Social
  Security. The empirical case is the combination, not dominance on any one axis —
  precisely the paper's thesis.

## Honest limits

The per-person figures are not like-for-like welfare comparisons: they mix a
universal resident dividend (Alaska), a contributory retirement benefit (Social
Security), a proposed universal flow (UBI), and a theoretical floor (Citizens
Standard). They are reported on common axes to make the *structure* of the
comparison checkable, not to declare a winner. Georgism is represented as a funding
base because that is what it is; pairing it with a citizen's dividend would change
its row, and the paper notes that variants shift specific cells.

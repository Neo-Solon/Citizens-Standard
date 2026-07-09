# Citizens Standard — Innovation Counterfactual Replication Package

Bounds the direct financing-cost effect of full-reserve banking on R&D / innovation.

## The question
A common objection: constraining bank money-creation (full reserve) will choke
innovation, since "most advancement was financed by debt or deficit." This package
tests the *direct financing-cost* channel of that claim.

## Run
    python run_all.py
Writes results/INNOVATION_CF_RESULTS.md. No third-party dependencies.

## Method
R&D responds to its user cost with a measured elasticity. The Citizens Standard
removes ONE financing channel — bank deposit-creation via lending — and leaves
company own-funds, external equity, and public/deficit-funded research intact:

    %ΔR&D = elasticity_RD × (debt share of R&D finance) × (cost increase on debt slice)

## Result (see SOURCES.json for every input)
- Grounded central (1% debt share, elasticity -2, +20% debt cost): **-0.4%**
- Adversarial (5% share, -4, +30%): **-6%**
- Extreme "even if" (10% share, -4, +50%): **-20%**

The measured debt reliance of R&D-intensive firms is ~0.5% of assets, and debt is
*negatively* correlated with R&D intensity; external equity funds most of the rise
in US R&D. So the channel full reserve removes is close to irrelevant to how R&D is
actually financed, and the direct effect is negligible in the grounded case.

## Scope and honest limits
- **Partial equilibrium.** Bounds the direct financing-cost channel only. Does NOT
  capture a general-equilibrium demand channel (less credit-fuelled demand → fewer
  profitable products). That channel requires behavioural assumptions and is left
  explicitly open — it is the residual uncertainty, not the financing channel.
- **Favourable offset not quantified.** CS routes issuance into a broad equity pool;
  since R&D is equity/own-funds financed, a deeper equity base plausibly offsets even
  this small loss. Flagged directionally, not claimed as a result.

## Files
    run_all.py                     entry point
    src/run_innovation_cf.py       the model
    data/SOURCES.json              every parameter with citation
    results/INNOVATION_CF_RESULTS.md  generated output
    requirements.txt               (none)

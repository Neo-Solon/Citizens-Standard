"""
Bounded partial-equilibrium innovation counterfactual for the Citizens Standard.
=================================================================================
Question (raised by an MMT interlocutor): does constraining bank money-creation
via full-reserve banking reduce innovation, given the claim that "most
advancement since the 19th century was financed by debt or deficit"?

APPROACH
--------
R&D responds to its user cost with a measured elasticity. The Citizens Standard
removes exactly ONE financing channel: bank deposit-creation via lending. It
leaves intact (a) company own-funds / retained earnings, (b) external EQUITY,
and (c) public / deficit-financed research. So the direct financing-cost effect
on R&D is bounded by:

    %ΔR&D  =  elasticity_RD  ×  %Δ(user cost of R&D)
    %Δ(user cost of R&D)  ≈  (debt share of R&D finance) × (cost increase on debt slice)

If R&D is barely debt-financed, the effect is small no matter how responsive R&D
is or how much the debt slice's cost rises.

SCOPE / LIMITS (stated, not hidden)
-----------------------------------
* PARTIAL equilibrium. Bounds the direct financing-cost channel only. Does NOT
  capture a general-equilibrium demand channel (less credit-fueled demand ->
  fewer profitable products to develop). That channel needs behavioural
  assumptions and is left explicitly open.
* The favourable offset (CS deepens the equity base that R&D actually uses) is
  flagged directionally and NOT quantified.

SOURCES (all public)
--------------------
[1] NSF NCSES 2023 (nsf25353, nsf26314): of $722B business R&D, company own-funds
    ~87-89%; federal govt the largest EXTERNAL source. Debt not a broken-out
    category. Total US R&D 2023 ~$937B: business-funded 75%, federal 18%.
[2] Gao (NUS), citing Brown-Fazzari-Petersen: median short- and long-term
    debt-to-assets for high-tech firms in the 2000s = 0.005 each. "Low reliance
    on debt financing."
[3] Hall & Lerner (2009): "debt is a disfavored source of finance for R&D";
    R&D intensity and leverage NEGATIVELY correlated (Friend-Lang 1988; Hall
    1992; Bhagat-Welch 1995).
[4] Brown & Petersen (2009, 2011): external EQUITY, not debt, funds most of the
    rise in US R&D. "Neither debt finance nor cash flow" is the funding source.
[5] CRS R48848: recent R&D user-cost elasticity estimates -2.0 to -4.0
    (older -1.0).
"""

# ---- INPUTS (grounded, sourced) ------------------------------------------

# Debt-financed share of R&D finance.
#   Measured reliance is ~0.5% of assets for R&D-intensive firms [2], and debt
#   is NEGATIVELY correlated with R&D intensity [3]. We nonetheless carry a
#   RANGE whose TOP end is far above measured reality, to be adversarial.
debt_share_measured = 0.01   # ~1%, generous vs the 0.5% debt-to-assets figure [2]
debt_share_adverse  = 0.05   # 5%: deliberately 5-10x measured, adversarial
debt_share_extreme  = 0.10   # 10%: implausible upper bound, "even if"

# R&D user-cost elasticity [5]. Use the full published span.
elast_most_responsive = -4.0
elast_mid             = -2.0
elast_least           = -1.0

# Cost increase on the debt slice from removing deposit-creation (intermediation
# premium). CS Paper 6 frames this as a rise in intermediation cost, not a ban.
# Bound generously.
cost_up_mid     = 0.20   # +20%
cost_up_adverse = 0.30   # +30%
cost_up_extreme = 0.50   # +50%, implausibly high

def rd_effect(debt_share, elasticity, cost_up):
    pct_change_usercost = debt_share * cost_up
    return elasticity * pct_change_usercost * 100.0  # percent change in R&D

# ---- SCENARIOS -----------------------------------------------------------

scenarios = {
    "Grounded central (1% debt share, elast -2, +20% cost)":
        rd_effect(debt_share_measured, elast_mid, cost_up_mid),
    "Adversarial (5% debt share, elast -4, +30% cost)":
        rd_effect(debt_share_adverse, elast_most_responsive, cost_up_adverse),
    "Extreme 'even if' (10% debt share, elast -4, +50% cost)":
        rd_effect(debt_share_extreme, elast_most_responsive, cost_up_extreme),
    "Least responsive (1% debt share, elast -1, +20% cost)":
        rd_effect(debt_share_measured, elast_least, cost_up_mid),
}

print("=== Bounded innovation counterfactual: %Δ business R&D under CS full reserve ===\n")
for name, val in scenarios.items():
    print(f"  {name}")
    print(f"     ΔR&D = {val:+.2f}%\n")

print("READING")
print("-------")
print("The measured debt reliance of R&D-intensive firms is ~0.5% of assets [2],")
print("and debt is NEGATIVELY correlated with R&D intensity [3]; external equity,")
print("not debt, funds most of the rise in US R&D [4]. So the channel CS removes")
print("is close to irrelevant for R&D finance. Even a deliberately adversarial 5%")
print("debt share with the most-responsive elasticity gives only a -6% R&D change,")
print("and an implausible 10%/-4/+50% 'even if' still only reaches -20%.")
print()
print("The grounded central estimate is about -0.4% -- economically negligible.")
print()
print("NOT MODELLED (both directions):")
print(" + Favourable: CS routes issuance into a broad equity pool; since R&D is")
print("   equity/own-funds financed [4], a deeper equity base plausibly offsets")
print("   even this tiny loss. Unquantified.")
print(" - Open: general-equilibrium demand channel (less credit-fuelled demand ->")
print("   fewer profitable products). Needs behavioural assumptions; left open.")
print()
print("CONCLUSION: the DIRECT financing-cost channel of the innovation worry is")
print("bounded and negligible. The residual uncertainty is the GE demand channel,")
print("not the financing channel.")

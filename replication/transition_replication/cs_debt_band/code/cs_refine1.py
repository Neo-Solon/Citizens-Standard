"""
Core refinement: should CS aggressively retire debt to 15%, or just STABILIZE it
and route the saved seigniorage to citizens?

Key fact from ch8b: at r<g the carry on standing debt is negative -- it is nearly
free to hold. So seigniorage spent retiring it is seigniorage NOT given to
citizens, to pay down debt that was not costing anything. Test the alternative:
retire only as much as needed to keep debt/GDP from RISING (stabilize), and give
the rest to citizens.

Anchors: GDP $29T, M2 $21.5T, real g 2.0%, nominal g 4.3%. Budget = real_g*M2.
"""
GDP0=29000.0; M2_0=21500.0; real_g=0.020; g_nom=0.043; years=40

def simulate(policy, r_path, floor=0.15):
    d=1.00*GDP0; gdp=GDP0; m2=M2_0
    cum_cit=0.0; cum_bond=0.0; taps=0.0; ratio=[]; cit=[]
    hit=None
    for y in range(1,years+1):
        r=r_path[y-1]; gdp*=(1+g_nom); m2*=(1+g_nom)
        budget=real_g*m2
        interest=r*d
        to_bond=policy(r,g_nom,d,gdp,budget,interest)   # seigniorage routed to redemption
        to_bond=min(to_bond,budget)                     # cannot exceed the clean budget
        to_bond=max(to_bond,0.0)
        # inflationary tap only if you CHOOSE to retire beyond the clean budget (not here)
        to_cit=budget-to_bond
        d=d+interest-to_bond
        if d<floor*gdp: d=floor*gdp
        if hit is None and d<=floor*gdp*1.001: hit=y
        cum_cit+=to_cit; cum_bond+=to_bond
        ratio.append(100*d/gdp); cit.append(to_cit)
    return dict(hit=hit, cum_cit=cum_cit, cum_bond=cum_bond, ratio=ratio, cit=cit, end=100*d/gdp)

# Policies
def aggressive(r,g,d,gdp,budget,interest):    # baseline CS: fixed KT=0.6 of budget to debt
    return 0.6*budget
def stabilize(r,g,d,gdp,budget,interest):     # retire only enough to hold ratio flat
    needed=max(0.0,(r-g)*d)                    # (r-g)*d holds debt/GDP constant; 0 when r<g
    return needed

paths = {
 "central r<g (r=3.3% all years)":      [0.033]*years,
 "cyclical (calm, r>g stress yr 11-18)":[0.033]*10+[0.048]*8+[0.033]*22,
 "permanent moderate r>g (r=4.6%)":     [0.046]*years,
}

for name, rp in paths.items():
    A=simulate(aggressive,rp); S=simulate(stabilize,rp)
    print("="*78); print(name); print("="*78)
    print(f"  {'policy':<26}{'debt/GDP yr40':>14}{'cum citizen $B':>16}{'cum bondholder $B':>18}")
    print(f"  {'aggressive KT=0.6':<26}{A['end']:>13.0f}%{A['cum_cit']:>16,.0f}{A['cum_bond']:>18,.0f}")
    print(f"  {'stabilize-only':<26}{S['end']:>13.0f}%{S['cum_cit']:>16,.0f}{S['cum_bond']:>18,.0f}")
    gain=S['cum_cit']-A['cum_cit']
    print(f"  -> stabilize gives citizens ${gain:,.0f}B more over 40y, "
          f"debt ends at {S['end']:.0f}% vs {A['end']:.0f}%.")
    print()

print("="*78)
print("READING IT HONESTLY")
print("="*78)
print("""- In the r<g central path, 'stabilize-only' retires essentially NOTHING (the
  snowball holds the ratio down on its own) and hands citizens the entire budget.
  Debt/GDP still drifts down via growth. Aggressive retirement buys a lower debt
  ratio that, at r<g, you did not need -- paid for with citizen floors.

- The cost of stabilize-only is HONEST and real: debt/GDP stays HIGHER for longer
  (near launch level), so (a) more of the economy's safe-asset stock is public
  debt -- fine, even useful per ch8b -- but (b) you carry more rate-risk: a future
  r>g shock hits a bigger stock. Stabilize-only trades a lower debt ratio for
  higher citizen floors now, accepting more rate-exposure later.

- Under PERMANENT r>g, stabilize-only must spend (r-g)*d each year just to hold
  the line, which eats into citizen floors -- but only by the gap, not the whole
  budget. It never lets debt run away, and it never starves citizens to zero.

- This is the opposite of aggressive retirement and it is mostly BETTER on CS's
  own objective (citizen floors), with one genuine cost (rate-risk on a larger
  standing stock). The synthesis: stabilize by default, and pre-fund a small
  retirement buffer ONLY against the tail r>g scenario, rather than retiring hard
  in every calm year you did not need to.""")

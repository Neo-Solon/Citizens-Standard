"""
Stage 2 -- how much of the gap CS issuance covers, and the honest framing of
whether intermediation fills the rest. NOT a fabricated "credit availability"
sweep -- there is no empirical parameter to ground that, so we do not invent one.

Two parts:
  (1) QUANTIFIABLE: CS growth-matched issuance supplies ~ (real growth) x M2 of new
      money per year. Compare to the ~3.3%/GDP bank-created flow being removed, to
      size the RESIDUAL that term-deposit intermediation must cover.
  (2) HONEST FRAMING: whether intermediation covers that residual is a genuine,
      unresolved debate. We state both sides with citations; we do not pick a number.
"""
import csv, os, statistics

HIST=os.path.join(os.path.dirname(__file__),'..','..','..','empirical_replication',
                  'data','citizens_standard_historical_data_1960_2025_v2.csv')
rows=[r for r in csv.DictReader(open(HIST))]
for r in rows:
    r['m2']=float(r['m2_billions_usd']); r['gdp']=float(r['gdp_nominal_billions_usd'])
    r['g']=float(r['real_gdp_growth_pct'])/100

BANK_SHARE=0.90

# (1) CS issuance vs bank-created flow, as % of GDP, recent decade
print("="*72)
print("RESIDUAL AFTER CS ISSUANCE -- what term-deposit intermediation must cover")
print("="*72)
print(f"  {'year':>5} {'bank-created':>13} {'CS issuance':>12} {'residual':>10}")
res=[]
for i in range(len(rows)-10,len(rows)):
    dm2=rows[i]['m2']-rows[i-1]['m2']
    bankflow=BANK_SHARE*dm2
    cs_iss=max(0,rows[i]['g'])*rows[i-1]['m2']     # growth-matched issuance
    residual=bankflow-cs_iss
    g=rows[i]['gdp']
    res.append(100*residual/g)
    print(f"  {rows[i]['year']:>5} {100*bankflow/g:>11.1f}% {100*cs_iss/g:>10.1f}% {100*residual/g:>8.1f}%")
print("-"*72)
medres=statistics.median([r for r in res if r==r])
print(f"  Typical residual for intermediation to cover: ~{medres:.1f}% of GDP/yr")
print(f"  (bank-created flow minus what CS sovereign issuance directly supplies)")
print()
print("="*72)
print("THE UNRESOLVED QUESTION (stated honestly, not modelled as a number):")
print("="*72)
print("""
Can term-deposit intermediation cover that residual without starving credit?
This is a genuine, unsettled macro debate. We do NOT assign it a number because
no empirical parameter exists to ground one; doing so would be false precision.

  FOR (intermediation suffices):
   - Benes & Kumhof (IMF WP 2012, "The Chicago Plan Revisited") simulate the
     transition and find credit provision MAINTAINED or improved, with lower
     volatility, because stable funding replaces run-prone deposit creation.
   - McLeay et al. (BoE 2014): the binding constraint on lending is loan demand
     and capital, not deposits per se; a saver-funded system can still lend.
   - CS adds a channel the classic Chicago Plan lacked: sovereign growth-matched
     issuance directly supplies part of the flow, shrinking the residual.

  AGAINST (intermediation falls short):
   - Critics (sovereignmoney.site; Austrian intermediation theorists) argue
     maturity transformation and the sheer volume of bank-created credit (~90% of
     broad money) cannot be replicated by term deposits without raising the cost
     of capital and rationing credit, especially to riskier productive borrowers.
   - The credit-ALLOCATION function (screening, the thing banks actually add, per
     the earlier full-reserve exchange) is unaffected by who creates the money but
     is also not solved by full reserve.

  WHERE CS SITS: CS does not claim intermediation seamlessly replaces bank credit
  at current volume. It claims (a) sovereign issuance supplies the growth-matched
  core directly, (b) the residual is intermediated, and (c) the result is almost
  certainly LESS total credit and a higher cost of capital than the current
  system -- a deliberate trade (less credit-fuelled boom-bust for less credit),
  whose net desirability is contested and unproven. This module sizes the gap;
  it does not claim to close it.
""")

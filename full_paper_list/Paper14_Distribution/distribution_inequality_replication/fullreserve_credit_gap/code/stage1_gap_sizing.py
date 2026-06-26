"""
Full-reserve credit-supply gap -- sizing the quantifiable part, honestly.

THE QUESTION (Wilson's / blackout's frontier): under full reserve, banks no longer
create money by lending; credit is intermediated from real savings (term deposits).
Can intermediation supply enough credit, or does removing money-creation-via-
lending starve credit?

WHAT IS QUANTIFIABLE (this module): the SIZE of the flow intermediation must
replace. It does NOT resolve whether intermediation can meet it -- that is a
genuine, unresolved macro debate (see README and stage2 framing). We size the gap;
we do not fabricate a "credit availability = X%" result, because no empirical
parameter exists to ground one.

EMPIRICAL ANCHORS (verified):
  - ~90% of US broad money (M2) is bank-created deposits, ~10% currency
    (US Dec-2010: M2 8,853B, currency 915.7B). UK/M4 figure is 97% (McLeay et al.,
    BoE 2014; Werner 2005: "similar proportions in most industrialised economies").
    We use 90% (US, conservative).
  - Annual M2 growth from the bundled 1960-2025 series.

The gap = the share of annual broad-money creation currently done by bank lending,
which full reserve removes and intermediation (or CS issuance) must otherwise
supply.
"""
import csv, os, statistics

BANK_SHARE = 0.90   # US bank-created share of M2 (verified; UK/M4 is 0.97)

HIST=os.path.join(os.path.dirname(__file__),'..','..','..','empirical_replication',
                  'data','citizens_standard_historical_data_1960_2025_v2.csv')
rows=[r for r in csv.DictReader(open(HIST))]
for r in rows:
    r['m2']=float(r['m2_billions_usd']); r['gdp']=float(r['gdp_nominal_billions_usd'])

print("="*72)
print("FULL-RESERVE CREDIT GAP -- sizing the flow intermediation must replace")
print("="*72)
print(f"Bank-created share of US broad money (M2): {100*BANK_SHARE:.0f}% (verified)")
print()

# annual M2 growth and the bank-created portion of it, recent decades
print("Annual broad-money creation and the bank-lending share (recent years):")
print(f"  {'year':>5} {'M2 growth $B':>13} {'%GDP':>7} {'bank-created $B':>16} {'%GDP':>7}")
flows=[]
for i in range(len(rows)-10,len(rows)):
    dm2=rows[i]['m2']-rows[i-1]['m2']
    bankflow=BANK_SHARE*dm2
    pctgdp=100*dm2/rows[i]['gdp']
    bankpct=100*bankflow/rows[i]['gdp']
    flows.append((dm2,bankflow,pctgdp,bankpct))
    print(f"  {rows[i]['year']:>5} {dm2:>12.0f} {pctgdp:>6.1f}% {bankflow:>15.0f} {bankpct:>6.1f}%")

# long-run average (exclude COVID spike outliers for the typical figure)
allflows=[]
for i in range(1,len(rows)):
    dm2=rows[i]['m2']-rows[i-1]['m2']
    if rows[i]['gdp']>0:
        allflows.append(100*BANK_SHARE*dm2/rows[i]['gdp'])
med=statistics.median(allflows)
print("-"*72)
print(f"Long-run median bank-created money flow: ~{med:.1f}% of GDP per year")
print(f"  (1960-2025; this is the annual credit-creation flow full reserve removes")
print(f"  and that intermediation -- or CS issuance -- must otherwise supply.)")
print()
print("HOW CS RELATES: CS issuance is growth-matched (G = k2*M2*g), roughly the")
print("real-growth share of M2 per year. That REPLACES part of this bank-created")
print("flow with sovereign issuance, and full reserve routes the rest through")
print("term-deposit intermediation. The gap intermediation must fill is therefore")
print("this bank-created flow MINUS what CS issuance supplies -- a smaller residual,")
print("but still the load-bearing open question (stage2 / README).")

"""
The Citizens Standard — Demographic Equity-Flow Model (v3, corrected accounting)
===============================================================================
Net external absorption (the price-pressure-relevant flow) = issuance into floors
(new money, buying) MINUS retiree consumption withdrawn from them (selling).
Dividends are NOT independent demand: in aggregate a reinvested dividend buys back
exactly the ex-dividend price drop it is funded from (a wash); only consumed
dividends (part of retiree withdrawals) leave the circuit.

Findings (consistent with Macro paper Proposition 2, now dated):
  (1) NET BUYER during the accumulation decades; crosses to NET SELLER around
      year ~55 (varying each parameter alone 43-67; wider under combined extremes) as the retiree stock matures -- the dated form of
      "the structural buyer is also a structural seller in demographic steady state."
  (2) The mature structural outflow is the r>g rebalancing: at a bounded market
      share it equals (r-g) x floor stock -- a few % of GDP/yr, smooth and bounded,
      matched by market growth and the Q-channel; it vanishes when r <= g.
  (3) The flood-as-crash is ruled out (gradual ramp; inheritance prevents a
      death-liquidation spike -- liquidation roughly doubles the mature outflow).
  Inheritance keeps the outflow smooth and bounded; it does NOT make floors
  permanent net buyers.
"""
import numpy as np

def model(n=0.005, g=0.015, r=0.045, w=0.04, retire=65, death=85, M2_GDP=0.74,
          k1_gdppc=0.025, mode='inherit', years=160):
    rg=g+n; A=death; GDP=1.0; POP=1.0
    age=np.array([(1+n)**(-a) for a in range(A)]); age/=age.sum()
    floor=np.zeros(A); out=[]
    for t in range(years):
        GDPpc=GDP/POP; counts=age*POP
        issuance=rg*(M2_GDP*GDP); K1=k1_gdppc*GDPpc*counts[0]
        dep=np.zeros(A); dep[:retire]=((issuance-K1)/counts[:retire].sum())*counts[:retire]; dep[0]+=K1
        floor+=dep; floor*=(1+r)                       # total return grows the stock
        wd=np.zeros(A); wd[retire:]=w*floor[retire:]; floor[retire:]-=wd[retire:]
        ret_consumption=wd[retire:].sum()
        net_abs=issuance-ret_consumption               # issuance in - consumption out
        beq=floor[A-1]; floor[1:]=floor[:-1]; floor[0]=0.0
        if mode=='liquidate': net_abs-=beq             # estate liquidation adds selling
        elif mode=='inherit':
            wc=counts[:retire]; floor[:retire]+=beq*(wc/wc.sum())
        out.append((t, net_abs/GDP*100, floor.sum()/GDP*100))
        GDP*=(1+rg); POP*=(1+n)
    return np.array(out)

if __name__=="__main__":
    tr=model()
    cross=next((int(tr[i][0]) for i in range(len(tr)) if tr[i][1]<0), None)
    print(f"Net absorption (% of GDP): buyer early, seller at maturity. Crossover year {cross}.")
    for y in (20,40,55,65,80,100): print(f"  year {y:>3}: {tr[y][1]:+.2f}% of GDP")
    print("\nBounded steady-state outflow = (r-g)*floor_stock at a capped share:")
    for s in (0.5,1.0,1.8): print(f"  stock capped at {s*100:.0f}% of GDP -> {(0.045-0.02)*s*100:.1f}% of GDP/yr")

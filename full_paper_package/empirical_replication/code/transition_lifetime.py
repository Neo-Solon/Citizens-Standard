# Lifetime real captured value (floor + cumulative KI dividend) under mode transitions,
# built directly on the corrected real-return engine (cs_engine.py logic, ki_C=3.65%).
M2_0, GDP_0, POP_0 = 22366.2e9, 30762.099e9, 341.8e6
RG, PG, HZ = 0.02, 0.005, 65
PRESETS = {
 'A': dict(k1=.025, k2=.175, k3=0, ki=0,     cpi=-.016),
 'B': dict(k1=.025, k2=1.0,  k3=0, ki=0,     cpi=0.0),
 'C': dict(k1=.025, k2=.175, k3=0, ki=.0365, cpi=.02),
}
def lifetime(mode1, mode2=None, switch=30, er=0.045):
    mode2 = mode2 or mode1
    m2,gdp,pop = M2_0,GDP_0,POP_0
    cpiIdx,floorReal,kiCum = 1.0,0.0,0.0
    births = pop*PG
    for t in range(HZ+1):
        p = PRESETS[mode1] if t < switch else PRESETS[mode2]
        gpc=gdp/pop
        k1T=p['k1']*gpc*max(births,0)
        k2Budget=p['k2']*m2*RG
        split=max(0,k2Budget-k1T)
        k2T=split
        kiT=p['ki']*m2
        k1pc=k1T/births if births>0 else 0
        k2pc=k2T/pop
        kipc=kiT/pop
        deposit=(k1pc if t==0 else 0)+k2pc
        floorReal=(floorReal+deposit/cpiIdx)*(1+er)
        kiCum += kipc/cpiIdx
        m2+=k1T+split+kiT
        gdp=gdp*(1+RG)*(1+p['cpi'])
        pop*=(1+PG)
        births=max(0,pop*PG)
        cpiIdx*=(1+p['cpi'])
    return (floorReal+kiCum)/1e3  # $K real

scen = [("Pure A",'A','A'),("Pure B",'B','B'),("Pure C",'C','C'),
        ("A→B@30",'A','B'),("A→C@30",'A','C'),("B→C@30",'B','C'),
        ("C→A@30",'C','A'),("C→B@30",'C','B')]
vals=[]
for name,m1,m2 in scen:
    v=lifetime(m1,m2)
    vals.append(round(v))
    print(f"  {name:9s}: ${v:,.0f}K")
print("\nvals =", [round(v) for v in vals])
print("validation — Pure A/B/C should match 160/745/420:", [round(lifetime(m,m)) for m in 'ABC'])

# Faithful Python port of the corrected Citizens Standard engine simulate()
M2_0, GDP_0, POP_0 = 22366.2e9, 30762.099e9, 341.8e6
RG, PG, HZ = 0.02, 0.005, 65
# Gross new-citizen rate (births + pro-rated naturalizations), ~1.17% of population.
# This is the K1 recipient base, NOT net population growth (PG=0.5%): K1 is an endowment
# to every new citizen, a far larger flow than the net change in headcount. Reproduces
# the paper's $9B launch-year K1.
NC = 0.011703
PRESETS = {
 'A': dict(k1=.025, k2=.175, k3=0,  ki=0),
 'B': dict(k1=.025, k2=1.0,  k3=0,  ki=0),
 'C': dict(k1=.025, k2=.175, k3=0,  ki=.0365),
}
def derive_cpi(p):
    # Inflation is DERIVED, not rounded/dialed: it equals the total issuance rate minus
    # real growth. K1/K2 at most match real growth (full-rate K2 = price stability);
    # K3 only reallocates within the K2 budget (price-neutral); only KI adds issuance
    # above the growth line. No rounding.
    k1Share = p['k1']*(GDP_0/M2_0)*NC
    return max(k1Share, p['k2']*RG) + p['ki'] - RG
def simulate(mode, er=0.045):
    p=PRESETS[mode]
    p=dict(p, cpi=derive_cpi(p))
    m2,gdp,pop=M2_0,GDP_0,POP_0
    cpiIdx,floorReal,k3Cum=1.0,0.0,0.0
    newcit=pop*NC
    Y=[]
    for t in range(HZ+1):
        gpc=gdp/pop
        k1T=p['k1']*gpc*max(newcit,0)
        k2Budget=p['k2']*m2*RG
        split=max(0,k2Budget-k1T)
        k3T=p['k3']*split
        k2T=split-k3T
        kiT=p['ki']*m2
        k1pc=k1T/newcit if newcit>0 else 0
        k2pc=k2T/pop
        k3pc=k3T/pop
        kipc=kiT/pop
        deposit=(k1pc if t==0 else 0)+k2pc
        depositReal=deposit/cpiIdx
        floorReal=(floorReal+depositReal)*(1+er)
        k3Cum+=k3pc/cpiIdx
        Y.append(dict(t=t,floorReal=floorReal,cpiIdx=cpiIdx,m2=m2,
                      kiReal=kipc/cpiIdx,k3Real=k3pc/cpiIdx,
                      k1pc=k1pc,k2pc=k2pc))
        m2+=k1T+split+kiT
        gdp=gdp*(1+RG)*(1+p['cpi'])
        pop*=(1+PG)
        newcit=max(0,pop*NC)
        cpiIdx*=(1+p['cpi'])
    return Y
if __name__=="__main__":
    for er in (0.03,0.045,0.065):
        r={m:simulate(m,er)[-1]['floorReal'] for m in 'ABC'}
        print(f"er={er}: A=${r['A']/1e3:.0f}K B=${r['B']/1e3:.0f}K C=${r['C']/1e3:.0f}K")
    # cumulative KI real for Mode C
    c=simulate('C'); kiCum=sum(y['kiReal'] for y in c)
    print(f"Mode C cumulative KI real: ${kiCum/1e3:.0f}K ; C lifetime = ${(c[-1]['floorReal']+kiCum)/1e3:.0f}K")

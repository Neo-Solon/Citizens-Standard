# Correct deflation: FLOOR = equity (regime-independent real), KI = spent stream (deflate at mode CPI).
M2_0,GDP_0,POP_0,RG,PG,HZ,NC = 22366.2e9,30762.099e9,341.8e6,0.02,0.005,65,0.011703
def run(mode):
    cfg={'A':dict(k2=.175,ki=0,cpi=-0.0186,er=0.054),
         'B':dict(k2=1.0, ki=0,cpi=0.0,    er=0.043,k3=0.40),
         'C':dict(k2=.175,ki=.0198,cpi=0.02,er=0.054)}[mode]
    k3share=cfg.get('k3',0.0)
    m2,gdp,pop=M2_0,GDP_0,POP_0
    realIdx=1.0   # real-GDP deflator path (regime-INDEPENDENT): grows at RG
    cpiIdx=1.0    # actual price path (mode CPI) for spent streams
    floorReal=0.0; kiReal=0.0; k3Real=0.0; kiNom=0.0
    newcit=pop*NC
    for t in range(HZ+1):
        k1T=.025*(gdp/pop)*max(newcit,0)
        k2Budget=cfg['k2']*m2*RG
        split=max(0,k2Budget-k1T)
        k3T=k3share*split; k2T=split-k3T; kiT=cfg['ki']*m2
        # FLOOR deposits -> real via REAL-GDP path (regime-independent equity)
        depReal=((k1T if t==0 else 0)+k2T)/pop/realIdx
        floorReal=(floorReal+depReal)*(1+cfg['er'])
        # KI / K3 spent streams -> real via ACTUAL CPI path
        kiNom+=kiT/pop
        kiReal+=(kiT/pop)/cpiIdx
        k3Real+=(k3T/pop)/cpiIdx
        m2+=k1T+split+kiT
        gdp=gdp*(1+RG)*(1+cfg['cpi'])
        pop*=(1+PG); newcit=max(0,pop*NC)
        realIdx*=(1+RG); cpiIdx*=(1+cfg['cpi'])
    return floorReal,kiReal,kiNom,k3Real
for m in 'ABC':
    f,ki,kin,k3=run(m)
    print(f"Mode {m}: floor=${f/1e3:.0f}K  KIreal=${ki/1e3:.0f}K  KInom=${kin/1e3:.0f}K  K3real=${k3/1e3:.0f}K  total_real=${(f+ki+k3)/1e3:.0f}K")
print("\nPAPER: A floor ~$233K | B floor ~$413K+K3 | C floor ~$230K + KI(nom $142K) | lifetime real C ~?")

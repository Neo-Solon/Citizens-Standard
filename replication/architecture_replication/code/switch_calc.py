# Faithful GE mode-switch lifetime-value calc, built on cs_engine constants.
import cs_engine as E
M2_0,GDP_0,POP_0,RG,PG,HZ,NC = E.M2_0,E.GDP_0,E.POP_0,E.RG,E.PG,E.HZ,E.NC
# GE presets: Mode B is 60/40 (k3=0.40 -> 60% of split to floor); er = realizable return by mode
GE = {
 'A': dict(k1=.025,k2=.175,k3=0,   ki=0,     er=0.054),
 'B': dict(k1=.025,k2=1.0, k3=0.40, ki=0,     er=0.043),
 'C': dict(k1=.025,k2=.175,k3=0,   ki=.0198, er=0.054),
}
def cpi_of(p): return max(p['k1']*(GDP_0/M2_0)*NC, p['k2']*RG)+p['ki']-RG
def lifetime(schedule):
    """schedule: list of 65 mode letters (one per year). Returns floor, k3cum, kicum, total."""
    m2,gdp,pop=M2_0,GDP_0,POP_0; cpiIdx,floorReal,k3Cum,kiCum=1.0,0.0,0.0,0.0
    newcit=pop*NC
    for t in range(HZ+1):
        p=GE[schedule[min(t,len(schedule)-1)]]; cpi=cpi_of(p); er=p['er']
        gpc=gdp/pop
        k1T=p['k1']*gpc*max(newcit,0)
        k2Budget=p['k2']*m2*RG
        split=max(0,k2Budget-k1T)
        k3T=p['k3']*split; k2T=split-k3T; kiT=p['ki']*m2
        k1pc=k1T/newcit if newcit>0 else 0
        k2pc=k2T/pop; k3pc=k3T/pop; kipc=kiT/pop
        deposit=(k1pc if t==0 else 0)+k2pc
        floorReal=(floorReal+deposit/cpiIdx)*(1+er)
        k3Cum+=k3pc/cpiIdx; kiCum+=kipc/cpiIdx
        m2+=k1T+split+kiT; gdp=gdp*(1+RG)*(1+cpi); pop*=(1+PG); newcit=max(0,pop*NC); cpiIdx*=(1+cpi)
    return floorReal,k3Cum,kiCum,floorReal+k3Cum+kiCum
def sched(m1,m2=None,switch=30):
    return [m1 if t<switch else (m2 or m1) for t in range(HZ+1)]

# Pure modes
for m in ['A','B','C']:
    f,k3,ki,tot=lifetime(sched(m))
    print(f"Pure {m}: floor=${f/1e3:.0f}K  K3cum=${k3/1e3:.0f}K  KIcum=${ki/1e3:.0f}K  total=${tot/1e3:.0f}K")
print("---- transitions (switch at yr 30) ----")
for a,b in [('A','B'),('A','C'),('B','C'),('C','A'),('C','B')]:
    f,k3,ki,tot=lifetime(sched(a,b))
    print(f"{a}->{b}@30: floor=${f/1e3:.0f}K  K3cum=${k3/1e3:.0f}K  KIcum=${ki/1e3:.0f}K  total=${tot/1e3:.0f}K")

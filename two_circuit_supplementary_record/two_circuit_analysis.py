"""
Two-circuit (transactional vs asset) empirical extension — 2026-07-10.
Independent robustness work extending Paper 10. NOT a paper claim.
Builds a clean dollar MA series and runs cross-country/cross-measure regime tests.
Requires (FRED/CFS CSVs): CURRSL, DEMDEPSL, M2SL, CPIAUCSL, divisia_dm1,
WSAVNS, MDLM (savings splice), STDSL, MANMM101USM189S, MANMM101JPM189S, JPNCPIALLMINMEI.
"""
import pandas as pd, numpy as np
def load(f,n):
    d=pd.read_csv(f); d=d.rename(columns={d.columns[0]:'date',d.columns[-1]:n})
    d['date']=pd.to_datetime(d['date']); return d[['date',n]]

# ---- clean dollar MA: savings (WSAVNS pre-2020 spliced to MDLM post) + small-time (STDSL) ----
def build_MA():
    wsav=load('WSAVNS.csv','WSAVNS'); mdlm=load('MDLM.csv','MDLM'); std=load('STDSL.csv','STDSL')
    wsav['ym']=wsav['date'].dt.to_period('M')
    wm=wsav.groupby('ym')['WSAVNS'].mean().reset_index(); wm['date']=wm['ym'].dt.to_timestamp(); wm=wm[['date','WSAVNS']]
    w_mar=wm[wm['date']=='2020-03-01']['WSAVNS'].values[0]; w_apr=wm[wm['date']=='2020-04-01']['WSAVNS'].values[0]
    m_may=mdlm[mdlm['date']=='2020-05-01']['MDLM'].values[0]
    splice=m_may/(w_apr*(w_apr/w_mar))              # seam-adjust for the May-2020 M1 reclassification
    wm['SAV']=wm['WSAVNS']*splice
    pre=wm[wm['date']<'2020-05-01'][['date','SAV']]
    post=mdlm[mdlm['date']>='2020-05-01'].rename(columns={'MDLM':'SAV'})
    sav=pd.concat([pre,post]).sort_values('date')
    ma=sav.merge(std,on='date'); ma['MA']=ma['SAV']+ma['STDSL']
    return ma, splice

# ---- regime test: narrow money -> next-yr CPI, non-overlapping annual, regime-split ----
def regime_test(nm,cpi):
    d=nm.merge(cpi,on='date').sort_values('date')
    d['nm_g']=d['NM'].pct_change(12)*100; d['infl']=d['CPI'].pct_change(12)*100
    d['infl_fwd']=d['CPI'].pct_change(12).shift(-12)*100
    d=d.dropna(subset=['nm_g','infl_fwd','infl']); ann=d.iloc[::12,:]
    r2=lambda s: np.corrcoef(s['nm_g'],s['infl_fwd'])[0,1]**2 if len(s)>=6 else None
    med=ann['infl'].median()
    return dict(n=len(ann), all=r2(ann), above=r2(ann[ann['infl']>=med]), below=r2(ann[ann['infl']<med]))

if __name__=='__main__':
    ma,splice=build_MA(); ma.to_csv('MA_series.csv',index=False)
    print('MA built, splice factor', round(splice,3), 'n', len(ma))
    us=regime_test(load('MANMM101USM189S.csv','NM'), load('CPIAUCSL.csv','CPI'))
    jp=regime_test(load('MANMM101JPM189S.csv','NM'), load('JPNCPIALLMINMEI.csv','CPI'))
    print('US OECD-narrow regime:', us)
    print('JP OECD-narrow regime:', jp)

def japan_horserace():
    """Japan narrow (MANMM101) vs broad (MABMM301) -> own next-yr CPI, non-overlapping annual."""
    nm=load('MANMM101JPM189S.csv','NM'); bm=load('MABMM301JPM189S.csv','BM'); cpi=load('JPNCPIALLMINMEI.csv','CPI')
    d=nm.merge(bm,on='date').merge(cpi,on='date').sort_values('date')
    d['nm_g']=d['NM'].pct_change(12)*100; d['bm_g']=d['BM'].pct_change(12)*100
    d['infl']=d['CPI'].pct_change(12)*100; d['infl_fwd']=d['CPI'].pct_change(12).shift(-12)*100
    d=d.dropna(subset=['nm_g','bm_g','infl','infl_fwd']); ann=d.iloc[::12,:]
    r2=lambda s,c: np.corrcoef(s[c],s['infl_fwd'])[0,1]**2 if len(s)>=6 else None
    med=ann['infl'].median()
    return dict(n=len(ann), med_infl=round(med,1),
        all=(round(r2(ann,'nm_g'),3),round(r2(ann,'bm_g'),3)),
        above=(round(r2(ann[ann['infl']>=med],'nm_g'),3),round(r2(ann[ann['infl']>=med],'bm_g'),3)),
        below=(round(r2(ann[ann['infl']<med],'nm_g'),3),round(r2(ann[ann['infl']<med],'bm_g'),3)))

if __name__=='__main__':
    print('Japan narrow-vs-broad (narrow_R2, broad_R2):', japan_horserace())

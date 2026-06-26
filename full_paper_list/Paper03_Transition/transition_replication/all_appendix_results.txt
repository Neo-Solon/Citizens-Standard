
##############################################################################
# A.2  Debt trajectory
##############################################################################
==============================================================================
APPENDIX A.2 — PUBLIC-DEBT-TO-GDP TRAJECTORY UNDER MODE T
==============================================================================
Public debt: $31.4T (102% of GDP); gross $39T; intragov $7.6T (nets out)
KT calibration: 1.5% of M2/yr; retires public debt to a
~15%-of-GDP operational floor (~Year 45), where it stabilizes.

Year  Coupon   KT ($B)   Surplus($B)  Interest($B)  Debt ($T)   D/GDP   
------------------------------------------------------------------------------
0      4.50%   $   336    $       0    $     1413     $   31.4       102%
10     1.50%   $   402    $     184    $      466     $   31.0        84%
20     1.50%   $   480    $     440    $      422     $   28.2        64%
30     1.50%   $   574    $     788    $      311     $   20.7        39%
40     1.50%   $    53    $     942    $      152     $   10.1        16%
45     1.50%   $     0    $    1030    $      152     $   10.1        15%

Operational floor (~15% of GDP) reached by ~Year 45 (D/GDP 16% at Yr40, 15% at Yr45, stabilizes)
Cumulative KT issuance:  $17.7T
(remainder retired by primary surplus and nominal output growth)

vs CBO March 2025 projection: 156% of GDP by 2055 under current law.

##############################################################################
# A.2  KT inflation
##############################################################################
==============================================================================
APPENDIX A.2.3 — KT CONSUMER-PRICE IMPACT
==============================================================================
KT annual issuance at launch: $336B (1.5% of M2)

Holder class            Share   MPC    Rationale
------------------------------------------------------------------------------
Foreign central banks     30%     0%   FX-reserve mandate; rotate to other sovereigns
Pension funds             15%     0%   Liability-matched; reinvest in fixed income/equity
Federal Reserve           14%     0%   Balance-sheet runoff; spends nothing
Mutual funds / ETFs       12%     2%   Mandate-bound; minimal leakage to consumption
Banks / insurance         12%     3%   Regulatory capital; reinvest
State / local govt         7%     5%   Mostly reinvest
Households                10%    15%   Some consumption out of redemption
------------------------------------------------------------------------------
BLENDED MPC                     2.5%

CPI Scenario                MPC     KT spent/yr   CPI impact
----------------------------------------------------------------
Full reinvestment (0%)       0.0%   $     0B       +0.00pp
Expected (blended ~2.5%)     2.5%   $     8B       +0.03pp
Pessimistic (15%)           15.0%   $    50B       +0.16pp
Extreme (50%)               50.0%   $   168B       +0.55pp

KT is self-throttling: calibration to a price-level path automatically
reduces issuance if consumer inflation rises. Cannot produce runaway
inflation by construction.

##############################################################################
# A.3  Banking + KT synergy
##############################################################################
==============================================================================
APPENDIX A.3 — BANKING SEPARATION AND KT SYNERGY
==============================================================================
Total deposits: $18T | reserve gap: $16.2T | credit-at-risk: $810B/yr over 20yr

M2 composition through the transition (total grows; inside -> outside):
Year  M2 ($T)   Inside ($T)  Outside ($T)  KT ($B)   Note
------------------------------------------------------------------------------
0       22.4       17.9          4.5         336     Pre-banking-transition
5       24.5       19.6          4.9         367     Pre-banking-transition
10      26.8       21.4          5.4         402     Pre-banking-transition
15      29.3       23.4          5.9         439     Pre-banking-transition
20      32.0       25.6          6.4         480     Converting (0% done)
25      35.0       21.0         14.0         525     Converting (25% done)
30      38.3       15.3         23.0         574     Converting (50% done)
35      41.8        8.4         33.5         627     Converting (75% done)
40      45.7        0.0         45.7         686     Converting (100% done)
45      50.0        0.0         50.0         750     Full reserve complete

KT offset of credit-at-risk (Years 20-40 overlap):
Year  Credit-at-risk ($B)   Domestic KT ($B)    Offset
----------------------------------------------------------------
20    $   810              $   336              41%
25    $   810              $   367              45%
30    $   810              $   402              50%
35    $   810              $   439              54%
40    $   810              $   480              59%

KT offsets 41-59% of annual credit-at-risk,
complementary to the Transition Lending Facility's 12-38% coverage.
The two mechanisms are complementary: KT supplies outside-money creation
precisely as full-reserve conversion removes inside-money creation.

##############################################################################
# A.4  Equity rotation
##############################################################################
==============================================================================
APPENDIX A.4 — EQUITY ROTATION AND RETURN COMPRESSION
==============================================================================
Holder class            Share   Eq-rotation  
--------------------------------------------------
Foreign central banks     30%      5%
Pension funds             15%     40%
Federal Reserve           14%      0%
Mutual funds / ETFs       12%     30%
Banks / insurance         12%     10%
State / local govt         7%     15%
Households                10%     35%
--------------------------------------------------
WEIGHTED ROTATION ESTIMATE        16.8%
(roughly half the original unsourced 35% guess; the two largest
 holders -- foreign CBs and the Fed -- rotate almost nothing)

Rotation    Bond->Eq ($B)   Combined ($B)   % of mkt cap  Compression
------------------------------------------------------------------------
15.0%       $    50          $   322           0.47%        +0.22pp
16.8%       $    57          $   329           0.48%        +0.25pp  <- central
35.0%       $   118          $   390           0.56%        +0.51pp

For comparison: 401k+IRA contributions ~1.1% of mkt cap/yr; QE peak ~2.1%.
Combined transition-era equity demand ~0.48% of market cap at central rotation
(peaks ~0.57% across 15-35%; Stable Floor flow alone ~0.39% under the 60/40 split);
permanent SF flow is a steady-state feature, not a transition cost.
Transition-specific compression ~0.4-0.6pp (KT-rotation driven), reverting
to baseline once KT sunsets. The precise rotation fraction is an open
empirical question; results are robust across the 15-35% range.

##############################################################################
# A.4.4 Rotation sensitivity
##############################################################################
==============================================================================
APPENDIX A.4.4 -- ROTATION SENSITIVITY AND HISTORICAL GROUNDING
==============================================================================

PART 1 -- SENSITIVITY OF THE EQUITY EFFECT TO THE ROTATION FRACTION
------------------------------------------------------------------------------
Rotation    Bond->Eq ($B)   Combined ($B)   % of mkt cap  Compression   
------------------------------------------------------------------------------
  15%       $    50          $   322           0.47%        +0.22pp
  17%       $    57          $   329           0.48%        +0.25pp  <- central
  25%       $    84          $   356           0.52%        +0.37pp
  35%       $   118          $   390           0.56%        +0.51pp
------------------------------------------------------------------------------
Across the full 15-35% range:
  Combined equity demand: 0.47% -> 0.56% of market cap (spread 0.10pp)
  Forward return compression: +0.22pp -> +0.51pp (both transient; revert once KT sunsets)
  For comparison: 401k+IRA contributions ~1.4% of mkt cap/yr; QE peak ~2.6%.

  Stress beyond the assumed range:
    rotation 50%: combined 0.64% of mkt cap, compression +0.73pp
    rotation 75%: combined 0.76% of mkt cap, compression +1.10pp

  INVARIANT QUANTITIES (independent of rotation fraction):
    - Debt trajectory: 102% -> ~15% operational floor by ~Year 45 (solvency is an
      asset-swap arithmetic; freed-capital allocation does not enter it)
    - KT consumer-price neutrality: redemption MPC analysis (A.2) is
      unaffected by the equity/bond split of reinvested proceeds

PART 2 -- HISTORICAL GROUNDING (large sovereign-debt reductions)
------------------------------------------------------------------------------
Episode                     Peak D/GDP  End D/GDP  Horizon  Equity bubble?
------------------------------------------------------------------------------
UK post-WWII (1946-1976)      250%        50%       30yr    no
Canada 1990s (1995-2000)       68%        50%        5yr    no
------------------------------------------------------------------------------
  UK post-WWII (1946-1976):
    mechanism: nominal growth > interest rate (negative growth-corrected rate); modest primary surpluses ~1.6% of GDP/yr; financial repression
    Capital reabsorbed across gilts, savings products, and real economy; no equity bubble attributable to debt reduction.
  Canada 1990s (1995-2000):
    mechanism: large primary surpluses via spending cuts (~6-7:1 cuts:taxes); sustained nominal growth
    Released capital flowed to private investment broadly; no destabilising equity concentration.

  LESSON: In both episodes, capital released by retiring a large
  sovereign-debt stock was reabsorbed across the full asset spectrum
  without a destabilising equity concentration. The work was done by
  a negative growth-corrected interest rate (nominal growth exceeding
  the average coupon) plus primary surpluses -- the same lever KT
  relies on. This supports a rotation fraction at the LOW end of the
  15-35% range, making the paper's central ~17% conservative.

==============================================================================
CONCLUSION: The debt-retirement trajectory and KT's consumer-price
neutrality are robust across (and well beyond) the 15-35% rotation
range. The rotation fraction governs only the magnitude of a
transient, reverting equity-valuation effect that accrues largely to
citizen Stable Floors. Historical precedent places the realistic
fraction at the low end, so the central estimate is conservative.
==============================================================================

##############################################################################
# A.5  Mode T-stable
##############################################################################
==============================================================================
APPENDIX A.5 — MODE T-STABLE CONTINUITY
==============================================================================
Continuity of citizen accumulation across the KT sunset:
  K2 per citizen BEFORE sunset (Mode T):        $2,007/yr
  K2 per citizen AFTER sunset (Mode T-stable):  $2,007/yr
  -> IDENTICAL. KT never deposited into citizen accounts, so its
     deactivation is invisible to Stable Floor accumulation.

Price-level path under residual K1-funded K2 (money grows at real-output rate):
  Year  M2 growth   Real growth   Price level
  ----------------------------------------------
  0        1.8%        1.8%       1.000
  10       1.8%        1.8%       1.000
  20       1.8%        1.8%       1.000
  30       1.8%        1.8%       1.000
  40       1.8%        1.8%       1.000
  50       1.8%        1.8%       1.000

  Price level stays at 1.000 indefinitely: Mode T-stable is a sound
  permanent steady state, not a temporary bridge.

Constitutional lock credibility (Appendix A.5): three conditions --
  electoral majority of account holders, a completed market cycle, and
  politically legible balances -- converge in the Year 38-45 window,
  consistent with the durability timelines of Social Security (~25-30
  years) and Medicare (~15-20 years) post-enactment.

==============================================================================
All appendix modules reproduced. See AUDIT.md for the validation table.
==============================================================================

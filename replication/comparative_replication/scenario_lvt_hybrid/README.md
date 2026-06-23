# Scenario: a worked Georgist-LVT / Citizens-Standard hybrid

**This is an ILLUSTRATIVE SCENARIO, not part of the audited comparative replication.**

Paper 13 establishes that Georgist land-value taxation (LVT) and the Citizens Standard (CS) are
complementary rather than rival: LVT is a *funding source*, CS a *distribution architecture*, and a
land tax could fund a CS dividend. This folder works that complementarity into quantified scenarios.

It is kept separate from the audited results on purpose. Every other figure in
`comparative_replication/` is sourced to a primary reference (see `../AUDIT.md`). The exhibits here
instead rest on **external, contested** estimates of US land rent — the conservative-to-aggressive
spread is roughly fourfold — so they are scenario illustrations, **not** measured results, and must
not be read with the confidence of the Paper-13 comparison tables.

## Run

    python3 lvt_hybrid.py      # prints the magnitudes, writes figures/*.png

## What it shows (and the caveats baked in)

1. **LVT is the larger, more efficient revenue base.** Even at 70% capture the central land-rent
   estimate yields a per-person dividend several times the CS monetary dividend ($516–$2,388/yr).
2. **Capitalization.** The dividend rides the *rent flow* (stable), while the land *price* collapses
   as the rate rises — a feature for Georgism, not a base that self-erodes. The fundamental rent is
   derived internally as R = i·(land value), which is deliberately conservative.
3. **The Mode-D hybrid drops the equity buyer.** CS buys a broad equity index in Modes A/B/C but
   buys none in Mode D (κ_d = 100%). An LVT land dividend + a Mode-D monetary dividend gives two
   clean flows with no sovereign equity bid — at the cost of the locked wealth stock the floor modes
   build. The equity-buyer distortion is about *buying assets*, not how the buying is funded.
4. **Two-way complementarity.** LVT suppresses land speculation and supports productive growth — the
   assumption CS most depends on. And CS full-reserve banking removes the *monetary* amplification of
   a land-price fall (no deposit-money contraction), so a phased LVT transition is far safer and can
   run roughly twice as fast as under fractional reserve. The specific tolerable-decline thresholds
   are illustrative judgment calls, stated as such.
5. **No land conflict.** The direct REIT overlap is ~1.5% of US land (and vanishes in Mode D); the
   one channel that runs against Georgism — CS compressing equity yields could push capital into land
   — is itself neutralized by the LVT, which makes land an unattractive store of value. Net: the two
   systems are self-reinforcing on land.

## Key external inputs and sources

- US land value ~$48T: STATED ASSUMPTION extrapolated from BEA $23T (2009, Larson) and Case $34.7T
  (2005); no authoritative 2026 figure exists. The dividend scales directly with this.
- Land rent: Lincoln Inst. (Barker) ~13.6% of personal income; Georgist sources 20–40% of GDP
  (contested). Central case derived internally as R = i·(land value) (~$2.4T, ~8.3% of GDP).
- Land yield i ~5% (Baa-based, Barker); current Baa ~6%; carried as a 4–6% assumption.
- Real-estate sector ~2.5–3% of the broad US equity index (S&P DJI / GICS, 2026).
- Real-estate-secured loans ~$5.76T of ~$12.5T US bank loans ≈ 45% (FRED H.8 REALLN, Dec 2025).
- CS dividend $516–$2,388/person/yr; wealth floor $233k–$413k/person; mode index-buying behavior:
  Paper 13 and the engine presets (verified).

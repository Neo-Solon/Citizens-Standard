# Engine execution verification — 2026-07-05

A one-time execution check of `Citizens_Standard_Engine.html`, recorded as dated
provenance. This is a statement of what was true as of the check, not a regression
test to be maintained (the engine may change; brittle harnesses pinned to its
current structure would rot).

## Method
The engine's actual HTML + JavaScript was executed against a real DOM using Node
v22 + jsdom, with the real Chart.js 4.4.1 library injected locally (the page loads
Chart.js from a CDN that was unavailable in the check environment, so a local copy
was substituted for execution only — the engine file itself was not modified).
This runs the real code end-to-end, not a mock.

## What was verified (passed)
- Engine loads and initializes with ZERO script errors; Chart.js loads.
- All 10 tabs execute their render path without error, including the three
  previously unconfirmed ones: Stable Floor, Mode Ω, and μ & Stability.
  Their view containers (omega-view, mu-view, compare-view) exist and toggle.
- Compare-first is the default view ("What you get" active on load).
- All 7 mode buttons (A, B, C, D, O, Z, X) execute without error.
- Canonical US values render correctly: Stable Floor $421K; Mode B 100.0% (k2=1);
  Mode C 1.98% (KI rate); Mode D 51.4%.
- No NaN/undefined/Infinity in any visible readout text node (an apparent NaN was
  traced to chart-internal data, not user-facing output).

## What this does NOT verify (still needs a human in a real browser)
jsdom builds and manipulates the DOM but performs NO visual layout or painting.
Chart.js draws to <canvas>, which jsdom does not paint. So the VISUAL layer is
untested: whether chart lines/SVG actually appear in the right positions, colors,
spacing, responsive layout, and the Stable Floor lines being visibly drawn.

## Net status
The engine moved from "logic verified in isolation, rendering unverified" to
"executes correctly end-to-end against a real DOM with correct values and no
errors." The remaining gap is specifically the visual paint step, which only a
real-browser check (Chrome/Firefox) can close.

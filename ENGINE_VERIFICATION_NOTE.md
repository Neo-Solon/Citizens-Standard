# Engine execution verification — 2026-07-07

A one-time execution check of `Citizens_Standard_Engine.html`, recorded as dated
provenance. This is a statement of what was true as of the check, not a regression
test to be maintained (the engine may change; brittle harnesses pinned to its
current structure would rot). This check supersedes the 2026-07-05 note: the engine
was edited after that date (Mode T debt-band recalibration), so the earlier note's
canonical values no longer describe the current file.

## Method
The engine's actual HTML + JavaScript was executed against a real DOM using Node
v22 + jsdom, with the real Chart.js 4.4.1 library injected locally (the page loads
Chart.js from a CDN that was unavailable in the check environment, so a local copy
was substituted for execution only — the engine file itself was not modified).
This runs the real code end-to-end, not a mock.

## What was verified (passed)
- Engine loads and initializes with ZERO script errors; Chart.js loads.
- All 10 tabs execute their render path without error, including Stable Floor,
  Mode Ω, and μ & Stability. Their view containers (omega-view, mu-view,
  compare-view) exist and toggle.
- All 7 mode buttons (A, B, C, D, Ω, 0/Zero-Issuance, Custom) execute without error.
- Canonical US values render correctly, including the Mode B Stable Floor (~$413K,
  matching the Architecture paper's realizable-basis figure) and the Mode A/C
  floors (~$233K / ~$230K).
- Mode T debt controls reflect the Transition paper's operational band: the debt
  band target defaults to 45% of GDP (central path) on a 0–60% range, replacing
  the superseded ~15% operational floor.
- No NaN/undefined/Infinity in any visible (non-script) text node after clicking
  every mode button and every tab.

## What this does NOT verify (still needs a human in a real browser)
jsdom builds and manipulates the DOM but performs NO visual layout or painting.
Chart.js draws to <canvas>, which jsdom does not paint. So the VISUAL layer is
untested: whether chart lines/SVG actually appear in the right positions, colors,
spacing, responsive layout, and the Stable Floor lines being visibly drawn.

## Net status
The current engine (with the Mode T band recalibration) executes correctly
end-to-end against a real DOM with correct values and no errors. The remaining gap
is specifically the visual paint step, which only a real-browser check
(Chrome/Firefox) can close.

# Little North

**A tiny fox. An enormous winter world.**

A warm, cozy third-person Arctic exploration game in the making. Working title **Little North**. Current phase: **A01 — Sculpted Arctic Storybook Art Calibration**.

## What is implemented in this prototype?
- A small explorable Three.js winter vignette, for desktop and touch.
- Hand-authored procedural snow-laden spruce with layered foliage/snow and low-draw-call batching.
- Snowy heightfield, atmospheric winter lighting, spruce grove, rocks, ice, distant mountain backdrop.
- Cozy cabin, chimney smoke, warm window lighting.
- A white arctic fox **character proxy** with simple gait animation and follow camera (not final sculpt).
- An independent tree sculpture review viewer at `/sculpt.html` (1–4 locks the viewing angle).
- Live scene statistics with **P**, plus touch joystick and hop control.

## Run

```bash
npm install
npm run dev
```

Open the dev-server URL. Alternatively, serve the root via any static HTTP server: the HTML import maps resolve `three@0.180.0` from jsDelivr. **Internet is required for these static import-map previews**. In a standard Vite setup the local `three` dependency is installed by npm instead.

> Only an art study, not the full island or 60-minute game. The appearance has not yet passed browser visual review; check `docs/IMG2THREE_STUDY.md` before accepting any asset.

## Controls

Desktop: WASD/arrow keys to move, Shift run, Space hop, drag to orbit, mouse wheel zoom, P diagnostics, Reset. Mobile: left joystick, Hop button, drag right/center to look.

## Design contract
See `docs/ART_DIRECTION.md` and `docs/IMG2THREE_STUDY.md`. Quality targets: stylized but crafted (not generic low-poly), coherent geometry from all angles, compact real-time WebGL for future Android browser use.

## Browser QA

A dedicated GitHub Actions workflow (`.github/workflows/qa.yml`) runs syntax checks, a Vite build, and six Chromium screenshots (desktop, mobile and the four spruce angles). The resulting evidence is uploaded as an artifact on the PR run. Pass/fail must be checked in Actions; merely committing the workflow does **not** demonstrate a pass.

## Live preview via GitHub Pages (A01 review, not production acceptance)
The GitHub repository is currently **public**. For the fastest browser/mobile review, configure the Pages source manually once:
1. Repository Settings > Pages > **Deploy from a branch**.
2. Branch: `phase-a01-art-calibration`; folder: `/(root)`; Save.
3. Visit https://algolon.github.io/Little-North/ (world) and https://algolon.github.io/Little-North/sculpt.html (four-angle spruce study).

This temporary preview intentionally publishes the *working review branch*, without merging PR #1. It serves the source files directly and uses the pinned CDN import map for Three.js; an internet connection is required. A root-level `.nojekyll` prevents Jekyll from altering the source. Pages publishing status and availability MUST be verified in the GitHub Pages settings / Actions.
After A01 acceptance, replace branch-source publishing with a Vite build-and-deploy Actions workflow, pinned dependencies and production quality gates.

**Acceptance is separate from deploy**: publishing a preview does not imply art direction approval.

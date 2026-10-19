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

## Deployment
The repository is private. GitHub Pages visibility/deployment depends on the account/repository settings. The candidate must be visually reviewed before a production deployment. No deployment is configured by this branch.

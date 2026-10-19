# LN-A01a — Playability Base / Controller & Camera

**Scope:** input, locomotion, jumping, camera, basic collisions and regression QA. Fox mesh, trees, cabin and material style unchanged.

## Root problems diagnosed
- Old horizontal movement was a continuous lerp with coupled input and no explicit stop/acceleration contract.
- Mouse/touch orbit and fox heading were coupled only loosely; camera had no ground clearance correction.
- The old jump consumed Space in an animation frame and key autorepeat could enqueue further jumps.
- There was no wall/tree collision; fox could walk through the cabin.
- No automated behavioral tests existed (only screenshots).

## Implemented / intended behavior
- World movement relative to camera heading; W = away from viewer; A/D strafes relative to viewpoint while fox turns smoothly to travel direction.
- 3.8m/s walk, 6.1m/s run; acceleration 22m/s², braking 25m/s², air control 5.5m/s².
- Jump: 5.25m/s impulse under 14m/s² gravity. One jump per distinct press; 120ms input buffer, 110ms coyote time.
- Camera: damped follow position and look target, yaw/pitch orbit, distance 5.1–12m; terrain clearance and basic ground line-of-sight.
- Basic non-penetrating cabin/hero-tree obstacles; no full rigid-body physics yet. Terrain handled by height sampling.
- Desktop WASD/arrows/Shift/Space; drag to orbit, wheel zoom, R or RESET to reset.
- Mobile left joystick, right-side drag on world to orbit, HOP. Pointer capture and blur/visibility input release.
- Live P diagnostics reports actual renderer.draw calls and triangles rather than approximating draw calls from object count.
- QA probes exposed only when `?qa=1` is present.

## Validation requirements
1. `npm run test:syntax`
2. `npm run test:movement`: Node's deterministic tests (forward-relative, stop/brake, jump/landing, buffer, obstacles, slope and FPS resilience).
3. `npm run build`
4. `npm run visual:qa`: existing desktop/mobile and sculpt screenshots.
5. `npm run qa:controller`: automated Chromium desktop & emulated-mobile inputs with state verification and screenshots.
6. **Device review required**: Android touch sensitivity and browser performance cannot be fully certified from emulated Chromium.

## Limits / next steps
- Fixed camera smoothing and ground clearance do not provide fully robust camera/object occlusion (e.g. looking through cabin walls); defer to a later bounded camera-collision pass if reproduced.
- Hero assets and animated fox body are proxies; no art decisions here.
- If a player finds walking/turning unnatural, collect a 10–20 second device recording showing input and camera, then calibrate speed, damping, orbit response and camera distance based on evidence.

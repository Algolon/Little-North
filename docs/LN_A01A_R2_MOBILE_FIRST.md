# LN-A01a-R2 · Mobile-first third-person locomotion / root cause and acceptance

**Working asset**: Arctic fox character proxy. No fox-art redesign or environment-art changes in this scope.
**Source evidence**: owner's real Samsung/Android portrait recording, 19.4 s, provided in chat 19 Oct 2026. Do not commit the recording to the public repo.

## Research baseline
Consulted:
- Official Three.js + Rapier character-controller demonstration: https://threejs.org/examples/physics_rapier_character_controller.html
- pmndrs/ecctrl: https://github.com/pmndrs/ecctrl (R3F/Rapier, not a drop-in vanilla Three.js package)
- Three.js mobile + camera orbit + joystick examples: https://github.com/SahilK-027/TPP-Orbit-Camera-Controller
- Three.js interaction/input patterns: device input -> semantic actions -> gameplay movement; pointer capture and separate input zones.

We choose conventional mobile dual-stick conventions with just one left analog stick and drag-to-look on the right. The goal is not to invent another physics motor: the current prototype uses one heightfield, few obstacles and straightforward kinematic movement. Use a physics character controller such as Rapier's when the game adds real ledges/steps/complex scenery. A switch to React Three Fiber simply to access ecctrl is inappropriate for this small vanilla-Three.js project.

## Root cause #1 · Visual facing is mirrored
Fox geometry defaults to local forward (0,0,-1); rotating about positive world Y maps this local direction to (-sin(angle),0,-cos(angle)). Old heading was `atan2(vx,-vz)`, which points local -Z to the *opposite horizontal X direction* whenever walking left/right. Correct is `atan2(-vx,-vz)`. The previous QA tested only controller positions, never character facing.

## Root cause #2 · Input basis can diverge from camera the player sees
Old movement projected input onto **desired** yaw, while camera position/target were still smoothing. Thus on mobile during a simultaneous thumb-forward/right-finger-orbit action, the world movement could reflect the future camera orientation rather than the current rendered view. Fix: derive movement axes each frame from `camera.getWorldDirection()` (projected onto XZ); view-right = (-forwardZ,forwardX). Keep this world-space semantic input independent from device source (joystick/keyboard).

## Root cause #3 · Mobile sensitivity & frame budget
Old touch target was 105px and high vertical orbit reach produced a near overhead framing; touch softness/angle varied with the device. 132px stick, 48px knob, radial deadzone, reduced portrait camera pitch/vertical orbit sensitivity, and CSS touch-action/pointercapture zones. Lower rendering cost for coarse-pointer: DPR capped 1.2 and one 1024² sun shadow map (desktop unchanged), to prioritize input response. Full-world rendering remains heavier than the controlled locomotion calculations.

Frame delta cap raised from 50ms to 100ms. Numerical substeps retain stable short-term physics on 10–30 FPS devices rather than slowing simulated locomotion at low FPS.

## Mobile interaction contract
1. Thumb drags within lower-left virtual stick to choose travel direction **on screen**. Neutral stick stops; analog displacement controls speed.
2. Independently swipe the world canvas on the right to orbit around the fox. Character steering should match the camera orientation *actually rendered* that instant.
3. Fox's head/body faces its travel direction, not toward/away from camera by default. It does not spin when the camera alone is rotated while joystick is neutral.
4. HOP triggers exactly one jump; position is grounded back on terrain.
5. Switching fingers, pointercancel, focus loss and page background should clear held controls.
6. Fox is readable at roughly 6.6m portrait follow distance and low default angle; no involuntary camera spin or over-the-top elevation.
7. No character-visual quality claims in this sprint. Character mesh, leg animation and snow-vs-fur contrast remain A02.

## Acceptance gates
- Node: forward/right axes in four camera orientations, visible fox heading vs velocity on cardinal/diagonals, actual-view override, 10FPS time step, terrain/collision and jumps.
- Chromium browser: desktop keyboard + orbit, simulated portrait touch joystick and concurrent independent right-touch orbit, model facing/direction dot products, jump+landing+reset, no page JS error, screenshots.
- Android physical device: 3–5 minutes with thumb+finger including diagonal movement, circling hut, 180° camera orbit without letting go of joystick, repeated jumps. Record screen and report lag/steering discrepancies if still present.
- Art is NOT accepted by controller QA; owner sign-off only after live device playtest.
- Expose optional diagnostic HUD at `/?controls=1` to show FPS estimate, actual facing/movement alignment, stick vector and camera yaw. A negative alignment while moving proves a model facing defect.

## Follow-up trigger
If control bugs persist *despite* dual-touch QA and oriented model agreement, the next diagnostic should be screen-to-world instrumentation on the actual Android frame (record pointer ids, stick vector, camera world forward, player velocity, rendered heading), not another blind acceleration tweak.

# LN-A01a-R1 — Android video diagnostic / camera-relative input

## Evidence
Owner supplied a ~19.4s Android portrait screen recording in chat (19 Oct 2026), **not committed to the public repository**. It shows a tiny fox in a predominantly white, strongly overhead scene while the virtual stick is pushed and camera is orbited. The thumb direction and visible character travel become hard to reconcile after orbiting.

## Proven root cause
The camera orbits via:
`camera.x = fox.x + sin(yaw)*distance*cos(pitch)`
`camera.z = fox.z + cos(yaw)*distance*cos(pitch)`

So in the ground plane, **camera-relative forward = (-sin(yaw), -cos(yaw))** and **camera-right = (+cos(yaw), -sin(yaw))**.

The original controller instead used `(+sin(yaw), -cos(yaw))` for forward and `(+cos(yaw), +sin(yaw))` for right. With the view at 90°, joystick-up moved *toward* camera rather than away; screen-right was similarly mirrored. Original test incorrectly asserted the bad direction, thus passed.

## Changes
- Fix camera-relative basis signs in `src/controller.js`. Both desktop and joystick use one consistent path.
- Replace incorrect unit expectation with four cardinal orientations for screen-forward and screen-right; verify continuous motion while orbiting.
- For portrait touch, start camera closer (6.1m vs 8.6m) and lower (pitch .20 vs .28); reduce vertical orbit response and cap upward angle to .55rad. This mitigates the extreme overhead framing visible in recording without redesigning visuals.
- Add real dual-touch browser QA: hold left stick forward while dragging a second finger on the scene, asserting movement aligns with screen-forward. Desktop QA now also tests WASD *after* orbit.
- No changes to fox mesh, scene assets, art direction, or lighting.

## QA requirements
`npm run test:syntax`; `npm run test:movement`; `npm run build`; automated Chromium screenshots and controller browser QA must all pass. Android physical-device playtest remains required because headless Chromium is not real device proof.

## Remaining separate issues
The fox mesh is a placeholder composed of separate primitives with no convincing walk animation; the snow and foreground are too close in luminance, making the white fox visually difficult to track. Art redesign belongs to A01b/A02, not this bounded input fix. Camera object occlusion and intelligent recentering are later options, not part of R1.

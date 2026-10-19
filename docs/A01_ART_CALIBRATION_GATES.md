# Little North — A01 Art Calibration Gates v0.1

Status: **experimental / not art-approved**. GitHub Pages preview is a review surface, not a production sign-off.

## North-star
**Sculpted Arctic Storybook**: a handcrafted northern wilderness viewed at fox eye-height. Soft, shaped snow; complex yet legible snow-laden evergreen silhouettes; restrained angular rock; warm handcrafted cabin; tiny fluffy fox. Stylized is not a synonym for bare primitives, repetitive cones, flat terrain, or default PBR.

## Explicit img2threejs implementation boundary
We adapt the methodology from https://github.com/img2threejs/img2threejs (Apache-2.0): observation before inference, macro→meso→micro hierarchy, topology/material spec, passes, four-angle rendering, deterministic metrics, explicit visual review and bounded correction. **The original `forge/state.py`, `forge/next.py`, scoring and mesh gates have not been installed or executed.** We must not call our adaptations equivalent to official skill validation. A local standalone skill install may be considered *only if* it improves fidelity or removes QA overhead.

## A01 controlled slice and order
1. **A01-1: calibrated hero spruce** — the first reproducible image→procedural Three.js artifact. Work in `src/procedural.js` and `sculpt.html`; prove continuous asymmetric crown, believable downward bough rhythm, snow resting on branches, irregular frayed silhouette, no isolated apex, and visual coherence at 0/90/180/270°. Accept close-up and game-distance views. Reject repeated naked cone tiers.
2. **A01-2: camera, composition and terrain** — sculpt snowdrifts and readable gentle terrain transitions in a close forest/cabin composition. Remove dominating background triangle mountains. Show near/mid/far detail hierarchy from fox eye-level.
3. **A01-3: cabin hero prop** — ensure timber scale, roof thickness, eaves and snow placement, coherent wall corners, inviting doorway and *visible amber windows from initial camera*. Differentiate carved details from material grain; no floating pieces.
4. **A01-4: fox character direction** — replace segmented white proxy with a coherent quadruped and expressive silhouette, especially ears, muzzle, legs, and oversized furry tail. Pose and idle animation first; do not equate unrigged geometry with an animation-ready character.
5. **A01-5: integrated lighting and first-person-size check** — soft blue winter fill and low warm sun, legible snow relief, restrained fog and snow variation. Validate actual desktop and Android viewport.
  
The first art lock is one *single* highly polished tree+cabin vignette, not the island.

## Required evidence for each asset
- Source reference & rights/provenance recorded in notes (user images are reference only; don't republish as art assets).
- Geometry analysis: silhouettes, parts hierarchy, contact/attachments, material channels, inferred/hidden areas.
- Reference camera + independently controlled *orbit/turntable* screenshot(s).
- One screenshot in the world under final scene lighting.
- Explicit before/after image comparison and written critique with **blockers and next specific correction**.
- WebGL console errors = 0, JS checks + Vite build = pass.
- Real renderer draw calls and triangles recorded (not object count mislabeled as draw calls).
- Mobile-browser manual confirmation before performance acceptance; provisional target >=30fps during exploration with high quality disabled only when necessary.

## Reject criteria even if automation passes
- Snow/foliage looks like repeated cones or disconnected flat ribbons.
- Feature silhouette fails at thumbnail scale or from rear/side.
- Snow caps appear disconnected, clip through foliage, or create unnatural hard edges.
- Unconvincing fake flat texture, visible floating/overlapping geometry, z-fighting.
- Cabin poorly oriented, dark on camera, shape unclear.
- The fox still looks like stacked primitives in normal gameplay framing.
- Scene quality relies on a single hand-picked angle.

## Operational workflow
Implement only one high-impact visual change per iteration → syntax & browser QA → review 4-angle and world evidence → accept/reject → commit. Commit screenshots under docs/qa only when practical; prefer Actions artifacts for bulk screenshot sets. No blind multi-asset polish merges. Keep A01 as a review branch (Pages preview may intentionally publish experiments). Production merge requires owner approval.

## Immediate next move
Use the A01 spruce source crop as reference. Review the *latest* four-angle screenshot set (not the original). If its crown/needle/snow silhouette still fails, sculpt hero spruce geometry before adding more scenery. Later test the same process on the cabin and fox.

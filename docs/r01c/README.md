# LN-R01c — Blender mesh hero spruce calibration

Status: one candidate, **not art-approved**. No merge or deployment. Base branch `phase-a01-art-calibration`, initial base `71023cc59a2e09d962b92402f80131a70e3832bc`.

## Feasibility and method selection

Blender was absent initially. The official Blender 4.2.0 Linux distribution was downloaded and executed locally. A factory cube was rendered with Cycles **CPU**, saved as `.blend`, and exported as GLB. CPU rendering is proven; GPU availability/performance is not claimed. Installing the `bpy` pip wheel did not succeed, so the standalone Blender distribution was used. Chromium 141 / Playwright 1.56.1 was subsequently installed and actual WebGL screenshots produced using ANGLE SwiftShader. The first CDN mirror returned invalid archives; the alternate official Playwright mirror worked.

Selected route: deterministic Blender Python → editable meshes and studio in `.blend` → material-batched GLB → existing Three.js sculptviewer. Blender's voxel union/smoothing is used for continuous snow surfaces, and a separate wooden skeleton and small closed needle meshes establish geometry at different scales. This enables actual mesh editing and export; merely using Blender does not establish artistic quality.

The original `img2threejs` skill was not available or executed. Only its useful principles are adapted: reference decomposition, primary/secondary/tertiary hierarchy, deterministic construction, multi-angle render evidence and a separate technical/art verdict.

## Prior experiment inspected

Read PR #5 and its explicit ART REJECT review, `src/hero-spruce.js`, `src/sculpt.js`, and `docs/LN_R01B_HERO_SPRUCE.md` at R01b head `f49eebe5eb1a78da2c1a6f35328272fd13d437ea`. Re-rendered and personally inspected the actual R01b front WebGL image. The full original R01b QA script encountered a CDN import failure later in its run; its remaining measurements are historical, not newly validated. R01b's coarse leaf-spray lofts are not reused here.

## Source and reproduction

- `tools/r01c/build_spruce.py`: seeded mesh authoring, snow remesh, export and seven CPU renders.
- `assets/r01c/hero-spruce.blend`: editable four mesh objects plus studio lights/camera/ground. Studio ground is excluded from GLB.
- `public/models/ln-r01c-hero-spruce.glb`: +Y-up glTF asset, approximately 9.6 m tall.
- `src/sculpt.js`: GLTFLoader integration in the existing sculptviewer. Seven view presets, existing orbit/zoom, legacy comparison via `?legacy=1`.
- `scripts/r01c-visual-qa.mjs`: seven desktop screenshots and a portrait mobile viewport, actual renderer counters, error checks.

Run from repository root, using Blender 4.2.0:

```sh
blender --background --threads 4 --python tools/r01c/build_spruce.py
npm install
# Tested browser tooling version:
npm install --no-save --package-lock=false playwright@1.56.1
npx playwright install chromium
npm run dev -- --host 127.0.0.1 --port 4174
# In another shell:
node scripts/r01c-visual-qa.mjs
```

Open `sculpt.html`; use keys 1–4 for cardinal views, 5 for three-quarter, 6 for close-up, 7 for gameplay distance. Query `?qa=1` disables redundant redraws between fixed poses for software-renderer captures; the ordinary viewer continuously renders. Renderer counters come from actual `renderer.render` calls. `info.autoReset=false` with an explicit reset before each render retains shadow-pass calls, which Three.js normally resets before the main pass.

No controller, gameplay world, ordinary forest assets, fox or other game systems are modified. Unlike R01b, the candidate is only loaded by the sculptviewer, keeping the original playable world intact. Owner reference images remain outside the repository.

## Bounded corrections

Initial construction: 563,124 triangles; actual front render exposed excessive smooth snow plates and insufficient visible foliage. Correction 1: narrower branching snow forms, larger overlapping needle fingers, 30 independently staggered main boughs, mesh simplification; 226,080 triangles. Correction 2 (final): rounder needle ends, irregular snow widths/heights, mild wood contour variation and per-needle simplification (the added rings still increase the final total). **No further geometry iterations in this assignment.**

This is a scripted reconstruction inferred from two single-view references, not a recovered scan. Unseen sides are authored interpretations. Numerical budget reductions are not art acceptance.

## Final technical measurements

| Measurement | Final candidate |
|---|---:|
| GLB mesh triangles | 253,132 |
| Vertices loaded by Three.js | 141,974 |
| Material count / mesh batches | 4 / 4 |
| GLB size | 6,042,616 bytes |
| Loaded geometry attribute + index bytes | 6,038,432 bytes |
| Bounds (width × height × depth) | 6.047 × 9.675 × 6.383 m |
| Main pass (4 tree meshes + ground) | 5 calls / 253,404 triangles |
| Full frame, including tree shadow pass | **9 calls / 506,536 submitted triangles** |
| Portrait test | 390 × 844 CSS px, DPR 1.25, 487 × 1055 render buffer |
| Renderer | Chromium 141, ANGLE Vulkan SwiftShader (software) |

See `mesh-metrics.json` and `webgl-metrics.json` for independent export/import measurements and eight WebGL views with no recorded page errors. Mesh triangles and submitted triangles differ because the latter includes the ground and shadow pass. Geometry bytes exclude runtime object overhead, driver allocations, framebuffer, shadow textures and the downloaded GLB buffer; they are not total VRAM usage.

The final round contains more triangles than round 1 because extra needle rings round the silhouette. It exceeds R01b's provisional 175k hero guardrail by about 45%. Four material batches keep submission count moderate, but ~506k submitted triangles per frame for one isolated tree leaves limited room for an environment on weaker mobile GPUs. The 2048 shadow map and antialiasing add cost. Repeated trees would need a separate LOD/instance/shadow strategy. No smartphone FPS, thermal, load-time or memory verdict is justified by this software viewport test. Mobile framing also clips some lower lateral boughs.

## Visual comparison and reviewer verdict

**Recommendation: do not art-lock or merge this as the premium hero spruce.** This is a completed, reviewable calibration candidate; the target style is not yet achieved. Owner and creative-direction review retain the acceptance decision.

| Criterion | What approaches the references | Remaining gap visible in actual renders |
|---|---|---|
| Silhouette | Tapered asymmetric outline, staggered boughs, real rear/side volume | Long central stem and regular hanging feather rhythm; less naturally composed than either reference |
| Foliage | Small closed 3D fingers replace R01b's large spray lofts; overlapping fans | Still pointed individual leaves; insufficient soft, layered spruce character and secondary variation |
| Snow | Thick closed surfaces follow connected bough/branchlet layouts with scalloped margins | Several flat-edged slab caps; overlaps show seams/artifacts in close-up; limited natural draped lips |
| Wood/joints | Main boughs originate on trunk; secondary twigs start on main boughs | Intersecting rather than fused meshes; tapered rods, exposed tips and simple roots lack reference anatomy |
| Materials | Evergreen/sage palette, warm wood, cool rough snow | Uniform PBR colors; no authored bark carving, painterly treatment or rich surface variation |
| Volume/lighting | Real depth and self-shadowing in cardinal views; studio and WebGL evidence | Soft Cycles lighting is more forgiving; game lighting exposes geometry artifacts |
| Cozy game | Recognizable snow spruce at gameplay distance; standard glTF materials | Still too mechanical for premium art and too heavy to call mobile-ready |

Reference 1 contributes substantial snow and layered foliage; reference 2 contributes exposed trunk, asymmetry and separated boughs. Neither was reconstructed precisely. Judgments use the images shown in the conversation; reference images are not embedded in the repository.

### Actual render evidence

- Blender CPU: [front](evidence/blender-front.png), [right](evidence/blender-right.png), [rear](evidence/blender-rear.png), [left](evidence/blender-left.png), [three-quarter](evidence/blender-three-quarter.png), [close-up](evidence/blender-close-up.png), [gameplay distance](evidence/blender-gameplay-distance.png).
- Three.js: [front](evidence/webgl-front.png), [right](evidence/webgl-right.png), [rear](evidence/webgl-rear.png), [left](evidence/webgl-left.png), [three-quarter](evidence/webgl-three-quarter.png), [close-up](evidence/webgl-close-up.png), [gameplay distance](evidence/webgl-gameplay-distance.png), [portrait viewport](evidence/webgl-mobile.png).
- History: [R01b front](evidence/history/r01b-front.jpg), [initial R01c front](evidence/history/initial-front.png), [round 1 front](evidence/history/round1-front.png).

No generated illustration or reference image is presented as a render. Blender and WebGL cameras/lighting differ and are not pixel-matched comparisons.

### Validation and boundary

`npm run test:syntax`, all 13 `npm run test:movement` tests, and `npm run build` pass locally. Vite reports its shared Three.js chunk exceeds 500 kB. `node scripts/r01c-visual-qa.mjs` captures seven final desktop views and one mobile viewport without page errors. Software-browser FPS is not an acceptance gate. Original controller/world source files are unchanged from the requested base.

Two focused correction rounds completed. Stop here: no additional variants, ordinary forest replacement, merge or deployment. If art is rejected, a further assignment needs an explicit method/art-direction decision before more generation.

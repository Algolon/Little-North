# LN-R01e — Local Blender hero spruce / review checkpoint

**ART REJECT — editable whole-tree study, below premium reference quality. No merge or deployment.**

Created locally on the Mac with `/Applications/Blender.app/Contents/MacOS/Blender`, Blender **5.2.2 LTS**, Cycles CPU. The sandboxed launch crashed; the approved native process succeeded. This is an actual authored 3D mesh, not an AI image, a VTK substitution, or merely a GLB imported into Blender. Source branch: `art/ln-r01d-branch-study` at `39af524216d8c2dea472794b4fb1b7119a87706c`; working branch: `art/ln-r01e-sculptural-hero`.

## Scope and reference review

One whole hero spruce, isolated source, export, viewer, five Blender views and four WebGL views. Initial target: first visual review within about 20 minutes after repository inspection; session limit about 60 minutes; maximum two substantive correction rounds. No game integration, variants, LOD work or production-file edits. This assignment explicitly authorizes the whole tree, superseding R01d's historical bough-only scope.

Read R01c and R01d README files, R01c's modeling script, and personally inspected their Blender contact sheets. Both original owner references were recovered from the linked conversation and viewed: `83585.png` (denser snow and canopy) and `83584.png` (more exposed organic trunk). They are inspiration, not redistributed assets. Compare their broad overlapping foliage, quiet rounded snow rims, staggered open spaces and carved trunk against the actual evidence below; cameras are not pixel matched.

## New construction method and its limits

No R01c/d mesh generator or geometry was reused. The Blender-native hybrid process uses an explicitly composed list of 22 asymmetric bough arms; connected tapering wood control surfaces with voxel fusion at junctions; broad deformed foliage cages with overlapping compact ridges and short embedded 3D needle tips; and overlapping support volumes, saddle bridges, voxel fusion and smoothing for snow. Longitudinal wood grooves and broad tonal variation are applied directly to the mesh. Source retains 47 named editable components. A temporary joined export copy produces four material primitives.

**This is script-assisted sculptural volume construction and local vertex deformation, not manually executed Sculpt Mode brush work.** There are no hand-sculpted master clusters and no recorded artist brush strokes. Blender execution alone does not establish premium craftsmanship. The result still exposes the limits of generated mass construction; it should not be described as a finished premium hero.

## Bounded visual rounds

1. Initial real Blender candidate: smooth green cushions and isolated domes. **ART REJECT.** Preserved at `evidence/initial/blender-three-quarter.png`, source checkpoint `2ad9564`.
2. Correction 1: denser short surface needles, slimmer core volumes and supported snow bridges. The silhouette improves, but exposed smooth cores and grassy needle fringes remain. Preserved at `evidence/round1/blender-three-quarter.png`.
3. Correction 2, final: stronger small-scale foliage relief, shorter wider needles, narrower trunk and deeper longitudinal wood carving. Stop after this round; do not repeatedly tune the generator.

Actual WebGL testing exposed an unsupported material-node combination: initial export was white. The finalization stage bakes full linear RGB point colors and connects them directly to Principled Base Color, then exports GLTF `COLOR_0`. All final Blender views and WebGL captures are regenerated from these corrected materials. The initial failed color export is not acceptance evidence.

## Strict art gates

| Gate | Rating | Evidence and remaining deficit |
|---|---|---|
| Whole-tree architecture | Partial | Individually composed arms and negative spaces; canopy still stair-stepped and underfilled compared with references. |
| Compact layered spruce foliage | **Fail** | Short true needles replace large feathers, but grassy fringes and visible cushion cores lack authored cluster hierarchy. |
| Supported snow volume | Partial | Connected soft blankets and saddle bridges sit on foliage; repeated dome rhythm and some cap-like edges remain. |
| Snow rims | Partial | Rounded irregular lips improve on plates; insufficient gravity-shaped overhang variation and coherent wind accumulation. |
| Organic wood | Partial | Fused branch junctions, root flare and longitudinal grooves; trunk still simple and roots too graphic. |
| Materials | Partial | Evergreen/jade, warm umber and rough off-white survive export; no richly authored painterly bark/foliage treatment. |
| Multi-angle quality | Partial | True front-quarter/rear/side/top/close-up evidence; top reveals the repeated cushion layout. |
| Premium Nordic Storybook identity | **Fail** | Recognizable snowy spruce, but neither reference's sculptural craftsmanship is achieved. |
| Technical export | Pass for desktop study | Actual Blender source, GLB and genuine Three.js render; see measured metrics. Performance readiness is not claimed. |

**Overall: ART REJECT.** Main next action: replace one exposed foliage cushion plus its snow rim with a manually sculpted, visually accepted master, before undertaking another whole-tree iteration. Do not approve this asset merely because it loads or has dense geometry.

## Files and reproduction

- `assets/r01e/hero-spruce.blend` — editable source, studio lights, camera and component meshes.
- `assets/r01e/hero-spruce.glb` — actual +Y-up export; studio excluded.
- `assets/r01e/viewer.html` and `viewer.js` — isolated orbit viewer, no production integration.
- `tools/r01e/sculpt_hero.py` — complete reproducible Blender construction; invokes finalization.
- `tools/r01e/finalize_export.py` — source color parity, material-batched export and final renders.
- `tools/r01e/webgl-qa.mjs` — four actual browser captures and renderer measurements.
- `tools/r01e/contact_sheet.py` — contact-sheet assembly from actual renders, Pillow required.
- `mesh-metrics.json` / `webgl-metrics.json` — measured export and runtime figures.

Run from repo root:

```sh
/Applications/Blender.app/Contents/MacOS/Blender --background --factory-startup --threads 6 --python tools/r01e/sculpt_hero.py
npm install --package-lock=false
npm run dev -- --host 127.0.0.1 --port 4176
node tools/r01e/webgl-qa.mjs
python tools/r01e/contact_sheet.py
```

The browser QA executable path is Mac-specific and points to the already installed Chromium headless shell. The viewer is served by the local development server; it is intentionally not added to the production build. Blender lights and Three.js lighting differ. Desktop software WebGL proves rendering and metrics, not mobile speed, thermals or total GPU memory. Source geometry count and glTF vertices can differ at normals/material/color boundaries.

## Evidence

[Contact sheet](evidence/review-contact-sheet.jpg) · [Blender three-quarter](evidence/blender-three-quarter.png) · [rear](evidence/blender-rear.png) · [side](evidence/blender-side.png) · [top](evidence/blender-top.png) · [close-up](evidence/blender-closeup.png) · [actual WebGL](evidence/webgl-three-quarter.png).

## Final measured technical results

| Measurement | Actual value |
|---|---:|
| Triangles | 766,942 |
| Source vertices / imported vertices | 460,141 / 460,162 |
| Editable source mesh objects | 47 |
| Exported glTF mesh / material primitives | 1 / 4 |
| Materials / actual WebGL main-pass draw calls | 4 / 4 |
| GLB bytes | 28,943,760 |
| Loaded geometry attribute + index bytes | 28,938,830 |
| Bounds, Three.js X/Y/Z | 6.047 / 8.973 / 6.390 m |
| Browser page/console errors | 0 across four captured views |
| Runtime | Chromium headless, ANGLE SwiftShader, desktop software WebGL |

The isolated WebGL scene has no shadow pass or ground; four calls is not a full game-frame budget. Geometry bytes exclude framebuffer, driver allocations, object overhead and GLB buffer. **This model is too heavy to declare production/mobile ready.** No device FPS test was performed.

Validation: actual Blender process completed, five final Cycles renders inspected, four final WebGL views captured; GLB JSON confirms four PBR materials and `COLOR_0` on every primitive. Viewer and QA JavaScript syntax checks plus `git diff --check` pass. No production code changed relative to the R01d source branch; no full-game tests are needed for the isolated artifact. No merge or deployment performed.

# LN-R01d — premium spruce bough calibration (ISOLATED STUDY)

**ART REJECT — do not merge, deploy, or expand into a tree.** Two substantive corrections completed after the initial candidate. Explicit creative acceptance remains with owner. Source: 969226a0651daeab9b7b8861cb1b3ec5382f5d60, art/ln-r01c-mesh-calibration.

## Reference decomposition

- Primary silhouette: one curved lower/mid bough with asymmetrically staggered secondaries and slight snow-induced droop. Image 1 exposes more branch structure; image 2 shows heavier snow.
- Foliage: broad, soft layered spruce clusters, short needle tips, dark green-teal-sage variation. Reject oversized feather/leaf/finger repetition.
- Snow: soft heavy accumulated volume conforming to upper needle masses; uneven overhangs and natural hanging lips; green visible below.
- Wood: organically connected tapered curvature, no intersecting cylinders.

## Actual method and blockers

This is a **hybrid fallback mesh-first study, NOT a manually sculpted Blender candidate**. Local execution environment has no Blender executable. Deterministic numpy/trimesh loft construction generated the candidate and exported a **real 5 MB GLB**. Offscreen VTK rendered four diagnostic views for artistic inspection. These are NOT Blender Cycles renders or in-game WebGL. The Blender import/save/render script and Three.js isolated viewer are supplied to enable independent validation. Any CI-generated .blend is an editable import of the mesh, NOT evidence of hand sculpting.

- tools/r01d/build_bough.py — reproducible authoring, deterministic seed.
- tools/r01d/render_blender.py — imports GLB, saves Blender source, Cycles CPU evidence; run only in Blender 4.2.
- bough.html / src/bough.js — isolated Three.js viewer, no game integration.
- scripts/r01d-visual-qa.mjs — actual WebGL screenshot and renderer counters once executable.
- docs/r01d/evidence — render evidence after CI, if that job succeeds.

Run: python -m pip install numpy trimesh; python tools/r01d/build_bough.py; blender -b -t 4 --python tools/r01d/render_blender.py; npm install; npm run dev -- --port 4174; node scripts/r01d-visual-qa.mjs.

## Bounded art rounds

**Initial candidate:** paired twig rhythm, long hanging green feathers, ribbed snow. ART REJECT.

**Round 1:** compact 3D foliage clusters and shorter tuft sprouts; obvious fishbone regularity and duplicated caps remain. ART REJECT.

**Round 2 (stop):** staggered asymmetric forks; larger centre foliage; simplified snow surface frequencies. True VTK diagnostic shows suspended narrow green masses and separated white cap forms. The result is technically real 3D, but still below the reference standard. ART REJECT. No more iterative parameter tuning.

## Quality gates (based on actual VTK diagnostic meshes)

| Gate | Rating | Evidence |
|---|---|---|
| Foliage silhouette | **Fail** | Narrow hanging clumps, not broad overlapping spruce needles |
| Foliage detail | **Fail** | Smooth repeated leaf/finger forms remain |
| Snow geometry | **Fail** | Distinct caps, not natural physical accumulation |
| Snow edges | **Fail** | Several angular smooth plate edges and weak hanging lips |
| Wood | **Partial** | Taper, bend and layout; offshoot joins are intersecting geometry |
| Multi-angle | **Fail** | Top clearly shows separate fan groups |
| Stylized art identity | **Fail** | Does not achieve tactile handcrafted Nordic Storybook |
| Technical usability | **Partial** | Locally parsed GLB; independently validate Blender and WebGL through actual runtime |

## Measured local export data

- Triangles: **248,008**
- Vertices: **127,484**
- Material/mesh batches: **5 / 5**
- GLB: **5,019,800 bytes**
- Approximate raw mesh arrays: **9,011,808 bytes** (NOT VRAM total)
- WebGL draw calls: **not locally verified**; only state measured values if browser job succeeds.
- Mobile performance: **not tested**; desktop/software render is not a device FPS result.

**Handoff:** Preserve result as rejected reference. The next step should be **manually artist-sculpting one needle mass plus its snow blanket in Blender**, validating from all angles, then only scripting assembly of approved components. Do not scale this parameterized generator into a full spruce.

No fox, camera, movement, gameplay, UI, world, variants, LOD, merge or deployment was modified.

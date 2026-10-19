# A01-TREE-001 — Image → Procedural Three.js spruce study

## Method attribution and boundary
This study uses the **principles** in `img2threejs/img2threejs` (Apache-2.0), notably `SKILL.md`, `grimoire/intake/image_analysis.md`, and `grimoire/build/geometry_patterns.md`. It does **not** claim to have passed the official skill's `forge/next.py` state gates or its automated image/mesh self-intersection tests. Those scripts are not installed in the chat runtime. Source: https://github.com/img2threejs/img2threejs

## Reference
Source: user's first moodboard image, foreground snow-laden evergreen on the right side. Analysis is performed against the provided image in the chat, not a copied reference committed to this repository.

## Observation before inference
- Object class: coniferous tree with snow. Primary domain: object / botanical. Complexity: moderate.
- Silhouette: tall taper, narrow top, wide and irregular lower crown; broad descending heavy branch tiers; distinguishable trunk mostly hidden behind foliage.
- Macro: trunk, long drooping boughs, crown. Meso: uneven clustered needle fronds, large snow mantles, secondary boughs. Micro: frayed needle margin, pendent snow fringes, irregular layering.
- Spatial relations: boughs radiate in whorls from trunk; snow rests on *top* of individual boughs and folds over their outside edges.
- Materials: dark teal-blue rough needles, near-white matte snow, desaturated rough bark, cold blue fill shadows.
- Uncertainty: back crown and bough layout occluded; intentionally invented based on plausible botanical asymmetry; reference uses perspective and cinematic lighting, not a measured orthographic drawing.

## Quality contract — minimum acceptance for the sculpt
1. Obvious spruce silhouette at thumbnail size, including irregularity, thin crown and wide lower boughs.
2. Snow visibly lies *on* upper surfaces, with exposed dark green underneath.
3. No repeating naked-cone or identical-tier appearance.
4. 3D coherent from front/side/rear/oblique views, not a billboard.
5. Low number of draw calls using same-material geometry batching, not one draw call per twig.
6. Acceptable standalone render and in-world render required before 'art-approved'.

## Planned review evidence
- Standalone turntable on `sculpt.html`, views 0°, 90°, 180°, 270°.
- Scene view on `index.html`, near-camera and medium distance.
- Capture hero tree triangles/drawables via `P` statistics.
- Compare against image with qualitative notes, not a fake quantitative pixel similarity claim.

## Implementation
`src/procedural.js` uses layered radial asymmetry, custom tapered branch ribbons, top snow ribbons with uneven drooping margins and geometry batching by material. `src/sculpt.js` provides an inspectable four-view test harness.

## Status
- Reference analysis: completed.
- Sculpt code: implemented candidate.
- JavaScript syntax: check via `npm run test:syntax`.
- Browser visuals, multi-angle imagery, self-intersection: **NOT YET VERIFIED** until an actual Three.js browser run.
- Acceptance: **PENDING**; no art-style lock until reviewed.

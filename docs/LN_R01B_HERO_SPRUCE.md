# LN-R01b — Hero Spruce Art Calibration

**Status:** implementation candidate, **not yet art-approved**. Owner's two snow spruce images are visual references in the ChatGPT conversation; image rights/provenance are not republished to this public repository.

## Goal and intentional trade-off
One premium stylized, genuinely volumetric Three.js tree. First supplied reference anchors the heavy sculpted snow / fuller inviting silhouette; second anchors the irregular separated drooping boughs, visible roots/trunk and readable branching. The 70/30 weighting is directional, not a pixel metric. **Nothing in this branch approves the tree or changes general forest generation.**

## Image-to-Three.js reconstruction notes (principles adapted; original skill not installed)
- **Macro:** asymmetric tapered 9.6m trunk with buttressed roots, 12 uneven branch tiers, variable azimuth and lengths; taper decreases toward a coherent crown.
- **Meso:** multiple woody branch segments, central needle bundles plus secondary lateral sprays with several finer tuft fingers.
- **Snow:** actual closed rounded loft volumes (not floating flat ribbons). Each mantle follows the bough's sag path; widths, lengths, overhangs and coverage vary. White top surface exposes pine underbough.
- **Micro:** scalloped needle silhouettes, varied teal/olive green and cold-shadow snow channels. Avoid photoreal fur/needles and high frequency noise.
- **Uncertainty:** only one camera angle per reference. Rear and inner branch anatomy inferred from plausible spruce structure; front/back/side renders required to test.
- **Runtime:** deterministic PRNG by seed, branch geometry baked by material. GeometryBatch produces compact material batches instead of hundreds of draw calls. Accept renderer-measured counts only, not unverified estimates.
- **Style failure conditions:** giant flat cones, repeated radial level cakes, snow detached from needles, overly smooth/round cotton blobs, branch joints floating, no credible trunk, unreadable foliage, artificially thin needle-like top, silhouette hollow across other views.

## Entry points
- `src/hero-spruce.js`: new standalone generator (does not replace regular forest generator).
- `src/sculpt.js`: studio viewer using generator. `sculpt.html?legacy=1` is old procedural baseline.
- `src/world.js`: only the original main hero tree at x=8.6 z=-9.7 uses new generator. Other trees remain unchanged.
- `/?heroReview=1`: opt-in QA photographic position; normal game controls unchanged.

## Proof and acceptance
- Standalone front, right, rear, left, 3/4, detail, gameplay distance (keys 1–7 in viewer).
- Legacy side-by-side comparison from same approximate view.
- In-world render to check scale, lighting and integration.
- `npm run test:syntax`, `npm run test:movement`, `npm run build`, `npm run visual:qa`, `npm run qa:controller` and `npm run qa:hero`.
- `qa-evidence/r01b-results.json`: geometry bounds, triangles, material batches, errors. Screen JPGs in GitHub Actions artifact.
- **Strict evaluation:** actual screenshot inspection and written accept/reject before any merge. Passing CI is *not* an art quality gate.
- A single hero under 175k triangles and at most 10 material batches for current prototype. World draw calls measured separately. These are guardrails, not performance evidence for Android.
- If insufficient, iterate in two bounded passes before reporting. Work isolated on `art/ln-r01b-hero-spruce`.

## Deferred
No tree variants/LOD, no generalized forest replacement, no camera or movement changes, no fox, UI or level design changes. Any performance/LOD policy for multiple repeated premium spruces is a separate R01c task.

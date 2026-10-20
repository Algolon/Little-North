# LN-FOX-R01a — intended proportion sheet

Reference: user-supplied 83588.png (visual guidance; not bundled).
Art source: docs/ART_DIRECTION.md on phase-a01-art-calibration.
Base commit: 71023cc59a2e09d962b92402f80131a70e3832bc. This deliberately avoids bringing the spruce studies into the fox branch.

## Intended silhouette, before the neutral form gate

| Landmark | Intended study value | Purpose |
|---|---:|---|
| Ground to withers | approximately 0.85 m including coat envelope | Project-relative study scale; not a biological size claim |
| Ground to ear tips | approximately 1.22 m | Readable compact protagonist at the project's proxy scale |
| Ribcage width | 0.41 m | Dense winter coat envelope |
| Skull width | 0.38 m | Expressive face, restrained enlargement |
| Ear rise above skull | 0.19 m | Small rounded pinnae, avoid red-fox ears |
| Belly clearance | approximately 0.36 m | Short-legged, naturally quadrupedal |
| Tail brush length | approximately 0.68 m | Full descending tail with gentle lateral curl |
| Front/rear paw separation | approximately 0.69 m | Neutral supported stance |

These are construction targets, not measurements of an accepted final mesh. Actual export dimensions are recorded in the render artifact.

## Gate order

1. Assess front, side, rear, three-quarter and rear gameplay-distance Cycles renders.
2. Check muzzle taper, brow, ear-to-head scale, chest, hind hocks, feet and brush contour.
3. Correct major anatomy and silhouette before any fur detail or painterly material pass.
4. Only proceed if clay forms are convincing. A technically valid GLB does not pass the art gate.

## Method and limits

Scripted Blender volume construction, voxel union, surface relaxation, editable subdivision. Sources initially use overlapping anatomical volumes; the deliverable body is fused rather than an assembly of intersecting primitives. Separate eyes and nose are intentional facial parts. This is not represented as hand-sculpted work. Voxel topology is a sculpt foundation, not deformation topology; future retopology is required. No rig or animation.

## Evidence

The scoped workflow executes official Blender 4.2 on a GitHub runner because Blender is unavailable in the local session and local download access is blocked. It exports a selected-only GLB and imports it again into a fresh Blender scene. Neutral grey clay uses the same studio for all views. Gameplay-distance view is an isolated studio framing, not an in-game screenshot; no gameplay integration is performed.

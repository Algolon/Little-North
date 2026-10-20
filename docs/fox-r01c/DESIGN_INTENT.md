# LN-FOX-R01c — new whole-character sculpt

User explicitly requested a complete arctic fox, automated while working on mobile. No reuse of the rejected R01a/R01b anatomy meshes. Work remains isolated on `art/ln-fox-r01a-character-study`.

## Primary form decisions

- Rounded cranium: initial construction envelope 0.290 m wide / 0.344 m tall; corrected to 0.310 m / 0.310 m after the first review; shorter muzzle, smaller cheek planes. These are explicit construction targets, not a claim that reference proportions have already been matched.
- Compact winter body with a curved withers-to-croup profile and integrated rising neck/breast.
- Shorter visible legs, shoulder-supported forelimbs, fleshed thighs, forward knees, rear hocks and flat contacting paw soles; slight stance asymmetry.
- Full tail brush curved down and gently to the side, widening from the root then tapering continuously.
- Small upright rounded pinnae. Temporary eye/nose markers only during the primary form gate; no iris/gaze or finished fur design is locked.

## Modeling and sculpt method

A fresh smooth signed-distance field blends the complete anatomical/coat envelope continuously. Local field carving develops an orbital plane. Marching cubes extracts the genuine 3D surface, which Blender imports as editable mesh, renders with Cycles CPU and exports as selected-only GLB. The scalar volume is not an image or a generated concept render. This is scripted volume modeling/sculpting, not manual brush work in a viewport.

Scripts and construction parameters are preserved. The actual .blend retains the complete mesh; it is a sculpt study requiring future retopology. No production topology, mobile budget or gameplay integration is claimed.

## Gate sequence

1. Review the whole animal: front, side, rear, three-quarter, head front and head three-quarter, plus a studio distance view.
2. Compare skull width/height/depth and the body/leg/tail ratios against the supplied fox reference. Do not accept a good isolated head with a poor whole-character silhouette.
3. Correct major form issues before fur/material development.
4. Apply broad integrated coat sculpting only if the primary forms convince, and repeat whole-animal assessment.
5. Report ART ACCEPT or ART REJECT on the actual final evidence. Export success is a separate technical finding.

No Hero Spruce, gameplay, rigging, animation, production integration, merge or deployment changes.

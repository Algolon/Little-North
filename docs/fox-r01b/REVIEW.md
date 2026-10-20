# LN-FOX-R01b — focused head and chest review

## Round 1 — ART REJECT

Source commit a337dbd08d9ebe152783ac712534b170e4882d3b. Actual seven-view Blender 4.2 Cycles evidence was rendered by run 39412839892, downloaded and visually inspected. Genuine edited `.blend` and GLB outputs were preserved at commit 6f15353bd02f9876e29aaf3dccd5a1794c54b472.

Observed improvement: eyes are seated in sockets instead of exposed bead spheres; the nose has a fox-like triangular outline; the muzzle has a readable mouth line; ear bowls are present.

Observed failures: the rooted ruff lofts read as block-like hanging tabs, not flowing coat masses. Thin sharp seams and visible nicks occur around the eyelids. The mouth is too smile-like, while the ear depressions look drilled and circular. These fail the intended calm, handcrafted anatomical coherence.

Independent technical inspection: GLB 2.0, four meshes/two neutral materials, 173,903 triangles; reimport into a fresh Blender scene succeeded. Root orientation -Z forward/+Y up verified. Geometry inspection found two connected components in the body and 33 zero-area triangles across body/nose in this threshold check. No nonfinite positions. A successful import does not override these issues or the ART REJECT.

## Round 2 — correction design

Starts again from the preserved R01a `.blend` so failed lofts do not accumulate. Replace block-like ruff construction with localized continuous-skin displacement and broad descending relief. Form orbital tissue in the head surface itself, use softly beveled almond openings and a larger embedded eye surface to prevent body clipping through the aperture. Subdue the mouth's upturn; shape the conchal bowls as rounded triangles. Resurface incisions and remove only demonstrably tiny disconnected remnants. Clean a reduced export copy separately while retaining the detailed source.

The revised source saves its `.blend` before rendering as well as after choosing a useful final camera. The intended next gate is neutral head/chest form only. Whole-character ART ACCEPT remains blocked by unresolved limbs/paws/tail and absent premium coat/material pass.

## Round 2 — ART REJECT

Source commit 997826cc6fcf70625720e54f986b0461e24d10fb; actual seven-view evidence from successful run 39413906156. Generated source/evidence preserved at 468b110ccb5c58ccb7b350214994373dc2350a23.

The block-like ruff and sharp lid seams are removed. Chest is now a continuous surface with broad relief; sockets no longer show the previous clipping/nicks. Independent technical checks found one body component, zero degenerate triangles and zero nonfinite positions across all four exported meshes. Test GLB: 172,068 triangles, 86,042 exported vertices, 4,119,500 bytes. Import into a fresh Blender scene succeeded.

The visual gate still fails: resurfacing attenuated the mouth incision and inner-ear bowl; iris-less eyes do not adequately establish a gentle alert gaze. Kraag/ruff relief is smoother but still lacks the sculptural flow of the reference. The full front/side/rear orthographic studio views reveal a bottom background strip because their ray origins extend below the ground plane; this is an evidence-camera issue, not fox geometry.

## Round 3 correction scope

Make closed cutter normals explicit, restore mouth/ear incisions after resurfacing, add neutral iris/pupil surfaces for gaze assessment, and move orthographic cameras backward along their unchanged viewing directions so all rays start above the studio floor. No painterly body coat or premium fur pass. Neutral iris surfaces are facial form/gaze evidence, not an artistic acceptance claim.

## Final round 3 — ART REJECT

### Evidence and result

Source commit 70ec843b542a61fa000703198c43e447d1fad74d, run 39414841631. Seven actual Blender Cycles images were downloaded and inspected: front/side/three-quarter head close-ups and front/side/rear/three-quarter full character. The comparison sheet uses those images and the prior R01a three-quarter render; it is not a generated concept image or a pixel-matched camera comparison.

The restored mouth incision and triangular conchal bowls are visible. The body no longer contains the previous block-like ruff additions or sharp lid seams. The studio-camera background strips are gone. These are concrete corrections, not evidence of premium artistic acceptance.

The neutral iris/pupil prototype fails artistically: the pale circular iris patches and small round pupils look graphic and button-like, giving a fixed, toy-like expression rather than the intended gentle arctic fox gaze. The head remains overly smooth and mask-like. Cheek/muzzle planes, lid weight and ruff flow do not yet have professional sculptural definition; nose side profile and mouth corners remain schematic. The new eye patches are a rejected gaze experiment, not a locked eye design. The rear/limb/tail limitations recorded in R01a remain unresolved.

### Quality gate

**ART REJECT, including the focused head/chest gate.** No component is declared production-approved. The premium hero deliverable has not been achieved. Do not use the neutral iris test as the final character style. No painterly coat/material pass, retopology, rigging, animation or production integration has been started.

### Technical evidence

- Actual editable Blender 4.2 source: `artifacts/fox-r01b/fox-head-chest-study.blend`.
- Selected-only test GLB reimported successfully in a fresh Blender scene.
- Independent inspection: GLB 2.0; 174,133 triangles, 87,362 exported vertices, eight meshes, four neutral facial/clay materials; 4,850,724 bytes.
- Body is one connected component. Each intentional eye/iris/pupil/nose object is individually connected. Zero degenerate triangles or nonfinite coordinates in the recorded export inspection.
- +Y up / -Z forward checked through the export root and nose geometry; no skins, armatures or animation actions.
- Full sculpt source retains 425,250 body vertices and 424,587 polygons. The test copy is reduced separately. This is not production deformation topology or a mobile performance certification.
- Views are studio orthographic render evidence, not in-game camera/device validation.

### Method limitation and next decision

The available environment executed Blender through scripts and CPU batch renders. It did not provide an interactive sculpt viewport session. Local mesh fields and Boolean editing solved several construction defects but did not close the artistic gap. Another small parameter-only pass is not the recommended next step.

Recommended next action: use the preserved `.blend` in an interactive Blender sculpt session with continuous visual feedback. Start with an isolated head: orbital planes, lid overlap, muzzle pads and cheek-to-neck flow. Replace the rejected iris test with an anatomically seated eye/gaze design; compare against the supplied fox reference in neutral clay. Require that focused sculpt gate to pass before fur layering or painterly materials. Then address hock articulation and paw support. This is a change of modeling workflow, not an art approval.

### Scope and preservation

All work is isolated to fox source, outputs, scoped workflow and review documents on `art/ln-fox-r01a-character-study`. R01a and earlier R01b checkpoints remain in Git history. No Hero Spruce or gameplay files changed; no merge or deployment performed.

Final rendered `.blend`, test GLB and PNG evidence were committed automatically at `1768da1e46064751e5949baa0a77be7b62bc554f`. Final report/inspection metadata is committed separately after visual review. The scripts in this review directory reproduce the independent checks and image-sheet composition without running a modeling job.

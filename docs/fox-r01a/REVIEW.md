# LN-FOX-R01a — evidence-based review

## Round 1: ART REJECT

Actual Blender 4.2 Cycles CPU render and .blend/GLB outputs were produced by run 39407659538 at source commit e70254f24ceb5fc1f35da6b8e828c1256039a972. All five PNGs were downloaded and visually inspected. This is actual mesh evidence, not an image-generation render.

Visible failures:
- Drooping spherical cheeks and protruding bead eyes produce a toy-like expression.
- Raised pelvis breaks the intended smooth croup profile.
- Scalloped foreleg surfaces retain the sampled-volume construction rhythm.
- Rounded paw soles lack convincing supported contact.
- Side-view framing clips the tail; the evidence camera must change.
- Coat masses and painterly material are absent; the anatomy gate must pass first.

Technical observations: 83,518 base body vertices; GLB imported into a fresh Blender scene as four meshes, zero armatures and zero animation actions. Initial GLB forward direction is +Z; the initial metrics field claiming -Z was incorrect. Round 2 adds an explicit export-root rotation to correct that. Technical success does not override the art rejection.

## Round 2 correction scope

Continuous authored lofts replace the trunk, muzzle, cheek and limb constructions; reduced ears; smaller and more embedded eyes; lowered croup; flat paw contact; full tail framing. A ground-origin export root rotates the GLB into the game's -Z convention while keeping the editable Blender source in -Y modeling orientation.

No premium fur/material pass is authorized by the round 1 form result. Review the corrected neutral evidence first. No rigging, animation or gameplay integration.

## Round 2: ART REJECT

Actual five-view render set from run 39408342591 was downloaded and inspected. Improved: full tail framing, smaller ears, cleaner forelegs, less pendulous cheeks. Remaining: overly straight trunk, long-legged silhouette, abrupt haunch transition, oval smooth tail and insufficient facial structure. Premium fur/material pass remains withheld.

The generated .blend, GLB and five-view evidence are committed at d1fc12762c3dc389cbf4a4f6f5c2a0c5899582a0. Independent container inspection verified GLB 2.0 header/length, four meshes, two materials, no skins/actions and the explicit -Z-facing root. Round 2 test export has 616,208 triangles; it is a high-resolution study, not a production mobile character.

## Round 3 correction scope

Compact lower limbs, subtly broader/shorter head, curved ribcage-to-loin transition, smoother haunch root, tapered descending tail brush. Test GLB receives a temporary reduction modifier while the .blend retains the editable high-resolution sculpt surface. Neutral sheet is composed entirely from actual Blender PNGs.

## Final round 3: ART REJECT

### Evidence actually reviewed

All five round 3 Cycles renders plus their neutral review sheet were downloaded from completed run 39409188360 and visually inspected at full size. Render-source commit: 02120717ed8537577dd67481d1c4af9f27b1e80f. Blender 4.2 ran on a GitHub Actions CPU runner, not on the local host. The .blend contains the genuine mesh and editable subdivision; geometry was built with a Blender Python construction script, voxel union, smoothing and a proportion deformation. This is not claimed to be an artist's manually sculpted surface.

### Why it fails

- Recognizable generic fox, but insufficient specifically arctic winter-coat identity.
- Face is too blank and toy-like: bead-like eyes without developed sockets/lids, flat cheek transitions, absent mouth structure and weak muzzle-pad definition.
- Shorter limbs improve the ratio, but straight forelegs and schematic hocks do not yet provide professional anatomical credibility. Paw forms remain underdeveloped.
- Chest and tail remain smooth envelopes; no sculpted layered coat masses exist. A fused mesh is not the same as sculptural coherence.
- The rear and distance views are readable as a quadruped with a large tail, but lack the intended handcrafted character and expressive hero silhouette.
- The distance preview uses a studio orthographic camera. It is not calibrated to the actual gameplay perspective camera and cannot establish in-game/mobile acceptance.

### Gate decision

The neutral anatomy/form gate has not passed. Premium fur sculpt and painterly materials are therefore deliberately NOT applied. Retopology and rigging readiness are NOT certified. The requested premium hero deliverable is not achieved. This checkpoint is a rejected, non-rigged 3D character study with preserved evidence, not an accepted production character.

### Technical validation

- GLB 2.0 container and buffer length checked; fresh Blender import succeeded.
- Test export: 149,088 triangles, 74,795 exported vertices, four meshes and two neutral materials; 3,583,060 bytes.
- One connected component for the body; each intentional face component also connected. Zero degenerate triangles and zero nonfinite coordinates in this inspection.
- +Y up, -Z forward verified from the parent rotation and nose marker. Ground-origin export root; Blender source models forward along -Y.
- Actual study height: approximately 1.080 m at existing project proxy scale. This is NOT a claim of real animal size or final environmental scale approval.
- No skins, armatures or animation actions. No Three.js runtime/device test, full Khronos certification, LOD or production performance claim.
- Test GLB is reduced separately; editable .blend retains the denser sculpt foundation. Retopology remains future work.

### Recommended next iteration: LN-FOX-R01b, head-and-chest sculpt gate

Use the .blend only as an editable starting volume. Work directly on cranial planes, almond eye sockets and lids, muzzle pads/mouth line, and broad flowing cheek-to-chest ruff. Review close-up and full silhouette in neutral clay before expanding detail elsewhere. Rework the hocks and paw support with anatomical reference before authorizing the coat pass. Do not spend another iteration making small parameter adjustments across the whole body. An actual hands-on Blender sculpt workflow is the stronger next method for the quality gap demonstrated here.

### Boundaries

No Hero Spruce assets, gameplay, rigging, animation or production integration changed. No merge or deployment performed. Only the isolated art workflow, fox source scripts, review documents and generated study assets were added.

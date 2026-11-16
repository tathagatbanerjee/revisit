> Historical project record, preserved as research evidence. Plans and commands
> below are not current Revisit operating instructions. Original source: `archive/2026-10-19/brush-mosca-multiphone/shared-person/camera13-result.md`.
> Original SHA-256: `e5478bd5ddae69be4086d36e28173a4943f7d7ebfbfc80684255dc2470610ca0`. Private media/logs are not included.

# Camera 13 coverage audit and pair result

Subsequent work: MASt3R now runs locally (historical reference: `mast3r-result.md`). The selected
confidence-filtered output fails, but rejected-match diagnostics support
correspondence-acceptance validation as the next step. The NCC record below
remains unchanged.

19 October 2026. **Camera 13 has useful full-body observations and synchronized
source clocks, but the fixed 21/13 dense comparison still fails initialization
readiness.** It adds a few shoe samples, not complete feet or a complete person.
No Gaussian fit, paid compute or evaluation-camera access occurred.

## Source and input audit

CMU supplied the requested original: 8,445,549 bytes, SHA256 in
provenance (historical reference: `camera13-input.json`). H.264, 1920×1080, 30000/1001 fps, 101 frames,
3.370033 seconds; full decode passes. Camera 21 has the same 101 presentation
timestamps with zero residual. Inspected states 0/10/19 correspond to
0/1.5015/2.9029 seconds; arm phases agree. This supports authored synchronization,
not independent trigger accuracy. Preparation took 9.56 seconds.

The official [Panoptic toolbox](https://github.com/CMU-Perceptual-Computing-Lab/panoptic-toolbox#license)
documents noncommercial/research use and citation. Images remain private under
the existing corpus policy. The website lookup timed out, but the specific CMU
data URL succeeded. No mirror or additional view was used.

Source coverage (historical reference: `../../working/shared-person/camera13/source-coverage.jpg`)
shows head, hands and both shoes in frame; face/fingers and hidden body surfaces
remain partly occluded. Camera 13 is now **seen training input**. The earlier
training-view proposal is a historical snapshot; its `rgbRead:false` describes
that earlier time.

State 0 uses a hand-traced person polygon with two-pixel erosion at 640×360.
Mask vertices (historical reference: `camera13-mask.json`),
overlay (historical reference: `../../working/shared-person/camera13/mask-overlay.jpg`) and
review (historical reference: `camera13-review.json`) are retained. Camera 21's automatic conservative
mask is unchanged. This asymmetry limits attribution to camera choice alone;
this is not a mask-method comparison.

## Fixed-setting pair result

The exact previous dense code and settings are hash-verified: 256 inverse-depth
planes over 1–6 m, 9×9 NCC patches and unchanged confidence/geometric filters.

| Reference | Confident depth pixels | Reciprocal pixels | Person-mask coverage |
| --- | ---: | ---: | ---: |
| 21 | 3,170 | 1,369 | 7.72% |
| 13 | 1,881 | 1,320 | 10.23% |

The 2,689 directed observations yield **2,375 distinct 5 mm bins**. Coarse
head/hands/feet groups contain 195/211/**8** bins. These correlated samples and
image boxes are not anatomical ground truth. See measurements (historical reference: `camera13-pair-report.json`).

The unchanged gate fails on camera 21's 10% coverage minimum and the foot group's
20-bin minimum. Visual inspection fails too: most shirt/pants surfaces remain
empty and the foot matches cluster around one shoe/ankle. Adding the pair to
the previous observations gives **10,560 bins**, up from 8,812, without repairing
the missing surfaces. The union includes old 02/00/24/21 and new 21/13 observations;
it does not establish new matches between 13 and 00/24/02. Old files are intact.

Inspected private outputs:

- Source/support/depth (historical reference: `../../working/shared-person/camera13/pair/pair-diagnostics.jpg`).
- Pair and union clouds (historical reference: `../../working/shared-person/camera13/pair/cloud-comparison.jpg`).
- Shoe candidates (historical reference: `../../working/shared-person/camera13/pair/foot-crops.jpg`).

## Foot rejection diagnosis

The diagnostic (historical reference: `camera13-foot-diagnostics.json`) counts pixels in coarse foot boxes:

| Reference | Person mask | Whole patch inside mask | Enough texture | Confident | Reciprocal |
| --- | ---: | ---: | ---: | ---: | ---: |
| 21 | 1,289 | 714 | 326 | 65 | 4 |
| 13 | 816 | 240 | 30 | 4 | 4 |

Small image footprint, conservative boundaries and low texture remove most
shoe-interior candidates before geometric consistency. This diagnoses this
640 px configuration; it does not prove original-resolution texture is absent
or all methods must fail. Do not relax filters or assign silhouette interiors
measured depth. Point density alone does not establish body completeness.

## Verification, resources and next decision

Pair runs took 8.76/9.08 seconds, peaking at 568.94/569.16 MiB RSS, under the
600-second timeout. Numeric results and all artifact hashes match between runs.
The camera 13 workspace, including source/repeats, occupies about 32 MiB.
Source/mask/control/prior-output hashes pass; clouds/colors are finite, cycles
meet bounds, and world transforms agree within 1e-7 SfM units. All six geometry
tests pass; all four original clips pass `prepare_footage.py --verify-only`
unchanged. Imagery and points are Git-ignored. See verification (historical reference: `camera13-verification.json`).

Keep camera 13's validated observations and stop adding views to unchanged
640 px NCC. Next investigate **one learned dense matching/depth initializer**
on the seen inputs, with code/weight/license pins, resource bounds, visibility
checks and real body-surface acceptance before installation/download. Distinguish
inferred depth from independently observed multiview support. Preserve the
body-initialized comparison C separately; A still precedes coherent motion B.

Camera 20 stays sealed until selected architecture candidates freeze. The Brush
room and inherited person stay fixed. No new model/browser candidate was made.

> Historical project record, preserved as research evidence. Plans and commands
> below are not current Revisit operating instructions. Original source: `archive/2026-10-19/brush-mosca-multiphone/shared-person/threeview-result.md`.
> Original SHA-256: `29280999b80b386f1fffc1999d31555e553b7e215b5c9ebea2d9550fc6b6c258`. Private media/logs are not included.

# Seen three-view check — 19 October 2026

**Full-person readiness still fails.** Actual third-view matches support much
of the previously confidence-rejected upper-body geometry. Neither shoe obtains
third-view support, and broad diagnostic boxes overstate anatomical coverage.
No replacement initializer or Gaussian model was exported.

The pre-run investigation (historical reference: `threeview-investigation.md`) and
hashed plan (historical reference: `threeview-plan.json`) fixed exactly two pairs, visibility regions,
join and geometry rules before inference. Source/checkpoint/environment pins
are unchanged. Mask13 remains manually traced while other masks are automatic
conservative derivatives. All images are previously seen training data at state000;
evaluation camera 20 RGB was never read.

| Check |21/13 validated against24 |21/13 validated against02 |
| --- | ---: | ---: |
| New descriptor pair |21/24 |13/02 |
| Raw reciprocal matches |21,820 |379 |
| Pair matches passing masks/similarity/geometry |16,828 |0 |
| Unambiguous shared-image joins |5,103 |0 |
| Tracks passing third reprojection and3cm position agreement |4,584 |0 |
| Of those, rejected by the old>=1.5 confidence rule |4,370 |0 |

The accepted21/13/24 tracks have133 distinct5mm bins in the coarse head box,
59 in the image-left hand box and77 in the image-right hand box. All regional
tracks come from the old confidence-rejected cohort. Shoes have zero validated
bins. These are diagnostic image-region counts, not verified anatomy or complete
surface reconstruction. The numeric regional gate fails; the visual gate fails.

## Inspection changes the interpretation

The full-source overlays show broad shirt/upper-trouser support in all three
views, while the old high-confidence matches concentrate on shirt lettering.
Magnified, consistently numbered source patches show some agreeing hair features
and image-right wrist/watch/hand features. Much of the image-left “hand” support
is actually the adjacent trouser boundary; the head box also includes neck and
shirt collar. Do not translate59 hand-box bins into59 true hand-surface samples,
or claim a recovered face, fingers, complete head or both hands. Source boxes
were intentionally coarse; they are now demonstrated to be insufficient as an
anatomical readiness test. Preserve their pre-run definitions and failed result.

Both source shoes are visible in02, and its processed crop retains them. The
13/02 failure therefore is not a missing-foot crop. Saved-stage replay gives
379 raw pairs →332 after network borders →48 inside both person masks →2 with
fixed descriptor dot>=0.8 →0 calibrated epipolar-consistent pairs. No new
confidence cutoff was applied. The13/02 descriptors/matching fail in this
configuration; merely removing the previous confidence cutoff is insufficient.
Do not relax similarity/geometry gates to manufacture support. Viewpoint and
self-occlusion differ substantially, but this run does not isolate their causal
contribution. No alternate pair, role swap or crop was tried.

This is seen-data consistency using the same learned matcher with different
pair context, not independent ground truth, held-out quality, or a visibility
oracle. Mutual-nearest spatial joining can still associate nearby surfaces.
Third-view reprojection<=1.5px640 and pair position agreement<=3cm strengthen the
evidence without proving every accepted point correct.

## Runtime and verification

Two sequential CPU forwards took8.98s and9.11s; matching dominated. Total guarded
execution407.77s, sampled peak3,170.93MiB, worker peak3,265.06MiB, below5GiB/900s.
Initial available RAM9.14GiB. Two CPU threads, no GPU, new download, paid compute
or unrelated application changes. Raw matches, crops and tracks remain private
in ignored `working/shared-person/mast3r/threeview/`.

All 11 focused geometry tests pass, including duplicate/ambiguous joins and
third-view outlier rejection. Dependency check passes. Exact saved-coordinate
replay reproduces every join and acceptance decision without rerunning inference.
Crop tensors match the upstream loader. Plan/input/source/checkpoint/artifact
hashes, fixed room/person controls and every frozen293-bin candidate artifact
verify unchanged. See machine report (historical reference: `threeview-report.json`),
bounds (historical reference: `threeview-bounds.json`), verification (historical reference: `threeview-verification.json`) and
foot-stage diagnostic (historical reference: `threeview-foot-diagnostic.json`).

Inspected source grid/crops,24 full-source accepted-track overlay, magnified
regional patches for both trios, and02 network crop. The separate visual-review
receipt retains the image hashes; the numeric report's visual gate stays false.

## Next step

Close the anatomy/foot evidence gap before joint initialization. Mark genuinely
homologous visible shoe and hand details in the existing native21/13/02 images,
recording occluded or unidentifiable details explicitly; approximate semantic
centers and silhouette tips are not automatically the same3D surface point.
Use those observations to test the saved21/13 geometry without new inference.
If actual common foot details cannot be identified, record that limitation;
then scope one targeted21/02 correspondence trial with the same cached model,
fixed manual inspection targets and finite limits, rather than repeating13/02
or sweeping thresholds. Do not open20 or start Gaussian fitting from this result.
Once credible coverage exists, initialize jointly from all selected synchronized
training views with per-point provenance, then implement observed-surface growth.

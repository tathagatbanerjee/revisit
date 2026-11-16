> Historical project record, preserved as research evidence. Plans and commands
> below are not current Revisit operating instructions. Original source: `archive/2026-10-19/mosca-observation-registration/result.md`.
> Original SHA-256: `0b2d9b55d2055d9ae262e74841c0b9b281294148b08a82dd234a2cb03353558a`. Private media/logs are not included.

# Result — 19 October 2026

**Background selection passes; real alignment stops at insufficient correspondences.** The new subsets retain substantially more native room geometry, but this classical RGB-assisted matcher finds only one accepted cross-video proposal. No real similarity can be estimated from one point. No merged scene was created.

| Check | Outcome |
| --- | --- |
| Observation-supported selection | PASS:16564 A/11780 B static Gaussians |
| Spatial support | PASS: all four quadrants/model exceed50 points |
| Known A-person membership |0 retained; no precise B membership claim |
| Shuffled known-transform control | PASS:30 correspondences; rotation error1.88e-14deg |
| Middle70% partial-overlap control | PASS:20 correspondences; rotation error1.93e-14deg |
| Native pixel/lift convention | PASS: maximum1.46e-5px |
| Tied-descriptor rejection | PASS; explicit repeated-grid fixture also rejects |
| Real appearance association |1 accepted mutual-ratio match; insufficient |
| Real similarity fitting | NOT RUN: fewer than three correspondences |
| Reserved room/person scoring and transformed union | NOT RUN: no candidate transform |

The local run took47.93s with329.5MiB peak RSS. No paid worker, model download or reconstruction training was needed. All215 frozen source files—including every original MoSca state, selected source RGB, masks and A membership—are unchanged. The existing viewer4318 is unchanged; camera20 RGB remains sealed.

## What changed

A seed can now qualify through several clear observations even if the person covers it in other frames. Eligibility also requires source-colour agreement, full-scene depth/alpha/spread support and an observation span. A's four quadrant counts are5875/5689/2580/2420; B's are3889/4117/1436/2338. This is a compound observation policy, not an isolated proof that any one criterion caused the retention gain.

Native subset renders retain recognizable wall-panel seams and markers. Black holes are excluded matching evidence, not holes deleted from the original models. Only subsets used for finding alignment were produced. B still lacks validated complete-person Gaussian membership; broad masks, depth consistency and inspected subset views do not certify semantic ground truth.

## Where it stops

After native-image extraction, descriptor-footprint checks, selected-geometry support, composited-depth checks and duplicate image-bin suppression, only30 A and62 B features remain. The underlying masked SIFT detector finds18–36 A and68–91 B features per frame; its1500-feature cap is not binding.

Thirteen pairs are mutual nearest descriptor neighbours before the ratio checks, but only one passes the required two-way0.70 ratio. Their median forward ratio is0.859, consistent with weak distinctiveness under this descriptor. The room has many visually similar markers/panels, but this test does not isolate repetition, viewpoint change or extraction settings as the cause. Thresholds were not weakened after the failure.

This tests **source-image SIFT associations lifted through MoSca geometry**, not pretrained BUFFER-X on the new point subsets. Successful same-model controls establish transform mechanics under shared descriptors; they do not establish reliable independent-scene association. Image-bin duplicate suppression is not verified physical-landmark identity.

The initial tied-descriptor control used real feature positions. The explicitly planned8×8 planar grid fixture was added after the real association failed, before any real similarity could run; it also rejects. This negative control only covers tied descriptors, not arbitrary repeated-room ambiguities. In raw `controls.json`, `passed` is the numerical control decision; the generic nested matcher `status` applies real-pair reserved-evidence checks, which are not applicable to these copy controls.

## Interpretation and next step

Observation-supported selection provides a larger, visibly useful native background input. That is promising input preparation. This run supplies **no new evidence that the two rooms or people can be aligned**, because it never estimates a real transform.

The most direct follow-up is to test the previously validated learned3D matcher on these frozen native background subsets, with its own known-copy/partial/ambiguity controls and the same independently scored room/person gates. That would isolate whether removing unsuitable matching evidence helps compared with the earlier full-MoSca BUFFER-X failure. It may still fail on repeated geometry or inherited depth inconsistencies. No such GPU inference was run here.

See the frozen test document (historical reference: `README.md`), execution record (historical reference: `docs/execution.json`), selection A (historical reference: `docs/selection-a.json`), selection B (historical reference: `docs/selection-b.json`), controls (historical reference: `docs/controls.json`), matching diagnostic (historical reference: `docs/diagnostic.json`), verification (historical reference: `docs/verification.json`) and next steps (historical reference: `next-steps.md`).

Local inspected images: A selection (historical reference: `../working/mosca-observation-registration/a-selection-inspection.jpg`), B selection (historical reference: `../working/mosca-observation-registration/b-selection-inspection.jpg`), single match proposal (historical reference: `../working/mosca-observation-registration/single-match.jpg`). Heavy media/models remain ignored and are not distributed in Git.

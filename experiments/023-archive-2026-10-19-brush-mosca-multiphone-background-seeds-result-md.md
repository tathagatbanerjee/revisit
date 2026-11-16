> Historical project record, preserved as research evidence. Plans and commands
> below are not current Revisit operating instructions. Original source: `archive/2026-10-19/brush-mosca-multiphone/background-seeds/result.md`.
> Original SHA-256: `31e7c5d3944eee283bcd635d88ee7767f086824f980253e91e20abd87622cce5`. Private media/logs are not included.

# Background seed and optimization results

Renderer follow-up: the calibrated trial (historical reference: `../calibrated-multiview/result.md`)
finds that white backfill differs materially from Brush's native black-backed
rendering for this translucent background. The historical numbers below remain
valid for their stated render setup, but do not isolate geometry or SH fidelity.
The full-SH diagnostic is not evidence that retaining SH is generally harmful.

17 October 2026. Static-person seed removal alone produces small gains, with
visible background streaks remaining. A separate 12,000-step easy-phone fit
improves fitted-view background fidelity further, while leaving reconstructed
people byte-identical. Full MoSca remains substantially better overall, and
changed viewpoints still expose severe holes/tearing. The
locked baseline/development decision (historical reference: `../decision.md`) remains unchanged.

## Inspect in the harness

Open http://localhost:4318, select **Brush + MoSca · whole-person layer**.
For **Day · phones, easy**, compare:

1. **MoSca control · all points** — unchanged quality baseline.
2. **whole-person hybrid · experimental** — previous corrected hybrid.
3. **clean-seed hybrid · candidate** — filtered initialization, 3,000 steps.
4. **clean-seed hybrid · 12k candidate** — same filtered initialization,
   longer training horizon, the strongest new outdoor hybrid candidate.

There is also a new indoor **clean-seed hybrid · candidate**. Its change is
small; keep the previous indoor whole-person hybrid as the reference hybrid.
No new foreground/motion optimization or simultaneous-camera fusion occurred.

At the original view, the 12k outdoor candidate has less intense background
streaking and a more continuous deck than the 3k candidates. It still has
coarse/ghosted floor detail and blurry building/chairs. Standing people remain
present, with the same silhouette halos. A shifted camera still tears through
the performer and exposes room/deck holes. This is a modest fitted-view
improvement, not a solved background or validated geometry improvement.

## Controlled changes and measurements

The first two fits reconstruct the exact prior seed subsample, then remove
only semantic static-person indices: **823 of 10,176** seeds indoors and
**1,565 of 14,836** outdoors. The unfiltered seed files match the original
byte-for-byte. Remaining seed order, camera/image/mask contents, 3,000-step
profile, growth stop 1,800, seed 42 and resolution 640 are unchanged. All images
and cameras remain from the lead recording; the evaluation camera stays unused.

The separate outdoor fit changes the total training horizon to 12,000 steps
from the same filtered initialization. Its other explicit optimization flags
are unchanged, including growth stop. Default schedules may depend on total
steps; this is a fresh fit, not a continuation with an identical first 3k path.

Mean RGB absolute error against source values normalized to 0–1, over the same
20 actual source-view snapshots, with matched DC appearance and no point
subsampling. Render values are evaluated before display clipping:

| Scene and region | Full MoSca control | Previous hybrid | Filtered seeds, 3k | Filtered seeds, 12k |
| --- | ---: | ---: | ---: | ---: |
| Easy phones, background | 0.0105 | 0.0892 | 0.0879 | 0.0723 |
| Easy phones, floor | 0.0108 | 0.1150 | 0.1126 | 0.0960 |
| Easy phones, people | 0.0291 | 0.0473 | 0.0474 | 0.0470 |
| Single person, background | 0.0074 | 0.0718 | 0.0716 | Not run |
| Single person, floor | 0.0071 | 0.0706 | 0.0690 | Not run |

Background excludes padded automatic person masks. Floor is the bottom 40% of
the image, excluding those masks; person error uses masks with the padding
removed. These images participated in fitting. This measures source-view
fidelity, **not independently held-out accuracy or 3D completeness**.

Seed filtering reduces background error by about 0.2% indoors and 1.6% outdoors;
floor error falls by about 2%. Longer optimization reduces outdoor background
error by **17.8%** and floor error by **14.8%** relative to the filtered 3k fit.
Relative to the previous hybrid, these reductions are 19.0% and 16.5%. The full
MoSca control still has much lower error and cleaner observed surroundings.

The corrected people geometry, opacity, DC colour and membership are copied
unchanged into every new snapshot. Background changes can affect person-region
RGB through translucent boundary pixels; this does not imply new motion.

Detailed records: indoor seeds (historical reference: `indoor-panoptic-person-report.json`),
outdoor seeds (historical reference: `outdoor-day-phones-easy-report.json`),
outdoor 12k (historical reference: `outdoor-day-phones-easy-12k-report.json`).

## Retained appearance diagnostic

One additional diagnostic evaluates the saved outdoor Brush degree-3 world-space
SH with unchanged DC people, without fitting. In the shared native renderer,
background error worsens from 0.0892 to 0.1165 for the old background and from
0.0879 to 0.1147 for the filtered 3k background. These renders are retained,
but no full-SH hybrid is promoted or added to the viewer.

PLY coefficient ordering and camera-to-Gaussian direction were checked against
the pinned Brush [exporter](https://github.com/ArthurBrussee/brush/blob/3edecbb2fe79d3e2c87eeab85b15e0b1dd10d486/crates/brush-serde/src/export.rs)
and [shader](https://github.com/ArthurBrussee/brush/blob/3edecbb2fe79d3e2c87eeab85b15e0b1dd10d486/crates/brush-render/src/shaders/project_visible.wgsl),
and the installed Spark 2.3.1 direction convention. This still needs pixel
parity against Brush's own renderer before drawing a general conclusion about
SH fidelity. See the diagnostic report (historical reference: `appearance-report.json`).

## Native evidence and resources

All three candidates passed real-browser loading, final-state seeking,
fixed-camera playback/rewind, frozen-time orbit and reset without page errors.
Their first/final/shifted screenshots were inspected. All 60 snapshots passed
finite fields, quaternion normalization, strict source clocks, fixed-layer
identity, moving-geometry changes and model hashes. The people suffix is
byte-identical to the preceding hybrid at every event time. Seed subset indices
and unchanged input hashes were checked, including exact 3k/12k initialization
equality. All four transfer archive hashes and the per-file manifests passed.
Harness syntax, all eight existing tests, Compose configuration and Python
compilation passed. Browser checks use SwiftShader and do not establish GPU
throughput. See verification.json (historical reference: `verification.json`).

- Outdoor filtered 3k (historical reference: `../../working/multiphone-tests/outdoor-day-phones-easy/background-seeds-12k/before-fixed-000.png`),
  12k first (historical reference: `../../working/multiphone-tests/outdoor-day-phones-easy/background-seeds-12k/after-fixed-000.png`),
  12k final (historical reference: `../../working/multiphone-tests/outdoor-day-phones-easy/background-seeds-12k/after-fixed-029.png`),
  12k shifted (historical reference: `../../working/multiphone-tests/outdoor-day-phones-easy/background-seeds-12k/after-alternate-029.png`).
- Indoor filtered first (historical reference: `../../working/multiphone-tests/indoor-panoptic-person/background-seeds-v1/after-fixed-000.png`),
  indoor shifted final (historical reference: `../../working/multiphone-tests/indoor-panoptic-person/background-seeds-v1/after-alternate-035.png`).

The two seed-only fits took 18.30 seconds indoors and 21.62 seconds outdoors.
The separate 12k fit took 73.04 seconds. Those command times include Brush
startup; native diagnostics/retrieval are additional. No new cloud resource,
motion model or footage was created. Vulkan whole-GPU training peak memory was
not measured for these fits; report render-only PyTorch allocation separately.

Heavy models, logs, seed indices, images, transfer archives and browser evidence
remain ignored/private. The Pod remains available under the unchanged US$4
allowance and **17 October 14:28:28 Sydney** watchdog cutoff. Do not infer an
extension or another automatic fitting sequence from these candidates.

## Reproduction

On the existing pinned worker, run `runpod/refit-background-seeds.py CASE` for
the initial seed-only fit. For the separate easy-phone comparison, pass
`--steps 12000`; the first filtered fit must exist. Both refuse to overwrite
their output directories. `runpod/inspect-background-sh.py CASE` performs the
separate saved-fit colour diagnostic without fitting. Retrieve the results and
verify archive/per-file hashes before publishing locally:

```bash
working/brush-mosca/tools/bin/python runpod/publish-background-seeds.py working/multiphone-tests/SCENE
working/brush-mosca/tools/bin/python runpod/publish-background-seeds.py working/multiphone-tests/outdoor-day-phones-easy --steps 12000
working/brush-mosca/tools/bin/python runpod/validate-batch.py --prefix seed --report working/multiphone-tests/seed-all-validation.json
```

`runpod/inspect-batch.mjs` accepts `EXPERIMENT_ID=brush-mosca-people` and a
comma-separated `RUN_IDS` selection for the three new candidates. Earlier
controls and hybrids are immutable and need no re-export.

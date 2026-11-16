> Historical project record, preserved as research evidence. Plans and commands
> below are not current Revisit operating instructions. Original source: `archive/2026-10-19/pipeline/brush-mosca/person-masks-result.md`.
> Original SHA-256: `eb6b4b1c42e722ff7f6f9c826ece273cc19a965f13cc29e5d14ec3b0f193a9a7`. Private media/logs are not included.

# Visitor-mask follow-up result

2026-10-14. **The visible carpet and lower pedestal return in the hybrid viewer.**
They remain blurred/stretched; this is an improvement over the broad-mask void,
not a demonstration of accurate or complete floor geometry. The prior H1 scene
is preserved for comparison. Only the static fitting masks changed.

Open **http://localhost:4318**, choose **Brush + MoSca hybrid scene**, then
**H1 precise masks · Brush + MoSca hybrid**. Compare with **H1 · Brush + MoSca
hybrid**, or compare the corresponding Brush-background-only runs. Original
higher-order-SH exports remain separately selectable.

## Controlled change

Thirty source images, camera poses/intrinsics, sparse initial points, alignment,
MoSca model, train/holdout split, 3,000 steps, growth stop 1,800 and seed 42 stayed
fixed. The earlier mask kept only the top 220/360 pixels. The new recipe excludes
individual visitors with manually reviewed padded rectangles, plus localized
crowd regions. It is not automatic semantic segmentation or an exact silhouette.
Six clean images retain all pixels. Source frames are not painted or generated.

The masks retain **92.7% of image pixels** and **81.5% of the previously excluded
lower 140 rows** on average. All 30 originals/overlays were reviewed; the last
crowd views received corrections after full-size inspection. The versioned
recipe (historical reference: `resources/person-mask-recipe.json`) and
preparation/check scripts (historical reference: `prepare-person-masks.py`) make the inputs reproducible.
Images/masks were undistorted consistently using the same H1 cameras.
The inherited worker status label still said “floor excluded”; that was a
hardcoded H1 label, not the mask content. Actual reviewed masks/archive hashes
and the renders demonstrate the changed input. Future status uses dataset
mask-strategy metadata; the logging correction needed no fitting rerun.

Brush v0.3.0 produced **9,801 Gaussians**, versus 9,912 for the original H1 fit.
The masked-load smoke took **8.53 s** and the final command **22.93 s**. Sampling
observed **366 MiB GPU use / 70% utilization** during fitting; this is not a full
peak or host-RAM measurement. The prior MoSca moving slice is unchanged, with
14,188 displayed Gaussians (fixed stride 2 from 28,376). Twenty hybrid snapshots
contain **23,989 Gaussians each**, ending at 35/12 = 2.9167 s.

## Inspection and limitations

Matched screenshots compare old/new Brush backgrounds and old/new hybrids at
the identical source camera plus three previously localized held-out poses.
The new background alone shows red-carpet appearance and more pedestal/lower-wall
coverage, so the difference does not come from adding the moving carpet artifact
in MoSca. No recognizable permanent foreground visitor was apparent at the
inspected source view, but small mask-border/shadow artifacts remain possible.

At the shared source pose, the lower-band fraction substantially different from
the clear-screen colour rose from **28.1% to 82.3%**. Red-carpet-colour pixels
rose from **2.0% to 25.3%**. These are appearance diagnostics over a screen band
that also contains pedestal/wall/doorway pixels; they are not physical floor area,
geometry completeness, calibration or a reconstruction-quality score. Other
matched viewpoints were also measured and inspected.

Floor/pedestal edges are still smeared, and new viewpoints expose stretch and
missing coverage. The sparse initialization was deliberately left as the original
architecture-focused H1 model for this controlled comparison; newly unmasked
floor pixels have no new feature-triangulated anchors. A follow-up can add verified
static lower-surface features while retaining camera/world alignment. More fitting
alone would not validate unseen surfaces or guarantee navigation far from capture.
MoSca's moving component still carries its original carpet/visitor artifacts.
No joint multi-camera motion fitting or inferred identity/UTC was added.

Browser checks passed frozen-time orbit, fixed-camera time seeking, alternate-view
rewind, play/pause and actual final-state loading. Camera drift was zero within
the recorded check. Across all states, the new static background is byte-identical
and the foreground is **bit-for-bit identical to the original H1 moving slice**.
All Gaussian fields are finite and quaternions normalized. No per-frame alignment,
scripted actor motion, motion interpolation or synthetic floor was introduced.
The native Brush SH export was inspected separately. Software-rendered browser
checks do not measure desktop GPU throughput or calibrated accuracy.

## Setup failure and cleanup

The initial worker failed before training because an automatic Ubuntu update held
the dpkg package-install lock. Its console log is retained. A 300-second package
lock wait repaired bootstrap; exactly one replacement launched only after the
first instance and disk were verified removed, under the original four-hour
cutoff and US$6 allowance. No parallel workers or larger inputs ran.

The completed worker self-shut down after export, and outputs were retrieved.
Final termination/access/disk verification and the measured cost allowance are
recorded in the cleanup report (historical reference: `person-masks-cleanup-report.json`) and
the lightweight trial report (historical reference: `person-masks-trial-report.json`). Both instances,
all job volumes, temporary roles/profile, security group and schedule are removed.
Cleanup finished at 2026-10-14T11:23:55.684373+00:00; independent audit passed at
2026-10-14T11:26:22.724445+00:00.

The conservative combined launch-to-verified-termination/cleanup allowance is
**US$0.255 compute**, including failed setup and post-shutdown intervals.
Allow roughly **US$0.30–0.50 total before tax**, not an AWS invoice; actual billed
compute can be lower than this conservative allowance. About 16.2 MB current
S3 objects / 20.8 MB including versions remain private, below US$0.001/month at
the earlier indicative Sydney storage rate while unchanged. No GPU continues.

## Reproduction

Use the existing isolated tools venv and preserved H1/native MoSca evidence:

```bash
working/brush-mosca/tools/bin/python pipeline/brush-mosca/prepare-person-masks.py
# Review all overlays in working/brush-mosca/person-masks/review-grid/.
# Mark mask-review.json reviewed only after inspecting/correcting the recipe.
working/brush-mosca/tools/bin/python pipeline/brush-mosca/check-person-masks.py
HYBRID_TRIAL=person-masks working/brush-mosca/tools/bin/python \
  pipeline/brush-mosca/prepare-brush-dataset.py
```

`HYBRID_TRIAL=person-masks` selects a separate manager state/input/output namespace.
The historical launch used `infrastructure/aws/hybrid-worker.py start`; that job
state now prevents an implicit relaunch. The scoped `retry-setup` permits only
one verified dpkg-lock replacement and preserves the original deadline. Existing
inputs/worker access stay prefix-only; no new project key or browser credentials.

After separately selected authorized fitting, download/cleanup/audit and publish
using that same environment selector. `publish-h1.py` refuses to overwrite runs
and gives the follow-up `-person-masks` IDs. The same `inspect-h1.mjs` validates
playback with `PLAYBACK_RUN_ID=brush-mosca-h1-person-masks`. `compare-h1.mjs` accepts
`COMPARISON_RUNS=brush-h1-background,brush-h1-background-person-masks,brush-mosca-h1,brush-mosca-h1-person-masks`
and the original H1 `comparison-poses.json`. `measure-floor-appearance.py`
records the limited colour/clear-screen diagnostics after matched screenshots.

Local evidence remains ignored under `working/brush-mosca/person-masks/`;
viewer runs are under ignored `output/runs/`. Plans, recipes, scripts and
lightweight reports are committed; media/models/credentials stay outside Git.

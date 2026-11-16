> Historical project record, preserved as research evidence. Plans and commands
> below are not current Revisit operating instructions. Original source: `guildhall-fixed-world-workflow/docs/core-pipeline-validation.md`.
> Original SHA-256: `15dc7c015f7f517ccac325ca0d42db955b2ed9fd88dcaa1cfca2e91264fee0a1`. Private media/logs are not included.

# Firming up the core pipeline

29 October 2026. Current direction: defer 360 cameras and unusual capture setups.
Use a few ordinary continuous videos to make the successful fixed-world path
repeatable, then measure where it needs to become faster or better.

Hardware preference: L40S if available. See current quote, rough costs and proposed staged caps (historical reference: `l40s-budget.md`).

## One clean sequence

**Video → frames → static map and locked cameras → cached depth/tracks/flow →
background depth refinement → motion scaffold and foreground review → appearance
fit → review and export.**

Use the existing COLMAP and fixed-world MoSca implementation. Keep its depth
propagation, positive-depth safeguards and camera-lock checks. No new renderer,
360 adapter, multi-video fusion or separate reconstruction architecture in this
batch. A scene without moving actors still exercises the same core stages;
record a motion stage as not applicable if there is no meaningful motion rather
than fabricating dynamic tracks or treating absence of people as tracking failure.

There are two substantive review points before final publication:

1. **Geometry ready:** one coherent camera map, adequate background observations,
   good projection overlays through the shot, and cameras actually locked.
2. **Ready for appearance:** corrected depth reaches the dense inputs, motion
   support is understood, and foreground assignments do not attach the room to
   people. If a stage fails, retain its outcome and stop that clip at that stage.

Do not create an automatic exploratory fallback that converts failed motion into
a passing result. A labelled exploratory continuation remains a separate decision,
as it was for Guild Hall. Quiet intervals need source review before calling their
low dynamic counts a failure.

## Use these videos first

Local sources have already been downloaded. The existing compressed 30-second
derivatives were resampled to 30fps; new preparations should use the originals
and preserve their timestamp mapping. See source provenance (historical reference: `../../archive/2026-10-19/docs/footage-sources.md`).

| Video | Characteristics | First fit | Duration follow-up |
| --- | --- | --- | --- |
| Sculpture orbit, original Postshot sample | Camera translates around mostly static outdoor geometry | 30s; existing 5–35s interval is a candidate | 60s from the same original after continuity review; original is 109.72s |
| El Kobba Museum exterior | Textured outdoor architecture, more limited baseline/view coverage | 30s; existing 5–35s interval is a candidate | Source is only 45.21s; no artificial extension |
| Guild Hall original recording | Indoor walk, turn, occlusion and visitors | Select a different continuous 30s interval from the saved 491.27s original | Nested 60s, then 120s if an uninterrupted useful interval exists |

The saved 25.333s fixed-world result remains our reference; no need to reproduce
it merely to begin. A new Guild Hall interval tests temporal generalization within
the same recording, not an independent new location. It should include visible
visitor motion if it is to test the dynamic part of the pipeline.

First inspect candidate intervals for cuts and usable camera translation. Original
duration alone does not establish a usable continuous segment. Sparse preview
frames help choose candidates but cannot certify that a whole interval has no cut.
Freeze exact intervals before training. If Guild Hall cannot supply a clean
120-second interval, find another original rather than concatenate shots.

Keep the underexposed, nearly fixed-camera pedestrian footage, very fast motion,
heavy reflections and camera rigs for later. This first batch needs useful
variation, not a collection of worst cases.

## Small execution order

1. Audit sources, select the three 30s intervals and save exact timestamps.
2. Make the current scripts accept a per-video configuration rather than Guild
   Hall-specific source paths, time windows, IDs and visitor assumptions. Reuse
   stage code; do not build a scheduler or a new framework.
3. Run the same recipe once on each 30s interval. Publish or record the stage
   that failed. Avoid adding an extra 3/6/12-second ladder to every video.
4. Extend a useful sculpture interval to 60s and a useful Guild Hall interval to
   60s, using the same start time and settings. These test length independently
   of changing scene. Cache/reuse compatible inputs, but regard each full fit
   as a separate measured run.
5. Extend the selected Guild Hall interval to 120s only after its 60s result and
   memory/runtime estimates justify it. Lengthen the continuous reconstruction;
   do not hide failure by stitching independently fitted windows.

This is three initial fits and at most three duration extensions, not every
duration crossed with every model and setting. Preparation can proceed locally;
paid execution needs a new explicit allocation because previous sessions closed.
No paid worker is started by this plan.

## Freeze the recipe for the first batch

- Start at the demonstrated 640×360/nominal 12Hz preparation, keeping actual source
  timestamps. Declare any aspect-ratio handling; update intrinsics with resizing.
- Keep the Guild Hall large-Metric3D/BootsTAPIR/RAFT recipe, observed-map background
  anchors and fixed-camera depth refinement as the initial candidate. Its cross-scene
  generalization is what we are measuring; do not quietly switch models per clip.
- Keep seed, losses, mask policy and geometry/motion review rules consistent.
  Replace absolute Guild Hall time windows with relative bins and explicitly
  annotated difficult intervals. No manual edits to suit a result after fitting.
- Use the current duration-aware appearance schedule initially and record exact
  steps and sampling policy. At 12Hz, 30/60/120 seconds are approximately
  360/720/1,440 observations. Longer clips can increase geometry work, memory,
  training exposure and exported sequence size; costs need measurement.

The current runners are experiment wrappers with fixed session names and paths.
The recipe works, but we do not yet have a general one-command new-video pipeline.
The first implementation change should be a thin configuration layer over those
stages, with one output directory per run and a way to resume from the last
successful stage. Keep the trained models and media ignored under `working/` and
the existing app output roots.

## Optimise after we have comparable results

First measure stage wall time, peak device memory and output size. The saved Guild
Hall appearance fit is the initial quality reference. Pick the largest measured
cost instead of assuming a larger GPU or more aggressive compression is needed.

The first speed experiment should be **the existing appearance schedule versus
half as many steps on one already successful 30s clip**, with identical inputs,
initialization, seed and sample policy. Compare native start/middle/end renders,
people, temporal consistency and shifted views. If quality remains useful, try
the shorter schedule on another successful clip before making it the default.
If it harms quality, retain the original schedule.

The first foreground-quality experiment, if people are the dominant defect,
should compare current visitor-box support with better person masks on the same
saved camera/depth package. Do this separately from the schedule experiment so
we can tell what changed the outcome. It is a candidate improvement, not already
validated behavior.

Do not tune resolution, frame rate, tracker, depth model, masking and appearance
schedule simultaneously. A small number of matched changes is enough to learn
which adjustments deserve inclusion in the core path.

## One results table, one visual review per run

| Record | Purpose |
| --- | --- |
| Source interval, observations and recipe | Know exactly what was tested |
| Stage outcome and camera/background checks | Locate failures before appearance |
| Native source-fit metrics and fixed review frames | Compare image fit within the same clip |
| Room stability, people/motion and shifted-view notes | Separate visual strengths and weaknesses |
| Stage times, peak memory, export size and session cost | Find actual efficiency bottlenecks |

Source-fit metrics remain development evidence. Do not rank unrelated videos by
PSNR or introduce a new physical/novel-view fidelity claim. Reuse the same review
times/view offsets within each clip's paired trials and show weak frames too.

We are ready to call this a firmer pipeline when all three ordinary 30s cases have
honest outcomes, at least one useful 60s and one useful 120s continuous result are
demonstrated, and a new clip can run through configuration without code edits.
Any missing duration stays explicitly unproven. No web dashboard, task queue or
broad camera abstraction is needed to establish that.

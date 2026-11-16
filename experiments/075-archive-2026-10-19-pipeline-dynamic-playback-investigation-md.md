> Historical project record, preserved as research evidence. Plans and commands
> below are not current Revisit operating instructions. Original source: `archive/2026-10-19/pipeline/dynamic-playback/investigation.md`.
> Original SHA-256: `defad4ed79c87c4e420ab2536aa4aa16d23ec5f491e32769baad4938a417e51f`. Private media/logs are not included.

# Milestone 2: independent time and viewpoint

Investigated 2026-10-14. Trial authorized by the user's request to move to
Milestone 2. Start with playback of an existing reconstruction; this does not
claim reconstruction of our footage or training from two arbitrary videos.

## Selected example

Use the `boxes` pretrained scene from Jonathon Luiten et al., **Dynamic 3D
Gaussians: Tracking by Persistent Dynamic View Synthesis** (3DV 2024).
[Project](https://dynamic3dgaussians.github.io/),
[implementation](https://github.com/JonathonLuiten/Dynamic3DGaussians),
[published files](https://omnomnom.vision.rwth-aachen.de/data/Dynamic3DGaussians/).
The authors reconstruct real CMU Panoptic multiview footage. Persistent
Gaussians have per-timestep means, RGB and rotations, and shared scales,
opacities and segmentation. That gives a common coordinate system across time.

The original viewer loads `params.npz`, uses a CUDA rasterizer and Open3D,
and plays at 20 timesteps/second. Its camera can remain interactive rather
than following a programmed orbit. Read its published `visualize.py` before
conversion. Inspected source revision:
`7dbbd4dec404308524ff402756bdb8143a2589b0`. The original CUDA/Open3D
viewer is not installed or run; its file layout and camera defaults are read
from this version. For our constrained WSL environment, use an equivalent CPU export
of existing Gaussians to timestamped degree-zero PLY snapshots and our Spark
viewer. No training, neural inference, CUDA extension build or scene fitting.
Preserve original Gaussian indices, positions and orientations; do not align
separate independently fitted frames. Inspect the native parameter layout
first, then compare frozen snapshots from two views in the harness.

## Terms and attribution

The authors' [license notes](https://github.com/JonathonLuiten/Dynamic3DGaussians/blob/main/LICENSE.md)
permit research/experimentation for the original rendering stack; most code
is MIT, but its Inria-derived rasterizer and `external.py` are restricted.
We do not install those components. The [CMU dataset terms](https://github.com/CMU-Perceptual-Computing-Lab/panoptic-toolbox#license)
limit the underlying recordings to noncommercial research. Keep the checkpoint,
derived PLYs and inspection captures ignored and local for this experiment;
this is not a commercially cleared asset. The model archive does not provide a
separate permissive model license; preserve this limitation rather than treating
MIT code as licensing the recording or trained asset.

Credit Luiten, Kopanas, Leibe and Ramanan, 2024, and Joo et al., *Panoptic
Studio: A Massively Multiview System for Social Motion Capture*, ICCV 2015.

Other candidates checked: CAT4D has small browser-ready dynamic assets but uses
generated multiview content, requiring stronger generated-content labelling and
asset-rights verification. CAP4D is controllable generated portrait animation.
IR-MichaelRF has aligned individual PLYs but requires an access request. The
PlayCanvas basketball flipbook is convenient but its example lists a creator
without explicit asset terms. None is needed for this first trial.

## Steps

1. Read the outer ZIP directory using HTTP ranges. The full model archive is
   11,574,992,208 bytes; avoid downloading six scenes. The `boxes/params.npz`
   member is 1,954,472,326 compressed bytes and 2,118,375,050 uncompressed bytes.
2. Download only that member, decompress incrementally, verify its ZIP CRC,
   and record a SHA-256. Save it under ignored `working/dynamic-playback/`.
3. Inspect NumPy array shapes/dtypes. Extract numerical arrays one at a time
   and memory-map them; never load the whole temporal checkpoint into RAM.
4. Export a small interval at reduced playback cadence, preserving the native
   20 Hz timestamps. Map RGB to degree-zero spherical harmonics, normalize
   WXYZ quaternions, retain log scales and opacity logits. No interpolation.
5. Publish an ignored `output/runs/` sequence and provenance with source frame
   indices, source URLs/hashes, terms, conversion and limits.
6. Add only the necessary standalone timeline play/pause support. Do not show
   our sculpture recording as evidence for this unrelated published scene.
7. Inspect time changes at fixed camera, camera changes at paused time, rewind,
   and a second view. Save screenshots/short recording and measured resources.
8. Record lessons and follow-up steps. Stop any temporary process; retain the
   local viewer and ignored small artifacts. No AWS resources to tear down.

## Costs and hard bounds

Incremental AWS cost: **US$0**, since download, CPU conversion and browser
playback run locally. No Lambda, GPU instance or cloud upload. Network transfer
is about 1.96 GB for one checkpoint member; ordinary local bandwidth/electricity
are not priced here. Reusing Spark 2.3.1 and Three.js 0.180.0 avoids adding a
second viewer runtime.

Bounds: one scene; at most 2.2 GB checkpoint download; at most 8 GB temporary
and output disk; export at most 25 snapshots from at most six seconds; first
export at 5 Hz or less; at most 250,000 Gaussians per snapshot, with deterministic
sampling only if needed and explicitly reported. CPU conversion target <1 GiB
RSS; browser target <1.5 GiB RSS. Check actual memory and stop/reduce if pressure
worsens. Local session cutoff 60 minutes, no paid fallback automatically.
The machine currently has ~840 GiB disk free but only ~3.1 GiB RAM available;
streaming and memory mapping matter more than disk. Browser software rendering
can verify interactions but does not establish desktop GPU frame rate.

## Evidence and the moved-chair requirement

A reconstruction is an estimate supported by recordings, not an observation
in itself. Keep three meanings separate: **observed** source content;
**reconstructed** spatial/temporal state fitted to that content; **inferred**
completion, transition or motion inside an unobserved gap. The first demo is a
published reconstructed sequence, with no locally attached source video.

If a chair is observed at A before a gap and B after it, the supported claim is
that its state changed within that interval. A candidate path/time/actor is a
best guess unless evidence supports it. Store the interval and links to the
before/after evidence; keep any proposed transition explicitly inferred and
optional. Do not create numeric confidence scores without calibration or animate
a guessed path as if it were recorded. Automatic object tracking, chair-event
inference and our own-video reconstruction are subsequent experiments.

## Preview adjustment after first inspection

The first export retained every second native Gaussian (175,711/frame). Its
software-rendered inspection process tree, including Chromium, Node and video
encoding, reached 1,562 MiB sampled RSS, slightly above the 1.5 GiB target.
Preserve that run in ignored working storage and use every fourth native
Gaussian (87,856/frame) for the final local preview. The initial export is not
retrained or refitted; sampling preserves the same indices across all times.

Limit standalone playback clock advances to 0.1 s per rendered frame and pause
the clock during model loading. This prevents a slow software-rendered frame
from skipping the whole event before the Pause button can respond. Scene-time
playback can therefore be slower than real time. This is a viability preview,
not a smooth native 20 Hz player or a performance benchmark.

## Outcome

First trial completed (historical reference: `result.md`): camera/time independence verified from two
views, with manual pause at 1.2 s. Final CPU export: 2.79 s / 326.4 MiB RSS;
119,493,900 bytes of PLYs. Sampled browser/test/encoder tree peak 1,519.9 MiB,
just below the 1.5 GiB target. Cloud cost remained US$0. See the result for
quality limits, adjustments, checks and retained artifacts.

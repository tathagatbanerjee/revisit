> Historical project record, preserved as research evidence. Plans and commands
> below are not current Revisit operating instructions. Original source: `archive/2026-10-19/docs/reuse-research.md`.
> Original SHA-256: `966fbdd8077678d978881cd985848d3fe62996f3eab6f71d7483976dcdbcbc2d`. Private media/logs are not included.

# Reusable components and first experiments

Researched on 2026-10-14 using vendor documentation, official repositories and
project pages. This is a feasibility assessment, not a benchmark. No tools or
model weights were installed and no reconstruction was run for this research.

The original recommendations below describe the initial research. SHARP has
since completed two real frozen-frame tests. Current milestones and method
priorities are maintained in the global roadmap (historical reference: `../pipeline/roadmap.md`), with
procedures in each package's own next-step document. The global aim is
independent control of time and viewpoint.

## Recommendation

Separate the first experiment into two small deliverables:

1. **Static map and inspection:** reconstruct the sculpture clip with MipMap,
   export a Gaussian PLY, and view it with SuperSplat. Keep the original video
   beside the map. Link inspection markers and camera poses to source times.
2. **Dynamic playback and reconstruction:** try an existing animated splat in
   Brush to establish camera movement and playback, then evaluate a small
   monocular reconstruction with RiGS. Begin with roughly 3–5 seconds at
   480p–720p, not all 900 frames. This is a proposed starting budget, not a
   verified memory requirement.

The first deliverable can offer a useful memory-exploration interface without
claiming that the static map preserves the recorded movement. The second tests
the harder independent-time-and-viewpoint part of the braindance concept.

## MipMap and the existing SDK

The user identified the archive as MipMap. A read-only ZIP listing confirms
270 entries including `reconstruct_full_engine.exe`, `gaussian_splat.dll`,
license utilities, and CUDA/PyTorch/TensorRT dependencies. No SDK documentation,
headers or examples were found in the listing. No binaries were executed.

The [current full-pipeline documentation](https://docs.mipmap3d.com/engine/en/basic/reconstruct-full)
describes a CLI driven by a task JSON and license key. It accepts
`video_meta_data`, with extraction interval, start and end settings, and can
emit Gaussian PLY or SOG via `generate_gs_ply` or `generate_gs_sog`.
`generate_ply` is a different output selector; use the explicitly Gaussian
option. For footage without GPS, the documented coordinate system is Local.

The [vendor's 360-degree guide](https://na.mipmap3d.com/blogs/360deg-videos-for-gaussian-splatting-what-you-need-to-know/)
describes direct supported-video import and capture while moving through the
environment. Our existing clips are perspective footage, not 360 captures;
add a real panoramic-camera recording when testing that specific workflow.

**Assessment:** MipMap is a strong candidate for a static scene-map backend.
The public documentation reviewed does not establish time-dependent 4D output.
Confirm the options supported by the bundled 5.1.0.6 version, activation, and
actual output schema before connecting it to a viewer.

The [SDK overview](https://docs.mipmap3d.com/engine/en/) lists Windows/Linux,
NVIDIA GPU support, at least 16 GB RAM, and 500 GB free storage. The generic
storage requirement exceeds the current physical free space on C:; we have
not established the smaller resource needs of a 30-second trial. WSL's virtual
free-space number must not be used as physical capacity. Existing license
activation is also unverified. Use a small run to measure resources once these
requirements are resolved, or use the fallback below.

## Shortlist

| Component | Reusable role | Fit for our first experiment |
| --- | --- | --- |
| MipMap Engine | Video/panoramic capture to static Gaussian map | Primary existing SDK candidate, subject to activation/version checks |
| Postshot | Direct video-to-static-splat application | Simple manual baseline if SDK integration is inconvenient |
| Brush | Static trainer, splat viewer, animated splat-sequence playback | Open alternative and first dynamic-playback viewer |
| SuperSplat Viewer | Browser navigation, annotations, optional walk controls | Lowest UI effort for the static inspection experience |
| Spark | Three.js Gaussian renderer and programmable modifiers | More control for custom camera, timeline and inspection UI |
| gsplat | Python/CUDA differentiable Gaussian rasterizer | Library foundation for custom training/rendering; not an end-to-end 4D importer |
| SHARP | Single-image Gaussian prediction | Quick explorable frozen-frame experiment with restricted nearby viewpoints |
| RiGS | Monocular dynamic reconstruction and interactive viewer | First custom-video 4D candidate; preprocessing and memory need evaluation |
| MoSca | Monocular 4D reconstruction with motion scaffolding | Established research alternative with substantial preprocessing |
| 4DGaussians | Dynamic Gaussian training, rendering and SIBR integration | Reference baseline, especially with its supported prepared datasets |
| videosplat | Multi-camera calibration/training/4D viewer orchestration | Consider when we have multiple simultaneous viewpoints |
| CAT4D | Generated multi-view video followed by dynamic Gaussian reconstruction | Inspiring interactive demo; not a verified turnkey local pipeline |

### Static training and viewers

[Postshot](https://www.jawset.com/docs/d/Postshot%2BUser%2BGuide/Getting%2BStarted)
accepts a video directly and exports Gaussian PLY. This provides a quick manual
comparison for our sculpture sample.

[Brush](https://github.com/ArthurBrussee/brush) trains from COLMAP or Nerfstudio
datasets, so extracting MP4 frames alone is not its full training pipeline.
It views PLY/compressed PLY and supports ZIPs of per-frame splats and a delta
frame representation used by CAT4D/Cap4D. Its code is Apache-2.0. Sequence
playback is reusable; timeline controls and our annotations may need work.

[SuperSplat Viewer](https://developer.playcanvas.com/user-manual/supersplat/viewer/)
is MIT licensed, self-hostable, and provides navigation, annotations and
optional walking controls. Use its standalone viewer or npm package. Its
camera animations should not be mistaken for replay of reconstructed events.

[Spark](https://sparkjs.dev/docs/) integrates splats into a Three.js scene;
its [Dyno modifiers](https://sparkjs.dev/docs/dyno-overview/) enable programmable
changes to splat attributes. It is a renderer, not a video reconstruction
model. Dynamic model formats require an adapter or sampled splat sequence.

[gsplat](https://github.com/nerfstudio-project/gsplat) is an Apache-2.0
Python/CUDA library with differentiable rasterization and training examples.
It is useful for custom methods and inspection rendering. Camera estimation,
motion modeling and video preprocessing remain pipeline responsibilities.
Pin versions: current main and packaged releases may have different features.

### Fast frozen-frame alternative

[Apple SHARP](https://github.com/apple-aiml-research/ml-sharp) predicts a
Gaussian scene from a single image and exports PLY. It targets nearby novel
views and avoids fitting a new scene from scratch for each image. Its CLI can
process a folder of frames. This is attractive for a first "pause the video,
move slightly around that moment" experiment.

**Assessment:** independent frame predictions do not create a globally aligned,
temporally consistent 4D model. Moving-camera frame sequences can drift or
flicker. Use a few frozen moments first, with explicit limited-view navigation.
The project has separate code and model licenses; review both when adopting it.

### Actual dynamic reconstruction

[RiGS](https://github.com/ladvu/RiGS) explicitly targets single monocular videos.
Its documented workflow uses ViPE for depth, poses, optical flow and masks,
then TAPIR/BootsTAPIR tracks, dynamic Gaussian optimization, and an interactive
viewer. The viewer renders static/dynamic/other scene components. It requires
CUDA/PyTorch setup and several checkpoints; it is not simply an MP4 import API.
No clear root license was visible in the reviewed repository listing; resolve
reuse terms and dependency licenses before incorporating its code.

[MoSca](https://github.com/JiahuiLei/MoSca) provides prior-model preprocessing
and 4D scene fitting, plus camera estimation through its MoCa module. It
supports several depth/point-tracking models. The authors describe the release
as a pre-release; their own code is MIT, with separate terms for incorporated
models/renderers. Useful as an alternative if RiGS does not fit our data.

[4DGaussians](https://github.com/hustvl/4DGaussians) provides actual
time-dependent scene training, rendering and SIBR viewer guidance. Its
documented datasets include D-NeRF, HyperNeRF and multi-camera video. The setup
uses older Python/PyTorch/CUDA dependencies and custom extensions. Start with
a supported example to distinguish setup failure from input-data failure.
Check the repository and upstream/submodule license terms before reuse.

[videosplat](https://github.com/Ahmedn1/videosplat) wraps several dynamic
backbones, calibration and a local browser timeline viewer. Its input is
multiple camera videos of the same event, including casual moving-camera
captures. The README discusses 16 GB VRAM operation and multi-GB keyframe
exports. It is promising orchestration code, but its documented budget is
larger than this laptop's GPU and it is not a direct fit for our single-view
corpus. Its algorithm paths have different capabilities and dependencies.

[CAT4D](https://cat-4d.github.io/) demonstrates independent camera and time
control in the browser using Brush. It generates missing viewpoints with
video diffusion before fitting deforming Gaussians. Use its interactive demos
to establish the target behavior; generated completion is not source evidence.
Availability of a complete local inference pipeline and weights was not verified.

## A 360 camera helps coverage, but does not solve dynamic reconstruction

A panorama captures many directions from essentially one position. Moving
the camera provides spatial baseline for a static map. At different times,
moving objects may have changed, so a surrounding-room capture does not
automatically supply simultaneous views of a person's motion. Two fisheye
lenses are not equivalent to a widely spaced synchronized camera rig.

For inspection, retain source video and timestamped poses. Keep generated
completion, occluded regions and weakly supported camera viewpoints explicit.

## Concrete experiment order

1. Verify MipMap activation and bundled CLI options; try the sculpture clip
   with a small frame set and Gaussian PLY output. Measure resource use.
2. Load the exported PLY in SuperSplat. Add three markers and source-frame links.
   Check coordinate orientation/scale and the supported navigation region.
3. Try existing dynamic splat playback in Brush before custom dynamic training.
4. Optionally predict one frozen frame with SHARP to compare the fastest
   inferred-geometry path with a multi-view static reconstruction.
5. Run RiGS on a short, downscaled single-video interval. Check masks, depth,
   camera trajectory and tracks before training. Use its own viewer first.
6. Only after a successful dynamic example, decide whether to adapt Brush,
   Spark or a backend-rendered viewer to our inspection UI.

Research from local `nvidia-smi` found an RTX 4070 Laptop GPU with 8188 MiB VRAM
and driver 581.57. WSL currently exposes about 15 GiB RAM and hosts active tasks.
Those tasks must remain running. None of the dynamic candidates has been
validated against this machine's available memory; do not promise full-length
1080p training or use published benchmark runtimes as local predictions.

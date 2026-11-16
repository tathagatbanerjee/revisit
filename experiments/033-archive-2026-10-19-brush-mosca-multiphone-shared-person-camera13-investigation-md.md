> Historical project record, preserved as research evidence. Plans and commands
> below are not current Revisit operating instructions. Original source: `archive/2026-10-19/brush-mosca-multiphone/shared-person/camera13-investigation.md`.
> Original SHA-256: `35a72eedd02b8c32aad106a60ac20f10152f3294069ba34366ac0410066d75ed`. Private media/logs are not included.

# Camera13 input audit and fixed-setting pair comparison

19 October 2026. The user requested proceeding with the proposed camera13
coverage/timing check. Scope: retrieve one existing Panoptic sample video,
audit its source and three instants, then run one local21/13 dense comparison
only after the input gate passes. No Gaussian fitting or paid infrastructure.
Camera20 remains reserved and unopened. Opening13 makes it a seen training view.

## Source and terms

Use only `171204_pose1_sample/videos/hd_shared_crf20/hd_00_13.mp4` from
`http://domedb.perception.cs.cmu.edu/webdata/dataset/`. The official
[toolbox README](https://github.com/CMU-Perceptual-Computing-Lab/panoptic-toolbox#license),
checked19 October2026, identifies this sample's31 synchronized HD views,
29.97fps extraction and noncommercial/research-only use with citation. Retain
the existing corpus's no-redistribution policy. The website times out in the
web tool; this is not evidence that the specific data URL is unavailable.
The official[download script](https://github.com/CMU-Perceptual-Computing-Lab/panoptic-toolbox/blob/master/scripts/getData.sh)
documents the CMU path and SNU mirror. Try CMU once; if unavailable, the same
relative source path at `http://vcl.snu.ac.kr/panoptic/webdata/dataset/` is the
only fallback. Record actual URL, response headers, byte count and SHA256.
Do not fetch skeleton/face/hand annotations, camera20 or another training view.

## Input gate

Preserve the prior calibration hash, evaluation reservation, source inputs and
fixed room/person control hashes. Fetch<=50MB, total download/preparation bound
180 seconds. Check full decode,1920x1080 dimensions, frame count and presentation
timestamps against the existing21 original. Extract source-clock states0/10/19
from the existing twenty-state event schedule, rectifying using supplied K and
distortion. Inspect head/hands/feet, self-occlusion, source margins and matching
motion phases in21/13. These are studio sources with documented synchronization;
agreeing PTS and visual spot checks do not measure independent trigger accuracy.

Before pair execution, record a manual coverage/mask review for state0. For this
one-image feasibility probe, trace camera13's visible person polygon at640x360,
erode two pixels to avoid uncertain boundaries, and record the vertices/hash.
Camera21 keeps its existing conservative automatic mask unchanged. This mask
asymmetry is explicit: the pair tests whether additional observed surfaces are
usable, not whether camera choice alone improves an otherwise identical full
pipeline. Save overlays and coarse head/hand/foot boxes before the matching run.
Do not invent hidden body surfaces or paint masks from an inferred skeleton.

## One bounded dense comparison

If source, timing and full-body audit pass, import the exact existing
`dense.py` settings and functions without altering their file or thresholds.
Run21->13 and13->21 at640x360,256 planes over1–6m,9x9 NCC, reciprocal depth,
uniqueness and angle filters exactly as declared in `dense-investigation.md`.
Export accepted points and the union with the existing four-camera cloud,
keeping old observations distinct from newly observed points. Report pair-only
and union coverage in the seen cameras, with head/hands/feet bins separately.
A projection of an old point is not a new correspondence.

Pair readiness uses the same dense minima:>=500 distinct5mm bins,>=50 accepted
reference pixels and>=10% person-mask coverage in each of21/13,>=20 distinct
bins per coarse body-region group. A numeric pass still requires credible body
surfaces in native depth/cloud/source inspection. No Gaussian fit follows a
gate failure. Never call this a complete body because point count alone passes.

Reuse the existing isolated CPU environment. One600-second external process
timeout; expected pair matching<30seconds,<2GiB RSS and<100MiB results. Overall
disk allowance<1GiB including the video and preparation; no weights/dependency
downloads or new services. No tuning sweep; one code repair for a software
fault only. An unchanged repeat is allowed for verification. Session service
cost isUS$0; existing machine/electricity are not separately billed here.

Deliverable: identified original and derived hashes, timing/coverage review,
fixed-setting native outputs, actual support/failures and next decision.
All imagery/models/points remain private in `working/shared-person/camera13/`.

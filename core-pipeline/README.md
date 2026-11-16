# Fixed-world reconstruction code

This directory migrates project-owned code and recipes from the gaussian-splatting
experiment. Its static30s baseline was executed historically, but the relocated
Revisit GPU environment has **not** been qualified. The public app does not launch
paid workers. Nothing here grants a cloud budget.

## What is available

- `runner/prepare_video.py`: standard-library frame extraction via ffmpeg, actual
  source PTS and byte hashes; called by the app.
- `runner/map_video.py`: CPU COLMAP mapping and observed static anchors; called
  by the app after explicit source review. Pinned preparation dependencies are
  included in the local Docker image.
- `runner/freeze.py`: allowlisted isolated handoff packaging, preserving all
  extracted observations and hashes; no credentials/weights/source video.
- `worker/`: migrated native geometry, appearance, depth-validity helpers,
  source patches, native tests/exporter, model download/preflight and adapters.
- `configs/`: historical static recipe, depth safeguards and public weight URLs /
  hashes. These are research settings, not a universal quality guarantee.
- `bootstrap.sh`: advanced setup draft that fetches the pinned public MoSca
  revision/submodules on the worker. This recipe needs fresh GPU qualification.

## Local path

The normal upload/source review/mapping/package steps are available in the app.
For native CLI development:

```bash
# Python3.11 preparation environment, not your system Python:
python3.11 -m venv working/preparation
working/preparation/bin/pip install -r core-pipeline/requirements-preparation.txt
export REVISIT_PREP_PYTHON="$PWD/working/preparation/bin/python"
# Start the app and upload/review a source before using these advanced commands.
working/preparation/bin/python core-pipeline/runner/map_video.py data/projects/PROJECT_ID
python3 core-pipeline/runner/freeze.py data/projects/PROJECT_ID working/worker-handoff
```

Do not rerun a completed/failed mapping into the same folder; use a new upload.
The app persists failed evidence. Numeric mapping success does not replace
subsequent priors/geometry review.

## Native worker boundary

The historical reference environment used a PyTorch2.1/CUDA11.8 Python3.10 stack
and L40S. This is an environment reference, not a current offer or paid allocation.
The pinned MoSca revision is `02404d2841b4e0dc2d9074860950bce5da579656`.
`bootstrap.sh` is intended for `/workspace/revisit` on a manually supervised
compatible worker, with the extracted handoff in place and explicit acceptance
of upstream research terms via `REVISIT_ACCEPT_RESEARCH_TERMS=1`.

Do not run the script on your local host: it installs OS/native dependencies.
It fetches upstream source/weights directly, records source/submodule versions,
checks model bytes/hashes and applies recorded project patches. It deliberately
does not copy the old private source cache. Some secondary pip dependencies remain
unpinned, so the GPU recipe is a migrated research draft, not a fully reproducible
production image. Terminate any manually managed worker yourself and verify it
in the provider console.

The supervised `worker/stage.py` wrapper requires a separately supplied
`runtime-bounds.json` absolute `deadlineEpoch`, reserves20minutes for retrieval,
checks immutable receipts and review gates, and records failed stage attempts.
It times out worker processes; it does not terminate billable resources. Never
claim independent cleanup from this wrapper.

The intended native progression is priors → reviewed priors → fixed-camera
background/depth → dense gates → reviewed geometry → static appearance → native
export. `worker.py` receives a stage and case ID; per-case review receipts are
required. It must execute only after native/model preflight and qualified external
lifecycle control. Export uses the static branch explicitly. Camera locks,
positive-depth handling and observed-anchor coverage remain mandatory.

The old cloud controllers with historical SSH paths/budgets were not migrated.
There is no public automatic paid controller or guaranteed remote deadline here.
Read [Runpod status and prerequisites](../docs/runbooks/operations/runpod.md).

## Licensing/provenance

Our adapters and documentation use MIT. Upstream MoSca author code, priors,
renderers and checkpoints have separate licenses/terms. In particular, historical
native renderer terms were research/evaluation restricted. Do not assume a
commercially unrestricted training stack from our code license. External code and
weights are not included in Git. See [licensing](../docs/licensing.md),
[third-party notices](../THIRD_PARTY_NOTICES.md) and the
[migration manifest](../docs/archive/migration-manifest.json).

# Revisit

**Experiments in explorable video memories.**

Revisit explores turning a real recording into a scene you can revisit: pause a
moment, move your viewpoint, then resume playback from there. It also preserves
the research record of what worked, what failed, and what remains uncertain.

**Status: runnable local preview.** Explore a real sample, import saved splats,
upload/prepare your video, recover static cameras on CPU and package a native
worker handoff. Paid reconstruction is disabled until independent lifecycle and
fresh GPU qualification pass. See [current state](docs/architecture/current-state.md).

## Run locally

```bash
git clone https://github.com/tathagatbanerjee/revisit.git
cd revisit
docker compose up --build -d
```

Open **http://localhost:4320**, then choose **Explore Houseplant** for a real,
attributed community capture. No cloud key or local CUDA GPU is required. The
3.5MiB sample downloads once and is checksum verified. It is not a model trained
by Revisit. Use the labelled synthetic sequence to test playback independently.

For native startup, prerequisites, video preparation, imports and checks, follow
the [local app runbook](docs/runbooks/operations/local-app.md).

## Repository layout

```text
app/                 local Node service, browser viewer and tests
core-pipeline/       CPU preparation, migrated native research worker and recipes
docs/                architecture, runbooks, provenance, verification and changelog
experiments/         historical project research/result records and evidence index
examples/            real sample provenance, download hash and attribution
schemas/             versioned artifact contracts
scripts/             import, documentation and publication-audit tools
working/             ignored temporary work; never published
data/                ignored uploads, model downloads, project state and results
```

This follows the original gaussian-splatting experiment's conventions as a
standalone Git checkout. Keep credentials and footage out of Git. Before pushing,
run `python3 scripts/audit-publication.py` and the [documented checks](docs/runbooks/operations/local-app.md).

## Start here

- [Documentation index](docs/README.md): architecture, runbooks, verification and change history.
- [Implementation plan](docs/implementation-plan.md): milestones, architecture,
  onboarding, acceptance tests and release criteria.
- [Experiments and outcomes](docs/experiments.md): executed trials, failed
  candidates, controls and methods that were researched but never fitted.
- [Licensing and assets](docs/licensing.md): MIT for project-owned material;
  separate terms for external code, models and footage.

## The experience we are building

1. Start the app locally and explore a supplied example without cloud credentials.
2. Choose a video, select a continuous interval and inspect local input checks.
3. Configure your own Runpod credentials and review a bounded compute job.
4. Follow preparation, geometry and fitting progress; inspect failures or open the
   downloaded reconstruction in the same app.
5. See that the owned cloud worker has been terminated.

The first supported reconstruction path will be a static scene from a moving
camera. Experimental dynamic replay will be labelled separately. Static models
cannot preserve the motion of people in a recording. Neither useful source-view
renders nor plausible unseen surfaces establish physical or novel-view accuracy.

## First release priorities

The first release completes one supported static reconstruction journey:

**Clone → start locally → explore a real sample → upload a suitable video →
reconstruct on Runpod → inspect locally → confirm worker terminated.**

- Include a cleared real reconstruction in the first five-minute experience;
  the synthetic sample remains a diagnostic fixture.
- Offer one supported recipe for a short, continuous video of mostly stationary
  surroundings, with a capture guide and suitable example input. Advanced depth,
  tracker and training settings stay out of the main flow.
- Explain failures with the stage, diagnostic and a concrete next action.
- Make worker status visible and qualify cleanup across cancellation, laptop
  disconnection and failed retrieval before inviting users to spend on jobs.
- Present experiments as question, outcome and lesson, with detailed evidence
  linked separately.
- Have a new user rehearse the public instructions from scratch and record
  actual setup times and every intervention before claiming quick setup.

Further reconstruction-quality research and new-video dynamic fitting follow
qualification of this complete static journey. Existing short dynamic samples
can still demonstrate independent time and viewpoint controls.

## Research context

Work to date includes frozen-frame inference, static multi-view reconstruction,
short MoSca replay, Brush/MoSca hybrids, calibrated multi-view refinement,
registration/fusion, depth/tracker comparisons and fixed-world camera correction.
Short dynamic results still ghost; fusion did not pass end-to-end quality gates.
A 30-second static pipeline completed on tested indoor and outdoor clips.

The research record contains 143 project-authored evidence documents and 103 published model records, including controls and
rejected diagnostics; that is not 103 successful independent reconstructions.
Historical model files, footage, SDKs, credentials and cloud execution state have
not been published here.

## License

Project-owned code and accompanying documentation are licensed under
[MIT](LICENSE). Third-party material retains its own terms; see
[licensing and assets](docs/licensing.md).

# Revisit

**Experiments in explorable video memories.**

Revisit explores turning a real recording into a scene you can revisit: pause a
moment, move your viewpoint, then resume playback from there. It also preserves
the research record of what worked, what failed, and what remains uncertain.

**Status: runnable local preview.** Explore a real sample, import saved splats,
upload/prepare your video, recover static cameras on CPU and package a native
worker handoff. Paid reconstruction is disabled until independent lifecycle and
fresh GPU qualification pass. See [current state](docs/architecture/current-state.md).

## See it first

**[Try Guildhall in your browser](https://revisit-guildhall.elephant-str-5431.chatgpt.site)** —
no installation, account or cloud key. Watch the original recording, enter our
reconstruction, freeze time and move your viewpoint.

[![Watch the 30-second Guildhall walkthrough](https://github.com/tathagatbanerjee/revisit/releases/download/guildhall-fixedworld-v1/revisit-tour-poster.jpg)](https://github.com/tathagatbanerjee/revisit/releases/download/guildhall-fixedworld-v1/revisit-30-second-tour.mp4)

[Watch the 30-second walkthrough](https://github.com/tathagatbanerjee/revisit/releases/download/guildhall-fixedworld-v1/revisit-30-second-tour.mp4)
(about 2.1 MB). Source footage followed by recorded full-density viewer states;
this illustrates the controls rather than real-time loading performance.
Footage and derived media: Acabashi / Wikimedia Commons, CC BY-SA 4.0.

## Run locally

```bash
git clone https://github.com/tathagatbanerjee/revisit.git
cd revisit
docker compose up --build -d
```

If Git is not installed, use GitHub’s **Code → Download ZIP**, extract it and open
a terminal in that folder, then run `docker compose up --build -d`.

Open **http://localhost:4320**. **Guildhall is the main example of our work:**

1. Watch the original interior walkaround.
2. Choose **Enter the Guildhall reconstruction** to move around the same event.
3. Pause, scrub the observed timeline, change your viewpoint and reset to a recorded camera.

No cloud key or local CUDA GPU is required. The first model state is about 31 MiB;
additional states download about 5 MiB each on demand from our public sample release, with SHA-256
verification and local caching. All 305 states and 475,357 Gaussians per state are
retained; the complete download is about 1.7 GB (about 11.5 GB expanded cache). This is our exploratory full-interior
fixed-world result: room structure is recognizable, but people ghost, the turn
blurs and unseen surfaces are incomplete. It is not validated novel-view geometry.

Houseplant remains under **Other samples and interaction checks**, alongside a
separately labelled synthetic interaction test. It is a community capture, not
our reconstruction.

Use **Check my setup** for graphics and storage guidance. The download panel shows
progress, cache usage and how much remains. **Download Guildhall for offline use**
fetches the complete sample explicitly; cancel/resume keeps completed files.
**Clear Guildhall cache** removes sample files while retaining local uploads.

| Path | Installation | Sample storage |
| --- | --- | --- |
| Hosted viewer | Open the link above; WebGL2 required | About 1.7 GB for all sample parts, plus the small viewer; browser storage may be evicted |
| Docker app | Docker Engine/Desktop + Compose v2 | Local data volume; up to about 11.5 GB for parts and expanded model files |
| Native app | Node 24+, ffmpeg/ffprobe, Python for preparation | Ignored `data/` folder or your `REVISIT_DATA` location |

The hosted viewer caches its interface and visited sample states for offline
reloads. Keep the tab open while downloading the full pack; after an interrupted
download, click Download again to resume. Your own video preparation runs locally.

An optional host check, if Node 24+ is already installed:

```bash
node scripts/setup-check.mjs
```

It checks Docker, Compose, disk space and the local port without showing keys.
Node is not required on the host for the Docker setup. If startup fails before
you can open the app, see [setup troubleshooting](docs/runbooks/operations/setup.md).

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
hosted/              reproducible public viewer build and hosting identity
working/             ignored temporary work; never published
data/                ignored uploads, model downloads, project state and results
```

This follows the original gaussian-splatting experiment's conventions as a
standalone Git checkout. Keep credentials and footage out of Git. Before pushing,
run `python3 scripts/audit-publication.py` and the [documented checks](docs/runbooks/operations/local-app.md).

## Start here

- [Fresh-install rehearsal](docs/testing/fresh-install.md): independent desktop checklist and automated platform coverage.
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
The Guildhall example is distributed separately as checksummed release assets;
large media stays outside Git. Other historical model files, footage, SDKs,
credentials and cloud execution state are not included.

## License

Project-owned code and accompanying documentation are licensed under
[MIT](LICENSE). Third-party material retains its own terms; see
[licensing and assets](docs/licensing.md).

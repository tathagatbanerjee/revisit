# Revisit

**Experiments in explorable video memories.**

Revisit explores turning a real recording into a scene you can revisit: pause a
moment, move your viewpoint, then resume playback from there. It also preserves
the research record of what worked, what failed, and what remains uncertain.

**Status: planning and research documentation.** The portable app and public
Runpod workflow are not implemented in this repository yet. There is no working
quick-start command here today. Earlier local prototypes demonstrated static
inspection and short dynamic replay, with substantial reconstruction defects.

## Start here

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

## Research context

Work to date includes frozen-frame inference, static multi-view reconstruction,
short MoSca replay, Brush/MoSca hybrids, calibrated multi-view refinement,
registration/fusion, depth/tracker comparisons and fixed-world camera correction.
Short dynamic results still ghost; fusion did not pass end-to-end quality gates.
A 30-second static pipeline completed on tested indoor and outdoor clips.

The research record contains 103 published model records, including controls and
rejected diagnostics; that is not 103 successful independent reconstructions.
Historical model files, footage, SDKs, credentials and cloud execution state have
not been published here.

## License

Project-owned code and accompanying documentation are licensed under
[MIT](LICENSE). Third-party material retains its own terms; see
[licensing and assets](docs/licensing.md).

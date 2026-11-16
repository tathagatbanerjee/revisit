> Historical project record, preserved as research evidence. Plans and commands
> below are not current Revisit operating instructions. Original source: `archive/2026-10-19/independent-mosca-fusion/registration/balanced-investigation.md`.
> Original SHA-256: `001236d0ac48f0d886ec4044c3fc4f3c9f5139072c8ae21333740e63d79f9414`. Private media/logs are not included.

# One scene-balanced registration diagnostic — 19 October 2026

The frozen background-only candidates improve room landmark alignment but expose
a large person discrepancy:20 old seen-person observations worsen from24.69px
to~220px; browser rendering shows two separated people. Preserve those outputs,
failed SIFT preparation, original union and all original gates.

Within the user's registration-only request, run ONE additional global7-parameter
transform estimate, without retraining, changing relative Gaussian geometry,
opacity or colours. This is a separately identified development diagnostic, not
a retuned version of the frozen background-only experiment. No cloud/paid work.

Use the28 background fitting identities and the existing20 person-region
correspondences selected by A's cached person mask and a conservative B torso
rectangle. Those20 were already inspected in the post-freeze diagnostic and are
now explicitly repurposed as development input; they are not fresh evaluation.
Reserve person native grid29 from this optimizer and retain six background
validation identities. Report reserved-person observations as previously seen
validation only; reuse/method selection precludes independent-accuracy claims.

Initialize from the old constrained alignment expressed B-native to A-native.
Optimize rotation, position and log-positive-scale using symmetric reprojection
in both fitted source cameras. Give room/person residual groups equal total
mean-square weight by fixed sqrt(Ntotal/(2*Ngroup)) factors. Use soft-L1 loss,
f_scale5px, max300 function evaluations, fixed broad scale bounds0.05–7.4.
No weight sweep, alternative initializations, topology edits or per-frame transforms.
Measure room/person errors separately and inspect the same viewpoints/times.
Do not assume a single transform can resolve internal shape/depth disagreement.

Estimate under30s CPU, limit120s and1GiB registration RAM, zero paid compute.
Export one all-points union, same40-state source-valid timeline, A unchanged;
append as a fifth clearly named comparison only after the original four-model
browser pass completes. Preserve the first publication record and save this
candidate's plan/report/publication separately. Keep all old models immutable.

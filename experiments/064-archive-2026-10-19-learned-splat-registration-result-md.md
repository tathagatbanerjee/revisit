> Historical project record, preserved as research evidence. Plans and commands
> below are not current Revisit operating instructions. Original source: `archive/2026-10-19/learned-splat-registration/result.md`.
> Original SHA-256: `2055d061a9c4392ad4714cc59199105f1186e420a432ffad5bdd2ad33e43464c`. Private media/logs are not included.

# Learned splat registration results — 19 October 2026

**Both real pretrained models ran. Neither produces an acceptable merge of this independent MoSca pair.**

| Method | Exact-copy control | Room error | Person error |
| --- | --- | --- | --- |
| GaussReg coarse | FAIL (rotation): 0.552deg, 0.247% scale | 308.52px / 2.116m-equivalent | 72.62px / 0.477m-equivalent |
| splatreg + BUFFER-X | PASS: 0.194deg, 0.140% scale | 163.60px / 1.580m-equivalent | 54.89px / 0.422m-equivalent |

The same predeclared gates apply to both: <=15px and <=.10m-equivalent for room and person. The six reserved room identities and20 person observations are already-seen development evidence, not fresh evaluation. No matching labels, calibration or previous transforms entered inference.

GaussReg selected3277 A/3648 B centers using its unmodified opacity/percentile filter; BUFFER-X’s splatreg wrapper received all65507/62380 centers. This compares the declared released methods, not identical preprocessing. No model training, full person segmentation, timing recovery, image-guided GaussReg fine stage or local deformation was tested.

The known-copy control isolates transformation recovery on compatible geometry. The independent pair adds reconstruction differences and viewpoint-dependent Gaussian distributions. BUFFER-X passing the control while failing the pair is evidence that more than transform bookkeeping is needed; it does not isolate the precise cause.

At http://localhost:4318 choose **Learned splat registration / diagnostics**, seek **1.5015s**, and compare original A, B with previous alignment, previous rejected union, GaussReg, and BUFFER-X. All use the same40-state timeline and fixed A/B/reserved-virtual cameras. The virtual camera is a development view, not fresh RGB.

The A5000 allocation failed with supply constraints and no allocated Pod. User-approved fallback used one A40 atUS$.59/hour for590.55s. Estimated computeUS$.0968 before disk/tax, not an invoice; no retained paid volume. Evidence retrieved and29 remote input/weight/result hashes verified before termination. An independent account query returned no Pods.

Source/checkpoint code pins, compatibility changes, initial failed setup/import/download attempts, input/receipt hashes and results are retained. Heavy logs/models/previews stay ignored. No merged model promoted; camera20 RGB remains sealed.

Verification completed:200 snapshots pass source/hash/count/covariance/clock checks;10 viewer tests, syntax and Compose checks pass. Actual five-run browser checks cover five clock positions, recorded/reserved views, orbit/reset and play/pause, with no uncaught exceptions or invalid manifests. Browser uses software rendering, not a hardware performance benchmark.

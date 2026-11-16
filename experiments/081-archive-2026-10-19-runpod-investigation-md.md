> Historical project record, preserved as research evidence. Plans and commands
> below are not current Revisit operating instructions. Original source: `archive/2026-10-19/runpod/investigation.md`.
> Original SHA-256: `10d5fbcfb9c84252ee29846e0dc491612d16d455d19b9356e43205b02a00a4b4`. Private media/logs are not included.

# A40 compatibility trial

17 October 2026. The user authorized Runpod setup and a compatibility trial,
following the commit and push of the multi-phone preparation branch.

## Selected scope

One A40 Secure Cloud Pod, one GPU, public TCP SSH, at least four vCPUs and 16 GB
host RAM, 80 GB container disk and no persistent or network volume. Use the
official Runpod PyTorch 2.1.0 / Python 3.10 / CUDA 11.8 development image,
Ubuntu 22.04. Docker Hub's amd64 digest was checked as
`sha256:2594f25beeef751aeebcc207ba4c45a382ba174655f01e15cbbfad0e2bdb5ef8`.
Request NVIDIA driver capabilities including graphics for hardware Vulkan.

Check actual GPU/VRAM, disk, CPU/RAM, CUDA matrix operations, and Vulkan device
selection. Reuse pinned Brush v0.3.0 and the existing reviewed 30-view precise-mask
Guildhall dataset for a 20-step masked smoke fit. For MoSca, use the retained
source revision and its CUDA extensions, then a small rasterization forward and
backward check; if the environment permits, inspect the retained dynamic
checkpoint at fixed and alternate times/views. No new multi-phone fit is in scope.
An extension import alone is not a full pipeline compatibility pass. Preserve
artifacts and logs under ignored `runpod/working/` without changing old results.

## Cost estimate and run limits

- Live price basis: Runpod GraphQL, A40 Secure, USD $0.59/hour, checked today.
  Recheck immediately before launch; reject rates above $0.59/hour.
- Expected session: 20–60 minutes including image pull, setup, checks and retrieval.
  Expected compute $0.20–$0.59.
- Maximum running time: two hours from launch attempt, including setup and waiting.
  Maximum compute $1.18. Running 80 GB disk at $0.10/GB/month adds about $0.023
  for two hours using a 720-hour month. Reserve the remainder of a **US$2 session
  allowance** for timing uncertainty and other charges before tax.
- One worker, no parallel Pods. Routine repairs may use remaining time; no
  automatic replacement or more expensive GPU fallback.
- A separate local watchdog, armed before creation, finds only the unique trial
  name and terminates its Pod at the deadline independently of the smoke-test
  process. It still depends on the local host and Runpod API being available;
  this is not a provider-enforced billing cap. Verify its heartbeat before work.
  Terminate earlier after results are retrieved. Do not retain paid storage.
- Stop if image startup/SSH cannot be established within 15 minutes, hardware
  Vulkan cannot be exposed, disk is insufficient, or remaining time cannot cover
  output retrieval. Record a compatibility failure without launching larger fits.

## Evidence and decision

Hash-check the transferred dataset and pinned Brush archive; inspect exported
Gaussians and GPU adapter logs. Record actual wall times and sampled resource use.
MoSca's pinned environment requires PyTorch 2.1/CUDA 11.8 and native extensions;
reuse the established repairs rather than invoking its destructive installer.
Neither Vulkan/CUDA detection nor another provider's earlier results establish
success on this Pod. Write actual outcomes in result/lessons/next steps, retrieve
evidence, terminate the Pod and verify no trial volume remains.

Sources: [Runpod GraphQL](https://docs.runpod.io/sdks/graphql/manage-pods),
[GraphQL schema](https://graphql-spec.runpod.io/),
[Pod pricing and storage](https://docs.runpod.io/pods/pricing),
previous hybrid execution (historical reference: `../pipeline/brush-mosca/execution.md`),
previous MoSca environment (historical reference: `../pipeline/mosca-dynamic/setup-worker.sh`).

## User steering during setup

The user subsequently requested keeping the Pod running if compatibility passes
and continuing pipeline testing. Keep the successful environment available
within the original two-hour cutoff rather than terminating immediately after
retrieval. The small end-to-end check may reproduce the 3,000-step precise-mask
Brush fit and replay the existing MoSca checkpoint. A fresh multi-phone dynamic
fit is outside this compatibility scope. The user was informed that the cutoff
remains active. No perpetual or unattended GPU retention is implied.

> Historical project record, preserved as research evidence. Plans and commands
> below are not current Revisit operating instructions. Original source: `archive/2026-10-19/splat-fusion-validation/06-time-alignment/initial-result.md`.
> Original SHA-256: `0a369d54b8ac609cc3a958062c7caff9fb1c022d2fccee9a0f1e468891eeada4`. Private media/logs are not included.

# Result

Exact cropped-source control recovers shift 6; independent-view motion selects shift 6 (true6), clock error 0.1001s, ambiguity margin 12.89%.

Status: **PASS exact-clock control; FAIL cross-view timing gate**. See numerical record (historical reference: `docs/result.json`).

Distance-quantile motion signatures are a deliberately small unsupervised baseline. A/B Gaussian pairs are sampled separately; no identities or true timestamps enter the similarity search. Short/periodic motion may remain ambiguous. Same-source success is not arbitrary phone synchronization.

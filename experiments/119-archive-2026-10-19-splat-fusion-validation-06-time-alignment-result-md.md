> Historical project record, preserved as research evidence. Plans and commands
> below are not current Revisit operating instructions. Original source: `archive/2026-10-19/splat-fusion-validation/06-time-alignment/result.md`.
> Original SHA-256: `3c9a3f2b6d7e756d499ac14bf4372b070c615715d4ab7743546f347cb2e04301`. Private media/logs are not included.

# Result

Exact cropped-source control recovers shift 6; independent-view motion selects shift 6 (true6), clock error 0.0000s, ambiguity margin 12.89%.

Status: **PASS exact-clock control; PASS limited cross-view gate**. See numerical record (historical reference: `docs/result.json`).

Distance-quantile motion signatures are a deliberately small unsupervised baseline. A/B Gaussian pairs are sampled separately; no identities or true timestamps enter the similarity search. Short/periodic motion may remain ambiguous. Same-source success is not arbitrary phone synchronization.

The initial uniform-sample conversion failed despite the correct motion shift. See preserved initial result (historical reference: `initial-result.md`) and timestamp correction (historical reference: `clock-conversion-correction.md`). Corrected mapping uses actual local PTS; it does not retune motion matching.

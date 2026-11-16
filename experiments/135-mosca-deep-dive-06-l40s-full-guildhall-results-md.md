> Historical project record, preserved as research evidence. Plans and commands
> below are not current Revisit operating instructions. Original source: `mosca-deep-dive/06-l40s-full-guildhall/results.md`.
> Original SHA-256: `48d57efa97fedb2da87a520a7e65e810f0e26529eda4392db4dc43c78d625151`. Private media/logs are not included.

# L40S full Guildhall results

Worker terminated and independently verified absent. Conservative cumulative estimateUS$3.1323 before tax; US$6.8677 remains of the acceptedUS$10 ceiling. All98 previous viewer records, including86 archived records, are unchanged.

| Case | Outcome | Source-fit median |
| --- | --- | ---: |
| guildhall-25s-large | FAILED_GEOMETRY_REVIEW | — |
| guildhall-outro | NOT_RUN | — |

Native render scores are fitted-source development evidence. Quality and GPU speed are not independently validated. Interior and outro remain separate shots; edited transition is source-only.

Stage outcomes, reviews, cost and closure (historical reference: `docs/execution-results.json`). Frozen inputs (historical reference: `docs/input-manifest.json`).

CPU postmortem: why the camera solve degraded (historical reference: `diagnosis.md`). In the replay,
2.87% of co-visible projections are behind camera and contribute99.9966% of
initial depth-ratio loss. The12s reference has no such pairs. This establishes
a concrete numerical failure mechanism; no corrected reconstruction was run.

> Historical project record, preserved as research evidence. Plans and commands
> below are not current Revisit operating instructions. Original source: `archive/2026-10-19/brush-mosca-multiphone/shared-person/targeted-feet-investigation.md`.
> Original SHA-256: `951f4bb9b553f798f542c9bc754046fdfd863dd9176476c28a0646299055be36`. Private media/logs are not included.

# One targeted21/02 pair — 19 October 2026

The native source-detail audit cannot establish reliable point identities on
both shoes or either hand: black uppers have little resolvable texture, sole
silhouettes change with view, fingers overlap and the watch face lacks a clearly
identical resolved corner in all relevant views. No manual3D landmark score can
honestly be produced from those uncertain labels. See landmark-audit.json.

Run exactly one new cached-MASt3R21/02 pair at state000. Its role is to test
whether a different already-seen pair supplies observed shoe correspondences;
no new camera, model, role swap, crop/threshold sweep or Gaussian fitting.
Reuse the pinned model/source and current512px crop/margin32 recipe, reciprocal
stride2, dot>=0.8, existing masks, finite confidence without a cutoff. Use saved
21/13 data and the unchanged three-view join/reprojection/3cm agreement rule.

Before inference, record conservative interior shoe polygons in21/13/02 from
unmarked native crops. Exclude soles' floor-contact silhouettes, ankles, trousers
and floor. These polygons label surface membership, **not homologous points or
an independent3D truth**. Reference21 image-left maps provisionally to02's near
shoe and image-right to its far shoe using visible leg continuity. Require a
track to land inside the same labelled shoe interior in all three cameras;
report swapped-label or ambiguous membership as failure, never reassign after
seeing the points. At least20 distinct5mm bins per shoe is only a regional
consistency signal, not a complete-person gate. Both hands remain unvalidated.
No initializer is exported, even if the shoe consistency signal passes.

Local existing Python3.12 CPU environment with cached weights; two CPU/BLAS
threads,5GiB child RSS limit,>=5.5GiB available RAM before launch. One attempt,
900s hard child deadline, no fallback; expected3–5minutes and under100MiB added
scratch. Parent kills only this child process group on limit. Maximum paid cost
US$0, no downloads, installs, cloud/GPU or unrelated process changes. Outputs
stay in ignored working/shared-person/mast3r/targeted-feet/. Hash the plan, source,
inputs, old frozen outputs and final evidence; inspect real source overlays,
including zero-support outcomes. Preserve every previous result unchanged.

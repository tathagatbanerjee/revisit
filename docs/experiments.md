# Experiments and outcomes

This is a retrospective of local experiments conducted mainly 14–29 October 2026,
reviewed 16 November 2026. These summaries report recorded outcomes; the original
models, media and execution trees are not included in this initial publication.
Portable per-attempt cards and reviewed supporting evidence will be migrated as
part of the [implementation plan](implementation-plan.md).

## What we were trying to do

The original idea was a braindance-inspired explorable video memory: pause event
time, move the viewpoint, then replay from there. Later uploads might enrich the
same event if world coordinates, clocks and geometry could be reconciled. Static
inspection and downloaded dynamic playback were stepping stones, not proof of
our own faithful event reconstruction. Observed recordings, reconstructed states
and guessed missing transitions must remain distinguishable.

## How to read and extend this history

Start each detailed experiment card with three short statements:

- **Question:** what were we trying to establish?
- **Outcome:** what actually happened, including failures and stopped stages?
- **Lesson:** what should someone do differently or investigate next?

Put inputs, configurations, metrics and logs in linked supporting detail. The
family table below is an initial overview; converting it into readable per-attempt
cards remains planned work. Keep the source-view versus novel-view distinction,
failed gates and unavailable evidence explicit. Further quality experiments wait
until the complete supported static onboarding journey is qualified.

## Results


This table summarizes experimental families and important subtrials. Entries
can overlap: exported controls and alternate renderers are not separate training
jobs. Dates are historical, principally 14–29 October 2026. Later results take
precedence over old README handoffs and stale catalog status strings.

| Experiment | What happened |
| --- | --- |
| SHARP frozen frames | Two real inferred sculpture/Guildhall moments loaded with nearby parallax; disocclusion artifacts remain. No aligned dynamic scene |
| Brush static sculpture | 60-view static fit completed, with wider navigation and source reset. Does not reconstruct moving events |
| Published dynamic boxes | 20 aligned snapshots over 3.8s demonstrate independent event time and camera. Someone else's reconstruction, not our training result |
| RiGS readiness audit | Runner/submodule/reuse gaps identified; no reconstruction fitting trial |
| First MoSca duck/Guildhall | Author control and short own-input fit completed. Coarse moving replay works; ghosted people and holes remain |
| Brush + MoSca H1 | Background/motion alignment and playback integrate. Masking leaves lower-scene holes; superiority unproven |
| H1 person-mask correction | Fixed cameras/motion and revised visitor masks restore coarse lower-scene appearance. Floor accuracy remains unproven |
| Runpod environment migration | Real A40 Brush/MoSca reconstruction and native dependency checks executed. Operational reproduction, not independent quality evidence |
| Seven-scene batch | Indoor person/group/exhibition, easy/medium/hard daylight phones and night flames tested. Five motion fits, five hybrids, four static backgrounds; exhibition/night motion failed. Four hybrids use lead-camera fallback |
| Whole-person layer | Selecting people from both MoSca components restores stationary body parts/bystanders in two fits. No new geometry or joint multi-camera motion |
| Background seed filtering / 12k fit | Filtering gives small gains; longer outdoor fit improves fitted-view background error 17.8%. People unchanged; shifted-view tearing persists |
| Calibrated two-camera refinement | Both synchronized images contribute gradients; second-view person error falls about 72%. Elevated held-out person error worsens about 7.5%, with fragmented anatomy |
| Image-only shared camera coordinates | Medium connects three phones/15 images; 3/3 later-frame localizations, but only 1/3 other-phone-only. Other phones disconnected |
| Supplied phone-pose priors | Coordinate convention verified; fixed/refined priors do not improve strict localization. Image-only map remains preferred |
| Assembled multi-view hybrid | Recovered indoor cameras drive fresh Brush background plus retained motion/shared refinement. Fresh-view whole-image error improves 52.8%, person worsens 48.0% |
| Shared-person sparse readiness | One synchronized instant across four calibrated cameras. Foreground input gate fails; no Gaussian fit |
| Dense person initialization | Reciprocal plane sweep gives 8,812 bins, but only two foot bins and 2.15% camera02 mask coverage. Readiness still fails |
| Camera13 foreground audit | More suitable pair slightly improves foot sampling but still fails readiness. Camera13 becomes seen, not fresh evaluation |
| MASt3R foreground correspondence | Actual learned matching runs locally. Frozen confidence acceptance fails; rejected matches motivate diagnostic follow-ups, not a promoted initializer |
| Third-view foreground check | Supports upper-body correspondences, but neither shoe obtains third-view support; coarse region boxes overstate anatomy |
| Landmark / targeted shoe check | Native detail cannot establish reliable shoe/hand identities; cached extra pair supplies three pair matches, no unambiguous three-view tracks. No initializer/export |
| Incremental scene enrichment | Add/refine 1,500 splats at one instant; new-view person RGB error improves 28.7%, old views 24–30%. Missing shoes/grain remain; not coherent motion fusion |
| Matched Guildhall full/hybrid comparison | Saved full-MoSca and precise-mask hybrids shown at matched camera/time/colour. No retraining or general hybrid superiority |
| Independent full-MoSca A/B | Fresh independent second recording and full-density union extend valid time coverage. Person duplicates; spatial gates fail |
| Background / balanced registration | Room-only reserved error improves 59.84→6.99px but bodies separate; balanced transform retains head/limb ghosts. No overall winner |
| Eight-stage fusion validation | Export/transform, injected change, clock and incremental fragment controls pass within scope; room gate limited pass. Real consolidation/refinement and actor geometry fail; real changed-room/third-upload unvalidated |
| Local fusion refinement variants | Appearance-only correction worsens MAE; bounded 512-position geometry trial gains only 0.362%, below 2% gate |
| Integrated two-upload prototype | Cached inputs, clock recovery, registration and export mechanically work. Person mismatch and tiny consolidation/refinement gains reject merge |
| Eight-stage edge-registration suite | Known-transform/ambiguity controls and edge evidence audited. Room edge scores improve while 3D consistency worsens; actor remains doubled. Person-only fit unrun without verified B layer |
| GaussReg / BUFFER-X learned registration | Actual weights run; BUFFER-X copy control passes and GaussReg narrowly misses rotation gate. Blind independent-pair room/person alignment fails for both |
| Brush registration proxies, stages01–08 | Transform and input/bridge stages pass; both Brush fits complete but lose 6–11dB and substantial coverage. Stages04–08 not run |
| Proxy seed-retention follow-up | More seeds improve all six views by 1.32–3.17dB and 7.9–19.6 coverage points; still fails original gates. No matching/transfer |
| Native observation-supported backgrounds | Stronger supported input selection and numerical controls pass. Classical matcher accepts only one pair; no real transform or merge |
| BUFFER-X on supported backgrounds | Known controls complete but scale errors 7.445%/9.966% fail 1% gate. Real A/B inference unrun |
| Fresh original-video A/B | Both short rooms fit usefully, with native source scores 33.88/34.44dB and ghosted people. Learned union still fails scale controls/doubles actor |
| First full Guildhall source | Shot-aware full-source test: 25.333s interior poor, 15.66dB median; separate static outro sharper, 38.85dB. Dissolve preserved source-only |
| Reproduction and depth/tracker screen | Fresh short control reproduced. Eight matrix arms: seven succeed, duck large-depth fails; plus a separate reproduction gives eight published exports from nine fits. Large depth helps Guildhall, hurts studio, fails duck |
| Duration ladder | Fresh 3s large, 6s small/large and 12s large exports all pass exploratory continuation reviews. 12s retains ghosting/smearing; not validated actor geometry |
| L40S full-interior attempt | Full priors complete, camera geometry fails manual review. No appearance or outro. CPU replay identifies behind-camera depth-loss dominance |
| Positive-depth correction | Overall median geometry improves 68.54→1.75px, but late/worst-frame failures remain. No appearance/export |
| Windowed camera tests | 0–18s passes at 1.21px median; independent 14–25.333s fails at 13.79px and worsens during BA. No stitched scene |
| Static-world camera anchoring | Two 52-keyframe controls and map alignment fail coverage; denser153-frame map plus152 localized cameras qualifies all305. Fixed-camera depth errors pass but final anchor count fails |
| Observed-anchor / depth arms | Same 4,000 observed tracks, frozen cameras: CPU unchanged-depth preflight and native scale-only/full arms pass. Full refinement median0.764px, worst1.060px; geometry only |
| Full-interior fixed-world appearance | 305 exported states, 475,357 points/state, 27.988dB median source fit. Original motion coverage fails87 frames; separately declared exploratory arm retains ghosting, no quality promotion |
| Fresh30s sculpture timing | 360 fixed cameras and332,079 static Gaussians; 30k appearance steps in14m13s. Full-depth propagation fails; separately declared scale-only arm passes. Source median19.60dB, exploratory; optional diagnostics interrupted |
| Standardized core static pipeline | First sculpture, repeat and Guild Hall detail finish cleanly; static30s baseline validated on two recordings. About25–30min required GPU stages; source medians19.648/19.630/27.828dB |
| Core preparation / motion failures | Museum source rejected for transition/wide-angle issues; confidence0.5 masks miss people, separate0.15 revision retained. Visitor geometry passes but motion fails116/120 required frames; no appearance/export/fallback |
| Core operational controls | Four network-only allocations rejected/closed; immutable-config, patch, stage-lock and retrieval checks exercised. Engineering evidence, not four additional scene fits |

## Researched or proposed, not completed fitting experiments

MipMap, Postshot, gsplat static, 4DGaussians, videosplat and CAT4D remained catalog
plans. RiGS was audited but not fitted. Conditional quality/duration programs,
60–120s scaling and unexecuted foreground ideas are proposals, not results.

## Overall conclusions

- Static inspection and short dynamic replay are useful interaction demonstrations.
- Ghosted people, missing feet/surfaces and disocclusion artifacts remain material.
- Whole-person partitioning repairs omissions without supplying missing geometry.
- A good room transform does not imply consistent independently fitted actors.
- Larger depth/tracker models are content dependent, not universal upgrades.
- Fixed-world observed cameras/anchors improved long-span geometry; motion remained
  weak. No general fusion or arbitrary-view quality claim passed.
- The most repeatable tested reconstruction path is the 30s static baseline.

Historical source-view PSNR is not independent novel-view accuracy. Native full-SH
and browser DC renders differ. The source interval, frame sampling, evaluation
exposure and failed gates belong with each future detailed card.

## Counts and evidence scope

The local review indexed 143 tracked research/result documents, 36 experiment
catalog entries and 103 published model records. Documents overlap; catalog entries
include plans; exports include controls and rejected diagnostics. None of these
numbers is a count of independent successful training jobs. All model paths
referenced by those 103 records existed locally during review, but the files are
not public assets. Transient setup attempts and ignored execution logs were not
exhaustively indexed. Camera20 stayed sealed.

The family-level table above is an initial summary, not a replacement for the
planned per-attempt evidence ledger. Source hashes, selected configuration details
and reviewed portable evidence should accompany that migration, with explicit
availability/provenance status and no inaccessible machine-path links.

## Supporting research records

The [historical evidence index](../experiments/README.md) provides the143
project-authored research/result records behind these summaries. The
[published-run inventory](archive/published-run-inventory.json) lists all103
historical exports without models/media; the [catalog](archive/experiment-catalog.json)
includes planned methods and original status strings. Later results supersede
stale catalog/handoff text.

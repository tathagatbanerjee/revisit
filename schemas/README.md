# Artifact contracts

`run.schema.json` describes a static or timestamped exported scene. Runtime
validation in `app/lib/contracts.mjs` adds safe relative paths, finite ordered
clocks and calibrated camera checks. This is an export contract, not a native
MoSca checkpoint loader.

```json
{
  "schemaVersion": 1,
  "id": "my-scene",
  "title": "My saved reconstruction",
  "representation": "sequence",
  "coordinateSystem": "y-up",
  "durationSeconds": 1.0,
  "frames": [
    {"time": 0.0, "model": "frames/000.splat"},
    {"time": 0.73, "model": "frames/001.splat"}
  ],
  "notes": "Actual source observation timestamps; states hold between observations."
}
```

Static runs specify `model` instead of frames. Each exported timestamp must be
retained. Do not silently resample irregular times or imply continuous motion.

Optional `inspectionCamera` / `inspectionViews` camera records use position[3],
unit quaternion[x,y,z,w], fx/fy/cx/cy, width/height, positive near/far planes and
positive targetDistance. Recorded poses are reset targets; seeking does not move
the selected camera. Native exporter conventions need their actual coordinate
conversion; a PLY path alone does not establish a shared world.

The local importer computes `fileHashes` on every copied model. A source manifest
with hashes is verified before importing; importing does not clear asset rights.

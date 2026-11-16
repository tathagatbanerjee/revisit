# Third-party notices

Revisit's own code/docs are MIT. Dependencies and samples are separately licensed.
Packages are installed from pinned manifests; downloaded assets stay outside Git.

| Component | Role | Terms/source |
| --- | --- | --- |
| Three.js0.180.0 | Scene/camera/navigation | MIT; https://github.com/mrdoob/three |
| Spark2.3.1 | Gaussian rendering | MIT; https://github.com/sparkjsdev/spark |
| fflate0.8.3 | Spark transitive package | MIT; https://github.com/101arrowz/fflate |
| Houseplant, Marcel Padilla | Real phone-captured sample | CC BY4.0, explicit photographic capture/reconstruction scope at pinned source |
| ffmpeg | Local decoding/extraction | System-distribution build and its own licensing; not relicensed by Revisit |
| COLMAP/pycolmap4.2.1 | CPU camera mapping | BSD3-Clause and dependencies; https://github.com/colmap/colmap |
| NumPy/OpenCV/Pillow | Optional CPU preparation | Their respective upstream licenses, retained in installed packages |

## Main research example: Guildhall

Guildhall interior walkaround by **Acabashi / Wikimedia Commons**, source:
[original recording](https://commons.wikimedia.org/wiki/File:Guildhall_City_of_London_England_interior_walkaround_video.webm),
[CC BY-SA 4.0](https://creativecommons.org/licenses/by-sa/4.0/).
The source excerpt is trimmed from original 50–75.433 seconds, resized to 1280×720
and has no audio. The interactive reconstruction derives from the interior
observations through original 75.333 seconds using the fixed-world MoSca experiment;
all 305 exported states retain all 475,357 Gaussians (viewer displays DC colour).
The footage and derived reconstruction are distributed under CC BY-SA 4.0,
separately from Revisit's MIT app code. Download hashes and saved timestamps are
in `examples/guildhall.json`; large assets live in the `guildhall-fixedworld-v1`
GitHub release and cache locally outside Git. No pretrained weights, training
checkpoints or native renderer code are included in this sample.

## Real example attribution

“Houseplant” photographic capture and reconstruction by Marcel Padilla, from
[marcelpadilla/splats](https://github.com/marcelpadilla/splats/tree/c3e5ec0a8ddb3ab26f28a067a29d272fe1a23411/data/plant),
licensed [CC BY4.0](https://creativecommons.org/licenses/by/4.0/). The `.splat`
file is unmodified. Revisit displays it using its viewer and an axis convention
conversion; it is not a Revisit-trained result.

Pinned [asset/license scope](https://github.com/marcelpadilla/splats/blob/c3e5ec0a8ddb3ab26f28a067a29d272fe1a23411/LICENSE)
and [metadata](https://github.com/marcelpadilla/splats/blob/c3e5ec0a8ddb3ab26f28a067a29d272fe1a23411/data/plant/meta.json).
The descriptor in `examples/houseplant.json` records URL, size, hash and credit;
the app displays attribution and downloads the unmodified bytes on demand.
The sample is SH0, uses nonmetric reconstruction units and is not ground truth.

## Advanced native research backend

The migrated adapter/patch files are project-owned. MoSca author source and its
priors/native renderers are fetched separately by an opt-in research setup draft.
MoSca's own MIT grant does not blanket-license its upstream priors/renderers;
native rasterizer terms and weights require separate review. No upstream source,
SDK or pretrained weight has been vendored in this repo. The separately released
Guildhall reconstruction is an output asset, not a redistribution of that stack.
Retain all notices when using or distributing any advanced worker image, and do
not advertise the complete stack as commercially unrestricted until that review
is complete.

Installed JavaScript package license texts are also preserved below.

## three installed license

```text
The MIT License

Copyright © 2010-2025 three.js authors

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in
all copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
THE SOFTWARE.
```

## @sparkjsdev/spark installed license

```text
The MIT License

Copyright © 2025 WORLD LABS TECHNOLOGIES, INC.

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in
all copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
THE SOFTWARE.
```

## fflate installed license

```text
MIT License

Copyright (c) 2026 Arjun Barrett

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
```

## MoSca author license (adapted recipe provenance)

```text
MIT License

Copyright (c) 2024 Jiahui Lei

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
```

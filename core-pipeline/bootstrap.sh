#!/bin/bash
# Advanced research worker setup. Not called by the public preview app.
set -euo pipefail
if [[ "${REVISIT_ACCEPT_RESEARCH_TERMS:-}" != "1" ]]; then
  echo 'Read core-pipeline/README.md and upstream terms first; explicit research-terms acceptance is required.' >&2
  exit 2
fi
cd /workspace/revisit
export DEBIAN_FRONTEND=noninteractive CUDA_HOME=/usr/local/cuda-11.8
export PATH="$CUDA_HOME/bin:$PATH" MAX_JOBS=2 TORCH_CUDA_ARCH_LIST=8.9
export XDG_RUNTIME_DIR=/tmp OMP_NUM_THREADS=4 OPENBLAS_NUM_THREADS=4 MPLBACKEND=Agg GS_BACKEND=native_add3
mkdir -p output results
python - <<'PY'
import hashlib,json
from pathlib import Path
for name,digest in json.loads(Path('payload-manifest.json').read_text()).items():
    p=Path(name)
    assert not p.is_absolute() and '..' not in p.parts and p.is_file()
    assert hashlib.sha256(p.read_bytes()).hexdigest()==digest,name
PY
apt-get -o DPkg::Lock::Timeout=300 update
apt-get -o DPkg::Lock::Timeout=300 install -y git libegl1 libgl1 libglib2.0-0 ffmpeg ninja-build build-essential
# Public source at an explicit revision, including its pinned submodules.
git clone --no-checkout https://github.com/JiahuiLei/MoSca.git mosca
git -C mosca checkout --detach 02404d2841b4e0dc2d9074860950bce5da579656
git -C mosca submodule update --init --recursive
git -C mosca submodule status --recursive > output/source-submodules.txt
python download_worker.py
python -m venv --system-site-packages mosca-env
PY="$PWD/mosca-env/bin/python"
"$PY" -m pip install 'numpy==1.26.4' 'setuptools==69.5.1' wheel ninja
"$PY" -m pip install pytorch3d -f https://dl.fbaipublicfiles.com/pytorch3d/packaging/wheels/py310_cu118_pyt210/download.html
"$PY" -m pip install torch-scatter torch-cluster -f https://data.pyg.org/whl/torch-2.1.0+cu118.html
"$PY" -m pip install torch-geometric==2.4.0 opencv-python==4.10.0.84 pillow==9.5.0 scipy==1.10.1 matplotlib==3.7.5 imageio==2.34.1 imageio-ffmpeg mediapy==1.2.2 einops einshape tqdm kornia==0.7.3 omegaconf open3d==0.18.0 transforms3d tensorboardX rich scikit-learn timm==0.9.2 huggingface-hub==0.20.3 iopath fvcore easydict packaging plyfile==1.0.3 psutil absl-py scikit-image==0.22.0 yapf==0.40.1 lpips==0.1.4 pandas==2.1.4 evo==1.29.0
"$PY" -m pip install --no-build-isolation mmcv==1.7.2
for extension in simple-knn diff-gaussian-rasterization-alphadep diff-gaussian-rasterization-alphadep-add3; do
  "$PY" -m pip install --no-build-isolation "$PWD/mosca/lib_render/$extension"
done
"$PY" patch_worker.py
"$PY" patch_depth_validity.py
"$PY" cuda_depth_smoke.py > output/depth-validity-smoke.json
"$PY" gpu-smoke.py > output/gpu-smoke.json
"$PY" preflight_models.py > output/model-preflight.log 2>&1
"$PY" variant_queries.py install mosca
"$PY" -m pip freeze > output/pip-freeze.txt
touch output/preflight-complete

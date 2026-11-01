#!/usr/bin/env bash
# Set up a fresh Debian/Ubuntu machine (or cloud container) to compute and render every video, silently.
#
#     bash tools/setup_linux.sh          # system packages (needs root or sudo), then .venv with the locked versions
#     source .venv/bin/activate
#     EXPLAINER_TTS=silent python tools/smoke.py quant10 --lang en
#
# Safe to rerun: apt and uv skip what is already installed.  Narration (Qwen3-TTS) is a separate setup (README).
set -euo pipefail
cd "$(dirname "$0")/.."

SUDO=""
if [ "$(id -u)" -ne 0 ]; then SUDO="sudo"; fi
$SUDO apt-get update -qq
DEBIAN_FRONTEND=noninteractive $SUDO apt-get install -y -qq ffmpeg libcairo2-dev libpango1.0-dev pkg-config \
    espeak-ng texlive-latex-extra texlive-fonts-recommended texlive-science texlive-xetex texlive-lang-chinese \
    dvisvgm fonts-dejavu fonts-liberation fonts-noto-cjk

command -v uv >/dev/null || { curl -LsSf https://astral.sh/uv/install.sh | sh; export PATH="$HOME/.local/bin:$PATH"; }
[ -x .venv/bin/python ] || uv venv --python 3.12 .venv
uv pip install --python .venv/bin/python --index-url https://download.pytorch.org/whl/cpu torch
uv pip install --python .venv/bin/python -r requirements-lock.txt
uv pip install --python .venv/bin/python -e . --no-deps
echo "ready: source .venv/bin/activate"

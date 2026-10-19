#!/bin/bash
# Toolchain for a Colab render box (tools/colab_factory.py): TeX (with xeCJK and the Fandol fonts), Manim's system
# libraries, Manim itself and the Qwen3 speech stack, into the VM's system Python. About 10 minutes on a fresh VM.
set -ex
export DEBIAN_FRONTEND=noninteractive
apt-get update -qq
apt-get install -y -qq texlive-xetex texlive-latex-extra texlive-fonts-recommended texlive-science \
  texlive-lang-chinese texlive-lang-cjk dvisvgm libpango1.0-dev libcairo2-dev pkg-config ffmpeg fonts-dejavu fonts-noto-cjk
pip install -q "manim==0.22.0" numba soundfile pypinyin
# qwen-tts and qwen-asr pin different transformers versions: one after the other (the later one wins, and both run)
pip install -q qwen-tts
pip install -q qwen-asr
touch /content/.toolchain_ok

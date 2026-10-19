# Explainer Videos

Math, physics, ML and markets explainers in the style of 3Blue1Brown, built entirely in code with
[Manim Community](https://www.manim.community/) and narrated by a local neural voice. Only the code is stored here;
every video builds from source. Each video lives in `videos/<series>/<name>/` with its own README (outline and sources); the series are
`ai`, `analysis`, `physics`, `math`, `ml` and `markets`. Videos are always addressed by name (`tools/build.py quantum`).

| Video | Length | Build |
|---|---|---|
| The Navier–Stokes Equations, Derived and Visualized | 28 min | `python -m videos.physics.navier_stokes.simulate && python tools/build.py navier_stokes` |
| How Large Language Models Work | 37 min | `python -m videos.ml.llm.analyze && python tools/build.py llm` |
| Opposing Forces: Earnings vs. the Cost of Money | 37 min | `python tools/build.py opposing_forces` |
| The Riemann Hypothesis, Visualized | 39 min | `python -m videos.math.riemann.compute && python tools/build.py riemann` |
| Inside the Open Frontier (MiMo, GLM, Kimi) | 33 min | `python tools/build.py open_models` |
| How Frontier AI Models Are Trained | 60 min | `python -m videos.ml.frontier.compute && python tools/build.py frontier` |
| Reinforcement Learning for LLMs, Derived | 46 min | `python -m videos.ml.rl.compute && python tools/build.py rl` |
| Stochastic Calculus, Visualized | 49 min | `python -m videos.math.stochastic.compute && python tools/build.py stochastic` |
| Building a Real-Time Trading System | 43 min | `python tools/build.py trading` |
| Quantum Mechanics, Visualized | 64 min | `python -m videos.physics.quantum.compute && python tools/build.py quantum` |
| General Relativity, Derived | 69 min | `python -m videos.physics.relativity.compute && python tools/build.py relativity` |
| General Relativity, Part 2 | 56 min | `python -m videos.physics.relativity2.compute && python tools/build.py relativity2` |
| Quantum Mechanics, Part 2 | 57 min | `python -m videos.physics.quantum2.compute && python tools/build.py quantum2` |
| Analysis, Built (10 parts: real, complex and functional analysis; English and Chinese) | 5 h 20 min | `python -m videos.analysis.analysisN.compute && python tools/build.py analysisN` |
| AI, Built, Part 1: The Guessing Game (of 31: [the plan](videos/ai/README.md); English and Chinese) | ~45 min | `python -m videos.ai.ai1.compute && python tools/build.py ai1` |

## Layout

```
explainer/   shared toolkit: style, TTS, voiceover, language tables, paths (explainer/paths.py finds a video by name)
videos/      one package per video, grouped by series: ai/ analysis/ physics/ math/ ml/ markets/
tools/       build, narration, QA, publishing scripts (run from the repo root)
docs/        CREDITS.md
renders/ published/ media/ .cache/   generated, git-ignored
```

## Setup

```bash
# macOS
brew install ffmpeg pango pkg-config espeak-ng mactex
# Linux (Debian/Ubuntu)
sudo apt install ffmpeg libcairo2-dev libpango1.0-dev pkg-config espeak-ng texlive-latex-extra texlive-fonts-recommended \
    texlive-science texlive-xetex texlive-lang-chinese dvisvgm fonts-dejavu fonts-liberation fonts-noto-cjk

uv venv --python 3.12 .venv && source .venv/bin/activate
uv pip install --index-url https://download.pytorch.org/whl/cpu torch && uv pip install -e .
```

The same code renders on both: Chinese TeX uses xelatex with Fandol (part of TeX Live everywhere), and Chinese plain
text uses Songti SC on macOS, Noto Serif CJK SC (or AR PL UMing) on Linux (`explainer/zh_text.py: cjk_font`).

## Build

```bash
python tools/build.py <video> -q l                 # 480p preview
python tools/build.py <video>                      # 1080p30 -> renders/<video>.mp4, .srt, chapters
python tools/build.py <video> -q k --fps 60        # 2160p60
```

Narration and animations are cached, so rebuilds redo only what changed. `EXPLAINER_TTS=silent` skips speech.
QA: `tools/contact_sheet.py` (layout), `tools/dead_air.py` (empty screen under narration).

## Analysis, Built and AI, Built in English and Chinese

```bash
uv venv --python 3.12 .venv-tts && uv pip install --python .venv-tts/bin/python mlx-audio soundfile pypinyin
.venv-tts/bin/python tools/tts_server.py --voice qwen3-calm-a      # Qwen3-TTS on Apple Silicon (MLX)
# Linux: the same model and voice in PyTorch (CUDA, or CPU at several times slower than real time)
#   uv pip install --python .venv-tts/bin/python torch qwen-tts soundfile pypinyin
#   uv pip install --python .venv-tts/bin/python qwen-asr     # after qwen-tts: they pin different transformers
#   .venv-tts/bin/python tools/tts_server.py --voice qwen3-calm-a --engine torch
# or narrate whole videos on a Colab GPU: tools/colab_narrate.py
export EXPLAINER_TTS=server EXPLAINER_VOICE=qwen3-calm-a
python tools/narrate.py analysis1 --lang en                        # then --lang zh
python tools/build.py analysis1 -q k --fps 60 --crf 16 [--lang zh]
python tools/package_uploads.py                                    # YouTube / Bilibili kits in renders/upload/
```

Chinese narration lives in `videos/analysis/analysisN/narration_zh.json`, on-screen text in `videos/analysis/analysis_text_zh.json`
(`tools/collect_text.py --check`); terms in `videos/analysis/ANALYSIS_ZH_GUIDE.md`. *AI, Built* works the same way (`aiN`,
`videos/ai/ai_text_zh.json`, `videos/ai/AI_ZH_GUIDE.md`; `tools/package_uploads.py --series ai`).

## Credits

See [`docs/CREDITS.md`](docs/CREDITS.md).

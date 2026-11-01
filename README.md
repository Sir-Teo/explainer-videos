# Explainer Videos

Math, physics, ML and markets explainers in the style of 3Blue1Brown, built entirely in code with
[Manim Community](https://www.manim.community/) and narrated by a local neural voice. Only the code is stored here;
every video builds from source. Each video lives in `videos/<series>/<name>/` with its own README (outline and sources); the series are
`ai`, `analysis`, `physics`, `math`, `ml` and `markets`, with `quant` planned. Videos are always addressed by name (`tools/build.py quantum`).

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
| AI, Built (31 parts: [the plan](videos/ai/README.md); English and Chinese) | 30–60 min each | `python tools/make.py ai1` … `ai31`, or `--series ai` |
| Quant, Built (30 parts, planned: [the plan](videos/quant/README.md), [syllabus](videos/quant/SYLLABUS.md), [reading](videos/quant/READING.md)) | 30–60 min each | not yet written |

## Layout

```
explainer/   shared toolkit: style, TTS, voiceover, language tables, paths (explainer/paths.py finds a video by name)
videos/      one package per video, grouped by series: ai/ analysis/ physics/ math/ ml/ markets/ quant/
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
# or exactly the versions the series was built with (on Linux, CPU torch first as above, then):
#   uv pip install -r requirements-lock.txt && uv pip install -e . --no-deps
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
# Linux: the same model and voice in PyTorch. On a CUDA GPU it is quick; on a CPU it works (16 GB of RAM is
# enough) but runs 10-30x slower than real time, so narrate whole videos on a GPU or Colab instead.
#   uv pip install --python .venv-tts/bin/python torch qwen-tts soundfile pypinyin
#   uv pip install --python .venv-tts/bin/python qwen-asr     # after qwen-tts: they pin different transformers
#   CPU-only torch: install torch and torchaudio from https://download.pytorch.org/whl/cpu (matching builds)
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

## Rebuilding everything on your own computer

Everything regenerates from this repo: the numbers (`.cache/`), the narration and the films. One command per video
runs the whole chain, and every step resumes where it stopped:

```bash
.venv-tts/bin/python tools/tts_server.py --voice qwen3-calm-a      # narration server, in its own terminal (above)
python tools/make.py ai26                     # Part 26: its computations, then the narrated cut in English and Chinese
python tools/make.py ai26 -q k --fps 60 --crf 16                   # 4K60 upload masters
python tools/make.py --series ai              # all of AI, Built, in order (each part computes what it builds on)
python tools/make.py ai27 --silent -q l --lang en                  # a quick silent preview
```

* **Resumable.** Interrupted (laptop closed, crash, power)? Run the same command again. Each computed result is saved
  to `.cache/<video>/` the moment it is finished, and only then; the long jobs checkpoint as they go (AlphaZero in
  Part 26 after every generation, the series' language models every 100 steps); narration and animation are cached
  by content, so a rebuild redoes only what's missing.
* **Reproducible.** Every computation is seeded, and `requirements-lock.txt` pins the versions the series was built
  with (Python 3.12). The same machine gives the same numbers. Another machine's floating point can move the last
  digits of a result; the narration is written over the data, in English and in Chinese (each part's
  `zh_lines.py` translates computed lines as templates), so it says what your run measured. Before each Chinese
  build, `tools/zh_lines.py <video> --verify` checks that every line will translate.
* **Dependencies between parts** are found from the code: Part 30 reuses Part 13's transformer, Parts 14, 27 and 31
  the novels model (`python -m explainer.ai.novels`), so `make.py` computes those first.
* **Time.** Most parts compute in under an hour on a laptop. The long ones: Part 26's AlphaZero (about 5 hours on 4
  CPU cores; `python -m videos.ai.ai26.alphazero` trains it alone), the novels model (about an hour), Part 27's
  post-training experiments (about 2 hours). Rendering a 50-minute part at 1080p takes a few hours; `-q l` previews
  take minutes per chapter (`tools/qa_scene.py <video> <Scene>` renders one chapter with a contact sheet).
* Logs go to `renders/make/`, films to `renders/`.

## Credits

See [`docs/CREDITS.md`](docs/CREDITS.md).

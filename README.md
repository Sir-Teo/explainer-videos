# Explainer Videos

Math, physics, ML and markets explainers in the style of 3Blue1Brown, built entirely in code with
[Manim Community](https://www.manim.community/) and narrated by a local neural voice. Only the code is stored here;
every video builds from source. Each `videos/<name>/README.md` has the outline and sources.

| Video | Length | Build |
|---|---|---|
| The Navier–Stokes Equations, Derived and Visualized | 28 min | `python -m videos.navier_stokes.simulate && python tools/build.py navier_stokes` |
| How Large Language Models Work | 37 min | `python -m videos.llm.analyze && python tools/build.py llm` |
| Opposing Forces: Earnings vs. the Cost of Money | 37 min | `python tools/build.py opposing_forces` |
| The Riemann Hypothesis, Visualized | 39 min | `python -m videos.riemann.compute && python tools/build.py riemann` |
| Inside the Open Frontier (MiMo, GLM, Kimi) | 33 min | `python tools/build.py open_models` |
| How Frontier AI Models Are Trained | 60 min | `python -m videos.frontier.compute && python tools/build.py frontier` |
| Reinforcement Learning for LLMs, Derived | 46 min | `python -m videos.rl.compute && python tools/build.py rl` |
| Stochastic Calculus, Visualized | 49 min | `python -m videos.stochastic.compute && python tools/build.py stochastic` |
| Building a Real-Time Trading System | 43 min | `python tools/build.py trading` |
| Quantum Mechanics, Visualized | 64 min | `python -m videos.quantum.compute && python tools/build.py quantum` |
| General Relativity, Derived | 69 min | `python -m videos.relativity.compute && python tools/build.py relativity` |
| General Relativity, Part 2 | 56 min | `python -m videos.relativity2.compute && python tools/build.py relativity2` |
| Quantum Mechanics, Part 2 | 57 min | `python -m videos.quantum2.compute && python tools/build.py quantum2` |
| Analysis, Built (10 parts: real, complex and functional analysis; English and Chinese) | 5 h 20 min | `python -m videos.analysisN.compute && python tools/build.py analysisN` |

## Setup

```bash
brew install ffmpeg pango pkg-config espeak-ng mactex      # or the apt equivalents
uv venv --python 3.12 .venv && source .venv/bin/activate
uv pip install --index-url https://download.pytorch.org/whl/cpu torch && uv pip install -e .
```

## Build

```bash
python tools/build.py <video> -q l                 # 480p preview
python tools/build.py <video>                      # 1080p30 -> renders/<video>.mp4, .srt, chapters
python tools/build.py <video> -q k --fps 60        # 2160p60
```

Narration and animations are cached, so rebuilds redo only what changed. `EXPLAINER_TTS=silent` skips speech.
QA: `tools/contact_sheet.py` (layout), `tools/dead_air.py` (empty screen under narration).

## Analysis, Built in English and Chinese

```bash
uv venv --python 3.12 .venv-tts && uv pip install --python .venv-tts/bin/python mlx-audio soundfile pypinyin
.venv-tts/bin/python tools/tts_server.py --voice qwen3-calm-a      # Qwen3-TTS on Apple Silicon
export EXPLAINER_TTS=server EXPLAINER_VOICE=qwen3-calm-a
python tools/narrate.py analysis1 --lang en                        # then --lang zh
python tools/build.py analysis1 -q k --fps 60 --crf 16 [--lang zh]
python tools/package_uploads.py                                    # YouTube / Bilibili kits in renders/upload/
```

Chinese narration lives in `videos/analysisN/narration_zh.json`, on-screen text in `videos/analysis_text_zh.json`
(`tools/collect_text.py --check`); terms in `videos/ANALYSIS_ZH_GUIDE.md`.

## Credits

* Animation engine: [Manim Community Edition](https://www.manim.community/) (MIT).
* Voices: [Kokoro-82M](https://huggingface.co/hexgrad/Kokoro-82M) (Apache-2.0), `af_heart`; *Analysis, Built*: [Qwen3-TTS](https://huggingface.co/Qwen) 1.7B (Apache-2.0), the English voice cloned from `af_heart`, the Chinese from Qwen3's Serena.
* Model under the microscope: [GPT-2](https://huggingface.co/openai-community/gpt2) (OpenAI, modified MIT license), via Hugging Face `transformers`.
* Training text for the tiny model: Tiny Shakespeare from [`karpathy/char-rnn`](https://github.com/karpathy/char-rnn) (Shakespeare, public domain).
* Market note explained: Jurrien Timmer, [*Opposing Forces*](https://www.linkedin.com/pulse/opposing-forces-week-10526-jurrien-timmer-anaac/) (Fidelity Investments, Oct 5, 2026). The video paraphrases and attributes its arguments; it is not affiliated with Fidelity.
* Market and macro data: [FRED](https://fred.stlouisfed.org/) (Federal Reserve Bank of St. Louis), the [New York Fed](https://www.newyorkfed.org/research/data_indicators/term-premia-tabs) (ACM term premium), [Robert Shiller](https://shillerdata.com/), [U.S. Treasury Fiscal Data](https://fiscaldata.treasury.gov/), [FactSet Earnings Insight](https://insight.factset.com/), and Nasdaq daily prices.
* Frontier-training video: web data from [Common Crawl](https://commoncrawl.org/) (CC-MAIN-2026-39) filtered with Hugging Face's [`datatrove`](https://github.com/huggingface/datatrove) (Apache-2.0); pretraining text from [FineWeb-Edu](https://huggingface.co/datasets/HuggingFaceFW/fineweb-edu) (ODC-By) via `karpathy/fineweb-edu-100b-shuffle`; quality scores from [`HuggingFaceFW/fineweb-edu-classifier`](https://huggingface.co/HuggingFaceFW/fineweb-edu-classifier); chat template and outputs from [Qwen3-0.6B](https://huggingface.co/Qwen/Qwen3-0.6B) and its base model (Apache-2.0); training-compute data from [Epoch AI](https://epoch.ai/data/ai-models) (CC BY 4.0). Muon after [`KellerJordan/Muon`](https://github.com/KellerJordan/Muon); the end-to-end framing owes much to [`karpathy/nanochat`](https://github.com/karpathy/nanochat) and Hugging Face's training playbooks.
* Mathematics explained: OpenAI, [`github.com/openai/math`](https://github.com/openai/math), family 003, *The quasi-Riemann hypothesis* (Sept 30 – Oct 5, 2026). The video explains and attributes the manuscripts; it is not affiliated with OpenAI. Numerics: [mpmath](https://mpmath.org/) (BSD) and NumPy.
* Models explained: Xiaomi [MiMo-V2.6-Pro](https://huggingface.co/XiaomiMiMo/MiMo-V2.6-Pro-RL), Z.ai [GLM-5.3](https://huggingface.co/zai-org/GLM-5.3), Moonshot AI [Kimi K3](https://huggingface.co/moonshotai/Kimi-K3), as ranked by the [Artificial Analysis Intelligence Index](https://artificialanalysis.ai/models/open-source) (v4.3.2, Oct 8, 2026). Configs and weights are read from Hugging Face; the video explains and attributes the labs' technical reports and is not affiliated with any of them.
* Reinforcement-learning video: sampler/learner mismatch measured on [Qwen3-0.6B](https://huggingface.co/Qwen/Qwen3-0.6B) (Apache-2.0); defaults compared across the open RL frameworks [verl](https://github.com/volcengine/verl), [TRL](https://github.com/huggingface/trl), [OpenRLHF](https://github.com/OpenRLHF/OpenRLHF), [open-instruct](https://github.com/allenai/open-instruct), [nanochat](https://github.com/karpathy/nanochat), [prime-rl](https://github.com/PrimeIntellect-ai/prime-rl), [slime](https://github.com/THUDM/slime), [AReaL](https://github.com/inclusionAI/AReaL), [SkyRL](https://github.com/NovaSky-AI/SkyRL), [ROLL](https://github.com/alibaba/ROLL) and [ART](https://github.com/OpenPipe/ART). GRPO's arcsine objective after Davis & Recht (2025), the KL estimators after John Schulman's note, the entropy-covariance identity after Cui et al. (2025); full list in [`videos/rl/README.md`](videos/rl/README.md).
* Trading-system video: market data from Nasdaq's public TotalView-ITCH 5.0 sample files (December 10, 2025); facts from Jane Street's tech talks and the [Signals and Threads](https://signalsandthreads.com/) podcast, HRT's [tech blog](https://www.hudsonrivertrading.com/hrtbeat/), Budish, Cramton & Shim (2015), Aquilina, Budish & O'Neill (2022), STAC, and the SEC's 2013 order against Knight Capital; map data from Natural Earth and OpenStreetMap (ODbL). The video explains public information and is not affiliated with any firm named.
* Quantum-mechanics video: no external data; every wave is computed from the Schrödinger equation. Physical constants are CODATA 2022 (via `scipy.constants`). Historical claims were checked against the primary papers (Schrödinger 1926, Born 1926, Born & Jordan 1925, Kennard 1927, Stern & Gerlach 1922, Tonomura et al. 1989, Bell 1964, CHSH 1969, Hensen et al. 2015), with the full list in [`videos/quantum/README.md`](videos/quantum/README.md#fact-check-notes-and-sources).
* General-relativity video: gravitational-wave strain for GW150914 from LIGO via the [Gravitational Wave Open Science Center](https://gwosc.org/) (GWTC-1); the image of M87* by the [Event Horizon Telescope Collaboration](https://www.eso.org/public/images/eso1907a/) (ESO, CC BY 4.0); derivations after Carroll's *Spacetime and Geometry*, Misner–Thorne–Wheeler and Schutz; the "ball of coffee grounds" after Baez & Bunn (2005); the thin-disk image after Luminet (1979); experimental values after Will's Living Review (2014) and Ashby (2003); full list in [`videos/relativity/README.md`](videos/relativity/README.md).
* General-relativity Part 2: GW150914 strain from LIGO via [GWOSC](https://gwosc.org/) (reused from Part 1); event parameters from LVK (GWTC-1; GW250114, PRL 135, 111403, 2025); Kerr quasinormal modes from the [`qnm`](https://github.com/duetosymmetry/qnm) package (Stein 2019, MIT); cosmological parameters from Planck 2018; the horizon diagram after Davis & Lineweaver (2004); Hulse–Taylor timing from Weisberg & Huang (2016); Gravity Probe B from Everitt et al. (2011); EHT values for M87* and Sgr A*; derivations after Carroll, Poisson's *A Relativist's Toolkit*, Wald, MTW and Maggiore; full list in [`videos/relativity2/README.md`](videos/relativity2/README.md#fact-check-notes-and-sources).
* Quantum mechanics, Part 2: alpha-decay half-lives from the [NNDC NuDat 3](https://www.nndc.bnl.gov/nudat3/) database and decay energies from the [AME2020](https://www-nds.iaea.org/amdc/) atomic mass evaluation; first ionization energies from the [NIST Atomic Spectra Database](https://physics.nist.gov/PhysRefData/ASD/ionEnergy.html) (snapshots committed in `videos/quantum2/data/`); constants are CODATA 2022 (via `scipy.constants`); derivations after Sakurai & Napolitano, Ballentine, Feynman & Hibbs, Griffiths & Schroeter and Thaller; full list in [`videos/quantum2/README.md`](videos/quantum2/README.md).
* Visual style inspired by Grant Sanderson's [3Blue1Brown](https://www.3blue1brown.com/).

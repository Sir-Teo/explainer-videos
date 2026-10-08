# Explainer Videos

3Blue1Brown-style explainers of math, physics, machine learning and markets, built entirely in code with
[Manim Community](https://www.manim.community/), narrated by an offline neural
TTS voice, and stitched into a finished video with subtitles and chapters.

| Video | Length | Watch | Source |
|---|---|---|---|
| **The Navier–Stokes Equations, Derived and Visualized** | 28 min | [`published/navier_stokes.mp4`](published/navier_stokes.mp4) | [`videos/navier_stokes`](videos/navier_stokes) |
| **How Large Language Models Work: The Transformer, Visualized** | 37 min | [`published/llm.mp4`](published/llm.mp4) | [`videos/llm`](videos/llm) |
| **Opposing Forces: Booming Earnings vs. the Rising Cost of Money** (Jurrien Timmer's market note of Oct 5, 2026, explained and fact-checked) | 37 min | [`published/opposing_forces.mp4`](published/opposing_forces.mp4) | [`videos/opposing_forces`](videos/opposing_forces) |
| **The Riemann Hypothesis, Visualized: Primes, Zeros, and the 2026 Quasi-Riemann Proof** (RH from scratch, then OpenAI's claimed zero-free half-plane Re s > 7/8 and how its proof works) | 39 min | [`published/riemann.mp4`](published/riemann.mp4) | [`videos/riemann`](videos/riemann) |
| **How Frontier AI Models Are Trained, End to End** (data, scaling laws, MoE, Muon, FP8/FP4, GPU clusters, RLHF and RL with verifiable rewards, as of Oct 2026; every chart a real miniature run on a 4-core CPU) | FRONTIER_MIN min | [`published/frontier.mp4`](published/frontier.mp4) | [`videos/frontier`](videos/frontier) |

The published files are 1080p30 MP4s (H.264, mono AAC narration mastered to
-16 LUFS) with soft English subtitles and chapter markers, sized to fit under
GitHub's 100 MB file limit by `tools/publish.py`; a sidecar `.srt` sits next
to each. Download one and open it in any player (VLC, QuickTime, a browser).
The LLM, Opposing Forces and Riemann videos' pictures are bit-identical to the full renders; the
Navier–Stokes video is re-encoded with two-pass x264 at ~350 kb/s (SSIM
0.98–0.9996 against the full render, lowest on the turbulence footage). The
96 kb/s narration is within measurement noise of the 192 kb/s master on
UTMOSv2 (3.99 vs 4.06 on seven 12 s speech clips).

## Quick start

```bash
# 1. System packages (Ubuntu/Debian). LaTeX is used for all math.
sudo apt-get install ffmpeg libpango1.0-dev pkg-config espeak-ng libmagic1 \
     texlive-latex-base texlive-latex-extra texlive-fonts-recommended texlive-science dvisvgm cm-super

# 2. Python env (3.10–3.12)
uv venv --python 3.12 .venv && source .venv/bin/activate
uv pip install --index-url https://download.pytorch.org/whl/cpu torch
uv pip install -e .

# 3. Precompute each video's "footage" (cached in .cache/)
python -m videos.navier_stokes.simulate      # fluid simulations (~40 min on 4 cores)
python -m videos.llm.analyze                 # GPT-2 probes + a tiny transformer trained on Shakespeare (~20 min)
python -m videos.riemann.compute             # real zeta zeros, prime counts, Möbius sums, domain coloring (~4 min)
python -m videos.frontier.compute            # Common Crawl + FineWeb filters, 43 pocket-model training runs, RL (~4 CPU-hours)
# (opposing_forces needs nothing: its market data snapshot, videos/opposing_forces/data.json, is committed)

# 4. Render: fast preview, then the final 1080p cut
python tools/build.py navier_stokes -q l      # -> renders/navier_stokes_480p.mp4
python tools/build.py navier_stokes           # -> renders/navier_stokes.mp4 (+ .srt, chapters)
python tools/build.py llm                     # -> renders/llm.mp4
python tools/build.py opposing_forces         # -> renders/opposing_forces.mp4
python tools/build.py riemann                 # -> renders/riemann.mp4
python tools/build.py frontier                # -> renders/frontier.mp4
```

Iterate on a single scene:

```bash
manim render -ql videos/navier_stokes/s04_material_derivative.py MaterialDerivative
manim render -ql --dry_run videos/navier_stokes/s04_material_derivative.py MaterialDerivative  # just check it runs
python tools/contact_sheet.py media/videos/s04_material_derivative/480p15/MaterialDerivative.mp4   # visual QA
```

Set `EXPLAINER_TTS=silent` to skip speech synthesis (timing is estimated), and
`EXPLAINER_VOICE` / `EXPLAINER_SPEED` to change the narrator.

## Repository layout

```
explainer/                 shared toolkit (import with `from explainer import *`)
  style.py                 semantic color palette, LaTeX macros, typography
  voiceover.py             VoiceoverScene: narration-driven timing, bookmarks, subtitles
  tts.py                   Kokoro-82M TTS backend, on-disk cache, pronunciation lexicon
  fluids/                  numpy/numba solvers that generate "real physics" footage
    lbm.py                 D2Q9 lattice-Boltzmann (flow past a cylinder), Smagorinsky LES
    spectral.py            pseudo-spectral 2D vorticity solver (periodic box)
    colormaps.py           field -> RGB maps tuned for the dark background
  lm/                      "real model" footage for the LLM and frontier-training videos
    gpt2.py                probes of GPT-2 (tokens, attention, residual stream, logit lens, ...)
    tiny_gpt.py            a minimal character-level GPT, trained from scratch on CPU
    bpe.py                 byte-pair encoding, step by step
    pocket.py              a modern pocket GPT (RMSNorm, RoPE, SwiGLU, QK-norm, MoE) + AdamW/Muon, cosine/WSD
  data/                    web-data footage for the frontier-training video
    crawl.py               Common Crawl through datatrove's FineWeb filters; MinHash LSH with FineWeb's settings
videos/<name>/
  manifest.py              scene order + chapter titles
  sNN_*.py                 one Scene class per chapter (narration lives in the code)
  simulate.py / analyze.py precomputes and caches the simulations / model data for this video
  fetch.py                 (opposing_forces) downloads public market data into a committed data.json snapshot
  compute.py               (riemann) mpmath/NumPy: zeta zeros, prime counts, Möbius walk, Gauss sums, domain coloring
                           (frontier) Common Crawl funnel, dedup, FineWeb-Edu scores, BPE, scaling-law / optimizer /
                           schedule / stability / MoE sweeps, Newton-Schulz, FP8/FP4, chat template, GRPO, Epoch data
  README.md                outline, color legend, sources and fact-check notes
  SCRIPT.md                narration, generated by tools/export_script.py
tools/
  build.py                 parallel render -> concat -> loudness mastering -> subtitles + chapters
  publish.py               GitHub-sized copy (< 100 MB) of a finished video -> published/
  export_script.py         extracts the narration script from the scene code
  contact_sheet.py         tiles frames of a render into one image for layout QA
  check_narration.py       Whisper "listen test": diffs what the TTS said against the script
  score_voice.py           UTMOSv2 naturalness + Whisper word error rate for narration audio
published/                 the finished videos, small enough for GitHub (see tools/publish.py)
```

## How a video is made (the workflow these tools encode)

1. **Outline the argument before animating.** Each chapter answers one question
   and ends on the idea the next chapter needs. Start from a concrete hook,
   build intuition, *then* derive, then pay it off.
2. **Narration is the clock.** Scenes are written as
   `with self.voiceover("... <bookmark mark='x'/> ...") as vo:` blocks. The audio
   is synthesized (and cached) first, and animations are timed to word-level
   bookmarks (`vo.until("x")`, `vo.wait_until("x")`), so picture and voice can
   never drift apart, and editing a sentence re-times only that block.
3. **One color per concept, everywhere.** `explainer/style.py` defines semantic
   colors (velocity is always blue, pressure red, viscosity green, ...). Scenes
   never hard-code a hex value for a concept.
4. **Derive on screen, step by step.** Every new line of a derivation is a
   transform of the previous one, with the term that changes highlighted and a
   brace or label saying *why* it changed.
5. **Real physics, not cartoons.** Fluid footage comes from actual solvers in
   `explainer/fluids`, precomputed once and played back with `FieldMovie`; the
   LLM video shows a real model's internals (GPT-2) and a real training run;
   every chart in the markets video is drawn from public data (FRED, the NY Fed,
   Shiller, Treasury, FactSet, per-stock prices), frozen in a committed snapshot;
   in the Riemann video every zero, prime count, Möbius walk, Gauss sum and
   domain-coloring pixel is computed (mpmath, NumPy), and the paper being
   explained is quoted from its own source. Schematics are labeled as schematics, and numbers the narration states are
   asserted against the data at render time.
6. **QA every render.** `--dry_run` catches exceptions in seconds;
   `tools/contact_sheet.py` catches overlaps and off-screen text;
   `tools/check_narration.py` catches mispronunciations (e.g. "dy" read as
   "die", "m a" read as "Emma"), fixed via the lexicon in `explainer/tts.py`;
   `tools/score_voice.py` measures how natural the narration sounds; the
   generated `SCRIPT.md` is what gets fact-checked. Claims about recent events
   get sources in the video's README.
7. **Ship with accessibility and good sound.** The build emits subtitles
   (soft-muxed and as `.srt`) and YouTube-style chapters automatically, and
   masters the soundtrack to -16 LUFS (EBU R128, -1.5 dBTP peak ceiling) so
   every video plays at the same comfortable level.

## The narration voice, and how it was chosen

The narrator is [Kokoro-82M](https://huggingface.co/hexgrad/Kokoro-82M), voice
`af_heart`, chosen by measurement. Small open-weight TTS models from Hugging
Face that run on a 4-core CPU were given the same four narration lines from
these videos, then scored with [UTMOSv2](https://huggingface.co/sarulab-speech/UTMOSv2)
(a predicted 1-5 naturalness MOS, VoiceMOS 2024 winner) and for intelligibility
(word error rate of a Whisper-small transcription against the script), using
`tools/score_voice.py`:

| Voice | Naturalness (UTMOSv2) | Word error rate |
|---|---|---|
| **Kokoro-82M `af_heart`** (used) | **3.84** | 3.2% |
| Kokoro-82M `am_michael` | 3.79 | 3.2% |
| Kyutai Pocket TTS (100M) `charles` | 3.52 | 3.7% |
| Kyutai Pocket TTS (100M) `alba` | 3.30 | 3.7% |
| Kokoro-82M `af_bella` | 3.06 | 2.5% |
| Qwen3-TTS 0.6B, Chatterbox-Turbo (350M) | not usable on CPU: more than 25 min for a single 15 s line | |

The remaining errors were pronunciation, not voice quality, and are fixed in
the lexicon (for example "F equals m a" was heard as "F equals Emma" from every
voice). Set `EXPLAINER_VOICE` to try another Kokoro voice.

## Credits

* Animation engine: [Manim Community Edition](https://www.manim.community/) (MIT).
* Voice: [Kokoro-82M](https://huggingface.co/hexgrad/Kokoro-82M) (Apache-2.0), voice `af_heart`.
* Model under the microscope: [GPT-2](https://huggingface.co/openai-community/gpt2) (OpenAI, modified MIT license), via Hugging Face `transformers`.
* Training text for the tiny model: Tiny Shakespeare from [`karpathy/char-rnn`](https://github.com/karpathy/char-rnn) (Shakespeare, public domain).
* Market note explained: Jurrien Timmer, [*Opposing Forces*](https://www.linkedin.com/pulse/opposing-forces-week-10526-jurrien-timmer-anaac/) (Fidelity Investments, Oct 5, 2026). The video paraphrases and attributes its arguments; it is not affiliated with Fidelity.
* Market and macro data: [FRED](https://fred.stlouisfed.org/) (Federal Reserve Bank of St. Louis), the [New York Fed](https://www.newyorkfed.org/research/data_indicators/term-premia-tabs) (ACM term premium), [Robert Shiller](https://shillerdata.com/), [U.S. Treasury Fiscal Data](https://fiscaldata.treasury.gov/), [FactSet Earnings Insight](https://insight.factset.com/), and Nasdaq daily prices.
* Frontier-training video: web data from [Common Crawl](https://commoncrawl.org/) (CC-MAIN-2026-39) filtered with Hugging Face's [`datatrove`](https://github.com/huggingface/datatrove) (Apache-2.0); pretraining text from [FineWeb-Edu](https://huggingface.co/datasets/HuggingFaceFW/fineweb-edu) (ODC-By) via `karpathy/fineweb-edu-100b-shuffle`; quality scores from [`HuggingFaceFW/fineweb-edu-classifier`](https://huggingface.co/HuggingFaceFW/fineweb-edu-classifier); chat template and outputs from [Qwen3-0.6B](https://huggingface.co/Qwen/Qwen3-0.6B) and its base model (Apache-2.0); training-compute data from [Epoch AI](https://epoch.ai/data/ai-models) (CC BY 4.0). Muon after [`KellerJordan/Muon`](https://github.com/KellerJordan/Muon); the end-to-end framing owes much to [`karpathy/nanochat`](https://github.com/karpathy/nanochat) and Hugging Face's training playbooks.
* Mathematics explained: OpenAI, [`github.com/openai/math`](https://github.com/openai/math), family 003, *The quasi-Riemann hypothesis* (Sept 30 – Oct 5, 2026). The video explains and attributes the manuscripts; it is not affiliated with OpenAI. Numerics: [mpmath](https://mpmath.org/) (BSD) and NumPy.
* Visual style inspired by Grant Sanderson's [3Blue1Brown](https://www.3blue1brown.com/).

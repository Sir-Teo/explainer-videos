# Writing a part of *AI, Built*: the working guide

[SYLLABUS.md](SYLLABUS.md) says what each part covers and the standard it meets. This file says how a part gets made,
with the lessons of the pilot (Part 26). Read Part 26's code (`videos/ai/ai26/`) next to it: it is the reference.

## Layout of a part

```
videos/ai/aiN/
  manifest.py        TITLE and SCENES = [(module, Scene class, chapter title)], film order
  common.py          PART = N, colours, small drawing helpers; re-exports compute.load (cached results)
  compute.py         every computed number: CACHE = Cache("aiN"), one compute_<item>() per experiment, ITEMS = {...}
  sNN_<name>.py      one chapter per module, one VoiceoverScene class each
  README.md          chapter outline with references, run instructions, problems with solutions (English, then 中文)
  narration_zh.json  the Chinese narration (tools/translate_narration.py manages it)
```

Shared instruments live in `explainer/ai/` (`lecture.py`: definition, theorem, history, objectives cards and the
problem set; `games.py`: boards and search trees; `viz.py`: plots, braces, glows). Chapter cards:
`chapter_card(k, title, question, lit=(years on the timeline,), part=PART)`.

## A chapter

A chapter is one scene of 3–5 minutes made of a few `self.voiceover(...)` blocks, each a paragraph of narration with
`<bookmark mark='x'/>` cues and the animations timed to them (`vo.wait_until("x")`). Each block ends with
`self.clear_scene()` or leads into the next.

- **Something on screen from the first word.** The screen must never sit empty or nearly empty under narration.
  Put a heading, a history card, the axes or the first object up before the first bookmark. `tools/dead_air.py`
  catches empty screens; a contact sheet catches sparse ones (a lone card on half the screen for 15 s).
- **One idea per block, every step of a derivation on screen** (`ladder(...)` with `why(...)` margin notes).
- **Visualize training.** Every learner that is trained gets a replay: snapshots during training, and the model's
  behaviour at each one (policy maps, episodes, prior bars, trees), scrubbed together with the learning curve.

## Numbers and claims

- **Every number on screen or in the narration comes from `compute.py` or a cited source.** Narration that states a
  result is an f-string over the cached data.
- **Narration follows the data, never the other way round.** When the story depends on a result (one method beats
  another, a curve climbs), compute the verdict and branch the sentence on it. Part 26's DQN ablation, policy-gradient
  comparison and AlphaZero chapter do this. Do not hide a disappointing result; explain it (cart-pole is too easy to
  separate REINFORCE from actor-critic; say so, and say where the difference shows up).
- **Measure fairly.** The pilot first graded Connect Four moves by "fastest win", which AlphaZero's ±1 value cannot
  see; the fair criterion is "keeps the win or the draw". Compare methods at equal budgets, or say what the
  budgets were. Use several seeds (5–8 for small RL runs) and show the spread (min–max, or ± one standard error
  for a comparison of means, labelled).
- **Show the pathology when it happens.** Without a target network DQN's values diverged to 10¹⁰; that became an
  on-screen measurement of the deadly triad instead of an assertion failure.
- Keep `assert`s in `compute.py` for invariants only (a solver agrees with brute force), not for hoped-for results.
- Pick the replayed run honestly: if the replay shows the best of several runs, say so on screen and in the
  narration, and show all runs elsewhere.

## Compute

- CPU budget about 2 hours per part; named exceptions are resumable and seeded. `python -m videos.ai.aiN.compute
  [items] [--force]`; long jobs run detached with logs under `.cache/aiN/`.
- On a 4-core machine: small torch jobs `OMP_NUM_THREADS=1`; a training job `torch.set_num_threads(2)` (4 threads
  under contention ran ten times slower); parallel evaluation through `ProcessPoolExecutor` once training is done.
- A scene that loads a missing cache item computes it. Never dry-run or render a scene whose data is still being
  produced: it computes (and caches) a result from incomplete data.
- Killing jobs: match with a bracket (`pgrep -f "[a]lphazero"`), and never inside a command line that contains the
  pattern itself.

## QA loop

1. Render a chapter silently at 480p15 (`EXPLAINER_TTS=silent`, `manim render -ql`), make a contact sheet
   (`tools/contact_sheet.py VIDEO -n 24 -c 4`), and look at every frame: overlaps, text off screen, sparse or empty
   stretches, labels that collide with data.
2. `tools/dead_air.py` on the built chapters.
3. `tools/lecture_length.py aiN` for the running time (30–60 min).
4. Full silent build: `EXPLAINER_TTS=silent python tools/build.py aiN -q l`.

## Chinese

1. Translate the narration in the style of [AI_ZH_GUIDE.md](AI_ZH_GUIDE.md) (spoken Mandarin, digits, the glossary).
   Lines computed from data are translated as templates with the same `{placeholders}`; the rendered English line
   is matched against the scene's f-string and its formatted values carried over.
2. After a render: `python tools/translate_narration.py aiN --lang zh` builds `narration_zh.json` from the rendered
   lines; fill it, then `--check`.
3. On-screen text: `python tools/collect_text.py aiN`, then `--check aiN`; add exact strings to
   `videos/ai/ai_text_zh.json`, and regex `patterns` for animated readouts ("after N steps: balanced M of 500").
   Strings that keep an acronym (TD, DQN) need an exact entry for `--check` to count them done.
4. `python tools/collect_text.py --lang zh aiN` dry-runs the Chinese build; then render a Chinese preview.

## Platforms

Renders work on macOS and Linux (`tools/smoke.py`). `explainer/compat.py` patches Pillow 13's `fromarray` for
manim 0.22's image drawing; the Chinese font is found per platform (`explainer/zh_text.py`). Narration: MLX on Apple
Silicon, PyTorch elsewhere (`tools/tts_server.py --engine torch`; CPU works with 16 GB but is 10–30× slower than
real time).

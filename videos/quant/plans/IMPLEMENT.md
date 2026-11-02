# Implementing a part's expansion (shared brief for every implementing agent)

You are expanding one part of *Quant, Built* (`videos/quant/quantN/`) from about 20–30 minutes to a 50–60 minute
lecture that can replace a university course: 3Blue1Brown-grade visuals, full technical depth, hands-on like the
*AI, Built* series. The research plan for your part already exists and is your blueprint:
`/tmp/claude-0/-home-user-explainer-videos/e79d9910-3070-5b5d-804d-ed98af9b99fd/scratchpad/plans/quantN.md`.

The owner's words: "make sure that our videos are as complete as possible (all the textbooks, papers, and frontier
systems by hedge funds or trading things), heavy focus on visualization so that users can see how cool those are
(just like our AI series)"; "visualization and technical because people might actually watch this in replacement of
the college lectures (think of 3b1b) and cool!"; "should have some hands-on things — see how the AI series actually
visualizes and trains a lot".

## Read first

1. Your plan file (above), all of it.
2. `CLAUDE.md`, `videos/quant/SYLLABUS.md` section 1 (the standard; chapters are about 3 minutes, 16–20 per part)
   and your part's section-6 entry; `videos/ai/LECTURE_GUIDE.md`.
3. Your part's existing code: `manifest.py`, `common.py`, `compute.py`, every `sNN_*.py`, `zh_lines.py`, `README.md`.
4. The instruments: `explainer/quant/__init__.py` (chapter_card, ladder/why/cmath, history_card, firm_card,
   desk_question, problem_set, payoff_card, reference_card, house_chart, series_map, axes, curve, band, legend,
   label, wrapped_label, note, code_block, objectives_card, …) and `explainer/quant/viz.py`, including the new
   hands-on instruments: `lab_card(title, lines, source)` + `lab_run(scene, card, outputs)` (House code on screen,
   then run, output typed out), `TrainingReplay(steps, loss, frame, checkpoints, …).play(scene)` (a fit or training
   scrubbed checkpoint by checkpoint with the loss curve and a live left panel), `seed_band(ax, xs, runs, color)`.
   A working example of all three: `scratchpad/vt/t.py`.
5. Exemplars of the bar: a rich finished quant part (`videos/quant/quant17/`, `videos/quant/quant16/`) and the AI
   series' hands-on parts (grep `videos/ai/*/s*.py` for `ValueTracker`, `always_redraw`, `ThreeDScene` to see live
   training replays, simulations and 3D).

## What to build

* Implement the plan's chapters (hook + 16–19 numbered chapters + outro), about 3 minutes each (2.5–4), total
  narration measured by `python tools/lecture_length.py quantN --floor 50` at 50–60 minutes. Narration speed is
  about 139 words per minute in English. A part that runs short is missing material, not padding.
* Every chapter: a signature visual that *moves* (built before the formula), derivations step by step with a reason
  per step (`ladder`), a computed experiment whose numbers come from `compute.py` via the cache (never typed into
  narration by hand; use f-strings), and narration that branches honestly on the computed result if it could go
  either way. 3D (`ThreeDScene`/`ThreeDAxes`, camera moves) wherever there are two inputs.
* Hands-on: at least three `lab_card`/`lab_run` moments with real House code (short excerpts of the actual library
  functions, ≤12 lines) whose printed outputs are the cached computed results; every fit or training shown as a
  `TrainingReplay` or ValueTracker-driven replay, with seeds as bands; simulations running on screen.
* Industry chapter (how desks, hedge funds, exchanges, regulators actually do it, public record only, allegations
  labelled as allegations, "as reported by X") and a frontier chapter (2023–2026 papers). Every paper on the
  part's READING.md list appears on screen somewhere; the README gets a textbook-audit table (textbook section →
  chapter).
* Keep existing scene module names and Scene class names for chapters you keep (narration and render caches are
  keyed by them); new chapters get new modules; order by `manifest.py`. Chapter numbers on `chapter_card`s and in the
  manifest must agree. Keep `compute.py` item names that exist; add new items. Scene method names must not shadow
  Scene methods (`setup`, `render`, `play`, `wait`, `add`, `remove`, `clear`).
* New House library functions go into the natural module under `explainer/quant/house/` (append; do not reorganise),
  each with a test appended to `tests/test_quant_house.py`; run `.venv/bin/python -m pytest -q tests/test_quant_house.py`.
* Update your part's SYLLABUS.md section-6 entry from the plan's paste-ready entry, your part's READING.md section
  (papers added), and `videos/quant/quantN/README.md` (English and Chinese halves: chapters, textbook audit,
  desk questions, problem solutions).

## Facts

Verify every fact before it goes on screen (primary sources; WebSearch/WebFetch). Anything the plan marks
*(verify)* or *(unverified)* is either verified by you now or dropped/reworded so it no longer asserts it. Firms only
from the public record; "as reported by"; allegations as allegations; nothing is investment advice. Numbers that the
plan says come from a planning run must be recomputed by `compute.py`; narration follows what the computation
actually returns.

## Chinese

Bilingual like the AI series. Narration: `videos/quant/quantN/zh_lines.py` (follow the existing file's format and
`videos/ai/AI_ZH_GUIDE.md`; term guide in `videos/quant/`), every English line translated, bookmarks and
`{placeholders}` identical. On-screen text: collect with `python tools/collect_text.py quantN` (English dry run;
it lists untranslated strings via `--check quantN`), write translations to a JSON file in the scratchpad
(`{"strings": {english: chinese}}`) and merge with `python tools/text_zh_add.py quant FILE.json` (locked; safe while
other agents merge). Checks, all must pass:
`python tools/zh_lines.py --todo quantN` (nothing left);
`python /tmp/claude-0/-home-user-explainer-videos/e79d9910-3070-5b5d-804d-ed98af9b99fd/scratchpad/zhcheck.py quantN`;
`python tools/collect_text.py --check quantN` (0 left);
`python tools/collect_text.py --lang zh quantN` (the Chinese dry run renders every scene).

## Checking visuals

`EXPLAINER_TTS=silent python tools/qa_scene.py quantN SceneName` writes a contact sheet
`renders/qa/quantN/SceneName_en.png` — Read it and look: overlaps, text off-frame, unreadable sizes, empty axes,
wrong signs, negative zeros, legends covering data. Fix and re-check. Do this for every new or changed scene, and in
Chinese (`--lang zh`) for the busiest ones.

## Shared machine (4 cores, ~7 GB free disk, other agents run in parallel)

* Run Python as `.venv/bin/python` from the repo root, with `OMP_NUM_THREADS=1 MKL_NUM_THREADS=1
  OPENBLAS_NUM_THREADS=1` and `torch.set_num_threads(1)` in any training code; launch long compute under `nice -n 10`
  with `nohup … &` and a log in the scratchpad, so it survives your turn. Budget about 2 CPU-hours of compute per part;
  make long items resumable (cache per item, checkpoints).
* Do not run narrated builds (`tools/make.py`, `tools/build.py`) — the lead does those. Dry runs and qa_scene only.
  Delete any large scratch outputs you create.
* Touch only your part's directory, your part's sections of SYLLABUS.md / READING.md, House modules (append-only),
  `tests/test_quant_house.py` (append-only), the zh text table via `text_zh_add.py`, and — append-only — new years in
  the shared timeline in `explainer/quant/__init__.py` if needed. Edit shared files with the Edit tool (small exact
  replacements), never by rewriting the whole file. If an Edit fails because the file changed, re-read and retry.
* Do not commit or push; the lead commits. No `pip install` into the system; if a package is truly needed, say so in
  your report instead. No model identifiers or personal emails in any file. Never send files to the user.

## Done means

`lecture_length.py quantN --floor 50` passes (50–60 min); all chapters implemented and previewed; all zh checks
pass including the Chinese dry run; House tests pass; README/SYLLABUS/READING updated; every plan item marked
verify is verified or removed. Then report briefly: minutes, chapters, compute items and CPU time, labs and replays,
facts verified and facts dropped, anything left undone and why.

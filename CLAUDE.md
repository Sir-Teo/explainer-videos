# Explainer videos

Manim videos with local neural narration. See README.md for layout and build commands.

- Run everything from the repo root; videos are addressed by name (`python tools/build.py quantum`), and
  `explainer/paths.py` (`video_dir`, `video_package`) resolves `videos/<series>/<name>/`. Never hard-code `videos/<name>`.
- A new video goes in `videos/<series>/<name>/` with `manifest.py`, `README.md`, `sNN_*.py` scenes.
- Generated and git-ignored: `media/`, `renders/`, `published/`, `.cache/`. Narration/manim caches are keyed by video
  name and scene module name, so renaming either invalidates them.
- Chinese narration: `videos/<series>/<name>/narration_zh.json`; each bilingual series (`analysis`, `ai`) keeps its on-screen text
  table (`<series>_text_zh.json`) and term guide in `videos/<series>/`.
- *AI, Built* (`videos/ai/`): thirty-one parts (`ai1` … `ai31`); the series plan is `videos/ai/README.md`, the
  chapter-by-chapter syllabus and the lecture standard every part meets are `videos/ai/SYLLABUS.md`; shared
  instruments in `explainer/ai/`.
- *Computer Science, Built* (`videos/cs/`): sixty-one parts in eleven acts (`cs1` … `cs61`: a CS degree plus industry practice in Acts I–X, a research tier in Act XI and a *Frontier* chapter in every part), Parts 1–21 built or in progress; the series plan
  is `videos/cs/README.md`, the chapter-by-chapter syllabus and standard are `videos/cs/SYLLABUS.md`. The machine the
  series builds (Pebble) and its instruments will live in `explainer/cs/`.

# Explainer videos

Manim videos with local neural narration. See README.md for layout and build commands.

- Run everything from the repo root; videos are addressed by name (`python tools/build.py quantum`), and
  `explainer/paths.py` (`video_dir`, `video_package`) resolves `videos/<series>/<name>/`. Never hard-code `videos/<name>`.
- A new video goes in `videos/<series>/<name>/` with `manifest.py`, `README.md`, `sNN_*.py` scenes.
- Generated and git-ignored: `media/`, `renders/`, `published/`, `.cache/`. Narration/manim caches are keyed by video
  name and scene module name, so renaming either invalidates them.
- Chinese narration: `videos/<series>/<name>/narration_zh.json`; each bilingual series (`analysis`, `ai`, `philosophy`) keeps its on-screen text
  table (`<series>_text_zh.json`) and term guide in `videos/<series>/`.
- *AI, Built* (`videos/ai/`): thirty-one parts (`ai1` … `ai31`); the series plan is `videos/ai/README.md`, the
  chapter-by-chapter syllabus and the lecture standard every part meets are `videos/ai/SYLLABUS.md`; shared
  instruments in `explainer/ai/`.
- *Philosophy, Built* (`videos/philosophy/`): forty-two parts (`philosophy1` … `philosophy42`); the plan is
  `videos/philosophy/README.md`, the part-by-part syllabus and the standard each part meets `videos/philosophy/SYLLABUS.md`;
  shared scene tools in `explainer/philosophy/` (the Reasoner's modules in `explainer/philosophy/reasoner/`, tested in
  `tests/philosophy/`); Chinese narration tables in `philosophyN/zh_lines.py`.

# Explainer videos

Manim videos with local neural narration. See README.md for layout and build commands.

- Run everything from the repo root; videos are addressed by name (`python tools/build.py quantum`), and
  `explainer/paths.py` (`video_dir`, `video_package`) resolves `videos/<series>/<name>/`. Never hard-code `videos/<name>`.
- A new video goes in `videos/<series>/<name>/` with `manifest.py`, `README.md`, `sNN_*.py` scenes.
- Generated and git-ignored: `media/`, `renders/`, `published/`, `.cache/`. Narration/manim caches are keyed by video
  name and scene module name, so renaming either invalidates them.
- Chinese narration: `videos/analysis/analysisN/narration_zh.json`; on-screen text table and term guide in `videos/analysis/`.

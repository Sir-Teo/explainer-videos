# Quant, Built: progress log (read this first when resuming)

The plan is [`SYLLABUS.md`](SYLLABUS.md); this file says what exists, what is next, and the exact commands.

## Resume in a fresh container

```bash
bash tools/setup_linux.sh && source .venv/bin/activate     # system packages + .venv (idempotent)
python -m explainer.quant.data                            # market data into .cache/quant_data (checksummed)
python -m pytest -q tests/test_quant_house.py             # the House library
python -m videos.quant.quant10.compute                    # Part 10's numbers into .cache/quant10 (~8 min)
EXPLAINER_TTS=silent python tools/qa_scene.py quant10 Hook   # one chapter, silent, with a contact sheet
```

Videos, audio, `media/`, `renders/` and `.cache/` are never committed (`.gitignore`); everything regenerates.

## Done

- **Phase 0 (partial).** `explainer/quant/` (acts, parts, timeline, cards, House chart; palette `explainer.style.QC`),
  the House library v0 (`explainer/quant/house/`: `bs`, `trees`, `paths`, `hedge`, `surface`), tests, the data
  layer (`explainer/quant/data.py`, manifest `videos/quant/data/manifest.json`), `tools/setup_linux.sh`.
- **The Surface** (Deribit BTC, 10 Dec 2025 08:00 UTC; 11 Dec for out-of-sample): 254 out-of-the-money quotes,
  11 expiries.
- **Part 10 compute** (`videos/quant/quant10/compute.py`): all items.
- **Part 10 English**: all 15 chapters written and reviewed by silent contact sheet (`tools/qa_scene.py`); README
  with desk questions and problems (English and Chinese); lecture_length estimate 55 min.
- **Part 10 Chinese narration**: `videos/quant/quant10/zh_lines.py` covers 70 of 70 source lines (templates for
  the computed ones); glossary and style in `videos/quant/QUANT_ZH_GUIDE.md`; `quant` is in `make.py`'s `BILINGUAL`,
  and `qa_audio.py` / `qa_series.py` resolve the series from the video name.
- **Part 10 silent build**: `renders/quant10_480p.mp4`, 52.6 min, 15 chapters; `tools/dead_air.py` finds only
  three 1.5–2.2 s transitions. (Implied's 3D surface is the slow chapter: about 29 min at 480p.)
- **Part 10 Chinese**: `narration_zh.json` filled (70 lines, `--verify` clean); on-screen text in
  `videos/quant/quant_text_zh.json` (577 strings; only "Vega" stays Latin); a Chinese Hook preview reviewed.

## In progress

- Chinese dry run of every chapter (`python tools/collect_text.py --lang zh quant10`, log
  `renders/make/quant10_zh_dry.log`): TeX and layout asserts.

## Next

1. Chinese silent previews of the dense chapters (`python tools/qa_scene.py quant10 <Scene> --lang zh`); then narrated
   builds (`python tools/make.py quant10`) in both languages.
2. Review with the user; lock the standard; then Part 1.
3. Phase 0 remainder: `qa_report.py` and `package_uploads.py` still list only the AI series.

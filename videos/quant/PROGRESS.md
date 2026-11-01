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

## In progress

- Part 10 full silent build (`python tools/build.py quant10 -q l` with `EXPLAINER_TTS=silent`; log
  `renders/make/quant10_silent_l.log`), then `tools/dead_air.py`, then `python tools/zh_lines.py quant10 --verify`.
- Part 10 on-screen text: `python tools/collect_text.py quant10`, `--check quant10`, translations merged into
  `videos/quant/quant_text_zh.json` with `tools/text_zh_add.py quant FILE`, then `--lang zh quant10` dry run.

## Next

1. Chinese preview of a few chapters (`EXPLAINER_LANG=zh`), QA; then narrated builds (Qwen3-TTS) in both languages.
2. Review with the user; lock the standard; then Part 1.
3. Phase 0 remainder: `qa_report.py` and `package_uploads.py` still list only the AI series.

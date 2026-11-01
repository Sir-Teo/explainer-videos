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

## In progress

- **Part 10 scenes** (the pilot), English, silent previews and QA. Chapter list in `videos/quant/quant10/manifest.py`.

## Next

1. Finish Part 10's scenes; QA every chapter (contact sheets, dead air, layout); README with problems and solutions.
2. Part 10 Chinese (zh_lines, narration_zh.json, quant_text_zh.json, QUANT_ZH_GUIDE.md).
3. Review with the user; lock the standard; then Part 1.
4. Phase 0 remainder: `quant` in make.py / qa_series.py / qa_report.py / qa_audio.py / package_uploads.py.

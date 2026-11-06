# Statistics, Built Part 1: source and visual review

Branch: `statistics-built`. This review covers Part 1's sixteen chapters in manifest order.
It is an English source/render review, not bilingual production approval.

## Repairs

- Quantiles: the generalized inverse of the ECDF now uses observations at its actual jumps. The box plot explicitly uses a separate, interpolated convention. Regional plots include all whiskers and count off-scale outliers.
- Histograms: bars receiving rounded dots count the rounded observations. The gold population overlay uses the full finite population's one-centimetre histogram, rather than a subsample KDE described as truth.
- Centres: the median's loss reports its one-sided slopes at a corner. Moving loss markers evaluate the actual objective. Off-scale income is labelled. The mode has its own window demonstration, replacing the continuous-data claim about the limit as p approaches zero.
- QQ plots: the fifteen-point example uses a seeded random subset. Reference lines retain their actual slope when clipped; omitted extreme points are counted. A heading remains visible during the introduction to the derivation.
- Correlation: all 400 families fit inside the axes; illustrative clouds have the sample correlations printed beneath them; vector labels are separated.
- Honest pictures: Minard's ribbon width is proportional to troop counts; pie slices have the labels needed to answer the question; Nightingale's annualized rate is distinguished from a probability; the lie-factor introduction retains a visible heading.
- Narration and recap: exact finite-population quantities refer to adults, approximate intervals are identified, rounded Anscombe summaries are described as nearly equal, and a finite-sample QQ plot is not claimed to prove a distribution family.
- Layout: the rotating spread diagram stays inside the frame; crowded timelines name the event relevant to the chapter; the payoff introduction retains its heading; loss labels sit within the plot.

The cache schema and seeds are preserved. The new quantile, QQ-subset, and correlation-cloud helpers operate on existing arrays.

## Verification and evidence

Final receipts are `verification.json`, `endpoints.json`, `native-endpoints.json`, `motion.json`, and `center-audio.json`. The complete regression run passed 540 tests and five subtests; its log is archived alongside this file. The six `*-1080-sheet.png` files preserve the reviewed native-render contact sheets. All sixteen English endpoint cases and all four motion cases are current and have no non-translation warnings.
Generated raw evidence remains under `renders/qa/series/stats1/en/`, `renders/qa/native1080/stats1/en/`, and `renders/qa/narrated/stats1/en/Center/`.

- `initial-findings.json` is a diagnostic snapshot from the first pass while repairs were in progress. Its source/data fingerprints are deliberately not presented as final approval.
- `native_endpoints.py` reproduces selected captures at 1920×1080 through the standard QA worker. It evaluates animation endpoints, not intermediate motion.
- The narrated Centre preview uses local Kokoro (`af_heart`) at 480p15. The remaining sampled motion previews use silent estimated timing.
- Automated waveform/alignment checks, when recorded, establish signal integrity only. They do not constitute listening approval.

Useful commands from the repository root, with the rendering environment active:

```bash
python -m pytest tests/test_stats*.py tests/test_qa*.py -q
python -m videos.stats.stats1.compute
python tools/qa_series.py stats1 --cached-only --resume --timeout 300
python docs/qa/evidence/stats1-polish-20261106/native_endpoints.py
python tools/qa_series.py stats1 --only Spread QQ SameStats Integrity --motion --cached-only --resume --timeout 1200
EXPLAINER_TTS=kokoro EXPLAINER_VOICE=af_heart python tools/qa_audio.py stats1
python tools/lecture_length.py stats1 --floor 50
python tools/qa_report.py stats1
```

## Remaining production work

The branch has no Chinese narration tables for any of its 65 parts and no statistics on-screen translation table. Translation warnings remain failures of the bilingual production standard; they have not been suppressed or counted as passes.

Full continuous playback/listening and final narrated masters in both languages remain pending. The QA runner's `needs-review` verdict must be retained while these translation warnings exist.

Parts 2–65 have not received this chapter-by-chapter review. See [the progress tracker](../../statistics-built-progress.md).

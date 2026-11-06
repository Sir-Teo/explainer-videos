# Statistics, Built Part 3: source and visual review

All sixteen chapters were read and inspected in manifest order. This is an English source/render review; bilingual production gates remain open.

## Repairs

- Distribution relationships now state their parameterizations and assumptions: negative-binomial failures versus trials, equal-scale gamma ratios, finite MGFs near zero, regular exponential families, canonical links, and conjugate prior families.
- Heavy-tail pictures retain omitted draws in density denominators. The t mixture and Cauchy simulations no longer truncate their samples; discrete overflow is not folded into an ordinary final bin. The chi-squared-one curve leaves the viewport with its divergence identified.
- The Zipf overlay uses the fitted intercept. Pareto moment claims distinguish the underlying unbounded law from the finite World. Product/lognormal and family-tree claims distinguish approximations, derived arrows, and later proofs.
- The horse-kick chart labels its final category as four or more. The binomial code block fits the frame; the rare-event chart leaves room for its definition card. Rotating normal draws stay inside the frame.
- The general Jacobian diagram uses an increasing transformation consistent with its increasing-map derivation. Gamma assumptions and clustered serial-number labels are readable; the Student historical card specifies the centered mean. Section headings remove empty narration beats.

## Verification

All sixteen final endpoint cases, seven native 1080p cases, and two silent motion cases are current and free of non-translation warnings. Compact source/data-keyed receipts and native contact sheets are saved here. The native selections are Hook, Rare, Normal, Transforms, Sampling, Order, and Mixtures. Motion checks cover Transforms and Sampling.

Normal has a 235.80-second narrated Kokoro preview. All seven actual audio segments pass signal/alignment checks, and its raw narration matches the current endpoint script. `normal-narrated-sheet.png` preserves the reviewed contact sheet. Automated scanning found no blank or sparse run lasting 1.5 seconds. This does not constitute continuous listening approval.

The combined statistics/QA run passed 554 tests and five subtests, with 15 warnings; its compressed log is archived here. Four new numerical regressions verify total variation, Box--Muller inversion, Student-mixture tail mass, and the fitted Zipf line. Raw renders remain under `renders/qa/series/stats3/en/`, `renders/qa/native1080/stats3/en/`, and `renders/qa/narrated/stats3/en/Normal/`.

Reproduce with the rendering environment active:

```bash
python -m videos.stats.stats3.compute
python tools/qa_series.py stats3 --cached-only --resume --timeout 300
python docs/qa/evidence/stats3-polish-20261106/native_endpoints.py
python tools/qa_series.py stats3 --motion --only Transforms Sampling --cached-only --timeout 1200
EXPLAINER_TTS=kokoro EXPLAINER_VOICE=af_heart python tools/qa_audio.py stats3 --only Normal
python -m pytest tests/test_stats*.py tests/test_qa*.py -q
```

Chinese narration and on-screen translation tables, continuous listening/playback, and final narrated masters remain pending. Translation warnings are retained. See [the progress tracker](../../statistics-built-progress.md).

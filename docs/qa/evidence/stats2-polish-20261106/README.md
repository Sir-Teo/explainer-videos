# Statistics, Built Part 2: source and visual review

All sixteen chapters have been read and inspected in manifest order. This is an English source/render review; bilingual production gates remain open.

## Repairs

- Probability models distinguish Bose occupation counts from equiprobable outcomes and specify the stationary, isotropic line model in Jaynes's chord argument.
- Bayes and Monty Hall distinguish conditioning on a particular reveal from the unconditional switching strategy. The prosecutor example states its restricted alternative model.
- Random variables distinguish atomic, density and singular continuous laws. Moment identities state finite-moment assumptions.
- The St Petersburg game separates a prize's certainty equivalent from an entry fee and states Feller's convergence in probability. Dutch-book and Cox arguments state their scope and assumptions.
- The axioms chapter now displays the complement and nested-event diagrams at the narration beats. Bayes's historical card clears before the derivation. Section headings remove empty introductions, and the CDF heading gives its classification a visible focus.
- The README and syllabus reconcile these claims with the displayed examples and exercises.

## Verification

The final source fingerprint is recorded in `verification.json`. All sixteen English endpoint cases, six native 1080p cases (Axioms, Bayes, Prosecutor, Monty, Variables, Variance), and two silent motion cases (Axioms and Variables) are current and free of non-translation warnings. The native contact sheets are saved alongside the compact receipts.

Variance has a 238.13-second narrated Kokoro preview. All six actual audio segments pass signal/alignment checks, and the captured raw narration matches the current endpoint script. Its contact sheet is `variance-narrated-sheet.png`; automated scanning found no blank or sparse run lasting 1.5 seconds. These checks do not constitute continuous listening approval.

The combined statistics/QA suite passed 554 tests and five subtests, with 15 warnings. The compressed regression log is preserved here. Raw render evidence remains under `renders/qa/series/stats2/en/`, `renders/qa/native1080/stats2/en/`, and `renders/qa/narrated/stats2/en/Variance/`.

Reproduce from the repository root with the rendering environment active:

```bash
python -m pytest tests/test_stats*.py tests/test_qa*.py -q
python -m videos.stats.stats2.compute
python tools/qa_series.py stats2 --cached-only --resume --timeout 300
python docs/qa/evidence/stats2-polish-20261106/native_endpoints.py
python tools/qa_series.py stats2 --motion --only Axioms Variables --cached-only --timeout 1200
EXPLAINER_TTS=kokoro EXPLAINER_VOICE=af_heart python tools/qa_audio.py stats2 --only Variance
```

## Remaining production work

Chinese narration and on-screen translation tables, continuous listening/playback, and final narrated masters remain pending. Translation warnings are retained. See [the progress tracker](../../statistics-built-progress.md) for the remaining parts.

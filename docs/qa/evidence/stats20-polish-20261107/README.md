# Part 20 English QA evidence

Every chapter was reviewed in manifest order, including survey weighting, domain variance, uncertainty propagation, measurement error, confounding and reporting. All six historical CDC input files were verified byte-for-byte.

Final capture fingerprint: `6dc53d18b13dada7776e1d27b03da20774793ec5a29bcd2cc6050e7f74615924`.

- All 15 English endpoint sheets and ten native 1920×1080 sheets were inspected. Runtime, bounds and blank-beat checks are clean; only missing-translation warnings remain.
- All nine selected silent motion sheets were inspected, with clean blank/sparse scans. Persistent context headings repair the estimand, checking and reporting introductions. Sensitivity plots display their full confidence-interval range.
- The actual narrated Sensitivity preview is 267.666 seconds. Its sheet was inspected, seven speech checks report zero issues, narration matches current source, and no blank/sparse gaps were detected.
- All 15 compute items and scene imports succeed. Fifteen focused numerical/reference checks pass; see `tests-final.txt`.

This is an English source/visual pass. Chinese narration/caption tables, continuous listening and full narrated playback, and final narrated masters in both languages remain open. No bilingual production approval is claimed.

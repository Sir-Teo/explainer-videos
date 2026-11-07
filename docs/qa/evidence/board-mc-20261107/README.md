# Coverage Board Monte Carlo uncertainty

Part 26 evaluates eight school intervals within each of 1,000 independent simulated datasets. Intervals within one dataset share a fitted hierarchy, so 8,000 intervals do not provide 8,000 independent Bernoulli coverage trials.

The Board now accepts an optional empirical Monte Carlo standard error. It is retained by serialization and reloads into later parts, so both the calibration band and verdict use the same error throughout the course. Existing rows without this field preserve their original independent-Bernoulli reference.

Six focused shared tests and sixteen Bayesian numerical/reference tests pass. Tests cover a correlated-target reference band, save/load preservation, unchanged legacy behavior, and invalid empirical errors.

This changes the conservative shared-code fingerprint for all parts. Previously inspected Parts 1–22 are being rendered again with fresh receipts; their scene sources and legacy Board values are unchanged. Parts 23–25 resume capture against this correction. No stale receipt is relabelled as current.

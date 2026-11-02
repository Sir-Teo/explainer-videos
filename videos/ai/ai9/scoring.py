"""Presentation-only score cohorts, pinned to the original evaluation recipes.

Indices are zero-based Unicode-code-point targets, inclusive. This module never
loads caches, evaluates a model, reconstructs an unrecorded score or changes a
stored number. In particular, lm['kn'] is a legacy Part 7 aggregate, not the
Kneser--Ney score aligned to Part 9's targets.
"""

from dataclasses import dataclass
import math


@dataclass(frozen=True)
class TargetCohort:
    first: int
    last: int

    @property
    def count(self):
        return self.last - self.first + 1


PASSAGE_COUNTING = TargetCohort(7, 21405)
PASSAGE_NEURAL = TargetCohort(24, 21405)
# curve[:, 1]: prefix of the first 50,000 validation source characters.
VALIDATION_CHECKPOINT = TargetCohort(24, 49999)
# lam_curve: prefix of the first 200,000 validation source characters.
VALIDATION_MIXTURE = TargetCohort(24, 199999)
# valid_bits: full validation suffix, not the short checkpoint-validation curve.
VALIDATION_FINAL = TargetCohort(24, 1239856)

METRIC_COHORTS = {
    "curve_passage": PASSAGE_NEURAL,
    "passage_bits": PASSAGE_NEURAL,
    "mix_bits": PASSAGE_NEURAL,
    "curve_validation": VALIDATION_CHECKPOINT,
    "lam_curve": VALIDATION_MIXTURE,
    "valid_bits": VALIDATION_FINAL,
    "legacy_kn": PASSAGE_COUNTING,
}


def passage_groups(lm, kn, infini):
    """Two within-cohort pairs; their order is historical, never a global rank.

    Return fresh rows so callers cannot mutate the original cache dictionaries.
    Only the final neural/mixture pair shares Part 9's passage suffix. The
    aligned KN-only scalar is absent from the original result and stays absent.
    """
    if int(lm['n_ctx']) != PASSAGE_NEURAL.first:
        raise ValueError('neural context differs from the audited target cohort')
    neural = [
        dict(key='nlm', label='the neural model', bits=lm['passage_bits'], part=9, kind='lm'),
        dict(key='mix', label=r'the neural model $+$ Kneser--Ney', bits=lm['mix_bits'], part=9, kind='lm'),
    ]
    historical = [
        dict(key='kn', label='Kneser--Ney', bits=kn['best_bits'], part=7, kind='count'),
        dict(key='infini', label=r'infinity-gram $+$ Kneser--Ney', bits=infini['mix_bits'], part=7, kind='count'),
    ]
    return ((PASSAGE_NEURAL, neural), (PASSAGE_COUNTING, historical))


def score_range(values, step=0.5):
    """Tick-aligned finite bounds containing every recorded value, without clipping."""
    values = [float(v) for v in values]
    if not values or not all(math.isfinite(v) and v >= 0 for v in values):
        raise ValueError('score range requires finite, nonnegative recorded scores')
    if not math.isfinite(step) or step <= 0:
        raise ValueError('tick step must be finite and positive')
    low = max(0.0, math.floor(min(values) / step) * step)
    high = math.ceil(max(values) / step) * step
    return low, max(high, low + step)

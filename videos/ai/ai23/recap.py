"""Small display projections for the recap; no cache access or producers."""
from __future__ import annotations

import numpy as np


def bpe_trace(data):
    """The recorded lengths are sampled every 50 merges, not every merge."""
    count = int(data["n_merges"])
    saved = np.asarray(data["saved"], float)
    lengths = np.asarray(data["length"], float)
    merges = np.arange(0, count + 1, 50)
    if count < 1 or saved.shape != (count,) or lengths.shape != merges.shape:
        raise ValueError("BPE recap needs the complete recorded merge/length trace")
    if not (np.isfinite(saved).all() and np.isfinite(lengths).all()) or np.any(saved < 0):
        raise ValueError("BPE savings and remaining symbol counts must be finite")
    expected = float(data["sample_chars"]) - np.r_[0.0, np.cumsum(saved)][merges]
    if np.any(lengths < 1) or not np.array_equal(lengths, expected):
        raise ValueError("BPE lengths disagree with recorded symbol savings")
    return merges, lengths


def entropy_window(data, limit=40):
    """Keep byte positions, including the unscored first byte's missing value."""
    scores = np.asarray(data["example_H"], float)
    if scores.ndim != 1 or len(scores) < 2 or not np.isnan(scores[0]):
        raise ValueError("The recap requires the corrected unscored initial byte")
    if not np.isfinite(scores[1:]).all() or np.any(scores[1:] < 0):
        raise ValueError("Scored byte entropies must be finite and nonnegative")
    if not isinstance(limit, int) or limit < 2:
        raise ValueError("Entropy window needs at least two byte positions")
    scores = scores[:limit].copy()
    return np.arange(len(scores)), scores


def modality_products(data):
    """Only an explicitly bound, independently accepted recap bundle may render.

    No producer is registered for this presentation namespace. Its provider must
    validate the products and their provenance before supplying this receipt.
    """
    required = {"vqtrain", "nyquist", "codec", "ctc", "clip"}
    if not isinstance(data, dict) or data.get("numerical_acceptance", {}).get("status") != "passed":
        raise ValueError("The full recap requires independently accepted modality products")
    products = data.get("products", {})
    if set(products) != required or not all(isinstance(v, dict) for v in products.values()):
        raise ValueError("The full recap needs exactly its five accepted modality products")
    return products


def entropy_threshold(data):
    value = float(data["threshold"])
    if not np.isfinite(value) or value < 0:
        raise ValueError("Entropy threshold must be finite and nonnegative")
    return value

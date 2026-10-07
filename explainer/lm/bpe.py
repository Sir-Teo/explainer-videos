"""Byte-pair encoding on a toy word list, step by step (Sennrich et al., 2016).

Start from single characters; repeatedly merge the most frequent adjacent pair
into a new vocabulary entry.  GPT-2's tokenizer was built the same way (on
bytes, with 50,000 merges).
"""

from __future__ import annotations

from collections import Counter


def train(word_counts: dict[str, int], n_merges: int) -> list[dict]:
    """Return one record per step: the segmentation of every word, the pair
    counts, and the pair that gets merged next."""
    words = {w: list(w) for w in word_counts}
    steps = []
    for _ in range(n_merges + 1):
        pairs: Counter = Counter()
        for w, segs in words.items():
            for a, b in zip(segs, segs[1:]):
                pairs[(a, b)] += word_counts[w]
        best = max(pairs.items(), key=lambda kv: (kv[1], kv[0]))[0] if pairs else None
        steps.append({
            "segments": {w: list(s) for w, s in words.items()},
            "pairs": sorted(([a, b, c] for (a, b), c in pairs.items()), key=lambda t: -t[2]),
            "merge": list(best) if best else None,
        })
        if best is None:
            break
        for w, segs in words.items():
            out, i = [], 0
            while i < len(segs):
                if i + 1 < len(segs) and (segs[i], segs[i + 1]) == best:
                    out.append(segs[i] + segs[i + 1])
                    i += 2
                else:
                    out.append(segs[i])
                    i += 1
            words[w] = out
    return steps[:n_merges + 1]

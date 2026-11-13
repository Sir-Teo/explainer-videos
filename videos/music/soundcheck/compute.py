"""The sounds of the sound check.

    python -m videos.music.soundcheck.compute [--force]

Items (clips are saved under ``.cache/soundcheck/audio/``):
    clicks    five clicks half a second apart, the first at 0.5 s: the sync test's reference
    tone      one pluck of the monochord's open string
    pan       the same pluck panned from left to right in five steps
    levels    a 1 kHz tone at the example level, then 6 dB quieter, then 6 dB quieter again
"""

from __future__ import annotations

import numpy as np

from explainer.ai.cache import Cache
from explainer.music.monochord import SR, Clip, ClipStore, concat, mix
from explainer.music.monochord.instruments import plucked, pure_tone
from explainer.music.monochord.loudness import integrated, true_peak_db

CACHE = Cache("soundcheck")
CLIPS = ClipStore("soundcheck")
load = CACHE.load


def compute_clicks() -> dict:
    n = int(3.2 * SR)
    y = np.zeros(n, np.float32)
    times = [0.5 + 0.5 * i for i in range(5)]
    k = int(0.004 * SR)
    burst = (np.sin(2 * np.pi * 2000 * np.arange(k) / SR) * np.hanning(k)).astype(np.float32)
    for t in times:
        i = int(round(t * SR))
        y[i:i + k] += 0.5 * burst
    CLIPS.save("clicks.five", Clip(y, events={f"click{i}": t for i, t in enumerate(times)}).label("synthesized"))
    return {"times": times}


def compute_tone() -> dict:
    c = Clip(plucked(seconds=3.0)).fade(0.002, 0.2).at_level(-15.0).label("physical model")
    CLIPS.save("tone.open", c)
    return {"lufs": integrated(c), "true_peak_db": true_peak_db(c), "seconds": c.duration}


def compute_pan() -> dict:
    note = Clip(plucked(seconds=0.9)).fade(0.002, 0.1)
    pans = [-1.0, -0.5, 0.0, 0.5, 1.0]
    c = mix([(note, 0.9 * i, 0.0, p) for i, p in enumerate(pans)]).at_level(-15.0)
    c.events = {f"p{i}": 0.9 * i for i in range(len(pans))}
    CLIPS.save("pan.sweep", c.label("physical model", needs="headphones"))
    return {"pans": pans}


def compute_levels() -> dict:
    ref = Clip(pure_tone(1000.0, 1.0)).fade(0.01, 0.05).at_level(-15.0)
    steps = [0.0, -6.0, -12.0]
    c = concat([ref.gain(g) for g in steps], gap=0.25, names=[f"s{i}" for i in range(3)])
    CLIPS.save("levels.steps", c.label("synthesized"))
    return {"steps_db": steps, "lufs": [integrated(ref.gain(g)) for g in steps]}


ITEMS = {"clicks": compute_clicks, "tone": compute_tone, "pan": compute_pan, "levels": compute_levels}

if __name__ == "__main__":
    CACHE.main(ITEMS, __doc__)

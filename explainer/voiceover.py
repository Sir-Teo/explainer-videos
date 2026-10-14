"""Narration-driven scenes.

Usage inside ``construct``::

    with self.voiceover(
        "A fluid is described by a velocity <bookmark mark='field'/> field."
    ) as vo:
        self.play(FadeIn(title), run_time=vo.until("field"))
        self.play(Create(field), run_time=vo.remaining())

The block always lasts at least as long as the audio: whatever time the
animations inside don't use is filled with ``wait`` on exit.  Animations that
run *past* the audio simply push the next line later, so nothing overlaps.

Each rendered scene also gets a ``.srt`` subtitle file and a ``.narration.json``
next to its video; ``tools/build.py`` stitches those into the final cut.
"""

from __future__ import annotations

import inspect
import json
import re
from contextlib import contextmanager
from pathlib import Path

from collections import OrderedDict

import manim.mobject.svg.svg_mobject as _svg_mobject
from manim import FadeOut, Scene

from . import lang, tts


class _BoundedCache(OrderedDict):
    """Manim keeps every parsed SVG (every distinct Tex string) forever. A readout that re-typesets a number each
    frame fills that cache by the thousand, and a long scene can grow past 6 GB. Keep only the most recent ones:
    the cache is an optimization, so rendering is unchanged."""

    def __init__(self, maxsize: int = 400):
        super().__init__()
        self.maxsize = maxsize

    def __getitem__(self, key):
        self.move_to_end(key)
        return super().__getitem__(key)

    def __setitem__(self, key, value):
        super().__setitem__(key, value)
        self.move_to_end(key)
        while len(self) > self.maxsize:
            self.popitem(last=False)


if not isinstance(_svg_mobject.SVG_HASH_TO_MOB_MAP, _BoundedCache):
    _svg_mobject.SVG_HASH_TO_MOB_MAP = _BoundedCache()

_BOOKMARK = re.compile(r"<bookmark\s+mark\s*=\s*['\"]([^'\"]+)['\"]\s*/>")


def _strip_bookmarks(text: str) -> tuple[str, dict[str, int]]:
    """Return clean text and {mark: index of the word (token) that follows it}."""
    marks: dict[str, int] = {}
    clean_parts: list[str] = []
    pos = 0
    for m in _BOOKMARK.finditer(text):
        clean_parts.append(text[pos : m.start()])
        marks[m.group(1)] = len(lang.tokens(lang.clean("".join(clean_parts))))
        pos = m.end()
    clean_parts.append(text[pos:])
    clean = lang.clean("".join(clean_parts))
    return clean, marks


class VoiceoverTracker:
    def __init__(self, scene: Scene, utt: tts.Utterance, marks: dict[str, int], start: float):
        self.scene = scene
        self.utt = utt
        self.marks = marks
        self.start = start

    @property
    def duration(self) -> float:
        return self.utt.duration

    def elapsed(self) -> float:
        return self.scene.renderer.time - self.start

    def remaining(self, minimum: float = 0.5) -> float:
        """Seconds of audio left in this block (at least ``minimum``)."""
        return max(minimum, self.duration - self.elapsed())

    def mark_time(self, mark: str) -> float:
        idx = self.marks[mark]
        words = self.utt.words
        if idx >= len(words):
            return self.duration
        return words[idx].start

    def until(self, mark: str, minimum: float = 0.5) -> float:
        """Seconds from *now* until the word after ``<bookmark mark=.../>``."""
        return max(minimum, self.mark_time(mark) - self.elapsed())

    def wait_until(self, mark: str) -> None:
        dt = self.mark_time(mark) - self.elapsed()
        if dt > 1 / 60:
            self.scene.wait(dt)


class VoiceoverScene(Scene):
    """A Scene whose pacing is driven by narration."""

    def setup(self):
        super().setup()
        self._narration: list[dict] = []

    @contextmanager
    def voiceover(self, text: str, gain: float | None = None, pad: float = 0.15):
        raw = text
        text = lang.translate(text, Path(inspect.getfile(type(self))).parent, type(self).__name__)
        clean, marks = _strip_bookmarks(text)
        utt = tts.synthesize(clean)
        start = self.renderer.time
        self._add_narration(str(utt.audio_path), gain)
        tracker = VoiceoverTracker(self, utt, marks, start)
        yield tracker
        left = utt.duration - tracker.elapsed()
        if left > 1 / 60:
            self.wait(left)
        if pad > 0:
            self.wait(pad)
        self._narration.append(
            {
                "start": start,
                "duration": utt.duration,
                "text": clean,
                "raw": " ".join(raw.split()),
                "words": [[w.text, start + w.start, start + w.end] for w in utt.words],
            }
        )

    def _add_narration(self, path: str, gain: float | None) -> None:
        # Not Scene.add_sound: it returns early while renderer.skip_animations is set, which is also the
        # case right after any play() served from the partial-movie cache, so a re-render of a cached
        # scene silently lost most of its narration. Only genuine skipping (-n, -s) drops the sound.
        if getattr(self.renderer, "_original_skipping_status", False):
            return
        self.renderer.file_writer.add_sound(path, self.renderer.time, gain)

    def clear_scene(self, *keep, extra=(), run_time: float = 1.0):
        """Fade out everything except ``keep`` (plus run any ``extra`` animations).

        Mobjects built piecewise (e.g. ``Write(eq[0])``, ``Write(eq[1:])``) are
        re-consolidated first, and updaters on the faded mobjects are cleared so
        ``always_redraw`` objects actually fade instead of popping out.
        """
        keep_family = set()
        for k in keep:
            self.add(k)
            keep_family.update(k.get_family())
        others = [m for m in self.mobjects if m not in keep_family]
        for m in others:
            m.clear_updaters()
        anims = [FadeOut(m) for m in others] + list(extra)
        if anims:
            self.play(*anims, run_time=run_time)

    # ------------------------------------------------------------------
    # Subtitles / script export
    # ------------------------------------------------------------------
    def tear_down(self):
        super().tear_down()
        try:
            movie = Path(self.renderer.file_writer.movie_file_path)
        except Exception:
            return
        if not self._narration or movie is None:
            return
        movie.parent.mkdir(parents=True, exist_ok=True)
        meta = {"scene": type(self).__name__, "duration": self.renderer.time, "lines": self._narration}
        movie.with_suffix(".narration.json").write_text(json.dumps(meta, ensure_ascii=False, indent=1))
        movie.with_suffix(".srt").write_text(to_srt(subtitle_cues(self._narration)))


# ---------------------------------------------------------------------------
# Subtitle helpers (also used by tools/build.py)
# ---------------------------------------------------------------------------
# Where a long sentence may be cut so that each piece still reads naturally.
_SOFT_BREAK = {"en": (",", ";", ":"), "zh": ("，", "、", "；", "：")}


def _sentences(words: list, ends: tuple) -> list[list]:
    out, cur = [], []
    for w in words:
        cur.append(w)
        if w[0].endswith(ends):
            out.append(cur)
            cur = []
    return out + [cur] if cur else out


def _even_split(words: list, language: str, max_chars: int) -> list[list]:
    """Cut one sentence into the fewest cues of at most ``max_chars``, as even in length as possible and preferring
    cuts after a comma: no orphaned last word, no cue twice as long as its neighbour."""
    n = len(words)
    sizes = [0]
    for w in words:
        sizes.append(sizes[-1] + len(w[0].strip()))
    gap = 1 if language == "en" else 0  # the joining space between English words

    def width(i: int, j: int) -> int:
        return sizes[j] - sizes[i] + gap * (j - i - 1)

    total = width(0, n)
    if total <= max_chars or n == 1:
        return [words]
    soft = _SOFT_BREAK.get(language, ())
    inf = float("inf")
    chosen, chosen_cost, first = [[w] for w in words], inf, None
    k = -(-total // max_chars)
    while k <= n and (first is None or k <= first + 1):  # the fewest cues, or one more if that cuts more cleanly
        target = total / k
        best = [[inf] * (k + 1) for _ in range(n + 1)]
        prev = [[0] * (k + 1) for _ in range(n + 1)]
        best[0][0] = 0.0
        for j in range(1, n + 1):
            for c in range(1, min(k, j) + 1):
                for i in range(c - 1, j):
                    w_ = width(i, j)
                    if best[i][c - 1] == inf or (w_ > max_chars and j - i > 1):
                        continue
                    cost = best[i][c - 1] + (w_ - target) ** 2
                    if j < n and not words[j - 1][0].endswith(soft):
                        cost += (0.4 * target) ** 2  # a cut mid-clause costs as much as being 40% off the target
                    if cost < best[j][c]:
                        best[j][c], prev[j][c] = cost, i
        if best[n][k] < inf:
            first = k if first is None else first
            cost = best[n][k] + k * (0.25 * max_chars) ** 2  # each extra cue costs a little
            if cost < chosen_cost:
                parts, j = [], n
                for c in range(k, 0, -1):
                    parts.append(words[prev[j][c]:j])
                    j = prev[j][c]
                chosen, chosen_cost = parts[::-1], cost
        k += 1
    return chosen


def subtitle_cues(lines: list[dict], offset: float = 0.0, language: str | None = None) -> list[tuple[float, float, str]]:
    """Split narration into readable cues: one per sentence, with long sentences cut evenly (see _even_split)."""
    language = language or lang.LANG
    ends, max_chars = lang.SENTENCE_END[language], lang.CUE_CHARS[language]
    cues = []
    for line in lines:
        for sentence in _sentences(line["words"], ends):
            for part in _even_split(sentence, language, max_chars):
                cues.append([offset + part[0][1], offset + part[-1][2], lang.join([w[0] for w in part], language)])
    # Keep each cue on screen until the next one starts (max +1.5 s).
    for a, b in zip(cues, cues[1:]):
        a[1] = max(a[1], min(b[0], a[1] + 1.5))
    return [tuple(c) for c in cues]


def _ts(t: float) -> str:
    ms = int(round(t * 1000))
    h, ms = divmod(ms, 3_600_000)
    m, ms = divmod(ms, 60_000)
    s, ms = divmod(ms, 1000)
    return f"{h:02d}:{m:02d}:{s:02d},{ms:03d}"


def to_srt(cues) -> str:
    out = []
    for i, (a, b, text) in enumerate(cues, 1):
        out.append(f"{i}\n{_ts(a)} --> {_ts(b)}\n{text}\n")
    return "\n".join(out)

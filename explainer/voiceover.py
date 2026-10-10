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

import json
import os
import re
from contextlib import contextmanager
from pathlib import Path

from manim import FadeOut, Scene

from . import tts

_BOOKMARK = re.compile(r"<bookmark\s+mark\s*=\s*['\"]([^'\"]+)['\"]\s*/>")


def _strip_bookmarks(text: str) -> tuple[str, dict[str, int]]:
    """Return clean text and {mark: index of the word that follows it}."""
    marks: dict[str, int] = {}
    clean_parts: list[str] = []
    pos = 0
    for m in _BOOKMARK.finditer(text):
        clean_parts.append(text[pos : m.start()])
        so_far = " ".join("".join(clean_parts).split())
        marks[m.group(1)] = len(so_far.split()) if so_far else 0
        pos = m.end()
    clean_parts.append(text[pos:])
    clean = " ".join("".join(clean_parts).split())
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
        # Set encoding quality before the first frame reaches PyAV. Manim's
        # default CRF is 23; source masters for YouTube can use a lower value.
        crf = os.environ.get("EXPLAINER_RENDER_CRF")
        if crf is not None:
            value = int(crf)
            if not 0 <= value <= 51:
                raise ValueError("EXPLAINER_RENDER_CRF must be between 0 and 51")
            writer = self.renderer.file_writer
            open_stream = writer.open_partial_movie_stream

            def open_master_stream(*args, **kwargs):
                open_stream(*args, **kwargs)
                if writer.video_stream.codec_context.name == "libx264":
                    writer.video_stream.codec_context.thread_count = int(
                        os.environ.get("EXPLAINER_RENDER_THREADS", "2")
                    )
                    writer.video_stream.codec_context.options = {
                        **writer.video_stream.codec_context.options, "crf": str(value),
                    }

            writer.open_partial_movie_stream = open_master_stream

    @contextmanager
    def voiceover(self, text: str, gain: float | None = None, pad: float = 0.15):
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
MAX_CUE_CHARS = 84


def subtitle_cues(lines: list[dict], offset: float = 0.0) -> list[tuple[float, float, str]]:
    """Split narration into readable cues, breaking at sentence ends / length."""
    cues = []
    for line in lines:
        words = line["words"]
        cur: list = []
        for i, w in enumerate(words):
            cur.append(w)
            text = " ".join(x[0] for x in cur)
            sentence_end = w[0].endswith((".", "?", "!", ":", ";"))
            too_long = len(text) > MAX_CUE_CHARS - 12
            last = i == len(words) - 1
            if sentence_end or too_long or last:
                cues.append([offset + cur[0][1], offset + cur[-1][2], text])
                cur = []
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

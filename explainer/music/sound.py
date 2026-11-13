"""Scenes that make sound (videos/music/SYLLABUS.md, section 3).

A :class:`SoundScene` is a :class:`~explainer.voiceover.VoiceoverScene` with a second layer of audio: clips computed
by the part's ``compute.py`` (:class:`explainer.music.monochord.Clip`), placed on the timeline next to the
narration::

    with self.listen(clip) as snd:              # a listening window: the narration is silent, the clip plays
        snd.drive(playhead, lambda m, t: m.set_x(x0 + w * t / clip.duration))
        snd.wait_until("note3")                 # the clip's named events, like bookmarks in a narrated line
        self.play(Indicate(third_note))
    # on exit the block has lasted as long as the clip

    with self.voiceover("... <bookmark mark='a'/> ...") as vo:
        vo.wait_until("a")
        self.sound(clip, gain_db=-8, underscore=True)   # sound under narration, where the plan calls for it

Two rules of the series are enforced here.  *Every sound is a computed result*: a scene can only play a ``Clip``
that came from the cache.  *Everything you hear, you see*: :meth:`SoundTracker.drive` moves a picture from the
clip's own clock, so the picture cannot drift from the sound, and ``tools/qa_sound.py`` checks that every window had
one.

Each rendered scene writes ``<Scene>.cues.json`` next to its video.  ``tools/build.py`` mixes the master's music stem
from those cues at full resolution (float, stereo, 48 kHz); a scene rendered on its own (a preview) gets the same
clips through manim's mixer instead.
"""

from __future__ import annotations

import json
import os
from contextlib import contextmanager
from pathlib import Path

from explainer.music.monochord.audio import Clip
from explainer.voiceover import VoiceoverScene

EXAMPLE_LEVEL = -15.0  # LUFS, loudest 400 ms: the level an example is authored at (Clip.at_level); the narration
#                        is mastered to -16 LUFS integrated, whose loudest moments read about -12
QUIET_LEVEL = -21.0    # an example meant to sit back, or to run under narration
PEAK_CEILING_DB = -1.5  # dBTP: nothing in a master may exceed it (checked, never limited)


def clip_loader(cache, store):
    """``clip(name)`` for a part's scenes: the clip ``<item>.<sub>`` from the part's store, computing the item that
    makes it on first use (as ``Cache.load`` does for numbers)."""

    def clip(name: str) -> Clip:
        if not store.has(name):
            cache.load(name.split(".")[0])
            if not store.has(name):
                raise FileNotFoundError(
                    f"clip {name!r} is missing although its item is cached: rerun the part's compute with --force "
                    f"{name.split('.')[0]}")
        return store.load(name)

    return clip


class SoundTracker:
    """A playing clip: its clock, its events."""

    def __init__(self, scene: "SoundScene", clip: Clip, start: float):
        self.scene, self.clip, self.start = scene, clip, start
        self._driven: list = []
        self._owned: list = []

    @property
    def duration(self) -> float:
        return self.clip.duration

    def elapsed(self) -> float:
        """Seconds since the clip started (exact between animations)."""
        return self.scene.renderer.time - self.start

    def remaining(self, minimum: float = 0.0) -> float:
        return max(minimum, self.duration - self.elapsed())

    def time_of(self, event) -> float:
        """An event's time in the clip: a name from ``clip.events`` or a number of seconds."""
        if isinstance(event, (int, float)):
            return float(event)
        if event not in self.clip.events:
            raise KeyError(f"clip {self.clip.meta.get('name', '?')!r} has no event {event!r}: "
                           f"{sorted(self.clip.events)}")
        return float(self.clip.events[event])

    def until(self, event, minimum: float = 1 / 30) -> float:
        """Seconds from now until an event: a ``run_time`` that lands on it."""
        return max(minimum, self.time_of(event) - self.elapsed())

    def wait_until(self, event) -> None:
        dt = self.time_of(event) - self.elapsed()
        if dt > 1 / 60:
            self.scene.wait(dt)

    def wait(self) -> None:
        """Wait for the clip to end."""
        dt = self.remaining()
        if dt > 1 / 60:
            self.scene.wait(dt)

    def drive(self, mob, fn):
        """Update ``mob`` every frame from the clip's clock: ``fn(mob, t)`` with t in seconds since the clip began.
        The mobject keeps its own count of the time, so it is right whatever order the scene updates things in."""
        state = {"t": self.elapsed()}

        def upd(m, dt):
            state["t"] += dt
            fn(m, state["t"])

        fn(mob, state["t"])
        mob.add_updater(upd)
        self._driven.append((mob, upd))
        return mob

    def show(self, *mobs):
        """Add mobjects that belong to this clip (a listening strip, a sound tag): they leave the scene when the
        window closes."""
        self.scene.add(*mobs)
        self._owned += list(mobs)
        return mobs[0] if len(mobs) == 1 else mobs

    def release(self) -> None:
        for mob, upd in self._driven:
            mob.remove_updater(upd)
        self._driven = []
        if self._owned:
            self.scene.remove(*self._owned)
            self._owned = []


class SoundScene(VoiceoverScene):
    """A narrated scene that also plays computed clips."""

    def setup(self):
        super().setup()
        self._cues: list[dict] = []
        self._windows: list[SoundTracker] = []

    # ------------------------------------------------------------------
    def sound(self, clip: Clip, gain_db: float = 0.0, underscore: bool = False, window: bool = False) -> SoundTracker:
        """Start a clip now and return its tracker.  ``underscore`` marks sound that is meant to run under
        narration; without it the sound gate reports any overlap with a narrated line."""
        if not isinstance(clip, Clip) or "path" not in clip.meta:
            raise TypeError("a scene plays clips from the part's clip store (ClipStore.load), not raw arrays")
        start = self.renderer.time
        self._cues.append({
            "clip": clip.meta.get("name", ""), "path": clip.meta["path"], "start": start,
            "duration": clip.duration, "gain_db": float(gain_db), "underscore": bool(underscore),
            "window": bool(window), "label": clip.meta.get("label", ""), "peak_db": round(clip.peak_db + gain_db, 2),
        })
        # A preview rendered by manim alone gets the clip through manim's own mixer (16-bit).  A build asks for
        # stems instead: the master's music is mixed from the cue sheet, in float.
        if not os.environ.get("EXPLAINER_SOUND_STEMS") and not getattr(self.renderer, "_original_skipping_status", False):
            pcm = Path(clip.meta["path"]).with_suffix(".pcm.wav")
            self.renderer.file_writer.add_sound(str(pcm), start, gain_db or None)
        return SoundTracker(self, clip, start)

    @contextmanager
    def listen(self, clip: Clip, gain_db: float = 0.0, pad: float = 0.3):
        """A listening window: the clip plays with no narration over it, and the block lasts as long as the clip
        (plus ``pad`` seconds of quiet)."""
        snd = self.sound(clip, gain_db, window=True)
        cue = self._cues[-1]
        self._windows.append(snd)
        try:
            yield snd
            left = snd.remaining()
            if left > 1 / 60:
                self.wait(left)
            if pad > 0:
                self.wait(pad)
        finally:
            cue["driven"] = len(snd._driven)  # how many pictures moved on this clip's clock (the gate wants one)
            snd.release()

    # ------------------------------------------------------------------
    def tear_down(self):
        super().tear_down()
        meta = {"scene": type(self).__name__, "duration": self.renderer.time, "cues": self._cues}
        out = os.environ.get("EXPLAINER_NARRATION_OUT")
        if out:
            path = Path(out) / f"{type(self).__name__}.cues.json"
        else:
            try:
                path = Path(self.renderer.file_writer.movie_file_path).with_suffix(".cues.json")
            except Exception:
                return
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(json.dumps(meta, indent=1))

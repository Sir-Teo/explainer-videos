"""Checks every part of *Music, Built* must pass, whatever it is about: its clips keep the series' rules, its scenes
and its clip store agree, every listening window says what it is, and the ear thread is there."""

from __future__ import annotations

import re
from pathlib import Path

from explainer.music.monochord.loudness import momentary_max, true_peak_db

LABELS = ("physical model", "synthesized", "rendered", "recording")


def scene_sources(compute, scenes) -> dict[str, str]:
    here = Path(compute.__file__).parent
    return {module: (here / f"{module}.py").read_text() for module, _, _ in scenes}


def check_clips(compute, minimum: int = 10, floor: float = -26.0) -> None:
    """Labelled, under the peak ceiling, and inside the series' range of loudness."""
    names = sorted(p.stem for p in compute.CLIPS.dir.glob("*.json"))
    assert len(names) >= minimum, names
    for name in names:
        c = compute.CLIPS.load(name)
        assert c.meta.get("label") in LABELS, name
        assert true_peak_db(c) <= -1.5, (name, true_peak_db(c))
        assert floor <= momentary_max(c) <= -15.0, (name, momentary_max(c))
        assert all(0 <= t <= c.duration + 1e-6 for t in c.events.values()), name


def check_scenes_and_clips(compute, scenes) -> None:
    """Every clip a scene asks for exists, and every stored clip is used."""
    stored = {p.stem for p in compute.CLIPS.dir.glob("*.json")}
    asked = set()
    for src in scene_sources(compute, scenes).values():
        asked |= set(re.findall(r'clip\("([a-z_0-9]+\.[a-z_0-9]+)"\)', src))
        for item in re.findall(r'clip\(f"([a-z_0-9]+)\.\{', src):
            asked |= {n for n in stored if n.startswith(item + ".")}
    assert asked <= stored, sorted(asked - stored)
    assert stored <= asked, sorted(stored - asked)


def check_windows(compute, scenes) -> None:
    """With the sound off, the subtitles name each example: every window passes its words to the cue sheet."""
    for module, src in scene_sources(compute, scenes).items():
        assert not re.search(r"window\(snd\)", src), f"{module}: a listening window without a caption"
        assert src.count("self.listen(") <= src.count("window(snd"), f"{module}: a window without its strip"


def check_ear_thread(compute, scenes) -> None:
    """Three to six pause-and-listen questions in a part (SYLLABUS section 1)."""
    asked = sum(src.count("listen_card(") for src in scene_sources(compute, scenes).values())
    assert 3 <= asked <= 6, asked


def check_part(compute, scenes, minimum: int = 10) -> None:
    check_clips(compute, minimum)
    check_scenes_and_clips(compute, scenes)
    check_windows(compute, scenes)
    check_ear_thread(compute, scenes)

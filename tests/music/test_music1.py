"""Part 1 of *Music, Built*: what the film says is what was computed, and every sound keeps the series' rules.

    python -m pytest -q tests/music/test_music1.py

The cache is filled on first use (about half a minute).
"""

import json

import numpy as np
import pytest

from explainer.music.monochord.loudness import momentary_max, true_peak_db
from videos.music.music1 import compute
from videos.music.music1.manifest import SCENES

load = compute.load


def test_the_legend_fails_on_a_string():
    d = load("hammers")
    assert d["as_weights"]["octave"]["measured_cents"] == pytest.approx(600, abs=2)     # not 1200
    assert d["f_w24"] / d["f_w6"] == pytest.approx(2.0, rel=2e-3)                       # four times the weight


def test_the_monochords_ratios():
    d = load("ratios")
    for name, want in (("octave", 2.0), ("fifth", 1.5), ("fourth", 4 / 3)):
        assert d["rows"][name]["ratio"] == pytest.approx(want, rel=3e-4)
        assert abs(d["rows"][name]["cents_off"]) < 0.5


def test_mersennes_exponents():
    d = load("mersenne")
    e = d["exponents"]
    assert (round(e["L"], 2), round(e["T"], 2), round(e["mu"], 2)) == (-1.0, 0.5, -0.5)
    assert d["constant"] == pytest.approx(0.5, abs=0.005)


def test_beads_against_dalembert_and_the_wave_speed():
    assert load("dalembert")["b20_error"] < 1e-12
    p = load("pulse")
    assert p["speed_measured"] == pytest.approx(p["speed_formula"], rel=1e-3)
    assert np.abs(p["right"][:, 0]).max() == 0 and np.abs(p["right"][:, -1]).max() < 1e-12   # the ends stay still


def test_a_few_beads_are_flat():
    d = load("beads")["rows"]
    assert d["6"]["flat_cents"][1] < -60 and abs(d["200"]["flat_cents"][3]) < 1


def test_the_touched_harmonic():
    t = load("modes")["touch"]
    assert t["half"]["pitch_after"] == pytest.approx(2 * compute.STRING.f1, rel=5e-3)
    assert t["third"]["pitch_after"] == pytest.approx(3 * compute.STRING.f1, rel=5e-3)
    assert t["half"]["after_db"][0] < -60 and t["half"]["after_db"][1] > -15


def test_fourier_sum_and_the_pluck():
    f = load("fourier")
    assert f["error_slope"] == pytest.approx(-1.0, abs=0.05)
    assert abs(f["a"][4]) < 1e-12                       # plucked at a fifth: no fifth mode
    for row in load("pluck")["rows"].values():
        assert row["worst_db"] < 1.0


def test_partials_of_the_open_string():
    t = load("overtones")["table"]
    assert [r["note"] for r in t[:6]] == ["C3", "C4", "G4", "C5", "E5", "G5"]
    assert t[0]["t60"] > t[9]["t60"] > 0


def test_shared_partials_and_beats():
    c = load("coincide")
    assert [c["rows"][k]["count"] for k in ("octave", "fifth", "fourth", "tritone")] == [6, 4, 3, 0]
    assert c["mistuned"]["beat_hz"] == pytest.approx(2.73, abs=0.02)


def test_the_beats_are_in_the_clip_itself():
    """The picture of the mistuned fifth is the band round the two partials, filtered out of the clip that is heard."""
    c = load("coincide")
    band = c["band"]
    assert band["beat_hz_measured"] == pytest.approx(c["mistuned"]["beat_hz"], abs=0.05)
    bad, good = (np.array(band["env"][k]) for k in ("mistuned", "pure"))
    # after the attack the mistuned band rises again and again; the true one only falls
    rise = lambda e: float(max(e[i + 10] - e[i] for i in range(10, 290)))
    assert rise(bad) > 0.2 and rise(good) < 0.02


def test_every_listening_window_says_what_it_is():
    """With the sound off, the subtitles name each example: every window passes its words to the cue sheet."""
    import re
    from pathlib import Path

    from explainer.music.sound import plain

    here = Path(compute.__file__).parent
    for module, _, _ in SCENES:
        src = (here / f"{module}.py").read_text()
        assert not re.search(r"window\(snd\)", src), f"{module}: a listening window without a caption"
        assert src.count("self.listen(") <= src.count("window(snd"), f"{module}: a window without its strip"
    assert plain(r"lower, \ upper, \ both") == "lower, upper, both"
    assert plain(r"plucked at $\tfrac{1}{5}$") == "plucked at 1/5"
    assert plain(r"\textbf{A}, \ then B") == "A, then B"


def test_the_ear_thread():
    """Three to six pause-and-listen questions in a part (SYLLABUS section 1)."""
    from pathlib import Path

    here = Path(compute.__file__).parent
    asked = sum((here / f"{module}.py").read_text().count("listen_card(") for module, _, _ in SCENES)
    assert 3 <= asked <= 6, asked


def test_real_strings_and_the_frontier():
    r = load("real")
    assert r["decay_worst_rel"] < 0.02
    n = load("nonlinear")
    hard = n["runs"]["hard"]
    assert hard["tension_start"] == pytest.approx(hard["static_formula"], rel=5e-3)
    assert hard["start_cents"] > hard["estimate_cents"][0] > 40          # the estimate is a lower one
    assert abs(n["runs"]["soft"]["start_cents"]) < 2
    assert n["energy_drift"] < 1e-12
    assert n["third_mode"]["stretching"] < 1e-10                           # the missing mode stays missing


def test_variation_one():
    t = load("tune")
    assert len(t["notes"]) == 42 and t["worst_cents"] < 1.0
    assert load("variation")["part"] == 1


def test_every_clip_keeps_the_rules():
    """Labelled, under the peak ceiling, and at one loudness."""
    names = sorted(p.stem for p in compute.CLIPS.dir.glob("*.json"))
    assert len(names) >= 30
    for name in names:
        c = compute.CLIPS.load(name)
        assert c.meta.get("label") in ("physical model", "synthesized"), name
        assert true_peak_db(c) <= -1.5, (name, true_peak_db(c))
        assert -24.0 <= momentary_max(c) <= -15.0, (name, momentary_max(c))
        assert all(0 <= t <= c.duration + 1e-6 for t in c.events.values()), name


def test_scenes_and_clips_agree():
    """Every clip a scene asks for exists, and every stored clip is used."""
    import re
    from pathlib import Path

    here = Path(compute.__file__).parent
    asked = set()
    for module, _, _ in SCENES:
        src = (here / f"{module}.py").read_text()
        asked |= set(re.findall(r'clip\("([a-z_0-9]+\.[a-z_0-9]+)"\)', src))
        for item, sub in re.findall(r'clip\(f"([a-z_0-9]+)\.\{?([a-z_{}0-9]*)', src):
            asked |= {n for n in (p.stem for p in compute.CLIPS.dir.glob(f"{item}.*.json")) if n.startswith(item + ".")}
    stored = {p.stem for p in compute.CLIPS.dir.glob("*.json")}
    assert asked <= stored, sorted(asked - stored)
    assert stored <= asked, sorted(stored - asked)

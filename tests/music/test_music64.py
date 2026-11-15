"""Part 64 of *Music, Built*: what the film says is what was computed, and every sound keeps the series' rules.

    python -m pytest -q tests/music/test_music64.py
"""

import pytest

from tests.music.partcheck import check_clips, check_ear_thread, check_scenes_and_clips, check_windows
from videos.music.music64 import compute
from videos.music.music64.manifest import SCENES
from videos.music.variations import LEDGER

load = compute.load


def test_stereo_ica_and_median_filtering():
    p = load("pan")
    assert p["side_level_db"] < -6 and p["sdr_piano"] > 0
    i = load("ica")
    assert min(i["dry"].values()) > 0.999 and max(i["room"].values()) < 0.3
    k = load("icascatter")
    assert k["kurt_sources"]["vocals"] > max(k["kurt_mixes"]) and abs(k["kurt_gauss"]) < 0.05
    assert max(k["kurtosis"]) == pytest.approx(k["kurt_sources"]["vocals"], abs=0.05)      # the peak direction is the voice
    h = load("hpss")
    assert h["sdr_tonal"] > h["sdr_drums"]
    sw = load("hpsssweep")["power"]["2"]
    assert sw["tonal"][-1] > sw["tonal"][0] and sw["drums"][-1] > sw["drums"][0]


def test_masks_and_their_bounds():
    n, o = load("nmf")["sdr"], load("oracle")["sdr"]
    for k in ("vocals", "bass", "other"):
        assert o["irm"][k] > o["ibm"][k]
    assert o["ibm"]["drums"] > o["irm"]["drums"]                                        # said in Chapter 6
    for k in n:
        assert o["true_phase"][k] > o["irm"][k]
    assert 0 < o["irm"]["vocals"] - n["vocals"] < 2.5
    r = load("nmfrank")
    assert r["vocals"][0] < r["vocals"][2] and r["vocals"][-1] - r["vocals"][2] < 0.5     # gains flatten


def test_phase_networks_and_metrics():
    ph = load("phase")["sdr"]
    assert ph["mixture_phase"] > 5 and ph["griffin_lim"] < 0
    g = load("glcurve")
    assert g["inconsistency_db"][-1] < g["inconsistency_db"][0] - 10 and max(g["sdr"]) < 0
    net, leak, nmf = load("net")["sdr"], load("netleak"), load("nmf")["sdr"]["vocals"]
    assert leak["honest"] == pytest.approx(net) and leak["sdr"] > nmf > net                 # honest: below NMF; leaked: above
    m = load("metrics")
    assert m["sdr_leak"] == pytest.approx(m["sdr_artifacts"], abs=0.01)
    rows = load("gain")["rows"]
    assert rows["half as loud"]["si_sdr"] > 100 and rows["1 ms late"]["sdr"] < 0 < rows["dull (2 kHz low-pass)"]["sdr"] - 20
    rm = load("remix")
    assert rm["sdr_remix"] > rm["sdr_mix"] + 3


def test_variation_64():
    v = load("variation")
    row = [r for r in LEDGER if r["part"] == 64][0]
    assert v["part"] == 64 and row["measure"] == v["measure"] and row["seconds"] == pytest.approx(v["seconds"], abs=0.05)


def test_the_part_keeps_the_series_rules():
    check_clips(compute)
    check_scenes_and_clips(compute, SCENES)
    check_windows(compute, SCENES)
    check_ear_thread(compute, SCENES)

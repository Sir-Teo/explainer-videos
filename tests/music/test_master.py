"""Monochord's mastering bench (Part 57): K-weighting, gating, true peak, the limiter, normalization, dither and the
RIAA curve.  The meter itself is checked against ffmpeg's ebur128 here too.

    python -m pytest -q tests/music/test_master.py
"""

import math
import shutil
import subprocess
import tempfile
from pathlib import Path

import numpy as np
import pytest

from explainer.music.monochord import Clip
from explainer.music.monochord import master as M

SR = 48000


def test_k_weighting():
    k = M.k_response(np.array([20.0, 1000.0, 10000.0]))
    assert k[0] < -10 and abs(k[1]) < 1.0 and k[2] == pytest.approx(4.0, abs=0.2)


def test_reference_tone():
    t = np.arange(10 * SR) / SR
    y = np.sin(2 * np.pi * 997 * t)
    assert M.lufs(np.stack([y, np.zeros_like(y)], axis=1)) == pytest.approx(-3.01, abs=0.05)


def test_gates():
    rng = np.random.default_rng(0)
    loud = 0.1 * rng.standard_normal((8 * SR, 2))
    quiet = 0.003 * rng.standard_normal((8 * SR, 2))
    y = np.r_[np.zeros((3 * SR, 2)), quiet, loud]
    b = M.blocks(y)
    assert b["integrated"] == pytest.approx(M.lufs(loud), abs=0.3)
    assert b["ungated"] < b["integrated"] - 1.0 and b["rel_gate"] == pytest.approx(b["ungated"] - 10.0)


def test_true_peak():
    n = np.arange(4 * SR)
    s = np.sin(2 * np.pi * n / 4 + math.pi / 4)
    s = s / np.max(np.abs(s))
    assert M.sample_peak_db(s) == pytest.approx(0.0, abs=1e-9)
    assert M.true_peak_db(s) == pytest.approx(3.01, abs=0.2)


def test_limiter_holds_the_ceiling():
    rng = np.random.default_rng(1)
    y = 1.5 * rng.standard_normal((2 * SR, 2)) * np.linspace(0.1, 1, 2 * SR)[:, None]
    r = M.limiter(y, -1.0)
    assert M.true_peak_db(r["y"]) <= -0.95 and np.max(np.abs(r["y"])) <= 10 ** (-1 / 20) + 1e-9
    quiet = 0.1 * rng.standard_normal((SR, 2))
    assert np.allclose(M.limiter(quiet, -1.0)["y"], quiet)      # below the ceiling it does nothing


def test_master_reaches_its_target():
    rng = np.random.default_rng(2)
    y = 0.05 * rng.standard_normal((4 * SR, 2))
    r = M.master(y, -14.0)
    assert r["lufs"] == pytest.approx(-14.0, abs=0.1) and r["true_peak"] <= -0.95


def test_normalize():
    rng = np.random.default_rng(3)
    y = 0.3 * rng.standard_normal((3 * SR, 2))
    r = M.normalize(y, -14.0)
    assert M.lufs(r["y"]) == pytest.approx(-14.0, abs=0.05) or r["gain_db"] == 0.0
    q = 0.001 * rng.standard_normal((3 * SR, 2))
    assert M.normalize(q, -14.0)["gain_db"] == 0.0
    up = M.normalize(q, -14.0, allow_up=True)
    assert up["gain_db"] > 0 and M.true_peak_db(up["y"]) <= -0.99


def test_dither_decorrelates():
    t = np.arange(SR) / SR
    x = 1.3 * 2 ** -7 * np.sin(2 * np.pi * 441 * t)               # under two steps tall at 8 bits
    r = M.quantize(x, 8) - x
    d = M.tpdf_dither(x, 8, np.random.default_rng(4)) - x
    spec = lambda e: np.abs(np.fft.rfft(e)) ** 2                    # noqa: E731
    h3 = 3 * 441
    ratio_r = spec(r)[h3] / np.median(spec(r))
    ratio_d = spec(d)[h3] / np.median(spec(d))
    assert ratio_r > 1000 and ratio_d < 50                          # rounding makes a third harmonic; dither does not
    s = M.shaped(x[:SR // 4], 8, np.random.default_rng(5)) - x[:SR // 4]
    S = np.abs(np.fft.rfft(s)) ** 2
    f = np.fft.rfftfreq(len(s), 1 / SR)
    assert S[(f > 15000)].mean() > 10 * S[(f > 500) & (f < 3000)].mean()


def test_riaa():
    assert M.riaa_db(np.array([1000.0]))[0] == pytest.approx(0.0, abs=1e-9)
    assert M.riaa_db(np.array([20.0]))[0] == pytest.approx(19.27, abs=0.05)
    assert M.riaa_db(np.array([20000.0]))[0] == pytest.approx(-19.62, abs=0.05)
    from scipy.signal import freqz
    (bp, ap), (bc, ac) = M.riaa_filters()
    w, h1 = freqz(bp, ap, worN=[2 * np.pi * 300 / SR])
    _, h2 = freqz(bc, ac, worN=[2 * np.pi * 300 / SR])
    assert abs(h1[0] * h2[0]) == pytest.approx(1.0, abs=1e-9)


@pytest.mark.skipif(shutil.which("ffmpeg") is None, reason="ffmpeg is not installed")
def test_meter_agrees_with_ffmpeg():
    rng = np.random.default_rng(6)
    y = 0.08 * rng.standard_normal((6 * SR, 2)) * (1 + np.sin(np.arange(6 * SR) / SR * 2)[:, None])
    with tempfile.TemporaryDirectory() as d:
        p = Path(d) / "x.wav"
        Clip(y, SR).write(p)
        err = subprocess.run(["ffmpeg", "-nostats", "-i", str(p), "-af", "ebur128=peak=true", "-f", "null", "-"], text=True, capture_output=True).stderr
    import re
    s = err[err.rindex("Summary:"):]
    assert M.lufs(y) == pytest.approx(float(re.search(r"I:\s+(-?[\d.]+) LUFS", s).group(1)), abs=0.1)
    assert M.true_peak_db(y) == pytest.approx(float(re.search(r"Peak:\s+(-?[\d.]+) dBFS", s).group(1)), abs=0.15)

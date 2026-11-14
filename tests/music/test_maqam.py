"""Monochord's maqam engine (Part 35)."""

import numpy as np

from explainer.music.monochord import maqam as Q


def test_ajnas_and_maqamat():
    assert Q.AJNAS["Rast"] == [0, 200, 350, 500] and Q.AJNAS["Hijaz"] == [0, 100, 400, 500]
    assert Q.maqam_scale("Rast") == [0, 200, 350, 500, 700, 900, 1050, 1200]
    assert Q.maqam_scale("Bayati") == [0, 150, 300, 500, 700, 800, 1000, 1200]
    assert 1200 not in Q.maqam_scale("Saba")
    for k in Q.MAQAMAT:
        sc = Q.maqam_scale(k)
        assert sc == sorted(sc) and sc[0] == 0


def test_ratios_and_grids():
    r = Q.farabi_ratios()
    assert abs(r["Zalzal's neutral third 27/22"] - 354.55) < 0.01
    s17 = Q.safi_17()
    steps = np.diff(s17 + [1200.0])
    assert len(s17) == 17 and set(np.round(steps, 0)) <= {90.0, 23.0, 24.0}
    assert Q.edo_error(350, 24) == (7, 0.0)
    k, e = Q.edo_error(1200 * np.log2(1.5), 53)
    assert k == 31 and abs(e) < 0.1
    tr = Q.turkish_rast()
    assert tr["commas"][-1] == 53 and tr["commas"][2] == 17


def test_sounds():
    for hz in (196.0, 261.63 * 2 ** (3.5 / 12)):
        y = Q.oud(hz, 1.2)
        n = len(y)
        f = np.abs(np.fft.rfft(y * np.hanning(n), 8 * n))
        fr = np.fft.rfftfreq(8 * n, 1 / 48000)
        m = (fr > hz * 0.9) & (fr < hz * 1.1)
        peak = fr[np.argmax(f * m)]
        assert abs(1200 * np.log2(peak / hz)) < 2.0                              # within two cents
    for s in ("dum", "tek", "ka"):
        assert abs(np.abs(Q.darbuka(s)).max() - 1) < 1e-9
    assert all(len(v["strokes"]) == v["beats"] for v in Q.IQAAT.values())

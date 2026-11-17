import numpy as np
import pytest

from explainer.psychology.psyche import hearing as H


def test_decibels_and_the_threshold_in_quiet():
    assert H.db_spl(H.P_REF) == pytest.approx(0.0)
    assert H.db_spl(10 * H.P_REF) == pytest.approx(20.0)
    assert H.pressure(120) / H.pressure(0) == pytest.approx(1e6)
    f = np.geomspace(20, 16000, 2000)
    t = H.threshold_in_quiet(f)
    assert 2500 < f[np.argmin(t)] < 4500  # most sensitive where the ear canal resonates
    assert H.threshold_in_quiet(50.0) > H.threshold_in_quiet(1000.0) + 30


def test_place_map_and_bandwidths():
    assert H.greenwood(0.0) == pytest.approx(19.85, rel=0.01)
    assert 18000 < H.greenwood(1.0) < 22000
    assert H.greenwood(H.greenwood_place(1000.0)) == pytest.approx(1000.0)
    assert H.erb(1000) == pytest.approx(132.6, rel=0.01)
    cfs = H.erb_space(100, 8000, 30)
    assert np.allclose(np.diff(H.erb_rate(cfs)), np.diff(H.erb_rate(cfs))[0])
    # a tone excites the channel tuned to it most
    ex = H.excitation(H.tone(1000, 0.1), cfs)
    assert abs(cfs[np.argmax(ex)] - 1000) < H.erb(1000)


@pytest.mark.parametrize("f0,harmonics,seed", [(200, range(1, 7), None), (200, range(3, 7), None),
                                               (250, [3, 4, 5], 3), (150, range(5, 9), 1)])
def test_autocorrelation_hears_the_missing_fundamental(f0, harmonics, seed):
    x = H.harmonic_complex(f0, harmonics, 0.2, seed=seed)
    assert H.pitch(x) == pytest.approx(f0, rel=0.02)


def test_masking_flattens_beyond_one_filter():
    w = H.erb(2000)
    assert H.masked_threshold(2000, w / 4) < H.masked_threshold(2000, w / 2) < H.masked_threshold(2000, w)
    assert H.masked_threshold(2000, 4 * w) == pytest.approx(H.masked_threshold(2000, w))


def test_interaural_delay_and_a_jeffress_array():
    assert H.itd(0.0) == pytest.approx(0.0)
    assert 600e-6 < H.itd(90.0) < 700e-6
    assert H.azimuth_from_itd(float(H.itd(30.0))) == pytest.approx(30.0, abs=0.01)
    rng = np.random.default_rng(4)
    true = float(H.itd(30.0))
    L = H.phase_locked_spikes(500, 0.0, 3.0, rng, rate=0.5)
    R = H.phase_locked_spikes(500, true, 3.0, rng, rate=0.5)
    delays = np.arange(-700, 701, 25) * 1e-6
    best = delays[np.argmax(H.jeffress(L, R, delays))]
    assert abs(best - true) <= 50e-6


def test_labels_predict_a_discrimination_peak_and_mcgurk_fuses():
    steps = np.arange(1, 15)
    p = H.identification(steps, 7.5, 0.6)
    abx = H.abx_from_labels(p[:-2], p[2:])
    assert abx.min() == pytest.approx(0.5, abs=0.01) and abx.max() > 0.65
    assert 5 <= np.argmax(abx) + 1 <= 7  # the peak straddles the boundary
    shares = H.mcgurk(0.0, 2.0, 0.45, 0.45, n=20000, rng=np.random.default_rng(1))
    assert shares[1] > 0.8  # equal reliabilities: the fused /d/
    voice = H.mcgurk(0.0, 2.0, 0.3, 3.0, n=20000, rng=np.random.default_rng(1))
    assert voice[0] > 0.6  # an untrusted face: the voice wins


def test_the_gate_and_the_fragile_count():
    assert H.gate(0.0, 1.0) == pytest.approx(1.0)
    assert H.gate(1.2, 1.0) < 0.5 * H.gate(0.0, 1.0)  # rubbing helps
    assert H.gate(1.2, 0.0) < 0.1  # touch alone is not pain
    counts = [H.bushdid_estimate(128, 30, t) for t in (0.4, 0.6, 0.8)]
    assert counts[0] < 100 < 1e6 < counts[1] < 1e7 < 1e14 < counts[2]

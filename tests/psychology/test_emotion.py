"""Psyche's emotion module (Part 29), and the R reader's compact (ALTREP) vectors."""
from __future__ import annotations

import struct

import numpy as np
import pytest

from explainer.psychology import rdata
from explainer.psychology.psyche import emotion as E


def test_classical_mds_recovers_a_euclidean_configuration():
    rng = np.random.default_rng(1)
    X = rng.normal(size=(12, 2))
    D = np.linalg.norm(X[:, None] - X[None], axis=2)
    m = E.classical_mds(D)
    assert m["share"] == pytest.approx(1.0, abs=1e-9)
    pr = E.procrustes(m["X"], X - X.mean(0))
    assert pr["r"] == pytest.approx(1.0, abs=1e-9)
    # distances are preserved exactly
    Dm = np.linalg.norm(m["X"][:, None] - m["X"][None], axis=2)
    assert np.allclose(Dm, D, atol=1e-9)


def test_procrustes_undoes_a_rotation_and_a_reflection():
    rng = np.random.default_rng(2)
    Y = rng.normal(size=(10, 2))
    Y -= Y.mean(0)
    th = 0.7
    R = np.array([[np.cos(th), -np.sin(th)], [np.sin(th), np.cos(th)]]) @ np.diag([1, -1])
    pr = E.procrustes(Y @ R, Y)
    assert np.allclose(pr["Z"], Y, atol=1e-9)


def test_fit_scale_finds_the_direction_of_a_linear_rating():
    rng = np.random.default_rng(3)
    X = rng.normal(size=(40, 2))
    y = 2 * X[:, 0] - X[:, 1] + 0.5
    f = E.fit_scale(X, y)
    assert f["R"] == pytest.approx(1.0, abs=1e-9)
    assert np.allclose(f["direction"], np.array([2, -1]) / np.sqrt(5), atol=1e-9)


def test_pairs_map_improves_with_repetitions():
    r = [E.pairs_map(n_reps=k, seed=29)["r"] for k in (1, 10)]
    assert r[1] > r[0] > 0.5
    assert r[1] > 0.95


def test_attribution_is_a_truncated_normal_posterior():
    a, c, m, sd = 1.2, 0.3, 0.3, 0.5
    got = E.attribution(arousal=a, explanation=c, prior_situation=m, spread=sd)["mean"]
    mu = a - c - sd ** 2 / m
    from scipy.stats import truncnorm
    want = truncnorm.mean((0 - mu) / sd, (3 - mu) / sd, loc=mu, scale=sd)
    assert got == pytest.approx(want, abs=2e-3)
    # an explanation takes arousal away from the situation
    assert E.attribution(1.2, 1.0)["mean"] < E.attribution(1.2, 0.0)["mean"]


def test_appraisal_labels_its_own_prototypes():
    for name, code in E.PROTOTYPES.items():
        assert E.appraise(code)["labels"][0] == name
    p = E.appraise(E.PROTOTYPES["anger"])["p"]
    assert p.sum() == pytest.approx(1.0) and np.all(np.diff(p) <= 0)


def test_two_roads():
    snake, stick = E.two_roads("snake"), E.two_roads("stick")
    none = E.two_roads("snake", amygdala=False)
    assert snake["peak_early"] == pytest.approx(stick["peak_early"])
    assert snake["peak_early"] > 0.4
    assert snake["late"] == pytest.approx(1.4, abs=1e-3)
    assert stick["late"] < 1e-6 and none["late"] == 0 and none["peak_early"] == 0


def test_forecast_overstates_duration_not_impact():
    f = E.forecast(impact=3.0, tau_actual=20.0, tau_predicted=150.0, at=60.0)
    assert f["actual"][0] == pytest.approx(f["predicted"][0])
    assert f["actual_at"] == pytest.approx(3 * np.exp(-3), rel=1e-3)
    assert f["predicted_at"] == pytest.approx(3 * np.exp(-60 / 150), rel=1e-3)


def test_income_world_hides_a_plateau_in_the_average():
    w = E.income_world()
    x = np.log2(np.asarray(w["income"]))
    mean, p10 = np.asarray(w["mean"]), np.asarray(w["p10"])
    hi = x > np.log2(120_000)
    lo = (x > np.log2(25_000)) & (x < np.log2(90_000))
    assert np.polyfit(x[hi], mean[hi], 1)[0] > 0.2
    assert abs(np.polyfit(x[hi], p10[hi], 1)[0]) < 0.08 < 0.2 < np.polyfit(x[lo], p10[lo], 1)[0]


def test_lorenz_stays_on_the_attractor():
    L = E.lorenz(T=20.0)
    assert np.isfinite(L).all()
    assert L[:, 2].max() < 55 and L[:, 0].min() < -10 < 10 < L[:, 0].max()


# ----------------------------------------------------------------------------- the R reader's ALTREP vectors
def _sym(name: str) -> bytes:
    raw = name.encode()
    return struct.pack(">ii", 1, 9 | (1 << 12)) + struct.pack(">i", len(raw)) + raw


def _altrep(cls: str, state: bytes) -> bytes:
    info = (struct.pack(">i", 2) + _sym(cls) + struct.pack(">i", 2) + _sym("base") + struct.pack(">i", 2)
            + struct.pack(">iii", 13, 1, 13) + struct.pack(">i", 254))
    return struct.pack(">i", 238) + info + state + struct.pack(">i", 254)


def test_rdata_expands_compact_sequences():
    state = struct.pack(">ii", 14, 3) + struct.pack(">3d", 5.0, 1.0, 1.0)
    obj = rdata.Reader(_altrep("compact_intseq", state)).item()
    assert obj["type"] == rdata.INTSXP and obj["value"] == [1, 2, 3, 4, 5]
    state = struct.pack(">ii", 14, 3) + struct.pack(">3d", 3.0, 0.5, 2.0)
    obj = rdata.Reader(_altrep("compact_realseq", state)).item()
    assert obj["type"] == rdata.REALSXP and obj["value"] == [0.5, 2.5, 4.5]


def test_rdata_refuses_other_altrep_classes():
    state = struct.pack(">ii", 14, 1) + struct.pack(">d", 1.0)
    with pytest.raises(ValueError, match="unsupported ALTREP"):
        rdata.Reader(_altrep("mmap_real", state)).item()

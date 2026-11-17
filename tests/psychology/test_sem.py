"""Psyche's latent-variable models (Part 44), checked against lavaan's published results."""

import numpy as np
import pytest

from explainer.psychology.psyche import sem as E

P3 = np.zeros((9, 3), int)
P3[0:3, 0] = 1
P3[3:6, 1] = 1
P3[6:9, 2] = 1


@pytest.fixture(scope="module")
def hs():
    from explainer.psychology import opendata
    try:
        return opendata.holzinger_1939()
    except Exception as exc:  # the data are fetched on first use
        pytest.skip(f"Holzinger-Swineford data unavailable: {exc}")


def test_three_factor_model_matches_lavaan(hs):
    X = hs["X"]
    r = E.fit_cfa(np.cov(X.T, bias=True), len(X), P3)
    assert abs(r["T"] - 85.306) < 0.01 and r["df"] == 24
    assert abs(r["cfi"] - 0.931) < 0.001 and abs(r["tli"] - 0.896) < 0.001 and abs(r["rmsea"] - 0.092) < 0.001
    assert abs(r["T0"] - 918.852) < 0.01
    assert np.allclose(r["L"][[1, 2, 4, 5, 7, 8], [0, 0, 1, 1, 2, 2]], [0.553, 0.729, 1.113, 0.926, 1.180, 1.082],
                       atol=0.002)


def test_invariance_ladder_matches_lavaan(hs):
    X, sch = hs["X"], np.array(hs["school"])
    gs = [X[sch == "Pasteur"], X[sch == "Grant-White"]]
    want = {"configural": (115.851, 48), "metric": (124.044, 54), "scalar": (164.103, 60)}
    for lev, (T, df) in want.items():
        r = E.fit_multigroup(gs, P3, lev)
        assert abs(r["T"] - T) < 0.02 and r["df"] == df


def test_path_tracing():
    a, b = 0.5, 0.6
    R = E.markov_equivalent(a, b)
    assert abs(R["chain"][0, 2] - a * b) < 1e-12
    assert np.allclose(R["chain"], R["fork"]) and np.allclose(R["chain"], R["reverse"])
    assert abs(R["collider"][0, 2]) < 1e-12


def test_factor_and_network_imply_the_same_matrix():
    f = E.factor_as_network([0.8, 0.7, 0.6, 0.5])
    assert np.allclose(f["R"], f["reproduced"]) and np.all(f["partial"][np.triu_indices(4, 1)] > 0)


def test_confounded_mediator_shows_an_indirect_effect_that_is_not_there():
    m = E.mediation(seed=0)
    assert m["true"] == 0 and m["lo"] > 0

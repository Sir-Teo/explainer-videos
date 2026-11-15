"""Psyche's concepts module, Part 22: exemplar and prototype models, the six problems and ALCOVE, scaling,
Shepard's law and consequential regions, the contrast model and Tversky's count, category utility, the number game,
spreading activation, word vectors and RSA; and the R data reader on the open CRAN data."""

import numpy as np
import pytest

from explainer.psychology import opendata
from explainer.psychology.psyche import concepts as K

FIVE_FOUR_A = np.array([[1, 1, 1, 0], [1, 0, 1, 0], [1, 0, 1, 1], [1, 1, 0, 1], [0, 1, 1, 1]], float)
FIVE_FOUR_B = np.array([[1, 1, 0, 0], [0, 1, 1, 0], [0, 0, 0, 1], [0, 0, 0, 0]], float)


def test_gcm_and_prototype_disagree_on_the_5_4_structure():
    ex = np.r_[FIVE_FOUR_A, FIVE_FOUR_B]
    lab = np.r_[np.zeros(5, int), np.ones(4, int)]
    pg = K.gcm_prob(ex, ex, lab, c=3.0)[:, 0]
    pp = K.prototype_prob(ex, ex, lab, c=3.0)[:, 0]
    assert pg[0] < pg[1]  # exemplars: A2 easier than A1, as people found
    assert pp[0] > pp[1]  # the prototype says the reverse
    assert np.all((pg > 0) & (pg < 1))


def test_one_exemplar_per_category_is_a_prototype_model():
    rng = np.random.default_rng(0)
    x = rng.random((20, 3))
    means = np.array([[0.2, 0.3, 0.4], [0.7, 0.6, 0.5]])
    p1 = K.gcm_prob(x, means, np.array([0, 1]), c=2.0)
    ex = np.r_[rng.normal(means[0], 0.1, (6, 3)), rng.normal(means[1], 0.1, (6, 3))]
    lab = np.r_[np.zeros(6, int), np.ones(6, int)]
    centred = np.r_[ex[:6] - ex[:6].mean(0) + means[0], ex[6:] - ex[6:].mean(0) + means[1]]
    p2 = K.prototype_prob(x, centred, lab, c=2.0)
    assert np.allclose(p1, p2)


def test_shj_structures():
    chk = K.shj_check()
    assert all(chk.values())
    for t, lab in K.SHJ_TYPES.items():
        assert sum(lab) == 4, t


def test_alcove_orders_the_extremes_and_learns_attention():
    rng = np.random.default_rng(1)
    err = {t: K.alcove(K.SHJ_TYPES[t], c=6.5, phi=2.0, lw=0.1, la=0.3, orders=8, rng=rng).mean() for t in (1, 6)}
    assert err[1] < err[6]
    att = K.alcove_attention(K.SHJ_TYPES[1], 6.5, 2.0, 0.1, 0.3, orders=8, rng=np.random.default_rng(2))
    assert att[0] > att[1] and att[0] > att[2]  # Type I: only the first dimension matters


def test_classical_mds_recovers_a_configuration():
    rng = np.random.default_rng(3)
    X = rng.normal(size=(10, 2))
    D = np.sqrt(((X[:, None] - X[None]) ** 2).sum(-1))
    Y, _ = K.classical_mds(D, 2)
    DY = np.sqrt(((Y[:, None] - Y[None]) ** 2).sum(-1))
    assert np.allclose(D, DY, atol=1e-8)
    assert K.stress(D, Y) < 1e-8


def test_nonmetric_mds_needs_only_the_order():
    rng = np.random.default_rng(4)
    X = rng.normal(size=(12, 2))
    D = np.sqrt(((X[:, None] - X[None]) ** 2).sum(-1))
    r = K.nonmetric_mds(np.exp(D) - 1, 2, rng=np.random.default_rng(5))  # a monotone distortion
    assert r["stress"] < 0.05


def test_shepard_generalization_measure():
    P = np.array([[0.9, 0.3], [0.1, 0.8]])
    G = K.shepard_generalization(P)
    assert np.allclose(np.diag(G), 1.0)
    assert G[0, 1] == pytest.approx(np.sqrt(0.3 * 0.1 / (0.9 * 0.8)))
    assert np.allclose(G, G.T)


def test_consequential_regions_give_the_exponential():
    d = np.linspace(0, 4, 17)
    s = np.linspace(1e-3, 40, 8000)
    g = K.consequential_region_gradient(d, s, s * np.exp(-s))
    assert np.allclose(g, np.exp(-d), atol=2e-3)
    L = 4.0
    u = K.consequential_region_gradient(d, s, (s < L).astype(float))
    dd = d[(d > 0) & (d < L)]
    assert np.allclose(u[(d > 0) & (d < L)], (L - dd - dd * np.log(L / dd)) / L, atol=5e-3)


def test_contrast_model_asymmetry_identity():
    A, B = {"a", "b", "c", "x"}, {"a", "b", "c", "y", "z", "w"}
    al, be = 0.8, 0.2
    diff = K.contrast_similarity(A, B, 1.0, al, be) - K.contrast_similarity(B, A, 1.0, al, be)
    assert diff == pytest.approx((be - al) * (len(A - B) - len(B - A)))
    assert K.contrast_similarity(A, B, 1.0, 0.5, 0.5) == pytest.approx(K.contrast_similarity(B, A, 1.0, 0.5, 0.5))


def test_prominence_asymmetry_counts():
    S = np.array([[100.0, 30.0, 20.0], [10.0, 100.0, 25.0], [10.0, 25.0, 100.0]])
    r = K.prominence_asymmetry(S, [1, 2, 2])  # 0 is the least prominent; 1 and 2 tie and drop out
    assert r["pairs"] == 2 and r["more"] == 2 and r["fewer"] == 0
    assert K.morse_duration(".-") == pytest.approx(0.25)


def test_polythetic_count_for_depression():
    assert K.polythetic_count(9, 5, 2) == 227


def test_category_utility_and_the_basic_level():
    U0 = K.level_utilities(*K.nested_world(f_super=0))
    U4 = K.level_utilities(*K.nested_world(f_super=4))
    assert U0.argmax() == 1  # loose superordinates: the basic level wins
    assert U4.argmax() == 0  # tight superordinates: the peak climbs
    F, labels = K.nested_world()
    assert K.category_utility(F, np.ones(len(F), bool)) == pytest.approx(0.0)


def test_number_game_size_principle():
    assert K.number_game([16, 8, 2, 64])["top"][0][0] == "powers of 2"
    r = K.number_game([16, 23, 19, 20])
    assert r["gen"][16] > 0.9 and r["gen"][31] < 0.2  # 17 in, 32 out
    a, b = K.number_game([60, 80, 10, 30])["top"][:2]
    assert {a[0], b[0]} == {"ending in 0", "multiples of 10"} and a[1] == pytest.approx(b[1])
    names, H, prior = K.number_game_hypotheses()
    assert prior.sum() == pytest.approx(1.0) and H.shape[1] == 100


def test_spreading_activation_fan():
    A = np.array([[0, 1, 1, 1], [1, 0, 0, 0], [1, 0, 0, 0], [1, 0, 0, 0]], float)
    h = K.spreading_activation(A, 0, steps=1, decay=0.5)
    assert h[1][1] == pytest.approx(0.5 / 3)  # divided among three links
    h2 = K.spreading_activation(A, 0, steps=1, decay=0.5, fan=False)
    assert h2[1][1] == pytest.approx(0.5)


def test_ppmi_vectors_and_neighbours():
    tokens = ("the cat sat on the mat the dog sat on the rug a cat and a dog ran " * 40).split()
    vocab = ["cat", "dog", "mat", "rug", "sat", "ran"]
    C = K.cooccurrence(tokens, vocab, window=2)
    assert np.allclose(C, C.T) and C.min() >= 0
    V = K.ppmi_svd(C, k=3)
    assert V.shape == (6, 3)
    assert K.neighbours(V, vocab, "cat", 1)[0][0] in ("dog", "mat", "rug", "sat", "ran")


def test_rsa_is_a_rank_correlation():
    rng = np.random.default_rng(6)
    X = rng.normal(size=(8, 2))
    D = np.sqrt(((X[:, None] - X[None]) ** 2).sum(-1))
    assert K.rsa(D, D ** 2) == pytest.approx(1.0)
    assert K.rsa(D, -D) == pytest.approx(-1.0)


def test_open_data_through_the_r_reader():
    if not (opendata.available("nosof94") and opendata.available("rothkopf_1957")):
        pytest.skip("the CRAN packages could not be fetched")
    err = opendata.nosof94()["error"]
    assert err.shape == (6, 16)
    m = err.mean(1)
    assert m[0] < m[1] < m[5] and m[0] == m.min() and m[5] == m.max()
    r = opendata.rothkopf_1957()
    assert r["same"].shape == (36, 36) and r["signals"][0] == ".-"
    a = K.prominence_asymmetry(100 * r["same"], [K.morse_duration(s) for s in r["signals"]])
    assert (a["pairs"], a["more"]) == (555, 336)  # Tversky (1977): 555 and 336
    e = opendata.ekman_1954()
    assert e["similarity"].shape == (14, 14) and e["nm"][0] == 434

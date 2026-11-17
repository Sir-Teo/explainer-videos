"""Lab 22: the generalized context model and the prototype model on the 5-4 structure; ALCOVE on the six problems of
Shepard, Hovland and Jenkins, with and without attention learning, against Nosofsky et al.'s (1994) open data;
non-metric scaling of Ekman's colours and Rothkopf's Morse code; Shepard's exponential law and its derivation from
consequential regions; Tversky's asymmetry count; category utility; the number game; spreading activation; and word
vectors from Jane Austen."""

import numpy as np

from videos.coursekit import labs
from explainer.psychology import opendata
from explainer.psychology.psyche import concepts as K

TITLE = "Concepts and categories"
GOAL = ("Fit exemplar, prototype and attention-learning models; turn confusions into a map; test Shepard's law and "
        "derive it; count Tversky's asymmetries; find the most useful level of a taxonomy; learn a concept from a few "
        "examples by Bayesian inference; and read meaning from the company words keep.")
TASKS = [
    "Refit ALCOVE to the six problems with `concepts.fit_alcove_shj`, with `attention=False` and then with "
    "attention learning (a few minutes each). Which problem's place changes most, and why does attention matter?",
    "In the number game, find a set of three examples after which the model generalizes to a range and to a "
    "mathematical rule about equally. What makes the tie?",
    "Rerun `concepts.prominence_asymmetry` on Rothkopf's table with prominence measured by the number of dashes. "
    "Is the asymmetry larger or smaller than with length?",
]


def run(seed=0):
    out = labs.Lab()
    rng = np.random.default_rng(seed)

    # 1. the 5-4 structure: exemplars against a prototype
    a = np.array([[1, 1, 1, 0], [1, 0, 1, 0], [1, 0, 1, 1], [1, 1, 0, 1], [0, 1, 1, 1]], float)
    b = np.array([[1, 1, 0, 0], [0, 1, 1, 0], [0, 0, 0, 1], [0, 0, 0, 0]], float)
    ex, lab_ = np.r_[a, b], np.r_[np.zeros(5, int), np.ones(4, int)]
    pg = K.gcm_prob(ex, ex, lab_, c=3.0)[:, 0]
    pp = K.prototype_prob(ex, ex, lab_, c=3.0)[:, 0]
    out.row("P(A) for A1 and A2: exemplar model; prototype model",
            f"{pg[0]:.2f}, {pg[1]:.2f}; {pp[0]:.2f}, {pp[1]:.2f}")
    assert pg[0] < pg[1] and pp[0] > pp[1]  # the models disagree, and people side with the exemplars

    # 2. the six problems
    ok = opendata.available("nosof94")
    if ok:
        obs = opendata.nosof94()["error"]
        # the parameters fitted in the film (concepts.fit_alcove_shj, 20 orders; refitting takes a couple of minutes)
        c, phi, lw, la = 7.774, 1.823, 0.178, 0.466
        pred = [float(K.alcove(K.SHJ_TYPES[t], c, phi, lw, la, orders=4, rng=rng).mean()) for t in range(1, 7)]
        out.row("mean error, Types I to VI: data", ", ".join(f"{obs[t].mean():.3f}" for t in range(6)))
        out.row("mean error, Types I to VI: ALCOVE at the film's fitted values", ", ".join(f"{v:.3f}" for v in pred))
        assert pred[0] < pred[1] < pred[5]
    else:
        out.row("the six problems", "Nosofsky et al.'s data could not be fetched")

    # 3. a map of colours
    if opendata.available("ekman_1954"):
        e = opendata.ekman_1954()
        r = K.nonmetric_mds(1 - e["similarity"], 2, rng=np.random.default_rng(1954))
        ang = np.unwrap(np.arctan2(*(r["X"] - r["X"].mean(0)).T[::-1]))
        out.row("Ekman's colours: stress; angular span of the circle (degrees)",
                f"{r['stress']:.3f}; {np.degrees(np.ptp(ang)):.0f}")
        assert r["stress"] < 0.1

    # 4. Shepard's law, tested and derived
    if opendata.available("rothkopf_1957"):
        m = opendata.rothkopf_1957()
        G = K.shepard_generalization(m["same"])
        r = K.nonmetric_mds(1 - G, 2, rng=np.random.default_rng(1957))
        D = np.sqrt(((r["X"][:, None] - r["X"][None]) ** 2).sum(-1))
        iu = np.triu_indices(36, 1)
        law = K.fit_exponential_law(D[iu] / D[iu].mean(), G[iu])
        out.row("Morse: stress; exponential law k and R^2 in log g", f"{r['stress']:.3f}; {law['k']:.2f}, "
                f"{law['r2_log']:.2f}")
        asy = K.prominence_asymmetry(100 * m["same"], [K.morse_duration(s) for s in m["signals"]])
        out.row("Tversky's count: pairs, shorter-first more, fewer, equal (1977: 555, 336, 181, 38)",
                f"{asy['pairs']}, {asy['more']}, {asy['fewer']}, {asy['ties']}")
        assert asy["more"] > asy["fewer"]
    d = np.linspace(0, 4, 9)
    s = np.linspace(1e-3, 40, 8000)
    g = K.consequential_region_gradient(d, s, s * np.exp(-s))
    out.row("consequential regions, sizes ~ s e^-s: g(d) at d = 0, 1, 2", ", ".join(f"{v:.3f}" for v in g[[0, 2, 4]]))
    assert np.allclose(g, np.exp(-d), atol=2e-3)

    # 5. the basic level
    U = K.level_utilities(*K.nested_world(f_super=0))
    out.row("category utility, superordinate, basic, subordinate (superordinates share nothing)",
            ", ".join(f"{v:.3f}" for v in U))
    assert U[1] == U.max()

    # 6. the number game
    for ex_ in ([16], [16, 8, 2, 64], [16, 23, 19, 20]):
        top = K.number_game(ex_)["top"][0]
        out.row(f"number game after {ex_}: best hypothesis", f"{top[0]} ({top[1]:.2f})")
    assert K.number_game([16, 8, 2, 64])["top"][0][0] == "powers of 2"

    # 7. spreading activation with a fan
    A = np.array([[0, 1, 1, 1], [1, 0, 0, 0], [1, 0, 0, 0], [1, 0, 0, 0]], float)
    h = K.spreading_activation(A, 1, steps=2)
    out.row("activation of a hub's other neighbours after two steps (fan of 3)", f"{h[-1][2]:.3f}")

    # 8. meaning from company
    if opendata.available("austen_emma"):
        import collections

        tokens = opendata.austen()
        cnt = collections.Counter(tokens)
        stop = set(K.STOPWORDS)
        vocab = [w for w, _ in cnt.most_common(2500) if w not in stop][:1500]
        V = K.ppmi_svd(K.cooccurrence(tokens, vocab, window=4), k=60)
        nb = [w for w, _ in K.neighbours(V, vocab, "letter", 5)]
        out.row("Austen: nearest neighbours of 'letter'", ", ".join(nb))
        assert any(w in nb for w in ("note", "letters", "written", "wrote"))

    out.note = ("The exemplar model gets the 5-4 structure's hard item right and the prototype model does not; "
                "attention learning orders the six problems; Ekman's colours lie on a circle; generalization in "
                "Rothkopf's map is exponential, and an Erlang prior on region size gives exactly e^-d; the shorter "
                "Morse signal heard first is called 'same' more often; the basic level wins when superordinates are "
                "loose; four powers of 2 are enough to pick out the rule; Austen's letters are written and read.")

    fig, ax = labs.figure(2, size=(11, 4.2))
    for ex_, col in (([16], labs.GOLD), ([16, 8, 2, 64], labs.BLUE), ([16, 23, 19, 20], "#5bd18b")):
        ax[0].plot(np.arange(1, 101), K.number_game(ex_)["gen"], color=col, lw=1.2, label=str(ex_))
    ax[0].set(title="The number game", xlabel="number", ylabel="P(in the concept)")
    ax[0].legend(fontsize=8)
    for name, p in (("s e^-s", s * np.exp(-s)), ("uniform to 4", (s < 4).astype(float)),
                    ("near 2", np.exp(-((s - 2) ** 2) / 0.5))):
        dd = np.linspace(0, 4, 81)
        ax[1].plot(dd, K.consequential_region_gradient(dd, s, p), lw=1.5, label=name)
    ax[1].set(title="Generalization from consequential regions", xlabel="distance", ylabel="generalization")
    ax[1].legend(fontsize=8)
    out.fig = fig
    return out

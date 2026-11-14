"""Lab 16: the Rescorla-Wagner rule on the classic designs and as gradient descent; its asymptote, the contingency;
Rescorla's (1968) ten groups; renewal and spontaneous recovery in a two-memory model of extinction; Mackintosh's and
Pearce and Hall's attention; the four schedules; and the matching law from melioration."""

import numpy as np

from videos.coursekit import labs
from explainer.psychology.psyche import conditioning as K

TITLE = "Conditioning: prediction errors, contingency, extinction and choice"
GOAL = ("Run the Rescorla-Wagner rule on acquisition, blocking, inhibition and overexpectation; check that it is "
        "gradient descent; solve its asymptote and see the contingency appear; reproduce the ordering of Rescorla's "
        "ten groups; extinguish in one context and test in another; let attention learn; read the signatures of the "
        "four schedules; and watch a meliorating chooser match.")
TASKS = [
    "Give the outcome a larger learning rate than its absence (beta = 1 and 0.5). Where does V_X settle when "
    "P(US | X) = P(US | no X) = 0.8, and when both are 0.2? Is the asymptote still the contingency?",
    "Change extinction_in_context so that a share of acquisition is bound to its context (problem 6 in the README) "
    "and find a share that makes ABA > ABC > AAB.",
    "Run concurrent with a changeover rule: after switching keys, no reward for the next 2 seconds. What does it do to "
    "the generalized matching sensitivity?",
]


def run(seed=0):
    out = labs.Lab()
    rng = np.random.default_rng(seed)

    # 1. the rule and its gradient
    v, x = rng.normal(size=3), np.array([1.0, 1.0, 0.0])
    eps = 1e-6
    num = np.array([((1 - x @ (v + eps * e)) ** 2 - (1 - x @ (v - eps * e)) ** 2) / (4 * eps) for e in np.eye(3)])
    assert np.allclose(K.rw_gradient(v, x, 1.0), num, atol=1e-6), "the rule is gradient descent"
    out.row("largest gap between the rule's gradient and a numerical one", f"{np.abs(K.rw_gradient(v, x, 1.0) - num).max():.1e}")
    _, Vb = K.rescorla_wagner(K.sequence([("A+", 30), ("AX+", 20)]))
    _, Vc = K.rescorla_wagner(K.sequence([("AX+", 20)]))
    out.row("blocking: V of the added cue, after pretraining and without", f"{Vb[-1, 1]:.3f}, {Vc[-1, 1]:.3f}")
    _, Vi = K.rescorla_wagner(K.sequence([("A+ AX-", 300)]))
    _, Vo = K.rescorla_wagner(K.sequence([("A+ B+", 80), ("AB+", 60)]))
    out.row("conditioned inhibitor X; overexpectation, A before and after the compound",
            f"{Vi[-1, 1]:.2f}; {Vo[80, 0]:.2f} -> {Vo[-1, 0]:.2f}")

    # 2. the asymptote is the contingency
    for p1, p0 in ((0.6, 0.2), (0.75, 0.75), (0.2, 0.6)):
        _, V = K.rw_asymptote([("CX", 0.3, p1), ("C", 0.7, p0)])
        assert abs(V[1] - (p1 - p0)) < 1e-9
        out.row(f"P(US|X) = {p1}, P(US|no X) = {p0}: asymptote of V_X and delta P", f"{V[1]:+.3f}, {p1 - p0:+.3f}")
    med = {g: np.median([K.rescorla_1968(*g, rng=np.random.default_rng(s)) for s in range(8)])
           for g in K.RESCORLA_1968_GROUPS}
    out.row("Rescorla 1968 on Psyche, suppression ratio: 0.4/0.4, 0.4/0.2, 0.4/0.1, 0.4/0",
            ", ".join(f"{float(K.suppression_ratio(med[g])):.2f}" for g in ((0.4, 0.4), (0.4, 0.2), (0.4, 0.1), (0.4, 0.0))))

    # 3. extinction bound to context
    ren = {d: K.renewal(d) for d in ("AAA", "ABA", "ABC", "AAB")}
    out.row("renewal: response at test in AAA, ABA, ABC, AAB", ", ".join(f"{v:.2f}" for v in ren.values()))
    probes, _ = K.extinction_in_context([("A", 1.0, 20), ("A", 0.0, 40), ("test", "A", 0.0), ("test", "A", 48.0)],
                                        tau=48.0)
    out.row("spontaneous recovery: at once, and 48 hours later", f"{probes[0]:.2f}, {probes[1]:.2f}")

    # 4. attention
    seq = K.sequence([("A+ B+ A+ B-", 160)])
    _, _, Am = K.mackintosh(seq)
    _, _, Ap = K.pearce_hall(seq)
    out.row("attention to A (reliable) and B (uncertain): Mackintosh; Pearce-Hall",
            f"{Am[-1, 0]:.2f}, {Am[-1, 1]:.2f}; {Ap[-1, 0]:.2f}, {Ap[-1, 1]:.2f}")

    # 5. schedules and choice
    rates = {}
    for kind, val in (("FR", 20), ("VR", 20), ("FI", 60), ("VI", 60)):
        r, _ = K.schedule(kind, val, duration=900.0, rng=np.random.default_rng(7))
        rates[kind] = len(r) / 15.0
    out.row("responses a minute on FR 20, VR 20, FI 60 s, VI 60 s", ", ".join(f"{v:.0f}" for v in rates.values()))
    Bs, Rs = [], []
    for k, (a, b) in enumerate(((15, 135), (30, 90), (45, 45), (90, 30), (135, 15))):
        B, R = K.concurrent(means=(float(a), float(b)), minutes=300, rng=np.random.default_rng(100 + k))
        Bs.append(B)
        Rs.append(R)
    sens, bias = K.generalized_matching(np.array(Bs), np.array(Rs))
    out.row("generalized matching: sensitivity a and bias log b", f"{sens:.2f}, {bias:+.2f}")
    out.note = ("The rule is gradient descent; it blocks, makes inhibitors and overexpects; with a context cue its "
                "asymptote is exactly delta P, which orders Rescorla's groups as the paper did. Extinction stored with "
                "its context returns elsewhere and with time. Mackintosh attends to the reliable cue, Pearce and Hall "
                "to the uncertain one. Ratio schedules give the highest rates, and a meliorating chooser matches.")

    fig, ax = labs.figure(2, size=(11, 4.2))
    x = np.arange(Vb.shape[0])
    ax[0].plot(x, Vb[:, 0], color=labs.PINK, lw=1.6, label="A (pretrained)")
    ax[0].plot(x, Vb[:, 1], color=labs.BLUE, lw=1.6, label="X, blocked")
    ax[0].plot(np.arange(30, 30 + Vc.shape[0]), Vc[:, 1], color=labs.GREEN, lw=1.6, label="X, control")
    ax[0].set(title="Blocking under Rescorla-Wagner", xlabel="trial", ylabel="V")
    ax[0].legend(fontsize=8)
    Bs, Rs = np.array(Bs), np.array(Rs)
    ax[1].scatter(Rs[:, 0] / Rs.sum(1), Bs[:, 0] / Bs.sum(1), color=labs.GREEN)
    ax[1].plot([0, 1], [0, 1], color=labs.GREY, lw=0.8)
    ax[1].set(title="Matching by melioration", xlabel="share of rewards on the left", ylabel="share of responses")
    out.fig = fig
    return out

"""Lab 44: latent variables: tracing rules, a confirmatory factor model fitted by maximum likelihood to Holzinger and
Swineford's nine tests, fit indices, invariance across two schools, attenuation, a confounded mediator, and
equivalent models."""

import numpy as np

from videos.coursekit import labs
from explainer.psychology import opendata
from explainer.psychology.psyche import sem as E

TITLE = "Latent Variables"
GOAL = ("Fit the three-factor model to Holzinger and Swineford's tests, judge its fit, test whether the two schools "
        "can be compared, then see three ways a well-fitting model can still mislead: attenuation, a confounded "
        "mediator, and diagrams that fit identically.")
TASKS = [
    "Free the loading of x9 on the visual factor. How much does χ² fall, for one degree of freedom, and what happens "
    "to the RMSEA?",
    "Raise the confounding in the mediation simulator to 0 and to 1.0. How does the indirect effect's interval move?",
    "Make the traits in the attenuation simulation correlate 0.8 with loadings 0.4. How far are the sum scores off?",
]

P3 = np.zeros((9, 3), int)
P3[0:3, 0] = 1
P3[3:6, 1] = 1
P3[6:9, 2] = 1


def run(seed=0):
    out = labs.Lab()

    out.row("tracing rule: X -> M (0.5) -> Y (0.6) gives r(X, Y)", f"{0.5 * 0.6:.2f}")

    h = opendata.holzinger_1939()
    X = h["X"]
    n = len(X)
    S = np.cov(X.T, bias=True)
    r3 = E.fit_cfa(S, n, P3)
    r1 = E.fit_cfa(S, n, np.ones((9, 1), int))
    out.row("three factors: chi2 / df; CFI; TLI; RMSEA; SRMR",
            f"{r3['T']:.2f} / {r3['df']}; {r3['cfi']:.3f}; {r3['tli']:.3f}; {r3['rmsea']:.3f}; {r3['srmr']:.3f}")
    assert abs(r3["T"] - 85.306) < 0.05 and r3["df"] == 24
    out.row("one factor: chi2 / df; CFI; RMSEA", f"{r1['T']:.1f} / {r1['df']}; {r1['cfi']:.3f}; {r1['rmsea']:.3f}")

    sch = np.array(h["school"])
    gs = [X[sch == "Pasteur"], X[sch == "Grant-White"]]
    inv = {lev: E.fit_multigroup(gs, P3, lev) for lev in ("configural", "metric", "scalar")}
    out.row("invariance: chi2 (df) configural; metric; scalar",
            "; ".join(f"{inv[k]['T']:.2f} ({inv[k]['df']})" for k in ("configural", "metric", "scalar")))
    from scipy import stats
    dm = inv["metric"]["T"] - inv["configural"]["T"]
    ds = inv["scalar"]["T"] - inv["metric"]["T"]
    out.row("loadings equal: delta chi2 on 6 df, p; intercepts equal: delta chi2, p",
            f"{dm:.2f}, {stats.chi2.sf(dm, 6):.2f}; {ds:.2f}, {stats.chi2.sf(ds, 6):.1e}")

    rng = np.random.default_rng(seed + 44)
    m = 500
    F = rng.multivariate_normal([0, 0], [[1, 0.5], [0.5, 1]], m)
    Xs = np.column_stack([0.6 * F[:, j // 3] + 0.8 * rng.normal(0, 1, m) for j in range(6)])
    P2 = np.zeros((6, 2), int)
    P2[:3, 0] = 1
    P2[3:, 1] = 1
    r2 = E.fit_cfa(np.cov(Xs.T, bias=True), m, P2)
    d = np.sqrt(np.diag(r2["Phi"]))
    out.row("attenuation: sum scores correlate; the factors (truth 0.5)",
            f"{np.corrcoef(Xs[:, :3].sum(1), Xs[:, 3:].sum(1))[0, 1]:.2f}; {r2['Phi'][0, 1] / (d[0] * d[1]):.2f}")

    med = E.mediation(seed=seed + 44, boots=500)
    out.row("a confounded mediator with no effect: indirect a*b and 95% interval",
            f"{med['indirect']:.3f} [{med['lo']:.3f}, {med['hi']:.3f}] (truth {med['true']:.1f})")

    eq = E.markov_equivalent()
    out.row("equivalent models: largest gap between chain, reverse and fork; collider differs",
            f"{max(np.abs(eq[k] - eq['chain']).max() for k in ('reverse', 'fork')):.1e}; "
            f"{np.abs(eq['collider'] - eq['chain']).max():.2f}")

    out.note = ("The three-factor model is rejected by χ² but describes the tests well; the schools share loadings "
                "but not intercepts, so their means cannot be compared as they stand; and fit cannot rescue a "
                "confounded mediator or choose among equivalent diagrams.")

    fig, ax = labs.figure(2, size=(11, 4.0))
    std = r3["L"] * np.sqrt(np.diag(r3["Phi"]))[None, :] / np.sqrt(np.diag(r3["Sigma"]))[:, None]
    ax[0].bar(range(1, 10), std.sum(1), color=[labs.BLUE] * 3 + [labs.GREEN] * 3 + [labs.RED] * 3)
    ax[0].set(title="standardized loadings, three factors", xlabel="test", ylabel="loading")
    levs = ("configural", "metric", "scalar")
    ax[1].bar(levs, [inv[k]["T"] for k in levs], color=[labs.BLUE, labs.GREEN, labs.RED])
    ax[1].set(title="invariance across two schools", ylabel="chi-square")
    out.fig = fig
    return out


if __name__ == "__main__":
    print(run())

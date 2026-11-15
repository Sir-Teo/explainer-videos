"""Lab 32: Spearman's tetrads and one factor, one factor against three in Holzinger and Swineford's battery, three
worlds that make the same positive manifold and the experiment that separates them, and range restriction."""

import numpy as np

from videos.coursekit import labs
from explainer.psychology import archive, opendata
from explainer.psychology.psyche import traits as T
from explainer.stats.kit import multi

TITLE = "Intelligence"
GOAL = ("Fit one factor to Spearman's 1904 correlations and check his tetrads; test one, two and three factors on a "
        "real battery; build a common-cause, a sampling and a mutualism world that all fit one factor, and train one "
        "ability in two of them; restrict the range of a validity study and correct it.")
TASKS = [
    "Raise the coupling in the mutualism world from 0.08 to 0.15. How do the correlations, the one-factor loadings "
    "and the transfer from training change?",
    "In the range-restriction simulation, hire the top 10% instead of 30%. How far does the observed validity fall, "
    "and does Thorndike's correction still recover it?",
    "Give the matrix items fewer answer options (n_options in traits.matrix_item). How does the solver's accuracy at "
    "each capacity change, and why does chance matter for what a score means?",
]


def run(seed=0):
    out = labs.Lab()

    # 1. Spearman's table
    s = archive.SPEARMAN_1904
    R = np.asarray(s.data["R"], float)
    f1 = T.one_factor(R)
    out.row("Spearman: one-factor loadings", ", ".join(f"{v:.2f}" for v in f1["loadings"]))
    tet = T.tetrads(R)
    out.row("Spearman: mean absolute tetrad difference; RMSR of residuals",
            f"{np.mean(np.abs(tet)):.3f}; {np.sqrt(np.mean(f1['residual'][np.triu_indices(6, 1)] ** 2)):.3f}")
    assert f1["loadings"].min() > 0.6

    # 2. Holzinger and Swineford (fetched from CRAN on first use and checked by SHA-256)
    if opendata.available("holzinger1939"):
        X = opendata.holzinger_1939()["X"]
        Rh = T.corr(X)
        fits = [multi.factor_ml(Rh, k, n=X.shape[0]) for k in (1, 2, 3)]
        out.row("Holzinger and Swineford, 301 children: chi-square / df for 1, 2, 3 factors",
                "; ".join(f"{f['chi2']:.1f}/{f['df']:.0f}" for f in fits))
        assert fits[0]["chi2"] > 200 and fits[2]["chi2"] < 40
    else:
        out.row("Holzinger and Swineford", "not fetched (python -m videos.psychology.psych32.compute holzinger)")

    # 3. three worlds
    worlds = {"common cause": T.common_cause(n=2000, seed=seed),
              "sampling": T.sampling(n=2000, seed=seed + 1),
              "mutualism": T.mutualism(n=2000, seed=seed + 2)}
    for name, Xw in worlds.items():
        Rw = T.corr(Xw)
        fw = T.one_factor(Rw, n=Xw.shape[0])
        off = Rw[np.triu_indices(8, 1)]
        out.row(f"{name}: smallest correlation; one-factor p", f"{off.min():.2f}; {fw['p']:.2f}")
        assert off.min() > 0
    for name in ("common", "mutualism"):
        tr = T.train_one(name)
        out.row(f"train ability 1 by 0.5 in the {name} world: change in it, mean change in the others",
                f"{tr['change'][0]:.2f}, {np.mean(tr['change'][1:]):.3f}")

    # 4. range restriction
    rng = np.random.default_rng(seed + 32)
    x = rng.normal(size=100_000)
    y = 0.5 * x + np.sqrt(0.75) * rng.normal(size=x.size)
    sel = x > np.quantile(x, 0.7)
    r_sel = np.corrcoef(x[sel], y[sel])[0, 1]
    u = x[sel].std() / x.std()
    out.row("validity 0.50; hired top 30%: observed r, u, corrected",
            f"{r_sel:.2f}, {u:.2f}, {T.restriction_corrected(r_sel, u):.2f}")
    assert abs(T.restriction_corrected(r_sel, u) - 0.5) < 0.03

    out.note = ("Spearman's correlations fit one factor almost exactly, a real battery needs three, and three very "
                "different worlds make the same positive manifold: a one-factor fit cannot say which world is ours, "
                "but an experiment that trains one ability can. Selecting on a test lowers its validity, and the "
                "correction recovers it only if the selection was on the test alone.")

    fig, ax = labs.figure(2, size=(11, 4.2))
    im = ax[0].imshow(R, vmin=0, vmax=1, cmap="viridis")
    ax[0].set_xticks(range(6), [n[:4] for n in s.data["names"]], fontsize=8)
    ax[0].set_yticks(range(6), [n[:4] for n in s.data["names"]], fontsize=8)
    ax[0].set(title="Spearman (1904): every correlation positive")
    fig.colorbar(im, ax=ax[0], fraction=0.046)
    ax[1].scatter(x[:3000], y[:3000], s=4, color="#888888", alpha=0.4)
    ax[1].scatter(x[:3000][sel[:3000]], y[:3000][sel[:3000]], s=4, color=labs.GOLD, alpha=0.6)
    ax[1].set(title=f"Hired top 30%: r falls from 0.50 to {r_sel:.2f}", xlabel="test", ylabel="performance")
    out.fig = fig
    return out

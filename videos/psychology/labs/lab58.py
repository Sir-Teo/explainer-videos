"""Lab 58: the efficient, predictive brain: sparse coding, Laughlin's code and the tilt after-effect."""

import numpy as np

from videos.coursekit import labs
from explainer.psychology.psyche import efficient as E

TITLE = "The Efficient, Predictive Brain"
GOAL = ("Grow edge detectors by sparse coding, compare them with principal components, and predict the tilt "
        "after-effect from an adapting population code.")
TASKS = [
    "Lower lambda to 0.1. Are the basis functions still localized?",
    "Learn on unwhitened patches. What do the basis functions look like now?",
    "Make the adapted units lose 80% of their gain. Where does the after-effect peak, and how large is it?",
]


def run(seed=0):
    out = labs.Lab()
    imgs = [E.dead_leaves(size=96, seed=seed + s) for s in range(4)]
    X = E.patches(imgs, n=8000, seed=seed)
    Xw, _, _ = E.zca(X, eps=1.0)
    Xw = Xw / Xw.std()
    d = E.learn_dictionary(Xw, atoms=64, lam=0.4, epochs=150, seed=seed)
    loc = E.localization(d["D"])
    pcs = np.linalg.eigh(np.cov(X, rowvar=False))[1][:, ::-1]
    ploc = E.localization(pcs)
    assert np.median(loc["localization"]) > np.median(ploc["localization"]) + 0.2
    out.row("median localization: sparse; principal components",
            f"{np.median(loc['localization']):.2f}; {np.median(ploc['localization']):.2f}")
    out.row("share of zero coefficients at the end", f"{d['sparsity'][-1]:.2f}")
    t = E.tilt_aftereffect()
    i = int(np.argmax(t["shift"]))
    assert 5 <= t["tests"][i] <= 35
    out.row("tilt after-effect: peak shift (degrees) and where", f"{t['shift'][i]:.1f} at {t['tests'][i]:.0f}")
    b = E.efficient_bias()
    out.row("largest efficient-coding bias (degrees)", f"{np.max(np.abs(b['bias'])):.2f}")

    out.note = ("Sparseness, not decorrelation, gives localized oriented units; adaptation that keeps a code "
                "efficient also pushes perception away from the adapter.")

    fig, ax = labs.figure(2, size=(11, 4.0))
    tiles = np.full((8 * 9 + 1, 8 * 9 + 1), np.nan)
    for k in range(64):
        f = d["D"][:, k].reshape(8, 8)
        r, c = divmod(k, 8)
        tiles[1 + r * 9:1 + r * 9 + 8, 1 + c * 9:1 + c * 9 + 8] = f / np.abs(f).max()
    ax[0].imshow(tiles, cmap="gray", vmin=-1, vmax=1)
    ax[0].set(title="sparse basis functions")
    ax[0].axis("off")
    ax[1].plot(t["tests"], t["shift"], "o-")
    ax[1].axhline(0, color="grey", lw=0.8)
    ax[1].set(title="tilt after-effect", xlabel="test minus adapter (deg)", ylabel="perceived shift (deg)")
    out.fig = fig
    return out


if __name__ == "__main__":
    print(run())

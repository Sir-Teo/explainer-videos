from __future__ import annotations

import math

import numpy as np

from explainer.ai import *  # noqa: F403
from videos.ai.ai4.common import GRAD, HESS, HIST, PART, VALUE, expo, load, log_axes, mant

CLASS_COL = [C.TRUE_P, GRAD, C.BITS]


def region_image(P, side, width):
    """Class probabilities on a grid as a picture: each pixel the classes' colours, mixed by probability."""
    cols = np.array([ManimColor(c).to_rgb() for c in CLASS_COL])
    rgb = (np.asarray(P)[:, :, None] * cols[None]).sum(1).reshape(side, side, 3)
    bg = np.array(ManimColor("#121722").to_rgb())
    rgb = 0.45 * rgb + 0.55 * bg
    rgb = rgb[::-1]  # rows from the top
    img = ImageMobject((np.concatenate([rgb, np.ones((side, side, 1))], -1) * 255).astype(np.uint8))
    img.set_resampling_algorithm(RESAMPLING_ALGORITHMS["nearest"])
    return img.stretch_to_fit_width(width).stretch_to_fit_height(width)


def symlog(v, lin=1e-3):
    """Signed log scale for eigenvalues relative to the largest: 0 at 0, +-1 at +-1, log-spaced below."""
    v = np.asarray(v, float)
    return np.sign(v) * np.log10(1 + np.abs(v) / lin) / math.log10(1 + 1 / lin)


class HVP(VoiceoverScene):
    def construct(self):
        self.card()
        self.derive()
        self.checks()
        self.replay()

    def card(self):
        card = chapter_card(13, r"Hessian-vector products", r"Can we use curvature without the Hessian?", part=PART)
        with self.voiceover("Chapter thirteen. Curvature without the Hessian."):
            self.play(FadeIn(card[0], shift=UP * 0.2), FadeIn(card[1]))
        self.play(FadeOut(card))

    # ------------------------------------------------------------------
    def derive(self):
        rows = [
            cmath(r"H v", r"=", r"\lim_{t \to 0} \frac{\nabla f(\theta + t v) - \nabla f(\theta)}{t}", font_size=38,
                  colors={r"H v": HESS}),
            cmath(r"H v", r"=", r"\nabla_\theta \big(\nabla f(\theta) \cdot v\big)", font_size=40, colors={r"H v": HESS}),
            cmath(r"\text{cost}(H v)", r"\approx", r"c \times \text{cost}(\nabla f)", font_size=40),
        ]
        whys = [why(r"how the gradient changes along $v$"), why(r"$v$ is fixed: \ the gradient of one number"),
                why(r"reverse mode, run through the gradient's own computation")]
        step = ladder(self, rows, whys, keep=3, top=2.9, x=-2.6, buff=0.65, edge=6.9)
        hist = history_card(1994, r"Barak Pearlmutter, \ \textit{Fast Exact Multiplication by the Hessian}",
                            r"$Hv$ exactly, \ for a few times the cost of a gradient, \ without forming $H$", width=8.0,
                            font_size=19, color=HIST).to_edge(DOWN, buff=0.4)
        with self.voiceover(
            "A Hessian with a billion rows is out of reach, but its product with one vector is not. "
            "<bookmark mark='a'/> H times v is how the gradient changes as you move along v. <bookmark mark='b'/> "
            "Since v is fixed, that's the gradient of a single number, the gradient dotted with v. "
            "<bookmark mark='c'/> And a gradient of one number is what reverse mode does cheaply: run it once more, "
            "through the computation of the gradient itself, and you get H v exactly, for a small multiple of the "
            "cost of a gradient. Barak Pearlmutter published the trick in 1994."
        ) as vo:
            step(0)
            vo.wait_until("a")
            self.play(Indicate(rows[0][2], color=HESS, scale_factor=1.04))
            vo.wait_until("b")
            step(1)
            vo.wait_until("c")
            step(2)
            self.play(FadeIn(hist, shift=UP * 0.2))
        self.wait(0.3)
        self.clear_scene()

    # ------------------------------------------------------------------
    def checks(self):
        d = load("hessian")
        hs, fe = np.asarray(d["hs"]), np.asarray(d["fd_err"])
        assert d["hv_full_diff"] < 1e-10
        g1 = log_axes((-10, -1), (-10, 0), x_length=5.4, y_length=3.6, xlabel=r"step $h$",
                      ylabel=r"finite differences of gradients: \ error", center=[-3.6, -0.6, 0], ystep=2, xstep=3)
        c1 = curve(g1.ax, np.log10(hs), np.clip(np.log10(fe), -10, 0), GRAD, 3)
        best = Dot(g1.ax.c2p(math.log10(d["fd_best_h"]), math.log10(d["fd_best"])), radius=0.07, color=GRAD)
        lam = np.asarray(d["lam_est"])
        top = float(d["lam_top"])
        K_ = 40
        relerr = np.maximum(np.abs(lam[:K_] - top) / top, 1e-16)
        g2 = log_axes((0, K_), (-16, 0), x_length=4.6, y_length=3.2, xlabel=r"power iteration step",
                      ylabel=r"error of the largest eigenvalue", xticks=[], ystep=4, font_size=18, center=[3.6, -0.9, 0])
        for k_ in (0, 20, 40):
            g2.add(MathTex(str(k_), font_size=18, color=GREY_B).next_to(g2.ax.c2p(k_, -16), DOWN, buff=0.1))
        c2 = VGroup(curve(g2.ax, np.arange(K_), np.log10(relerr), HESS, 3),
                    *[Dot(g2.ax.c2p(i, float(np.log10(v))), radius=0.035, color=HESS) for i, v in enumerate(relerr)])
        line = VMobject()
        rel = abs(d["lam_power"] - top) / top
        info = VGroup(
            label(rf"a ${d['sizes'][0]}$--${d['sizes'][1]}$--${d['sizes'][2]}$--${d['sizes'][3]}$ network, \ "
                  rf"${d['P']}$ parameters, \ trained \ (computed)", font_size=22, color=GREY_A),
            label(rf"Pearlmutter against the full ${d['P']} \times {d['P']}$ Hessian: \ ${sci(max(d['hv_full_diff'], 1e-18), 0)}$",
                  font_size=22, color=HESS),
            label(rf"time: \ ${d['t_hvp'] / d['t_grad']:.1f}$ gradients' worth", font_size=22, color=HESS),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.14).to_edge(UP, buff=0.35)
        fdl = label(rf"best: \ ${sci(d['fd_best'], 0)}$ at $h = {sci(d['fd_best_h'], 0)}$", font_size=20, color=GRAD)
        fdl.next_to(best, DOWN, buff=0.15)
        pwl = label(rf"from products alone: \ off by ${sci(max(rel, 1e-16), 0)}$", font_size=20, color=HESS)
        pwl.next_to(g2, DOWN, buff=0.1).align_to(g2, LEFT)
        ratio = d["t_hvp"] / d["t_grad"]
        e = d["fd_best"]
        with self.voiceover(
            "Check it on a small network we'll meet in a moment. <bookmark mark='a'/> Against the full Hessian, "
            f"built the slow way, Pearlmutter's product agrees to rounding error, and it costs {ratio:.1f} gradients. "
            "<bookmark mark='b'/> Finite differences of gradients make another V, as in chapter ten, and at their best "
            f"are off by {mant(e)} times ten to the minus {expo(e)}. <bookmark mark='c'/> And products are all you "
            "need to learn about curvature: multiply a vector by H, again and again, renormalizing, and it turns "
            "toward the steepest direction. The estimate of the largest eigenvalue converges to the true one."
        ) as vo:
            self.play(FadeIn(info[0]), FadeIn(g1), FadeIn(g2))
            vo.wait_until("a")
            self.play(FadeIn(info[1]), FadeIn(info[2]))
            vo.wait_until("b")
            self.play(Create(c1), FadeIn(best), FadeIn(fdl), run_time=1.6)
            vo.wait_until("c")
            self.play(Create(c2), FadeIn(pwl), run_time=2.0)
        self.wait(0.3)
        self.clear_scene()

    # ------------------------------------------------------------------
    def replay(self):
        d = load("hessian")
        keep = [int(k) for k in d["keep"]]
        K = len(keep)
        X, y = np.asarray(d["X"]), np.asarray(d["y"])
        side = len(np.asarray(d["grid_xs"]))
        W = 3.4
        cen = np.array([-4.7, 0.55, 0])
        imgs = [region_image(d[f"region{k}"], side, W).move_to(cen) for k in range(K)]
        frame = SurroundingRectangle(imgs[0], buff=0, color=GREY_D, stroke_width=1.5)
        lo, hi = float(np.asarray(d["grid_xs"])[0]), float(np.asarray(d["grid_xs"])[-1])

        def to_xy(p):
            return cen + np.array([(p[0] - lo) / (hi - lo) - 0.5, (p[1] - lo) / (hi - lo) - 0.5, 0]) * W

        pts = VGroup(*[Dot(to_xy(p), radius=0.03, color=CLASS_COL[int(c)]) for p, c in zip(X, y)]).set_z_index(3)
        # the loss curve
        cv = np.asarray(d["curve"])
        g1 = log_axes((0, math.log10(d["steps"])), (-5, 1), x_length=3.4, y_length=1.25, xlabel=r"step",
                      ylabel=r"loss", center=[-4.5, -2.55, 0], ystep=3, font_size=16)
        a1 = g1.ax
        okc = cv[:, 0] > 0
        lc = curve(a1, np.log10(cv[okc, 0]), np.clip(np.log10(cv[okc, 1]), -5, 1), C.LOSS, 2.5)
        # the spectrum: eigenvalues over the largest, sorted, on a signed log scale
        P = int(d["P"])
        g2 = axes([0, P, 100], [-1.05, 1.05, 0.5], x_length=6.2, y_length=4.0, xlabel=r"eigenvalues, \ smallest to largest",
                  ylabel=r"$\lambda / \lambda_{\max}$ \ (signed log scale)", xticks=[], yticks=[-1, 0, 1],
                  yfmt=lambda v: {-1: "-1", 0: "0", 1: "1"}[int(v)], font_size=18, center=[2.9, -0.75, 0])
        a2 = g2.ax
        for v in (-0.1, -0.01, 0.01, 0.1):
            yv = float(symlog(v))
            g2.add(MathTex(f"{v:g}", font_size=14, color=GREY_C).next_to(a2.c2p(0, yv), LEFT, buff=0.08))

        def spectrum(k):
            ev = np.sort(np.asarray(d[f"eig{k}"]))
            ys = symlog(ev / ev.max())
            return VGroup(*[Dot(a2.c2p(i, float(v)), radius=0.022,
                                color=(HESS if v > symlog(0.1) else (C.SURPRISE if v < symlog(-0.01) else GREY_B)))
                            for i, v in enumerate(ys)])

        def readout(k):
            t = keep[k]
            return VGroup(
                label(rf"step ${t:,}$".replace(",", "{,}") + rf": \ loss ${d[f'loss{k}']:.4f}$, \ accuracy "
                      rf"${100 * d[f'acc{k}']:.0f}\%$", font_size=23, color=WHITE),
                label(rf"$\lambda_{{\max}} = {d[f'top{k}']:.3g}$; \ outliers ${d[f'nout{k}']}$, \ negative ${d[f'nneg{k}']}$, "
                      rf"\ near zero ${100 * d[f'flat{k}']:.0f}\%$", font_size=21, color=GREY_A),
            ).arrange(DOWN, aligned_edge=LEFT, buff=0.08).move_to([2.9, 2.55, 0])

        dots = [spectrum(k) for k in range(K)]
        reads = [readout(k) for k in range(K)]
        marker = Dot(a1.c2p(0, math.log10(d["loss0"])), radius=0.06, color=WHITE)

        def mpos(k):
            t = max(keep[k], 1)
            return a1.c2p(math.log10(t), float(np.clip(math.log10(d[f"loss{k}"]), -5, 1)))

        marker.move_to(mpos(0))
        title = label(rf"three spirals, \ a ${P}$-parameter network, \ trained with Adam: \ its full Hessian at "
                      rf"${K}$ checkpoints", font_size=22, color=GREY_A).to_edge(UP, buff=0.2)
        tag = note(r"computed").to_corner(DR, buff=0.2)
        nk = K - 1
        neg0, negK = int(d["nneg0"]), int(d[f"nneg{nk}"])
        out_end = int(d[f"nout{nk}"])
        flat_end = 100 * float(d[f"flat{nk}"])
        neg_v = (f"from {neg0} clearly negative eigenvalues at the start to {negK}" if negK < neg0 else
                 f"{neg0} clearly negative eigenvalues at the start and {negK} at the end")
        out_v = (f"{out_end} eigenvalues stand out above a tenth of the largest" if out_end > 0 else
                 "no eigenvalue stands out")
        with self.voiceover(
            "Now watch a landscape change as a network learns. Three interleaved spirals, a network with "
            f"{P} parameters, and its full Hessian, computed at {K} moments during training. "
            "<bookmark mark='a'/> At the start, the eigenvalues spread both ways: the initial point is a saddle in "
            f"many directions. <bookmark mark='b'/> As the network fits the spirals, the negative curvature drains "
            f"away, {neg_v}. <bookmark mark='c'/> At the end, {out_v}, and "
            f"{flat_end:.0f} percent lie within a hundredth of zero: a bulk of nearly flat directions, plus a few "
            "steep ones, the shape Levent Sagun and colleagues reported for real networks in 2016. And as the loss "
            "goes to zero, the whole spectrum shrinks with it."
        ) as vo:
            self.play(FadeIn(title), FadeIn(imgs[0]), FadeIn(frame), FadeIn(pts), FadeIn(g1), Create(lc), FadeIn(marker),
                      FadeIn(g2), FadeIn(dots[0]), FadeIn(reads[0]), FadeIn(tag), run_time=2.0)
            vo.wait_until("a")
            self.play(Indicate(dots[0], color=C.SURPRISE, scale_factor=1.0))
            vo.wait_until("b")
            for k in range(1, K):
                rt = 1.0
                self.play(FadeOut(imgs[k - 1]), FadeIn(imgs[k]), Transform(dots[0], dots[k]),
                          FadeOut(reads[k - 1]), FadeIn(reads[k]), marker.animate.move_to(mpos(k)), run_time=rt)
                if k == 2:
                    vo.wait_until("c")
        self.wait(0.3)
        self.clear_scene()

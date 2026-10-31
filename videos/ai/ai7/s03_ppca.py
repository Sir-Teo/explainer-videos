from __future__ import annotations

import numpy as np

from explainer.ai import *  # noqa: F403
from videos.ai.ai7.common import HIDDEN, MONO, PART, SEEN, card_in, edge, load, node

W_C = C.MODEL_Q  # the loading matrix W
NOISE = C.SURPRISE  # the noise sigma^2


class PPCA(VoiceoverScene):
    def construct(self):
        card_in(self, 2, r"PCA as a probability model", r"Can PCA say how likely a new page is?",
                "Chapter two. PCA as a probability model.")
        self.model()
        self.solution()
        self.heldout()
        self.family()

    # ------------------------------------------------------------------
    def model(self):
        p = load("pca2")
        Z2 = np.asarray(p["Z2"])
        C2 = Z2.T @ Z2 / len(Z2)
        lv, lV = np.linalg.eigh(C2)
        u, l1, s2 = lV[:, -1], float(lv[-1]), float(lv[0])
        g = np.random.default_rng(1999)  # illustrative samples from the fitted two-rate model
        zs = g.normal(size=160)
        eps = g.normal(size=(160, 2)) * np.sqrt(s2)
        w = u * np.sqrt(l1 - s2)
        ax = Axes(x_range=[-3.2, 3.2, 1], y_range=[-3.2, 3.2, 1], x_length=5.0, y_length=5.0, tips=False,
                  axis_config={"stroke_color": GREY_D, "include_ticks": False}).move_to([3.6, -0.6, 0])
        names = VGroup(data_text("the", font=MONO, font_size=20, color=GREY_A).next_to(ax.x_axis.get_right(), DOWN, buff=0.1),
                       data_text("not", font=MONO, font_size=20, color=GREY_A).next_to(ax.y_axis.get_top(), RIGHT, buff=0.1))
        zl = NumberLine(x_range=[-3, 3, 1], length=3.4, color=HIDDEN, include_numbers=False).move_to([3.6, 2.85, 0])
        zlab = MathTex(r"z", font_size=30, color=HIDDEN).next_to(zl, LEFT, buff=0.2)
        zdots = VGroup(*[Dot(zl.n2p(float(np.clip(z, -3, 3))), radius=0.035, color=HIDDEN) for z in zs])
        on_line = VGroup(*[Dot(ax.c2p(*(z * w)), radius=0.035, color=W_C) for z in zs])
        noisy = VGroup(*[Dot(ax.c2p(*np.clip(z * w + e, -3.1, 3.1)), radius=0.035, color=SEEN) for z, e in zip(zs, eps)])
        wline = Line(ax.c2p(*(-3.2 * u)), ax.c2p(*(3.2 * u)), color=W_C, stroke_width=2, stroke_opacity=0.6)
        rows = VGroup(
            cmath(r"z", r"\sim", r"\mathcal{N}(0,\, I_k)", colors={r"z": HIDDEN}, font_size=38),
            cmath(r"x", r"=", r"W", r"z", r"+", r"\mu", r"+", r"\varepsilon", colors={r"z": HIDDEN, r"W": W_C,
                                                                                   r"\varepsilon": NOISE, r"x": SEEN},
                  font_size=38),
            cmath(r"\varepsilon", r"\sim", r"\mathcal{N}(0,\, \sigma^2 I)", colors={r"\varepsilon": NOISE}, font_size=38),
            cmath(r"x", r"\sim", r"\mathcal{N}\big(\mu,\;", r"W W^{\top}", r"+", r"\sigma^2 I", r"\big)",
                  colors={r"x": SEEN, r"WW^{\top}": W_C, r"\sigma^2I": NOISE}, font_size=38),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.35).move_to([-3.4, 0.9, 0])
        gz = node(r"z", [-5.2, -2.2, 0])
        gx = node(r"x", [-3.4, -2.2, 0], hidden=False)
        gm = VGroup(gz, gx, edge(gz, gx))
        gl = label(r"$k$ hidden factors \\ $\to$ $d$ observed rates", font_size=22, color=GREY_A).next_to(gm, RIGHT, buff=0.4)
        tag = note(r"samples from the model fitted to two rates", font_size=20).next_to(ax, DOWN, buff=0.15)
        hc = history_card(1999, r"M.~Tipping \& C.~Bishop; \ S.~Roweis", r"PCA as a model with hidden factors",
                          width=5.0).move_to([-3.4, 1.4, 0])
        with self.voiceover(
            "PCA finds directions, but it isn't a model of the data: it can't say how likely a new page is. In 1999 "
            "Michael Tipping and Christopher Bishop, and independently Sam Roweis, turned it into one. "
            "<bookmark mark='a'/> Imagine each page begins as a few hidden numbers, z, drawn from a standard bell "
            "curve. <bookmark mark='b'/> A matrix W maps them up into the seventy word rates, onto a flat sheet "
            "through the data. <bookmark mark='c'/> Then noise of the same size in every direction blurs the "
            "sheet. <bookmark mark='d'/> Add it up, and a page is Gaussian, with covariance W W transpose plus sigma "
            "squared times the identity: a few big directions, and a fog around them."
        ) as vo:
            self.play(FadeIn(gm), FadeIn(gl), Create(ax), FadeIn(names))
            self.play(FadeIn(hc, shift=UP * 0.2))
            vo.wait_until("a")
            self.play(FadeOut(hc))
            self.play(Write(rows[0]), Create(zl), FadeIn(zlab), LaggedStart(*[FadeIn(d) for d in zdots], lag_ratio=0.005))
            vo.wait_until("b")
            self.play(Write(rows[1]), Create(wline), TransformFromCopy(zdots, on_line), run_time=1.8)
            vo.wait_until("c")
            self.play(Write(rows[2]), ReplacementTransform(on_line, noisy), FadeIn(tag), run_time=1.8)
            vo.wait_until("d")
            self.play(Write(rows[3]))
        self.wait(0.3)
        self.clear_scene()

    # ------------------------------------------------------------------
    def solution(self):
        p = load("pca2")
        colors = {r"W_{\mathrm{ML}}": W_C, r"\sigma^2_{\mathrm{ML}}": NOISE, r"U_k": C.BITS}
        thm = theorem_card(
            r"One maximum-likelihood fit for probabilistic PCA",
            VGroup(cmath(r"W_{\mathrm{ML}}", r"=", r"U_k", r"\,(\Lambda_k - \sigma^2 I)^{1/2}", colors=colors, font_size=36),
                   cmath(r"\sigma^2_{\mathrm{ML}}", r"=", r"\frac{1}{d - k} \sum_{j > k} \lambda_j", colors=colors,
                         font_size=36)).arrange(DOWN, aligned_edge=LEFT, buff=0.3),
            who=r"M.~E.~Tipping \& C.~M.~Bishop (1999)", width=7.6).move_to([-2.6, 0.9, 0])
        notes = VGroup(label(r"$U_k$: \ the top $k$ eigenvectors \ (chapter 1)", font_size=24, color=C.BITS),
                       label(r"the noise: \ the average variance left out", font_size=24, color=NOISE),
                       label(r"$\sigma^2 \to 0$: \ plain PCA again", font_size=24, color=GREY_A))
        notes.arrange(DOWN, aligned_edge=LEFT, buff=0.3).next_to(thm, DOWN, buff=0.45).align_to(thm, LEFT)
        lam = np.asarray(p["vals"])[:30]
        k = 5
        bars_ = VGroup(*[Rectangle(width=0.11, height=max(0.33 * v, 0.02), stroke_width=0,
                                   fill_color=C.BITS if i < k else NOISE, fill_opacity=0.85)
                         .move_to([2.0 + 0.14 * i, -2.3 + 0.33 * v / 2, 0]) for i, v in enumerate(lam)])
        s2 = float(np.asarray(p["vals"])[k:].mean())
        fog = DashedLine([1.9, -2.3 + 0.33 * s2, 0], [2.0 + 0.14 * 30, -2.3 + 0.33 * s2, 0], color=WHITE, stroke_width=3)
        bl = label(rf"the eigenvalues, \ $k = {k}$ kept: \\ the rest become the fog $\sigma^2 = {s2:.2f}$", font_size=22,
                   color=GREY_A).next_to(bars_, UP, buff=0.3)
        with self.voiceover(
            "The best W and sigma, by maximum likelihood, come out in closed form. <bookmark mark='a'/> W's columns "
            "can point along the top k eigenvectors of chapter one, each stretched by the square root of its "
            "eigenvalue minus the noise variance. Rotating the hidden axes gives an equally good fit. "
            "<bookmark mark='b'/> And the noise is the average variance of all the directions left out. "
            "<bookmark mark='c'/> Shrink the noise to zero and you get plain PCA back. So PCA was always the limit of "
            "a probability model, and now it has a likelihood."
        ) as vo:
            self.play(FadeIn(thm, shift=UP * 0.2), LaggedStart(*[GrowFromEdge(b, DOWN) for b in bars_], lag_ratio=0.03))
            vo.wait_until("a")
            self.play(FadeIn(notes[0]), FadeIn(bl))
            vo.wait_until("b")
            self.play(FadeIn(notes[1]), Create(fog))
            vo.wait_until("c")
            self.play(FadeIn(notes[2]))
        self.wait(0.3)
        self.clear_scene()

    # ------------------------------------------------------------------
    def heldout(self):
        p = load("pca2")
        tr, te = np.asarray(p["ll_tr"]), np.asarray(p["ll_te"])
        best, full = int(p["best_k"]), float(p["full_te"])
        d = len(tr)
        lo = float(min(te.min(), tr[0])) - 1
        hi = float(max(tr.max(), te.max())) + 1
        g = axes([0, d, 10], [lo, hi, 5], x_length=8.4, y_length=4.6, xlabel=r"hidden directions $k$",
                 ylabel=r"log-likelihood per page (nats)", xticks=[0, 10, 20, 30, 40, 50, 60, 70],
                 yticks=[round(v) for v in np.linspace(lo + 1, hi - 1, 4)], yfmt=lambda v: f"{v:g}",
                 center=[-1.4, -0.3, 0])
        ax = g.ax
        ks = np.arange(d)
        ctr = curve(ax, ks, tr, GREY_B, 3)
        cte = curve(ax, ks, te, C.BITS, 4)
        pk = Dot(ax.c2p(best, te[best]), radius=0.09, color=C.BITS)
        fl = DashedLine(ax.c2p(0, full), ax.c2p(d, full), color=GREY_C, stroke_width=2)
        lg = legend([(GREY_B, rf"the ${p['n_train']}$ training pages"), (C.BITS, rf"the ${p['n_test']}$ held-out pages"),
                     (GREY_C, r"a full $70 \times 70$ covariance")], font_size=22).move_to([4.9, 1.6, 0])
        res = label(rf"best: \ $k = {best}$ \ (${100 * p['share_best']:.0f}\%$ of the variance)", font_size=26,
                    color=C.BITS).move_to([4.6, -0.6, 0])
        better = te[best] > full
        if better:
            verdict = (f"Held-out pages are most likely with {best} hidden directions, at {te[best]:.1f} nats per page, "
                       f"better than a full covariance, at {full:.1f}: the other directions are mostly noise.")
        else:
            verdict = (f"Held-out pages peak at {best} hidden directions, at {te[best]:.1f} nats per page, but a full "
                       f"covariance does as well, at {full:.1f}: on these pages every direction carries a little signal.")
        with self.voiceover(
            "A likelihood lets us choose how many hidden directions to keep, on pages the model never saw. Fit on "
            f"part six's {p['n_train']} training pages, score the {p['n_test']} held-out ones. <bookmark mark='a'/> On "
            "the training pages, every extra direction helps. <bookmark mark='b'/> " + verdict
        ) as vo:
            self.play(FadeIn(g), FadeIn(lg))
            self.play(Create(ctr), run_time=1.5)
            vo.wait_until("a")
            self.play(Indicate(lg[0], color=GREY_B))
            vo.wait_until("b")
            self.play(Create(cte), Create(fl), run_time=2.0)
            self.play(FadeIn(pk, scale=1.5), FadeIn(res))
        self.wait(0.3)
        self.clear_scene()

    # ------------------------------------------------------------------
    def family(self):
        items = [(1904, r"factor analysis", r"Spearman: \ a noise level \\ for every variable", GREY_B),
                 (1999, r"probabilistic PCA", r"one noise level; \\ $W$ by eigenvectors", W_C),
                 (2013, r"the variational autoencoder", r"a network in place of $W$ \\ (Part 20)", HIDDEN)]
        boxes = VGroup()
        for yr, name, sub, col in items:
            t = VGroup(label(str(yr), font_size=34, color=col), label(name, font_size=26),
                       label(sub, font_size=20, color=GREY_A)).arrange(DOWN, buff=0.15)
            box = RoundedRectangle(width=3.8, height=t.height + 0.5, corner_radius=0.15, stroke_color=col,
                                   stroke_width=2, fill_color="#0B0F17", fill_opacity=0.9)
            boxes.add(VGroup(box, t.move_to(box)))
        boxes.arrange(RIGHT, buff=0.7).move_to(UP * 0.4)
        arrs = VGroup(*[Arrow(a.get_right(), b.get_left(), buff=0.1, color=GREY_B) for a, b in zip(boxes, boxes[1:])])
        gm = VGroup(node(r"z", [-0.8, -2.4, 0]), node(r"x", [0.8, -2.4, 0], hidden=False))
        gm.add(edge(gm[0], gm[1]))
        gl = label(r"the same picture in all three: \ hidden $z$, observed $x$", font_size=24, color=GREY_A)
        gl.next_to(gm, DOWN, buff=0.25)
        with self.voiceover(
            "Probabilistic PCA sits in a family. <bookmark mark='a'/> Charles Spearman's factor analysis, from "
            "1904, is the same model with a separate noise level for every variable. <bookmark mark='b'/> "
            "Probabilistic PCA ties them into one, which is why the eigenvectors fall out. <bookmark mark='c'/> And "
            "replace the matrix W with a neural network, and you have the variational autoencoder of part twenty: "
            "the same hidden z, the same picture, a curved sheet instead of a flat one."
        ) as vo:
            self.play(FadeIn(gm), FadeIn(gl))
            vo.wait_until("a")
            self.play(FadeIn(boxes[0], shift=UP * 0.2))
            vo.wait_until("b")
            self.play(GrowArrow(arrs[0]), FadeIn(boxes[1], shift=UP * 0.2))
            vo.wait_until("c")
            self.play(GrowArrow(arrs[1]), FadeIn(boxes[2], shift=UP * 0.2))
        self.wait(0.3)
        self.clear_scene()

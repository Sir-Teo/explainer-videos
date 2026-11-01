from __future__ import annotations

import math

import numpy as np

from explainer.ai import *  # noqa: F403
from videos.ai.ai6.common import (AUSTEN, DICKENS, GOOD, HL, chapter, load, page_dots, page_plane, plot, pow10,
                                  regions, side_ladder)

NN1, NNK, BAYES, BOUND = C.MODEL_Q, C.REWARD, C.TRUE_P, C.PENALTY
SHOW_K = [1, 3, 15, 45, 201]


class KNN(VoiceoverScene):
    def construct(self):
        chapter(self, 9, r"Neighbours, and the curse of dimensionality", r"What if there is no line at all?",
                "Chapter nine. Nearest neighbours.", lit=(1967,))
        self.vote()
        self.regions()
        self.cover_hart()
        self.curse()

    def setup_data(self):
        p = load("pages")
        X2, y, test = np.asarray(p["X2"]), np.asarray(p["y"]), np.asarray(p["test"], bool)
        mu, sd = X2[~test].mean(0), X2[~test].std(0)
        return X2, y, test, mu, sd

    # ------------------------------------------------------------------
    def vote(self):
        X2, y, test, mu, sd = self.setup_data()
        plane = page_plane(x_length=7.6, y_length=5.0, center=[-2.2, -0.3, 0])
        ax = plane[0]
        tr = np.nonzero(~test)[0]
        dots = page_dots(ax, X2, y, idx=tr, jitter=0.35, radius=0.045, opacity=0.7)
        te = np.nonzero(test)[0]
        Ztr = (X2[tr] - mu) / sd
        cand = [i for i in te if 40 <= X2[i, 0] <= 50 and 7 <= X2[i, 1] <= 10]
        q = cand[0]
        zq = (X2[q] - mu) / sd
        d = np.sqrt(((Ztr - zq) ** 2).sum(1))
        nn = np.argsort(d, kind="stable")[:15]
        nd = int(y[tr][nn].sum())
        qd = glow_dot(ax.c2p(*X2[q]), color=WHITE, radius=0.1)
        links = VGroup(*[Line(ax.c2p(*X2[q]), ax.c2p(*X2[tr[j]]), color=AUSTEN if y[tr[j]] == 0 else DICKENS,
                              stroke_width=2, stroke_opacity=0.8) for j in nn])
        r_scr = max(np.linalg.norm(ax.c2p(*X2[tr[j]]) - ax.c2p(*X2[q])) for j in nn)
        ring = Circle(radius=r_scr + 0.05, color=WHITE, stroke_width=2).move_to(ax.c2p(*X2[q])).set_stroke(opacity=0.6)
        tally = VGroup(label(rf"Austen: \ ${15 - nd}$", font_size=32, color=AUSTEN),
                       label(rf"Dickens: \ ${nd}$", font_size=32, color=DICKENS)).arrange(DOWN, aligned_edge=LEFT, buff=0.2)
        tally.move_to([4.4, 1.0, 0])
        verdict = label(r"the vote: \ " + ("Dickens" if nd > 7 else "Austen"), font_size=32,
                        color=DICKENS if nd > 7 else AUSTEN).next_to(tally, DOWN, buff=0.4).align_to(tally, LEFT)
        truth = label(r"(it's " + ("Dickens" if y[q] == 1 else "Austen") + ")", font_size=26, color=GREY_A)
        truth.next_to(verdict, DOWN, buff=0.15).align_to(tally, LEFT)
        note_ = label(r"distances measured in standard deviations of each rate", font_size=22, color=GREY_B)
        note_.to_edge(DOWN, buff=0.25)
        cite_ = cite(r"E.~Fix \& J.~Hodges (1951); \ T.~Cover \& P.~Hart (1967)", corner=UR)
        with self.voiceover(
            "Here's a method with no line at all, written down by Fix and Hodges in 1951. To classify a page, find "
            "the training pages most like it, its nearest neighbours, and let them vote. <bookmark mark='a'/> Take "
            f"this page from the test set. <bookmark mark='b'/> Its fifteen nearest neighbours: {15 - nd} by Austen, "
            f"{nd} by Dickens. <bookmark mark='c'/> The majority wins. There's no training at all: the model is the data."
        ) as vo:
            self.play(Create(ax), FadeIn(plane[1:]), LaggedStart(*[FadeIn(d_) for d_ in dots], lag_ratio=0.003),
                      FadeIn(cite_), run_time=2.0)
            vo.wait_until("a")
            self.play(FadeIn(qd, scale=0.5))
            vo.wait_until("b")
            self.play(Create(ring), LaggedStart(*[Create(l_) for l_ in links], lag_ratio=0.08), FadeIn(tally), FadeIn(note_),
                      run_time=2.0)
            self.play(Indicate(ring, color=WHITE, scale_factor=1.15), run_time=1.2)
            vo.wait_until("c")
            self.play(FadeIn(verdict), FadeIn(truth))
        self.wait(0.3)
        self.clear_scene()

    # ------------------------------------------------------------------
    def regions(self):
        X2, y, test, mu, sd = self.setup_data()
        k_ = load("knn")
        ks = [int(k) for k in k_["ks"]]
        plane = page_plane(x_length=6.4, y_length=4.4, center=[-3.4, -0.2, 0])
        ax = plane[0]
        tr = np.nonzero(~test)[0]
        dots = page_dots(ax, X2, y, idx=tr, jitter=0.35, radius=0.035, opacity=0.9)
        imgs = {k: regions(ax, k_[f"region{k}"], k_["xs"], k_["ys"], opacity=0.45) for k in SHOW_K}
        lx = np.log10(ks)
        g = plot([0, lx[-1] + 0.1, 1], [0.6, 1.0, 0.1], x_length=5.0, y_length=3.6, xticks=[0, 1, 2],
                 yticks=[0.6, 0.7, 0.8, 0.9, 1.0], xfmt=lambda v: pow10(int(v)), yfmt=lambda v: rf"{100 * v:.0f}\%",
                 center=[3.7, -0.3, 0], xlabel=r"neighbours $k$ \ (log scale)", ylabel=r"pages right")
        a2 = g.ax
        trc = curve(a2, lx, [k_[f"train{k}"] for k in ks], GREY_A, stroke_width=3)
        tec = curve(a2, lx, [k_[f"acc{k}"] for k in ks], HL, stroke_width=4)
        cvm, cvs = np.asarray(k_["cv"]), np.asarray(k_["cv_sd"])
        cvb = band(a2, lx, cvm - cvs / math.sqrt(10), cvm + cvs / math.sqrt(10), GOOD, opacity=0.25)
        cvc = curve(a2, lx, cvm, GOOD, stroke_width=3)
        key = VGroup(label(r"training pages", font_size=20, color=GREY_A), label(r"held-out pages", font_size=20, color=HL),
                     label(r"ten-fold cross-validation, $\pm 1$ s.e.", font_size=20, color=GOOD))
        key.arrange(DOWN, aligned_edge=LEFT, buff=0.06).next_to(g, UP, buff=0.12).align_to(g, LEFT)
        kv = ValueTracker(0)
        kl = always_redraw(lambda: MathTex(rf"k = {SHOW_K[int(round(kv.get_value()))]}", font_size=34, color=HL)
                           .next_to(ax, UP, buff=0.12).align_to(ax, RIGHT))
        kcv = int(k_["k_cv"])
        t1, a1 = k_["train1"], k_["acc1"]
        best_te = max(ks, key=lambda k: k_[f"acc{k}"])
        same = kcv == best_te
        acc_b = k_[f"acc{best_te}"]
        say_cv = (f"Cross-validation, which never looks at the held-out pages, picks the same k."
                  if same else
                  f"Cross-validation, which never looks at them, picks k equals {kcv}, and gets "
                  f"{100 * k_['acc_kcv']:.0f} percent of them right: the held-out pages' best k was partly luck.")
        with self.voiceover(
            "Colour every point of the plane by how its neighbours would vote, and you see the method's whole answer. "
            f"<bookmark mark='a'/> With one neighbour, the regions are a ragged patchwork that copies the training pages: "
            f"{100 * t1:.0f} percent of them right, but only {100 * a1:.0f} percent of new ones. <bookmark mark='b'/> "
            "More neighbours smooth it out. <bookmark mark='c'/> On the held-out pages the best is k equals "
            f"{best_te}, {100 * acc_b:.0f} percent. {say_cv}"
        ) as vo:
            self.play(Create(ax), FadeIn(plane[1:]), FadeIn(dots), FadeIn(g), FadeIn(key))
            vo.wait_until("a")
            self.play(FadeIn(imgs[1]), FadeIn(kl))
            self.bring_to_front(dots)
            self.play(Create(trc), Create(tec), run_time=1.5)
            vo.wait_until("b")
            cur = imgs[1]
            for i, k in enumerate(SHOW_K[1:], 1):
                self.play(FadeOut(cur), FadeIn(imgs[k]), kv.animate.set_value(i), run_time=1.0)
                self.bring_to_front(dots)
                cur = imgs[k]
            vo.wait_until("c")
            self.play(FadeIn(cvb), Create(cvc))
        kl.clear_updaters()
        self.wait(0.3)
        self.clear_scene()

    # ------------------------------------------------------------------
    def cover_hart(self):
        ch = load("coverhart")
        Rs, lim, bnd = ch["Rstar"], ch["lim1"], ch["bound"]
        thm = theorem_card(r"Cover--Hart (1967)",
                           r"As the training set grows, the error of the single nearest neighbour approaches "
                           r"$\mathbb{E}\,2\eta(1-\eta)$, \ which lies between $R^*$ and $2R^*(1 - R^*)$; \ $R^*$ is the "
                           r"best possible error.", width=6.6, font_size=21).to_corner(UL, buff=0.25)
        rows = [
            cmath(r"P(\text{err} \mid x, x')", "=", r"\eta(1 - \eta') + (1 - \eta)\,\eta'", font_size=32),
            cmath(r"P(\text{err} \mid x)", r"\;\to\;", r"2\eta(1 - \eta)", font_size=32),
            cmath(r"2\eta(1-\eta)", "=", r"2r(1 - r) \;\ge\; r", font_size=32),
            cmath(r"\mathbb{E}\,2r(1-r)", r"\;\le\;", r"2R^*(1 - R^*)", font_size=32),
        ]
        whys = [why(r"$\eta' = \eta(x')$: \\ the neighbour's coin", font_size=20),
                why(r"$x' \to x$ \\ as $n \to \infty$", font_size=20),
                why(r"$r = \min(\eta, 1 - \eta)$, \\ the best rule's error", font_size=20),
                why(r"Jensen, \\ $R^* = \mathbb{E}\, r$", font_size=20)]
        step = side_ladder(self, rows, whys, -3.2, 3.5, keep=4, top=0.95, buff=0.26)
        ns = [int(n) for n in ch["ns"]]
        lx = np.log10(ns)
        # Domain includes every measured mean/percentile and theoretical reference.
        values = [Rs, lim, bnd] + [ch[key][str(n)][field]
                  for key in ("e1", "ek") for n in ns for field in ("mean", "lo", "hi")]
        bottom = max(0, math.floor((min(values) - 0.05) / 0.05) * 0.05)
        top = math.ceil(1.08 * max(values) / 0.05) * 0.05
        ticks = np.arange(bottom, top + 1e-9, 0.05).tolist()
        g = plot([0.9, 4.1, 1], [bottom, top, 0.05], x_length=5.2, y_length=4.2, xticks=[1, 2, 3, 4],
                 yticks=ticks, xfmt=lambda v: pow10(int(v)), yfmt=lambda v: rf"{100 * v:.0f}\%",
                 center=[3.9, 0.0, 0], xlabel=r"training points $n$", ylabel=r"error on fresh points")
        ax = g.ax

        def hline(v, col, txt):
            ln = DashedLine(ax.c2p(0.9, v), ax.c2p(4.1, v), color=col, stroke_width=2)
            t = label(txt, font_size=18, color=col).next_to(ax.c2p(4.1, v), LEFT, buff=0.05).shift(UP * 0.14)
            return VGroup(ln, t)

        lines = VGroup(hline(Rs, BAYES, rf"$R^* = {100 * Rs:.1f}\%$"), hline(lim, NN1, rf"limit ${100 * lim:.1f}\%$"),
                       hline(bnd, BOUND, rf"$2R^*(1-R^*) = {100 * bnd:.1f}\%$"))
        art = []
        for key, col in (("e1", NN1), ("ek", NNK)):
            m = [ch[key][str(n)]["mean"] for n in ns]
            lo = [ch[key][str(n)]["lo"] for n in ns]
            hi = [ch[key][str(n)]["hi"] for n in ns]
            art.append(VGroup(band(ax, lx, lo, hi, col, opacity=0.2), curve(ax, lx, m, col, stroke_width=4),
                              VGroup(*[Dot(ax.c2p(a, b), radius=0.04, color=col) for a, b in zip(lx, m)])))
        key_ = VGroup(label(r"$1$ neighbour", font_size=20, color=NN1), label(r"$\sqrt{n}$ neighbours", font_size=20, color=NNK))
        key_.arrange(RIGHT, buff=0.4).next_to(g, UP, buff=0.1)
        tag = note(rf"two overlapping bells, \ centres $\pm{ch['mu']:g}$ apart in one coordinate; \ bands: $10$th--$90$th "
                   r"percentile").to_edge(DOWN, buff=0.15)
        e1n = ch["e1"][str(ns[-1])]["mean"]
        ekn = ch["ek"][str(ns[-1])]["mean"]
        with self.voiceover(
            "How good can copying a neighbour be? Cover and Hart answered in 1967. <bookmark mark='a'/> Let eta of x "
            "be the chance a page at x is Dickens. The nearest neighbour's label is an independent coin with its "
            "own eta, so an error is a disagreement. <bookmark mark='b'/> With enough data the neighbour sits on top "
            "of x, and the error becomes two eta times one minus eta. <bookmark mark='c'/> That's at least the "
            "smaller of eta and one minus eta, the best any rule can do there, <bookmark mark='d'/> and by Jensen's "
            "inequality, on average at most twice the best possible error. <bookmark mark='e'/> Check it on two "
            f"overlapping bells, where the best possible error is {100 * Rs:.1f} percent. With {ns[-1]:,} points the "
            f"single neighbour errs {100 * e1n:.1f} percent of the time, near its limit of {100 * lim:.1f}, inside the "
            f"bound of {100 * bnd:.1f}. Let k grow with n, and the error falls toward the best: {100 * ekn:.1f}."
        ) as vo:
            self.play(FadeIn(thm, shift=DOWN * 0.2), FadeIn(g), FadeIn(lines), FadeIn(tag), FadeIn(key_))
            vo.wait_until("a")
            step(0)
            vo.wait_until("b")
            step(1, transform=False)
            vo.wait_until("c")
            step(2, transform=False)
            vo.wait_until("d")
            step(3, transform=False)
            vo.wait_until("e")
            for a in art:
                self.play(FadeIn(a[0]), Create(a[1]), FadeIn(a[2]), run_time=1.3)
        self.wait(0.3)
        self.clear_scene()

    # ------------------------------------------------------------------
    def curse(self):
        cu = load("curse")
        dims = np.asarray(cu["dims"], float)
        con = np.asarray(cu["contrast"])
        nnf = np.asarray(cu["nn_frac"])
        lx = np.log10(dims)
        g1 = plot([0, 3, 1], [0, 1, 0.25], x_length=4.6, y_length=3.0, xticks=[0, 1, 2, 3], yticks=[0, 0.5, 1],
                  xfmt=lambda v: pow10(int(v)), center=[-4.0, 0.2, 0], xlabel=r"dimensions $d$",
                  ylabel=r"nearest distance $/$ average distance")
        c1 = curve(g1.ax, lx, nnf, BOUND, stroke_width=4)
        d1 = VGroup(*[Dot(g1.ax.c2p(a, b), radius=0.04, color=BOUND) for a, b in zip(lx, nnf)])
        t1 = label(r"$2{,}000$ random points in a cube", font_size=22, color=GREY_A).next_to(g1, UP, buff=0.12)
        ed = cu["edge"]
        cube = VGroup(*[label(rf"$d = {d}$: \ side ${float(ed[str(d)]):.2f}$", font_size=22, color=GREY_A)
                        for d in (1, 2, 10, 100)]).arrange(DOWN, aligned_edge=LEFT, buff=0.1)
        cube_h = label(r"a cube holding $10\%$ of the data", font_size=22, color=WHITE)
        cubes = VGroup(cube_h, cube).arrange(DOWN, aligned_edge=LEFT, buff=0.15)
        for c_ in cube:
            c_.scale(1.25)
        cube_h.scale(1.25)
        cubes.arrange(DOWN, aligned_edge=LEFT, buff=0.2).move_to([3.4, 0.2, 0])
        noise = [int(m) for m in cu["noise"]]
        lxn = np.log10(np.maximum(noise, 1))
        # Include the full measured uncertainty bands with one tick of clearance.
        noise_values = [cu[key][str(n)][field] for key in ("knn", "lr")
                        for n in noise for field in ("mean", "lo", "hi")]
        noise_bottom = max(0, math.floor((min(noise_values) - 0.01) / 0.05) * 0.05)
        noise_top = min(1, math.ceil(max(noise_values) / 0.05) * 0.05)
        noise_ticks = np.arange(noise_bottom, noise_top + 1e-9, 0.05).tolist()
        g2 = plot([0, 3, 1], [noise_bottom, noise_top, 0.05], x_length=4.8, y_length=3.6, xticks=[0, 1, 2, 3], yticks=noise_ticks,
                  xfmt=lambda v: "0" if v == 0 else pow10(int(v)), yfmt=lambda v: rf"{100 * v:.0f}\%", center=[3.4, -0.3, 0],
                  xlabel=r"pure-noise columns added to the $70$ rates", ylabel=r"held-out pages right")
        art = []
        for key, col, nm in (("knn", NN1, r"$15$ nearest neighbours"), ("lr", HL, r"logistic regression")):
            m = [cu[key][str(n)]["mean"] for n in noise]
            lo = [cu[key][str(n)]["lo"] for n in noise]
            hi = [cu[key][str(n)]["hi"] for n in noise]
            art.append(VGroup(band(g2.ax, lxn, lo, hi, col, opacity=0.25), curve(g2.ax, lxn, m, col, stroke_width=4),
                              label(nm, font_size=20, color=col)))
        art[0][2].next_to(g2, UP, buff=0.1).align_to(g2, LEFT)
        art[1][2].next_to(art[0][2], RIGHT, buff=0.4)
        cite_ = cite(r"R.~Bellman, \textit{Dynamic Programming} (1957): \ ``the curse of dimensionality''", corner=DR)
        kn0, kn1 = cu["knn"]["0"]["mean"], cu["knn"][str(noise[-1])]["mean"]
        lr0, lr1 = cu["lr"]["0"]["mean"], cu["lr"][str(noise[-1])]["mean"]
        i10 = list(dims).index(10.0)
        with self.voiceover(
            "There's a catch, and Richard Bellman named it: the curse of dimensionality. <bookmark mark='a'/> In "
            "many dimensions, everything is far from everything, and equally far. Scatter points in a cube: in one "
            "dimension the nearest is a tiny fraction of the average distance; "
            f"in a thousand dimensions, {100 * nnf[-1]:.0f} percent of it. <bookmark mark='b'/> To hold a tenth "
            f"of the data, a cube in ten dimensions needs sides {float(ed['10']):.2f} long: a neighbourhood that "
            "isn't local any more. <bookmark mark='c'/> On the pages, add columns of pure noise. Nearest neighbours "
            f"fall from {100 * kn0:.0f} to {100 * kn1:.0f} percent, because every noise column counts as much as "
            f"a real word. Logistic regression learns to ignore them, and falls only from {100 * lr0:.0f} to "
            f"{100 * lr1:.0f}."
        ) as vo:
            self.play(FadeIn(g1), FadeIn(t1), FadeIn(cite_))
            vo.wait_until("a")
            self.play(Create(c1), FadeIn(d1), run_time=2.0)
            vo.wait_until("b")
            self.play(FadeIn(cubes))
            vo.wait_until("c")
            self.play(FadeOut(cubes), FadeIn(g2))
            for a in art:
                self.play(FadeIn(a[0]), Create(a[1]), FadeIn(a[2]), run_time=1.2)
        self.wait(0.3)
        self.clear_scene()

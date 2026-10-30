from __future__ import annotations

import math

import numpy as np

from explainer.ai import *  # noqa: F403
from videos.ai.ai8.common import BOUND, HIST, MEAS, NEG, POS, TEST, card_body, chapter, curve, load, log_axes


class Stability(VoiceoverScene):
    def construct(self):
        chapter(self, 8, r"Compression and stability", r"Two more ways to say ``simple''",
                "Chapter eight. Compression, and stability.")
        self.compression()
        self.stability()
        self.sgd()

    # ------------------------------------------------------------------
    def compression(self):
        c = load("compress")
        X, t, w = np.asarray(c["X"]), np.asarray(c["t"]), np.asarray(c["w"])
        sv = [int(i) for i in c["sv"]]
        ax = Axes(x_range=[-3.2, 3.2, 1], y_range=[-3.2, 3.2, 1], x_length=5.4, y_length=5.4, tips=False,
                  axis_config={"stroke_color": GREY_D, "include_ticks": False}).move_to([-3.6, -0.4, 0])
        dots = VGroup(*[Dot(ax.c2p(*np.clip(p, -3.1, 3.1)), radius=0.045, color=POS if y > 0 else NEG)
                        for p, y in zip(X, t)])
        u = w / np.linalg.norm(w)
        d = np.array([-u[1], u[0]])
        line = Line(ax.c2p(*(-3.4 * d)), ax.c2p(*(3.4 * d)), color=C.BITS, stroke_width=3)
        gam = 1 / np.linalg.norm(w)
        m1 = DashedLine(ax.c2p(*(-3.4 * d + gam * u)), ax.c2p(*(3.4 * d + gam * u)), color=GREY_B, stroke_width=1.5)
        m2 = DashedLine(ax.c2p(*(-3.4 * d - gam * u)), ax.c2p(*(3.4 * d - gam * u)), color=GREY_B, stroke_width=1.5)
        rings = VGroup(*[Circle(radius=0.14, color=C.BITS, stroke_width=3).move_to(dots[i]) for i in sv])
        others = VGroup(*[dt for i, dt in enumerate(dots) if i not in sv])
        thm = theorem_card(r"sample compression",
                           card_body(r"if a learner's rule can be rebuilt from $k$ of its $n$ examples, \ and it "
                                     r"fits all $n$, \ then with probability $1 - \delta$:",
                                     r"R \le \dfrac{k \ln n + \ln(1/\delta)}{n - k}", width=5.6, font_size=21),
                           who=r"N.~Littlestone \& M.~Warmuth (1986)", width=6.4, font_size=21).to_corner(UR, buff=0.3)
        res = VGroup(
            label(rf"${c['n']}$ points, \ ${c['k']}$ support vectors: \ $R \le {c['bound']:.3f}$", font_size=24, color=BOUND),
            label(rf"VC for the same lines: \ gap $\le {c['vc']:.2f}$", font_size=22, color=GREY_A),
            label(rf"the pages: \ ${c['k_pages']}$ support vectors of ${c['n_pages']}$: \ $R \le {c['bound_pages']:.2f}$",
                  font_size=22, color=GREY_A),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.16).next_to(thm, DOWN, buff=0.35).align_to(thm, LEFT)
        same = c["same"] < 1e-6
        again = ("Throw away the rest, train again on those alone, and you get the same line, to the last digit. "
                 if same else "Train again on those alone and you get nearly the same line. ")
        with self.voiceover(
            f"A third way to say a rule is simple: it can be described by a few of its own examples. Here are "
            f"{c['n']} points, and the widest-margin line through the origin that separates them. "
            f"<bookmark mark='a'/> Only {c['k']} points touch the margin: the support vectors. "
            + again
            + "<bookmark mark='b'/> Littlestone and Warmuth showed in 1986 that such a learner generalizes like one "
            "with k parameters: its error is at most about k log n over n. <bookmark mark='c'/> Here that's "
            f"{100 * c['bound']:.1f} percent, much tighter than the VC bound for lines. On the pages the machine "
            f"needs {c['k_pages']} support vectors, and the bound is {c['bound_pages']:.2f}: a rule is only as "
            "simple as the examples it needs. Compression is also how the network bounds of the last chapter got "
            "tight: Arora and colleagues in 2018, and the language-model bounds, compress the network first."
        ) as vo:
            self.play(Create(ax), FadeIn(dots), Create(line), Create(m1), Create(m2), run_time=1.6)
            vo.wait_until("a")
            self.play(Create(rings))
            self.play(others.animate.set_opacity(0.2))
            vo.wait_until("b")
            self.play(FadeIn(thm, shift=LEFT * 0.2))
            vo.wait_until("c")
            self.play(LaggedStart(*[FadeIn(r_) for r_ in res], lag_ratio=0.4), run_time=2.0)
        self.wait(0.3)
        self.clear_scene()

    # ------------------------------------------------------------------
    def stability(self):
        s = load("stability")
        lams, st, gap = np.asarray(s["lams"]), np.asarray(s["stab"]), np.asarray(s["gap"])
        ns, stn = np.asarray(s["ns"], float), np.asarray(s["stab_n"])
        dfn = definition_card(r"uniform stability",
                              r"a learner is $\beta$-stable if replacing any one training example changes its loss "
                              r"on any point by at most $\beta$. \ Then the expected gap between true and training "
                              r"error is at most $\beta$.", width=6.2, font_size=21).to_corner(UL, buff=0.3)
        hist = history_card(2002, r"O.~Bousquet \& A.~Elisseeff", r"\textit{Stability and Generalization}: \ "
                            r"regularized learners are stable, \ $\beta \propto 1/(\lambda n)$", width=6.2,
                            font_size=18, color=HIST).next_to(dfn, DOWN, buff=0.25).align_to(dfn, LEFT)
        lo = math.floor(math.log10(min(st.min(), stn.min())) * 2) / 2
        hi = math.ceil(math.log10(max(st.max(), stn.max())) * 2) / 2
        G = log_axes((-3, 2), (lo, hi), x_length=5.2, y_length=3.0, xticks=[-3, -2, -1, 0, 1, 2], yticks=[lo, hi],
                     xlabel=r"ridge strength $\lambda$", ylabel=r"largest change in a prediction", center=(3.5, 1.3, 0),
                     font_size=18)
        ax = G.ax
        cs = VGroup(curve(ax, np.log10(lams), np.log10(st), MEAS, 3.5),
                    *[Dot(ax.c2p(math.log10(a), math.log10(b)), radius=0.04, color=MEAS) for a, b in zip(lams, st)])
        H = log_axes((1.6, 2.8), (lo, hi), x_length=5.2, y_length=2.2, xticks=[2], yticks=[lo, hi],
                     xlabel=r"training pages $n$ \ ($\lambda = 1$)", center=(3.5, -2.2, 0), font_size=18)
        hx = H.ax
        cn = VGroup(curve(hx, np.log10(ns), np.log10(stn), TEST, 3.5),
                    *[Dot(hx.c2p(math.log10(a), math.log10(b)), radius=0.05, color=TEST) for a, b in zip(ns, stn)])
        ref = DashedLine(hx.c2p(math.log10(ns[0]), math.log10(stn[0])),
                         hx.c2p(math.log10(ns[-1]), math.log10(stn[0]) - (math.log10(ns[-1]) - math.log10(ns[0]))),
                         color=GREY_B, stroke_width=2)
        rl = label(r"slope $-1$", font_size=18, color=GREY_B).next_to(ref.get_end(), UR, buff=0.05)
        slope_n = float(s["slope_n"])
        ok_n = abs(slope_n + 1) < 0.2
        close = ", close to the predicted minus one." if ok_n else ", shallower than the predicted minus one."
        with self.voiceover(
            "A fourth: a rule is safe if it doesn't depend much on any single example. <bookmark mark='a'/> Call a "
            "learner beta-stable if swapping one training example for another changes its loss anywhere by at most "
            "beta. Then, on average, its true error exceeds its training error by at most beta, because swapping a "
            "training example for a fresh one is exactly how a training point turns into a test point. "
            "<bookmark mark='b'/> Bousquet and Elisseeff showed in 2002 that regularized learners are stable, with "
            "beta like one over lambda n. <bookmark mark='c'/> Measure it for ridge regression on the pages: swap one "
            "training page for a held-out one, and see how far any prediction moves. Stronger regularization, "
            f"smaller change. <bookmark mark='d'/> And against n, the slope is {slope_n:.2f}"
            + close
        ) as vo:
            self.play(FadeIn(G))
            vo.wait_until("a")
            self.play(FadeIn(dfn, shift=DOWN * 0.2))
            vo.wait_until("b")
            self.play(FadeIn(hist, shift=UP * 0.2))
            vo.wait_until("c")
            self.play(Create(cs), run_time=1.6)
            vo.wait_until("d")
            self.play(FadeIn(H), Create(ref), FadeIn(rl), Create(cn), run_time=1.6)
        self.wait(0.3)
        self.clear_scene()

    # ------------------------------------------------------------------
    def sgd(self):
        s = load("stability")
        runs = np.asarray(s["sgd"])
        mean, hardt = np.asarray(s["sgd_mean"]), np.asarray(s["hardt"])
        E = int(s["epochs"])
        ep = np.arange(E + 1)
        G = axes([0, E], [0, 0.12], x_length=6.2, y_length=4.0, xticks=[0, 10, 20, 30], yticks=[0, 0.04, 0.08, 0.12],
                 xlabel=r"passes over the data", ylabel=r"$|w - w'|$: \ distance between the two runs",
                 center=(-2.6, -0.5, 0))
        ax = G.ax
        rc = VGroup(*[curve(ax, ep, r_, MEAS, 1.2).set_stroke(opacity=0.35) for r_ in runs])
        mc = curve(ax, ep, mean, MEAS, 4)
        k1 = int(np.searchsorted(hardt, 0.12))
        hc = curve(ax, ep[:k1], hardt[:k1], BOUND, 3.5)
        hl = label(rf"bound $2\eta G\,T/n$: \ ${hardt[-1]:.1f}$ after ${E}$ passes", font_size=20, color=BOUND)
        hl.next_to(hc.get_end(), RIGHT, buff=0.1)
        keep_in_frame(hl)
        mean_end = float(mean[-1])
        head = label(r"SGD twice, \ same order of examples; \ the training sets differ in one page", font_size=26)
        head.to_edge(UP, buff=0.35)
        hist = history_card(2016, r"M.~Hardt, B.~Recht \& Y.~Singer", r"\textit{Train Faster, Generalize Better}: \ "
                            r"SGD on convex losses is stable \ if it doesn't run too long", width=5.0, font_size=18,
                            color=HIST).to_corner(DR, buff=0.3)
        ratio = hardt[-1] / max(mean_end, 1e-12)
        with self.voiceover(
            "Stability also applies to training itself. Run stochastic gradient descent twice, visiting the examples "
            "in the same order, on two training sets that differ in one page. <bookmark mark='a'/> The runs drift "
            f"apart only when they meet the differing page: after {E} passes, by {mean_end:.3f} on average, over "
            "twenty such pairs. <bookmark mark='b'/> Hardt, Recht and Singer proved in 2016 that, for convex losses, "
            "the drift grows at most in proportion to the step size times the number of steps, over n: train faster, "
            f"generalize better. Here the bound is about {ratio:.0f} times the measured drift; true, and loose. "
            "For networks, which aren't convex, nothing this clean holds, and that's where the puzzles start."
        ) as vo:
            self.play(FadeIn(head), FadeIn(G))
            vo.wait_until("a")
            self.play(LaggedStart(*[Create(r_) for r_ in rc], lag_ratio=0.05), Create(mc), run_time=2.5)
            vo.wait_until("b")
            self.play(Create(hc), FadeIn(hl), FadeIn(hist, shift=UP * 0.2))
        self.wait(0.3)
        self.clear_scene()

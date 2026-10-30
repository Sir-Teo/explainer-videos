from __future__ import annotations

import math

import numpy as np

from explainer.ai import *  # noqa: F403
from videos.ai.ai8.common import BOUND, HIST, MEAS, TEST, TRAIN, chapter, curve, load


class Margins(VoiceoverScene):
    def construct(self):
        chapter(self, 6, r"Margins", r"Can a confident fit be a simple one?",
                "Chapter six. Margins.", lit=(1995,))
        self.margins()
        self.bound()
        self.boosting()

    # ------------------------------------------------------------------
    def margins(self):
        m = load("margins")
        mg = np.asarray(m["margins"])
        n = int(m["n"])
        G = axes([0, 0.5], [0, 1], x_length=6.4, y_length=4.2, xticks=[0, 0.1, 0.2, 0.3, 0.4, 0.5],
                 yticks=[0, 0.25, 0.5, 0.75, 1], yfmt=lambda v: rf"{100 * v:.0f}\%",
                 xlabel=r"margin $\gamma$, \ in units of the largest $|x|$",
                 ylabel=r"share of training pages with margin $< \gamma$", center=(-2.9, -0.5, 0))
        ax = G.ax
        xs = np.linspace(0, 0.5, 200)
        cdf = np.array([(mg < x).mean() for x in xs])
        c = curve(ax, xs, cdf, MEAS, 4)
        # a picture: a line, two classes, and the gap
        pic = VGroup()
        g = np.random.default_rng(3)
        a_ = Axes(x_range=[-2, 2, 1], y_range=[-2, 2, 1], x_length=3.2, y_length=3.2, tips=False,
                  axis_config={"stroke_color": GREY_D, "include_ticks": False})
        for s in (1, -1):
            for _ in range(9):
                p = np.array([s * (0.55 + abs(g.normal(0.6, 0.35))), g.normal(0, 0.8)])
                pic.add(Dot(a_.c2p(*np.clip(p, -1.9, 1.9)), radius=0.06, color="#58A6FF" if s > 0 else "#E86F8A"))
        line = Line(a_.c2p(0, -2), a_.c2p(0, 2), color=C.BITS, stroke_width=3)
        lm = DashedLine(a_.c2p(0.55, -2), a_.c2p(0.55, 2), color=GREY_B, stroke_width=1.5)
        rm = DashedLine(a_.c2p(-0.55, -2), a_.c2p(-0.55, 2), color=GREY_B, stroke_width=1.5)
        br = BraceBetweenPoints(a_.c2p(0, 1.75), a_.c2p(0.55, 1.75), UP, color=GREY_A)
        gl = MathTex(r"\gamma", font_size=28, color=GREY_A).next_to(br, UP, buff=0.05)
        P = VGroup(a_, pic, lm, rm, line, br, gl).move_to([4.1, 1.4, 0])
        dfn = definition_card(r"margin",
                              r"$\gamma_i = y_i\, w \cdot x_i \,/\, (|w|\, R)$: \ how far example $i$ sits on the "
                              r"right side of the boundary. \ Margin loss $\hat R_\gamma(h)$: \ the share with "
                              r"margin below $\gamma$.", width=5.4, font_size=20).move_to([4.0, -2.0, 0])
        with self.voiceover(
            "The Rademacher bound for linear rules depends on the weights' length, not on how many there are. To "
            "use that, measure how confidently a rule separates the data: its margin, the distance from each "
            "example to the boundary, on the right side of it. <bookmark mark='a'/> The support vector machine from "
            "part six chooses the line with the widest margin. <bookmark mark='b'/> On the pages it separates all "
            f"{n} training pages, and here is the distribution of their margins: the closest page sits at "
            f"{m['min_margin']:.3f} of the largest input's length. <bookmark mark='c'/> The margin loss at gamma "
            "counts the pages closer than gamma to the boundary: the share a rule gets right, but not "
            "confidently."
        ) as vo:
            self.play(FadeIn(a_), FadeIn(pic), Create(line))
            vo.wait_until("a")
            self.play(Create(lm), Create(rm), FadeIn(br), FadeIn(gl))
            vo.wait_until("b")
            self.play(FadeIn(G), Create(c), run_time=1.6)
            vo.wait_until("c")
            self.play(FadeIn(dfn, shift=UP * 0.2))
        self.wait(0.3)
        self.clear_scene()

    # ------------------------------------------------------------------
    def bound(self):
        m = load("margins")
        rows = [
            cmath(r"\mathbf{1}[\,y\,h(x) \le 0\,]", r"\le", r"\phi_\gamma\big(y\,h(x)\big)", r"\le",
                  r"\mathbf{1}[\,y\,h(x) < \gamma\,]", font_size=30),
            cmath(r"R(h)", r"\le", r"\hat R_\gamma(h) + 2\,\hat{\mathfrak R}_S(\phi_\gamma \circ \mathcal H) + "
                  r"3\sqrt{\tfrac{\ln(2/\delta)}{2n}}", font_size=30),
            cmath(r"R(h)", r"\le", r"\hat R_\gamma(h) + \frac{2BR}{\gamma\sqrt n} + 3\sqrt{\tfrac{\ln(2/\delta)}{2n}}",
                  font_size=32, colors={r"\hat R_\gamma(h) + \frac{2BR}{\gamma\sqrt n} + 3\sqrt{\tfrac{\ln(2/\delta)}{2n}}": BOUND}),
        ]
        whys = [why(r"the ramp $\phi_\gamma$: \ $1$ below $0$, \ $0$ above $\gamma$"),
                why(r"chapter 5, \ for the ramp loss"),
                why(r"$\phi_\gamma$ is $\tfrac1\gamma$-Lipschitz: \ contraction; \ chapter 5's $BR/\sqrt n$")]
        step = ladder(self, rows, whys, keep=3, top=3.3, x=-2.6, buff=0.36, edge=6.9)
        gm = np.asarray(m["gammas"])
        emp, cpx, bd = np.asarray(m["emp"]), np.asarray(m["cplx"]), np.asarray(m["bound"])
        top = 2.0
        G = axes([math.log10(gm[0]), math.log10(gm[-1])], [0, top], x_length=6.2, y_length=3.0,
                 xticks=[-2, -1.5, -1, -0.5], xfmt=lambda v: f"{10 ** v:.2g}", yticks=[0, 0.5, 1, 1.5, 2],
                 xlabel=r"$\gamma$ \ (log scale)", center=(-2.6, -1.9, 0), font_size=18)
        ax = G.ax
        lg = np.log10(gm)
        ce = curve(ax, lg, emp, MEAS, 3.5)
        cc = curve(ax, lg, np.clip(cpx, 0, top), GREY_B, 3)
        cb = curve(ax, lg, np.clip(bd, 0, top), BOUND, 4)
        half = DashedLine(ax.c2p(lg[0], 0.5), ax.c2p(lg[-1], 0.5), color=C.SURPRISE, stroke_width=2)
        hl = label(r"chance", font_size=18, color=C.SURPRISE).next_to(half, RIGHT, buff=0.08)
        k = int(np.argmin(bd))
        dot = Dot(ax.c2p(lg[k], min(bd[k], top)), radius=0.08, color=BOUND)
        key = legend([(MEAS, r"$\hat R_\gamma$: \ margin loss"), (GREY_B, r"$2BR/(\gamma\sqrt n)$"),
                      (BOUND, r"the bound")], font_size=19).next_to(G, RIGHT, buff=0.4).align_to(G, UP)
        res = VGroup(
            label(rf"best: \ ${m['best_bound']:.2f}$ \ at $\gamma = {m['best_gamma']:.2f}$", font_size=24, color=BOUND),
            label(rf"VC, \ $d = 71$: \ ${m['vc']:.2f}$ \ (gap alone)", font_size=22, color=GREY_A),
            label(rf"below $0.5$ \ with the same margins: \ $n \approx {fmt_int(m['n_half'])}$", font_size=22,
                  color=GREY_A),
            label(rf"actual test error: \ ${100 * (1 - m['test_acc']):.1f}\%$", font_size=22, color=TEST),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.14).next_to(key, DOWN, buff=0.35).align_to(key, LEFT)
        vac = m["best_bound"] >= 0.5
        hist = history_card(1998, r"P.~Bartlett", r"\textit{The size of the weights is more important than the size "
                            r"of the network}", width=5.2, font_size=18, color=HIST).to_corner(UR, buff=0.25)
        with self.voiceover(
            "The bound comes in three steps. <bookmark mark='a'/> Replace the error, one when the margin is "
            "negative, with a ramp that's one below zero and zero above gamma; it lies between the error and the "
            "margin loss. <bookmark mark='b'/> Apply the Rademacher bound to the ramp. <bookmark mark='c'/> The ramp "
            "has slope one over gamma, and a contraction lemma says a Lipschitz function scales the complexity by its "
            "slope: the gap is two B R over gamma root n. The number of inputs never appears. Peter Bartlett made "
            "this the point in 1998: the size of the weights matters more than the number of them. "
            "<bookmark mark='d'/> Now compute it on the pages. Small gamma: no margin loss, but a huge complexity "
            "term. Large gamma: the reverse. "
            + (f"The best trade-off gives {m['best_bound']:.2f}, more than a coin's error rate: vacuous, while the "
               f"actual test error is {100 * (1 - m['test_acc']):.1f} percent. With the same margins it would take "
               f"about {int(m['n_half']):,} pages. Our 448 aren't enough for the margin, either."
               if vac else
               f"The best trade-off gives {m['best_bound']:.2f}, below a coin's error rate, against an actual test "
               f"error of {100 * (1 - m['test_acc']):.1f} percent.")
        ) as vo:
            step(0)
            vo.wait_until("a")
            self.play(Indicate(rows[0][2], color=WHITE, scale_factor=1.04))
            vo.wait_until("b")
            step(1)
            vo.wait_until("c")
            step(2)
            self.play(FadeIn(hist, shift=LEFT * 0.2))
            vo.wait_until("d")
            self.play(FadeOut(hist), FadeIn(G), Create(ce), Create(cc), FadeIn(key[:2]), Create(half), FadeIn(hl))
            self.play(Create(cb), FadeIn(key[2]), FadeIn(dot))
            self.play(LaggedStart(*[FadeIn(r_) for r_ in res], lag_ratio=0.4), run_time=2.0)
        self.wait(0.3)
        self.clear_scene()

    # ------------------------------------------------------------------
    def boosting(self):
        m = load("margins")
        tr, te = np.asarray(m["ada_tr"]), np.asarray(m["ada_te"])
        T = int(m["ada_T"])
        zero = int(m["ada_zero"]) if m["ada_zero"] is not None else None
        G = axes([0, math.log10(T)], [0, 0.12], x_length=5.6, y_length=3.6, xticks=[0, 1, 2],
                 xfmt=lambda v: f"{10 ** v:.0f}", yticks=[0, 0.04, 0.08, 0.12], yfmt=lambda v: rf"{100 * v:.0f}\%",
                 xlabel=r"boosting rounds \ (log scale)", center=(-3.4, -0.4, 0))
        ax = G.ax
        rr = np.arange(1, T + 1)
        ctr = curve(ax, np.log10(rr), np.clip(tr, 0, 0.12), TRAIN, 3)
        cte = curve(ax, np.log10(rr), np.clip(te, 0, 0.12), TEST, 4)
        key = legend([(TRAIN, r"training error"), (TEST, r"error on new pages")], font_size=20)
        key.next_to(G, UP, buff=0.1).align_to(G, RIGHT)
        snaps = [int(s) for s in m["ada_snaps"]]
        H = axes([-1, 1], [0, 1], x_length=5.4, y_length=3.6, xticks=[-1, -0.5, 0, 0.5, 1], yticks=[0, 0.5, 1],
                 yfmt=lambda v: rf"{100 * v:.0f}\%", xlabel=r"normalized margin $y \sum_t \alpha_t h_t(x) / "
                 r"\sum_t \alpha_t$", center=(3.4, -0.4, 0))
        hx = H.ax
        cols = [GREY_C, GREY_B, C.MODEL_Q, C.BITS]
        cdfs = VGroup()
        for s, cl in zip(snaps, cols):
            v = np.asarray(m[f"cdf{s}"])
            cdfs.add(VMobject(color=cl, stroke_width=3.5).set_points_as_corners(
                [hx.c2p(-1, 0)] + [hx.c2p(float(x), (i + 1) / len(v)) for i, x in enumerate(v)] + [hx.c2p(1, 1)]))
        hkey = legend([(cl, rf"round ${s}$") for s, cl in zip(snaps, cols)], font_size=18)
        hkey.next_to(hx.c2p(-1, 1), DR, buff=0.15)
        head = label(r"AdaBoost on the pages: \ $70$ word rates, \ one-cut ``stumps''", font_size=28).to_edge(UP, buff=0.35)
        hist = history_card(1998, r"R.~Schapire, Y.~Freund, P.~Bartlett \& W.~S.~Lee", r"\textit{Boosting the Margin}: "
                            r"test error keeps falling after training error reaches zero, \ because margins grow",
                            width=6.2, font_size=18, color=HIST).to_corner(DR, buff=0.2)
        if zero is not None:
            after = te[zero - 1:]
            kmin = zero - 1 + int(np.argmin(after))
            fell = te[kmin] < te[zero - 1] - 1e-9
        else:
            fell = False
        with self.voiceover(
            "Margins first explained a puzzle twenty years before deep learning's. Boosting builds a classifier from "
            "many weak ones, here single cuts on one word rate each, reweighting the examples it gets wrong. "
            "<bookmark mark='a'/> "
            + (f"On the pages, its training error reaches zero at round {zero}. " if zero is not None else
               "On the pages, its training error falls quickly. ")
            + "<bookmark mark='b'/> "
            + ("By the classical story, it should stop improving there, or start to overfit. "
               f"Instead the error on new pages keeps falling, from {100 * te[zero - 1]:.1f} percent at round {zero} "
               f"to {100 * te[kmin]:.1f} at round {kmin + 1}, "
               + (f"and ends at {100 * te[-1]:.1f} after {T}. " if abs(te[-1] - te[kmin]) > 1e-9 else "and stays there. ")
               if fell else
               "After that, the error on new pages stays about where it was. ")
            + "<bookmark mark='c'/> The explanation, by Schapire, Freund, Bartlett and Lee in 1998: with the training "
            "points all correct, later rounds keep pushing their margins outward, and the margin bound only cares "
            "about margins. The same shape, more training past zero training error and better on new data, is "
            "about to come back for neural networks."
        ) as vo:
            self.play(FadeIn(head), FadeIn(G), FadeIn(key))
            vo.wait_until("a")
            self.play(Create(ctr), run_time=1.5)
            vo.wait_until("b")
            self.play(Create(cte), run_time=2.0)
            vo.wait_until("c")
            self.play(FadeIn(H), FadeIn(hkey))
            self.play(LaggedStart(*[Create(c_) for c_ in cdfs], lag_ratio=0.6), run_time=3.0)
            self.play(FadeIn(hist, shift=UP * 0.2))
        self.wait(0.3)
        self.clear_scene()

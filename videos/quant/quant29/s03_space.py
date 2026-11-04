from __future__ import annotations

import numpy as np

from explainer.quant import *  # noqa: F403
from videos.quant.quant29.common import FORMULA, HURDLE, PART, fit_right, load, sci


class Space(VoiceoverScene):
    def construct(self):
        s = load("space")
        self.card()
        self.recursion(s)
        self.growth(s)
        self.question()

    def card(self):
        c = chapter_card(2, r"The search space", r"How many formulas are there?", part=PART)
        with self.voiceover("Chapter two. If signals are trees, how many trees are there to search?"):
            self.play(FadeIn(c[0], shift=UP * 0.2), FadeIn(c[1]))
        self.play(FadeOut(c))

    def recursion(self, s):
        nf, nu, nt, nb, nw = len(s["fields"]), len(s["unary"]), len(s["ts"]), len(s["binary"]), len(s["windows"])
        rows = [cmath(r"N_1", r"=", rf"{nf}\ \text{{fields}}", font_size=34, colors={r"N_1": FORMULA}),
                cmath(r"N_d", r"=", rf"N_1 + {nu}\,N_{{d-1}} + {nt}\cdot{nw}\,N_{{d-1}} + ({nb} + {nw})\,N_{{d-1}}^2", font_size=32,
                      colors={r"N_d": FORMULA}),
                cmath(r"N_d", r"\approx", r"c\,N_{d-1}^2 \ \Rightarrow\ \log N_d \sim 2^d", font_size=34, colors={r"N_d": HURDLE})]
        whys = [why(r"a tree of depth one is a single field"),
                why(rf"a tree of depth at most $d$ is a field, or a one-argument operator ({nu} of them) on a smaller tree, "
                    rf"or a time-series operator ({nt}) with one of {nw} windows, or a two-argument one ({nb} arithmetic, "
                    r"and \texttt{corr} with a window) on two smaller trees"),
                why(r"the square term wins: the count is doubly exponential in depth")]
        step = ladder(self, rows, whys, keep=3, top=2.6, x=-0.3, buff=0.5, edge=6.9)
        with self.voiceover(
            "Count them. <bookmark mark='a'/> A tree of depth one is a single field: six of them. <bookmark mark='b'/> "
            "A tree of depth d is a field, or an operator applied to smaller trees: one argument, or a time-series "
            "operator with one of four windows, or two arguments. <bookmark mark='c'/> The two-argument term squares "
            "the previous count, so the number of trees grows doubly exponentially with depth."
        ) as vo:
            step(0)
            vo.wait_until("a")
            self.wait(0.1)
            vo.wait_until("b")
            step(1)
            vo.wait_until("c")
            step(2)
        self.wait(0.5)
        self.clear_scene()

    def growth(self, s):
        cnt = np.asarray(s["count"], float)
        lg = np.log10(cnt)
        g = axes([0.5, 6.5], [0, 60], x_length=7.4, y_length=4.4, xlabel=r"maximum depth of the tree",
                 ylabel=r"number of distinct formulas (log$_{10}$)", xticks=[1, 2, 3, 4, 5, 6], yticks=[0, 20, 40, 60],
                 font_size=15).move_to(LEFT * 2.0 + DOWN * 0.2)
        ax = g.ax
        bars = VGroup(*[Rectangle(width=0.6, height=max(ax.c2p(0, v)[1] - ax.c2p(0, 0)[1], 0.02), stroke_width=0,
                                  fill_color=FORMULA, fill_opacity=0.85).move_to([ax.c2p(k + 1, 0)[0],
                                                                                 (ax.c2p(0, 0)[1] + ax.c2p(0, v)[1]) / 2, 0])
                        for k, v in enumerate(lg)])
        tags = VGroup(*[MathTex(sci(v) if v >= 1e4 else f"{v:,.0f}".replace(",", "{,}"), font_size=18).next_to(b, UP, buff=0.08)
                        for v, b in zip(cnt, bars)])
        side = wrapped_label(r"at a hundred formulas a second, depth 3 takes about 5.4 hours; depth 4 about ten thousand "
                             r"years. Search cannot be exhaustive: it must be guided, and every step it takes is a trial",
                             3.6, 16, GREY_A).to_edge(RIGHT, buff=0.35)
        fit_right(side)
        with self.voiceover(
            f"The numbers. <bookmark mark='a'/> Six formulas of depth one; {cnt[1]:,.0f} of depth two; about two million "
            f"of depth three; about three times ten to the thirteen of depth four. <bookmark mark='b'/> Depth six gives "
            "around ten to the fifty-six. No computer will ever evaluate them all. So search has to be guided: random, "
            "evolutionary, learned, or written by a language model. And every formula it evaluates is a trial, which "
            "Part twenty-six taught us to count."
        ) as vo:
            self.play(FadeIn(g))
            vo.wait_until("a")
            self.play(LaggedStart(*[GrowFromEdge(b, DOWN) for b in bars[:4]], lag_ratio=0.3),
                      LaggedStart(*[FadeIn(t_) for t_ in tags[:4]], lag_ratio=0.3))
            vo.wait_until("b")
            self.play(GrowFromEdge(bars[4], DOWN), GrowFromEdge(bars[5], DOWN), FadeIn(tags[4]), FadeIn(tags[5]),
                      FadeIn(side))
        self.wait(0.4)
        self.clear_scene()

    def question(self):
        q = pause_card(r"a million machines each evaluate 100 formulas a second. How long to try every formula of "
                       r"depth 5?")
        with self.voiceover(
            "Pause and predict. A million machines each evaluate a hundred formulas a second. How long to try every "
            "formula of depth five?"
        ):
            self.play(FadeIn(q))
        self.wait(0.5)
        self.clear_scene()

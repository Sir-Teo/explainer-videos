from __future__ import annotations

import math

import numpy as np

from explainer.analysis import *  # noqa: F403
from videos.analysis8.common import load, rationals_in


class Baire(VoiceoverScene):
    def construct(self):
        self.card()
        self.nested()
        self.meager()

    # ------------------------------------------------------------------
    def card(self):
        card = chapter_card(3, r"Baire's theorem", r"Can a complete space be a countable union of thin sets?", lit=(), part=8)
        with self.voiceover("Chapter three: Baire's category theorem, the root of three of the four pillars."):
            self.play(FadeIn(card[0], shift=UP * 0.2), FadeIn(card[1]))
        self.play(FadeOut(card))

    # ------------------------------------------------------------------
    def nested(self):
        d = load("baire")
        rats, ivs, x = d["rats"], d["ivs"], float(d["x"])
        L, R_ = -6.0, 6.0

        def X(t):
            return L + (R_ - L) * t

        line = Line([L, 0.6, 0], [R_, 0.6, 0], color=GREY_B, stroke_width=2)
        ends = VGroup(MathTex("0", font_size=24).next_to([L, 0.6, 0], DOWN, buff=0.15),
                      MathTex("1", font_size=24).next_to([R_, 0.6, 0], DOWN, buff=0.15))
        ticks = VGroup(*[Line([X(q), 0.45, 0], [X(q), 0.75, 0], color=C.RATIONAL, stroke_width=2) for q in rats[:30]])
        q_l = VGroup(*[MathTex(rf"q_{{{k + 1}}}", font_size=20, color=C.RATIONAL).next_to([X(q), 0.75, 0], UP, buff=0.05)
                       for k, q in enumerate(rats[:4])])
        bars = [Line([X(a), 0.2 - 0.0 * k, 0], [X(b), 0.2, 0], color=C.EPS, stroke_width=8) for k, (a, b) in enumerate(ivs)]
        # a zoom: the last intervals are tiny, so show their lengths
        lens = [b - a for a, b in ivs]
        readout = [MathTex(rf"I_{{{k + 1}}}: \ \text{{length }} 3^{{-{k + 1}}} = {sci(lens[k], 1)}, \ q_{{{k + 1}}} = "
                           rf"{rats[k]:.4f} \notin I_{{{k + 1}}}", font_size=26, color=C.EPS).move_to([0, -0.6, 0])
                   for k in range(len(ivs))]
        xl = MathTex(rf"\bigcap_n I_n = \{{{x:.10f}\ldots\}}", font_size=32, color=C.EPS).move_to([0, -1.5, 0])
        assert all(not (a <= q <= b) for (a, b), q in zip(ivs, rats))
        thm = VGroup(
            label(r"\textbf{RCA 5.6} \ (Baire) \ a complete metric space is not a countable union of nowhere dense sets",
                  font_size=24, color=C.EPS),
            label(r"proof: \ nested closed balls, \ each dodging one more thin set; \ completeness gives a point in all of them",
                  font_size=22, color=GREY_A),
            label(r"here the thin sets are the rationals $\{q_1\}, \{q_2\}, \ldots$: \ so $\R$ is uncountable \ (a third proof)",
                  font_size=22),
        ).arrange(DOWN, buff=0.12).to_edge(DOWN, buff=0.3)
        head = label(r"Dodge the rationals one at a time", font_size=34).to_edge(UP, buff=0.3)
        with self.voiceover(
            "<bookmark mark='a'/> List the rationals between zero and one: q one, q two, and so on. Can the list be "
            "all the real numbers? <bookmark mark='b'/> Pick a closed third of the interval that misses q one. Inside "
            "it, a closed third that misses q two. And so on: the intervals shrink by a factor of three each time, "
            "each one dodging one more rational. <bookmark mark='c'/> Because the real line is complete, the nested "
            "intervals close in on a real number, and it's none of the q n. <bookmark mark='d'/> That's Baire's "
            "theorem in miniature: a complete metric space can't be a countable union of nowhere dense sets. The "
            "proof is always this: nested closed balls, each avoiding one more thin set, and completeness to finish."
        ) as vo:
            vo.wait_until("a")
            self.play(FadeIn(head), Create(line), FadeIn(ends), LaggedStart(*[Create(t_) for t_ in ticks], lag_ratio=0.03),
                      FadeIn(q_l))
            vo.wait_until("b")
            self.play(Create(bars[0]), FadeIn(readout[0]))
            for k in range(1, 6):
                self.play(Create(bars[k]), bars[k - 1].animate.set_stroke(opacity=0.3),
                          FadeTransform(readout[k - 1], readout[k]), run_time=0.8)
            for k in range(6, len(bars)):
                self.add(bars[k])
            self.play(FadeTransform(readout[5], readout[-1]))
            vo.wait_until("c")
            self.play(FadeIn(xl), Flash([X(x), 0.2, 0], color=C.EPS))
            vo.wait_until("d")
            self.play(FadeIn(thm))
        self.wait(0.3)
        self.clear_scene()

    # ------------------------------------------------------------------
    def meager(self):
        d = load("baire")
        rats, eps, measures = d["rats"], d["eps"], d["measures"]
        L, R_ = -6.6, 2.4

        def X(t):
            return L + (R_ - L) * t

        rows_y = [1.3, 0.3, -0.7]
        lines = VGroup()
        covers = VGroup()
        labs = VGroup()
        for e, m, y in zip(eps, measures, rows_y):
            lines.add(Line([L, y, 0], [R_, y, 0], color=GREY_D, stroke_width=1.5))
            g = VGroup()
            for k, q in enumerate(rats):
                r = e * 2.0 ** (-(k + 1)) / 2
                g.add(Line([X(max(0, q - r)), y, 0], [X(min(1, q + r)), y, 0], color=C.MEASURE, stroke_width=10))
            covers.add(g)
            labs.add(MathTex(rf"U: \ \varepsilon = {e}, \ m(U) \le {e} \ ({m:.4f})", font_size=24, color=C.MEASURE).next_to(
                [R_, y, 0], RIGHT, buff=0.2))
        assert np.all(measures <= eps + 1e-3) and labs.get_right()[0] < 6.9
        defs = VGroup(
            label(r"\emph{nowhere dense}: \ closure has empty interior; \ \emph{meager}: \ a countable union of those",
                  font_size=24),
            label(r"each $U_\varepsilon$ is open and dense \ (it contains every rational); \ $G = \bigcap_n U_{1/n}$ "
                  r"is a dense $G_\delta$", font_size=24),
            label(r"so $G$ is \emph{residual}: \ ``almost all'' of $[0, 1]$ to Baire, \ yet $m(G) = 0$", font_size=26,
                  color=C.PATHOLOGY),
            label(r"two meanings of ``most'', \ and they disagree", font_size=24, color=C.EPS),
        ).arrange(DOWN, buff=0.14).to_edge(DOWN, buff=0.3)
        head = label(r"Meager and residual: \ Baire's notion of ``small'' and ``almost everything''", font_size=30).to_edge(
            UP, buff=0.3)
        # a meager set to look at first: the rationals, each point nowhere dense, countably many of them
        ticks = VGroup(*[VGroup(*[Line([X(q), y - 0.12, 0], [X(q), y + 0.12, 0], color=GREY_A, stroke_width=1.5)
                                  for q in rats]) for y in rows_y])
        q_l = MathTex(r"\mathbb Q \cap [0, 1]: \ \text{countably many points, each nowhere dense: meager}", font_size=26,
                      color=GREY_A).next_to([L, rows_y[0] + 0.45, 0], RIGHT, buff=0)
        assert q_l.get_right()[0] < 6.9 and q_l.get_top()[1] < head.get_bottom()[1] - 0.2
        with self.voiceover(
            "<bookmark mark='a'/> Baire's theorem gives a notion of size. A set is meager if it's a countable union of "
            "nowhere dense sets, and residual if its complement is meager. In a complete space, residual sets are "
            "dense: in Baire's sense, they're almost everything. <bookmark mark='b'/> It's a different notion from "
            "measure. Put a tiny open interval around each rational, of total length epsilon. The union is open and "
            "dense, but its length is at most epsilon. <bookmark mark='c'/> Intersect these sets as epsilon goes to "
            "zero. The result is a dense G delta, residual, almost everything to Baire, and it has measure zero. "
            "Two meanings of most, and they disagree."
        ) as vo:
            vo.wait_until("a")
            self.play(FadeIn(head), FadeIn(defs[0]))
            self.play(Create(lines), LaggedStart(*[FadeIn(t_) for t_ in ticks], lag_ratio=0.2), FadeIn(q_l), run_time=1.6)
            vo.wait_until("b")
            self.play(FadeOut(q_l))
            for k in range(3):
                self.play(FadeIn(covers[k]), FadeIn(labs[k]), run_time=1.0)
            self.play(FadeIn(defs[1]))
            vo.wait_until("c")
            self.play(FadeIn(defs[2]))
            self.play(FadeIn(defs[3]))
        self.wait(0.4)
        self.clear_scene()

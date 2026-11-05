from __future__ import annotations

import math

from explainer.cs import *  # noqa: F403
from videos.cs.cs16.common import (CODE, COST, CTRL, DATA, FUNC, HEAD, LAM, NO, PART, YES, load, mono, words)


class Concentration(VoiceoverScene):
    def construct(self):
        self.card()
        self.recurrence()
        self.histogram()
        self.tails()

    def card(self):
        card = chapter_card(9, r"How lucky can quicksort get?", r"Is the average what you will see?", lit=(1952,),
                            extra=((1952, r"Chernoff's bound"),), part=PART)
        with self.voiceover("Chapter nine. How lucky can quicksort get?"):
            self.play(FadeIn(card[0], shift=UP * 0.2), FadeIn(card[1]), FadeIn(card[2]))
        self.play(FadeOut(card))

    def recurrence(self):
        head = label(r"The same answer, \ from the recurrence", font_size=34).to_edge(UP, buff=0.3)
        steps = VGroup(
            MathTex(r"C_n = n - 1 + \frac{2}{n} \sum_{k=0}^{n-1} C_k", font_size=34),
            label(r"the pivot's rank is uniform: \ each side is $C_k$ for a uniform $k$", font_size=20, color=GREY_B),
            MathTex(r"n C_n - (n-1) C_{n-1} = 2(n-1) + 2 C_{n-1}", font_size=32),
            MathTex(r"\frac{C_n}{n+1} = \frac{C_{n-1}}{n} + \frac{2(n-1)}{n(n+1)}", font_size=32),
            MathTex(r"\frac{C_n}{n+1} = \sum_{k=1}^{n} \frac{2(k-1)}{k(k+1)} \;\Rightarrow\; C_n = 2(n+1)H_n - 4n",
                    font_size=32, color=YES),
            label(r"multiply by $n$, \ subtract the same line for $n - 1$, \ divide, \ telescope", font_size=20,
                  color=GREY_B),
        ).arrange(DOWN, buff=0.22).next_to(head, DOWN, buff=0.4)
        with self.voiceover(
            "Before measuring the spread, here is the classical way to get the mean, which uses no clever "
            "observation, only algebra. <bookmark mark='a'/> The pivot's rank is uniformly random, so the two "
            "sides have sizes k and n minus one minus k for a uniform k, and the expected cost is n minus one "
            "plus two over n times the sum of all smaller costs. <bookmark mark='b'/> Multiply by n, and subtract "
            "the same equation for n minus one: the sum disappears, leaving a relation between neighbours. "
            "<bookmark mark='c'/> Divide by n times n plus one and the relation telescopes. <bookmark mark='d'/> "
            "Summing it gives the same exact answer as before, two times n plus one times H n, minus four n. Two "
            "proofs, one number."
        ) as vo:
            self.play(FadeIn(head))
            vo.wait_until("a")
            self.play(Write(steps[0]), FadeIn(steps[1]))
            vo.wait_until("b")
            self.play(Write(steps[2]))
            vo.wait_until("c")
            self.play(Write(steps[3]))
            vo.wait_until("d")
            self.play(Write(steps[4]), FadeIn(steps[5]))
        self.wait(0.3)
        self.clear_scene()

    def histogram(self):
        d = load("concentration")
        head = label(rf"{words(d['runs'])} runs of quicksort, \ $n = {words(d['n'])}$", font_size=34).to_edge(
            UP, buff=0.3)
        hist, edges = d["hist"], d["edges"]
        mx = max(hist)
        ax = Axes(x_range=[edges[0], edges[-1], 1000], y_range=[0, mx * 1.1, mx / 2], x_length=10.0, y_length=4.0,
                  axis_config={"color": GREY_D, "include_numbers": False}).move_to(DOWN * 0.3)
        bars = VGroup()
        for h, a, b in zip(hist, edges[:-1], edges[1:]):
            p0, p1 = ax.c2p(a, 0), ax.c2p(b, h)
            bars.add(Rectangle(width=p1[0] - p0[0] - 0.01, height=max(p1[1] - p0[1], 0.01), stroke_width=0,
                               fill_color=DATA, fill_opacity=0.85).move_to([(p0[0] + p1[0]) / 2, (p0[1] + p1[1]) / 2, 0]))
        mean = DashedLine(ax.c2p(d["mean"], 0), ax.c2p(d["mean"], mx * 1.05), color=HEAD, stroke_width=2)
        ml = label(rf"mean {d['mean']:,.0f} \ (exact: {d['exact_mean']:,.0f})", font_size=19, color=HEAD).next_to(
            mean, UP, buff=0.08)
        ticks = VGroup(*[label(f"{v:,}", font_size=15, color=GREY_B).next_to(ax.c2p(v, 0), DOWN, buff=0.1)
                         for v in range(10000, int(edges[-1]) + 1, 1000)])
        xl = label(r"comparisons in one run", font_size=18, color=GREY_B).next_to(ticks, DOWN, buff=0.12)
        cap = VGroup(
            label(rf"standard deviation {d['sd']:,.0f}: \ {d['sd_over_n']:.3f}\,$n$; \ theory: \ "
                  rf"$\sqrt{{7 - 2\pi^2/3}}\,n = {d['theory_sd_over_n']:.3f}\,n$", font_size=21, color=GREY_A),
            label(rf"the worst run of ten thousand: \ {d['max']:,.0f}; \ the worst possible: \ {d['worst']:,.0f}",
                  font_size=21, color=NO),
        ).arrange(DOWN, buff=0.12).to_edge(DOWN, buff=0.3)
        with self.voiceover(
            "An average is a promise about many runs. You will run your sort once. How far from the average can a "
            "single run be? <bookmark mark='a'/> We sorted the same thousand elements ten thousand times, with "
            "fresh random pivots each time, and counted comparisons. <bookmark mark='b'/> The runs pile up around "
            "the mean, which matches the exact formula. <bookmark mark='c'/> The standard deviation is about "
            "zero point six four n, as the theory predicts: the spread grows like n, while the mean grows like n "
            "log n, so relative to the mean it shrinks. <bookmark mark='d'/> The worst of ten thousand runs made "
            "fourteen and a half thousand comparisons. The worst possible run makes half a million."
        ) as vo:
            self.play(FadeIn(head), Create(ax), FadeIn(ticks), FadeIn(xl))
            vo.wait_until("a")
            self.play(LaggedStart(*[GrowFromEdge(b, DOWN) for b in bars], lag_ratio=0.03), run_time=3)
            vo.wait_until("b")
            self.play(Create(mean), FadeIn(ml))
            vo.wait_until("c")
            self.play(FadeIn(cap[0]))
            vo.wait_until("d")
            self.play(FadeIn(cap[1]))
        self.wait(0.3)
        self.clear_scene()

    def tails(self):
        d = load("concentration")
        head = label(r"The tails", font_size=34).to_edge(UP, buff=0.3)
        t = d["tails"]
        rows = VGroup(*[label(rf"more than {k} standard deviation{'s' if k > 1 else ''} above the mean: \ {100 * t[str(k)]:.2f}\% of runs",
                              font_size=22, color=GREY_A) for k in (1, 2, 3, 4)]).arrange(DOWN, buff=0.18).next_to(
            head, DOWN, buff=0.5)
        pts = VGroup(
            label(r"a tail bound \ (McDiarmid and Hayward, \ 1996): \ the chance of exceeding the mean by a "
                  r"factor $1 + \varepsilon$ is $n^{-\Omega(\varepsilon \ln \ln n)}$", font_size=21, color=YES),
            label(r"in practice: \ a run twice the average almost never happens, \ for any input", font_size=22,
                  color=HEAD),
            label(r"randomized algorithms give a distribution, \ not a guarantee: \ Part 20 studies the tools",
                  font_size=21, color=GREY_B),
        ).arrange(DOWN, buff=0.18).next_to(rows, DOWN, buff=0.5)
        with self.voiceover(
            "How often does a run stray far? <bookmark mark='a'/> One standard deviation above the mean: fifteen "
            "percent of runs. Two: four percent. Three: under one percent. Four: two runs in a thousand. The right "
            "tail is longer than a bell curve's, but it falls fast. <bookmark mark='b'/> McDiarmid and Hayward "
            "proved how fast in 1996: the chance of exceeding the mean by any fixed fraction vanishes faster than "
            "any power of n. <bookmark mark='c'/> So a run that takes twice the average essentially never happens, "
            "whatever the input. A randomized algorithm promises a distribution rather than a bound, and Part 20, "
            "on randomness, studies the tools that measure such promises."
        ) as vo:
            self.play(FadeIn(head))
            vo.wait_until("a")
            self.play(LaggedStart(*[FadeIn(r) for r in rows], lag_ratio=0.4), run_time=2.5)
            vo.wait_until("b")
            self.play(FadeIn(pts[0]))
            vo.wait_until("c")
            self.play(FadeIn(pts[1:]))
        self.wait(0.3)
        self.clear_scene()

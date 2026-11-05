from __future__ import annotations

import math

from explainer.cs import *  # noqa: F403
from videos.cs.cs20.common import (BG, CTRL, DATA, HEAD, LAM, NO, PART, YES, grid_table, load, mono, words)


def histogram(counts, width=5.4, height=2.4, color=DATA):
    top = max(counts)
    bw = width / len(counts)
    bars = VGroup(*[Rectangle(width=bw * 0.9, height=max(height * c / top, 0.02), stroke_width=0, fill_color=color,
                              fill_opacity=0.85) for c in counts])
    for k, b in enumerate(bars):
        b.move_to([k * bw - width / 2 + bw / 2, b.height / 2, 0])
    base = Line([-width / 2 - 0.1, 0, 0], [width / 2 + 0.1, 0, 0], color=GREY_C, stroke_width=1.5)
    return VGroup(base, bars)


class LasVegas(VoiceoverScene):
    def construct(self):
        self.card()
        self.two_kinds()
        self.quicksort()
        self.amplify()

    def card(self):
        card = chapter_card(1, r"Las Vegas and Monte Carlo", r"What can a coin flip buy?", lit=(1949,),
                            extra=((1949, r"the Monte Carlo method"),), part=PART)
        with self.voiceover("Chapter one. Las Vegas and Monte Carlo."):
            self.play(FadeIn(card[0], shift=UP * 0.2), FadeIn(card[1]), FadeIn(card[2]))
        self.play(FadeOut(card))

    def two_kinds(self):
        head = label(r"Two ways to gamble", font_size=36).to_edge(UP, buff=0.35)
        lv = VGroup(
            label(r"\textbf{Las Vegas}", font_size=32, color=YES),
            label(r"always right", font_size=24, color=WHITE),
            label(r"the running time is random", font_size=22, color=GREY_A),
            label(r"randomized quicksort, \ hashing", font_size=20, color=GREY_B),
        ).arrange(DOWN, buff=0.25)
        mc = VGroup(
            label(r"\textbf{Monte Carlo}", font_size=32, color=LAM),
            label(r"a fixed running time", font_size=24, color=WHITE),
            label(r"the answer may be wrong, \ with probability $\le \varepsilon$", font_size=22, color=GREY_A),
            label(r"Freivalds, \ Karger, \ Miller--Rabin", font_size=20, color=GREY_B),
        ).arrange(DOWN, buff=0.25)
        VGroup(lv, mc).arrange(RIGHT, buff=1.6).move_to(UP * 0.4)
        div = DashedLine(UP * 2.0, DOWN * 1.2, color=GREY_D).move_to((lv.get_right() + mc.get_left()) / 2 * RIGHT
                                                                    + UP * 0.4)
        foot = label(r"in both, \ the coins are the algorithm's own: \ no assumption about the input", font_size=22,
                     color=HEAD).to_edge(DOWN, buff=0.8)
        with self.voiceover(
            "An algorithm that flips coins can gamble in two ways. <bookmark mark='a'/> A Las Vegas algorithm is "
            "always right, and only its running time depends on the coins. Randomized quicksort, from Part 16, is "
            "one. <bookmark mark='b'/> A Monte Carlo algorithm runs for a fixed time, and its answer may be wrong, "
            "with a probability we can bound and then make as small as we like. Most of this part is Monte Carlo. "
            "<bookmark mark='c'/> In both cases the randomness belongs to the algorithm. We assume nothing about "
            "the input: the guarantee holds for every input, averaged only over the algorithm's own coins."
        ) as vo:
            self.play(FadeIn(head))
            vo.wait_until("a")
            self.play(FadeIn(lv, shift=UP * 0.1), Create(div))
            vo.wait_until("b")
            self.play(FadeIn(mc, shift=UP * 0.1))
            vo.wait_until("c")
            self.play(FadeIn(foot))
        self.wait(0.3)
        self.clear_scene()

    def quicksort(self):
        d = load("lasvegas")
        head = label(rf"Las Vegas: \ quicksort on {words(d['n'])} keys, \ {d['runs']} runs", font_size=32
                     ).to_edge(UP, buff=0.35)
        h = histogram(d["hist"], color=YES).move_to(LEFT * 2.6 + DOWN * 0.6)
        lo, hi = d["edges"][0], d["edges"][-1]
        ticks = VGroup(label(words(round(lo)), font_size=16, color=GREY_B).next_to(h[0].get_left(), DOWN, buff=0.15),
                       label(words(round(hi)), font_size=16, color=GREY_B).next_to(h[0].get_right(), DOWN, buff=0.15))
        cap = label(r"comparisons in one run", font_size=18, color=GREY_A).next_to(h, DOWN, buff=0.55)
        ex = d["expected"]
        x_ex = h[0].get_left()[0] + 0.1 + (ex - lo) / (hi - lo) * (h[0].width - 0.2)
        mark = DashedLine([x_ex, h[0].get_y(), 0], [x_ex, h[0].get_y() + 2.7, 0], color=HEAD, stroke_width=2)
        side = VGroup(
            label(rf"mean: \ {words(round(d['mean']))}", font_size=22, color=YES),
            label(rf"exact expectation: \ $2(n+1)H_n - 4n = {words(round(ex))}$", font_size=22, color=HEAD),
            label(rf"spread: \ {words(round(d['sd']))} \ (one standard deviation)", font_size=22, color=GREY_A),
            label(rf"slowest of {d['runs']}: \ {words(d['max'])}", font_size=22, color=GREY_A),
            label(rf"the worst case, \ $\binom{{n}}{{2}}$: \ {words(round(d['worst']))}", font_size=22, color=NO),
            label(r"every run sorted correctly", font_size=22, color=WHITE),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.3).to_edge(RIGHT, buff=0.5).shift(DOWN * 0.3)
        with self.voiceover(
            f"Here is a Las Vegas algorithm at work: quicksort with random pivots on {words(d['n'])} keys, run "
            f"{d['runs']} times. Each bar counts the runs that made that many comparisons. <bookmark mark='a'/> "
            f"The average was {words(round(d['mean']))}, and Part 16's exact formula predicts "
            f"{words(round(ex))}. <bookmark mark='b'/> The runs spread by about {words(round(d['sd']))} either side, "
            f"and the slowest made {words(d['max'])}. <bookmark mark='c'/> The worst case, about two million "
            "comparisons, is possible in principle, but it needs a long run of terrible pivots, and its probability "
            "is far too small to observe. <bookmark mark='d'/> And every single run sorted the keys correctly. "
            "Only the time was a gamble."
        ) as vo:
            self.play(FadeIn(head), FadeIn(h[0]), FadeIn(ticks), FadeIn(cap))
            self.play(LaggedStart(*[GrowFromEdge(b, DOWN) for b in h[1]], lag_ratio=0.05), run_time=2.0)
            vo.wait_until("a")
            self.play(Create(mark), FadeIn(side[0]), FadeIn(side[1]))
            vo.wait_until("b")
            self.play(FadeIn(side[2]), FadeIn(side[3]))
            vo.wait_until("c")
            self.play(FadeIn(side[4]))
            vo.wait_until("d")
            self.play(FadeIn(side[5]))
        self.wait(0.3)
        self.clear_scene()

    def amplify(self):
        d = load("lasvegas")
        head = label(r"Monte Carlo: \ shrinking the error", font_size=34).to_edge(UP, buff=0.35)
        one = VGroup(
            label(r"\textbf{one-sided error}: \ a ``no'' is always right, \ a ``yes'' is wrong with probability "
                  r"$\le \tfrac12$", font_size=22, color=WHITE),
            MathTex(r"\Pr[\text{all } k \text{ independent runs wrong}] \le \left(\tfrac12\right)^k", font_size=34,
                    color=LAM),
        ).arrange(DOWN, buff=0.3)
        rows = [[str(r["rounds"]), (rf"${r['error']:.3g}$" if r["error"] > 1e-3 else
                                    rf"${r['error'] * 10 ** -math.floor(math.log10(r['error'])):.1f} \times "
                                    rf"10^{{{math.floor(math.log10(r['error']))}}}$")]
                for r in d["amplify"]]
        tab = grid_table([r"runs $k$", r"chance of an error"], rows, widths=[2.0, 3.6], row_h=0.44, font_size=21,
                         mono_cols=(0,), colors=[[LAM, LAM]] * len(rows))
        two = VGroup(
            label(r"\textbf{two-sided error}: \ right with probability $p > \tfrac12$; \ take the majority of $k$",
                  font_size=22, color=WHITE),
            MathTex(r"\Pr[\text{majority wrong}] \le e^{-2k\,(p - 1/2)^2}", font_size=34, color=CTRL),
            label(r"Hoeffding's inequality \ (\textit{AI, Built}, Part 5)", font_size=18, color=GREY_B),
        ).arrange(DOWN, buff=0.25)
        one.next_to(head, DOWN, buff=0.45)
        tab.next_to(one, DOWN, buff=0.4).to_edge(LEFT, buff=0.7)
        two.next_to(one, DOWN, buff=0.5).shift(RIGHT * 2.6)
        if two.width > 6.6:
            two.width = 6.6
        two.to_edge(RIGHT, buff=0.5)
        with self.voiceover(
            "A Monte Carlo algorithm that errs half the time sounds useless. It isn't, because we can run it "
            "again. <bookmark mark='a'/> Many of this part's algorithms have one-sided error: when they say no, "
            "they are certainly right, and when they say yes, they are wrong with probability at most a half. Run "
            "one k times with fresh coins and believe yes only if every run says yes. All k must be fooled, and "
            "they are independent, so the error falls to a half to the k. <bookmark mark='b'/> Ten runs give one in "
            "a thousand. Forty give about one in a trillion, a smaller chance than that of the hardware itself "
            "failing during the computation. <bookmark mark='c'/> With error on both sides, say right with "
            "probability p above a half, take the majority of k runs. Hoeffding's inequality, from the AI "
            "series, says the majority is wrong with probability exponentially small in k."
        ) as vo:
            self.play(FadeIn(head))
            vo.wait_until("a")
            self.play(FadeIn(one))
            vo.wait_until("b")
            self.play(FadeIn(tab))
            vo.wait_until("c")
            self.play(FadeIn(two))
        self.wait(0.3)
        self.clear_scene()

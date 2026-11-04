from __future__ import annotations

import numpy as np

from explainer.cs import *  # noqa: F403
from videos.cs.cs7.common import (BG, CLOCK, CODE, COST, CTRL, DATA, FUNC, HEAD, HIST, INF, NO, PART, YES, box, fmt,
                                  load, mono)


class Amdahl(VoiceoverScene):
    def construct(self):
        self.card()
        self.derive()
        self.curves()
        self.job()

    def card(self):
        card = chapter_card(13, r"Amdahl's law", r"How much can speeding up one part help?", lit=(1967,), extra=((1967, r"Amdahl's law"),), part=PART)
        with self.voiceover("Chapter thirteen. Amdahl's law."):
            self.play(FadeIn(card[0], shift=UP * 0.2), FadeIn(card[1]), FadeIn(card[2]))
        self.play(FadeOut(card))

    # ------------------------------------------------------------------
    def derive(self):
        head = label(r"Speed up a part of the work", font_size=38).to_edge(UP, buff=0.35)
        whole = Rectangle(width=9.0, height=0.7, stroke_width=0, fill_color=GREY_D, fill_opacity=0.6)
        part = Rectangle(width=9.0 * 0.7, height=0.7, stroke_width=0, fill_color=YES, fill_opacity=0.6)
        bar = VGroup(whole, part)
        part.align_to(whole, RIGHT)
        bar.move_to(UP * 1.4)
        lab = VGroup(label(r"$1 - p$", font_size=26, color=GREY_A).move_to(whole.get_left() + RIGHT * 1.35),
                     label(r"$p$: \ the part we improve", font_size=26, color=WHITE).move_to(part))
        fast = Rectangle(width=9.0 * 0.7 / 4, height=0.7, stroke_width=0, fill_color=YES, fill_opacity=0.9)
        fast.next_to(whole.get_left() + RIGHT * 2.7, RIGHT, buff=0).shift(DOWN * 1.2)
        slow = Rectangle(width=2.7, height=0.7, stroke_width=0, fill_color=GREY_D, fill_opacity=0.6).next_to(
            fast, LEFT, buff=0)
        fl = label(r"$p/n$", font_size=24, color=WHITE).move_to(fast)
        eqs = VGroup(
            MathTex(r"T_{\text{new}} = (1 - p)\,T + \frac{p}{n}\,T", font_size=38, color=CODE),
            MathTex(r"\text{speedup} = \frac{1}{(1 - p) + p/n} \ \le \ \frac{1}{1 - p}", font_size=42, color=HEAD),
        ).arrange(DOWN, buff=0.35).to_edge(DOWN, buff=0.6)
        with self.voiceover(
            "In 1967 Gene Amdahl of IBM made an argument against building machines with many processors, and it "
            "applies to every speed-up of anything. <bookmark mark='a'/> Suppose a fraction p of a program's time is "
            "spent in the part you can improve, and you make that part n times faster. <bookmark mark='b'/> The rest, "
            "one minus p, is untouched. So the new time is one minus p, plus p over n. <bookmark mark='c'/> The speedup "
            "is one over that, and however large n becomes, it can never exceed one over one minus p. Make ninety "
            "percent of a program infinitely fast, and it runs only ten times faster: the other ten percent is still "
            "there."
        ) as vo:
            self.play(FadeIn(head))
            vo.wait_until("a")
            self.play(FadeIn(bar), FadeIn(lab))
            vo.wait_until("b")
            self.play(FadeIn(slow), TransformFromCopy(part, fast), FadeIn(fl))
            self.play(Write(eqs[0]))
            vo.wait_until("c")
            self.play(Write(eqs[1]))
        self.wait(0.3)
        self.clear_scene()

    # ------------------------------------------------------------------
    def curves(self):
        a = load("amdahl")
        head = label(r"The ceiling", font_size=38).to_edge(UP, buff=0.3)
        ax = Axes(x_range=[0, 3, 1], y_range=[0, 100, 20], x_length=7.0, y_length=4.4, tips=False,
                  axis_config={"color": GREY_C, "font_size": 18}).move_to(LEFT * 1.2 + DOWN * 0.3)
        ax.y_axis.add_numbers(list(range(20, 101, 20)), font_size=18, num_decimal_places=0)
        xt = VGroup(*[MathTex(t, font_size=20, color=GREY_B).next_to(ax.c2p(k, 0), DOWN, buff=0.15)
                      for k, t in enumerate(["1", "10", "100", "1000"])])
        xl = note(r"$n$: \ how much faster the improved part runs", font_size=20).next_to(xt, DOWN, buff=0.15)
        yl = note(r"speedup", font_size=20).next_to(ax, UP, buff=0.1).align_to(ax, LEFT)
        ns = np.log10(np.array(a["n"]))
        cols = {"0.5": GREY_B, "0.9": DATA, "0.95": HEAD, "0.99": YES}
        curves = VGroup()
        tags = VGroup()
        for p, ys in a["curves"].items():
            c = VMobject(color=cols[p], stroke_width=3).set_points_as_corners([ax.c2p(x, min(y, 100)) for x, y in
                                                                               zip(ns, ys)])
            curves.add(c)
            tags.add(label(rf"$p = {p}$", font_size=20, color=cols[p]).next_to(ax.c2p(3, min(ys[-1], 100)), RIGHT,
                                                                             buff=0.1))
        notes = VGroup(
            label(r"corollary: \ make the common case fast", font_size=24, color=YES),
            label(r"and look for the part you did not speed up: \\ it is now most of the time", font_size=22,
                  color=GREY_A),
            label(r"Gustafson (1988): \ bigger machines run bigger problems, \\ and the parallel part grows",
                  font_size=20, color=GREY_B),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.3).to_edge(RIGHT, buff=0.3).shift(DOWN * 0.3)
        with self.voiceover(
            "Plot the speedup against n for a few values of p. <bookmark mark='a'/> Each curve rises, then flattens "
            "against its ceiling: two for p of a half, ten for ninety percent, twenty for ninety-five, a hundred for "
            "ninety-nine. <bookmark mark='b'/> The corollary is the design rule this series keeps meeting: make the "
            "common case fast. And after every improvement, look again, because the part you did not speed up is now "
            "most of the time. <bookmark mark='c'/> John Gustafson pointed out in 1988 that people given a bigger "
            "machine usually run a bigger problem, whose improvable part grows with it, which is why many processors "
            "turned out to be worth building after all."
        ) as vo:
            self.play(FadeIn(head), Create(ax), FadeIn(xt), FadeIn(xl), FadeIn(yl))
            vo.wait_until("a")
            self.play(LaggedStart(*[Create(c) for c in curves], lag_ratio=0.3), FadeIn(tags), run_time=3.0)
            vo.wait_until("b")
            self.play(FadeIn(notes[0]), FadeIn(notes[1]))
            vo.wait_until("c")
            self.play(FadeIn(notes[2]))
        self.wait(0.3)
        self.clear_scene()

    # ------------------------------------------------------------------
    def job(self):
        a = load("amdahl")
        il = load("ironlaw")
        head = label(r"Amdahl and the Job", font_size=38).to_edge(UP, buff=0.35)
        rows = VGroup(
            label(rf"the pipeline speeds up \textit{{every}} instruction: \ $p = 1$, \ {il['speedup']:.2f} times",
                  font_size=26, color=GREY_A),
            label(rf"the linear search is {100 * a['job_scan_share']:.1f}\% of the Job's instructions", font_size=26,
                  color=NO),
            label(rf"an idea that removed the search entirely: \ at most $1/(1 - p) \approx {a['job_limit']:.0f}$ "
                  r"times", font_size=26, color=YES),
            label(r"a hardware trick reaches the whole program, \ but gently; \\ an algorithm reaches only the search, "
                  r"\ but the search is nearly everything", font_size=24, color=HEAD),
        ).arrange(DOWN, buff=0.35).move_to(DOWN * 0.1)
        with self.voiceover(
            "Apply the law to the Job. <bookmark mark='a'/> The pipeline makes every instruction faster, so p is one, "
            "and the gain is the clock times the CPI: one point nine. <bookmark mark='b'/> But almost all of the Job's "
            "instructions are spent in one place: the linear search through the word table, ninety-nine point seven "
            "percent of them. <bookmark mark='c'/> An idea that eliminated the search, as Part 17's hash table nearly "
            "will, could therefore make the Job up to three hundred and fifty times faster, while touching less than "
            "one percent of the program's text. <bookmark mark='d'/> That is the ledger's question in miniature. "
            "Hardware improves everything a little; an algorithm improves one thing enormously, and when that one "
            "thing is nearly all the time, the algorithm wins."
        ) as vo:
            self.play(FadeIn(head))
            for mk, r in zip("abcd", rows):
                vo.wait_until(mk)
                self.play(FadeIn(r, shift=UP * 0.1))
        self.wait(0.3)
        self.clear_scene()

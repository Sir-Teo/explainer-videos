from __future__ import annotations

import numpy as np

from videos.psychology.psych11.common import *  # noqa: F403


class Curve(VoiceoverScene):
    def construct(self):
        self.card()
        self.step()
        self.four()
        self.forms()

    def card(self):
        card = chapter_card(4, r"The threshold is a curve", r"Is there a line below which nothing is noticed?",
                            lit=(), part=PART, scale=("mind",), marr=("what",))
        with self.voiceover(
            "Chapter four. The threshold is a curve."
        ):
            self.play(FadeIn(card, shift=UP * 0.2))
        self.clear_scene()

    def step(self):
        d = load("methods")
        s = load("shapes")
        head = heading(r"A step, \ or a slope?")
        A = axes([0, 25], [0.4, 1.02], x_length=7.0, y_length=4.2, xticks=[0, 4, 8, 12, 16, 20, 24], yticks=[0.5, 0.75, 1.0],
                 yfmt=lambda v: f"{v:g}", xlabel=r"the increment", ylabel=r"share of trials right", center=[-2.8, -0.35, 0])
        ax = A.ax
        th = 8.0
        stepline = VMobject(color=GREY_B, stroke_width=4).set_points_as_corners(
            [ax.c2p(0, 0.5), ax.c2p(th, 0.5), ax.c2p(th, 1.0), ax.c2p(25, 1.0)])
        sl = label(r"a threshold as a line", font_size=26, color=GREY_A).next_to(ax.c2p(th, 1.0), UR, buff=0.1)
        p = d["cs_k"] / d["cs_n"]
        dots = VGroup(*[Dot(ax.c2p(x, y), radius=0.1, color=YOU) for x, y in zip(d["cs_delta"], p)])
        smooth = curve(ax, s["x"], s["gauss"], MODEL, stroke_width=5)
        rows = rows_of([
            (r"if a threshold were a line, \ guessing below it, \ always right above it", GREY_A),
            (r"the data never look like that: \ the share right climbs gradually", YOU),
            (r"because the impression of each stimulus is noisy: \ on some trials 6 looks like 10, \ on some like 2", WHITE),
            (r"so the threshold is a point we choose on a curve: \ by custom, \ 75\% right in a two-interval task", THRESH),
        ], 5.0, 28, 0.3).move_to([4.3, -0.25, 0])
        keep_in_frame(rows)
        tag = psyche_tag(r"simulated: the counts of chapter 3")
        with self.voiceover(
            "Behind all three methods is a picture of what a threshold is. The simplest picture is a "
            "line. <bookmark mark='a'/> Below it, nothing is noticed and the observer guesses. Above it, "
            "the difference is always seen. <bookmark mark='b'/> The data never look like that. The share "
            "of right answers climbs gradually, over a wide range of increments. <bookmark mark='c'/> "
            "Because the impression each stimulus makes is noisy. On some trials an increment of six "
            "feels like ten, and on some like two. <bookmark mark='d'/> So there is no line. There is a "
            "curve, called the psychometric function, and the threshold is a point we choose on it: by "
            "custom, the increment that gets seventy-five percent right in a two-interval task, halfway "
            "between guessing and certainty."
        ) as vo:
            self.play(FadeIn(head), FadeIn(tag), FadeIn(A), Create(stepline), FadeIn(sl), FadeIn(rows[0]))
            vo.wait_until("a")
            self.wait(0.5)
            vo.wait_until("b")
            self.play(FadeIn(dots, lag_ratio=0.2), FadeIn(rows[1]))
            vo.wait_until("c")
            self.play(FadeIn(rows[2]))
            vo.wait_until("d")
            self.play(Create(smooth), stepline.animate.set_stroke(opacity=0.3), FadeIn(rows[3]), run_time=2.0)
        self.clear_scene()

    def four(self):
        s = load("shapes")
        head = heading(r"Four numbers describe it")
        A = axes([0, 24], [0.4, 1.02], x_length=7.4, y_length=4.4, xticks=[0, 4, 8, 12, 16, 20, 24], yticks=[0.5, 0.75, 1.0],
                 yfmt=lambda v: f"{v:g}", xlabel=r"stimulus level, $x$", ylabel=r"$\psi(x)$", center=[-2.6, -0.4, 0])
        ax = A.ax
        c = curve(ax, s["x"], s["four"], MODEL, stroke_width=5)
        g = s["four_gamma"]
        lam = s["four_lam"]
        guess = DashedLine(ax.c2p(0, g), ax.c2p(24, g), color=GREY_C, stroke_width=2)
        top = DashedLine(ax.c2p(0, 1 - lam), ax.c2p(24, 1 - lam), color=BAD, stroke_width=2)
        mid = (g + 1 - lam) / 2
        al = Dot(ax.c2p(s["four_alpha"], mid), radius=0.1, color=THRESH)
        tan = Line(ax.c2p(s["four_alpha"] - 4, mid - 0.13), ax.c2p(s["four_alpha"] + 4, mid + 0.13), color=WEBERC, stroke_width=3)
        eq = MathTex(r"\psi(x)", r"=", r"\gamma", r"+", r"(1 - \gamma - \lambda)", r"\,F(x;\ ", r"\alpha", r",\ ", r"\beta", r")",
                     font_size=40)
        eq[2].set_color(GREY_A)
        eq[4].set_color(BAD)
        eq[6].set_color(THRESH)
        eq[8].set_color(WEBERC)
        eq.to_edge(UP, buff=1.2)
        rows = rows_of([
            (r"$\gamma$: \ the guess rate: \ $\tfrac12$ with two intervals, \ near 0 for yes-no", GREY_A),
            (r"$\alpha$: \ the threshold, \ where the curve is halfway up", THRESH),
            (r"$\beta$: \ the spread: \ a shallow curve means a noisy observer", WEBERC),
            (r"$\lambda$: \ the lapse rate: \ blinks, \ slips, \ a wandering mind", BAD),
        ], 4.9, 28, 0.32).move_to([4.4, -0.45, 0])
        keep_in_frame(rows)
        with self.voiceover(
            "The curve is described by four numbers. Here is the formula. <bookmark mark='a'/> Gamma is "
            "the guess rate: where the curve starts. With two intervals, a guess is right half the time. "
            "<bookmark mark='b'/> Alpha is the threshold: where the curve is halfway up. "
            "<bookmark mark='c'/> Beta is the spread: how gradually it climbs. A shallow curve means a "
            "noisy observer. <bookmark mark='d'/> And lambda is the lapse rate. Even at an increment "
            "nobody could miss, people get a few trials wrong: a blink, a slip of the finger, a moment "
            "of thinking about lunch. So the curve tops out a little below one. Remember lambda. It "
            "matters more than it looks, in chapter six."
        ) as vo:
            self.play(FadeIn(head), Write(eq), FadeIn(A), Create(c), run_time=2.0)
            vo.wait_until("a")
            self.play(Create(guess), FadeIn(rows[0]))
            vo.wait_until("b")
            self.play(FadeIn(al, scale=1.5), FadeIn(rows[1]))
            vo.wait_until("c")
            self.play(Create(tan), FadeIn(rows[2]))
            vo.wait_until("d")
            self.play(Create(top), FadeIn(rows[3]))
        self.clear_scene()

    def forms(self):
        s = load("shapes")
        head = heading(r"Three shapes for $F$, \ nearly the same")
        A = axes([0, 24], [0.4, 1.02], x_length=7.4, y_length=4.4, xticks=[0, 4, 8, 12, 16, 20, 24], yticks=[0.5, 0.75, 1.0],
                 yfmt=lambda v: f"{v:g}", xlabel=r"stimulus level", ylabel=r"", center=[-2.6, -0.4, 0])
        ax = A.ax
        cs = [(s["gauss"], MODEL, r"cumulative Gaussian"), (s["logistic"], STEVC, r"logistic"), (s["weibull"], WEBERC, r"Weibull")]
        lines = VGroup(*[curve(ax, s["x"], y, col, stroke_width=4) for y, col, _ in cs])
        lg = legend([(col, name) for _, col, name in cs], font_size=27).move_to(ax.c2p(17.5, 0.62))
        rows = rows_of([
            (r"matched at the threshold and at the slope there, \ the three differ only in the tails", WHITE),
            (r"the Gaussian: \ noise that is normal; \ the Weibull: \ a race among many detectors", GREY_A),
            (r"with a few hundred trials, \ the data cannot tell them apart: \ choose one, \ say which", THRESH),
        ], 4.9, 28, 0.34).move_to([4.4, -0.3, 0])
        keep_in_frame(rows)
        tag = psyche_tag(r"computed: three functions matched at 75\%")
        with self.voiceover(
            "And F, the climbing part, can take several shapes. The three in common use: a cumulative "
            "Gaussian, a logistic, and a Weibull. <bookmark mark='a'/> Matched at the threshold and at the "
            "slope there, they differ only in the tails. <bookmark mark='b'/> Each comes with a story. The "
            "Gaussian says the noise in the head is normal. The Weibull came from a model in which many "
            "detectors race and the first to fire wins. <bookmark mark='c'/> With a few hundred trials, "
            "the data can't tell them apart. So the rule is practical: pick one, and say which."
        ) as vo:
            self.play(FadeIn(head), FadeIn(tag), FadeIn(A), FadeIn(lg), LaggedStart(*[Create(l) for l in lines], lag_ratio=0.5),
                      run_time=3.0)
            vo.wait_until("a")
            self.play(FadeIn(rows[0]))
            vo.wait_until("b")
            self.play(FadeIn(rows[1]))
            vo.wait_until("c")
            self.play(FadeIn(rows[2]))
        self.clear_scene()

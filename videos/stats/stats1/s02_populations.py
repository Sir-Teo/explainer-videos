from __future__ import annotations

import numpy as np

from videos.stats.stats1.common import *  # noqa: F403


class Populations(VoiceoverScene):
    def construct(self):
        self.card()
        self.two_sides()
        self.hidden()
        self.promise()
        self.colours()

    def card(self):
        card = chapter_card(1, r"Populations and samples", r"What we want to know, and what we get to see",
                            lit=(1662,), part=PART)
        with self.voiceover("Chapter one. Populations and samples."):
            self.play(FadeIn(card[0], shift=UP * 0.2), FadeIn(card[1]))
        self.play(FadeOut(card))

    def two_sides(self):
        d = load("populations")
        g = np.random.Generator(np.random.PCG64(4))
        k = 700
        pos = np.column_stack([g.uniform(-2.0, 2.0, k), g.uniform(-1.9, 1.9, k), np.zeros(k)]) + [-4.4, -1.1, 0]
        field = VGroup(*[Dot(p, radius=0.028, color=S.POP) for p in pos])
        frame = RoundedRectangle(width=4.5, height=4.3, corner_radius=0.15, stroke_color=S.WORLD,
                                 stroke_width=1.5).move_to([-4.4, -1.1, 0])
        ftitle = label(r"the population", font_size=26, color=S.WORLD).next_to(frame, UP, buff=0.12)
        A = axes([150, 190], [0, 1], x_length=7.4, y_length=0.5, xlabel=r"height (cm)",
                 xticks=[150, 160, 170, 180, 190], center=[2.6, -1.6, 0])
        A.ax.y_axis.set_opacity(0)
        ax = A.ax
        mu, xbar = d["mu"], d["xbar"]
        tline = Line(ax.c2p(mu, 0) + DOWN * 0.1, ax.c2p(mu, 0) + UP * 2.6, color=S.TRUTH, stroke_width=4)
        tlab = MathTex(r"\theta", font_size=46, color=S.TRUTH).next_to(tline, UP, buff=0.1)
        tval = label(rf"{mu:.2f} cm", font_size=24, color=S.TRUTH).next_to(tlab, RIGHT, buff=0.15)
        d_pop = definition_card(r"Population, parameter", r"everyone we want to know about; \ a number that "
                                r"describes them, \ $\theta$ \ (always gold)", color=S.TRUTH, width=4.6,
                                font_size=22).move_to([-4.3, 2.45, 0])
        pick = g.choice(k, 25, replace=False)
        sample = VGroup(*[field[i].copy().set_color(S.DATA).scale(1.6) for i in pick])
        x = np.sort(d["x"])
        ends = [ax.c2p(v, 0) + UP * (0.12 + 0.13 * int(np.sum(np.abs(x[:j] - v) < 0.9))) for j, v in enumerate(x)]
        eline = Line(ax.c2p(xbar, 0) + DOWN * 0.1, ax.c2p(xbar, 0) + UP * 1.7, color=S.EST, stroke_width=4)
        elab = MathTex(r"\hat\theta", font_size=46, color=S.EST).next_to(eline, UP, buff=0.1)
        eval_ = label(rf"{xbar:.2f}", font_size=24, color=S.EST).next_to(elab, LEFT, buff=0.15)
        d_smp = definition_card(r"Sample, statistic", r"the few we measure; \ a number computed from them, "
                                r"\ $\hat\theta$ \ (always blue)", color=S.EST, width=4.6,
                                font_size=22).move_to([3.6, 2.55, 0])
        err = BraceBetweenPoints(ax.c2p(xbar, 0) + UP * 1.0, ax.c2p(mu, 0) + UP * 1.0, direction=UP, color=S.RESID)
        errl = MathTex(r"\hat\theta - \theta", r"=", f"{d['err']:.2f}", font_size=34, color=S.RESID)
        errl.next_to(err, UP, buff=0.08).shift(RIGHT * 1.6)
        tag = simulated_tag()
        with self.voiceover(
            "Every statistical question has two sides. <bookmark mark='a'/> On one side is the population: everyone "
            f"we want to know about. Here it's the World's {money(d['n_adults'])} adults; we'll build the World in "
            "the next chapter. A number that describes the whole population, like the average height of all of "
            "them, is a parameter. We'll write it theta, and it's always gold. <bookmark mark='b'/> Here it's "
            f"{mu:.2f} centimetres. <bookmark mark='c'/> On the other side is the sample: the few we actually "
            "measure. Here, twenty-five adults chosen at random. <bookmark mark='d'/> A number computed from the "
            "sample is a statistic. When it's meant to estimate a parameter we write it theta hat, and it's always "
            f"blue. The average of these twenty-five is {xbar:.2f}. <bookmark mark='e'/> The sample's average is "
            f"not the population's. It missed by {abs(d['err']):.2f} of a centimetre. That gap, theta hat minus "
            "theta, is the error, and in one way or another the rest of the series is about it."
        ) as vo:
            self.play(FadeIn(frame), FadeIn(ftitle), FadeIn(field, lag_ratio=0.002), FadeIn(A), FadeIn(tag))
            vo.wait_until("a")
            self.play(FadeIn(d_pop, shift=DOWN * 0.2))
            vo.wait_until("b")
            self.play(Create(tline), FadeIn(tlab), FadeIn(tval))
            vo.wait_until("c")
            self.play(LaggedStart(*[Indicate(m, color=S.DATA, scale_factor=2.2) for m in sample], lag_ratio=0.05),
                      FadeIn(sample), run_time=1.6)
            self.play(LaggedStart(*[m.animate.move_to(e) for m, e in zip(sample, ends)], lag_ratio=0.06),
                      run_time=2.2)
            vo.wait_until("d")
            self.play(FadeIn(d_smp, shift=DOWN * 0.2), Create(eline), FadeIn(elab), FadeIn(eval_))
            vo.wait_until("e")
            self.play(GrowFromCenter(err), FadeIn(errl))
        self.keep = dict(field=field, frame=frame, ftitle=ftitle, A=A, tline=tline, tlab=tlab, tval=tval,
                         d_pop=d_pop, d_smp=d_smp, sample=sample, eline=eline, elab=elab, eval_=eval_, err=err,
                         errl=errl, tag=tag)

    def hidden(self):
        k = self.keep
        q = label(r"?", font_size=120, color=GREY_C).move_to(k["frame"])
        qt = MathTex(r"\theta = \ ?", font_size=46, color=GREY_B).move_to(k["tlab"])
        errq = MathTex(r"\hat\theta - \theta", r"=", r"?", font_size=34, color=S.RESID).move_to(k["errl"])
        with self.voiceover(
            "Now the part that makes it hard. <bookmark mark='a'/> In real life you never see the population. "
            "Graunt never saw London's living. A pollster never hears every voter, and a drug trial never treats "
            "every future patient. <bookmark mark='b'/> So the gold line is gone. All you have is the sample, and "
            "its average. <bookmark mark='c'/> You can't know the error, because knowing it would mean knowing "
            "theta. <bookmark mark='d'/> But you can know something nearly as useful: how big errors like this tend "
            "to be. Draw a different twenty-five and you'd get a different average. If you knew how those averages "
            "scatter around theta, you could say how far from theta your one average is likely to be. That "
            "scatter is the subject of Parts 6 and 8, and at the end of this part we'll watch it happen."
        ) as vo:
            vo.wait_until("a")
            self.play(k["field"].animate.set_opacity(0.12), FadeIn(q), k["d_pop"].animate.set_opacity(0.35))
            vo.wait_until("b")
            self.play(FadeOut(k["tline"]), FadeOut(k["tval"]), ReplacementTransform(k["tlab"], qt))
            vo.wait_until("c")
            self.play(Transform(k["errl"], errq))
            vo.wait_until("d")
            self.play(Indicate(k["sample"], color=S.EST, scale_factor=1.3))
        self.clear_scene()

    def promise(self):
        d = load("populations")
        mu = d["mu"]
        A = axes([161, 178], [0, 21], x_length=6.6, y_length=4.6, xlabel=r"height (cm)",
                 xticks=[162, 166, 170, 174, 178], center=[-3.3, -0.4, 0])
        A.ax.y_axis.set_opacity(0)
        ax = A.ax
        tl = DashedLine(ax.c2p(mu, 0), ax.c2p(mu, 21), color=S.TRUTH, stroke_width=3)
        tlab = MathTex(r"\theta", font_size=40, color=S.TRUTH).next_to(tl, UP, buff=0.08)
        bars = VGroup()
        for i, (m, h, c) in enumerate(zip(d["means"], d["half"], d["cover"])):
            y = i + 0.8
            col = S.KEPT if c else S.BROKEN
            bars.add(VGroup(Line(ax.c2p(m - h, y), ax.c2p(m + h, y), color=col, stroke_width=4),
                            Dot(ax.c2p(m, y), radius=0.05, color=S.EST)))
        cap = label(rf"20 samples of 25: \ {d['n_cover']} intervals catch $\theta$", font_size=26,
                    color=GREY_A).next_to(A, DOWN, buff=0.2)
        preview = note(r"a preview: \ intervals are built in Part 11").to_corner(DL, buff=0.3)
        board = coverage_board([], placeholders=6, font_size=24).scale_to_fit_width(6.3).move_to([3.55, 0.1, 0])
        with self.voiceover(
            "That's what statistics promises: not the answer, but an honest statement of how often you'll be "
            "wrong. <bookmark mark='a'/> The classic form is an interval: a range computed from the sample, built so "
            "that it captures theta in, say, ninety-five percent of samples. Here are twenty samples, each with its "
            f"interval. <bookmark mark='b'/> {d['n_cover']} of these twenty catch the gold line; the red ones miss. "
            "<bookmark mark='c'/> A promise like ninety-five percent can be checked, but only if you know the truth. "
            "So the series keeps a scoreboard, the Coverage Board. Every interval and every test we meet will be "
            "run thousands of times on a population whose truth we know, and the board records whether the "
            "promise was kept. <bookmark mark='d'/> Right now it's empty. The first rows arrive in Part 8, and some "
            "of them will be red: textbook methods that don't do what they say."
        ) as vo:
            self.play(FadeIn(A), Create(tl), FadeIn(tlab), FadeIn(preview))
            vo.wait_until("a")
            self.play(LaggedStart(*[Create(b) for b in bars], lag_ratio=0.12), run_time=3.0)
            vo.wait_until("b")
            self.play(FadeIn(cap), *[Indicate(b, color=S.BROKEN) for b, c in zip(bars, d["cover"]) if not c])
            vo.wait_until("c")
            self.play(FadeIn(board, shift=LEFT * 0.3))
            vo.wait_until("d")
            self.play(Indicate(board.body, color=GREY_B, scale_factor=1.02))
        self.clear_scene()

    def colours(self):
        rows = [
            (S.TRUTH, r"\theta,\ \mu", r"the truth: \ a parameter, \ a population"),
            (S.EST, r"\hat\theta,\ \bar x", r"an estimate: \ a statistic, \ a fitted curve"),
            (S.DATA, r"x_1, \dots, x_n", r"data"),
            (S.RESID, r"x_i - \bar x", r"a deviation, \ an error"),
            (S.NULL, r"H_0", r"a null hypothesis \ (and teal: \ its alternative)"),
            (S.POST, r"p(\theta \mid x)", r"Bayes: \ prior purple, \ likelihood green, \ posterior orange"),
        ]
        g = VGroup()
        for col, sym, txt in rows:
            g.add(VGroup(Circle(radius=0.16, stroke_width=0, fill_color=col, fill_opacity=1),
                         MathTex(sym, font_size=38, color=col), label(txt, font_size=28, color=GREY_A)))
        for r in g:
            r[1].next_to(r[0], RIGHT, buff=0.35)
            r[2].next_to(r[0], RIGHT, buff=2.4)
        g.arrange(DOWN, aligned_edge=LEFT, buff=0.38).move_to(DOWN * 0.3)
        title = label(r"Colour is meaning", font_size=44).to_edge(UP, buff=0.6)
        with self.voiceover(
            "One convention runs through the whole series: colour is meaning. <bookmark mark='a'/> Gold is the "
            "truth: a parameter, a population. Blue is an estimate: a statistic, a fitted line. White is data. "
            "Red is a deviation or an error. Grey is a null hypothesis, and teal its alternative. Purple, green and "
            "orange are Bayes's prior, likelihood and posterior. <bookmark mark='b'/> Whenever you see gold, you're "
            "looking at something that, in real life, nobody gets to see."
        ) as vo:
            self.play(FadeIn(title))
            vo.wait_until("a")
            self.play(LaggedStart(*[FadeIn(r, shift=RIGHT * 0.2) for r in g], lag_ratio=0.5), run_time=6.0)
            vo.wait_until("b")
            self.play(Indicate(g[0], color=S.TRUTH, scale_factor=1.1))
        self.clear_scene()

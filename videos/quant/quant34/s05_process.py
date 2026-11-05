from __future__ import annotations

import math

import numpy as np

from explainer.quant import *  # noqa: F403
from videos.quant.quant34.common import BAD, FIRM_C, GOOD, HURDLE, OOS_C, PART, PM_C, comma, fit_right, load


class Process(VoiceoverScene):
    def construct(self):
        h = load("house")
        self.card()
        self.pipeline()
        self.review()
        self.record(h)
        self.haircut(h)
        self.incubation()
        self.ramp()
        self.retire()
        self.question()

    def card(self):
        c = chapter_card(4, r"From idea to capital", r"How does a firm decide which research to trust with money?",
                         part=PART)
        with self.voiceover("Chapter four. A quant firm produces thousands of ideas a year and funds a handful. The "
                            "process that chooses them is the firm's real product, and it is the process this series "
                            "has been running in the House since Part one."):
            self.play(FadeIn(c[0], shift=UP * 0.2), FadeIn(c[1]))
        self.play(FadeOut(c))

    def pipeline(self):
        steps = [r"idea", r"data", r"backtest", r"review", r"incubation", r"capital", r"monitoring", r"retirement"]
        boxes = VGroup()
        for k, t in enumerate(steps):
            b = RoundedRectangle(width=2.6, height=0.8, corner_radius=0.12, color=FIRM_C if k < 6 else GREY_B,
                                 fill_opacity=0.15)
            boxes.add(VGroup(b, label(t, font_size=20).move_to(b)))
        top = VGroup(*boxes[:4]).arrange(RIGHT, buff=0.5).move_to(UP * 1.2)
        bot = VGroup(*boxes[4:]).arrange(RIGHT, buff=0.5).move_to(DOWN * 0.8)
        arrows = VGroup(*[Arrow(boxes[k].get_right(), boxes[k + 1].get_left(), buff=0.08, stroke_width=2,
                                max_tip_length_to_length_ratio=0.25, color=GREY_B) for k in (0, 1, 2, 4, 5, 6)])
        turn = CurvedArrow(boxes[3].get_bottom(), boxes[4].get_top(), angle=-PI / 2, color=GREY_B, stroke_width=2)
        notes = wrapped_label(r"most ideas stop at the backtest or the review; the House's version of each step is in "
                              r"brackets on the next pages", 11.0, 16, GREY_A).to_edge(DOWN, buff=0.6)
        with self.voiceover(
            "The pipeline, as quant firms describe it. <bookmark mark='a'/> An idea; the data to test it; a backtest; a "
            "review by people who did not build it. <bookmark mark='b'/> Then incubation, trading small; capital; "
            "monitoring; and, eventually, retirement. Most ideas stop at the backtest or the review, and a firm is "
            "judged by how few bad ideas get past them."
        ) as vo:
            vo.wait_until("a")
            self.play(LaggedStart(*[FadeIn(b_) for b_ in boxes[:4]], lag_ratio=0.3), Create(VGroup(*arrows[:3])))
            vo.wait_until("b")
            self.play(Create(turn), LaggedStart(*[FadeIn(b_) for b_ in boxes[4:]], lag_ratio=0.3),
                      Create(VGroup(*arrows[3:])), FadeIn(notes))
        self.wait(0.4)
        self.clear_scene()

    def review(self):
        cards = VGroup(
            desk_question(r"how many trials?", r"every variant, parameter and universe tried counts (Part 26); the "
                          r"House's counter is the firm's research log, made public", width=12.4, font_size=19),
            desk_question(r"is it after costs, at size?", r"costs on every leg (Part 33), capacity from the "
                          r"square-root law (Part 31), and the borrow on the short side", width=12.4, font_size=19),
            desk_question(r"why should it work?", r"who pays the premium and why they keep paying (Part 32); a rule "
                          r"with no reason is the first to decay", width=12.4, font_size=19),
            desk_question(r"what does it add?", r"its correlation with what the firm already runs; a good strategy that "
                          r"duplicates a book adds risk, not return (Part 30)", width=12.4, font_size=19),
        ).arrange(DOWN, buff=0.2)
        with self.voiceover(
            "What a review asks, collected from this series. <bookmark mark='a'/> How many trials did it take to find? "
            "<bookmark mark='b'/> Is it after costs, at the size the firm would run it? <bookmark mark='c'/> Why should "
            "it work, and who pays? <bookmark mark='d'/> And what does it add to what the firm already holds? A "
            "strategy can pass all four and still be rejected for the last."
        ) as vo:
            for k, mk in enumerate(("a", "b", "c", "d")):
                vo.wait_until(mk)
                self.play(FadeIn(cards[k], shift=UP * 0.2))
        self.wait(0.4)
        self.clear_scene()

    def record(self, h):
        n_rows = len(h["names"])
        trials = h["trials"]
        rows = [cmath(r"\text{trials counted}", r"=", comma(trials), font_size=38, colors={r"\text{trials counted}": FIRM_C}),
                cmath(r"\text{registered books}", r"=", str(n_rows), font_size=38),
                cmath(r"\text{envelopes opened}", r"=", r"\text{once each, on 2021--2025}", font_size=34,
                      colors={r"\text{envelopes opened}": OOS_C})]
        whys = [why(r"every configuration compared in Parts 1--33, each charged to the rule finally chosen"),
                why(r"the strategies that passed review in this series, each with its research and sealed-year rows"),
                why(r"the incubation step, compressed: the sealed years play the part of live trading")]
        step = ladder(self, rows, whys, keep=3, top=2.6, x=-0.3, buff=0.55, edge=6.9)
        with self.voiceover(
            "The House has been running this pipeline. <bookmark mark='a'/> Its counter has charged "
            f"{trials:,} trials, every configuration compared in thirty-three parts. <bookmark mark='b'/> {n_rows} "
            "strategies were registered. <bookmark mark='c'/> And each was opened once on sealed years, the House's "
            "stand-in for incubation. So the House can ask the question a firm asks of its own research desk: how much "
            "do registered books shrink when they meet new data?"
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

    def haircut(self, h):
        rs = np.asarray(h["research"], float)
        hs = np.asarray(h["holdout"], float)
        se = np.asarray(h["se"], float)
        lim = (-1.0, 3.0)
        g = axes(list(lim), list(lim), x_length=5.4, y_length=5.4, xlabel=r"Sharpe ratio, research years",
                 ylabel=r"Sharpe ratio, sealed years", xticks=[-1, 0, 1, 2, 3], yticks=[-1, 0, 1, 2, 3],
                 font_size=14).move_to(LEFT * 2.2 + DOWN * 0.1)
        ax = g.ax
        diag = DashedLine(ax.c2p(-1, -1), ax.c2p(3, 3), color=GREY_C, stroke_width=1.5)
        dots, bars = VGroup(), VGroup()
        for a, b, s in zip(rs, hs, se):
            if a > lim[1]:
                continue
            bb = float(np.clip(b, *lim))
            dots.add(Dot(ax.c2p(a, bb), radius=0.06, color=OOS_C))
            bars.add(Line(ax.c2p(a, max(lim[0], bb - s)), ax.c2p(a, min(lim[1], bb + s)), color=OOS_C, stroke_width=1,
                          stroke_opacity=0.5))
        b1, b0 = h["slope"], h["intercept"]
        fit = Line(ax.c2p(-1, b0 - b1), ax.c2p(3, b0 + 3 * b1), color=HURDLE, stroke_width=2.5)
        st = VGroup(label(rf"slope {b1:.2f}, intercept {b0:+.2f}", font_size=17, color=HURDLE),
                    label(rf"mean research {h['mean_research']:.2f}, sealed {h['mean_holdout']:.2f}", font_size=17,
                          color=GREY_A),
                    label(rf"{100 * h['share_positive']:.0f}\% positive on the sealed years", font_size=17, color=GREY_A),
                    label(r"bars: one standard error", font_size=15, color=GREY_B))
        st.arrange(DOWN, aligned_edge=LEFT, buff=0.15).to_edge(RIGHT, buff=0.4).shift(UP * 0.8)
        fit_right(st)
        with self.voiceover(
            "The House's own record. <bookmark mark='a'/> Each dot is a registered book: its Sharpe ratio on the "
            "research years against the sealed years, with a standard error. The dashed line is no shrinkage. "
            f"<bookmark mark='b'/> Fitted, the slope is {b1:.2f}: a book that looked one Sharpe point better in "
            f"research was about {b1:.2f} better on new data. The average fell from {h['mean_research']:.2f} to "
            f"{h['mean_holdout']:.2f}, and {100 * h['share_positive']:.0f} percent stayed positive. Most of these are "
            "classic premia with long histories; a firm's own research, with more trials per idea, shrinks more, which "
            "is why the review counts them."
        ) as vo:
            self.play(FadeIn(g), Create(diag))
            vo.wait_until("a")
            self.play(FadeIn(bars), LaggedStart(*[FadeIn(d_) for d_ in dots], lag_ratio=0.05))
            vo.wait_until("b")
            self.play(Create(fit), FadeIn(st))
        self.wait(0.4)
        self.clear_scene()

    def incubation(self):
        cards = VGroup(
            desk_question(r"what live trading tests", r"real fills, real costs, data that arrives late or revised, and "
                          r"the firm's own impact: everything a backtest assumes", width=12.4, font_size=19),
            desk_question(r"what it cannot test", r"a Sharpe ratio: six months of live trading has a standard error of "
                          r"about 1.4; incubation catches broken strategies, not mediocre ones", width=12.4, font_size=19),
            desk_question(r"paper, then small, then larger", r"a strategy earns capital by surviving each stage with its "
                          r"costs and slippage inside the bounds the review predicted", width=12.4, font_size=19),
        ).arrange(DOWN, buff=0.25)
        se6 = 1 / math.sqrt(0.5)
        with self.voiceover(
            "Incubation. <bookmark mark='a'/> Trading a little real money tests what a backtest assumes: fills, costs, "
            "late or revised data, and the firm's own impact. <bookmark mark='b'/> It cannot test the Sharpe ratio: six "
            f"months of returns give a standard error of about {se6:.1f}. Incubation catches broken strategies, not "
            "mediocre ones. <bookmark mark='c'/> So capital is earned in stages, each passed by keeping costs and "
            "slippage inside the bounds the review predicted."
        ) as vo:
            for k, mk in enumerate(("a", "b", "c")):
                vo.wait_until(mk)
                self.play(FadeIn(cards[k], shift=UP * 0.2))
        self.wait(0.4)
        self.clear_scene()

    def ramp(self):
        tau = 0.5
        rows = [cmath(r"S", r"\sim", r"N(0,\ \tau^2),\quad \hat S_T \mid S \sim N(S,\ 1/T)", font_size=34),
                cmath(r"\mathbb E[S \mid \hat S_T]", r"=", r"\frac{T\tau^2}{1 + T\tau^2}\, \hat S_T", font_size=36,
                      colors={r"\mathbb E[S \mid \hat S_T]": GOOD}),
                cmath(r"\tau = 0.5", r":", rf"T = 1:\ {tau ** 2 / (1 + tau ** 2):.2f};\quad T = 4:\ "
                      rf"{4 * tau ** 2 / (1 + 4 * tau ** 2):.2f};\quad T = 10:\ {10 * tau ** 2 / (1 + 10 * tau ** 2):.2f}",
                      font_size=30)]
        whys = [why(r"a prior over true Sharpe ratios centred on zero, and a track record of $T$ years"),
                why(r"the posterior mean shrinks the measured Sharpe ratio toward zero, less as the record lengthens"),
                why(r"with a prior spread of one half: a year's record is believed one fifth, four years' one half; size "
                    r"in proportion, so capital follows the posterior, not the backtest")]
        step = ladder(self, rows, whys, keep=3, top=2.6, x=-0.3, buff=0.55, edge=6.9)
        with self.voiceover(
            "How much capital, as the record grows. <bookmark mark='a'/> Take a prior over true Sharpe ratios centred on "
            "zero, and a live record of T years. <bookmark mark='b'/> The posterior mean shrinks the measured ratio "
            "toward zero, by a factor that rises with the record's length. <bookmark mark='c'/> With a prior spread of "
            "one half, a year's record is believed one fifth; four years', one half; ten years', nearly three quarters. "
            "Size in proportion, and capital follows the evidence: the ramp that platforms run by rule of thumb."
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

    def retire(self):
        cards = VGroup(
            desk_question(r"decay is the default", r"every edge in this series weakened after it was published or "
                          r"crowded (Parts 24, 32, 33); monitoring compares live returns with the review's forecast",
                          width=12.4, font_size=19),
            desk_question(r"retire on evidence", r"a book is cut when its live record makes the posterior Sharpe ratio "
                          r"too small to pay for its capital, or its costs exceed the bound", width=12.4, font_size=19),
            desk_question(r"keep the record", r"a retired strategy stays in the log with its trials, so the next idea "
                          r"that resembles it is charged for the family", width=12.4, font_size=19),
        ).arrange(DOWN, buff=0.25)
        with self.voiceover(
            "And retirement. <bookmark mark='a'/> Decay is the default: every edge in this series weakened after it was "
            "published or crowded. <bookmark mark='b'/> A book is retired on evidence, when its live record makes the "
            "posterior Sharpe ratio too small to pay for its capital. <bookmark mark='c'/> And it stays in the log, with "
            "its trials, so the next idea that resembles it is charged for the whole family."
        ) as vo:
            for k, mk in enumerate(("a", "b", "c")):
                vo.wait_until(mk)
                self.play(FadeIn(cards[k], shift=UP * 0.2))
        self.wait(0.4)
        self.clear_scene()

    def question(self):
        q = pause_card(r"a strategy shows a live Sharpe ratio of 2 over one year. With a prior spread of 0.5 centred on "
                       r"zero, what is the posterior mean, and after four years at the same rate?")
        with self.voiceover(
            "Pause and predict. A strategy shows a live Sharpe ratio of two over one year. With a prior spread of one "
            "half centred on zero, what is the posterior mean? And after four years at the same rate?"
        ):
            self.play(FadeIn(q))
        self.wait(0.5)
        self.clear_scene()

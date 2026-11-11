from __future__ import annotations

import math

import numpy as np

from explainer.quant import *  # noqa: F403
from videos.quant.quant34.common import BAD, FIRM_C, GOOD, HURDLE, OOS_C, PART, PM_C, comma, fit_right, load


class Process(VoiceoverScene):
    def construct(self):
        self.card()
        self.pipeline()
        self.review()
        self.record()
        self.protocol()
        self.incubation()
        self.ramp()
        self.retire()
        self.question()

    def card(self):
        c = chapter_card(4, r"From idea to capital", r"How does a firm decide which research to trust with money?",
                         part=PART)
        self.add(c)
        with self.voiceover('Chapter four. A research firm needs a process for deciding which ideas deserve further study and, eventually, carefully controlled capital. We describe review, accounting, incubation and an illustrative Bayesian ramp. This review does not open the House sealed-result regression or claim that the complete live process has been implemented.'):
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
        turn = VGroup(Line(boxes[3].get_bottom(), [boxes[3].get_x(), 0.2, 0], color=GREY_B, stroke_width=2), Line([boxes[3].get_x(), 0.2, 0], [boxes[4].get_x(), 0.2, 0], color=GREY_B, stroke_width=2), Arrow([boxes[4].get_x(), 0.2, 0], boxes[4].get_top(), buff=0.04, color=GREY_B, stroke_width=2, max_tip_length_to_length_ratio=0.2))
        notes = wrapped_label(r"most ideas stop at the backtest or the review; the House's version of each step is in "
                              r"brackets on the next pages", 11.0, 16, GREY_A).to_edge(DOWN, buff=0.6)
        self.add(boxes[0], notes)
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
        cards = VGroup(desk_question('how many trials?', "every variant, parameter and universe tried counts (Part 26); the House's counter is the firm's research log, made public", width=6.2, font_size=26), desk_question('is it after costs, at size?', 'costs on every leg (Part 33), capacity from the square-root law (Part 31), and the borrow on the short side', width=6.2, font_size=26), desk_question('why should it work?', 'who pays the premium and why they keep paying (Part 32); a rule with no reason is the first to decay', width=6.2, font_size=26), desk_question('what does it add?', 'its correlation with what the firm already runs; a good strategy that duplicates a book adds risk, not return (Part 30)', width=6.2, font_size=26)).arrange_in_grid(rows=2, cols=2, buff=0.28)
        if cards.height > 6.6:
            cards.scale_to_fit_height(6.6)
        self.add(cards[0])
        with self.voiceover(
            "What a review asks, collected from this series. <bookmark mark='a'/> How many trials did it take to find? <bookmark mark='b'/> Is it after costs, at the size the firm would run it? <bookmark mark='c'/> Why should it work, and who pays? <bookmark mark='d'/> And what does it add to what the firm already holds? A strategy can pass the first three and still be rejected for the last."
        ) as vo:
            for k, mk in enumerate(("a", "b", "c", "d")):
                vo.wait_until(mk)
                self.play(FadeIn(cards[k], shift=UP * 0.2))
        self.wait(0.4)
        self.clear_scene()

    def record(self):
        rows = [cmath(r"\text{existing recorded trials}", r"=", r"23{,}552", font_size=36),
                cmath(r"N_{\rm effective}", r"\ne", r"N_{\rm recorded}\ \text{in general}", font_size=34),
                cmath(r"\text{this review}", r":", r"\text{no sealed strategy result is consulted}", font_size=30)]
        whys = [why(r"unchanged registration metadata through Part 34; this lesson adds no market trial"),
                why(r"shared data, assets, models and selection make comparisons dependent; missing variants remain missing"),
                why(r"the excluded House regression is not loaded, fitted or used to certify a strategy")]
        step = ladder(self, rows, whys, keep=3, top=2.6, x=-0.3, buff=0.55, edge=6.9)
        self.add(rows[0], whys[0])
        with self.voiceover("Keep a search record before selecting a book. <bookmark mark='a'/> The unchanged registration metadata contains twenty-three thousand five hundred and fifty-two trials through this part; this review adds none. A count is not an effective number of independent tests. <bookmark mark='b'/> Shared data and modeling choices create dependence, and unlogged variants cannot be recovered from a winning result. <bookmark mark='c'/> We do not open or regress sealed strategy outcomes here. The process lesson is an evaluation protocol, not a new investment verdict.") as vo:
            step(0)
            vo.wait_until("a")
            vo.wait_until("b")
            step(1)
            vo.wait_until("c")
            step(2)
        self.clear_scene()

    def protocol(self):
        head = label(r"Clock, positions and cash before a performance claim", font_size=30).to_edge(UP, buff=0.5)
        model = MathTex(r"\mathcal F_t\longrightarrow q_t\longrightarrow q_t^\top\Delta P_{t+1}", font_size=36).shift(UP * 0.6)
        ledger = MathTex(r"\Delta W=q^\top\Delta P+\text{cash}-\text{borrow}-\text{fees}-\text{impact}", font_size=30).shift(DOWN * 0.6)
        note_ = wrapped_label(r"Publication and rebalance times; executable prices; every hedge and cash leg; fixed evaluation and retirement rules.", 11.8, 23).shift(DOWN * 1.8)
        self.add(head, model, ledger, note_)
        with self.voiceover("An evaluation starts with the information clock and the ledger. State when a datum becomes available, when a position can be chosen, and the earliest executable price. A fitted residual is not itself a self-financing portfolio. Reconstruct positions, financing, borrow, fees and impact on every leg. Separate exploratory research from a specified later evaluation, and report uncertainty and selection. These requirements are proposed review criteria. No stored sealed result is opened to fill this panel."):
            self.wait(0.4)
        self.clear_scene()

    def incubation(self):
        cards = VGroup(
            desk_question(r"what live trading tests", r"real fills, real costs, data that arrives late or revised, and "
                          r"the firm's own impact: everything a backtest assumes", width=12.4, font_size=26),
            desk_question(r"what it cannot test", r"precision under an iid low-Sharpe model: six months has approximate standard error "
                          r"about 1.4; operational checks alone do not establish a premium", width=12.4, font_size=26),
            desk_question(r"paper, then small, then larger", r"a strategy earns capital by surviving each stage with its "
                          r"costs and slippage inside the bounds the review predicted", width=12.4, font_size=26),
        ).arrange(DOWN, buff=0.25)
        se6 = 1 / math.sqrt(0.5)
        if cards.height > 6.6:
            cards.scale_to_fit_height(6.6)
        self.add(cards[0])
        with self.voiceover(
            f"""Incubation checks implementation as well as statistics. <bookmark mark='a'/> Small live positions can reveal fills, financing, delayed or revised data and impact that a simulation misses. <bookmark mark='b'/> Under an iid low-Sharpe approximation, six months gives a Sharpe standard error around {se6:.1f}; that is weak precision, not an impossibility theorem for every test. <bookmark mark='c'/> Operational consistency is necessary but does not prove an enduring premium. Any progression in size needs specified evidence, limits and stop conditions."""
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
                    r"proportionally only under a stated objective, comparable risk and additional limits")]
        step = ladder(self, rows, whys, keep=3, top=2.6, x=-0.3, buff=0.55, edge=6.9)
        self.add(rows[0], whys[0])
        with self.voiceover(
            "Here is a chosen Bayesian illustration. <bookmark mark='a'/> True annual Sharpe has a normal prior centered at zero, and the estimated ratio has a normal likelihood with variance one over T. The latter is an iid low-Sharpe approximation. <bookmark mark='b'/> Posterior mean equals the measured ratio times T tau squared over one plus T tau squared. <bookmark mark='c'/> With prior spread one half, the weights are one fifth after one year, one half after four, and about five sevenths after ten. Proportional sizing needs comparable fixed risk and a stated objective; financing, caps, covariance, selection and prior calibration remain separate."
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
            desk_question('monitor for structural change', 'edges can decay; monitor evidence against a specified forecast, without claiming every strategy has demonstrated live decay',
                          width=12.4, font_size=26),
            desk_question(r"retire on evidence", r"a book is cut when its live record makes the posterior Sharpe ratio "
                          r"too small to pay for its capital, or its costs exceed the bound", width=12.4, font_size=26),
            desk_question(r"keep the record", r"a retired strategy stays in the log with its trials, so the next idea "
                          r"that resembles it is charged for the family", width=12.4, font_size=26),
        ).arrange(DOWN, buff=0.25)
        if cards.height > 6.6:
            cards.scale_to_fit_height(6.6)
        self.add(cards[0])
        with self.voiceover(
            "Retirement needs a specified decision rule. <bookmark mark='a'/> Edges can decay through competition, structural change or costs, but not every strategy in this series has a demonstrated live decay. <bookmark mark='b'/> A posterior comparison is conditional on its prior and likelihood; covariance, financing and opportunity cost also matter for capital allocation. <bookmark mark='c'/> Retired ideas remain in the search log. These are proposed governance practices, not claims that a live process has been implemented."
        ) as vo:
            for k, mk in enumerate(("a", "b", "c")):
                vo.wait_until(mk)
                self.play(FadeIn(cards[k], shift=UP * 0.2))
        self.wait(0.4)
        self.clear_scene()

    def question(self):
        q = pause_card('Use the stated assumptions; derive the result and check its units and denominator.')
        working = MathTex('S\\sim N(0,0.5^2),\\quad \\hat S_T\\mid S\\sim N(S,1/T),\\quad \\hat S_T=2', font_size=32).move_to(UP*0.9)
        if working.width > 12.1:
            working.scale_to_fit_width(12.1)
        setup_note = wrapped_label('Complete the square for T=1 and T=4. The likelihood is a chosen iid low-Sharpe approximation; a posterior mean is not a complete capital policy.', 11.7, 23).move_to(DOWN*0.8)
        self.add(working, setup_note, q)
        with self.voiceover('Pause and predict. Use the stated Normal prior with spread one half and the chosen likelihood variance one over T. If observed Sharpe is two, what are the posterior means after one and four years? This is a conditional illustration, not a validated allocation rule.'):
            self.wait(0.5)
        self.wait(0.5)
        self.clear_scene()

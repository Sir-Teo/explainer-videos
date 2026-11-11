from __future__ import annotations

import numpy as np

from explainer.quant import *  # noqa: F403
from videos.quant.quant26.common import BAD, GOOD, HURDLE, IS_C, OOS_C, PART, RULE, ask, comma, fit_right, illustration, load


class PBO(VoiceoverScene):
    def construct(self):
        p = load("pbo")
        self.card()
        self.blocks()
        self.logit()
        self.hists(p)
        self.degrade(p)
        self.limits()
        self.question()

    def card(self):
        c = chapter_card(9, r"The probability of backtest overfitting", r"How often does the in-sample winner lose?",
                         lit=(2014,), part=PART)
        with self.voiceover("Chapter nine. The probability of backtest overfitting: how often the configuration chosen "
                            "in sample turns out worse than the median out of sample."):
            self.play(FadeIn(c[0], shift=UP * 0.2), FadeIn(c[1]))
        self.play(FadeOut(c))

    def blocks(self):
        S = 16
        rng = np.random.default_rng(3)
        W, H = 0.62, 3.2
        cells = VGroup(*[Rectangle(width=W, height=H, stroke_color=GREY_C, stroke_width=1.5, fill_color=GREY_D,
                                   fill_opacity=0.3) for _ in range(S)]).arrange(RIGHT, buff=0.08).move_to(UP * 0.6)
        lab_t = label(r"time: the backtest's $T$ days, cut into $S = 16$ blocks", font_size=20, color=GREY_A).next_to(
            cells, UP, buff=0.25)
        conf = VGroup(*[Line(cells.get_left() + RIGHT * 0.05 + DOWN * (H / 2 - 0.25 - 0.3 * k),
                             cells.get_right() + LEFT * 0.05 + DOWN * (H / 2 - 0.25 - 0.3 * k), color=RULE,
                             stroke_width=1.2, stroke_opacity=0.5) for k in range(10)])
        conf_l = label(r"each line: one of $N$ configurations' returns", font_size=17, color=RULE).next_to(cells, DOWN,
                                                                                                         buff=0.2)
        combos = [sorted(rng.choice(S, S // 2, replace=False)) for _ in range(4)]
        steps = VGroup(
            label(r"1. choose 8 blocks as in-sample (gold); the other 8 are out-of-sample (teal)", font_size=19),
            label(r"2. find the configuration with the best Sharpe ratio in sample", font_size=19),
            label(r"3. find its rank $\omega$ among all $N$ out of sample, as a fraction", font_size=19),
            label(r"4. repeat for every one of the $\binom{16}{8} = 12{,}870$ ways to choose", font_size=19),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.12).to_edge(DOWN, buff=0.35)
        with self.voiceover(
            "Bailey, Borwein, Lopez de Prado and Zhu proposed combinatorially symmetric cross-validation. "
            "<bookmark mark='a'/> Take the matrix of every configuration's returns, day by day, and cut time into "
            "sixteen blocks. <bookmark mark='b'/> Choose eight blocks as the in-sample set, and leave the other eight out. "
            "Find the configuration with the best in-sample Sharpe ratio. Then find where it ranks among all of them in "
            "the eight blocks it never saw. <bookmark mark='c'/> And repeat for every one of the twelve thousand eight "
            "hundred and seventy ways to choose eight blocks of sixteen. Each split is symmetric, half and half, and "
            "every block is in sample exactly as often as out."
        ) as vo:
            self.play(FadeIn(cells), FadeIn(lab_t))
            vo.wait_until("a")
            self.play(LaggedStart(*[Create(c_) for c_ in conf], lag_ratio=0.1), FadeIn(conf_l))
            vo.wait_until("b")
            self.play(FadeIn(steps[0]), FadeIn(steps[1]), FadeIn(steps[2]))
            vo.wait_until("c")
            self.play(FadeIn(steps[3]))
            for cb in combos:
                self.play(*[cells[i].animate.set_fill(IS_C if i in cb else OOS_C, opacity=0.55) for i in range(S)],
                          run_time=0.7)
        self.wait(0.4)
        self.clear_scene()

    def logit(self):
        rows = [cmath(r"\omega_c", r"=", r"\frac{\#\{b_i<b_j\}+\tfrac12\#\{b_i=b_j\}+\tfrac12}{N+1}", font_size=36,
                      colors={r"\omega_c": OOS_C}),
                cmath(r"\lambda_c", r"=", r"\ln\frac{\omega_c}{1 - \omega_c}", font_size=40, colors={r"\lambda_c": HURDLE}),
                cmath(r"\text{PBO}", r"=", r"\Pr(\lambda_c \le 0)", font_size=42, colors={r"\text{PBO}": BAD})]
        whys = [why(r"near 1: the in-sample winner is also near the top out of sample; near 0: it is near the bottom"),
                why(r"the logit spreads the rank over the line: positive when the winner beats the out-of-sample median"),
                why(r"the fraction of overlapping splits at or below the median; this need not be calibrated for "
                    r"future deployment outcomes")]
        step = ladder(self, rows, whys, keep=3, top=2.9, x=-0.5, buff=0.45, edge=6.9)
        with self.voiceover(
            "Summarise each combinatorial split by a relative rank. <bookmark mark='a'/> The implementation uses a half-tie rank and an offset to keep the rank fraction inside zero and one. <bookmark mark='b'/> Its logit is positive above the later half-sample median. <bookmark mark='c'/> The reported PBO is the fraction of splits whose selected rule is at or below that median. The splits overlap heavily; the fraction is not a probability calibrated for a future trading failure. Even a value of zero neither guarantees the top rank in every split nor rules out overfitting."
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

    def hists(self, p):
        e = np.linspace(-8, 8, 41)
        c = (e[:-1] + e[1:]) / 2
        panels = VGroup()
        for era, title, col in (("in", r"1926--1986", IS_C), ("out", r"1987--2020", OOS_C)):
            h = np.asarray(p[era]["logit_hist"], float)
            h[-1] += 0
            top = max(1.0, float(h.max()) * 1.1)
            g = axes([-8, 8], [0, top], x_length=5.4, y_length=3.4, xlabel=r"logit $\lambda$", ylabel=r"splits",
                     xticks=[-8, -4, 0, 4, 8], yticks=[], font_size=13)
            ax = g.ax
            w = ax.c2p(e[1], 0)[0] - ax.c2p(e[0], 0)[0]
            bars = VGroup(*[Rectangle(width=w * 0.9, height=ax.c2p(0, v)[1] - ax.c2p(0, 0)[1], stroke_width=0,
                                      fill_color=BAD if x < 0 else col, fill_opacity=0.8).move_to(
                [ax.c2p(x, 0)[0], (ax.c2p(0, v)[1] + ax.c2p(0, 0)[1]) / 2, 0]) for x, v in zip(c, h) if v > 0])
            zero = DashedLine(ax.c2p(0, 0), ax.c2p(0, top), color=GREY_C, stroke_width=1.5)
            cap = VGroup(label(title, font_size=22, color=col),
                         MathTex(rf"\text{{PBO}} = {p[era]['pbo']:.2f}", font_size=28, color=BAD if p[era]['pbo'] > 0.2
                                 else GOOD)).arrange(RIGHT, buff=0.4)
            outside=label(rf"outside saved window: {comma(p[era]['n_combos']-int(h.sum()))} / {comma(p[era]['n_combos'])}",font_size=16,color=GREY_A)
            panels.add(VGroup(cap, VGroup(g, zero, bars),outside).arrange(DOWN, buff=0.2))
        panels.arrange(RIGHT, buff=0.7).move_to(UP * 0.2)
        foot = wrapped_label(rf"CSCV on the 10{{,}}000 rules, {comma(p['in']['n_combos'])} splits in each era. Before "
                             r"1987 none of the selected half-sample winners ranked at or below the other half's median. This does not mean rank 1 in every split or no overfitting. Splits overlap and are not independent experiments.", 12.0, 18, GREY_A).to_edge(DOWN, buff=0.4)
        with self.voiceover(
            f"Apply CSCV separately to each research era. <bookmark mark='a'/> The earlier fraction at or below the complementary median is {p['in']['pbo']:.2f}; {p['in']['n_combos']-sum(p['in']['logit_hist']):,} logits lie outside the saved minus-eight to eight histogram window. The large omitted positive tail explains the sparse earlier plot. <bookmark mark='b'/> The later PBO is {p['out']['pbo']:.2f}, with {p['out']['n_combos']-sum(p['out']['logit_hist']):,} logits outside that window. These omitted observations are counted explicitly rather than silently clipped into bins. The full split frequency remains a descriptive, dependent half-sample diagnostic."
        ) as vo:
            self.play(FadeIn(panels[0]))
            vo.wait_until("b")
            self.play(FadeIn(panels[1]), FadeIn(foot))
        self.add(illustration(r"the House's \texttt{backtest.cscv}, $S = 16$"))
        self.wait(0.4)
        self.clear_scene()

    def degrade(self, p):
        xx=np.concatenate([np.asarray(p[e]["is_sr"],float) for e in ("in","out")]);yy=np.concatenate([np.asarray(p[e]["oos_sr"],float) for e in ("in","out")]);xlo=min(-.5,float(xx.min())-.05);xhi=max(2.2,float(xx.max())+.05);ylo=min(-1.,float(yy.min())-.05);yhi=max(2.2,float(yy.max())+.05)
        g = axes([xlo,xhi], [ylo,yhi], x_length=6.0, y_length=4.6, xlabel=r"the winner's Sharpe ratio in sample",
                 ylabel=r"the same rule out of sample", xticks=[0, 1, 2], yticks=[-1, 0, 1, 2], font_size=14).to_edge(
            LEFT, buff=0.7).shift(DOWN * 0.3)
        ax = g.ax
        diag = DashedLine(ax.c2p(max(xlo,ylo), max(xlo,ylo)), ax.c2p(min(xhi,yhi), min(xhi,yhi)), color=GREY_C, stroke_width=1.5)
        zero = Line(ax.c2p(xlo, 0), ax.c2p(xhi, 0), color=GREY_D, stroke_width=1)
        clouds = VGroup()
        for era, col in (("in", IS_C), ("out", OOS_C)):
            a, b = np.asarray(p[era]["is_sr"]), np.asarray(p[era]["oos_sr"])
            clouds.add(VGroup(*[Dot(ax.c2p(x,y), radius=0.025, color=col,
                                    fill_opacity=0.6) for x, y in zip(a, b)]))
        side = VGroup(
            MathTex(rf"1926\text{{--}}86:\ {p['in']['mean_is']:.2f} \to {p['in']['mean_oos']:.2f}", font_size=26, color=IS_C),
            MathTex(rf"1987\text{{--}}2020:\ {p['out']['mean_is']:.2f} \to {p['out']['mean_oos']:.2f}", font_size=26,
                    color=OOS_C),
            MathTex(rf"\text{{losses out of sample}}:\ {100 * p['out']['oos_loss']:.0f}\%", font_size=24, color=BAD),
            wrapped_label(r"each dot is one split: the in-sample winner's Sharpe ratio in its eight blocks, and in the "
                          r"other eight. On the diagonal, nothing is lost", 3.6, 15, GREY_A),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.24).to_edge(RIGHT, buff=0.35)
        fit_right(side)
        with self.voiceover(
            f"Here are eight hundred saved split pairs from each era, displayed without clipping their returns. <bookmark mark='a'/> In the earlier era the mean selected ratio is {p['in']['mean_is']:.2f} in selection blocks and {p['in']['mean_oos']:.2f} in the complementary blocks. <bookmark mark='b'/> In the later era the corresponding means are {p['out']['mean_is']:.2f} and {p['out']['mean_oos']:.2f}; {100*p['out']['oos_loss']:.1f} percent have a negative complementary ratio. These are descriptive half-sample diagnostics, not independent prospective tests or a decomposition of the source of the decline."
        ) as vo:
            self.play(FadeIn(g), Create(diag), Create(zero))
            vo.wait_until("a")
            self.play(LaggedStart(*[FadeIn(d) for d in clouds[0]], lag_ratio=0.002, run_time=2), FadeIn(side[0]))
            vo.wait_until("b")
            self.play(LaggedStart(*[FadeIn(d) for d in clouds[1]], lag_ratio=0.002, run_time=2), FadeIn(side[1:]))
        self.wait(0.4)
        self.clear_scene()

    def limits(self):
        cards = VGroup(
            desk_question(r"what PBO saw", r"strong half-sample rankings and the deflated "
                          r"Sharpe ratio are descriptive diagnostics within one archive, not proof of no overfitting", width=12.2, font_size=20),
            desk_question(r"what it could not see", r"available-time inputs, executable prices and future market structure are not certified; "
                          r"each split is inside the same historical archive", width=12.2,
                          font_size=20),
            desk_question(r"so", r"a statistical test of overfitting is necessary and not sufficient: it must be joined "
                          r"by an economic reason the effect should exist, and by a test the strategy could actually "
                          r"trade", width=12.2, font_size=20),
        ).arrange(DOWN, buff=0.25)
        with self.voiceover(
            "Be precise about the scope. <bookmark mark='a'/> Strong early half-sample rankings indicate stability within that archive and rule grid. They do not prove absence of overfitting, point-in-time data quality or tradeability. <bookmark mark='b'/> Stale recorded prices are a possible implementation concern; the split diagnostic alone cannot identify that mechanism or predict a market-structure change. <bookmark mark='c'/> Use independent economic reasoning, available-time inputs, realistic fills and costs, and a fresh evaluation protocol. Statistical selection diagnostics answer only part of that problem."
        ) as vo:
            for k, mk in enumerate(("a", "b", "c")):
                if k:
                    vo.wait_until(mk)
                self.play(FadeIn(cards[k], shift=UP * 0.2))
        self.wait(0.4)
        self.clear_scene()

    def question(self):
        q = ask(r"CSCV gives a PBO of 0.05 for your strategy family on 2000--2020, but 90\% of the family's tries share "
                r"one feature: they all buy after big down days. What would you test next?")
        with self.voiceover(
            "Pause and predict. CSCV gives your family of strategies a probability of overfitting of only five percent "
            "on 2000 to 2020, but nearly all of them share one feature: they buy after big down days. What would you "
            "test next?"
        ):
            self.play(FadeIn(q))
        self.wait(0.5)
        self.clear_scene()

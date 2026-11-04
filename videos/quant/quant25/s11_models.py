from __future__ import annotations

import numpy as np

from explainer.quant import *  # noqa: F403
from videos.quant.quant25.common import BAD, GOOD, HURDLE, NOISE, PART, SDF, TRUE, ask, fit_right, illustration, load


class Models(VoiceoverScene):
    def construct(self):
        m = load("models")
        self.card()
        self.insight()
        self.named(m)
        self.scatter(m)
        self.top(m)
        self.bayes()
        self.lesson()

    def card(self):
        c = chapter_card(10, r"Comparing models", r"Which factor model is best, and how would you know?", lit=(2018,),
                         part=PART)
        with self.voiceover("Chapter ten. Not whether a model is true, but which of several is best."):
            self.play(FadeIn(c[0], shift=UP * 0.2), FadeIn(c[1]))
        self.play(FadeOut(c))

    def insight(self):
        rows = [cmath(r"\text{GRS}(f; R)", r"\propto", r"SR^2(f, R) - SR^2(f)", font_size=40, colors={r"\text{GRS}(f; R)": BAD}),
                cmath(r"f_A \succ f_B", r"\iff", r"SR^2(f_A) > SR^2(f_B)", font_size=42, colors={r"f_A \succ f_B": GOOD})]
        whys = [why(r"Part 24's geometry: a model's failure on any test assets is the Sharpe ratio they add to its factors"),
                why(r"Barillas and Shanken (2017, 2018): so with traded factors, comparing two models needs no test assets "
                    r"at all. The better model is the one whose factors reach the higher squared Sharpe ratio, because "
                    r"it leaves less for any asset to add")]
        step = ladder(self, rows, whys, keep=2, top=2.5, x=-0.6, buff=0.8, edge=6.9)
        with self.voiceover(
            "Recall Part twenty-four's geometry: a model fails on some test assets exactly to the extent that they "
            "raise the best Sharpe ratio beyond what its factors reach. <bookmark mark='a'/> Francisco Barillas and Jay "
            "Shanken drew the conclusion. With traded factors, comparing two models needs no test assets at all. The "
            "better model is the one whose own factors reach the higher squared Sharpe ratio, because it leaves less "
            "for any asset to add. Choose the test assets and you can make almost any model win; this comparison "
            "cannot be gamed that way."
        ) as vo:
            step(0)
            vo.wait_until("a")
            step(1)
        self.wait(0.4)
        self.clear_scene()

    def named(self, m):
        nm = m["named"]
        order = ["CAPM", "FF3", "Carhart", "FF5", "FF6", "q4", "q5"]
        hx = [-4.4, -1.6, 0.8, 3.4]
        heads = [r"model", r"$SR^2$, 1967--1993", r"$SR^2$, 1967--2020", r"Sharpe, 1994--2020"]
        tab = VGroup(VGroup(*[label(h_, font_size=17, color=GREY_A).move_to([x, 2.6, 0]) for h_, x in zip(heads, hx)]))
        names = {"CAPM": r"CAPM", "FF3": r"Fama--French 3", "Carhart": r"Carhart 4", "FF5": r"Fama--French 5",
                 "FF6": r"Fama--French 5 + UMD", "q4": r"q-factor (4)", "q5": r"q5 (+ expected growth)"}
        for i, k in enumerate(order):
            r_ = nm[k]
            y = 2.0 - 0.55 * i
            tab.add(VGroup(label(names[k], font_size=18).move_to([hx[0], y, 0]),
                           MathTex(f"{r_['sh2_in']:.2f}", font_size=24).move_to([hx[1], y, 0]),
                           MathTex(f"{r_['sh2_full']:.2f}", font_size=24).move_to([hx[2], y, 0]),
                           MathTex(f"{r_['sr_out']:.2f}", font_size=24, color=GOOD if r_["sr_out"] > 0.6 else WHITE).move_to(
                               [hx[3], y, 0])))
        foot = wrapped_label(r"annualised. The squared Sharpe ratio of each model's tangency portfolio, in the first half "
                             r"and over the whole window; and the Sharpe ratio of the first half's tangency weights held "
                             r"through the second half. q5 leads, mostly through its expected-growth factor", 12.0, 16,
                             GREY_A).to_edge(DOWN, buff=0.35)
        with self.voiceover(
            "The usual suspects, compared that way. <bookmark mark='a'/> The CAPM reaches a squared Sharpe ratio of a "
            "tenth in 1967 to 1993; three factors seven tenths; Carhart nearly two; five factors almost three; adding "
            "momentum three and a half; the q-factor model four and a half; and the q5 model, with expected growth, "
            "seven. <bookmark mark='b'/> Held out of sample, from 1994 to 2020, the ranking mostly survives, and q5 "
            "leads with a Sharpe ratio near one and a half. But recall chapter five of Part twenty-four: the "
            "expected-growth factor uses a forecast fitted on the same data, and that deserves suspicion."
        ) as vo:
            self.play(FadeIn(tab[0]), *[FadeIn(r_[0]) for r_ in tab[1:]])
            vo.wait_until("a")
            self.play(*[FadeIn(r_[1:3]) for r_ in tab[1:]])
            vo.wait_until("b")
            self.play(*[FadeIn(r_[3]) for r_ in tab[1:]], FadeIn(foot))
        self.wait(0.4)
        self.clear_scene()

    def scatter(self, m):
        g = axes([0, 9], [-0.2, 1.8], x_length=7.0, y_length=4.4, xlabel=r"$SR^2$ in 1967--1993", ylabel=r"Sharpe ratio, "
                 r"1994--2020", xticks=[0, 2, 4, 6, 8], yticks=[0, 0.5, 1.0, 1.5], font_size=13).to_edge(LEFT, buff=0.6).shift(
            DOWN * 0.3)
        ax = g.ax
        allm = m.get("all")
        side = VGroup(
            MathTex(rf"{m['n_models']}\ \text{{models}}", font_size=26),
            MathTex(rf"\text{{rank correlation}}:\ {m['rank_corr']:.2f}", font_size=24, color=GOOD),
            wrapped_label(r"every subset of ten factors (Fama--French five, momentum, and the four q-factors beyond the "
                          r"market) that includes the market, up to six factors. In-sample rank predicts out-of-sample "
                          r"rank well: the comparison is not just fitting noise, but the top is crowded with near ties",
                          3.6, 16, GREY_A),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.28).to_edge(RIGHT, buff=0.3)
        fit_right(side)
        dots = VGroup(*[Dot(ax.c2p(min(x, 8.9), min(max(y, -0.19), 1.79)), radius=0.04, color=SDF, fill_opacity=0.7)
                        for x, y in allm])
        with self.voiceover(
            "Now every model: every subset of the ten factors that includes the market, up to six of them, three "
            "hundred and eighty-two models. <bookmark mark='a'/> The rank correlation between a model's in-sample "
            "squared Sharpe ratio and its out-of-sample Sharpe ratio is about three quarters. The comparison is not "
            "just fitting noise. But the top is crowded with near ties, models that swap one profitability factor for "
            "another, and the data cannot separate them."
        ) as vo:
            self.play(FadeIn(g), FadeIn(side[0]))
            vo.wait_until("a")
            self.play(LaggedStart(*[FadeIn(d_) for d_ in dots], lag_ratio=0.05), FadeIn(side[1]), FadeIn(side[2]))
        self.wait(0.4)
        self.clear_scene()

    def top(self, m):
        hx = [-2.4, 2.4, 4.8]
        tab = VGroup(VGroup(label(r"best five in sample", font_size=18, color=GREY_A).move_to([hx[0], 2.4, 0]),
                            label(r"$SR^2$ in", font_size=18, color=GREY_A).move_to([hx[1], 2.4, 0]),
                            label(r"Sharpe out", font_size=18, color=GREY_A).move_to([hx[2], 2.4, 0])))
        for i, r_ in enumerate(m["top_in"][:5]):
            y = 1.8 - 0.5 * i
            tab.add(VGroup(label(r", ".join(r_["model"]), font_size=17).move_to([hx[0], y, 0]),
                           MathTex(f"{r_['sh2_in']:.2f}", font_size=22).move_to([hx[1], y, 0]),
                           MathTex(f"{r_['sr_out']:.2f}", font_size=22).move_to([hx[2], y, 0])))
        foot = wrapped_label(r"every top model mixes families: size, a profitability factor, an investment factor, expected "
                             r"growth. No published model is in the top five; their pieces are", 12.0, 17,
                             GREY_A).to_edge(DOWN, buff=0.8)
        with self.voiceover(
            "The five best in sample. <bookmark mark='a'/> Every one mixes the families: the market, size, a "
            "profitability factor, an investment factor, and expected growth. No published model makes the top five, "
            "but their pieces do. The best model is a committee of the existing ones."
        ) as vo:
            self.play(FadeIn(tab[0]))
            vo.wait_until("a")
            self.play(LaggedStart(*[FadeIn(r_) for r_ in tab[1:]], lag_ratio=0.3), FadeIn(foot))
        self.wait(0.4)
        self.clear_scene()

    def bayes(self):
        rows = [cmath(r"\Pr(\mathcal M_j \mid \text{data})", r"=", r"\frac{\Pr(\text{data} \mid \mathcal M_j)\,\Pr(\mathcal M_j)}"
                      r"{\sum_k \Pr(\text{data} \mid \mathcal M_k)\,\Pr(\mathcal M_k)}", font_size=38,
                      colors={r"\Pr(\mathcal M_j \mid \text{data})": SDF})]
        whys = [why(r"Barillas and Shanken (2018) give each model a marginal likelihood in closed form, with a prior on "
                    r"how large a Sharpe ratio is plausible, and average over models. Bryzgalova, Huang and Julliard (2023) "
                    r"'ran two quadrillion models': no single model wins; the SDF is dense, built from many factors with "
                    r"small weights, and robust only when averaged")]
        step = ladder(self, rows, whys, keep=1, top=2.4, x=-0.4, buff=0.8, edge=6.9)
        with self.voiceover(
            "The Bayesian version gives each model a probability. Barillas and Shanken derived each model's marginal "
            "likelihood in closed form, with a prior on how large a Sharpe ratio is plausible, chapter six's "
            "kappa again. Svetlana Bryzgalova, Jiantao Huang and Christian Julliard pushed it to every combination of "
            "fifty factors, two quadrillion models. No single model wins. The discount factor that emerges is dense: "
            "many factors, each with a small weight, and robust only when averaged over models."
        ) as vo:
            step(0)
        self.wait(0.4)
        self.clear_scene()

    def lesson(self):
        cards = VGroup(
            desk_question(r"compare by Sharpe, not by test assets", r"with traded factors, the squared Sharpe ratio "
                          r"ranks models; test assets chosen by the modeller can make anything win", width=12.0, font_size=20),
            desk_question(r"average, do not choose", r"near ties at the top mean the choice is noise; model averaging and "
                          r"shrinkage, as in chapter 6, are more robust than any one winner", width=12.0, font_size=20),
        ).arrange(DOWN, buff=0.35)
        with self.voiceover(
            "So: <bookmark mark='a'/> compare traded-factor models by the squared Sharpe ratio their factors reach, "
            "not by test assets the modeller chose. <bookmark mark='b'/> And when the top is a crowd of near ties, "
            "average over it rather than crowning one. That is what the shrinkage discount factor of chapter six does."
        ) as vo:
            for i, mk in enumerate(("a", "b")):
                vo.wait_until(mk)
                self.play(FadeIn(cards[i], shift=UP * 0.2))
        self.wait(0.4)
        self.clear_scene()
        q = ask(r"model A beats model B on the 25 size--value portfolios, but B's factors reach a higher squared Sharpe "
                r"ratio. Which is better, and why can the test assets mislead?")
        with self.voiceover("Model A beats model B on the twenty-five size and value portfolios, but B's factors reach a "
                            "higher squared Sharpe ratio. Which is better, and why can the test assets mislead?"):
            self.play(FadeIn(q))
        self.wait(0.5)
        self.clear_scene()

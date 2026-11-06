from __future__ import annotations

import numpy as np

from videos.stats.stats26.common import *  # noqa: F403


class Decisions(VoiceoverScene):
    def construct(self):
        self.card()
        self.utility()
        self.losses()
        self.admissible()
        self.coaching()
        self.voi()
        self.evsi()

    def card(self):
        card = chapter_card(9, r"Decisions", r"Expected utility, \ and what information is worth", lit=(1954,), part=PART)
        with self.voiceover("Chapter nine. Decisions."):
            self.play(FadeIn(card[0], shift=UP * 0.2), FadeIn(card[1]))
        self.play(FadeOut(card))

    def utility(self):
        rows = [
            cmath(r"\text{actions } a", r",", r"\ \text{utility } U(a, \theta)", font_size=30),
            cmath(r"a^*", r"=", r"\arg\max_a \, E\{U(a, \theta) \mid y\} = \arg\max_a \textstyle\int U(a, \theta)\, p(\theta \mid y)\, d\theta", font_size=26),
            cmath(r"\text{why}", r":", r"\text{coherent preferences } \Rightarrow \text{ a utility and a probability}", font_size=28),
            cmath(r"\text{the posterior}", r":", r"\text{an input to decisions, \ not the end}", font_size=30),
        ]
        rows[1][2].set_color(SHRUNK)
        whys = [why(r"what we can do; \ what we care about"), why(r"maximize expected utility"),
                why(r"von Neumann \& Morgenstern (1944); \ Savage (1954)"), why(r"Part 45's decision theory")]
        with self.voiceover(
            "<bookmark mark='a'/> Statistics is often done to decide something. Write down the actions available, and a "
            "utility saying how good each action is if the truth is theta. <bookmark mark='b'/> The Bayesian rule is to "
            "choose the action with the highest expected utility under the posterior. <bookmark mark='c'/> Leonard Savage's "
            "1954 theorem says any coherent ordering of preferences among gambles behaves as if it maximized expected "
            "utility under some probability, which is one of the deepest arguments for being Bayesian. "
            "<bookmark mark='d'/> The posterior is an input to decisions, not the end of the analysis."
        ) as vo:
            step = ladder(self, rows, whys, keep=4, top=2.6, x=-0.9, buff=0.85, edge=6.9)
            for k, m_ in enumerate("abcd"):
                vo.wait_until(m_)
                step(k, transform=False)
        self.clear_scene()

    def losses(self):
        rows = [
            cmath(r"(a - \theta)^2", r"\Rightarrow", r"a^* = \text{posterior mean}", font_size=30),
            cmath(r"|a - \theta|", r"\Rightarrow", r"a^* = \text{posterior median}", font_size=30),
            cmath(r"1\{a \ne \theta\}", r"\Rightarrow", r"a^* = \text{posterior mode}", font_size=30),
            cmath(r"c_1(\theta - a)_+ + c_2(a - \theta)_+", r"\Rightarrow", r"\text{the } \tfrac{c_1}{c_1 + c_2} \text{ quantile}", font_size=28),
        ]
        rows[3][2].set_color(SHRUNK)
        whys = [why(r"squared error"), why(r"absolute error"), why(r"all-or-nothing"),
                why(r"Part 23's check loss: \ overstock vs understock")]
        with self.voiceover(
            "<bookmark mark='a'/> Even a point estimate is a decision. Under squared-error loss the best estimate is the "
            "posterior mean; <bookmark mark='b'/> under absolute error, the posterior median; <bookmark mark='c'/> under "
            "all-or-nothing loss, the mode. <bookmark mark='d'/> And when overestimating costs differently from "
            "underestimating, as when a baker must not run out of bread, the best estimate is a quantile, the check loss of "
            "Part 23's quantile regression. 'Which estimate?' is answered by 'what does an error cost?'"
        ) as vo:
            step = ladder(self, rows, whys, keep=4, top=2.6, x=-0.9, buff=0.85, edge=6.9)
            for k, m_ in enumerate("abcd"):
                vo.wait_until(m_)
                step(k, transform=False)
        self.clear_scene()

    def coaching(self):
        d = load("decision")
        e = np.asarray(d["edges"])
        h = np.asarray(d["hist"])
        ymax = float(h.max()) * 1.1
        A = axes([-40, 50], [0, ymax], x_length=7.4, y_length=4.2, xlabel=r"$\theta_{\text{new}}$: \ coaching's effect in a ninth school",
                 ylabel=r"posterior predictive density", xticks=[-40, -20, 0, 20, 40], yticks=[], center=[-2.0, 0.3, 0])
        ax = A.ax
        bars = hist_bars(ax, e, h, color=POST, opacity=0.55)
        for b, lo in zip(bars, e[:-1]):
            if lo >= d["cost"]:
                b.set_fill(SHRUNK, opacity=0.7)
        cl = DashedLine(ax.c2p(d["cost"], 0), ax.c2p(d["cost"], ymax), color=PATH, stroke_width=2.5)
        rows = fit_rows(VGroup(
            label(r"a ninth school: \ adopt coaching?", font_size=22),
            label(r"it pays if the effect exceeds 5 points", font_size=22, color=PATH),
            label(rf"P($\theta_{{\text{{new}}}} > 5$) $= {d['p_exceed']:.2f}$", font_size=22, color=SHRUNK),
            label(rf"expected gain: \ ${d['mean_new']:.1f} - 5 = {d['eu_adopt']:.1f}$ points", font_size=22, color=HIT),
            label(r"adopt, \ though it fails in 1 school out of 3", font_size=22, color=GREY_A),
        ), 4.3, 0.42, [4.5, 0.3, 0])
        with self.voiceover(
            "<bookmark mark='a'/> A ninth school is deciding whether to buy the coaching course. Its effect there, theta "
            "new, is a fresh draw from the population of schools, so the posterior predictive for it combines every source of "
            "uncertainty: draw mu and tau from the posterior, then a new effect. <bookmark mark='b'/> Suppose the course is "
            "worth its cost if it raises scores by at least five points. <bookmark mark='c'/> The chance it does is two "
            "thirds. <bookmark mark='d'/> Measured in points above cost, the expected gain is about three. "
            "<bookmark mark='e'/> So adopt it, knowing it will disappoint about one school in three."
        ) as vo:
            self.add(schools_tag())
            self.play(FadeIn(A))
            vo.wait_until("a")
            self.play(LaggedStart(*[GrowFromEdge(b, DOWN) for b in bars], lag_ratio=0.02), FadeIn(rows[0]))
            vo.wait_until("b")
            self.play(Create(cl), FadeIn(rows[1]))
            vo.wait_until("c")
            self.play(FadeIn(rows[2]))
            vo.wait_until("d")
            self.play(FadeIn(rows[3]))
            vo.wait_until("e")
            self.play(FadeIn(rows[4]))
        self.clear_scene()

    def voi(self):
        d = load("decision")
        rows = [
            cmath(r"\text{now}", r":", rf"\max\{{E(\theta - 5), 0\}} = {d['eu_adopt']:.2f}", font_size=30),
            cmath(r"\text{if we knew } \theta", r":", rf"E\,\max\{{\theta - 5, 0\}} = {d['eu_adopt'] + d['evpi']:.2f}", font_size=30),
            cmath(r"\text{EVPI}", r"=", rf"{d['evpi']:.2f} \text{{ points}}", font_size=32),
            cmath(r"\text{meaning}", r":", r"\text{the most any study could be worth}", font_size=30),
        ]
        rows[2][2].set_color(SHRUNK)
        whys = [why(r"decide now"), why(r"decide after learning the truth"), why(r"the expected value of perfect information"),
                why(r"Raiffa \& Schlaifer (1961)")]
        with self.voiceover(
            "<bookmark mark='a'/> What would it be worth to find out first? Deciding now, the expected gain is two point nine "
            "three points. <bookmark mark='b'/> If we could learn the school's true effect before deciding, we'd adopt only "
            "when it pays, and the expected gain would rise to five point one two. <bookmark mark='c'/> The difference, two "
            "point one nine points, is the expected value of perfect information. <bookmark mark='d'/> No study, however "
            "large, can be worth more than that, a ceiling on what to spend finding out, from Howard Raiffa and Robert "
            "Schlaifer's 1961 book."
        ) as vo:
            step = ladder(self, rows, whys, keep=4, top=2.6, x=-0.9, buff=0.85, edge=6.9)
            for k, m_ in enumerate("abcd"):
                vo.wait_until(m_)
                step(k, transform=False)
        self.clear_scene()

    def evsi(self):
        d = load("decision")
        tot = d["evpi"]
        bar_w = 8.0
        full = Rectangle(width=bar_w, height=0.8, stroke_color=GREY_B, stroke_width=1.5, fill_opacity=0).move_to([0, 0.8, 0])
        part = Rectangle(width=bar_w * d["evsi"] / tot, height=0.8, stroke_width=0, fill_color=SHRUNK, fill_opacity=0.8)
        part.align_to(full, LEFT).set_y(0.8)
        rows = fit_rows(VGroup(
            label(rf"perfect information: \ {d['evpi']:.2f} points", font_size=24, color=GREY_A),
            label(rf"one pilot experiment in the school, \ SE {d['se']:.0f}: \ {d['evsi']:.2f} points", font_size=24, color=SHRUNK),
            label(r"run the pilot if it costs less than that", font_size=24, color=HIT),
            label(r"pre-posterior analysis: \ simulate the study, \ then the decision", font_size=22, color=GREY_A),
        ), 11.0, 0.35, [0, -1.4, 0])
        with self.voiceover(
            "<bookmark mark='a'/> Real studies are imperfect. The outer box is the value of perfect information. "
            "<bookmark mark='b'/> A pilot experiment in the new school, as noisy as the original eight, with a standard "
            "error of ten points, is worth one point two one: the expected value of sample information, a little over half "
            "the ceiling. <bookmark mark='c'/> If the pilot costs less than that, run it. <bookmark mark='d'/> It is computed "
            "by simulation: imagine the pilot's result, update, decide, and average over possible results, a pre-posterior "
            "analysis. The same reasoning sizes clinical trials, Part 35."
        ) as vo:
            self.add(schools_tag())
            vo.wait_until("a")
            self.play(Create(full), FadeIn(rows[0]))
            vo.wait_until("b")
            self.play(GrowFromEdge(part, LEFT), FadeIn(rows[1]))
            vo.wait_until("c")
            self.play(FadeIn(rows[2]))
            vo.wait_until("d")
            self.play(FadeIn(rows[3]))
        self.clear_scene()

    def admissible(self):
        rows = [
            cmath(r"R(\theta, \delta)", r"=", r"E_\theta\, L(\theta, \delta(y)): \ \text{frequentist risk}", font_size=30),
            cmath(r"r(\delta)", r"=", r"\textstyle\int R(\theta, \delta)\, p(\theta)\, d\theta: \ \text{Bayes risk}", font_size=30),
            cmath(r"\text{Bayes rule}", r":", r"\text{minimizes } r; \ \text{the posterior expected loss, \ case by case}", font_size=28),
            cmath(r"\text{Wald}", r":", r"\text{admissible rules are (limits of) Bayes rules}", font_size=30),
        ]
        rows[3][2].set_color(SHRUNK)
        whys = [why(r"average over data, \ for fixed $\theta$"), why(r"then average over the prior"),
                why(r"minimizing pointwise minimizes the average"), why(r"the complete class theorem: \ Part 45")]
        with self.voiceover(
            "<bookmark mark='a'/> Decision theory also links the two schools. A frequentist judges a rule by its risk, the "
            "expected loss over data for each fixed theta. <bookmark mark='b'/> Average that over a prior and you get the "
            "Bayes risk. <bookmark mark='c'/> The rule minimizing it is found case by case, by minimizing posterior "
            "expected loss for the data actually seen. <bookmark mark='d'/> Abraham Wald's complete class theorem says the "
            "admissible rules, those no other rule beats everywhere, are essentially the Bayes rules and their limits. "
            "Stein's paradox in Part 25 was a frequentist discovering this the hard way."
        ) as vo:
            step = ladder(self, rows, whys, keep=4, top=2.6, x=-0.9, buff=0.85, edge=6.9)
            for k, m_ in enumerate("abcd"):
                vo.wait_until(m_)
                step(k, transform=False)
        self.clear_scene()

from __future__ import annotations

import numpy as np

from videos.stats.stats36.common import *  # noqa: F403


class Unconfounded(VoiceoverScene):
    def construct(self):
        self.card()
        self.assumption()
        self.identify()
        self.world()
        self.overlap()
        self.untestable()

    def card(self):
        card = chapter_card(1, r"Unconfoundedness and overlap", r"The assumptions that replace a coin", lit=(1983,), part=PART)
        with self.voiceover("Chapter one. Unconfoundedness and overlap."):
            self.play(FadeIn(card[0], shift=UP * 0.2), FadeIn(card[1]))
        self.play(FadeOut(card))

    def assumption(self):
        rows = [
            cmath(r"\text{randomized}", r":", r"(Y(0), Y(1)) \perp\!\!\!\perp T", font_size=32),
            cmath(r"\text{unconfounded}", r":", r"(Y(0), Y(1)) \perp\!\!\!\perp T \mid X", font_size=32),
            cmath(r"\text{overlap}", r":", r"0 < e(x) = P(T = 1 \mid X = x) < 1", font_size=32),
            cmath(r"\text{together}", r":", r"\text{`strong ignorability'}", font_size=32),
        ]
        rows[1][-1].set_color(TAUC)
        whys = [why(r"Part 35"), why(r"as if randomized within each $x$"), why(r"everyone could have gone either way"),
                why(r"Rosenbaum \& Rubin (1983)")]
        with self.voiceover(
            "<bookmark mark='a'/> In a randomized trial, treatment is independent of the potential outcomes. <bookmark "
            "mark='b'/> Without randomization, the best we can hope for is independence given covariates X: among patients "
            "who look alike on X, treatment is as good as random. This is unconfoundedness, also called selection on "
            "observables. <bookmark mark='c'/> We also need overlap: at every value of X, there must be some chance of "
            "either treatment, so that every kind of treated patient has comparable untreated ones. <bookmark mark='d'/> "
            "Paul Rosenbaum and Donald Rubin called the pair strong ignorability in 1983."
        ) as vo:
            step = ladder(self, rows, whys, keep=4, top=2.6, x=-0.9, buff=0.85, edge=6.9)
            for k, m_ in enumerate("abcd"):
                vo.wait_until(m_)
                step(k, transform=False)
        self.clear_scene()

    def identify(self):
        rows = [
            cmath(r"E[Y(1)]", r"=", r"E_X\big[E[Y(1) \mid X]\big]", font_size=32),
            cmath(r"", r"=", r"E_X\big[E[Y(1) \mid T = 1, X]\big]", font_size=32),
            cmath(r"", r"=", r"E_X\big[E[Y \mid T = 1, X]\big]", font_size=32),
            cmath(r"\tau", r"=", r"E_X\big[E[Y \mid T = 1, X] - E[Y \mid T = 0, X]\big]", font_size=30),
        ]
        rows[3][-1].set_color(BANDC)
        whys = [why(r"average over $X$"), why(r"unconfoundedness"), why(r"consistency; \ overlap makes it defined"),
                why(r"the adjustment formula")]
        with self.voiceover(
            "<bookmark mark='a'/> Under these assumptions the average effect is identified, which means it can be written "
            "in terms of the distribution of observable things. Start with the average treated outcome, and average it over "
            "X. <bookmark mark='b'/> By unconfoundedness, within each X the treated outcome has the same average among the "
            "treated as among everyone. <bookmark mark='c'/> For the treated, the treated outcome is simply what we see. "
            "Overlap ensures that there are treated patients at every X, so the conditional mean exists. <bookmark "
            "mark='d'/> The average effect is the average over X of the difference in conditional means: the adjustment "
            "formula. Every method in this part is a way of estimating it."
        ) as vo:
            step = ladder(self, rows, whys, keep=4, top=2.6, x=-0.9, buff=0.85, edge=6.9)
            for k, m_ in enumerate("abcd"):
                vo.wait_until(m_)
                step(k, transform=False)
        self.clear_scene()

    def world(self):
        d = load("obs")
        rows = fit_rows(VGroup(
            label(r"the World's observational study: \ 3,000 eligible patients, \ no trial", font_size=26),
            label(r"doctors prescribe the drug more often to higher pressures, \ older and heavier patients", font_size=26, color=Y1C),
            label(rf"{100 * d['share']:.0f}\% are treated; \ the truth: \ ATE ${d['ate']:.2f}$, \ ATT ${d['att']:.2f}$", font_size=26, color=TAUC),
            label(rf"the naive comparison: \ ${d['naive']['est']:.2f}$", font_size=26, color=MISSC),
            label(r"unconfounded given baseline, \ age, \ BMI, \ sex: \ by construction, \ here only", font_size=26, color=BANDC),
        ), 12.4, 0.55, [0, 0, 0])
        with self.voiceover(
            "<bookmark mark='a'/> The World gives us a test bed. Take three thousand eligible patients from the island and no "
            "trial at all: <bookmark mark='b'/> doctors prescribe the drug as they see fit, more often to patients with "
            "higher pressure, older patients and heavier ones. <bookmark mark='c'/> " + f"{100 * d['share']:.0f}" + " percent "
            "are treated. The World knows the truth: an average effect of minus " + say(-d["ate"], 1) + ", and minus "
            + say(-d["att"], 1) + " among the treated, who are sicker and benefit more. <bookmark mark='d'/> The naive "
            "comparison says minus " + say(-d["naive"]["est"], 1) + ". <bookmark mark='e'/> Here, unlike in life, we know that "
            "the doctors used only the four recorded covariates, so unconfoundedness holds by construction."
        ) as vo:
            self.add(obs_tag())
            for k, m_ in enumerate("abcde"):
                vo.wait_until(m_)
                self.play(FadeIn(rows[k], shift=RIGHT * 0.2))
        self.clear_scene()

    def overlap(self):
        d = load("obs")
        h1, h0 = np.asarray(d["h_t"], float), np.asarray(d["h_c"], float)
        e = np.linspace(0, 1, 21)
        A = axes([0, 1], [0, 0.35], x_length=7.4, y_length=4.2, xlabel=r"estimated propensity $\hat e(x)$", ylabel=r"share",
                 xticks=[0, 0.5, 1], yticks=[0, 0.1, 0.2, 0.3], center=[-2.0, 0.2, 0])
        ax = A.ax
        b1 = hist_bars(ax, e, h1 / h1.sum(), color=Y1C, opacity=0.5)
        b0 = hist_bars(ax, e, h0 / h0.sum(), color=Y0C, opacity=0.5)
        side = fit_rows(VGroup(
            label(r"red: \ treated; \ blue: \ untreated", font_size=22),
            label(r"the treated pile up near 1, \ the untreated near 0", font_size=22, color=TAUC),
            label(r"in between, \ both: \ overlap", font_size=22, color=BANDC),
            label(r"at the ends, \ few or no comparable patients", font_size=22, color=MISSC),
        ), 4.2, 0.42, [4.6, 0.3, 0])
        with self.voiceover(
            "<bookmark mark='a'/> Overlap can be checked. Here is each patient's estimated probability of being treated, "
            "from a logistic regression on the four covariates, for the treated in red and the untreated in blue. <bookmark "
            "mark='b'/> The treated pile up near one and the untreated near zero, as they should when doctors choose. "
            "<bookmark mark='c'/> In between both groups are present. <bookmark mark='d'/> At the ends there are few "
            "comparable patients, and the methods ahead will have to extrapolate, or weight a handful of people very heavily."
        ) as vo:
            self.add(obs_tag())
            self.play(FadeIn(A))
            vo.wait_until("a")
            self.play(FadeIn(b1), FadeIn(b0), FadeIn(side[0]))
            for k, m_ in enumerate("bcd"):
                vo.wait_until(m_)
                self.play(FadeIn(side[k + 1]))
        self.clear_scene()

    def untestable(self):
        rows = fit_rows(VGroup(
            label(r"overlap can be checked; \ unconfoundedness cannot", font_size=26, color=MISSC),
            label(r"it is a claim about what we did \emph{not} measure", font_size=26),
            label(r"so it must be argued from knowledge of how treatment was chosen", font_size=26, color=TAUC),
            label(r"the next three chapters give that argument a language: \ causal diagrams", font_size=26, color=Y0C),
        ), 12.4, 0.6, [0, 0, 0])
        with self.voiceover(
            "<bookmark mark='a'/> Overlap can be checked in the data. Unconfoundedness cannot. <bookmark mark='b'/> It is a "
            "claim about what we did not measure, and no amount of data on what we did measure can confirm it. <bookmark "
            "mark='c'/> It has to be argued from knowledge of how the treatment was actually chosen. <bookmark mark='d'/> The "
            "next chapters give that argument a precise language: causal diagrams."
        ) as vo:
            for k, m_ in enumerate("abcd"):
                vo.wait_until(m_)
                self.play(FadeIn(rows[k], shift=RIGHT * 0.2))
        self.clear_scene()

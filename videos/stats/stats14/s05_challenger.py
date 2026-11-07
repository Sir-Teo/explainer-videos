from __future__ import annotations

import numpy as np
from scipy import special, stats

from explainer.stats.kit import glm
from videos.stats.stats14.common import *  # noqa: F403


def challenger_fit():
    d = load("challenger")
    T, Y = np.asarray(d["T"]), np.asarray(d["Y"])
    return T, Y, glm.logistic(np.column_stack([np.ones(23), T]), Y)


class ChallengerFit(VoiceoverScene):
    def construct(self):
        self.card()
        self.dashboard()
        self.wald()
        self.profile()
        self.compare()
        self.extrapolation()
        self.verdict()

    def card(self):
        card = chapter_card(4, r"The Challenger fit", r"What 23 flights say about 31$^\circ$F", lit=(1986,), part=PART)
        with self.voiceover("Chapter four. The Challenger fit."):
            self.play(FadeIn(card[0], shift=UP * 0.2), FadeIn(card[1]))
        self.play(FadeOut(card))

    def dashboard(self):
        T, Y, f = challenger_fit()
        A = axes([25, 85], [-0.1, 1.15], x_length=8.4, y_length=4.8, xlabel=r"launch temperature, \ $^\circ$F", ylabel=r"$P(\text{distress})$",
                 xticks=[30, 40, 50, 60, 70, 80], yticks=[0, 0.5, 1], center=[-1.8, 0.0, 0])
        ax = A.ax
        dash = ChallengerDashboard(ax, T, Y, f, x0=81, readout_pos=[5.0, 1.0, 0])
        cold = DashedLine(ax.c2p(53, 0), ax.c2p(53, 1.1), color=GREY_C, stroke_width=1.5)
        cl = label(r"coldest flight", font_size=18, color=GREY_B).next_to(cold, UP, buff=0.05)
        foot = label(r"pointwise nominal 95\% Wald intervals on the log-odds scale", font_size=20, color=GREY_A).to_corner(DR, buff=0.4)
        with self.voiceover(
            "Here is the Challenger dashboard: the flights, the fitted curve, and a ninety-five percent band around it. "
            "<bookmark mark='a'/> At eighty-one degrees, the warmest flight, the fitted chance of O-ring distress is about "
            "two percent. <bookmark mark='b'/> At seventy, twenty-three percent. <bookmark mark='c'/> At fifty-three, the coldest "
            "flight anyone had flown, ninety-four percent, and the band is already wide. <bookmark mark='d'/> Now keep going, "
            "past the last data point, to thirty-one degrees. The fitted probability is point nine nine nine six. The band "
            "spreads out in a way we need to look at."
        ) as vo:
            self.play(FadeIn(A), FadeIn(dash.dots), Create(cold), FadeIn(cl))
            self.play(FadeIn(dash.band), Create(dash.curve), FadeIn(foot), run_time=1.5)
            self.add(dash.probe, dash.readout)
            vo.wait_until("a")
            self.wait(0.5)
            vo.wait_until("b")
            self.play(dash.slide_to(70))
            vo.wait_until("c")
            self.play(dash.slide_to(53))
            vo.wait_until("d")
            self.play(dash.slide_to(31, run_time=3.0))
            dash.stop()
        self.clear_scene()

    def wald(self):
        d = load("challenger")
        lo, hi = d["p31_wald"]
        e = d["eta31"][1]
        T, Y, f = challenger_fit()
        se = float(np.sqrt(np.array([1, 31.0]) @ f.cov() @ np.array([1, 31.0])))
        rows = [
            cmath(r"\hat\eta(31)", r"=", rf"\hat\beta_0 + 31\hat\beta_1 = {e:.2f}", font_size=32),
            cmath(r"\mathrm{SE}", r"=", rf"\sqrt{{x_0^\top (X^\top W X)^{{-1}} x_0}} = {se:.2f}", font_size=32),
            cmath(r"\eta", r"\in", rf"{e:.2f} \pm 1.96 \times {se:.2f} = [{e - 1.96 * se:.2f},\ {e + 1.96 * se:.2f}]", font_size=30),
            cmath(r"p(31)", r"\in", rf"[{lo:.2f},\ 1.00]", font_size=32),
        ]
        rows[3][2].set_color(RES)
        whys = [why(r"log-odds of distress at 31$^\circ$F: \ odds of 2,500 to 1"), why(r"Part 12's prediction SE, \ weighted"),
                why(r"a Wald interval on the log-odds scale"), why(r"mapped back: \ ``somewhere between a coin flip and certain''")]
        intro = label('Quantify extrapolation uncertainty on the log-odds scale', font_size=36)
        with self.voiceover(
            "<bookmark mark='a'/> On the log-odds scale, the fitted value at thirty-one degrees is seven point eight five, "
            "odds of about two thousand five hundred to one. <bookmark mark='b'/> Its standard error comes from the inverse "
            "information, exactly like Part 12's prediction standard error, and it's big: four point oh, because thirty-one "
            "degrees is so far from the data. <bookmark mark='c'/> The Wald interval, plus or minus one point nine six "
            "standard errors, runs from about zero to fifteen point eight. <bookmark mark='d'/> Mapped back to "
            "probabilities: from point four eight to nearly one. As stated, that's uninformative, somewhere between a coin "
            "flip and certainty. But the Wald interval trusts a quadratic approximation to the log-likelihood, far from where "
            "it was fitted."
        ) as vo:
            self.play(FadeIn(intro))
            step = ladder(self, rows, whys, keep=4, top=2.6, x=-1.2, buff=0.7, edge=6.9)
            for k, m_ in enumerate("abcd"):
                vo.wait_until(m_)
                step(k, transform=False)
                if k == 0:
                    self.play(FadeOut(intro), run_time=0.25)
        self.clear_scene()

    def profile(self):
        d = load("challenger")
        T, Y, f = challenger_fit()
        x0 = np.array([1.0, 31.0])
        es = np.linspace(-1.5, 22, 95)
        ll = []
        warm = f.coef.copy()
        for e in es:
            v, warm = glm._constrained_loglik(f, x0, e, start=warm)
            ll.append(v - f.loglik)
        ll = np.array(ll)
        eh = d["eta31"][1]
        se = float(np.sqrt(x0 @ f.cov() @ x0))
        quad = -0.5 * ((es - eh) / se) ** 2
        A = axes([-1.5, 22], [-3.5, 0.3], x_length=8.0, y_length=4.4, xlabel=r"$\eta(31)$, \ log-odds of distress at 31$^\circ$F",
                 ylabel=r"$\ell - \ell_{\max}$", xticks=[0, 5, 10, 15, 20], yticks=[-3, -2, -1, 0], center=[-1.8, 0.2, 0])
        ax = A.ax
        cp = curve(ax, es, ll, S.LIK, 4)
        cq = DashedVMobject(curve(ax, es, quad, S.ALT, 3), num_dashes=50)
        cut = DashedLine(ax.c2p(-1.5, -stats.chi2.ppf(0.95, 1) / 2), ax.c2p(22, -stats.chi2.ppf(0.95, 1) / 2), color=GREY_B, stroke_width=2)
        lo, _, hi = d["eta31"]
        m1 = DashedLine(ax.c2p(lo, -3.5), ax.c2p(lo, 0), color=S.LIK, stroke_width=2)
        m2 = DashedLine(ax.c2p(hi, -3.5), ax.c2p(hi, 0), color=S.LIK, stroke_width=2)
        rows = fit_rows(VGroup(
            label(r"green: \ the profile log-likelihood", font_size=22, color=S.LIK),
            label(r"teal: \ Wald's quadratic", font_size=22, color=S.ALT),
            label(r"keep every $\eta$ within 1.92 of the top", font_size=22),
            MathTex(rf"\eta \in [{lo:.2f},\ {hi:.1f}]", font_size=28, color=S.LIK),
            MathTex(rf"p(31) \in [{d['p31_profile'][0]:.2f},\ 1.00]", font_size=30, color=OBS),
        ), 4.0, 0.34, [4.9, 0.4, 0])
        with self.voiceover(
            "<bookmark mark='a'/> An alternative interval uses the likelihood itself with an asymptotic likelihood-ratio cutoff. For each possible value of the "
            "log-odds at thirty-one degrees, find the best fit to the flights that has that value, and record its "
            "log-likelihood. That's the profile log-likelihood, in green. <bookmark mark='b'/> The Wald interval pretends it's "
            "the teal parabola. They agree near the top and part company in the tails: the real profile falls steeply on the "
            "left, and only slowly on the right. <bookmark mark='c'/> Part 11's likelihood-ratio interval keeps every value "
            "within one point nine two of the maximum, half the chi-squared cutoff. <bookmark mark='d'/> On the log-odds scale, "
            "one point four to eighteen. <bookmark mark='e'/> As a probability, from point eight oh to one. Even at the edge "
            "most favourable to launching, the flights say distress at thirty-one degrees is at least four times as likely as "
            "not."
        ) as vo:
            self.play(FadeIn(A))
            vo.wait_until("a")
            self.play(Create(cp), FadeIn(rows[0]), run_time=2.0)
            vo.wait_until("b")
            self.play(Create(cq), FadeIn(rows[1]))
            vo.wait_until("c")
            self.play(Create(cut), FadeIn(rows[2]))
            vo.wait_until("d")
            self.play(Create(m1), Create(m2), FadeIn(rows[3]))
            vo.wait_until("e")
            self.play(FadeIn(rows[4]))
        self.clear_scene()

    def compare(self):
        d = load("challenger")
        W = 9.0
        A = axes([0, 1], [0, 3], x_length=W, y_length=2.4, xlabel=r"$p(31^\circ\text{F})$", ylabel=r"", xticks=[0, 0.25, 0.5, 0.75, 1],
                 yticks=[], center=[0, 0.8, 0])
        ax = A.ax
        wl, wh = d["p31_wald"]
        pl, ph = d["p31_profile"]
        b1 = Line(ax.c2p(wl, 2), ax.c2p(wh, 2), color=S.ALT, stroke_width=8)
        b2 = Line(ax.c2p(pl, 1), ax.c2p(ph, 1), color=S.LIK, stroke_width=8)
        dot = VGroup(Dot(ax.c2p(d["p31"], 2), color=OBS, radius=0.1), Dot(ax.c2p(d["p31"], 1), color=OBS, radius=0.1))
        l1 = label(r"Wald", font_size=24, color=S.ALT).next_to(ax.c2p(wl, 2), LEFT, buff=0.25)
        l2 = label(r"profile", font_size=24, color=S.LIK).next_to(ax.c2p(pl, 1), LEFT, buff=0.25)
        rows = fit_rows(VGroup(
            label(r"both are nominal 95\% intervals from the same fit", font_size=24),
            label(r"profile sets transform under one-to-one changes of scale", font_size=24, color=S.LIK),
            label(r"the Wald interval depends on the scale it was built on", font_size=24, color=S.ALT),
            label(r"which keeps its promise at $n = 23$? \ The Coverage Board, \ chapter six", font_size=24, color=OBS),
        ), 12.4, 0.3, [0, -1.7, 0])
        with self.voiceover(
            "<bookmark mark='a'/> Side by side: the Wald interval, point four eight to one, and the profile interval, point "
            "eight oh to one, from the same fit to the same twenty-three flights. <bookmark mark='b'/> The profile interval has "
            "a property the Wald interval lacks: it transforms consistently under one-to-one changes of scale, probability, odds or "
            "log-odds, because it's defined by the likelihood, not by an approximation on one scale. <bookmark mark='c'/> The "
            "Wald interval depends on the scale it was built on. <bookmark mark='d'/> Which keeps its promise with only "
            "twenty-three flights? Likelihood geometry favours profiling, while its chi-squared calibration is asymptotic; the Coverage Board, at the end of chapter six, has a "
            "surprise."
        ) as vo:
            self.play(FadeIn(A))
            vo.wait_until("a")
            self.play(Create(b1), FadeIn(l1), Create(b2), FadeIn(l2), FadeIn(dot), FadeIn(rows[0]))
            for k, m_ in enumerate("bcd"):
                vo.wait_until(m_)
                self.play(FadeIn(rows[k + 1]))
        self.clear_scene()

    def extrapolation(self):
        d = load("challenger")
        rows = fit_rows(VGroup(
            label(r"31$^\circ$F is 22 degrees below the coldest flight: \ an extrapolation", font_size=26, color=RES),
            label(rf"the tail is the model's: \ logit {d['p31']:.4f}, \ probit 0.999998 \ (chapter two)", font_size=24),
            label(r"linear in temperature on the log-odds scale? \ The data cannot check it below 53$^\circ$F", font_size=24),
            label(rf"Dalal et al.'s binomial model, \ 6 rings per flight: \ each ring {d['p6_31']:.2f}, \ at least one: \ virtually 1", font_size=24, color=S.ALT),
            label(r"the fitted models agree: \ colder is associated with more distress, \ and nothing in the data suggests 31$^\circ$F is safe", font_size=24, color=OBS),
        ), 12.6, 0.44, [0, 0.1, 0])
        with self.voiceover(
            "<bookmark mark='a'/> Now the caveat that every statistics course must teach with this example. Thirty-one "
            "degrees is twenty-two degrees colder than any flight: an extrapolation. <bookmark mark='b'/> The probability "
            "there comes from the model's tail, and as chapter two showed, the logit and probit tails differ by a factor of "
            "more than a hundred in the chance of no distress. <bookmark mark='c'/> And nothing in the data can check whether the "
            "log-odds keep falling in a straight line below fifty-three degrees. <bookmark mark='d'/> A second fit treats each flight's six O-rings as binomial trials, assuming equal risk and independence within flight: each ring's chance of distress at thirty-one is about "
            "point eight two, so this binomial model puts the chance of at least one distress event very near one. Shared flight conditions can violate ring independence. <bookmark mark='e'/> The models disagree about the "
            "number. They agree about the direction: colder is worse, and nothing in twenty-three flights suggests that "
            "thirty-one degrees was safe. The fitted probabilities describe thermal distress, not the probability of catastrophic vehicle loss."
        ) as vo:
            for k, m_ in enumerate("abcde"):
                vo.wait_until(m_)
                self.play(FadeIn(rows[k], shift=RIGHT * 0.2))
        self.clear_scene()

    def verdict(self):
        rows = [
            cmath(r"\text{the evidence}", r":", r"\text{all 23 flights, \ not the 7 with damage}", font_size=30),
            cmath(r"\text{the model}", r":", r"\text{logit}\,p = \beta_0 + \beta_1 T,\ \text{fitted by ML}", font_size=30),
            cmath(r"\text{the answer}", r":", r"\hat p(31) = 0.9996,\ \ \text{profile } [0.80, 1]", font_size=30),
            cmath(r"\text{the caveat}", r":", r"\text{an extrapolation \ (Lavine 1991)}", font_size=30),
        ]
        rows[2][2].set_color(OBS)
        whys = [why(r"selecting on the outcome hid the effect"), why(r"one curve, \ bounded in $[0, 1]$"),
                why(r"invariant under one-to-one changes; calibration still needs checking"), why(r"a model's tail is an assumption")]
        intro = label('Separate the evidence, model and extrapolation', font_size=36)
        with self.voiceover(
            "So, the Challenger analysis in four lines. <bookmark mark='a'/> Use all the evidence, including the flights where "
            "nothing happened: selecting on the outcome hid the effect. <bookmark mark='b'/> Model the probability with a "
            "curve that stays between zero and one, fitted by maximum likelihood. <bookmark mark='c'/> Report the "
            "estimate with an interval that respects the likelihood's shape. <bookmark mark='d'/> And say plainly that a "
            "prediction far outside the data rests on the model's assumptions, a point Michael Lavine made about exactly this "
            "example in 1991."
        ) as vo:
            self.play(FadeIn(intro))
            step = ladder(self, rows, whys, keep=4, top=2.6, x=-1.4, buff=0.7, edge=6.9)
            for k, m_ in enumerate("abcd"):
                vo.wait_until(m_)
                step(k, transform=False)
                if k == 0:
                    self.play(FadeOut(intro), run_time=0.25)
        self.clear_scene()

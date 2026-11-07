from __future__ import annotations

import numpy as np
from scipy import stats

from videos.stats.stats10.common import *  # noqa: F403


class LRT(VoiceoverScene):
    def construct(self):
        self.card()
        self.definition()
        self.wilks()
        self.simulation()
        self.trinity()
        self.trinity_numbers()
        self.sides()

    def card(self):
        card = chapter_card(6, r"The likelihood ratio test", r"One recipe for almost every test", part=PART)
        with self.voiceover("Chapter six. The likelihood ratio test."):
            self.play(FadeIn(card[0], shift=UP * 0.2), FadeIn(card[1]))
        self.play(FadeOut(card))

    def definition(self):
        rows = [
            cmath(r"\Lambda", r"=", r"\frac{\sup_{\theta \in \Theta_0} L(\theta)}{\sup_{\theta \in \Theta} L(\theta)} = \frac{L(\hat\theta_0)}{L(\hat\theta)}",
                  font_size=34),
            cmath(r"W", r"=", r"-2\log\Lambda = 2\big(\ell(\hat\theta) - \ell(\hat\theta_0)\big) \ \ge 0", font_size=34),
            cmath(r"\text{Poisson},\ H_0{:}\ \lambda = \lambda_0:\ \ W", r"=", r"2\Big(S\log\frac{S}{n\lambda_0} - (S - n\lambda_0)\Big)", font_size=32),
        ]
        rows[1][2].set_color(OBS)
        whys = [why(r"the best fit allowed by $H_0$, \ over the best fit overall"), why(r"twice the log-likelihood lost by imposing $H_0$"),
                why(r"Part 9's Poisson log-likelihood, \ $\hat\lambda = S/n$")]
        foot = label(r"NP compares $L_1/L_0$; the generalized ratio compares the null fit with the full-model fit", font_size=24,
                     color=GREY_A).to_edge(DOWN, buff=0.5)
        intro = label('Compare the null fit with the full-model fit', font_size=36)
        with self.voiceover(
            "The Neyman–Pearson lemma compares two single distributions. Most real hypotheses are composite: a "
            "normal mean is zero, but the variance is unknown; a treatment has no effect, whatever the baseline. "
            "<bookmark mark='a'/> The natural generalization: compare the best fit the null allows with the best fit "
            "overall. Lambda is the ratio of the two maximized likelihoods. It's at most one. <bookmark mark='b'/> "
            "Minus twice its log, W, is twice the log-likelihood lost by imposing the null. Large W means the null "
            "costs a lot of fit. <bookmark mark='c'/> For a Poisson rate, with Part 9's log-likelihood, W has this "
            "closed form. <bookmark mark='d'/> The simple-versus-simple Neyman–Pearson test compares the two likelihoods directly. This generalized full-model ratio follows that idea; in "
            "general it's a recipe, not a theorem, but an extraordinarily good one."
        ) as vo:
            self.play(FadeIn(intro))
            step = ladder(self, rows, whys, keep=3, top=2.6, x=0.4, buff=0.9, edge=6.9)
            for k, m_ in enumerate("abc"):
                vo.wait_until(m_)
                if k == 0:
                    self.play(FadeOut(intro), run_time=0.25)
                step(k, transform=False)
            vo.wait_until("d")
            self.play(FadeIn(foot))
        self.clear_scene()

    def wilks(self):
        tc = theorem_card(r"Wilks' theorem", r"Under the regularity conditions of Part 9, \ if the true null is a smooth interior submodel of codimension $r$, \ "
                          r"then $W = -2\log\Lambda \to \chi^2_r$ as $n \to \infty$.", who=r"S. S. Wilks, \ \emph{Ann.\ Math.\ Stat.} 9 (1938)",
                          color=ALTC, width=10.4, font_size=26).move_to([0, 2.0, 0])
        rows = [
            cmath(r"\ell(\theta_0)", r"\approx", r"\ell(\hat\theta) - \tfrac12\,n I\,(\hat\theta - \theta_0)^2", font_size=32),
            cmath(r"W", r"\approx", r"n I\,(\hat\theta - \theta_0)^2 = \Big(\frac{\hat\theta - \theta_0}{1/\sqrt{nI}}\Big)^2", font_size=32),
            cmath(r"W", r"\to", r"Z^2 \sim \chi^2_1", font_size=34),
        ]
        rows[2][2].set_color(OBS)
        whys = [why(r"Part 9: \ the log-likelihood is a parabola near its peak"), why(r"twice the drop"),
                why(r"Part 9's asymptotic normality: \ a squared normal")]
        intro = label("Wilks' theorem needs a regular interior null", font_size=36)
        with self.voiceover(
            "What's the null distribution of W? <bookmark mark='a'/> In 1938 Samuel Wilks proved that, in regular "
            "problems, if the null is true, W is approximately chi-squared, with degrees of freedom equal to the number "
            "of parameters the null pins down. <bookmark mark='b'/> The reason is Part 9's picture. Near its peak, the "
            "log-likelihood is a parabola with curvature n times the information. <bookmark mark='c'/> So twice the "
            "drop from the peak to the null value is the squared distance, measured in standard errors. "
            "<bookmark mark='d'/> And the MLE is approximately normal around the truth, so W is approximately a squared "
            "standard normal: chi-squared with one degree of freedom. One recipe, one reference distribution, for "
            "almost every test."
        ) as vo:
            self.play(FadeIn(intro))
            vo.wait_until("a")
            self.play(FadeOut(intro), run_time=0.25)
            self.play(FadeIn(tc, shift=UP * 0.2))
            step = ladder(self, rows, whys, keep=3, top=0.6, x=-0.6, buff=0.5, edge=6.9)
            for k, m_ in enumerate("bcd"):
                vo.wait_until(m_)
                step(k, transform=False)
        self.clear_scene()

    def simulation(self):
        d = load("wilks")
        ed, xs = np.asarray(d["edges"]), np.asarray(d["xs"])
        panels = VGroup()
        for j, n in enumerate(("3", "30")):
            A = axes([0, 8], [0, max(1.2, 1.1 * max(max(d[k]["hist"]) for k in ("3", "30")))], x_length=5.4, y_length=3.4, xlabel=rf"$W$, \ $n = {n}$, \ $\lambda_0 = 2$", xticks=[0, 2, 3.84, 6, 8],
                     yticks=[0, 0.5, 1], center=[-3.4 + 6.8 * j, 0.5, 0])
            ax = A.ax
            h = np.asarray(d[n]["hist"])
            bars = hist_bars(ax, ed, h, color=SIM, opacity=0.65)
            cv = clip_curve(ax, xs, d["chi2"], OBS, 3, ymax=1.2)
            cut = DashedLine(ax.c2p(3.84, 0), ax.c2p(3.84, 1.2), color=REJ, stroke_width=2)
            num = MathTex(rf"P(W > 3.84) = {d[n]['size']:.3f}", font_size=28, color=REJ).next_to(A, DOWN, buff=0.25)
            panels.add(VGroup(A, bars, cv, cut, num))
        leg = legend([(SIM, r"simulated $W$"), (OBS, r"$\chi^2_1$ density")], font_size=22).to_edge(UP, buff=0.4)
        foot = label(r"$n = 3$: \ the Poisson total takes few values, \ and $W$ is lumpy; \ $n = 30$: \ close to $\chi^2_1$", font_size=24,
                     color=GREY_A).to_edge(DOWN, buff=0.4)
        tag = simulated_tag(r"simulated: \ 100,000 samples each", corner=UR)
        with self.voiceover(
            "Check it by simulation. <bookmark mark='a'/> A hundred thousand Poisson samples of three, with the null "
            "true. W takes only a few values, because the total does, and the histogram is lumpy. Rejecting beyond three "
            "point eight four, the chi-squared five percent point, happens three point six percent of the time. "
            "<bookmark mark='b'/> With thirty observations, the histogram follows the chi-squared curve closely, and the "
            "size is five point four percent. <bookmark mark='c'/> Wilks' theorem is a large-sample result, like "
            "everything built on Part 9's asymptotics, and Part 22 shows how to correct it in small samples."
        ) as vo:
            self.play(FadeIn(leg), FadeIn(tag), *[FadeIn(p[0]) for p in panels], *[Create(p[3]) for p in panels])
            vo.wait_until("a")
            self.play(FadeIn(panels[0][1], lag_ratio=0.03), Create(panels[0][2]), FadeIn(panels[0][4]))
            vo.wait_until("b")
            self.play(FadeIn(panels[1][1], lag_ratio=0.03), Create(panels[1][2]), FadeIn(panels[1][4]))
            vo.wait_until("c")
            self.play(FadeIn(foot))
        self.clear_scene()

    def trinity(self):
        n, Sk, lam0 = 200, 122, 0.5
        lh = Sk / n
        lams = np.linspace(0.42, 0.72, 300)
        ll = Sk * np.log(lams) - n * lams
        top = Sk * np.log(lh) - n * lh
        A = axes([0.42, 0.72], [-4, 0.4], x_length=8.0, y_length=4.6, xlabel=r"$\lambda$, \ horse kicks", ylabel=r"$\ell(\lambda) - \ell(\hat\lambda)$",
                 xticks=[0.45, 0.5, 0.55, 0.61, 0.65, 0.7], yticks=[-4, -2, 0], center=[-1.8, -0.2, 0])
        ax = A.ax
        cv = clip_curve(ax, lams, ll - top, S.LIK, 3.5, ymin=-4)
        l0 = Sk * np.log(lam0) - n * lam0 - top
        drop = VGroup(DashedLine(ax.c2p(lam0, l0), ax.c2p(lam0, 0), color=OBS, stroke_width=3),
                      DashedLine(ax.c2p(lam0, 0), ax.c2p(lh, 0), color=GREY_B, stroke_width=1.5))
        wald = Line(ax.c2p(lam0, -3.6), ax.c2p(lh, -3.6), color=S.POST, stroke_width=5)
        slope = Sk / lam0 - n
        tang = Line(ax.c2p(lam0 - 0.04, l0 - slope * 0.04), ax.c2p(lam0 + 0.04, l0 + slope * 0.04), color=ALTC, stroke_width=4)
        p0 = Dot(ax.c2p(lam0, l0), radius=0.07, color=WHITE)
        rows = fit_rows(VGroup(
            label(r"$H_0$: \ $\lambda = 0.5$ \ (a guess)", font_size=24, color=GREY_A),
            label(r"likelihood ratio: \ the vertical drop", font_size=24, color=OBS),
            label(r"Wald (1943): \ the horizontal distance, \ in SEs", font_size=24, color=S.POST),
            label(r"score (Rao, 1948): \ the slope at $\lambda_0$", font_size=24, color=ALTC),
        ), 4.4, 0.36, [4.7, 0.6, 0])
        with self.voiceover(
            "There are three classic ways to test with a likelihood, and they're three ways of reading one curve. "
            "<bookmark mark='a'/> Here is the horse-kick log-likelihood again, with the null hypothesis that the rate "
            "is point five per corps-year. <bookmark mark='b'/> The likelihood ratio test measures the vertical drop "
            "from the peak to the null value. <bookmark mark='c'/> Abraham Wald's test, from 1943, measures the "
            "horizontal distance from the MLE to the null, in standard errors. <bookmark mark='d'/> And C. R. Rao's "
            "score test, from 1948, measures the slope of the log-likelihood at the null value: under the null the score is centred at zero, and the test scales its observed departure by its null variance. The score test never needs the MLE at all, which makes it the cheapest of "
            "the three."
        ) as vo:
            self.play(FadeIn(A))
            vo.wait_until("a")
            self.play(Create(cv), FadeIn(p0), FadeIn(rows[0]))
            vo.wait_until("b")
            self.play(Create(drop), FadeIn(rows[1]))
            vo.wait_until("c")
            self.play(Create(wald), FadeIn(rows[2]))
            vo.wait_until("d")
            self.play(Create(tang), FadeIn(rows[3]))
        self.clear_scene()

    def trinity_numbers(self):
        n, Sk, lam0 = 200, 122, 0.5
        lh = Sk / n
        W = 2 * (Sk * np.log(lh / lam0) - (Sk - n * lam0))
        Wa = (lh - lam0) ** 2 / (lh / n)
        Sc = (Sk / lam0 - n) ** 2 / (n / lam0)
        rows = [
            cmath(r"W_{\mathrm{LR}}", r"=", rf"2\Big(S\log\frac{{\hat\lambda}}{{\lambda_0}} - (S - n\lambda_0)\Big) = {W:.2f}", font_size=32),
            cmath(r"W_{\mathrm{Wald}}", r"=", rf"\frac{{(\hat\lambda - \lambda_0)^2}}{{\hat\lambda/n}} = {Wa:.2f}", font_size=32),
            cmath(r"W_{\mathrm{score}}", r"=", rf"\frac{{U(\lambda_0)^2}}{{n I(\lambda_0)}} = \frac{{(S/\lambda_0 - n)^2}}{{n/\lambda_0}} = {Sc:.2f}",
                  font_size=32),
        ]
        whys = [why(rf"$p = {stats.chi2.sf(W, 1):.3f}$"), why(rf"$p = {stats.chi2.sf(Wa, 1):.3f}$"), why(rf"$p = {stats.chi2.sf(Sc, 1):.3f}$")]
        foot = fit_rows(VGroup(
            label(r"all three are $\chi^2_1$ in large samples, \ and agree to first order", font_size=26, color=OBS),
            label(r"in small samples they differ; \ the Wald test is the least reliable, \ and not invariant to reparametrization",
                  font_size=24, color=GREY_A),
            label(r"Pearson's $\chi^2$ (ch.~8) is a score test; \ Part 14 compares Wald and LR for logistic regression on the Board",
                  font_size=24, color=GREY_A),
        ), 12.6, 0.3, [0, -2.1, 0])
        with self.voiceover(
            "The numbers. <bookmark mark='a'/> The likelihood ratio statistic is four point five two, a p-value of "
            "point zero three four. <bookmark mark='b'/> Wald's is three point nine seven, point zero four six. "
            "<bookmark mark='c'/> The score statistic is four point eight four, point zero two eight. "
            "<bookmark mark='d'/> In large samples all three are chi-squared with one degree of freedom, and they agree "
            "to first order, as here. In small samples they can disagree, and the Wald test, which depends on how the "
            "parameter is written, is usually the least reliable. Part 14 tests that on the Coverage Board. And "
            "Pearson's chi-squared, the subject of chapter eight, turns out to be a score test."
        ) as vo:
            step = ladder(self, rows, whys, keep=3, top=2.7, x=-0.4, buff=0.7, edge=6.9)
            for k, m_ in enumerate("abc"):
                vo.wait_until(m_)
                step(k, transform=False)
            vo.wait_until("d")
            self.play(FadeIn(foot))
        self.clear_scene()

    def sides(self):
        xs = np.linspace(-3.6, 3.6, 300)
        panels = VGroup()
        for j, (ttl, lo, hi) in enumerate(((r"one-sided: \ $H_1{:}\ \mu > 0$", None, 1.645), (r"two-sided: \ $H_1{:}\ \mu \ne 0$", -1.96, 1.96))):
            A = axes([-3.6, 3.6], [0, 0.42], x_length=5.4, y_length=2.8, xticks=[-1.96, 0, 1.96] if j else [0, 1.645],
                     center=[-3.4 + 6.8 * j, 0.9, 0], font_size=18)
            ax = A.ax
            cv = curve(ax, xs, stats.norm.pdf(xs), NULLC, 3)
            sh = VGroup(shade(ax, xs[xs >= hi], stats.norm.pdf(xs[xs >= hi]), REJ, 0.6))
            if lo is not None:
                sh.add(shade(ax, xs[xs <= lo], stats.norm.pdf(xs[xs <= lo]), REJ, 0.6))
            panels.add(VGroup(A, cv, sh, label(ttl, font_size=24).next_to(A, UP, buff=0.15)))
        rows = fit_rows(VGroup(
            label(r"a one-sided test puts all of $\alpha$ in one tail: \ more power in that direction, \ no rejection for estimates in the opposite tail", font_size=24),
            label(r"the direction must be chosen before seeing the data; \ choosing it after doubles the real size", font_size=24,
                  color=OBS),
            label(r"in a regular scalar two-sided test, the signed root of $W$, $\mathrm{sign}(\hat\theta - \theta_0)\sqrt W$ gives one-sided tests", font_size=24,
                  color=GREY_A),
        ), 12.6, 0.3, [0, -2.0, 0])
        intro = label('Choose the direction before seeing the data', font_size=36)
        with self.voiceover(
            "A last practical point: one tail or two? <bookmark mark='a'/> A one-sided test puts the whole five percent "
            "in one tail, so it rejects more readily in that direction, and never in the other. "
            "<bookmark mark='b'/> A two-sided test splits it, two and a half percent in each tail. "
            "<bookmark mark='c'/> A one-sided test is legitimate only if the direction was fixed before the data were "
            "seen. Picking the tail after looking, whichever way the data went, is really a two-sided test at ten "
            "percent. <bookmark mark='d'/> The likelihood ratio statistic is naturally two-sided; its signed square "
            "root gives the one-sided version."
        ) as vo:
            self.play(FadeIn(intro))
            vo.wait_until("a")
            self.play(FadeOut(intro), run_time=0.25)
            self.play(FadeIn(panels[0]), FadeIn(rows[0]))
            vo.wait_until("b")
            self.play(FadeIn(panels[1]))
            vo.wait_until("c")
            self.play(FadeIn(rows[1]))
            vo.wait_until("d")
            self.play(FadeIn(rows[2]))
        self.clear_scene()

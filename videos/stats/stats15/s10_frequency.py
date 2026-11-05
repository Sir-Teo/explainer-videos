from __future__ import annotations

import numpy as np
from scipy import stats

from explainer.stats.board import coverage_board, load_all
from videos.stats.stats15.common import *  # noqa: F403


class Frequency(VoiceoverScene):
    def construct(self):
        self.card()
        self.question()
        self.wrong_prior()
        self.average()
        self.sbc()
        self.board()
        self.lessons()

    def card(self):
        card = chapter_card(9, r"Bayes and frequency", r"How often does a credible interval catch the truth?", part=PART)
        with self.voiceover("Chapter nine. Bayes and frequency."):
            self.play(FadeIn(card[0], shift=UP * 0.2), FadeIn(card[1]))
        self.play(FadeOut(card))

    def question(self):
        rows = [
            cmath(r"\text{fix the truth}", r":", r"p = 0.05,\ \ n = 50", font_size=32),
            cmath(r"\text{repeat}", r":", r"s \sim \text{Binomial}(50, p);\ \text{build the 95\% credible interval}", font_size=30),
            cmath(r"\text{coverage}", r"=", r"P_p\big(p \in \text{CI}(s)\big)", font_size=34),
            cmath(r"\text{Bayesian promise}", r":", r"P(p \in \text{CI}(s) \mid s) = 0.95\ \text{for every } s", font_size=30),
        ]
        rows[2][2].set_color(OBS)
        whys = [why(r"a frequentist experiment"), why(r"ten thousand times, \ each with its own posterior"),
                why(r"the Coverage Board's question"), why(r"a different promise: \ coverage is not guaranteed")]
        with self.voiceover(
            "Credible intervals make a promise about belief. The Coverage Board asks a frequentist question of them anyway. "
            "<bookmark mark='a'/> Fix the truth: a probability of five percent, fifty trials. <bookmark mark='b'/> Repeat the "
            "experiment ten thousand times, each time building the ninety-five percent credible interval from that sample's "
            "posterior. <bookmark mark='c'/> How often does the interval contain the fixed truth? <bookmark mark='d'/> Nothing "
            "in Bayes's theorem promises ninety-five percent here. The Bayesian promise is conditional on the data, for every "
            "possible outcome; the frequentist one averages over outcomes, for a fixed truth. It's a fair question whether they "
            "coincide."
        ) as vo:
            step = ladder(self, rows, whys, keep=4, top=2.6, x=-0.6, buff=0.7, edge=6.9)
            for k, m_ in enumerate("abcd"):
                vo.wait_until(m_)
                step(k, transform=False)
        self.clear_scene()

    def wrong_prior(self):
        A = axes([0, 1], [0, 8], x_length=7.4, y_length=4.2, xlabel=r"$p$", ylabel=r"density", xticks=[0, 0.25, 0.5, 0.75, 1], yticks=[0, 4, 8],
                 center=[-2.2, 0.2, 0])
        ax = A.ax
        xs = np.linspace(0.002, 0.998, 400)
        pr = density(ax, xs, np.minimum(stats.beta(18, 2).pdf(xs), 7.8), PRIOR)
        po = density(ax, xs, np.minimum(stats.beta(18 + 2.5, 2 + 47.5).pdf(xs), 7.8), POST)
        lo, hi = stats.beta(20.5, 49.5).ppf([0.025, 0.975])
        br = Line(ax.c2p(lo, 0.3), ax.c2p(hi, 0.3), color=POST, stroke_width=8)
        tr = DashedLine(ax.c2p(0.05, 0), ax.c2p(0.05, 7.6), color=S.TRUTH, stroke_width=3)
        rows = fit_rows(VGroup(
            label(r"a confident, \ wrong prior: \ Beta(18, 2), \ ``about 0.9''", font_size=24, color=PRIOR),
            label(r"the truth is 0.05; \ typical data: \ 2 or 3 successes in 50", font_size=24, color=S.TRUTH),
            label(r"the posterior is dragged between them", font_size=24, color=POST),
            MathTex(rf"\text{{interval}} \approx [{lo:.2f},\ {hi:.2f}]", font_size=28, color=POST),
            label(r"it misses the truth \ every time", font_size=24, color=RES),
        ), 4.6, 0.36, [4.5, 0.2, 0])
        with self.voiceover(
            "<bookmark mark='a'/> Start with an extreme case. A confident prior, Beta eighteen two, says the probability is about "
            "point nine, and it's worth twenty imaginary trials. <bookmark mark='b'/> The truth is point oh five, so fifty real "
            "trials typically produce two or three successes. <bookmark mark='c'/> The posterior lands between the prior and the "
            "data, <bookmark mark='d'/> with an interval around point two to point four. <bookmark mark='e'/> It never contains "
            "point oh five. Ninety-five percent credible, zero percent coverage. With fifty trials, a twenty-trial prior that "
            "is badly wrong can't be overcome."
        ) as vo:
            self.play(FadeIn(A))
            vo.wait_until("a")
            self.play(FadeIn(pr), FadeIn(rows[0]))
            vo.wait_until("b")
            self.play(Create(tr), FadeIn(rows[1]))
            vo.wait_until("c")
            self.play(FadeIn(po), FadeIn(rows[2]))
            vo.wait_until("d")
            self.play(Create(br), FadeIn(rows[3]))
            vo.wait_until("e")
            self.play(FadeIn(rows[4]))
        self.clear_scene()

    def average(self):
        rows = [
            cmath(r"\theta \sim \pi,\quad y \mid \theta \sim p(y \mid \theta)", r":", r"\text{draw the truth from the prior}", font_size=30),
            cmath(r"P\big(\theta \in \text{CI}(y)\big)", r"=", r"\int P\big(\theta \in \text{CI}(y) \mid y\big)\,p(y)\,dy", font_size=30),
            cmath(r"\ ", r"=", r"\int 0.95\ p(y)\,dy = 0.95", font_size=32),
            cmath(r"\text{so}", r":", r"\text{exact coverage, \ on average over the prior}", font_size=30),
        ]
        rows[3][2].set_color(OBS)
        whys = [why(r"the world really works the way the prior says"), why(r"condition on the data first"),
                why(r"every posterior gives 95\%"), why(r"simulation-based calibration (Cook, Gelman \& Rubin 2006)")]
        with self.voiceover(
            "But there's a theorem in the other direction. <bookmark mark='a'/> Suppose the truth itself is drawn from the prior: "
            "the world really works the way the prior says. <bookmark mark='b'/> Then the coverage, averaged over truths and "
            "data, can be computed by conditioning on the data first. <bookmark mark='c'/> And for every possible dataset the "
            "posterior puts ninety-five percent on its interval, so the average is exactly ninety-five percent. "
            "<bookmark mark='d'/> Credible intervals are perfectly calibrated on average over the prior, whatever the prior "
            "is, as long as it's the right one. That fact is the basis of simulation-based calibration, a standard check on "
            "Bayesian software."
        ) as vo:
            step = ladder(self, rows, whys, keep=4, top=2.6, x=-0.2, buff=0.7, edge=6.9)
            for k, m_ in enumerate("abcd"):
                vo.wait_until(m_)
                step(k, transform=False)
        self.clear_scene()

    def board(self):
        rows = [r for r in load_all(upto=15) if r.part == 15]
        b = coverage_board(rows, lit_part=15, placeholders=0, font_size=20, row_h=0.58)
        b.scale_to_fit_width(min(b.width, 13.0)).move_to(ORIGIN)
        with self.voiceover(
            "The Coverage Board's six new rows. <bookmark mark='a'/> At p equals point oh five with fifty trials, the Jeffreys "
            "credible interval covers eighty-nine percent: broken, the same shortfall Part 11 found for the Jeffreys interval, "
            "because near the boundary the posterior's lower tail is too thin. The uniform prior covers ninety-six percent: "
            "conservative. <bookmark mark='b'/> The confident, wrong prior: zero. <bookmark mark='c'/> The same prior when the "
            "truth is point nine, where it's right: ninety-eight and a half percent, conservative, because a correct prior adds "
            "real information. <bookmark mark='d'/> The same prior when the truth is drawn from it: ninety-four point six, "
            "kept, as the theorem says. <bookmark mark='e'/> And the reference-prior interval for the World's mean height, "
            "which is Part 8's t-interval: ninety-four point eight, kept."
        ) as vo:
            self.play(FadeIn(b.head), FadeIn(b.axis), FadeIn(b.legend))
            vo.wait_until("a")
            self.play(FadeIn(b.body[0]), FadeIn(b.body[1]))
            vo.wait_until("b")
            self.play(FadeIn(b.body[2]))
            vo.wait_until("c")
            self.play(FadeIn(b.body[3]))
            vo.wait_until("d")
            self.play(FadeIn(b.body[4]))
            vo.wait_until("e")
            self.play(FadeIn(b.body[5]))
        self.wait(1.0)
        self.clear_scene()

    def lessons(self):
        rows = fit_rows(VGroup(
            label(r"vague priors: \ credible $\approx$ confidence, \ with similar coverage, \ and similar weak spots", font_size=24),
            label(r"a correct informative prior: \ shorter intervals, \ and coverage to spare", font_size=24, color=HIT),
            label(r"a wrong informative prior: \ confident and wrong, \ until the data outweigh it", font_size=24, color=RES),
            label(r"averaged over a true prior: \ exactly calibrated", font_size=24, color=OBS),
            label(r"so: \ a prior is a strong assumption; \ check it, \ and check sensitivity", font_size=26, color=POST),
        ), 12.4, 0.46, [0, 0, 0])
        with self.voiceover(
            "So: <bookmark mark='a'/> with vague priors, credible and confidence intervals nearly coincide, with similar coverage "
            "and the same weak spots near boundaries. <bookmark mark='b'/> A correct informative prior gives shorter intervals and "
            "coverage to spare. <bookmark mark='c'/> A wrong one is confident and wrong, until enough data outweigh it. "
            "<bookmark mark='d'/> Averaged over a prior that really describes the world, credible intervals are exactly "
            "calibrated. <bookmark mark='e'/> The prior is a strong assumption, as strong as any model. Treat it like one: "
            "justify it, check it against the data, and report how much the answer depends on it."
        ) as vo:
            for k, m_ in enumerate("abcde"):
                vo.wait_until(m_)
                self.play(FadeIn(rows[k], shift=RIGHT * 0.2))
        self.clear_scene()

    def sbc(self):
        rows = [
            cmath(r"\theta^\star \sim \pi,\ \ y \sim p(y \mid \theta^\star)", r":", r"\text{simulate a truth and data}", font_size=30),
            cmath(r"\theta_1, \ldots, \theta_L \sim \pi(\theta \mid y)", r":", r"\text{draw from the computed posterior}", font_size=30),
            cmath(r"r", r"=", r"\#\{\ell : \theta_\ell < \theta^\star\}", font_size=32),
            cmath(r"\text{if correct}", r":", r"r \text{ is uniform on } 0, \ldots, L", font_size=32),
        ]
        rows[3][2].set_color(OBS)
        whys = [why(r"the prior as the data-generating process"), why(r"by grid, \ by MCMC, \ by anything"),
                why(r"the truth's rank among the draws"), why(r"Talts et al.\ (2018): \ a bug shows up as a non-flat histogram")]
        with self.voiceover(
            "The averaging theorem gives a powerful check on Bayesian software. <bookmark mark='a'/> Simulate a truth from the "
            "prior and data from the model. <bookmark mark='b'/> Compute the posterior however you like, grid or Markov chain, "
            "and draw from it. <bookmark mark='c'/> Record the rank of the truth among the draws. <bookmark mark='d'/> If the "
            "computation is right, the truth is just another draw from the posterior, so its rank is uniform. Repeat a few "
            "hundred times; a histogram of ranks that isn't flat exposes a bug, or a sampler that hasn't converged. Sean Talts "
            "and colleagues systematized this simulation-based calibration in 2018."
        ) as vo:
            step = ladder(self, rows, whys, keep=4, top=2.6, x=-0.2, buff=0.7, edge=6.9)
            for k, m_ in enumerate("abcd"):
                vo.wait_until(m_)
                step(k, transform=False)
        self.clear_scene()

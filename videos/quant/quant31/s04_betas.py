from __future__ import annotations

import numpy as np

from explainer.quant import *  # noqa: F403
from videos.quant.quant31.common import BAD, EST_C, GOOD, HURDLE, PART, REAL_C, SPEC_C, TRUE_C, fit_right, load


class Betas(VoiceoverScene):
    def construct(self):
        v = load("vasicek")
        self.card()
        self.specific()
        self.blume()
        self.formula(v)
        self.scatter(v)
        self.scores(v)
        self.why_works()
        self.nonsync()
        self.question()

    def card(self):
        c = chapter_card(3, r"Specific risk and Bayesian betas", r"Why should an estimate borrow from its neighbours?",
                         part=PART)
        with self.voiceover("Chapter three. The factor model leaves two kinds of number to estimate asset by asset: a "
                            "specific variance, and, in the simplest model, a beta. Both are noisy, and both are improved "
                            "by the same trick."):
            self.play(FadeIn(c[0], shift=UP * 0.2), FadeIn(c[1]))
        self.play(FadeOut(c))

    def specific(self):
        rows = [cmath(r"\hat s^2_{i,t}", r"=", r"\lambda\,\hat s^2_{i,t-1} + (1-\lambda)\,u_{i,t}^2", font_size=36,
                      colors={r"\hat s^2_{i,t}": SPEC_C}),
                cmath(r"\tilde s^2_{i,t}", r"=", r"(1-c)\,\hat s^2_{i,t} + c\;\overline{s^2_t}", font_size=36,
                      colors={r"\tilde s^2_{i,t}": GOOD}),
                cmath(r"c", r"=", r"0.3\ \text{in the House; larger for short histories}", font_size=30)]
        whys = [why(r"an exponentially weighted average of the asset's squared residuals: its own history"),
                why(r"shrunk toward the cross-sectional mean of that day: Barra's Bayesian adjustment, which shrinks toward "
                    r"peers of similar size"),
                why(r"a listing two months old has little history of its own, and borrows more")]
        step = ladder(self, rows, whys, keep=3, top=2.6, x=-0.3, buff=0.55, edge=6.9)
        with self.voiceover(
            "Specific risk first. <bookmark mark='a'/> Each asset's residual variance is an exponentially weighted "
            "average of its own squared residuals. <bookmark mark='b'/> Then it is pulled part of the way toward the "
            "average of its peers that day. Commercial models shrink toward assets of similar size, because "
            "small assets have more specific risk. <bookmark mark='c'/> The House pulls thirty percent of the way; a "
            "model would pull further for an asset that listed two months ago, because its own history says little."
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

    def blume(self):
        rows = [cmath(r"\beta_{\text{next}}", r"\approx", r"0.34 + 0.68\,\hat\beta_{\text{now}}", font_size=36),
                cmath(r"\beta_{\text{adjusted}}", r"=", r"\tfrac23\,\hat\beta + \tfrac13", font_size=36,
                      colors={r"\beta_{\text{adjusted}}": GOOD})]
        whys = [why(r"Blume (1971, 1975): betas of US stock portfolios, estimated over one seven-year period, regressed "
                    r"toward one in the next; the coefficients are close to these"),
                why(r"the rule of thumb printed on financial terminals as the adjusted beta, ever since")]
        step = ladder(self, rows, whys, keep=2, top=2.2, x=-0.3, buff=0.7, edge=6.9)
        head = label(r"Blume (1971): betas regress toward one", font_size=28).to_edge(UP, buff=0.4)
        with self.voiceover(
            "Betas. Marshall Blume noticed in 1971 that betas estimated in one period regress toward one in the next. "
            "<bookmark mark='a'/> A portfolio with a high beta now will probably have a lower one later, and a low one a "
            "higher one; regressing the later betas on the earlier ones gives a slope of about two thirds. "
            "<bookmark mark='b'/> Two thirds of the estimate plus one third of one became the adjusted beta printed on "
            "financial terminals. Blume read it partly as real drift, and partly as the statistics of noisy estimates."
        ) as vo:
            self.play(FadeIn(head))
            vo.wait_until("a")
            step(0)
            vo.wait_until("b")
            step(1)
        self.wait(0.5)
        self.clear_scene()

    def formula(self, v):
        rows = [cmath(r"\hat\beta_i", r"\sim", r"N(\beta_i,\ \sigma^2_{\hat\beta_i}),\quad \beta_i \sim N(\bar\beta,\ s^2)",
                      font_size=34),
                cmath(r"\beta^*_i", r"=", r"\frac{\hat\beta_i/\sigma^2_{\hat\beta_i} + \bar\beta/s^2}{1/\sigma^2_{\hat\beta_i} + "
                      r"1/s^2}", font_size=36, colors={r"\beta^*_i": GOOD}),
                cmath(r"s^2", r"=", r"\operatorname{Var}_i(\hat\beta_i) - \overline{\sigma^2_{\hat\beta}}", font_size=34),
                cmath(r"w", r"\approx", rf"{v['weight']:.2f}\ \text{{on the coins' own estimates}}", font_size=32)]
        whys = [why(r"each estimate is the true beta plus sampling noise of known variance; the true betas are spread "
                    r"around their cross-sectional mean"),
                why(r"Vasicek (1973): the posterior mean, a precision-weighted average of the asset's estimate and the "
                    r"prior mean"),
                why(r"empirical Bayes: the spread of the true betas is the spread of the estimates, less the noise"),
                why(r"60-day windows of daily returns, 2018--2020: about a quarter of the weight moves to the mean")]
        step = ladder(self, rows, whys, keep=4, top=2.8, x=-0.3, buff=0.45, edge=6.9)
        with self.voiceover(
            "Oldrich Vasicek made the statistical part exact in 1973. <bookmark mark='a'/> Each estimated beta is the true "
            "beta plus noise whose variance we know from the regression; and the true betas themselves are spread around "
            "a mean. <bookmark mark='b'/> The best guess of the true beta is a weighted average of the estimate and the "
            "mean, weighted by their precisions: the noisier the estimate, the more it is pulled in. "
            "<bookmark mark='c'/> The spread of the true betas is estimated from the data: the variance of the "
            "estimates, less the average noise. Empirical Bayes, as in Part thirty's Bayes-Stein means. "
            f"<bookmark mark='d'/> On the coins, with sixty days of data, the average weight on a coin's own estimate is "
            f"{v['weight']:.2f}."
        ) as vo:
            step(0)
            for k, mk in enumerate(("a", "b", "c", "d")):
                vo.wait_until(mk)
                if k:
                    step(k)
        self.wait(0.5)
        self.clear_scene()

    def scatter(self, v):
        e = v["example"]
        raw, shr, nxt = (np.asarray(e[k], float) for k in ("raw", "shrunk", "next"))
        lo, hi = 0.2, 1.8
        g = axes([lo, hi], [lo, hi], x_length=5.2, y_length=4.6, xlabel=r"beta estimated on this quarter's 60 days",
                 ylabel=r"beta on the next 60 days", xticks=[0.5, 1.0, 1.5], yticks=[0.5, 1.0, 1.5],
                 xfmt=lambda x: f"{x:.1f}", yfmt=lambda x: f"{x:.1f}", font_size=15).move_to(LEFT * 2.0 + DOWN * 0.2)
        ax = g.ax
        diag = DashedLine(ax.c2p(lo, lo), ax.c2p(hi, hi), color=GREY_C, stroke_width=1.5)
        d_raw = VGroup(*[Dot(ax.c2p(a, b), radius=0.045, color=EST_C, fill_opacity=0.85) for a, b in zip(raw, nxt)])
        d_shr = VGroup(*[Dot(ax.c2p(a, b), radius=0.045, color=GOOD, fill_opacity=0.85) for a, b in zip(shr, nxt)])
        arrows = VGroup(*[Line(ax.c2p(a, b), ax.c2p(c, b), color=GREY_B, stroke_width=1, stroke_opacity=0.6)
                          for a, c, b in zip(raw, shr, nxt)])
        leg = legend([(EST_C, r"the raw estimate"), (GOOD, r"shrunk toward the mean")], font_size=17)
        leg.to_edge(RIGHT, buff=0.5).shift(UP * 1.5)
        fit_right(leg)
        txt = wrapped_label(rf"the last of {v['n_windows']} quarter pairs: {len(raw)} coins listed for both quarters; "
                            r"the dashed line is a perfect forecast", 4.2, 16, GREY_A).next_to(leg, DOWN, buff=0.5)
        fit_right(txt)
        with self.voiceover(
            "One quarter of the coins. <bookmark mark='a'/> On the horizontal axis, each coin's beta estimated on sixty "
            "days; on the vertical, its beta over the next sixty. A perfect forecast lies on the dashed line. The cloud "
            "is flatter than the line: high estimates were too high, low ones too low. <bookmark mark='b'/> Shrinking "
            "slides each point horizontally toward the mean, and the cloud lines up closer to the diagonal."
        ) as vo:
            self.play(FadeIn(g), Create(diag), FadeIn(leg), FadeIn(txt))
            vo.wait_until("a")
            self.play(LaggedStart(*[FadeIn(d_) for d_ in d_raw], lag_ratio=0.02))
            vo.wait_until("b")
            self.play(FadeIn(arrows), Transform(d_raw, d_shr), run_time=2.0)
        self.wait(0.4)
        self.clear_scene()

    def scores(self, v):
        mse = v["mse"]
        items = [(r"raw estimate", mse["raw"], EST_C), (r"Vasicek", mse["shrunk"], GOOD), (r"beta = 1 for all", mse["one"], GREY_B)]
        mx = max(x for _, x, _ in items)
        bars = VGroup()
        for j, (nm, x, col) in enumerate(items):
            r = Rectangle(width=7.0 * x / mx, height=0.6, fill_color=col, fill_opacity=0.8, stroke_width=0)
            r.move_to([-2.0, 1.2 - 1.0 * j, 0], aligned_edge=LEFT)
            bars.add(VGroup(r, label(nm, font_size=22, color=col).next_to(r, LEFT, buff=0.3),
                            MathTex(f"{x:.3f}", font_size=26).next_to(r, RIGHT, buff=0.2)))
        head = label(r"mean squared error of next quarter's beta", font_size=28).to_edge(UP, buff=0.6)
        foot = wrapped_label(rf"averaged over {v['n_windows']} pairs of consecutive 60-day windows, 2018--2020", 11.0, 17,
                             GREY_A).to_edge(DOWN, buff=0.6)
        gain = 1 - mse["shrunk"] / mse["raw"]
        with self.voiceover(
            f"Scored over all {v['n_windows']} pairs of quarters. <bookmark mark='a'/> The raw estimates miss next "
            f"quarter's beta with a mean squared error of {mse['raw']:.3f}. Setting every beta to one does a little worse. "
            f"Vasicek's shrinkage does best, cutting the error by {100 * gain:.0f} percent. The best estimate is neither "
            "the data alone nor the prior alone."
        ) as vo:
            self.play(FadeIn(head), FadeIn(foot))
            vo.wait_until("a")
            self.play(LaggedStart(*[FadeIn(b, shift=RIGHT * 0.2) for b in bars], lag_ratio=0.4))
        self.wait(0.4)
        self.clear_scene()

    def why_works(self):
        cards = VGroup(
            desk_question(r"why it works", r"the largest estimates are the most likely to be large partly by luck: "
                          r"selecting on an estimate selects on its noise, so the extremes regress", width=12.4,
                          font_size=19),
            desk_question(r"the same idea, four times", r"Stein's means, Ledoit and Wolf's covariances (Part 30), "
                          r"Vasicek's betas, Barra's specific variances: one bias accepted to cut much more variance",
                          width=12.4, font_size=19),
            desk_question(r"where it fails", r"when the prior is wrong: shrinking a new kind of asset toward an old "
                          r"group's mean, or across a change in regime", width=12.4, font_size=19),
        ).arrange(DOWN, buff=0.25)
        with self.voiceover(
            "Why it works. <bookmark mark='a'/> The largest estimates are the ones most likely to have been helped by "
            "luck; selecting on an estimate selects on its noise. <bookmark mark='b'/> It is the same idea for the "
            "fourth time in two parts: Stein's means, Ledoit and Wolf's covariances, Vasicek's betas, and the specific "
            "variances. Accept a little bias to cut much more variance. <bookmark mark='c'/> It fails when the prior is "
            "wrong: shrinking a new kind of asset toward the mean of a group it does not belong to."
        ) as vo:
            for k, mk in enumerate(("a", "b", "c")):
                vo.wait_until(mk)
                self.play(FadeIn(cards[k], shift=UP * 0.2))
        self.wait(0.4)
        self.clear_scene()

    def nonsync(self):
        rows = [cmath(r"\hat\beta_{\text{daily}}", r"\to", r"\text{too low for assets that trade rarely}", font_size=32,
                      colors={r"\hat\beta_{\text{daily}}": BAD}),
                cmath(r"\beta_{\text{Dimson}}", r"=", r"\textstyle\sum_{k=-1}^{1} b_k,\quad r_{i,t} = a + \sum_k b_k\,"
                      r"r_{m,t+k} + e", font_size=32, colors={r"\beta_{\text{Dimson}}": GOOD}),
                cmath(r"\text{or}", r":", r"\text{estimate on weekly or monthly returns}", font_size=30)]
        whys = [why(r"an asset whose last trade of the day was hours before the close moves with the market a day late: "
                    r"the same-day covariance misses part of its beta"),
                why(r"Dimson (1979), after Scholes and Williams (1977): add the slopes on the market's lagged and leading "
                    r"returns"),
                why(r"longer returns let the lagged reaction fall inside the same period, at the cost of fewer observations")]
        step = ladder(self, rows, whys, keep=3, top=2.6, x=-0.3, buff=0.55, edge=6.9)
        with self.voiceover(
            "One more source of error in betas: time. <bookmark mark='a'/> An asset that trades rarely reacts to the "
            "market a day late, so a beta from same-day returns is too low. Small stocks, and thinly traded coins, are "
            "the worst cases. <bookmark mark='b'/> Myron Scholes and Joseph Williams, and then Elroy Dimson, fixed it by "
            "adding the slopes on yesterday's and tomorrow's market returns. <bookmark mark='c'/> Or estimate on weekly "
            "returns, so that the late reaction falls inside the same week, and accept fewer observations, which is "
            "exactly when shrinkage matters most."
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

    def question(self):
        q = pause_card(r"a beta is estimated at 1.8 with standard error 0.3; across stocks, true betas have mean 1.0 and "
                       r"standard deviation 0.3. What is Vasicek's estimate?")
        with self.voiceover(
            "Pause and predict. A beta is estimated at one point eight with a standard error of point three. Across "
            "stocks, true betas have mean one and standard deviation point three. What is Vasicek's estimate?"
        ):
            self.play(FadeIn(q))
        self.wait(0.5)
        self.clear_scene()

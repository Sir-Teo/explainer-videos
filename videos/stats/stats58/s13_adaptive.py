from __future__ import annotations

import numpy as np

from videos.stats.stats58.common import *  # noqa: F403


class Adaptive(LectureMixin, VoiceoverScene):
    def construct(self):
        self.card_voiceover("Chapter twelve. Inference after adaptivity: what the data can still tell us when the design "
                       "chased them.", 12, r"Inference after adaptivity", r"When the design chased the data", lit=(2018, 2021))
        self.bias()
        self.why_bias()
        self.hist()
        self.clt_fails()
        self.aipw()
        self.weights()
        self.board()
        self.anytime()

    def bias(self):
        self.lad_voiceover(
            "<bookmark mark='a'/> The first surprise: after an adaptive experiment, the sample mean of each arm is biased "
            "downward. Xinkun Nie, Xiaoying Tian, Jonathan Taylor and James Zou proved it in 2018 for a broad class of "
            "designs. <bookmark mark='b'/> The reason is that an arm which happens to do badly early is sampled less, so "
            "its unlucky early outcomes are not diluted by later ones. <bookmark mark='c'/> An arm that does well early is "
            "sampled more, and its lucky start is diluted. <bookmark mark='d'/> Both effects push the mean down, and the "
            "naive interval, centred on it, covers less than promised.",
            [(r"\text{Nie et al. (2018)}", r":", r"E[\bar Y_k] \le \mu_k \text{ for optimistic designs}", 38),
             (r"\text{bad start}", r":", r"\text{sampled less: \ the bad luck stays}", 38),
             (r"\text{good start}", r":", r"\text{sampled more: \ the good luck is diluted}", 38),
             (r"\text{so}", r":", r"\text{downward bias; \ naive intervals undercover}", 38)],
            [r"Nie, \ Tian, \ Taylor \& Zou", r"stuck with it", r"averaged away", r"the Board's next row"],
            colors=[(0, FIXEDC), (3, FIXEDC)])

    def why_bias(self):
        self.lad_voiceover(
            "<bookmark mark='a'/> In symbols: the sample mean is a sum of outcomes divided by a random count, and the count "
            "depends on the outcomes. <bookmark mark='b'/> Each outcome is unbiased given the past, so the numerator's "
            "expectation is mu times the expected count. <bookmark mark='c'/> But a ratio is not unbiased when its "
            "denominator is correlated with its numerator, and here the correlation is negative in exactly the harmful "
            "direction. <bookmark mark='d'/> Inverse-propensity weighting repairs the expectation: dividing each outcome by "
            "the probability of having been sampled gives an unbiased estimate, whatever the design.",
            [(r"\bar Y_k", r"=", r"\frac{\sum_t 1\{A_t = k\}Y_t}{N_k}, \ \ N_k \text{ random}", 38),
             (r"E\big[\textstyle\sum_t 1\{A_t = k\}Y_t\big]", r"=", r"\mu_k\,E[N_k]", 38),
             (r"\text{but}", r":", r"N_k \text{ depends on the outcomes: \ a biased ratio}", 38),
             (r"\text{repair}", r":", r"\frac1T\textstyle\sum_t \frac{1\{A_t = k\}Y_t}{e_t(k)} \text{ is unbiased}", 38)],
            [r"a ratio", r"martingale differences", r"the design reacted", r"Horvitz \& Thompson, \ again"],
            colors=[(3, CSC)])

    def hist(self):
        d = load("adapt")
        ne, ae = np.asarray(d["naive_est"]), np.asarray(d["aw_est"])
        edges = np.linspace(0.3, 0.7, 33)
        A = axes([0.3, 0.7], [0, 0.22], x_length=5.4, y_length=3.6, xlabel=r"estimate of arm A's rate \ (truth 0.5)", ylabel=r"fraction of experiments",
                 xticks=[0.3, 0.5, 0.7], yticks=[0, 0.1, 0.2], center=[-3.4, 0.5, 0])
        B = axes([0.3, 0.7], [0, 0.22], x_length=5.4, y_length=3.6, xlabel=r"estimate of arm A's rate \ (truth 0.5)", ylabel=r"fraction of experiments",
                 xticks=[0.3, 0.5, 0.7], yticks=[0, 0.1, 0.2], center=[3.4, 0.5, 0])
        h1 = hist_bars(A.ax, edges, np.histogram(np.clip(ne, 0.3, 0.7 - 1e-9), edges)[0] / len(ne), color=FIXEDC, opacity=0.7)
        h2 = hist_bars(B.ax, edges, np.histogram(np.clip(ae, 0.3, 0.7 - 1e-9), edges)[0] / len(ae), color=CSC, opacity=0.7)
        t1 = DashedLine(A.ax.c2p(0.5, 0), A.ax.c2p(0.5, 0.22), color=WEALTHC, stroke_width=2)
        t2 = DashedLine(B.ax.c2p(0.5, 0), B.ax.c2p(0.5, 0.22), color=WEALTHC, stroke_width=2)
        foot = fit_rows(VGroup(
            label(rf"two equal arms, \ 50\% each; \ Thompson sampling, \ {d['T']:,} visitors, \ floor {d['floor']}; \ {d['reps']:,} experiments", font_size=24, color=GREY_A),
            label(rf"left: \ sample means, \ bias ${100 * d['naive_bias']:+.1f}$ points; \ right: \ adaptively weighted AIPW, \ ${100 * d['aw_bias']:+.1f}$", font_size=24, color=GREY_A),
            label(rf"arm A got between {d['n0_q10']:.0f} and {d['n0_q90']:.0f} visitors in 80\% of experiments", font_size=24, color=BANDITC),
        ), 12.4, 0.18, [0, -2.75, 0])
        with self.voiceover(
            f"<bookmark mark='a'/> A stark case: two arms that are exactly equal, fifty percent each, run by Thompson sampling "
            f"for a thousand visitors, a thousand times. <bookmark mark='b'/> The arm's sample size swings wildly, from about "
            f"{d['n0_q10']:.0f} to {d['n0_q90']:.0f} visitors, depending on early luck. <bookmark mark='c'/> On the left, the "
            f"sample means: biased by {100 * d['naive_bias']:.1f} points and lopsided. <bookmark mark='d'/> On the right, the "
            f"adaptively weighted estimate of the next ladders: bias {100 * d['aw_bias']:.1f} points, more tightly "
            f"concentrated, though still skewed at this size."
        ) as vo:
            self.play(FadeIn(A), FadeIn(B), Create(t1), Create(t2), FadeIn(simulated_tag(r"simulated")))
            vo.wait_until("a")
            self.play(FadeIn(foot[0]))
            vo.wait_until("b")
            self.play(FadeIn(foot[2]))
            vo.wait_until("c")
            self.play(FadeIn(h1, lag_ratio=0.05), run_time=2.0)
            vo.wait_until("d")
            self.play(FadeIn(h2, lag_ratio=0.05), FadeIn(foot[1]), run_time=2.0)
        self.clear_scene()

    def clt_fails(self):
        self.lad_voiceover(
            "<bookmark mark='a'/> Worse than bias, the central limit theorem can fail. Kelly Zhang, Lucas Janson and Susan "
            "Murphy showed in 2020 that for batched bandits, when the arms are equal, the ordinary estimator is not "
            "asymptotically normal. <bookmark mark='b'/> The share of samples each arm receives does not settle down: it "
            "converges to a random limit. <bookmark mark='c'/> So the variance estimate does not stabilize, and the "
            "studentized statistic has a non-normal limit. <bookmark mark='d'/> Their fix is to studentize batch by batch "
            "and combine: the batched OLS estimator, normal even when the arms are equal.",
            [(r"\text{Zhang, \ Janson \& Murphy}", r":", r"\text{no CLT for equal arms}", 38),
             (r"N_k/T", r"\to", r"\text{a random limit, \ not a constant}", 38),
             (r"\Rightarrow", r"\;", r"\text{the } t\text{-statistic is not asymptotically normal}", 38),
             (r"\text{fix}", r":", r"\text{studentize per batch, \ then combine}", 38)],
            [r"NeurIPS (2020)", r"no stable allocation", r"the naive interval's failure", r"batched OLS"],
            colors=[(2, FIXEDC), (3, CSC)])

    def aipw(self):
        self.lad_voiceover(
            "<bookmark mark='a'/> Vitor Hadad, David Hirshberg, Ruohan Zhan, Stefan Wager and Susan Athey start from "
            "augmented inverse-propensity scores. At each time, use the past to predict the arm's mean, m hat. <bookmark "
            "mark='b'/> If the arm was shown, correct the prediction by the residual divided by the assignment probability. "
            "<bookmark mark='c'/> Each score is unbiased for the arm's mean given the past, because m hat and the probability "
            "are fixed before the outcome. <bookmark mark='d'/> So the scores' average is unbiased; but its variance is "
            "dominated by the times the probability was tiny, and it is still not normal.",
            [(r"\hat m_{t-1}(k)", r":", r"\text{prediction from the past}", 38),
             (r"\Gamma_t(k)", r"=", r"\hat m_{t-1}(k) + \frac{1\{A_t = k\}}{e_t(k)}\big(Y_t - \hat m_{t-1}(k)\big)", 36),
             (r"E[\Gamma_t(k) \mid \mathcal F_{t-1}]", r"=", r"\mu_k", 40),
             (r"\text{but}", r":", r"\text{variance} \propto 1/e_t(k): \ \text{tiny propensities dominate}", 36)],
            [r"Hadad et al., \ \emph{PNAS} (2021)", r"Part 36's AIPW, \ online", r"a martingale difference", r"heavy tails"],
            colors=[(1, WEALTHC), (2, CSC)])

    def weights(self):
        self.lad_voiceover(
            "<bookmark mark='a'/> The fix is to weight the scores. Give score t a weight h t, chosen from the past. <bookmark "
            "mark='b'/> Variance-stabilizing weights, h t equal to root of e t, make each weighted score's conditional "
            "variance roughly constant over time. <bookmark mark='c'/> The weighted average is then a martingale whose "
            "increments have stable variance, and the martingale central limit theorem of Part forty-four applies. <bookmark "
            "mark='d'/> Studentized by its own weighted spread, it gives intervals that are asymptotically valid under the "
            "adaptive design.",
            [(r"\hat Q_k", r"=", r"\frac{\sum_t h_t\,\Gamma_t(k)}{\sum_t h_t}", 40),
             (r"h_t", r"=", r"\sqrt{e_t(k)}: \ \text{stabilizes the variance}", 40),
             (r"\text{martingale CLT}", r":", r"\frac{\hat Q_k - \mu_k}{\widehat{\mathrm{se}}} \Rightarrow N(0, 1)", 38),
             (r"\widehat{\mathrm{se}}", r"=", r"\sqrt{\textstyle\sum_t h_t^2(\Gamma_t - \hat Q_k)^2}\,\big/\textstyle\sum_t h_t", 36)],
            [r"predictable weights", r"Hadad et al.", r"Part 44", r"the interval"],
            colors=[(0, CSC), (2, CSC)])

    def board(self):
        br = load("board")["rows"]
        show_board(self, board_rows("Thompson", "adaptively weighted"),
                   f"<bookmark mark='a'/> On the Board: after Thompson sampling with two equal arms, the naive ninety-five "
                   f"percent interval for an arm's rate covers {100 * br[2]['achieved']:.1f} percent of the time: broken. "
                   f"<bookmark mark='b'/> The adaptively weighted interval covers {100 * br[3]['achieved']:.1f} percent: kept, "
                   f"though a little short, as an asymptotic method at a thousand visitors may be.", [("a", [0]), ("b", [1])])

    def anytime(self):
        self.list_voiceover(
            "<bookmark mark='a'/> Two routes to honest inference from adaptive experiments. <bookmark mark='b'/> "
            "Asymptotic: weighted AIPW and batched estimators, with intervals at the end of the experiment. <bookmark "
            "mark='c'/> Anytime-valid: inverse-propensity-weighted test martingales, which give confidence sequences for "
            "the arms' means and their differences under any adaptive design with known propensities. <bookmark mark='d'/> "
            "Either way, the propensities must be recorded. An adaptive experiment that does not log them cannot be "
            "analysed honestly afterwards.",
            [(r"two routes:", GREY_A),
             (r"asymptotic: \ weighted AIPW, \ batched OLS, \ intervals at the end", CSC),
             (r"anytime-valid: \ IPW test martingales, \ confidence sequences throughout", WEALTHC),
             (r"either way: \ record the propensities $e_t(k)$", FIXEDC)])

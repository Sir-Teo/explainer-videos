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
        heading = label('Selection bias in adaptive sampling', font_size=30, color=WEALTHC).move_to([0, 3.35, 0])
        if heading.width > 12.5:
            heading.width = 12.5
        self.add(heading)
        self.lad_voiceover(
            (
            "<bookmark mark='a'/> Adaptive sampling can bias an arm's sample mean. Nie and colleagues prove "
            'downward bias for a class of optimistic sampling designs under their conditions; it is not a theorem '
            "for every adaptive rule. <bookmark mark='b'/> A poor early outcome can reduce subsequent sampling, "
            "leaving that poor start less diluted. <bookmark mark='c'/> A favourable start can attract more "
            'observations and be averaged away. This explains the direction in our example, while different '
            "stopping and selection rules can produce other biases. <bookmark mark='d'/> Bias alone does not "
            'determine coverage. We simulate the actual nominal intervals and report their empirical coverage with '
            'Monte Carlo uncertainty.'
        ),
            [(r"\text{Nie et al. (2018)}", r":", r"E[\bar Y_k] \le \mu_k \text{ for optimistic designs}", 38),
             (r"\text{bad start}", r":", r"\text{sampled less: \ the bad luck stays}", 38),
             (r"\text{good start}", r":", r"\text{sampled more: \ the good luck is diluted}", 38),
             (r"\text{so}", r":", r"\text{downward bias for stated designs; \ assess coverage separately}", 38)],
            [r"Nie, \ Tian, \ Taylor \& Zou", r"stuck with it", r"averaged away", r"the Board's next row"],
            colors=[(0, FIXEDC), (3, FIXEDC)])

    def why_bias(self):
        heading = label('Why bias', font_size=30, color=WEALTHC).move_to([0, 3.35, 0])
        if heading.width > 12.5:
            heading.width = 12.5
        self.add(heading)
        self.lad_voiceover(
            (
            "<bookmark mark='a'/> An arm's sample mean divides its total reward by a random sample count. The count "
            "depends on previous rewards. <bookmark mark='b'/> With stationary arm means and predictable "
            "assignment, expected total reward is mu times expected count. <bookmark mark='c'/> That identity does "
            'not make the ratio unbiased. The count and reward total are generally dependent; a universal sign '
            "cannot be read from this equation alone. <bookmark mark='d'/> With known positive conditional "
            'assignment probabilities and sequential randomization, the average inverse-propensity score is '
            'unbiased. In our finite-Monte-Carlo policy those probabilities condition on the auxiliary posterior '
            'draws before action.'
        ),
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
        heading = label('A counterexample for batched bandits', font_size=30, color=WEALTHC).move_to([0, 3.35, 0])
        if heading.width > 12.5:
            heading.width = 12.5
        self.add(heading)
        self.lad_voiceover(
            (
            "<bookmark mark='a'/> Zhang, Janson and Murphy give batched-bandit examples in which the usual "
            'estimator and t statistic fail to become normal, even asymptotically. Equal arms are the difficult '
            "case in their model. <bookmark mark='b'/> Allocation probabilities need not concentrate at a "
            'deterministic limit as batch sizes grow. This is a failure of a stability condition, not a theorem '
            "that every equal-arm adaptive design has the same random limiting allocation. <bookmark mark='c'/> The "
            'resulting ordinary studentized statistic can have a nonnormal limit and invalidate nominal intervals. '
            "Our one-visitor-at-a-time simulation is a separate finite-sample illustration. <bookmark mark='d'/> "
            'Their batched OLS combines appropriately studentized batch contributions and is asymptotically normal '
            "under the paper's sampling, moment and clipping conditions."
        ),
            [(r"\text{Zhang, \ Janson \& Murphy}", r":", r"\text{a nonnormal equal-arm batched-bandit example}", 38),
             (r"\text{allocations}", r":", r"\text{need not concentrate at a deterministic limit}", 38),
             (r"\Rightarrow", r"\;", r"\text{the } t\text{-statistic is not asymptotically normal}", 38),
             (r"\text{fix}", r":", r"\text{studentize per batch, \ then combine}", 38)],
            [r"NeurIPS (2020)", r"no stable allocation", r"the naive interval's failure", r"batched OLS"],
            colors=[(2, FIXEDC), (3, CSC)])

    def aipw(self):
        heading = label('Predictable augmented scores', font_size=30, color=WEALTHC).move_to([0, 3.35, 0])
        if heading.width > 12.5:
            heading.width = 12.5
        self.add(heading)
        self.lad_voiceover(
            (
            "<bookmark mark='a'/> Start from an augmented inverse-propensity score. Predict each arm's stationary "
            "mean using past observations. <bookmark mark='b'/> If that arm is selected, add its observed residual "
            "divided by its known positive conditional assignment probability. <bookmark mark='c'/> The score has "
            "conditional mean equal to the arm's mean, under sequential randomization and the stationary response "
            "model. A predictable misspecified prediction still gives an unbiased score. <bookmark mark='d'/> "
            'Averaging these scores is unbiased, but small propensities can create large variance. Normality needs '
            'a martingale central limit theorem, not just score unbiasedness.'
        ),
            [(r"\hat m_{t-1}(k)", r":", r"\text{prediction from the past}", 38),
             (r"\Gamma_t(k)", r"=", r"\hat m_{t-1}(k) + \frac{1\{A_t = k\}}{e_t(k)}\big(Y_t - \hat m_{t-1}(k)\big)", 36),
             (r"E[\Gamma_t(k) \mid \mathcal F_{t-1}]", r"=", r"\mu_k", 40),
             (r"\text{but}", r":", r"\text{variance} \propto 1/e_t(k): \ \text{tiny propensities dominate}", 36)],
            [r"Hadad et al., \ \emph{PNAS} (2021)", r"Part 36's AIPW, \ online", r"a martingale difference", r"heavy tails"],
            colors=[(1, WEALTHC), (2, CSC)])

    def weights(self):
        heading = label('A martingale numerator, a self-normalized estimate', font_size=30, color=WEALTHC).move_to([0, 3.35, 0])
        if heading.width > 12.5:
            heading.width = 12.5
        self.add(heading)
        self.lad_voiceover(
            (
            "<bookmark mark='a'/> Hadad and colleagues weight the scores predictably, then divide their weighted "
            'sum by the sum of weights. This self-normalized estimator can retain finite-sample bias. <bookmark '
            "mark='b'/> Square-root propensity weights help stabilize the variance contribution, though they need "
            "not make it exactly constant when outcome variance or prediction error changes. <bookmark mark='c'/> "
            'The centered weighted numerator is a martingale sum. The ratio itself is not a martingale. Asymptotic '
            'normality requires suitable variance stabilization, effective sample growth and Lindeberg conditions. '
            "<bookmark mark='d'/> Under those conditions, a consistent studentized spread gives an asymptotically "
            'valid interval. It is not an exact finite-sample guarantee for every adaptive design.'
        ),
            [(r"\hat Q_k", r"=", r"\frac{\sum_t h_t\,\Gamma_t(k)}{\sum_t h_t}", 40),
             (r"h_t", r"=", r"\sqrt{e_t(k)}: \ \text{variance-stabilizing choice under conditions}", 40),
             (r"\text{martingale CLT}", r":", r"\frac{\hat Q_k - \mu_k}{\widehat{\mathrm{se}}} \Rightarrow N(0, 1)", 38),
             (r"\widehat{\mathrm{se}}", r"=", r"\sqrt{\textstyle\sum_t h_t^2(\Gamma_t - \hat Q_k)^2}\,\big/\textstyle\sum_t h_t", 36)],
            [r"predictable weights", r"Hadad et al.", r"Part 44", r"the interval"],
            colors=[(0, CSC), (2, CSC)])

    def board(self):
        br = load("board")["rows"]
        show_board(self, board_rows("Thompson", "adaptively weighted"),
                   f"<bookmark mark='a'/> On the Board: after Thompson sampling with two equal arms, the naive ninety-five percent interval for an arm's rate covers {100 * br[2]['achieved']:.1f} percent of the time: broken. <bookmark mark='b'/> The adaptively weighted interval covers {100 * br[3]['achieved']:.1f} percent. This is an asymptotic interval, and the observed shortfall must be read with simulation uncertainty; the Board's tolerance label is not a proof of nominal coverage.", [("a", [0]), ("b", [1])])

    def anytime(self):
        self.list_voiceover(
            (
            "<bookmark mark='a'/> Two routes support inference from adaptive experiments under explicit response "
            "and assignment assumptions. <bookmark mark='b'/> Weighted AIPW and batched estimators can give "
            "asymptotic intervals when their martingale central limit conditions hold. <bookmark mark='c'/> "
            'Properly constructed inverse-propensity betting processes can instead give confidence sequences, with '
            "known positive propensities and appropriate outcome bounds or moment assumptions. <bookmark mark='d'/> "
            'Record the assignment probabilities, including the information used for each randomization. Missing '
            'logs obstruct these methods, although other design-specific analyses may sometimes remain possible.'
        ),
            [('Two routes to inference under adaptive sampling', GREY_A),
             (r"asymptotic: \ weighted AIPW, \ batched OLS, \ intervals at the end", CSC),
             (r"anytime-valid: \ IPW test martingales, \ confidence sequences throughout", WEALTHC),
             (r"either way: \ record the propensities $e_t(k)$", FIXEDC)], head_size=36)

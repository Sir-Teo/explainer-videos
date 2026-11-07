from __future__ import annotations

import numpy as np

from explainer.stats.board import coverage_board, load_all
from videos.stats.stats21.common import *  # noqa: F403


class Stochastic(VoiceoverScene):
    def construct(self):
        self.card()
        self.robbins_monro()
        self.median_path()
        self.sgd()
        self.averaging()
        self.step_sizes()
        self.beyond()
        self.board()

    def card(self):
        card = chapter_card(10, r"Stochastic gradient", r"One observation at a time", lit=(1951,), part=PART)
        with self.voiceover("Chapter ten. Stochastic gradient methods."):
            self.play(FadeIn(card[0], shift=UP * 0.2), FadeIn(card[1]))
        self.play(FadeOut(card))

    def robbins_monro(self):
        rows = [
            cmath(r"\text{find } \theta^*", r":", r"M(\theta^*) = E\,H(\theta^*, X) = 0", font_size=30),
            cmath(r"\theta_{k+1}", r"=", r"\theta_k - a_k H(\theta_k, X_k)", font_size=30),
            cmath(r"\text{steps}", r":", r"\textstyle\sum_k a_k = \infty, \ \ \sum_k a_k^2 < \infty", font_size=30),
            cmath(r"\text{e.g. the median}", r":", r"H(\theta, x) = 1\{x \le \theta\} - \tfrac12", font_size=30),
        ]
        rows[1][2].set_color(PATH)
        whys = [why(r"only noisy evaluations of $M$"), why(r"step against one noisy reading"),
                why(r"far enough to arrive; \ small enough to settle"), why(r"Robbins \& Monro (1951)")]
        intro = label('A noisy root can be tracked under stability and step conditions', font_size=36).move_to([0, 3.35, 0])
        if intro.width > 12.5:
            intro.width = 12.5
        with self.voiceover(
            "<bookmark mark='a'/> In 1951 Herbert Robbins and Sutton Monro asked how to find the root of a function "
            "you can only measure with noise: the expected value of some H of theta and X. <bookmark mark='b'/> Their"
            " answer: after each new observation, nudge theta against its noisy reading, with a step a k. <bookmark "
            "mark='c'/> Classical step conditions require a divergent sum but a finite sum of squared steps. "
            "Stability, an appropriate root and controlled unbiased noise are also needed; the step conditions alone "
            "do not guarantee convergence. <bookmark mark='d'/> To find a median, for instance, move down by a step "
            "whenever the new observation is below the current guess, and up when it's above."
        ) as vo:
            self.play(FadeIn(intro))
            step = ladder(self, rows, whys, keep=4, top=2.6, x=-0.6, buff=0.78, edge=6.9)
            for k, m_ in enumerate("abcd"):
                vo.wait_until(m_)
                step(k, transform=False)
        self.clear_scene()

    def median_path(self):
        d = load("sgd")
        p = np.asarray(d["rm_path"])
        ks = np.arange(1, len(p) + 1)
        A = axes([0, np.log10(len(p))], [0, 16], x_length=8.4, y_length=4.2, xlabel=r"observations (log scale)", ylabel=r"$\theta_k$",
                 xticks=[0, 1, 2, 3], yticks=[0, 5, 10, 15], center=[-1.4, 0.3, 0], xfmt=lambda v: f"{10 ** v:,.0f}")
        ax = A.ax
        ln = polyline(ax, np.log10(ks), p, PATH, 3)
        tr = DashedLine(ax.c2p(0, 10), ax.c2p(np.log10(len(p)), 10), color=TRUE, stroke_width=2.5)
        rows = fit_rows(VGroup(
            label(r"a stream of $N(10, 3^2)$ observations", font_size=22),
            label(r"start at 0; \ steps $10/k$", font_size=22, color=PATH),
            label(r"dashed: \ the true median, \ 10", font_size=22, color=TRUE),
            label(rf"after 2,000: \ {p[-1]:.2f}", font_size=22, color=HIT),
            label(r"no data stored: \ one number, \ updated", font_size=22, color=GREY_A),
        ), 3.45, 0.42, [5.1, 0.3, 0])
        with self.voiceover(
            "<bookmark mark='a'/> Here's the median of a stream of observations, centred on ten, starting from a guess of zero, "
            "with steps ten over k. <bookmark mark='b'/> The early steps are big, and the guess races up and overshoots. "
            "<bookmark mark='c'/> Then the steps shrink and it settles on ten. <bookmark mark='d'/> And it never stores the "
            "data: one number, updated as each observation arrives. That's why the idea now trains models on data sets too big "
            "to hold in memory."
        ) as vo:
            self.add(simulated_tag(r"simulated: \ a stream", corner=UR))
            self.play(FadeIn(A), Create(tr), FadeIn(rows[0]), FadeIn(rows[2]))
            vo.wait_until("a")
            vo.wait_until("b")
            self.play(Create(ln), FadeIn(rows[1]), run_time=3.0)
            vo.wait_until("c")
            self.play(FadeIn(rows[3]))
            vo.wait_until("d")
            self.play(FadeIn(rows[4]))
        self.clear_scene()

    def sgd(self):
        rows = [
            cmath(r"\beta_{k+1}", r"=", r"\beta_k + a_k\,\big(y_k - \operatorname{expit}(x_k'\beta_k)\big)\,x_k", font_size=30),
            cmath(r"\text{cost per step}", r":", r"O(p), \ \text{one observation}", font_size=30),
            cmath(r"a_k", r"=", r"k^{-0.6}", font_size=30),
            cmath(r"\text{the last iterate}", r":", r"\text{noisy: \ it is always responding to the latest point}", font_size=28),
        ]
        rows[0][2].set_color(GRAD)
        whys = [why(r"the gradient of one observation's log likelihood"), why(r"vs $O(np)$ for a full gradient"),
                why(r"bigger steps than $1/k$: \ faster to arrive"), why(r"its error shrinks like $\sqrt{a_k}$")]
        intro = label('One observation supplies a noisy likelihood gradient', font_size=36).move_to([0, 3.35, 0])
        if intro.width > 12.5:
            intro.width = 12.5
        with self.voiceover(
            "<bookmark mark='a'/> Stochastic gradient ascent applies the same idea to a likelihood: after each observation, "
            "step in the direction of that one observation's gradient, here for logistic regression. <bookmark mark='b'/> Each "
            "step costs almost nothing. <bookmark mark='c'/> We use steps of k to the minus point six, larger than one over k, "
            "so the estimate gets to the right region quickly. <bookmark mark='d'/> The price is that the latest estimate is "
            "noisy: it's always reacting to the most recent observation."
        ) as vo:
            self.play(FadeIn(intro))
            step = ladder(self, rows, whys, keep=4, top=2.6, x=-0.6, buff=0.78, edge=6.9)
            for k, m_ in enumerate("abcd"):
                vo.wait_until(m_)
                step(k, transform=False)
        self.clear_scene()

    def averaging(self):
        d = load("sgd")
        k = np.asarray(d["k"], float)
        lk = np.log10(k)
        A = axes([1, np.log10(d["n"])], [-0.1, 1.0], x_length=8.4, y_length=4.4, xlabel=r"observations seen (log scale)",
                 ylabel=r"slope, \ per SD of log income", xticks=[1, 2, 3, 4], yticks=[0, 0.2, 0.4, 0.6, 0.8, 1.0], center=[-1.4, 0.3, 0],
                 xfmt=lambda v: f"{10 ** v:,.0f}")
        ax = A.ax
        mle, se = d["mle"][1], d["se"][1]
        bandr = Polygon(ax.c2p(1, mle - 1.96 * se), ax.c2p(np.log10(d["n"]), mle - 1.96 * se), ax.c2p(np.log10(d["n"]), mle + 1.96 * se),
                        ax.c2p(1, mle + 1.96 * se), stroke_width=0, fill_color=TRUE, fill_opacity=0.18)
        mline = DashedLine(ax.c2p(1, mle), ax.c2p(np.log10(d["n"]), mle), color=TRUE, stroke_width=2.5)
        last = polyline(ax, lk, d["last"], GRAD, 2.5)
        avg = polyline(ax, lk, d["avg"], FAST, 3.5)
        rows = fit_rows(VGroup(
            label(r"the World's vote, \ 20,000 adults, \ one pass", font_size=22),
            label(r"gold band: \ the MLE $\pm$ 1.96 SE", font_size=22, color=TRUE),
            label(r"red: \ SGD's last iterate", font_size=22, color=GRAD),
            label(r"green: \ the running average of all iterates", font_size=22, color=FAST),
            label(r"Polyak \& Juditsky (1992), \ Ruppert (1988)", font_size=20, color=GREY_A),
        ), 3.45, 0.42, [5.1, 0.3, 0])
        with self.voiceover(
            "<bookmark mark='a'/> Here's one pass over twenty thousand of the World's adults, estimating the slope of"
            " the vote on log income. <bookmark mark='b'/> The gold band is the maximum likelihood estimate from all "
            "the data, with its ninety-five percent interval. <bookmark mark='c'/> In red, SGD's latest estimate, "
            "wandering. <bookmark mark='d'/> In green, the plain average of every estimate so far. It's smoother, and"
            " it settles inside the band. <bookmark mark='e'/> Boris Polyak and Anatoli Juditsky, and independently "
            "David Ruppert, proved something remarkable about this average: under stability, smoothness and "
            "nonsingular curvature, with independent observations and step exponents strictly between one half and "
            "one, averaging can match the asymptotic variance of the corresponding estimating-equation solution. "
            "Under a correctly specified likelihood that is MLE efficiency; under misspecification it involves a "
            "sandwich variance. A finite stream is not itself an asymptotic guarantee."
        ) as vo:
            self.add(simulated_tag(r"simulated: \ the World's vote"))
            self.play(FadeIn(A), FadeIn(rows[0]))
            vo.wait_until("a")
            vo.wait_until("b")
            self.play(FadeIn(bandr), Create(mline), FadeIn(rows[1]))
            vo.wait_until("c")
            self.play(Create(last), FadeIn(rows[2]), run_time=2.5)
            vo.wait_until("d")
            self.play(Create(avg), FadeIn(rows[3]), run_time=2.5)
            vo.wait_until("e")
            self.play(FadeIn(rows[4]))
        self.clear_scene()

    def step_sizes(self):
        d = load("sgdsteps")
        pw = np.asarray(d["powers"])
        A = axes([0.45, 1.05], [-2.2, -0.5], x_length=8.0, y_length=4.2, xlabel=r"step exponent $\gamma$: \ $a_k = k^{-\gamma}$",
                 ylabel=r"RMS distance to the MLE (log$_{10}$)", xticks=[0.5, 0.6, 0.7, 0.8, 0.9, 1.0], yticks=[-2, -1.5, -1, -0.5],
                 center=[-1.6, 0.3, 0])
        ax = A.ax
        la = polyline(ax, pw, np.log10(d["rmse_last"]), GRAD, 3.5)
        lv = polyline(ax, pw, np.log10(d["rmse_avg"]), FAST, 3.5)
        da = VGroup(*[Dot(ax.c2p(a, b), radius=0.06, color=GRAD) for a, b in zip(pw, np.log10(d["rmse_last"]))])
        dv = VGroup(*[Dot(ax.c2p(a, b), radius=0.06, color=FAST) for a, b in zip(pw, np.log10(d["rmse_avg"]))])
        se = DashedLine(ax.c2p(0.45, np.log10(d["se"])), ax.c2p(1.05, np.log10(d["se"])), color=TRUE, stroke_width=2.5)
        rows = fit_rows(VGroup(
            label(r"30 streams of 5,000; \ one pass each", font_size=22),
            label(r"red: \ the last iterate", font_size=22, color=GRAD),
            label(r"green: \ the average", font_size=22, color=FAST),
            label(rf"dashed: \ the MLE's own SE, \ {d['se']:.3f}", font_size=22, color=TRUE),
            label(r"averaging wants big steps, \ $\gamma$ near $1/2$; \ $\gamma = 1$ is too timid for both", font_size=20, color=GREY_A),
        ), 3.45, 0.42, [5.1, 0.3, 0])
        with self.voiceover(
            "<bookmark mark='a'/> The step sizes matter. Thirty streams of five thousand adults, one pass each, "
            "measuring how far the final answer is from the exact maximum likelihood estimate, for step exponents "
            "from a half to one. <bookmark mark='b'/> The last iterate, in red, does best around point eight, and "
            "even then is about half a standard error away. <bookmark mark='c'/> The average, in green, does best "
            "with the biggest steps, exponents near a half, where it lands within a third of a standard error of the "
            "MLE. <bookmark mark='d'/> The half-exponent endpoint is a finite-sample comparison, outside the classic "
            "square-summable-step condition. In these streams, with this step constant and starting point, one over k"
            " is too timid for both: the steps shrink too fast to get there in one pass. Averaging lets you take bold"
            " steps and then smooths away their noise."
        ) as vo:
            self.add(simulated_tag(r"simulated: \ the World's vote"))
            self.play(FadeIn(A), Create(se), FadeIn(rows[0]), FadeIn(rows[3]))
            vo.wait_until("a")
            vo.wait_until("b")
            self.play(Create(la), FadeIn(da), FadeIn(rows[1]))
            vo.wait_until("c")
            self.play(Create(lv), FadeIn(dv), FadeIn(rows[2]))
            vo.wait_until("d")
            self.play(FadeIn(rows[4]))
        self.clear_scene()

    def beyond(self):
        rows = fit_rows(VGroup(
            label(r"minibatches: \ average the gradient over $b$ observations; \ variance $/b$", font_size=24, color=GRAD),
            label(r"momentum accumulates a direction; \ Adam adapts steps using gradient moments", font_size=24, color=NEWT),
            label(r"variance reduction: \ linear guarantees for suitable strongly convex finite sums", font_size=24, color=TEAL),
            label(r"several passes over the data: \ epochs", font_size=24, color=PATH),
            label(r"the workhorses of deep learning: \ Part 64", font_size=22, color=GREY_A),
        ), 12.4, 0.5, [0, 0, 0])
        with self.voiceover(
            "Modern practice adds refinements. <bookmark mark='a'/> Minibatches average the gradient over a handful "
            "of observations, cutting its variance and using hardware well. <bookmark mark='b'/> Momentum accumulates"
            " a running direction. Adam, introduced by Diederik Kingma and Jimmy Ba, also uses first and second "
            "gradient moments to adapt parameter-wise steps. <bookmark mark='c'/> SVRG uses periodic full gradients, "
            "while SAGA maintains a table of past component gradients. Under suitable smooth strongly convex "
            "finite-sum conditions, such variance reduction can yield linear convergence; it is not a blanket "
            "guarantee for deep networks. <bookmark mark='d'/> Training usually makes several passes over the data, "
            "called epochs. <bookmark mark='e'/> These are the workhorses of deep learning, which Part 64 takes up."
        ) as vo:
            for k, m_ in enumerate("abcde"):
                vo.wait_until(m_)
                self.play(FadeIn(rows[k], shift=RIGHT * 0.2))
        self.clear_scene()

    def board(self):
        rows = [r for r in load_all(upto=21) if r.part == 21]
        b = coverage_board(rows, lit_part=21, placeholders=0, font_size=20, row_h=0.62)
        b.scale_to_fit_width(min(b.width, 13.0)).move_to(ORIGIN)
        with self.voiceover(
            "<bookmark mark='a'/> The Board checks the claim. Five hundred streams of two thousand adults; after one "
            "pass, a Wald interval of plus or minus one point nine six standard errors, computed at the estimate. "
            "Using the last iterate: eighty-two percent coverage, broken, because the last iterate carries "
            "optimization noise the standard error doesn't know about. <bookmark mark='b'/> Using the Polyak–Ruppert "
            "average: ninety-three percent, within this Board's tolerance. The target is the exact finite-World "
            "logistic projection, not a sampled reference. Five hundred replicates assess this one procedure and "
            "setting; they do not prove nominal coverage or the general efficiency theorem."       ) as vo:
            self.play(FadeIn(b.head), FadeIn(b.axis), FadeIn(b.legend))
            vo.wait_until("a")
            self.play(FadeIn(b.body[0]))
            vo.wait_until("b")
            self.play(FadeIn(b.body[1]))
        self.wait(1.0)
        self.clear_scene()

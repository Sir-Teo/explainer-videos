from __future__ import annotations

import numpy as np

from videos.stats.stats53.common import *  # noqa: F403


class Adaptation(VoiceoverScene):
    def construct(self):
        self.card()
        self.methods()
        self.likelihood()
        self.table()
        self.why_eb()
        self.hb()
        self.hierarchical()

    def card(self):
        card = chapter_card(8, r"Adaptation", r"Letting the data choose the prior's smoothness", lit=(2008,), part=PART)
        with self.voiceover("Chapter eight. Adaptation: letting the data choose the prior's smoothness."):
            self.play(FadeIn(card[0], shift=UP * 0.2), FadeIn(card[1]))
        self.play(FadeOut(card))

    def methods(self):
        rows = [
            cmath(r"\text{empirical Bayes}", r":", r"\hat\alpha = \arg\max_\alpha p(Y \mid \alpha) = \arg\max \textstyle\int p(Y \mid \theta)\, d\Pi_\alpha(\theta)", font_size=30),
            cmath(r"\text{hierarchical Bayes}", r":", r"\alpha \sim \lambda(\alpha), \ \ \theta \mid \alpha \sim \Pi_\alpha", font_size=34),
            cmath(r"\text{sequence model}", r":", r"Y_k \mid \alpha \sim N\big(0, \ k^{-1-2\alpha} + 1/n\big): \ \text{explicit}", font_size=32),
            cmath(r"\text{both}", r":", r"\text{contract at } n^{-\beta/(1+2\beta)} \text{ for every } \beta, \ \text{up to logs}", font_size=32),
        ]
        rows[3][-1].set_color(GOODC)
        whys = [why(r"type-II maximum likelihood"), why(r"a prior on the prior"), why(r"the marginal likelihood"), why(r"Knapik, \ Szabó et al. (2016)")]
        with self.voiceover(
            "<bookmark mark='a'/> Two ways to choose the smoothness from the data. Empirical Bayes maximizes the marginal "
            "likelihood, the probability of the data with the parameter integrated out. <bookmark mark='b'/> Hierarchical "
            "Bayes puts a prior on alpha too, and averages. <bookmark mark='c'/> In the sequence model the marginal "
            "likelihood is explicit: given alpha, each observation is normal with variance k to the minus one minus two "
            "alpha, plus one over n. <bookmark mark='d'/> Bartek Knapik, Botond Szabó and colleagues proved in 2016 that both "
            "contract at the minimax rate for every smoothness beta, up to logarithmic factors: the posterior adapts."
        ) as vo:
            step = ladder(self, rows, whys, keep=4, top=2.6, x=-0.9, buff=0.85, edge=6.9)
            for k, m_ in enumerate("abcd"):
                vo.wait_until(m_)
                step(k, transform=False)
        self.clear_scene()

    def likelihood(self):
        d = load("adapt")
        g = np.asarray(d["grid"])
        ll = np.asarray(d["ll"])
        ll = ll - ll.max()
        A = axes([0.2, 3.0], [-60, 3], x_length=7.4, y_length=4.4, xlabel=r"prior smoothness $\alpha$", ylabel=r"log marginal likelihood (max $= 0$)",
                 xticks=[0.5, 1, 1.5, 2, 2.5, 3], yticks=[-60, -40, -20, 0], center=[-2.5, 0.2, 0])
        ax = A.ax
        c = clip_curve(ax, g, ll, PRIORC, 4, ymin=-60, ymax=3)
        pk = Dot(ax.c2p(d["alpha_hat"], 0), radius=0.12, color=BALLC)
        tr = DashedLine(ax.c2p(d["beta"], -60), ax.c2p(d["beta"], 3), color=TRUTHC, stroke_width=2.5)
        side = fit_rows(VGroup(
            label(rf"one data set, \ $n = 10^4$, \ truth $\beta = {d['beta']:g}$", font_size=22),
            label(r"purple: \ $\log p(Y \mid \alpha)$", font_size=22, color=PRIORC),
            label(rf"gold: \ $\hat\alpha = {d['alpha_hat']:.2f}$", font_size=22, color=BALLC),
            label(r"white: \ the truth's smoothness", font_size=22, color=TRUTHC),
            label(r"the data know how smooth they are", font_size=22, color=GOODC),
        ), 4.6, 0.42, [4.45, 0.4, 0])
        with self.voiceover(
            f"<bookmark mark='a'/> One data set of ten thousand observations from a truth of smoothness one. <bookmark "
            f"mark='b'/> The log marginal likelihood as a function of the prior's smoothness. <bookmark mark='c'/> Its maximum "
            f"is at {say(d['alpha_hat'], 2)}. <bookmark mark='d'/> The truth's smoothness is one. <bookmark mark='e'/> The "
            f"data carry information about their own smoothness, and the marginal likelihood finds it."
        ) as vo:
            self.play(FadeIn(A), FadeIn(simulated_tag(r"one simulated data set")))
            vo.wait_until("a")
            self.play(FadeIn(side[0]))
            vo.wait_until("b")
            self.play(Create(c), FadeIn(side[1]))
            vo.wait_until("c")
            self.play(FadeIn(pk), FadeIn(side[2]))
            vo.wait_until("d")
            self.play(Create(tr), FadeIn(side[3]))
            vo.wait_until("e")
            self.play(FadeIn(side[4]))
        self.clear_scene()

    def table(self):
        d = load("adapt")
        rows = [[r"$n$"] + [f"$10^{{{int(np.log10(r['n']))}}}$" for r in d["rows"]],
                [r"$\hat\alpha$ \ (mean, \ 20 data sets)"] + [f"{r['alpha_hat']:.2f}" for r in d["rows"]],
                [r"SD of $\hat\alpha$"] + [f"{r['alpha_sd']:.2f}" for r in d["rows"]],
                [r"EB risk / best fixed $\alpha$"] + [f"{r['risk'] / r['oracle']:.3f}" for r in d["rows"]]]
        tab = table_rows(rows, font_size=28, col_buff=0.7, row_buff=0.42, colors=[GREY_B, BALLC, GREY_A, GOODC])
        tab.move_to([0, 0.9, 0])
        rr = d["rows"]
        foot = label(r"$\hat\alpha$ drifts towards $\beta = 1$ \ and steadies; \ the risk approaches the oracle's", font_size=24, color=GREY_A).move_to([0, -1.2, 0])
        foot2 = label(r"empirical Bayes costs almost nothing in risk", font_size=24, color=GOODC).move_to([0, -2.0, 0])
        with self.voiceover(
            f"<bookmark mark='a'/> Over twenty data sets at each size. The estimated smoothness averages "
            f"{say(rr[0]['alpha_hat'], 2)} at a hundred observations and {say(rr[-1]['alpha_hat'], 2)} at a million, with "
            f"its spread shrinking from {say(rr[0]['alpha_sd'], 2)} to {say(rr[-1]['alpha_sd'], 2)}. <bookmark mark='b'/> "
            f"The empirical Bayes posterior's risk is within {100 * (rr[0]['risk'] / rr[0]['oracle'] - 1):.0f} percent of the "
            f"best fixed smoothness's at a hundred, and within {100 * (rr[-1]['risk'] / rr[-1]['oracle'] - 1):.1f} percent at a "
            f"million. <bookmark mark='c'/> For estimation, adaptation is nearly free, as Part fifty found for Lepski's "
            f"method."
        ) as vo:
            vo.wait_until("a")
            self.play(FadeIn(tab), FadeIn(simulated_tag(r"simulated; \ risks exact")))
            vo.wait_until("b")
            self.play(FadeIn(foot))
            vo.wait_until("c")
            self.play(FadeIn(foot2))
        self.clear_scene()

    def why_eb(self):
        rows = [
            cmath(r"\partial_\alpha \log p(Y \mid \alpha) = 0", r"\iff", r"\textstyle\sum_k \frac{\partial_\alpha\lambda_k}{(\lambda_k + 1/n)^2}\big(Y_k^2 - \lambda_k - 1/n\big) = 0", font_size=30),
            cmath(r"\text{read}", r":", r"\text{match observed and prior energy, \ per frequency}", font_size=32),
            cmath(r"\text{the frequencies that matter}", r":", r"k \approx n^{1/(1+2\beta)}: \ \text{where signal meets noise}", font_size=32),
            cmath(r"\text{so}", r":", r"\hat\alpha \text{ tracks the truth's smoothness at the critical frequency}", font_size=32),
        ]
        rows[3][-1].set_color(GOODC)
        whys = [why(r"the score in $\alpha$"), why(r"method of moments, \ weighted"), why(r"the bias--variance frontier"), why(r"and only there")]
        with self.voiceover(
            "<bookmark mark='a'/> Why does the marginal likelihood find the smoothness? Set its derivative in alpha to zero. <bookmark mark='b'/> The equation matches the observed energy at each frequency, Y k squared, to the energy the prior predicts, lambda k plus one over n, a weighted method of moments. <bookmark mark='c'/> The weights concentrate the information around the frequency where signal and noise are of the same size, about n to the one over one plus two beta. <bookmark mark='d'/> So alpha hat measures the truth's smoothness at the critical frequency, and only there. If the truth behaves differently elsewhere, as an inconvenient truth does, alpha hat is fooled."
        ) as vo:
            step = ladder(self, rows, whys, keep=4, top=2.6, x=-0.9, buff=0.85, edge=6.9)
            for k, m_ in enumerate("abcd"):
                vo.wait_until(m_)
                step(k, transform=False)
        self.clear_scene()

    def hb(self):
        rows = [
            cmath(r"\text{hierarchical}", r":", r"\pi(\alpha \mid Y) \propto \lambda(\alpha)\, p(Y \mid \alpha)", font_size=34),
            cmath(r"\text{concentrates}", r":", r"\text{around } \hat\alpha \text{ as } n \text{ grows}", font_size=34),
            cmath(r"\text{so}", r":", r"\text{hierarchical} \approx \text{empirical Bayes, \ asymptotically}", font_size=34),
            cmath(r"\text{in practice}", r":", r"\text{a little more honesty in small samples}", font_size=32),
        ]
        rows[2][-1].set_color(GOODC)
        whys = [why(r"a posterior over priors"), why(r"Knapik et al. (2016)"), why(r"same rates"), why(r"the full-Bayes argument")]
        with self.voiceover(
            "<bookmark mark='a'/> The hierarchical alternative puts a prior on alpha and lets the data update it, the posterior over alpha being the prior times the marginal likelihood. <bookmark mark='b'/> That posterior concentrates around the empirical Bayes choice. <bookmark mark='c'/> So asymptotically the two behave the same, with the same rates and the same coverage problems. <bookmark mark='d'/> In small samples, the spread of the posterior over alpha propagates into the credible sets, which makes them a little wider and a little more honest: the usual argument for being fully Bayesian."
        ) as vo:
            step = ladder(self, rows, whys, keep=4, top=2.6, x=-0.9, buff=0.85, edge=6.9)
            for k, m_ in enumerate("abcd"):
                vo.wait_until(m_)
                step(k, transform=False)
        self.clear_scene()

    def hierarchical(self):
        rows = fit_rows(VGroup(
            label(r"but for uncertainty, \ adaptation has a price (Part 50, \ Low 1997):", font_size=28, color=GREY_A),
            label(r"the posterior's spread depends on $\hat\alpha$; \ if $\hat\alpha$ is too large, \ the ball is too small", font_size=26, color=BADC),
            label(r"for most truths, \ $\hat\alpha$ is about right, \ and an inflated ball covers", font_size=26, color=GOODC),
            label(r"for some truths, \ $\hat\alpha$ is fooled, \ and no inflation saves every $n$", font_size=26, color=BADC),
            label(r"which truths? \ the next chapter, \ and the Board", font_size=26, color=BALLC),
        ), 12.4, 0.55, [0, 0, 0])
        with self.voiceover(
            "<bookmark mark='a'/> But for uncertainty quantification, adaptation has a price, as Mark Low's theorem in Part "
            "fifty warned. <bookmark mark='b'/> The posterior's spread depends on the estimated smoothness. If the data make "
            "alpha hat too large, the posterior is too confident and the credible ball too small. <bookmark mark='c'/> For "
            "most truths alpha hat is about right, and a modestly inflated ball covers. <bookmark mark='d'/> For some truths, "
            "alpha hat is fooled, and no fixed inflation rescues coverage at every sample size. <bookmark mark='e'/> Which "
            "truths those are is the next chapter's question."
        ) as vo:
            for k, m_ in enumerate("abcde"):
                vo.wait_until(m_)
                self.play(FadeIn(rows[k], shift=RIGHT * 0.2))
        self.clear_scene()

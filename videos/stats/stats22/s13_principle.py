from __future__ import annotations

import numpy as np
from scipy import stats

from videos.stats.stats22.common import *  # noqa: F403


class Principle(VoiceoverScene):
    def construct(self):
        self.card()
        self.two_experiments()
        self.same_curve()
        self.sample_spaces()
        self.bayes()
        self.birnbaum()
        self.debate()

    def card(self):
        card = chapter_card(12, r"The likelihood principle", r"Should the stopping rule matter?", lit=(1962,), part=PART)
        with self.voiceover("Chapter twelve. The likelihood principle."):
            self.play(FadeIn(card[0], shift=UP * 0.2), FadeIn(card[1]))
        self.play(FadeOut(card))

    def two_experiments(self):
        rows = [
            cmath(r"\text{the data}", r":", r"\text{9 heads and 3 tails; \ is the coin biased to heads?}", font_size=28),
            cmath(r"\text{Alice}", r":", r"\text{toss 12 times: \ } \binom{12}{9}\theta^9 (1 - \theta)^3", font_size=30),
            cmath(r"\text{Bob}", r":", r"\text{toss until the 3rd tail: \ } \binom{11}{9}\theta^9 (1 - \theta)^3", font_size=30),
            cmath(r"\text{both}", r"\propto", r"\theta^9 (1 - \theta)^3", font_size=32),
        ]
        rows[3][2].set_color(LIK)
        whys = [why(r"the same twelve tosses"), why(r"binomial: \ $n$ fixed"), why(r"negative binomial: \ tails fixed"),
                why(r"the same likelihood, \ up to a constant")]
        intro = label('Different stopping plans can yield proportional likelihoods', font_size=36).move_to([0, 3.35, 0])
        if intro.width > 12.5:
            intro.width = 12.5
        with self.voiceover(
            "<bookmark mark='a'/> Consider a sequence whose twelfth toss is its third tail, with nine heads in total."
            " Is the coin biased towards heads? <bookmark mark='b'/> Alice had planned to toss twelve times. For her,"
            " the number of heads is binomial. <bookmark mark='c'/> Bob had planned to toss until the third tail. For"
            " him, the number of heads is negative binomial, with a different constant in front. <bookmark mark='d'/>"
            " As functions of theta, the two likelihoods are proportional: the same curve, rescaled."
        ) as vo:
            self.play(FadeIn(intro))
            step = ladder(self, rows, whys, keep=4, top=2.6, x=-0.9, buff=0.82, edge=6.9)
            for k, m_ in enumerate("abcd"):
                vo.wait_until(m_)
                step(k, transform=False)
        self.clear_scene()

    def same_curve(self):
        d = load("principle")
        th, lk = np.asarray(d["theta"]), np.asarray(d["lik"])
        A = axes([0.3, 1.0], [0, 1.15], x_length=8.0, y_length=4.4, xlabel=r"$\theta$, \ the chance of heads",
                 ylabel=r"likelihood, \ scaled to 1", xticks=[0.3, 0.5, 0.7, 0.9], yticks=[0, 0.5, 1], center=[-1.6, 0.3, 0])
        ax = A.ax
        alice = curve(ax, th, lk, LIK, 5)
        bob = DashedVMobject(curve(ax, th, lk, PATH, 3), num_dashes=40)
        half = DashedLine(ax.c2p(0.5, 0), ax.c2p(0.5, 1.1), color=GREY_B, stroke_width=2)
        ratio = float((0.5 ** 12) / (0.75 ** 9 * 0.25 ** 3))
        rows = fit_rows(VGroup(
            label(r"green: \ Alice's likelihood", font_size=22, color=LIK),
            label(r"gold, \ dashed: \ Bob's: \ the same curve", font_size=22, color=PATH),
            label(r"peak at $\hat\theta = 0.75$ for both", font_size=22),
            label(rf"$L(0.5)/L(0.75) = {ratio:.3f}$ for both", font_size=22, color=GREY_A),
            label(r"so the evidence about $\theta$ is the same?", font_size=22, color=HIT),
        ), 3.45, 0.42, [5.1, 0.3, 0])
        with self.voiceover(
            "<bookmark mark='a'/> Here is Alice's likelihood, scaled to peak at one. <bookmark mark='b'/> Bob's, "
            "dashed, lies exactly on top of it. <bookmark mark='c'/> Both peak at three quarters. <bookmark "
            "mark='d'/> The observed data have about a fifth as much likelihood under a fair coin as under the fitted"
            " probability. This is not a posterior probability that the coin is fair. <bookmark mark='e'/> If the "
            "likelihood is all the data have to say about theta, then Alice and Bob have the same evidence, and "
            "should reach the same conclusion."
        ) as vo:
            self.play(FadeIn(A), Create(half))
            vo.wait_until("a")
            self.play(Create(alice), FadeIn(rows[0]))
            vo.wait_until("b")
            self.play(Create(bob), FadeIn(rows[1]))
            for k, m_ in enumerate("cde"):
                vo.wait_until(m_)
                self.play(FadeIn(rows[k + 2]))
        self.clear_scene()

    def sample_spaces(self):
        d = load("principle")
        ka = np.arange(0, 13)
        A1 = axes([-0.6, 12.6], [0, 0.25], x_length=5.6, y_length=3.2, xlabel=r"heads in 12 tosses", ylabel=r"$P$ if fair",
                  xticks=[0, 3, 6, 9, 12], yticks=[0, 0.1, 0.2], center=[-3.5, 0.6, 0])
        a = bars_at(A1.ax, ka, stats.binom.pmf(ka, 12, 0.5), 0.75, GREY_B, 0.8, highlight=set(range(9, 13)), hcolor=LIK)
        kb = np.arange(0, 21)
        A2 = axes([-0.6, 20.6], [0, 0.25], x_length=5.6, y_length=3.2, xlabel=r"heads before the 3rd tail", ylabel=r"$P$ if fair",
                  xticks=[0, 5, 10, 15, 20], yticks=[0, 0.1, 0.2], center=[3.4, 0.6, 0])
        b = bars_at(A2.ax, kb, stats.nbinom.pmf(kb, 3, 0.5), 0.75, GREY_B, 0.8, highlight=set(range(9, 21)), hcolor=PATH)
        la = label(rf"Alice: \ $P(\ge 9) = {d['p_binomial']:.3f}$", font_size=26, color=LIK).next_to(A1, DOWN, buff=0.3)
        lb = label(rf"Bob: \ $P(\ge 9) = {d['p_negbin']:.3f}$", font_size=26, color=PATH).next_to(A2, DOWN, buff=0.3)
        foot = label(r"at 5\%: \ Alice cannot reject a fair coin; \ Bob can", font_size=28, color=RES).to_edge(DOWN, buff=0.55)
        with self.voiceover(
            "<bookmark mark='a'/> Now compute p-values for a fair coin. A p-value asks about outcomes at least as extreme as "
            "the one observed, and those outcomes depend on the plan. Alice's possible results are zero to twelve heads; nine or "
            "more has probability point oh seven three. <bookmark mark='b'/> Bob's possible results are any number of heads "
            "before the third tail, with no upper limit; nine or more has probability point oh three three. "
            "<bookmark mark='c'/> At the five percent level, Alice can't reject a fair coin and Bob can, from the same tosses. "
            "The difference lies entirely in outcomes that didn't happen."
        ) as vo:
            vo.wait_until("a")
            self.play(FadeIn(A1), LaggedStart(*[GrowFromEdge(x, DOWN) for x in a], lag_ratio=0.05), FadeIn(la))
            vo.wait_until("b")
            self.play(FadeIn(A2), LaggedStart(*[GrowFromEdge(x, DOWN) for x in b], lag_ratio=0.04), FadeIn(lb))
            vo.wait_until("c")
            self.play(FadeIn(foot))
        self.clear_scene()

    def bayes(self):
        from scipy import stats as st
        post = st.beta(10, 4)
        lo, hi = post.ppf([0.025, 0.975])
        rows = [
            cmath(r"\text{prior}", r":", r"\theta \sim \text{Beta}(1, 1), \ \text{uniform}", font_size=30),
            cmath(r"\text{posterior}", r"\propto", r"\theta^9 (1 - \theta)^3 \Rightarrow \text{Beta}(10, 4) \ \text{for both}", font_size=30),
            cmath(r"P(\theta > 0.5 \mid \text{data})", r"=", rf"{post.sf(0.5):.3f}", font_size=30),
            cmath(r"\text{95\% credible interval}", r":", rf"[{lo:.2f}, \ {hi:.2f}]", font_size=30),
        ]
        rows[2][2].set_color(PRIOR)
        whys = [why(r"Part 15's conjugate prior"), why(r"the constants $\binom{12}{9}$, \ $\binom{11}{9}$ cancel"),
                why(r"the same for Alice and Bob"), why(r"Part 15: \ theta-free stopping; \ same fixed prior")]
        intro = label('The same fixed prior gives the same posterior here', font_size=36).move_to([0, 3.35, 0])
        if intro.width > 12.5:
            intro.width = 12.5
        with self.voiceover(
            "<bookmark mark='a'/> A Bayesian with Part 15's uniform prior sees no difference at all. <bookmark "
            "mark='b'/> The posterior is proportional to prior times likelihood, the constants in front cancel, and "
            "both Alice and Bob get a beta with parameters ten and four. <bookmark mark='c'/> The posterior "
            "probability that the coin favours heads is point nine five four, for both. <bookmark mark='d'/> Their "
            "ninety-five percent credible intervals are identical too, point four six to point nine one. For these "
            "theta-free stopping rules and the same fixed prior, the stopping factor cancels. Informative sampling or"
            " selection and data-dependent prior choices must be modeled."
        ) as vo:
            self.play(FadeIn(intro))
            step = ladder(self, rows, whys, keep=4, top=2.6, x=-0.9, buff=0.82, edge=6.9)
            for k, m_ in enumerate("abcd"):
                vo.wait_until(m_)
                step(k, transform=False)
        self.clear_scene()

    def birnbaum(self):
        rows = [
            cmath(r"\text{sufficiency}", r":", r"\text{same sufficient statistic} \Rightarrow \text{same evidence}", font_size=28),
            cmath(r"\text{conditionality}", r":", r"\text{a coin chose the experiment} \Rightarrow \text{judge the one done}", font_size=28),
            cmath(r"\text{together}", r"\Rightarrow", r"\text{proportional likelihoods, \ same evidence}", font_size=28),
            cmath(r"\text{who obeys}", r":", r"\text{Bayes, \ pure likelihood; \ not p-values, \ CIs, \ unbiasedness}", font_size=28),
        ]
        rows[2][2].set_color(LIK)
        whys = [why(r"Part 9: \ nobody objects"), why(r"Fisher; \ chapter four's ancillaries; \ Cox (1958)"),
                why(r"Birnbaum (1962): \ the likelihood principle"), why(r"stopping rules stop mattering")]
        intro = label('The likelihood principle depends on the interpretation of conditionality', font_size=36).move_to([0, 3.35, 0])
        if intro.width > 12.5:
            intro.width = 12.5
        with self.voiceover(
            "In 1962 Allan Birnbaum turned this into a theorem that alarmed his colleagues. <bookmark mark='a'/> "
            "Start from two principles almost everyone accepts. Sufficiency: two data sets with the same sufficient "
            "statistic carry the same evidence. <bookmark mark='b'/> Conditionality: if a coin flip chose which of "
            "two experiments to run, judge the result by the experiment actually run, the idea behind chapter four's "
            "conditioning, and David Cox's 1958 example of two measuring instruments. <bookmark mark='c'/> Birnbaum "
            "showed that together they imply the likelihood principle: experiments with proportional likelihoods give"
            " the same evidence. <bookmark mark='d'/> Bayesian updating with the same fixed prior obeys it when the "
            "full sampling and stopping likelihoods are proportional. Conventional p-values and confidence procedures"
            " generally use sampling distributions beyond the observed likelihood. Their operating properties depend "
            "on the plan. And for a Bayesian, a stopping rule doesn't matter."
        ) as vo:
            self.play(FadeIn(intro))
            step = ladder(self, rows, whys, keep=4, top=2.6, x=-0.9, buff=0.82, edge=6.9)
            for k, m_ in enumerate("abcd"):
                vo.wait_until(m_)
                step(k, transform=False)
        self.clear_scene()

    def debate(self):
        rows = fit_rows(VGroup(
            label(r"Savage (1962): \ praised the principle\'s implications", font_size=24, color=PRIOR),
            label(r"Birnbaum himself later doubted it; \ Mayo (2014): \ the proof has a gap", font_size=24, color=RES),
            label(r"Gandenberger (2015), \ Evans (2013): \ the argument repaired and re-attacked", font_size=24, color=GREY_A),
            label(r"the practical answer: \ coverage is a property of the procedure", font_size=24, color=HIT),
            label(r"so the plan matters to the Board: \ peeking, \ optional stopping, \ Part 58", font_size=24, color=OBS),
        ), 12.4, 0.5, [0, 0, 0])
        with self.voiceover(
            "<bookmark mark='a'/> Jimmie Savage, discussing the paper, said the likelihood principle had striking "
            "implications for statistical inference. Savage had already published his Bayesian Foundations of "
            "Statistics in 1954. <bookmark mark='b'/> Birnbaum himself later had doubts, and Deborah Mayo argued in "
            "2014 that the proof has a gap: the conditionality principle is being applied where it doesn't belong. "
            "<bookmark mark='c'/> Others have repaired and re-attacked the argument since; the debate is open. "
            "<bookmark mark='d'/> For this series, the practical answer is that coverage is a property of a "
            "procedure, and the procedure includes the plan. <bookmark mark='e'/> An analyst who peeks at the data "
            "and stops when the result looks good does change the Board's verdict, even when the final likelihood is "
            "the same. Part 58 builds tests that stay valid however you stop."
        ) as vo:
            for k, m_ in enumerate("abcde"):
                vo.wait_until(m_)
                self.play(FadeIn(rows[k], shift=RIGHT * 0.2))
        self.clear_scene()

from __future__ import annotations

import numpy as np

from videos.stats.stats11.common import *  # noqa: F403


class Credible(VoiceoverScene):
    def construct(self):
        self.card()
        self.credible()
        self.coverage()
        self.hpd()
        self.welch()
        self.welch_numbers()
        self.moral()

    def card(self):
        card = chapter_card(10, r"Credible vs confidence", r"Where they agree, \ and where they part", part=PART)
        with self.voiceover("Chapter ten. Credible intervals versus confidence intervals."):
            self.play(FadeIn(card[0], shift=UP * 0.2), FadeIn(card[1]))
        self.play(FadeOut(card))

    def credible(self):
        rows = [
            cmath(r"\pi(p \mid x)", r"\propto", r"p^x(1 - p)^{n - x}\cdot \pi(p)", font_size=34),
            cmath(r"\pi(p) \propto p^{-1/2}(1 - p)^{-1/2}", r"\Rightarrow", r"p \mid x \sim \mathrm{Beta}\big(x + \tfrac12,\ n - x + \tfrac12\big)", font_size=30),
            cmath(r"P\big(p \in C \mid x\big)", r"=", r"0.95", r"\quad\text{the statement people want to make}", font_size=32),
        ]
        rows[2][2].set_color(OBS)
        whys = [why(r"Bayes' rule (Part 2), \ with a prior on $p$"), why(r"Jeffreys' prior: \ the posterior is a beta (Part 15)"),
                why(r"a probability about $p$, \ given these data")]
        with self.voiceover(
            "The interpretation that chapter one forbade has a home: Bayesian inference. <bookmark mark='a'/> Give the "
            "parameter a prior distribution, and Bayes' rule turns the likelihood into a posterior distribution for p "
            "given the data. <bookmark mark='b'/> With Jeffreys' prior, the posterior for a proportion is a beta "
            "distribution, and its middle ninety-five percent is the Jeffreys interval of chapter four. "
            "<bookmark mark='c'/> For that interval, the statement there's a ninety-five percent probability that p lies "
            "in it is correct, as a statement about the posterior. Part 15 builds this properly. The question here is "
            "how the two kinds of interval relate."
        ) as vo:
            step = ladder(self, rows, whys, keep=3, top=2.4, x=0.4, buff=0.9, edge=6.9)
            for k, m_ in enumerate("abc"):
                vo.wait_until(m_)
                step(k, transform=False)
        self.clear_scene()

    def coverage(self):
        d = load("credible")
        ps = np.asarray(d["ps"])
        A = axes([0, 1], [0.85, 1], x_length=8.0, y_length=4.4, xlabel=r"true $p$, \ $n = 50$", ylabel=r"frequentist coverage of 95\% credible intervals",
                 xticks=[0, 0.25, 0.5, 0.75, 1], yticks=[0.85, 0.9, 0.95, 1], yfmt=lambda v: f"{v:.2f}", center=[-1.8, -0.3, 0])
        ax = A.ax
        nom = DashedLine(ax.c2p(0, 0.95), ax.c2p(1, 0.95), color=EXACT, stroke_width=2)
        cj = polyline(ax, ps, np.clip(d["jeffreys"], 0.85, 1), METHOD_COL["jeffreys"], 2.2)
        cf = polyline(ax, ps, np.clip(d["flat"], 0.85, 1), S.POST, 2.2)
        leg = legend([(METHOD_COL["jeffreys"], rf"Jeffreys prior: \ mean {100 * d['j_mean']:.1f}\%"),
                      (S.POST, rf"flat prior: \ mean {100 * d['f_mean']:.1f}\%")], font_size=22).to_edge(UP, buff=0.35)
        rows = fit_rows(VGroup(
            label(r"close to 95\% on average: \ for large $n$ they coincide", font_size=24),
            label(r"Bernstein--von Mises (Part 53): \ the posterior becomes $N(\hat\theta, 1/nI)$", font_size=22, color=GREY_A),
            MathTex(rf"p = 0.01:\ \text{{flat}}\ {100 * d['f_small']:.1f}\%,\ \text{{Jeffreys}}\ {100 * d['j_small']:.1f}\%", font_size=24),
            label(r"at the edges the prior matters", font_size=22, color=GREY_A),
        ), 4.4, 0.34, [4.7, -0.5, 0])
        with self.voiceover(
            "<bookmark mark='a'/> Judge Bayesian intervals by Neyman's standard: fix the true p and ask how often the "
            "ninety-five percent credible interval contains it. The Jeffreys interval: ninety-five point oh percent on "
            "average. <bookmark mark='b'/> With a flat prior instead, ninety-five point two. <bookmark mark='c'/> On "
            "average they behave like good confidence intervals, and for large samples the two theories agree almost "
            "exactly: the Bernstein–von Mises theorem of Part 53 says the posterior becomes the same normal curve that "
            "Part 9's asymptotics give the estimator. <bookmark mark='d'/> At the edges, though, the prior matters. At p "
            "equals point zero one, the flat-prior interval covers ninety-one percent of the time, Jeffreys' "
            "ninety-nine."
        ) as vo:
            self.play(FadeIn(A), Create(nom))
            vo.wait_until("a")
            self.play(Create(cj), FadeIn(leg[0]))
            vo.wait_until("b")
            self.play(Create(cf), FadeIn(leg[1]))
            vo.wait_until("c")
            self.play(FadeIn(rows[:2]))
            vo.wait_until("d")
            self.play(FadeIn(rows[2:]))
        self.clear_scene()

    def welch(self):
        hc = history_card(1939, r"B. L. Welch, \ \emph{Annals of Mathematical Statistics} 10", r"two draws from Uniform$(\theta - \tfrac12, \theta + \tfrac12)$: \ "
                          r"the interval between them is a 50\% confidence interval, \ yet sometimes we \emph{know} it contains $\theta$",
                          color=OBS, width=9.6, font_size=24).move_to([0, 2.0, 0])
        nl1 = NumberLine(x_range=[-1, 1, 0.5], length=9.0, include_numbers=False, color=GREY_C).move_to([0, 0.1, 0])
        nl2 = NumberLine(x_range=[-1, 1, 0.5], length=9.0, include_numbers=False, color=GREY_C).move_to([0, -1.9, 0])
        th1 = Triangle(color=EXACT, fill_opacity=1).scale(0.1).rotate(PI).move_to(nl1.n2p(0) + UP * 0.25)
        th2 = Triangle(color=EXACT, fill_opacity=1).scale(0.1).rotate(PI).move_to(nl2.n2p(0) + UP * 0.25)
        w = VGroup(Line(nl1.n2p(-0.4), nl1.n2p(0.35), color=HIT, stroke_width=8), Dot(nl1.n2p(-0.4), color=DATA), Dot(nl1.n2p(0.35), color=DATA))
        nrw = VGroup(Line(nl2.n2p(0.05), nl2.n2p(0.2), color=MISS, stroke_width=8), Dot(nl2.n2p(0.05), color=DATA), Dot(nl2.n2p(0.2), color=DATA))
        l1 = label(r"far apart ($\ge \tfrac12$): \ $\theta$ \emph{must} be between them", font_size=24, color=HIT).next_to(nl1, DOWN, buff=0.25)
        l2 = label(r"close together: \ only a 1 in 3 chance", font_size=24, color=MISS).next_to(nl2, DOWN, buff=0.25)
        with self.voiceover(
            "But the two ideas can part company sharply, and Bernard Welch gave the classic example in 1939. "
            "<bookmark mark='a'/> Take two draws from a uniform distribution of width one, centred on an unknown theta. "
            "The interval between them contains theta exactly when the two draws fall on opposite sides of it, which "
            "happens half the time. So it's a fifty percent confidence interval. <bookmark mark='b'/> Now suppose the two "
            "draws are more than a half apart. Each is within a half of theta, so theta must be between them. In this "
            "case we know, with certainty, that this fifty percent interval is right. <bookmark mark='c'/> And if they're "
            "very close together, the interval is right only about a third of the time. The confidence level is the "
            "same, fifty percent, in both cases."
        ) as vo:
            vo.wait_until("a")
            self.play(FadeIn(hc, shift=UP * 0.2))
            vo.wait_until("b")
            self.play(Create(nl1), FadeIn(th1), FadeIn(w), FadeIn(l1))
            vo.wait_until("c")
            self.play(Create(nl2), FadeIn(th2), FadeIn(nrw), FadeIn(l2))
        self.clear_scene()

    def welch_numbers(self):
        d = load("welch")
        rows = [
            cmath(r"P_\theta(\theta \in [X_{(1)}, X_{(2)}])", r"=", rf"{d['cov']:.3f}", r"\quad\text{the confidence level}", font_size=32),
            cmath(r"P(\text{range} \ge \tfrac12)", r"=", rf"{d['p_wide']:.3f}", r"\quad\text{then coverage } " + f"{d['cov_wide']:.3f}", font_size=30),
            cmath(r"P(\text{range} < \tfrac12)", r"=", rf"{1 - d['p_wide']:.3f}", r"\quad\text{then coverage } " + f"{d['cov_narrow']:.3f}", font_size=30),
        ]
        rows[1][2].set_color(HIT)
        rows[2][2].set_color(MISS)
        whys = [why(r"exact: \ $\tfrac12$"), why(r"a quarter of samples: \ certainly right"), why(r"the rest: \ right one time in three")]
        foot = fit_rows(VGroup(
            label(r"$0.25 \times 1 + 0.75 \times \tfrac13 = 0.5$: \ the average hides two very different situations", font_size=26, color=OBS),
            label(r"the conditionality principle: \ judge by the situation you are in \ (Fisher's ``relevant subsets''; \ Part 46)", font_size=24,
                  color=GREY_A),
        ), 12.6, 0.3, [0, -2.1, 0])
        tag = simulated_tag(r"simulated: \ 100,000 pairs", corner=UR)
        with self.voiceover(
            "The simulation confirms it. <bookmark mark='a'/> Overall, the interval covers theta half the time. "
            "<bookmark mark='b'/> A quarter of the time the draws are at least a half apart, and then it covers every "
            "time. <bookmark mark='c'/> Three quarters of the time they're closer, and then it covers a third of the time. "
            "<bookmark mark='d'/> A quarter times one plus three quarters times a third is a half. The fifty percent "
            "average hides two completely different situations, and once you've seen the data, you know which one you're "
            "in. Reporting fifty percent confidence for an interval you know is right seems perverse. This is the "
            "conditionality principle: inference should be judged by the situation you're actually in, an idea Fisher "
            "called relevant subsets, which Part 46 develops."
        ) as vo:
            self.play(FadeIn(tag))
            step = ladder(self, rows, whys, keep=3, top=2.4, x=0.0, buff=0.7, edge=6.9)
            for k, m_ in enumerate("abc"):
                vo.wait_until(m_)
                step(k, transform=False)
            vo.wait_until("d")
            self.play(FadeIn(foot))
        self.clear_scene()

    def moral(self):
        left = VGroup(label(r"confidence", font_size=32, color=OBS), label(r"a property of the procedure", font_size=24),
                      label(r"holds for every $\theta$", font_size=24), label(r"no prior needed", font_size=24),
                      label(r"can ignore what this sample reveals", font_size=24, color=GREY_A)).arrange(DOWN, buff=0.28)
        right = VGroup(label(r"credibility", font_size=32, color=METHOD_COL["jeffreys"]), label(r"a property of this interval, \ given $x$", font_size=24),
                       label(r"holds on average over the prior", font_size=24), label(r"needs a prior", font_size=24),
                       label(r"conditions on the data by construction", font_size=24, color=GREY_A)).arrange(DOWN, buff=0.28)
        left.move_to([-3.4, 0.6, 0])
        right.move_to([3.4, 0.6, 0])
        div = Line([0, 2.4, 0], [0, -1.4, 0], color=GREY_D)
        foot = label(r"in regular problems with lots of data they agree; \ the Board judges both by coverage", font_size=24, color=GREY_A).to_edge(DOWN, buff=0.6)
        with self.voiceover(
            "<bookmark mark='a'/> Confidence is a property of a procedure: it holds for every value of the parameter, needs "
            "no prior, but can ignore what a particular sample reveals. <bookmark mark='b'/> Credibility is a property of "
            "a particular interval given the data: it conditions on everything observed, but it needs a prior, and its "
            "probability statement holds on average over that prior. <bookmark mark='c'/> In regular problems with plenty "
            "of data they agree, and the Coverage Board judges both kinds by the same frequentist test, as Part 26 does "
            "for hierarchical models."
        ) as vo:
            vo.wait_until("a")
            self.play(FadeIn(left, lag_ratio=0.2), Create(div))
            vo.wait_until("b")
            self.play(FadeIn(right, lag_ratio=0.2))
            vo.wait_until("c")
            self.play(FadeIn(foot))
        self.clear_scene()

    def hpd(self):
        from scipy import optimize, stats as st
        a, b = 2 + 0.5, 28 + 0.5
        eq = (st.beta.ppf(0.025, a, b), st.beta.ppf(0.975, a, b))

        def width(lo):
            return st.beta.ppf(st.beta.cdf(lo, a, b) + 0.95, a, b) - lo

        lo = optimize.minimize_scalar(width, bounds=(1e-6, st.beta.ppf(0.0499, a, b)), method="bounded").x
        hp = (lo, st.beta.ppf(st.beta.cdf(lo, a, b) + 0.95, a, b))
        ps = np.linspace(0.001, 0.3, 300)
        A = axes([0, 0.3], [0, 14], x_length=7.4, y_length=3.8, xlabel=r"$p$: \ Jeffreys posterior after 2 of 30", xticks=[0, 0.1, 0.2, 0.3],
                 center=[-2.0, 0.2, 0])
        ax = A.ax
        cv = curve(ax, ps, st.beta.pdf(ps, a, b), METHOD_COL["jeffreys"], 3)
        e1 = Line(ax.c2p(eq[0], 1.0), ax.c2p(eq[1], 1.0), color=METHOD_COL["jeffreys"], stroke_width=7)
        h1 = Line(ax.c2p(hp[0], 2.2), ax.c2p(hp[1], 2.2), color=OBS, stroke_width=7)
        rows = fit_rows(VGroup(
            MathTex(rf"\text{{equal-tailed: }}[{eq[0]:.3f},\ {eq[1]:.3f}]", font_size=28, color=METHOD_COL["jeffreys"]),
            MathTex(rf"\text{{highest density: }}[{hp[0]:.3f},\ {hp[1]:.3f}]", font_size=28, color=OBS),
            label(r"both hold 95\% posterior probability; \ the HPD is the shortest", font_size=22, color=GREY_A),
            label(r"but the HPD is not invariant: \ transform $p$ and it changes", font_size=22, color=GREY_A),
        ), 4.8, 0.32, [4.6, -0.2, 0])
        with self.voiceover(
            "A Bayesian interval has the same freedom as a pivot interval. <bookmark mark='a'/> After two successes in "
            "thirty, the Jeffreys posterior is skewed. <bookmark mark='b'/> Its equal-tailed ninety-five percent interval "
            "cuts two and a half percent from each tail. <bookmark mark='c'/> The highest posterior density interval "
            "instead collects the most probable values first; it's the shortest set with ninety-five percent probability, "
            "and here it starts much closer to zero. <bookmark mark='d'/> But it isn't invariant: on the log-odds scale the "
            "highest-density set is a different set of p's. Equal tails are invariant, which is one reason Brown, Cai and "
            "DasGupta used them."
        ) as vo:
            self.play(FadeIn(A))
            vo.wait_until("a")
            self.play(Create(cv))
            vo.wait_until("b")
            self.play(Create(e1), FadeIn(rows[0]))
            vo.wait_until("c")
            self.play(Create(h1), FadeIn(rows[1:3]))
            vo.wait_until("d")
            self.play(FadeIn(rows[3]))
        self.clear_scene()

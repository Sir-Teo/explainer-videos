from __future__ import annotations

import numpy as np

from videos.stats.stats45.common import *  # noqa: F403


class CompleteClass(VoiceoverScene):
    def construct(self):
        self.card()
        self.bayes_admissible()
        self.traced()
        self.wald()
        self.limits()
        self.blyth()
        self.variance()

    def card(self):
        card = chapter_card(3, r"Complete class theorems", r"Which rules are worth considering?", lit=(1950,), part=PART)
        with self.voiceover("Chapter three. Complete class theorems: which rules are worth considering at all?"):
            self.play(FadeIn(card[0], shift=UP * 0.2), FadeIn(card[1]))
        self.play(FadeOut(card))

    def bayes_admissible(self):
        rows = [
            cmath(r"\delta_\pi", r":", r"\text{proper prior; finite Bayes risk; uniqueness under all model laws}", font_size=32),
            cmath(r"\text{if } \delta' \text{ dominates } \delta_\pi", r"\Rightarrow", r"r(\pi, \delta') \le r(\pi, \delta_\pi)", font_size=32),
            cmath(r"\Rightarrow", r"\;", r"\delta' \text{ is Bayes too, } \ \text{so } \delta' = \delta_\pi: \ \text{no strict domination}", font_size=30),
            cmath(r"\text{so}", r":", r"\text{unique Bayes rules are admissible}", font_size=34),
        ]
        rows[3][-1].set_color(ADMC)
        whys = [why(r"e.g.\ a posterior mean"), why(r"average the domination over $\pi$"), why(r"uniqueness"), why(r"one direction")]
        with self.voiceover(
            "<bookmark mark='a'/> First, the easy direction. Take a proper prior with finite Bayes risk and a Bayes "
            "rule unique up to sets null under every model law. This holds for the full-support finite example and "
            "for the Gaussian examples here. Posterior uniqueness only under the prior predictive law would not be "
            "sufficient in every statistical model. <bookmark mark='b'/> If some rule dominated it, then averaging "
            "its smaller-or-equal risk over the prior would give a Bayes risk no larger. <bookmark mark='c'/> So the "
            "dominating rule would also be Bayes, and by uniqueness it would be the same rule: there is no strict "
            "domination. <bookmark mark='d'/> Unique Bayes rules are admissible. The deeper question is the converse:"
            " is every admissible rule Bayes?"
        ) as vo:
            heading=label('Uniqueness under every model law makes a Bayes rule admissible',font_size=36).move_to([0,3.3,0])
            if heading.width>12.5: heading.width=12.5
            self.play(FadeIn(heading))
            step = ladder(self, rows, whys, keep=4, top=2.6, x=-0.9, buff=0.85, edge=6.9)
            for k, m_ in enumerate("abcd"):
                vo.wait_until(m_)
                step(k, transform=False)
        self.clear_scene()

    def traced(self):
        d = load("complete")
        dd = load("decision")
        A = axes([0, 1.05], [0, 2.1], x_length=6.6, y_length=5.0, xlabel=r"$R(\text{fair}, \delta)$", ylabel=r"$R(\text{biased}, \delta)$",
                 xticks=[0, 0.25, 0.5, 0.75, 1], yticks=[0, 0.5, 1, 1.5, 2], center=[-2.7, 0.0, 0])
        rs = RiskSet(A.ax, dd["R"])
        base = VGroup(rs.hull(MLEC, 0.15), rs.rule_dots(MLEC, radius=0.07))
        low = rs.lower(dd["lower"], ADMC, 6)
        pis = np.asarray(d["pis"])
        tr = np.asarray(d["traced"])
        marks = VGroup(*[Dot(A.ax.c2p(*t), radius=0.12, color=interpolate_color(ManimColor(BAYESC), ManimColor(MMC), q)) for t, q in zip(tr[::7], pis[::7])])
        side = fit_rows(VGroup(
            label(r"sweep the prior $\pi$ from 0 to 1", font_size=22),
            label(r"each supporting line touches the edge", font_size=22, color=BAYESC),
            label(r"corners: \ Bayes rules; \ edges: \ mixtures", font_size=22, color=ADMC),
            label(r"this finite randomized problem: Bayes rules form a complete class", font_size=22, color=S.ACCENT),
            label(r"the supporting-hyperplane theorem, \ in 2D", font_size=22, color=GREY_B),
        ), 4.4, 0.42, [4.4, 0.3, 0])
        with self.voiceover(
            "<bookmark mark='a'/> In the coin problem, sweep the prior from zero to one. <bookmark mark='b'/> Each "
            "prior's supporting line touches the lower edge somewhere, <bookmark mark='c'/> and as the prior moves, "
            "the touching points visit every corner; points between corners are mixtures of two Bayes rules, Bayes "
            "for the prior at which the line lies flat along that edge. So every admissible rule is Bayes. <bookmark "
            "mark='d'/> That is the finite randomized decision theorem for this compact risk polytope: the Bayes "
            "rules form a complete class, meaning that any rule outside it is dominated by one inside. <bookmark "
            "mark='e'/> The proof is the supporting-hyperplane theorem for convex sets, which this picture shows in "
            "two dimensions."
        ) as vo:
            self.play(FadeIn(A), FadeIn(base))
            vo.wait_until("a")
            self.play(FadeIn(side[0]))
            vo.wait_until("b")
            self.play(Create(low), FadeIn(side[1]))
            vo.wait_until("c")
            self.play(LaggedStart(*[FadeIn(m) for m in marks], lag_ratio=0.15), FadeIn(side[2]), run_time=2.5)
            vo.wait_until("d")
            self.play(FadeIn(side[3]))
            vo.wait_until("e")
            self.play(FadeIn(side[4]))
        self.clear_scene()

    def wald(self):
        rows = fit_rows(VGroup(
            label(r"infinitely many $\theta$: \ admissible rules need not be Bayes for any proper prior", font_size=26),
            label(r"Wald (1950), \ Le Cam (1955), \ Brown (1986): \ they are \emph{limits} of Bayes rules", font_size=26, color=BAYESC),
            label(r"generalized Bayes representations require model, loss and regularity conditions", font_size=26, color=ADMC),
            label(r"so the search for good rules is a search over priors", font_size=28, color=S.ACCENT),
        ), 12.4, 0.6, [0, 0, 0])
        with self.voiceover(
            "<bookmark mark='a'/> With infinitely many parameter values the converse fails as stated: there are "
            "admissible rules that are Bayes for no proper prior. <bookmark mark='b'/> Under the relevant "
            "compactness, continuity and loss assumptions, complete-class theorems of Wald, Le Cam and Brown "
            "represent admissible rules through suitable limits of Bayes rules. Mere pointwise convergence alone does"
            " not prove admissibility. <bookmark mark='c'/> In particular regular exponential-family decision "
            "problems, with the specified loss and complete-class conditions, one obtains generalized Bayes "
            "representations, possibly using improper priors. This is not a statement about every loss and "
            "exponential family. <bookmark mark='d'/> So the search for good rules becomes a search over priors, "
            "whether or not one believes in them. That is a frequentist argument for Bayesian methods."
        ) as vo:
            for k, m_ in enumerate("abcd"):
                vo.wait_until(m_)
                self.play(FadeIn(rows[k], shift=RIGHT * 0.2))
        self.clear_scene()

    def limits(self):
        d = load("complete")
        p = np.asarray(d["p"])
        A = axes([0, 1], [0, 0.03], x_length=7.4, y_length=4.4, xlabel=r"$p$", ylabel=r"risk",
                 xticks=[0, 0.25, 0.5, 0.75, 1], yticks=[0, 0.01, 0.02, 0.03], center=[-2.5, 0.2, 0])
        ax = A.ax
        mle = polyline(ax, p, d["mle"], MLEC, 5)
        cols = {"4.0": S.PRIOR, "1.0": BAYESC, "0.25": S.ALT, "0.05": MMC}
        cs = {k: polyline(ax, p, d["curves"][k], c, 3) for k, c in cols.items()}
        side = fit_rows(VGroup(
            label(r"$\mathrm{Beta}(\varepsilon, \varepsilon)$ prior: \ Bayes rule $(X + \varepsilon)/(n + 2\varepsilon)$", font_size=22),
            label(r"$\varepsilon = 4, \ 1, \ 0.25, \ 0.05$", font_size=22, color=BAYESC),
            label(r"blue: $X/n$, a limit of proper Beta posterior means", font_size=22, color=MLEC),
            label(r"Haldane: formal posterior only for $0<X<n$; endpoints by a limit", font_size=22, color=GREY_A),
            label(r"and it is admissible", font_size=22, color=ADMC),
        ), 4.6, 0.42, [4.45, 0.4, 0])
        with self.voiceover(
            "<bookmark mark='a'/> The binomial shows it. A Beta prior with both parameters equal to epsilon has Bayes"
            " rule X plus epsilon over n plus two epsilon. <bookmark mark='b'/> As epsilon shrinks from four to one, "
            "a quarter and a twentieth, the risk curves close in on one limit, <bookmark mark='c'/> the risk of the "
            "sample proportion, The sample proportion is not Bayes for a nondegenerate proper interior prior. Priors "
            "on the endpoints are an exception because the experiment then reveals the parameter. Unbiasedness alone "
            "is not a universal obstruction to every Bayes representation in all models. <bookmark mark='d'/> For "
            "interior counts it is the formal posterior mean under Haldane's improper prior. At zero or n heads that "
            "posterior is improper; the endpoint answers come from the limit of the proper Beta rules. <bookmark "
            "mark='e'/> And it is admissible, as a limit of Bayes rules whose risks converge fast enough."
        ) as vo:
            self.play(FadeIn(A), FadeIn(exact_tag(r"exact risk functions, \ $n = 16$")))
            vo.wait_until("a")
            self.play(FadeIn(side[0]))
            vo.wait_until("b")
            self.play(*[Create(cs[k]) for k in cols], FadeIn(side[1]), run_time=2.5)
            vo.wait_until("c")
            self.play(Create(mle), FadeIn(side[2]))
            vo.wait_until("d")
            self.play(FadeIn(side[3]))
            vo.wait_until("e")
            self.play(FadeIn(side[4]))
        self.clear_scene()

    def blyth(self):
        rows = [
            cmath(r"X \sim N(\theta, 1)", r",", r"\ \pi_\tau = N(0, \tau^2): \ \delta_\tau = \tfrac{\tau^2}{1 + \tau^2} X", font_size=32),
            cmath(r"r(\pi_\tau, X) - r(\pi_\tau, \delta_\tau)", r"=", r"1 - \tfrac{\tau^2}{1 + \tau^2} = \tfrac{1}{1 + \tau^2}", font_size=32),
            cmath(r"\text{if } \delta' \text{ beat } X \text{ by } \varepsilon \text{ near } 0", r"\Rightarrow", r"\text{a gain} \ge c\, \varepsilon / \tau \text{ in Bayes risk}", font_size=30),
            cmath(r"1/\tau \gg 1/(1 + \tau^2)", r"\Rightarrow", r"\text{contradiction: } X \text{ is admissible in 1D}", font_size=30),
        ]
        rows[3][-1].set_color(ADMC)
        whys = [why(r"normal priors, \ wider and wider"), why(r"the gap closes like $1/\tau^2$"), why(r"the prior's mass near 0: \ $\sim 1/\tau$"), why(r"Blyth (1951)")]
        with self.voiceover(
            "<bookmark mark='a'/> Colin Blyth's 1951 method makes the limit argument precise. Observe one normal with"
            " mean theta, and use normal priors with variance tau squared; the Bayes rule shrinks X by tau squared "
            "over one plus tau squared. <bookmark mark='b'/> The Bayes risk of X itself exceeds the Bayes rule's by "
            "one over one plus tau squared: the gap closes like one over tau squared. <bookmark mark='c'/> Suppose a "
            "dominating finite-risk rule improved by epsilon near some fixed parameter value. Continuity of its "
            "normal-model risk provides an interval of strict improvement, not necessarily around zero. A normal "
            "prior of width tau puts mass of order one over tau there, so the rival would gain at least a constant "
            "times epsilon over tau in Bayes risk. <bookmark mark='d'/> For large tau that gain is larger than the "
            "whole gap, which is impossible. So X is admissible in one dimension. Chapter eleven will show that the "
            "same race between gap and mass is lost in three."
        ) as vo:
            heading=label('Blyth compares a Bayes-risk gap with local prior mass',font_size=36).move_to([0,3.3,0])
            if heading.width>12.5: heading.width=12.5
            self.play(FadeIn(heading))
            step = ladder(self, rows, whys, keep=4, top=2.6, x=-0.9, buff=0.85, edge=6.9)
            for k, m_ in enumerate("abcd"):
                vo.wait_until(m_)
                step(k, transform=False)
        self.clear_scene()

    def variance(self):
        d = load("complete")
        c = np.asarray(d["c"])
        n = d["n2"]
        A = axes([0.04, 0.14], [0.15, 0.42], x_length=7.4, y_length=4.4, xlabel=r"$c$ in $c \sum (x_i - \bar x)^2$", ylabel=r"MSE $/\, \sigma^4$",
                 xticks=[0.05, 0.075, 0.1, 0.125], yticks=[0.2, 0.3, 0.4], xfmt=lambda v: f"{v:.3f}", center=[-2.5, 0.2, 0])
        ax = A.ax
        cur = polyline(ax, c, d["scale"], MLEC, 4)
        pts = VGroup(*[Dot(ax.c2p(cc, v), radius=0.11, color=col) for cc, v, col in
                       ((1 / (n - 1), d["s_unbiased"], INADC), (1 / n, d["s_mle"], BAYESC), (1 / (n + 1), d["s_best"], ADMC))])
        side = fit_rows(VGroup(
            label(rf"$n = {n}$ normal observations, \ estimate $\sigma^2$", font_size=22),
            label(rf"red: \ unbiased, \ $c = 1/(n - 1)$: \ {d['s_unbiased']:.3f}", font_size=22, color=INADC),
            label(rf"orange: \ the MLE, \ $c = 1/n$: \ {d['s_mle']:.3f}", font_size=22, color=BAYESC),
            label(rf"green: \ $c = 1/(n + 1)$: \ {d['s_best']:.3f}, \ for every $\sigma$", font_size=22, color=ADMC),
            label(r"$s^2$ inadmissible; \ so is $c = \tfrac{1}{n+1}$ \ (Stein 1964)", font_size=22, color=S.ACCENT),
        ), 4.6, 0.42, [4.45, 0.4, 0])
        with self.voiceover(
            f"<bookmark mark='a'/> Admissibility can embarrass familiar estimators. Estimate a normal variance from ten "
            f"observations by a constant times the sum of squared deviations, and plot the mean squared error, in units of "
            f"sigma to the fourth, against the constant. <bookmark mark='b'/> The unbiased choice, one over n minus one, "
            f"scores {say(d['s_unbiased'], 3)}; <bookmark mark='c'/> the MLE, one over n, {say(d['s_mle'], 2)}; <bookmark "
            f"mark='d'/> and one over n plus one, {say(d['s_best'], 3)}, the minimum, at every value of sigma, because all "
            f"three risks are proportional to sigma to the fourth. <bookmark mark='e'/> So the unbiased sample variance is "
            f"inadmissible under squared error. And in 1964 Stein showed that even the best of these is inadmissible "
            f"when the mean is unknown: using the sample mean's size as well does slightly better."
        ) as vo:
            self.play(FadeIn(A), FadeIn(exact_tag(r"exact: \ $\chi^2_{n-1}$ moments")))
            vo.wait_until("a")
            self.play(Create(cur), FadeIn(side[0]))
            vo.wait_until("b")
            self.play(FadeIn(pts[0]), FadeIn(side[1]))
            vo.wait_until("c")
            self.play(FadeIn(pts[1]), FadeIn(side[2]))
            vo.wait_until("d")
            self.play(FadeIn(pts[2]), FadeIn(side[3]))
            vo.wait_until("e")
            self.play(FadeIn(side[4]))
        self.clear_scene()

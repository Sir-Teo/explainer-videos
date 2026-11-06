from __future__ import annotations

import numpy as np

from videos.stats.stats45.common import *  # noqa: F403


class EmpiricalBayes(VoiceoverScene):
    def construct(self):
        self.card()
        self.robbins()
        self.table()
        self.chart()
        self.npmle()
        self.regret()
        self.modeling()

    def card(self):
        card = chapter_card(13, r"Empirical Bayes theory", r"Learning the prior from many problems at once", lit=(1956,), part=PART)
        with self.voiceover("Chapter thirteen. Empirical Bayes theory: learning the prior from many problems at once."):
            self.play(FadeIn(card[0], shift=UP * 0.2), FadeIn(card[1]))
        self.play(FadeOut(card))

    def robbins(self):
        rows = [
            cmath(r"x_i \mid \theta_i \sim \text{Poisson}(\theta_i)", r",", r"\ \theta_i \sim g \ \text{unknown}", font_size=34),
            cmath(r"E[\theta \mid x]", r"=", r"\frac{\int \theta\, e^{-\theta}\theta^x / x!\ g(d\theta)}{\int e^{-\theta}\theta^x / x!\ g(d\theta)}", font_size=34),
            cmath(r"\phantom{E}", r"=", r"(x + 1)\, \frac{f(x + 1)}{f(x)}, \ \ f = \text{the marginal of } x", font_size=34),
            cmath(r"\hat E[\theta \mid x]", r"=", r"(x + 1)\, \frac{\#\{x_i = x + 1\}}{\#\{x_i = x\}}", font_size=34),
        ]
        rows[2][-1].set_color(S.ACCENT)
        rows[3][-1].set_color(BAYESC)
        whys = [why(r"many units, \ one prior"), why(r"the Bayes rule, \ if $g$ were known"), why(r"$\theta^{x+1}/x! = (x + 1)\,\theta^{x+1}/(x+1)!$"), why(r"Robbins (1956)")]
        with self.voiceover(
            "<bookmark mark='a'/> Herbert Robbins's idea of 1956. Many units each have a Poisson count with its own rate, "
            "and the rates come from an unknown distribution g. <bookmark mark='b'/> If g were known, the Bayes rule for a "
            "unit with count x would be this ratio of integrals. <bookmark mark='c'/> But theta times theta to the x over x "
            "factorial is x plus one times theta to the x plus one over x plus one factorial, so the ratio is x plus one "
            "times the marginal probability of x plus one over that of x. <bookmark mark='d'/> Those marginal probabilities "
            "can be estimated by counting: the Bayes rule can be estimated without ever estimating the prior. Jerzy "
            "Neyman later called it a breakthrough in the theory of statistical decision making."
        ) as vo:
            step = ladder(self, rows, whys, keep=4, top=2.6, x=-0.9, buff=0.85, edge=6.9)
            for k, m_ in enumerate("abcd"):
                vo.wait_until(m_)
                step(k, transform=False)
        self.clear_scene()

    def table(self):
        d = load("eb")
        c = d["counts"]
        fmt = lambda v: "---" if v is None else f"{v:.3f}"  # noqa: E731
        rows = [[r"claims $x$"] + [str(i) for i in range(7)],
                [r"policies"] + [f"{int(v):,}" for v in c[:7]],
                [r"Robbins"] + [fmt(v) for v in d["robbins"][:7]],
                [r"gamma prior"] + [fmt(v) for v in d["gamma"][:7]],
                [r"NPMLE prior"] + [fmt(v) for v in d["npmle"][:7]]]
        tab = table_rows(rows, font_size=26, col_buff=0.5, row_buff=0.3, colors=[GREY_A, None, INADC, MMC, JSC]).move_to([0, 0.6, 0])
        if tab.width > 13:
            tab.width = 13
        note_ = label(rf"{d['total']:,} policies, \ one year; \ the estimated claim rate next year, \ given $x$ claims this year", font_size=24, color=GREY_A).move_to([0, -2.4, 0])
        with self.voiceover(
            f"<bookmark mark='a'/> Efron and Hastie's example: {d['total']:,} automobile insurance policies, and how many "
            f"claims each made in one year. <bookmark mark='b'/> Robbins's formula estimates next year's claim rate for a "
            f"policy with x claims this year: {say(d['robbins'][0], 3)} for a policy with none, {say(d['robbins'][1], 3)} for "
            f"one claim, {say(d['robbins'][2], 3)} for two. Far below the raw counts: most policies with a claim were merely "
            f"unlucky. <bookmark mark='c'/> But it rests on small counts in the tail: with five claims it says six, with six "
            f"it says {say(d['robbins'][6], 2)}. <bookmark mark='d'/> Fitting a gamma prior, the negative binomial, smooths "
            f"it into a straight line. <bookmark mark='e'/> And the nonparametric maximum likelihood prior gives a smooth, "
            f"increasing rule that makes no shape assumption."
        ) as vo:
            vo.wait_until("a")
            self.play(FadeIn(tab[0]), FadeIn(tab[1]), FadeIn(note_), FadeIn(museum_tag(r"Efron \& Hastie (2016), \ Table 6.1")))
            vo.wait_until("b")
            self.play(FadeIn(tab[2]))
            vo.wait_until("c")
            self.play(Indicate(VGroup(tab[2][-2], tab[2][-1]), color=INADC))
            vo.wait_until("d")
            self.play(FadeIn(tab[3]))
            vo.wait_until("e")
            self.play(FadeIn(tab[4]))
        self.clear_scene()

    def chart(self):
        d = load("eb")
        x = np.arange(7)
        A = axes([-0.3, 6.3], [0, 6.5], x_length=7.4, y_length=4.4, xlabel=r"claims this year, \ $x$", ylabel=r"$\hat E[\theta \mid x]$",
                 xticks=[0, 1, 2, 3, 4, 5, 6], yticks=[0, 2, 4, 6], center=[-2.5, 0.2, 0])
        ax = A.ax
        raw = polyline(ax, x, x, GREY_B, 2)
        rob = VGroup(polyline(ax, x, d["robbins"][:7], INADC, 3), *[Dot(ax.c2p(a, b), radius=0.08, color=INADC) for a, b in zip(x, d["robbins"][:7])])
        gam = polyline(ax, x, d["gamma"][:7], MMC, 4)
        npm = VGroup(polyline(ax, x, d["npmle"][:7], JSC, 4), *[Dot(ax.c2p(a, b), radius=0.08, color=JSC) for a, b in zip(x, d["npmle"][:7])])
        side = fit_rows(VGroup(
            label(r"grey: \ the raw count, \ $\hat\theta = x$", font_size=22, color=GREY_B),
            label(r"red: \ Robbins, \ unbiased but jumpy in the tail", font_size=22, color=INADC),
            label(rf"gold: \ gamma prior, \ shape {d['nu']:.2f}, \ scale {d['scale']:.2f}", font_size=22, color=MMC),
            label(r"green: \ NPMLE: \ monotone, \ no shape assumed", font_size=22, color=JSC),
            label(rf"log-likelihoods: \ gamma {d['loglik_gamma']:,.1f}, \ NPMLE {d['loglik_npmle']:,.1f}", font_size=22, color=GREY_A),
        ), 4.6, 0.42, [4.45, 0.4, 0])
        with self.voiceover(
            f"<bookmark mark='a'/> The same rules as curves. The grey diagonal is the raw count. <bookmark mark='b'/> "
            f"Robbins's estimates in red follow a smooth path for small counts and then jump around where there are only a "
            f"handful of policies. <bookmark mark='c'/> The gamma prior's rule is linear in x, the familiar credibility "
            f"formula of actuaries. <bookmark mark='d'/> The NPMLE's rule bends: it shrinks hard for small counts and less "
            f"for large ones, and it is increasing, as any Bayes rule for a Poisson mean must be. <bookmark mark='e'/> It "
            f"also fits the counts better than the gamma prior, by about seven units of log-likelihood."
        ) as vo:
            self.play(FadeIn(A), Create(raw), FadeIn(museum_tag(r"Efron \& Hastie (2016), \ Table 6.1")))
            vo.wait_until("a")
            self.play(FadeIn(side[0]))
            vo.wait_until("b")
            self.play(Create(rob), FadeIn(side[1]))
            vo.wait_until("c")
            self.play(Create(gam), FadeIn(side[2]))
            vo.wait_until("d")
            self.play(Create(npm), FadeIn(side[3]))
            vo.wait_until("e")
            self.play(FadeIn(side[4]))
        self.clear_scene()

    def npmle(self):
        rows = [
            cmath(r"\hat g", r"=", r"\arg\max_{g} \textstyle\sum_i \log \int p(x_i \mid \theta)\, g(d\theta)", font_size=34),
            cmath(r"\text{concave in } g", r":", r"\text{a convex problem over all distributions}", font_size=32),
            cmath(r"\hat g", r":", r"\text{discrete, \ with at most } \#\{\text{distinct } x_i\} \text{ atoms}", font_size=32),
            cmath(r"\text{algorithms}", r":", r"\text{EM on a grid; \ interior point (Koenker \& Mizera 2014)}", font_size=30),
        ]
        rows[0][-1].set_color(JSC)
        rows[2][-1].set_color(S.ACCENT)
        whys = [why(r"Kiefer \& Wolfowitz (1956)"), why(r"linear in $g$, \ then log"), why(r"Lindsay (1983)"), why(r"\texttt{statkit} uses EM")]
        with self.voiceover(
            "<bookmark mark='a'/> The nonparametric maximum likelihood estimate of the prior, due to Jack Kiefer and Jacob "
            "Wolfowitz in 1956, maximizes the marginal likelihood over all distributions. <bookmark mark='b'/> The marginal "
            "is linear in g, so the log-likelihood is concave and the problem is convex, with no tuning parameter at all. "
            "<bookmark mark='c'/> Bruce Lindsay showed in 1983 that the maximizer is discrete, with no more atoms than there "
            "are distinct observations. <bookmark mark='d'/> It can be computed by EM on a fine grid, as statkit does, or "
            "much faster by the interior-point methods of Roger Koenker and Ivan Mizera."
        ) as vo:
            step = ladder(self, rows, whys, keep=4, top=2.6, x=-0.9, buff=0.85, edge=6.9)
            for k, m_ in enumerate("abcd"):
                vo.wait_until(m_)
                step(k, transform=False)
        self.clear_scene()

    def regret(self):
        d = load("eb")["regret"]
        n = np.asarray(d["n"], float)
        ln = np.log10(n)
        A = axes([1.5, 3.9], [0, 0.7], x_length=7.4, y_length=4.4, xlabel=r"number of means, \ $\log_{10} n$", ylabel=r"risk per coordinate",
                 xticks=[2, 3], yticks=[0, 0.2, 0.4, 0.6], center=[-2.5, 0.2, 0])
        ax = A.ax
        mk = lambda ys, c: VGroup(polyline(ax, ln, ys, c, 4), *[Dot(ax.c2p(a, b), radius=0.08, color=c) for a, b in zip(ln, ys)])  # noqa: E731
        js, npm, orc = mk(d["js"], MMC), mk(d["npmle"], JSC), mk(d["oracle"], BAYESC)
        side = fit_rows(VGroup(
            label(r"$\theta_i = 4$ w.p.\ 0.1, \ else 0; \ $x_i \sim N(\theta_i, 1)$", font_size=22),
            label(r"gold: \ James--Stein, \ about 0.59 at every $n$", font_size=22, color=MMC),
            label(r"orange: \ the oracle Bayes rule, \ knowing $g$", font_size=22, color=BAYESC),
            label(r"green: \ NPMLE + Tweedie \ (GMLEB)", font_size=22, color=JSC),
            label(r"its regret $\to 0$: \ it learns the prior", font_size=22, color=S.ACCENT),
        ), 4.6, 0.42, [4.45, 0.4, 0])
        with self.voiceover(
            f"<bookmark mark='a'/> Does learning the prior work as the number of problems grows? Take normal means that are "
            f"zero ninety percent of the time and four otherwise, a sparse prior that no normal prior describes. <bookmark "
            f"mark='b'/> James–Stein, which in effect fits a normal prior, has risk about point six per coordinate however "
            f"many means there are. <bookmark mark='c'/> The oracle Bayes rule, which knows the true prior, does much "
            f"better. <bookmark mark='d'/> The NPMLE plugged into Tweedie's formula, the general maximum likelihood empirical "
            f"Bayes rule of Wenhua Jiang and Cun-Hui Zhang, starts at twice the oracle's risk with fifty means <bookmark "
            f"mark='e'/> and closes the gap as n grows: its regret tends to zero, nearly at a parametric rate, as Jiang and "
            f"Zhang proved in 2009. With enough parallel problems, the frequentist can act as a Bayesian who knew the prior."
        ) as vo:
            self.play(FadeIn(A), FadeIn(exact_tag(r"simulated: 4 to 12 replications per $n$")))
            vo.wait_until("a")
            self.play(FadeIn(side[0]))
            vo.wait_until("b")
            self.play(Create(js), FadeIn(side[1]))
            vo.wait_until("c")
            self.play(Create(orc), FadeIn(side[2]))
            vo.wait_until("d")
            self.play(Create(npm), FadeIn(side[3]))
            vo.wait_until("e")
            self.play(FadeIn(side[4]))
        self.clear_scene()

    def modeling(self):
        rows = fit_rows(VGroup(
            label(r"$f$-modeling: \ estimate the marginal, \ plug into Robbins or Tweedie", font_size=26, color=INADC),
            label(r"$g$-modeling: \ estimate the prior, \ then compute its Bayes rule \ (Efron 2014)", font_size=26, color=JSC),
            label(r"James--Stein is $g$-modeling with a normal $g$: \ Efron \& Morris (1973)", font_size=26, color=MMC),
            label(r"Stein, \ Robbins and Wald, \ reconciled: \ frequentist risk, \ Bayesian form", font_size=26, color=S.ACCENT),
        ), 12.4, 0.6, [0, 0, 0])
        with self.voiceover(
            "<bookmark mark='a'/> Bradley Efron's 2014 survey sorts empirical Bayes methods into two kinds. f-modeling "
            "estimates the marginal density of the data and plugs it into Robbins's or Tweedie's formula. <bookmark "
            "mark='b'/> g-modeling estimates the prior itself and then computes its Bayes rule, which keeps the estimates "
            "coherent, monotone and inside the parameter space. <bookmark mark='c'/> James–Stein is g-modeling with a "
            "normal prior, as Efron and Morris showed in 1973. <bookmark mark='d'/> So the three threads of this part meet: "
            "Wald's frequentist risk as the criterion, Stein's shrinkage as the phenomenon, and Robbins's empirical Bayes as "
            "the method, all in Bayesian form."
        ) as vo:
            for k, m_ in enumerate("abcd"):
                vo.wait_until(m_)
                self.play(FadeIn(rows[k], shift=RIGHT * 0.2))
        self.clear_scene()

from __future__ import annotations

import numpy as np

from videos.stats.stats53.common import *  # noqa: F403


class Dirichlet(VoiceoverScene):
    def construct(self):
        self.card()
        self.definition()
        self.newcomb()
        self.urn()
        self.bootstrap()
        self.mixture()
        self.faithful()
        self.polya()
        self.pitman()

    def card(self):
        card = chapter_card(6, r"Dirichlet processes and Pólya trees", r"Priors on distributions", lit=(1973,), part=PART)
        with self.voiceover("Chapter six. Dirichlet processes and Pólya trees: priors on distributions."):
            self.play(FadeIn(card[0], shift=UP * 0.2), FadeIn(card[1]))
        self.play(FadeOut(card))

    def definition(self):
        rows = [
            cmath(r"F \sim \mathrm{DP}(\alpha, G_0)", r":", r"(F(A_1), \dots, F(A_k)) \sim \mathrm{Dir}(\alpha G_0(A_1), \dots, \alpha G_0(A_k))", font_size=30),
            cmath(r"\text{conjugate}", r":", r"F \mid X_{1:n} \sim \mathrm{DP}\big(\alpha + n, \ \tfrac{\alpha G_0 + n\mathbb F_n}{\alpha + n}\big)", font_size=32),
            cmath(r"E[F(x) \mid X]", r"=", r"\tfrac{\alpha}{\alpha + n}G_0(x) + \tfrac{n}{\alpha + n}\mathbb F_n(x): \ \text{a shrunken ECDF}", font_size=32),
            cmath(r"\text{draws}", r":", r"\text{discrete, \ almost surely: \ } F = \textstyle\sum_k w_k\delta_{\phi_k}", font_size=32),
        ]
        rows[1][-1].set_color(POSTC)
        rows[3][-1].set_color(BADC)
        whys = [why(r"Ferguson (1973)"), why(r"the posterior is a DP"), why(r"$\alpha$ = prior sample size"), why(r"Sethuraman's sticks (1994)")]
        with self.voiceover(
            "<bookmark mark='a'/> Thomas Ferguson's Dirichlet process of 1973 is a prior on probability distributions. A "
            "random distribution F has it if, for every partition of the space, the probabilities F gives the pieces are "
            "Dirichlet, with parameters alpha times the base measure's probabilities. <bookmark mark='b'/> It is conjugate: "
            "after n observations the posterior is again a Dirichlet process, with concentration alpha plus n and a base "
            "measure mixing the prior guess with the empirical distribution. <bookmark mark='c'/> So the posterior mean CDF is "
            "the empirical CDF shrunk towards the prior guess, with alpha acting as a prior sample size. <bookmark mark='d'/> "
            "But its draws are discrete, almost surely: infinitely many atoms with weights given by Jayaram Sethuraman's "
            "stick-breaking. That is why it cannot serve directly as a prior for densities."
        ) as vo:
            step = ladder(self, rows, whys, keep=4, top=2.6, x=-0.9, buff=0.85, edge=6.9)
            for k, m_ in enumerate("abcd"):
                vo.wait_until(m_)
                step(k, transform=False)
        self.clear_scene()

    def newcomb(self):
        d = load("dp")
        g = np.asarray(d["grid"])
        A = axes([-46, 42], [0, 1.02], x_length=7.4, y_length=4.4, xlabel=r"Newcomb's passage times (deviation from 24,800 ns)", ylabel=r"$F(x)$",
                 xticks=[-40, -20, 0, 20, 40], yticks=[0, 0.25, 0.5, 0.75, 1], center=[-2.5, 0.2, 0])
        ax = A.ax
        x = np.sort(d["x"])
        ecdf = VGroup(*[Line(ax.c2p(x[i], (i + 1) / len(x)), ax.c2p(x[i + 1] if i + 1 < len(x) else 42, (i + 1) / len(x)), color=GREY_B, stroke_width=2)
                        for i in range(len(x))])
        mean = polyline(ax, g, d["H"], POSTC, 4)
        poly = Polygon(*[ax.c2p(a, b) for a, b in zip(g, d["lo"])], *[ax.c2p(a, b) for a, b in zip(g[::-1], np.asarray(d["hi"])[::-1])],
                       fill_color=BALLC, fill_opacity=0.25, stroke_width=0)
        side = fit_rows(VGroup(
            label(rf"Newcomb's 66 measurements of the speed of light (1882)", font_size=22),
            label(r"grey: \ the empirical CDF, \ two outliers at $-44$ and $-2$", font_size=22, color=GREY_B),
            label(r"blue: \ the DP posterior mean, \ $\alpha = 1$, \ a wide normal $G_0$", font_size=22, color=POSTC),
            label(r"gold: \ pointwise 95\% credible band, \ Beta marginals", font_size=22, color=BALLC),
            label(r"with $\alpha = 1$, \ the data are 98.5\% of the answer", font_size=22, color=GOODC),
        ), 4.6, 0.42, [4.45, 0.4, 0])
        with self.voiceover(
            "<bookmark mark='a'/> Real data: Simon Newcomb's sixty-six measurements of the time light took to travel about "
            "seven kilometres, from 1882, which Part thirty used for robustness. <bookmark mark='b'/> The empirical CDF in grey, "
            "with its two famous low outliers. <bookmark mark='c'/> The Dirichlet-process posterior mean, with concentration "
            "one and a wide normal prior guess, is almost exactly the empirical CDF. <bookmark mark='d'/> Its pointwise "
            "credible band, from the Beta distribution of each F of x, is the Bayesian bootstrap's band, close to the "
            "frequentist one. <bookmark mark='e'/> With alpha equal to one, the prior counts as a single observation, and the "
            "data are ninety-eight and a half percent of the answer."
        ) as vo:
            self.play(FadeIn(A), FadeIn(museum_tag(r"Newcomb (1891); \ Stigler (1977)")))
            vo.wait_until("a")
            self.play(FadeIn(side[0]))
            vo.wait_until("b")
            self.play(FadeIn(ecdf), FadeIn(side[1]))
            vo.wait_until("c")
            self.play(Create(mean), FadeIn(side[2]))
            vo.wait_until("d")
            self.play(FadeIn(poly), FadeIn(side[3]))
            vo.wait_until("e")
            self.play(FadeIn(side[4]))
        self.clear_scene()

    def urn(self):
        d = load("dp")
        rows = [[r"concentration $\alpha$", r"tables, \ $n = 10$", r"$n = 100$", r"$n = 1{,}000$", r"expected at 1,000"]]
        for a in ("1.0", "5.0", "25.0"):
            rows.append([a.rstrip("0").rstrip("."), *[str(v) for v in d["tables"][a]], f"{d['tables_exp'][a][-1]:.1f}"])
        tab = table_rows(rows, font_size=28, col_buff=0.7, row_buff=0.45, colors=[GREY_B, POSTC, POSTC, POSTC])
        tab.move_to([0, 0.9, 0])
        foot = label(r"the Chinese restaurant: \ join a table with probability $\propto$ its size, \ a new one $\propto \alpha$", font_size=24, color=GREY_A).move_to([0, -1.0, 0])
        foot2 = label(r"the number of distinct values grows like $\alpha\log(1 + n/\alpha)$: \ ties, \ always", font_size=24, color=BADC).move_to([0, -1.8, 0])
        with self.voiceover(
            "<bookmark mark='a'/> The discreteness, seen through the Blackwell–MacQueen urn of Part twenty-six's Chinese "
            "restaurant: each new draw repeats an old value with probability proportional to its count, or makes a new one "
            "with probability proportional to alpha. <bookmark mark='b'/> With alpha one, a thousand draws take only about "
            f"{d['tables']['1.0'][-1]} distinct values. <bookmark mark='c'/> The number grows only like alpha times the log of "
            "n: a sample from a Dirichlet-process draw always has ties, which continuous data never do."
        ) as vo:
            vo.wait_until("a")
            self.play(FadeIn(tab), FadeIn(simulated_tag(r"simulated; \ expectations exact")))
            vo.wait_until("b")
            self.play(FadeIn(foot))
            vo.wait_until("c")
            self.play(FadeIn(foot2))
        self.clear_scene()

    def bootstrap(self):
        rows = [
            cmath(r"\alpha \to 0", r":", r"F \mid X \sim \mathrm{DP}(n, \mathbb F_n): \ \text{weights } (w_1, \dots, w_n) \sim \mathrm{Dir}(1, \dots, 1)", font_size=30),
            cmath(r"\text{the Bayesian bootstrap}", r":", r"\text{reweight the data at random, \ recompute the statistic}", font_size=32),
            cmath(r"\text{vs Efron's}", r":", r"\text{multinomial counts replaced by smooth Dirichlet weights}", font_size=32),
            cmath(r"\text{BvM for it}", r":", r"\text{the same first-order behaviour as the bootstrap of Part 16}", font_size=32),
        ]
        rows[1][-1].set_color(GOODC)
        whys = [why(r"the noninformative limit"), why(r"Rubin (1981)"), why(r"Part 16"), why(r"Lo (1987)")]
        with self.voiceover(
            "<bookmark mark='a'/> In the limit alpha to zero the prior guess disappears, and the posterior is a Dirichlet process on the observed points alone: random weights on the data with a flat Dirichlet distribution. <bookmark mark='b'/> This is Donald Rubin's Bayesian bootstrap of 1981: reweight the observations at random and recompute the statistic. <bookmark mark='c'/> It differs from Efron's bootstrap of Part sixteen only in replacing the multinomial resampling counts with smooth Dirichlet weights. <bookmark mark='d'/> Albert Lo showed in 1987 that the two agree to first order, a Bernstein–von Mises theorem for the bootstrap, and a reason the frequentist bootstrap has a Bayesian reading."
        ) as vo:
            step = ladder(self, rows, whys, keep=4, top=2.6, x=-0.9, buff=0.85, edge=6.9)
            for k, m_ in enumerate("abcd"):
                vo.wait_until(m_)
                step(k, transform=False)
        self.clear_scene()

    def mixture(self):
        rows = [
            cmath(r"p(x)", r"=", r"\int N(x; \mu, \sigma^2)\, dF(\mu, \sigma^2), \ \ F \sim \mathrm{DP}(\alpha, G_0)", font_size=32),
            cmath(r"\text{a density}", r":", r"\text{smooth the discrete } F \text{ with a kernel}", font_size=34),
            cmath(r"\text{KL support}", r":", r"\text{at most smooth densities \ (Ghosal, \ Ghosh \& Ramamoorthi 1999)}", font_size=30),
            cmath(r"\text{computation}", r":", r"\text{collapsed Gibbs: \ reassign each point to a cluster (Neal 2000)}", font_size=30),
        ]
        rows[2][-1].set_color(GOODC)
        whys = [why(r"Lo (1984)"), why(r"a mixture of normals"), why(r"Schwartz's first condition"), why(r"Algorithm 3")]
        with self.voiceover(
            "<bookmark mark='a'/> The repair is to smooth the discreteness away. Albert Lo's Dirichlet-process mixture of "
            "1984 draws a discrete distribution of normal components, and mixes the normal densities over it. <bookmark "
            "mark='b'/> The result is a random smooth density. <bookmark mark='c'/> It has Kullback–Leibler support at most "
            "smooth densities, so by Schwartz's theorem the posterior is consistent there. <bookmark mark='d'/> And it is "
            "computable: Radford Neal's collapsed Gibbs sampler of 2000 reassigns each observation in turn to an existing "
            "cluster or a new one, with the cluster parameters integrated out."
        ) as vo:
            step = ladder(self, rows, whys, keep=4, top=2.6, x=-0.9, buff=0.85, edge=6.9)
            for k, m_ in enumerate("abcd"):
                vo.wait_until(m_)
                step(k, transform=False)
        self.clear_scene()

    def faithful(self):
        d = load("dp")
        A = axes([1.0, 6.0], [0, 1.15], x_length=7.4, y_length=4.4, xlabel=r"Old Faithful: \ eruption length (minutes)", ylabel=r"density",
                 xticks=[1, 2, 3, 4, 5, 6], yticks=[0, 0.25, 0.5, 0.75, 1], center=[-2.5, 0.2, 0])
        ax = A.ax
        bars = hist_bars(ax, d["f_edges"], d["f_hist"], color=GREY_B, opacity=0.35)
        dens = polyline(ax, d["faithful_grid"], d["faithful_density"], POSTC, 4)
        kc = np.asarray(d["k_counts"], float)
        kc = kc / kc.sum()
        mode = int(np.argmax(kc))
        side = fit_rows(VGroup(
            label(r"272 eruptions; \ a DP mixture of normals, \ $\alpha = 1$", font_size=22),
            label(r"blue: \ the posterior mean density, \ 500 Gibbs sweeps", font_size=22, color=POSTC),
            label(rf"clusters used: \ mean {d['k_mean']:.1f}, \ mode {mode}", font_size=22, color=BALLC),
            label(r"two humps, \ but five or six clusters: \ the DP overclusters", font_size=22, color=BADC),
            label(r"the density is consistent; \ the number of clusters is not", font_size=22, color=GOODC),
        ), 4.6, 0.42, [4.45, 0.4, 0])
        with self.voiceover(
            f"<bookmark mark='a'/> Old Faithful's two hundred and seventy-two eruption lengths, last seen in Part twenty-nine. "
            f"<bookmark mark='b'/> The posterior mean density from five hundred sweeps of the sampler traces both humps. "
            f"<bookmark mark='c'/> But the number of clusters it uses averages {say(d['k_mean'], 1)}, most often {mode}. "
            f"<bookmark mark='d'/> The data have two humps, and the model insists on five or six components, splitting each "
            f"hump into pieces. <bookmark mark='e'/> This is no accident: Jeffrey Miller and Matthew Harrison proved in 2014 "
            f"that the Dirichlet-process mixture's posterior on the number of clusters is inconsistent, even though its "
            f"density estimate is consistent. Use it for densities, not for counting components."
        ) as vo:
            self.play(FadeIn(A), FadeIn(bars), FadeIn(museum_tag(r"Härdle (1991); \ Azzalini \& Bowman (1990)")))
            vo.wait_until("a")
            self.play(FadeIn(side[0]))
            vo.wait_until("b")
            self.play(Create(dens), FadeIn(side[1]))
            vo.wait_until("c")
            self.play(FadeIn(side[2]))
            vo.wait_until("d")
            self.play(FadeIn(side[3]))
            vo.wait_until("e")
            self.play(FadeIn(side[4]))
        self.clear_scene()

    def pitman(self):
        rows = [
            cmath(r"\text{Pitman--Yor}", r":", r"\text{a discount } d \in [0, 1): \ \text{new tables} \propto \alpha + d\,K", font_size=34),
            cmath(r"\text{tables}", r"\asymp", r"n^{d}: \ \text{power laws, \ not logarithms}", font_size=34),
            cmath(r"\text{word frequencies, \ species}", r":", r"\text{Zipf's law, \ heavy-tailed abundances}", font_size=32),
            cmath(r"\text{species sampling}", r":", r"\text{how many unseen species? \ Good--Turing, \ Bayesian}", font_size=32),
        ]
        rows[1][-1].set_color(GOODC)
        whys = [why(r"Pitman \& Yor (1997)"), why(r"vs \ DP's $\alpha\log n$"), why(r"language models' ancestors"), why(r"Lijoi, \ Mena \& Prünster (2007)")]
        with self.voiceover(
            "<bookmark mark='a'/> The Dirichlet process has a two-parameter generalization, Jim Pitman and Marc Yor's process of 1997, with a discount d that makes new tables more likely the more tables there already are. <bookmark mark='b'/> Its number of distinct values grows like a power of n rather than a logarithm. <bookmark mark='c'/> That matches the power laws of word frequencies and species abundances, which is why it was used for language models before neural networks. <bookmark mark='d'/> And it answers species-sampling questions, how many species have not yet been seen, the Bayesian cousin of Good and Turing's estimator from Bletchley Park."
        ) as vo:
            step = ladder(self, rows, whys, keep=4, top=2.6, x=-0.9, buff=0.85, edge=6.9)
            for k, m_ in enumerate("abcd"):
                vo.wait_until(m_)
                step(k, transform=False)
        self.clear_scene()

    def polya(self):
        rows = fit_rows(VGroup(
            label(r"Pólya trees: \ the other classical prior on distributions", font_size=28, color=GREY_A),
            label(r"split $[0, 1]$ dyadically; \ send mass left with a Beta$(a_j, a_j)$ fraction at level $j$", font_size=26, color=PRIORC),
            label(r"$a_j = j^2$ or faster: \ the draws have densities, \ almost surely", font_size=26, color=GOODC),
            label(r"conjugate, \ like the DP: \ the posterior just counts points in each piece", font_size=26, color=POSTC),
            label(r"but its densities jump at the dyadic points: \ the partition shows", font_size=26, color=BADC),
        ), 12.4, 0.55, [0, 0, 0])
        with self.voiceover(
            "<bookmark mark='a'/> The other classical prior on distributions is the Pólya tree, studied by Michael Lavine in "
            "1992 and Mauldin, Sudderth and Williams. <bookmark mark='b'/> Split the interval in half, again and again, and at "
            "each split send a Beta-distributed fraction of the mass to the left. <bookmark mark='c'/> If the Beta "
            "parameters grow fast enough with the level, like the square of the level, the random distribution has a density "
            "almost surely, unlike the Dirichlet process. <bookmark mark='d'/> It is conjugate too: the posterior just adds "
            "the counts of points in each piece to the Beta parameters. <bookmark mark='e'/> Its weakness is that its "
            "densities jump at the dyadic split points, so the partition shows through."
        ) as vo:
            for k, m_ in enumerate("abcde"):
                vo.wait_until(m_)
                self.play(FadeIn(rows[k], shift=RIGHT * 0.2))
        self.clear_scene()

from __future__ import annotations

import numpy as np

from videos.stats.stats24.common import *  # noqa: F403


class Counts(VoiceoverScene):
    def construct(self):
        self.card()
        self.negbin()
        self.offsets()
        self.histogram()
        self.zeros()
        self.compare()
        self.ppml()
        self.truth()

    def card(self):
        card = chapter_card(8, r"Counts", r"Overdispersion and too many zeros", lit=(1992,), part=PART)
        with self.voiceover("Chapter eight. Counts: overdispersion and too many zeros."):
            self.play(FadeIn(card[0], shift=UP * 0.2), FadeIn(card[1]))
        self.play(FadeOut(card))

    def negbin(self):
        rows = [
            cmath(r"y \mid \lambda", r"\sim", r"\text{Poisson}(\lambda), \ \ \lambda = \mu\,\varepsilon, \ \ \varepsilon \sim \text{Gamma}(k, k)", font_size=28),
            cmath(r"y", r"\sim", r"\text{NB}(\mu, k): \ \mathrm{Var} = \mu + \mu^2/k", font_size=30),
            cmath(r"k \to \infty", r":", r"\text{the Poisson}", font_size=30),
            cmath(r"\text{fit}", r":", r"\text{IRLS for } \beta \text{ given } k, \ \text{Newton for } k, \ \text{alternate}", font_size=28),
        ]
        rows[1][2].set_color(NBC)
        whys = [why(r"each person's own rate, \ gamma-distributed"), why(r"Greenwood \& Yule (1920): \ accident-proneness"),
                why(r"no heterogeneity left"), why(r"not quite a GLM: \ $k$ is in the variance")]
        with self.voiceover(
            "<bookmark mark='a'/> Where does overdispersion come from? Suppose each person has their own rate: the model's "
            "mean times a gamma-distributed frailty with mean one. Given the rate, the count is Poisson. "
            "<bookmark mark='b'/> Averaged over the frailty, the count is negative binomial, with variance mu plus mu "
            "squared over k. Major Greenwood and Udny Yule derived it in 1920 to describe accident-prone factory workers. "
            "<bookmark mark='c'/> As k grows the frailty disappears and the Poisson returns. <bookmark mark='d'/> With k "
            "fixed it's a generalized linear model; in practice we alternate IRLS for the coefficients with a Newton step for "
            "k."
        ) as vo:
            step = ladder(self, rows, whys, keep=4, top=2.6, x=-0.9, buff=0.85, edge=6.9)
            for k, m_ in enumerate("abcd"):
                vo.wait_until(m_)
                step(k, transform=False)
        self.clear_scene()

    def offsets(self):
        rows = [
            cmath(r"\text{counts over exposure } t_i", r":", r"E\,y_i = t_i\, e^{x_i^\top\beta}", font_size=30),
            cmath(r"\log E\,y_i", r"=", r"\log t_i + x_i^\top\beta", font_size=30),
            cmath(r"\log t_i", r":", r"\text{an offset: \ a column with coefficient fixed at } 1", font_size=30),
            cmath(r"e^{\beta_j}", r":", r"\text{a rate ratio}", font_size=30),
        ]
        rows[1][-1].set_color(MODEL)
        whys = [why(r"person-years, \ population, \ road length"), why(r"the log link turns rates into sums"), why(r"Part 14: \ Doll and Hill's doctors"), why(r"per unit of exposure")]
        with self.voiceover(
            "<bookmark mark='a'/> First, an essential tool for any count. Counts usually accumulate over some exposure: "
            "person-years of follow-up, a town's population, kilometres of road. The mean is the exposure times a rate. "
            "<bookmark mark='b'/> With a log link that becomes the log exposure plus the linear predictor. "
            "<bookmark mark='c'/> The log exposure enters as an offset, a column whose coefficient is fixed at one, as in Part "
            "14's study of smoking doctors. <bookmark mark='d'/> Every other coefficient then exponentiates to a rate ratio, "
            "per unit of exposure."
        ) as vo:
            step = ladder(self, rows, whys, keep=4, top=2.6, x=-0.9, buff=0.85, edge=6.9)
            for k, m_ in enumerate("abcd"):
                vo.wait_until(m_)
                step(k, transform=False)
        self.clear_scene()

    def histogram(self):
        d = load("visits")
        ks = np.asarray(d["ks"])[:13]
        obs = np.asarray(d["obs"])[:13]
        A = axes([-0.6, 12.6], [0, 0.45], x_length=8.0, y_length=4.4, xlabel=r"doctor visits last year",
                 ylabel=r"share of adults", xticks=[0, 2, 4, 6, 8, 10, 12], yticks=[0, 0.1, 0.2, 0.3, 0.4], center=[-1.6, 0.3, 0])
        ax = A.ax
        bars = bars_at(ax, ks, obs, 0.7, OBSC, 0.75)
        pois = VGroup(polyline(ax, ks, np.asarray(d["exp_p"])[:13], POIS, 3), *[Dot(ax.c2p(k, v), radius=0.06, color=POIS) for k, v in zip(ks, np.asarray(d["exp_p"])[:13])])
        nb = VGroup(polyline(ax, ks, np.asarray(d["exp_nb"])[:13], NBC, 3), *[Dot(ax.c2p(k, v), radius=0.06, color=NBC) for k, v in zip(ks, np.asarray(d["exp_nb"])[:13])])
        rows = fit_rows(VGroup(
            label(rf"{d['n']:,} adults: \ {100 * d['zeros']:.0f}\% saw no doctor", font_size=22, color=OBSC),
            label(rf"red: \ Poisson expects {100 * d['exp_p'][0]:.0f}\% zeros", font_size=22, color=POIS),
            label(r"too many 1s and 2s, \ too few 10s", font_size=22, color=GREY_A),
            label(rf"green: \ NB, \ $\hat k = {d['nb']['k']:.2f}$: \ {100 * d['exp_nb'][0]:.1f}\% zeros", font_size=22, color=NBC),
        ), 3.45, 0.42, [5.1, 0.3, 0])
        with self.voiceover(
            "<bookmark mark='a'/> The World's two thousand adults: forty percent saw no doctor last year. "
            "<bookmark mark='b'/> The Poisson regression, with all four covariates, expects only nineteen percent zeros. "
            "<bookmark mark='c'/> It also expects too many people with one or two visits and almost nobody with ten. "
            "<bookmark mark='d'/> The negative binomial, with k estimated at point eight two, expects thirty-nine percent "
            "zeros and matches the whole shape."
        ) as vo:
            self.add(simulated_tag())
            self.play(FadeIn(A), LaggedStart(*[GrowFromEdge(b, DOWN) for b in bars], lag_ratio=0.05))
            vo.wait_until("a")
            self.play(FadeIn(rows[0]))
            vo.wait_until("b")
            self.play(Create(pois), FadeIn(rows[1]))
            vo.wait_until("c")
            self.play(FadeIn(rows[2]))
            vo.wait_until("d")
            self.play(Create(nb), FadeIn(rows[3]))
        self.clear_scene()

    def zeros(self):
        rows = [
            cmath(r"\text{zero-inflated}", r":", r"P(y = 0) = \pi + (1 - \pi)e^{-\lambda}", font_size=30),
            cmath(r"\text{fit}", r":", r"\text{EM: \ is each zero structural?}", font_size=30),
            cmath(r"\text{hurdle}", r":", r"\text{logit for } y > 0; \ \text{truncated Poisson for how many}", font_size=28),
            cmath(r"\text{the difference}", r":", r"\text{two kinds of zero, \ or one gate}", font_size=30),
        ]
        rows[0][2].set_color(ZIPC)
        whys = [why(r"Lambert (1992): \ structural zeros plus Poisson"), why(r"Part 22, \ chapter eight"),
                why(r"Mullahy (1986)"), why(r"never-goers, \ or not this year")]
        with self.voiceover(
            "<bookmark mark='a'/> Excess zeros have a second explanation: some people never go. Diane Lambert's "
            "zero-inflated Poisson, from 1992, mixes a share pi of structural zeros with a Poisson for everyone else. "
            "<bookmark mark='b'/> It is fitted by Part 22's EM algorithm: the missing information is whether each zero is "
            "structural. <bookmark mark='c'/> John Mullahy's hurdle model instead separates the decision from the amount: a "
            "logistic regression for whether there are any visits, and a zero-truncated Poisson for how many. "
            "<bookmark mark='d'/> Zero inflation says there are two kinds of zero; a hurdle says there's one gate to pass."
        ) as vo:
            step = ladder(self, rows, whys, keep=4, top=2.6, x=-0.9, buff=0.85, edge=6.9)
            for k, m_ in enumerate("abcd"):
                vo.wait_until(m_)
                step(k, transform=False)
        self.clear_scene()

    def compare(self):
        d = load("visits")
        models = [(r"Poisson", d["poisson"]["ll"], 5, POIS), (r"zero-inflated Poisson", d["zip"]["ll"], 6, ZIPC),
                  (r"Poisson hurdle", d["hurdle"]["ll"], 10, PATH), (r"negative binomial", d["nb"]["ll"], 6, NBC)]
        hdr = [r"\textbf{model}", r"\textbf{log likelihood}", r"\textbf{parameters}", r"\textbf{AIC}"]
        body = [[m, f"{ll:,.0f}", f"{p}", f"{-2 * ll + 2 * p:,.0f}"] for m, ll, p, _ in models]
        t = table_rows([hdr] + body, font_size=28, col_buff=0.8, row_buff=0.32, colors=[GREY_A] + [c for *_, c in models])
        t.move_to([0, 0.8, 0])
        foot = fit_rows(VGroup(
            label(rf"ZIP's structural zeros: \ $\hat\pi = {d['zip']['pi']:.2f}$", font_size=22, color=ZIPC),
            label(r"zero-inflation alone does not fix the long right tail", font_size=22),
            label(r"the negative binomial wins by 700 in AIC", font_size=22, color=HIT),
        ), 12.0, 0.25, [0, -1.9, 0])
        with self.voiceover(
            "<bookmark mark='a'/> Fit all four to the same visits. <bookmark mark='b'/> The Poisson's log likelihood is minus "
            "four thousand six hundred and eighty-two. <bookmark mark='c'/> Zero inflation helps a lot, putting thirty-five "
            "percent of the adults among the never-goers; the hurdle helps a little more. <bookmark mark='d'/> But the "
            "negative binomial beats them all, by about seven hundred in AIC: inflating the zeros cannot create the long right tail, "
            "which needs people with high rates."
        ) as vo:
            self.add(simulated_tag())
            vo.wait_until("a")
            self.play(FadeIn(t[0]))
            vo.wait_until("b")
            self.play(FadeIn(t[1]))
            vo.wait_until("c")
            self.play(FadeIn(t[2]), FadeIn(t[3]), FadeIn(foot[0]), FadeIn(foot[1]))
            vo.wait_until("d")
            self.play(FadeIn(t[4]), FadeIn(foot[2]))
        self.clear_scene()

    def ppml(self):
        rows = [
            cmath(r"\text{Poisson score}", r":", r"\textstyle\sum_i x_i (y_i - e^{x_i^\top\beta}) = 0", font_size=30),
            cmath(r"\text{consistent if}", r":", r"E(y \mid x) = e^{x^\top\beta}, \ \text{any variance, \ any distribution}", font_size=28),
            cmath(r"\text{even for}", r":", r"\text{continuous } y \ge 0: \ \text{trade flows, \ costs}", font_size=30),
            cmath(r"\text{with}", r":", r"\text{the sandwich SE}", font_size=30),
        ]
        rows[1][-1].set_color(HIT)
        whys = [why(r"the canonical-link score"), why(r"Gourieroux, \ Monfort \& Trognon (1984)"),
                why(r"Santos Silva \& Tenreyro (2006): \ PPML"), why(r"chapter seven's Board row")]
        with self.voiceover(
            "<bookmark mark='a'/> A reassuring fact behind chapter seven's Board. The Poisson score equations involve only "
            "the mean. <bookmark mark='b'/> So the Poisson estimates are consistent whenever the log mean is linear, whatever "
            "the variance and whatever the distribution, as Christian Gourieroux, Alain Monfort and Alain Trognon proved in "
            "1984. <bookmark mark='c'/> It even works for continuous non-negative outcomes: economists fit international "
            "trade flows this way, Poisson pseudo-maximum likelihood, avoiding the bias of taking logs of data with zeros. "
            "<bookmark mark='d'/> Paired with the sandwich, it is one of the most robust tools in this part."
        ) as vo:
            step = ladder(self, rows, whys, keep=4, top=2.6, x=-0.9, buff=0.85, edge=6.9)
            for k, m_ in enumerate("abcd"):
                vo.wait_until(m_)
                step(k, transform=False)
        self.clear_scene()

    def truth(self):
        d = load("visits")
        rows = [
            cmath(r"\text{the World}", r":", rf"\text{{a never-goer share of about }} {100 * d['true_never']:.0f}\% \text{{, then NB with }} k = {d['true_k']}", font_size=28),
            cmath(r"\text{so the truth}", r"=", r"\text{zero-inflated negative binomial}", font_size=30),
            cmath(r"\text{NB's } \hat k", r"=", rf"{d['nb']['k']:.2f} \ < \ {d['true_k']}: \ \text{{the zeros absorbed into }} k", font_size=28),
            cmath(r"\text{lesson}", r":", r"\text{the model that fits best need not be the mechanism}", font_size=28),
        ]
        rows[1][2].set_color(HIT)
        whys = [why(r"we built it, \ so we know"), why(r"both stories at once"), why(r"extra heterogeneity, \ to explain the zeros"),
                why(r"Part 28: \ which model?")]
        with self.voiceover(
            "<bookmark mark='a'/> Here's the advantage of a World whose truth we know. It was built with about fifteen percent "
            "never-goers, who stay at zero, and a negative binomial with k equal to one point two for everyone else. "
            "<bookmark mark='b'/> So the truth is a zero-inflated negative binomial, both stories at once. "
            "<bookmark mark='c'/> The plain negative binomial fits well by pretending the heterogeneity is larger than it is, "
            "k of point eight two instead of one point two, so that its spread covers the extra zeros. "
            "<bookmark mark='d'/> The model that fits best need not be the mechanism that made the data. Part 28 takes up how "
            "to choose."
        ) as vo:
            step = ladder(self, rows, whys, keep=4, top=2.6, x=-0.9, buff=0.85, edge=6.9)
            for k, m_ in enumerate("abcd"):
                vo.wait_until(m_)
                step(k, transform=False)
        self.clear_scene()

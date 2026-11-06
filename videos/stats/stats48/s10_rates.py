from __future__ import annotations

import numpy as np

from videos.stats.stats48.common import *  # noqa: F403


class Rates(VoiceoverScene):
    def construct(self):
        self.card()
        self.theorem()
        self.cuberoot()
        self.chernoff()
        self.grenander()
        self.others()

    def card(self):
        card = chapter_card(9, r"Rates of convergence", r"When the answer is not $\sqrt n$", lit=(1990,), part=PART)
        with self.voiceover("Chapter nine. Rates of convergence: when the answer is not root n."):
            self.play(FadeIn(card[0], shift=UP * 0.2), FadeIn(card[1]))
        self.play(FadeOut(card))

    def theorem(self):
        rows = [
            cmath(r"M(\theta) - M(\theta_0)", r"\lesssim", r"-\,d(\theta, \theta_0)^2 \ \ \text{near } \theta_0", font_size=34),
            cmath(r"E \sup_{d(\theta, \theta_0) < \delta} |\mathbb G_n(m_\theta - m_{\theta_0})|", r"\lesssim", r"\phi_n(\delta)", font_size=32),
            cmath(r"r_n^2\, \phi_n(1/r_n)", r"\le", r"\sqrt n \ \ \Rightarrow \ \ r_n\, d(\hat\theta_n, \theta_0) = O_P(1)", font_size=34),
            cmath(r"\phi_n(\delta) = \delta", r"\Rightarrow", r"r_n = \sqrt n; \ \ \ \phi_n(\delta) = \sqrt\delta \Rightarrow r_n = n^{1/3}", font_size=32),
        ]
        rows[2][-1].set_color(GOODC)
        rows[3][-1].set_color(CLASSC)
        whys = [why(r"curvature of the criterion"), why(r"the local modulus, \ by chaining"), why(r"the rate theorem"), why(r"smooth vs.\ indicator criteria")]
        with self.voiceover(
            "<bookmark mark='a'/> For an M-estimator, two things fix the rate. The population criterion curves away from its "
            "maximum quadratically. <bookmark mark='b'/> And the empirical process, restricted to parameters within delta of "
            "the truth, has expected supremum of order some function phi n of delta, which chaining computes. <bookmark "
            "mark='c'/> The rate theorem says the estimator converges at the rate r n that balances the two: r n squared times "
            "phi n of one over r n equal to root n. <bookmark mark='d'/> For smooth criteria the local modulus is linear in "
            "delta, and the rate is root n, as in Part forty-seven. But when the criterion is an indicator, the local "
            "increments have variance proportional to delta, not delta squared, the modulus is root delta, and the balance "
            "gives n to the one third."
        ) as vo:
            step = ladder(self, rows, whys, keep=4, top=2.6, x=-0.9, buff=0.85, edge=6.9)
            for k, m_ in enumerate("abcd"):
                vo.wait_until(m_)
                step(k, transform=False)
        self.clear_scene()

    def cuberoot(self):
        rows = [
            cmath(r"\text{Kim \& Pollard (1990)}", r":", r"n^{1/3}(\hat\theta - \theta_0) \Rightarrow \operatorname*{argmax}_t \{ \sigma W(t) - c\,t^2 \}", font_size=30),
            cmath(r"\text{Grenander (1956)}", r":", r"\hat f = \text{the slope of the least concave majorant of } F_n", font_size=30),
            cmath(r"n^{1/3}(\hat f(x_0) - f(x_0))", r"\Rightarrow", r"\big|\tfrac12 f(x_0) f'(x_0)\big|^{1/3} \cdot 2Z", font_size=34),
            cmath(r"Z", r"=", r"\operatorname*{argmax}_t \{W(t) - t^2\}: \ \text{Chernoff's distribution}", font_size=34),
        ]
        rows[0][-1].set_color(CLASSC)
        rows[2][-1].set_color(GOODC)
        rows[3][-1].set_color(BRIDGEC)
        whys = [why(r"cube-root asymptotics"), why(r"Part 29's monotone density"), why(r"Prakasa Rao (1969); \ Groeneboom (1985)"), why(r"Chernoff (1964), \ the mode")]
        with self.voiceover(
            "<bookmark mark='a'/> Jeankyung Kim and David Pollard showed in 1990 that such cube-root estimators share a "
            "universal limit: the location of the maximum of a two-sided Brownian motion minus a parabola. <bookmark "
            "mark='b'/> The best-known example is Ulf Grenander's estimator of a decreasing density, from Part twenty-nine: "
            "the slope of the least concave majorant of the empirical distribution function. <bookmark mark='c'/> At a "
            "point where the density has a negative derivative, its error, scaled by n to the one third, converges to a "
            "constant depending on f and f prime, times twice Z. <bookmark mark='d'/> Z is Chernoff's distribution: where "
            "Brownian motion minus t squared reaches its maximum. Herman Chernoff met it in 1964 estimating a mode."
        ) as vo:
            step = ladder(self, rows, whys, keep=4, top=2.6, x=-0.9, buff=0.85, edge=6.9)
            for k, m_ in enumerate("abcd"):
                vo.wait_until(m_)
                step(k, transform=False)
        self.clear_scene()

    def chernoff(self):
        d = load("rates")
        e = np.asarray(d["edges"])
        A = axes([-1.6, 1.6], [0, 1.0], x_length=7.4, y_length=4.4, xlabel=r"$Z = \operatorname{argmax}_t\,(W(t) - t^2)$", ylabel=r"density",
                 xticks=[-1.5, -1, -0.5, 0, 0.5, 1, 1.5], yticks=[0, 0.5, 1], center=[-2.5, 0.2, 0])
        ax = A.ax
        hb = hist_bars(ax, e, d["z_hist"], color=CLASSC, opacity=0.55)
        u = np.linspace(-1.6, 1.6, 300)
        sd = d["z_sd_ref"]
        nc = polyline(ax, u, np.exp(-u ** 2 / (2 * sd ** 2)) / np.sqrt(2 * np.pi * sd ** 2), BRIDGEC, 3)
        side = fit_rows(VGroup(
            label(r"6,000 two-sided Brownian paths minus $t^2$", font_size=22),
            label(rf"gold: \ where each peaks: \ SD {d['z_sd']:.3f}", font_size=22, color=CLASSC),
            label(rf"Groeneboom \& Wellner (2001): \ SD {sd:.4f}", font_size=22, color=GOODC),
            label(r"white: \ a normal with that SD, \ for contrast", font_size=22, color=BRIDGEC),
            label(r"lighter tails than normal: \ like $e^{-c|t|^3}$", font_size=22, color=GREY_A),
        ), 4.6, 0.42, [4.45, 0.4, 0])
        with self.voiceover(
            f"<bookmark mark='a'/> Here is Chernoff's distribution, simulated: six thousand two-sided Brownian paths, each "
            f"with t squared subtracted, <bookmark mark='b'/> and where each one peaks. The simulated standard deviation is "
            f"{say(d['z_sd'], 3)}. <bookmark mark='c'/> Piet Groeneboom and Jon Wellner computed the distribution exactly in "
            f"2001, with Airy functions; its standard deviation is {say(sd, 3)}. <bookmark mark='d'/> Against a normal with "
            f"the same spread, <bookmark mark='e'/> it is more peaked and has much lighter tails, decaying like e to the minus "
            f"a constant times the cube of t."
        ) as vo:
            self.play(FadeIn(A), FadeIn(simulated_tag(r"simulated: \ 6,000 paths")))
            vo.wait_until("a")
            self.play(FadeIn(side[0]))
            vo.wait_until("b")
            self.play(FadeIn(hb), FadeIn(side[1]))
            vo.wait_until("c")
            self.play(FadeIn(side[2]))
            vo.wait_until("d")
            self.play(Create(nc), FadeIn(side[3]))
            vo.wait_until("e")
            self.play(FadeIn(side[4]))
        self.clear_scene()

    def grenander(self):
        d = load("rates")
        rows = [[r"$n$", r"SD of $n^{1/3}(\hat f(1) - f(1))$", r"mean", r"samples"]]
        for r in d["rows"]:
            rows.append([f"{r['n']:,}", f"{r['sd']:.3f}", f"{r['mean']:+.3f}", f"{r['reps']:,}"])
        rows.append([r"limit", f"{d['pred_sd']:.3f}", r"0", r""])
        tab = table_rows(rows, font_size=30, col_buff=0.8, row_buff=0.36, colors=[GREY_B, None, None, None, GOODC])
        tab.move_to([0, 0.8, 0])
        foot = label(rf"Exp(1) data, \ $x_0 = 1$: \ $|\tfrac12 f f'|^{{1/3}} \cdot 2 = {d['const']:.3f}$, \ times SD$(Z)$ = {d['z_sd_ref']:.4f}", font_size=24, color=GREY_A).move_to([0, -1.6, 0])
        foot2 = label(r"$\sqrt n$ would be wrong: \ the scaled error would grow like $n^{1/6}$", font_size=24, color=BADC).move_to([0, -2.4, 0])
        with self.voiceover(
            f"<bookmark mark='a'/> Grenander's estimator for exponential data, at x equal to one, where both the density and "
            f"its slope are e to the minus one. The limit predicts that n to the one third times the error has standard "
            f"deviation {say(d['pred_sd'], 3)}. The simulated values at a hundred, a thousand and ten thousand observations "
            f"are {say(d['rows'][0]['sd'], 3)}, {say(d['rows'][1]['sd'], 3)} and {say(d['rows'][2]['sd'], 3)}: stable, and "
            f"close to the limit. <bookmark mark='b'/> Scaled by root n instead, the error would grow like n to the one sixth. "
            f"Using root n theory here would give intervals that are far too narrow."
        ) as vo:
            vo.wait_until("a")
            self.play(FadeIn(tab), FadeIn(foot), FadeIn(simulated_tag(r"simulated")))
            vo.wait_until("b")
            self.play(FadeIn(foot2))
        self.clear_scene()

    def others(self):
        rows = fit_rows(VGroup(
            label(r"other cube-root estimators: \ Manski's maximum score; \ the shorth; \ isotonic regression; \ current status data", font_size=26),
            label(r"the bootstrap fails for all of them \ (Kosorok 2008; \ Sen, \ Banerjee \& Woodroofe 2010)", font_size=26, color=BADC),
            label(r"what works: \ subsampling, \ $m$ out of $n$ \ (Part 47's chapter 13), \ or likelihood-ratio inversion", font_size=26, color=GOODC),
            label(r"Banerjee \& Wellner (2001): \ the LR statistic's limit is pivotal: \ intervals without $f'$", font_size=26, color=CLASSC),
        ), 12.4, 0.6, [0, 0, 0])
        with self.voiceover(
            "<bookmark mark='a'/> Cube-root asymptotics turn up wherever an estimator maximizes a sum of indicators: "
            "Charles Manski's maximum score estimator for binary choice, the shortest half of the data, isotonic regression, "
            "and current status data in survival analysis. <bookmark mark='b'/> The ordinary bootstrap is inconsistent for all "
            "of them, for the reason Part forty-seven found with the sample maximum. <bookmark mark='c'/> What works is "
            "subsampling, or the m out of n bootstrap, <bookmark mark='d'/> or, more elegantly, Moulinath Banerjee and Jon "
            "Wellner's likelihood ratio statistic, whose limit is free of all unknowns, so that intervals need no estimate "
            "of the derivative."
        ) as vo:
            for k, m_ in enumerate("abcd"):
                vo.wait_until(m_)
                self.play(FadeIn(rows[k], shift=RIGHT * 0.2))
        self.clear_scene()

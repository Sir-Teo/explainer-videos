from __future__ import annotations

import numpy as np

from videos.stats.stats48.common import *  # noqa: F403


class FunctionalDelta(VoiceoverScene):
    def construct(self):
        self.card()
        self.theorem()
        self.quantile()
        self.qtable()
        self.km()
        self.kmtable()

    def card(self):
        card = chapter_card(7, r"The functional delta method", r"Quantile processes and Kaplan--Meier, from one theorem", part=PART)
        with self.voiceover("Chapter seven. The functional delta method: quantile processes and Kaplan–Meier, from one theorem."):
            self.play(FadeIn(card[0], shift=UP * 0.2), FadeIn(card[1]))
        self.play(FadeOut(card))

    def theorem(self):
        rows = [
            cmath(r"\sqrt n(F_n - F)", r"\Rightarrow", r"\mathbb G_F = B \circ F \ \text{ in } \ell^\infty(\mathbb R)", font_size=36),
            cmath(r"\phi \text{ Hadamard differentiable at } F", r":", r"\sqrt n(\phi(F_n) - \phi(F)) \Rightarrow \phi'_F(\mathbb G_F)", font_size=32),
            cmath(r"\phi(F) = F^{-1}", r":", r"\phi'_F(h) = -\,\frac{h \circ F^{-1}}{f \circ F^{-1}}", font_size=36),
            cmath(r"\Rightarrow", r"\;", r"\sqrt n(Q_n(p) - Q(p)) \Rightarrow -\,B(p)/f(Q(p)), \ \text{jointly on } p\in[a,b]\subset(0,1)", font_size=32),
        ]
        rows[1][-1].set_color(GOODC)
        rows[3][-1].set_color(EMPC)
        whys = [why(r"chapter 5: \ Donsker"), why(r"Part 47's chapter 4, \ now with a process"), why(r"the inverse map"), why(r"a whole quantile process")]
        heading = label('A tangential linear derivative transfers a process limit', font_size=34).move_to([0, 3.3, 0])
        if heading.width > 12.5: heading.width = 12.5
        self.add(heading)
        with self.voiceover(
            "<bookmark mark='a'/> Donsker's theorem says the empirical process converges to a Brownian bridge run on the scale of F. <bookmark mark='b'/> Part forty-seven's functional delta method then applies to any map of the distribution function that is Hadamard differentiable: the map's derivative, applied to the bridge, is the limit. <bookmark mark='c'/> Inverting a distribution function is such a map, at regular F with a positive continuous density, uniformly bounded away from zero on the quantile range in question. Its derivative in the direction h is minus h at the quantile, divided by the density there. <bookmark mark='d'/> So the whole quantile process converges: root n times the error of the sample quantile function is asymptotically minus a Brownian bridge over the density, jointly over a compact interior range of p; an unweighted whole-interval result generally fails at the tails. Bahadur's representation, from Part forty-seven, was a single coordinate of this."
        ) as vo:
            step = ladder(self, rows, whys, keep=4, top=2.6, x=-0.9, buff=0.85, edge=6.9)
            for k, m_ in enumerate("abcd"):
                vo.wait_until(m_)
                step(k, transform=False)
        self.clear_scene()

    def quantile(self):
        d = load("delta")
        pg = np.asarray(d["pg"])
        A = axes([0, 1], [-6, 6], x_length=7.4, y_length=4.4, xlabel=r"$p$", ylabel=r"$\sqrt n\,(Q_n(p) - Q(p))$",
                 xticks=[0, 0.25, 0.5, 0.75, 1], yticks=[-4, 0, 4], center=[-2.5, 0.2, 0])
        ax = A.ax
        path = clip_curve(ax, pg, d["path"], EMPC, 3, ymin=-6, ymax=6)
        hi = clip_curve(ax, pg, d["band"], BRIDGEC, 2.5, ymin=-6, ymax=6)
        lo = clip_curve(ax, pg, -np.asarray(d["band"]), BRIDGEC, 2.5, ymin=-6, ymax=6)
        side = fit_rows(VGroup(
            label(rf"Exp(1) data, \ $n = {d['n']}$", font_size=22),
            label(r"blue: \ one sample's quantile process", font_size=22, color=EMPC),
            label(r"white: \ $\pm 1.96\,\sqrt{p(1-p)}/f(Q(p)) = \pm 1.96\sqrt{p/(1-p)}$", font_size=22, color=BRIDGEC),
            label(r"the spread explodes as $p \to 1$: \ the density vanishes", font_size=22, color=BADC),
            label(r"pointwise bands, \ not a uniform one", font_size=22, color=GREY_A),
        ), 4.6, 0.42, [4.45, 0.4, 0])
        with self.voiceover(
            f"<bookmark mark='a'/> Exponential data, {d['n']} observations. <bookmark mark='b'/> In blue, one sample's "
            f"quantile process: root n times the error of its quantile function, across p. <bookmark mark='c'/> In white, "
            f"plus and minus one point nine six asymptotic standard deviations. For the exponential, the root of p times one "
            f"minus p over the density at the quantile simplifies to the root of p over one minus p. <bookmark mark='d'/> "
            f"The spread blows up as p approaches one, because the density there vanishes: the upper quantiles of a "
            f"long-tailed distribution are hard to pin down. <bookmark mark='e'/> These are pointwise limits. A band that "
            f"holds for all p at once needs the supremum of the limiting process, which the bootstrap of chapter eleven provides."
        ) as vo:
            self.play(FadeIn(A), FadeIn(seeded_tag()))
            vo.wait_until("a")
            self.play(FadeIn(side[0]))
            vo.wait_until("b")
            self.play(Create(path), FadeIn(side[1]))
            vo.wait_until("c")
            self.play(Create(hi), Create(lo), FadeIn(side[2]))
            vo.wait_until("d")
            self.play(FadeIn(side[3]))
            vo.wait_until("e")
            self.play(FadeIn(side[4]))
        self.clear_scene()

    def qtable(self):
        d = load("delta")
        rows = [[r"$p$"] + [f"{p:g}" for p in d["ps"]],
                [r"simulated SD"] + [f"{v:.3f}" for v in d["sd_sim"]],
                [r"$\sqrt{p/(1-p)}$"] + [f"{v:.3f}" for v in d["sd_th"]]]
        tab = table_rows(rows, font_size=30, col_buff=0.7, row_buff=0.4, colors=[GREY_B, EMPC, None])
        tab.move_to([0, 0.9, 0])
        foot = label(rf"SD of $\sqrt n(Q_n(p) - Q(p))$, \ Exp(1), \ $n = {d['n']}$, \ 20,000 samples", font_size=24, color=GREY_A).move_to([0, -1.2, 0])
        foot2 = label(r"the delta method holds at every $p$, \ to two decimals, \ already at $n = 200$", font_size=24, color=GOODC).move_to([0, -2.0, 0])
        with self.voiceover(
            f"<bookmark mark='a'/> Checked by simulation at five values of p: the simulated standard deviations are "
            f"{say(d['sd_sim'][0], 3)}, {say(d['sd_sim'][2], 3)} at the median, and {say(d['sd_sim'][4], 3)} at the ninetieth "
            f"percentile, against the delta method's {say(d['sd_th'][0], 3)}, one, and three. <bookmark mark='b'/> Agreement "
            f"to about two decimals, at two hundred observations."
        ) as vo:
            vo.wait_until("a")
            self.play(FadeIn(tab), FadeIn(foot), FadeIn(simulated_tag(r"simulated: \ 20,000 samples")))
            vo.wait_until("b")
            self.play(FadeIn(foot2))
        self.clear_scene()

    def km(self):
        rows = [
            cmath(r"\sqrt n\big((H_n^{\text{event}}, H_n)-(H^{\text{event}},H)\big)", r"\Rightarrow", r"\text{a Gaussian process}: \ \text{a Donsker class of indicators}", font_size=30),
            cmath(r"\Lambda_n(t)", r"=", r"\int_0^t \frac{dH_n^{\text{event}}}{1 - H_{n-}}: \ \text{Nelson--Aalen, \ a smooth map of } (H^{\text{event}}_n, H_n)", font_size=28),
            cmath(r"\hat S(t)", r"=", r"\textstyle\prod_{s \le t}(1 - d\Lambda_n(s)): \ \text{the product integral, \ Hadamard differentiable}", font_size=28),
            cmath(r"\sqrt n(\hat S - S)", r"\Rightarrow", r"-S \cdot W, \ \ \mathrm{Var}\,W(t) = \int_0^t \frac{d\Lambda}{S\,G}", font_size=34),
        ]
        rows[3][-1].set_color(GOODC)
        whys = [why(r"observed times and events"), why(r"Part 40's hazard"), why(r"Gill \& Johansen (1990)"), why(r"Greenwood's formula, \ as a limit")]
        heading = label('Centre and scale the joint event and time process', font_size=34).move_to([0, 3.3, 0])
        if heading.width > 12.5: heading.width = 12.5
        self.add(heading)
        with self.voiceover(
            "<bookmark mark='a'/> The Kaplan–Meier estimator of Part forty yields to the same method. For iid subjects with independent right censoring and positive at-risk probability on a fixed finite horizon, the empirical distribution of the observed times, and of the times that were events, form a two-dimensional empirical process over a Donsker class of indicators. <bookmark mark='b'/> The Nelson–Aalen cumulative hazard is an integral of one with respect to the other, a smooth map. <bookmark mark='c'/> The Kaplan–Meier curve is the product integral of the hazard, and Richard Gill and Søren Johansen showed in 1990 that the product integral is Hadamard differentiable. <bookmark mark='d'/> Chaining the derivatives: root n times the Kaplan–Meier error converges to minus S times a Gaussian martingale whose variance at t is the integral of the hazard over S times G, where G is the censoring survivor function. Greenwood's formula estimates this asymptotic variance; it is not an exact finite-sample variance."
        ) as vo:
            step = ladder(self, rows, whys, keep=4, top=2.6, x=-0.9, buff=0.85, edge=6.9)
            for k, m_ in enumerate("abcd"):
                vo.wait_until(m_)
                step(k, transform=False)
        self.clear_scene()

    def kmtable(self):
        d = load("delta")
        rows = [[r"$t$"] + [f"{t:g}" for t in d["tt"]],
                [r"$S(t)$"] + [f"{np.exp(-t):.3f}" for t in d["tt"]],
                [r"simulated SD"] + [f"{v:.3f}" for v in d["km_sd"]],
                [r"$\sqrt{S^2 \int_0^t d\Lambda/(SG)}$"] + [f"{v:.3f}" for v in d["km_th"]]]
        tab = table_rows(rows, font_size=28, col_buff=0.7, row_buff=0.38, colors=[GREY_B, GREY_A, EMPC, None])
        tab.move_to([0, 0.9, 0])
        foot = label(rf"SD of $\sqrt n(\hat S(t) - S(t))$: \ Exp(1) times, \ Exp(1/2) censoring, \ $n = {d['n']}$, \ {d['km_reps']:,} samples", font_size=24, color=GREY_A).move_to([0, -1.5, 0])
        foot2 = label(r"here $S^2\!\int_0^t e^{1.5u}\,du$ in closed form: \ the limit matches to about 0.01", font_size=24, color=GOODC).move_to([0, -2.3, 0])
        with self.voiceover(
            f"<bookmark mark='a'/> A check. Exponential survival times with rate one, exponential censoring with rate one "
            f"half, two hundred subjects. The simulated standard deviations of root n times the Kaplan–Meier error, at five "
            f"times, against the limit, which here has a closed form: at t equal to one, {say(d['km_sd'][2], 3)} simulated "
            f"against {say(d['km_th'][2], 3)}. <bookmark mark='b'/> One theorem, the functional delta method on a Donsker "
            f"class, gives the quantile process, the Kaplan–Meier process, and many more: the Nelson–Aalen estimator, "
            f"the L-statistics, the ROC curve."
        ) as vo:
            vo.wait_until("a")
            self.play(FadeIn(tab), FadeIn(foot), FadeIn(simulated_tag(r"simulated: \ 3,000 samples")))
            vo.wait_until("b")
            self.play(FadeIn(foot2))
        self.clear_scene()

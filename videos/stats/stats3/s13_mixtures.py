from __future__ import annotations

import numpy as np

from videos.stats.stats3.common import *  # noqa: F403


class Mixtures(VoiceoverScene, TreeMixin):
    def construct(self):
        self.card()
        self.betabin()
        self.total_variance()
        self.gamma_poisson()
        self.scale_mixture()
        self.tree_voiceover("The last two arrows are mixtures: <bookmark mark='t'/> a Poisson whose rate is gamma is "
                             "negative binomial, and a binomial whose success chance is beta is beta-binomial.", 12)

    def card(self):
        card = chapter_card(12, r"Mixtures and hierarchies", r"When the parameter is random too", lit=(), part=PART)
        with self.voiceover("Chapter twelve. Mixtures and hierarchies."):
            self.play(FadeIn(card[0], shift=UP * 0.2), FadeIn(card[1]))
        self.play(FadeOut(card))

    def betabin(self):
        d = load("mixtures")
        kk = np.asarray(d["kk"])
        A = axes([-0.6, 20.6], [0, 0.2], x_length=7.6, y_length=4.0, xlabel=r"successes in 20 trials",
                 xticks=[0, 5, 10, 15, 20], yticks=[0, 0.1, 0.2], center=[-2.4, -0.8, 0])
        ax = A.ax
        bars = pmf_bars(ax, kk, d["bb_emp"], SIM, width=0.65)
        bb = pmf_dots(ax, kk, d["bb_pmf"], EXACT, radius=0.06)
        bi = curve(ax, kk, d["bin_pmf"], GREY_A, 2.5)
        steps = VGroup(MathTex(r"p \sim \text{beta}(2, 3)", font_size=32, color=S.PRIOR),
                       MathTex(r"X \mid p \sim \text{binomial}(20, p)", font_size=32, color=DISC))
        steps.arrange(DOWN, aligned_edge=LEFT, buff=0.25).move_to([4.2, 2.4, 0])
        leg = legend([(SIM, r"50,000 simulated"), (EXACT, r"beta-binomial"), (GREY_A, r"binomial$(20, 0.4)$")],
                     font_size=22).move_to([4.4, 0.6, 0])
        var = MathTex(rf"\text{{variance }} {d['bb_var']:.1f} \ \text{{vs}}\ {d['bin_var']:.1f}", font_size=28, color=S.ACCENT)
        var.move_to([4.4, -0.8, 0])
        ex = label(r"batting averages, \ hospital survival rates, \ any rate that varies between units", font_size=22,
                   color=GREY_B).move_to([4.2, -1.8, 0])
        if ex.width > 5.6:
            ex.width = 5.6
        with self.voiceover(
            "So far every parameter has been a fixed number. Let the parameter itself be random. "
            "<bookmark mark='a'/> Choose a success chance p from a beta distribution, then run twenty trials with "
            "that p. Each unit, a player, a hospital, a batch, has its own rate. <bookmark mark='b'/> The count is "
            "beta-binomial. <bookmark mark='c'/> Compared with a binomial with the same average chance, grey, it's "
            f"far more spread out: variance {d['bb_var']:.0f} against about five. That extra spread is called "
            "overdispersion, and real counts nearly always have it."
        ) as vo:
            vo.wait_until("a")
            self.play(FadeIn(steps))
            vo.wait_until("b")
            self.play(FadeIn(A), FadeIn(bars), FadeIn(bb))
            vo.wait_until("c")
            self.play(Create(bi), FadeIn(leg), FadeIn(var), FadeIn(ex))
        self.clear_scene()

    def total_variance(self):
        d = load("mixtures")
        rows = [
            cmath(r"\mathrm{Var}\, X", r"=", r"E\big[\mathrm{Var}(X \mid p)\big]", r"+", r"\mathrm{Var}\big(E[X \mid p]\big)",
                  font_size=36),
            cmath(r"\mathrm{Var}\, X", r"=", r"E\big[20\, p(1-p)\big]", r"+", r"\mathrm{Var}(20\, p)", font_size=36),
            cmath(r"\mathrm{Var}\, X", r"=", r"4", r"+", r"16", r"=", r"20", font_size=40),
        ]
        rows[0][2].set_color(DISC)
        rows[0][4].set_color(S.PRIOR)
        rows[2][6].set_color(EXACT)
        whys = [why(r"the law of total variance"), why(r"binomial, \ given $p$"), why(r"beta$(2,3)$ moments")]
        cap = VGroup(label(r"noise within units", font_size=24, color=DISC),
                     label(r"$+$ \ variation between units", font_size=24, color=S.PRIOR)).arrange(RIGHT, buff=0.3)
        cap.to_edge(DOWN, buff=0.7)
        with self.voiceover(
            "Where does the extra variance come from? <bookmark mark='a'/> The law of total variance splits it in "
            "two: the average variance within units, given their p, plus the variance of their means between "
            "units. <bookmark mark='b'/> For our mixture, the binomial variance twenty p times one minus p, "
            "averaged over the beta, <bookmark mark='c'/> is four; the variance of twenty p is sixteen; total "
            "twenty, exactly what the simulation found. This decomposition, within plus between, is the seed of "
            "the analysis of variance in Part 13 and of the mixed models in Part 25."
        ) as vo:
            step = ladder(self, rows, whys, keep=3, top=2.4, x=-0.6, buff=0.6)
            for k, m in enumerate("abc"):
                vo.wait_until(m)
                step(k, transform=k > 0)
            self.play(FadeIn(cap))
        self.clear_scene()

    def gamma_poisson(self):
        d = load("waiting")
        kk = np.asarray(d["gp_k"])
        A = axes([-0.6, 15.6], [0, 0.2], x_length=7.4, y_length=4.0, xlabel=r"count", xticks=[0, 5, 10, 15],
                 yticks=[0, 0.1, 0.2], center=[-2.4, -0.8, 0])
        ax = A.ax
        from scipy import stats as st
        bars = pmf_bars(ax, kk, d["gp_emp"], SIM, width=0.65)
        nb = pmf_dots(ax, kk, d["gp_nb"], EXACT, radius=0.06)
        pc = curve(ax, kk, st.poisson.pmf(kk, d["gp_mean"]), GREY_A, 2.5)
        steps = VGroup(MathTex(rf"\lambda \sim \text{{gamma}}({d['shape']:g},\ {d['scale']:g})", font_size=30, color=S.PRIOR),
                       MathTex(r"X \mid \lambda \sim \text{Poisson}(\lambda)", font_size=30, color=DISC),
                       MathTex(r"\Rightarrow\ X \sim \text{negative binomial}", font_size=30, color=EXACT))
        steps.arrange(DOWN, aligned_edge=LEFT, buff=0.22).move_to([4.2, 2.3, 0])
        mv = MathTex(rf"\text{{mean }} {d['gp_mean']:.2f},\ \text{{variance }} {d['gp_var']:.2f}", font_size=26, color=SIM)
        mv.move_to([4.4, 0.3, 0])
        leg = legend([(EXACT, r"negative binomial"), (GREY_A, r"Poisson, same mean")], font_size=22).move_to([4.4, -0.8, 0])
        with self.voiceover(
            "Now chapter three's promise. <bookmark mark='a'/> Give each unit its own Poisson rate, drawn from a "
            "gamma distribution: some corps more dangerous than others, some roads more accident-prone. "
            "<bookmark mark='b'/> The resulting counts are exactly negative binomial; integrating the Poisson "
            "against the gamma gives its formula. <bookmark mark='c'/> The mean is three, but the variance is "
            "about seven and a half, where a Poisson's would equal its mean. That's why the negative binomial is "
            "the standard model for overdispersed counts, in Part 24."
        ) as vo:
            vo.wait_until("a")
            self.play(FadeIn(steps[:2]))
            vo.wait_until("b")
            self.play(FadeIn(A), FadeIn(bars), FadeIn(nb), FadeIn(steps[2]))
            vo.wait_until("c")
            self.play(Create(pc), FadeIn(mv), FadeIn(leg))
        self.clear_scene()

    def scale_mixture(self):
        d = load("mixtures")
        ts = np.asarray(d["ts"])
        A = axes([-6, 6], [0, 0.42], x_length=7.4, y_length=4.0, xlabel=r"$x$", xticks=[-6, -3, 0, 3, 6],
                 yticks=[0, 0.2, 0.4], center=[-2.4, -0.6, 0])
        ax = A.ax
        x = np.asarray(d["t_x"])
        ed = np.linspace(-6, 6, 61)
        h = hist_bars(ax, ed, np.histogram(x, ed)[0] / (len(x) * np.diff(ed)), color=SIM, opacity=0.6)
        tc = curve(ax, ts, np.asarray(d["tden"]), EXACT, 3)
        nc = curve(ax, ts, np.asarray(d["nden"]), GREY_A, 2.5)
        steps = VGroup(MathTex(rf"\sigma^2 = \nu / V,\ \ V \sim \chi^2_{{{d['nu']}}}", font_size=30, color=S.PRIOR),
                       MathTex(r"X \mid \sigma \sim \text{normal}(0, \sigma^2)", font_size=30, color=CONT),
                       MathTex(rf"\Rightarrow\ X \sim t_{{{d['nu']}}}", font_size=30, color=EXACT))
        steps.arrange(DOWN, aligned_edge=LEFT, buff=0.22).move_to([4.2, 2.2, 0])
        leg = legend([(EXACT, rf"$t_{{{d['nu']}}}$"), (GREY_A, r"normal")], font_size=22).move_to([4.4, 0.3, 0])
        take = label(r"heavy tails from a mixture of light ones: \ robust models, \ Part 30", font_size=22, color=GREY_B)
        take.move_to([4.2, -0.8, 0])
        if take.width > 5.6:
            take.width = 5.6
        with self.voiceover(
            "Mixtures explain heavy tails too. <bookmark mark='a'/> Draw a normal, but first choose its variance at "
            "random, from an inverse chi-squared: most of the time a modest spread, occasionally a huge one. "
            "<bookmark mark='b'/> The mixture is exactly Student's t. Every component has light normal tails, yet "
            "the occasional wide component makes the mixture's tails heavy. It's the basis of robust statistical "
            "models, in Part 30."
        ) as vo:
            vo.wait_until("a")
            self.play(FadeIn(steps[:2]))
            vo.wait_until("b")
            self.play(FadeIn(A), FadeIn(h), Create(tc), Create(nc), FadeIn(steps[2]), FadeIn(leg), FadeIn(take))
        self.clear_scene()

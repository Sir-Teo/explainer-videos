from __future__ import annotations

import numpy as np
from scipy.stats import norm

from explainer.quant import *  # noqa: F403
from videos.quant.quant16.common import BAD, GOOD, OPT, PART, SPOT, illustration, load, predict, axes, data_range, pause_card, flat_camera


class Importance(VoiceoverScene):
    def construct(self):
        s = load("is_sweep")
        m = load("mc")
        self.card()
        self.slide(s)
        self.proof()
        self.learn(s, m)

    def card(self):
        c = chapter_card(4, r"Variance reduction: importance sampling", r"Where should a simulation look for a rare "
                         r"payoff?", part=PART)
        with self.voiceover("Chapter four. Importance sampling, and rare events."):
            self.play(FadeIn(c[0], shift=UP * 0.2), FadeIn(c[1]))
        self.play(FadeOut(c))

    def slide(self, s):
        th = np.asarray(s["theta"])
        ratio = np.asarray(s["ratio"])
        ess = np.asarray(s["ess"])
        zs = s["theta_strike"]
        top = axes([-4, 8], [0, 0.45], x_length=8.2, y_length=2.2, xlabel=r"the normal $z$ that drives $S_T$",
                   xticks=[-4, 0, 4, 8], font_size=15).to_edge(UP, buff=0.5).to_edge(LEFT, buff=0.7)
        ta = top.ax
        xs = np.linspace(-4, 8, 300)
        p = curve(ta, xs, norm.pdf(xs), SPOT, stroke_width=3)
        # the tail beyond the strike, filled by hand (Axes.get_area breaks on this manim version's 2D axes)
        xt = np.linspace(zs, 8, 120)
        reg = Polygon(*[ta.c2p(float(x), 0) for x in (zs, 8)][::-1], *[ta.c2p(float(x), float(norm.pdf(x))) for x in xt],
                      stroke_width=0, fill_color=BAD, fill_opacity=0.5)
        t = ValueTracker(0.0)
        q = always_redraw(lambda: curve(ta, xs, norm.pdf(xs - t.get_value()), OPT, stroke_width=3))
        lr = np.log10(ratio)
        yr = data_range(lr, [0])
        bot = axes([0, 7], yr, x_length=8.2, y_length=2.6, xlabel=r"shift $\theta$",
                   ylabel=r"variance divided by (log scale)", xticks=[0, 1, 2, 3, 4, 5, 6, 7], yticks=[0, 1, 2],
                   yfmt=lambda v: f"10^{{{int(v)}}}", font_size=15)
        bot.next_to(top, DOWN, buff=0.5).align_to(top, LEFT)
        ba = bot.ax
        one = DashedLine(ba.c2p(0, 0), ba.c2p(7, 0), stroke_color=GREY_C, stroke_width=1.5)

        def make():
            k = int(np.searchsorted(th, t.get_value(), side="right"))
            k = max(k, 2)
            return VMobject(stroke_color=OPT, stroke_width=3).set_points_as_corners(
                [ba.c2p(a, b) for a, b in zip(th[:k], lr[:k])])

        trace = always_redraw(make)

        def at(arr):
            return float(np.interp(t.get_value(), th, arr))

        rd = VGroup(readout(r"\theta =", lambda: t.get_value(), digits=2, font_size=30, color=OPT),
                    readout(r"\log_{10}(\mathrm{variance\ gain}) =", lambda: np.log10(at(ratio)), digits=2, font_size=23, color=GOOD),
                    readout(r"\log_{10}(\mathrm{ESS}/n) =", lambda: np.log10(at(ess)), digits=2, font_size=23, color=GREY_A),
                    ).arrange(DOWN, aligned_edge=LEFT, buff=0.18).to_edge(RIGHT, buff=0.6).shift(UP * 0.8)
        tag = label(rf"the payoff lives here: $z > {zs:.2f}$ ({100 * s['share_in_money']:.1f}\% of draws)", font_size=18,
                    color=BAD).next_to(ta.c2p(zs + 0.2, 0.3), RIGHT, buff=0.1)
        src = illustration(r"a call struck at 160 (one year, 20\% volatility); 400{,}000 common normals; empirical variance ratios on a finite shift grid")
        with self.voiceover(
            f"A call struck at one hundred and sixty pays in the normal tail, about one and a half percent of these draws. Importance sampling shifts the normal and applies the exact likelihood ratio. The expectation is preserved when support and integrability conditions hold. <bookmark mark='a'/> These are empirical variance ratios from four hundred thousand common normals on a finite grid. The strike-centred shift gives a ratio of {s['ratio_strike']:.0f}; the best tested shift, {s['theta_best']:.2f}, gives {s['ratio_best']:.0f}. This is not an exact global optimum. <bookmark mark='b'/> At shift five the recorded ratio is {s['ratio_5']:.1f}; at more extreme shifts it collapses. The full curve is shown, including ratios below one. Very rare large weights can be missed, so a favourable sample ratio is not an accuracy guarantee. The tiny weight effective sample size is a warning about the proposal, rather than a payoff-specific error bar."
        ) as vo:
            self.play(FadeIn(top), Create(p), FadeIn(reg), FadeIn(tag), FadeIn(src))
            vo.wait_until("a")
            self.play(FadeIn(bot), FadeIn(one), FadeIn(q), FadeIn(trace), FadeIn(rd))
            self.play(t.animate.set_value(s["theta_best"]), run_time=4, rate_func=linear)
            vo.wait_until("b")
            self.play(t.animate.set_value(7.0), run_time=max(vo.remaining(0.5), 2.5), rate_func=linear)
        for x in (q, trace, rd):
            x.clear_updaters()
        self.wait(0.4)
        self.clear_scene()

    def proof(self):
        rows = [
            cmath(r"\mathbb{E}_p[f]", r"=", r"\mathbb{E}_q\Big[f\,\frac{p}{q}\Big]", font_size=38, colors={r"\mathbb{E}_p[f]": OPT}),
            cmath(r"\operatorname{Var}_q", r"=", r"\mathbb{E}_p\Big[f^2\,\frac{p}{q}\Big] - (\mathbb{E}_p f)^2,\qquad "
                  r"q^* \propto |f|\,p", font_size=34),
            cmath(r"\frac{p}{q_\theta}(z)", r"=", r"e^{-\theta z + \theta^2/2},\qquad m(\theta) = "
                  r"\mathbb{E}\big[f(Z)^2 e^{-\theta Z + \theta^2/2}\big]\ \text{convex}", font_size=32),
            cmath(r"\theta_{k+1}", r"=", r"\frac{\mathbb{E}_{\theta_k}[f\,w\,Z]}{\mathbb{E}_{\theta_k}[f\,w]}", font_size=36,
                  colors={r"\theta_{k+1}": GOOD}),
            cmath(r"\text{ESS}", r"=", r"\frac{(\sum w_i)^2}{\sum w_i^2},\qquad \mathbb{E}_q w^2 = e^{\theta^2}", font_size=34,
                  colors={r"\text{ESS}": BAD}),
        ]
        whys = [why(r"multiply and divide by $q$ (with $q > 0$ wherever $fp \ne 0$): any sampling density, reweighted"),
                why(r"by Cauchy--Schwarz the best $q$ is the payoff times the density, normalised: zero variance if "
                    r"$f \ge 0$, but it needs the answer; it says where to look"),
                why(r"for this nonzero call, the finite second moment is strictly log-convex and coercive: a unique minimiser; "
                    r"convexity alone would not establish uniqueness or existence"),
                why(r"cross-entropy (Rubinstein 1997): maximise $\mathbb{E}_{\theta_k}[f\,w\log q_\theta]$; for normals "
                    r"the maximiser is a weighted mean"),
                why(r"weight ESS is not payoff-specific; for representative iid draws, ESS$/n \to e^{-\theta^2}$")]
        step = ladder(self, rows, whys, keep=4, top=3.2, x=-1.3, buff=0.42, edge=6.9)
        with self.voiceover(
            "Multiply and divide by a proposal density positive wherever payoff times the original density is nonzero, with the required moments finite. <bookmark mark='a'/> Cauchy–Schwarz gives a variance-minimising density proportional to absolute payoff times density. Its variance is zero for a constant-sign payoff, but normalising it requires the unknown integral. <bookmark mark='b'/> For this nonzero call and a normal shift, the second moment is strictly log-convex and coercive, giving a unique minimiser. Convexity alone would not be enough. <bookmark mark='c'/> Cross-entropy instead fits the payoff-weighted target density by a Kullback–Leibler criterion. For a normal proposal this yields a weighted mean. It is a different objective from variance minimisation. <bookmark mark='d'/> Weight effective sample size has population fraction exponential minus theta squared, provided independent proposal draws represent the weight distribution. It measures weight concentration, not the precision of every payoff estimate."
        ) as vo:
            for i, mk in enumerate("abcd"):
                step(i)
                vo.wait_until(mk)
            step(4)
        self.wait(0.4)
        self.clear_scene()

    def learn(self, s, m):
        th = np.asarray(s["theta"])
        lr = np.log10(np.asarray(s["ratio"]))
        yr = data_range(lr, [0])
        g = axes([0, 7], yr, x_length=7.0, y_length=4.0, xlabel=r"shift $\theta$",
                 ylabel=r"variance divided by (log scale)", xticks=[0, 1, 2, 3, 4, 5, 6, 7], yticks=[0, 1, 2],
                 yfmt=lambda v: f"10^{{{int(v)}}}", font_size=15).to_edge(LEFT, buff=0.7).shift(DOWN * 0.3)
        ax = g.ax
        cur = curve(ax, th, lr, OPT, stroke_width=3)
        strike = DashedLine(ax.c2p(s["theta_strike"], yr[0]), ax.c2p(s["theta_strike"], yr[1]), stroke_color=GREY_B,
                            stroke_width=1.5)
        ce = [np.asarray(x) for x in s["ce"]]
        cols = [QC.GAIN, QC.DELTA, QC.THETA, QC.Q, QC.SPOT]

        def y(t_):
            return float(np.interp(t_, th, lr))

        hops = []
        for k in range(1, 3):
            hops.append(VGroup(*[Arrow(ax.c2p(c[k - 1], y(c[k - 1])), ax.c2p(c[k], y(c[k])), buff=0.05, stroke_width=2,
                                       color=cols[j], tip_length=0.12) for j, c in enumerate(ce)]))
        dots = [VGroup(*[Dot(ax.c2p(c[k], y(c[k])), radius=0.06, color=cols[j]) for j, c in enumerate(ce)])
                for k in range(3)]
        lo1, hi1 = min(c[1] for c in ce), max(c[1] for c in ce)
        lo2, hi2 = min(c[2] for c in ce), max(c[2] for c in ce)
        d = m["deep"]
        side = VGroup(
            MathTex(rf"\theta_1 \in [{lo1:.2f}, {hi1:.2f}],\ \ \theta_2 \in [{lo2:.2f}, {hi2:.2f}]", font_size=28, color=GOOD),
            MathTex(rf"\text{{best tested shift:}}\ {s['theta_best']:.2f};\ \ \text{{strike-centred:}}\ {s['theta_strike']:.2f}",
                    font_size=26, color=GREY_A),
            MathTex(rf"\text{{s.e.}}\ {d['plain_se']:.4f} \to {d['is_se']:.5f}\ \ (10^5\ \text{{paths}})", font_size=28, color=OPT),
            wrapped_label(r"Glasserman, Heidelberger and Shahabuddin (1999): for a path-dependent payoff, shift the whole "
                          r"Brownian path along the most likely route to the payoff (a saddle point), then stratify along it. "
                          r"Part 5 did this shift as Girsanov's theorem; Part 40 uses it for tail risk", 5.0, 18, GREY_A),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.28).to_edge(RIGHT, buff=0.35)
        q = predict(r"Shift the normal far beyond the strike. What happens to the error?", width=4.6, font_size=21)
        q.to_corner(DR, buff=0.3)  # the lower left holds the chart axis
        src = illustration(r"cross-entropy from $\theta_0 = 0$, 20{,}000 draws per step, five seeds", corner=UR)
        with self.voiceover(
            f"Five pilot seeds start at zero shift. <bookmark mark='a'/> One cross-entropy update lands between {lo1:.2f} and {hi1:.2f}; <bookmark mark='b'/> the second between {lo2:.2f} and {hi2:.2f}. The payoff evaluation includes the strike. What is learned is a useful shift without knowing its optimal value in advance. Cross-entropy minimises a divergence, so it need not find the variance optimum. Freeze the learned proposal and use an independent production sample to retain ordinary conditional unbiasedness. <bookmark mark='c'/> In the separate fixed-shift House example, the estimated standard error changes from {d['plain_se']:.4f} to {d['is_se']:.5f}. This is a case-specific sampling comparison, with pilot work and rare-weight uncertainty considered separately. For path-dependent payoffs, a useful proposal may shift the whole Brownian path toward a likely paying route. Shift too far and the error can grow. Next, spread points more evenly."
        ) as vo:
            self.play(FadeIn(g), Create(cur), FadeIn(strike), FadeIn(src), FadeIn(dots[0]), FadeIn(q))
            vo.wait_until("a")
            self.play(*[GrowArrow(a) for a in hops[0]], FadeIn(dots[1]), run_time=1.5)
            vo.wait_until("b")
            self.play(*[GrowArrow(a) for a in hops[1]], FadeIn(dots[2]), FadeIn(side[0]), FadeIn(side[1]), run_time=1.5)
            vo.wait_until("c")
            self.play(FadeIn(side[2]), FadeIn(side[3]))
        self.wait(0.5)
        self.clear_scene()

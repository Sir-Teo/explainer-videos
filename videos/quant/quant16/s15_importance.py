from __future__ import annotations

import numpy as np
from scipy.stats import norm

from explainer.quant import *  # noqa: F403
from videos.quant.quant16.common import BAD, GOOD, OPT, PART, SPOT, illustration, load, predict


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
        reg = ta.get_area(ta.plot(lambda x: norm.pdf(x), x_range=[zs, 8]), x_range=[zs, 8], color=BAD, opacity=0.5)
        t = ValueTracker(0.0)
        q = always_redraw(lambda: curve(ta, xs, norm.pdf(xs - t.get_value()), OPT, stroke_width=3))
        bot = axes([0, 7], [-0.5, 2.5], x_length=8.2, y_length=2.6, xlabel=r"shift $\theta$",
                   ylabel=r"variance divided by (log scale)", xticks=[0, 1, 2, 3, 4, 5, 6, 7], yticks=[0, 1, 2],
                   yfmt=lambda v: f"10^{{{int(v)}}}", font_size=15)
        bot.next_to(top, DOWN, buff=0.5).align_to(top, LEFT)
        ba = bot.ax
        one = DashedLine(ba.c2p(0, 0), ba.c2p(7, 0), stroke_color=GREY_C, stroke_width=1.5)
        lr = np.log10(np.maximum(ratio, 10 ** -0.5))

        def make():
            k = int(np.searchsorted(th, t.get_value(), side="right"))
            k = max(k, 2)
            return VMobject(stroke_color=OPT, stroke_width=3).set_points_as_corners(
                [ba.c2p(a, np.clip(b, -0.5, 2.5)) for a, b in zip(th[:k], lr[:k])])

        trace = always_redraw(make)

        def at(arr):
            return float(np.interp(t.get_value(), th, arr))

        rd = always_redraw(lambda: VGroup(
            MathTex(rf"\theta = {t.get_value():.2f}", font_size=30, color=OPT),
            MathTex(rf"\text{{variance}} \div {at(ratio):.1f}", font_size=28, color=GOOD if at(ratio) > 1 else BAD),
            MathTex(rf"\text{{ESS}}/n = {at(ess):.4f}", font_size=28, color=GREY_A),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.18).to_edge(RIGHT, buff=0.4).shift(UP * 0.8))
        tag = label(rf"the payoff lives here: $z > {zs:.2f}$ ({100 * s['share_in_money']:.1f}\% of draws)", font_size=18,
                    color=BAD).next_to(ta.c2p(zs + 0.2, 0.3), RIGHT, buff=0.1)
        src = illustration(r"a call struck at 160 (one year, 20\% volatility); 400{,}000 normals at every shift")
        with self.voiceover(
            "A call struck at a hundred and sixty pays only when the driving normal exceeds 2.2: in about one and a "
            "half percent of draws. Plain Monte Carlo wastes the rest. Importance sampling draws from a different "
            "density, here the same normal shifted by theta, and reweights every path so the answer is unchanged. "
            "<bookmark mark='a'/> Slide the shift and watch the variance. Moving toward the payoff helps enormously: "
            f"centred on the strike, as the House does, the variance falls {s['ratio_strike']:.0f} times, and the best "
            f"shift, near {s['theta_best']:.2f}, gives {s['ratio_best']:.0f}. <bookmark mark='b'/> Keep going and it "
            f"turns: at five the gain is down to {s['ratio_5']:.1f}, and beyond about six the shifted estimate is worse "
            "than doing nothing. A handful of paths now carry enormous weights, and the effective sample size collapses."
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
                why(r"the ratio of two normals; the second moment is convex in $\theta$ (log-convex), so there is one "
                    r"best shift"),
                why(r"cross-entropy (Rubinstein 1997): maximise $\mathbb{E}_{\theta_k}[f\,w\log q_\theta]$; for normals "
                    r"the maximiser is a weighted mean"),
                why(r"the effective sample size: with the shift far from the payoff a few weights dominate")]
        step = ladder(self, rows, whys, keep=4, top=2.9, x=-1.3, buff=0.55, edge=6.9)
        with self.voiceover(
            "The theory, in five lines. Multiply and divide by the sampling density: the expectation is unchanged, "
            "with the likelihood ratio as weight. <bookmark mark='a'/> The variance under the new density has a "
            "minimiser, the payoff times the old density, normalised. It would have zero variance, and it needs the "
            "answer to build, but it says where to look: where payoff times probability is large. "
            "<bookmark mark='b'/> For a shifted normal the ratio is an exponential, and the second moment is convex in "
            "the shift, so there is exactly one best shift. <bookmark mark='c'/> We can learn it. The cross-entropy "
            "method moves the shift to the payoff-weighted mean of the draws, and repeats. "
            "<bookmark mark='d'/> And the warning sign of going too far is the effective sample size, which falls "
            "like e to the minus theta squared."
        ) as vo:
            for i, mk in enumerate("abcd"):
                step(i)
                vo.wait_until(mk)
            step(4)
        self.wait(0.4)
        self.clear_scene()

    def learn(self, s, m):
        th = np.asarray(s["theta"])
        lr = np.log10(np.maximum(np.asarray(s["ratio"]), 10 ** -0.5))
        g = axes([0, 7], [-0.5, 2.5], x_length=7.0, y_length=4.0, xlabel=r"shift $\theta$",
                 ylabel=r"variance divided by (log scale)", xticks=[0, 1, 2, 3, 4, 5, 6, 7], yticks=[0, 1, 2],
                 yfmt=lambda v: f"10^{{{int(v)}}}", font_size=15).to_edge(LEFT, buff=0.7).shift(DOWN * 0.3)
        ax = g.ax
        cur = curve(ax, th, np.clip(lr, -0.5, 2.5), OPT, stroke_width=3)
        strike = DashedLine(ax.c2p(s["theta_strike"], -0.5), ax.c2p(s["theta_strike"], 2.5), stroke_color=GREY_B,
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
            MathTex(rf"\text{{variance-optimal:}}\ {s['theta_best']:.2f};\ \ \text{{strike-centred:}}\ {s['theta_strike']:.2f}",
                    font_size=26, color=GREY_A),
            MathTex(rf"\text{{s.e.}}\ {d['plain_se']:.4f} \to {d['is_se']:.5f}\ \ (10^5\ \text{{paths}})", font_size=28, color=OPT),
            wrapped_label(r"Glasserman, Heidelberger and Shahabuddin (1999): for a path-dependent payoff, shift the whole "
                          r"Brownian path along the most likely route to the payoff (a saddle point), then stratify along it. "
                          r"Part 5 did this shift as Girsanov's theorem; Part 40 uses it for tail risk", 5.0, 18, GREY_A),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.28).to_edge(RIGHT, buff=0.35)
        q = predict(r"Shift the normal far beyond the strike. What happens to the error?", width=4.6, font_size=21)
        q.to_corner(DL, buff=0.3)
        src = illustration(r"cross-entropy from $\theta_0 = 0$, 20{,}000 draws per step, five seeds", corner=UR)
        with self.voiceover(
            "Here is the estimator learning its own sampling law. Five seeds start at zero shift. "
            f"<bookmark mark='a'/> One cross-entropy step lands every seed between {lo1:.2f} and {hi1:.2f}; "
            f"<bookmark mark='b'/> a second, between {lo2:.2f} and {hi2:.2f}. Two steps, and no knowledge of "
            "the strike. It lands a little past the variance optimum, because cross-entropy minimises a different "
            "criterion, a divergence rather than the variance, but on this flat top the cost is negligible. "
            "<bookmark mark='c'/> The House's fixed shift turned a standard error of "
            f"{d['plain_se']:.4f} into {d['is_se']:.5f}, worth a hundred times the paths. For whole paths, Glasserman, "
            "Heidelberger and Shahabuddin shift along the most likely route to the payoff. And the pause-and-predict "
            "answer you have already seen: shift too far, and the error grows."
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

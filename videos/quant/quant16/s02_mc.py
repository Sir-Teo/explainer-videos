from __future__ import annotations

import numpy as np

from explainer.quant import *  # noqa: F403
from videos.quant.quant16.common import BAD, GOOD, METHOD_COL, OPT, PART, illustration, load, loglog


class MC(VoiceoverScene):
    def construct(self):
        m = load("mc")
        self.card()
        self.rate(m)
        self.reduce(m)
        self.importance(m)

    def card(self):
        c = chapter_card(1, r"Monte Carlo, and variance reduction", r"How many paths for a price to one basis point?",
                         part=PART)
        with self.voiceover("Chapter one. Monte Carlo, and variance reduction."):
            self.play(FadeIn(c[0], shift=UP * 0.2), FadeIn(c[1]))
        self.play(FadeOut(c))

    def rate(self, m):
        rows = [cmath(r"\hat V_n", r"=", r"\frac{e^{-rT}}{n}\sum_{i=1}^n f\big(S^{(i)}_T\big),\qquad "
                      r"\text{error} \approx \frac{\sigma_f}{\sqrt n}", font_size=36, colors={r"\hat V_n": OPT})]
        whys = [why(r"Boyle (1977): a price is an expectation, so average simulated payoffs; the central limit theorem gives "
                    r"the error, and it falls only like one over the square root of the number of paths, in any dimension")]
        step = ladder(self, rows, whys, keep=1, top=2.2, x=-0.6, buff=1.0, edge=6.9)
        sd = m["rmse"]["plain"][0] * np.sqrt(m["ns"][0])
        bp = 0.0001 * m["exact"] * 100 / 100
        need = (sd / (0.01)) ** 2
        foot = wrapped_label(rf"for this call (price {m['exact']:.2f}), the payoff's standard deviation is about {sd:.0f}: an "
                             rf"error of one cent needs about {need / 1e6:.0f} million paths. Ten times the accuracy costs a "
                             r"hundred times the work", 11.0, 21, GREY_A).to_edge(DOWN, buff=0.8)
        with self.voiceover(
            "Phelim Boyle pointed out in 1977 that a price is an expectation, so it can be estimated by averaging "
            "simulated payoffs. The error follows from the central limit theorem: the payoff's standard deviation, "
            "over the square root of the number of paths. It does not care how many dimensions the problem has, "
            "which is why Monte Carlo wins for path-dependent and many-asset products. <bookmark mark='a'/> But it "
            f"converges slowly. For a one-year at-the-money call, an error of one cent needs about "
            f"{need / 1e6:.0f} million paths, and ten times the accuracy costs a hundred times the work."
        ) as vo:
            step(0)
            vo.wait_until("a")
            self.play(FadeIn(foot))
        self.wait(0.4)
        self.clear_scene()

    def reduce(self, m):
        ns = np.log10(np.asarray(m["ns"], float))
        g = loglog(3, 5.5, -5, 0, r"paths", r"root-mean-square error", xt=[3, 4, 5], yt=[-4, -3, -2, -1, 0])
        g.to_edge(LEFT, buff=0.8).shift(DOWN * 0.2)
        ax = g.ax
        lines = VGroup()
        names = [("plain", r"plain"), ("antithetic", r"antithetic pairs"), ("control", r"control variate: the stock"),
                 ("sobol", r"Sobol points (quasi-Monte Carlo)")]
        for key, _ in names:
            y = np.log10(np.asarray(m["rmse"][key]))
            pts = [ax.c2p(a, np.clip(b, -5, 0)) for a, b in zip(ns, y)]
            lines.add(VGroup(VMobject(stroke_color=METHOD_COL[key], stroke_width=3).set_points_as_corners(pts),
                             *[Dot(p_, radius=0.05, color=METHOD_COL[key]) for p_ in pts]))
        leg = legend([(METHOD_COL[k], t) for k, t in names], font_size=17).next_to(g, RIGHT, buff=0.3).align_to(g, UP)
        r = {k: m["rmse"][k][-1] for k in m["rmse"]}
        side = VGroup(
            wrapped_label(r"antithetics pair every path with its mirror; the stock is a control variate because its price "
                          r"is known exactly; Sobol points fill the space evenly instead of at random", 4.2, 18, GREY_A),
            wrapped_label(rf"at the largest size: plain {r['plain']:.4f}, control variate {r['control']:.4f}, Sobol "
                          rf"{r['sobol']:.5f}. Same slope for the first three; Sobol's is steeper, close to $1/n$", 4.2, 18,
                          WHITE),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.3).next_to(leg, DOWN, buff=0.4).align_to(leg, LEFT)
        src = illustration(r"one-year at-the-money call, 20\% volatility, 5\% rates; 20 runs at each size")
        with self.voiceover(
            "The art is in making the constant smaller. Here is the error against the number of paths, on log "
            "scales, for plain Monte Carlo: a line of slope minus a half. <bookmark mark='a'/> Pair every path with "
            "its mirror image, and the line drops a little. Use the stock as a control variate, since its expected "
            "discounted value is known exactly, and it drops further. Both keep the slope. <bookmark mark='b'/> "
            "Sobol points, which fill the space evenly instead of at random, change the slope itself: in one dimension "
            "the error falls almost like one over n."
        ) as vo:
            self.play(FadeIn(g), FadeIn(src), Create(lines[0]), FadeIn(leg[0]))
            vo.wait_until("a")
            self.play(Create(lines[1]), FadeIn(leg[1]), Create(lines[2]), FadeIn(leg[2]), FadeIn(side[0]), run_time=2)
            vo.wait_until("b")
            self.play(Create(lines[3]), FadeIn(leg[3]), FadeIn(side[1]))
        self.wait(0.4)
        self.clear_scene()

    def importance(self, m):
        d = m["deep"]
        rows = [cmath(r"\mathbb{E}\big[f(Z)\big]", r"=", r"\mathbb{E}\Big[f(Z + \theta)\,e^{-\theta Z - \theta^2/2}\Big]",
                      font_size=38, colors={r"\mathbb{E}\big[f(Z)\big]": OPT})]
        whys = [why(r"importance sampling: draw from a shifted normal that lands where the payoff lives, and reweight by the "
                    r"likelihood ratio so the answer is unchanged")]
        step = ladder(self, rows, whys, keep=1, top=2.0, x=-0.6, buff=1.0, edge=6.9)
        stats = VGroup(
            MathTex(rf"K = {d['K']:.0f}:\ \ \text{{price}}\ {d['exact']:.3f},\ \ \text{{paid in}}\ {100 * d['share_in_money']:.1f}\%"
                    r"\ \text{of paths}", font_size=30),
            MathTex(rf"\text{{standard error: plain}}\ {d['plain_se']:.4f} \to \text{{shifted}}\ {d['is_se']:.4f}", font_size=30,
                    color=GOOD),
        ).arrange(DOWN, buff=0.3).move_to(DOWN * 0.8)
        foot = wrapped_label(rf"{d['plain_se'] / d['is_se']:.0f} times less noise, as if with "
                             rf"{(d['plain_se'] / d['is_se']) ** 2:.0f} times the paths; the same idea prices credit "
                             r"tails and risk measures (Part 31)", 11.0, 20, GREY_A).to_edge(DOWN, buff=0.7)
        with self.voiceover(
            "One more trick, for rare events. A call struck at 160 pays in only "
            f"{100 * d['share_in_money']:.1f} percent of paths, so almost every simulated path is wasted. "
            "<bookmark mark='a'/> Importance sampling draws from a normal shifted toward the strike, where the payoff "
            "lives, and reweights each path by the likelihood ratio so the answer is unchanged. The standard error "
            f"falls from {d['plain_se']:.4f} to {d['is_se']:.4f}: "
            f"{d['plain_se'] / d['is_se']:.0f} times less noise, as if you had run "
            f"{(d['plain_se'] / d['is_se']) ** 2:.0f} times as many paths."
        ) as vo:
            step(0)
            vo.wait_until("a")
            self.play(FadeIn(stats), FadeIn(foot))
        self.wait(0.4)
        self.clear_scene()

from __future__ import annotations

import numpy as np

from explainer.quant import *  # noqa: F403
from explainer.quant.house import vol
from videos.quant.quant7.common import ALT, BAD, FC, GOOD, PART, RET, VOL, load, real_data


class Zoo(VoiceoverScene):
    def construct(self):
        gl = load("garch_lik")
        g = load("garch")
        self.card()
        self.plane(gl, g)
        self.derive()
        self.news(g)
        self.tails(gl)

    def card(self):
        c = chapter_card(7, r"The GARCH zoo", r"Stationarity, fat tails and asymmetry", part=PART)
        with self.voiceover("Chapter seven. Stationarity, fat tails and asymmetry: the GARCH zoo."):
            self.play(FadeIn(c[0], shift=UP * 0.2), FadeIn(c[1]))
        self.play(FadeOut(c))

    def plane(self, gl, g):
        gp = axes([0, 0.6], [0, 1.4], x_length=6.0, y_length=5.6, xticks=[0, 0.2, 0.4, 0.6], yticks=[0, 0.5, 1.0],
                  xlabel=r"$\alpha$", ylabel=r"$\beta$", font_size=18).to_edge(LEFT, buff=0.7).shift(DOWN * 0.1)
        ax = gp.ax
        tri = Polygon(ax.c2p(0, 0), ax.c2p(0.6, 0), ax.c2p(0.6, 0.4), ax.c2p(0, 1.0), stroke_width=0, fill_color=GOOD,
                      fill_opacity=0.25)
        ig = Line(ax.c2p(0, 1.0), ax.c2p(0.6, 0.4), color=GOOD, stroke_width=3)
        na, nb = np.asarray(gl["nelson_a"]), np.asarray(gl["nelson_b"])
        m = nb <= 1.4
        nel = curve(ax, na[m], nb[m], BAD, stroke_width=4)
        strict = VMobject(stroke_width=0, fill_color=BAD, fill_opacity=0.15).set_points_as_corners(
            [ax.c2p(0, 1.0)] + [ax.c2p(a, b) for a, b in zip(na[m], nb[m])] + [ax.c2p(0.6, 0.4), ax.c2p(0, 1.0)])
        l1 = label(r"$\alpha + \beta < 1$: finite variance", font_size=19, color=GOOD).move_to(ax.c2p(0.22, 0.35))
        l2 = label(r"strictly stationary, infinite variance", font_size=19, color=BAD).move_to(ax.c2p(0.33, 1.08)).rotate(-0.42)
        l3 = label(r"$\mathbb{E}\ln(\alpha z^2 + \beta) = 0$ (Nelson 1990)", font_size=19, color=BAD).next_to(ax.c2p(0.42, 0.98), UR, buff=0.05)
        us, btc = gl["us"], gl["btc"]
        d1 = Dot(ax.c2p(us[1], us[2]), radius=0.08, color=FC)
        d2 = Dot(ax.c2p(btc[1], btc[2]), radius=0.08, color=ALT)
        t1 = label(r"US stocks", font_size=18, color=FC).next_to(d1, RIGHT, buff=0.1)
        t2 = label(r"Bitcoin", font_size=18, color=ALT).next_to(d2, RIGHT, buff=0.1)
        q1, q2 = Dot(ax.c2p(0.3, 0.75), radius=0.07, color=WHITE), Dot(ax.c2p(0.25, 0.80), radius=0.07, color=WHITE)
        pc = pause_card(r"$\alpha = 0.30$, $\beta = 0.75$: the sum is 1.05. Does the variance explode? And at "
                        r"$\alpha = 0.25$, $\beta = 0.80$?", width=5.4, font_size=21).to_edge(RIGHT, buff=0.4).shift(UP * 1.6)
        ans = VGroup(MathTex(rf"\mathbb{{E}}\ln(0.30z^2 + 0.75) = {gl['e_03_075']:+.4f}", font_size=28, color=GOOD),
                     MathTex(rf"\mathbb{{E}}\ln(0.25z^2 + 0.80) = {gl['e_025_080']:+.4f}", font_size=28, color=BAD),
                     label(r"Gauss--Hermite quadrature, $z \sim N(0,1)$", font_size=17, color=GREY_B))
        ans.arrange(DOWN, aligned_edge=LEFT, buff=0.15).next_to(pc, DOWN, buff=0.35)
        s1 = gl["e_03_075"] < 0
        s2 = gl["e_025_080"] < 0
        verdict = ("The first is negative: the process is strictly stationary, it settles into a distribution, just "
                   "one with infinite variance. The second is positive: it explodes. The same sum, opposite fates."
                   if s1 and not s2 else "Both come out on the same side of zero here.")
        with self.voiceover(
            "Every GARCH is a point on this plane. Below the line alpha plus beta equal to one, the variance is finite "
            "and the forecasts revert. <bookmark mark='a'/> The American market sits just under the line, Bitcoin a "
            "little further in. <bookmark mark='b'/> What happens above it? Daniel Nelson showed in 1990 that the "
            "variance need not explode. The process settles down whenever the average of the log of alpha z squared "
            "plus beta is negative, and that boundary, in red, lies beyond the line. <bookmark mark='c'/> Pause and "
            "predict. Alpha zero point three and beta zero point seven five add up to one point zero five; so do "
            "zero point two five and zero point eight. Does either explode? <bookmark mark='d'/> " + verdict
        ) as vo:
            self.play(FadeIn(gp), FadeIn(tri), Create(ig), FadeIn(l1))
            vo.wait_until("a")
            self.play(GrowFromCenter(d1), FadeIn(t1), GrowFromCenter(d2), FadeIn(t2))
            vo.wait_until("b")
            self.play(Create(nel), FadeIn(strict), FadeIn(l2), FadeIn(l3), run_time=2)
            vo.wait_until("c")
            self.play(FadeIn(pc), FadeIn(q1), FadeIn(q2))
            vo.wait_until("d")
            self.play(FadeIn(ans))
        self.wait(0.3)
        self.clear_scene()

    def derive(self):
        rows = [
            cmath(r"\sigma_t^2", r"=", r"\omega\sum_{k\ge0}\prod_{j=1}^{k}(\alpha z_{t-j}^2 + \beta)", font_size=34),
            cmath(r"\tfrac1k\ln\prod_{j\le k}(\alpha z^2 + \beta)", r"\to", r"\mathbb{E}\ln(\alpha z^2 + \beta)", font_size=34),
            cmath(r"\mathbb{E}\ln(\alpha z^2 + \beta)", r"<", r"\ln\mathbb{E}(\alpha z^2 + \beta) = \ln(\alpha + \beta)", font_size=34),
            cmath(r"\mathbb{E}\Big[\frac{\partial\ell_t}{\partial\theta}\Big]", r"=",
                  r"\tfrac12\mathbb{E}\Big[(z_t^2 - 1)\frac{\partial\ln\sigma_t^2}{\partial\theta}\Big] = 0", font_size=34),
            cmath(r"\sigma_t^2", r"=", r"\omega + (\alpha + \gamma\mathbf{1}_{r_{t-1}<0})\,r_{t-1}^2 + \beta\sigma_{t-1}^2", font_size=34),
            cmath(r"\ln\sigma_t^2", r"=", r"\omega + \alpha(|z_{t-1}| - \mathbb{E}|z|) + \gamma z_{t-1} + \beta\ln\sigma_{t-1}^2",
                  font_size=34),
        ]
        whys = [why(r"unroll the recursion with $r_{t-1}^2 = \sigma_{t-1}^2 z_{t-1}^2$"),
                why(r"the law of large numbers: the product shrinks geometrically iff the limit is negative (Nelson 1990)"),
                why(r"Jensen: so IGARCH, $\alpha + \beta = 1$, is strictly stationary"),
                why(r"the score has mean zero whenever $\mathbb{E}z^2 = 1$, Gaussian or not: QMLE (Bollerslev--Wooldridge 1992)"),
                why(r"GJR (Glosten, Jagannathan, Runkle 1993): falls add $\gamma$; persistence $\alpha + \gamma/2 + \beta$"),
                why(r"EGARCH (Nelson 1991): the log variance, so no positivity constraints; $\gamma < 0$ for asymmetry")]
        step = ladder(self, rows, whys, keep=3, top=3.1, x=-1.8, buff=0.5, edge=6.9)
        with self.voiceover(
            "Why. Unroll the recursion: the variance is omega times a sum of products of random factors. <bookmark "
            "mark='a'/> By the law of large numbers, a long product behaves like the exponential of k times the "
            "average log factor, so the sum converges exactly when that average is negative. <bookmark mark='b'/> By "
            "Jensen's inequality the average log is below the log of the average, so even integrated GARCH, alpha "
            "plus beta equal to one, is strictly stationary. <bookmark mark='c'/> A second result makes GARCH usable "
            "on real data: the Gaussian likelihood's score has mean zero whenever the shocks have unit variance, "
            "whatever their shape. So the estimates stay consistent under fat tails, with sandwich standard errors: "
            "Tim Bollerslev and Jeffrey Wooldridge, 1992. <bookmark mark='d'/> And two members of the zoo give bad "
            "news its own weight: GJR adds a term only after falls, <bookmark mark='e'/> and Nelson's EGARCH models "
            "the log of the variance, with a signed term."
        ) as vo:
            step(0)
            vo.wait_until("a")
            step(1)
            vo.wait_until("b")
            step(2)
            vo.wait_until("c")
            step(3)
            vo.wait_until("d")
            step(4)
            vo.wait_until("e")
            step(5)
        self.wait(0.3)
        self.clear_scene()

    def news(self, g):
        us = g["us"]
        pg, pj, pe = (np.asarray(us[k]["params"]) for k in ("garch", "gjr", "egarch"))
        h = pg[0] / (1 - pg[1] - pg[2])
        rr = np.linspace(-0.05, 0.05, 121)
        curves = {k: vol.news_impact(p, k, rr, h) for k, p in (("garch", pg), ("gjr", pj), ("egarch", pe))}
        hi = float(max(c.max() for c in curves.values())) * 1.05
        gp = axes([-0.05, 0.05], [0, hi], x_length=6.4, y_length=4.4, xlabel=r"today's return",
                  ylabel=r"tomorrow's variance (news impact, today's variance at its long-run level)",
                  xticks=[-0.04, -0.02, 0, 0.02, 0.04], xfmt=lambda u: f"{100 * u:+.0f}\\%" if u else "0", yticks=[],
                  font_size=16).to_edge(LEFT, buff=0.7).shift(DOWN * 0.2)
        ax = gp.ax
        line = curve(ax, rr, curves["garch"], VOL, stroke_width=4)
        name = label(r"GARCH: symmetric", font_size=24, color=VOL).to_corner(UR, buff=0.5)
        a, gam = pj[1], pj[2]
        side = VGroup(
            MathTex(rf"\text{{GJR: }}\alpha = {a:.3f},\ \gamma = {gam:.3f}", font_size=28, color=BAD),
            label(rf"a fall raises tomorrow's variance {(a + gam) / a:.1f} times as much as a rise", font_size=21, color=GREY_A),
            MathTex(rf"\log L:\ {us['garch']['loglik']:,.0f}\ \to\ {us['gjr']['loglik']:,.0f}\ (\text{{GJR}}),\ "
                    rf"{us['egarch']['loglik']:,.0f}\ (\text{{EGARCH}})".replace(",", "{,}"), font_size=24, color=GREY_A),
            label(rf"Bitcoin: GJR $\gamma = {g['btc']['gjr_gamma']:.2f}$: no balance sheet, the same asymmetry", font_size=20, color=ALT),
            wrapped_label(r"the leverage effect (Black 1976); news-impact curves (Engle and Ng 1993); GARCH-in-mean "
                          r"puts the variance in the expected return (Engle, Lilien and Robins 1987): Part 23", 5.2, 18, GREY_B),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.22).to_edge(RIGHT, buff=0.4).shift(DOWN * 0.4)
        with self.voiceover(
            "Draw tomorrow's variance against today's return: the news-impact curve. For GARCH it is a symmetric "
            "parabola: a fall and a rise of the same size count the same. <bookmark mark='a'/> Markets disagree. Fischer "
            "Black noticed in 1976 that volatility rises more after falls. Fit GJR to the American market and the "
            f"parabola tilts: a fall raises tomorrow's variance {(a + gam) / a:.0f} times as much as a rise. <bookmark "
            "mark='b'/> EGARCH, working in logs, bends it differently, and both fit far better than the symmetric "
            "model. <bookmark mark='c'/> Bitcoin, with no corporate leverage behind it, shows the same tilt: the effect "
            "is about fear as much as balance sheets."
        ) as vo:
            self.play(FadeIn(gp), Create(line), FadeIn(name))
            vo.wait_until("a")
            n2 = label(r"GJR: falls count more", font_size=24, color=BAD).move_to(name)
            self.play(Transform(line, curve(ax, rr, curves["gjr"], BAD, stroke_width=4)), Transform(name, n2),
                      FadeIn(side[0]), FadeIn(side[1]), run_time=2)
            vo.wait_until("b")
            n3 = label(r"EGARCH: the log variance", font_size=24, color=FC).move_to(name)
            ghost = curve(ax, rr, curves["gjr"], BAD, stroke_width=2).set_stroke(opacity=0.4)
            self.add(ghost)
            self.play(Transform(line, curve(ax, rr, curves["egarch"], FC, stroke_width=4)), Transform(name, n3),
                      FadeIn(side[2]), run_time=2)
            vo.wait_until("c")
            self.play(FadeIn(side[3]), FadeIn(side[4]))
        self.wait(0.3)
        self.clear_scene()

    def tails(self, gl):
        qq = gl["qq"]
        emp, nor, tt = (np.asarray(qq[k]) for k in ("emp", "normal", "t"))
        g = axes([-8, 8], [-8, 8], x_length=4.8, y_length=4.8, xticks=[-6, -3, 0, 3, 6], yticks=[-6, -3, 0, 3, 6],
                 xlabel=r"model quantile", ylabel=r"quantile of $r_t/\hat\sigma_t$ (GARCH residuals)", font_size=15)
        g.to_edge(LEFT, buff=0.8).shift(DOWN * 0.2)
        ax = g.ax
        diag = DashedLine(ax.c2p(-8, -8), ax.c2p(8, 8), color=GREY_B, stroke_width=2)
        dn = VGroup(*[Dot(ax.c2p(x, np.clip(y, -8, 8)), radius=0.035, color=BAD) for x, y in zip(nor, emp)])
        dt = VGroup(*[Dot(ax.c2p(x, np.clip(y, -8, 8)), radius=0.035, color=GOOD) for x, y in zip(tt, emp)])
        tg = gl["t_garch"]
        side = VGroup(
            legend([(BAD, r"against the normal"), (GOOD, rf"against Student-$t$, $\nu = {tg['nu']:.1f}$")], font_size=20),
            MathTex(rf"\text{{kurtosis of } } r_t/\hat\sigma_t = {gl['kurt_z']:.1f}\ \ (\text{{normal: }} 3)", font_size=26, color=GREY_A),
            MathTex(rf"\log L:\ {gl['g_loglik']:,.0f} \to {tg['loglik']:,.0f}".replace(",", "{,}"), font_size=28, color=GOOD),
            label(r"GARCH-$t$ (Bollerslev 1987)", font_size=19, color=GREY_B),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.25).to_edge(RIGHT, buff=0.6)
        with self.voiceover(
            "Last, the tails. Divide each day's return by GARCH's volatility. If the shocks were normal, these "
            "standardized residuals would line up on the diagonal against normal quantiles. <bookmark mark='a'/> They "
            f"don't: the ends curl away, and the kurtosis is {gl['kurt_z']:.1f}, not three. GARCH explains part of the "
            "fat tails of returns, not all of them. <bookmark mark='b'/> Give the shocks a Student-t distribution and "
            f"estimate its degrees of freedom: about {tg['nu']:.0f}. Now the points straighten, and the log-likelihood "
            f"rises by {tg['loglik'] - gl['g_loglik']:,.0f}. The volatility path barely changes; the tails do, and "
            "the tails are what risk managers are paid to get right."
        ) as vo:
            self.play(FadeIn(g), Create(diag))
            vo.wait_until("a")
            self.play(LaggedStart(*[FadeIn(d) for d in dn], lag_ratio=0.01, run_time=2), FadeIn(side[0][0]), FadeIn(side[1]))
            vo.wait_until("b")
            self.play(LaggedStart(*[FadeIn(d) for d in dt], lag_ratio=0.01, run_time=2), FadeIn(side[0][1]),
                      FadeIn(side[2]), FadeIn(side[3]))
        self.wait(0.3)
        self.clear_scene()

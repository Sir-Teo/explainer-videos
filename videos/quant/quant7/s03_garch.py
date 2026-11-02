from __future__ import annotations

import numpy as np

from explainer.quant import *  # noqa: F403
from videos.quant.quant7.common import ALT, BAD, FC, GOOD, PART, RET, VOL, load, real_data


class Garch(VoiceoverScene):
    def construct(self):
        r = load("regimes")
        g = load("garch")
        d = load("dcc")
        self.card()
        self.regimes(r)
        self.garch(g)
        self.leverage(g)
        self.dcc(d)

    def card(self):
        c = chapter_card(2, r"Hidden states and the GARCH family", r"How does volatility remember?", lit=(1982,), part=PART)
        with self.voiceover("Chapter two. Hidden states, and the GARCH family."):
            self.play(FadeIn(c[0], shift=UP * 0.2), FadeIn(c[1]))
        self.play(FadeOut(c))

    def regimes(self, r):
        t, p = np.asarray(r["t"]), np.asarray(r["prob_high"])
        g = axes([1926, 2021], [0, 1], x_length=9.0, y_length=2.6, ylabel=r"probability of the turbulent regime",
                 xticks=[1930, 1960, 1990, 2020], xfmt=lambda u: f"{int(u)}", yticks=[0, 0.5, 1], font_size=16)
        g.to_edge(UP, buff=0.9).to_edge(LEFT, buff=0.6)
        ax = g.ax
        fill = VMobject(stroke_width=0, fill_color=BAD, fill_opacity=0.6)
        pts = [ax.c2p(t[0], 0)] + [ax.c2p(a, b) for a, b in zip(t, p)] + [ax.c2p(t[-1], 0)]
        fill.set_points_as_corners(pts)
        mu, sd, dur = np.asarray(r["mu"]), np.asarray(r["sd"]), np.asarray(r["duration_months"])
        rows = VGroup(
            MathTex(rf"\text{{calm: mean }} {100 * mu[0]:+.0f}\%, \text{{ vol }} {100 * sd[0]:.0f}\%, \text{{ lasts }} "
                    rf"{dur[0]:.0f} \text{{ months}}", font_size=28, color=GOOD),
            MathTex(rf"\text{{turbulent: mean }} {100 * mu[1]:+.0f}\%, \text{{ vol }} {100 * sd[1]:.0f}\%, \text{{ lasts }} "
                    rf"{dur[1]:.0f} \text{{ months}}", font_size=28, color=BAD),
            label(rf"{100 * r['share_high']:.0f}\% of months turbulent; annualised; Hamilton (1989), fitted by EM", font_size=20,
                  color=GREY_B),
            wrapped_label(r"the Kalman filter is the same idea with a continuous hidden state: predict, observe, correct "
                          r"by the gain $P/(P + R)$. It drew the hook's river.", 11.0, 21, GREY_A),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.22).next_to(g, DOWN, buff=0.6).align_to(g, LEFT)
        src = real_data(r"Kenneth French's monthly market excess return, 1926--2020")
        with self.voiceover(
            "Volatility is hidden; we see only its effects. One way to model it is a small number of hidden states. "
            "James Hamilton's model of 1989 lets the economy switch between regimes according to a Markov chain, each "
            "regime with its own mean and volatility. <bookmark mark='a'/> Fitted to American monthly returns since "
            "1926, it finds a calm regime with a positive mean and thirteen percent volatility, lasting about four and "
            "a half years on average, and a turbulent one with a negative mean and thirty-six percent volatility, "
            "lasting about ten months. The turbulent regime lights up the Depression, 1974, 1987, 2008 and 2020. "
            "<bookmark mark='b'/> The Kalman filter does the same with a continuous hidden state, and it drew the "
            "river at the start of this part."
        ) as vo:
            self.play(FadeIn(g), FadeIn(src))
            vo.wait_until("a")
            self.play(FadeIn(fill), run_time=2)
            self.play(FadeIn(rows[0]), FadeIn(rows[1]), FadeIn(rows[2]))
            vo.wait_until("b")
            self.play(FadeIn(rows[3]))
        self.wait(0.4)
        self.clear_scene()

    def garch(self, g):
        us = g["us"]
        w, a, b = us["garch"]["params"]
        rows = [cmath(r"\sigma_t^2", r"=", r"\omega + \alpha\,r_{t-1}^2", font_size=40, colors={r"\sigma_t^2": VOL}),
                cmath(r"\sigma_t^2", r"=", r"\omega + \alpha\,r_{t-1}^2 + \beta\,\sigma_{t-1}^2", font_size=40,
                      colors={r"\sigma_t^2": VOL})]
        whys = [why(r"ARCH (Engle 1982): today's variance responds to yesterday's surprise"),
                why(r"GARCH (Bollerslev 1986): and remembers yesterday's variance; fitted by maximum likelihood")]
        step = ladder(self, rows, whys, keep=2, top=3.2, x=-2.8, buff=0.6, edge=6.9)
        t, v, ab = np.asarray(g["t"]), np.asarray(g["vol_ann"]), np.asarray(g["absr_ann"])
        gr = axes([1926, 2021], [0, 1.0], x_length=7.0, y_length=2.7, ylabel=r"US market volatility, annualised",
                  xticks=[1930, 1960, 1990, 2020], xfmt=lambda u: f"{int(u)}", yticks=[0, 0.5, 1.0],
                  yfmt=lambda u: f"{100 * u:.0f}\\%", font_size=16).to_edge(DOWN, buff=0.45).to_edge(LEFT, buff=0.6)
        ax = gr.ax
        dots = curve(ax, t, np.clip(ab, 0, 1.0), RET, stroke_width=1).set_stroke(opacity=0.35)
        line = curve(ax, t, np.clip(v, 0, 1.0), VOL, stroke_width=2.5)
        side = VGroup(
            MathTex(rf"\alpha = {a:.3f},\ \beta = {b:.3f}", font_size=30, color=VOL),
            MathTex(rf"\alpha + \beta = {us['garch']['persistence']:.3f}", font_size=30),
            label(rf"a shock to variance halves in {us['garch']['half_life']:.0f} trading days", font_size=21, color=GREY_A),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.18).next_to(gr, RIGHT, buff=0.3).align_to(gr, UP)
        src = real_data(r"Kenneth French's daily US market, 1926--2020: " + f"{g['n']:,}".replace(",", "{,}") + " days")
        with self.voiceover(
            "The other way is to let volatility respond to the data directly. In 1982 Robert Engle proposed ARCH: "
            "today's variance is a constant plus a multiple of yesterday's squared surprise. <bookmark mark='a'/> In "
            "1986 Tim Bollerslev added memory: today's variance also depends on yesterday's variance. GARCH, fitted by "
            "maximum likelihood. <bookmark mark='b'/> On twenty-five thousand days of the American market, alpha is "
            "about a tenth and beta about nine tenths: they add up to zero point nine nine. Volatility is extremely "
            f"persistent: a shock to the variance takes about {us['garch']['half_life']:.0f} trading days to halve. The "
            "fitted volatility follows the market's moves through the whole century, with the Depression, 1987, 2008 "
            "and 2020 all visible."
        ) as vo:
            step(0)
            vo.wait_until("a")
            step(1)
            vo.wait_until("b")
            self.play(FadeIn(gr), FadeIn(src), Create(dots), Create(line), run_time=3)
            self.play(FadeIn(side))
        self.wait(0.4)
        self.clear_scene()

    def leverage(self, g):
        us = g["us"]
        a, gam, b = us["gjr"]["params"][1], us["gjr"]["params"][2], us["gjr"]["params"][3]
        rr = np.linspace(-0.05, 0.05, 101)
        base = 0.0001
        nic_g = base + us["garch"]["params"][1] * rr ** 2
        nic_j = base + (a + gam * (rr < 0)) * rr ** 2
        gp = axes([-0.05, 0.05], [0, 0.0005], x_length=6.0, y_length=4.0, xlabel=r"yesterday's return",
                  ylabel=r"today's variance (news impact)", xticks=[-0.04, 0, 0.04], xfmt=lambda u: f"{100 * u:.0f}\\%",
                  yticks=[], font_size=18).to_edge(LEFT, buff=0.8).shift(DOWN * 0.2)
        ax = gp.ax
        lg = curve(ax, rr, nic_g, VOL, stroke_width=3)
        lj = curve(ax, rr, nic_j, BAD, stroke_width=3.5)
        leg = legend([(VOL, r"GARCH: symmetric"), (BAD, r"GJR: falls count more")], font_size=21)
        side = VGroup(
            leg,
            MathTex(rf"\text{{GJR: }} \alpha = {a:.3f},\ \gamma = {gam:.3f}", font_size=30, color=BAD),
            label(r"a fall raises tomorrow's variance about four times as much as a rise", font_size=21, color=GREY_A),
            MathTex(rf"\log L:\ \text{{GARCH }} {us['garch']['loglik']:,.0f},\ \text{{GJR }} {us['gjr']['loglik']:,.0f},\ "
                    rf"\text{{EGARCH }} {us['egarch']['loglik']:,.0f}".replace(",", "{,}"), font_size=24, color=GREY_A),
            label(rf"Bitcoin too: GJR $\gamma = {g['btc']['gjr_gamma']:.2f}$; GARCH half-life {g['btc']['half_life']:.0f} days",
                  font_size=21, color=FC),
            wrapped_label(r"the leverage effect (Black 1976): falling prices raise leverage and fear; Glosten, Jagannathan "
                          r"and Runkle (1993); Nelson's EGARCH (1991) models the log variance", 4.8, 20, GREY_B),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.22).to_edge(RIGHT, buff=0.4)
        with self.voiceover(
            "GARCH treats a fall and a rise of the same size alike. Markets don't. Fischer Black noticed in 1976 that "
            "volatility rises more after falls, and called it the leverage effect. <bookmark mark='a'/> The GJR model "
            "adds a term that switches on only after a negative return. On the American market it captures most of "
            "the response: a fall raises tomorrow's variance about four times as much as a rise of the same size. "
            "Both it and Nelson's EGARCH, which models the logarithm of the variance, fit far better than plain GARCH. "
            "<bookmark mark='b'/> Bitcoin shows the same asymmetry, though there is no corporate leverage behind it: "
            "the effect is about fear, not balance sheets."
        ) as vo:
            self.play(FadeIn(gp), Create(lg), FadeIn(leg[0]))
            vo.wait_until("a")
            self.play(Create(lj), FadeIn(leg[1]), FadeIn(side[1]), FadeIn(side[2]), FadeIn(side[3]))
            vo.wait_until("b")
            self.play(FadeIn(side[4]), FadeIn(side[5]))
        self.wait(0.4)
        self.clear_scene()

    def dcc(self, d):
        t, rho = np.asarray(d["t"]), np.asarray(d["rho"])
        g = axes([1962, 2021], [-0.8, 0.8], x_length=8.4, y_length=4.2, ylabel=r"correlation of stocks and Treasury bonds",
                 xticks=[1970, 1990, 2010], xfmt=lambda u: f"{int(u)}", yticks=[-0.8, -0.4, 0, 0.4, 0.8], font_size=18)
        g.to_edge(LEFT, buff=0.6).shift(DOWN * 0.2)
        ax = g.ax
        zero = DashedLine(ax.c2p(1962, 0), ax.c2p(2021, 0), color=GREY_B, stroke_width=2)
        line = curve(ax, t, rho, ALT, stroke_width=2.5)
        bd = d["by_decade"]
        names = {"1962": r"1962\text{--}69", "1970": r"1970\text{s}", "1980": r"1980\text{s}", "1990": r"1990\text{s}",
                 "2000": r"2000\text{s}", "2010": r"2010\text{--}20"}
        tab = VGroup(*[MathTex(rf"{names[k]}\text{{: }} {v:+.2f}", font_size=26, color=GOOD if v < 0 else BAD)
                       for k, v in bd.items()])
        tab.arrange(DOWN, aligned_edge=LEFT, buff=0.12)
        side = VGroup(label(r"average by decade:", font_size=21, color=GREY_A), tab,
                      wrapped_label(r"DCC (Engle 2002): each asset's GARCH, then a GARCH-like recursion for the correlation "
                                    rf"($a = {d['a']:.3f}$, $b = {d['b']:.3f}$)", 4.0, 19, GREY_B)).arrange(
            DOWN, aligned_edge=LEFT, buff=0.25).to_edge(RIGHT, buff=0.4)
        src = real_data(r"French daily market; a 10-year bond return from FRED DGS10 (carry minus 8 $\times$ yield change)")
        with self.voiceover(
            "Correlations move too. Robert Engle's dynamic conditional correlation model of 2002 fits a GARCH to each "
            "asset and then lets their correlation follow a similar recursion. <bookmark mark='a'/> Here is the "
            "correlation between American stocks and ten-year Treasury bonds since 1962. For forty years it was "
            "positive: inflation hurt both. Around 2000 it turned negative, and bonds became the hedge that made the "
            "sixty-forty portfolio work. <bookmark mark='b'/> Any risk model that assumed a fixed correlation would "
            "have been wrong about the most important number in a balanced portfolio, and in 2022, outside our "
            "window, it turned again."
        ) as vo:
            self.play(FadeIn(g), FadeIn(src), Create(zero))
            vo.wait_until("a")
            self.play(Create(line), run_time=3)
            self.play(FadeIn(side))
            vo.wait_until("b")
        self.wait(0.4)
        self.clear_scene()

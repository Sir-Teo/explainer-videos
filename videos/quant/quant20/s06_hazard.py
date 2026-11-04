from __future__ import annotations

import numpy as np

from explainer.quant import *  # noqa: F403
from videos.quant.quant20.common import BAD, HAZ, PART, RISKY, ZERO, ask, fit_right, illustration, load


class Hazard(VoiceoverScene):
    def construct(self):
        h = load("hazard")
        self.card()
        self.derive()
        self.clocks(h)
        self.bonds(h)
        self.cox()
        self.coxcurves(load("cox"))

    def card(self):
        c = chapter_card(5, r"Default as a random clock", r"What if default is a surprise?", part=PART)
        with self.voiceover("Chapter five. Reduced-form models: default as a surprise, arriving at a random rate."):
            self.play(FadeIn(c[0], shift=UP * 0.2), FadeIn(c[1]))
        self.play(FadeOut(c))

    def derive(self):
        rows = [cmath(r"\mathbb{P}(\tau \in [t, t + dt) \mid \tau \ge t)", r"=", r"\lambda_t\,dt", font_size=38,
                      colors={r"\mathbb{P}(\tau \in [t, t + dt) \mid \tau \ge t)": HAZ}),
                cmath(r"Q(t)", r"=", r"\mathbb{P}(\tau > t) = e^{-\int_0^t \lambda_s\,ds}", font_size=40,
                      colors={r"Q(t)": HAZ}),
                cmath(r"\bar P(0, T)", r"=", r"\mathbb{E}\Big[e^{-\int_0^T (r_s + \lambda_s)\,ds}\Big]", font_size=40,
                      colors={r"\bar P(0, T)": RISKY}),
                cmath(r"\bar P(0, T)", r"=", r"\mathbb{E}\Big[e^{-\int_0^T (r_s + (1 - R)\lambda_s)\,ds}\Big]", font_size=38,
                      colors={r"\bar P(0, T)": RISKY})]
        whys = [why(r"Jarrow and Turnbull (1995): default is the first jump of a Poisson process with intensity "
                    r"$\lambda$; no asset value, no barrier, no warning"),
                why(r"survival is exactly a discount factor, with the hazard rate in place of the interest rate"),
                why(r"a zero that pays nothing on default: discount at the risky rate $r + \lambda$; all of Part 19's "
                    r"machinery prices it"),
                why(r"Duffie and Singleton (1999): if default costs a fraction $1 - R$ of market value, discount at "
                    r"$r + (1 - R)\lambda$: the spread is $(1 - R)\lambda$, the credit triangle exactly")]
        step = ladder(self, rows, whys, keep=4, top=2.9, x=-1.0, buff=0.5, edge=6.9)
        with self.voiceover(
            "Structural models explain why firms default, and get short spreads wrong. Robert Jarrow and Stuart "
            "Turnbull, in 1995, gave up on the why: default is a surprise, the first tick of a random clock running at "
            "a rate lambda. <bookmark mark='a'/> Then the chance of surviving to t is an exponential of minus the "
            "integrated rate: a discount factor, with the hazard in place of the interest rate. <bookmark mark='b'/> "
            "A bond that pays nothing on default is discounted at the risky rate, r plus lambda, and every tool of "
            "Part nineteen applies to it. <bookmark mark='c'/> Darrell Duffie and Kenneth Singleton showed in 1999 "
            "that if default destroys a fraction of the bond's market value, the spread is exactly that fraction times "
            "the hazard: the credit triangle, derived."
        ) as vo:
            step(0)
            vo.wait_until("a")
            step(1)
            vo.wait_until("b")
            step(2)
            vo.wait_until("c")
            step(3)
        self.wait(0.4)
        self.clear_scene()

    def clocks(self, h):
        tau = np.sort(np.asarray(h["tau"]))
        T, Q, emp = np.asarray(h["T"]), np.asarray(h["Q"]), np.asarray(h["emp"])
        strip = NumberLine(x_range=[0, 10, 1], length=11, include_numbers=True, font_size=20).shift(UP * 2.2)
        ticks = VGroup(*[Line(strip.n2p(x) + UP * 0.12, strip.n2p(x) + DOWN * 0.12, color=BAD, stroke_width=2)
                         for x in tau if x < 10])
        g = axes([0, 10], [0, 1.05], x_length=7.4, y_length=3.4, xlabel=r"years", ylabel=r"surviving",
                 xticks=[0, 2, 4, 6, 8, 10], yticks=[0, 0.5, 1.0], font_size=14).shift(DOWN * 1.3 + LEFT * 1.6)
        ax = g.ax
        lq = curve(ax, T, Q, HAZ, stroke_width=3.5)
        stairs = VMobject().set_points_as_corners([ax.c2p(a, b) for a, b in zip(np.repeat(T, 2)[1:],
                                                                                  np.repeat(emp, 2)[:-1])])
        stairs.set_stroke(WHITE, 2)
        side = VGroup(
            MathTex(rf"\lambda = {100 * h['lam']:.0f}\%\ \text{{a year}}", font_size=28, color=HAZ),
            label(rf"{int(np.sum(tau < 10))} of 200 default within ten years", font_size=19, color=GREY_A),
            MathTex(rf"Q(10) = e^{{-{10 * h['lam']:.1f}}} = {np.exp(-10 * h['lam']):.3f}", font_size=26),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.3).to_edge(RIGHT, buff=0.5).shift(DOWN * 1.3)
        fit_right(side)
        with self.voiceover(
            "Two hundred firms, each with a clock running at three percent a year. Each red tick is one default. "
            "<bookmark mark='a'/> They arrive with no pattern and no warning: no firm's tick can be predicted. "
            "<bookmark mark='b'/> But the fraction surviving follows the exponential almost exactly, the white "
            "staircase against the curve. A portfolio is predictable where a single name is not."
        ) as vo:
            self.play(Create(strip))
            vo.wait_until("a")
            self.play(LaggedStart(*[FadeIn(t_) for t_ in ticks], lag_ratio=0.03, run_time=3))
            vo.wait_until("b")
            self.play(FadeIn(g), Create(lq), Create(stairs), FadeIn(side), run_time=2)
        self.wait(0.4)
        self.clear_scene()

    def bonds(self, h):
        T = np.asarray(h["T"])
        df, rmv, rf = np.asarray(h["df"]) * 100, np.asarray(h["rmv"]) * 100, np.asarray(h["rf"]) * 100
        g = axes([0, 10], [40, 100], x_length=7.4, y_length=4.4, xlabel=r"maturity, years", ylabel=r"price per 100 of face",
                 xticks=[0, 2, 4, 6, 8, 10], yticks=[40, 60, 80, 100], font_size=14).to_edge(LEFT, buff=0.6).shift(
            DOWN * 0.3)
        ax = g.ax
        l0 = curve(ax, T, df, ZERO, stroke_width=3)
        l1 = curve(ax, T, rmv, RISKY, stroke_width=3)
        l2 = curve(ax, T, rf, QC.IMPLIED, stroke_width=3)
        no = curve(ax, T, df * np.asarray(h["Q"]), BAD, stroke_width=2).set_stroke(opacity=0.6)
        side = VGroup(
            legend([(ZERO, r"safe zero, $r = 4\%$"), (RISKY, r"recovery of market value, $R = 40\%$"),
                    (QC.IMPLIED, r"recovery of face, paid at maturity"), (BAD, r"zero recovery")], font_size=16),
            wrapped_label(r"the convention matters most for long, risky bonds; in practice bonds recover a fraction of "
                          r"face at default (all bonds of one issuer, whatever their maturity, recover the same), which "
                          r"is what CDS auctions settle", 3.6, 17, GREY_A),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.3).to_edge(RIGHT, buff=0.3)
        fit_right(side)
        with self.voiceover(
            "Price zero-coupon bonds from one issuer with a three percent hazard. <bookmark mark='a'/> With nothing "
            "recovered, the price is the safe one times survival. <bookmark mark='b'/> With forty percent of market "
            "value recovered, Duffie and Singleton's convention, it is higher, and simplest to compute. With forty "
            "percent of face recovered, it is different again. In real defaults, all of an issuer's bonds recover the "
            "same fraction of face, long and short alike, which is what the auctions of the next chapter settle. One "
            "caution about every hazard read from prices: it is risk-neutral. Hull, Predescu and White found the "
            "default probabilities implied by investment-grade bond prices to be several times those actually "
            "observed; the difference is the premium for bearing the risk."
        ) as vo:
            self.play(FadeIn(g), Create(l0), FadeIn(side[0]))
            vo.wait_until("a")
            self.play(Create(no))
            vo.wait_until("b")
            self.play(Create(l1), Create(l2), FadeIn(side[1]), run_time=2)
        self.wait(0.4)
        self.clear_scene()

    def coxcurves(self, c):
        T = np.asarray(c["T"])
        cols = {"calm": QC.GAIN, "long run": QC.IMPLIED, "stressed": BAD}
        g = axes([0, 10], [0, 500], x_length=7.4, y_length=4.4, xlabel=r"maturity, years", ylabel=r"spread, bp",
                 xticks=[0, 2, 4, 6, 8, 10], yticks=[0, 100, 200, 300, 400, 500], font_size=14).to_edge(LEFT, buff=0.6
                                                                                                   ).shift(DOWN * 0.3)
        ax = g.ax
        lines = VGroup(*[curve(ax, T, np.clip(np.asarray(c["curves"][k]["spread_bp"]), 0, 500), col, stroke_width=3.5)
                         for k, col in cols.items()])
        side = VGroup(
            legend([(QC.GAIN, r"hazard today 0.5\%"), (QC.IMPLIED, r"2\% (its long-run level)"),
                    (BAD, r"8\% (stressed)")], font_size=17),
            MathTex(rf"\kappa = {c['kappa']:g},\ \theta = {100 * c['theta']:g}\%,\ \sigma = {c['sigma']:g}", font_size=26),
            wrapped_label(r"a safe name's curve slopes up, a stressed name's slopes down: from a stressed state the "
                          r"hazard is expected to fall, if the firm survives. Real CDS curves of distressed names invert "
                          r"exactly like this", 3.6, 17, GREY_A),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.3).to_edge(RIGHT, buff=0.3)
        fit_right(side)
        with self.voiceover(
            "Here are the spread curves that CIR intensity implies, from three starting levels of risk. "
            "<bookmark mark='a'/> A safe name's curve slopes up: its hazard is expected to rise toward the long-run "
            "level. <bookmark mark='b'/> A stressed name's slopes down: if it survives the next year or two, its hazard "
            "is expected to fall. Credit curves of distressed companies invert in exactly this way, and a structural "
            "model of a firm under water said the same in chapter two."
        ) as vo:
            self.play(FadeIn(g), FadeIn(side[0]), FadeIn(side[1]))
            vo.wait_until("a")
            self.play(Create(lines[0]), Create(lines[1]), run_time=2)
            vo.wait_until("b")
            self.play(Create(lines[2]), FadeIn(side[2]), run_time=1.5)
        self.wait(0.4)
        self.clear_scene()
        q = ask(r"a firm's hazard rate doubles overnight but nothing defaults. Who gained and who lost, and by how much "
                r"on a 5-year bond?")
        with self.voiceover("A firm's hazard rate doubles overnight, and nothing defaults. Who gained, who lost, and "
                            "roughly how much on a five-year bond?"):
            self.play(FadeIn(q))
        self.wait(0.5)
        self.clear_scene()

    def cox(self):
        rows = [cmath(r"d\lambda_t", r"=", r"\kappa(\theta - \lambda_t)\,dt + \sigma\sqrt{\lambda_t}\,dW_t", font_size=40,
                      colors={r"d\lambda_t": HAZ}),
                cmath(r"Q(0, T)", r"=", r"e^{A(T) - B(T)\lambda_0}", font_size=40, colors={r"Q(0, T)": HAZ})]
        whys = [why(r"Lando (1998): let the intensity itself be random, a Cox process; spreads move before defaults, "
                    r"and a CIR intensity (Part 19's model) stays positive"),
                why(r"survival is then a CIR bond price: the same Riccati equations, with the hazard in place of the "
                    r"short rate. A whole term structure of default, in closed form")]
        step = ladder(self, rows, whys, keep=2, top=2.4, x=-0.6, buff=0.8, edge=6.9)
        with self.voiceover(
            "One step further: let the hazard rate itself move at random. David Lando, in 1998, made it a Cox process: "
            "default risk that rises and falls, so spreads move every day, long before any default. "
            "<bookmark mark='a'/> Give the hazard Part nineteen's CIR dynamics, and survival is a CIR bond price, with "
            "the same Riccati equations and the hazard in place of the short rate. Credit is a second term structure, "
            "and the House prices it with the code it already has."
        ) as vo:
            step(0)
            vo.wait_until("a")
            step(1)
        self.wait(0.4)
        self.clear_scene()

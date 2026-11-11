from __future__ import annotations

import numpy as np

from explainer.quant import *  # noqa: F403
from videos.quant.quant19.common import FWD, PART, SHORT, VAS, ZERO, ask, fit_right, illustration, load


class HW(VoiceoverScene):
    def construct(self):
        h = load("hw")
        self.card()
        self.derive()
        self.calibrate(h)
        self.windows(load("hwwin"))
        self.drift(h)
        self.fan(h)
        self.trees()

    def card(self):
        c = chapter_card(3, r"Hull--White: fitting today's curve", r"Can a short-rate model reprice every bond?",
                         part=PART)
        with self.voiceover("Chapter three. Hull and White: a short-rate model that fits today's curve exactly."):
            self.play(FadeIn(c[0], shift=UP * 0.2), FadeIn(c[1]))
        self.play(FadeOut(c))

    def derive(self):
        rows = [cmath(r"dr_t", r"=", r"\big(\theta(t) - a\,r_t\big)\,dt + \sigma\,dW_t", font_size=44,
                      colors={r"dr_t": VAS}),
                cmath(r"r_t", r"=", r"x_t + \varphi(t),\quad dx = -a\,x\,dt + \sigma\,dW,\ x_0 = 0", font_size=40,
                      colors={r"r_t": VAS}),
                cmath(r"\varphi(t)", r"=", r"f^M(0, t) + \frac{\sigma^2}{2a^2}\big(1 - e^{-at}\big)^2", font_size=42,
                      colors={r"\varphi(t)": FWD}),
                cmath(r"P(t, T)", r"=", r"\frac{P^M(0, T)}{P^M(0, t)}\,e^{\frac12[V(t,T) - V(0,T) + V(0,t)] - B(t,T)\,x_t}",
                      font_size=38, colors={r"P(t, T)": ZERO})]
        whys = [why(r"Hull and White (1990): Vasicek with time-varying drift intercept $\theta(t)$; target $\theta(t)/a$"),
                why(r"split the rate into a zero-mean Gaussian part and a deterministic shift"),
                why(r"choose the shift so that every bond in today's market curve $P^M$ is repriced exactly: today's "
                    r"forward rate plus a convexity term"),
                why(r"every bond at every future date in closed form; $V$ is the variance of $\int x$, $B = (1 - e^{-a\tau})/a$ "
                    r"as in Vasicek")]
        step = ladder(self, rows, whys, keep=4, top=2.9, x=-1.6, buff=0.55, edge=6.9)
        with self.voiceover(
            "Vasicek's curve is whatever its three parameters allow; the market's curve is whatever it is. John Hull "
            "and Alan White, in 1990, let the target rate depend on time: one number for every future date. "
            "<bookmark mark='a'/> Split the short rate into a Gaussian part that starts at zero and a deterministic "
            "shift. <bookmark mark='b'/> Choose the shift so the model reprices every bond in today's curve: it is "
            "today's forward rate, plus a convexity term that grows with the horizon. <bookmark mark='c'/> Then every "
            "bond, at every future date and state, has a closed form, and so, by Jamshidian's trick in chapter five, "
            "do options on them."
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

    def calibrate(self, h):
        mats, vol, fv = np.asarray(h["mats"], float), np.asarray(h["vol"]) * 1e4, np.asarray(h["fitvol"]) * 1e4
        g = axes([0, 31], [0, 130], x_length=7.6, y_length=4.4, xlabel=r"maturity, years",
                 ylabel=r"volatility of the zero yield, $\mathrm{bp}/\sqrt{\mathrm{yr}}$", xticks=[1, 5, 10, 20, 30], yticks=[0, 40, 80, 120],
                 font_size=14).to_edge(LEFT, buff=0.6).shift(DOWN * 0.3)
        ax = g.ax
        bars = VGroup(*[Rectangle(width=0.7, height=max(ax.c2p(0, v)[1] - ax.c2p(0, 0)[1], 0.01), stroke_width=0,
                                  fill_color=GREY_B, fill_opacity=0.6).move_to(
            [ax.c2p(m, 0)[0], (ax.c2p(0, v)[1] + ax.c2p(0, 0)[1]) / 2, 0]) for m, v in zip(mats, vol)])
        mm = np.linspace(0.5, 30, 100)
        a, s = h["a"], h["sigma"]
        model = curve(ax, mm, s * (1 - np.exp(-a * mm)) / (a * mm) * 1e4, VAS, stroke_width=3)
        side = VGroup(
            MathTex(r"\sigma_{y}(n) = \sigma\,\frac{1 - e^{-an}}{a\,n}", font_size=32, color=VAS),
            MathTex(rf"a = {a:.4f},\quad \sigma = {100 * s:.2f}\%", font_size=30, color=VAS),
            wrapped_label(r"grey: the daily moves of the Fed's zero yields, 2023--2025, annualized. A single factor "
                          r"can only decay with maturity; the hump at 2--3 years needs a second", 4.2, 18, GREY_A),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.3).to_edge(RIGHT, buff=0.4)
        fit_right(side)
        with self.voiceover(
            "What are a and sigma? The curve fixes the shift, not the volatility. One honest way to choose them: make "
            "the model's yields as volatile as the real ones. In the model an n-year yield moves by sigma times B "
            "over n for each unit shock to the short rate. <bookmark mark='a'/> Fitted to the daily moves of the Fed's "
            f"curve over 2023 to 2025: sigma {100 * s:.2f} percent a year, and almost no mean reversion. "
            "<bookmark mark='b'/> The real volatilities have a hump at two to three years that one factor cannot "
            "make. A desk would instead calibrate to option prices; the House has no free option quotes, so it uses "
            "the curve's own history, and says so."
        ) as vo:
            self.play(FadeIn(g), LaggedStart(*[GrowFromEdge(b_, DOWN) for b_ in bars], lag_ratio=0.1), FadeIn(side[0]))
            vo.wait_until("a")
            self.play(Create(model), FadeIn(side[1]))
            vo.wait_until("b")
            self.play(FadeIn(side[2]))
        self.add(illustration(r"the Fed's GSW curve, daily changes, 2023--2025"))
        self.wait(0.4)
        self.clear_scene()

    def windows(self, w):
        W = w["windows"]
        cols = [QC.SPOT, QC.IMPLIED, QC.GAIN, QC.OPTION]
        g = axes([0, 31], [0, 130], x_length=7.0, y_length=4.2, xlabel=r"zero maturity, years",
                 ylabel=r"daily vol of the yield, $\mathrm{bp}/\sqrt{\mathrm{yr}}$", xticks=[1, 5, 10, 20, 30], yticks=[0, 40, 80, 120],
                 font_size=14).to_edge(LEFT, buff=0.6).shift(DOWN * 0.3)
        ax = g.ax
        dots, fits = VGroup(), VGroup()
        for c_, x in zip(cols, W):
            m_, v_, f_ = np.asarray(x["mats"]), np.asarray(x["vol"]) * 1e4, np.asarray(x["fit"]) * 1e4
            dots.add(VGroup(*[Dot(ax.c2p(a_, b_), color=c_, radius=0.06) for a_, b_ in zip(m_, v_)]))
            fits.add(curve(ax, m_, f_, c_, stroke_width=2.5, smooth=True))

        def a_txt(a):
            return r"\approx 0" if a < 5e-4 else f"= {a:.4f}"
        tab = VGroup(*[MathTex(rf"\text{{{x['window']}}}:\ a {a_txt(x['a'])},\ \sigma = {1e4 * x['sigma']:.0f}\ \text{{bp}}",
                               font_size=24, color=c_) for c_, x in zip(cols, W)])
        tab.arrange(DOWN, aligned_edge=LEFT, buff=0.2)
        side = VGroup(tab, wrapped_label(r"dots: the data; lines: the best Hull--White fit. When the short end was pinned "
                                         r"near zero, short yields barely moved and long ones did: a vol curve rising "
                                         r"with maturity, which Hull--White cannot draw with any positive $a$. The fit "
                                         r"sits on its boundary, and the parameter means nothing", 3.9, 17, GREY_A)
                      ).arrange(DOWN, aligned_edge=LEFT, buff=0.35).to_edge(RIGHT, buff=0.35)
        fit_right(side)
        with self.voiceover(
            "Fit the same two parameters in other three-year windows, and see how stable they are. "
            "<bookmark mark='a'/> In 2004 to 2006, and again since 2023, the volatility of yields falls with maturity, "
            "the shape the model is built for. <bookmark mark='b'/> But in 2010 to 2012, and 2019 to 2021, the Fed held "
            "the short rate near zero; short yields barely moved while long ones did, and volatility rose with "
            "maturity. No positive mean reversion can draw that. The fit runs to its boundary, and the parameter "
            "stops meaning anything. A desk recalibrates every day, and a parameter that jumps when the regime changes "
            "is a hedge that jumps with it."
        ) as vo:
            self.play(FadeIn(g))
            vo.wait_until("a")
            for i in (0, 3):
                self.play(FadeIn(dots[i]), Create(fits[i]), FadeIn(tab[i]))
            vo.wait_until("b")
            for i in (1, 2):
                self.play(FadeIn(dots[i]), Create(fits[i]), FadeIn(tab[i]))
            self.play(FadeIn(side[1]))
        self.add(illustration(r"Fed GSW zero yields, daily changes; least squares on nine maturities"))
        self.wait(0.4)
        self.clear_scene()

    def drift(self, h):
        t, phi, f0 = np.asarray(h["t"]), np.asarray(h["phi"]) * 100, np.asarray(h["f0"]) * 100
        g = axes([0, 30], [3, 10], x_length=8.2, y_length=4.4, xlabel=r"date $t$, years ahead", ylabel=r"percent",
                 xticks=[0, 5, 10, 20, 30], yticks=[4, 6, 8, 10], font_size=14).to_edge(LEFT, buff=0.6).shift(DOWN * 0.3)
        ax = g.ax
        lf = curve(ax, t, f0, FWD, stroke_width=3)
        lp = curve(ax, t, phi, VAS, stroke_width=3)
        leg = legend([(FWD, r"today's forward curve $f^M(0, t)$"), (VAS, r"the shift $\varphi(t)$: where the mean of "
                                                                         r"$r_t$ must sit")], font_size=18).to_edge(
            RIGHT, buff=0.3).shift(UP * 1.6)
        note_ = wrapped_label(r"the gap is the convexity term $\sigma^2(1 - e^{-at})^2/2a^2$: averaging $e^{-\int r}$ over "
                              r"random paths raises bond prices, so the average rate must be higher to match them. With "
                              r"almost no mean reversion it grows like $\sigma^2 t^2/2$", 4.0, 18, GREY_A).next_to(
            leg, DOWN, buff=0.4, aligned_edge=LEFT)
        fit_right(note_)
        fit_right(leg)
        with self.voiceover(
            "Here is that shift against today's forward curve. Near today they agree. <bookmark mark='a'/> Further out "
            "the shift climbs above the forwards. Because the discount factor is a convex function of the rates, "
            "randomness alone raises bond prices; to reprice the market, the model's average rate must sit higher. With "
            "this little mean reversion, by thirty years the gap is several points: a warning that the calibrated "
            "model is extrapolating far beyond anything it was fitted to."
        ) as vo:
            self.play(FadeIn(g), Create(lf), FadeIn(leg[0]), run_time=2)
            vo.wait_until("a")
            self.play(Create(lp), FadeIn(leg[1]), FadeIn(note_), run_time=2)
        self.wait(0.4)
        self.clear_scene()

    def fan(self, h):
        times = np.r_[0.0, np.asarray(h["times"])]
        paths = np.asarray(h["r_paths"]) * 100
        q = np.asarray(h["r_q"]) * 100
        r0 = float(np.asarray(h["f0"])[0]) * 100
        paths = np.c_[np.full(len(paths), r0), paths]
        q = np.c_[np.full(5, r0), q]
        g = axes([0, 10], [-4, 14], x_length=8.0, y_length=4.6, xlabel=r"years ahead", ylabel=r"short rate, \%",
                 xticks=[0, 2, 4, 6, 8, 10], yticks=[-4, 0, 4, 8, 12], font_size=14).to_edge(LEFT, buff=0.6).shift(
            DOWN * 0.3)
        ax = g.ax
        band = Polygon(*[ax.c2p(a, b) for a, b in zip(times, q[0])], *[ax.c2p(a, b) for a, b in zip(times[::-1], q[4][::-1])],
                       stroke_width=0, fill_color=VAS, fill_opacity=0.15)
        lines = VGroup(*[curve(ax, times, np.clip(p, -4, 14), SHORT, stroke_width=1).set_stroke(opacity=0.35)
                         for p in paths[:40]])
        med = curve(ax, times, q[2], WHITE, stroke_width=3)
        zero = DashedLine(ax.c2p(0, 0), ax.c2p(10, 0), color=GREY_C, stroke_width=1.5)
        side = VGroup(
            label(r"20{,}000 exact paths; band: 5th to 95th percentile", font_size=19, color=GREY_A),
            MathTex(rf"\max_T \Big|\tfrac{{\mathbb{{E}}[e^{{-\int_0^T r}}]}}{{P^M(0,T)}} - 1\Big| = "
                    rf"{100 * h['reprice_max_rel']:.2f}\%", font_size=28),
            wrapped_label(rf"{100 * h['neg_share_10y']:.0f}\% of paths are below zero in ten years", 4.0, 19,
                          QC.LOSS),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.3).to_edge(RIGHT, buff=0.35)
        fit_right(side)
        with self.voiceover(
            f"These twenty thousand Gaussian state and integrated-rate draws are exact at the sampled dates under the specified Hull-White model; they are not a continuous-path record. <bookmark mark='a'/> Averaging their discount factors reproduces the initial curve with maximum relative sample residual {100 * h['reprice_max_rel']:.2f} percent. The analytical initial-curve identity is exact, while this sample estimate has uncertainty. <bookmark mark='b'/> The shaded range is pointwise across paths. With weak mean reversion, shocks persist; {100 * h['neg_share_10y']:.0f} percent of the simulated short rates are negative at year ten. This is a pricing-measure simulation from historical volatility proxies, not a real-world probability forecast or a test of market option fit."
        ) as vo:
            self.play(FadeIn(g), FadeIn(band), Create(zero), LaggedStart(*[Create(l_) for l_ in lines], lag_ratio=0.03,
                                                                       run_time=3), FadeIn(side[0]))
            self.play(Create(med))
            vo.wait_until("a")
            self.play(FadeIn(side[1]))
            vo.wait_until("b")
            self.play(FadeIn(side[2]))
        self.wait(0.4)
        self.clear_scene()

    def trees(self):
        rows = [cmath(r"d\ln r_t", r"=", r"\big(\theta(t) - a\ln r_t\big)\,dt + \sigma\,dW_t", font_size=40,
                      colors={r"d\ln r_t": VAS})]
        whys = [why(r"Black, Derman and Toy (1990); Black and Karasinski (1991): model the logarithm of the rate, so it "
                    r"stays positive and its volatility scales with its level; no closed forms, so prices come from a "
                    r"lattice")]
        step = ladder(self, rows, whys, keep=1, top=3.0, x=-0.6, buff=0.6, edge=6.9)
        dx, dy, jmax, n = 1.15, 0.55, 2, 6
        org = np.array([-5.6, -1.3, 0])

        def P(i, j):
            return org + np.array([dx * i, dy * j, 0])
        nodes, edges = VGroup(), VGroup()
        for i in range(n):
            for j in range(-min(i, jmax), min(i, jmax) + 1):
                nodes.add(Dot(P(i, j), radius=0.07, color=WHITE if abs(j) < jmax else QC.LOSS))
                if i == n - 1:
                    continue
                ks = (0, -1, -2) if j == jmax else (0, 1, 2) if j == -jmax else (-1, 0, 1)
                for k in ks:
                    edges.add(Line(P(i, j), P(i + 1, j + k), stroke_width=1.6, color=GREY_B))
        side = wrapped_label(r"Hull and White's trinomial tree (1994): each node branches up, middle or down, with "
                             r"probabilities that match the drift and variance. At the edge (red) the branching turns "
                             r"inward, which is mean reversion; a shift at each date fits today's curve. Then any "
                             r"Bermudan or callable bond is valued backwards, node by node", 4.4, 18,
                             GREY_A).to_edge(RIGHT, buff=0.35).shift(DOWN * 1.0)
        fit_right(side)
        with self.voiceover(
            "Rates in Hull and White can go negative. In 1990 Fischer Black, Emanuel Derman and William Toy, and a "
            "year later Black and Piotr Karasinski, modelled the logarithm of the rate instead: it stays positive, and "
            "its volatility grows with its level. There are no closed forms, so the price comes from a lattice. "
            "<bookmark mark='a'/> Hull and White's trinomial tree: from each node the rate goes up, stays, or goes "
            "down, with probabilities that match the model's drift and variance. At the edges the branches turn "
            "inward, which is mean reversion in a picture. Shift each column until the tree reprices today's curve, "
            "and value any callable bond backwards from its maturity, node by node."
        ) as vo:
            step(0)
            vo.wait_until("a")
            self.play(LaggedStart(*[Create(e) for e in edges], lag_ratio=0.02, run_time=3), FadeIn(nodes), FadeIn(side))
        q_ = ask(r"Hull--White reprices today's curve exactly. Why can its option prices still be wrong tomorrow?")
        with self.voiceover("Any of these models reprices today's curve exactly. Why can its option prices still be "
                            "wrong tomorrow?"):
            self.play(FadeIn(q_))
        self.wait(0.5)
        self.clear_scene()

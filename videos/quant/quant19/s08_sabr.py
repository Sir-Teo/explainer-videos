from __future__ import annotations

import numpy as np

from explainer.quant import *  # noqa: F403
from videos.quant.quant19.common import BAD, NORMAL, PART, ask, fit_right, illustration, load


class SABR(VoiceoverScene):
    def construct(self):
        s = load("sabr")
        self.card()
        self.model()
        self.history(load("ratevol"))
        self.data(load("ratevol"))
        self.dials(s)
        self.backbone()
        self.density(load("sabrpdf"))

    def card(self):
        c = chapter_card(7, r"SABR for rates", r"Why does every expiry have its own smile?", lit=(2002,), part=PART)
        with self.voiceover("Chapter seven. SABR: the model every rates desk uses for the smile."):
            self.play(FadeIn(c[0], shift=UP * 0.2), FadeIn(c[1]))
        self.play(FadeOut(c))

    def model(self):
        rows = [cmath(r"dF_t", r"=", r"\alpha_t\,F_t^{\beta}\,dW_t", font_size=44, colors={r"dF_t": NORMAL}),
                cmath(r"d\alpha_t", r"=", r"\nu\,\alpha_t\,dZ_t,\qquad d\langle W, Z\rangle = \rho\,dt", font_size=42,
                      colors={r"d\alpha_t": QC.VEGA}),
                cmath(r"\sigma_N(K)", r"\approx", r"\alpha\,\frac{z}{x(z)}\Big(1 + \tfrac{2 - 3\rho^2}{24}\,\nu^2 T\Big),"
                      r"\quad z = \tfrac{\nu}{\alpha}(F - K)", font_size=36, colors={r"\sigma_N(K)": NORMAL})]
        whys = [why(r"Hagan, Kumar, Lesniewski and Woodward (2002): one forward rate (a swap rate, or a caplet's rate), "
                    r"with no drift under its own measure"),
                why(r"its volatility is itself random, and correlated with it: Part 13's stochastic volatility, one "
                    r"expiry at a time"),
                why(r"$\beta = 0$, the normal SABR used where rates can be negative: a closed-form smile, "
                    r"$x(z) = \ln\frac{\sqrt{1 - 2\rho z + z^2} + z - \rho}{1 - \rho}$ (the House's \texttt{sabr\_normal\_iv})")]
        step = ladder(self, rows, whys, keep=3, top=2.9, x=-1.4, buff=0.7, edge=6.9)
        with self.voiceover(
            "Market swaptions and caps are not flat in strike; they smile. In 2002 Patrick Hagan and his coauthors "
            "wrote the model that the market adopted for it, SABR. Take one forward rate, with no drift under its own "
            "measure. <bookmark mark='a'/> Make its volatility random too, and correlated with the rate: Part "
            "thirteen's stochastic volatility, applied one expiry at a time. <bookmark mark='b'/> With beta equal to "
            "zero, the normal version used since rates went negative, the implied normal volatility has a closed form."
        ) as vo:
            step(0)
            vo.wait_until("a")
            step(1)
            vo.wait_until("b")
            step(2)
        self.wait(0.4)
        self.clear_scene()

    def dials(self, s):
        K = (np.asarray(s["K"]) - s["F"]) * 1e4
        base = np.asarray(s["base"]) * 1e4
        panels = VGroup()
        titles = {"alpha": r"$\alpha$: the level", "rho": r"$\rho$: the skew", "nu": r"$\nu$: the curvature"}
        for name in ("alpha", "rho", "nu"):
            g = axes([K.min(), K.max()], [40, 200], x_length=3.8, y_length=3.0, xlabel=r"strike $-$ forward, bp",
                     ylabel=titles[name], xticks=[-300, 0, 300], yticks=[50, 100, 150], font_size=12)
            ax = g.ax
            lines = VGroup(curve(ax, K, np.clip(base, 40, 200), WHITE, stroke_width=2.5))
            for v_, c_ in zip(s[name], (QC.SPOT, QC.OPTION)):
                lines.add(curve(ax, K, np.clip(np.asarray(v_) * 1e4, 40, 200), c_, stroke_width=2.5))
            vals = s[name + "_vals"]
            lab = MathTex(rf"{vals[0]:g}\ \ /\ \ {s['params'][name]:g}\ \ /\ \ {vals[1]:g}", font_size=20).next_to(
                g, DOWN, buff=0.1)
            panels.add(VGroup(g, lines, lab))
        panels.arrange(RIGHT, buff=0.45).shift(DOWN * 0.3)
        leg = legend([(QC.SPOT, r"lower"), (WHITE, r"base"), (QC.OPTION, r"higher")], font_size=17).arrange(
            RIGHT, buff=0.4).to_edge(UP, buff=0.5)
        foot = wrapped_label(r"normal vol in bp a year against strike, a 2-year option on a 3.5\% forward; illustrative "
                             r"parameters. A desk fits $\alpha$, $\rho$ and $\nu$ to each expiry's quotes every day, and "
                             r"uses the fitted model to price strikes nobody quotes", 12.0, 19, GREY_A).to_edge(DOWN, buff=0.4)
        with self.voiceover(
            "Each parameter has one job. <bookmark mark='a'/> Alpha sets the level of the smile, up and down. "
            "<bookmark mark='b'/> Rho tilts it: when volatility tends to rise as the rate falls, a negative rho, low "
            "strikes become dearer. <bookmark mark='c'/> And nu, the volatility of volatility, bends the wings up. A desk fits "
            "the three to each expiry's quotes every morning, and uses the fitted curve to price every strike in "
            "between, and every strike beyond."
        ) as vo:
            self.play(FadeIn(leg), FadeIn(foot))
            for i, m in enumerate(("a", "b", "c")):
                vo.wait_until(m)
                self.play(FadeIn(panels[i]))
        self.add(illustration(r"Hagan, Kumar, Lesniewski and Woodward (2002), normal SABR; illustrative parameters"))
        self.wait(0.5)
        self.clear_scene()

    def history(self, v):
        yr, nv, lv = np.asarray(v["year"]), np.asarray(v["nvol_bp"]), np.asarray(v["lvol_pct"])
        g1 = axes([1961, 2026], [0, 300], x_length=5.6, y_length=3.6, xlabel=r"year", ylabel=r"normal vol, bp a year",
                  xticks=[1970, 1990, 2010], yticks=[0, 100, 200, 300], font_size=13)
        g2 = axes([1961, 2026], [0, 110], x_length=5.6, y_length=3.6, xlabel=r"year", ylabel=r"lognormal vol, \%",
                  xticks=[1970, 1990, 2010], yticks=[0, 50, 100], font_size=13)
        VGroup(g1, g2).arrange(RIGHT, buff=0.9).shift(DOWN * 0.4)
        b1 = VGroup(*[Rectangle(width=0.06, height=max(g1.ax.c2p(0, h)[1] - g1.ax.c2p(0, 0)[1], 0.01), stroke_width=0,
                                fill_color=NORMAL, fill_opacity=0.85).move_to(
            [g1.ax.c2p(y_, 0)[0], (g1.ax.c2p(0, h)[1] + g1.ax.c2p(0, 0)[1]) / 2, 0]) for y_, h in zip(yr, np.clip(nv, 0, 300))])
        b2 = VGroup(*[Rectangle(width=0.06, height=max(g2.ax.c2p(0, h)[1] - g2.ax.c2p(0, 0)[1], 0.01), stroke_width=0,
                                fill_color=QC.OPTION, fill_opacity=0.85).move_to(
            [g2.ax.c2p(y_, 0)[0], (g2.ax.c2p(0, h)[1] + g2.ax.c2p(0, 0)[1]) / 2, 0]) for y_, h in zip(yr, np.clip(lv, 0, 110))])
        k = int(np.argmax(nv))
        head = label(r"Realised volatility of the 10-year Treasury yield, year by year", font_size=24).to_edge(UP, buff=0.5)
        foot = wrapped_label(rf"normal vol peaked at {nv[k]:.0f} bp in {int(yr[k])}, under Volcker; in 2022 it was "
                             rf"{nv[list(yr).index(2022)]:.0f}. Lognormal vol was highest in the 2010s and 2020s, when "
                             rf"yields were lowest, {lv[list(yr).index(2020)]:.0f}\% in 2020: a percentage of a small "
                             r"number", 12.0, 19, GREY_A).to_edge(DOWN, buff=0.4)
        with self.voiceover(
            "Before choosing beta, look at sixty years of rate volatility, measured both ways. "
            f"<bookmark mark='a'/> In basis points, it peaked at {nv[k]:.0f} a year in {int(yr[k])}, as Paul Volcker "
            f"fought inflation, and reached {nv[list(yr).index(2022)]:.0f} in 2022. <bookmark mark='b'/> In percent of "
            "the rate, the picture turns over: the most volatile years were the recent ones, when yields were so low "
            "that ordinary moves were large fractions of them. Which picture is the stable one?"
        ) as vo:
            self.play(FadeIn(head), FadeIn(g1), FadeIn(g2))
            vo.wait_until("a")
            self.play(LaggedStart(*[GrowFromEdge(b_, DOWN) for b_ in b1], lag_ratio=0.02, run_time=2))
            vo.wait_until("b")
            self.play(LaggedStart(*[GrowFromEdge(b_, DOWN) for b_ in b2], lag_ratio=0.02, run_time=2), FadeIn(foot))
        self.wait(0.4)
        self.clear_scene()

    def data(self, v):
        lv, nv, lg = np.asarray(v["level"]), np.asarray(v["nvol_bp"]), np.asarray(v["lvol_pct"])
        yr = np.asarray(v["year"])
        g = axes([np.log(1.2), np.log(16)], [np.log(20), np.log(400)], x_length=6.2, y_length=4.4,
                 xlabel=r"", ylabel=r"normal vol, bp a year (log scale)",
                 xticks=[], yticks=[], font_size=13).to_edge(LEFT, buff=0.7).shift(DOWN * 0.1)
        ax = g.ax
        g.add(label(r"10-year yield that year, \% (log scale)", font_size=15, color=GREY_B).next_to(
            ax.c2p(np.log(4.4), np.log(20)), DOWN, buff=0.55))
        tx = VGroup(*[MathTex(f"{x_:g}", font_size=20).next_to(ax.c2p(np.log(x_), np.log(20)), DOWN, buff=0.12)
                      for x_ in (1.5, 3, 6, 12)])
        ty = VGroup(*[MathTex(f"{y_:g}", font_size=20).next_to(ax.c2p(np.log(1.2), np.log(y_)), LEFT, buff=0.12)
                      for y_ in (25, 50, 100, 200, 400)])
        dots = VGroup(*[Dot(ax.c2p(np.log(a_), np.log(b_)), radius=0.06,
                            color=interpolate_color(ManimColor(QC.SPOT), ManimColor(QC.OPTION), (y_ - 1962) / 63))
                        for a_, b_, y_ in zip(lv, nv, yr)])
        xs = np.linspace(np.log(1.4), np.log(15), 20)
        fit = Line(ax.c2p(xs[0], v["c"] + v["beta"] * xs[0]), ax.c2p(xs[-1], v["c"] + v["beta"] * xs[-1]),
                   color=WHITE, stroke_width=3)
        rows = VGroup(
            MathTex(r"\sigma_N \approx \alpha\,F^{\beta}", font_size=34),
            MathTex(rf"\hat\beta = {v['beta']:.2f}", font_size=34, color=NORMAL),
            MathTex(rf"\text{{spread of vols: normal }} {100 * v['cv_n']:.0f}\%,\ \text{{lognormal }} {100 * v['cv_l']:.0f}\%",
                    font_size=24),
            wrapped_label(r"each dot a year, 1962 (blue) to 2025 (pink): realised volatility of daily changes in the "
                          r"10-year Treasury yield against its level. $\beta = 0$ would be a flat line (normal), "
                          r"$\beta = 1$ a slope of one (lognormal)", 4.2, 17, GREY_A),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.3).to_edge(RIGHT, buff=0.35)
        fit_right(rows)
        with self.voiceover(
            "Which beta should a desk use? Ask the data. For each year since 1962, the realised volatility of daily "
            "moves in the ten-year Treasury yield, in basis points, against the yield's level, both on log scales. "
            "<bookmark mark='a'/> If rates were normal, the dots would lie flat; if lognormal, on a slope of one. "
            f"<bookmark mark='b'/> The fitted slope is {v['beta']:.2f}: much closer to normal than to lognormal. "
            "Measured in basis points, rate volatility is far steadier across decades than measured in percent of "
            f"the rate: a spread of {100 * v['cv_n']:.0f} percent against {100 * v['cv_l']:.0f}. That is one reason "
            "the market moved to normal quotes, and why low betas are common on rates desks."
        ) as vo:
            self.play(FadeIn(g), FadeIn(tx), FadeIn(ty), FadeIn(rows[3]))
            self.play(LaggedStart(*[FadeIn(d) for d in dots], lag_ratio=0.03, run_time=3))
            vo.wait_until("a")
            self.play(FadeIn(rows[0]))
            vo.wait_until("b")
            self.play(Create(fit), FadeIn(rows[1]), FadeIn(rows[2]))
        self.add(illustration(r"FRED: DGS10, daily, 1962--2025"))
        self.wait(0.4)
        self.clear_scene()

    def backbone(self):
        from explainer.quant.house import termstructure as TS
        F = np.linspace(0.01, 0.06, 26)
        T = 2.0
        cols = {0.0: QC.SPOT, 0.5: QC.IMPLIED, 1.0: QC.OPTION}
        g = axes([1, 6], [40, 160], x_length=6.6, y_length=4.2, xlabel=r"forward rate, \%",
                 ylabel=r"at-the-money normal vol, bp", xticks=[1, 2, 3, 4, 5, 6], yticks=[50, 100, 150], font_size=14
                 ).to_edge(LEFT, buff=0.6).shift(DOWN * 0.3)
        ax = g.ax
        lines = VGroup()
        for beta, col in cols.items():
            alpha = 0.009 / 0.035 ** beta  # every model agrees at 3.5%: 90 bp
            v = np.array([float(TS.sabr_normal_iv(f, f, T, alpha, beta, -0.2, 0.35)) for f in F]) * 1e4
            lines.add(curve(ax, F * 100, np.clip(v, 40, 160), col, stroke_width=3.5, smooth=True))
        mark = Dot(ax.c2p(3.5, 0.009 * 1e4 * (1 + (2 - 3 * 0.04) / 24 * 0.35 ** 2 * T)), color=WHITE)
        rows = VGroup(
            legend([(QC.SPOT, r"$\beta = 0$"), (QC.IMPLIED, r"$\beta = \tfrac12$"), (QC.OPTION, r"$\beta = 1$")],
                   font_size=18),
            MathTex(r"\Delta = \frac{\partial V}{\partial F} + \frac{\partial V}{\partial \sigma_N}\,"
                    r"\frac{\partial \sigma_N}{\partial F}", font_size=30),
            wrapped_label(r"the backbone: how the at-the-money vol moves when the rate moves. All three fit today's "
                          r"quotes equally well; they disagree about tomorrow, and so about the hedge. The second term is "
                          r"the vega times the backbone's slope (Bartlett, 2006, refines it)", 4.0, 17, GREY_A),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.3).to_edge(RIGHT, buff=0.35)
        fit_right(rows)
        with self.voiceover(
            "What does beta do, if alpha, rho and nu can fit any one day's smile? It decides the backbone: how the "
            "at-the-money volatility moves when the rate moves. Calibrate three versions to the same quotes at three "
            "and a half percent. <bookmark mark='a'/> With beta zero, normal vol stays put as rates move. With beta "
            "one, it grows in proportion to the rate. All three agree today and disagree about tomorrow. "
            "<bookmark mark='b'/> And that changes the hedge: the delta of an option includes its vega times the "
            "backbone's slope. Two desks with identical prices can hold different hedges, and the data from earlier, "
            "a slope near one third, is the evidence for choosing between them."
        ) as vo:
            self.play(FadeIn(g), FadeIn(mark), FadeIn(rows[0]))
            vo.wait_until("a")
            self.play(LaggedStart(*[Create(l_) for l_ in lines], lag_ratio=0.4, run_time=3))
            vo.wait_until("b")
            self.play(FadeIn(rows[1]), FadeIn(rows[2]))
        self.wait(0.4)
        self.clear_scene()

    def density(self, p):
        a, b = p["2"], p["10"]
        g = axes([0, 9], [-40, 40], x_length=7.6, y_length=4.4, xlabel=r"rate at expiry, \%",
                 ylabel=r"implied density", xticks=[0, 2, 4, 6, 8], yticks=[-40, 0, 40], font_size=14
                 ).to_edge(LEFT, buff=0.6).shift(DOWN * 0.3)
        ax = g.ax
        zero = Line(ax.c2p(0, 0), ax.c2p(9, 0), color=WHITE, stroke_width=1.5)
        K2, d2 = np.asarray(a["K"]) * 100, np.asarray(a["pdf"])
        K10, d10 = np.asarray(b["K"]) * 100, np.asarray(b["pdf"])
        l2 = curve(ax, K2, np.clip(d2, -40, 40), QC.SPOT, stroke_width=3)
        l10 = curve(ax, K10, np.clip(d10, -40, 40), BAD, stroke_width=3)
        prm = p["params"]
        side = VGroup(
            legend([(QC.SPOT, r"2-year expiry"), (BAD, r"10-year expiry")], font_size=18),
            MathTex(r"\text{density} = \frac{\partial^2 C}{\partial K^2}", font_size=30),
            MathTex(rf"\text{{10 years: negative below }} {100 * b['neg_upto']:.2f}\%", font_size=24, color=BAD),
            wrapped_label(rf"Hagan's expansion with $\beta = {prm['beta']:g}$, $\rho = {prm['rho']:g}$, "
                          rf"$\nu = {prm['nu']:g}$, forward {100 * p['F']:.1f}\%; the negative part runs off the "
                          r"chart. Buy the butterfly there and collect money for a payoff that is never negative: an "
                          r"arbitrage. Fixes: arbitrage-free SABR (Hagan and coauthors, 2014) solves the model's PDE "
                          r"instead", 4.0, 17, GREY_A),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.28).to_edge(RIGHT, buff=0.35)
        fit_right(side)
        with self.voiceover(
            "One warning about the formula. It is an expansion in time to expiry, and at long expiries it fails. "
            "Read the density of the rate at expiry off the prices, the second derivative in strike, as in Part "
            "nine. <bookmark mark='a'/> For two years, with a beta of one half, it is a proper bell. "
            "<bookmark mark='b'/> For ten years, with the same parameters, it dives below zero for every strike under "
            f"{100 * b['neg_upto']:.2f} percent. A negative probability means a butterfly with a payoff that is never "
            "negative, sold at a negative price: an arbitrage, printed by the formula. Desks that price long-dated "
            "options use an arbitrage-free version, published by Hagan and his coauthors in 2014, which solves the "
            "model's equation instead of expanding it."
        ) as vo:
            self.play(FadeIn(g), Create(zero), FadeIn(side[0]), FadeIn(side[1]))
            vo.wait_until("a")
            self.play(Create(l2), run_time=1.5)
            vo.wait_until("b")
            self.play(Create(l10), FadeIn(side[2]), FadeIn(side[3]), run_time=1.5)
        q = ask(r"SABR fits each expiry separately. What can go wrong when you price a product that depends on two "
                r"expiries at once?")
        with self.voiceover("SABR fits each expiry on its own. What can go wrong when a product depends on two expiries "
                            "at once?"):
            self.play(FadeIn(q))
        self.wait(0.5)
        self.clear_scene()

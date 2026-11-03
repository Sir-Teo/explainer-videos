from __future__ import annotations

import numpy as np

from explainer.quant import *  # noqa: F403
from videos.quant.quant11.common import (ALT, GAMMA, OPT, PART, SPOT, THETA, VEGA, axes3d, fixed, hint3d, illustration,
                                         load, pause, real_data, surf)


def sig_index(rho, s, N=50):
    return float(np.sqrt(s * s * (1 / N + (1 - 1 / N) * rho)))


class Dispersion(VoiceoverScene, ThreeDScene):
    def construct(self):
        c3 = load("cor3m")
        self.card()
        self.matrix()
        self.surface()
        self.derive(c3)
        self.cor3m(c3, load("dispersion"))
        self.trade(load("dispersion_sim"))

    def card(self):
        c = chapter_card(13, r"Dispersion and implied correlation", r"Is an index riskier than its members?",
                         lit=(2008, 2020), part=PART)
        with self.voiceover("Chapter thirteen. Dispersion, and implied correlation."):
            self.play(FadeIn(c[0], shift=UP * 0.2), FadeIn(c[1]))
        self.play(FadeOut(c))

    # ------------------------------------------------------------------
    def matrix(self):
        n = 12
        rho = ValueTracker(0.1)

        def mat():
            r = rho.get_value()
            g = VGroup()
            for i in range(n):
                for j in range(n):
                    v = 1.0 if i == j else r
                    g.add(Square(0.3, stroke_width=0.5, stroke_color=GREY_D, fill_color=interpolate_color(
                        ManimColor(BACKGROUND), ManimColor(QC.LOSS), v), fill_opacity=1).move_to([j * 0.3, -i * 0.3, 0]))
            return g.move_to(LEFT * 3.2 + DOWN * 0.3)
        M = always_redraw(mat)
        g = axes([0, 1], [0, 0.32], x_length=4.0, y_length=3.6, xlabel=r"average correlation $\rho$",
                 ylabel=r"index volatility", xticks=[0, 0.5, 1], yticks=[0, 0.1, 0.2, 0.3],
                 yfmt=lambda u: f"{100 * u:.0f}\\%", font_size=16).to_edge(RIGHT, buff=0.8).shift(DOWN * 0.3)
        xs = np.linspace(0, 1, 50)
        line = curve(g.ax, xs, [sig_index(x, 0.3) for x in xs], VEGA, stroke_width=3)
        dot = always_redraw(lambda: Dot(g.ax.c2p(rho.get_value(), sig_index(rho.get_value(), 0.3)), radius=0.08,
                                        color=YELLOW))
        ro = always_redraw(lambda: MathTex(rf"\rho = {rho.get_value():.2f}\quad \sigma_I = "
                                           rf"{100 * sig_index(rho.get_value(), 0.3):.1f}\%", font_size=28, color=YELLOW)
                           .next_to(g, UP, buff=0.15))
        cap = label(r"fifty members, each at 30\% volatility, equal weights", font_size=20, color=GREY_A).to_edge(
            UP, buff=0.35)
        with self.voiceover(
            "An index is a basket, and its volatility depends on how its members move together. Take fifty stocks, "
            "each at thirty percent volatility. Their correlation matrix glows hotter as the average correlation "
            "rises. <bookmark mark='a'/> When they move independently, the index is calm: four percent volatility, "
            "the members' noise cancels. As correlation rises toward one, the cancellation disappears and the index "
            "becomes as volatile as a single member. <bookmark mark='b'/> So the price of index options, set against "
            "the prices of the members' options, is a price on correlation."
        ) as vo:
            self.play(FadeIn(cap), FadeIn(g), Create(line))
            self.add(M, dot, ro)
            self.play(rho.animate.set_value(0.0), run_time=1)
            vo.wait_until("a")
            self.play(rho.animate.set_value(0.95), run_time=max(vo.until("b") - 0.3, 2.0), rate_func=linear)
            self.play(rho.animate.set_value(0.45), run_time=1.5)
        for m in (M, dot, ro):
            m.clear_updaters()
        self.wait(0.4)
        self.clear_scene()

    # ------------------------------------------------------------------
    def surface(self):
        ax = axes3d([0, 1, 0.25], [0.15, 0.45, 0.1], [0, 0.45, 0.15], x_length=7.0, y_length=5.0, z_length=3.2)
        sf = surf(ax, lambda r, s: sig_index(r, s), (0, 1), (0.15, 0.45), [(QC.SPOT, 0.05), (VEGA, 0.2), (QC.LOSS, 0.4)],
                  resolution=(24, 20), opacity=0.75)
        lvl = 0.20
        rs = np.linspace(0, 1, 60)
        pts = []
        for s in np.linspace(0.2, 0.45, 40):
            r = (lvl ** 2 / s ** 2 - 1 / 50) / (1 - 1 / 50)
            if 0 <= r <= 1:
                pts.append(ax.c2p(r, s, lvl) + OUT * 0.03)
        cut = VMobject(stroke_color=YELLOW, stroke_width=6).set_points_as_corners(pts)
        plane = Surface(lambda u, v: ax.c2p(u, v, lvl), u_range=[0, 1], v_range=[0.15, 0.45], resolution=(2, 2),
                        fill_color=YELLOW, fill_opacity=0.15, stroke_width=0)
        r30 = (lvl ** 2 / 0.09 - 1 / 50) / (1 - 1 / 50)
        mark = Dot3D(ax.c2p(r30, 0.30, lvl), radius=0.09, color=WHITE)
        hint = hint3d((r"average correlation $\rho$", QC.LOSS), (r"members' volatility $\bar\sigma$", OPT),
                      (r"index volatility $\sigma_I$", VEGA), ax=ax)
        cap = label(rf"index at 20\%, members at 30\%: $\rho_{{\text{{impl}}}} \approx {r30:.2f}$", font_size=24,
                    color=YELLOW).to_corner(DL, buff=0.4)
        self.set_camera_orientation(phi=64 * DEGREES, theta=-52 * DEGREES, zoom=0.9)
        fixed(self, hint, cap)
        with self.voiceover(
            "Draw the index volatility over two inputs: the average correlation, and the members' volatility. It "
            "rises in both. <bookmark mark='a'/> Now the market tells you the index's implied volatility: slice the "
            "surface at that height, twenty percent. The yellow curve is every combination consistent with it. "
            "<bookmark mark='b'/> Read off the members' implied volatility, thirty percent, and the correlation that "
            f"fits is about {r30:.2f}. That number is the implied correlation."
        ) as vo:
            self.play(Create(ax), FadeIn(hint), run_time=1.2)
            self.play(Create(sf), run_time=2.5)
            vo.wait_until("a")
            self.play(FadeIn(plane), Create(cut), run_time=1.5)
            vo.wait_until("b")
            self.play(FadeIn(mark, scale=2), FadeIn(cap))
            self.move_camera(theta=-25 * DEGREES, run_time=max(vo.remaining(1.0) - 0.3, 1.0))
        self.move_camera(phi=0, theta=-90 * DEGREES, zoom=1.0, added_anims=[FadeOut(VGroup(ax, sf, plane, cut, mark)),
                                                                             FadeOut(hint), FadeOut(cap)], run_time=1.5)
        self.clear_scene()

    # ------------------------------------------------------------------
    def derive(self, c3):
        rows = [
            cmath(r"\sigma_I^2", r"=", r"\sum_i w_i^2\sigma_i^2 + \sum_{i \ne j} w_i w_j\,\rho_{ij}\,\sigma_i\sigma_j",
                  font_size=36, colors={r"\sigma_I^2": VEGA}),
            cmath(r"\rho_{\text{impl}}", r"=", r"\frac{\sigma_I^2 - \sum_i w_i^2\sigma_i^2}{\big(\sum_i w_i\sigma_i\big)^2 - "
                  r"\sum_i w_i^2\sigma_i^2}", font_size=36, colors={r"\rho_{\text{impl}}": QC.LOSS}),
            cmath(r"\rho_{\text{impl}}", r"\approx", r"\frac{\sigma_I^2}{\big(\sum_i w_i\sigma_i\big)^2}\qquad (N\ "
                  r"\text{large})", font_size=36, colors={r"\rho_{\text{impl}}": QC.LOSS}),
        ]
        whys = [why(r"the variance of a weighted sum"),
                why(r"set every $\rho_{ij}$ to one number and solve: Cboe's implied correlation indices do this with "
                    r"the 50 largest S\&P 500 members"),
                why(r"the members' own variances shrink like $1/N$: implied correlation is the squared ratio of index "
                    r"to average member volatility")]
        step = ladder(self, rows, whys, keep=3, top=3.0, x=-0.6, buff=0.6, edge=6.9)
        card = lab_card(r"implied correlation", [
            "def implied_correlation(index_vol, weights, vols) -> float:",
            "    w, s = np.asarray(weights, float), np.asarray(vols, float)",
            "    own = np.sum(w ** 2 * s ** 2)",
            "    cross = np.sum(w * s) ** 2 - own",
            "    return float((index_vol ** 2 - own) / cross)",
        ], source="explainer/quant/house/quoting.py", width=6.6, font_size=17).to_edge(UP, buff=0.8).to_edge(LEFT, buff=0.5)
        pc = pause(r"Index implied vol 20\%, every member 30\%, many members. Implied correlation?", width=4.6,
                   font_size=20, corner=UR)  # the first row makes way for it
        with self.voiceover(
            "The algebra. An index's variance is the weighted members' variances plus every pair's covariance. "
            "<bookmark mark='a'/> Replace every pairwise correlation by one number and solve: that is the implied "
            "correlation, and it is how Cboe computes its implied correlation indices, from the fifty largest S&P 500 "
            "members. <bookmark mark='b'/> With many members the own-variance terms vanish, and the implied "
            "correlation is just the square of index volatility over average member volatility. Pause and predict: "
            "index at twenty percent, members at thirty. <bookmark mark='c'/> In the House: a toy of three names, "
            f"then fifty. About {c3['big']:.2f}, four ninths."
        ) as vo:
            step(0)
            vo.wait_until("a")
            step(1)
            vo.wait_until("b")
            step(2)
            self.play(FadeOut(rows[0]), FadeOut(whys[0]), FadeIn(pc))
            vo.wait_until("c")
            # the derivation is done: the lab takes the whole frame
            self.play(*[FadeOut(m) for m in (pc, *rows[1:3], *whys[1:3])])
            self.play(FadeIn(card))
            lab_run(self, card, [f"implied_correlation(0.20, [1/3]*3, [.25, .30, .35])  ->  {c3['toy']:.3f}",
                                 f"implied_correlation(0.20, [1/50]*50, [.30]*50)       ->  {c3['big']:.3f}"],
                    font_size=16, direction=RIGHT)
        self.wait(0.4)
        self.clear_scene()

    # ------------------------------------------------------------------
    def cor3m(self, c3, d):
        t, v = np.asarray(c3["t"]), np.asarray(c3["v"])
        g = axes([2006, 2026], [0, 100], x_length=8.4, y_length=4.0, ylabel=r"Cboe 3-month implied correlation (COR3M)",
                 xticks=[2008, 2012, 2016, 2020, 2024], xfmt=lambda u: f"{int(u)}", yticks=[0, 25, 50, 75, 100],
                 font_size=16).to_edge(LEFT, buff=0.6).shift(DOWN * 0.3)
        tr = ValueTracker(0.0)
        line = tracing(g.ax, t, v, tr, QC.LOSS, stroke_width=2)
        Y = c3["years"]

        def ymd(x):
            s = str(int(x))
            return s[:4] + "-" + s[4:6] + "-" + s[6:]
        side = VGroup(
            label(rf"mean {c3['mean']:.1f}", font_size=21, color=GREY_A),
            label(rf"peak {c3['max']:.1f} ({ymd(c3['argmax'])})", font_size=21, color=QC.LOSS),
            label(rf"March 2020: {Y['2020']['max']:.1f}", font_size=21, color=QC.LOSS),
            label(rf"lows: {Y['2024']['min']:.1f} (2024), {Y['2025']['min']:.1f} (2025)", font_size=21, color=GAMMA),
            wrapped_label(rf"realized, for comparison: the average correlation of 40 US industries over 36 months had "
                          rf"a median of {d['median']:.2f} from 1929 to 2020 (not like for like: industries are "
                          r"baskets, which correlate more than single stocks)", 4.0, 17, GREY_B),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.18).to_edge(RIGHT, buff=0.35)
        src = real_data(rf"Cboe COR3M daily, {c3['n']:,} days, 2006--2025".replace(",", "{,}"))
        with self.voiceover(
            "Here is the real thing: Cboe's three-month implied correlation index, every day since 2006. "
            "<bookmark mark='a'/> It spikes in crises, when everything falls together: "
            f"{c3['max']:.0f} in December 2011, during the euro crisis, and {Y['2020']['max']:.0f} in March 2020. "
            f"<bookmark mark='b'/> And look at the end: record lows, {Y['2024']['min']:.1f} in July 2024 and "
            f"{Y['2025']['min']:.1f} in January 2025, while a few giant technology stocks drove the index and the rest "
            "went their own ways: the conditions in which a dispersion trade, short index volatility and long the "
            "members', pays. Implied correlation tends to sit above the correlation later "
            "realized, Joost Driessen, Pascal Maenhout and Grigory Vilkov showed in 2009: the correlation risk premium, "
            "the reason index options are dear."
        ) as vo:
            self.play(FadeIn(g), FadeIn(src), FadeIn(side[0]))
            self.add(line)
            self.play(tr.animate.set_value(len(t) - 1), run_time=vo.until("a") + 1.5, rate_func=linear)
            self.play(FadeIn(side[1]), FadeIn(side[2]))
            vo.wait_until("b")
            self.play(FadeIn(side[3]), FadeIn(side[4]))
        self.wait(0.4)
        self.clear_scene()

    # ------------------------------------------------------------------
    def trade(self, ds):
        x = ds["rho_impl"] - np.asarray(ds["rho_real"])
        y = np.clip(np.asarray(ds["pnl"]), -12, 12)
        g = axes([-0.5, 0.5], [-12, 12], x_length=6.2, y_length=4.2, xlabel=r"implied minus realized correlation",
                 ylabel=r"dispersion P\&L, per 100", xticks=[-0.4, 0, 0.4], yticks=[-10, 0, 10], font_size=16)
        g.to_edge(LEFT, buff=0.6).shift(DOWN * 0.3)
        dots = VGroup(*[Dot(g.ax.c2p(a, b), radius=0.035, color=QC.GAIN if b > 0 else QC.LOSS, fill_opacity=0.7)
                        for a, b in zip(x, y)])
        rows = [cmath(r"P\&L", r"\approx", r"\sum_i w_i\,\tfrac12\Gamma_i S_i^2\big(\sigma_{r,i}^2 - \sigma_{i,i}^2\big) - "
                      r"\tfrac12\Gamma_I S_I^2\big(\sigma_{r,I}^2 - \sigma_{i,I}^2\big)", font_size=24),
                cmath(r"\text{sign}", r"\approx", r"\text{sign}\big(\rho_{\text{impl}} - \rho_{\text{real}}\big)",
                      font_size=28)]
        eqs = VGroup(*rows).arrange(DOWN, aligned_edge=LEFT, buff=0.3).to_edge(RIGHT, buff=0.35).shift(UP * 1.8)
        side = VGroup(
            label(rf"correlation with the gap: {ds['corr']:.2f}", font_size=21, color=GREY_A),
            label(rf"right sign in {100 * ds['share_right_sign']:.0f}\% of scenarios", font_size=21, color=GAMMA),
            wrapped_label(r"short the index's volatility, long the members': a bet that they move apart. In a crash "
                          r"they move together, and it loses: dispersion is short a crash", 4.6, 19, THETA),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.2).next_to(eqs, DOWN, buff=0.4).align_to(eqs, LEFT)
        src = illustration(rf"simulated: {ds['N']} stocks at 30\%, index options at $\rho_{{\text{{impl}}}} = "
                           rf"{ds['rho_impl']:.1f}$, 400 scenarios of realized correlation, hedged daily for 63 days")
        with self.voiceover(
            "The trade. Sell straddles on the index, buy straddles on the members, matched in vega, and hedge them all "
            "daily. Each member straddle collects its own realized minus implied variance; the short index straddle "
            "pays the index's. Substitute the variance of a sum for the index terms and the profit is driven by "
            "implied minus realized correlation. <bookmark mark='a'/> Simulate it: twenty stocks, index options priced "
            "at an implied correlation of one half, four hundred scenarios of what correlation turns out to be. "
            f"Each dot is one scenario: the profit tracks the gap with a correlation of {ds['corr']:.2f}, and has the "
            f"predicted sign {100 * ds['share_right_sign']:.0f} percent of the time. <bookmark mark='b'/> On the left, "
            "where realized correlation came in above implied, it loses. That is a crash: everything falls together. "
            "Dispersion earns the correlation premium by being short a crash."
            " Next: the world's largest options market by contracts, and who trades it."
        ) as vo:
            self.play(FadeIn(g), FadeIn(src), FadeIn(eqs))
            vo.wait_until("a")
            self.play(LaggedStart(*[FadeIn(d_) for d_ in dots], lag_ratio=0.004, run_time=3))
            self.play(FadeIn(side[0]), FadeIn(side[1]))
            vo.wait_until("b")
            self.play(FadeIn(side[2]))
        self.wait(0.4)
        self.clear_scene()

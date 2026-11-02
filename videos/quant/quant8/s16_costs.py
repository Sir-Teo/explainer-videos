from __future__ import annotations

import numpy as np

from explainer.quant import *  # noqa: F403
from videos.quant.quant8.common import ALT, GOOD, KELLY, OVER, PART, UNDER, VALUE, illustration, load


class Costs(VoiceoverScene):
    def construct(self):
        d = load("davis_norman")
        self.card()
        self.wedge(d)
        self.derive()
        self.lab(d)
        self.slider(d)

    def card(self):
        c = chapter_card(7, r"Transaction costs: the no-trade wedge", r"If every trade costs money, when should you "
                         r"trade?", part=PART)
        with self.voiceover("Chapter seven. Transaction costs, and the no-trade wedge."):
            self.play(FadeIn(c[0], shift=UP * 0.2), FadeIn(c[1]))
        self.play(FadeOut(c))

    def wedge(self, d):
        w = d["wedge"]
        P = np.asarray(w["path"])
        lo, hi, pm = w["lo"], w["hi"], d["pi_merton"]
        top = float(np.max(P) * 1.08)
        g = axes([0, top], [0, top], x_length=5.6, y_length=5.6, xlabel=r"dollars in bonds", ylabel=r"dollars in stocks",
                 xticks=[0, round(top / 2, 1)], yticks=[0, round(top / 2, 1)], font_size=16)
        g.to_edge(LEFT, buff=0.8).shift(DOWN * 0.2)
        ax = g.ax

        def ray(p, col, sw=3, dashed=False):
            # stock share p: y/(x + y) = p, i.e. y = p/(1 - p) x
            k = p / (1 - p)
            end = (top, k * top) if k <= 1 else (top / k, top)
            L = DashedLine if dashed else Line
            return L(ax.c2p(0, 0), ax.c2p(*end), color=col, stroke_width=sw)

        merton = ray(pm, KELLY, 3, dashed=True)
        k_lo, k_hi = lo / (1 - lo), hi / (1 - hi)
        region = Polygon(ax.c2p(0, 0), ax.c2p(top, min(k_lo * top, top)) if k_lo <= 1 else ax.c2p(top / k_lo, top),
                         ax.c2p(top / k_hi, top) if k_hi > 1 else ax.c2p(top, k_hi * top),
                         stroke_width=0, fill_color=VALUE, fill_opacity=0.18)
        if k_lo <= 1 < k_hi:
            region = Polygon(ax.c2p(0, 0), ax.c2p(top, k_lo * top), ax.c2p(top, top), ax.c2p(top / k_hi, top),
                             stroke_width=0, fill_color=VALUE, fill_opacity=0.18)
        edges = VGroup(ray(lo, VALUE, 2), ray(hi, VALUE, 2))
        tk = ValueTracker(0)
        trades = np.asarray(w["trades"])
        dot = always_redraw(lambda: Dot(ax.c2p(*P[int(tk.get_value())]), radius=0.08, color=WHITE))
        trail = always_redraw(lambda: VMobject(stroke_color=UNDER, stroke_width=1.6, stroke_opacity=0.6)
                              .set_points_as_corners([ax.c2p(*p) for p in P[:max(int(tk.get_value()), 1) + 1]]))
        n_band = Integer(0, font_size=34, color=VALUE)
        n_ray = Integer(0, font_size=34, color=KELLY)
        n_band.add_updater(lambda m: m.set_value(int(np.sum(trades <= tk.get_value()))))
        n_ray.add_updater(lambda m: m.set_value(int(tk.get_value())))
        cnt = VGroup(VGroup(label(r"trades, wedge:", font_size=22, color=VALUE), n_band).arrange(RIGHT, buff=0.2),
                     VGroup(label(r"trades, stay on the ray (weekly):", font_size=22, color=KELLY), n_ray).arrange(
                         RIGHT, buff=0.2)).arrange(DOWN, aligned_edge=LEFT, buff=0.2).to_edge(RIGHT, buff=0.5).shift(UP * 2.2)
        res = VGroup(
            MathTex(rf"\text{{turnover a year: }}{100 * w['turn_band']:.1f}\%\ \text{{vs}}\ {100 * w['turn_ray']:.0f}\%",
                    font_size=28),
            wrapped_label(rf"$\gamma = 3$, a cost of 1\% of every dollar traded: the wedge from {100 * lo:.1f}\% to "
                          rf"{100 * hi:.1f}\% in stocks, around Merton's {100 * pm:.1f}\%", 5.4, 19, GREY_A),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.25).next_to(cnt, DOWN, buff=0.5).align_to(cnt, LEFT)
        src = illustration(r"simulation: one market, weekly, 15 years; band from dynamic programming")
        with self.voiceover(
            "Merton's investor trades every instant to hold a constant fraction. If every trade costs one percent of "
            "the amount traded, that is ruinous: continuous rebalancing has infinite turnover. What should she do? "
            "<bookmark mark='a'/> Draw her wealth as a point in a plane: dollars in bonds across, dollars in stocks "
            "up. Merton's rule is a ray from the origin: every point on it has the same stock share. "
            "<bookmark mark='b'/> With costs, the ray opens into a wedge. Inside it, do nothing. When the market "
            "pushes the point to an edge, trade just enough to stay on the edge, never back to the middle. "
            "<bookmark mark='c'/> Watch fifteen years of one market. The point wanders freely inside the wedge, and "
            "each flash at an edge is a tiny trade. Count them against an investor who goes back to the ray every "
            f"week. <bookmark mark='d'/> The wedge trades {100 * w['turn_band']:.1f} percent of wealth a year; "
            f"staying on the ray, {100 * w['turn_ray']:.0f} percent. Mathematically the point is a diffusion "
            "reflected at the edges of a cone."
        ) as vo:
            self.play(FadeIn(g), FadeIn(src))
            vo.wait_until("a")
            self.play(Create(merton))
            vo.wait_until("b")
            self.play(FadeIn(region), Create(edges))
            vo.wait_until("c")
            self.add(trail, dot)
            self.play(FadeIn(cnt))
            self.play(tk.animate.set_value(len(P) - 1), run_time=max(min(vo.remaining(14.0) - 4, 18), 10),
                      rate_func=linear)
            vo.wait_until("d")
            self.play(FadeIn(res))
        for m in (dot, trail, n_band, n_ray):
            m.clear_updaters()
        self.wait(0.4)
        self.clear_scene()

    def derive(self):
        rows = [cmath(r"dx = -(1+\varepsilon)\,dL + (1-\varepsilon)\,dU", r",\quad", r"dy = dL - dU", font_size=32),
                cmath(r"\max\Big\{\mathcal{L}V,\ V_y - (1+\varepsilon)V_x,\ (1-\varepsilon)V_x - V_y\Big\}", r"=", r"0",
                      font_size=32, colors={r"0": VALUE}),
                cmath(r"V(x, y)", r"=", r"(x + y)^{1-\gamma}\, v(\pi),\qquad \pi = \frac{y}{x + y}", font_size=32,
                      colors={r"V(x, y)": VALUE}),
                cmath(r"\pi_\pm", r"\approx", r"\pi^* \pm \Big(\frac{3}{2\gamma}\,\pi^{*2}(1-\pi^*)^2\,\varepsilon\Big)^{1/3}",
                      font_size=34, colors={r"\pi_\pm": KELLY})]
        whys = [why(r"the controls are cumulative purchases $L$ and sales $U$, paying $\varepsilon$ on each dollar: a "
                    r"singular control", font_size=21),
                why(r"a variational inequality: in each region one term binds: no trade ($\mathcal{L}V = 0$), buy, or "
                    r"sell", font_size=21),
                why(r"homogeneity: only the stock share matters; the wedge is a band in $\pi$", font_size=21),
                why(r"small costs: the half-width grows like $\varepsilon^{1/3}$, the loss in welfare like "
                    r"$\varepsilon^{2/3}$ (Janecek and Shreve 2004; Rogers 2004)", font_size=21)]
        step = ladder(self, rows, whys, keep=4, top=3.1, x=0.0, buff=0.7, edge=6.9)
        foot = wrapped_label(r"Magill and Constantinides (1976) saw the band; Davis and Norman (1990) constructed the "
                             r"solution; Shreve and Soner (1994) proved it, as a viscosity solution", 12.0, 20, GREY_B)
        foot.to_edge(DOWN, buff=0.4)
        with self.voiceover(
            "The mathematics. The controls are no longer rates but cumulative purchases and sales, each dollar "
            "costing epsilon: a singular control problem. <bookmark mark='a'/> The HJB equation becomes a "
            "variational inequality: the largest of three terms is zero. Where the first binds, the value obeys the "
            "no-trade equation; where the second binds, buying is worth exactly its cost; where the third binds, "
            "selling is. Three regions: buy, sell, and the wedge between them. <bookmark mark='b'/> Power utility "
            "again lets wealth factor out, so only the stock share matters. <bookmark mark='c'/> For small costs the "
            "band's half-width grows as the cube root of the cost: a tiny cost already buys a wide band. Michael "
            "Magill and George Constantinides saw the band in 1976; Mark Davis and Andrew Norman constructed the "
            "solution in 1990; and Steven Shreve and Mete Soner proved it in 1994, as a viscosity solution, with the "
            "tools of chapter four."
        ) as vo:
            step(0)
            vo.wait_until("a")
            step(1)
            vo.wait_until("b")
            step(2)
            vo.wait_until("c")
            step(3)
            self.play(FadeIn(foot))
        self.wait(0.4)
        self.clear_scene()

    def lab(self, d):
        card = lab_card(r"the no-trade band", [
            "def no_trade_band(mu, r, sigma, gamma, eps, dt, steps, grid):",
            "    R = exp((mu - sigma**2/2)*dt + sigma*sqrt(dt)*z)  # nodes",
            "    h = ones_like(grid)          # E[growth^(1-gamma)] to go",
            "    cost = 1 - eps*abs(grid[None, :] - grid[:, None])",
            "    for _ in range(steps):",
            "        G = grid[:, None]*R + (1 - grid[:, None])*exp(r*dt)",
            "        p_next = grid[:, None]*R / G             # drifted share",
            "        C = (G**(1-gamma) * interp(p_next, grid, h) * wq).sum(1)",
            "        J = cost**(1-gamma) * C[None, :]       # trade, then wait",
            "        k = J.argmin(1); h = J[arange(len(grid)), k]",
            "    stay = grid[k] == grid                   # no trade here",
            "    return grid[stay].min(), grid[stay].max()",
        ], source="explainer/quant/house/control.py", width=8.8, font_size=17).to_edge(UP, buff=0.25).to_edge(LEFT, buff=0.3)
        rows = d["rows"]
        outs = ["eps     band            half   eps^(1/3) rule"]
        for r_ in rows:
            outs.append(f"{100 * r_['eps']:<4.1f}%  {100 * r_['lo']:.1f}-{100 * r_['hi']:.1f}%   "
                        f"{100 * r_['half']:.1f}pp  {100 * r_['asym']:.1f}pp")
        with self.voiceover(
            "Lab two: the band by dynamic programming. The House's solver works on a grid of stock shares. Each "
            "month, from every starting share it may trade to any other share, paying the cost, and then the market "
            "moves the share. Working backwards over thirty years, it keeps the best target for every start; the "
            "shares whose best move is to stay put are the band. <bookmark mark='a'/> Run it for gamma three and four "
            f"cost levels. At one percent the band runs from {100 * rows[2]['lo']:.1f} to {100 * rows[2]['hi']:.1f} "
            f"percent. Its half-width is {100 * rows[2]['half']:.1f} points against the cube-root rule's "
            f"{100 * rows[2]['asym']:.1f}: close, and the rule is an asymptote for continuous trading, while the "
            "solver can only trade monthly, which narrows the band most when costs are tiny."
        ) as vo:
            self.play(FadeIn(card, shift=UP * 0.2))
            vo.wait_until("a")
            lab_run(self, card, ["no_trade_band(0.08, 0.02, 0.18, 3, eps, 1/12, 360)"] + outs, run_time=3)
        self.wait(0.4)
        self.clear_scene()

    def slider(self, d):
        rows = d["rows"]
        eg, asym = np.asarray(d["eps_grid"]), np.asarray(d["asym"])
        g = axes([np.log10(0.0005), np.log10(0.03)], [0, 0.11], x_length=6.4, y_length=3.8,
                 xlabel=r"cost per dollar traded, $\varepsilon$ (log scale)", ylabel=r"half-width of the band",
                 xticks=[-3, -2], xfmt=lambda u: {-3: r"0.1\%", -2: r"1\%"}[int(u)], yticks=[0, 0.05, 0.1],
                 yfmt=lambda u: f"{100 * u:.0f}" + r"\text{ pp}", font_size=16).to_edge(LEFT, buff=0.7).shift(DOWN * 0.2)
        ax = g.ax
        line = curve(ax, np.log10(eg), asym, KELLY, stroke_width=3.5)
        dots = VGroup(*[Dot(ax.c2p(np.log10(r_["eps"]), r_["half"]), color=VALUE) for r_ in rows])
        leg = legend([(KELLY, r"$\varepsilon^{1/3}$ rule"), (VALUE, r"dynamic programming, monthly")], font_size=18)
        leg.next_to(g, UP, buff=0.1).align_to(g, LEFT)
        g1 = d["g1"]
        q = pause_card(r"Costs double. Does the band double?", width=5.0, font_size=22).to_edge(RIGHT, buff=0.4).shift(
            UP * 2.0)
        ans = MathTex(r"\times\, 2^{1/3} \approx 1.26", font_size=36, color=KELLY).next_to(q, DOWN, buff=0.25)
        res = VGroup(
            label(r"log utility, 1\% cost, quarterly, 10 years:", font_size=21, color=GREY_A),
            MathTex(rf"\text{{band: }}{100 * g1['lo']:.0f}\%\text{{ to }}{100 * g1['hi']:.0f}\%\ \ (\text{{Merton }}"
                    rf"{100 * g1['pi_merton']:.0f}\%)", font_size=26, color=VALUE),
            MathTex(rf"\text{{net growth: band }}{100 * g1['band']['growth']:.2f}\%,\ \text{{rebalance to Merton }}"
                    rf"{100 * g1['merton']['growth']:.2f}\%", font_size=26),
            MathTex(rf"\text{{turnover: }}{100 * g1['band']['turnover']:.0f}\%\ \text{{vs}}\ "
                    rf"{100 * g1['merton']['turnover']:.0f}\%\text{{ a year}}", font_size=26),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.2).next_to(ans, DOWN, buff=0.5).to_edge(RIGHT, buff=0.4)
        with self.voiceover(
            "Pause and predict: if costs double, does the band double? <bookmark mark='a'/> No. It grows by the cube "
            "root of two, about a quarter. The curve is the cube-root rule, the dots the dynamic program; from a "
            f"half percent to one percent the solver's half-width goes from {100 * rows[1]['half']:.1f} to "
            f"{100 * rows[2]['half']:.1f} points. <bookmark mark='b'/> Is the band worth having? Take a log-utility "
            f"investor paying one percent and trading quarterly. The band, {100 * g1['lo']:.0f} to "
            f"{100 * g1['hi']:.0f} percent around Merton's {100 * g1['pi_merton']:.0f}, grows "
            f"{100 * g1['gain']:.2f} percent a year faster after costs than rebalancing to Merton every quarter, "
            f"and turns over {100 * g1['band']['turnover']:.0f} percent of wealth a year instead of "
            f"{100 * g1['merton']['turnover']:.0f}. Every rebalancing rule used in practice, from pension funds to "
            "Part thirty-one's portfolios, is a version of this band."
        ) as vo:
            self.play(FadeIn(g), FadeIn(q), Create(line), FadeIn(leg))
            vo.wait_until("a")
            self.play(FadeIn(ans), LaggedStart(*[GrowFromCenter(d_) for d_ in dots], lag_ratio=0.2))
            vo.wait_until("b")
            self.play(LaggedStart(*[FadeIn(r_) for r_ in res], lag_ratio=0.3, run_time=2.5))
        self.wait(0.4)
        self.clear_scene()

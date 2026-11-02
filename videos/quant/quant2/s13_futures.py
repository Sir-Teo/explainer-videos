from __future__ import annotations

import numpy as np

from explainer.quant import *  # noqa: F403
from videos.quant.quant2.common import ro, BTC, PART, RATE, TRADE, lab, load, real_data, ts_date

C_ = {r"F_0": TRADE, r"S_0": BTC, r"S_0e^{rT}": BTC, r"h": QC.HOUSE, r"h^*": QC.HOUSE, r"\rho": QC.IDEA}
K_RATIO = 1.2  # sigma_S / sigma_F in the 3D picture


def row(*parts, fs=38):
    return cmath(*parts, colors=C_, font_size=fs)


class Futures(VoiceoverScene, ThreeDScene):
    def construct(self):
        b = load("basis")
        h = load("hedge")
        self.card()
        self.carry(b)
        self.converge(b)
        self.hedge_math()
        self.valley(h)
        self.hedge_lab(h)

    def card(self):
        c = chapter_card(2, r"Futures: carry, basis and the hedge", r"What should a future cost, and how do you hedge "
                         r"with one?", part=PART)
        with self.voiceover("Chapter two. Futures: carry, basis and the hedge."):
            self.play(FadeIn(c[0], shift=UP * 0.2), FadeIn(c[1]))
        self.play(FadeOut(c))

    def carry(self, b):
        r = b["table"]["2021-02-10"]
        fact = MathTex(rf"\text{{10 Feb 2021: March BTC future}}\ {100 * r['basis']:.1f}\%\ \text{{over spot,}}\ "
                       rf"{r['days']:.0f}\ \text{{days to expiry}}", font_size=32, color=BTC).to_edge(UP, buff=0.4)
        rows = [
            row(r"\text{today: borrow } S_0, \text{ buy, sell forward at } F_0", r"\Rightarrow", r"\text{outlay } 0"),
            row(r"\text{at } T: \text{ deliver for } F_0, \text{ repay } S_0e^{rT}", r"\Rightarrow",
                r"F_0 - S_0e^{rT} \text{ riskless}"),
            row(r"F_0", r"\le", r"S_0e^{rT}", r"\quad \text{and, in reverse,} \quad", r"F_0 \ge S_0e^{rT}"),
            row(r"F_0", r"=", r"S_0 e^{(r-q)T}"),
            row(r"\hat r - \hat q", r"=", r"\frac{\ln(F_t/S_t)}{T-t}"),
        ]
        whys = [why(r"cash-and-carry: the coin is bought with borrowed money and sold forward"),
                why(r"no risk, no money down: this must not be positive"),
                why(r"no arbitrage both ways: reverse carry shorts the coin, lends, buys forward"),
                why(r"an asset yielding $q$: hold $e^{-qT}$ units, reinvest the yield"),
                why(r"read backwards: the carry the market is charging, a year's rate")]
        step = ladder(self, rows, whys, keep=5, top=2.6, x=0.6, buff=0.42, edge=6.9)
        ann = MathTex(rf"\ln({r['F']:,.0f}/{r['S']:,.0f})\ /\ ({r['days']:.0f}/365) \approx {100 * r['ann']:.0f}\%\ "
                      r"\text{a year}".replace(",", "{,}"), font_size=34, color=QC.IDEA).to_edge(DOWN, buff=0.5)
        with self.voiceover(
            f"On the tenth of February 2021 the March Bitcoin future on Binance traded {100 * r['basis']:.1f} percent above "
            f"the coin, with {r['days']:.0f} days to go. A forecast? No: a price for carrying the coin. "
            "<bookmark mark='a'/> Borrow cash, buy the coin, sell it forward at F nought: no money down. "
            "<bookmark mark='b'/> At expiry deliver it and repay the loan. That profit is riskless, so it can't be positive. "
            "<bookmark mark='c'/> Run it in reverse and the inequality flips: the forward is spot grown at the interest rate. "
            "<bookmark mark='d'/> An asset paying a yield q grows at r minus q. <bookmark mark='e'/> Read backwards, a "
            f"future tells you the carry the market charges: that February, about {100 * r['ann']:.0f} percent a year, paid "
            "by leveraged longs to whoever bought the coin and sold the future."
        ) as vo:
            self.play(FadeIn(fact))
            vo.wait_until("a")
            step(0)
            vo.wait_until("b")
            step(1)
            vo.wait_until("c")
            step(2)
            vo.wait_until("d")
            step(3)
            vo.wait_until("e")
            step(4)
            self.play(FadeIn(ann))
        self.wait(0.4)
        self.clear_scene()

    def converge(self, b):
        t = np.asarray(b["t"], float)
        d = (t - t[0]) / 86400
        S, F, ann = np.asarray(b["S"]), np.asarray(b["F"]), np.asarray(b["ann"])
        D = float(d[-1])
        top = axes([0, D], [15000, 62000], x_length=7.6, y_length=2.9, ylabel=r"BTC, \$ (hourly)",
                   yticks=[20000, 40000, 60000], yfmt=lambda v: rf"{v / 1000:.0f}\text{{k}}", font_size=17)
        bot = axes([0, D], [0, 0.65], x_length=7.6, y_length=1.9, ylabel=r"implied carry, a year",
                   yticks=[0, 0.3, 0.6], yfmt=lambda v: f"{100 * v:.0f}\\%", xticks=[0, 31, 62, 90],
                   xfmt=lambda v: {0: "1 Dec", 31: "1 Jan", 62: "1 Feb", 90: "1 Mar"}[int(v)], font_size=17)
        VGroup(top, bot).arrange(DOWN, buff=0.35).to_edge(LEFT, buff=0.6).shift(DOWN * 0.1)
        k = ValueTracker(0)
        ls = tracing(top.ax, d, S, k, BTC, stroke_width=2.5)
        lf = tracing(top.ax, d, F, k, TRADE, stroke_width=2.5)
        la = tracing(bot.ax, d, np.clip(ann, 0, 0.65), k, QC.IDEA, stroke_width=2.5)
        dd = np.asarray(b["days"], float)
        cnt = ro(r"\text{days to expiry:}", lambda: max(at_index(dd, k), 0), digits=0, font_size=30,
                      color=GREY_A).to_corner(UR, buff=0.5)
        gap = ro(r"F/S - 1 =", lambda: 100 * (at_index(F, k) / at_index(S, k) - 1), digits=2, font_size=30,
                      color=TRADE, unit=r"\%").next_to(cnt, DOWN, buff=0.25).align_to(cnt, LEFT)
        leg = legend([(TRADE, r"BTCUSD March 2021 future"), (BTC, r"BTC spot (USDT)"),
                      (QC.IDEA, r"$\ln(F/S)/(T-t)$")], font_size=19).to_edge(RIGHT, buff=0.4).shift(UP * 0.6)
        res = VGroup(
            MathTex(rf"\text{{mean}}\ {100 * b['mean_ann']:.0f}\%,\ \text{{max}}\ {100 * b['max_ann']:.0f}\%\ "
                    r"\text{a year}", font_size=28, color=QC.IDEA),
            label(r"(more than 10 days to expiry)", font_size=18, color=GREY_B),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.1).next_to(leg, DOWN, buff=0.4).align_to(leg, LEFT)
        src = real_data(r"Binance coin-margined BTCUSD\_210326 and spot BTCUSDT, hourly closes")
        off = abs(b["last_basis"]) > 0.003
        last_hour = (f"The last hour is off by {abs(100 * b['last_basis']):.1f} percent: the future settles on a dollar "
                     "index, this spot price is in USDT on one exchange." if off else
                     "In the last hour the two agree.")
        with self.voiceover(
            "Now watch a real future converge: Bitcoin in orange, the March 2021 future in blue, hour by hour from December, "
            "its implied carry below. <bookmark mark='a'/> Bitcoin triples, and the future stays above it; the carry swings "
            f"between fifteen and fifty percent a year, {100 * b['mean_ann']:.0f} on average. <bookmark mark='b'/> As expiry "
            "nears the ribbons zip shut, because at expiry a future is the asset. "
            f"{last_hour} That gap between spot and future is the basis."
        ) as vo:
            self.play(FadeIn(top), FadeIn(bot), FadeIn(leg), FadeIn(src))
            self.add(ls, lf, la, cnt, gap)
            vo.wait_until("a")
            self.play(k.animate.set_value(len(t) * 0.75), run_time=7, rate_func=linear)
            self.play(FadeIn(res))
            vo.wait_until("b")
            self.play(k.animate.set_value(len(t) - 1), run_time=4, rate_func=linear)
        for m in (ls, lf, la, cnt, gap):
            m.clear_updaters()
        self.wait(0.4)
        self.clear_scene()

    def hedge_math(self):
        rows = [
            row(r"\operatorname{Var}(\Delta S - h\,\Delta F)", r"=", r"\sigma_S^2 - 2h\rho\sigma_S\sigma_F + h^2\sigma_F^2"),
            row(r"\frac{d}{dh}", r"=", r"-2\rho\sigma_S\sigma_F + 2h\sigma_F^2 = 0"),
            row(r"h^*", r"=", r"\rho\,\frac{\sigma_S}{\sigma_F}"),
            row(r"\operatorname{Var}^*", r"=", r"\sigma_S^2(1-\rho^2), \quad \text{effectiveness } \rho^2"),
            row(r"N^*", r"=", r"h^*\,\frac{Q_A}{Q_F}, \qquad N^*_{\text{equity}} = \beta\,\frac{V_A}{V_F}"),
        ]
        whys = [why(r"the hedged position's change: the variance of a difference"),
                why(r"set the slope in $h$ to zero"),
                why(r"a minimum: the second derivative is $2\sigma_F^2 > 0$"),
                why(r"substitute $h^*$ back"),
                why(r"in contracts: units to hedge over units per contract; for a stock portfolio, its beta")]
        head = label(r"Hedging with a future that is not quite the asset: basis risk", font_size=28,
                     color=QC.HOUSE).to_edge(UP, buff=0.35)
        step = ladder(self, rows, whys, keep=5, top=2.4, x=-0.3, buff=0.42, edge=6.9)
        with self.voiceover(
            "Hedgers use futures the other way round, often on something close to the asset but not the same: basis risk. "
            "How many futures? <bookmark mark='a'/> Sell h of them; the hedged variance is the variance of a difference. "
            "<bookmark mark='b'/> Set its slope in h to zero. <bookmark mark='c'/> The best ratio is the correlation times "
            "the ratio of volatilities, a minimum since the curvature is positive. <bookmark mark='d'/> What's left is one "
            "minus rho squared of the variance: the hedge's effectiveness is rho squared. <bookmark mark='e'/> In contracts, "
            "scale by the sizes; for a stock portfolio, use its beta; and roll the hedge from one expiry to the next."
        ) as vo:
            self.play(FadeIn(head))
            for i, mk in enumerate("abcde"):
                vo.wait_until(mk)
                step(i)
        self.wait(0.4)
        self.clear_scene()

    def valley(self, hd):
        ax = ThreeDAxes(x_range=[0, 1.6, 0.4], y_range=[0, 1, 0.25], z_range=[0, 1.3, 0.5], x_length=6.5,
                        y_length=5.0, z_length=3.2, tips=False,
                        axis_config={"stroke_color": GREY_C, "include_ticks": False, "stroke_width": 2})
        ax.shift(DOWN * 0.4)

        def f(h, rho):
            return min(1 - 2 * h * rho / K_RATIO + h * h / K_RATIO ** 2, 1.3)
        surf = loss_surface(ax, f, (0, 1.6), (0, 1.0), resolution=(32, 24), z_lo=0, z_hi=1.3)
        floor = VMobject(stroke_color=QC.HOUSE, stroke_width=5).set_points_as_corners(
            [ax.c2p(K_RATIO * r_, r_, 1 - r_ * r_) + OUT * 0.03 for r_ in np.linspace(0, 1 / K_RATIO * 1.33, 40)
             if K_RATIO * r_ <= 1.6])
        rho0 = 0.8
        ball_h = ValueTracker(0.05)
        ball = always_redraw(lambda: Dot3D(ax.c2p(ball_h.get_value(), rho0, f(ball_h.get_value(), rho0)) + OUT * 0.08,
                                           radius=0.1, color=YELLOW, resolution=(8, 8)))
        slice_ = VMobject(stroke_color=YELLOW, stroke_width=3).set_points_as_corners(
            [ax.c2p(x, rho0, f(x, rho0)) + OUT * 0.03 for x in np.linspace(0, 1.6, 50)])
        hint = VGroup(label(r"hedge ratio $h$", font_size=24, color=QC.HOUSE),
                      label(r"correlation $\rho$", font_size=24, color=QC.IDEA),
                      label(r"remaining variance / $\sigma_S^2$", font_size=24)).arrange(DOWN, aligned_edge=LEFT,
                                                                                    buff=0.1).to_corner(UL, buff=0.4)
        cap = VGroup(MathTex(r"\text{valley: } h^* = 1.2\,\rho,\ \text{depth } 1-\rho^2", font_size=30, color=QC.HOUSE),
                     MathTex(rf"\text{{ETH on BTC: }} \rho = {hd['rho']:.2f},\ \rho^2 = {hd['rho'] ** 2:.2f}",
                             font_size=28, color=QC.IDEA)).arrange(DOWN, aligned_edge=LEFT).to_corner(DR, buff=0.4)
        params = note(r"$\sigma_S/\sigma_F = 1.2$", font_size=20).to_corner(UR, buff=0.4)
        self.set_camera_orientation(phi=66 * DEGREES, theta=-62 * DEGREES, zoom=0.9)
        self.add_fixed_in_frame_mobjects(hint, cap, params)
        self.remove(hint, cap, params)
        with self.voiceover(
            "Here is the whole problem as a landscape: hedge ratio across, correlation into the screen, leftover variance up. "
            "<bookmark mark='a'/> At rho of point eight the slice is a parabola, and a ball rolls to h star, one point two "
            "times rho. <bookmark mark='b'/> The valley floor runs diagonally, and its depth is one minus rho squared: the "
            "effectiveness."
        ) as vo:
            self.play(FadeIn(hint), FadeIn(params), Create(ax), run_time=1.5)
            self.play(Create(surf), run_time=2.5)
            vo.wait_until("a")
            self.play(Create(slice_))
            self.add(ball)
            self.play(ball_h.animate.set_value(K_RATIO * rho0), run_time=2.5, rate_func=rate_functions.ease_out_quad)
            vo.wait_until("b")
            self.play(Create(floor), FadeIn(cap))
            self.move_camera(theta=-28 * DEGREES, phi=70 * DEGREES, run_time=max(vo.remaining(1.0) - 0.5, 1.0))
        ball.clear_updaters()
        self.move_camera(phi=0, theta=-90 * DEGREES, zoom=1.0,
                         added_anims=[FadeOut(VGroup(ax, surf, floor, slice_, ball)), FadeOut(hint), FadeOut(cap),
                                      FadeOut(params)], run_time=1.2)
        self.clear_scene()

    def hedge_lab(self, h):
        card = lab_card(r"the minimum-variance hedge", [
            "def min_var_hedge(dS, dF):",
            "    c = np.cov(dS, dF)",
            "    h = c[0, 1] / c[1, 1]",
            "    resid = dS - h * dF",
            "    return h, 1 - resid.var() / dS.var()",
            "",
            "h, eff = min_var_hedge(eth_2021_22, btc_2021_22)",
            "hedge_effectiveness(eth_2023, btc_2023, h)",
        ], source="explainer/quant/house/funding.py", width=6.6).to_corner(UL, buff=0.35)
        held = h["eff_out"] > h["eff_in"] - 0.1
        verdict = (f"It held up, though 2023's own best ratio was {h['h_2023']:.2f}: desks refit. " if held else
                   f"Much less: 2023's best ratio was {h['h_2023']:.2f}, and desks refit. ")
        q = desk_question(r"A future at 102, spot at 100, six months, rates 3\%, no yield. Trade?",
                          r"fair value $100e^{0.015} = 101.51$: sell the future, buy spot with borrowed money, "
                          r"lock in 0.49", width=6.0, font_size=22).to_corner(DR, buff=0.35)
        sc = axes([-0.12, 0.12], [-0.15, 0.15], x_length=3.6, y_length=3.0, xlabel=r"BTC daily return",
                  ylabel=r"ETH", font_size=15).to_corner(UR, buff=0.5)
        dots = VGroup(*[Dot(sc.ax.c2p(float(np.clip(x, -0.12, 0.12)), float(np.clip(y, -0.15, 0.15))), radius=0.02,
                            color=QC.IDEA, fill_opacity=0.6) for x, y in zip(h["btc"], h["eth"])])
        fit = Line(sc.ax.c2p(-0.12, -0.12 * h["h"]), sc.ax.c2p(0.12, 0.12 * h["h"]), color=QC.HOUSE, stroke_width=3)
        with self.voiceover(
            "The House does it on data: hedge Ether with Bitcoin, fitted on 2021 and 2022. <bookmark mark='a'/> The ratio is "
            f"{h['h']:.2f}, between {h['h_ci'][0]:.2f} and {h['h_ci'][1]:.2f} by bootstrap, and in sample it removes "
            f"{100 * h['eff_in']:.0f} percent of the variance. <bookmark mark='b'/> Keep that ratio through 2023: it removes "
            f"{100 * h['eff_out']:.0f} percent. "
            f"{verdict}<bookmark mark='c'/> Pause and predict: future a hundred and two, spot a hundred, six months, three percent. "
            "Trade?"
        ) as vo:
            self.play(FadeIn(card), FadeIn(sc))
            self.play(LaggedStart(*[FadeIn(d_) for d_ in dots], lag_ratio=0.002, run_time=1.5))
            vo.wait_until("a")
            out = lab(self, card, [f"h = {h['h']:.3f}   95% bootstrap [{h['h_ci'][0]:.2f}, {h['h_ci'][1]:.2f}]",
                             f"eff = {h['eff_in']:.3f}   (in sample, {h['n_in']} days)"])
            self.play(Create(fit))
            vo.wait_until("b")
            from explainer.zh_text import verbatim
            with verbatim():
                extra = Text(f"{h['eff_out']:.3f}   (2023, {h['n_out']} days)", font="DejaVu Sans Mono",
                             font_size=19, color=QC.GAIN).scale(card.text_scale)
            extra.next_to(out, DOWN, buff=0.12).align_to(out, LEFT)
            self.play(AddTextLetterByLetter(extra), run_time=0.8)
            vo.wait_until("c")
            self.play(FadeOut(sc), FadeOut(dots), FadeOut(fit), FadeIn(q))
        self.wait(1.0)
        self.clear_scene()

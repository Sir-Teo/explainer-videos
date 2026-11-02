from __future__ import annotations

import numpy as np

from explainer.quant import *  # noqa: F403
from videos.quant.quant2.common import BTC, LOSS, PART, lab, load, real_data, ts_date

C_ = {r"P": BTC, r"P_0": BTC, r"L": QC.HOUSE, r"m": LOSS, r"d": QC.IDEA, r"\sigma": LOSS, r"H": QC.IDEA}


def row(*parts, fs=40):
    return cmath(*parts, colors=C_, font_size=fs)


LCOL = {"2": QC.GAIN, "3": QC.IDEA, "10": LOSS}


class Margin(VoiceoverScene, ThreeDScene):
    def construct(self):
        m = load("margin")
        f = load("funding")
        q = load("liq_surface")
        self.card()
        self.mechanics()
        self.formula()
        self.crash(m)
        self.funding(f, m)
        self.reflection(q)
        self.surface(q)

    def card(self):
        c = chapter_card(8, r"Margin and liquidation", r"When does a leveraged position get closed for you?",
                         lit=(2020,), part=PART)
        with self.voiceover("Chapter eight. Margin and liquidation."):
            self.play(FadeIn(c[0], shift=UP * 0.2), FadeIn(c[1]))
        self.play(FadeOut(c))

    def mechanics(self):
        d1 = definition_card(r"Initial margin", r"The collateral posted to open a position: notional divided by the "
                             r"leverage allowed.", width=4.2, color=QC.HOUSE, font_size=22)
        d2 = definition_card(r"Variation margin", r"Every day (or every second, on crypto exchanges) gains are paid "
                             r"in and losses paid out: the position is marked to market.", width=4.2, color=BTC,
                             font_size=22)
        d3 = definition_card(r"Maintenance margin", r"The minimum the account must keep. Below it: a margin call, or, "
                             r"on most crypto exchanges, liquidation on the spot.", width=4.2, color=LOSS, font_size=22)
        row_ = VGroup(d1, d2, d3).arrange(RIGHT, buff=0.3, aligned_edge=UP).move_to(UP * 0.6)
        foot = wrapped_label(r"portfolio margin: a hedged book (long one future, short a close cousin) is margined on "
                             r"its net risk, not leg by leg; how the number is set is the next chapter", 11.0, 22, GREY_A)
        foot.to_edge(DOWN, buff=0.7)
        with self.voiceover(
            "A future costs nothing to enter, but the exchange wants collateral: initial margin, the size over the leverage "
            "allowed. <bookmark mark='a'/> Then gains and losses are paid every day, on crypto exchanges continuously. "
            "<bookmark mark='b'/> Below the maintenance margin comes a margin call, or, on most crypto exchanges, "
            "liquidation on the spot. <bookmark mark='c'/> Hedged books get portfolio margin, on their net risk."
        ) as vo:
            self.play(FadeIn(d1, shift=UP * 0.2))
            vo.wait_until("a")
            self.play(FadeIn(d2, shift=UP * 0.2))
            vo.wait_until("b")
            self.play(FadeIn(d3, shift=UP * 0.2))
            vo.wait_until("c")
            self.play(FadeIn(foot))
        self.wait(0.4)
        self.clear_scene()

    def formula(self):
        rows = [
            row(r"\text{equity}", r"=", r"\frac{P_0}{L}", r"+", r"(P - P_0)"),
            row(r"\frac{P_0}{L} + P - P_0", r"=", r"m", r"P"),
            row(r"P_{\text{liq}}", r"=", r"P_0\,\frac{1 - 1/L}{1 - m}"),
        ]
        whys = [why(r"one coin long, opened at $P_0$ with margin $P_0/L$"),
                why(r"liquidated when equity falls to the maintenance level $m$ of the position"),
                why(r"10x: a 9.5\% fall; 3x: 33\%; 2x: 50\% (with $m = 0.5\%$)")]
        step = ladder(self, rows, whys, keep=3, top=2.4, x=-1.6, buff=0.75, edge=6.9)
        with self.voiceover(
            "How far can the price fall? Hold one coin opened at P nought with margin P nought over L; equity is the margin "
            "plus the gain. <bookmark mark='a'/> Liquidation comes when equity falls to a fraction m of the position. "
            "<bookmark mark='b'/> Solve: with m at half a percent, ten times leverage survives a nine and a half percent "
            "fall, three times a third, two times a half."
        ) as vo:
            step(0)
            vo.wait_until("a")
            step(1)
            vo.wait_until("b")
            step(2)
        self.wait(0.5)
        self.clear_scene()

    def crash(self, m):
        t = np.asarray(m["t"])
        p = np.asarray(m["price"])
        days = (t - t[0]) / 86400
        g = axes([0, 19], [3500, 9500], x_length=6.6, y_length=4.0, xlabel=r"March 2020 (UTC)",
                 ylabel=r"BTC perpetual, Binance, hourly close", xticks=[0, 5, 10, 15],
                 xfmt=lambda v: f"{int(v) + 1}", yticks=[4000, 6000, 8000],
                 yfmt=lambda v: rf"\${v / 1000:.0f}\text{{k}}", font_size=17).to_edge(LEFT, buff=0.5).shift(UP * 0.2)
        ax = g.ax
        k = ValueTracker(0)
        line = tracing(ax, days, p, k, BTC, stroke_width=2.5)
        hl = VGroup()
        for L in ("10", "3", "2"):
            lp = m["runs"][L]["liq_price_formula"]
            hl.add(DashedLine(ax.c2p(0, lp), ax.c2p(19, lp), color=LCOL[L], stroke_width=1.8, dash_length=0.08))
        # the ledger: each account's equity as a bar that drains, crossed out when liquidated
        ledger = VGroup()
        scale = 2.6 / max(m["runs"][L]["margin"] for L in ("2", "3", "10"))
        x_led = 2.2
        for j, L in enumerate(("10", "3", "2")):
            r_ = m["runs"][L]
            eq = np.asarray(r_["equity"], float)
            li = r_["liq_index"]
            y = 1.6 - j * 1.0

            def bar(eq=eq, li=li, y=y, col=LCOL[L]):
                i = int(np.clip(round(k.get_value()), 0, len(eq) - 1))
                if li >= 0 and i >= li:
                    v = float(eq[li])
                else:
                    v = float(eq[i])
                w = max(abs(v) * scale, 0.02)
                rect = Rectangle(width=w, height=0.45, stroke_width=0, fill_color=col if v > 0 else LOSS,
                                 fill_opacity=0.8).move_to([x_led + (w / 2 if v > 0 else -w / 2), y, 0])
                grp = VGroup(rect)
                if li >= 0 and i >= li:
                    grp.add(Cross(rect, stroke_color=LOSS, stroke_width=4, scale_factor=0.8) if w > 0.2 else
                            Cross(scale_factor=0.15, stroke_color=LOSS, stroke_width=4).move_to(rect))
                return grp
            ledger.add(always_redraw(bar))
            ledger.add(MathTex(rf"{L}\times", font_size=30, color=LCOL[L]).move_to([x_led - 0.5, y, 0]))
            ledger.add(label(rf"\${r_['margin']:,.0f} margin; ".replace(",", "{,}") + (
                "liquidated " + ts_date(r_["liq_time"], "%d %b, %H:00") if li >= 0 else "survives"),
                font_size=17, color=GREY_A).move_to([x_led + 1.9, y - 0.38, 0]))
        zero = Line([x_led, 2.0, 0], [x_led, -0.6, 0], color=GREY_C, stroke_width=1.5)
        head = label(r"equity in each account, hour by hour", font_size=20, color=GREY_A).move_to([x_led + 1.6, 2.4, 0])
        res = VGroup(
            MathTex(rf"\text{{1 March}}\ \${m['entry']:,.0f}\ \to\ \text{{13 March}}\ \${m['min_price']:,.0f}".replace(",", "{,}"),
                    font_size=28, color=BTC),
            wrapped_label(rf"the 2x account ends \${-m['runs']['2']['left']:.0f} below zero: a loss the exchange's "
                          r"insurance fund absorbs", 5.6, 20, GREY_A),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.15).to_corner(DR, buff=0.35)
        src = real_data(r"Binance USD-M BTCUSDT perpetual, hourly, with 8-hourly funding; maintenance 0.5\%",
                        corner=DL)
        i10 = m["runs"]["10"]["liq_index"]
        i3 = m["runs"]["3"]["liq_index"]
        i2 = m["runs"]["2"]["liq_index"]
        with self.voiceover(
            f"A real test, hour by hour. On the first of March 2020 Bitcoin was at {m['entry']:,.0f} dollars. Three traders "
            "go long one coin each on a perpetual, at ten, three and two times leverage: dashed lines for their liquidation "
            "prices, and on the right, each account's equity. <bookmark mark='a'/> On the ninth of March the price slips "
            "under the first line: the ten-times account is gone. <bookmark mark='b'/> On the twelfth, Part one's crisis, the "
            "three-times account goes that evening, and early on the thirteenth, at "
            f"{m['min_price']:,.0f} dollars, even two times is closed out, below zero: a hole for the exchange's insurance "
            "fund. <bookmark mark='c'/> Within weeks Bitcoin was back above seven thousand. None of them saw it."
        ) as vo:
            self.play(FadeIn(g), FadeIn(src), FadeIn(zero), FadeIn(head), LaggedStart(*[Create(x) for x in hl]))
            self.add(line, ledger)
            vo.wait_until("a")
            self.play(k.animate.set_value(i10 + 2), run_time=5, rate_func=linear)
            vo.wait_until("b")
            self.play(k.animate.set_value(i3 + 1), run_time=3, rate_func=linear)
            self.play(k.animate.set_value(i2 + 1), run_time=1.5, rate_func=linear)
            self.play(FadeIn(res))
            vo.wait_until("c")
            self.play(k.animate.set_value(len(t) - 1), run_time=2, rate_func=linear)
        line.clear_updaters()
        ledger.clear_updaters()
        self.wait(0.4)
        self.clear_scene()

    def funding(self, f, m):
        card = lab_card(r"the margin account", [
            "for i in range(1, n):",
            "    pay = funding[i] * qty * p[i - 1]",
            "    equity[i] = equity[i-1] + qty * (p[i] - p[i-1]) - pay",
            "    if equity[i] < maintenance * abs(qty) * p[i]:",
            "        liq = i      # closed at this bar's price",
            "        break",
        ], source="explainer/quant/house/funding.py: margin_account", width=7.0).to_edge(UP, buff=0.4).shift(LEFT * 2.6)
        d = definition_card(r"Funding", r"A perpetual swap never expires. To keep its price near spot, longs pay "
                            r"shorts a funding rate every 8 hours when it trades above spot, and shorts pay longs "
                            r"when it trades below.", width=4.6, color=BTC, font_size=20).to_edge(RIGHT, buff=0.3)
        d.shift(UP * 1.6)
        res = VGroup(
            MathTex(rf"\text{{2020: longs paid in}}\ {100 * f['share_positive']:.0f}\%\ \text{{of settlements}}",
                    font_size=26),
            MathTex(rf"\text{{average}}\ {100 * f['annualized']:.1f}\%\ \text{{a year}}", font_size=28, color=BTC),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.15).next_to(d, DOWN, buff=0.4).align_to(d, LEFT)
        with self.voiceover(
            "The House's margin account is that loop: pay the funding, add the gain or loss, check the line. "
            "<bookmark mark='a'/> On March 2020 it closes the three accounts at those hours. And funding is real money: "
            f"through 2020 perpetual longs paid shorts about {100 * f['annualized']:.0f} percent a year, chapter two's carry "
            "again."
        ) as vo:
            self.play(FadeIn(card), FadeIn(d))
            vo.wait_until("a")
            lab(self, card, ["margin_account(btc_hourly, 1, L, 0.005, funding)",
                             "   ".join(f"L={L}: bar {m['runs'][L]['liq_index']}" for L in ("10", "3", "2"))
                             + f"  (left {m['runs']['2']['left']:.0f})"])
            self.play(FadeIn(res))
        self.wait(0.4)
        self.clear_scene()

    def reflection(self, q):
        rows = [
            row(r"d", r"=", r"-\ln\frac{P_{\text{liq}}}{P_0} = -\ln\frac{1 - 1/L}{1 - m}"),
            row(r"\mathbb P\Big(\min_{t \le H} X_t \le -d\Big)", r"=", r"2\,\mathbb P(X_H \le -d)"),
            row(r"\mathbb P(\text{liquidated by } H)", r"=", r"2\,\Phi\!\Big(\frac{-d}{\sigma\sqrt{H}}\Big)"),
        ]
        whys = [why(r"the distance to liquidation, in log price"),
                why(r"the reflection principle: a path that touched $-d$ is as likely to end above it as below"),
                why(r"a driftless Brownian log price with daily volatility $\sigma$")]
        step = ladder(self, rows, whys, keep=3, top=2.5, x=-0.8, buff=0.7, edge=6.9)
        ex = MathTex(rf"5\times:\ d = {q['d5']:.2f} \qquad 10\times:\ d = {q['d10']:.2f}", font_size=36,
                     color=QC.IDEA).to_edge(DOWN, buff=1.4)
        pq = desk_question(r"Go from 5x to 10x. Does the distance to liquidation halve, or worse? And the chance?",
                           width=8.0, font_size=22).to_edge(DOWN, buff=0.25)
        with self.voiceover(
            "How likely is liquidation before it happens? Measure the distance to the liquidation price in log terms. "
            "<bookmark mark='a'/> For a Brownian log price, the reflection principle says the chance of touching it within H "
            "days is twice the chance of ending below it. <bookmark mark='b'/> So it is two Phi of minus d over sigma root H. "
            f"At five times, d is {q['d5']:.2f}; at ten, {q['d10']:.2f}, less than half. Predict what that does to the odds."
        ) as vo:
            step(0)
            vo.wait_until("a")
            step(1)
            vo.wait_until("b")
            step(2)
            self.play(FadeIn(ex))
            self.play(FadeIn(pq))
        self.wait(0.6)
        self.clear_scene()

    def surface(self, q):
        L = np.asarray(q["L"], float)
        H = np.asarray(q["H"], float)
        P = np.asarray(q["P"], float)
        Pf = np.asarray(q["P_formula"], float)
        lx = np.log10(L)
        ax = ThreeDAxes(x_range=[float(lx[0]), float(lx[-1]), 0.5], y_range=[1, 90, 30], z_range=[0, 1, 0.5],
                        x_length=6.4, y_length=5.0, z_length=3.0, tips=False,
                        axis_config={"stroke_color": GREY_C, "include_ticks": False, "stroke_width": 2})
        ax.shift(DOWN * 0.5)

        def interp(A):
            def f(x, y):
                i = np.interp(x, lx, np.arange(len(lx)))
                j = np.interp(y, H, np.arange(len(H)))
                i0, j0 = int(min(i, len(lx) - 2)), int(min(j, len(H) - 2))
                a, b = i - i0, j - j0
                return float((1 - a) * (1 - b) * A[i0, j0] + a * (1 - b) * A[i0 + 1, j0] + (1 - a) * b * A[i0, j0 + 1]
                             + a * b * A[i0 + 1, j0 + 1])
            return f
        surf = loss_surface(ax, interp(P), (float(lx[0]), float(lx[-1])), (1, 90), resolution=(29, 30), z_lo=0, z_hi=1)
        form = Surface(lambda u, v: ax.c2p(u, v, interp(Pf)(u, v)), u_range=(float(lx[0]), float(lx[-1])),
                       v_range=(1, 90), resolution=(14, 15), fill_opacity=0.0, stroke_width=0.8,
                       stroke_color=WHITE, stroke_opacity=0.5)
        i10 = int(np.argmin(np.abs(L - 10)))
        sl = VMobject(stroke_color=YELLOW, stroke_width=5).set_points_as_corners(
            [ax.c2p(lx[i10], h, P[i10, j]) + OUT * 0.03 for j, h in enumerate(H)])
        pin = Dot3D(ax.c2p(lx[i10], 19, P[i10, 18]) + OUT * 0.05, radius=0.09, color=YELLOW, resolution=(8, 8))
        i3 = int(np.argmin(np.abs(L - 3.1)))
        p3, f3 = float(P[i3, 29]), float(Pf[i3, 29])
        p3l, f3l = float(P[i3, 89]), float(Pf[i3, 89])
        hint = VGroup(label(r"leverage (log scale, 1.5x to 50x)", font_size=22, color=QC.HOUSE),
                      label(r"horizon $H$, days (1 to 90)", font_size=22, color=QC.IDEA),
                      label(r"share of days a long was liquidated", font_size=22, color=BTC),
                      label(r"white mesh: the reflection formula", font_size=20, color=GREY_A)).arrange(
            DOWN, aligned_edge=LEFT, buff=0.1).to_corner(UL, buff=0.35)
        cap = VGroup(
            MathTex(rf"10\times,\ 19\ \text{{days: data}}\ {100 * q['p_L10_H19']:.0f}\%,\ \text{{formula}}\ "
                    rf"{100 * q['pf_L10_H19']:.0f}\%", font_size=26, color=YELLOW),
            MathTex(rf"{L[i3]:.1f}\times,\ 30\ \text{{days: data}}\ {100 * p3:.1f}\%,\ \text{{formula}}\ {100 * f3:.1f}\%",
                    font_size=26, color=BTC),
            MathTex(rf"{L[i3]:.1f}\times,\ 90\ \text{{days: data}}\ {100 * p3l:.0f}\%,\ \text{{formula}}\ {100 * f3l:.0f}\%",
                    font_size=26, color=BTC),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.12).to_corner(DR, buff=0.35)
        src = note(rf"Binance BTCUSDT hourly lows, 2020--2025: {q['n_entries']:,} daily entries; "
                   rf"$\sigma$ = {100 * q['sigma_daily']:.1f}\% a day".replace(",", "{,}"), font_size=16).to_corner(DL, buff=0.2)
        tails = p3 > f3
        month = (f"At modest leverage over a month, data beats the formula, {100 * p3:.1f} percent against "
                 f"{100 * f3:.1f}: fat tails." if tails else "At modest leverage over a month, data and formula agree.")
        quarter = (f"the formula is too gloomy, {100 * f3l:.0f} against {100 * p3l:.0f}: Bitcoin's rise rescued "
                   "patient longs." if f3l > p3l else "the data is worse still.")
        self.set_camera_orientation(phi=64 * DEGREES, theta=-130 * DEGREES, zoom=0.85)
        self.add_fixed_in_frame_mobjects(hint, cap, src)
        self.remove(hint, cap, src)
        with self.voiceover(
            "Check it on six years of Bitcoin: a long opened every day from 2020 to 2025, at leverage from one and a half to "
            "fifty, liquidated if the hourly lows touched its line within H days. Colour is the data; the white mesh, the "
            "formula. <bookmark mark='a'/> Leverage turns a slope into a cliff. The pin is ten times for nineteen days, the "
            f"March 2020 trade: liquidated from {100 * q['p_L10_H19']:.0f} percent of starting days. <bookmark mark='b'/> "
            + month
            + " Over ninety days, "
            + quarter
        ) as vo:
            self.play(FadeIn(hint), FadeIn(src), Create(ax), run_time=1.2)
            self.play(Create(surf), run_time=3)
            self.play(Create(form), run_time=2)
            self.move_camera(theta=-110 * DEGREES, run_time=max(vo.until("a") - 0.2, 0.5))
            self.play(Create(sl), FadeIn(pin), FadeIn(cap[0]))
            vo.wait_until("b")
            self.play(FadeIn(cap[1:]))
            self.move_camera(theta=-150 * DEGREES, phi=70 * DEGREES, run_time=max(vo.remaining(1.0) - 0.5, 1.0))
        self.move_camera(phi=0, theta=-90 * DEGREES, zoom=1.0,
                         added_anims=[FadeOut(VGroup(ax, surf, form, sl, pin)), FadeOut(hint), FadeOut(cap),
                                      FadeOut(src)], run_time=1.2)
        self.clear_scene()

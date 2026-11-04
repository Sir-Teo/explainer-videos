from __future__ import annotations

import numpy as np

from explainer.quant import *  # noqa: F403
from videos.quant.quant19.common import LOGN, NORMAL, PART, VAS, ZERO, ask, fit_right, illustration, load


class Options(VoiceoverScene):
    def construct(self):
        h = load("hw")
        self.card()
        self.formulas()
        self.jamshidian()
        self.parity()
        self.smile(h)
        self.strip(load("capstrip"))
        self.grid(h)

    def card(self):
        c = chapter_card(5, r"Caps, floors and swaptions", r"How are options on rates priced and quoted?", part=PART)
        with self.voiceover("Chapter five. Caps, floors and swaptions: the options a rates desk trades."):
            self.play(FadeIn(c[0], shift=UP * 0.2), FadeIn(c[1]))
        self.play(FadeOut(c))

    def formulas(self):
        rows = [cmath(r"\text{caplet}", r"=", r"\delta\,(L_T - K)^+\ \text{paid at } T + \delta", font_size=40,
                      colors={r"\text{caplet}": ZERO}),
                cmath(r"\text{Black}", r"=", r"\delta\,P(0, T{+}\delta)\big[F\,N(d_1) - K\,N(d_2)\big],\ "
                      r"d_{1,2} = \frac{\ln(F/K) \pm \sigma^2 T/2}{\sigma\sqrt T}", font_size=34,
                      colors={r"\text{Black}": LOGN}),
                cmath(r"\text{Bachelier}", r"=", r"\delta\,P(0, T{+}\delta)\big[(F - K)\,N(d) + \sigma_N\sqrt T\,\phi(d)\big],"
                      r"\ d = \frac{F - K}{\sigma_N\sqrt T}", font_size=34, colors={r"\text{Bachelier}": NORMAL}),
                cmath(r"\text{swaption}", r"=", r"A(0)\times\text{Black or Bachelier on the forward swap rate}",
                      font_size=36, colors={r"\text{swaption}": ZERO})]
        whys = [why(r"a cap is a string of caplets: insurance that a floating rate $L$ over each period stays below $K$; "
                    r"a floor is the mirror"),
                why(r"Black (1976): under the measure that pays at $T + \delta$, the forward $F$ is a martingale; if it "
                    r"is lognormal, Black--Scholes with no drift"),
                why(r"Bachelier (1900): if $F$ is normal instead, with absolute volatility $\sigma_N$ in basis points a "
                    r"year: rates may go below zero"),
                why(r"the same with the annuity as numeraire: a payer swaption is a call on the swap rate")]
        step = ladder(self, rows, whys, keep=4, top=2.9, x=-1.4, buff=0.55, edge=6.9)
        with self.voiceover(
            "A caplet pays the excess of a floating rate over a strike, for one period: insurance against rates rising. "
            "A cap is a string of them; a floor is the mirror image. <bookmark mark='a'/> The market quotes them "
            "through Fischer Black's 1976 formula: under the measure that pays at the end of the period, the forward "
            "rate has no drift, so if it is lognormal the price is Black and Scholes with zero drift. "
            "<bookmark mark='b'/> Or through Louis Bachelier's of 1900: the forward is normal, with a volatility in "
            "basis points a year rather than percent of the rate. <bookmark mark='c'/> A swaption, the right to enter "
            "a swap, is the same formula on the forward swap rate, with the annuity in place of the discount factor."
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

    def jamshidian(self):
        rows = [cmath(r"(1 - \textstyle\sum_i c_i P(T, t_i))^+", r"=", r"\textstyle\sum_i c_i\,\big(K_i - P(T, t_i)\big)^+",
                      font_size=36, colors={r"=": WHITE}),
                cmath(r"K_i", r"=", r"P(T, t_i;\ x^*),\quad \textstyle\sum_i c_i P(T, t_i; x^*) = 1", font_size=38,
                      colors={r"K_i": VAS})]
        whys = [why(r"a receiver swaption is a call on a coupon bond with strike 1; in a one-factor model every bond "
                    r"falls as the state $x$ rises, all together"),
                why(r"Jamshidian (1989): find the state $x^*$ where the coupon bond is worth exactly 1; exercise happens "
                    r"on one side of it for every zero, so the option on the sum is a sum of options on zeros, each in "
                    r"closed form (the House's \texttt{HullWhite.swaption})")]
        step = ladder(self, rows, whys, keep=2, top=2.2, x=-0.8, buff=0.8, edge=6.9)
        with self.voiceover(
            "In Hull and White a swaption has a closed form, by a trick of Farshid Jamshidian's. A receiver swaption is "
            "an option on a coupon bond. In a one-factor model every zero-coupon bond falls when the state rises, all "
            "together. <bookmark mark='a'/> So find the one state where the coupon bond is worth exactly par. On one "
            "side of it every zero is in the money, on the other every zero is out: the option on the sum splits into "
            "a sum of options on zeros, each one closed form."
        ) as vo:
            step(0)
            vo.wait_until("a")
            step(1)
        self.wait(0.4)
        self.clear_scene()

    def parity(self):
        from explainer.quant.house import termstructure as TS
        from videos.quant.quant19.compute import _curve_2025, _hw_params
        c = _curve_2025()
        a, sg, *_ = _hw_params()
        hw = TS.HullWhite(c, a, sg)
        T, n = 5.0, 5
        times = T + np.arange(1, n + 1)
        A = float(c.df(times).sum())
        S = float((c.df(T) - c.df(times[-1])) / A)
        rows = VGroup()
        hx = [-4.6, -2.2, 0.2, 2.6, 5.0]
        heads = [r"strike", r"payer", r"receiver", r"payer $-$ receiver", r"$A(0)\,(S_0 - K)$"]
        rows.add(VGroup(*[label(h_, font_size=19, color=GREY_A).move_to([x_, 1.6, 0]) for h_, x_ in zip(heads, hx)]))
        for i, dK in enumerate((-0.01, 0.0, 0.01)):
            K = S + dK
            pay, rec = hw.swaption(K, T, n, 1, payer=True), hw.swaption(K, T, n, 1, payer=False)
            vals = [rf"{100 * K:.2f}\%"] + [f"{0.0 if abs(1e4 * x) < 0.05 else 1e4 * x:.1f}"
                                            for x in (pay, rec, pay - rec, A * (S - K))]
            rows.add(VGroup(*[MathTex(v_, font_size=28).move_to([x_, 0.8 - 0.7 * i, 0]) for v_, x_ in zip(vals, hx)]))
        title = label(rf"5-year options on a 5-year swap, Hull--White; forward swap rate $S_0 = {100 * S:.2f}\%$, bp of "
                      r"notional", font_size=22).to_edge(UP, buff=0.6)
        foot = wrapped_label(r"put--call parity for swaptions: a payer minus a receiver at the same strike is a forward "
                             r"swap, whatever the model. A payer plus a receiver at the money, the straddle, has no "
                             r"exposure to the level of rates, only to how far they move: the market's way to trade "
                             r"rate volatility itself", 12.0, 19, GREY_A).to_edge(DOWN, buff=0.6)
        with self.voiceover(
            "One identity holds in every model. A payer swaption pays if the swap rate ends above the strike, a "
            "receiver if below. Hold a payer and sell a receiver at the same strike, and you are certain to enter the "
            "swap: it is a forward swap, worth the annuity times the gap between the forward rate and the strike. "
            "<bookmark mark='a'/> In the model, at three strikes, the differences match that line to the basis point. "
            "<bookmark mark='b'/> And a payer plus a receiver at the money, a straddle, cares nothing for the direction "
            "of rates, only for how far they move: it is how the market trades rate volatility itself."
        ) as vo:
            self.play(FadeIn(title), FadeIn(rows[0]))
            vo.wait_until("a")
            self.play(LaggedStart(*[FadeIn(r_) for r_ in rows[1:]], lag_ratio=0.3))
            vo.wait_until("b")
            self.play(FadeIn(foot))
        self.wait(0.4)
        self.clear_scene()

    def smile(self, h):
        c = h["caplet"]
        K = (np.asarray(c["K"]) - c["F"]) * 1e4
        nv, lv = np.asarray(c["nvol"]) * 1e4, np.asarray(c["lvol"]) * 100
        g1 = axes([K.min(), K.max()], [0, 160], x_length=5.4, y_length=3.8, xlabel=r"strike minus forward, bp",
                  ylabel=r"normal vol, bp a year", xticks=[-200, -100, 0, 100, 200], yticks=[0, 50, 100, 150], font_size=13)
        g2 = axes([K.min(), K.max()], [0, 50], x_length=5.4, y_length=3.8, xlabel=r"strike minus forward, bp",
                  ylabel=r"Black (lognormal) vol, \%", xticks=[-200, -100, 0, 100, 200], yticks=[0, 25, 50], font_size=13)
        VGroup(g1, g2).arrange(RIGHT, buff=0.8).shift(DOWN * 0.5)
        l1 = curve(g1.ax, K, nv, NORMAL, stroke_width=3.5)
        l2 = curve(g2.ax, K, lv, LOGN, stroke_width=3.5)
        head = label(rf"Hull--White caplets on the 3-month rate, 2 years out; forward {100 * c['F']:.2f}\%", font_size=24
                     ).to_edge(UP, buff=0.5)
        foot = wrapped_label(rf"the same prices, quoted two ways. In normal terms Hull--White is flat, {nv.mean():.0f} bp; "
                             rf"in Black terms it falls from {lv[0]:.0f}\% to {lv[-1]:.0f}\% across strikes: a model with "
                             r"normal rates looks skewed through a lognormal lens. Rule of thumb: $\sigma_N \approx "
                             r"\sigma_{\text{Black}}\,F$", 12.0, 19, GREY_A).to_edge(DOWN, buff=0.4)
        with self.voiceover(
            "Price caplets in Hull and White across a range of strikes, and quote each price both ways. "
            "<bookmark mark='a'/> In normal volatility the model is flat: about "
            f"{nv.mean():.0f} basis points a year at every strike, because its rates are normal. <bookmark mark='b'/> "
            f"In Black volatility the same prices fall from {lv[0]:.0f} percent at low strikes to {lv[-1]:.0f} at high "
            "ones. Neither number is the price; they are two languages for it, and the rule of thumb is that normal vol "
            "is roughly Black vol times the rate."
        ) as vo:
            self.play(FadeIn(head), FadeIn(g1), FadeIn(g2))
            vo.wait_until("a")
            self.play(Create(l1), run_time=1.5)
            vo.wait_until("b")
            self.play(Create(l2), FadeIn(foot), run_time=1.5)
        self.wait(0.4)
        self.clear_scene()

    def strip(self, c):
        t, spot = np.asarray(c["t"]), np.asarray(c["spot"]) * 1e4
        mats, flat, st = np.asarray(c["mats"]), np.asarray(c["flat"]) * 1e4, np.asarray(c["strip"]) * 1e4
        rows = [cmath(r"\text{cap}_M(\sigma^{\text{flat}}_M)", r"=", r"\textstyle\sum_{T_i < M} \text{caplet}_i(\sigma_i)",
                      font_size=34, colors={r"\text{cap}_M(\sigma^{\text{flat}}_M)": ZERO}),
                cmath(r"\sigma_i", r"=", r"(a + bT_i)\,e^{-cT_i} + d", font_size=34, colors={r"\sigma_i": NORMAL})]
        g = axes([0, 10.2], [60, 160], x_length=6.6, y_length=4.0, xlabel=r"years", ylabel=r"normal vol, bp a year",
                 xticks=[0, 2, 4, 6, 8, 10], yticks=[60, 100, 140], font_size=13).to_edge(LEFT, buff=0.5).shift(DOWN * 0.6)
        ax = g.ax
        lspot = curve(ax, t, spot, NORMAL, stroke_width=3, smooth=True)
        dflat = VGroup(*[Dot(ax.c2p(m_, f_), color=ZERO, radius=0.07) for m_, f_ in zip(mats, flat)])
        steps = VGroup()
        for i, m_ in enumerate(mats):
            a_ = mats[i - 1] if i else 0.25
            steps.add(Line(ax.c2p(a_, st[i]), ax.c2p(m_, st[i]), color=QC.HOUSE, stroke_width=4))
        rows_g = VGroup(rows[0], rows[1]).arrange(DOWN, aligned_edge=LEFT, buff=0.3).to_edge(UP, buff=0.5)
        side = VGroup(
            legend([(NORMAL, r"caplet vols: Rebonato's hump"), (ZERO, r"flat cap vols, as quoted"),
                    (QC.HOUSE, r"stripped back from the quotes")], font_size=17),
            wrapped_label(r"a cap is quoted with one flat vol for all its caplets. Bootstrap, as for the curve: the "
                          r"1-year cap fixes the first caplets, the 2-year cap the next, and so on. The flat vols are "
                          r"averages; the hump shows only in the strip", 4.2, 17, GREY_A),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.3).to_edge(RIGHT, buff=0.35).shift(DOWN * 0.6)
        fit_right(side)
        with self.voiceover(
            "Brokers quote a cap with one number: the flat volatility that, used for all its caplets, gives the cap's "
            "price. But each caplet has its own volatility, and a model needs those. <bookmark mark='a'/> Suppose the "
            "caplet vols have the hump shape Riccardo Rebonato parametrized, rising for two years as uncertainty about "
            "policy builds, then falling. <bookmark mark='b'/> The flat vols quoted for caps of one to ten years are "
            "averages of it: smoother, and late to fall. <bookmark mark='c'/> Strip them, the way chapter four of "
            "Part eighteen bootstrapped the curve: the one-year cap fixes the first caplets, each longer cap the "
            "next ones. The hump comes back, as a staircase."
        ) as vo:
            self.play(FadeIn(rows_g[0]), FadeIn(g), FadeIn(side[0]))
            vo.wait_until("a")
            self.play(FadeIn(rows_g[1]), Create(lspot), run_time=1.5)
            vo.wait_until("b")
            self.play(LaggedStart(*[FadeIn(d) for d in dflat], lag_ratio=0.15))
            vo.wait_until("c")
            self.play(LaggedStart(*[Create(l_) for l_ in steps], lag_ratio=0.2, run_time=2.5), FadeIn(side[1]))
        self.add(illustration(r"illustrative caplet vols; forwards and discount factors from the Fed's curve, 31 December 2025"))
        self.wait(0.4)
        self.clear_scene()

    def grid(self, h):
        sw = h["swaptions"]
        exps, tens = (1, 2, 5, 10), (2, 5, 10)
        W, H = 2.4, 0.9
        x0, y0 = -3.0, 1.4
        cells = VGroup()
        vals = np.array([[sw[f"{e}x{t}"]["nvol"] for t in tens] for e in exps]) * 1e4
        lo, hi = vals.min(), vals.max()
        for i, e in enumerate(exps):
            for j, t in enumerate(tens):
                v = vals[i, j]
                col = interpolate_color(ManimColor(QC.SPOT), ManimColor(QC.OPTION), (v - lo) / max(hi - lo, 1e-9))
                box = Rectangle(width=W - 0.1, height=H - 0.1, stroke_width=0, fill_color=col, fill_opacity=0.5)
                box.move_to([x0 + W * j, y0 - H * i, 0])
                cells.add(VGroup(box, MathTex(f"{v:.0f}", font_size=30).move_to(box)))
        heads = VGroup(*[label(rf"{t}-year swap", font_size=19, color=GREY_A).move_to([x0 + W * j, y0 + 0.75, 0])
                         for j, t in enumerate(tens)])
        rows = VGroup(*[label(rf"{e}y expiry", font_size=19, color=GREY_A).move_to([x0 - 2.0, y0 - H * i, 0])
                        for i, e in enumerate(exps)])
        title = label(r"At-the-money swaption normal vols in Hull--White, bp a year", font_size=26).to_edge(UP, buff=0.5)
        side = VGroup(
            MathTex(rf"\text{{5-year ATM cap}} = {100 * h['cap5']:.2f}\%", font_size=28),
            wrapped_label(r"of notional, quarterly caplets at the 2-year forward's strike. One factor and almost no mean "
                          r"reversion give a nearly flat grid; a market grid has a shape this model cannot fit, which is "
                          r"why desks calibrate to the swaptions they hedge", 3.6, 17, GREY_A),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.3).to_edge(RIGHT, buff=0.35)
        fit_right(side)
        with self.voiceover(
            "And swaptions: the grid by option expiry and swap length, the table every rates desk watches, here as the "
            "model prices it, at the money, in normal volatility. <bookmark mark='a'/> It is almost flat, between "
            f"{lo:.0f} and {hi:.0f} basis points. Real grids are not: their shape is information the market prices "
            "and one factor cannot produce. A desk calibrates its model to the options it hedges, and accepts that it "
            "misprices the rest."
        ) as vo:
            self.play(FadeIn(title), FadeIn(heads), FadeIn(rows))
            self.play(LaggedStart(*[FadeIn(c_) for c_ in cells], lag_ratio=0.1, run_time=3))
            vo.wait_until("a")
            self.play(FadeIn(side))
        q = ask(r"a caplet is quoted at 25\% Black volatility with rates at 4\%. Roughly what normal vol is that, in "
                r"basis points?")
        with self.voiceover("A caplet is quoted at twenty-five percent Black volatility with rates at four percent. "
                            "Roughly what is that in basis points of normal volatility?"):
            self.play(FadeIn(q))
        self.wait(0.5)
        self.clear_scene()

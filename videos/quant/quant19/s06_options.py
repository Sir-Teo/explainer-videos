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
        self.smile(h)
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

    def grid(self, h):
        sw = h["swaptions"]
        exps, tens = (1, 2, 5, 10), (2, 5, 10)
        W, H = 2.4, 0.9
        x0, y0 = -1.6, 1.4
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

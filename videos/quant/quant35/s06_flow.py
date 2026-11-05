from __future__ import annotations

import numpy as np

from explainer.quant import *  # noqa: F403
from videos.quant.quant35.common import BAD, DEALER_C, FLOW_C, GOOD, HURDLE, PART, PRICE_C, comma, fit_right, load


class Flow(VoiceoverScene):
    def construct(self):
        f = load("flow")
        self.card()
        self.signed()
        self.regress(f)
        self.concave(f)
        self.reconcile()
        self.persist(load("acf"))
        self.months(f)
        self.hours(f)
        self.cross(load("cross"))
        self.horizons(f)
        self.reading()
        self.question()

    def card(self):
        c = chapter_card(5, r"Kyle's lambda, measured", r"How far does a million dollars of buying move Bitcoin?",
                         part=PART)
        with self.voiceover("Chapter five. Kyle's lambda is the price of order flow. To measure it you need to know which "
                            "trades were buys. Bitcoin's public data says so directly: every minute, how much was bought "
                            "by traders who crossed the spread."):
            self.play(FadeIn(c[0], shift=UP * 0.2), FadeIn(c[1]))
        self.play(FadeOut(c))

    def signed(self):
        rows = [cmath(r"\text{taker buys}_t", r":", r"\text{volume bought at the offer}", font_size=34,
                      colors={r"\text{taker buys}_t": GOOD}),
                cmath(r"\text{flow}_t", r"=", r"(2\,\text{taker buys}_t - \text{volume}_t) \times p_t", font_size=34,
                      colors={r"\text{flow}_t": FLOW_C}),
                cmath(r"r_t", r"=", r"a + \lambda\,\text{flow}_t + e_t", font_size=38, colors={r"\lambda": FLOW_C})]
        whys = [why(r"Binance's one-minute bars record how much of the volume was bought by the side that crossed the "
                    r"spread, the aggressor"),
                why(r"signed flow, in dollars: aggressive buying minus aggressive selling"),
                why(r"Kyle's equation as a regression: the minute's return in basis points on its signed flow in millions "
                    r"of dollars; BTCUSDT spot, 2021--2024, over two million minutes")]
        step = ladder(self, rows, whys, keep=3, top=2.6, x=-0.3, buff=0.55, edge=6.9)
        with self.voiceover(
            "The data. <bookmark mark='a'/> Binance's one-minute bars record how much volume was bought by the side that "
            "crossed the spread, the aggressor. <bookmark mark='b'/> So the signed flow, in dollars, is aggressive "
            "buying minus aggressive selling. <bookmark mark='c'/> And Kyle's equation becomes a regression: each "
            "minute's return on its signed flow, over two million minutes of Bitcoin from 2021 to 2024."
        ) as vo:
            step(0)
            vo.wait_until("a")
            self.wait(0.1)
            vo.wait_until("b")
            step(1)
            vo.wait_until("c")
            step(2)
        self.wait(0.5)
        self.clear_scene()

    def regress(self, f):
        fu = f["full"]
        rows = [cmath(r"\hat\lambda", r"=", rf"{fu['lambda']:.2f}\ \text{{bp per \$1m}}", font_size=38,
                      colors={r"\hat\lambda": FLOW_C}),
                cmath(r"t", r"=", rf"{fu['t']:.0f},\qquad R^2 = {fu['r2']:.2f}", font_size=36),
                cmath(r"\sigma(\text{flow})", r"\approx", rf"\${f['flow_sd']:.2f}\text{{m a minute}}", font_size=34)]
        whys = [why(r"each million dollars of net aggressive buying moves the price by this many basis points, within the "
                    r"minute"),
                why(r"signed flow explains a fifth of the variance of one-minute returns: most of what moves the price is "
                    r"the flow itself"),
                why(r"a typical minute's net flow, so a one-standard-deviation minute moves the price by about four basis "
                    r"points")]
        step = ladder(self, rows, whys, keep=3, top=2.6, x=-0.3, buff=0.55, edge=6.9)
        move = fu["lambda"] * f["flow_sd"]
        with self.voiceover(
            f"The answer. <bookmark mark='a'/> Lambda is {fu['lambda']:.1f} basis points per million dollars of net "
            f"aggressive buying. <bookmark mark='b'/> It is estimated with a t-statistic in the hundreds, and the flow "
            f"explains {100 * fu['r2']:.0f} percent of the variance of minute returns: a large share of what moves the "
            "price is the flow itself. <bookmark mark='c'/> A typical minute's net flow is about "
            f"{f['flow_sd']:.1f} million dollars, so it moves the price by about {move:.0f} basis points."
        ) as vo:
            step(0)
            vo.wait_until("a")
            self.wait(0.1)
            vo.wait_until("b")
            step(1)
            vo.wait_until("c")
            step(2)
        self.wait(0.5)
        self.clear_scene()

    def concave(self, f):
        b = f["buckets"]
        x = np.array([q["flow"] for q in b])
        y = np.array([q["ret"] for q in b])
        lim_x = float(np.ceil(np.abs(x).max() * 2) / 2)
        lim_y = float(np.ceil(np.abs(y).max() / 2) * 2)
        g = axes([-lim_x, lim_x], [-lim_y, lim_y], x_length=7.0, y_length=4.6, xlabel=r"signed flow in the minute, \$m",
                 ylabel=r"mean return, bp", xticks=[-lim_x, 0, lim_x], yticks=[-lim_y, 0, lim_y],
                 xfmt=lambda v: f"{v:.1f}", yfmt=lambda v: f"{v:.0f}", font_size=15).move_to(LEFT * 1.4 + DOWN * 0.2)
        ax = g.ax
        dots = VGroup(*[Dot(ax.c2p(a, c), radius=0.07, color=FLOW_C) for a, c in zip(x, y)])
        lam = f["full"]["lambda"]
        lin = Line(ax.c2p(-lim_x, -lam * lim_x), ax.c2p(lim_x, lam * lim_x), color=GREY_B, stroke_width=1.5)
        xs = np.linspace(-lim_x, lim_x, 81)
        k = float(np.sum(y * np.sign(x) * np.sqrt(np.abs(x))) / np.sum(np.abs(x)))
        sq = curve(ax, xs, k * np.sign(xs) * np.sqrt(np.abs(xs)), HURDLE, stroke_width=2.5)
        leg = legend([(GREY_B, r"linear, slope $\hat\lambda$"), (HURDLE, r"square root, fitted")], font_size=16)
        leg.to_edge(RIGHT, buff=0.3).shift(UP * 1.6)
        fit_right(leg)
        r_small = y[len(y) // 2] / x[len(x) // 2] if x[len(x) // 2] != 0 else float("nan")
        r_big = y[-1] / x[-1]
        with self.voiceover(
            "But the response is not a straight line. <bookmark mark='a'/> Group the minutes by their flow, and the "
            "mean return rises steeply for small flows and flattens for large ones. <bookmark mark='b'/> The largest "
            f"buying minutes move the price {r_big:.0f} basis points per million dollars; the smallest, far more per "
            "dollar. A square root fits better than a line: the concave impact of Part thirty-one, found again in a "
            "market with no dealers at all."
        ) as vo:
            self.play(FadeIn(g))
            vo.wait_until("a")
            self.play(LaggedStart(*[FadeIn(d_) for d_ in dots], lag_ratio=0.05))
            vo.wait_until("b")
            self.play(Create(lin), Create(sq), FadeIn(leg))
        self.wait(0.4)
        self.clear_scene()

    def reconcile(self):
        rows = [cmath(r"\text{Kyle}", r":", r"\Delta p = \lambda\,y\ \ \text{(linear)}", font_size=34, colors={r"\text{Kyle}": FLOW_C}),
                cmath(r"\text{metaorders}", r":", r"\Delta p \approx Y\sigma\sqrt{Q/V}\ \ \text{(concave)}", font_size=34,
                      colors={r"\text{metaorders}": HURDLE}),
                cmath(r"\text{why}", r":", r"\text{normal flow, informative sizes, and order books refilling}", font_size=30)]
        whys = [why(r"linearity is a consequence of normal distributions: with normal values and noise, the best "
                    r"estimate of value given flow is linear"),
                why(r"Part 31's square-root law, measured on large orders executed over hours: impact grows like the root of "
                    r"the order's share of volume"),
                why(r"large flows are partly predictable from earlier flows, so each extra dollar surprises less; and "
                    r"liquidity providers refill the book as a large order proceeds")]
        step = ladder(self, rows, whys, keep=3, top=2.6, x=-0.3, buff=0.55, edge=6.9)
        with self.voiceover(
            "Linear in Kyle, concave in data. Why? <bookmark mark='a'/> Kyle's line comes from normal distributions: "
            "with normal values and noise, the best estimate of value given the flow is linear. "
            "<bookmark mark='b'/> Large orders executed over hours obey Part thirty-one's square-root law instead. "
            "<bookmark mark='c'/> Large flows are partly predictable from earlier flow, so each further dollar surprises "
            "the market less; and liquidity providers refill the book while a large order works. Fat-tailed flow, "
            "rather than normal flow, bends Kyle's line into a curve."
        ) as vo:
            step(0)
            vo.wait_until("a")
            self.wait(0.1)
            vo.wait_until("b")
            step(1)
            vo.wait_until("c")
            step(2)
        self.wait(0.5)
        self.clear_scene()

    def persist(self, a):
        lags = np.log10(np.asarray(a["lags"], float))
        fl = np.asarray(a["flow"], float)
        rt = np.asarray(a["ret"], float)
        g = axes([0, 2.5], [-0.05, 0.2], x_length=7.4, y_length=4.4, xlabel=r"lag, minutes (log scale)",
                 ylabel=r"autocorrelation", xticks=[0, 1, 2], yticks=[0, 0.1, 0.2],
                 xfmt=lambda v: f"{10 ** v:.0f}", font_size=15).move_to(LEFT * 1.4 + DOWN * 0.2)
        ax = g.ax
        zero = DashedLine(ax.c2p(0, 0), ax.c2p(2.5, 0), color=GREY_C, stroke_width=1)
        c1 = curve(ax, lags, fl, FLOW_C, stroke_width=3)
        c2 = curve(ax, lags, rt, PRICE_C, stroke_width=3)
        d1 = VGroup(*[Dot(ax.c2p(x_, y_), radius=0.05, color=FLOW_C) for x_, y_ in zip(lags, fl)])
        d2 = VGroup(*[Dot(ax.c2p(x_, y_), radius=0.05, color=PRICE_C) for x_, y_ in zip(lags, rt)])
        leg = legend([(FLOW_C, r"signed flow"), (PRICE_C, r"returns")], font_size=16).to_edge(RIGHT, buff=0.4)
        leg.shift(UP * 1.6)
        fit_right(leg)
        f1, f240 = fl[0], fl[-1]
        with self.voiceover(
            "A puzzle hidden in the same data. <bookmark mark='a'/> Signed flow is persistent: this minute's net buying "
            f"predicts the next minute's with a correlation of {f1:.2f}, and the correlation is still positive four hours "
            f"later, at {f240:.3f}. Large orders are sliced, so buying follows buying. <bookmark mark='b'/> Yet returns are "
            "almost unpredictable. If flow is predictable and flow moves prices, why are prices not predictable? Because "
            "the market anticipates the flow: the predictable part of each minute's buying has less impact than the "
            "surprise, which is the concavity measured above. Prices respond to the news in the flow, not to "
            "the flow."
        ) as vo:
            self.play(FadeIn(g), Create(zero), FadeIn(leg))
            vo.wait_until("a")
            self.play(Create(c1), FadeIn(d1))
            vo.wait_until("b")
            self.play(Create(c2), FadeIn(d2))
        self.wait(0.4)
        self.clear_scene()

    def months(self, f):
        ms = f["months"]
        x = np.arange(len(ms))
        lam = np.array([m["lambda"] for m in ms])
        vol = np.array([m["vol"] for m in ms])
        top = float(np.ceil(lam.max() / 2) * 2)
        g = axes([0, len(ms) - 1], [0, top], x_length=8.0, y_length=4.2, xlabel=r"2021--2024, by month",
                 ylabel=r"$\hat\lambda$, bp per \$1m", xticks=[0, 12, 24, 36], yticks=[0, top / 2, top],
                 xfmt=lambda v: str(2021 + int(v) // 12), yfmt=lambda v: f"{v:.0f}", font_size=15)
        g.move_to(LEFT * 1.0 + DOWN * 0.2)
        ax = g.ax
        bars = VGroup(*[Rectangle(width=0.1, height=max(1e-3, ax.c2p(0, v)[1] - ax.c2p(0, 0)[1]), fill_color=FLOW_C,
                                  fill_opacity=0.8, stroke_width=0).move_to(ax.c2p(i, v / 2)) for i, v in enumerate(lam)])
        rho = float(np.corrcoef(lam, vol)[0, 1])
        lo, hi = float(lam.min()), float(lam.max())
        st = label(rf"correlation with the month's volatility: {rho:+.2f}", font_size=17, color=HURDLE)
        st.to_edge(UP, buff=0.5)
        with self.voiceover(
            f"Lambda month by month. <bookmark mark='a'/> It ranges from {lo:.1f} to {hi:.1f} basis points per million "
            "dollars. Its correlation with the month's volatility is "
            f"{rho:+.2f}: in volatile months the same flow moves the price further, as Kyle's formula says it should, "
            "because lambda grows with what there is to learn."
        ) as vo:
            self.play(FadeIn(g), FadeIn(st))
            vo.wait_until("a")
            self.play(LaggedStart(*[GrowFromEdge(b_, DOWN) for b_ in bars], lag_ratio=0.02))
        self.wait(0.4)
        self.clear_scene()

    def hours(self, f):
        hs = f["hours"]
        lam = np.array([h["lambda"] for h in hs])
        vol = np.array([h["volume"] for h in hs])
        g = axes([0, 23], [0, float(np.ceil(lam.max()))], x_length=7.4, y_length=4.2, xlabel=r"hour of the day, UTC",
                 ylabel=r"$\hat\lambda$", xticks=[0, 6, 12, 18, 23], yticks=[0, float(np.ceil(lam.max()))],
                 font_size=15).move_to(LEFT * 1.4 + DOWN * 0.2)
        ax = g.ax
        c1 = curve(ax, np.arange(24), lam, FLOW_C, stroke_width=3)
        rho = float(np.corrcoef(lam, vol)[0, 1])
        lo_h, hi_h = int(np.argmin(lam)), int(np.argmax(lam))
        st = VGroup(label(rf"lowest at {lo_h}:00, highest at {hi_h}:00", font_size=17, color=GREY_A),
                    label(rf"correlation with the hour's volume: {rho:+.2f}", font_size=17, color=HURDLE))
        st.arrange(DOWN, aligned_edge=LEFT, buff=0.12).to_edge(RIGHT, buff=0.4).shift(UP * 1.4)
        fit_right(st)
        with self.voiceover(
            "And through the day. <bookmark mark='a'/> Bitcoin trades around the clock, but not evenly. Lambda moves "
            f"with the hour, and its correlation with the hour's volume is {rho:+.2f}. Kyle's depth is the noise to hide "
            "in, and the busiest hours are not automatically the deepest: when the busy hours are also the hours of "
            "news, both the noise and the information arrive together."
        ) as vo:
            self.play(FadeIn(g))
            vo.wait_until("a")
            self.play(Create(c1), FadeIn(st))
        self.wait(0.4)
        self.clear_scene()

    def cross(self, c):
        co = c["coins"]
        x = np.log10([o["sigma_r"] / o["sigma_flow"] for o in co])
        y = np.log10([o["lambda"] for o in co])
        g = axes([0.5, 2.0], [0.3, 1.7], x_length=6.6, y_length=4.4,
                 xlabel=r"$\log_{10}$ (return volatility / flow volatility)", ylabel=r"$\log_{10} \hat\lambda$",
                 xticks=[0.5, 1.0, 1.5, 2.0], yticks=[0.5, 1.0, 1.5], font_size=14).move_to(LEFT * 1.6 + DOWN * 0.2)
        ax = g.ax
        dots = VGroup(*[Dot(ax.c2p(a, b), radius=0.08, color=FLOW_C) for a, b in zip(x, y)])
        labs = VGroup(*[label(o["sym"], font_size=15, color=GREY_A).next_to(d_, UL, buff=0.05) for d_, o in zip(dots, co)])
        b1 = c["slope"]
        a0 = float(np.mean(y) - b1 * np.mean(x))
        fit = Line(ax.c2p(0.5, a0 + 0.5 * b1), ax.c2p(2.0, a0 + 2.0 * b1), color=HURDLE, stroke_width=2)
        rows = VGroup(*[label(rf"{o['sym']}: {o['lambda']:.1f} bp per \$1m", font_size=15, color=GREY_A) for o in co])
        rows.arrange(DOWN, aligned_edge=LEFT, buff=0.08).to_edge(RIGHT, buff=0.4).shift(UP * 1.0)
        fit_right(rows)
        btc, xrp = co[0]["lambda"], co[3]["lambda"]
        with self.voiceover(
            "Across coins, in 2024. <bookmark mark='a'/> Five coins, from Bitcoin to Dogecoin. Moving Bitcoin costs "
            f"{btc:.1f} basis points per million dollars; moving XRP, {xrp:.0f}. <bookmark mark='b'/> Kyle's formula says "
            "lambda should be proportional to what there is to learn over the noise to hide in: return volatility over "
            f"flow volatility. On logarithmic scales the slope is {b1:.2f}, close to one. The constant in front is the "
            "flow's correlation with the return, about one half for every coin: the same market, at five depths."
        ) as vo:
            self.play(FadeIn(g), FadeIn(rows))
            vo.wait_until("a")
            self.play(LaggedStart(*[FadeIn(d_) for d_ in dots], lag_ratio=0.2), FadeIn(labs))
            vo.wait_until("b")
            self.play(Create(fit))
        self.wait(0.4)
        self.clear_scene()

    def horizons(self, f):
        a = f["agg"]
        hx = [-3.6, -1.0, 1.6, 4.0]
        head = VGroup(label(r"bar", font_size=17, color=GREY_B), label(r"$\hat\lambda$, bp per \$1m", font_size=17,
                                                                     color=FLOW_C),
                      label(r"$R^2$", font_size=17, color=GREY_B), label(r"observations", font_size=17, color=GREY_B))
        tab = VGroup(head)
        for k, nm in (("1", r"1 minute"), ("5", r"5 minutes"), ("15", r"15 minutes"), ("60", r"1 hour")):
            r = a[k]
            tab.add(VGroup(label(nm, font_size=20), MathTex(f"{r['lambda']:.2f}", font_size=26),
                           MathTex(f"{r['r2']:.2f}", font_size=26), MathTex(comma(r["n"]), font_size=26)))
        for j, row in enumerate(tab):
            for i, cell in enumerate(row):
                cell.move_to([hx[i], 1.8 - 0.8 * j, 0])
        l1, l60 = a["1"]["lambda"], a["60"]["lambda"]
        r1, r60 = a["1"]["r2"], a["60"]["r2"]
        with self.voiceover(
            "Over longer horizons. <bookmark mark='a'/> Add up the flow and the return over five minutes, fifteen, an "
            f"hour. Lambda falls, from {l1:.1f} to {l60:.1f}: part of each minute's impact reverses, so the permanent "
            f"price of flow is smaller than its first touch. And the R squared rises, from {r1:.2f} to {r60:.2f}: over an "
            "hour, a third of Bitcoin's moves are explained by who was buying."
        ) as vo:
            self.play(FadeIn(tab[0]))
            vo.wait_until("a")
            self.play(LaggedStart(*[FadeIn(r_) for r_ in tab[1:]], lag_ratio=0.3))
        self.wait(0.4)
        self.clear_scene()

    def reading(self):
        cards = VGroup(
            desk_question(r"temporary and permanent impact", r"the minute's impact partly reverses; the part that stays "
                          r"is information, the part that goes is the cost of demanding liquidity (Part 37)", width=12.4,
                          font_size=19),
            desk_question(r"why taker flow moves prices", r"in Kyle the market maker cannot tell informed from noise, so "
                          r"it moves the price for both; here every aggressive order is treated as possibly informed",
                          width=12.4, font_size=19),
            desk_question(r"what this costs a trader", r"a trader who must buy \$10m in a minute moves the price by "
                          r"roughly the square-root law's amount; spread over an hour, far less: the case for slicing "
                          r"orders", width=12.4, font_size=19),
        ).arrange(DOWN, buff=0.25)
        with self.voiceover(
            "What it means. <bookmark mark='a'/> Impact has a temporary part, which reverses, and a permanent part, which "
            "is information. <bookmark mark='b'/> Taker flow moves prices because the other side cannot tell an informed "
            "order from a noise order, exactly Kyle's market maker. <bookmark mark='c'/> And for a trader, the concave "
            "response is the case for slicing a large order over time, Part thirty-seven's subject."
        ) as vo:
            for k, mk in enumerate(("a", "b", "c")):
                vo.wait_until(mk)
                self.play(FadeIn(cards[k], shift=UP * 0.2))
        self.wait(0.4)
        self.clear_scene()

    def question(self):
        q = pause_card(r"with $\lambda = 4.6$ bp per \$1m on a linear model, what does buying \$10m in one minute cost? "
                       r"Why is the real cost lower than that, and the real cost per dollar of \$1m higher?")
        with self.voiceover(
            "Pause and predict. With a lambda of four point six basis points per million on a linear model, what does "
            "buying ten million dollars in one minute cost? And why is the real cost lower than that, while the real cost "
            "per dollar of a one-million order is higher?"
        ):
            self.play(FadeIn(q))
        self.wait(0.5)
        self.clear_scene()

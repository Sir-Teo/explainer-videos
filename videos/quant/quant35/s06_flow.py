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
        self.add(c)
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
                why('base-asset taker imbalance times the bar close approximates signed dollar flow; individual execution prices are not used'),
                why(r"Kyle's equation as a regression: the minute's return in basis points on its signed flow in millions "
                    r"of dollars; BTCUSDT spot, 2021--2024, over two million minutes")]
        step = ladder(self, rows, whys, keep=3, top=2.6, x=-0.3, buff=0.55, edge=6.9)
        self.add(rows[0], whys[0])
        with self.voiceover(
            "Define the measurement. <bookmark mark='a'/> Binance records taker-buy base volume for each one-minute bar. Taker sells equal total base volume minus those buys. <bookmark mark='b'/> Twice taker buys minus total volume is net aggressive base flow. Multiplying by the bar close approximates dollars; it is not a sum of timestamped signed execution values. <bookmark mark='c'/> Regress same-bar log return in basis points on that approximate flow in millions of dollars. Returns use successive available closes, so archive gaps can compress the clock. This venue aggregate does not identify who was informed."
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
        whys = [why('same-bar fitted return per million dollars of approximate net taker flow; descriptive and endogenous'),
                why('R squared is a same-sample fit statistic; the displayed classical t-statistic assumes iid homoskedastic residuals'),
                why('multiply the saved flow standard deviation by the slope for a fitted change, without causal or execution-cost interpretation')]
        step = ladder(self, rows, whys, keep=3, top=2.6, x=-0.3, buff=0.55, edge=6.9)
        move = fu["lambda"] * f["flow_sd"]
        self.add(rows[0], whys[0])
        with self.voiceover(
            f"""The descriptive fit. <bookmark mark='a'/> The slope is {fu['lambda']:.1f} basis points per million dollars. It measures same-bar association; flow and prices respond jointly to news and to one another. <bookmark mark='b'/> The stored classical iid t-statistic is {fu['t']:.0f}, with R squared {fu['r2']:.2f}; it is not a heteroskedasticity- and autocorrelation-robust inference result. <bookmark mark='c'/> Flow standard deviation is {f['flow_sd']:.1f} million dollars, giving a fitted change of {move:.0f} basis points per flow standard deviation. None of these is the causal execution cost of an added parent order."""
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
        self.add(g, dots[0], leg)
        with self.voiceover(
            f"""Bin the observed minutes by signed flow. <bookmark mark='a'/> Each dot is a conditional sample mean; the displayed square-root curve is fitted to those selected bins. <bookmark mark='b'/> The largest positive bin has return divided by flow of {r_big:.0f} basis points per million dollars. This can show nonlinearity in same-minute association. It is not a forecast for executing a large parent order, and no out-of-sample curve comparison or uncertainty bands are supplied. A limit-order market still has liquidity suppliers, even without a designated dealer."""
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
                why('possible mechanisms include predictable flow and book replenishment; these minute bins identify neither their causal contributions nor parent-order costs')]
        step = ladder(self, rows, whys, keep=3, top=2.6, x=-0.3, buff=0.55, edge=6.9)
        self.add(rows[0], whys[0])
        with self.voiceover(
            "Compare the objects before comparing curves. <bookmark mark='a'/> Independent Gaussian value and noise support a linear conditional-expectation price rule in the specified Kyle equilibrium. <bookmark mark='b'/> A parent-order square-root relation concerns identified orders executed over time; our minute bins are different observations and a different estimand. <bookmark mark='c'/> Persistence, changing liquidity and non-Gaussian distributions are possible mechanisms, not conclusions established by this plot. Fat-tailed flow alone does not prove a square-root response, and a concave minute curve does not identify an optimal execution schedule."
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
        self.add(g, c1, leg)
        with self.voiceover(
            f"""Serial association in the saved arrays. <bookmark mark='a'/> Signed-flow autocorrelation is {f1:.2f} at one row and {f240:.3f} at two hundred forty rows. Rows usually represent minutes, but this helper does not reindex missing timestamps. Order slicing is one possible source of persistence, not a causal finding from autocorrelation. <bookmark mark='b'/> The plotted return autocorrelations are much smaller. That does not establish unpredictability under every information set. Anticipation and innovation-based impact can reconcile persistent flow with efficient prices, but this ACF comparison does not estimate such a model."""
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
        self.add(g, bars[0], st)
        with self.voiceover(
            f"""Monthly descriptive slopes range from {lo:.1f} to {hi:.1f} basis points per million dollars. <bookmark mark='a'/> Each fit reuses the research archive; variation can reflect volatility, flow scale, composition and measurement. The correlation with within-month return volatility is {rho:+.2f}. It is an association across selected months, without uncertainty bands or independent structural identification. This plot does not isolate changes in private information."""
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
        self.add(g, c1, st)
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
        labs[4].next_to(dots[4], DR, buff=0.12)
        doge_leader = Line(dots[4].get_bottom(), labs[4].get_left(), color=GREY_C, stroke_width=1)
        b1 = c["slope"]
        a0 = float(np.mean(y) - b1 * np.mean(x))
        fit = Line(ax.c2p(0.5, a0 + 0.5 * b1), ax.c2p(2.0, a0 + 2.0 * b1), color=HURDLE, stroke_width=2)
        rows = VGroup(*[label(rf"{o['sym']}: {o['lambda']:.1f} bp per \$1m", font_size=15, color=GREY_A) for o in co])
        rows.arrange(DOWN, aligned_edge=LEFT, buff=0.08).to_edge(RIGHT, buff=0.4).shift(UP * 1.0)
        fit_right(rows)
        btc, xrp = co[0]["lambda"], co[3]["lambda"]
        self.add(g, dots[0], rows)
        with self.voiceover(
            f"""Five coins in 2024. <bookmark mark='a'/> The fitted same-minute slopes include Bitcoin at {btc:.1f} and XRP at {xrp:.0f} basis points per million dollars. They are associations, not measured costs of an imposed order. <bookmark mark='b'/> The log-log slope against return volatility divided by flow volatility is {b1:.2f}. In OLS with an intercept, lambda times flow standard deviation over return standard deviation equals their sample correlation when samples match. The original marginal standard deviations differ slightly through the initial missing return. This scaling plot is therefore largely an accounting relation, not an independent test of Kyle equilibrium."""
        ) as vo:
            self.play(FadeIn(g), FadeIn(rows))
            vo.wait_until("a")
            self.play(LaggedStart(*[FadeIn(d_) for d_ in dots], lag_ratio=0.2), FadeIn(labs), Create(doge_leader))
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
        self.add(tab[0], tab[1])
        with self.voiceover(
            f"""Aggregate consecutive stored rows into longer bars. <bookmark mark='a'/> From one to sixty rows, the saved slope changes from {l1:.1f} to {l60:.1f} and R squared from {r1:.2f} to {r60:.2f}. These regressions use different aggregation and noise scales. They do not trace one identified trade's response, so they do not establish impact decay or isolate a permanent component. The aggregation does not repair missing calendar bars; sixty rows need not always equal one clock hour."""
        ) as vo:
            self.play(FadeIn(tab[0]))
            vo.wait_until("a")
            self.play(LaggedStart(*[FadeIn(r_) for r_ in tab[1:]], lag_ratio=0.3))
        self.wait(0.4)
        self.clear_scene()

    def reading(self):
        cards = VGroup(
            desk_question(r"association and causal impact", r"Same-bar OLS and conditional means describe an archive. Causal impact needs an identification argument; parent-order cost also needs an execution path and fees.", width=12.4, font_size=25),
            desk_question(r"temporary and permanent components", r"Different aggregation slopes do not follow a single trade through time. Persistence requires an identified response design and a stated horizon.", width=12.4, font_size=25),
            desk_question(r"execution questions", r"Spread, fill prices, participation, information and opportunity cost matter. A net-flow regression alone cannot prescribe slicing or a live order schedule.", width=12.4, font_size=25),
        ).arrange(DOWN, buff=0.25)
        if cards.height > 6.6:
            cards.scale_to_fit_height(6.6)
        self.add(cards[0])
        with self.voiceover("The practical interpretation. <bookmark mark='a'/> Same-bar regressions describe associations in this archive; a causal effect needs an identification argument. <bookmark mark='b'/> Aggregation slopes alone do not separate temporary from permanent impact. <bookmark mark='c'/> To estimate parent-order cost, specify the path, spread, fees, fills and opportunity cost. These measurements motivate further questions; they do not provide a live execution prescription.") as vo:
            for k, mk in enumerate(("a", "b", "c")):
                vo.wait_until(mk)
                self.play(FadeIn(cards[k], shift=UP * 0.2))
        self.clear_scene()

    def question(self):
        eq = MathTex('\\hat\\lambda=4.6\\ \\mathrm{bp}/\\$1\\mathrm m,\\quad F=\\$10\\mathrm m', font_size=32)
        if eq.width > 12.1:
            eq.scale_to_fit_width(12.1)
        conditions = wrapped_label('First compute a fitted same-bar change. Separately stipulate permanent linear execution impact p(q)-p0=lambda q with no spread or fees; derive mean shortfall.', 12.0, 22, GREY_A)
        setup = VGroup(eq, conditions).arrange(DOWN, buff=0.6).move_to(UP * 0.2)
        q = pause_card(r"Use the stated assumptions; derive the result and check its units and interpretation.")
        self.add(setup, q)
        with self.voiceover('Pause and predict. A descriptive slope is four point six basis points per million, with ten million of net flow. Find its fitted return. Separately assume a permanent linear execution path, no spread or fees, and derive average shortfall. Why is neither an identified real parent-order cost?'):
            self.wait(0.4)
        self.wait(0.5)
        self.clear_scene()

from __future__ import annotations

import numpy as np

from explainer.quant import *  # noqa: F403
from videos.quant.quant17.common import BAD, DELTA, GOOD, NET, PART, REF, era_strip, illustration, load, step_xy


class Hook(VoiceoverScene):
    def construct(self):
        h = load("hedge")
        self.title_card()
        self.teaser(h)
        self.live(load("hedge_live"), h)
        self.history()
        self.objectives()
        self.house()

    def title_card(self):
        card = part_title(PART, r"A machine that hedges")
        disc = note(DISCLAIMER, font_size=18, color=GREY_C).to_edge(DOWN, buff=0.35)
        with self.voiceover(
            "Part seventeen. Deep pricing and hedging. Networks that price, calibrate and hedge, trained on the House's "
            "own engines, and checked against them."
        ):
            self.play(FadeIn(card, shift=UP * 0.2), FadeIn(disc))
        self.play(FadeOut(card), FadeOut(disc))

    def teaser(self, h):
        sf = h["band"]["surface"]
        S = np.asarray(sf["S"])
        tau = np.asarray(sf["tau"])
        k = int(np.argmin(np.abs(tau - 0.5)))
        lo, hi = np.asarray(sf["lo"])[k], np.asarray(sf["hi"])[k]
        wl, wh = np.asarray(sf["ww_lo"])[k], np.asarray(sf["ww_hi"])[k]
        dl = (lo + hi) / 2
        g = axes([S[0], S[-1]], [0, 1], x_length=6.4, y_length=4.4, xlabel=r"price, 15 days before expiry",
                 ylabel=r"shares held against one short call", xticks=[90, 100, 110], yticks=[0, 0.5, 1],
                 font_size=15).to_edge(LEFT, buff=0.8).shift(DOWN * 0.2)
        ax = g.ax
        top = ax.plot_line_graph(S, np.clip(hi, 0, 1), add_vertex_dots=False, line_color=NET, stroke_width=3)
        bot = ax.plot_line_graph(S, np.clip(lo, 0, 1), add_vertex_dots=False, line_color=NET, stroke_width=3)
        fill = Polygon(*[ax.c2p(a, b) for a, b in zip(S, np.clip(hi, 0, 1))],
                       *[ax.c2p(a, b) for a, b in zip(S[::-1], np.clip(lo, 0, 1)[::-1])], stroke_width=0,
                       fill_color=NET, fill_opacity=0.25)
        ww = VGroup(DashedVMobject(curve(ax, S, np.clip(wl, 0, 1), WHITE, stroke_width=2), num_dashes=30),
                    DashedVMobject(curve(ax, S, np.clip(wh, 0, 1), WHITE, stroke_width=2), num_dashes=30))
        rows = h["band"]["rows"]
        r5 = next(r for r in rows if abs(r["cost"] - 0.005) < 1e-9)
        side = VGroup(
            label(r"a network learns where not to trade", font_size=24),
            label(r"when every trade costs 0.5\%", font_size=22, color=GREY_A),
            legend([(NET, r"the band it learned: inside, do nothing"), (WHITE, r"the band theory derived in 1997")],
                   font_size=18),
            MathTex(rf"\text{{price to charge: }}{r5['deep']['price']:.2f}\ \ \text{{vs}}\ \ {r5['delta']['price']:.2f}"
                    rf"\ \text{{hedging daily}}", font_size=26, color=NET),
            firm_card(r"J.P. Morgan", r"vanilla index option books on the S\&P 500 and Euro Stoxx hedged by a "
                      r"data-driven engine since 2018, as reported", source=r"Risk.net, 2022", width=4.6, font_size=18),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.28).to_edge(RIGHT, buff=0.5)
        src = illustration(r"the deep hedger of chapters 11--14; a 30-day at-the-money call, 20\% volatility")
        with self.voiceover(
            "This is a neural network learning to hedge an option when every trade costs half a percent. It learns "
            "a corridor around the hedge: inside it, do nothing; outside it, trade back to the nearest edge. "
            "<bookmark mark='a'/> Theory derived such a corridor in 1997, for small costs. The network's is "
            "narrower, and on the same simulated paths it needs a lower price: "
            f"{r5['deep']['price']:.2f} against {r5['delta']['price']:.2f} for hedging every day. "
            "<bookmark mark='b'/> Machines like this already hedge real books: since 2018, Risk.net reported, J.P. "
            "Morgan has hedged vanilla index option books on the S&P 500 and the Euro Stoxx with a data-driven engine."
        ) as vo:
            self.play(FadeIn(g), FadeIn(src), FadeIn(side[0]), FadeIn(side[1]))
            self.play(FadeIn(fill), Create(top), Create(bot), FadeIn(side[2][0]), run_time=2)
            vo.wait_until("a")
            self.play(Create(ww), FadeIn(side[2][1]), FadeIn(side[3]))
            vo.wait_until("b")
            self.play(FadeIn(side[4], shift=UP * 0.2))
        self.wait(0.5)
        self.clear_scene()

    def live(self, L, h):
        S = np.asarray(L["S"])
        n = len(S) - 1
        t = np.arange(n + 1)
        hb, hd, lo, hi = (np.asarray(L[k]) for k in ("band", "delta", "lo", "hi"))
        top = axes([0, n], [S.min() - 1, S.max() + 1], x_length=6.6, y_length=1.6, ylabel=r"price",
                   xticks=[], yticks=[round(S.min()), round(S.max())], font_size=13)
        bot = axes([0, n], [0, 1], x_length=6.6, y_length=3.6, xlabel=r"trading day", ylabel=r"shares held",
                   xticks=[0, 10, 20, 30], yticks=[0, 0.5, 1], font_size=13)
        VGroup(top, bot).arrange(DOWN, buff=0.25, aligned_edge=LEFT).to_edge(LEFT, buff=0.7)
        tr = ValueTracker(0.0)

        def upto(xs, ys):
            k = tr.get_value()
            m = xs <= k + 1e-9
            return xs[m], ys[m]

        def make_price():
            xs, ys = upto(t.astype(float), S)
            if len(xs) < 2:
                return VMobject()
            return curve(top.ax, xs, ys, REF, stroke_width=2.5)

        def make_band():
            k = int(min(tr.get_value(), n - 1))
            pts = [bot.ax.c2p(j, np.clip(hi[j], 0, 1)) for j in range(k + 1)] + \
                  [bot.ax.c2p(j, np.clip(lo[j], 0, 1)) for j in range(k, -1, -1)]
            if k < 1:
                return VMobject()
            return Polygon(*pts, stroke_width=0, fill_color=NET, fill_opacity=0.22)

        def make_step(hh, col):
            def f():
                k = int(min(tr.get_value(), n - 1))
                xs, ys = step_xy(t[:k + 2], hh[:k + 1])
                return VMobject(stroke_color=col, stroke_width=3).set_points_as_corners(
                    [bot.ax.c2p(a, b) for a, b in zip(xs, ys)])
            return f
        price = always_redraw(make_price)
        band = always_redraw(make_band)
        sb = always_redraw(make_step(hb, NET))
        sd = always_redraw(make_step(hd, DELTA))
        cb, cd = np.asarray(L["cost_band"]), np.asarray(L["cost_delta"])
        idx = lambda: int(min(tr.get_value(), n - 1))  # noqa: E731
        rb = readout(r"\text{band: costs paid}", lambda: float(cb[idx()]), digits=3, font_size=26, color=NET)
        rd = readout(r"\text{daily delta: costs paid}", lambda: float(cd[idx()]), digits=3, font_size=26, color=DELTA)
        rows = h["band"]["rows"]
        r5 = next(r for r in rows if abs(r["cost"] - 0.005) < 1e-9)
        side = VGroup(legend([(NET, r"the learned band, and the network's holding"), (DELTA, r"Black--Scholes delta, "
                                                                                               r"rebalanced daily")],
                             font_size=17), rb, rd,
                      wrapped_label(rf"on this path: the band trades on {L['trades_band']} of 30 days, delta on "
                                    rf"{L['trades_delta']}. Over 200{{,}}000 paths the price to charge is "
                                    rf"{r5['deep']['price']:.2f} against {r5['delta']['price']:.2f}", 4.6, 19, GREY_A)
                      ).arrange(DOWN, aligned_edge=LEFT, buff=0.35).to_edge(RIGHT, buff=0.45)
        with self.voiceover(
            "Watch it work on one simulated month: the stock on top; below, the corridor the network draws each day, "
            "and what it holds. <bookmark mark='a'/> Inside the corridor it does nothing; when an edge reaches the "
            "holding, it trades, but only to that edge. The delta hedger trades every single day. "
            f"<bookmark mark='b'/> On this path the band trades on {L['trades_band']} days of thirty, delta on "
            f"{L['trades_delta']}, and the fees pile up accordingly."
        ) as vo:
            self.play(FadeIn(top), FadeIn(bot), FadeIn(side[0]))
            self.add(price, band, sb, sd)
            self.play(FadeIn(rb), FadeIn(rd))
            vo.wait_until("a")
            self.play(tr.animate.set_value(n), run_time=11, rate_func=linear)
            vo.wait_until("b")
            self.play(FadeIn(side[3]))
        for m in (price, band, sb, sd):
            m.clear_updaters()
        rb.num.clear_updaters()
        rd.num.clear_updaters()
        q = label(r"Pause and predict: trading costs double. Does the corridor double in width?", font_size=26,
                  color=QC.IDEA).to_edge(DOWN, buff=0.3)
        with self.voiceover(
            "A question to carry through the part. If trading costs double, does the corridor double in width? "
            "Chapter thirteen derives the answer, and chapter fourteen measures it."
        ):
            self.play(FadeIn(q))
        self.wait(0.4)
        self.clear_scene()

    def history(self):
        I, F, R = QC.IDEA, QC.FIRM, QC.HOUSE
        entries = [(1985, r"Leland: hedging with costs", I), (1989, r"Hodges--Neuberger; Cybenko", I),
                   (1994, r"Hutchinson--Lo--Poggio", I), (1997, r"Whalley--Wilmott's band", I),
                   (2011, r"SR 11-7", R), (2016, r"Hernandez: calibration by network", I),
                   (2017, r"deep BSDE", I), (2019, r"deep hedging; deep stopping", I),
                   (2020, r"differential ML; Quant GANs", I), (2021, r"neural calibration; band networks", I),
                   (2022, r"neural SDE bounds", I), (2026, r"SR 26-2; generative option markets", R)]
        strip = era_strip(entries).move_to(DOWN * 0.3)
        head = label(r"How we got here", font_size=34).to_edge(UP, buff=0.6)
        marks = ["a", "b", "c", "d", "e"]
        groups = [(0, 1), (1, 4), (4, 8), (8, 11), (11, 12)]
        with self.voiceover(
            "How we got here. In 1985 Hayne Leland priced hedging with costs. In 1989 Hodges and Neuberger priced by "
            "indifference, and George Cybenko proved that one hidden layer can approximate any continuous function. "
            "<bookmark mark='a'/> In 1994 Hutchinson, Lo and Poggio let a network learn option prices; in 1997 Whalley "
            "and Wilmott derived the corridor you just saw. In 2011 American supervisors wrote the rules for model risk. "
            "<bookmark mark='b'/> Then the deep wave: calibration by a network in 2016, the deep BSDE solver in 2017, "
            "deep hedging and deep optimal stopping in 2019. <bookmark mark='c'/> Differential machine learning and "
            "generative market models in 2020; neural calibration of rough volatility and band networks in 2021; neural "
            "models for robust bounds in 2022. <bookmark mark='d'/> And in 2026 the supervisors rewrote their rules, "
            "while researchers began to build generators of whole option markets."
        ) as vo:
            self.play(FadeIn(head), Create(strip[0]), FadeIn(strip[1]))
            for (a, b), m in zip(groups, [None] + marks[:4]):
                if m:
                    vo.wait_until(m)
                self.play(LaggedStart(*[FadeIn(strip.items[i], shift=UP * 0.1) for i in range(a, b)], lag_ratio=0.4),
                          run_time=1.5)
        self.wait(0.4)
        self.clear_scene()

    def objectives(self):
        card = objectives_card([
            r"Learning a pricing formula from prices (Hutchinson, Lo and Poggio 1994), and a network's Greeks",
            r"The neural calibrator: rough Bergomi in milliseconds, every week of 2024--2025",
            r"Differential machine learning, and its classical twin, a Gaussian process with gradients",
            r"High dimensions: the deep BSDE solver and deep optimal stopping",
            r"The deep hedger: costs, entropic risk and CVaR, indifference prices, the drift trap",
            r"Where not to trade: Leland, Whalley--Wilmott, and the band a network learns",
            r"Neural SDEs: how far vanillas leave an exotic's price free",
            r"Market generators, and hedgers tested across them",
            r"Production (SR 26-2), what has reached desks, and the frontier of 2023--2026",
        ], color=QC.IDEA)
        with self.voiceover(
            "The plan, in nine steps: pricing networks and their Greeks; neural calibration; derivatives as labels; "
            "a hundred dimensions and early exercise; the deep hedger and its traps; where not to trade; model risk; "
            "market generators; and what it takes to let any of them trade. Every network is trained on screen, more "
            "than once, and checked against an answer we already know."
        ):
            self.play(FadeIn(card.head), LaggedStart(*[FadeIn(r, shift=RIGHT * 0.2) for r in card.rows],
                                                     lag_ratio=0.5, run_time=16))
        self.play(FadeOut(card))

    def house(self):
        chart = house_chart(PART, lit=("vol", "research"))
        with self.voiceover(
            "In the House, the volatility desk gets a deep hedger, and research gets a market generator. "
            "<bookmark mark='a'/> The finale will use that generator to stress-test the whole firm."
        ) as vo:
            self.play(FadeIn(chart))
            vo.wait_until("a")
            self.play(Indicate(chart.desk["research"], color=QC.HOUSE, scale_factor=1.05))
        self.wait(0.3)
        self.clear_scene()

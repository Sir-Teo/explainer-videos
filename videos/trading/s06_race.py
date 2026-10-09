from __future__ import annotations

import numpy as np

from explainer import *  # noqa: F403
from videos.trading.common import (
    FACTS, Plot, fmt_int, fmt_ns, label, load, mtex, node, note, real_tag, schematic_tag, show_part, source, tagged,
)

ETF_COLORS = {"SPY": C.MSG, "IVV": C.SIGNAL, "VOO": C.OURS}


class TheRace(VoiceoverScene):
    def construct(self):
        show_part(self, 3, r"The race", r"why microseconds are worth billions")
        self.lockstep()
        self.epps()
        self.stale()
        self.reaction()

    # ------------------------------------------------------------------
    def lockstep(self):
        r = load("race")
        day = {k: np.array(v, float) for k, v in r["day_mid"].items()}
        pct = {k: 100 * (v / v[0] - 1) for k, v in day.items()}
        lo = min(p.min() for p in pct.values())
        hi = max(p.max() for p in pct.values())
        assert -1.5 < lo and hi < 1.5
        x = np.arange(len(day["SPY"])) / 60 + 9.5
        ch = Plot((9.5, 16), (-0.6, 1.0), width=10.5, height=4.4, x_ticks=[10, 11, 12, 13, 14, 15, 16],
                  x_fmt=lambda v: f"{int(v) if v <= 12 else int(v) - 12}", y_ticks=[-0.5, 0, 0.5, 1.0],
                  y_fmt=lambda v: f"{v:+.1f}\\%" if v else "0").shift(DOWN * 0.4)
        assert lo > -0.6 and hi < 1.0
        lines = VGroup(*[ch.line(x, pct[k], ETF_COLORS[k], 3) for k in ("SPY", "IVV", "VOO")])
        key = VGroup(*[label(t, font_size=26, color=ETF_COLORS[k]) for k, t in [
            ("SPY", r"SPY (State Street)"), ("IVV", r"IVV (BlackRock)"), ("VOO", r"VOO (Vanguard)")]]).arrange(RIGHT, buff=0.6)
        key.next_to(ch, UP, buff=0.2)
        ttl = label(r"three funds, the same 500 stocks: change since the open", font_size=32).to_edge(UP, buff=0.3)
        with self.voiceover(
            "Why does any of this have to be so fast? Here's the clearest example I know. <bookmark mark='e'/> SPY, IVV "
            "and VOO are three exchange-traded funds run by three different companies, and all three hold exactly "
            "the same thing: the 500 stocks of the S&P 500. <bookmark mark='d'/> Over the day, measured by their prices "
            "on Nasdaq, they move in perfect lockstep, as they must."
        ) as vo:
            self.play(FadeIn(ttl), FadeIn(real_tag()))
            vo.wait_until("e")
            self.play(FadeIn(key), Create(ch))
            vo.wait_until("d")
            self.play(*[Create(l) for l in lines], run_time=3)
        self.clear_scene()

        sec = r["second"]
        ch2 = Plot((0, 1000), (-1.6, 1.6), width=10.5, height=4.4, x_ticks=[0, 200, 400, 600, 800, 1000],
                   x_fmt=lambda v: rf"{int(v)}\,\mathrm{{ms}}", y_ticks=[-1, 0, 1],
                   y_fmt=lambda v: f"{v:+.0f}" if v else "0").shift(DOWN * 0.4)
        steps = VGroup()
        for k in ("SPY", "IVV", "VOO"):
            t = np.array(sec[k]["t"], float) / 1e6
            m = np.array(sec[k]["mid"], float)
            base = m[0]
            y = (m - base) / (m[0] / 100) * 100  # basis points from the start of the second
            ts = np.clip(t, 0, 1000)
            xs = np.repeat(ts, 2)[1:]
            ys = np.repeat(y, 2)[:-1]
            xs = np.r_[xs, 1000]
            ys = np.r_[ys, ys[-1]]
            steps.add(ch2.line(xs, ys, ETF_COLORS[k], 3))
        ttl2 = label(r"zoom in: one second, 11:00:00 to 11:00:01", font_size=32).to_edge(UP, buff=0.3)
        yl = ch2.y_title(r"mid-price change, basis points", font_size=22)
        with self.voiceover(
            "<bookmark mark='z'/> Now zoom in to a single second. They don't move together at all. Each fund's price "
            "jumps at its own moments, a few milliseconds apart. Information reaches each of them separately, through "
            "the separate decisions of the traders quoting them."
        ) as vo:
            vo.wait_until("z")
            self.play(FadeIn(ttl2), Create(ch2), FadeIn(yl), FadeIn(real_tag()))
            self.play(*[Create(s) for s in steps], run_time=3, rate_func=linear)
        self.clear_scene()

    # ------------------------------------------------------------------
    def epps(self):
        r = load("race")
        sc = np.array(r["corr_scales_ms"], float)
        c = {k: np.array(v) for k, v in r["corr"].items()}
        i1 = list(sc).index(1)
        i10 = list(sc).index(10)
        i1s = list(sc).index(1000)
        i60 = list(sc).index(60000)
        assert c["SPY_IVV"][i1] < 0.3 and c["SPY_IVV"][i1s] > 0.95 and c["SPY_IVV"][i60] > 0.99
        ch = Plot((0.1, 60000), (0, 1), width=10.5, height=4.3, log_x=True,
                  x_ticks=[0.1, 1, 10, 100, 1000, 10000, 60000],
                  x_fmt=lambda v: fmt_ns(v * 1e6), y_ticks=[0, 0.25, 0.5, 0.75, 1.0], y_fmt=lambda v: f"{v:g}").shift(DOWN * 0.4)
        curves = VGroup(*[ch.line(sc, c[k], col, 4) for k, col in [("SPY_IVV", C.SIGNAL), ("SPY_VOO", C.OURS),
                                                                    ("IVV_VOO", C.MSG)]])
        dots = VGroup(*[ch.dot(sc[i], c["SPY_IVV"][i], C.SIGNAL) for i in range(len(sc))])
        ttl = label(r"how correlated are their price changes? It depends on the time scale", font_size=30).to_edge(UP, buff=0.3)
        xl = label(r"length of the interval", font_size=24, color=GREY_A).next_to(ch.x_labels, DOWN, buff=0.15)
        yl = ch.y_title(r"correlation of returns", font_size=22)
        key = VGroup(label(r"SPY--IVV", font_size=22, color=C.SIGNAL), label(r"SPY--VOO", font_size=22, color=C.OURS),
                     label(r"IVV--VOO", font_size=22, color=C.MSG)).arrange(DOWN, aligned_edge=LEFT, buff=0.08)
        key.move_to(ch.c2p(1.0, 0.82))
        notes = VGroup(
            tagged(rf"1 minute: {c['SPY_IVV'][i60]:.3f}", font_size=22).next_to(ch.c2p(60000, c['SPY_IVV'][i60]), DL, buff=0.1),
            tagged(rf"1 second: {c['SPY_IVV'][i1s]:.2f}", font_size=22).next_to(ch.c2p(1000, c['SPY_IVV'][i1s]), DR, buff=0.1),
            tagged(rf"10 ms: {c['SPY_IVV'][i10]:.2f}", font_size=22).next_to(ch.c2p(10, c['SPY_IVV'][i10]), RIGHT, buff=0.15),
            tagged(rf"1 ms: {c['SPY_IVV'][i1]:.2f}", font_size=22).next_to(ch.c2p(1, c['SPY_IVV'][i1]), RIGHT, buff=0.15),
        )
        bcs = note(rf"Budish, Cramton \& Shim (2015): S\&P 500 futures vs SPY, 2011: {FACTS['bcs_corr_1ms']} at 1 ms",
                   font_size=22, color=GREY_A).to_edge(DOWN, buff=0.25)
        with self.voiceover(
            "We can measure this. <bookmark mark='c'/> Take the price changes of two of these funds over intervals of "
            "a given length, and compute their correlation. <bookmark mark='m'/> Over a minute: 0.999, practically "
            "identical. <bookmark mark='s'/> Over a second: 0.96. <bookmark mark='t'/> Over ten milliseconds, a coin "
            "flip's worth: one half. <bookmark mark='o'/> Over one millisecond, almost nothing. <bookmark mark='b'/> "
            "Economists Eric Budish, Peter Cramton and John Shim found the same collapse in 2011 data, between S&P "
            "500 futures in Chicago and SPY in New York."
        ) as vo:
            self.play(FadeIn(ttl), Create(ch), FadeIn(xl), FadeIn(yl), FadeIn(real_tag()))
            vo.wait_until("c")
            self.play(Create(curves[0]), FadeIn(dots), run_time=2)
            self.play(Create(curves[1]), Create(curves[2]), FadeIn(key))
            for n, m in zip(notes, "msto"):
                vo.wait_until(m)
                self.play(FadeIn(n, shift=UP * 0.1), run_time=0.6)
            vo.wait_until("b")
            self.play(FadeIn(bcs))
        self.clear_scene()

    # ------------------------------------------------------------------
    def stale(self):
        # one fund moves; quotes on the others are stale until someone updates them
        spy = node(r"SPY moves up", color=C.MSG, width=2.6, height=0.8, font_size=24).move_to(LEFT * 4.8 + UP * 1.6)
        book = VGroup(label(r"IVV's book", font_size=26, color=C.SIGNAL),
                      VGroup(Rectangle(width=2.4, height=0.5, stroke_color=C.ASK, fill_color=C.ASK, fill_opacity=0.5),
                             label(r"ask 686.00, now too cheap", font_size=20)),
                      ).arrange(DOWN, buff=0.15).move_to(RIGHT * 4.3 + UP * 0.2)
        book[1][1].move_to(book[1][0])
        sniper = VGroup(node(r"sniper: buy it!", color=C.INFORMED, width=2.6, height=0.7, font_size=22)).move_to(LEFT * 3.2 + DOWN * 0.6)
        maker = VGroup(node(r"maker: cancel it!", color=C.OURS, width=2.6, height=0.7, font_size=22)).move_to(LEFT * 3.2 + DOWN * 2.0)
        tag = schematic_tag()
        with self.voiceover(
            "That collapse is where the race lives. <bookmark mark='u'/> Suppose SPY ticks up. For a few microseconds, "
            "<bookmark mark='b'/> an offer to sell IVV at the old price is stale: too cheap. <bookmark mark='s'/> "
            "Somebody will try to buy it before it disappears. <bookmark mark='m'/> And the market maker who posted it "
            "will try to cancel it before that happens. Both see the same news; both send a message to the same "
            "matching engine. <bookmark mark='w'/> Whoever arrives first wins, and the one that loses, loses money."
        ) as vo:
            self.play(FadeIn(tag))
            vo.wait_until("u")
            self.play(FadeIn(spy, shift=UP * 0.2))
            vo.wait_until("b")
            self.play(FadeIn(book))
            vo.wait_until("s")
            self.play(FadeIn(sniper))
            vo.wait_until("m")
            self.play(FadeIn(maker))
            vo.wait_until("w")
            a = Dot(sniper.get_right(), radius=0.09, color=C.INFORMED)
            b = Dot(maker.get_right(), radius=0.09, color=C.OURS)
            pa = Line(sniper.get_right(), book[1].get_left())
            pb = Line(maker.get_right(), book[1].get_left() + DOWN * 0.1)
            self.add(a, b)
            self.play(MoveAlongPath(a, pa), MoveAlongPath(b, pb), run_time=1.4, rate_func=linear)
            self.play(Flash(book[1], color=C.INFORMED), book[1][0].animate.set_fill(C.TRADE, 0.9))
        facts = VGroup(
            label(r"latency-arbitrage races, London Stock Exchange (Aquilina, Budish \& O'Neill, 2022)", font_size=26),
            label(rf"typical race: {FACTS['abo_race_us'][0]}--{FACTS['abo_race_us'][1]} microseconds, start to finish",
                  font_size=26, color=C.LATENCY),
            label(rf"about {FACTS['abo_races_per_min']} race per minute in every FTSE 100 stock", font_size=26, color=GREY_A),
            label(rf"{100 * FACTS['abo_volume_share']:.0f}\% of all trading volume", font_size=26, color=GREY_A),
            label(rf"over {100 * FACTS['abo_top6_share']:.0f}\% of races won or lost by just 6 firms", font_size=26, color=GREY_A),
            label(rf"worth about \${FACTS['abo_global_per_year'] / 1e9:.0f} billion a year in global stock markets", font_size=26,
                  color=C.PNL_UP),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.16).to_edge(DOWN, buff=0.3)
        facts.add_background_rectangle(color=BACKGROUND, opacity=0.95, buff=0.15)
        with self.voiceover(
            "<bookmark mark='f'/> How often does this happen? Using the London Stock Exchange's own message logs, "
            "which record the losers of each race as well as the winners, Matteo Aquilina, Eric Budish and Peter "
            "O'Neill found that a typical race lasts five to ten microseconds. <bookmark mark='g'/> There's about one "
            "a minute in every major stock, races account for a fifth of all trading, and six firms are on one side "
            "or the other of more than eighty percent of them. <bookmark mark='h'/> In global stock markets, about "
            "five billion dollars a year."
        ) as vo:
            vo.wait_until("f")
            self.play(FadeIn(facts[0]), FadeIn(facts[1]), FadeIn(facts[2]))
            vo.wait_until("g")
            self.play(FadeIn(facts[3]), FadeIn(facts[4]))
            vo.wait_until("h")
            self.play(FadeIn(facts[5]))
        self.clear_scene()

    # ------------------------------------------------------------------
    def reaction(self):
        r = load("race")
        edges = np.array(r["reaction_bins_ns"], float)
        h = np.array(r["reaction"][4], float)  # any order message after an execution
        n = h.sum()
        mode_bin = int(np.argmax(h))
        mode_lo, mode_hi = edges[mode_bin], edges[mode_bin + 1]
        assert 18_000 < mode_lo < 21_000 and h[mode_bin] / n > 0.1
        lo, hi = 1e3, 1e8
        m = (edges[:-1] >= lo) & (edges[1:] <= hi)
        frac = h / n
        ch = Plot((lo, hi), (0, frac[m].max() * 1.12), width=11, height=4.0, log_x=True,
                  x_ticks=[1e3, 1e4, 1e5, 1e6, 1e7, 1e8], x_fmt=lambda v: fmt_ns(v), y_ticks=[]).shift(DOWN * 0.5)
        idx = np.nonzero(m)[0]
        hist = ch.histogram(edges[idx[0]:idx[-1] + 2], frac[idx[0]:idx[-1] + 1], C.MSG, opacity=0.85)
        ttl = label(r"after a trade in a stock, how long until the next order message in that stock?", font_size=30)
        ttl.to_edge(UP, buff=0.3)
        sub = note(rf"every trade of the regular session on Nasdaq, all stocks: {n / 1e6:.1f} million gaps", font_size=22,
                   color=GREY_A).next_to(ttl, DOWN, buff=0.1)
        peak = tagged(r"20--25 $\mu$s", font_size=30, color=C.LATENCY).next_to(ch.c2p(np.sqrt(mode_lo * mode_hi), frac[mode_bin]), RIGHT,
                                                                                buff=0.2)
        lt = load("race")
        dw = lt["deleted_within"]
        fate = lt["fate_rth"]
        q1ms = dw["1ms"] / fate["deleted"]
        q100 = dw["100ms"] / fate["deleted"]
        assert 0.13 < q1ms < 0.17 and 0.40 < q100 < 0.44
        with self.voiceover(
            "And you can see the race in Nasdaq's data. <bookmark mark='h'/> For every trade that day, in every stock, "
            "here is the time until the next order message in the same stock: a new order, a cancel, a change. "
            "<bookmark mark='p'/> Look at that spike, between twenty and twenty-five microseconds. That's the round "
            "trip of the fastest firms: Nasdaq publishes the trade, their machines receive it, decide, and send a "
            "response, and Nasdaq's own systems accept it and put it in line. Every reaction faster than that spike "
            "is a reaction to something other than this trade. <bookmark mark='l'/> The orders themselves are "
            f"fleeting: {100 * q1ms:.0f} percent of the orders canceled that day were canceled within a millisecond of "
            f"being placed, and {100 * q100:.0f} percent within a tenth of a second, faster than a blink."
        ) as vo:
            self.play(FadeIn(ttl), FadeIn(sub), Create(ch), FadeIn(real_tag()))
            vo.wait_until("h")
            self.play(LaggedStart(*[FadeIn(b, shift=UP * 0.1) for b in hist], lag_ratio=0.02), run_time=2.5)
            vo.wait_until("p")
            self.play(FadeIn(peak), Indicate(hist[int(np.searchsorted(idx, mode_bin))], color=C.LATENCY))
            vo.wait_until("l")
            fl = label(rf"canceled within 1 ms: {100 * q1ms:.0f}\% \qquad within 0.1 s: {100 * q100:.0f}\%", font_size=30,
                       color=C.CANCEL).to_edge(DOWN, buff=0.2)
            self.play(FadeIn(fl))
        self.clear_scene()

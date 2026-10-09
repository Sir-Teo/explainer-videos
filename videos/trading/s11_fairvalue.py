from __future__ import annotations

import numpy as np

from explainer import *  # noqa: F403
from videos.trading.common import (
    Ladder, Plot, fmt_int, fmt_ns, label, load, mtex, node, note, real_tag, schematic_tag, show_part, tagged,
)


class FairValue(VoiceoverScene):
    def construct(self):
        show_part(self, 4, r"The brain", r"fair value, quoting, and testing on real queues")
        self.queues()
        self.curve()
        self.microprice()
        self.decay()
        self.many_signals()

    # ------------------------------------------------------------------
    def queues(self):
        lad = Ladder([(18385, [400, 300, 200, 100])], [(18386, [100])], row_h=0.7, price_w=1.6).shift(UP * 0.3)
        q = VGroup(label(r"1{,}000 shares want to buy at 183.85", font_size=26, color=C.BID),
                   label(r"100 shares want to sell at 183.86", font_size=26, color=C.ASK)).arrange(DOWN, buff=0.12)
        q.to_edge(DOWN, buff=1.0)
        quest = label(r"which way will the price move next?", font_size=34).to_edge(UP, buff=0.5)
        tag = schematic_tag()
        with self.voiceover(
            "Speed only matters if you know what to do with it. The other half of the machine is the brain: an "
            "estimate, updated on every message, of what the stock is really worth. <bookmark mark='q'/> Start with "
            "the simplest clue there is. Here a thousand shares are waiting to buy at the bid, and only a hundred "
            "are offered at the ask. <bookmark mark='w'/> Which way is the price more likely to move? The thin side "
            "is the one that's about to run out: one modest buyer clears the ask, and the price ticks up."
        ) as vo:
            self.play(FadeIn(tag))
            vo.wait_until("q")
            self.play(FadeIn(lad), FadeIn(q))
            vo.wait_until("w")
            self.play(FadeIn(quest), Indicate(lad.blocks[("S", 18386)], color=C.ASK))
        self.clear_scene()

    # ------------------------------------------------------------------
    def curve(self):
        s = load("signal")
        ch = Plot((0, 1), (0, 1), width=6.6, height=4.9, x_ticks=[0, 0.25, 0.5, 0.75, 1], y_ticks=[0, 0.25, 0.5, 0.75, 1],
                  x_fmt=lambda v: f"{v:g}", y_fmt=lambda v: f"{v:g}").move_to(LEFT * 2.2 + DOWN * 0.35)
        mids = (np.array(s["NVDA"]["edges"][:-1]) + np.array(s["NVDA"]["edges"][1:])) / 2
        curves = VGroup()
        dots = VGroup()
        for sym, col in (("NVDA", C.SIGNAL), ("SPY", C.MSG)):
            p = np.array([np.nan if v is None else v for v in s[sym]["p_up"]])
            curves.add(ch.line(mids, p, col, 4))
            dots.add(VGroup(*[ch.dot(x, y, col, 0.05) for x, y in zip(mids, p) if np.isfinite(y)]))
        assert s["SPY"]["p_up"][-1] > 0.8 and s["SPY"]["p_up"][0] < 0.2 and s["NVDA"]["p_up"][-1] > 0.75
        diag = DashedLine(ch.c2p(0, 0.5), ch.c2p(1, 0.5), color=GREY_B, dash_length=0.08)
        xl = label(r"imbalance $I = \dfrac{Q_{\mathrm{bid}}}{Q_{\mathrm{bid}} + Q_{\mathrm{ask}}}$", font_size=28).next_to(
            ch.x_labels, DOWN, buff=0.15)
        yl = ch.y_title(r"chance the next move is up", font_size=24)
        key = VGroup(label(r"SPY", font_size=26, color=C.MSG), label(r"NVDA", font_size=26, color=C.SIGNAL)).arrange(
            DOWN, aligned_edge=LEFT, buff=0.1).move_to(ch.c2p(0.15, 0.85))
        side = VGroup(
            label(r"every change of the best bid or ask,", font_size=24, color=GREY_A),
            label(r"9:30 to 4:00, one-cent spreads only:", font_size=24, color=GREY_A),
            label(rf"{fmt_int(s['SPY']['states'])} states in SPY", font_size=24, color=C.MSG),
            label(rf"{fmt_int(s['NVDA']['states'])} in NVDA", font_size=24, color=C.SIGNAL),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.08).to_edge(RIGHT, buff=0.5).shift(UP * 1.4)
        hi = tagged(rf"bid side 95\%+ of the queue:\\next move up {100 * s['SPY']['p_up'][-1]:.0f}\% of the time (SPY)",
                    font_size=22, color=C.MSG).next_to(side, DOWN, buff=0.5).align_to(side, LEFT)
        with self.voiceover(
            "Let's test that on the real data. <bookmark mark='i'/> Define the imbalance as the fraction of the shares "
            "waiting at the best bid and the best ask that are on the bid side. <bookmark mark='c'/> Then, for every moment of the day when "
            "the spread was one cent, check which way the mid-price moved next. <bookmark mark='r'/> The relationship "
            "is almost a straight line. <bookmark mark='h'/> When nearly all the waiting shares are on the bid, SPY's "
            "next move was up 85 percent of the time; when they're nearly all on the ask, down 85 percent of the time. "
            "Free information, sitting in plain sight in the order book, for anyone fast enough to use it."
        ) as vo:
            self.play(FadeIn(real_tag()))
            vo.wait_until("i")
            self.play(Create(ch), FadeIn(xl), FadeIn(yl), Create(diag))
            vo.wait_until("c")
            self.play(FadeIn(side))
            vo.wait_until("r")
            self.play(Create(curves[0]), FadeIn(dots[0]), Create(curves[1]), FadeIn(dots[1]), FadeIn(key), run_time=2.5)
            vo.wait_until("h")
            self.play(FadeIn(hi))
        self.clear_scene()

    # ------------------------------------------------------------------
    def microprice(self):
        bid, ask, qb, qa = 183.85, 183.86, 1000, 100
        imb = qb / (qb + qa)
        micro = imb * ask + (1 - imb) * bid
        nl = NumberLine(x_range=[183.85, 183.86, 0.0025], length=9, include_ticks=True, color=GREY_B).shift(DOWN * 0.2)
        bl = VGroup(Dot(nl.n2p(bid), color=C.BID, radius=0.1), label(r"bid 183.85", font_size=26, color=C.BID))
        bl[1].next_to(bl[0], DOWN, buff=0.25)
        al = VGroup(Dot(nl.n2p(ask), color=C.ASK, radius=0.1), label(r"ask 183.86", font_size=26, color=C.ASK))
        al[1].next_to(al[0], DOWN, buff=0.25)
        ml = VGroup(Triangle(color=C.MID, fill_opacity=1).scale(0.1).rotate(PI).next_to(nl.n2p(183.855), UP, buff=0.05),
                    label(r"mid 183.855", font_size=24, color=C.MID))
        ml[1].next_to(ml[0], UP, buff=0.1)
        mp = VGroup(Triangle(color=C.SIGNAL, fill_opacity=1).scale(0.13).rotate(PI).next_to(nl.n2p(micro), UP, buff=0.05),
                    label(rf"weighted mid {micro:.4f}", font_size=26, color=C.SIGNAL))
        mp[1].next_to(mp[0], UP, buff=0.1)
        f = mtex(r"P_{\mathrm{fair}} = I\cdot P_{\mathrm{ask}} + (1-I)\cdot P_{\mathrm{bid}}", font_size=40, color=C.SIGNAL)
        f.to_edge(UP, buff=0.7)
        ex = mtex(rf"I = \tfrac{{1000}}{{1000+100}} = {imb:.3f}", font_size=34).next_to(f, DOWN, buff=0.3)
        ms = note(r"a refined version is Stoikov's ``microprice'' (2018)", font_size=22).to_edge(DOWN, buff=0.5)
        with self.voiceover(
            "That gives us a first estimate of fair value. <bookmark mark='f'/> Instead of the plain mid-price, weight "
            "each side by the imbalance: <bookmark mark='e'/> with a thousand shares bid and a hundred offered, the "
            "imbalance is 0.91, <bookmark mark='m'/> and the fair price sits not halfway between bid and ask, but most "
            "of the way toward the ask. Researchers have refined this idea; Sasha Stoikov's version is called the "
            "microprice."
        ) as vo:
            vo.wait_until("f")
            self.play(FadeIn(f), Create(nl), FadeIn(bl), FadeIn(al), FadeIn(ml))
            vo.wait_until("e")
            self.play(FadeIn(ex))
            vo.wait_until("m")
            self.play(FadeIn(mp, shift=DOWN * 0.1), FadeIn(ms))
        self.clear_scene()

    # ------------------------------------------------------------------
    def decay(self):
        s = load("signal")
        hs = np.array(s["SPY"]["horizons_ms"], float)
        ch = Plot((1, 300000), (0, 0.18), width=10.5, height=4.2, log_x=True, x_ticks=[1, 10, 100, 1e3, 1e4, 1e5],
                  x_fmt=lambda v: fmt_ns(v * 1e6), y_ticks=[0, 0.05, 0.1, 0.15], y_fmt=lambda v: f"{v:g}").shift(DOWN * 0.4)
        lines = VGroup(ch.line(hs, s["SPY"]["corr"], C.MSG, 4), ch.line(hs, s["NVDA"]["corr"], C.SIGNAL, 4))
        k = int(np.argmax(s["SPY"]["corr"]))
        assert hs[k] == 50 and s["SPY"]["corr"][list(hs).index(60000)] < 0.03
        ttl = label(r"how well does imbalance predict the price change over the next\dots", font_size=30).to_edge(UP, buff=0.35)
        yl = ch.y_title(r"correlation with the future price change", font_size=22)
        key = VGroup(label(r"SPY", font_size=24, color=C.MSG), label(r"NVDA", font_size=24, color=C.SIGNAL)).arrange(
            DOWN, aligned_edge=LEFT, buff=0.08).move_to(ch.c2p(20000, 0.15))
        pk = tagged(r"strongest: about 50 ms ahead", font_size=24, color=C.MSG).next_to(ch.c2p(50, s["SPY"]["corr"][k]), UP, buff=0.15)
        gone = tagged(r"a minute ahead: gone", font_size=24, color=GREY_A).next_to(ch.c2p(60000, 0.02), UP, buff=0.3)
        with self.voiceover(
            "But it's a fleeting kind of knowledge. <bookmark mark='c'/> Here's how strongly the imbalance predicts "
            "the price change over the next millisecond, second, or minute. <bookmark mark='p'/> It's strongest about "
            "fifty milliseconds ahead, <bookmark mark='g'/> and a minute ahead it's worth nothing. Whatever it knows, "
            "the market learns almost immediately. A signal like this is only worth having if you can act on it "
            "within milliseconds, which is why the brain and the pipe have to be built together."
        ) as vo:
            self.play(FadeIn(ttl), FadeIn(real_tag()))
            vo.wait_until("c")
            self.play(Create(ch), FadeIn(yl))
            self.play(Create(lines[0]), Create(lines[1]), FadeIn(key), run_time=2)
            vo.wait_until("p")
            self.play(FadeIn(pk))
            vo.wait_until("g")
            self.play(FadeIn(gone))
        self.clear_scene()

    # ------------------------------------------------------------------
    def many_signals(self):
        center = node(r"fair value\\{\small and how sure we are}", C.SIGNAL, width=3.4, height=1.5, font_size=28)
        inputs = [
            (r"this stock's own book", C.MSG), (r"futures in Chicago,\\via microwave", C.MICROWAVE),
            (r"the same stock on\\a dozen other exchanges", C.MSG), (r"related stocks\\and ETFs", C.OURS),
            (r"options", C.INFORMED), (r"news, in\\machine-readable form", GREY_B),
        ]
        nodes = VGroup()
        for i, (t, c) in enumerate(inputs):
            a = PI / 2 + i * TAU / len(inputs) + PI / 6
            n = node(t, c, width=3.1, height=1.0, font_size=20).move_to(np.array([np.cos(a) * 4.7, np.sin(a) * 2.6, 0]))
            nodes.add(n)
        arrows = VGroup(*[Arrow(n.get_center(), center.get_center(), buff=1.0, color=GREY_B, stroke_width=2.5) for n in nodes])
        etf = note(r"an ETF and the hundreds of stocks inside it must agree: Jane Street's traditional specialty",
                   font_size=22, color=GREY_A).to_edge(DOWN, buff=0.15)
        with self.voiceover(
            "A real fair-value model combines many such clues. <bookmark mark='a'/> The stock's own order book, "
            "<bookmark mark='b'/> S&P 500 futures, arriving from Chicago by microwave, <bookmark mark='c'/> the same "
            "stock's quotes on a dozen other exchanges, <bookmark mark='d'/> related stocks and funds: an ETF and the "
            "hundreds of stocks inside it must agree, and keeping them in line has long been one of Jane Street's "
            "specialties. <bookmark mark='e'/> Options, and news. The models range from simple weighted averages to "
            "machine learning trained on years of data, which is why these firms run some of the largest computing "
            "clusters in finance. But every one of them produces the same thing, many times a second: a number, and "
            "how sure we are of it."
        ) as vo:
            self.play(FadeIn(center))
            for i, m in enumerate("abcde"):
                vo.wait_until(m)
                idx = [0] if m == "a" else [i] if m in "bcd" else [4, 5]
                self.play(*[FadeIn(nodes[j]) for j in idx], *[GrowArrow(arrows[j]) for j in idx], run_time=0.7)
                if m == "d":
                    self.play(FadeIn(etf))
            self.play(Indicate(center, color=C.SIGNAL))
        self.clear_scene()

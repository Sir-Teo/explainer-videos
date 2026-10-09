from __future__ import annotations

import numpy as np

from explainer import *  # noqa: F403
from videos.trading.common import (
    DAY_LABEL, FACTS, Plot, fmt_int, label, load, loop_diagram, note, source, tagged,
)


def hms(sec: float) -> str:
    sec = int(sec)
    return f"{sec // 3600}:{sec % 3600 // 60:02d}"


class Hook(VoiceoverScene):
    def construct(self):
        self.before_two()
        self.the_day()
        self.the_firms()
        self.the_loop()

    # ------------------------------------------------------------------
    def before_two(self):
        w = load("windows")
        ks = np.array(w["bins_100ms"])  # 100 ms bins from 13:59:58.0 to 14:00:03.0
        bt = w["by_type"]
        dele = np.array(bt["D"]) + np.array(bt["X"])
        exe = np.array(bt["E"]) + np.array(bt["C"]) + np.array(bt["P"])
        add = np.array(bt["A"]) + np.array(bt["F"]) + np.array(bt["U"])
        tot = np.array(w["total"])
        k5 = list(ks).index(-5)
        assert dele[k5] > 16_000 and w["symbols"][k5] > 1400 and bt["D"][k5] == 16157
        after3 = int(tot[ks >= 0].sum())
        before1 = int(tot[(ks >= -10) & (ks < 0)].sum())
        early = tot[ks < -10].mean() * 10  # messages per second, 13:59:58
        assert 10_000 < early < 30_000
        ymax = 55_000
        assert tot.max() < ymax
        ch = Plot((-2, 3), (0, ymax), width=11.5, height=4.4, x_ticks=[-2, -1, 0, 1, 2, 3],
                  x_fmt=lambda v: label(["1:59:58", "1:59:59", "2:00:00", "2:00:01", "2:00:02", "2:00:03"][int(v) + 2],
                                        font_size=22, color=GREY_A),
                  y_ticks=[0, 20_000, 40_000], y_fmt=lambda v: fmt_int(v)).shift(DOWN * 0.55)
        ytl = ch.y_title(r"Nasdaq messages per 0.1 second", color=GREY_A)
        key = VGroup(*[VGroup(Square(0.2, stroke_width=0, fill_color=c, fill_opacity=0.9), label(t, font_size=22, color=c)
                              ).arrange(RIGHT, buff=0.12) for c, t in [(C.CANCEL, "cancellations"),
                                                                       (C.MSG, "new and changed orders"),
                                                                       (C.TRADE, "trades")]]).arrange(RIGHT, buff=0.4)
        key.next_to(ch, UP, buff=0.15).align_to(ch, RIGHT)
        bars = VGroup()
        for i, k in enumerate(ks):
            x0, x1 = k / 10 + 0.008, (k + 1) / 10 - 0.008
            col = VGroup()
            base = 0
            for v, c in [(dele[i], C.CANCEL), (add[i], C.MSG), (exe[i], C.TRADE)]:
                if v <= 0:
                    continue
                p0, p1 = ch.c2p(x0, base), ch.c2p(x1, base + v)
                col.add(Rectangle(width=p1[0] - p0[0], height=max(p1[1] - p0[1], 1e-3), stroke_width=0, fill_color=c,
                                  fill_opacity=0.9).move_to((p0 + p1) / 2))
                base += v
            bars.add(col)
        when = label(DAY_LABEL + r" \quad Nasdaq's data center, Carteret, New Jersey", font_size=28,
                     color=GREY_A).to_edge(UP, buff=0.35)
        clock_v = ValueTracker(-2.0)

        def clock_text():
            v = clock_v.get_value()
            sec = 14 * 3600 + v
            whole = int(np.floor(sec + 1e-9))
            ms = int(round((sec - whole) * 1000)) % 1000
            s = f"{whole // 3600 - 12}:{whole % 3600 // 60:02d}:{whole % 60:02d}.{ms:03d} pm"
            return Text(s, font="DejaVu Sans Mono", font_size=38, color=C.LATENCY).next_to(when, DOWN, buff=0.2)

        clock = always_redraw(clock_text)

        def reveal(upto):
            return [FadeIn(bars[i], shift=UP * 0.05) for i, k in enumerate(ks) if k / 10 < upto]

        shown = {"n": 0}

        def advance(to, run_time):
            idx = [i for i, k in enumerate(ks) if k / 10 < to and i >= shown["n"]]
            shown["n"] = max([shown["n"]] + [i + 1 for i in idx])
            anims = [clock_v.animate(rate_func=linear).set_value(to)]
            if idx:
                anims.append(LaggedStart(*[FadeIn(bars[i], shift=UP * 0.05) for i in idx], lag_ratio=1.0,
                                         rate_func=linear))
            self.play(*anims, run_time=run_time)

        src = source(r"Nasdaq TotalView-ITCH 5.0, " + DAY_LABEL, font_size=18)
        pull = tagged(rf"1:59:59.5: {fmt_int(bt['D'][k5])} cancellations\\in 0.1 s, across {fmt_int(w['symbols'][k5])} stocks",
                      font_size=24, color=C.CANCEL)
        pull.next_to(ch.c2p(-0.45, tot[k5]), UP, buff=0.1)
        with self.voiceover(
            "December 10th, 2025, a few seconds before two o'clock in the afternoon. <bookmark mark='dc'/> In a data "
            "center in Carteret, New Jersey, Nasdaq's computers are processing a stream of messages from traders: "
            "orders to buy, orders to sell, changes, cancellations. At exactly two o'clock, the Federal Reserve will "
            "announce its decision on interest rates, <bookmark mark='q'/> and the machines know it. In the last "
            "second, they start pulling their orders out of the book. <bookmark mark='p'/> Half a second before two: "
            "sixteen thousand cancellations in a tenth of a second, across more than fourteen hundred stocks. Nobody "
            "wants to be standing in the book when the news lands."
        ) as vo:
            self.play(FadeIn(when), FadeIn(clock))
            vo.wait_until("dc")
            self.play(Create(ch), FadeIn(ytl), FadeIn(src), FadeIn(key))
            advance(-1.0, max(vo.until("q") - 0.2, 1.0))
            vo.wait_until("q")
            advance(-0.4, 2.0)
            vo.wait_until("p")
            self.play(FadeIn(pull, shift=DOWN * 0.1), Indicate(bars[k5], color=WHITE))
            advance(-0.02, max(vo.remaining() - 0.4, 1.0))
        with self.voiceover(
            "<bookmark mark='go'/> Two o'clock. A quarter-point cut. <bookmark mark='x'/> Within a second the machines "
            f"are back, quoting and trading furiously: {round(after3 / 1000):,} thousand messages in the next three "
            "seconds. Nearly every one was generated by a computer, most of them within microseconds of the computer "
            "seeing something change."
        ) as vo:
            vo.wait_until("go")
            advance(0.5, 1.6)
            vo.wait_until("x")
            advance(3.0, max(vo.remaining() - 0.5, 2.0))
        clock.clear_updaters()
        self.clear_scene()

    # ------------------------------------------------------------------
    def the_day(self):
        d = load("day")
        ps = np.array(d["per_s"], float)
        t0 = d["per_s_t0"]
        a, b = 9 * 3600, 16 * 3600 + 30 * 60
        seg = ps[a - t0:b - t0]
        env = seg.reshape(-1, 10).max(1)  # the busiest second in each 10 s
        xs = (np.arange(len(env)) * 10 + a) / 3600
        open_n = int(ps[9 * 3600 + 30 * 60 - t0])
        peak_at = d["rth_s_max_at"]
        peak_n = d["rth_s_max"]
        close_n = int(ps[16 * 3600 + 2 - t0])
        assert peak_at == 14 * 3600 + 40 * 60 + 7 and 900_000 < peak_n < 950_000
        assert 700_000 < open_n < 740_000 and close_n > 1_700_000
        ch = Plot((9, 16.5), (5e3, 2e6), width=11.8, height=4.6, log_y=True, x_ticks=list(range(9, 17)),
                  x_fmt=lambda v: label(f"{int(v) if v <= 12 else int(v) - 12}{'am' if v < 12 else 'pm'}".replace("12pm", "noon"),
                                        font_size=22, color=GREY_A),
                  y_ticks=[1e4, 1e5, 1e6], y_fmt=lambda v: {1e4: "10{,}000", 1e5: "100{,}000", 1e6: "1{,}000{,}000"}[v]
                  ).shift(DOWN * 0.45 + RIGHT * 0.4)
        env_c = np.clip(env, 5e3, 2e6)
        area = ch.area(np.r_[xs, xs[-1]], np.r_[env_c, 5e3], C.MSG, opacity=0.8)
        ttl = label(r"Nasdaq messages per second, the whole trading day", font_size=34).to_edge(UP, buff=0.4)
        sub = note(r"busiest second in every 10-second window", font_size=22).next_to(ttl, DOWN, buff=0.12)
        notes = VGroup(
            tagged(rf"9:30 open\\{fmt_int(open_n)} in one second", font_size=22).next_to(ch.c2p(9.5, open_n), RIGHT, buff=0.15),
            tagged(r"2:00 the Fed", font_size=22, color=C.LATENCY).next_to(ch.c2p(14.0, 3.0e5), UP, buff=0.1).shift(LEFT * 0.5),
            tagged(rf"2:40:07, the press conference\\{fmt_int(peak_n)} in one second", font_size=22).next_to(
                ch.c2p(14 + 40 / 60, peak_n), UP, buff=0.12).shift(LEFT * 0.6),
            tagged(r"4:00 close", font_size=22).next_to(ch.c2p(16.0, 1.75e6), LEFT, buff=0.12),
        )
        total = VGroup(
            label(rf"{d['messages'] / 1e6:.1f} million messages", font_size=30, color=C.MSG),
            label(rf"{d['bytes'] / 1e9:.1f} gigabytes", font_size=30, color=C.MSG),
            label(r"one exchange, one day", font_size=24, color=GREY_A),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.1).move_to(ch.c2p(11.6, 1.0e6))
        total.next_to(notes[0], RIGHT, buff=0.3).set_y(ch.c2p(0, 1.1e6)[1])
        assert total.get_right()[0] < min(notes[1].get_left()[0], notes[2].get_left()[0]) - 0.1
        assert abs(d["messages"] / 1e6 - 846.8) < 0.05 and abs(d["bytes"] / 1e9 - 27.0) < 0.05
        with self.voiceover(
            "Zoom out to the whole day. <bookmark mark='o'/> The opening bell at 9:30: more than seven hundred "
            "thousand messages in a single second. <bookmark mark='f'/> The Fed at two. <bookmark mark='p'/> And the "
            "busiest second of the regular session came forty minutes later, during the Fed chair's press conference: "
            "933 thousand messages in one second. <bookmark mark='c'/> The close at four is busier still. <bookmark "
            "mark='t'/> In total, Nasdaq's feed carried 846.8 million messages that day, 27 gigabytes, from one "
            "exchange among more than a dozen in the United States."
        ) as vo:
            self.play(FadeIn(ttl), FadeIn(sub), Create(ch))
            self.play(FadeIn(area), run_time=1.0)
            for i, m in enumerate("ofpc"):
                vo.wait_until(m)
                self.play(FadeIn(notes[i], shift=DOWN * 0.1), run_time=0.6)
            vo.wait_until("t")
            self.play(FadeIn(total, shift=UP * 0.15))
        self.clear_scene()

    # ------------------------------------------------------------------
    def the_firms(self):
        js = VGroup(label(r"Jane Street", font_size=48),
                    label(rf"trades on more than {FACTS['js_venues']} venues in {FACTS['js_countries']} countries", font_size=26,
                          color=GREY_A),
                    label(rf"reported 2025 trading revenue: \${FACTS['js_rev_2025'] / 1e9:.1f} billion", font_size=26,
                          color=GREY_A)).arrange(DOWN, buff=0.15)
        hrt = VGroup(label(r"Hudson River Trading", font_size=48),
                     label(r"trades on ``nearly all the world's electronic markets''", font_size=26, color=GREY_A),
                     label(r"one of the largest U.S. stock traders", font_size=26, color=GREY_A)).arrange(DOWN, buff=0.15)
        VGroup(js, hrt).arrange(RIGHT, buff=1.2).move_to(UP * 1.2)
        others = label(r"also: Citadel Securities, Jump Trading, Optiver, Virtu, IMC, XTX, Tower, \dots", font_size=26,
                       color=GREY_B).next_to(VGroup(js, hrt), DOWN, buff=0.6)
        public = VGroup(*[label(s, font_size=28) for s in [
            r"\textbullet\ engineers' talks, papers and blog posts",
            r"\textbullet\ exchange specifications and regulatory filings",
            r"\textbullet\ one real day of Nasdaq data, every message",
            r"\textbullet\ experiments on a 4-core Intel Xeon virtual machine",
        ]]).arrange(DOWN, aligned_edge=LEFT, buff=0.16).to_edge(DOWN, buff=0.55)
        src = source(r"janestreet.com; hudsonrivertrading.com; Reuters (Jan 2026)", font_size=18)
        with self.voiceover(
            "The firms that thrive in this torrent are among the most profitable businesses in the world. <bookmark "
            "mark='j'/> Jane Street trades on more than two hundred venues in forty-five countries, and reportedly "
            "made 39.6 billion dollars of trading revenue in 2025. <bookmark mark='h'/> Hudson River Trading says it "
            "trades on nearly all the world's electronic markets. <bookmark mark='o'/> And there are others. <bookmark "
            "mark='p'/> None of them publishes a blueprint. But between their engineers' public talks and blog posts, "
            "exchange specifications, regulatory filings, a full day of real exchange data, and some experiments on "
            "this very computer, we can rebuild the machine they all converge on, piece by piece, and measure every "
            "piece."
        ) as vo:
            vo.wait_until("j")
            self.play(FadeIn(js, shift=UP * 0.2), FadeIn(src))
            vo.wait_until("h")
            self.play(FadeIn(hrt, shift=UP * 0.2))
            vo.wait_until("o")
            self.play(FadeIn(others))
            vo.wait_until("p")
            self.play(LaggedStart(*[FadeIn(p, shift=RIGHT * 0.2) for p in public], lag_ratio=0.5), run_time=3)
        self.clear_scene()

    # ------------------------------------------------------------------
    def the_loop(self):
        loop = loop_diagram().shift(UP * 0.6)
        ttl = label(r"one trip around the loop: \emph{tick to trade}", font_size=36, color=C.LATENCY).to_edge(UP, buff=0.5)
        parts = VGroup(*[label(s, font_size=27) for s in [
            r"Part 1\quad the game: what a market maker does, and what an exchange is",
            r"Part 2\quad seeing the market: the feed and the order book",
            r"Part 3\quad the race: light, silicon, software, hardware",
            r"Part 4\quad the brain: fair value, quoting, and testing on real queues",
            r"Part 5\quad staying alive: risk, determinism, the research loop",
        ]]).arrange(DOWN, aligned_edge=LEFT, buff=0.14).to_edge(DOWN, buff=0.45)
        pkt = Dot(radius=0.09, color=C.MSG).move_to(loop.nodes["exchange"].get_right())
        with self.voiceover(
            "Here is that machine, as a loop. <bookmark mark='ex'/> The exchange broadcasts every change to its order "
            "book. <bookmark mark='fd'/> A feed handler decodes the messages, <bookmark mark='bk'/> and rebuilds the "
            "book. <bookmark mark='fv'/> The strategy estimates what the stock is really worth, <bookmark mark='qt'/> "
            "decides where to buy and sell, <bookmark mark='rk'/> passes every order through risk checks, <bookmark "
            "mark='gw'/> and sends it back to the exchange. <bookmark mark='tt'/> The time for one trip around this "
            "loop is called tick-to-trade, and at the top firms, it's measured in nanoseconds. <bookmark mark='pp'/> "
            "We'll build it in five parts."
        ) as vo:
            vo.wait_until("ex")
            self.play(FadeIn(loop.nodes["exchange"], scale=1.1))
            for k, m in zip(["feed", "book", "signal", "quote", "risk", "gateway"], ["fd", "bk", "fv", "qt", "rk", "gw"]):
                vo.wait_until(m)
                i = loop.keys.index(k)
                self.play(GrowArrow(loop.arrows[i - 1]), FadeIn(loop.nodes[k], shift=RIGHT * 0.15), run_time=0.6)
            self.play(Create(loop.ret), run_time=0.8)
            vo.wait_until("tt")
            self.play(FadeIn(ttl))
            self.add(pkt)
            path = VMobject().set_points_as_corners(
                [loop.nodes[k].get_center() for k in loop.keys] + [loop.ret[0].get_points()[k] for k in (0, -1)] if False else
                [loop.nodes[k].get_center() for k in loop.keys])
            back = loop.ret[0].copy()
            self.play(MoveAlongPath(pkt, path), run_time=2.2, rate_func=linear)
            pkt.set_color(C.ORDER)
            self.play(MoveAlongPath(pkt, back), run_time=1.2, rate_func=linear)
            self.play(FadeOut(pkt))
            vo.wait_until("pp")
            self.play(LaggedStart(*[FadeIn(p, shift=UP * 0.1) for p in parts], lag_ratio=0.25), run_time=2.5)
        self.wait(1.5)
        self.clear_scene()
        card = VGroup(label(r"Building a Top-Tier", font_size=60), label(r"Real-Time Trading System", font_size=60),
                      label(r"from photons to fills, measured", font_size=32, color=GREY_A)).arrange(DOWN, buff=0.25)
        self.play(FadeIn(card, scale=1.05), run_time=1.2)
        self.wait(2.5)
        self.play(FadeOut(card))

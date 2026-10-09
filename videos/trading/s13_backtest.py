from __future__ import annotations

import numpy as np

from explainer import *  # noqa: F403
from videos.trading.common import Plot, fmt_int, fmt_ns, label, load, mtex, node, note, real_tag, tagged


class Backtest(VoiceoverScene):
    def construct(self):
        self.virtual_order()
        self.results()
        self.latency()

    # ------------------------------------------------------------------
    def virtual_order(self):
        b = load("book")
        rp = b["replay"]
        start = dict((p, q) for p, q in rp["start_bids"])[18385]
        assert start == [1, 10, 200, 1, 30, 100]
        t0 = rp["t0"]
        msgs = [m for m in rp["msgs"] if m["side"] == "B" and m["price"] == 18385]
        # build the queue: real orders + ours (gold) at the back
        y = 0.3
        unit = lambda s: float(np.clip(0.15 * np.sqrt(s), 0.16, 2.2))
        queue = [("real", s) for s in start] + [("ours", 100)]
        blocks = []

        def make(kind, s, behind=False):
            col = C.OURS if kind == "ours" else (GREY_B if behind else C.BID)
            return Rectangle(width=unit(s), height=0.85, stroke_color=col, stroke_width=1.5, fill_color=col,
                             fill_opacity=0.75 if kind == "ours" else 0.5)

        price = MathTex("183.85", font_size=44, color=C.BID).move_to([3.9, y, 0])
        front_x = 2.8

        def layout(bl):
            x = front_x
            for blk in bl:
                blk.move_to([x - blk.width / 2, y, 0])
                x -= blk.width + 0.06

        for kind, s in queue:
            blocks.append([kind, s, make(kind, s)])
        layout([b_[2] for b_ in blocks])
        front = label(r"front of the queue", font_size=24, color=GREY_A).next_to([front_x, y + 0.5, 0], UP, buff=0.05).shift(LEFT * 0.6)
        ttl = label(r"a backtest's hardest question: if our order had been there, when would it have filled?", font_size=28)
        ttl.to_edge(UP, buff=0.3)
        clock = Text("10:30:00.000 000", font="DejaVu Sans Mono", font_size=30, color=C.LATENCY).to_edge(UP, buff=1.0)
        ahead_t = always_redraw(lambda: label(
            rf"ahead of us: {sum(1 for k, s, _ in blocks[:[k for k, _, _ in blocks].index('ours')] if k == 'real')} orders, "
            rf"{sum(s for k, s, _ in blocks[:[k for k, _, _ in blocks].index('ours')] if k == 'real')} shares"
            if any(k == 'ours' for k, _, _ in blocks) else r"filled", font_size=30, color=C.OURS).move_to(DOWN * 1.1))
        log = VGroup().to_edge(DOWN, buff=0.4)
        with self.voiceover(
            "Now the hardest question in this whole business: does a strategy actually make money? You test it on "
            "history, but your orders weren't in the history. <bookmark mark='q'/> So take the real Nvidia bid queue "
            "at 10:30 that morning, six real orders, <bookmark mark='o'/> and put a virtual order of our own at the "
            "back. Because the feed reports every order individually, we can track exactly which orders are ahead of "
            "us, and replay what really happened to them."
        ) as vo:
            self.play(FadeIn(ttl), FadeIn(real_tag()))
            vo.wait_until("q")
            self.play(FadeIn(price), FadeIn(front), *[FadeIn(b_[2]) for b_ in blocks if b_[0] == "real"], FadeIn(clock))
            vo.wait_until("o")
            self.play(FadeIn(blocks[-1][2], shift=LEFT * 0.3))
            self.add(ahead_t)

        def stamp(ts):
            us = (ts - t0) / 1000 + (t0 - 37800 * 10**9) / 1000
            ms_, rem = divmod(us, 1000)
            return Text(f"10:30:00.{int(ms_):03d} {int(rem):03d}", font="DejaVu Sans Mono", font_size=30,
                        color=C.LATENCY).move_to(clock)

        filled_at = None
        with self.voiceover(
            "<bookmark mark='r'/> The replay: an order ahead of us is canceled, and we move up. Others join behind us "
            "and leave again. Another cancel ahead. <bookmark mark='e'/> Then, thirty-seven milliseconds in, a seller "
            "arrives and executes all four orders in front of us at once. We're at the front. <bookmark mark='f'/> A "
            "quarter of a millisecond later, a new order joins behind us and is executed immediately. In the real "
            "world that trade would have hit us first: we're filled, buying 100 shares at 183.85. <bookmark mark='w'/> "
            "And at that instant, the bid at 183.85 is gone. The price has just moved down through us. We bought "
            "exactly when the market was falling."
        ) as vo:
            vo.wait_until("r")
            pending_exec = []
            for m in msgs:
                ours_i = [k for k, _, _ in blocks].index("ours") if any(k == "ours" for k, _, _ in blocks) else None
                new_clock = stamp(m["ts"])
                if m["type"] == "D":
                    # pos counts real orders only
                    real_idx = [i for i, (k, _, _) in enumerate(blocks) if k != "ours"]
                    i = real_idx[m["pos"]] if m["pos"] < len(real_idx) else None
                    if i is None:
                        continue
                    blk = blocks.pop(i)
                    anims = [FadeOut(blk[2], shift=UP * 0.4), UpdateFromFunc(clock, lambda m, n=new_clock: m.become(n))]
                    tgt = [b_[2].copy() for b_ in blocks]
                    layout(tgt)
                    anims += [b_[2].animate.move_to(t.get_center()) for b_, t in zip(blocks, tgt)]
                    self.play(*anims, run_time=0.5)
                elif m["type"] == "A":
                    blk = ["real", m["shares"], make("real", m["shares"], behind=True)]
                    blocks.append(blk)
                    layout([b_[2] for b_ in blocks])
                    self.play(FadeIn(blk[2], shift=LEFT * 0.3), UpdateFromFunc(clock, lambda m, n=new_clock: m.become(n)), run_time=0.4)
                elif m["type"] == "E":
                    pending_exec.append(m)
                    if len(pending_exec) < 4 and m["ref"] != msgs[-1]["ref"]:
                        continue
                    if m["ref"] == msgs[-1]["ref"]:
                        vo.wait_until("f")
                        ours = blocks[[k for k, _, _ in blocks].index("ours")]
                        self.play(UpdateFromFunc(clock, lambda m, n=new_clock: m.become(n)), Flash(ours[2], color=C.TRADE),
                                  ours[2].animate.set_fill(C.TRADE, 0.95), run_time=0.6)
                        filled_at = m["ts"]
                        break
                    vo.wait_until("e")
                    front_blocks = [b_ for b_ in blocks if b_[0] == "real"][:4]
                    self.play(UpdateFromFunc(clock, lambda m, n=new_clock: m.become(n)),
                              *[b_[2].animate.set_fill(C.TRADE, 0.9).set_stroke(C.TRADE) for b_ in front_blocks], run_time=0.4)
                    for b_ in front_blocks:
                        blocks.remove(b_)
                    tgt = [b_[2].copy() for b_ in blocks]
                    layout(tgt)
                    self.play(*[FadeOut(b_[2], scale=0.5) for b_ in front_blocks],
                              *[b_[2].animate.move_to(t.get_center()) for b_, t in zip(blocks, tgt)], run_time=0.5)
                    pending_exec = []
            assert filled_at is not None and abs((filled_at - t0) / 1e6 - 34.3) < 1.0
            vo.wait_until("w")
            gone = tagged(r"bid 183.85 emptied: the mid falls", font_size=26, color=C.PNL_DOWN).next_to(price, DOWN, buff=0.6)
            gone.shift(LEFT * 1.5)
            self.play(FadeIn(gone), price.animate.set_opacity(0.3))
        ahead_t.clear_updaters()
        self.clear_scene()

    # ------------------------------------------------------------------
    def results(self):
        mm = load("mm")
        run = mm["runs"]["join_10000"]
        hz = mm["horizons_ms"]
        mk = run["markout_cents"]
        assert run["fills"] > 80_000 and mk[0] > 0.1 and mk[1] < -0.2 and -0.26 < run["pnl_cents_per_share"] < -0.22
        xs = np.arange(len(hz))
        ch = Plot((-0.3, len(hz) - 0.7), (-0.6, 0.3), width=10.0, height=4.2, x_ticks=list(xs),
                  x_fmt=lambda i: label(["at the fill", "1 ms", "10 ms", "100 ms", "1 s", "10 s", "1 min"][int(i)],
                                        font_size=22, color=GREY_A),
                  y_ticks=[-0.6, -0.4, -0.2, 0, 0.2], y_fmt=lambda v: rf"{v:+.1f}" if v else "0").shift(DOWN * 0.5)
        zero = ch.hline(0, color=GREY_B)
        line = ch.line(xs, mk, C.OURS, 5)
        dots = VGroup(*[ch.dot(x, v, C.OURS) for x, v in zip(xs, mk)])
        slow = mm["runs"]["join_10000000"]["markout_cents"]
        line_slow = ch.line(xs, slow, C.PNL_DOWN, 4)
        ttl = label(r"a simple market maker on Nvidia, replayed against the real queues, 9:45 to 3:45", font_size=28)
        ttl.to_edge(UP, buff=0.25)
        rules = note(r"join the best bid and ask with 100 shares; re-join when they move; at most 500 shares long or short;"
                     r" every action reaches the exchange 10 $\mu$s after the decision", font_size=20, color=GREY_A)
        rules.next_to(ttl, DOWN, buff=0.1)
        yl = ch.y_title(r"profit per share bought or sold, measured against the mid, cents", font_size=22)
        big_rules = VGroup(*[label(t, font_size=30) for t in [
            r"\textbullet\ always join the best bid and the best ask, 100 shares each",
            r"\textbullet\ when they move, cancel and re-join",
            r"\textbullet\ never more than 500 shares long or short",
            r"\textbullet\ every action reaches the exchange 10 $\mu$s after the decision",
            r"\textbullet\ our orders are virtual: queued behind the real ones",
        ]]).arrange(DOWN, aligned_edge=LEFT, buff=0.25).move_to(DOWN * 0.3)
        a1 = tagged(rf"+{mk[0]:.2f}\textcent: we seem to earn the spread", font_size=22, color=C.PNL_UP).next_to(
            ch.c2p(0, mk[0]), UR, buff=0.1)
        a2 = tagged(rf"{mk[1]:.2f}\textcent\ a millisecond later", font_size=22, color=C.PNL_DOWN).next_to(
            ch.c2p(1, mk[1]), DOWN, buff=0.2)
        res = label(rf"{fmt_int(run['fills'])} fills; result: {run['pnl_cents_per_share']:+.2f} cents per share",
                    font_size=26, color=C.PNL_DOWN).to_edge(DOWN, buff=0.25).shift(LEFT * 1.5)
        with self.voiceover(
            "Now run that idea all day long. <bookmark mark='s'/> A simple market maker on Nvidia: always join the best "
            "bid and the best ask with a hundred shares, re-join whenever they move, never hold more than five hundred "
            "shares either way, and assume every action takes ten microseconds to reach the exchange. Every one of its "
            "orders is a virtual order, queued behind the real ones. <bookmark mark='m'/> For each fill, measure the "
            "profit against the mid-price, at the moment of the fill and at later moments. This is called a markout. "
            "<bookmark mark='a'/> At the instant of the fill, we've earned a sliver of the spread. <bookmark "
            "mark='b'/> One millisecond later, the price has moved against us by more than that, and it stays there. "
            f"<bookmark mark='r'/> Over {run['fills']:,} fills, the strategy loses about a quarter of a cent per share. "
            "That's adverse selection, measured: you get filled precisely when you least want to be."
        ) as vo:
            self.play(FadeIn(ttl), FadeIn(real_tag()))
            vo.wait_until("s")
            self.play(LaggedStart(*[FadeIn(r, shift=RIGHT * 0.15) for r in big_rules], lag_ratio=0.6), run_time=5)
            vo.wait_until("m")
            self.play(FadeOut(big_rules), FadeIn(rules))
            self.play(Create(ch), FadeIn(yl), Create(zero))
            vo.wait_until("a")
            self.play(FadeIn(dots[0]), FadeIn(a1))
            vo.wait_until("b")
            self.play(Create(line), FadeIn(dots[1:]), FadeIn(a2), run_time=2)
            vo.wait_until("r")
            self.play(FadeIn(res))
        self.clear_scene()

    # ------------------------------------------------------------------
    def latency(self):
        mm = load("mm")
        lat = mm["latencies_ns"]
        join = [mm["runs"][f"join_{l}"]["pnl_cents_per_share"] for l in lat]
        sig = [mm["runs"][f"signal_{l}"]["pnl_cents_per_share"] for l in lat]
        ahead = [mm["runs"][f"join_{l}"]["median_ahead_shares"] for l in lat]
        assert join[-1] < join[0] - 0.2 and all(s > j for s, j in zip(sig[:3], join[:3]))
        xs = np.arange(len(lat))
        ch = Plot((-0.6, len(lat) - 0.4), (-0.6, 0), width=9.6, height=4.3, x_ticks=list(xs),
                  x_fmt=lambda i: fmt_ns(lat[int(i)]), y_ticks=[-0.6, -0.4, -0.2, 0],
                  y_fmt=lambda v: rf"{v:+.1f}" if v else "0", grid=True).shift(DOWN * 0.45 + LEFT * 1.1)
        bars_j, bars_s = VGroup(), VGroup()
        for x, j, s in zip(xs, join, sig):
            bars_j.add(ch.bar(x - 0.18, j, 0.32, C.OURS, base=0))
            bars_s.add(ch.bar(x + 0.18, s, 0.32, C.SIGNAL, base=0))
        xl = label(r"time for each action to reach the exchange", font_size=24, color=GREY_A).next_to(ch.x_labels, DOWN, buff=0.12)
        yl = ch.y_title(r"profit per share, cents", font_size=22)
        key = VGroup(label(r"join the best bid and ask", font_size=22, color=C.OURS),
                     label(r"same, but step aside when imbalance says the price is about to move through us",
                           font_size=22, color=C.SIGNAL)).arrange(DOWN, aligned_edge=LEFT, buff=0.08)
        key.to_edge(UP, buff=0.3)
        band = Rectangle(width=ch.w, height=abs(ch.y_to(-0.27) - ch.y_to(-0.20)), stroke_width=0, fill_color=C.PNL_UP,
                         fill_opacity=0.2).move_to([ch.x_to((-0.6 + len(lat) - 0.4) / 2), (ch.y_to(-0.27) + ch.y_to(-0.20)) / 2, 0])
        band_l = label(r"Nasdaq's rebates\\for posting orders\\(2025 tiers):\\0.20--0.27\textcent\ a share", font_size=22,
                       color=C.PNL_UP).next_to(band, RIGHT, buff=0.2)
        q = label(rf"slower also means further back in the queue: median {ahead[0]:.0f} shares ahead at 1 $\mu$s, "
                  rf"{ahead[3]:.0f} at 1 ms", font_size=22, color=GREY_A).to_edge(DOWN, buff=0.15).to_edge(LEFT, buff=0.4)
        with self.voiceover(
            "Now change one thing: how long our actions take to reach the exchange. <bookmark mark='j'/> From one "
            "microsecond up to a hundred, the loss barely changes. At one millisecond it's almost half again as bad, and at "
            "ten milliseconds, twice as bad: our quotes sit there stale, waiting for our own cancels to arrive, while "
            "faster traders pick them off. <bookmark mark='s'/> Add the imbalance signal, stepping aside whenever the "
            "queue on our side gets thin, and the loss shrinks, but doesn't go away. <bookmark mark='r'/> Real market "
            "makers have help we didn't model. Exchanges pay a rebate for posting orders that others trade against: "
            "on Nasdaq, around a fifth to a quarter of a cent a share for the busiest firms, which is just about the "
            "size of the loss of our fastest version. <bookmark mark='q'/> And the real edge is in everything else we "
            "left out: being first in line when a new price level opens, and signals from futures, other exchanges and "
            "related stocks that see the move coming. This is why a firm's simulator, which has to replay every queue "
            "honestly, is one of its most valuable systems."
        ) as vo:
            self.play(Create(ch), FadeIn(xl), FadeIn(yl), FadeIn(real_tag(corner=DR)))
            vo.wait_until("j")
            self.play(FadeIn(key[0]), LaggedStart(*[GrowFromEdge(b_, UP) for b_ in bars_j], lag_ratio=0.2), run_time=2)
            vo.wait_until("s")
            self.play(FadeIn(key[1]), LaggedStart(*[GrowFromEdge(b_, UP) for b_ in bars_s], lag_ratio=0.2), run_time=2)
            vo.wait_until("r")
            self.play(FadeIn(band), FadeIn(band_l))
            vo.wait_until("q")
            self.play(FadeIn(q))
        self.clear_scene()

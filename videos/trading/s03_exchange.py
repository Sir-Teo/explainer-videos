from __future__ import annotations

import numpy as np

from explainer import *  # noqa: F403
from videos.trading.common import (
    FACTS, fmt_int, label, load, mtex, node, note, real_tag, schematic_tag, server_box, source, tagged,
)


class TheExchange(VoiceoverScene):
    def construct(self):
        self.one_line()
        self.matching()
        self.multicast()
        self.mix()
        self.replication()

    # ------------------------------------------------------------------
    def one_line(self):
        clients = VGroup(*[server_box(color=GREY_B, width=0.9, height=0.55) for _ in range(6)]).arrange(DOWN, buff=0.22)
        clients.move_to(LEFT * 5.9)
        cl = label(r"trading firms", font_size=24, color=GREY_A).next_to(clients, UP, buff=0.2)
        gws = VGroup(*[node(r"port", color=C.ORDER, width=1.1, height=0.6, font_size=22) for _ in range(3)])
        gws.arrange(DOWN, buff=0.8).move_to(LEFT * 3.6)
        gl = label(r"gateways", font_size=24, color=C.ORDER).next_to(gws, UP, buff=0.2)
        seq = node(r"sequencer", color=C.LATENCY, width=2.0, height=1.0, font_size=26).move_to(LEFT * 0.9)
        eng = node(r"matching\\engine", color=C.TRADE, width=2.1, height=1.4, font_size=26).move_to(RIGHT * 2.2)
        core = label(r"one thread, one core", font_size=22, color=C.TRADE).next_to(eng, DOWN, buff=0.15)
        links = VGroup()
        for i, c in enumerate(clients):
            links.add(Line(c.get_right(), gws[i // 2].get_left(), stroke_width=1.5, color=GREY_D))
        for g in gws:
            links.add(Line(g.get_right(), seq.get_left(), stroke_width=1.5, color=GREY_D))
        links.add(Arrow(seq.get_right(), eng.get_left(), buff=0.05, color=C.LATENCY, stroke_width=3))
        counter = Integer(0, font_size=30, color=C.LATENCY).next_to(seq, UP, buff=0.15)
        clab = label(r"\#", font_size=30, color=C.LATENCY).next_to(counter, LEFT, buff=0.08)
        tag = schematic_tag()
        with self.voiceover(
            "Now the other side of every trade: the exchange. An exchange is at heart a machine for one job: deciding "
            "the order in which things happened. <bookmark mark='c'/> Thousands of connections from trading firms "
            "arrive through gateway machines, <bookmark mark='s'/> and every message from all of them is funneled into "
            "a single line, where a sequencer stamps it with the next number. <bookmark mark='e'/> Then a matching "
            "engine processes the messages one at a time, in exactly that order, on a single thread. One line, one "
            "thread: no locks, no ambiguity about who came first."
        ) as vo:
            self.play(FadeIn(tag))
            vo.wait_until("c")
            self.play(LaggedStart(*[FadeIn(c, shift=RIGHT * 0.2) for c in clients], lag_ratio=0.1), FadeIn(cl),
                      FadeIn(gws), FadeIn(gl), Create(links[:9]), run_time=1.5)
            vo.wait_until("s")
            self.play(FadeIn(seq), FadeIn(counter), FadeIn(clab), Create(links[9]))
            vo.wait_until("e")
            self.play(FadeIn(eng), FadeIn(core))
            # orders flow: each passes the sequencer and gets a number
            rng = np.random.default_rng(3)
            for k in range(8):
                ci = int(rng.integers(0, 6))
                d = Dot(clients[ci].get_right(), radius=0.08, color=C.ORDER)
                path = VMobject().set_points_as_corners([clients[ci].get_right(), gws[ci // 2].get_center(),
                                                         seq.get_center(), eng.get_center()])
                self.add(d)
                self.play(MoveAlongPath(d, path, rate_func=linear), counter.animate.set_value(k + 1), run_time=0.45)
                self.remove(d)
        self.stage = VGroup(clients, cl, gws, gl, seq, eng, core, links, counter, clab, tag)
        self.clear_scene()

    # ------------------------------------------------------------------
    def matching(self):
        w = load("windows")["burst"]
        assert w["symbol"] == "NFLX" and w["same_ns"] == 4108 and w["types"]["E"] == 4076
        # price-time priority, schematically: a queue at the best ask, an incoming buy
        row_y = [1.4, 0.7, 0.0]
        prices = ["100.02", "100.01", "100.00"]
        queues = VGroup()
        sizes = [[3, 5, 2, 4], [2, 6, 3, 2, 2], [4, 2, 5, 1, 3]]
        for y, p, sz in zip(row_y, prices, sizes):
            row = VGroup(MathTex(p, font_size=30, color=C.ASK).move_to([-1.0, y, 0]))
            x = -0.3
            blocks = VGroup()
            for s in sz:
                b = Rectangle(width=0.18 * s, height=0.42, stroke_color=C.ASK, stroke_width=1.2, fill_color=C.ASK,
                              fill_opacity=0.5)
                b.move_to([x + b.width / 2, y, 0])
                x += b.width + 0.05
                blocks.add(b)
            row.add(blocks)
            row.blocks = blocks
            queues.add(row)
        incoming = VGroup(Rectangle(width=2.8, height=0.42, stroke_color=C.BID, fill_color=C.BID, fill_opacity=0.6),
                          label(r"buy 25 at up to 100.01", font_size=22)).move_to(LEFT * 4.6 + DOWN * 0.0)
        incoming[1].move_to(incoming[0])
        rule = VGroup(label(r"price-time priority", font_size=34, color=C.TRADE),
                      label(r"best price first; at the same price, first come, first served", font_size=26, color=GREY_A)
                      ).arrange(DOWN, buff=0.1).to_edge(UP, buff=0.45)
        with self.voiceover(
            "The matching rule is called price-time priority. <bookmark mark='i'/> An incoming order to buy trades first "
            "against the cheapest offers, <bookmark mark='q'/> and among offers at the same price, against whichever "
            "arrived first. <bookmark mark='r'/> Whatever can't be filled rests in the book, at the back of its "
            "queue."
        ) as vo:
            self.play(FadeIn(rule), LaggedStart(*[FadeIn(q) for q in queues], lag_ratio=0.2))
            vo.wait_until("i")
            self.play(FadeIn(incoming, shift=RIGHT * 0.3))
            vo.wait_until("q")
            # eat 100.00 fully (15), then 100.01 from the front (10 of 15)
            for b in queues[2].blocks:
                self.play(b.animate.set_fill(C.TRADE, 0.9).set_stroke(C.TRADE), run_time=0.15)
                self.play(FadeOut(b, scale=0.5), run_time=0.15)
            eaten = 0
            for b in list(queues[1].blocks):
                s = round(b.width / 0.18)
                if eaten + s > 10:
                    break
                eaten += s
                self.play(b.animate.set_fill(C.TRADE, 0.9).set_stroke(C.TRADE), run_time=0.15)
                self.play(FadeOut(b, scale=0.5), run_time=0.15)
            vo.wait_until("r")
            rest = Rectangle(width=0.18 * (25 - 15 - eaten), height=0.42, stroke_color=C.BID, fill_color=C.BID,
                             fill_opacity=0.6)
            rest.move_to([-0.3 + rest.width / 2, -0.7, 0])
            rl = MathTex("100.01", font_size=30, color=C.BID).move_to([-1.0, -0.7, 0])
            self.play(ReplacementTransform(incoming, rest), FadeIn(rl))
        self.clear_scene()

        burst = VGroup(
            label(r"Netflix, 10:38:37.273156756 a.m.", font_size=36),
            label(rf"one incoming order traded against {fmt_int(w['types']['E'])} resting orders", font_size=30, color=C.TRADE),
            label(rf"{fmt_int(w['same_ns'])} messages, all stamped with the same nanosecond", font_size=30, color=C.MSG),
            label(r"to the matching engine, it was a single event", font_size=28, color=GREY_A),
        ).arrange(DOWN, buff=0.3)
        grid = VGroup(*[Square(0.075, stroke_width=0, fill_color=C.TRADE, fill_opacity=0.9) for _ in range(w["types"]["E"])])
        grid.arrange_in_grid(34, 120, buff=0.02).to_edge(DOWN, buff=0.35)
        burst.to_edge(UP, buff=0.5)
        with self.voiceover(
            "Because the engine handles one event at a time, a single order can produce a flood. <bookmark mark='n'/> "
            "At 10:38 that morning, one order in Netflix traded against 4,076 resting orders at once. The feed "
            "reported it as 4,108 messages, every one stamped with the same nanosecond. To the matching engine it was "
            "one event."
        ) as vo:
            vo.wait_until("n")
            self.play(FadeIn(burst[0]), FadeIn(real_tag()))
            self.play(FadeIn(burst[1]), LaggedStart(*[FadeIn(s) for s in grid], lag_ratio=0.0006), run_time=2.5)
            self.play(FadeIn(burst[2]))
            self.play(FadeIn(burst[3]))
        self.clear_scene()

    # ------------------------------------------------------------------
    def multicast(self):
        eng = node(r"matching\\engine", color=C.TRADE, width=2.0, height=1.2, font_size=24).move_to(LEFT * 5.3)
        n = 12
        recv = VGroup(*[server_box(color=GREY_B, width=0.7, height=0.42) for _ in range(n)]).arrange(DOWN, buff=0.1)
        recv.move_to(RIGHT * 5.5)
        # unicast: one copy per receiver, written one after another on the same wire
        left = VGroup(label(r"one copy per subscriber (TCP)", font_size=28, color=C.ORDER),
                      label(rf"600 subscribers $\times$ 1 $\mu$s each: the last waits {FACTS['nigito_unicast_600_us']} $\mu$s",
                            font_size=24, color=GREY_A)).arrange(DOWN, buff=0.08).to_edge(UP, buff=0.35)
        wire = Line(eng.get_right(), recv.get_left() + LEFT * 1.5, color=GREY_B, stroke_width=3)
        fan = VGroup(*[Line(wire.get_end(), r.get_left(), color=GREY_D, stroke_width=1.5) for r in recv])
        tag = schematic_tag()
        with self.voiceover(
            "Then the engine has to tell everyone what happened, and fairly: everyone should learn it at the same time. "
            "<bookmark mark='u'/> The obvious way is a separate connection to each subscriber, but then the messages "
            "leave one after another. At ten gigabits per second, a thousand-byte message takes about a microsecond "
            "to put on the wire, so the six-hundredth subscriber hears the news six hundred microseconds after the "
            "first. That's the example Jane Street's Brian Nigito gives."
        ) as vo:
            self.play(FadeIn(eng), FadeIn(recv), Create(wire), Create(fan), FadeIn(tag))
            vo.wait_until("u")
            self.play(FadeIn(left))
            dots = []
            for i in range(n):
                d = Dot(eng.get_right(), radius=0.07, color=C.MSG)
                path = VMobject().set_points_as_corners([eng.get_right(), wire.get_end(), recv[i].get_left()])
                dots.append((d, path))
            self.play(LaggedStart(*[MoveAlongPath(d, p, rate_func=linear) for d, p in dots], lag_ratio=0.35),
                      run_time=4.5)
            self.play(*[FadeOut(d) for d, _ in dots])
        right = VGroup(label(r"IP multicast: the switch makes the copies", font_size=28, color=C.MSG),
                       label(r"every subscriber, about 1 $\mu$s", font_size=24, color=GREY_A)).arrange(DOWN, buff=0.08)
        right.to_edge(UP, buff=0.35)
        sw = node(r"switch", color=C.MSG, width=1.2, height=0.6, font_size=22).move_to(wire.get_end())
        with self.voiceover(
            "<bookmark mark='m'/> So exchange data is sent with IP multicast: the engine sends each message once, and "
            "the network switches copy it in hardware to every subscriber at the same moment. It's unreliable, like "
            "all UDP, so every message carries a sequence number, and anyone who misses one asks a retransmission "
            "server to fill the gap."
        ) as vo:
            vo.wait_until("m")
            self.play(FadeOut(left), FadeIn(right), FadeIn(sw))
            d0 = Dot(eng.get_right(), radius=0.08, color=C.MSG)
            self.play(MoveAlongPath(d0, Line(eng.get_right(), sw.get_left())), run_time=0.8, rate_func=linear)
            copies = [Dot(sw.get_right(), radius=0.07, color=C.MSG) for _ in range(n)]
            self.remove(d0)
            self.play(*[MoveAlongPath(c, Line(sw.get_right(), r.get_left())) for c, r in zip(copies, recv)],
                      run_time=0.9, rate_func=linear)
            self.play(*[Flash(r, color=C.MSG, line_length=0.12, num_lines=8) for r in recv], *[FadeOut(c) for c in copies])
        self.clear_scene()

    # ------------------------------------------------------------------
    def mix(self):
        d = load("day")
        c = d["count_by_type_rth"]
        tot = d["messages_rth"]
        adds = c["A"] + c["F"]
        repl = c["U"]
        dels = c["D"] + c["X"]
        exe = c["E"] + c["C"]
        hidden = c["P"]
        other = tot - adds - repl - dels - exe - hidden
        share_exec = exe / tot
        assert 0.018 < share_exec < 0.022
        parts = [(adds, C.MSG, r"new orders"), (repl, C.SIGNAL, r"replaced (price or size changed)"),
                 (dels, C.CANCEL, r"canceled"), (exe, C.TRADE, r"executions against displayed orders"),
                 (hidden + other, GREY_D, r"other (hidden-order trades, auctions, admin)")]
        n = 1000
        counts = [int(round(p[0] / tot * n)) for p in parts]
        counts[0] += n - sum(counts)
        squares = VGroup()
        for (v, col, _), k in zip(parts, counts):
            for _ in range(k):
                squares.add(Square(0.2, stroke_width=0, fill_color=col, fill_opacity=0.9))
        squares.arrange_in_grid(20, 50, buff=0.04).move_to(LEFT * 1.9 + DOWN * 0.45)
        ttl = label(rf"what the {tot / 1e6:.0f} million messages of the regular session were", font_size=32)
        ttl.to_edge(UP, buff=0.35)
        sub = note(r"1{,}000 squares; each is 0.1\% of the messages", font_size=22).next_to(ttl, DOWN, buff=0.1)
        key = VGroup()
        for (v, col, txt) in parts:
            key.add(VGroup(Square(0.25, stroke_width=0, fill_color=col, fill_opacity=0.9),
                           label(txt, font_size=22, color=col if col != GREY_D else GREY_B),
                           MathTex(rf"{100 * v / tot:.1f}\%", font_size=26, color=WHITE)).arrange(RIGHT, buff=0.15))
        key.arrange(DOWN, aligned_edge=LEFT, buff=0.2).next_to(squares, RIGHT, buff=0.35)
        traded = d["added_rth_traded"] / d["added_rth"]
        never = label(rf"{100 * (1 - traded):.1f}\% of orders placed never trade at all", font_size=30, color=C.CANCEL)
        never.to_edge(DOWN, buff=0.35)
        assert 0.96 < 1 - traded < 0.98
        with self.voiceover(
            "So what is in that stream? Here are the 803 million messages of the regular session on Nasdaq that day, "
            "as a thousand squares. <bookmark mark='a'/> Over a third are new orders. <bookmark mark='u'/> More than a "
            "quarter are replacements: an order's price or size changed. <bookmark mark='d'/> A third are "
            "cancellations. <bookmark mark='e'/> And trades? Two percent, about what Nigito estimates for the U.S. "
            "market as a whole. <bookmark mark='n'/> Ninety-seven percent of all the orders placed that day never "
            "traded at all. Most of the activity of a modern market is quoting, and re-quoting, and getting out of "
            "the way."
        ) as vo:
            self.play(FadeIn(ttl), FadeIn(sub), FadeIn(real_tag()))
            starts = np.cumsum([0] + counts)
            for i, m in enumerate("aude"):
                vo.wait_until(m)
                self.play(LaggedStart(*[FadeIn(s) for s in squares[starts[i]:starts[i + 1]]], lag_ratio=0.002),
                          FadeIn(key[i]), run_time=1.2)
            self.play(FadeIn(squares[starts[4]:]), FadeIn(key[4]), run_time=0.6)
            vo.wait_until("n")
            self.play(FadeIn(never, shift=UP * 0.1))
        self.clear_scene()

    # ------------------------------------------------------------------
    def replication(self):
        log = VGroup(*[VGroup(Rectangle(width=0.62, height=0.5, stroke_color=C.LATENCY, stroke_width=1.5, fill_color=C.LATENCY,
                                        fill_opacity=0.15), Integer(i + 1, font_size=20)) for i in range(12)])
        for cell in log:
            cell[1].move_to(cell[0])
        log.arrange(RIGHT, buff=0.06).to_edge(UP, buff=1.0)
        ll = label(r"the sequenced log: every input, numbered", font_size=26, color=C.LATENCY).next_to(log, UP, buff=0.15)
        comps = VGroup(
            node(r"matching engine", color=C.TRADE, width=3.0, height=0.8, font_size=24),
            node(r"backup engine (passive)", color=C.TRADE, width=3.0, height=0.8, font_size=24),
            node(r"market data publisher", color=C.MSG, width=3.0, height=0.8, font_size=24),
            node(r"drop copies, clearing", color=GREY_B, width=3.0, height=0.8, font_size=24),
        ).arrange_in_grid(2, 2, buff=(0.8, 0.5)).shift(DOWN * 1.0)
        arrows = VGroup(*[Arrow(log.get_bottom(), c.get_top(), buff=0.15, color=C.LATENCY, stroke_width=2.5) for c in comps])
        eq = label(r"same inputs, same order $\Rightarrow$ same state, on every replica", font_size=30, color=WHITE)
        eq.to_edge(DOWN, buff=0.4)
        jx = note(rf"Jane Street's JX: components at $\sim${FACTS['nigito_component_rate'] / 1e3:.0f}k messages/s, "
                  rf"single-digit $\mu$s; any one rebuilt from the log in {FACTS['nigito_rebuild_s'][0]}--{FACTS['nigito_rebuild_s'][1]} s",
                  font_size=22, color=GREY_A).next_to(eq, UP, buff=0.2)
        with self.voiceover(
            "That single numbered line buys something else: reliability. <bookmark mark='l'/> If every component is a "
            "deterministic function of the sequenced log, <bookmark mark='c'/> then a backup matching engine reading "
            "the same log computes exactly the same state as the primary, message for message, and so does the "
            "market data publisher, and the clearing reports. Lose any machine, and its replacement replays the log "
            "and catches up. It's called state machine replication. <bookmark mark='j'/> Jane Street built its own "
            "matching system, JX, this way: each component handles around half a million messages a second, with "
            "latencies of a few microseconds, and any one of them can be rebuilt from the log in under a minute. "
            "Remember this idea: the best trading systems are built the same way."
        ) as vo:
            vo.wait_until("l")
            self.play(LaggedStart(*[FadeIn(c, shift=RIGHT * 0.1) for c in log], lag_ratio=0.08), FadeIn(ll), run_time=1.5)
            vo.wait_until("c")
            self.play(LaggedStart(*[AnimationGroup(GrowArrow(a), FadeIn(c)) for a, c in zip(arrows, comps)],
                                  lag_ratio=0.3), run_time=2)
            self.play(FadeIn(eq))
            vo.wait_until("j")
            self.play(FadeIn(jx))
        self.clear_scene()

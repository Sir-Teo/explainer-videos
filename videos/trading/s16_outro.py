from __future__ import annotations

import numpy as np

from explainer import *  # noqa: F403
from videos.trading.common import FACTS, label, load, loop_diagram, loop_focus, loop_reset, note, tagged


class Outro(VoiceoverScene):
    def construct(self):
        self.whole()
        self.recap()
        self.credits()

    # ------------------------------------------------------------------
    def whole(self):
        loop = loop_diagram().shift(UP * 0.9)
        bb = load("bookbench")["native"]["variants"]["prefaulted"]["ns_per_message"]
        geo = load("geo")["routes"]["carteret"]
        notes = {
            "exchange": (rf"one line, one thread;\\multicast to all", C.TRADE),
            "feed": (r"A/B arbitration;\\kernel bypass", C.MSG),
            "book": (rf"{bb:.0f} ns a message\\(measured)", C.MSG),
            "signal": (r"imbalance: strongest\\50 ms ahead", C.SIGNAL),
            "quote": (r"skew against\\inventory", C.OURS),
            "risk": (r"every order,\\inline", C.RISK),
            "gateway": (rf"FPGA record:\\{FACTS['stac_t0_ns']} ns", C.ORDER),
        }
        ann = VGroup()
        for k, (t, c) in notes.items():
            n = loop.nodes[k]
            ann.add(label(t, font_size=19, color=c).next_to(n, UP, buff=0.2))
        bottom = VGroup(
            label(rf"Chicago $\to$ New Jersey: {FACTS['quincy_carteret_ms']} ms by microwave; light needs {geo['vacuum_ms']:.2f}",
                  font_size=24, color=C.MICROWAVE),
            label(r"the fastest round trip on Nasdaq: 20--25 $\mu$s \quad races: 5--10 $\mu$s", font_size=24, color=C.LATENCY),
        ).arrange(DOWN, buff=0.12).to_edge(DOWN, buff=0.55)
        with self.voiceover(
            "So here's the whole machine again, with what we found at every stage. <bookmark mark='e'/> An exchange "
            "that puts every event in one line, on one thread, and multicasts the result to everyone at once. "
            "<bookmark mark='f'/> A feed handler that arbitrates two copies of the feed and bypasses the operating "
            "system. <bookmark mark='b'/> An order book that absorbs a message in tens of nanoseconds. <bookmark "
            "mark='s'/> A fair value built from clues that fade within a second, <bookmark mark='q'/> quotes that "
            "lean against inventory, <bookmark mark='r'/> risk checks on every single order, <bookmark mark='g'/> "
            "and, at the extreme, hardware that answers before the question has finished arriving. <bookmark "
            "mark='w'/> All of it racing the speed of light between Chicago and New Jersey, and other machines whose "
            "full round trip, on that ordinary Wednesday, took about twenty microseconds."
        ) as vo:
            self.play(FadeIn(loop))
            for k, m in zip(loop.keys, "efbsqrg"):
                vo.wait_until(m)
                i = loop.keys.index(k)
                self.play(FadeIn(ann[i], shift=DOWN * 0.1), Indicate(loop.nodes[k], color=notes[k][1], scale_factor=1.05),
                          run_time=0.7)
            vo.wait_until("w")
            self.play(FadeIn(bottom))
            pkt = Dot(radius=0.1, color=C.MSG).move_to(loop.nodes["exchange"].get_center())
            self.add(pkt)
            path = VMobject().set_points_as_corners([loop.nodes[k].get_center() for k in loop.keys])
            self.play(MoveAlongPath(pkt, path), run_time=1.6, rate_func=linear)
            pkt.set_color(C.ORDER)
            self.play(MoveAlongPath(pkt, loop.ret[0].copy()), run_time=0.9, rate_func=linear)
            self.remove(pkt)
        self.clear_scene()

    # ------------------------------------------------------------------
    def recap(self):
        pts = VGroup(*[label(t, font_size=28) for t in [
            r"1.\ A market maker earns fractions of a cent and loses to better-informed traders: be right, and be fast.",
            r"2.\ Exchanges are single-threaded sequencers broadcasting by multicast; 97\% of orders never trade.",
            r"3.\ Correlations vanish at millisecond scales, so stale quotes create races decided in microseconds.",
            r"4.\ Distance is time: microwaves within 1.3\% of light speed; equal cables inside the data center.",
            r"5.\ Inside the box: caches, no kernel, pinned cores, lock-free rings, and a war on the tail.",
            r"6.\ FPGAs act before the packet ends; software sets the plan.",
            r"7.\ Fills are adversely selected: simulate real queues honestly, and test every change.",
            r"8.\ Risk checks are part of the trading system; Knight Capital lost \$460 million in 45 minutes without them.",
        ]]).arrange(DOWN, aligned_edge=LEFT, buff=0.22)
        if pts.width > 13.4:
            pts.scale_to_fit_width(13.4)
        with self.voiceover(
            "To recap. A market maker earns fractions of a cent, and loses them to better-informed traders, so it must "
            "be both right and fast. Exchanges are single-threaded sequencers that broadcast by multicast, and nearly "
            "all of their traffic is quoting, not trading. Prices that move together over minutes move independently "
            "over milliseconds, and that's where the races happen. Distance is time, so firms bend radio waves along "
            "the shortest path and fight over meters of cable. Inside the box, they avoid the operating system, pin "
            "work to cores, and fight the slow tail. Hardware handles the reflexes. Fills are adversely selected, so "
            "everything is tested against real queues. And risk checks aren't paperwork: they're part of the machine."
        ) as vo:
            self.play(LaggedStart(*[FadeIn(p, shift=RIGHT * 0.15) for p in pts], lag_ratio=0.5), run_time=vo.duration - 1)
        self.clear_scene()

    # ------------------------------------------------------------------
    def credits(self):
        lines = VGroup(
            label(r"Building a Top-Tier Real-Time Trading System", font_size=40),
            label(r"market data: Nasdaq TotalView-ITCH 5.0, Wednesday December 10, 2025 (846.8 million messages)",
                  font_size=22, color=GREY_A),
            label(r"measurements: the 4-core virtual machine that rendered this video", font_size=22, color=GREY_A),
            label(r"sources: Jane Street tech talks and Signals and Threads (Brian Nigito); HRT Beat; Budish, Cramton \& Shim "
                  r"(2015);", font_size=22, color=GREY_A),
            label(r"Aquilina, Budish \& O'Neill (2022); Glosten \& Milgrom (1985); Avellaneda \& Stoikov (2008); STAC; "
                  r"the SEC's Knight Capital order (2013)", font_size=22, color=GREY_A),
            label(r"An explanation of public information. Not affiliated with any firm named. Not investment advice.",
                  font_size=22, color=GREY_B),
        ).arrange(DOWN, buff=0.22)
        with self.voiceover(
            "Every chart of market data in this video came from one real day of Nasdaq's feed, and every timing "
            "measurement from the computer that made the video. The sources are listed in the description. Thanks "
            "for watching."
        ) as vo:
            self.play(LaggedStart(*[FadeIn(l, shift=UP * 0.1) for l in lines], lag_ratio=0.3), run_time=3)
        self.wait(2)
        self.play(*[FadeOut(m) for m in self.mobjects])

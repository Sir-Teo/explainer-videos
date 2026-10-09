from __future__ import annotations

import numpy as np

from explainer import *  # noqa: F403
from videos.trading.common import FACTS, label, load, node, note, schematic_tag, server_box, tagged


class ResearchLoop(VoiceoverScene):
    def construct(self):
        self.replay()
        self.clocks()
        self.loop()

    # ------------------------------------------------------------------
    def replay(self):
        log = VGroup(*[VGroup(Rectangle(width=0.55, height=0.5, stroke_color=C.LATENCY, stroke_width=1.5,
                                        fill_color=[C.MSG, C.MSG, C.ORDER, C.MSG, C.LATENCY][i % 5], fill_opacity=0.35),
                              Integer(i + 1, font_size=18)) for i in range(14)])
        for c in log:
            c[1].move_to(c[0])
        log.arrange(RIGHT, buff=0.05).to_edge(UP, buff=1.1)
        ll = label(r"every input, in order, with a hardware timestamp: market data, order acknowledgments, timers",
                   font_size=24, color=GREY_A).next_to(log, UP, buff=0.15)
        prod = node(r"trading system\\(live)", C.OURS, width=3.0, height=1.1, font_size=24).move_to(LEFT * 3.2 + DOWN * 0.6)
        sim = node(r"the same code\\(replaying the log)", C.SIGNAL, width=3.0, height=1.1, font_size=24).move_to(RIGHT * 3.2 + DOWN * 0.6)
        a1 = Arrow(log.get_bottom() + LEFT * 2, prod.get_top(), buff=0.1, color=C.LATENCY, stroke_width=3)
        a2 = Arrow(log.get_bottom() + RIGHT * 2, sim.get_top(), buff=0.1, color=C.LATENCY, stroke_width=3)
        outs = VGroup(*[label(t, font_size=22, color=GREY_A) for t in [r"orders: \#1 buy 100 @ 183.85, \#2 cancel \#1, \dots",
                                                                         r"orders: \#1 buy 100 @ 183.85, \#2 cancel \#1, \dots"]])
        outs[0].next_to(prod, DOWN, buff=0.3)
        outs[1].next_to(sim, DOWN, buff=0.3)
        eq = MathTex(r"=", font_size=60).move_to((outs[0].get_center() + outs[1].get_center()) / 2)
        uses = VGroup(label(r"why it matters: explain any decision after the fact \quad test new code on last month's "
                            r"markets \quad rebuild a crashed process in seconds", font_size=22, color=GREY_A)).to_edge(DOWN, buff=0.4)
        tag = schematic_tag()
        head = label(r"same inputs, same decisions", font_size=40).to_edge(UP, buff=0.4)
        self.play(FadeIn(head), run_time=0.6)
        with self.voiceover(
            "Remember the exchange's trick: put every input in one numbered line, and make every component a "
            "deterministic function of that line. <bookmark mark='l'/> The best trading systems are built the same "
            "way. Every input, every market data packet, every acknowledgment from the exchange, even the ticks of "
            "the timer, is recorded in order, with a timestamp from the network hardware. <bookmark mark='p'/> The "
            "live system reads that stream, <bookmark mark='s'/> and so can a copy of exactly the same code, later, "
            "and it will make exactly the same decisions, message for message. <bookmark mark='w'/> That lets you "
            "explain any decision after the fact, test new code against last month's markets, and restart a crashed "
            "process by replaying its log. It's how Jane Street describes building its own systems, and it's why the "
            "simulator and the trading system are, as far as possible, the same program."
        ) as vo:
            self.play(FadeIn(tag))
            vo.wait_until("l")
            self.play(FadeOut(head), LaggedStart(*[FadeIn(c, shift=RIGHT * 0.1) for c in log], lag_ratio=0.06), FadeIn(ll),
                      run_time=1.6)
            vo.wait_until("p")
            self.play(FadeIn(prod), GrowArrow(a1))
            self.play(FadeIn(outs[0]))
            vo.wait_until("s")
            self.play(FadeIn(sim), GrowArrow(a2))
            self.play(FadeIn(outs[1]), FadeIn(eq))
            vo.wait_until("w")
            self.play(FadeIn(uses))
        self.clear_scene()

    # ------------------------------------------------------------------
    def clocks(self):
        offsets = [7.0, -4.0, 11.0, -9.0, 3.0]
        names = ["feed handler", "strategy", "gateway", "capture", "exchange"]
        clocks = VGroup()
        for name in names:
            c = Circle(radius=0.55, stroke_color=C.LATENCY, stroke_width=2.5)
            g = VGroup(c, label(name, font_size=20, color=GREY_A).next_to(c, DOWN, buff=0.12))
            clocks.add(g)
        clocks.arrange(RIGHT, buff=0.9).move_to(UP * 0.4)
        k = ValueTracker(1.0)
        hands = always_redraw(lambda: VGroup(*[Line(c[0].get_center(), c[0].get_center() + 0.45 * np.array(
            [np.sin(off * k.get_value() * 0.12), np.cos(off * k.get_value() * 0.12), 0]), color=C.LATENCY, stroke_width=3)
            for c, off in zip(clocks, offsets)]))
        ttl = label(r"to compare timestamps across machines, their clocks must agree", font_size=30).to_edge(UP, buff=0.45)
        gps = node(r"GPS-disciplined grandmaster clock, PTP over the network", C.LATENCY, width=8.2, height=0.7, font_size=24)
        gps.next_to(clocks, DOWN, buff=0.9)
        rule = label(rf"Europe's MiFID II rules: high-frequency traders within {FACTS['rts25_max_div_us']} $\mu$s of UTC, "
                     rf"timestamps to {FACTS['rts25_granularity_us']} $\mu$s or finer", font_size=24, color=GREY_A)
        rule.to_edge(DOWN, buff=0.4)
        with self.voiceover(
            "To line up events from many machines, and to measure your own latency honestly, every clock has to "
            "agree. <bookmark mark='c'/> Left alone, computer clocks drift apart by microseconds every second. <bookmark "
            "mark='g'/> So firms discipline them all from a master clock locked to GPS satellites, using a network "
            "protocol called PTP, with timestamps applied in the network hardware itself. <bookmark mark='r'/> "
            "Regulators care too: in Europe, high-frequency traders must keep their clocks within a hundred "
            "microseconds of official time and record events to the microsecond."
        ) as vo:
            self.play(FadeIn(ttl))
            vo.wait_until("c")
            self.play(FadeIn(clocks))
            self.add(hands)
            self.play(k.animate.set_value(6.0), run_time=2.5, rate_func=linear)
            vo.wait_until("g")
            self.play(FadeIn(gps))
            self.play(k.animate.set_value(0.0), run_time=1.5)
            vo.wait_until("r")
            self.play(FadeIn(rule))
        hands.clear_updaters()
        self.clear_scene()

    # ------------------------------------------------------------------
    def loop(self):
        steps = [(r"data\\{\small every message, every day, for years}", C.MSG),
                 (r"research\\{\small ideas, models, big compute}", C.SIGNAL),
                 (r"simulation\\{\small replay every queue honestly}", C.LATENCY),
                 (r"small live test", C.OURS),
                 (r"measure\\{\small fills, markouts, latency}", C.TRADE)]
        R = 2.5
        nodes = VGroup()
        for i, (t, c) in enumerate(steps):
            a = PI / 2 - i * TAU / len(steps)
            nodes.add(node(t, c, width=3.4, height=1.15, font_size=22).move_to([np.cos(a) * R * 1.45, np.sin(a) * R * 0.95 - 0.3, 0]))
        arrows = VGroup(*[CurvedArrow(nodes[i].get_center(), nodes[(i + 1) % len(steps)].get_center(), angle=-0.35,
                                      color=GREY_B, stroke_width=2.5) for i in range(len(steps))])
        for a, i in zip(arrows, range(len(steps))):
            a.scale(0.55, about_point=(nodes[i].get_center() + nodes[(i + 1) % len(steps)].get_center()) / 2)
        cul = VGroup(
            label(r"Jane Street: OCaml nearly everywhere, its type system catching mistakes before they trade", font_size=22,
                  color=GREY_A),
            label(r"HRT: C++ ``at the center of our live trading systems and research infrastructure''", font_size=22,
                  color=GREY_A),
        ).arrange(DOWN, buff=0.1).to_edge(DOWN, buff=0.2)
        head = label(r"the research loop", font_size=40).to_edge(UP, buff=0.3)
        self.play(FadeIn(head), run_time=0.6)
        with self.voiceover(
            "And then the whole machine sits inside a bigger loop, the one that makes it better. <bookmark mark='d'/> "
            "Data: every message from every venue, kept for years. <bookmark mark='r'/> Research: ideas and models, "
            "fitted on big computing clusters. <bookmark mark='s'/> Simulation: replaying the real queues, honestly, "
            "with your orders in them. <bookmark mark='l'/> A small live test, <bookmark mark='m'/> and measurement: "
            "did the fills, the markouts and the latency look the way the simulator said they would? If not, that "
            "difference is the most valuable data of all. <bookmark mark='c'/> The firms differ in style. Jane Street "
            "writes nearly everything in OCaml, a language whose strict types catch many mistakes before the code ever "
            "runs. Hudson River Trading puts C++ at the center of its trading systems and its research "
            "infrastructure, and says it has built one of the world's most advanced computing environments. But all of "
            "them run this loop, every day."
        ) as vo:
            for i, m in enumerate("drslm"):
                vo.wait_until(m)
                anims = [FadeIn(nodes[i], scale=1.05)]
                if i:
                    anims.append(Create(arrows[i - 1]))
                self.play(*anims, run_time=0.7)
            self.play(Create(arrows[-1]))
            vo.wait_until("c")
            self.play(FadeIn(cul))
        self.clear_scene()

from __future__ import annotations

import numpy as np

from explainer import *  # noqa: F403
from videos.trading.common import (
    FACTS, Mono, Plot, fmt_ns, label, load, mtex, node, note, schematic_tag, source, tagged,
)

# Byte layout of one Nasdaq add-order in a multicast frame: Ethernet 14, IPv4 20, UDP 8, MoldUDP64 header 20,
# message length 2, the 36-byte message, Ethernet checksum 4.
FRAME = [("Ethernet", 14, GREY_B), ("IP", 20, GREY_B), ("UDP", 8, GREY_B), ("MoldUDP64", 20, C.LATENCY),
         ("len", 2, GREY_D), ("type, stock, time", 11, C.MSG), ("order \\#", 8, C.SIGNAL), ("side", 1, C.BID),
         ("shares", 4, C.OURS), ("ticker", 8, C.TRADE), ("price", 4, C.ORDER), ("CRC", 4, GREY_D)]


class Hardware(VoiceoverScene):
    def construct(self):
        self.wire()
        self.pipeline()
        self.split()

    # ------------------------------------------------------------------
    def wire(self):
        total = sum(n for _, n, _ in FRAME)
        assert total == 104
        unit = 0.118
        segs = VGroup()
        for name, n, col in FRAME:
            r = Rectangle(width=n * unit, height=0.6, stroke_color=col, stroke_width=1.5, fill_color=col, fill_opacity=0.35)
            segs.add(r)
        segs.arrange(RIGHT, buff=0)
        labs = VGroup()
        for (name, n, col), r in zip(FRAME, segs):
            if n >= 8:
                t = label(name, font_size=16 if n < 14 else 18)
                if t.width > r.width - 0.04:
                    t.scale_to_fit_width(r.width - 0.06)
                labs.add(t.move_to(r))
        frame = VGroup(segs, labs).move_to(UP * 1.2)
        ttl = label(r"the real Nvidia add order, as it travels on the wire: 104 bytes", font_size=30).to_edge(UP, buff=0.4)
        ns_per_byte = 0.8
        t_frame = total * ns_per_byte
        info = VGroup(
            label(r"at 10 gigabits per second, one byte every 0.8 ns", font_size=26, color=GREY_A),
            label(rf"the whole frame takes {t_frame:.0f} ns to arrive", font_size=26, color=C.LATENCY),
            label(r"the price, the field a decision needs, is almost the last thing to arrive", font_size=26,
                  color=C.ORDER),
        ).arrange(DOWN, buff=0.15).move_to(DOWN * 0.6)
        price_i = [n for n, *_ in FRAME].index("price")
        self.play(FadeIn(ttl), FadeIn(segs), FadeIn(labs), run_time=0.8)
        with self.voiceover(
            "Software, however well tuned, has a floor: the whole packet has to arrive, cross into memory, and be picked up "
            "by the processor before any code can look at it. The fastest firms don't wait. <bookmark mark='f'/> Here "
            "is that real Nvidia order again, wrapped in the headers it travels in: 104 bytes. <bookmark mark='w'/> On a "
            "ten-gigabit link, a byte arrives every eight tenths of a nanosecond, so the frame takes 83 nanoseconds to "
            "arrive, and the field that matters most, the price, comes almost last."
        ) as vo:
            vo.wait_until("f")
            self.play(LaggedStart(*[Indicate(s, scale_factor=1.15, color=WHITE) for s in segs], lag_ratio=0.08), run_time=1.5)
            vo.wait_until("w")
            self.play(FadeIn(info[0]), FadeIn(info[1]))
            self.play(Indicate(segs[price_i], color=C.ORDER, scale_factor=1.3), FadeIn(info[2]))
        self.frame_parts = (frame, segs)
        self.clear_scene()

    # ------------------------------------------------------------------
    def pipeline(self):
        # an FPGA: stages laid out in silicon; the frame streams in 8 bytes per clock
        chip = RoundedRectangle(width=8.4, height=3.0, corner_radius=0.15, stroke_color=C.FPGA, stroke_width=3,
                                fill_color=C.FPGA, fill_opacity=0.06).move_to(DOWN * 0.2)
        cl = label(r"FPGA: a circuit, not a program", font_size=26, color=C.FPGA).next_to(chip, UP, buff=0.15)
        stages = [("Ethernet\\\\+ IP/UDP", GREY_B), ("sequence\\\\check", C.LATENCY), ("parse\\\\ITCH", C.MSG),
                  ("compare to\\\\trigger table", C.SIGNAL), ("send\\\\order", C.ORDER)]
        boxes = VGroup(*[node(t, c, width=1.45, height=1.25, font_size=20) for t, c in stages]).arrange(RIGHT, buff=0.18)
        boxes.move_to(chip)
        wires = VGroup(*[Arrow(a.get_right(), b.get_left(), buff=0.02, stroke_width=2.5, color=GREY_B, tip_length=0.1,
                               max_tip_length_to_length_ratio=0.5) for a, b in zip(boxes[:-1], boxes[1:])])
        yb = boxes.get_y()
        port_in = Line([-7.2, yb, 0], [chip.get_left()[0], yb, 0], color=C.MSG, stroke_width=4)
        port_out = Line([chip.get_right()[0], yb, 0], [7.2, yb, 0], color=C.ORDER, stroke_width=4)
        clock_t = ValueTracker(0)
        clk = always_redraw(lambda: VGroup(label(r"elapsed", font_size=24, color=GREY_A),
                                           MathTex(rf"{clock_t.get_value():5.1f}\,\mathrm{{ns}}", font_size=32,
                                                   color=C.LATENCY)).arrange(RIGHT, buff=0.15).to_corner(UL, buff=0.4))
        def word():
            return Rectangle(width=0.3, height=0.3, stroke_width=1, stroke_color=C.MSG, fill_color=C.MSG,
                             fill_opacity=0.7)
        step = 0.36
        x_in = chip.get_left()[0]
        words = VGroup(*[word().move_to([x_in - 0.2 - step * k, yb, 0]) for k in range(1, 9)])
        clk_note = note(r"one clock tick = 6.4 ns = 8 bytes in", font_size=22).next_to(chip, DOWN, buff=0.25)
        tag = schematic_tag()
        out_frame = VGroup(*[Rectangle(width=0.32, height=0.32, stroke_width=1, stroke_color=C.ORDER, fill_color=C.ORDER,
                                       fill_opacity=0.6) for _ in range(8)]).arrange(RIGHT, buff=0.04)
        out_frame.next_to(port_out.get_start(), RIGHT, buff=0.1)
        with self.voiceover(
            "<bookmark mark='c'/> An FPGA is a chip full of programmable logic: instead of running instructions, you "
            "lay out a circuit. <bookmark mark='p'/> A trading firm lays out a pipeline: decode the network headers, "
            "check the sequence number, parse the message, compare it against a table of triggers, send an order. "
            "<bookmark mark='s'/> The bytes stream in, eight at a time, one chunk every 6.4 nanoseconds, and each stage "
            "works on its piece of the frame while the rest is still arriving. <bookmark mark='o'/> And the reply can "
            "start before the input ends: the outgoing order's headers are prepared in advance, so the circuit starts "
            "sending them while the price is still on its way in, and fills in the decision at the last moment, or "
            "aborts the frame if the answer is no."
        ) as vo:
            self.play(FadeIn(tag))
            vo.wait_until("c")
            self.play(FadeIn(chip), FadeIn(cl))
            vo.wait_until("p")
            self.play(LaggedStart(*[FadeIn(b) for b in boxes], lag_ratio=0.15), FadeIn(wires), Create(port_in),
                      Create(port_out), run_time=1.5)
            vo.wait_until("s")
            self.add(clk, words)
            self.play(FadeIn(clk_note), FadeIn(words))
            # one 8-byte word reaches the chip every 6.4 ns (13 words in all); stages light up as their fields arrive
            stage_at = {1: 0, 6: 1, 8: 2, 12: 3}
            for k in range(1, 14):
                entering = words[0]
                new = word().move_to(words[-1].get_center() + LEFT * step) if k <= 5 else None
                anims = [words.animate.shift(RIGHT * step), clock_t.animate.set_value(6.4 * k)]
                if k in stage_at:
                    anims.append(boxes[stage_at[k]].box.animate.set_fill(opacity=0.55))
                if k == 11:
                    anims.append(FadeIn(out_frame, shift=RIGHT * 0.3))
                self.play(*anims, run_time=0.32 if k < 7 else 0.42, rate_func=linear)
                words.remove(entering)
                self.remove(entering)
                if new is not None:
                    words.add(new)
                    self.add(new)
                if k == 7:
                    vo.wait_until("o")
            self.play(boxes[4].box.animate.set_fill(opacity=0.6), out_frame.animate.shift(RIGHT * 1.4),
                      clock_t.animate.set_value(96.0), run_time=1.0, rate_func=linear)
        clk.clear_updaters()
        self.clear_scene()

        facts = VGroup(
            label(r"STAC-T0 benchmark record (AMD + Exegy, June 2024)", font_size=30),
            label(r"from the last bit of the data needed to the first bit of the order:", font_size=26, color=GREY_A),
            MathTex(rf"{FACTS['stac_t0_ns']}\ \mathrm{{nanoseconds}}", font_size=64, color=C.FPGA),
            label(rf"in that time, light travels about {FACTS['stac_t0_ns'] * 0.2998:.1f} meters", font_size=26,
                  color=GREY_A),
        ).arrange(DOWN, buff=0.25).move_to(UP * 0.3)
        with self.voiceover(
            "How fast can this be? <bookmark mark='s'/> There's an industry benchmark for exactly this, called STAC-T0. "
            "The record, set in 2024 with an AMD FPGA card and Exegy's design, is a minimum of 13.9 nanoseconds from "
            "the last bit of the market data to the first bit of the order. In that time, light travels about four "
            "meters."
        ) as vo:
            vo.wait_until("s")
            self.play(LaggedStart(*[FadeIn(f, shift=UP * 0.1) for f in facts], lag_ratio=0.3), run_time=2)
        self.clear_scene()

    # ------------------------------------------------------------------
    def split(self):
        brain = node(r"software: the brain\\{\small fair values, risk, strategy}", C.SIGNAL, width=4.6, height=1.5,
                     font_size=26).move_to(UP * 1.6)
        reflex = node(r"FPGA: the reflexes\\{\small if price in $X$ crosses $Y$, send order $Z$}", C.FPGA, width=4.6,
                      height=1.5, font_size=26).move_to(DOWN * 1.0)
        down = Arrow(brain.get_bottom(), reflex.get_top(), buff=0.1, color=C.SIGNAL, stroke_width=3)
        dl = label(r"updates the trigger tables, microseconds to seconds", font_size=22, color=GREY_A).next_to(down, RIGHT, buff=0.15)
        wire_in = Arrow(LEFT * 6.5 + DOWN * 1.0, reflex.get_left(), buff=0.1, color=C.MSG, stroke_width=3)
        wire_out = Arrow(reflex.get_right(), RIGHT * 6.5 + DOWN * 1.0, buff=0.1, color=C.ORDER, stroke_width=3)
        il = label(r"market data", font_size=22, color=C.MSG).next_to(wire_in, UP, buff=0.1)
        ol = label(r"orders, in nanoseconds", font_size=22, color=C.ORDER).next_to(wire_out, UP, buff=0.1)
        hc = VGroup(
            label(r"Jane Street designs its FPGAs in Hardcaml, an open-source hardware language it built on OCaml", font_size=24,
                  color=GREY_A),
            label(r"and on the network: layer-1 switches copy a signal in about 3--5 ns, vs 300--500 ns for a fast "
                  r"ordinary switch (Nigito)", font_size=24, color=GREY_A),
        ).arrange(DOWN, buff=0.12).to_edge(DOWN, buff=0.3)
        tag = schematic_tag()
        with self.voiceover(
            "But a circuit can't think very hard. So the work is split. <bookmark mark='b'/> Software is the brain: "
            "it works out fair values, risk limits and strategy, at its own pace, <bookmark mark='d'/> and keeps "
            "rewriting tables of instructions inside the hardware: if the price in this stock crosses this level, "
            "send that order. <bookmark mark='r'/> The FPGA is the reflex: it watches every packet and fires the "
            "pre-planned response in nanoseconds. <bookmark mark='h'/> Jane Street designs its FPGAs in Hardcaml, an "
            "open-source hardware language it built inside OCaml, the programming language it uses for nearly "
            "everything. And the same thinking reaches the network itself: special layer-1 switches that copy a signal "
            "in a few nanoseconds instead of hundreds."
        ) as vo:
            self.play(FadeIn(tag))
            vo.wait_until("b")
            self.play(FadeIn(brain))
            vo.wait_until("d")
            self.play(GrowArrow(down), FadeIn(dl))
            vo.wait_until("r")
            self.play(FadeIn(reflex), GrowArrow(wire_in), GrowArrow(wire_out), FadeIn(il), FadeIn(ol))
            for _ in range(2):
                d = Dot(wire_in.get_start(), radius=0.09, color=C.MSG)
                self.add(d)
                self.play(MoveAlongPath(d, Line(wire_in.get_start(), reflex.get_left())), run_time=0.5, rate_func=linear)
                d.set_color(C.ORDER)
                self.play(MoveAlongPath(d, Line(reflex.get_right(), wire_out.get_end())), run_time=0.4, rate_func=linear)
                self.remove(d)
            vo.wait_until("h")
            self.play(FadeIn(hc))
        self.clear_scene()

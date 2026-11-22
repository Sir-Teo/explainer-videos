from __future__ import annotations

import numpy as np

from explainer.cs import *  # noqa: F403
from videos.cs.cs5.common import fsm_block, tick_tokens, BG, CLOCK, CODE, COST, CTRL, DATA, FUNC, HEAD, INF, NO, PART, WIRE, YES, gate, load, wave


def box(w, h, text, color=CTRL, font_size=24):
    b = RoundedRectangle(width=w, height=h, corner_radius=0.08, stroke_color=color, stroke_width=2.2, fill_color=BG,
                         fill_opacity=1)
    return VGroup(b, MathTex(text, font_size=font_size, color=color).move_to(b))


class Logic(WatchScene):
    def construct(self):
        self.card()
        self.sync()
        self.celement()

    def card(self):
        self.chapter(13, r"Clocks, \ and memory as logic", r"Must everything march to one clock?", part=PART, said="Chapter thirteen. Clocks, and memory as logic.")

    # ------------------------------------------------------------------
    def sync(self):
        head = label(r"The synchronous discipline", font_size=38).to_edge(UP, buff=0.35)
        blk = fsm_block(0.85).move_to(UP * 1.25 + LEFT * 0.2)
        rules = VGroup(*[label(t, font_size=25, color=c) for t, c in (
            (r"every flip-flop on one clock", YES),
            (r"logic only between registers: \ no loops that avoid a register", YES),
            (r"meet setup and hold on every path; \ synchronize every outside input", YES),
            (r"then a chip of billions of transistors \ behaves like a state machine, \ one step per tick", HEAD),
            (r"the cost: \ every step waits for the slowest path, \ and the clock tree burns power", NO),
        )]).arrange(DOWN, aligned_edge=LEFT, buff=0.22).to_edge(DOWN, buff=0.35)
        with self.voiceover(
            "Within a simple synchronous clock domain, the design discipline is a few strict rules. <bookmark "
            "mark='a'/> Every flip-flop shares one clock. Every loop passes through a register. Every path meets "
            "its setup and hold times, and every crossing from an unrelated clock domain uses an appropriate "
            "synchronization protocol. <bookmark mark='b'/> Obey them, and a chip of billions of transistors "
            "behaves exactly like a finite-state machine, taking one clean step per tick, simulated cycle by "
            "cycle the way this series simulates Pebble. That predictability is worth an enormous amount. "
            "<bookmark mark='c'/> The price is that every step waits for the slowest path, even when the work "
            "this cycle was easy, and the clock network that reaches every flip-flop can consume a substantial "
            "fraction of dynamic power, depending on the chip. Modern chips soften both costs: clock gating "
            "switches the clock off to idle blocks, and different parts of a chip run on different clocks, joined "
            "by the synchronizers of chapter five."
        ) as vo:
            self.play(FadeIn(head), FadeIn(blk))
            vo.wait_until("a")
            self.play(LaggedStart(*[FadeIn(r) for r in rules[:3]], lag_ratio=0.4), run_time=2.0)
            vo.wait_until("b")
            self.play(FadeIn(rules[3]))
            tick_tokens(self, blk, ticks=3, run_time=1.1)
            vo.wait_until("c")
            self.play(FadeIn(rules[4]))
            self.play(Indicate(blk.logic, color=NO, scale_factor=1.05), Indicate(blk.clk, color=NO), run_time=1.2)
        self.wait(0.3)
        self.clear_scene()

    # ------------------------------------------------------------------
    def celement(self):
        self.ask(r"Can a digital circuit work with no clock at all?", [r"no", r"yes"], 1,
                 say="Could a digital circuit work with no clock at all?",
                 reveal="Yes: its parts tell each other when they are done.")
        head = label(r"Without a clock: \ the Muller C-element", font_size=36).to_edge(UP, buff=0.35)
        c = box(1.4, 1.2, r"\mathbf{C}", CTRL, 40).move_to(LEFT * 3.6 + UP * 1.0)
        ins = VGroup(Line(c.get_left() + UP * 0.3 + LEFT * 0.8, c.get_left() + UP * 0.3, color=WIRE, stroke_width=3),
                     Line(c.get_left() + DOWN * 0.3 + LEFT * 0.8, c.get_left() + DOWN * 0.3, color=WIRE, stroke_width=3))
        out = Line(c.get_right(), c.get_right() + RIGHT * 0.8, color=WIRE, stroke_width=3)
        labs = VGroup(MathTex("a", font_size=30, color=DATA).next_to(ins[0], LEFT, buff=0.1),
                      MathTex("b", font_size=30, color=DATA).next_to(ins[1], LEFT, buff=0.1),
                      MathTex("y", font_size=30, color=YES).next_to(out, RIGHT, buff=0.1))
        tt = VGroup(MathTex(r"a = b = 1 \Rightarrow y = 1", font_size=30, color=YES),
                    MathTex(r"a = b = 0 \Rightarrow y = 0", font_size=30, color=YES),
                    MathTex(r"a \ne b \Rightarrow y \text{ holds}", font_size=30, color=HEAD)).arrange(
            DOWN, aligned_edge=LEFT, buff=0.2).move_to(RIGHT * 2.6 + UP * 1.1)
        a = [0, 0, 1, 1, 1, 1, 1, 0, 0, 0, 0, 0, 1, 1, 1, 0, 0, 0]
        b = [0, 0, 0, 0, 1, 1, 1, 1, 1, 0, 0, 0, 0, 0, 1, 1, 0, 0]
        y, cur = [], 0
        for x1, x2 in zip(a, b):
            if x1 == x2:
                cur = x1
            y.append(cur)
        ws = VGroup(wave(a, x0=-4.0, y=-0.8, dx=0.45, color=DATA, name="a"),
                    wave(b, x0=-4.0, y=-1.6, dx=0.45, color=DATA, name="b"),
                    wave(y, x0=-4.0, y=-2.4, dx=0.45, color=YES, name="y"))
        foot = label(r"it waits for both: \ the building block of handshakes, \ asynchronous pipelines \ and "
                     r"arbiters \ (Muller, 1950s)", font_size=24, color=GREY_A).to_edge(DOWN, buff=0.3)
        with self.voiceover(
            "There is another way: circuits with no clock at all, which signal to each other when they are done. "
            "<bookmark mark='a'/> Their basic element, invented by David Muller in the 1950s, is the C-element. "
            "When both inputs are one, its output becomes one; when both are zero, zero; when they disagree, it "
            "holds its last value. It is a tiny state machine, and like the latch it needs feedback inside. "
            "<bookmark mark='b'/> In effect it waits for both of its inputs to agree before it acts, which is "
            "exactly what a handshake needs: I am ready, you are ready, go. Asynchronous circuits built this way "
            "run each step as fast as that step allows and avoid clock-driven switching while idle, though "
            "leakage and other static power remain. They are hard to design and test, so they survive mainly in "
            "niches: ultra-low-power chips, the arbiters that decide which of two requests came first, and the "
            "boundaries between clock domains."
        ) as vo:
            self.play(FadeIn(head), FadeIn(c), Create(ins), Create(out), FadeIn(labs), FadeIn(tt))
            vo.wait_until("a")
            self.play(Indicate(c, scale_factor=1.03))
            vo.wait_until("b")
            self.play(LaggedStart(*[Create(w) for w in ws], lag_ratio=0.2), run_time=2.5)
            self.play(FadeIn(foot))
        self.wait(0.3)
        self.clear_scene()


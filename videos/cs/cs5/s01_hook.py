from __future__ import annotations

import numpy as np

from explainer.cs import *  # noqa: F403
from videos.cs.cs5.common import (BG, CODE, CTRL, DATA, FUNC, HEAD, NO, PART, WIRE, YES, gate, load, nand_latch, wave)


class Hook(VoiceoverScene):
    def construct(self):
        self.forgets()
        self.loop()
        self.balance()
        self.plan()

    # ------------------------------------------------------------------
    def forgets(self):
        head = label(r"Everything so far forgets", font_size=40).to_edge(UP, buff=0.4)
        g = gate("AND", size=1.2).move_to(LEFT * 1.5 + UP * 0.6)
        a = Line(g.inp[0]() + LEFT * 1.4, g.inp[0](), color=WIRE, stroke_width=3)
        b = Line(g.inp[1]() + LEFT * 1.4, g.inp[1](), color=WIRE, stroke_width=3)
        o = Line(g.out(), g.out() + RIGHT * 1.6, color=WIRE, stroke_width=3)
        la = MathTex("a", font_size=34, color=DATA).next_to(a, LEFT, buff=0.1)
        lb = MathTex("b", font_size=34, color=DATA).next_to(b, LEFT, buff=0.1)
        lo = MathTex("y", font_size=34, color=YES).next_to(o, RIGHT, buff=0.1)
        circ = VGroup(g, a, b, o, la, lb, lo)
        wa = wave([0, 0, 1, 1, 1, 1, 0, 0, 0, 1, 1, 0, 0, 0], x0=-3.0, y=-1.4, dx=0.45, color=DATA, name="a")
        wb = wave([1] * 14, x0=-3.0, y=-2.1, dx=0.45, color=DATA, name="b")
        wy = wave([0, 0, 1, 1, 1, 1, 0, 0, 0, 1, 1, 0, 0, 0], x0=-3.0, y=-2.8, dx=0.45, color=YES, name="y")
        txt = label(r"the output depends only on the inputs \textit{now}", font_size=28, color=HEAD).to_edge(DOWN, buff=0.3)
        with self.voiceover(
            "Every circuit in Parts 3 and 4 had the same limitation. <bookmark mark='a'/> Its output depends only on "
            "its inputs right now. Change an input, and a few gate delays later the old answer is gone without a "
            "trace. An adder cannot remember the last sum, and a circuit like that cannot count, wait, or follow the "
            "steps of a program. <bookmark mark='b'/> A computer must remember: the program, the data, where it is in "
            "the program. This part is about how a circuit made of the same gates can hold on to a bit, and about "
            "what remembering costs."
        ) as vo:
            self.play(FadeIn(head), FadeIn(circ))
            vo.wait_until("a")
            self.play(Create(wa), Create(wb), Create(wy), run_time=2.5)
            self.play(FadeIn(txt))
        self.wait(0.3)
        self.clear_scene()

    # ------------------------------------------------------------------
    def loop(self):
        head = label(r"Feed the output back in", font_size=40).to_edge(UP, buff=0.4)
        lat = nand_latch(scale=1.2).move_to(UP * 0.2)
        cap = label(r"two NAND gates, \ each feeding the other", font_size=28, color=GREY_A).next_to(lat, DOWN, buff=0.6)
        hold = label(r"once set, \ it holds its value \ with both inputs idle", font_size=28, color=YES).next_to(
            cap, DOWN, buff=0.25)
        with self.voiceover(
            "The trick is a loop. <bookmark mark='a'/> Take two NAND gates, and wire each one's output into the "
            "other's input. Every circuit so far flowed from inputs to outputs; this one feeds back on itself, and "
            "that changes everything. <bookmark mark='b'/> Push it one way and it stays that way; push it the other "
            "way and it stays the other way. With its inputs left alone, it remembers which way it was pushed last. "
            "It is the simplest memory there is, and every register, cache and memory chip descends from it."
        ) as vo:
            self.play(FadeIn(head))
            vo.wait_until("a")
            self.play(FadeIn(lat.g1), FadeIn(lat.g2), FadeIn(lat.s_in), FadeIn(lat.r_in), FadeIn(lat.q_out),
                      FadeIn(lat.qn_out), FadeIn(lat.labs))
            self.play(Create(lat.w1), Create(lat.w2), run_time=1.5)
            self.play(FadeIn(cap))
            vo.wait_until("b")
            self.play(FadeIn(hold))
        self.wait(0.3)
        self.clear_scene()

    # ------------------------------------------------------------------
    def balance(self):
        head = label(r"A ball between two valleys", font_size=40).to_edge(UP, buff=0.4)
        ax = Axes(x_range=[-1.6, 1.6, 0.5], y_range=[-0.4, 1.2, 0.5], x_length=9.0, y_length=3.4, tips=False,
                  axis_config={"color": BG, "stroke_opacity": 0}).move_to(DOWN * 0.3)
        U = lambda x: (x ** 2 - 1) ** 2 * 0.8  # noqa: E731
        curve = ax.plot(U, x_range=[-1.5, 1.5], color=CTRL, stroke_width=4)
        xs = ValueTracker(0.0)
        ball = always_redraw(lambda: Dot(ax.c2p(xs.get_value(), U(xs.get_value())) + UP * 0.16, radius=0.16, color=HEAD))
        l0 = label(r"0", font_size=36, color=DATA).next_to(ax.c2p(-1, 0), DOWN, buff=0.3)
        l1 = label(r"1", font_size=36, color=DATA).next_to(ax.c2p(1, 0), DOWN, buff=0.3)
        top = label(r"balanced on the ridge: \ neither 0 nor 1", font_size=28, color=NO).next_to(ax.c2p(0, U(0)), UP,
                                                                                                 buff=0.5)
        foot = label(r"metastability: \ how long it stays up there \ has no upper bound", font_size=28,
                     color=HEAD).to_edge(DOWN, buff=0.5)
        with self.voiceover(
            "Memory brings something else into the story: time, and a strange risk. <bookmark mark='a'/> A latch is "
            "like a ball in a landscape with two valleys. Left is zero, right is one, and the ball rests in one of "
            "them. <bookmark mark='b'/> Between them is a ridge. A ball pushed exactly hard enough can come to rest on "
            "top, balanced, belonging to neither valley, and wait there for an amount of time that has no upper "
            "bound. Real flip-flops do this. It is called metastability, and every computer that listens to the "
            "outside world has to live with it."
        ) as vo:
            self.play(FadeIn(head), Create(curve), FadeIn(l0), FadeIn(l1))
            self.add(ball)
            self.play(xs.animate.set_value(-1.0), run_time=1.2)
            vo.wait_until("a")
            self.play(xs.animate.set_value(1.0), run_time=1.5, rate_func=there_and_back_with_pause)
            self.play(xs.animate.set_value(1.0), run_time=1.2)
            vo.wait_until("b")
            self.play(xs.animate.set_value(0.0), run_time=1.6, rate_func=rate_functions.ease_out_cubic)
            self.play(FadeIn(top))
            self.wait(1.0)
            self.play(FadeIn(foot))
        self.wait(0.3)
        self.clear_scene()

    # ------------------------------------------------------------------
    def plan(self):
        title = label(rf"Part {PART}: \ Memory and Time", font_size=46).to_edge(UP, buff=0.4)
        smap = series_map(current=PART, done=PART - 1).scale(0.92).next_to(title, DOWN, buff=0.35)
        obj = objectives_card([
            r"feedback: \ the SR latch, \ and the latch as a dynamical system with two stable states",
            r"flip-flops and the clock; \ setup, \ hold, \ and the fastest clock a circuit allows",
            r"metastability, \ measured, \ and the synchronizer that tames it",
            r"finite-state machines, \ Myhill--Nerode, \ and the first rung of a theory of languages",
            r"counters and LFSRs; \ Pebble's register file, \ built and verified",
            r"SRAM, \ DRAM, \ Rowhammer, \ and how computers remembered before chips",
        ], font_size=26).move_to(DOWN * 0.2)
        with self.voiceover(
            "This is Part 5 of Computer Science, Built. <bookmark mark='a'/> In this part: feedback, and the latch "
            "seen as a dynamical system with two stable states and a saddle between them. Flip-flops and the clock, "
            "setup and hold times, and the fastest clock a circuit can take. Metastability, measured, and the "
            "synchronizer that tames it. Finite-state machines, and the theorem that makes them the first rung of a "
            "theory of languages. Counters and linear feedback shift registers, and Pebble's register file, built and "
            "verified. Then real memory chips, static and dynamic, an attack that flips bits in them, and the strange "
            "machines that remembered before chips existed."
        ) as vo:
            self.play(FadeIn(title), FadeIn(smap))
            vo.wait_until("a")
            self.play(FadeOut(smap), FadeIn(obj))
        self.wait(0.4)
        self.clear_scene()

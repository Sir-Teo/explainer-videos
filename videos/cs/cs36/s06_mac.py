from __future__ import annotations

import math
import random

import numpy as np

from explainer.cs import *  # noqa: F403
from videos.cs.cs36.common import (DATA, HEAD, KERN, LAM, NO, PART, YES, box, grid_table, load)


class Mac(VoiceoverScene):
    def construct(self):
        self.card()
        self.aloha_timeline()
        self.aloha_curve()
        self.csma()
        self.hidden()

    def card(self):
        card = chapter_card(5, r"Sharing a channel", r"How do strangers take turns on one wire?", lit=(1970, 1976),
                            extra=((1970, r"Abramson: \ ALOHAnet"), (1976, r"Metcalfe and Boggs: \ Ethernet")),
                            part=PART)
        with self.voiceover("Chapter five. Sharing a channel."):
            self.play(FadeIn(card[0], shift=UP * 0.2), FadeIn(card[1]), FadeIn(card[2]))
        self.play(FadeOut(card))

    def aloha_timeline(self):
        head = label(r"ALOHA: \ just send", font_size=36).to_edge(UP, buff=0.3)
        rng = random.Random(9)
        starts, t = [], 0.0
        while t < 11.5:
            t += rng.expovariate(0.55)
            starts.append(t)
        starts = [s for s in starts if s < 11.5]
        x0, sc = -6.2, 1.05
        axis = Arrow([x0 - 0.1, -0.6, 0], [x0 + 12.4 * sc - 0.4, -0.6, 0], buff=0, color=GREY_D, stroke_width=2,
                     max_tip_length_to_length_ratio=0.02)
        tl = label(r"time, \ in frame lengths", font_size=17, color=GREY_B).next_to(axis, DOWN, buff=0.1)
        frames = VGroup()
        for i, s in enumerate(starts):
            ok = (i == 0 or s - starts[i - 1] >= 1) and (i == len(starts) - 1 or starts[i + 1] - s >= 1)
            r = Rectangle(width=sc * 1.0, height=0.45, stroke_color=YES if ok else NO, stroke_width=1.8,
                          fill_color=YES if ok else NO, fill_opacity=0.35)
            r.move_to([x0 + s * sc + sc / 2, -0.25 + 0.5 * (i % 3), 0])
            frames.add(r)
        vuln = VGroup(Brace(Line([x0 + 2 * sc, 0, 0], [x0 + 4 * sc, 0, 0]), UP, color=KERN))
        vl = label(r"vulnerable for two frame times", font_size=18, color=KERN).next_to(vuln, UP, buff=0.05)
        vg = VGroup(vuln, vl).move_to([-1.0, 2.0, 0])
        deriv = VGroup(
            MathTex(r"P(\text{no other start within } \pm 1) = e^{-2G}", font_size=30, color=WHITE),
            MathTex(r"S = G\,e^{-2G}, \qquad \max_G S = \frac{1}{2e} \approx 0.184 \ \text{at } G = \tfrac{1}{2}",
                    font_size=30, color=HEAD),
            MathTex(r"\text{slotted: } S = G\,e^{-G}, \qquad \max = \frac{1}{e} \approx 0.368", font_size=30,
                    color=YES),
        ).arrange(DOWN, buff=0.25).to_edge(DOWN, buff=0.4)
        with self.voiceover(
            "In 1970 Norman Abramson's ALOHAnet linked the Hawaiian islands by radio, every station sharing one "
            "frequency, with the simplest possible rule: when you have a frame, send it. <bookmark mark='a'/> If two "
            "frames overlap, both are garbled, and each sender tries again later, at random. <bookmark mark='b'/> "
            "How much gets through? Let frames start as a Poisson process, G of them per frame time, counting "
            "retries. A frame survives only if no other starts in the frame time before it or the frame time after: "
            "a window of two. <bookmark mark='c'/> The chance of that is e to the minus two G, so the throughput is G "
            "e to the minus two G. Its maximum, at G equal to a half, is one over two e: eighteen percent. "
            "<bookmark mark='d'/> If stations may start only at slot boundaries, the window halves, and the "
            "throughput doubles to one over e."
        ) as vo:
            self.play(FadeIn(head), GrowArrow(axis), FadeIn(tl))
            vo.wait_until("a")
            self.play(LaggedStart(*[FadeIn(f) for f in frames], lag_ratio=0.12), run_time=2.0)
            vo.wait_until("b")
            self.play(FadeIn(vg), FadeIn(deriv[0]))
            vo.wait_until("c")
            self.play(FadeIn(deriv[1]))
            vo.wait_until("d")
            self.play(FadeIn(deriv[2]))
        self.wait(0.3)
        self.clear_scene()

    def aloha_curve(self):
        m = load("mac")
        head = label(r"Measured against the formulas", font_size=36).to_edge(UP, buff=0.3)
        ax = Axes(x_range=[0, 3, 0.5], y_range=[0, 0.4, 0.1], x_length=7.0, y_length=4.0,
                  axis_config={"color": GREY_D, "include_numbers": False}).move_to([-2.2, -0.3, 0])
        xt = VGroup(*[label(f"{x:g}", font_size=16, color=GREY_B).next_to(ax.c2p(x, 0), DOWN, buff=0.1)
                      for x in (0.5, 1, 1.5, 2, 2.5, 3)])
        yt = VGroup(*[label(f"{y:.1f}", font_size=16, color=GREY_B).next_to(ax.c2p(0, y), LEFT, buff=0.1)
                      for y in (0.1, 0.2, 0.3, 0.4)])
        xl = label(r"offered load $G$, \ frames per frame time", font_size=17, color=GREY_A).next_to(xt, DOWN,
                                                                                                   buff=0.08)
        yl = label(r"throughput $S$", font_size=17, color=GREY_A).next_to(ax, UP, buff=0.1).align_to(ax, LEFT)
        f1 = ax.plot(lambda g: g * math.exp(-2 * g), x_range=[0, 3], color=HEAD, stroke_width=2.5)
        f2 = ax.plot(lambda g: g * math.exp(-g), x_range=[0, 3], color=YES, stroke_width=2.5)
        d1 = VGroup(*[Dot(ax.c2p(a["G"], a["S"]), radius=0.06, color=HEAD) for a in m["aloha"]])
        d2 = VGroup(*[Dot(ax.c2p(a["G"], a["S"]), radius=0.06, color=YES) for a in m["slotted"]])
        lg = VGroup(label(r"pure ALOHA: \ $Ge^{-2G}$", font_size=19, color=HEAD),
                    label(r"slotted: \ $Ge^{-G}$", font_size=19, color=YES),
                    label(r"dots: \ 80{,}000 simulated frames each", font_size=17, color=GREY_A)).arrange(
            DOWN, aligned_edge=LEFT, buff=0.15).move_to([4.2, 1.3, 0])
        lines = VGroup(
            wrapped_label(r"past the peak, \ more traffic means \\ \textit{less} gets through: \\ collisions breed retries",
                  5.6, font_size=20, color=NO),
            wrapped_label(r"a shared channel must keep \\ the offered load below the peak, \\ or collapse", 5.6, font_size=20,
                  color=WHITE),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.14).move_to([4.0, -1.0, 0])
        with self.voiceover(
            "We simulated eighty thousand frames at each load. <bookmark mark='a'/> Pure ALOHA's measured "
            "throughput falls on G e to the minus two G, peaking at point one eight four; slotted ALOHA's on G e to "
            "the minus G, peaking at point three six eight. <bookmark mark='b'/> Past the peak the curves fall: more "
            "traffic means more collisions, which mean more retries, which mean more traffic. Offered too much, a "
            "random-access channel collapses, and every such protocol must keep its load below the peak."
        ) as vo:
            self.play(FadeIn(head), Create(ax), FadeIn(xt), FadeIn(yt), FadeIn(xl), FadeIn(yl))
            vo.wait_until("a")
            self.play(Create(f1), Create(f2), FadeIn(d1), FadeIn(d2), FadeIn(lg), run_time=2)
            vo.wait_until("b")
            self.play(FadeIn(lines))
        self.wait(0.3)
        self.clear_scene()

    def csma(self):
        m = load("mac")
        head = label(r"Ethernet: \ listen first, \ and back off", font_size=36).to_edge(UP, buff=0.3)
        rules = VGroup(
            label(r"\textbf{carrier sense}: \ do not start while someone is sending", font_size=20, color=DATA),
            label(r"\textbf{collision detection}: \ if your signal is garbled, \ stop at once and jam", font_size=20,
                  color=NO),
            label(r"\textbf{binary exponential backoff}: \ after the $k$th collision, \ wait a random $0 \dots "
                  r"2^k - 1$ slots \ (capped at $2^{10}$)", font_size=20, color=HEAD),
            label(r"a slot is the round trip of the longest cable: \ 512 bits at 10 Mb/s, \ so a frame is at least "
                  r"64 bytes, \ long enough to hear a collision", font_size=20, color=KERN),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.18).next_to(head, DOWN, buff=0.4)
        for ln in rules:
            if ln.width > 12.8:
                ln.width = 12.8
        rows = [[f"{c['a']:g}", f"{c['beb']:.3f}", f"{c['p']:.3f}", f"{c['formula']:.3f}", f"{c['kurose']:.3f}"]
                for c in m["csma"]]
        tab = grid_table([r"$a$ = delay / frame", r"backoff, \ measured", r"$p = 1/n$, \ measured",
                          r"Metcalfe--Boggs", r"$1/(1 + 5a)$"], rows, widths=[2.6, 2.3, 2.3, 2.2, 1.8], row_h=0.38,
                         font_size=18, mono_cols=())
        tab.next_to(rules, DOWN, buff=0.4).set_x(0)
        for r in range(1, len(rows) + 1):
            tab.cells[r][1].set_color(YES)
            tab.cells[r][3].set_color(HEAD)
        foot = label(r"20 saturated stations: \ efficiency depends on $a$ \ (short cables, \ long frames are "
                     r"best), \ and backoff adapts as well as the best fixed probability", font_size=19,
                     color=WHITE).to_edge(DOWN, buff=0.3)
        if foot.width > 12.8:
            foot.width = 12.8
        with self.voiceover(
            "Bob Metcalfe's Ethernet, at Xerox in 1973, improved on ALOHA in three ways. <bookmark mark='a'/> Listen "
            "before sending, and wait if the cable is busy. <bookmark mark='b'/> While sending, keep listening; if "
            "the signal is garbled, someone else started too, so stop at once. <bookmark mark='c'/> Then wait a random "
            "number of slots, doubling the range after each collision, so the more crowded the cable, the more the "
            "stations spread out. <bookmark mark='d'/> A slot is the time for a signal to cross the longest cable and "
            "come back, and a frame must last at least that long, or a sender could finish before hearing the "
            "collision. That is why frames are at least sixty-four bytes. <bookmark mark='e'/> We simulated twenty "
            "busy stations. With delay small relative to the frame, efficiency is over ninety percent. Metcalfe and "
            "Boggs's formula matches the idealized protocol exactly, and real backoff does as well or better."
        ) as vo:
            self.play(FadeIn(head))
            for mk, r in zip("abcd", rules):
                vo.wait_until(mk)
                self.play(FadeIn(r))
            vo.wait_until("e")
            self.play(FadeIn(tab), FadeIn(foot))
        self.wait(0.3)
        self.clear_scene()

    def hidden(self):
        m = load("mac")
        head = label(r"Wi-Fi: \ the hidden terminal", font_size=36).to_edge(UP, buff=0.3)
        A = box(1.0, 0.6, r"A", DATA, font_size=24).move_to([-4.6, 0.9, 0])
        B = box(1.0, 0.6, r"B", YES, font_size=24).move_to([-3.0, 0.9, 0])
        C = box(1.0, 0.6, r"C", HEAD, font_size=24).move_to([-1.4, 0.9, 0])
        rA = Circle(radius=1.75, color=DATA, stroke_width=1.5).move_to(A).set_stroke(opacity=0.6)
        rC = Circle(radius=1.75, color=HEAD, stroke_width=1.5).move_to(C).set_stroke(opacity=0.6)
        rows = [[f"{h['G']:g}", f"{h['plain']:.3f}", f"{h['rts']:.3f}"] for h in m["hidden"]]
        tab = grid_table([r"load $G$", r"carrier sense", r"with RTS/CTS"], rows, widths=[1.6, 2.2, 2.2],
                         row_h=0.38, font_size=19, mono_cols=())
        tab.move_to([3.9, 0.9, 0])
        for r in range(1, len(rows) + 1):
            tab.cells[r][2].set_color(YES)
            tab.cells[r][1].set_color(NO)
        lines = VGroup(
            label(r"A and C both reach B, \ but not each other: \ carrier sense hears nothing, \ and their frames "
                  r"collide at B", font_size=20, color=NO),
            label(r"so to each other they are ALOHA: \ throughput $Ge^{-G}$, \ collapsing under load", font_size=20,
                  color=WHITE),
            label(r"\textbf{RTS/CTS}: \ ask B with a tiny request; \ B's clear-to-send, \ heard by both, \ reserves "
                  r"the air", font_size=20, color=YES),
            label(r"radios cannot hear while sending, \ so Wi-Fi \textit{avoids} collisions \ (CSMA/CA) \ and "
                  r"acknowledges every frame", font_size=20, color=LAM),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.18).to_edge(DOWN, buff=0.4)
        with self.voiceover(
            "Radio breaks carrier sense. <bookmark mark='a'/> Stations A and C can both reach the access point B, "
            "but not each other. Each listens, hears silence, and sends, and their frames collide at B. "
            "<bookmark mark='b'/> To each other they are back to ALOHA, and the throughput collapses as the load "
            "grows. <bookmark mark='c'/> The fix is to ask first: a short request to send, which can still collide "
            "but costs little, and B's reply, clear to send, which both A and C hear, and which reserves the air for "
            "the frame. In our simulation, at a load of two, it more than doubles the throughput. <bookmark mark='d'/> And because "
            "a radio cannot listen while it transmits, Wi-Fi cannot detect collisions as Ethernet does. It avoids "
            "them, and acknowledges every frame."
        ) as vo:
            self.play(FadeIn(head), FadeIn(A), FadeIn(B), FadeIn(C), Create(rA), Create(rC))
            vo.wait_until("a")
            self.play(FadeIn(lines[0]))
            vo.wait_until("b")
            self.play(FadeIn(tab), FadeIn(lines[1]))
            vo.wait_until("c")
            self.play(FadeIn(lines[2]))
            vo.wait_until("d")
            self.play(FadeIn(lines[3]))
        self.wait(0.3)
        self.clear_scene()


_ = (np, KERN)

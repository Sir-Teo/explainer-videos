from __future__ import annotations

import numpy as np

from explainer.cs import *  # noqa: F403
from videos.cs.cs38.common import (DATA, HEAD, KERN, LAM, NO, PART, PROCC, YES, grid_table, load)


class Snapshot(VoiceoverScene):
    def construct(self):
        self.card()
        self.cuts()
        self.algorithm()
        self.result()

    def card(self):
        card = chapter_card(3, r"Snapshots", r"How do you photograph a system that never stops?", lit=(1985, 1985),
                            extra=((1985, r"Chandy and Lamport: \ distributed snapshots"),), part=PART)
        with self.voiceover("Chapter three. Snapshots."):
            self.play(FadeIn(card[0], shift=UP * 0.2), FadeIn(card[1]), FadeIn(card[2]))
        self.play(FadeOut(card))

    def cuts(self):
        head = label(r"Consistent and inconsistent cuts", font_size=36).to_edge(UP, buff=0.3)
        x0, x1 = -5.4, 5.6
        lines = VGroup()
        for i in range(3):
            y = 1.4 - i * 1.4
            lines.add(VGroup(Line([x0, y, 0], [x1, y, 0], color=GREY_C, stroke_width=2),
                             label(f"$P_{i}$", font_size=22, color=PROCC[i]).move_to([x0 - 0.4, y, 0])))
        m1 = Arrow([-3.0, 1.4, 0], [-1.0, 0.0, 0], buff=0.05, color=GREY_B, stroke_width=2.5)
        m2 = Arrow([1.0, 0.0, 0], [3.0, -1.4, 0], buff=0.05, color=GREY_B, stroke_width=2.5)
        good = VMobject(color=YES, stroke_width=4).set_points_as_corners([[-2.0, 1.9, 0], [-0.4, 0.0, 0],
                                                                          [2.0, -1.9, 0]])
        bad = VMobject(color=NO, stroke_width=4).set_points_as_corners([[-3.6, 1.9, 0], [-0.4, 0.0, 0],
                                                                         [3.6, -1.9, 0]])
        gl = label(r"consistent: \ every message received before the cut was sent before it", font_size=20,
                   color=YES).to_edge(DOWN, buff=0.9)
        bl = label(r"inconsistent: \ a message received in the picture, \ but never sent", font_size=20,
                   color=NO).to_edge(DOWN, buff=0.4)
        with self.voiceover(
            "A snapshot records each process's state, but the processes cannot all stop at the same instant, "
            "because there is no instant. So a snapshot is a cut through the space-time diagram: one point on each "
            "process's line. <bookmark mark='a'/> A cut is consistent if every message received before it was also "
            "sent before it. Such a cut is a state the system could have been in, even if it never was at any one "
            "real moment. <bookmark mark='b'/> Here the red cut records a message arriving at P one that, in the "
            "picture, P zero has not yet sent. Money appears from nowhere, or a lock is held by two processes. That "
            "cut describes a state that could never have happened."
        ) as vo:
            self.play(FadeIn(head), FadeIn(lines), GrowArrow(m1), GrowArrow(m2))
            vo.wait_until("a")
            self.play(Create(good), FadeIn(gl))
            vo.wait_until("b")
            self.play(Create(bad), FadeIn(bl))
        self.wait(0.4)
        self.clear_scene()

    def algorithm(self):
        head = label(r"Chandy and Lamport's algorithm", font_size=36).to_edge(UP, buff=0.3)
        pos = [np.array(p) for p in ([-2.6, 1.2, 0], [2.6, 1.2, 0], [2.6, -1.6, 0], [-2.6, -1.6, 0])]
        nodes = VGroup(*[VGroup(Circle(radius=0.45, color=PROCC[i], stroke_width=3),
                                label(f"$P_{i}$", font_size=22, color=PROCC[i])).move_to(p)
                         for i, p in enumerate(pos)])
        chans = VGroup()
        for a in range(4):
            for b in range(4):
                if a < b:
                    chans.add(Line(pos[a], pos[b], color=GREY_D, stroke_width=1.5).scale(0.75))
        steps = VGroup(
            wrapped_label(r"the initiator records its own state and sends a \textbf{marker} on every outgoing "
                          r"channel", 4.6, font_size=19, color=HEAD),
            wrapped_label(r"on its \textit{first} marker a process records its state, \ records that channel as "
                          r"empty, \ and sends markers on", 4.6, font_size=19, color=KERN),
            wrapped_label(r"until a marker arrives on a channel, \ messages arriving on it are recorded as "
                          r"\textbf{in transit}", 4.6, font_size=19, color=LAM),
            wrapped_label(r"channels must be FIFO: \ the marker separates what was sent before the cut from what "
                          r"was sent after", 4.6, font_size=19, color=WHITE),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.25).move_to([4.6, -0.2, 0])
        nodes.shift(LEFT * 2.2)
        chans.shift(LEFT * 2.2)
        markers = VGroup(*[Square(0.18, stroke_width=0, fill_color=HEAD, fill_opacity=1).move_to(
            nodes[0].get_center()) for _ in range(3)])
        with self.voiceover(
            "K. Mani Chandy and Leslie Lamport found how to take a consistent cut while the system keeps "
            "running, in 1985. <bookmark mark='a'/> The process that starts the snapshot records its own state and "
            "sends a special message, a marker, on each of its outgoing channels. <bookmark mark='b'/> A process "
            "receiving its first marker records its own state at that moment, notes that channel as empty, and "
            "sends markers on all of its own channels. <bookmark mark='c'/> On every other incoming channel, it "
            "records whatever arrives until that channel's marker comes: those messages were in flight across the "
            "cut. <bookmark mark='d'/> It works because channels are first in, first out: the marker divides "
            "everything sent before the sender recorded its state from everything sent after."
        ) as vo:
            self.play(FadeIn(head), FadeIn(nodes), Create(chans))
            vo.wait_until("a")
            self.play(FadeIn(steps[0]), Indicate(nodes[0], color=HEAD))
            self.play(*[m.animate.move_to(nodes[k + 1].get_center()) for k, m in enumerate(markers)], run_time=1.5)
            vo.wait_until("b")
            self.play(FadeIn(steps[1]), FadeOut(markers))
            vo.wait_until("c")
            self.play(FadeIn(steps[2]))
            vo.wait_until("d")
            self.play(FadeIn(steps[3]))
        self.wait(0.4)
        self.clear_scene()

    def result(self):
        s = load("snapshot")
        d = s["demo"]
        head = label(r"A bank of four, \ photographed", font_size=36).to_edge(UP, buff=0.3)
        rows = [[f"$P_{k}$", f"{v}"] for k, v in sorted(d["states"].items())]
        tab = grid_table([r"recorded balance", r""], rows, widths=[2.6, 1.6], row_h=0.4, font_size=20,
                         mono_cols=())
        tab.move_to([-4.0, 0.6, 0])
        crow = [[k.replace("->", r" $\to$ "), f"{v}"] for k, v in d["channels"].items()]
        ctab = grid_table([r"in transit", r""], crow, widths=[2.2, 1.4], row_h=0.4, font_size=20, mono_cols=())
        ctab.move_to([0.2, 0.6, 0])
        for r in range(1, len(crow) + 1):
            ctab.cells[r][1].set_color(LAM)
        tot = VGroup(
            label(rf"balances {sum(d['states'].values())} \ $+$ \ in transit {sum(d['channels'].values())} \ "
                  rf"$=$ \ \textbf{{{d['recorded_total']}}}", font_size=24, color=YES),
            label(rf"asking each process in turn, \ a second apart: \ \textbf{{{d['survey_total']}}}", font_size=22,
                  color=NO),
            label(rf"{s['consistent']} of {s['runs']} snapshots exact; \ the naive surveys ranged from "
                  rf"{s['survey_range'][0]} to {s['survey_range'][1]}", font_size=20, color=GREY_A),
        ).arrange(DOWN, buff=0.22).to_edge(DOWN, buff=0.5)
        side = wrapped_label(r"the same idea checkpoints stream processors \ (Flink, \ Part 46) \ and detects "
                             r"deadlock and termination", 3.6, font_size=18, color=KERN).move_to([4.6, 0.6, 0])
        with self.voiceover(
            "We gave four processes a thousand units of money and let them send random amounts to each other over "
            "channels with random delays, never stopping. Then process zero started a snapshot. "
            "<bookmark mark='a'/> The recorded balances add up to seven hundred and forty-eight, and the money "
            "caught in transit on five channels to two hundred and fifty-two: exactly a thousand. "
            "<bookmark mark='b'/> A naive survey, asking each process its balance one second after the other, "
            "found seven hundred and forty-seven: money in flight was missed, and some was counted twice. Over "
            "fifty runs every snapshot was exact, and every survey was wrong. <bookmark mark='c'/> The same "
            "algorithm checkpoints the stream processors of Part 46, and detects when a distributed computation "
            "has deadlocked or finished."
        ) as vo:
            self.play(FadeIn(head))
            vo.wait_until("a")
            self.play(FadeIn(tab), FadeIn(ctab), FadeIn(tot[0]))
            vo.wait_until("b")
            self.play(FadeIn(tot[1]), FadeIn(tot[2]))
            vo.wait_until("c")
            self.play(FadeIn(side))
        self.wait(0.4)
        self.clear_scene()


_ = (DATA, HEAD)

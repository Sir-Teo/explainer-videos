from __future__ import annotations

import numpy as np

from explainer.cs import *  # noqa: F403
from videos.cs.cs5.common import BG, CLOCK, CODE, COST, CTRL, DATA, FUNC, HEAD, HIST, INF, NO, PART, WIRE, YES, load

MEMS = [
    (1949, r"delay lines", r"bits as sound pulses in tubes of mercury, \ read as they arrive; \ EDSAC, \ 1949"),
    (1948, r"Williams tubes", r"bits as charged spots on a TV screen; \ the Manchester Baby: \ 32 words of 32 bits"),
    (1953, r"core memory", r"magnetized ferrite rings, \ woven on wires; \ Forrester, \ MIT's Whirlwind"),
    (1970, r"DRAM", r"the Intel 1103: \ 1{,}024 bits on a chip; \ core is obsolete within a few years"),
    (1984, r"flash", r"charge trapped on a floating gate, \ kept without power \ (Part 34)"),
]


class History(VoiceoverScene):
    def construct(self):
        self.card()
        self.timeline_()
        self.delay()
        self.core()

    def card(self):
        card = chapter_card(14, r"Remembering, before chips", r"How did the first computers store their bits?",
                            lit=(1947, 1949, 1953, 1970), part=PART)
        with self.voiceover("Chapter fourteen. Remembering, before chips."):
            self.play(FadeIn(card[0], shift=UP * 0.2), FadeIn(card[1]), FadeIn(card[2]))
        self.play(FadeOut(card))

    # ------------------------------------------------------------------
    def timeline_(self):
        head = label(r"Five ways to hold a bit", font_size=38).to_edge(UP, buff=0.35)
        rows = VGroup()
        for i, (y, name, what) in enumerate(MEMS):
            r = VGroup(label(str(y), font_size=28, color=HIST), label(name, font_size=28, color=CTRL),
                       label(what, font_size=22, color=GREY_A))
            r[0].move_to([-6.0, 2.0 - 0.95 * i, 0], aligned_edge=LEFT)
            r[1].move_to([-4.6, 2.0 - 0.95 * i, 0], aligned_edge=LEFT)
            r[2].move_to([-1.8, 2.0 - 0.95 * i, 0], aligned_edge=LEFT)
            rows.add(r)
        with self.voiceover(
            "Before chips, computers remembered in ways that sound like science fiction. <bookmark mark='a'/> Delay "
            "lines turned bits into pulses of sound travelling down tubes of mercury; a bit was available only at the "
            "moment its pulse arrived at the end, so programmers arranged their data around the timing. Maurice "
            "Wilkes's EDSAC, at Cambridge in 1949, used them. <bookmark mark='b'/> The Williams tube stored bits as "
            "spots of charge on the face of a cathode-ray tube, which had to be redrawn constantly, like DRAM's "
            "refresh; the Manchester Baby, the first stored-program computer, ran on one in 1948, with thirty-two "
            "words of memory. <bookmark mark='c'/> Then core memory, magnetized rings, which ruled for twenty years, "
            "until the Intel 1103 of 1970 put a thousand bits on a chip, and the curve of Moore's law took over. "
            "<bookmark mark='d'/> Flash memory, which keeps its charge without power, arrived in the 1980s; it is the "
            "storage of Part 34."
        ) as vo:
            self.play(FadeIn(head))
            for mk, r in zip("abcd", (rows[0], rows[1], VGroup(rows[2], rows[3]), rows[4])):
                vo.wait_until(mk)
                self.play(FadeIn(r, shift=RIGHT * 0.15), run_time=1.0)
        self.wait(0.3)
        self.clear_scene()

    # ------------------------------------------------------------------
    def delay(self):
        head = label(r"Memory that moves: \ the delay line", font_size=38).to_edge(UP, buff=0.35)
        tube = RoundedRectangle(width=9.0, height=0.8, corner_radius=0.4, stroke_color=GREY_B, stroke_width=2.5,
                                fill_color=BG, fill_opacity=1).move_to(UP * 1.0)
        pulses = VGroup(*[Rectangle(width=0.12, height=0.5, stroke_width=0, fill_color=YES if b else BG,
                                    fill_opacity=0.9).move_to([-4.2 + 0.28 * i, 1.0, 0])
                          for i, b in enumerate([1, 0, 1, 1, 0, 0, 1, 0, 1, 1, 1, 0, 1, 0, 0, 1, 0, 1, 1, 0, 1, 0, 0, 1,
                                                 1, 0, 1, 1, 0, 1, 0])])
        tl = label(r"mercury", font_size=22, color=GREY_B).next_to(tube, UP, buff=0.1)
        ends = VGroup(label(r"crystal: \ sound out", font_size=20, color=DATA).next_to(tube, LEFT, buff=0.15),
                      label(r"crystal: \ sound in", font_size=20, color=DATA).next_to(tube, RIGHT, buff=0.15))
        loop = CurvedArrow(tube.get_right() + DOWN * 0.45, tube.get_left() + DOWN * 0.45, angle=-0.5, color=WIRE,
                           stroke_width=2.5)
        ll = label(r"amplified, \ reshaped \ and sent back in: \ the bits circulate", font_size=22,
                   color=GREY_A).next_to(loop, DOWN, buff=0.1)
        pts = VGroup(
            label(r"a word can be read only as it passes the end", font_size=24, color=HEAD),
            label(r"so programmers placed each instruction where it would arrive \ just as the previous one finished: "
                  r"\ ``optimum programming''", font_size=24, color=GREY_A),
            label(r"the first memory hierarchy problem: \ where your data is \ decides how fast you run \ (Part 9)",
                  font_size=24, color=YES),
        ).arrange(DOWN, buff=0.2).to_edge(DOWN, buff=0.35)
        with self.voiceover(
            "The delay line deserves a closer look too, because it made programmers think about memory in a way they "
            "still do. <bookmark mark='a'/> A tube of mercury, about a metre and a half long, with a quartz crystal at "
            "each end. One crystal turns electrical pulses into sound; the sound crawls down the mercury; the other "
            "crystal turns it back into pulses, which are amplified, cleaned up and fed back in. The bits circulate "
            "for as long as the machine runs. <bookmark mark='b'/> But a word can be read only at the moment it passes "
            "the end of the tube. So programmers placed each instruction and each piece of data where it would "
            "arrive just as the previous step finished, a craft called optimum programming. "
            "<bookmark mark='c'/> It was the first case of a lesson that Part 9 builds a whole hierarchy around: "
            "where your data is, and when, decides how fast your program runs."
        ) as vo:
            self.play(FadeIn(head), FadeIn(tube), FadeIn(tl), FadeIn(ends))
            vo.wait_until("a")
            self.play(FadeIn(pulses, lag_ratio=0.03), Create(loop), FadeIn(ll), run_time=1.6)
            self.play(pulses.animate.shift(RIGHT * 0.56), run_time=1.6, rate_func=linear)
            vo.wait_until("b")
            self.play(FadeIn(pts[0]), FadeIn(pts[1]))
            vo.wait_until("c")
            self.play(FadeIn(pts[2]))
        self.wait(0.3)
        self.clear_scene()

    # ------------------------------------------------------------------
    def core(self):
        head = label(r"Core memory", font_size=38).to_edge(UP, buff=0.35)
        n = 5
        grid = VGroup()
        cores = []
        for r in range(n):
            for c in range(n):
                p = np.array([-4.8 + 0.8 * c, 1.6 - 0.8 * r, 0])
                ring = Ellipse(width=0.42, height=0.28, color=FUNC, stroke_width=4).rotate(PI / 4 if (r + c) % 2 else
                                                                                          -PI / 4).move_to(p)
                cores.append(ring)
                grid.add(ring)
        xw = VGroup(*[Line([-5.4, 1.6 - 0.8 * r, 0], [-1.0, 1.6 - 0.8 * r, 0], color=GREY_C, stroke_width=1.5)
                      for r in range(n)])
        yw = VGroup(*[Line([-4.8 + 0.8 * c, 2.2, 0], [-4.8 + 0.8 * c, -2.2, 0], color=GREY_C, stroke_width=1.5)
                      for c in range(n)])
        sel = (2, 3)
        hx = xw[sel[0]].copy().set_stroke(HEAD, 4)
        hy = yw[sel[1]].copy().set_stroke(HEAD, 4)
        notes = VGroup(
            label(r"each ring is magnetized one way or the other: \\ 0 or 1", font_size=24, color=GREY_A),
            label(r"half the needed current on one row wire \\ and one column wire: \\ only the core at the crossing "
                  r"gets enough to flip", font_size=24, color=HEAD),
            label(r"reading flips it to 0 and senses the pulse: \\ destructive, \ like DRAM, \ so it is rewritten",
                  font_size=24, color=GREY_A),
            label(r"non-volatile: \ the bits survive with the power off; \\ threaded by hand, \ often by women "
                  r"textile workers; \\ Apollo's software was woven into core rope", font_size=22, color=HIST),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.32)
        notes.next_to(xw, RIGHT, buff=0.6).shift(DOWN * 0.1)
        with self.voiceover(
            "Core memory deserves a closer look, because its ideas are still in every memory chip. "
            "<bookmark mark='a'/> Each bit was a tiny ring of ferrite, magnetized clockwise or anticlockwise, threaded "
            "on a grid of wires. <bookmark mark='b'/> To select one core, send half the current needed to flip a core "
            "down its row wire and half down its column wire. Only the core at the crossing feels the full current "
            "and flips: the first two-dimensional address decoder, made of physics. "
            "<bookmark mark='c'/> Reading worked by trying to flip the core to zero and sensing whether it pulsed, "
            "which destroyed the value, so every read was followed by a write-back, exactly as in DRAM today. "
            "<bookmark mark='d'/> Unlike DRAM, core kept its bits with the power off. It was threaded by hand, often by "
            "women from the textile industry, and the Apollo guidance computer's programs were woven permanently into "
            "a related form, rope memory, wire by wire."
        ) as vo:
            self.play(FadeIn(head), Create(xw), Create(yw), FadeIn(grid))
            vo.wait_until("a")
            self.play(FadeIn(notes[0]))
            vo.wait_until("b")
            self.play(Create(hx), Create(hy), FadeIn(notes[1]))
            self.play(cores[sel[0] * n + sel[1]].animate.set_stroke(HEAD, 6).rotate(PI / 2))
            vo.wait_until("c")
            self.play(FadeIn(notes[2]))
            vo.wait_until("d")
            self.play(FadeIn(notes[3]))
        self.wait(0.3)
        self.clear_scene()

from __future__ import annotations

import numpy as np

from explainer.cs import *  # noqa: F403
from videos.cs.cs55.common import BG, DATA, HEAD, KERN, LAM, NO, PART, YES, mono


class Hardware(VoiceoverScene):
    def construct(self):
        self.card()
        self.rowhammer()
        self.spectre()
        self.channel()
        self.lesson()

    def card(self):
        card = chapter_card(4, r"When the hardware leaks", r"Can a layer below you betray you?", lit=(2014, 2018),
                            extra=((1996, r"Kocher: \ timing"), (2014, r"Rowhammer"), (2018, r"Spectre, Meltdown")),
                            part=PART)
        with self.voiceover("Chapter four. When the hardware leaks."):
            self.play(FadeIn(card[0], shift=UP * 0.2), FadeIn(card[1]), FadeIn(card[2]))
        self.play(FadeOut(card))

    def rowhammer(self):
        head = label(r"Rowhammer \ (Kim et al., 2014) \ --- \ Part 5", font_size=36).to_edge(UP, buff=0.3)
        nrows, ncols = 5, 14
        cells = []
        g = VGroup()
        for r in range(nrows):
            row = []
            for c in range(ncols):
                sq = Square(0.34, stroke_color=GREY_D, stroke_width=1, fill_color=YES, fill_opacity=0.6)
                sq.move_to([-5.2 + 0.4 * c, 1.7 - 0.5 * r, 0])
                row.append(sq)
                g.add(sq)
            cells.append(row)
        aggr, victim = (1, 3), 2
        tags = VGroup(label(r"aggressor", font_size=18, color=NO).next_to(cells[1][-1], RIGHT, buff=0.2),
                      label(r"victim row", font_size=18, color=HEAD).next_to(cells[2][-1], RIGHT, buff=0.2),
                      label(r"aggressor", font_size=18, color=NO).next_to(cells[3][-1], RIGHT, buff=0.2))
        notes = VGroup(
            wrapped_label(r"open two rows, \ again and again, \ as fast as you can", 5.0, font_size=19, color=GREY_A),
            wrapped_label(r"each activation disturbs the row between them \ and drains a little charge", 5.0,
                          font_size=19, color=GREY_A),
            wrapped_label(r"110 of 129 DDR3 modules flipped bits, \ some after $\approx$139{,}000 activations \ "
                          r"(within one 64 ms refresh)", 5.0, font_size=19, color=NO),
            wrapped_label(r"defences: \ refresh more often, \ count activations \ (TRR), \ ECC; \ in 2020 new "
                          r"patterns still flipped bits on DDR4", 5.0, font_size=19, color=YES),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.25).move_to([3.9, -0.2, 0])
        weak = [2, 6, 10]
        with self.voiceover(
            "Start at the bottom of the tower, with the memory itself, and recall Part 5. "
            "<bookmark mark='a'/> Pick two rows of DRAM and open them alternately, over and over, as fast as the "
            "machine allows. <bookmark mark='b'/> Each activation disturbs the row physically between them and drains "
            "a little charge from its cells, cells a program is never touching at all. <bookmark mark='c'/> In 2014 "
            "Yoongu Kim and colleagues measured this: of a hundred and twenty-nine DDR3 modules, a hundred and ten "
            "flipped bits, some after only about a hundred and thirty-nine thousand activations, well inside one "
            "sixty-four millisecond refresh period. A reliability margin had quietly become a security boundary. "
            "<bookmark mark='d'/> The defences, refreshing more often, counting activations, error-correcting codes, "
            "each helped and each was later worked around: in 2020 new access patterns flipped bits on DDR4 that had "
            "them all."
        ) as vo:
            self.play(FadeIn(head), FadeIn(g, lag_ratio=0.01), FadeIn(tags))
            vo.wait_until("a")
            self.play(FadeIn(notes[0]))
            for k in range(4):
                rr = aggr[k % 2]
                self.play(*[cells[rr][c].animate.set_fill(NO, 0.9) for c in range(ncols)], run_time=0.2)
                self.play(*[cells[rr][c].animate.set_fill(YES, 0.6) for c in range(ncols)], run_time=0.12)
            vo.wait_until("b")
            self.play(FadeIn(notes[1]), *[cells[victim][c].animate.set_fill(YES, 0.25) for c in range(ncols)])
            vo.wait_until("c")
            self.play(*[cells[victim][c].animate.set_fill(NO, 1.0) for c in weak], FadeIn(notes[2]))
            vo.wait_until("d")
            self.play(FadeIn(notes[3]))
        self.wait(0.4)
        self.clear_scene()

    def spectre(self):
        head = label(r"Spectre and Meltdown \ (2018) \ --- \ Part 8", font_size=36).to_edge(UP, buff=0.3)
        code = VGroup(mono("if x < len(array):        # a guess, predicted taken", 17, color=WHITE),
                      mono("    y = probe[ array[x]*64 ]  # runs before the check resolves", 17, color=NO)
                      ).arrange(DOWN, aligned_edge=LEFT, buff=0.12).move_to([0, 1.9, 0])
        n = 16
        lines = VGroup(*[Rectangle(width=0.5, height=0.5, stroke_color=GREY_C, stroke_width=1.3) for _ in range(n)])
        lines.arrange(RIGHT, buff=0.07).move_to([0, 0.2, 0])
        idx = VGroup(*[label(str(k), font_size=13, color=GREY_B).next_to(l, DOWN, buff=0.06)
                       for k, l in enumerate(lines)])
        hot = 11
        probe_l = label(r"probe array: \ one cache line per possible byte \ (16 of 256 shown)", font_size=17,
                        color=GREY_A).next_to(lines, UP, buff=0.3).set_x(0)
        notes = VGroup(
            wrapped_label(r"the branch predictor guesses ``in bounds'' and runs ahead, \ reading past the array", 12.4,
                          font_size=20, color=NO),
            wrapped_label(r"the result is \textit{rolled back} \ --- \ but the cache line it touched stays warm", 12.4,
                          font_size=20, color=HEAD),
            wrapped_label(r"time every line: \ the fast one names the secret byte \ (Flush+Reload, \ Yarom \& "
                          r"Falkner 2014). \ Meltdown read kernel memory the same way", 12.4, font_size=20,
                          color=YES),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.2).to_edge(DOWN, buff=0.4)
        with self.voiceover(
            "Now climb one layer, to the processor, and recall Part 8. <bookmark mark='a'/> To stay fast, the core "
            "guesses which way a branch will go and runs ahead before the guess is checked. Here it guesses that an "
            "index is in bounds and speculatively reads past the end of an array, then uses that secret byte to "
            "touch one line of a probe array. <bookmark mark='b'/> When the guess turns out wrong, the processor "
            "rolls the work back: architecturally, those instructions never happened. But the cache line it touched "
            "is still warm, and that it cannot undo. <bookmark mark='c'/> So the attacker times a read of every "
            "line; the one that is fast names the secret byte. That timing trick is Flush and Reload, from Yarom and "
            "Falkner in 2014, and it is how Spectre and Meltdown, disclosed in 2018, read memory across a boundary "
            "that every bounds check and every privilege bit said was closed."
        ) as vo:
            self.play(FadeIn(head), FadeIn(code))
            vo.wait_until("a")
            self.play(FadeIn(lines), FadeIn(idx), FadeIn(probe_l), FadeIn(notes[0]))
            vo.wait_until("b")
            self.play(lines[hot].animate.set_fill(YES, 0.8).set_stroke(YES), FadeIn(notes[1]))
            vo.wait_until("c")
            self.play(Indicate(lines[hot], color=YES, scale_factor=1.3), FadeIn(notes[2]))
        self.wait(0.4)
        self.clear_scene()

    def channel(self):
        head = label(r"Side channels \ (Parts 8 and 29)", font_size=36).to_edge(UP, buff=0.3)
        ax = Axes(x_range=[0, 16, 4], y_range=[0, 600, 200], x_length=5.4, y_length=3.0, tips=False,
                  axis_config={"color": GREY_C, "font_size": 15}).move_to([-3.3, -0.1, 0])
        xs = np.linspace(0, 16, 9)
        early = VMobject(color=NO, stroke_width=3).set_points_as_corners(
            [ax.c2p(x, 200 + 20 * x) for x in xs])
        const = VMobject(color=YES, stroke_width=3).set_points_as_corners(
            [ax.c2p(x, 520) for x in xs])
        xl = label(r"correct leading bytes of a guess", font_size=15, color=GREY_A).next_to(ax, DOWN, buff=0.2)
        yl = label(r"time (schematic)", font_size=15, color=GREY_A).next_to(ax, UP, buff=0.05).align_to(ax, LEFT)
        el = label(r"stop at first mismatch", font_size=16, color=NO).next_to(ax.c2p(9, 380), DR, buff=0.1)
        cl = label(r"constant time", font_size=16, color=YES).next_to(ax.c2p(1, 520), UR, buff=0.1)
        ill = label(r"illustrative", font_size=14, color=GREY_B).next_to(ax, DOWN, buff=0.5)
        notes = VGroup(
            wrapped_label(r"what you did not mean to say also leaks: \ \textbf{time}, \ \textbf{power}, \ the "
                          r"\textbf{cache}, \ even \textbf{sound}", 5.6, font_size=20, color=HEAD),
            wrapped_label(r"a check that quits early reveals how much of a guess was right \ (Kocher, 1996)", 5.6,
                          font_size=20, color=NO),
            wrapped_label(r"the fix: \ code whose time and memory use do not depend on secrets \ --- \ "
                          r"\textit{constant time}", 5.6, font_size=20, color=YES),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.3).move_to([3.3, 0.0, 0])
        with self.voiceover(
            "Rowhammer and Spectre are two cases of a wider truth, the one Parts 8 and 29 kept meeting. "
            "<bookmark mark='a'/> A computation says more than its output. It leaks through how long it takes, how "
            "much power it draws, what it leaves in the cache, even the sound the capacitors make. "
            "<bookmark mark='b'/> The classic example is a comparison that stops at the first wrong byte. The more "
            "of a guess is right, the longer it runs, so the time quietly tells the attacker how close they are, and "
            "they recover a secret one byte at a time. Paul Kocher showed in 1996 that timing alone breaks real "
            "cryptography. <bookmark mark='c'/> The defence is to write code whose running time and memory use do "
            "not depend on the secret at all, so the line is flat. It is called constant-time code, and it is as "
            "much a discipline as a technique."
        ) as vo:
            self.play(FadeIn(head), Create(ax), FadeIn(xl), FadeIn(yl), FadeIn(ill))
            vo.wait_until("a")
            self.play(FadeIn(notes[0]))
            vo.wait_until("b")
            self.play(Create(early), FadeIn(el), FadeIn(notes[1]))
            vo.wait_until("c")
            self.play(Create(const), FadeIn(cl), FadeIn(notes[2]))
        self.wait(0.4)
        self.clear_scene()

    def lesson(self):
        head = label(r"The abstraction leaked", font_size=36).to_edge(UP, buff=0.3)
        promise = VGroup(
            label(r"the promise", font_size=24, color=YES),
            wrapped_label(r"``memory holds what you wrote''; \ ``rolled-back work leaves no trace''; \ ``the answer "
                          r"is all you learn''", 5.8, font_size=19, color=GREY_A)).arrange(DOWN, buff=0.2)
        leak = VGroup(
            label(r"the leak", font_size=24, color=NO),
            wrapped_label(r"the physics underneath \ --- \ charge, \ timing, \ shared state \ --- \ shows through "
                          r"the layer above", 5.8, font_size=19, color=GREY_A)).arrange(DOWN, buff=0.2)
        VGroup(promise, leak).arrange(RIGHT, buff=0.9).next_to(head, DOWN, buff=0.6)
        foot = VGroup(
            wrapped_label(r"mitigations are not free: \ a speculation barrier or an extra refresh costs real "
                          r"performance \ --- \ the roofline of Part 9 moves", 12.6, font_size=21, color=HEAD),
            wrapped_label(r"the modern answer: \ a \textbf{hardware--software contract} that says exactly what the "
                          r"layer below promises not to leak", 12.6, font_size=21, color=WHITE),
        ).arrange(DOWN, buff=0.3).next_to(VGroup(promise, leak), DOWN, buff=1.0)
        with self.voiceover(
            "Step back, because these share one shape, and it is the thread of the whole series. "
            "<bookmark mark='a'/> Every layer makes a promise so the layer above need not look down. Memory holds "
            "what you wrote. Rolled-back work leaves no trace. The answer is all you learn. "
            "<bookmark mark='b'/> A side channel is the physics underneath, the charge, the timing, the shared cache, "
            "showing through the promise. <bookmark mark='c'/> And the fixes are never free: a speculation barrier or "
            "a faster refresh costs real performance, so the roofline of Part 9 moves the wrong way. "
            "<bookmark mark='d'/> The direction the field has taken is to stop pretending, and to write down a "
            "contract between hardware and software that states exactly what the layer below promises not to leak, "
            "so the layer above can finally rely on it."
        ) as vo:
            self.play(FadeIn(head))
            vo.wait_until("a")
            self.play(FadeIn(promise))
            vo.wait_until("b")
            self.play(FadeIn(leak))
            vo.wait_until("c")
            self.play(FadeIn(foot[0]))
            vo.wait_until("d")
            self.play(FadeIn(foot[1]))
        self.wait(0.4)
        self.clear_scene()


_ = (BG, DATA, HEAD, KERN, LAM, NO, YES, PART, mono)

from __future__ import annotations

import math

from explainer.cs import *  # noqa: F403
from videos.cs.cs37.common import (ACKC, DATA, HEAD, KERN, LAM, NO, PART, SEG, WIN, YES, axes, grid_table, load,
                                   trace)


def stream(n=16, cell=0.55, acked=0, sent=0, base=0, window=0, font=17, lost=()):
    g = VGroup()
    for i in range(n):
        if i < acked:
            c, op = ACKC, 0.35
        elif i < sent:
            c, op = SEG, 0.35
        else:
            c, op = GREY_D, 0.0
        if i in lost:
            c, op = NO, 0.35
        sq = VGroup(Square(cell, stroke_color=c, stroke_width=1.6, fill_color=c, fill_opacity=op),
                    label(str(i), font_size=font, color=c if op else GREY_B))
        g.add(sq)
    g.arrange(RIGHT, buff=0.04)
    return g


def window_frame(st, base, w, color=WIN):
    cells = st[base:base + w]
    r = SurroundingRectangle(VGroup(*cells), color=color, buff=0.06, stroke_width=3.5, corner_radius=0.05)
    return r


class Windows(VoiceoverScene):
    def construct(self):
        self.card()
        self.sliding()
        self.gbn_sr()
        self.measured()
        self.sequence_space()

    def card(self):
        card = chapter_card(3, r"Sliding windows", r"How many packets may be unacknowledged at once?",
                            lit=(1974, 1981), extra=((1974, r"Cerf and Kahn: \ windows"),
                                                     (1978, r"Go-Back-N in HDLC")), part=PART)
        with self.voiceover("Chapter three. Sliding windows."):
            self.play(FadeIn(card[0], shift=UP * 0.2), FadeIn(card[1]), FadeIn(card[2]))
        self.play(FadeOut(card))

    def sliding(self):
        head = label(r"A window over the stream", font_size=36).to_edge(UP, buff=0.3)
        st = stream(16, acked=0, sent=6).move_to([0, 1.2, 0])
        fr = window_frame(st, 0, 6)
        wl = label(r"window $W = 6$: \ sent, \ not yet acknowledged", font_size=20, color=WIN).next_to(fr, UP,
                                                                                                    buff=0.15)
        st2 = stream(16, acked=3, sent=9).move_to([0, -0.6, 0])
        fr2 = window_frame(st2, 3, 6)
        l2 = label(r"ACKs for 0, 1, 2 arrive: \ the window slides, \ 6, 7, 8 go out", font_size=20,
                   color=GREY_A).next_to(st2, DOWN, buff=0.2)
        eq = MathTex(r"U = \min\Big(1,\ \frac{W \cdot L/R}{\text{RTT} + L/R}\Big)", font_size=40,
                     color=HEAD).to_edge(DOWN, buff=1.0)
        eql = label(r"to fill the pipe, \ $W$ must reach the bandwidth--delay product \ (Part 36): \ "
                    r"1 Gb/s $\times$ 108 ms = 9{,}000 packets", font_size=21, color=YES).to_edge(DOWN, buff=0.35)
        with self.voiceover(
            "Instead of one packet at a time, allow W packets to be sent and not yet acknowledged: a window over the "
            "stream. <bookmark mark='a'/> The sender sends the first six and waits. As ACKs come back for zero, one "
            "and two, the window slides forward, and six, seven and eight go out. A steady stream of ACKs clocks out "
            "a steady stream of packets. <bookmark mark='b'/> In a round trip the sender now transmits W packets "
            "instead of one, so the utilization is W times larger, until it reaches one. <bookmark mark='c'/> To "
            "fill the pipe, the window must cover a whole round trip of sending: the bandwidth-delay product of the "
            "last part. Across the Atlantic at a gigabit a second, that is nine thousand packets in flight."
        ) as vo:
            self.play(FadeIn(head), FadeIn(st))
            vo.wait_until("a")
            self.play(Create(fr), FadeIn(wl))
            self.play(TransformFromCopy(st, st2), TransformFromCopy(fr, fr2))
            self.play(FadeIn(l2))
            vo.wait_until("b")
            self.play(Write(eq))
            vo.wait_until("c")
            self.play(FadeIn(eql))
        self.wait(0.4)
        self.clear_scene()

    def gbn_sr(self):
        head = label(r"When one is lost", font_size=36).to_edge(UP, buff=0.3)
        g1 = label(r"\textbf{Go-Back-N}", font_size=24, color=KERN).move_to([-4.6, 2.0, 0])
        st = stream(14, acked=2, sent=8, lost=(2,)).scale(0.9).next_to(g1, DOWN, buff=0.3).set_x(0)
        gl = wrapped_label(r"the receiver keeps only in-order data and ACKs ``everything up to 1'', \ again and "
                           r"again; \ on timeout the sender resends \textbf{2 through 7}", 12.2, font_size=20,
                           color=GREY_A).next_to(st, DOWN, buff=0.2)
        g2 = label(r"\textbf{Selective Repeat}", font_size=24, color=LAM).move_to([-4.2, -0.6, 0])
        st2 = stream(14, acked=2, sent=8, lost=(2,)).scale(0.9).next_to(g2, DOWN, buff=0.3).set_x(0)
        for i in range(3, 8):
            st2[i][0].set_stroke(ACKC).set_fill(ACKC, 0.35)
        sl = wrapped_label(r"the receiver buffers 3 to 7 and ACKs each one; \ the sender resends \textbf{only 2}, "
                           r"\ then 2 to 7 are delivered together", 12.2, font_size=20, color=GREY_A).next_to(
            st2, DOWN, buff=0.2)
        with self.voiceover(
            "With many packets in flight, what happens when one is lost? There are two classic answers. "
            "<bookmark mark='a'/> Go-Back-N keeps the receiver simple. It accepts only the next packet in order and "
            "discards anything after a gap, acknowledging, again and again, everything up to the last good packet. "
            "When the sender's timer expires, it goes back and resends the lost packet and every packet after it. "
            "<bookmark mark='b'/> Selective Repeat makes the receiver work harder. It buffers packets that arrive "
            "after a gap, and acknowledges each one individually. The sender resends only the packet that was "
            "lost, and when it arrives, the receiver delivers the whole run at once. TCP began close to Go-Back-N "
            "and has moved, with selective acknowledgements, to Selective Repeat."
        ) as vo:
            self.play(FadeIn(head))
            vo.wait_until("a")
            self.play(FadeIn(g1), FadeIn(st), FadeIn(gl))
            vo.wait_until("b")
            self.play(FadeIn(g2), FadeIn(st2), FadeIn(sl))
        self.wait(0.4)
        self.clear_scene()

    def measured(self):
        w = load("windows")
        head = label(r"Utilization against window", font_size=36).to_edge(UP, buff=0.3)
        g = axes([0, 7, 1], [0, 1.05, 0.25], x_length=7.2, y_length=4.2, x_label=r"window $W$ \ (packets)",
                 y_label=r"utilization", xticks=range(0, 8), yticks=(0.25, 0.5, 0.75, 1.0),
                 fx=lambda v: f"{2 ** int(v)}", fy=lambda v: f"{v:.2f}").move_to([-2.4, -0.5, 0])
        ax = g.ax
        rows = w["rows"]
        X = [math.log2(r["W"]) for r in rows]
        f = trace(ax, [(x, r["formula"]) for x, r in zip(X, rows)], GREY_B, width=2)
        series = {}
        for key, c in (("go-back-n_0.0", WHITE), ("go-back-n_0.02", KERN), ("selective-repeat_0.02", LAM)):
            series[key] = VGroup(trace(ax, [(x, r[key]) for x, r in zip(X, rows)], c, width=3),
                                 *[Dot(ax.c2p(x, r[key]), radius=0.05, color=c) for x, r in zip(X, rows)])
        leg = VGroup(
            label(r"formula, \ no loss", font_size=19, color=GREY_B),
            label(r"either protocol, \ no loss", font_size=19, color=WHITE),
            label(r"Go-Back-N, \ 2\% loss", font_size=19, color=KERN),
            label(r"Selective Repeat, \ 2\% loss", font_size=19, color=LAM),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.15).move_to([4.3, 1.4, 0])
        last = rows[-1]
        notes = VGroup(
            wrapped_label(rf"at $W = 128$ with 2\% loss: \ Go-Back-N sends {last['go-back-n_0.02_retx']:,} "
                          rf"retransmissions for 2{{,}}000 packets, \ Selective Repeat "
                          rf"{last['selective-repeat_0.02_retx']}", 4.9, font_size=19, color=WHITE),
            wrapped_label(r"both stall waiting out a whole timeout for each loss: \ the reason TCP added "
                          r"\textbf{fast retransmit}", 4.9, font_size=19, color=YES),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.25).move_to([4.3, -1.5, 0])
        with self.voiceover(
            "We measured both, on a channel with a hundred-millisecond round trip and a thousand packets a second. "
            "<bookmark mark='a'/> With no loss, both follow the formula exactly: utilization doubles with the "
            "window, until a hundred and twenty-eight packets fill the pipe. <bookmark mark='b'/> With two percent "
            "loss, Go-Back-N falls apart as the window grows. Every loss throws away a window's worth of good "
            "packets: at a window of a hundred and twenty-eight it sends nearly five thousand retransmissions for "
            "two thousand packets. <bookmark mark='c'/> Selective Repeat resends only what was lost, eighty-eight "
            "packets, and does three times better. But both still stall for a whole timeout after each loss, "
            "waiting to be sure. TCP's answer, fast retransmit, will be to treat a few later ACKs as evidence of a "
            "loss, without waiting for the timer."
        ) as vo:
            self.play(FadeIn(head), FadeIn(g), Create(f), FadeIn(leg[0]))
            vo.wait_until("a")
            self.play(Create(series["go-back-n_0.0"]), FadeIn(leg[1]))
            vo.wait_until("b")
            self.play(Create(series["go-back-n_0.02"]), FadeIn(leg[2]), FadeIn(notes[0]))
            vo.wait_until("c")
            self.play(Create(series["selective-repeat_0.02"]), FadeIn(leg[3]), FadeIn(notes[1]))
        self.wait(0.4)
        self.clear_scene()

    def sequence_space(self):
        w = load("windows")
        head = label(r"How many sequence numbers?", font_size=36).to_edge(UP, buff=0.3)
        thm = VGroup(
            label(r"\textbf{Theorem.} \ With sequence numbers taken mod $S$:", font_size=23, color=HEAD),
            label(r"Go-Back-N is correct iff $W \le S - 1$; \ \ Selective Repeat iff $W \le S/2$.", font_size=23,
                  color=HEAD),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.12).next_to(head, DOWN, buff=0.35)
        proof = VGroup(
            wrapped_label(r"\textit{Why $S/2$.} \ Suppose the receiver has just accepted $0, \dots, W-1$ and slid "
                          r"its window to $W, \dots, 2W - 1$, \ but every ACK was lost.", 12.4, font_size=20,
                          color=WHITE),
            wrapped_label(r"The sender times out and resends packet 0. \ If $2W > S$, \ the number $0$ is also "
                          r"$S$, \ which lies in the receiver's new window: \ the old packet is accepted as new.",
                          12.4, font_size=20, color=NO),
            wrapped_label(r"If $2W \le S$, \ the sender's possible numbers \ ($0 \dots W-1$, \ resent) \ and the "
                          r"receiver's \ ($W \dots 2W-1$) \ never overlap mod $S$, \ so every packet is "
                          r"classified correctly. \ Go-Back-N's receiver has a window of one, \ which gives $W + 1 "
                          r"\le S$.", 12.4, font_size=20, color=YES),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.2).next_to(thm, DOWN, buff=0.35)
        rows = [[r"Go-Back-N" if e["protocol"] == "go-back-n" else r"Selective Repeat", f"{e['W']}",
                 f"{e['space']}", f"{e['correct']} of {e['trials']}"] for e in w["edge"]]
        tab = grid_table([r"protocol", r"$W$", r"$S$", r"runs correct"], rows, widths=[3.0, 1.0, 1.0, 2.0],
                         row_h=0.38, font_size=19, mono_cols=())
        tab.next_to(proof, DOWN, buff=0.55).set_x(0)
        for k, e in enumerate(w["edge"], start=1):
            tab.cells[k][3].set_color(YES if e["correct"] == e["trials"] else NO)
        with self.voiceover(
            "With a window, how many sequence numbers are enough? With numbers taken modulo S, Go-Back-N is correct "
            "exactly when the window is at most S minus one, and Selective Repeat exactly when it is at most half "
            "of S. <bookmark mark='a'/> Here is why half. Suppose the receiver has just accepted packets zero to W "
            "minus one, and moved its window on to W through two W minus one, but every one of its ACKs was lost. "
            "<bookmark mark='b'/> The sender, hearing nothing, resends packet zero. If two W is more than S, the "
            "number zero is the same as S, which is inside the receiver's new window, and the receiver accepts an "
            "old packet as new data. <bookmark mark='c'/> If two W is at most S, what the sender might send and what "
            "the receiver might expect never share a number, so nothing is misclassified. Go-Back-N's receiver "
            "expects only one packet, which gives W plus one at most S. <bookmark mark='d'/> We tested the edges "
            "with three-bit numbers, S equal to eight, ten runs each. Go-Back-N with seven: always correct; with "
            "eight: never. Selective Repeat with four: always; with five: never. The bound is exact."
        ) as vo:
            self.play(FadeIn(head), FadeIn(thm))
            vo.wait_until("a")
            self.play(FadeIn(proof[0]))
            vo.wait_until("b")
            self.play(FadeIn(proof[1]))
            vo.wait_until("c")
            self.play(FadeIn(proof[2]))
            vo.wait_until("d")
            self.play(FadeIn(tab))
        self.wait(0.4)
        self.clear_scene()


_ = (DATA, YES)

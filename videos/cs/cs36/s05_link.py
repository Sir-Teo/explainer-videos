from __future__ import annotations

from explainer.cs import *  # noqa: F403
from videos.cs.cs36.common import (CODE, DATA, ETH, HEAD, IPC, KERN, NO, PART, PAY, YES, grid_table, header_strip,
                                   load, mono, num)


def bits_row(bits, highlight=(), color=WHITE, hl=NO, size=22):
    g = VGroup(*[Text(str(b), font="DejaVu Sans Mono", font_size=size, color=hl if i in highlight else color)
                 for i, b in enumerate(bits)]).arrange(RIGHT, buff=0.06)
    return g


class Link(VoiceoverScene):
    def construct(self):
        self.card()
        self.framing()
        self.coding()
        self.crc()
        self.ethernet()

    def card(self):
        card = chapter_card(4, r"Frames", r"Where does a frame begin, \ and is it intact?", lit=(1961, 1973),
                            extra=((1961, r"Peterson: \ cyclic codes for error detection"), (1973, r"Metcalfe: \ Ethernet")),
                            part=PART)
        with self.voiceover("Chapter four. Frames."):
            self.play(FadeIn(card[0], shift=UP * 0.2), FadeIn(card[1]), FadeIn(card[2]))
        self.play(FadeOut(card))

    def framing(self):
        lk = load("link")
        head = label(r"Finding the edges: \ bit stuffing", font_size=36).to_edge(UP, buff=0.3)
        flag = bits_row([0, 1, 1, 1, 1, 1, 1, 0], color=KERN)
        fl = label(r"the flag, \ \texttt{01111110}, \ marks each end of a frame", font_size=20, color=KERN)
        VGroup(fl, flag).arrange(RIGHT, buff=0.5).next_to(head, DOWN, buff=0.5)
        data = bits_row(lk["data"])
        dl = label(r"data:", font_size=20, color=GREY_A)
        st = lk["stuffed"]
        ins, run, idx = [], 0, 0
        for b in lk["data"]:
            idx += 1
            run = run + 1 if b else 0
            if run == 5:
                ins.append(idx)
                idx += 1
                run = 0
        stuffed = bits_row(st, highlight=set(ins), color=WHITE, hl=YES)
        sl = label(r"sent:", font_size=20, color=GREY_A)
        rows = VGroup(VGroup(dl, data).arrange(RIGHT, buff=0.3), VGroup(sl, stuffed).arrange(RIGHT, buff=0.3))
        rows.arrange(DOWN, aligned_edge=LEFT, buff=0.35).next_to(flag, DOWN, buff=0.7).set_x(0)
        lines = VGroup(
            label(r"the sender inserts a 0 \ (green) \ after every five 1s in a row; \ the receiver deletes it",
                  font_size=21, color=WHITE),
            label(r"so six 1s in a row can only be a flag: \ any data can be carried \ (HDLC, \ 1979)", font_size=21,
                  color=YES),
            label(r"Ethernet instead sends a fixed preamble, \ and the signal falls silent between frames",
                  font_size=21, color=GREY_A),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.2).to_edge(DOWN, buff=0.6)
        with self.voiceover(
            "A link carries a stream of bits. The first problem is to know where each frame begins and ends. "
            "<bookmark mark='a'/> One answer marks each end with a special pattern, a flag: zero, six ones, zero. "
            "<bookmark mark='b'/> But data can contain that pattern too. So the sender, whenever it has sent five "
            "ones in a row, inserts a zero, and the receiver, seeing five ones and a zero, removes it. "
            "<bookmark mark='c'/> Now six ones in a row can never appear inside a frame, and the flag is unambiguous, "
            "whatever the data. This is bit stuffing, from the HDLC family of protocols. <bookmark mark='d'/> "
            "Ethernet does it differently: a fixed preamble before each frame, and silence between them."
        ) as vo:
            self.play(FadeIn(head))
            vo.wait_until("a")
            self.play(FadeIn(flag), FadeIn(fl))
            vo.wait_until("b")
            self.play(FadeIn(rows[0]))
            self.play(FadeIn(rows[1]), FadeIn(lines[0]))
            vo.wait_until("c")
            self.play(FadeIn(lines[1]))
            vo.wait_until("d")
            self.play(FadeIn(lines[2]))
        self.wait(0.3)
        self.clear_scene()

    def coding(self):
        head = label(r"Keeping the clocks together", font_size=36).to_edge(UP, buff=0.3)
        bits = [1, 0, 1, 1, 0, 0, 0, 0, 1]
        W = 0.55
        nrz = VMobject(color=HEAD, stroke_width=3)
        pts = []
        for i, b in enumerate(bits):
            y = 0.35 if b else -0.35
            pts += [[-4.6 + i * W, y, 0], [-4.6 + (i + 1) * W, y, 0]]
        nrz.set_points_as_corners(pts).shift(UP * 1.5)
        man = VMobject(color=YES, stroke_width=3)
        pts = []
        for i, b in enumerate(bits):
            a, c = (-0.35, 0.35) if b else (0.35, -0.35)
            x = -4.6 + i * W
            pts += [[x, a, 0], [x + W / 2, a, 0], [x + W / 2, c, 0], [x + W, c, 0]]
        man.set_points_as_corners(pts).shift(DOWN * 0.1)
        bl = VGroup(*[Text(str(b), font="DejaVu Sans Mono", font_size=16, color=GREY_B).move_to([-4.6 + (i + 0.5) * W, 2.3, 0])
                      for i, b in enumerate(bits)])
        nl = label(r"plain levels: \ a run of zeros is a flat line, \ and the receiver's clock drifts", font_size=18,
                   color=HEAD).next_to(nrz, DOWN, buff=0.12).align_to(nrz, LEFT)
        ml = label(r"Manchester: \ a transition in every bit, \ at twice the signalling rate", font_size=18,
                   color=YES).next_to(man, DOWN, buff=0.12).align_to(man, LEFT)
        rows = [["Manchester", "10 Mb/s Ethernet", "1 bit in 2 symbols", "50\\%"],
                ["4B/5B", "100 Mb/s Ethernet", "4 bits in 5", "80\\%"],
                ["8b/10b", "1 Gb/s Ethernet, \\ USB 3", "8 bits in 10", "80\\%"],
                ["64b/66b", "10--400 Gb/s Ethernet", "64 bits in 66", "97\\%"]]
        tab = grid_table([r"line code", r"used in", r"rule", r"efficiency"], rows, widths=[1.8, 3.0, 2.4, 1.6], row_h=0.42,
                         font_size=17, mono_cols=())
        tab.move_to([3.4, 0.9, 0])
        for r in range(1, 5):
            tab.cells[r][3].set_color(YES)
        lines = VGroup(
            label(r"the receiver recovers the sender's clock from the edges of the signal: \ long runs without "
                  r"edges lose it", font_size=20, color=WHITE),
            label(r"line codes guarantee edges; \ later ones also scramble the bits, \ and spend only 2 bits in 66",
                  font_size=20, color=YES),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.16).to_edge(DOWN, buff=0.45)
        with self.voiceover(
            "Below framing there is a quieter problem: the receiver must sample each bit at the right moment, and "
            "it has no wire carrying the sender's clock. <bookmark mark='a'/> It recovers the clock from the "
            "signal's edges. Sent as plain levels, a long run of zeros is a flat line, and the receiver's clock "
            "drifts until it miscounts the bits. <bookmark mark='b'/> The first Ethernet used Manchester coding: "
            "every bit is a transition, up for a one, down for a zero, so edges never stop, at the cost of signalling "
            "twice as fast. <bookmark mark='c'/> Faster Ethernets use cheaper codes: four bits in five symbols, eight "
            "in ten, and at ten gigabits and above, sixty-four bits in sixty-six, with the bits scrambled so long "
            "runs are vanishingly rare. Ninety-seven percent of the line carries data."
        ) as vo:
            self.play(FadeIn(head), FadeIn(bl))
            vo.wait_until("a")
            self.play(Create(nrz), FadeIn(nl), FadeIn(lines[0]))
            vo.wait_until("b")
            self.play(Create(man), FadeIn(ml))
            vo.wait_until("c")
            self.play(FadeIn(tab), FadeIn(lines[1]))
        self.wait(0.3)
        self.clear_scene()

    def crc(self):
        lk = load("link")
        head = label(r"Is it intact? \ CRC-32", font_size=36).to_edge(UP, buff=0.3)
        eq = MathTex(r"\text{frame}(x)\cdot x^{32} \bmod g(x) = \text{FCS}", font_size=34, color=HEAD)
        eq.next_to(head, DOWN, buff=0.45)
        gl = label(r"$g(x) = x^{32} + x^{26} + x^{23} + \dots + x + 1$: \ the polynomial of Ethernet, \ zip and PNG "
                   r"\ (Part 28)", font_size=19, color=GREY_A).next_to(eq, DOWN, buff=0.2)
        names = {"single": r"one bit flipped", "double": r"two bits flipped", "burst": r"a burst of up to 32 bits",
                 "random": r"the frame replaced by noise"}
        rows = [[names[t["kind"]], num(t["frames"]), num(t["missed"])] for t in lk["trials"]]
        tab = grid_table([r"corruption", r"frames", r"undetected"], rows, widths=[5.0, 2.0, 2.2], row_h=0.44,
                         font_size=20, mono_cols=())
        tab.next_to(gl, DOWN, buff=0.5).set_x(0)
        for r in range(1, 5):
            tab.cells[r][2].set_color(YES)
        lines = VGroup(
            label(r"guaranteed: \ every burst up to 32 bits, \ and any 1, \ 2 or 3 flipped bits in a frame of "
                  r"Ethernet's size", font_size=20, color=YES),
            label(r"random garbage passes with probability $2^{-32}$: \ one in four billion", font_size=20,
                  color=HEAD),
            label(r"a CRC \textit{detects}; \ the frame is dropped, \ and someone higher up must resend it", font_size=20,
                  color=NO),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.16).to_edge(DOWN, buff=0.4)
        with self.voiceover(
            "The second problem is noise. <bookmark mark='a'/> Each Ethernet frame ends with a frame check sequence: "
            "the remainder when the frame, read as a polynomial over two elements, is divided by a fixed polynomial of "
            "degree thirty-two. This is the cyclic redundancy check of Part 28, the same one zip files and PNG images "
            "use. <bookmark mark='b'/> We corrupted a hundred thousand frames four ways. Single flipped bits, pairs, "
            "bursts up to thirty-two bits long: every one detected, as the algebra guarantees. Even frames replaced by "
            "pure noise: none slipped through. <bookmark mark='c'/> Random garbage passes only once in four billion "
            "tries. <bookmark mark='d'/> But a CRC only detects. A damaged frame is thrown away, and whether it is "
            "ever sent again is another layer's business."
        ) as vo:
            self.play(FadeIn(head))
            vo.wait_until("a")
            self.play(FadeIn(eq), FadeIn(gl))
            vo.wait_until("b")
            self.play(FadeIn(tab), FadeIn(lines[0]))
            vo.wait_until("c")
            self.play(FadeIn(lines[1]))
            vo.wait_until("d")
            self.play(FadeIn(lines[2]))
        self.wait(0.3)
        self.clear_scene()

    def ethernet(self):
        lk = load("link")
        head = label(r"An Ethernet frame", font_size=36).to_edge(UP, buff=0.3)
        strip = header_strip([("destination", 6, ETH), ("source", 6, ETH), ("type", 2, ETH), ("payload, 46--1500", 46, PAY),
                              ("FCS", 4, ETH)], unit=0.17, min_w=1.2, font=17)
        strip.next_to(head, DOWN, buff=0.6)
        fr = lk["frame"]
        b = [fr[i:i + 2] for i in range(0, len(fr), 2)]
        dump = VGroup(mono(" ".join(b[:6]) + "   " + " ".join(b[6:12]) + "   " + " ".join(b[12:14]), 18, ETH),
                      mono(" ".join(b[14:30]), 18, IPC), mono(" ".join(b[30:46]), 18, IPC),
                      mono(" ".join(b[46:60]) + "   " + " ".join(b[60:]), 18, PAY)).arrange(DOWN, aligned_edge=LEFT,
                                                                                         buff=0.08)
        dump.next_to(strip, DOWN, buff=0.5)
        lines = VGroup(
            label(r"a \textbf{MAC address}: \ 48 bits, \ burned into the interface; \ the first 24 name its maker",
                  font_size=20, color=ETH),
            label(r"\texttt{ff:ff:ff:ff:ff:ff} is broadcast: \ every station on the segment listens", font_size=20,
                  color=WHITE),
            label(r"\texttt{type} \texttt{0x0800} says the payload is IPv4: \ the layer above, \ named in the layer "
                  r"below", font_size=20, color=IPC),
            label(r"minimum 64 bytes, \ for a reason in the next chapter; \ maximum 1{,}518", font_size=20,
                  color=KERN),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.18).to_edge(DOWN, buff=0.4)
        with self.voiceover(
            "Here is an Ethernet frame, field by field, with our bytes. <bookmark mark='a'/> Six bytes of destination "
            "address and six of source. These are MAC addresses: forty-eight bits, fixed in each network interface "
            "when it is made, the first half naming the manufacturer. <bookmark mark='b'/> An address of all ones "
            "is broadcast: every machine on the cable takes the frame. <bookmark mark='c'/> Two bytes of type say "
            "what the payload is, here IPv4, so the receiving machine knows which layer to hand it to. "
            "<bookmark mark='d'/> Then the payload, and the CRC. A frame is never shorter than sixty-four bytes, and "
            "the reason is the subject of the next chapter."
        ) as vo:
            self.play(FadeIn(head), FadeIn(strip))
            vo.wait_until("a")
            self.play(FadeIn(dump), FadeIn(lines[0]))
            for mk, ln in zip("bcd", lines[1:]):
                vo.wait_until(mk)
                self.play(FadeIn(ln))
        self.wait(0.3)
        self.clear_scene()


_ = (CODE, DATA, HEAD)

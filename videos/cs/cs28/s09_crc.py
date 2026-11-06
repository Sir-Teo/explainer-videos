from __future__ import annotations

from explainer.cs import *  # noqa: F403
from videos.cs.cs28.common import (BG, CTRL, DATA, HEAD, LAM, NO, PART, YES, fit_right, grid_table, load, mono)


def long_division(bits, poly):
    """Rows of the GF(2) long division: (shift, current register as a string) at each XOR."""
    r = len(poly) - 1
    reg = list(bits) + [0] * r
    steps = []
    for i in range(len(bits)):
        if reg[i]:
            steps.append((i, "".join(map(str, reg))))
            for j, pb in enumerate(poly):
                reg[i + j] ^= pb
    return steps, "".join(map(str, reg[-r:]))


def bitline(text, color, x0, y, pitch=0.27, size=24):
    """Characters at a fixed pitch (spaces leave gaps), so columns line up."""
    return VGroup(*[mono(ch, size, color).move_to([x0 + pitch * i, y, 0]) for i, ch in enumerate(text) if ch != " "])


class Crc(VoiceoverScene):
    def construct(self):
        self.card()
        self.division()
        self.circuit()
        self.guarantees()

    def card(self):
        card = chapter_card(8, r"Cyclic codes and CRCs", r"How does a network notice a damaged packet?",
                            lit=(1961, 1975), extra=((1961, r"Peterson and Brown: \ CRC"), (1975, r"CRC-32")),
                            part=PART)
        with self.voiceover("Chapter eight. Cyclic codes and CRCs."):
            self.play(FadeIn(card[0], shift=UP * 0.2), FadeIn(card[1]), FadeIn(card[2]))
        self.play(FadeOut(card))

    def division(self):
        head = label(r"A checksum by polynomial division", font_size=34).to_edge(UP, buff=0.3)
        msg = [1, 1, 0, 1, 0, 0, 1, 1, 1, 0, 1, 1, 0, 0]
        poly = [1, 0, 1, 1]
        steps, rem = long_division(msg, poly)
        rows = VGroup()
        x0, y = -6.2, 2.1
        rows.add(bitline("".join(map(str, msg)) + "000", WHITE, x0, y))
        reg = list(msg) + [0, 0, 0]
        for i, _ in steps[:5]:
            y -= 0.36
            rows.add(bitline(" " * i + "1011", HEAD, x0, y))
            for j, pb in enumerate(poly):
                reg[i + j] ^= pb
            y -= 0.36
            rows.add(bitline("".join(str(b) if k >= i + 1 else " " for k, b in enumerate(reg)), GREY_B, x0, y))
        rem_l = label(rf"remainder after all {len(steps)} steps: \ \texttt{{{rem}}}", font_size=22,
                      color=YES).next_to(rows, DOWN, buff=0.3).align_to(rows, LEFT)
        lines = VGroup(
            label(r"bits are coefficients of a polynomial over GF(2): \\ \texttt{1011} $= x^3 + x + 1$", font_size=21,
                  color=WHITE),
            label(r"append $r$ zeros, \ divide by the generator $g(x)$ \\ (subtraction is XOR: \ no borrows)",
                  font_size=21, color=HEAD),
            label(r"send the message with the remainder appended: \\ now the whole word is divisible by $g(x)$",
                  font_size=21, color=YES),
            label(r"the receiver divides again: \ remainder $\ne 0$ \\ means damage", font_size=21, color=NO),
            label(r"in hardware: \ a shift register with XOR taps \\ at the 1s of $g$: \ Part 5's LFSR, \ one bit per "
                  r"clock", font_size=21, color=LAM),
            label(r"CRC-32 \ (Ethernet, \ zip, \ PNG): \\ ours matches zlib's on every test string", font_size=21,
                  color=DATA),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.3).next_to(rows, RIGHT, buff=0.8).align_to(rows, UP)
        fit_right(lines)
        with self.voiceover(
            "Most of the time a network only needs to notice damage, and ask again. <bookmark mark='a'/> The cyclic "
            "redundancy check treats bits as the coefficients of a polynomial whose coefficients are zero or one. "
            "<bookmark mark='b'/> Append a few zeros to the message and divide by a fixed generator polynomial, "
            "here x cubed plus x plus one. Long division over this field is just exclusive or, with no borrows. "
            "<bookmark mark='c'/> Send the message followed by the remainder. Now the whole word is divisible by the "
            "generator. <bookmark mark='d'/> The receiver divides again; a nonzero remainder means something "
            "changed. <bookmark mark='e'/> In hardware this is a shift register with exclusive-or taps where the "
            "generator has ones, the linear-feedback shift register of Part 5, consuming a bit per clock. <bookmark "
            "mark='f'/> The thirty-two-bit version guards every Ethernet frame, zip file and PNG image. Ours agrees "
            "with zlib's on every test string."
        ) as vo:
            self.play(FadeIn(head), FadeIn(rows[0]))
            vo.wait_until("a")
            self.play(FadeIn(lines[0]))
            vo.wait_until("b")
            self.play(LaggedStart(*[FadeIn(r) for r in rows[1:]], lag_ratio=0.3), FadeIn(lines[1]), run_time=3.0)
            self.play(FadeIn(rem_l))
            for mk, ln in zip("cdef", lines[2:]):
                vo.wait_until(mk)
                self.play(FadeIn(ln, shift=UP * 0.1))
        self.wait(0.3)
        self.clear_scene()

    def circuit(self):
        head = label(r"The same division, \ in hardware", font_size=34).to_edge(UP, buff=0.3)
        msg = [1, 1, 0, 1, 0, 0, 1, 1, 1, 0, 1, 1, 0, 0]
        regs = VGroup(*[Square(side_length=0.8, color=DATA, stroke_width=3).set_fill(BG, 1) for _ in range(3)])
        regs.arrange(RIGHT, buff=1.1).move_to(UP * 0.4)
        names = VGroup(*[label(t, font_size=18, color=GREY_A).next_to(r, DOWN, buff=0.12)
                         for t, r in zip((r"$x^0$", r"$x^1$", r"$x^2$"), regs)])
        x0 = Circle(radius=0.2, color=HEAD, stroke_width=3).move_to(regs[0].get_left() + LEFT * 0.6)
        x1 = Circle(radius=0.2, color=HEAD, stroke_width=3).move_to((regs[0].get_right() + regs[1].get_left()) / 2)
        x2 = Circle(radius=0.2, color=HEAD, stroke_width=3).move_to(regs[2].get_right() + RIGHT * 0.9)
        plus = VGroup(*[MathTex(r"+", font_size=26, color=HEAD).move_to(c) for c in (x0, x1, x2)])
        wires = VGroup(
            Arrow(x0.get_right(), regs[0].get_left(), buff=0.02, color=GREY_B, stroke_width=2),
            Arrow(regs[0].get_right(), x1.get_left(), buff=0.02, color=GREY_B, stroke_width=2),
            Arrow(x1.get_right(), regs[1].get_left(), buff=0.02, color=GREY_B, stroke_width=2),
            Arrow(regs[1].get_right(), regs[2].get_left(), buff=0.02, color=GREY_B, stroke_width=2),
            Arrow(regs[2].get_right(), x2.get_left(), buff=0.02, color=GREY_B, stroke_width=2),
        )
        fb_y = regs.get_top()[1] + 0.9
        feed = VGroup(Line(x2.get_top(), [x2.get_x(), fb_y, 0], color=LAM, stroke_width=2.5),
                      Line([x2.get_x(), fb_y, 0], [x0.get_x(), fb_y, 0], color=LAM, stroke_width=2.5),
                      Arrow([x0.get_x(), fb_y, 0], x0.get_top(), buff=0.02, color=LAM, stroke_width=2.5),
                      Arrow([x1.get_x(), fb_y, 0], x1.get_top(), buff=0.02, color=LAM, stroke_width=2.5))
        inp = label(r"message in", font_size=18, color=WHITE).next_to(x2, DOWN, buff=0.5)
        inarrow = Arrow(inp.get_top(), x2.get_bottom(), buff=0.05, color=WHITE, stroke_width=2)
        R = [0, 0, 0]
        digits = VGroup(*[mono("0", 30, WHITE).move_to(r) for r in regs])
        stream = VGroup(*[mono(str(b), 22, GREY_B) for b in msg]).arrange(RIGHT, buff=0.14).move_to(DOWN * 1.35)
        sl = label(r"input, \ one bit per clock", font_size=18, color=GREY_A).next_to(stream, UP, buff=0.12)
        lines = VGroup(
            label(r"three flip-flops and two XOR gates, \ taps where $g(x) = x^3 + x + 1$ has its 1s", font_size=21,
                  color=WHITE),
            label(r"after the last bit the register, \ read from $x^2$ down to $x^0$, \ holds \texttt{100}: \ as on paper",
                  font_size=21, color=YES),
            label(r"real CRC-32 hardware handles 8 to 512 bits per clock \ with the same algebra, \ unrolled",
                  font_size=21, color=GREY_A),
        ).arrange(DOWN, buff=0.18).to_edge(DOWN, buff=0.25)
        with self.voiceover(
            "In hardware the division is a shift register. <bookmark mark='a'/> Three flip-flops hold the running "
            "remainder, and exclusive-or gates sit where the generator has a one. The bit leaving the top is fed "
            "back into those gates. <bookmark mark='b'/> Clock in the message one bit at a time. <bookmark "
            "mark='c'/> After the last bit the register holds the remainder, one zero zero, the same as the long "
            "division on paper. <bookmark mark='d'/> Real network chips unroll the same algebra to process dozens "
            "or hundreds of bits per clock."
        ) as vo:
            self.play(FadeIn(head), FadeIn(regs), FadeIn(names), FadeIn(VGroup(x0, x1, x2, plus)), FadeIn(wires),
                      FadeIn(digits))
            vo.wait_until("a")
            self.play(Create(feed), FadeIn(lines[0]))
            vo.wait_until("b")
            self.play(FadeIn(stream), FadeIn(sl), FadeIn(inp), GrowArrow(inarrow), FadeOut(lines[0]))
            for i, b in enumerate(msg):
                fb = R[2] ^ b
                R = [fb, R[0] ^ fb, R[1]]
                new = VGroup(*[mono(str(v), 30, YES if v else WHITE).move_to(r) for v, r in zip(R, regs)])
                self.play(stream[i].animate.set_color(HEAD), Transform(digits, new), run_time=0.35)
            vo.wait_until("c")
            self.play(FadeIn(lines[1]), Indicate(digits, color=YES))
            vo.wait_until("d")
            self.play(FadeIn(lines[2]))
        self.wait(0.3)
        self.clear_scene()

    def guarantees(self):
        c = load("crc")
        head = label(r"What a CRC catches, \ measured", font_size=34).to_edge(UP, buff=0.35)
        rows = [[rf"burst of length {b['burst']}", f"{b['undetected'] * 100:.2f}\\%"] for b in c["bursts"]]
        rows.append([r"random garbage", f"{c['random_undetected'] * 100:.2f}\\%"])
        tab = grid_table([r"error pattern \ (64-byte message)", r"undetected by CRC-8"], rows, widths=[5.0, 3.4],
                         row_h=0.42, font_size=21, mono_cols=(),
                         colors=[[WHITE, YES if b["undetected"] == 0 else NO] for b in c["bursts"]] + [[WHITE, NO]])
        tab.next_to(head, DOWN, buff=0.4).to_edge(LEFT, buff=0.8)
        tl = label(rf"{c['trials']:,} trials per row".replace(",", "{,}"), font_size=18,
                   color=GREY_A).next_to(tab, DOWN, buff=0.12)
        lines = VGroup(
            label(r"an error pattern $e(x)$ goes unnoticed \\ only if $g(x)$ divides it", font_size=21, color=WHITE),
            label(r"a burst no longer than $r$ = 8 bits is $x^i$ times \\ a polynomial of degree $< 8$: \ "
                  r"\textbf{never} divisible", font_size=21, color=YES),
            label(r"length 9: \ missed about 1 time in 128 \ $= 2^{-7}$; \\ longer or random: \ 1 in 256 \ $= 2^{-8}$",
                  font_size=21, color=NO),
            label(r"CRC-32 guarantees all bursts up to 32 bits, \\ and misses random damage once in 4 billion",
                  font_size=21, color=DATA),
            label(r"a CRC is \textbf{not} a cryptographic hash: \\ anyone can forge a match \ (Part 29)",
                  font_size=21, color=HEAD),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.3).next_to(tab, RIGHT, buff=0.7).align_to(tab, UP)
        fit_right(lines)
        with self.voiceover(
            "What does a CRC catch? <bookmark mark='a'/> The received word differs from the sent one by an error "
            "polynomial, and the damage goes unnoticed only if the generator divides it. <bookmark mark='b'/> A "
            "burst, a run of errors no longer than the number of check bits, is a power of x times a polynomial of "
            "smaller degree, and the generator can never divide that. Our eight-bit CRC caught every burst we tried "
            "of length up to eight, thirty thousand of each length. <bookmark mark='c'/> Bursts of length nine slip through about "
            "one time in a hundred and twenty-eight, and random garbage one time in two hundred and fifty-six, "
            "exactly as the algebra predicts. <bookmark mark='d'/> The thirty-two-bit CRC of Ethernet catches every "
            "burst up to thirty-two bits and misses random damage once in four billion. <bookmark mark='e'/> But it "
            "is not a cryptographic hash: anyone can change a message and fix up the CRC. Part 29 builds hashes that "
            "resist that."
        ) as vo:
            self.play(FadeIn(head), FadeIn(tab), FadeIn(tl))
            for mk, ln in zip("abcde", lines):
                vo.wait_until(mk)
                self.play(FadeIn(ln, shift=UP * 0.1))
        self.wait(0.3)
        self.clear_scene()

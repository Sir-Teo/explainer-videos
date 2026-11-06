from __future__ import annotations

from explainer.cs import *  # noqa: F403
from videos.cs.cs29.common import (BG, DATA, HEAD, NO, PART, YES, code, flow_box, load, mono)


class Prg(VoiceoverScene):
    def construct(self):
        self.card()
        self.definition()
        self.lfsr()
        self.chacha()

    def card(self):
        card = chapter_card(6, r"Pseudorandom generators", r"Can a short key look like a long one?",
                            lit=(1982, 1984, 2008), extra=((1982, r"Yao: \ the next-bit test"),
                                                           (1984, r"Blum--Micali"), (2008, r"ChaCha20")), part=PART)
        with self.voiceover("Chapter six. Pseudorandom generators."):
            self.play(FadeIn(card[0], shift=UP * 0.2), FadeIn(card[1]), FadeIn(card[2]))
        self.play(FadeOut(card))

    def definition(self):
        head = label(r"Stretching a key", font_size=34).to_edge(UP, buff=0.3)
        seed = Rectangle(width=1.0, height=0.4, stroke_width=0, fill_color=HEAD, fill_opacity=0.9)
        G = flow_box(r"$G$", YES, w=0.9, h=0.7, font=26)
        out = Rectangle(width=6.5, height=0.4, stroke_width=0, fill_color=DATA, fill_opacity=0.9)
        chain = VGroup(seed, G, out).arrange(RIGHT, buff=0.4).next_to(head, DOWN, buff=0.6)
        a1 = Arrow(seed.get_right(), G.get_left(), buff=0.05, stroke_width=2.5, color=GREY_B)
        a2 = Arrow(G.get_right(), out.get_left(), buff=0.05, stroke_width=2.5, color=GREY_B)
        sl = label(r"seed $s$: \ $n$ bits", font_size=18, color=HEAD).next_to(seed, DOWN, buff=0.12)
        ol = label(r"$G(s)$: \ $\ell(n) > n$ bits", font_size=18, color=DATA).next_to(out, DOWN, buff=0.12)
        D = flow_box(r"distinguisher $D$", NO, w=2.8, h=0.7, font=20).next_to(chain, DOWN, buff=1.0).shift(LEFT * 1.6)
        srcs = VGroup(label(r"$G(s)$, \ $s$ random", font_size=19, color=DATA),
                      label(r"truly random $r$", font_size=19, color=GREY_A)).arrange(DOWN, buff=0.25).next_to(
            D, LEFT, buff=0.7)
        ins = VGroup(*[Arrow(s_.get_right(), D.get_left(), buff=0.08, stroke_width=2, color=GREY_B) for s_ in srcs])
        res = label(r"$\bigl|\Pr[D(G(s)) = 1] - \Pr[D(r) = 1]\bigr|$ \ negligible", font_size=21, color=YES).next_to(
            D, RIGHT, buff=0.5)
        lines = VGroup(
            label(r"stream cipher: \ $c = m \oplus G(k)$: \ secure if $G$ is, \ by reduction: \ a distinguisher for "
                  r"$c$ is one for $G$", font_size=21, color=WHITE),
            label(r"Yao \ (1982): \ fooling every test $\iff$ no efficient predictor guesses the next bit from the "
                  r"earlier ones", font_size=21, color=DATA),
            label(r"Blum--Micali \ (1984), \ Goldreich--Levin \ (1989), \ H\aa stad et al.\ (1999): \ a PRG from "
                  r"\textbf{any} one-way function", font_size=21, color=HEAD),
        ).arrange(DOWN, buff=0.18).to_edge(DOWN, buff=0.35)
        with self.voiceover(
            "Shannon needs a key as long as the message. A pseudorandom generator makes a short key look long. "
            "<bookmark mark='a'/> It is an efficient function G that stretches a random seed of n bits into more "
            "bits. <bookmark mark='b'/> The requirement: no efficient test, given a string, can tell whether it came "
            "from G with a random seed, or was truly random, with more than negligible advantage. <bookmark "
            "mark='c'/> Then XOR the message with G of the key. If an attacker could learn anything about the message "
            "from this ciphertext, we could turn that attacker into a test that tells G's output from random. So the "
            "cipher is as secure as the generator. <bookmark mark='d'/> Andrew Yao showed in 1982 that passing every "
            "test is the same as one simple property: nobody can predict the next bit from the bits before it. "
            "<bookmark mark='e'/> And by 1999, pseudorandom generators had been built from any one-way function at "
            "all: any function easy to compute and hard to invert."
        ) as vo:
            self.play(FadeIn(head), FadeIn(seed), FadeIn(sl))
            vo.wait_until("a")
            self.play(GrowArrow(a1), FadeIn(G), GrowArrow(a2), GrowFromEdge(out, LEFT), FadeIn(ol))
            vo.wait_until("b")
            self.play(FadeIn(D), FadeIn(srcs), *[GrowArrow(a) for a in ins])
            self.play(FadeIn(res))
            vo.wait_until("c")
            self.play(FadeIn(lines[0]))
            vo.wait_until("d")
            self.play(FadeIn(lines[1]))
            vo.wait_until("e")
            self.play(FadeIn(lines[2]))
        self.wait(0.3)
        self.clear_scene()

    def lfsr(self):
        f = load("lfsr")
        head = label(r"Random-looking is not pseudorandom", font_size=34).to_edge(UP, buff=0.3)
        bits = f["first"]
        size = 0.33
        cells = VGroup()
        for i, b in enumerate(bits):
            sq = Square(side_length=size, stroke_color=GREY_C, stroke_width=1, fill_color=GREY_D if b else BG,
                        fill_opacity=1)
            sq.move_to([(i % 32) * (size + 0.04), -(i // 32) * (size + 0.12), 0])
            cells.add(VGroup(sq, mono(str(b), 15, WHITE).move_to(sq)))
        cells.center().next_to(head, DOWN, buff=0.6)
        used = VGroup(*[SurroundingRectangle(c, color=HEAD, buff=0.0, stroke_width=2.5) for c in cells[:f["bits_used"]]])
        pred = [c[0].copy().set_fill(YES, 0.55).set_stroke(YES, 1) for c in cells[f["bits_used"]:]]
        poly = MathTex(r"C(x) = 1 + x^{14} + x^{17}", font_size=34, color=HEAD).next_to(cells, DOWN, buff=0.4)
        lines = VGroup(
            label(rf"a 17-bit LFSR \ (Part 5): \ period $2^{{17}} - 1 = {f['period']:,}$, \ balanced, \ "
                  r"passes simple statistical tests".replace(",", "{,}"), font_size=21, color=WHITE),
            label(r"but it is \textbf{linear}: \ Berlekamp--Massey \ (Part 28) \ finds the shortest LFSR from twice "
                  r"its length in bits", font_size=21, color=HEAD),
            label(r"from 34 bits it recovers the taps, \ and predicts all 2{,}000 bits correctly", font_size=21,
                  color=YES),
            label(r"GSM's A5/1 combined three LFSRs nonlinearly: \ broken too \ (2003--2009)", font_size=21,
                  color=NO),
        ).arrange(DOWN, buff=0.17).to_edge(DOWN, buff=0.35)
        with self.voiceover(
            "Passing statistical tests is not enough; the definition says every efficient test. <bookmark "
            "mark='a'/> Here is the linear feedback shift register of Part 5: seventeen bits, with a feedback "
            "polynomial chosen so its period is the maximum, a hundred and thirty-one thousand bits. Its output is "
            "balanced and looks random. <bookmark mark='b'/> But every bit is a fixed XOR of earlier bits. Part 28's "
            "Berlekamp-Massey algorithm, run over the two-element field, finds the shortest register that produces "
            "any sequence, from twice its length. <bookmark mark='c'/> Given these thirty-four bits, it returns the "
            "feedback polynomial, and from there every later bit: all two thousand predicted, no errors. As a "
            "keystream, this is useless. <bookmark mark='d'/> Real designs add nonlinearity. GSM phones combined "
            "three registers with irregular clocking, and that was broken too, eventually in real time with "
            "precomputed tables."
        ) as vo:
            self.play(FadeIn(head), LaggedStart(*[FadeIn(c) for c in cells], lag_ratio=0.02), FadeIn(lines[0]),
                      run_time=2.0)
            vo.wait_until("b")
            self.play(Create(used), FadeIn(lines[1]))
            vo.wait_until("c")
            self.play(FadeIn(poly))
            self.play(LaggedStart(*[FadeIn(p) for p in pred], lag_ratio=0.03), FadeIn(lines[2]), run_time=2.0)
            vo.wait_until("d")
            self.play(FadeIn(lines[3]))
        self.wait(0.3)
        self.clear_scene()

    def chacha(self):
        c = load("chacha")
        head = label(r"ChaCha20: \ add, \ rotate, \ XOR", font_size=34).to_edge(UP, buff=0.3)
        names = [["const", "const", "const", "const"], ["key", "key", "key", "key"], ["key", "key", "key", "key"],
                 ["count", "nonce", "nonce", "nonce"]]
        cols = {"const": GREY_B, "key": HEAD, "count": YES, "nonce": DATA}
        cell = 0.95
        grid = VGroup()
        cells = [[None] * 4 for _ in range(4)]
        for r in range(4):
            for q in range(4):
                n = names[r][q]
                sq = Square(side_length=cell, stroke_color=GREY_B, stroke_width=1.5, fill_color=cols[n],
                            fill_opacity=0.25).move_to([q * cell, -r * cell, 0])
                cells[r][q] = sq
                grid.add(VGroup(sq, label(n, font_size=16, color=WHITE).move_to(sq)))
        grid.center().next_to(head, DOWN, buff=0.5).to_edge(LEFT, buff=0.9)
        colh = VGroup(*[SurroundingRectangle(cells[r][0], color=YES, buff=0.02, stroke_width=3) for r in range(4)])
        diag = VGroup(*[SurroundingRectangle(cells[r][r], color=NO, buff=0.02, stroke_width=3) for r in range(4)])
        qr = code([
            "def quarter_round(a, b, c, d):",
            "    a += b; d ^= a; d <<<= 16",
            "    c += d; b ^= c; b <<<= 12",
            "    a += b; d ^= a; d <<<= 8",
            "    c += d; b ^= c; b <<<= 7",
        ], size=19).next_to(grid, RIGHT, buff=0.7).align_to(grid, UP)
        kbps = c["bytes_per_s"] / 1000
        notes = VGroup(
            label(r"16 words of 32 bits; \ 20 rounds: \ quarter-rounds on the \textbf{columns}, \ then the "
                  r"\textbf{diagonals}", font_size=20, color=WHITE),
            label(r"output: \ the final state plus the starting one: \ 64 bytes of keystream per counter value",
                  font_size=20, color=GREY_A),
            label(r"matches RFC 8439: \ \texttt{" + c["block16"][:16] + r"}$\ldots$", font_size=20, color=YES),
            label(rf"ours: \ {kbps:.0f} KB/s in Python; \ vectorised C: \ gigabytes per second, \ no tables, \ no "
                  r"secret-dependent branches", font_size=20, color=HEAD),
            label(r"TLS 1.3, \ WireGuard, \ SSH, \ and Linux's random-number generator", font_size=20, color=DATA),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.16).to_edge(DOWN, buff=0.35)
        with self.voiceover(
            "What is used in practice? Daniel Bernstein's ChaCha20, from 2008. <bookmark mark='a'/> Its state is a "
            "four by four grid of thirty-two-bit words: four constants, eight words of key, a block counter, and a "
            "nonce, a number used once per message. <bookmark mark='b'/> The whole cipher is one small function, "
            "the quarter-round, using only three operations: add, rotate, XOR. <bookmark mark='c'/> Twenty rounds "
            "apply it to each column, then to each diagonal, so that every word soon depends on every other. "
            "<bookmark mark='d'/> Add the starting grid back in, and you have sixty-four bytes of keystream; "
            "increment the counter for the next sixty-four. <bookmark mark='e'/> Our implementation matches the "
            "standard's test vectors. It manages about seven hundred kilobytes a second in Python; vectorised C runs "
            "at gigabytes per second. With no lookup tables and no branches that depend on secrets, it leaks "
            "nothing through timing. <bookmark mark='f'/> It encrypts TLS 1.3, WireGuard and SSH connections, and "
            "generates Linux's random numbers."
        ) as vo:
            self.play(FadeIn(head), FadeIn(grid))
            vo.wait_until("b")
            self.play(FadeIn(qr))
            vo.wait_until("c")
            self.play(Create(colh), FadeIn(notes[0]))
            self.play(ReplacementTransform(colh, diag))
            vo.wait_until("d")
            self.play(FadeIn(notes[1]))
            vo.wait_until("e")
            self.play(FadeIn(notes[2]), FadeIn(notes[3]))
            vo.wait_until("f")
            self.play(FadeIn(notes[4]))
        self.wait(0.3)
        self.clear_scene()

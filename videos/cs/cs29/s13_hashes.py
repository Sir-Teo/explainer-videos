from __future__ import annotations

import math

from explainer.cs import *  # noqa: F403
from videos.cs.cs29.common import (DATA, HEAD, LAM, NO, PART, YES, fit_right, flow_box, grid_table, load)


class Hashes(VoiceoverScene):
    def construct(self):
        self.card()
        self.birthday()
        self.breaks()
        self.chain()
        self.sponge()

    def card(self):
        card = chapter_card(12, r"Hash functions", r"Can a short fingerprint stand for any file?",
                            lit=(1989, 2004, 2017), extra=((1989, r"Merkle and Damg\aa rd"),
                                                           (2004, r"Wang: \ MD5 collisions"), (2015, r"SHA-3"),
                                                           (2017, r"SHAttered")), part=PART)
        with self.voiceover("Chapter twelve. Hash functions."):
            self.play(FadeIn(card[0], shift=UP * 0.2), FadeIn(card[1]), FadeIn(card[2]))
        self.play(FadeOut(card))

    def birthday(self):
        h = load("hashes")
        head = label(r"Collisions, \ by the birthday bound", font_size=34).to_edge(UP, buff=0.3)
        ax = Axes(x_range=[14, 34, 4], y_range=[6, 18, 2], x_length=5.6, y_length=3.6,
                  axis_config={"color": GREY_D, "include_numbers": False}).next_to(head, DOWN, buff=0.6).to_edge(
            LEFT, buff=1.0)
        xt = VGroup(*[label(str(b), font_size=15, color=GREY_A).next_to(ax.c2p(b, 6), DOWN, buff=0.08)
                      for b in (16, 20, 24, 28, 32)])
        yt = VGroup(*[MathTex(rf"2^{{{y}}}", font_size=20, color=GREY_A).next_to(ax.c2p(14, y), LEFT, buff=0.08)
                      for y in (8, 12, 16)])
        xl = label(r"hash length $n$ \ (SHA-256, \ cut to $n$ bits)", font_size=17, color=GREY_A).next_to(
            xt, DOWN, buff=0.12)
        yl = label(r"hashes until the first collision", font_size=17, color=GREY_A).next_to(ax, UP, buff=0.1).align_to(
            ax, LEFT)
        pred = ax.plot(lambda n: n / 2 + 0.5 * math.log2(math.pi / 2), x_range=[15, 33], color=YES, stroke_width=2.5)
        dots = VGroup(*[Dot(ax.c2p(r["bits"], math.log2(r["mean"])), radius=0.07, color=HEAD) for r in h["birthday"]])
        notes = VGroup(
            label(r"\textbf{collision resistance}: \\ hard to find $x \ne y$ \\ with $H(x) = H(y)$", font_size=20,
                  color=WHITE),
            label(r"generic attack: \ hash random inputs \\ until two outputs match: \\ about "
                  r"$\sqrt{\pi/2}\cdot 2^{n/2}$ \ (Part 17)", font_size=20, color=YES),
            label(r"our means \ (30 or 10 runs each) \\ sit on the prediction", font_size=20, color=HEAD),
            label(r"so SHA-256 offers $2^{128}$, \\ not $2^{256}$, \ against collisions", font_size=20, color=NO),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.3).next_to(ax, RIGHT, buff=0.7).align_to(ax, UP)
        fit_right(notes)
        with self.voiceover(
            "A hash function squeezes any input to a short fixed-length output: SHA-256 gives two hundred and "
            "fifty-six bits. <bookmark mark='a'/> The central property is collision resistance: nobody can find two "
            "different inputs with the same hash. Since there are infinitely many inputs, collisions exist; they "
            "must just be impossible to find. <bookmark mark='b'/> There is always a generic attack: hash random "
            "inputs until two outputs match. By Part 17's birthday paradox, that takes about the square root of the "
            "number of possible outputs: two to the n over two. <bookmark mark='c'/> We cut SHA-256 down to sixteen, "
            "twenty, up to thirty-two bits and searched for collisions. The averages sit on the prediction. "
            "<bookmark mark='d'/> So a two-hundred-and-fifty-six-bit hash offers a hundred and twenty-eight bits of "
            "security against collisions, matching AES-128."
        ) as vo:
            self.play(FadeIn(head), Create(ax), FadeIn(xt), FadeIn(yt), FadeIn(xl), FadeIn(yl))
            vo.wait_until("a")
            self.play(FadeIn(notes[0]))
            vo.wait_until("b")
            self.play(Create(pred), FadeIn(notes[1]))
            vo.wait_until("c")
            self.play(LaggedStart(*[FadeIn(d, scale=1.5) for d in dots], lag_ratio=0.3), FadeIn(notes[2]))
            vo.wait_until("d")
            self.play(FadeIn(notes[3]))
        self.wait(0.3)
        self.clear_scene()

    def breaks(self):
        head = label(r"When hash functions break", font_size=34).to_edge(UP, buff=0.3)
        tab = grid_table([r"hash", r"year", r"bits", r"collisions found"], [
            [r"MD5", "1992", "128", r"2004 \ (Wang et al.): \ hours; \ now seconds"],
            [r"SHA-1", "1995", "160", r"2017 \ (SHAttered): \ $2^{63}$ work, \ two PDFs"],
            [r"SHA-256", "2001", "256", r"none"],
            [r"SHA3-256", "2015", "256", r"none"],
        ], widths=[1.8, 1.0, 0.9, 6.4], row_h=0.55, font_size=21, mono_cols=(1, 2))
        tab.next_to(head, DOWN, buff=0.5)
        for r in (1, 2):
            tab.cells[r][3].set_color(NO)
        for r in (3, 4):
            tab.cells[r][3].set_color(YES)
        lines = VGroup(
            label(r"a collision attack uses the structure, \ not the birthday: \ MD5 now takes under a second, "
                  r"\ not $2^{64}$", font_size=21, color=WHITE),
            label(r"2008: \ a rogue certificate authority from MD5 collisions; \ 2012: \ the Flame malware forged a "
                  r"Microsoft signature the same way", font_size=21, color=NO),
            label(r"2020: \ chosen-prefix SHA-1 collisions for about \$45{,}000: \ any two documents can be made to "
                  r"collide", font_size=21, color=NO),
            label(r"so systems need \textbf{agility}: \ a way to change hash functions before they break", font_size=21,
                  color=HEAD),
        ).arrange(DOWN, buff=0.2).to_edge(DOWN, buff=0.4)
        with self.voiceover(
            "Real hash functions have broken, and it took years each time to stop using them. <bookmark mark='a'/> "
            "MD5, from 1992, has a hundred-and-twenty-eight-bit output, so the birthday attack needs two to the "
            "sixty-four. In 2004 Wang Xiaoyun and her colleagues found collisions using its internal structure; "
            "today a laptop finds one in seconds. <bookmark mark='b'/> In 2008 researchers used MD5 collisions to "
            "create a rogue certificate authority, and in 2012 the Flame malware used the same idea to forge a "
            "Microsoft code-signing certificate. <bookmark mark='c'/> SHA-1 fell in 2017: two different PDF files "
            "with the same hash, after two to the sixty-three operations. By 2020, any two chosen documents could "
            "be made to collide for about forty-five thousand dollars of computing. <bookmark mark='d'/> No attack "
            "is known on SHA-256 or SHA-3. But the lesson is agility: build systems that can change their hash "
            "function before it breaks, not after."
        ) as vo:
            self.play(FadeIn(head), FadeIn(tab))
            for mk, ln in zip("abcd", lines):
                vo.wait_until(mk)
                self.play(FadeIn(ln))
        self.wait(0.3)
        self.clear_scene()

    def chain(self):
        h = load("hashes")
        le = h["length_ext"]
        head = label(r"Merkle--Damg\aa rd, \ and length extension", font_size=34).to_edge(UP, buff=0.3)
        fs = VGroup(*[flow_box(r"$f$", DATA, w=0.8, h=0.7, font=24) for _ in range(3)]).arrange(RIGHT, buff=1.3)
        fs.next_to(head, DOWN, buff=1.2).shift(LEFT * 0.6)
        iv = label(r"IV", font_size=22, color=GREY_A).next_to(fs[0], LEFT, buff=0.8)
        out = label(r"$H(m)$", font_size=24, color=YES).next_to(fs[2], RIGHT, buff=0.8)
        blocks = VGroup(*[label(t, font_size=20, color=WHITE).next_to(f, UP, buff=0.6) for t, f in
                          zip((r"$m_1$", r"$m_2$", r"$m_3$ + padding + length"), fs)])
        wires = VGroup(Arrow(iv.get_right(), fs[0].get_left(), buff=0.08, stroke_width=2.5, color=GREY_B),
                       *[Arrow(a.get_right(), b.get_left(), buff=0.08, stroke_width=2.5, color=GREY_B)
                         for a, b in zip(fs, fs[1:])],
                       Arrow(fs[2].get_right(), out.get_left(), buff=0.08, stroke_width=2.5, color=GREY_B),
                       *[Arrow(b.get_bottom(), f.get_top(), buff=0.08, stroke_width=2.5, color=GREY_B)
                         for b, f in zip(blocks, fs)])
        ext = flow_box(r"$f$", NO, w=0.8, h=0.7, font=24).next_to(out, RIGHT, buff=0.8)
        ea = Arrow(out.get_right(), ext.get_left(), buff=0.08, stroke_width=2.5, color=NO)
        eb = label(r"\texttt{\&role=admin}", font_size=18, color=NO).next_to(ext, UP, buff=0.6)
        ebw = Arrow(eb.get_bottom(), ext.get_top(), buff=0.08, stroke_width=2.5, color=NO)
        msg = le["msg"].replace("&", r"\&")
        lines = VGroup(
            label(r"compression function $f$, \ chained: \ MD5, \ SHA-1, \ SHA-256; \ collision resistant if $f$ is "
                  r"\ (Merkle, \ Damg\aa rd, \ 1989)", font_size=21, color=WHITE),
            label(r"but $H(m)$ \textbf{is} the chain's state: \ anyone can continue it", font_size=21, color=NO),
            label(rf"a server tags \texttt{{{msg}}} with $H(\mathit{{secret}} \,\|\, m)$; \ without the secret, \ we "
                  rf"append {le['glue_len']} bytes of padding and \texttt{{\&role=admin}}", font_size=21, color=HEAD),
            label(rf"our forged tag verifies: \ {'valid' if le['valid'] else 'invalid'} \ (Flickr's API, \ 2009): \ "
                  r"use HMAC, \ never $H(k \,\|\, m)$", font_size=21, color=YES),
        ).arrange(DOWN, buff=0.18).to_edge(DOWN, buff=0.35)
        with self.voiceover(
            "How are hashes like SHA-256 built? <bookmark mark='a'/> Ralph Merkle and Ivan Damgård showed in 1989 "
            "how to hash any length with a compression function f that takes a fixed-size state and one block. "
            "Chain it: pad the message with its length, feed the blocks through f one by one, and output the final "
            "state. If f resists collisions, so does the chain. <bookmark mark='b'/> But the output is the chain's "
            "whole state, so anyone holding a hash can keep going. <bookmark mark='c'/> Suppose a server "
            "authenticates requests with the hash of a secret key followed by the message. We see a request and its "
            "tag. Without knowing the secret, we append the padding the server would have added, then role equals "
            "admin, and continue the chain from the tag. <bookmark mark='d'/> The server accepts our forged tag. "
            "This broke Flickr's API in 2009, and it is exactly why HMAC exists."
        ) as vo:
            self.play(FadeIn(head), FadeIn(fs), FadeIn(iv), FadeIn(out), FadeIn(blocks), FadeIn(wires))
            vo.wait_until("a")
            self.play(FadeIn(lines[0]))
            vo.wait_until("b")
            self.play(GrowArrow(ea), FadeIn(ext), FadeIn(eb), GrowArrow(ebw), FadeIn(lines[1]))
            vo.wait_until("c")
            self.play(FadeIn(lines[2]))
            vo.wait_until("d")
            self.play(FadeIn(lines[3]))
        self.wait(0.3)
        self.clear_scene()

    def sponge(self):
        h = load("hashes")
        head = label(r"SHA-3: \ the sponge", font_size=34).to_edge(UP, buff=0.3)
        W, rh, ch = 1.0, 1.1, 0.55
        cols = VGroup()
        xs = [-5.0, -2.6, -0.2, 2.2, 4.6]
        for i, x in enumerate(xs):
            r = Rectangle(width=W, height=rh, stroke_color=DATA, stroke_width=2, fill_color=DATA, fill_opacity=0.2)
            c = Rectangle(width=W, height=ch, stroke_color=LAM, stroke_width=2, fill_color=LAM, fill_opacity=0.2)
            VGroup(r, c).arrange(DOWN, buff=0).move_to([x, 0.6, 0])
            cols.add(VGroup(r, c))
        fbs = VGroup(*[flow_box(r"$f$", HEAD, w=0.75, h=1.65, font=24).move_to([(a + b) / 2, 0.6 - 0.27, 0])
                       for a, b in zip(xs, xs[1:])])
        rl = label(r"rate \\ 1088 bits", font_size=16, color=DATA).next_to(cols[0][0], LEFT, buff=0.15)
        cl = label(r"capacity \\ 512 bits", font_size=16, color=LAM).next_to(cols[0][1], LEFT, buff=0.15)
        ins = VGroup(*[VGroup(Arrow([x, 2.4, 0], cols[i][0].get_top(), buff=0.05, stroke_width=2.5, color=WHITE),
                              label(rf"$\oplus\, m_{i + 1}$", font_size=20, color=WHITE).move_to([x, 2.6, 0]))
                       for i, x in enumerate(xs[1:3], 1)])
        outs = VGroup(*[VGroup(Arrow(cols[i][0].get_top(), [x, 2.4, 0], buff=0.05, stroke_width=2.5, color=YES),
                               label(rf"$z_{k}$", font_size=20, color=YES).move_to([x, 2.6, 0]))
                        for k, (i, x) in enumerate(zip((3, 4), xs[3:]), 1)])
        ab = label(r"absorb", font_size=20, color=WHITE).move_to([(xs[1] + xs[2]) / 2, 3.0, 0])
        sq = label(r"squeeze", font_size=20, color=YES).move_to([(xs[3] + xs[4]) / 2, 3.0, 0])
        lines = VGroup(
            label(r"Keccak \ (Bertoni, \ Daemen, \ Peeters, \ Van Assche): \ a 1600-bit state and one fixed "
                  r"permutation $f$", font_size=21, color=WHITE),
            label(r"absorb: \ XOR each block into the rate part, \ apply $f$; \ squeeze: \ read output from the rate, "
                  r"\ apply $f$", font_size=21, color=DATA),
            label(r"the capacity is never output: \ no length extension, \ and generic security up to $c/2 = 256$ bits", font_size=21,
                  color=LAM),
            label(rf"ours matches \texttt{{hashlib}}'s SHA3-256 \ (and SHA-256, \ at {h['ours_us']:.0f} $\mu$s against "
                  rf"its {h['hashlib_us']:.2f})", font_size=21, color=YES),
        ).arrange(DOWN, buff=0.17).to_edge(DOWN, buff=0.3)
        with self.voiceover(
            "When SHA-1 began to crack, the US standards institute ran another open contest, and in 2012 chose "
            "Keccak, by Guido Bertoni, Joan Daemen, Michaël Peeters and Gilles Van Assche, as SHA-3. It is built "
            "differently. <bookmark mark='a'/> The state is sixteen hundred bits, scrambled by one fixed "
            "permutation f. <bookmark mark='b'/> The state is split into a rate and a capacity. To absorb the "
            "message, XOR each block into the rate part and apply f. To squeeze out the hash, read the rate part, "
            "apply f, and read again, as much as you need. <bookmark mark='c'/> The capacity part is never output "
            "and never directly touched by the message. That hidden half is the security: an attacker cannot "
            "continue the computation from an output, so length extension is impossible. <bookmark mark='d'/> Our "
            "SHA-3, like our SHA-256, matches Python's library on every test. Ours is pure Python, the library's is "
            "optimised C, which is the difference in speed."
        ) as vo:
            self.play(FadeIn(head), FadeIn(cols[0]), FadeIn(rl), FadeIn(cl))
            vo.wait_until("a")
            self.play(FadeIn(lines[0]))
            vo.wait_until("b")
            self.play(FadeIn(ab), FadeIn(ins[0]), FadeIn(fbs[0]), FadeIn(cols[1]))
            self.play(FadeIn(fbs[1]), FadeIn(cols[2]), FadeIn(ins[1]))
            self.play(FadeIn(fbs[2]), FadeIn(cols[3]), FadeIn(sq), FadeIn(outs[0]))
            self.play(FadeIn(fbs[3]), FadeIn(cols[4]), FadeIn(outs[1]), FadeIn(lines[1]))
            vo.wait_until("c")
            self.play(FadeIn(lines[2]), *[c[1].animate.set_fill(LAM, 0.5) for c in cols])
            vo.wait_until("d")
            self.play(FadeIn(lines[3]))
        self.wait(0.3)
        self.clear_scene()

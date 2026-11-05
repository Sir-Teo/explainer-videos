from __future__ import annotations

from explainer.cs import *  # noqa: F403
from videos.cs.cs21.common import (CTRL, DATA, HEAD, LAM, NO, PART, YES, grid_table, load, mono, words)


class Entropy(VoiceoverScene):
    def construct(self):
        self.card()
        self.whole_bits()
        self.ans()
        self.models()

    def card(self):
        card = chapter_card(11, r"Compression, \ II: \ coding the symbols", r"Can a symbol cost less than a bit?",
                            lit=(2009,), extra=((2009, r"Duda's ANS"),), part=PART)
        with self.voiceover("Chapter eleven. Compression, part two: coding the symbols."):
            self.play(FadeIn(card[0], shift=UP * 0.2), FadeIn(card[1]), FadeIn(card[2]))
        self.play(FadeOut(card))

    def whole_bits(self):
        d = load("entropy")
        head = label(r"Huffman's whole bits", font_size=34).to_edge(UP, buff=0.35)
        lines = VGroup(
            label(r"Shannon: \ a symbol of probability $p$ deserves $\log_2 (1/p)$ bits; \ the average is the "
                  r"entropy $H$", font_size=22, color=WHITE),
            label(r"Huffman (Part 19) gives every symbol a whole number of bits: \ within 1 bit of $H$ per symbol",
                  font_size=22, color=DATA),
        ).arrange(DOWN, buff=0.25).next_to(head, DOWN, buff=0.45)
        rows = [[f"{r['p']:.2f}", f"{r['entropy']:.3f}", f"{r['huffman']:.0f}", f"{r['rans']:.3f}"] for r in d["skew"]]
        tab = grid_table([r"$\Pr[\text{one symbol}]$", r"entropy, \ bits", r"Huffman", r"rANS"], rows,
                         widths=[3.2, 2.6, 2.0, 2.0], row_h=0.44, font_size=21, mono_cols=(),
                         colors=[[GREY_A, YES, NO, LAM]] * len(rows)).next_to(lines, DOWN, buff=0.45)
        tab.set_x(0)
        cap = label(r"200{,}000 symbols from a two-letter source, \ in bits per symbol", font_size=19, color=GREY_B
                    ).next_to(tab, DOWN, buff=0.2)
        md = label(rf"\textit{{Moby-Dick}}'s bytes: \ entropy {d['h0']:.3f}, \ Huffman {d['huffman']:.3f}, \ rANS "
                   rf"{d['rans']:.3f} bits each: \ there, \ whole bits cost under 1\%", font_size=21, color=HEAD
                   ).to_edge(DOWN, buff=0.5)
        with self.voiceover(
            "Lempel–Ziv finds the repetition; then the symbols must be written in bits. <bookmark mark='a'/> "
            "Shannon says a symbol of probability p is worth log of one over p bits, and the average is the "
            "entropy. <bookmark mark='b'/> Huffman's code from Part 19 gives each symbol a whole number of bits, "
            "which is within one bit of that. <bookmark mark='c'/> Usually that is fine. But take a source where "
            "one symbol has probability ninety-five percent: its entropy is under three tenths of a bit per symbol, "
            "and Huffman still spends a whole bit on every symbol, more than three times too much. <bookmark "
            "mark='d'/> The last column, rANS, gets to within a fraction of a percent of the entropy, at every "
            "skew. <bookmark mark='e'/> On the bytes of Moby-Dick, where no symbol dominates, Huffman's whole bits "
            "cost less than one percent."
        ) as vo:
            self.play(FadeIn(head))
            vo.wait_until("a")
            self.play(FadeIn(lines[0]))
            vo.wait_until("b")
            self.play(FadeIn(lines[1]))
            vo.wait_until("c")
            self.play(FadeIn(VGroup(*tab.cells[0][:3])), FadeIn(tab.rule),
                      LaggedStart(*[FadeIn(VGroup(*r[:3])) for r in tab.cells[1:]], lag_ratio=0.3), FadeIn(cap))
            vo.wait_until("d")
            self.play(FadeIn(tab.cells[0][3]), LaggedStart(*[FadeIn(r[3]) for r in tab.cells[1:]], lag_ratio=0.3))
            vo.wait_until("e")
            self.play(FadeIn(md))
        self.wait(0.3)
        self.clear_scene()

    def ans(self):
        head = label(r"Asymmetric numeral systems", font_size=34).to_edge(UP, buff=0.35)
        lines = VGroup(
            label(r"the whole message as one integer $x$; \ each symbol multiplies it by about $1/p$", font_size=22,
                  color=WHITE),
            MathTex(r"x' = \Big\lfloor \frac{x}{f_s} \Big\rfloor M + (x \bmod f_s) + c_s", font_size=36, color=LAM),
            label(r"$f_s$: \ the symbol's frequency out of $M$; \ $c_s$: \ the frequencies before it", font_size=20,
                  color=GREY_A),
            label(r"$\log_2 x$ grows by $\log_2 (M / f_s) \approx \log_2 (1/p_s)$: \ exactly the entropy", font_size=22,
                  color=YES),
            label(r"keep $x$ in a machine word by streaming out its low bytes; \ decode by running it backwards",
                  font_size=22, color=WHITE),
            label(r"Duda (2009--2014): \ as tight as arithmetic coding, \ as fast as Huffman; \ zstd, \ LZFSE, \ JPEG XL",
                  font_size=22, color=HEAD),
        ).arrange(DOWN, buff=0.3).next_to(head, DOWN, buff=0.5)
        with self.voiceover(
            "Arithmetic coding solved this in the 1970s by treating the whole message as one number, but it was "
            "slow. <bookmark mark='a'/> Jarek Duda's asymmetric numeral systems keep the message as a single "
            "integer x and push each symbol into it. <bookmark mark='b'/> Divide x by the symbol's frequency, "
            "multiply by the total, and add the remainder and the symbol's offset. <bookmark mark='c'/> Here f is "
            "the symbol's frequency out of M. <bookmark mark='d'/> Each step multiplies x by about one over the "
            "symbol's probability, so the number of bits grows by exactly its information content. <bookmark "
            "mark='e'/> In practice x stays inside a machine word by streaming out its low bytes, and decoding runs "
            "the same arithmetic backwards. <bookmark mark='f'/> Duda's work, published between 2009 and 2014, made "
            "entropy coding as tight as arithmetic coding and as fast as Huffman. It is inside zstd, Apple's LZFSE "
            "and JPEG XL. We wrote a byte-wise version in forty lines; it round-trips every test."
        ) as vo:
            self.play(FadeIn(head))
            for mk, ln in zip("abcdef", lines):
                vo.wait_until(mk)
                self.play(FadeIn(ln, shift=UP * 0.1))
        self.wait(0.3)
        self.clear_scene()

    def models(self):
        d = load("entropy")
        head = label(r"The coder is easy; \ the model is everything", font_size=34).to_edge(UP, buff=0.35)
        vals = [d["h0"], d["h1"], d["h2"]]
        names = [r"each byte alone", r"given the previous byte", r"given the previous two"]
        bars = VGroup()
        for k, (v, n) in enumerate(zip(vals, names)):
            b = Rectangle(width=v * 1.4, height=0.5, stroke_width=0, fill_color=[DATA, LAM, YES][k], fill_opacity=0.85)
            b.move_to([-2.6 + b.width / 2, 1.4 - k * 0.8, 0])
            bars.add(VGroup(b, label(n, font_size=19, color=GREY_A).next_to(b, LEFT, buff=0.2).align_to([-2.7, 0, 0],
                                                                                                    RIGHT),
                            label(rf"{v:.2f} bits", font_size=19, color=WHITE).next_to(b, RIGHT, buff=0.15)))
        cap = label(r"\textit{Moby-Dick}: \ empirical entropy of the next byte", font_size=20, color=GREY_B
                    ).next_to(bars, UP, buff=0.3)
        notes = VGroup(
            label(r"better predictions, \ fewer bits: \ compression \textbf{is} prediction", font_size=22, color=HEAD),
            label(r"PPM (1984), \ context mixing, \ \texttt{xz}'s LZMA; \ \textit{AI, Built} Part 1: \ language models "
                  r"are the best text compressors we have", font_size=20, color=GREY_A),
            label(r"zstd \ (Collet, \ 2016): \ LZ77 + Huffman + ANS, \ tuned for speed: \ the default in Linux and "
                  r"Meta's servers", font_size=20, color=DATA),
        ).arrange(DOWN, buff=0.22).to_edge(DOWN, buff=0.5)
        with self.voiceover(
            "With a coder that reaches the entropy of whatever probabilities it is given, the only question left is "
            "how good those probabilities are. <bookmark mark='a'/> Treat each byte of Moby-Dick on its own, and the "
            "entropy is four point four bits. Given the previous byte, three point five. Given the previous two, two "
            "point eight. <bookmark mark='b'/> Better prediction means fewer bits: compression is prediction. "
            "<bookmark mark='c'/> That is the road from PPM through context mixing to the language models of the "
            "AI series, whose first part found them to be the best compressors of text we have. <bookmark mark='d'/> At the other end, Yann "
            "Collet's zstd combines Lempel–Ziv, Huffman and ANS, tuned for speed, and is now the default compressor "
            "in much of the world's infrastructure."
        ) as vo:
            self.play(FadeIn(head), FadeIn(cap))
            vo.wait_until("a")
            self.play(LaggedStart(*[FadeIn(b) for b in bars], lag_ratio=0.6), run_time=4.0)
            vo.wait_until("b")
            self.play(FadeIn(notes[0]))
            vo.wait_until("c")
            self.play(FadeIn(notes[1]))
            vo.wait_until("d")
            self.play(FadeIn(notes[2]))
        self.wait(0.3)
        self.clear_scene()

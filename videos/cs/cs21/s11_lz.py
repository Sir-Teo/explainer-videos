from __future__ import annotations

import numpy as np

from explainer.cs import *  # noqa: F403
from videos.cs.cs21.common import (CTRL, DATA, HEAD, LAM, NO, PART, YES, grid_table, load, mono, words)


class Lz(VoiceoverScene):
    def construct(self):
        self.card()
        self.arcs()
        self.lz78()
        self.measured()

    def card(self):
        card = chapter_card(10, r"Compression, \ I: \ Lempel and Ziv", r"How do you say it again, shorter?",
                            lit=(1977, 1978), extra=((1977, r"LZ77"), (1978, r"LZ78")), part=PART)
        with self.voiceover("Chapter ten. Compression, part one: Lempel and Ziv."):
            self.play(FadeIn(card[0], shift=UP * 0.2), FadeIn(card[1]), FadeIn(card[2]))
        self.play(FadeOut(card))

    def arcs(self):
        d = load("lz")
        head = label(r"LZ77: \ point back to where you said it before", font_size=32).to_edge(UP, buff=0.3)
        txt = d["passage"][:150]
        per = 50
        lines = [txt[i:i + per] for i in range(0, len(txt), per)]
        cw = 0.245
        rows = VGroup()
        for r, ln in enumerate(lines):
            rows.add(VGroup(*[mono(c if c != " " else "·", 15, WHITE) for c in ln]))
            for k, m in enumerate(rows[-1]):
                m.move_to([-6.1 + k * cw, 1.6 - r * 1.3, 0])
        arcs = VGroup()
        for pos, L, D in d["arcs"]:
            if pos + L > len(txt):
                continue
            src = pos - D
            r1, c1 = divmod(src, per)
            r2, c2 = divmod(pos, per)
            a = np.array([-6.1 + c1 * cw, 1.6 - r1 * 1.3 + 0.2, 0])
            b = np.array([-6.1 + c2 * cw, 1.6 - r2 * 1.3 + 0.2, 0])
            arc = ArcBetweenPoints(b, a, angle=0.9 if r1 == r2 else 0.5, color=LAM, stroke_width=2)
            ul = VGroup(*[Line([-6.1 + ((pos + k) % per) * cw - cw / 2, 1.6 - ((pos + k) // per) * 1.3 - 0.18, 0],
                               [-6.1 + ((pos + k) % per) * cw + cw / 2, 1.6 - ((pos + k) // per) * 1.3 - 0.18, 0],
                               color=HEAD, stroke_width=3) for k in range(L)])
            tag = mono(f"({L},{D})", 12, HEAD).next_to(ul, DOWN, buff=0.04)
            arcs.add(VGroup(arc, ul, tag))
        side = VGroup(
            label(r"a match: \ (length, \ distance) \ copies $L$ characters from $D$ back", font_size=21, color=HEAD),
            label(r"a window of 32 KB; \ matches of 3 to 258 characters \ (DEFLATE's limits)", font_size=21,
                  color=GREY_A),
            label(r"find matches with a hash table of 3-character prefixes \ (Part 17)", font_size=21, color=DATA),
        ).arrange(DOWN, buff=0.2).to_edge(DOWN, buff=0.45)
        with self.voiceover(
            "In 1977 Abraham Lempel and Jacob Ziv proposed the idea behind zip, gzip and PNG. <bookmark mark='a'/> "
            "Read the text left to right. Whenever the next stretch has appeared recently, don't write it again: "
            "write a pair, how long it is and how far back it was. Here is the opening of A Tale of Two Cities. "
            "It was the, of times, it was the: each repetition becomes an arc back to its first appearance. "
            "<bookmark mark='b'/> The search looks back over a window, thirty-two kilobytes in DEFLATE, and "
            "matches from three to two hundred and fifty-eight characters. <bookmark mark='c'/> Finding the "
            "longest match fast is a hashing problem: index every three-character prefix in the window, and follow "
            "the chain of earlier positions with the same prefix."
        ) as vo:
            self.play(FadeIn(head), FadeIn(rows))
            vo.wait_until("a")
            self.play(LaggedStart(*[Create(a) for a in arcs], lag_ratio=0.3), FadeIn(side[0]), run_time=4.0)
            vo.wait_until("b")
            self.play(FadeIn(side[1]))
            vo.wait_until("c")
            self.play(FadeIn(side[2]))
        self.wait(0.3)
        self.clear_scene()

    def lz78(self):
        head = label(r"LZ78 and LZW: \ grow a dictionary of phrases", font_size=34).to_edge(UP, buff=0.35)
        lines = VGroup(
            label(r"read the longest phrase already in the dictionary; \ emit its number; \ add it plus the next "
                  r"character", font_size=22, color=WHITE),
            label(r"\texttt{a}, \ \texttt{b}, \ \texttt{ab}, \ \texttt{aba}, \ \dots: \ the phrases grow by one "
                  r"character each time", font_size=22, color=LAM),
            label(r"Welch (1984): \ start with all 256 bytes; \ Unix \texttt{compress}, \ GIF", font_size=22,
                  color=GREY_A),
            label(r"Ziv and Lempel's theorem: \ for any stationary ergodic source, \ the bits per character tend to "
                  r"the entropy rate", font_size=22, color=YES),
            label(r"universal: \ no model of the source is needed, \ only enough text", font_size=22, color=HEAD),
        ).arrange(DOWN, buff=0.35).next_to(head, DOWN, buff=0.6)
        with self.voiceover(
            "A year later Ziv and Lempel gave a second scheme. <bookmark mark='a'/> Keep a dictionary of phrases. "
            "Read the longest phrase already in it, write down its number, and add that phrase plus the next "
            "character as a new entry. <bookmark mark='b'/> The phrases grow one character at a time, so common "
            "stretches of text soon have a number of their own. <bookmark mark='c'/> Terry Welch's variant, LZW, "
            "starts with every single byte in the dictionary. It ran Unix's compress command and GIF images. "
            "<bookmark mark='d'/> Ziv and Lempel proved something remarkable: for any stationary ergodic source, "
            "the number of bits per character tends to the source's entropy rate, the best possible. <bookmark "
            "mark='e'/> The method is universal. It needs no model of the text, only enough of it."
        ) as vo:
            self.play(FadeIn(head))
            for mk, ln in zip("abcde", lines):
                vo.wait_until(mk)
                self.play(FadeIn(ln, shift=UP * 0.1))
        self.wait(0.3)
        self.clear_scene()

    def measured(self):
        d = load("lz")
        head = label(r"Our compressor against the real ones", font_size=34).to_edge(UP, buff=0.35)
        rows = [[r["book"], f"{r['n'] / 1000:.0f}", f"{r['ours'] / 1000:.0f}", f"{r['zlib'] / 1000:.0f}",
                 f"{r['lzw'] / 1000:.0f}", f"{r['bz2'] / 1000:.0f}", f"{r['xz'] / 1000:.0f}"] for r in d["rows"]]
        tab = grid_table([r"KB", r"text", r"ours: \ LZ77 + Huffman", r"\texttt{zlib -9}", r"LZW", r"\texttt{bzip2}",
                          r"\texttt{xz}"], rows, widths=[3.0, 1.2, 2.8, 1.6, 1.2, 1.4, 1.2], row_h=0.5,
                         font_size=19, mono_cols=(), colors=[[WHITE, GREY_A, YES, DATA, GREY_A, LAM, HEAD]] * len(rows))
        tab.next_to(head, DOWN, buff=0.5).set_x(0)
        md = next(r for r in d["rows"] if r["book"] == "Moby Dick")
        notes = VGroup(
            label(rf"\textit{{Moby-Dick}}: \ {words(md['matches'])} matches \ (mean {md['mean_len']:.1f} characters) "
                  rf"and {words(md['literals'])} literals", font_size=20, color=WHITE),
            label(r"ours is DEFLATE without lazy matching or block splitting: \ within 6\% of \texttt{zlib}", font_size=20,
                  color=YES),
            label(r"\texttt{bzip2} sorts \ (chapter 8); \ \texttt{xz} \ (LZMA) \ models what follows each match",
                  font_size=20, color=GREY_A),
            label(r"DEFLATE is LZ77 plus Huffman \ (Part 19, \ and \textit{AI, Built}, Part 1): \ zip, \ gzip, \ PNG, "
                  r"\ HTTP", font_size=20, color=DATA),
        ).arrange(DOWN, buff=0.2).to_edge(DOWN, buff=0.45)
        with self.voiceover(
            "We wrote an LZ77 compressor with hash chains and priced its output with Huffman codes, as DEFLATE "
            "does, and ran it on three novels. <bookmark mark='a'/> On Moby-Dick it found two hundred and twenty "
            "thousand matches, about five characters long on average, and only twenty-three thousand characters "
            "it had to spell out. <bookmark mark='b'/> It lands within six percent of zlib at its strongest "
            "setting, which adds lazy matching, trying one position later before committing. LZW is about as "
            "good. <bookmark mark='c'/> bzip2, which sorts, does better on novels, and xz better still, by modelling "
            "what is likely to follow each match. <bookmark mark='d'/> DEFLATE, Lempel–Ziv plus Huffman, is "
            "inside every zip file, PNG image and compressed web page."
        ) as vo:
            self.play(FadeIn(head), FadeIn(VGroup(*tab.cells[0])), FadeIn(tab.rule))
            self.play(LaggedStart(*[FadeIn(VGroup(*r)) for r in tab.cells[1:]], lag_ratio=0.3))
            vo.wait_until("a")
            self.play(FadeIn(notes[0]))
            vo.wait_until("b")
            self.play(FadeIn(notes[1]))
            vo.wait_until("c")
            self.play(FadeIn(notes[2]))
            vo.wait_until("d")
            self.play(FadeIn(notes[3]))
        self.wait(0.3)
        self.clear_scene()

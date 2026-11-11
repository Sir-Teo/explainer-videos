from __future__ import annotations

from explainer.cs import *  # noqa: F403
from videos.cs.cs25.common import (fit_right, CTRL, DATA, HEAD, LAM, NO, PART, YES, bar_chart, grid_table, load, mono, words)


class Kolmogorov(VoiceoverScene):
    def construct(self):
        self.card()
        self.compress()
        self.invariance()
        self.counting()
        self.berry()

    def card(self):
        card = chapter_card(10, r"Kolmogorov complexity", r"How much information is in a string?", lit=(1960, 1975),
                            extra=((1965, r"Kolmogorov"), (1975, r"Chaitin's incompleteness")), part=PART)
        with self.voiceover("Chapter ten. Kolmogorov complexity."):
            self.play(FadeIn(card[0], shift=UP * 0.2), FadeIn(card[1]), FadeIn(card[2]))
        self.play(FadeOut(card))

    def compress(self):
        k = load("kolmo")
        head = label(r"The shortest description", font_size=34).to_edge(UP, buff=0.3)
        defn = MathTex(r"C(x) = \min\{\, |p| \;:\; U(p) = x \,\}", font_size=38, color=HEAD).next_to(head, DOWN,
                                                                                                    buff=0.3)
        rows = k["rows"]
        names = [r["name"].replace("...", r"\ldots") for r in rows]
        vals = [r["best"] for r in rows]
        ch = bar_chart(vals, names, [NO, DATA, DATA, YES, YES, YES], height=2.6, bar_w=0.62, gap=0.5, log=True,
                       vmax=1.2e5, fmt_=lambda v: words(v), font_size=18)
        ch.next_to(defn, DOWN, buff=0.6).to_edge(LEFT, buff=0.7)
        cl = label(rf"best of zlib, bz2, xz \ (bytes, log scale), \ each input {words(k['n'])} bytes", font_size=18,
                   color=GREY_A).next_to(ch, DOWN, buff=0.15)
        notes = VGroup(
            label('this random-byte sample: all three retained compressed outputs are larger', font_size=20, color=NO),
            label('container bytes shown; every output is decompressed and compared in full', font_size=20,
                  color=DATA),
            label('finite pi printer: length input, caller and interpreter also required; \\\\ all 100,000 digits independently certified', font_size=20, color=HEAD),
            label('plain $C$: compressed bytes $\\times8$ PLUS fixed decoder, interpreter and framing costs', font_size=20, color=YES),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.22).next_to(ch, RIGHT, buff=0.6).align_to(ch, UP)
        fit_right(notes)
        with self.voiceover(
            "Fix an optimal plain description machine U. <bookmark mark='a'/> Plain complexity C of x is the minimum number of program BITS needed to output x. Later we will distinguish optimal prefix-free complexity K. <bookmark mark='b'/> Each retained input here has one hundred thousand bytes. Random bytes grow slightly under these three compressors. <bookmark mark='c'/> English and decimal pi compress, partly because their byte encodings contain redundancy. Every compressed output is retained and decompressed to its full original input. <bookmark mark='d'/> Our finite pi printer also needs its requested length, caller, libraries and interpreter. An independent integer-interval Chudnovsky computation certifies all one hundred thousand digits, including the leading three. <bookmark mark='e'/> Eight times a compressed byte length, PLUS fixed decoding and framing costs, supplies a plain-complexity upper bound. It does not compute the shortest description."
        ) as vo:
            self.play(FadeIn(head))
            vo.wait_until("a")
            self.play(FadeIn(defn))
            vo.wait_until("b")
            self.play(FadeIn(ch), FadeIn(cl), FadeIn(notes[0]))
            for mk, n_ in zip("cde", notes[1:]):
                vo.wait_until(mk)
                self.play(FadeIn(n_))
        self.wait(0.3)
        self.clear_scene()

    def invariance(self):
        head = label('Invariance needs OPTIMAL description machines', font_size=32).to_edge(UP, buff=0.35)
        lines = VGroup(
            MathTex(r"C_U(x) \;\le\; C_V(x) + c_V \quad \text{for every } x", font_size=40, color=HEAD),
            label('\\textbf{hypothesis}: optimal $U$ simulates $V$ with a fixed ADDITIVE program-length cost',
                  font_size=22, color=WHITE),
            label(r"the shortest $V$-program for $x$, \ prefixed by $i_V$, \ is a $U$-program for $x$: \ "
                  r"$c_V = |i_V|$", font_size=22, color=WHITE),
            label('two OPTIMAL plain machines: $|C_U(x)-C_V(x)|\\le c$',
                  font_size=22, color=YES),
            label('invariance: machine independence up to an additive constant, which can matter for short strings', font_size=22, color=DATA),
            label('interpreter/compiler description PLUS its effective encoding and runtime convention',
                  font_size=20, color=GREY_A),
        ).arrange(DOWN, buff=0.3).next_to(head, DOWN, buff=0.5)
        with self.voiceover(
            "The invariance theorem requires an OPTIMAL description system. <bookmark mark='a'/> An optimal U simulates every description machine V with a fixed additive program-length cost. <bookmark mark='b'/> The interpreter or compiler description is fixed for V. <bookmark mark='c'/> Combining it with a V description of x produces a U description only that constant longer, under the stipulated effective encoding. <bookmark mark='d'/> If both machines are optimal, the two inequalities bound their difference by a constant. <bookmark mark='e'/> The constant can matter for short strings; machine independence means only this additive equivalence. <bookmark mark='f'/> Arbitrary computational universality alone does not guarantee an additive length overhead, and an interpreter's raw source size omits its own runtime and encoding costs."
        ) as vo:
            self.play(FadeIn(head))
            for mk, ln in zip("abcdef", lines):
                vo.wait_until(mk)
                self.play(FadeIn(ln, shift=UP * 0.1))
        self.wait(0.3)
        self.clear_scene()

    def counting(self):
        head = label(r"Most strings cannot be compressed", font_size=34).to_edge(UP, buff=0.35)
        n = 8
        cols = []
        for L in range(n + 1):
            cnt = 2 ** L
            col = VGroup(*[Square(side_length=0.09, stroke_width=0, fill_color=DATA if L < n else HEAD,
                                  fill_opacity=0.9) for _ in range(min(cnt, 256))])
            col.arrange_in_grid(cols=max(1, min(16, cnt // 16 or 1)), buff=0.02)
            lab = label(rf"{cnt}", font_size=16, color=GREY_A).next_to(col, DOWN, buff=0.08)
            ll = label(rf"$|p| = {L}$", font_size=15, color=GREY_B).next_to(lab, DOWN, buff=0.04)
            cols.append(VGroup(col, lab, ll))
        row = VGroup(*cols).arrange(RIGHT, buff=0.18, aligned_edge=DOWN).next_to(head, DOWN, buff=0.4)
        if row.width > 12.5:
            row.width = 12.5
        row.set_x(0)
        lines = VGroup(
            MathTex(r"1 + 2 + 4 + \cdots + 2^{n-k-1} \;=\; 2^{n-k} - 1 \;<\; 2^{n-k}", font_size=34, color=WHITE),
            label(r"programs shorter than $n - k$ bits: \ too few to print more than a $2^{-k}$ fraction of the "
                  r"$2^n$ strings", font_size=22, color=DATA),
            label('fewer than $2^{-10}$ have $C(x)<n-10$; some length-$n$ string has $C(x)\\ge n$', font_size=22, color=YES),
            label('fixed deficit $c$: at least $1-2^{-c}$ have $C(x)\\ge n-c$; chosen-machine incompressibility', font_size=22, color=HEAD),
        ).arrange(DOWN, buff=0.28).next_to(row, DOWN, buff=0.45)
        with self.voiceover(
            "Count descriptions. <bookmark mark='a'/> Fewer than two to the n programs have length strictly below n, so at least one n-bit string has plain complexity at least n. <bookmark mark='b'/> More generally, fewer than a two-to-the-minus-k fraction have C strictly below n minus k, for zero through n as the deficit range. <bookmark mark='c'/> Thus fewer than one in a thousand and twenty-four have C below n minus ten. Saying shortened BY ten would instead include equality and change the threshold. <bookmark mark='d'/> Incompressibility is relative to a fixed machine and deficit. At least one minus two to the minus c of n-bit strings have C at least n minus c. The exact threshold C at least n guarantees some strings, not an overwhelming fraction. An injective lossless compressor cannot shorten every input."
        ) as vo:
            self.play(FadeIn(head), LaggedStart(*[FadeIn(c) for c in cols], lag_ratio=0.15), run_time=1.2)
            for mk, ln in zip("abcd", lines):
                vo.wait_until(mk)
                self.play(FadeIn(ln, shift=UP * 0.1))
        self.wait(0.3)
        self.clear_scene()

    def berry(self):
        head = label(r"$C$ is uncomputable, \ and randomness unprovable", font_size=32).to_edge(UP, buff=0.35)
        code_lines = [
            "def berry(L):",
            "    for x in all_strings():   # shortest first",
            "        if C(x) > L:",
            "            return x",
        ]
        prog = VGroup(*[mono(ln, 21, LAM) for ln in code_lines]).arrange(DOWN, aligned_edge=LEFT, buff=0.1)
        prog.next_to(head, DOWN, buff=0.45).to_edge(LEFT, buff=0.9)
        frame = SurroundingRectangle(prog, color=LAM, buff=0.2, corner_radius=0.08)
        side = VGroup(
            label(r"Berry's paradox \ (1906): \ ``the smallest number \\ not nameable in under sixty letters''",
                  font_size=19, color=GREY_A),
        ).next_to(frame, RIGHT, buff=0.5)
        lines = VGroup(
            label(r"if $C$ were computable, \ \texttt{berry(L)} would print a string of complexity $> L$", font_size=22,
                  color=WHITE),
            label(r"but \texttt{berry} with $L$ written in is only $\log_2 L + c$ bits long: \ for large $L$, \ "
                  r"$\log_2 L + c < L$", font_size=22, color=DATA),
            label(r"a short program printed a string that needs a long one: \ so $C$ is \textbf{not computable}",
                  font_size=22, color=NO),
            label('Chaitin: enumerate proofs in an EFFECTIVELY AXIOMATIZED SOUND arithmetic theory $T$', font_size=22, color=HEAD),
            label('for $L>c_T$, $T$ proves $C(x)>L$ for no $x$; effectiveness and soundness are essential', font_size=22, color=YES),
        ).arrange(DOWN, buff=0.27).next_to(frame, DOWN, buff=0.45).set_x(0)
        with self.voiceover(
            "Turn Berry's paradox into a program. <bookmark mark='a'/> The phrase names an object allegedly too complex for that phrase. <bookmark mark='b'/> If plain C were computable, search strings in shortlex order and output the first with C above L. Counting ensures one exists. <bookmark mark='c'/> Encoding L in this fixed plain program costs about log L plus a constant, less than L for large L. <bookmark mark='d'/> That contradicts the selected string's complexity, proving C uncomputable. <bookmark mark='e'/> For an EFFECTIVELY AXIOMATIZED SOUND theory T, enumerate proofs instead, seeking any assertion C of x exceeds L. <bookmark mark='f'/> Beyond a T-dependent constant none can appear. The effective hypothesis is essential. Incompressibility of most strings means a stated fixed deficit; it is not a claim that every sound theory lacks all proofs of randomness."
        ) as vo:
            self.play(FadeIn(head))
            vo.wait_until("a")
            self.play(FadeIn(side))
            vo.wait_until("b")
            self.play(Create(frame), FadeIn(prog), FadeIn(lines[0]))
            for mk, ln in zip("cdef", lines[1:]):
                vo.wait_until(mk)
                self.play(FadeIn(ln, shift=UP * 0.1))
        self.wait(0.3)
        self.clear_scene()

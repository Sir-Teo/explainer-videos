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
        defn = MathTex(r"K(x) = \min\{\, |p| \;:\; U(p) = x \,\}", font_size=38, color=HEAD).next_to(head, DOWN,
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
            label(r"random bytes: \\ \textbf{no} compressor gains anything", font_size=20, color=NO),
            label(r"English: \ about a third; \\ pi's digits: \ 43\% \ (a digit needs 3.32 bits)", font_size=20,
                  color=DATA),
            label(rf"yet a {k['pi_program_lines']}-line, \ {k['pi_program_bytes']}-byte program prints those digits: \\ "
                  r"$K$ is tiny, \\ the compressors cannot see it", font_size=20, color=HEAD),
            label(r"a compressor gives an \textbf{upper bound} \\ on $K$, \ never the value", font_size=20, color=YES),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.22).next_to(ch, RIGHT, buff=0.6).align_to(ch, UP)
        fit_right(notes)
        with self.voiceover(
            "Andrey Kolmogorov, Ray Solomonoff and Gregory Chaitin, independently in the 1960s, measured information "
            "by programs. <bookmark mark='a'/> The Kolmogorov complexity of a string is the length of the shortest "
            "program that prints it. <bookmark mark='b'/> Compressors give a feel for it. We gave three of them a "
            "hundred thousand bytes of six kinds. Random bytes do not shrink at all; the output is slightly larger. "
            "<bookmark mark='c'/> English text shrinks to about a third. The digits of pi to forty-three percent, "
            "which is just the cost of writing a digit in binary. <bookmark mark='d'/> But pi's digits are not "
            "random in Kolmogorov's sense: a nineteen-line function prints all of them. The compressors cannot "
            "find that program. <bookmark mark='e'/> Every compressor gives an upper bound on the complexity, never "
            "the value itself, and this chapter shows why nothing can do better."
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
        head = label(r"Which programming language? \ Hardly matters", font_size=32).to_edge(UP, buff=0.35)
        lines = VGroup(
            MathTex(r"K_U(x) \;\le\; K_V(x) + c_V \quad \text{for every } x", font_size=40, color=HEAD),
            label(r"\textbf{proof}: \ $U$ is universal, \ so some fixed program $i_V$ makes $U$ interpret $V$",
                  font_size=22, color=WHITE),
            label(r"the shortest $V$-program for $x$, \ prefixed by $i_V$, \ is a $U$-program for $x$: \ "
                  r"$c_V = |i_V|$", font_size=22, color=WHITE),
            label(r"so any two universal machines agree up to a constant: \ $|K_U(x) - K_V(x)| \le c$",
                  font_size=22, color=YES),
            label(r"the \textbf{invariance theorem}: \ information content is a property of $x$, \ not of the "
                  r"language", font_size=22, color=DATA),
            label(r"(the constant is the length of a Pebble interpreter written in Python, \ or the other way round)",
                  font_size=20, color=GREY_A),
        ).arrange(DOWN, buff=0.3).next_to(head, DOWN, buff=0.5)
        with self.voiceover(
            "Shortest program in which language? <bookmark mark='a'/> The invariance theorem says it barely "
            "matters. For any two universal machines, complexities differ by at most a constant. <bookmark "
            "mark='b'/> The proof: U is universal, so some fixed program makes U interpret V. <bookmark mark='c'/> "
            "Put that interpreter in front of the shortest V-program for x, and you have a U-program for x, longer "
            "by the interpreter's length and no more. <bookmark mark='d'/> Swap the roles, and the two measures "
            "agree up to a constant. <bookmark mark='e'/> So the information in a string belongs to the string. "
            "<bookmark mark='f'/> Between Python and the Pebble language, the constant is the size of an "
            "interpreter for one written in the other."
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
            label(r"so at most 1 string in 1,024 can be shortened by 10 bits; \ and \textbf{some} string of every "
                  r"length can't be shortened at all", font_size=22, color=YES),
            label(r"that is what \textbf{random} means here: \ $K(x) \ge |x|$; \ and every compressor expands "
                  r"some input", font_size=22, color=HEAD),
        ).arrange(DOWN, buff=0.28).next_to(row, DOWN, buff=0.45)
        with self.voiceover(
            "Now a proof that takes a single line. <bookmark mark='a'/> Count programs. There is one of length zero, "
            "two of length one, four of length two. All the programs shorter than n bits together number two to "
            "the n, minus one: fewer than the strings of length n. <bookmark mark='b'/> More generally, programs "
            "shorter than n minus k bits can print at most a two to the minus k fraction of the strings of length "
            "n. <bookmark mark='c'/> At most one string in a thousand and twenty-four can be shortened by ten "
            "bits, and at every length some string cannot be shortened at all. <bookmark mark='d'/> Such a string "
            "is called random: it has no description shorter than itself. It also shows that every compressor "
            "makes some file bigger, as it did for our random bytes."
        ) as vo:
            self.play(FadeIn(head), LaggedStart(*[FadeIn(c) for c in cols], lag_ratio=0.15), run_time=2.5)
            for mk, ln in zip("abcd", lines):
                vo.wait_until(mk)
                self.play(FadeIn(ln, shift=UP * 0.1))
        self.wait(0.3)
        self.clear_scene()

    def berry(self):
        head = label(r"$K$ is uncomputable, \ and randomness unprovable", font_size=32).to_edge(UP, buff=0.35)
        code_lines = [
            "def berry(L):",
            "    for x in all_strings():   # shortest first",
            "        if K(x) > L:",
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
            label(r"if $K$ were computable, \ \texttt{berry(L)} would print a string of complexity $> L$", font_size=22,
                  color=WHITE),
            label(r"but \texttt{berry} with $L$ written in is only $\log_2 L + c$ bits long: \ for large $L$, \ "
                  r"$\log_2 L + c < L$", font_size=22, color=DATA),
            label(r"a short program printed a string that needs a long one: \ so $K$ is \textbf{not computable}",
                  font_size=22, color=NO),
            label(r"Chaitin \ (1974): \ replace ``compute $K$'' by ``search for a proof that $K(x) > L$'' \ in a "
                  r"sound theory $T$", font_size=22, color=HEAD),
            label(r"so $T$ proves $K(x) > L$ for \textbf{no} $x$ once $L$ exceeds a constant $c_T$, \ though almost "
                  r"every $x$ is random", font_size=22, color=YES),
        ).arrange(DOWN, buff=0.27).next_to(frame, DOWN, buff=0.45).set_x(0)
        with self.voiceover(
            "Now the twist. <bookmark mark='a'/> In 1906 Bertrand Russell published a paradox he credited to a "
            "librarian, G. G. Berry: the smallest number that cannot be named in under sixty letters. That phrase "
            "names it in fewer. Turn the paradox into a program. <bookmark mark='b'/> If complexity were "
            "computable, this function would return the first string whose complexity exceeds L. <bookmark "
            "mark='c'/> But the function, with the number L written into it, is only about log L bits long, plus "
            "a constant, and for large L that is much less than L. <bookmark mark='d'/> A short program would have "
            "printed a string that has no short program. So complexity cannot be computed. <bookmark mark='e'/> "
            "Gregory Chaitin pushed this into logic. Instead of computing K, search a sound theory's proofs for a "
            "proof that some string has complexity above L. <bookmark mark='f'/> The same argument shows the "
            "search must fail once L passes a constant that depends on the theory. Almost every string is random, "
            "and beyond a fixed size, no theory can prove a single one of them is."
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

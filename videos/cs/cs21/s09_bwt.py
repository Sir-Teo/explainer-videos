from __future__ import annotations

import re

from explainer.cs import *  # noqa: F403
from videos.cs.cs21.common import (CTRL, DATA, HEAD, LAM, NO, PART, YES, grid_table, load, mono, words)


def clean(s, n):
    s = s.replace("\n", " ")
    s = re.sub(r"[^A-Za-z ,.;:'!?\-]", "·", s)
    return s[:n]


class Bwt(VoiceoverScene):
    def construct(self):
        self.card()
        self.matrix()
        self.invert()
        self.runs()
        self.context()

    def card(self):
        card = chapter_card(8, r"The Burrows--Wheeler transform", r"Can sorting make a book more compressible?",
                            lit=(1994,), extra=((1994, r"Burrows--Wheeler"),), part=PART)
        with self.voiceover("Chapter eight. The Burrows–Wheeler transform."):
            self.play(FadeIn(card[0], shift=UP * 0.2), FadeIn(card[1]), FadeIn(card[2]))
        self.play(FadeOut(card))

    def matrix(self):
        d = load("bwt")
        head = label(r"Sort the rotations, \ keep the last column", font_size=34).to_edge(UP, buff=0.3)
        rots = d["rotations"]
        w = "banana$"
        unsorted = [w[i:] + w[:i] for i in range(len(w))]
        grid = VGroup()
        for r in unsorted:
            grid.add(VGroup(*[mono(c, 26, WHITE) for c in r]).arrange(RIGHT, buff=0.22))
        grid.arrange(DOWN, buff=0.12).move_to(LEFT * 2.6 + DOWN * 0.2)
        cap1 = label(r"every rotation of \texttt{banana\$}", font_size=20, color=GREY_A).next_to(grid, UP, buff=0.25)
        target = VGroup()
        for r in rots:
            target.add(VGroup(*[mono(c, 26, WHITE) for c in r]).arrange(RIGHT, buff=0.22))
        target.arrange(DOWN, buff=0.12).move_to(grid)
        side = VGroup(
            label(r"sorted: \ the first column $F$ is just the letters in order", font_size=21, color=DATA),
            label(r"the last column $L$ is the transform: \ \texttt{annb\$aa}", font_size=21, color=YES),
            label(r"each character of $L$ \textbf{precedes} its row's rotation in the text", font_size=21, color=WHITE),
            label(r"rows that start alike sit together, \ so the characters before them cluster", font_size=21,
                  color=HEAD),
            label(r"in \textit{Moby-Dick}, \ 72\% of the rows beginning \texttt{he} \\ end in \texttt{t}: \ long runs "
                  r"of \texttt{t}", font_size=21, color=LAM),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.3).to_edge(RIGHT, buff=0.4)
        if side.width > 6.2:
            side.width = 6.2
            side.to_edge(RIGHT, buff=0.4)
        with self.voiceover(
            "In 1994 Michael Burrows and David Wheeler published a transform that Wheeler had found years earlier. "
            "<bookmark mark='a'/> Write down every rotation of the text, here banana with an end marker. <bookmark "
            "mark='b'/> Sort the rotations. The first column is now just the letters of the text in order. "
            "<bookmark mark='c'/> The last column is the transform: a n n b, end marker, a a. <bookmark mark='d'/> "
            "Each character in the last column is the one that comes just before its row in the text. Rows "
            "that begin alike are sorted next to each other, <bookmark mark='e'/> so the characters before them "
            "cluster too. <bookmark mark='f'/> In Moby-Dick, nearly three in four of the rows beginning h e end "
            "in t, so the sorted text has long runs of the same letter."
        ) as vo:
            self.play(FadeIn(head))
            vo.wait_until("a")
            self.play(FadeIn(grid), FadeIn(cap1))
            vo.wait_until("b")
            self.play(Transform(grid, target), FadeOut(cap1), run_time=1.5)
            first = VGroup(*[r[0] for r in grid])
            last = VGroup(*[r[-1] for r in grid])
            self.play(first.animate.set_color(DATA), FadeIn(side[0]))
            vo.wait_until("c")
            self.play(last.animate.set_color(YES), FadeIn(side[1]))
            vo.wait_until("d")
            self.play(FadeIn(side[2]))
            vo.wait_until("e")
            self.play(FadeIn(side[3]))
            vo.wait_until("f")
            self.play(FadeIn(side[4]))
        self.wait(0.3)
        self.clear_scene()

    def invert(self):
        d = load("bwt")
        head = label(r"Undoing it: \ the LF mapping", font_size=34).to_edge(UP, buff=0.3)
        L = d["L"]
        F = "".join(sorted(L))
        colF = VGroup(*[mono(c, 28, DATA) for c in F]).arrange(DOWN, buff=0.18).move_to(LEFT * 4.6 + DOWN * 0.2)
        colL = VGroup(*[mono(c, 28, YES) for c in L]).arrange(DOWN, buff=0.18).move_to(LEFT * 2.4 + DOWN * 0.2)
        hF = label(r"$F$", font_size=24, color=DATA).next_to(colF, UP, buff=0.2)
        hL = label(r"$L$", font_size=24, color=YES).next_to(colL, UP, buff=0.2)
        # LF: the k-th occurrence of c in L is the k-th occurrence of c in F
        seen, lf = {}, []
        for c in L:
            k = seen.get(c, 0)
            seen[c] = k + 1
            lf.append([i for i, x in enumerate(F) if x == c][k])
        arrows = VGroup(*[Arrow(colL[i].get_left(), colF[lf[i]].get_right(), buff=0.12, stroke_width=1.8,
                                color=GREY_B, max_tip_length_to_length_ratio=0.08) for i in range(len(L))])
        side = VGroup(
            label(r"the $k$-th \texttt{a} in $L$ is the $k$-th \texttt{a} in $F$: \ the same character of the text",
                  font_size=21, color=WHITE),
            label(r"(rows starting \texttt{a} are sorted by what follows; \ so are rows ending \texttt{a})", font_size=19,
                  color=GREY_A),
            label(r"start at the row ending in \texttt{\$}; \ read $L$, \ jump along the arrow, \ repeat", font_size=21,
                  color=HEAD),
            label(r"the text comes out backwards: \ \texttt{\$}, \ \texttt{a}, \ \texttt{n}, \ \texttt{a}, \ \texttt{n}, "
                  r"\ \texttt{a}, \ \texttt{b}", font_size=21, color=YES),
            label(r"the whole of \textit{Moby-Dick}, \ inverted and checked: \ identical", font_size=21, color=LAM),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.3).to_edge(RIGHT, buff=0.4)
        if side.width > 7.2:
            side.width = 7.2
            side.to_edge(RIGHT, buff=0.4)
        out = VGroup()
        with self.voiceover(
            "Sorting threw away the order of the text, or seemed to. <bookmark mark='a'/> The key fact: the "
            "k-th a in the last column and the k-th a in the first column are the same character of the text. "
            "<bookmark mark='b'/> Rows that start with a are sorted by what follows the a, and so are the rows "
            "that end with a, because the text after that a is the rest of each rotation. <bookmark mark='c'/> So "
            "start at the row ending with the end marker, which is the text itself. Read its last character, then "
            "jump along the arrow to the row that begins with that same character, and repeat. <bookmark mark='d'/> "
            "The text comes out backwards, one character per jump. <bookmark mark='e'/> We inverted the transform of "
            "all of Moby-Dick this way and got the novel back exactly."
        ) as vo:
            self.play(FadeIn(head), FadeIn(colF), FadeIn(colL), FadeIn(hF), FadeIn(hL))
            vo.wait_until("a")
            self.play(LaggedStart(*[GrowArrow(a) for a in arrows], lag_ratio=0.1), FadeIn(side[0]))
            vo.wait_until("b")
            self.play(FadeIn(side[1]))
            vo.wait_until("c")
            self.play(FadeIn(side[2]))
            i = L.index("$")
            for _ in range(len(L)):
                ch = L[i]
                box = SurroundingRectangle(colL[i], color=HEAD, buff=0.08)
                self.play(Create(box), run_time=0.25)
                out.add(mono(ch, 24, YES))
                out.arrange(LEFT, buff=0.1).move_to(RIGHT * 2.6 + DOWN * 3.2)
                self.play(FadeIn(out[-1]), Indicate(arrows[i], color=HEAD), run_time=0.35)
                self.remove(box)
                i = lf[i]
            vo.wait_until("d")
            self.play(FadeIn(side[3]))
            vo.wait_until("e")
            self.play(FadeIn(side[4]))
        self.wait(0.3)
        self.clear_scene()

    def context(self):
        e = load("entropy")
        head = label(r"Why sorting helps: \ contexts", font_size=34).to_edge(UP, buff=0.35)
        lines = VGroup(
            label(r"rows are sorted by what \textbf{follows}; \ $L$ holds what \textbf{precedes}", font_size=22, color=WHITE),
            label(r"so $L$ is the text's characters grouped by their right context: \ all the characters before "
                  r"\texttt{he}, \ then before \texttt{hi}, \ \dots", font_size=22, color=LAM),
            label(r"within a group, \ one or two characters dominate: \ a predictable stream", font_size=22, color=YES),
            MathTex('H_0(\\operatorname{BWT}(T))=H_0(T)\\quad\\text{(a permutation)}',
                    font_size=34, color=HEAD),
            label(rf"\textit{{Moby-Dick}}: \ $H_0 = {e['h0']:.2f}$, \ $H_1 = {e['h1']:.2f}$, \ $H_2 = {e['h2']:.2f}$ "
                  r"bits per character \ (chapter 11)", font_size=20, color=GREY_A),
            label('context-aware coding needs overhead terms; \\ the transform alone saves no bytes', font_size=20,
                  color=GREY_A),
        ).arrange(DOWN, buff=0.26)
        lines[:3].arrange(DOWN, buff=0.26).next_to(head, DOWN, buff=0.4)
        lines[3:].arrange(DOWN, buff=0.26).to_edge(DOWN, buff=0.4)
        ctx = load("bwt")["ctx"]
        pal = {"t": YES, " ": GREY_B, "w": DATA, "s": LAM, "c": HEAD, "T": CTRL}
        groups = VGroup()
        for c in ("he", "hi", "ho"):
            tot = ctx[c]["total"]
            bar = VGroup()
            for k, (ch, v) in enumerate(ctx[c]["top"]):
                w_ = 8.4 * v / tot
                col = pal.get(ch, GREY_D)
                seg = Rectangle(width=w_, height=0.42, stroke_width=0, fill_color=col, fill_opacity=0.85)
                lab = mono("␣" if ch == " " else ch, 16, BLACK if w_ > 0.3 else col)
                bar.add(VGroup(seg, lab))
            bar.arrange(RIGHT, buff=0.02)
            for seg, lab in bar:
                lab.move_to(seg)
            name = label(rf"before \texttt{{{c}}}", font_size=19, color=WHITE)
            pct = label(rf"{words(tot)} rows; \ {100 * ctx[c]['top'][0][1] / tot:.0f}\% \texttt{{"
                        rf"{'space' if ctx[c]['top'][0][0] == ' ' else ctx[c]['top'][0][0]}}}", font_size=17,
                        color=GREY_A)
            groups.add(VGroup(name, bar, pct).arrange(RIGHT, buff=0.25))
        groups.arrange(DOWN, buff=0.28, aligned_edge=LEFT).move_to(DOWN * 0.15)
        with self.voiceover(
            "Why does sorting help a later coder? <bookmark mark='a'/> Rows are sorted by what follows a position; the last column holds what precedes it. <bookmark mark='b'/> Characters before similar right contexts are grouped together: before he, before hi, and so on. <bookmark mark='c'/> Within those groups some characters dominate. Before he, t dominates here. <bookmark mark='d'/> The transform itself is a reversible permutation, so its zero-order histogram and entropy are unchanged. Compression comes from coding the resulting local structure. <bookmark mark='e'/> The lower-order conditional entropies shown below illustrate the value of context; they are not promised final file sizes. <bookmark mark='f'/> Manzini's 2001 analysis gives high-order entropy bounds for specified coding pipelines, with constants and overhead terms. Those terms matter for short texts and large context orders."
        ) as vo:
            self.play(FadeIn(head))
            vo.wait_until("a")
            self.play(FadeIn(lines[0], shift=UP * 0.1))
            vo.wait_until("b")
            self.play(FadeIn(lines[1], shift=UP * 0.1), LaggedStart(*[FadeIn(g) for g in groups], lag_ratio=0.4))
            vo.wait_until("c")
            self.play(FadeIn(lines[2], shift=UP * 0.1), *[Indicate(g[1][0], color=YES) for g in groups])
            for mk, ln in zip("def", lines[3:]):
                vo.wait_until(mk)
                self.play(FadeIn(ln, shift=UP * 0.1))
        self.wait(0.3)
        self.clear_scene()

    def runs(self):
        d = load("bwt")
        head = label(r"What the transform does to a novel", font_size=34).to_edge(UP, buff=0.35)
        t = clean(d["chapter_text_sample"], 64)
        b = clean(d["chapter_bwt_sample"], 64)
        before = VGroup(label(r"\textit{Moby-Dick}, \ chapter 1:", font_size=20, color=GREY_A),
                        mono(t, 16, WHITE)).arrange(DOWN, aligned_edge=LEFT, buff=0.12)
        after = VGroup(label(r"a stretch of its transform:", font_size=20, color=GREY_A),
                       mono(b, 16, YES)).arrange(DOWN, aligned_edge=LEFT, buff=0.12)
        VGroup(before, after).arrange(DOWN, aligned_edge=LEFT, buff=0.35).next_to(head, DOWN, buff=0.45)
        rows = [
            [r"runs of equal characters", words(d["md_runs"]), rf"{d['md_n'] / d['md_runs']:.1f} characters each"],
            [r"after move-to-front: \ zeros", f"{d['mtf_zero_share'] * 100:.0f}\\%", r"(of a 12 KB chapter)"],
            [r"entropy, \ bits per byte", f"{d['h0_text']:.2f}", rf"after BWT + MTF: \ {d['h0_mtf']:.2f}"],
            [r"\texttt{zlib} \ (LZ77 + Huffman)", f"{d['zlib_text'] / 1000:.0f} KB", r"chapter 10"],
            [r"\texttt{bzip2} \ (BWT + MTF + Huffman)", f"{d['bz2_text'] / 1000:.0f} KB", r"Seward, \ 1996"],
        ]
        tab = grid_table([r"\textit{Moby-Dick}, \ 1.2 MB", r"", r""], rows, widths=[5.2, 2.2, 4.4], row_h=0.44,
                         font_size=20, mono_cols=(), colors=[[WHITE, YES, GREY_A]] * len(rows))
        tab.next_to(after, DOWN, buff=0.45).set_x(0)
        with self.voiceover(
            "Here is the opening of Moby-Dick, and a stretch of its transform. <bookmark mark='a'/> The transform "
            "is full of runs. Across the novel there are just over half a million runs for 1.2 million characters. "
            "<bookmark mark='b'/> Move-to-front coding replaces each character by its position in a list of "
            "recently seen characters, so a run becomes a string of zeros: <bookmark mark='c'/> the entropy drops "
            "from four point four bits per character to two point seven. <bookmark mark='d'/> That is the recipe "
            "of bzip2, which Julian Seward released in 1996: transform, move to front, then Huffman. On the novel "
            "it beats zlib's Lempel–Ziv by a quarter."
        ) as vo:
            self.play(FadeIn(head), FadeIn(before), FadeIn(after))
            vo.wait_until("a")
            self.play(FadeIn(VGroup(*tab.cells[0])), FadeIn(tab.rule), FadeIn(VGroup(*tab.cells[1])))
            vo.wait_until("b")
            self.play(FadeIn(VGroup(*tab.cells[2])))
            vo.wait_until("c")
            self.play(FadeIn(VGroup(*tab.cells[3])))
            vo.wait_until("d")
            self.play(FadeIn(VGroup(*tab.cells[4])), FadeIn(VGroup(*tab.cells[5])))
        self.wait(0.3)
        self.clear_scene()

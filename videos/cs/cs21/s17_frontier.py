from __future__ import annotations

from explainer.cs import *  # noqa: F403
from videos.cs.cs21.common import (CTRL, DATA, HEAD, LAM, NO, PART, YES, grid_table, load, mono, words)


class Frontier(VoiceoverScene):
    def construct(self):
        self.card()
        self.repetitive()
        self.rindex()
        self.lower()
        self.open_()

    def card(self):
        card = chapter_card(16, r"Frontier: \ indexes as small as the information", r"How small can a searchable "
                            r"text be?", lit=(2018, 2020), extra=((2018, r"the r-index"), (2020, r"$r = O(z \log^2 n)$")),
                            part=PART)
        with self.voiceover("Chapter sixteen. Frontier: indexes as small as the information."):
            self.play(FadeIn(card[0], shift=UP * 0.2), FadeIn(card[1]), FadeIn(card[2]))
        self.play(FadeOut(card))

    def repetitive(self):
        d = load("period")
        head = label(r"When texts repeat themselves", font_size=34).to_edge(UP, buff=0.35)
        rows = [
            [r"the novels \ (first 6.5 MB)", words(d["vers_n"]), words(d["novel_runs"]),
             f"{d['vers_n'] / d['novel_runs']:.1f}"],
            [rf"{d['versions']} versions of this course's syllabus", words(d["vers_n"]), words(d["vers_runs"]),
             f"{d['vers_n'] / d['vers_runs']:.0f}"],
        ]
        tab = grid_table([r"text", r"$n$", r"BWT runs $r$", r"$n / r$"], rows, widths=[5.6, 2.4, 2.6, 1.6], row_h=0.5,
                         font_size=21, mono_cols=(), colors=[[GREY_A, GREY_A, DATA, DATA], [YES, YES, YES, YES]])
        tab.next_to(head, DOWN, buff=0.5).set_x(0)
        notes = VGroup(
            label(rf"\texttt{{xz}} squeezes the 27 versions to {d['vers_xz'] / 1000:.0f} KB: \ "
                  rf"{d['vers_n'] / d['vers_xz']:.0f}$\times$", font_size=22, color=HEAD),
            label(r"collections like this are everywhere: \ versioned documents, \ source histories, \ and above all "
                  r"genomes", font_size=22, color=WHITE),
            label(r"a pangenome: \ thousands of human genomes, \ each 99.9\% like the others", font_size=22, color=LAM),
            label(r"an FM-index costs about $nH_k$ bits: \ it compresses \textit{statistics}, \ not repetition",
                  font_size=22, color=NO),
        ).arrange(DOWN, buff=0.28).next_to(tab, DOWN, buff=0.5)
        with self.voiceover(
            "The frontier concerns texts that repeat themselves. <bookmark mark='a'/> Count the runs in the "
            "Burrows–Wheeler transform, r. For six and a half megabytes of the novels, there are about two "
            "characters per run. For all twenty-seven versions of this course's syllabus, concatenated, the same "
            "length of text has only a hundred and thirty thousand runs: fifty characters each. <bookmark "
            "mark='b'/> xz compresses those versions sixty-fold. <bookmark mark='c'/> Collections like this are "
            "everywhere: versioned documents, the history of every software project, and above all genomes. "
            "<bookmark mark='d'/> A pangenome holds thousands of human genomes, each ninety-nine point nine percent "
            "identical to the others. <bookmark mark='e'/> An FM-index's size tracks the text's statistical entropy, "
            "which barely notices that one genome repeats another. For such collections it is far too big."
        ) as vo:
            self.play(FadeIn(head), FadeIn(VGroup(*tab.cells[0])), FadeIn(tab.rule))
            vo.wait_until("a")
            self.play(LaggedStart(*[FadeIn(VGroup(*r)) for r in tab.cells[1:]], lag_ratio=0.5))
            for mk, n_ in zip("bcde", notes):
                vo.wait_until(mk)
                self.play(FadeIn(n_))
        self.wait(0.3)
        self.clear_scene()

    def rindex(self):
        head = label(r"The r-index", font_size=36).to_edge(UP, buff=0.35)
        lines = VGroup(
            label(r"store the BWT as $r$ runs; \ backward search needs rank only at run boundaries", font_size=22,
                  color=WHITE),
            label(r"the hard part was \textbf{locate}: \ suffix-array samples cost $n / s$, \ not $O(r)$", font_size=22,
                  color=NO),
            label(r"Gagie, \ Navarro and Prezza (2018): \ sample the suffix array only at run ends: \ $O(r)$ words, "
                  r"\ each occurrence in $O(\log\log n)$", font_size=22, color=YES),
            label(r"move structures \ (Nishimoto and Tabei, 2021): \ LF in constant time, \ in $O(r)$ space",
                  font_size=22, color=LAM),
            label(r"how big is $r$? \ Kempa and Kociumaka (2020): \ $r = O(z \log^2 n)$, \ $z$ = LZ77's phrases",
                  font_size=22, color=HEAD),
            label(r"measures of repetitiveness: \ $\delta \le \gamma \le z \le r$ \ (Kociumaka, Navarro and Prezza)",
                  font_size=20, color=GREY_A),
        ).arrange(DOWN, buff=0.32).next_to(head, DOWN, buff=0.5)
        with self.voiceover(
            "The answer is an index whose size depends on r. <bookmark mark='a'/> Store the transform as its runs, "
            "and backward search works with rank queries at run boundaries only. <bookmark mark='b'/> The obstacle "
            "for years was locating: suffix-array samples every s rows cost n over s, which is far more than r. "
            "<bookmark mark='c'/> In 2018 Travis Gagie, Gonzalo Navarro and Nicola Prezza showed that sampling the "
            "suffix array only at the ends of runs is enough, giving a full index in order r words that reports "
            "each occurrence in log log n time. <bookmark mark='d'/> Later work makes each LF step constant time in "
            "the same space. <bookmark mark='e'/> And how big is r, compared with Lempel–Ziv's number of phrases z? "
            "Dominik Kempa and Tomasz Kociumaka proved in 2020 that r is at most z times log n squared, settling a "
            "long-standing conjecture. <bookmark mark='f'/> A whole ladder of repetitiveness measures has grown up, "
            "and the open question is how low on it a fast index can go."
        ) as vo:
            self.play(FadeIn(head))
            for mk, ln in zip("abcdef", lines):
                vo.wait_until(mk)
                self.play(FadeIn(ln, shift=UP * 0.1))
        self.wait(0.3)
        self.clear_scene()

    def lower(self):
        head = label(r"And the quadratic wall", font_size=34).to_edge(UP, buff=0.35)
        lines = VGroup(
            label(r"edit distance, \ LCS, \ dynamic time warping: \ no $O(n^{2 - \varepsilon})$ under SETH \ "
                  r"(Backurs and Indyk; \ Abboud et al.; \ 2015)", font_size=22, color=NO),
            label(r"on compressible inputs: \ alignment speeds up with the compression \ (Crochemore, \ Landau and "
                  r"Ziv-Ukelson, \ 2003)", font_size=22, color=WHITE),
            label(r"approximately: \ a constant factor in almost linear time \ (Andoni and Nosatzki, 2020)", font_size=22,
                  color=YES),
            label(r"and for small distances: \ $O(n + d^2)$ \ (Landau and Vishkin, 1988), \ Myers' $O(nd)$ in practice",
                  font_size=22, color=LAM),
        ).arrange(DOWN, buff=0.4).next_to(head, DOWN, buff=0.6)
        with self.voiceover(
            "The other frontier is the wall that chapter twelve ran into. <bookmark mark='a'/> Edit distance, "
            "longest common subsequence and dynamic time warping have no truly subquadratic algorithms unless the "
            "strong exponential time hypothesis fails. <bookmark mark='b'/> But inputs are often compressible, and "
            "alignment can be sped up by working on Lempel–Ziv phrases instead of characters. <bookmark "
            "mark='c'/> Approximation escapes the wall entirely: a constant-factor approximation in almost linear "
            "time. <bookmark mark='d'/> And when the distance d is small, Landau and Vishkin's algorithm takes n "
            "plus d squared, the theory behind diff's speed on similar files."
        ) as vo:
            self.play(FadeIn(head))
            for mk, ln in zip("abcd", lines):
                vo.wait_until(mk)
                self.play(FadeIn(ln, shift=UP * 0.1))
        self.wait(0.3)
        self.clear_scene()

    def open_(self):
        head = label(r"Open questions", font_size=36).to_edge(UP, buff=0.35)
        qs = VGroup(
            label(r"a text index in $O(z)$ words that counts occurrences in $O(m \operatorname{polylog} n)$ time?",
                  font_size=23, color=GREY_A),
            label(r"edit distance: \ a $(1 + \varepsilon)$-approximation in near-linear time?", font_size=23,
                  color=GREY_A),
            label(r"is the runs theorem's constant tight: \ how many maximal repetitions can a string have?",
                  font_size=23, color=GREY_A),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.45).next_to(head, DOWN, buff=0.6)
        star = label(r"$\bigstar$ \ the part's research problem takes the first", font_size=22,
                     color=HEAD).to_edge(DOWN, buff=0.5)
        with self.voiceover(
            "Here is where things stand. <bookmark mark='a'/> Is there an index whose size is the number of "
            "Lempel–Ziv phrases and that counts any pattern's occurrences in time close to its length? <bookmark "
            "mark='b'/> Can edit distance be approximated to within one plus epsilon in near-linear time? <bookmark "
            "mark='c'/> And exactly how many maximal repetitions can a string of length n contain? Fewer than n, "
            "but the right constant is unknown. <bookmark mark='d'/> This part's research problem takes the first."
        ) as vo:
            self.play(FadeIn(head))
            for mk, q in zip("abc", qs):
                vo.wait_until(mk)
                self.play(FadeIn(q))
            vo.wait_until("d")
            self.play(FadeIn(star))
        self.wait(0.3)
        self.clear_scene()

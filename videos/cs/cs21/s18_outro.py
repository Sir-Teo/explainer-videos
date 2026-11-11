from __future__ import annotations

from explainer import narration_credit
from explainer.cs import *  # noqa: F403
from videos.cs.cs21.common import (BG, CODE, COST, CTRL, DATA, FUNC, HEAD, LAM, NO, PART, YES, load, mono)


def tile(content, caption, color, TW=3.6, TH=2.3):
    frame = RoundedRectangle(width=TW + 0.3, height=TH + 0.75, corner_radius=0.15, stroke_color=GREY_D,
                             stroke_width=1.5, fill_color=BG, fill_opacity=1)
    if content.width > TW:
        content.scale_to_fit_width(TW)
    if content.height > TH:
        content.scale_to_fit_height(TH)
    content.move_to(frame.get_center() + UP * 0.25)
    cap = label(caption, font_size=22, color=color).move_to(frame.get_bottom() + UP * 0.3)
    return Group(frame, content, cap)


class Outro(VoiceoverScene):
    def construct(self):
        self.recap()
        self.payoffs()
        self.practice()
        self.problems()
        self.next_time()
        self.references()

    def recap(self):
        tiles = Group(
            tile(MathTex(r"\le 2n", font_size=48, color=DATA), r"KMP's automaton", DATA),
            tile(MathTex(r"\approx n/m", font_size=48, color=YES), 'Boyer--Moore: favorable text', YES),
            tile(MathTex(r"O(m \log n)", font_size=44, color=LAM), r"suffix arrays", LAM),
            tile(mono("annb$aa", 40, HEAD), r"the BWT and FM-index", HEAD),
            tile(MathTex(r"(L, D)", font_size=48, color=CTRL), r"Lempel--Ziv; \ ANS", CTRL),
            tile(MathTex('O(N(D+1))', font_size=48, color=COST), 'Myers: \\ insertions/deletions', COST),
        ).arrange_in_grid(rows=2, cols=3, buff=(0.35, 0.35)).move_to(DOWN * 0.2)
        head = label(rf"Part {PART}: \ Strings", font_size=38).to_edge(UP, buff=0.3)
        with self.voiceover(
            "What we built in this part. Naive search and its worst case; rolling hashes; Knuth, Morris and Pratt's automaton; Boyer and Moore's skips; Aho–Corasick for many patterns. A small suffix tree and a suffix array for all the novels. The Burrows–Wheeler transform and the FM-index. Lempel–Ziv, Huffman and ANS. Alignment, Myers' diff, rsync and content-defined chunking. Periods, palindromes and Lyndon words."
        ):
            self.play(FadeIn(head))
            self.play(LaggedStart(*[FadeIn(t, shift=UP * 0.15) for t in tiles], lag_ratio=0.25), run_time=4.0)
        self.wait(0.5)
        self.clear_scene()

    def payoffs(self):
        card = payoff_card([
            (r"edit distance and SETH: \ conditional lower bounds", [27]),
            (r"information theory with noise: \ error-correcting codes", [28]),
            (r"compression in storage engines and column stores", [34, 35]),
            (r"diff, \ three-way merge and packfile deltas", [41]),
            (r"inverted indexes, \ near-duplicates, \ crawling", [47]),
            (r"Occam's razor and compression bounds", [57]),
        ], font_size=23)
        with self.voiceover(
            "Where this comes back. Part 27 proves the conditional lower bounds behind edit distance's quadratic "
            "wall. Part 28 adds noise to the information theory and builds error-correcting codes. Parts 34 and 35 compress "
            "storage engines and column stores. Part 41 builds git's merges on Myers' diff and its packfiles on "
            "delta compression. Part 47's search engine uses inverted indexes and near-duplicate detection, and "
            "Part 57 connects learning to compression."
        ):
            self.play(FadeIn(card.head), LaggedStart(*[FadeIn(r, shift=RIGHT * 0.15) for r in card.rows],
                                                     lag_ratio=0.3), run_time=3.0)
        self.wait(0.5)
        self.clear_scene()

    def practice(self):
        card = practice_card([
            (r"search", r"\texttt{grep} and \texttt{ripgrep}: \ Boyer--Moore loops, \ automata, \ and SIMD"),
            (r"compression", r"gzip and zlib \ (DEFLATE), \ bzip2 \ (BWT), \ xz \ (LZMA), \ zstd \ (LZ + ANS)"),
            (r"genomes", r"BWA and Bowtie \ (FM-index), \ BLAST \ (seeds), \ pangenome r-indexes"),
            (r"versions", r"\texttt{git diff} \ (Myers, \ patience, \ histogram), \ three-way merge"),
            (r"sync", r"rsync, \ restic and Borg \ (content-defined chunks), \ Dropbox"),
        ])
        with self.voiceover(
            'In practice, search tools choose among literal matching, automata and vectorized routines. Familiar compressors combine dictionaries, transforms and entropy coders in different ways. DNA aligners use FM-indexes or seeds. Git offers several diff strategies. Rolling checksums and content-defined chunks support synchronization and deduplication, with stronger content verification where required.'
        ):
            self.play(FadeIn(card.head), LaggedStart(*[FadeIn(r, shift=RIGHT * 0.15) for r in card.rows],
                                                     lag_ratio=0.35), run_time=3.0)
        self.wait(0.3)
        self.clear_scene()

    def problems(self):
        ps = problem_set([
            r"Prove that the KMP failure function of a pattern of length $m$ is computed in $O(m)$ time, \ and that "
            r"the search makes at most $2n$ comparisons.",
            r"Prove the LF property: \ the $k$-th occurrence of $c$ in $L$ and in $F$ are the same character of the "
            r"text, \ and deduce that inverting the BWT is correct.",
            r"Show that a text of length $n$ has exactly $\frac{n(n+1)}{2} - \sum_i \mathrm{LCP}[i]$ distinct "
            r"substrings.",
            r"Prove the Fine--Wilf theorem, \ and show the bound $p + q - \gcd(p, q)$ cannot be lowered.",
            r"\textit{Build.} \ Horspool's algorithm in the Pebble language: \ count \texttt{Queequeg} in the corpus "
            r"on the emulator, \ and compare its instructions per byte with Part 17's Job.",
            '$\\bigstar$ \\textit{Research.} \\ Reproduce a repetitive-index tradeoff: \\ allocated space, \\ count and locate; \\ audit newer results and their assumptions.',
        ], font_size=22)
        with self.voiceover(
            'Six exercises are in the notes, with worked mathematical solutions and explicit build guidance. The fifth provides a tested streaming Horspool prototype; a Pebble port and emulator instruction counts remain work for the learner, not a measured result in this video. The starred project reproduces index tradeoffs and audits dated primary papers. It does not ask you to solve a supposedly open problem whose current status has not been established.'
        ):
            self.play(FadeIn(ps.head), LaggedStart(*[FadeIn(r) for r in ps.rows], lag_ratio=0.3), run_time=3.0)
        self.wait(6.0)
        self.clear_scene()

    def next_time(self):
        nxt = label(r"Next: \ Part 22, \ Geometry", font_size=42).to_edge(UP, buff=0.6)
        items = VGroup(*[label(t, font_size=26, color=c) for t, c in (
            (r"an orientation test that floating point gets wrong", NO),
            (r"convex hulls, \ and why sorting is unavoidable", DATA),
            (r"Voronoi diagrams grown by a parabolic beach line", LAM),
            (r"Delaunay triangulations as the shadow of a hull", YES))]).arrange(DOWN, buff=0.35)
        items.move_to(UP * 0.0)
        q = label(r"get the predicates right, \ and the structure follows", font_size=26, color=GREY_A
                  ).to_edge(DOWN, buff=0.8)
        with self.voiceover(
            "Next time, geometry. It looks easy until a computer gets it wrong: a floating-point orientation test "
            "can say a point lies on both sides of a line. Get the predicates right and beautiful structure "
            "follows: convex hulls, Voronoi diagrams grown by a parabolic beach line, and Delaunay triangulations "
            "that are the shadow of a convex hull on a paraboloid. Part 22, Geometry."
        ):
            self.play(FadeIn(nxt), LaggedStart(*[FadeIn(i) for i in items], lag_ratio=0.3))
            self.play(FadeIn(q))
        self.wait(0.5)
        self.clear_scene()

    def references(self):
        card = reference_card(
            [r"Gusfield, \textit{Algorithms on Strings, Trees, and Sequences}; \ Crochemore, Hancart and Lecroq, "
             r"\textit{Algorithms on Strings}",
             r"Navarro, \textit{Compact Data Structures}; \ M\"akinen, Belazzougui, Cunial and Tomescu, "
             r"\textit{Genome-Scale Algorithm Design}",
             r"Salomon and Motta, \textit{Handbook of Data Compression}; \ Knuth, \textit{TAOCP}, \ volume 3"],
            [r"Knuth, Morris and Pratt (1977); \ Boyer and Moore (1977); \ Karp and Rabin (1987); \ Aho and Corasick "
             r"(1975)",
             r"Weiner (1973); \ Ukkonen (1995); \ Manber and Myers (1990); \ Kasai et al. (2001); \ Nong, Zhang and "
             r"Chan (2009)",
             r"Burrows and Wheeler (1994); \ Ferragina and Manzini (2000); \ Ziv and Lempel (1977, 1978); \ Duda "
             r"(2013)",
             r"Needleman and Wunsch (1970); \ Smith and Waterman (1981); \ Myers (1986); \ Tridgell and Mackerras "
             r"(1996)",
             r"Fine and Wilf (1965); \ Manacher (1975); \ Gagie, Navarro and Prezza (2018); \ Kempa and Kociumaka "
             r"(2020)"])
        credit = note(rf"narration: \ {narration_credit()}", font_size=18).to_edge(DOWN, buff=0.15)
        with self.voiceover("The books and papers this part follows are on screen and in the notes. Thank you for "
                            "watching."):
            self.play(FadeIn(card), FadeIn(credit))
        self.wait(4.0)
        self.clear_scene()

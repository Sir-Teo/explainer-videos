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
            [rf"novels: first {(d['vers_n']-1)/1e6:.1f} MB + end marker", words(d["vers_n"]), words(d["novel_runs"]),
             f"{d['vers_n'] / d['novel_runs']:.1f}"],
            [rf"{d['versions']} versions of this course's syllabus", words(d["vers_n"]), words(d["vers_runs"]),
             f"{d['vers_n'] / d['vers_runs']:.0f}"],
        ]
        tab = grid_table([r"text", r"$n$", r"BWT runs $r$", r"$n / r$"], rows, widths=[5.6, 2.4, 2.6, 1.6], row_h=0.5,
                         font_size=21, mono_cols=(), colors=[[GREY_A, GREY_A, DATA, DATA], [YES, YES, YES, YES]])
        tab.next_to(head, DOWN, buff=0.5).set_x(0)
        notes = VGroup(
            label(rf"\texttt{{xz}} squeezes {d['versions']} versions to {d['vers_xz'] / 1000:.0f} KB: \ "
                  rf"{d['vers_n'] / d['vers_xz']:.0f}$\times$", font_size=22, color=HEAD),
            label(r"collections like this are everywhere: \ versioned documents, \ source histories, \ and above all "
                  r"genomes", font_size=22, color=WHITE),
            label(r"a pangenome: \ thousands of human genomes, \ each 99.9\% like the others", font_size=22, color=LAM),
            label('fixed-order statistical entropy may miss long-range repetition; \\ run count measures something else',
                  font_size=22, color=NO),
        ).arrange(DOWN, buff=0.22).to_edge(DOWN, buff=0.4)
        pal = [DATA, LAM, YES, HEAD, CTRL, GREY_B]

        def strip(runs):
            tot = sum(n_ for _, n_ in runs)
            g = VGroup(*[Rectangle(width=12.0 * n_ / tot, height=0.34, stroke_width=0, fill_color=pal[c % len(pal)],
                                   fill_opacity=0.9) for c, n_ in runs]).arrange(RIGHT, buff=0)
            return g
        s1, s2 = strip(d["novel_strip"]), strip(d["vers_strip"])
        l1 = label(rf"480 characters of the novels' transform: \ {len(d['novel_strip'])} runs", font_size=18,
                   color=GREY_A)
        l2 = label(rf"480 characters of the syllabus versions' transform: \ {len(d['vers_strip'])} runs",
                   font_size=18, color=YES)
        VGroup(l1, s1, l2, s2).arrange(DOWN, buff=0.1).next_to(tab, DOWN, buff=0.35)
        with self.voiceover(
            f"Repetition changes what a useful index should store. <bookmark mark='a'/> We concatenate {d['versions']} captured syllabus revisions in reverse chronological git traversal order, without separators, and append one unique end marker. The comparison uses the same number of bytes from the novels, plus that marker. The table reports complete BWT run counts, not an extrapolation from these two display strips. <bookmark mark='b'/> xz's emitted size is checked by decoding it; the compression ratio is for this exact snapshot. <bookmark mark='c'/> Versioned documents and source histories commonly contain this kind of reuse. <bookmark mark='d'/> Genomic collections are another motivation, although this experiment measures no genome data. <bookmark mark='e'/> Fixed-order statistical entropy can miss long-range copies. BWT run count and phrase count capture different kinds of repetitiveness."
        ) as vo:
            self.play(FadeIn(head), FadeIn(VGroup(*tab.cells[0])), FadeIn(tab.rule))
            vo.wait_until("a")
            self.play(LaggedStart(*[FadeIn(VGroup(*r)) for r in tab.cells[1:]], lag_ratio=0.5))
            self.play(FadeIn(l1), Create(s1), run_time=1.5)
            self.play(FadeIn(l2), Create(s2), run_time=1.0)
            for mk, n_ in zip("bcde", notes):
                vo.wait_until(mk)
                self.play(FadeIn(n_))
        self.wait(0.3)
        self.clear_scene()

    def rindex(self):
        head = label(r"The r-index", font_size=36).to_edge(UP, buff=0.35)
        lines = VGroup(
            label('run-length BWT: \\ rank uses run prefixes and the partial run at each queried row', font_size=22,
                  color=WHITE),
            label(r"the hard part was \textbf{locate}: \ suffix-array samples cost $n / s$, \ not $O(r)$", font_size=22,
                  color=NO),
            label('Gagie--Navarro--Prezza (2018/2020): \\ $O(r)$ words; \\ $O(\\log\\log n)$ per occurrence after search', font_size=22, color=YES),
            label(r"move structures \ (Nishimoto and Tabei, 2021): \ LF in constant time, \ in $O(r)$ space",
                  font_size=22, color=LAM),
            label(r"how big is $r$? \ Kempa and Kociumaka (2020): \ $r = O(z \log^2 n)$, \ $z$ = LZ77's phrases",
                  font_size=22, color=HEAD),
            label('$\\delta\\le\\gamma\\le b\\le z$; \\ $r$ and $z$ are incomparable; \\ no universal $z\\le r$',
                  font_size=20, color=GREY_A),
        ).arrange(DOWN, buff=0.32).next_to(head, DOWN, buff=0.5)
        with self.voiceover(
            "A run-length index stores structure proportional to r. <bookmark mark='a'/> Rank at any queried row combines counts before its run with the partial run; predecessor search finds that run. <bookmark mark='b'/> Periodic suffix-array samples alone cost n over s, so locating needs a different representation to fit run-bounded space. <bookmark mark='c'/> Gagie, Navarro and Prezza's 2018 work, published in 2020, uses run-boundary samples with additional structures. On their word-RAM model, order r words support locating at log log n per occurrence after the pattern-search cost. <bookmark mark='d'/> Later move structures support constant-time LF within order r space. These are theoretical results, not implementations measured in this part. <bookmark mark='e'/> Kempa and Kociumaka's 2020 result bounds r by order z times log squared n. Here z uses the paper's unbounded LZ77 convention, not our fixed-window parser's token count. <bookmark mark='f'/> Delta, attractors, macro schemes and LZ give one hierarchy. But r and z are incomparable; they do not form the simple ladder z less than or equal to r."
        ) as vo:
            self.play(FadeIn(head), FadeIn(lines[0]))
            for mk, ln in zip("abcdef", lines):
                vo.wait_until(mk)
                self.play(Indicate(ln, color=WHITE) if mk == "a" else FadeIn(ln, shift=UP * 0.1))
        self.wait(0.3)
        self.clear_scene()

    def lower(self):
        head = label(r"And the quadratic wall", font_size=34).to_edge(UP, buff=0.35)
        lines = VGroup(
            label('2015: \\ exact unit-cost edit distance has no truly subquadratic algorithm under SETH', font_size=22, color=NO),
            label(r"on compressible inputs: \ alignment speeds up with the compression \ (Crochemore, \ Landau and "
                  r"Ziv-Ukelson, \ 2003)", font_size=22, color=WHITE),
            label('Andoni--Nosatzki (2020): \\ randomized factor $C_\\eta$, \\ time $n^{1+\\eta}$ for fixed $\\eta>0$', font_size=22,
                  color=YES),
            label('this part: \\ Myers uses $O(N(D+1))$, \\ insertion/deletion distance $D$; \\ distinct from Levenshtein',
                  font_size=22, color=LAM),
        ).arrange(DOWN, buff=0.4).next_to(head, DOWN, buff=0.6)
        with self.voiceover(
            "Here are selected dated results, rather than a complete current frontier. <bookmark mark='a'/> Backurs and Indyk's 2015 conditional lower bound concerns exact unit-cost edit distance in the worst case. It is not a lower bound for every biological score or every compressible input. <bookmark mark='b'/> Compression can speed up alignment on structured instances. <bookmark mark='c'/> Andoni and Nosatzki's 2020 randomized approximation takes n to the one plus eta, for each fixed positive eta, with an approximation constant depending on eta. That is not a claim of n times polylog n time. <bookmark mark='d'/> Our implemented distance-sensitive method is Myers: order N times the quantity D plus one for insertion-and-deletion distance. Unit-cost Levenshtein distance also allows substitutions, so it is a different problem."
        ) as vo:
            self.play(FadeIn(head), FadeIn(lines[0]))
            for mk, ln in zip("abcd", lines):
                vo.wait_until(mk)
                self.play(Indicate(ln, color=WHITE) if mk == "a" else FadeIn(ln, shift=UP * 0.1))
        self.wait(0.3)
        self.clear_scene()

    def open_(self):
        head = label('Research directions: \\ verify the model and the date', font_size=36).to_edge(UP, buff=0.35)
        qs = VGroup(
            label('compare actual index space, \\ construction, \\ count and locate costs separately',
                  font_size=23, color=GREY_A),
            label('for approximation: \\ record factor, \\ exponent, \\ randomness and error probability', font_size=23,
                  color=GREY_A),
            label('for repetitiveness: \\ fix sentinels, \\ parse conventions, \\ units and input families',
                  font_size=23, color=GREY_A),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.45).next_to(head, DOWN, buff=0.6)
        star = label('$\\bigstar$ \\ reproduce a dated tradeoff; \\ check newer primary work before claiming an open problem', font_size=22,
                     color=HEAD).to_edge(DOWN, buff=0.5)
        with self.voiceover(
            "A useful research project begins with precise questions. <bookmark mark='a'/> Compare space and construction costs, then count and locate separately, on fixed text families. <bookmark mark='b'/> For any approximation result, record its factor, running-time exponent, randomness and success probability. <bookmark mark='c'/> For repetitive indexes, fix sentinels, parsing conventions and whether space means bits, machine words or allocated bytes. <bookmark mark='d'/> The starred exercise asks for a reproducible tradeoff study and a dated literature review. Before declaring a question open, check newer primary work; the historical results in this chapter are not a claim about the latest boundary."
        ) as vo:
            self.play(FadeIn(head))
            for mk, q in zip("abc", qs):
                vo.wait_until(mk)
                self.play(FadeIn(q))
            vo.wait_until("d")
            self.play(FadeIn(star))
        self.wait(0.3)
        self.clear_scene()

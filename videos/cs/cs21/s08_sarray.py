from __future__ import annotations

from explainer.cs import *  # noqa: F403
from videos.cs.cs21.common import (CTRL, DATA, HEAD, LAM, NO, PART, YES, big, grid_table, load, mono, words)


class SuffixArray(VoiceoverScene):
    def construct(self):
        self.card()
        self.sorted_()
        self.build()
        self.measured()

    def card(self):
        card = chapter_card(7, r"Suffix arrays", r"What if we just sort the suffixes?", lit=(1990,),
                            extra=((1990, r"Manber--Myers"),), part=PART)
        with self.voiceover("Chapter seven. Suffix arrays."):
            self.play(FadeIn(card[0], shift=UP * 0.2), FadeIn(card[1]), FadeIn(card[2]))
        self.play(FadeOut(card))

    def sorted_(self):
        d = load("sa")
        head = label(r"Sort the suffixes, \ keep only their starts", font_size=34).to_edge(UP, buff=0.3)
        sa = d["small_sa"]
        suf = d["small_suffixes"]
        rows = VGroup()
        for k in range(len(sa)):
            r = VGroup(mono(f"{sa[k]:>2}", 16, YES), mono(suf[k].replace(" ", "␣"), 16, WHITE)).arrange(RIGHT,
                                                                                                         buff=0.3)
            rows.add(r)
        rows.arrange(DOWN, aligned_edge=LEFT, buff=0.04)
        if rows.height > 6.2:
            rows.scale_to_fit_height(6.2)
        rows.to_edge(LEFT, buff=0.8).shift(DOWN * 0.3)
        hl = VGroup(*[SurroundingRectangle(rows[k], color=HEAD, buff=0.03, stroke_width=1.5)
                      for k in range(len(sa)) if suf[k].startswith("t")])
        side = VGroup(
            label(rf"\texttt{{{d['small'].replace('$', chr(92) + '$')}}}: \ {len(sa)} suffixes, \ sorted", font_size=21,
                  color=WHITE),
            label(r"the suffix array is just the green column: \ $n$ integers", font_size=21, color=YES),
            label(r"all occurrences of a pattern are \textbf{adjacent}: \ every suffix starting with \texttt{t}",
                  font_size=21, color=HEAD),
            label(r"so: \ two binary searches, \ $O(m \log n)$ character comparisons", font_size=21, color=DATA),
            label(r"Manber and Myers (1990); \ Gonnet, Baeza-Yates and Snider (1992)", font_size=19, color=GREY_B),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.3).to_edge(RIGHT, buff=0.5)
        if side.width > 6.4:
            side.width = 6.4
            side.to_edge(RIGHT, buff=0.5)
        with self.voiceover(
            "Udi Manber and Gene Myers kept the suffix tree's power with far less memory. <bookmark mark='a'/> Take "
            "every suffix of the text and sort them, in dictionary order. <bookmark mark='b'/> Then throw the "
            "suffixes away and keep only where each one starts: an array of n integers, the suffix array. "
            "<bookmark mark='c'/> Every occurrence of a pattern is the beginning of some suffix, and suffixes "
            "beginning with the same pattern are next to each other in sorted order. Here, the four suffixes that "
            "start with t. <bookmark mark='d'/> So two binary searches find the block, with m times log n "
            "character comparisons at most, and the block's size is the number of occurrences."
        ) as vo:
            self.play(FadeIn(head))
            vo.wait_until("a")
            self.play(LaggedStart(*[FadeIn(r[1]) for r in rows], lag_ratio=0.05), FadeIn(side[0]))
            vo.wait_until("b")
            self.play(LaggedStart(*[FadeIn(r[0]) for r in rows], lag_ratio=0.05), FadeIn(side[1]))
            vo.wait_until("c")
            self.play(Create(hl), FadeIn(side[2]))
            vo.wait_until("d")
            self.play(FadeIn(side[3]), FadeIn(side[4]))
        self.wait(0.3)
        self.clear_scene()

    def build(self):
        head = label(r"Building it: \ prefix doubling", font_size=34).to_edge(UP, buff=0.35)
        lines = VGroup(
            label(r"rank every suffix by its first character", font_size=22, color=WHITE),
            label(r"rank by the first $2k$ characters \ = \ sort the pairs $(\text{rank}_k(i),\ \text{rank}_k(i + k))$",
                  font_size=22, color=LAM),
            label(r"$k = 1, 2, 4, 8, \dots$ \ until every rank is different: \ $O(n \log n)$ with radix sort", font_size=22,
                  color=WHITE),
            label(r"SA-IS \ (Nong, \ Zhang and Chan, \ 2009): \ linear time, \ by sorting a sample of suffixes "
                  r"recursively", font_size=22, color=HEAD),
            label(r"the \textbf{LCP array}: \ common prefix of each sorted neighbour pair, \ in linear time \ (Kasai et "
                  r"al., 2001)", font_size=22, color=YES),
            label(r"suffix array + LCP array \ = \ everything the suffix tree answered \ (Abouelhoda, Kurtz and "
                  r"Ohlebusch, 2004)", font_size=20, color=GREY_A),
        ).arrange(DOWN, buff=0.32).next_to(head, DOWN, buff=0.5)
        with self.voiceover(
            "How do you sort twenty-five million suffixes, each up to twenty-five million characters long? "
            "<bookmark mark='a'/> Rank them first by one character. <bookmark mark='b'/> Then notice that ranking "
            "by the first two k characters is the same as sorting pairs: the rank of the suffix's first k "
            "characters, and the rank of the k characters after them, which is the rank of another suffix. "
            "<bookmark mark='c'/> Double k until every suffix has its own rank: log n rounds of sorting. <bookmark "
            "mark='d'/> Linear-time algorithms exist too; SA-IS, from 2009, sorts a sample of the suffixes "
            "recursively and induces the rest, and it is what fast libraries use. <bookmark mark='e'/> Alongside, "
            "keep the longest common prefix of each pair of neighbours in sorted order, which Kasai and colleagues "
            "showed how to compute in linear time. <bookmark mark='f'/> With both arrays, every question the "
            "suffix tree answered can be answered again, in a quarter of the memory."
        ) as vo:
            self.play(FadeIn(head))
            for mk, ln in zip("abcdef", lines):
                vo.wait_until(mk)
                self.play(FadeIn(ln, shift=UP * 0.1))
        self.wait(0.3)
        self.clear_scene()

    def measured(self):
        d = load("sa")
        head = label(r"The suffix array of the novels", font_size=34).to_edge(UP, buff=0.35)
        stats = VGroup(
            label(rf"{words(d['n'])} suffixes, \ sorted by prefix doubling in numpy: \ {d['t_sa']:.0f} s", font_size=22,
                  color=WHITE),
            label(rf"{d['bytes_sa'] / 1e6:.0f} MB: \ 4 bytes per character", font_size=22, color=LAM),
        ).arrange(DOWN, buff=0.2).next_to(head, DOWN, buff=0.4)
        rows = [[s["pattern"], words(s["count"]), words(s["cmp"]), f"{s['bound']:.0f}"] for s in d["searches"]]
        tab = grid_table([r"pattern", r"occurrences", r"character comparisons", r"$2m \log_2 n$"], rows,
                         widths=[3.6, 2.4, 3.6, 2.2], row_h=0.46, font_size=21, mono_cols=(0,),
                         colors=[[DATA, YES, HEAD, GREY_A]] * len(rows)).next_to(stats, DOWN, buff=0.5)
        tab.set_x(0)
        lcp = label(rf"\textit{{Moby-Dick}}'s LCP array: \ {d['t_lcp']:.1f} s in Python; \ neighbours share "
                    rf"{d['md_mean_lcp']:.1f} characters on average", font_size=21, color=YES).next_to(tab, DOWN,
                                                                                                     buff=0.5)
        with self.voiceover(
            f"We built the suffix array of all {words(d['n'])} characters of the novels, by prefix doubling with "
            "numpy's sorts, in under two minutes. <bookmark mark='a'/> It takes a hundred megabytes, four bytes "
            "for every character. <bookmark mark='b'/> Now any pattern is a pair of binary searches: Queequeg's "
            "two hundred and fifty-three occurrences were found with a hundred and sixty-seven character "
            "comparisons, against twenty-five million for a scan. <bookmark mark='c'/> And Moby-Dick's LCP array "
            "says that neighbouring suffixes share eight characters on average, which is why the binary search "
            "rarely compares more than a few characters per step."
        ) as vo:
            self.play(FadeIn(head), FadeIn(stats[0]))
            vo.wait_until("a")
            self.play(FadeIn(stats[1]))
            vo.wait_until("b")
            self.play(FadeIn(VGroup(*tab.cells[0])), FadeIn(tab.rule),
                      LaggedStart(*[FadeIn(VGroup(*r)) for r in tab.cells[1:]], lag_ratio=0.3))
            vo.wait_until("c")
            self.play(FadeIn(lcp))
        self.wait(0.3)
        self.clear_scene()

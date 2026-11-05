from __future__ import annotations

from explainer.cs import *  # noqa: F403
from videos.cs.cs21.common import (COST, CTRL, DATA, HEAD, LAM, NO, PART, YES, big, grid_table, load, mono, words)


class Hook(VoiceoverScene):
    def construct(self):
        self.search()
        self.more()
        self.plan()

    def search(self):
        d = load("hook")
        head = label(rf"Find \texttt{{{d['pattern']}}} \ in 25 MB of novels", font_size=36).to_edge(UP, buff=0.35)
        rows = [
            [r"compare at every position", words(d["naive_cmp"]), r"chapter 1"],
            [r"Knuth--Morris--Pratt: \ never look back", words(d["kmp_cmp"]), r"chapter 3"],
            [r"Boyer--Moore: \ skip ahead", words(d["bm_cmp"]), r"chapter 4"],
            [r"FM-index: \ search the transformed text", rf"{d['fm_ranks']} \ (rank queries)", r"chapter 9"],
        ]
        tab = grid_table([r"method", r"comparisons", r""], rows, widths=[6.0, 3.6, 1.8], row_h=0.6, font_size=22,
                         mono_cols=(), colors=[[NO] * 3, [DATA] * 3, [LAM] * 3, [YES] * 3]).next_to(head, DOWN, buff=0.5)
        tab.set_x(0)
        res = label(rf"{d['hits']} occurrences; \ the index answers in {d['t_fm'] * 1000:.2f} ms, \ after building it once",
                    font_size=22, color=HEAD).to_edge(DOWN, buff=0.7)
        with self.voiceover(
            "Queequeg, the harpooner of Moby-Dick. Where does his name appear in the thirty novels, twenty-five "
            "megabytes of text? <bookmark mark='a'/> The obvious method compares the name against the text at "
            "every position: about twenty-five million character comparisons, roughly one per character. "
            "<bookmark mark='b'/> Knuth, Morris and Pratt's algorithm guarantees it never needs more than two "
            "per character, and never looks back. <bookmark mark='c'/> Boyer and Moore's algorithm looks at the "
            "end of the name first and skips ahead: three and a half million comparisons, seven times fewer. "
            "<bookmark mark='d'/> And an index built from a strange permutation of the text, the Burrows–Wheeler "
            "transform, answers with sixteen small table lookups, independent of the length of the novels. "
            f"<bookmark mark='e'/> All four find the same {d['hits']} occurrences."
        ) as vo:
            self.play(FadeIn(head), FadeIn(VGroup(*tab.cells[0])), FadeIn(tab.rule))
            for mk, r in zip("abcd", tab.cells[1:]):
                vo.wait_until(mk)
                self.play(FadeIn(VGroup(*r), shift=RIGHT * 0.1))
            vo.wait_until("e")
            self.play(FadeIn(res))
        self.wait(0.3)
        self.clear_scene()

    def more(self):
        lz = load("lz")
        df = load("diff")
        head = label(r"Text is the oldest data", font_size=36).to_edge(UP, buff=0.4)
        rows = VGroup(*[VGroup(label(a, font_size=26, color=c), label(b, font_size=21, color=GREY_A)).arrange(
            DOWN, buff=0.12) for a, b, c in (
            (r"search it", r"automata from patterns; \ indexes of every suffix", DATA),
            (r"compress it", rf"the novels: \ 25 MB to {lz['corpus_zlib'] / 1e6:.1f} MB with zlib; \ less with a "
                             r"sorting transform", LAM),
            (r"compare it", rf"\texttt{{git diff}} is a shortest path on a grid: \ {df['revisions']} versions of this "
                            r"course's syllabus", YES),
            (r"synchronize it", r"rsync and backups: \ send only what changed, \ found with rolling hashes", CTRL),
        )]).arrange(DOWN, buff=0.4).next_to(head, DOWN, buff=0.55)
        with self.voiceover(
            "Text is the oldest kind of data, and this part is about four things we do to it. <bookmark mark='a'/> "
            "We search it, with automata built from patterns and with indexes of every suffix. <bookmark "
            "mark='b'/> We compress it. zlib squeezes the novels to about a third, and a transform that sorts the "
            "text does better. <bookmark mark='c'/> We compare it: every git diff computes a shortest path on a "
            "grid, and we will run one on the history of this course's own syllabus. <bookmark mark='d'/> And we "
            "synchronize it, sending only what changed, found with the rolling hashes of Part 20."
        ) as vo:
            self.play(FadeIn(head))
            for mk, r in zip("abcd", rows):
                vo.wait_until(mk)
                self.play(FadeIn(r, shift=UP * 0.1))
        self.wait(0.3)
        self.clear_scene()

    def plan(self):
        title = label(rf"Part {PART}: \ Strings", font_size=46).to_edge(UP, buff=0.4)
        smap = series_map(current=PART, done=PART - 1).scale(0.92).next_to(title, DOWN, buff=0.35)
        obj = objectives_card([
            r"matching: \ naive, \ rolling hashes, \ KMP's automaton, \ Boyer--Moore, \ Aho--Corasick",
            r"suffix trees and suffix arrays, \ built for all 25 MB of the novels",
            r"the Burrows--Wheeler transform and the FM-index: \ search without decompressing",
            r"compression: \ Lempel--Ziv, \ Huffman and ANS, \ against zlib, \ bzip2 and xz",
            r"alignment, \ Myers' diff on this repository, \ rsync and content-defined chunks",
            r"periods and palindromes; \ the frontier: \ indexes as small as the information",
        ], font_size=26).move_to(DOWN * 0.2)
        with self.voiceover(
            "Part 21 of Computer Science, Built: Strings. <bookmark mark='a'/> In this part: five ways to find a "
            "pattern; suffix trees and suffix arrays, built for the whole corpus; the Burrows–Wheeler transform and "
            "the FM-index, which searches text without decompressing it; Lempel–Ziv compression and the entropy "
            "coders behind it; alignment, diff and rsync; periods and palindromes; and indexes as small as the "
            "information in the text."
        ) as vo:
            self.play(FadeIn(title), FadeIn(smap))
            vo.wait_until("a")
            self.play(FadeOut(smap), FadeIn(obj))
        self.wait(0.5)
        self.clear_scene()

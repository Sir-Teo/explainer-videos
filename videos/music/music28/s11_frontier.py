from __future__ import annotations

import numpy as np

from videos.music.music28.common import *  # noqa: F403


class Frontier(SoundScene):
    def construct(self):
        chapter(self, 10, r"Frontier: \ is it octatonic?", r"How would you know a passage was written in a scale?")
        self.debate()
        self.chance()
        self.forte()
        self.problem()

    # ------------------------------------------------------------------
    def debate(self):
        items = [
            (r"Pieter van den Toorn \ (1983), \ Richard Taruskin \ (1996): \ the octatonic as a key to Stravinsky", WHITE),
            (r"they find long passages whose notes all lie in one octatonic collection", WHITE),
            (r"Dmitri Tymoczko \ (2002): \ many of those passages fit other explanations as well, \ or better", WHITE),
            (r"for example, \ two diatonic layers superimposed, \ or modal scales", TUNE),
            (r"the question underneath: \ how often would a passage fit by chance?", EAR),
        ]
        rows_scene(self, r"the octatonic debate", items,
                   "Chapter four promised an argument. <bookmark mark='b'/> The theorist Pieter van den Toorn, in 1983, and the "
                   "historian Richard Taruskin made the octatonic scale a key to Stravinsky's music, <bookmark mark='c'/> "
                   "finding long passages whose notes all lie in one octatonic collection. <bookmark mark='d'/> In 2002 Dmitri "
                   "Tymoczko argued that many of those passages fit other explanations as well or better, "
                   "<bookmark mark='e'/> for instance two diatonic layers laid on top of each other. <bookmark mark='f'/> "
                   "Underneath is a statistical question: how often would a passage fit a scale by chance?", marks="cdef")

    # ------------------------------------------------------------------
    def chance(self):
        d = load("octatonic")
        ks = d["ks"]
        ax = Axes(x_range=[2, 9, 1], y_range=[0, 1, 0.25], x_length=7.6, y_length=4.0, tips=False,
                  axis_config={"color": GREY_B, "include_numbers": True, "font_size": 18}).move_to(LEFT * 2.0 + DOWN * 0.3)
        cols = {"octatonic": TUNE, "diatonic": BLUE, "whole-tone": EAR}
        lines = {k: ax.plot_line_graph(ks, d["chance"][k], line_color=c_, add_vertex_dots=True, stroke_width=4) for k, c_ in cols.items()}
        xl = label(r"how many different pitch classes the passage uses", font_size=18, color=GREY_A).next_to(ax, DOWN, buff=0.25)
        yl = label(r"share of all such sets that fit some transposition", font_size=18, color=GREY_A).next_to(ax.y_axis, UP, buff=0.2).shift(RIGHT * 1.8)
        key = VGroup(*[label(k, font_size=20, color=c_) for k, c_ in cols.items()]).arrange(DOWN, buff=0.2, aligned_edge=LEFT).move_to(ax.c2p(7.2, 0.85))
        o = d["chance"]["octatonic"]
        dd = d["chance"]["diatonic"]
        side = VGroup(*[label(s, font_size=21, color=c_) for s, c_ in (
            (rf"4 pitch classes: \ octatonic {100 * o[1]:.0f}, \ diatonic {100 * dd[1]:.0f} in 100", WHITE),
            (rf"6 pitch classes: \ {100 * o[3]:.0f} and {100 * dd[3]:.0f}", WHITE),
            (rf"7: \ {100 * o[4]:.0f} and {100 * dd[4]:.1f}", WHITE),
            (r"few pitch classes often fit several scales", EAR))]).arrange(DOWN, buff=0.35, aligned_edge=LEFT)
        side.scale_to_fit_width(min(side.width, 4.6))
        side.move_to(RIGHT * 4.4 + DOWN * 0.2)
        with self.voiceover(
            f"Here is the chance, computed exactly. Take every possible set of k pitch classes, and ask what share of them lies inside some octatonic scale, some diatonic scale, or some whole-tone scale. <bookmark mark='a'/> A passage using four pitch classes fits an octatonic scale {say(round(100 * o[1]))} times in a hundred by chance, and a diatonic one {say(round(100 * dd[1]))} times. <bookmark mark='b'/> With six pitch classes, {say(round(100 * o[3]))} and {say(round(100 * dd[3]))}. <bookmark mark='c'/> With seven, the octatonic still catches {say(round(100 * o[4]))} in a hundred and the diatonic hardly any. <bookmark mark='d'/> So a short passage that fits a scale proves little; many distinct pitch classes fitting one collection is more selective under this uniform-set null; musical controls and segmentation choices still matter."
        ) as vo:
            self.play(Create(ax), FadeIn(xl), FadeIn(yl), FadeIn(key), *[Create(l_) for l_ in lines.values()])
            for mark, r in zip("abcd", side):
                vo.wait_until(mark)
                self.play(FadeIn(r))
        self.wait(0.4)
        self.clear_scene()

    # ------------------------------------------------------------------
    def problem(self):
        rows_ = text_rows([
            (r"segment a score into passages; \ for each, \ find the best-fitting collection by duration", WHITE),
            (r"compare with a null: \ new pitch-class assignments preserving passage cardinality, or a musically motivated control; permuting the same notes cannot change set containment, \ or other composers' music", WHITE),
            (r"weigh the explanations: \ one octatonic collection, \ two diatonic layers, \ a mode", WHITE),
            (r"$\bigstar$ \ research problem: \ how much of a repertoire is octatonic beyond chance, \ and where?", EAR),
            (r"a model comparison, \ not a list of examples, \ would settle part of an old argument", TUNE),
        ])
        head = label(r"a research problem", font_size=30, color=GREY_A).to_edge(UP, buff=0.45)
        with self.voiceover(
            "A concrete version. <bookmark mark='a'/> Cut a score into passages and find, for each, the collection that "
            "holds the most of its sounding time. <bookmark mark='b'/> Compare with a null: the same passages with their "
            "pitch classes shuffled, or music by other composers. <bookmark mark='c'/> Weigh the rival explanations, one "
            "octatonic collection, two diatonic layers, a mode, by how well each fits and how much it assumes. "
            "<bookmark mark='d'/> How much of a repertoire is octatonic beyond chance, and where? <bookmark mark='e'/> A "
            "model comparison rather than a list of examples would settle part of an old argument."
        ) as vo:
            self.play(FadeIn(head), FadeIn(rows_[0]))
            for mark, r in zip("bcde", rows_[1:]):
                vo.wait_until(mark)
                self.play(FadeIn(r))
        self.wait(0.4)
        self.clear_scene()

    # ------------------------------------------------------------------
    def forte(self):
        items = [
            (r"Allen Forte, \ \textit{The Structure of Atonal Music} \ (1973): \ pitch-class sets in his catalogued cardinalities named and numbered", WHITE),
            (r"up to transposition and inversion: \ 224 set classes \ (chapter two counted 352 without inversion)", WHITE),
            (r"analysis as segmentation: \ which notes belong together? \ the analyst decides", WHITE),
            (r"computational studies now segment automatically and compare corpora", TUNE),
            (r"the same caution: \ a pattern found must be compared with what chance finds", GREY_A),
        ]
        rows_scene(self, r"sets as data", items,
                   "This kind of counting has a history in music theory. <bookmark mark='b'/> In 1973 Allen Forte named and numbered pitch-class sets in his catalogued cardinalities, <bookmark mark='c'/> up to transposition and inversion: two hundred and twenty-four classes when all cardinalities, including empty and full sets, are counted, against the three hundred and fifty-two chapter two counted without inversion. <bookmark mark='d'/> His analysis depends on segmentation, deciding which notes belong together, and the analyst decides. <bookmark mark='e'/> Computational studies now segment automatically and compare whole corpora, <bookmark mark='f'/> and the same caution applies to them: a pattern found must be compared with what chance would find.", marks="cdef")

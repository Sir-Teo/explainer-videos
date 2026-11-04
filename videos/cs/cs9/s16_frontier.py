from __future__ import annotations

import numpy as np

from explainer.cs import *  # noqa: F403
from videos.cs.cs9.common import (BG, CODE, COST, CTRL, DATA, FUNC, HEAD, HIST, INF, NO, PART, YES, bar_chart, fmt,
                                  load)


class Frontier(VoiceoverScene):
    """The research tier (videos/cs/SYLLABUS.md 1.1): how close can a real replacement policy come to Belady, and
    what do learned policies do?"""

    def construct(self):
        self.card()
        self.insertion()
        self.learned()
        self.now()

    def card(self):
        card = chapter_card(15, r"Frontier: \ learning to replace", r"How close can a cache come to the crystal ball?",
                            lit=(2007, 2016, 2019), extra=((2007, r"adaptive insertion"), (2016, r"Hawkeye"),
                                                           (2019, r"Glider")), part=PART)
        with self.voiceover("Chapter fifteen. Frontier: learning to replace."):
            self.play(FadeIn(card[0], shift=UP * 0.2), FadeIn(card[1]), FadeIn(card[2]))
        self.play(FadeOut(card))

    def insertion(self):
        d = load("frontier")
        head = label(r"Where to put a new line? \ The Job's scans, \ scaled down", font_size=32).to_edge(UP, buff=0.3)
        r = d["rows"]
        vals = [100 * r[k] for k in ("lru", "random", "bip", "opt")]
        ch = bar_chart(vals, [r"LRU", r"random", r"bimodal \\ insertion", r"Belady"], [NO, FUNC, DATA, YES], height=3.2,
                       bar_w=1.2, gap=1.1, font_size=22, fmt_=lambda v: rf"{v:.0f}\%").move_to(DOWN * 0.3)
        cap = note(rf"the first {d['words']:,} words of the corpus, \ {d['accesses'] / 1e6:.2f} million line reads, \ "
                   rf"a cache of {d['cache_lines']} lines", font_size=18).next_to(ch, UP, buff=0.3)
        rule = label(r"bimodal insertion: \ put a new line at the \textit{least}-recently-used end, \ except once in 32",
                     font_size=24, color=DATA).to_edge(DOWN, buff=0.4)
        with self.voiceover(
            "LRU fails on the Job because it trusts recency: every new line from a long scan goes to the top of the "
            "list, pushing out lines that will be needed soon. In 2007 Moinuddin Qureshi and colleagues proposed a "
            "small change. <bookmark mark='a'/> On a scaled-down version of the Job's scans, LRU misses sixty-four "
            "percent. Random replacement, fifty-five. <bookmark mark='b'/> Bimodal insertion puts a new line at the "
            "bottom of the list instead, where it will be the next to go unless it is used again, and only once in "
            "thirty-two at the top. A scan then sweeps through the bottom slot while the rest of the cache keeps the "
            "front of the table: forty-seven percent. Their adaptive version picks between the two policies by "
            "watching which does better. <bookmark mark='c'/> And Belady's crystal ball, thirty-three. Half the gap "
            "closed by one rule."
        ) as vo:
            self.play(FadeIn(head), FadeIn(cap), FadeIn(ch[0]))
            for mk, ks in (("a", [0, 1]), ("b", [2]), ("c", [3])):
                vo.wait_until(mk)
                self.play(*[GrowFromEdge(ch.bars[k], DOWN) for k in ks], *[FadeIn(ch.vals[k]) for k in ks],
                          *[FadeIn(ch.names[k]) for k in ks])
                if mk == "b":
                    self.play(FadeIn(rule))
        self.wait(0.3)
        self.clear_scene()

    def learned(self):
        head = label(r"Learning from Belady", font_size=38).to_edge(UP, buff=0.4)
        items = VGroup(
            label(r"Hawkeye \ (Jain and Lin, \ 2016): \ replay the recent past with Belady's policy, \ and learn, \ per "
                  r"instruction, \ whether its lines were worth keeping", font_size=23, color=DATA),
            label(r"Glider \ (Shi et al., \ 2019): \ train a deep network offline on traces; \ distil what it learned "
                  r"into a few hundred integer weights", font_size=23, color=YES),
            label(r"the champions of the Cache Replacement Championship: \ predictors, \ like Part 7's branch "
                  r"predictors", font_size=23, color=HEAD),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.4).move_to(DOWN * 0.1)
        with self.voiceover(
            "Bimodal insertion is one fixed rule. The research since then learns the rule. <bookmark mark='a'/> In "
            "2016 Akanksha Jain and Calvin Lin built Hawkeye. It cannot see the future, but it can replay the recent "
            "past: it runs Belady's policy on the last few thousand accesses to see which lines would have been worth "
            "keeping, and learns, for each load instruction, whether the lines it brings in tend to be. <bookmark "
            "mark='b'/> In 2019 their group trained a deep recurrent network offline on memory traces, found that "
            "what it learned could be captured by a few hundred integer weights, and built that into a policy called "
            "Glider. <bookmark mark='c'/> Replacement policy has become prediction, the same kind of problem as Part "
            "7's branch predictors, scored in public championships."
        ) as vo:
            self.play(FadeIn(head))
            for mk, it in zip("abc", items):
                vo.wait_until(mk)
                self.play(FadeIn(it, shift=RIGHT * 0.1))
        self.wait(0.3)
        self.clear_scene()

    def now(self):
        head = label(r"Open questions", font_size=40).to_edge(UP, buff=0.4)
        items = VGroup(
            label(r"how close can any online policy come to Belady \ on a given kind of program?", font_size=24,
                  color=YES),
            label(r"pebble games beyond matrix multiply: \ tight bounds for graphs, \ sparse problems, \ neural "
                  r"networks", font_size=24, color=HEAD),
            label(r"memory far away on purpose: \ disaggregated memory over CXL, \ hundreds of nanoseconds more",
                  font_size=24, color=CTRL),
            label(r"processing in memory: \ moving the arithmetic to the data instead", font_size=24, color=DATA),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.38).move_to(DOWN * 0.1)
        with self.voiceover(
            "Where the research stands. <bookmark mark='a'/> How close can any policy that sees only the past come to "
            "Belady's? For some programs the gap closes; nobody can say in general. <bookmark mark='b'/> The pebble "
            "game's tight bounds are known for matrix multiplication and a few relatives; for graph algorithms, "
            "sparse computations and the layers of a neural network, mostly not. <bookmark mark='c'/> Data centres "
            "now put memory deliberately further away, in shared pools reached over links like CXL, trading hundreds "
            "of nanoseconds for flexibility. <bookmark mark='d'/> And some designs give up on moving data at all, "
            "putting arithmetic inside the memory chips. The research problem for this part starts with the Job's own "
            "scans."
        ) as vo:
            self.play(FadeIn(head))
            for mk, it in zip("abcd", items):
                vo.wait_until(mk)
                self.play(FadeIn(it, shift=RIGHT * 0.1))
        self.wait(0.3)
        self.clear_scene()

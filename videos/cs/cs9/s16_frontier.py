from __future__ import annotations

import numpy as np

from explainer.cs import *  # noqa: F403
from videos.cs.cs9.common import (BG, CODE, COST, CTRL, DATA, FUNC, HEAD, HIST, INF, NO, PART, YES, bar_chart, box, fmt,
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
        with self.voiceover(
            "Chapter fifteen. Frontier: learning to replace."
        ):
            self.play(FadeIn(card[0], shift=UP * 0.2), FadeIn(card[1]), FadeIn(card[2]))
        self.play(FadeOut(card))

    def insertion(self):
        d = load("frontier")
        head = label(r"Where to put a new line? \ The Job's scans, \ scaled down", font_size=32).to_edge(UP, buff=0.3)
        r = d["rows"]
        vals = [100 * r[k] for k in ("lru", "random", "bip", "opt")]
        ch = bar_chart(vals, [r"LRU", r"random", r"bimodal \\ insertion", r"Belady"], [NO, FUNC, DATA, YES], height=3.2,
                       bar_w=1.2, gap=1.1, font_size=22, fmt_=lambda v: rf"{v:.0f}\%").move_to(DOWN * 0.3)
        cap = note(rf"first {d['words']:,} words: \ {d['accesses'] / 1e6:.2f} million approximate line events; \ "
                   rf"a cache of {d['cache_lines']} lines", font_size=18).next_to(ch, UP, buff=0.3)
        rule = label(r"bimodal insertion: \ put a new line at the \textit{least}-recently-used end, \ except once in 32",
                     font_size=24, color=DATA).to_edge(DOWN, buff=0.4)
        with self.voiceover(
            "This experiment replays an approximate line-event stream from the first six thousand corpus words in a "
            "cold fully associative one-hundred-twenty-eight-line cache. It is not the full instruction-level memory "
            "trace. <bookmark mark='a'/> The LRU and seeded-random bars use that same stream and capacity. <bookmark "
            "mark='b'/> Bimodal insertion usually places a newly fetched line at the LRU end, promoting a fraction "
            "of new lines to the MRU end. Here that fraction is one in thirty-two in expectation, not an exact "
            "periodic schedule. Hits update recency. <bookmark mark='c'/> MIN supplies the offline comparison under "
            "the same forced-insertion miss model. A reduced gap on this stream says nothing universal about other "
            "workloads; changing locality phases, training information or available state can change the result."
        ) as vo:
            self.play(FadeIn(head), FadeIn(cap), FadeIn(ch[0]))
            for mk, ks in (("a", [0, 1]), ("b", [2]), ("c", [3])):
                if mk != 'a':
                    vo.wait_until(mk)
                self.play(*[GrowFromEdge(ch.bars[k], DOWN) for k in ks], *[FadeIn(ch.vals[k]) for k in ks],
                          *[FadeIn(ch.names[k]) for k in ks])
                if mk == "b":
                    self.play(FadeIn(rule))
                if mk == 'a':
                    vo.wait_until(mk)
        self.wait(0.3)
        self.clear_scene()

    def learned(self):
        head = label(r"Learning from Belady", font_size=38).to_edge(UP, buff=0.4)
        items = VGroup(
            label(r"Hawkeye \ (2016): \ sampled historical OPTgen labels; \ PC-based prediction", font_size=24, color=DATA),
            label(r"Glider \ (2019): \ offline LSTM analysis; \ online unordered PC-history model", font_size=24, color=YES),
            label(r"Mockingjay \ (2022): \ reuse-distance classes; \ predicted reuse-time ordering", font_size=24, color=HEAD),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.4).move_to(UP * 0.5)
        flow = VGroup(*[VGroup(
            RoundedRectangle(width=3.0, height=.65, corner_radius=.08, stroke_color=col,
                             stroke_width=2.2, fill_color=BG, fill_opacity=1),
            label(text, font_size=21, color=col))
            for text, col in (("observed history", DATA), ("online prediction", HEAD),
                              ("replacement decision", YES))])
        flow.arrange(RIGHT, buff=.45).move_to(DOWN * 1.6)
        arrows = VGroup(*[Arrow(a.get_right(), b.get_left(), buff=0.08, color=GREY_B, stroke_width=2)
                         for a, b in zip(flow, flow[1:])])
        scope = note(r"different mechanisms; \ no complete hardware evaluation reproduced here", font_size=19).to_edge(DOWN, buff=0.35)
        with self.voiceover(
            "Learning-based replacement policies make different predictions. <bookmark mark='a'/> Hawkeye uses "
            "OPTgen to reconstruct cache-friendly behavior from sampled historical accesses, then trains a "
            "program-counter predictor. Historical feedback is not knowledge of the future. <bookmark mark='b'/> "
            "Glider analyzes an offline attention-based LSTM and uses the insights to design a much cheaper online "
            "predictor with an unordered history of load-instruction identities. It does not simply copy a few "
            "hundred trained LSTM weights into hardware. <bookmark mark='c'/> Mockingjay's 2022 study instead "
            "predicts reuse-distance classes and orders candidates by predicted reuse time. Its empirical gains "
            "depend on the evaluated platform, workloads and prefetch conditions. These primary studies motivate "
            "mechanisms; our chapter's small BIP experiment reproduces none of their complete hardware evaluations."
        ) as vo:
            self.play(FadeIn(head))
            for mk, it in zip("abc", items):
                if mk != 'a':
                    vo.wait_until(mk)
                self.play(FadeIn(it, shift=RIGHT * 0.1))
                if mk == 'a':
                    vo.wait_until(mk)
            self.play(FadeIn(flow), Create(arrows), FadeIn(scope))
        self.wait(0.3)
        self.clear_scene()

    def now(self):
        head = label(r"Open questions", font_size=40).to_edge(UP, buff=0.4)
        items = VGroup(
            label(r"how close can any online policy come to Belady \ on a given kind of program?", font_size=24,
                  color=YES),
            label(r"pebble games beyond matrix multiply: \ tight bounds for graphs, \ sparse problems, \ neural "
                  r"networks", font_size=24, color=HEAD),
            label(r"CXL-attached memory: \ topology, protocol, placement and scheduling costs",
                  font_size=24, color=CTRL),
            label(r"processing in memory: \ moving the arithmetic to the data instead", font_size=24, color=DATA),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.38).move_to(DOWN * 0.1)
        with self.voiceover(
            "Define the model before asking how close an online policy can get to MIN. <bookmark mark='a'/> Paging "
            "has established competitive bounds under explicit cache-size and adversary assumptions. Predicting "
            "which learned policy wins on a particular changing workload remains an empirical and theoretical "
            "question. <bookmark mark='b'/> Communication bounds exist for many computation graphs; tightness "
            "depends on graph structure, allowed algorithms, sparsity and recomputation rules. It is too broad to "
            "say that bounds beyond matrix multiplication are simply unknown. <bookmark mark='c'/> CXL-attached and "
            "pooled memory introduce topology, protocol, locality and scheduling tradeoffs, with no single universal "
            "extra latency. <bookmark mark='d'/> Processing near or inside memory changes where operations and data "
            "move, but adds its own precision, capacity, programming and transfer constraints. The research exercise "
            "asks for a reproducible, model-matched policy comparison."
        ) as vo:
            self.play(FadeIn(head))
            for mk, it in zip("abcd", items):
                if mk != 'a':
                    vo.wait_until(mk)
                self.play(FadeIn(it, shift=RIGHT * 0.1))
                if mk == 'a':
                    vo.wait_until(mk)
        self.wait(0.3)
        self.clear_scene()

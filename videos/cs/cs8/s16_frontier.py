from __future__ import annotations

import numpy as np

from explainer.cs import *  # noqa: F403
from videos.cs.cs8.common import (BG, CODE, COST, CTRL, DATA, FUNC, HEAD, HIST, INF, NO, PART, YES, bar_chart, box, fmt,
                                  load, mono)


class Frontier(VoiceoverScene):
    """The research tier (videos/cs/SYLLABUS.md 1.1): can a machine beat the dataflow limit by predicting values,
    and can speculation be made safe, and at what cost?"""

    def construct(self):
        self.card()
        self.values()
        self.verdict_vp()
        self.secure()
        self.now()

    def card(self):
        card = chapter_card(15, r"Frontier: \ past the dataflow limit, \ safely",
                            r"Can a machine guess values, \ and can guessing be made safe?", lit=(1996, 2014, 2019),
                            extra=((1996, r"Lipasti: \ value prediction"), (2014, r"Perais and Seznec"),
                                   (2019, r"STT, \ NDA")), part=PART)
        with self.voiceover("Chapter fifteen. Frontier: past the dataflow limit, safely."):
            self.play(FadeIn(card[0], shift=UP * 0.2), FadeIn(card[1]), FadeIn(card[2]))
        self.play(FadeOut(card))

    # ------------------------------------------------------------------
    def values(self):
        d = load("frontier")
        head = label(r"Value prediction: \ guess what a load will return", font_size=34).to_edge(UP, buff=0.3)
        idea = VGroup(
            label(r"the critical path runs through loads: \ \texttt{lw t1} \ $\to$ \ \texttt{bne}", font_size=24,
                  color=GREY_A),
            label(r"guess the value, \ start the users now, \ check when the load arrives", font_size=24, color=HEAD),
            label(r"(Lipasti, \ Wilkerson and Shen, \ 1996: \ many loads return the same value as last time)",
                  font_size=20, color=GREY_B),
        ).arrange(DOWN, buff=0.18).next_to(head, DOWN, buff=0.35)
        th = d["thresholds"]
        base = d["vp"]["8/256"]["base"]
        oracle = d["vp"]["8/256"]["oracle"]
        keys = ["1", "2", "4", "8", "15"]
        ax = Axes(x_range=[0, 5, 1], y_range=[2.6, 4.2, 0.4], x_length=7.0, y_length=3.0, tips=False,
                  axis_config={"color": GREY_C, "font_size": 16}).move_to(LEFT * 2.0 + DOWN * 1.6)
        ax.y_axis.add_numbers([2.6, 3.0, 3.4, 3.8], font_size=16, num_decimal_places=1)
        xt = VGroup(*[label(k, font_size=18, color=GREY_B).next_to(ax.c2p(i + 0.5, 2.6), DOWN, buff=0.12)
                      for i, k in enumerate(keys)])
        xl = note(r"confidence needed before guessing \ (correct in a row)", font_size=18).next_to(xt, DOWN, buff=0.1)
        bl = DashedLine(ax.c2p(0, base), ax.c2p(5, base), color=GREY_B, stroke_width=2)
        blt = label(rf"no prediction: \ {base:.2f}", font_size=18, color=GREY_B).next_to(bl, RIGHT, buff=0.1)
        ol = DashedLine(ax.c2p(0, oracle), ax.c2p(5, oracle), color=YES, stroke_width=2)
        olt = label(rf"every load guessed right: \ {oracle:.2f}", font_size=18, color=YES).next_to(ol, RIGHT, buff=0.1)
        pts = VGroup(*[Dot(ax.c2p(i + 0.5, th[k]["ipc"]), radius=0.08, color=NO) for i, k in enumerate(keys)])
        curve = VMobject(color=NO, stroke_width=3).set_points_as_corners([p.get_center() for p in pts])
        acc = VGroup(*[label(rf"{100 * th[k]['correct'] / th[k]['predicted']:.0f}\%", font_size=16, color=NO).next_to(
            pts[i], DOWN, buff=0.1) for i, k in enumerate(keys)])
        side = note(r"oracle scheduler, \ 8 wide, \ window 256, \ real branches; \ a stride predictor per load; \ "
                    r"red: \ IPC, \ and how often a confident guess was right", font_size=17).next_to(ax, UP, buff=0.12).align_to(
            ax, LEFT)
        with self.voiceover(
            "Two questions are open at the edge of this part. The first: can a machine beat the dataflow limit "
            "itself? The critical path is a chain of true dependences, and nothing we have built can shorten it. "
            "<bookmark mark='a'/> Unless the machine guesses values, not just branches. If a load usually returns the "
            "same value as last time, or the last value plus a fixed step, predict it, let the instructions that "
            "need it start at once, and check when the real value arrives. Mikko Lipasti and his colleagues proposed "
            "this in 1996. <bookmark mark='b'/> We tried it on the Job, in the limit study, with a stride predictor "
            "for each load that only guesses after it has been right several times in a row. <bookmark mark='c'/> "
            "Without prediction, three point three four instructions per cycle. A predictor that never erred would "
            "give three point nine eight. <bookmark mark='d'/> And the real predictor, at every confidence level, "
            "makes the machine slower. Its confident guesses are right only sixty to ninety percent of the time, "
            "and each wrong one costs a full recovery, which outweighs the dependences broken by the right ones."
        ) as vo:
            self.play(FadeIn(head))
            vo.wait_until("a")
            self.play(LaggedStart(*[FadeIn(i) for i in idea], lag_ratio=0.4))
            vo.wait_until("b")
            self.play(Create(ax), FadeIn(xt), FadeIn(xl), FadeIn(side))
            vo.wait_until("c")
            self.play(Create(bl), FadeIn(blt), Create(ol), FadeIn(olt))
            vo.wait_until("d")
            self.play(LaggedStart(*[FadeIn(p, scale=1.5) for p in pts], lag_ratio=0.2), Create(curve), FadeIn(acc))
        self.wait(0.3)
        self.clear_scene()

    # ------------------------------------------------------------------
    def verdict_vp(self):
        d = load("frontier")
        head = label(r"What it would take", font_size=38).to_edge(UP, buff=0.4)
        items = VGroup(
            label(r"guesses must be right far more than 99\% of the time to pay", font_size=26, color=HEAD),
            label(r"Perais and Seznec (2014): \ very high confidence, \ recovery only at commit", font_size=24,
                  color=GREY_A),
            label(r"on the Job, \ even perfect value prediction buys only 19\%: \ the branches still rule", font_size=24,
                  color=NO),
            label(r"open: \ which programs have values worth guessing, \ and can a core find them cheaply?",
                  font_size=26, color=YES),
        ).arrange(DOWN, buff=0.38).move_to(DOWN * 0.1)
        with self.voiceover(
            "That matches what researchers found. <bookmark mark='a'/> A value predictor must be right far more than "
            "ninety-nine percent of the time to pay its way. <bookmark mark='b'/> In 2014 Arthur Perais and André "
            "Seznec showed a design that does it, using very high confidence thresholds and repairing mistakes "
            "cheaply at commit, and revived a field many had given up. <bookmark mark='c'/> On the Job, though, even "
            "perfect value prediction would buy only nineteen percent, because the branches, not the loads, set the "
            "limit. <bookmark mark='d'/> Which programs have values worth guessing, and whether a core can find "
            "them cheaply, is still an open question."
        ) as vo:
            self.play(FadeIn(head))
            for mk, it in zip("abcd", items):
                vo.wait_until(mk)
                self.play(FadeIn(it, shift=UP * 0.1))
        self.wait(0.3)
        self.clear_scene()

    # ------------------------------------------------------------------
    def secure(self):
        d = load("frontier")["secure"]
        sp = load("spectre")["mitigations"]
        head = label(r"Can speculation be made safe?", font_size=36).to_edge(UP, buff=0.35)
        rule = VGroup(
            label(r"a rule for our core \ (in the spirit of STT and NDA, \ 2019):", font_size=24, color=GREY_A),
            label(r"a load that completes in the shadow of an unresolved branch \\ keeps its value to itself until "
                  r"every older branch has executed", font_size=24, color=HEAD),
        ).arrange(DOWN, buff=0.18).next_to(head, DOWN, buff=0.4)
        res = VGroup(
            label(r"the Spectre gadget: \ " + (r"no fast probe line, \ no leak" if all(
                x == 1 for x in sp["secure"]["output"]) else r"still leaks"), font_size=26, color=YES),
            label(rf"the Job: \ IPC {d['plain_ipc']:.3f} \ $\to$ \ {d['secure_ipc']:.3f}: \ "
                  rf"{100 * d['cost']:.1f}\% slower", font_size=26, color=COST),
            label(r"the speculation that remains is the harmless kind: \ arithmetic, \ branches, \ loads of known "
                  r"addresses", font_size=22, color=GREY_A),
        ).arrange(DOWN, buff=0.3).move_to(DOWN * 0.8)
        with self.voiceover(
            "The second question: can speculation be made safe, without giving up its speed? Spectre works because "
            "a speculatively loaded value is passed on to a second load whose address it chooses, and that second "
            "load leaves a footprint in the cache. <bookmark mark='a'/> So here is a rule for our core, in the "
            "spirit of two 2019 proposals, Speculative Taint Tracking and NDA. A load that completes while some older "
            "branch is still unresolved keeps its value to itself: nothing that depends on it may run until every "
            "older branch has executed. <bookmark mark='b'/> Run the attack against this core: the probe shows no "
            "fast line, and nothing leaks. <bookmark mark='c'/> Run the Job: three and a half percent slower. "
            "<bookmark mark='d'/> Cheap, here, because the speculation that remains is the useful kind: arithmetic, "
            "branches, and loads whose addresses are already known can all still run ahead."
        ) as vo:
            self.play(FadeIn(head))
            vo.wait_until("a")
            self.play(FadeIn(rule))
            for mk, r in zip("bcd", res):
                vo.wait_until(mk)
                self.play(FadeIn(r, shift=UP * 0.1))
        self.wait(0.3)
        self.clear_scene()

    # ------------------------------------------------------------------
    def now(self):
        head = label(r"Open questions", font_size=40).to_edge(UP, buff=0.4)
        items = VGroup(
            label(r"proof: \ does a rule like ours block \textit{every} speculative leak? \ (speculative "
                  r"non-interference, \ 2020)", font_size=23, color=YES),
            label(r"cost: \ published schemes cost from a few percent to tens of percent; \ what is the floor?",
                  font_size=23, color=COST),
            label(r"other channels: \ not only the cache, \ but ports, \ predictors, \ power", font_size=23,
                  color=NO),
            label(r"and the 2,400 instructions per cycle of chapter two: \ runahead execution, \ thousand-instruction "
                  r"windows, \ dataflow machines", font_size=23, color=HEAD),
        ).arrange(DOWN, buff=0.38, aligned_edge=LEFT).move_to(DOWN * 0.1)
        with self.voiceover(
            "Here is where the research stands. <bookmark mark='a'/> Does a rule like ours block every leak of "
            "speculatively loaded data, or only the one we tried? Since 2020, researchers have defined what it means "
            "for a program to be safe under speculation, speculative non-interference, and built tools that check "
            "it; proving a whole core safe is still out of reach. <bookmark mark='b'/> What does safety cost? "
            "Published hardware schemes report from a few percent to tens of percent, depending on how much they "
            "protect. Nobody knows the floor. <bookmark mark='c'/> The cache is not the only channel: execution "
            "ports, the predictors themselves, and power draw have all been used to leak. <bookmark mark='d'/> And "
            "the oldest question of all: the Job contains two thousand four hundred instructions per cycle of "
            "parallelism, and we use two. Runahead execution, windows of thousands of instructions, and dataflow "
            "machines have all tried to reach it. The problem with a star at the end of this part starts here."
        ) as vo:
            self.play(FadeIn(head))
            for mk, it in zip("abcd", items):
                vo.wait_until(mk)
                self.play(FadeIn(it, shift=RIGHT * 0.1))
        self.wait(0.3)
        self.clear_scene()

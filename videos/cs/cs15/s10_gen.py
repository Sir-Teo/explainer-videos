from __future__ import annotations

from explainer.cs import *  # noqa: F403
from videos.cs.cs15.common import (BG, CODE, COST, CTRL, DATA, FUNC, HEAD, LAM, NO, PART, YES, bar_chart,
                                   grid_table, load, mono, words)


class Generations(VoiceoverScene):
    def construct(self):
        self.card()
        self.hypothesis()
        self.nursery()
        self.barrier()

    def card(self):
        card = chapter_card(9, r"Generations", r"Do most objects die young?", lit=(1984,),
                            extra=((1984, r"Ungar: \ generation scavenging"),), part=PART)
        with self.voiceover("Chapter nine. Generations."):
            self.play(FadeIn(card[0], shift=UP * 0.2), FadeIn(card[1]), FadeIn(card[2]))
        self.play(FadeOut(card))

    def hypothesis(self):
        d = load("gen")
        head = label(r"Most objects die young", font_size=34).to_edge(UP, buff=0.3)
        sv = d["survival"]

        def age(a):
            return "0" if a == 0 else (f"{a // 1000}k" if a >= 1000 else str(a))
        vals = [100 * s["fraction"] for s in sv]
        ch = bar_chart(vals, [age(s["age"]) for s in sv], [YES if k == 0 else DATA for k in range(len(sv))],
                       height=3.0, bar_w=0.5, gap=0.3, fmt_=lambda v: f"{v:.1f}\\%", font_size=15).move_to(
            LEFT * 3.4 + DOWN * 0.4)
        xl = label(r"still alive after this many more words of allocation", font_size=18, color=GREY_B).next_to(
            ch, DOWN, buff=0.35)
        yl = label(rf"of the Job's {words(d['objects'])} objects", font_size=18, color=GREY_B).next_to(
            ch, UP, buff=0.3)
        died = 100 * (1 - sv[0]["fraction"])
        side = VGroup(
            label(rf"{died:.0f}\% never survive a single collection", font_size=23, color=YES),
            label(r"a word's letters, \ a cell of a table about to be rebuilt, \ a pair replaced by the next count",
                  font_size=19, color=GREY_A),
            label(r"those that do survive tend to live long: \ the text, \ the table", font_size=21, color=DATA),
            label(r"the \textbf{generational hypothesis} \ (Lieberman and Hewitt, \ 1983; \ Ungar, \ 1984)",
                  font_size=21, color=HEAD),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.22).to_edge(RIGHT, buff=0.4)
        if side.width > 5.4:
            side.scale_to_fit_width(5.4)
        with self.voiceover(
            "A copying collector's work is the live data, and the live data includes objects it has copied many "
            "times before. Is there a pattern in which objects die? <bookmark mark='a'/> We tagged every object "
            "the Job allocates with the time of its birth, and recorded the last time a collection found it "
            "alive. <bookmark mark='b'/> Eighty-seven percent of the Job's objects never survive one collection. "
            "They are a word's letters reversed, a table cell about to be rebuilt by bump, a pair replaced by the "
            "next count. <bookmark mark='c'/> And the few that survive tend to survive a long time: the text "
            "itself, the table of counts. <bookmark mark='d'/> This is the generational hypothesis, proposed by "
            "Lieberman and Hewitt in 1983 and exploited by David Ungar's generation scavenging for Smalltalk in "
            "1984. It has held for almost every language measured since."
        ) as vo:
            self.play(FadeIn(head), FadeIn(yl), FadeIn(xl))
            vo.wait_until("a")
            self.play(FadeIn(ch.names), FadeIn(ch[0]))
            vo.wait_until("b")
            self.play(LaggedStart(*[GrowFromEdge(b, DOWN) for b in ch.bars], lag_ratio=0.1), FadeIn(ch.vals),
                      FadeIn(side[:2]))
            vo.wait_until("c")
            self.play(FadeIn(side[2]))
            vo.wait_until("d")
            self.play(FadeIn(side[3]))
        self.wait(0.3)
        self.clear_scene()

    def nursery(self):
        d = load("gen")
        tr = load("tracing")
        head = label(r"A nursery for the young", font_size=34).to_edge(UP, buff=0.3)
        boxes = VGroup(
            VGroup(Rectangle(width=2.6, height=1.0, color=YES, stroke_width=2.5).set_fill(YES, 0.1),
                   label(r"nursery", font_size=22, color=YES)),
            VGroup(Rectangle(width=7.0, height=1.0, color=DATA, stroke_width=2.5).set_fill(DATA, 0.08),
                   label(r"old space", font_size=22, color=DATA)),
        )
        for b in boxes:
            b[1].move_to(b[0])
        boxes.arrange(RIGHT, buff=0.8).next_to(head, DOWN, buff=0.5)
        prom = CurvedArrow(boxes[0].get_top(), boxes[1].get_top() + LEFT * 2.5, angle=-0.8, color=GREY_B,
                           stroke_width=2.2, tip_length=0.14)
        pl = label(r"survivors promoted", font_size=18, color=GREY_B).next_to(prom, UP, buff=0.05)
        sel = [r for r in d["rows"] if r["nursery"] in (1024, 4096, 16384, 32768)]
        rows = [[words(r["nursery"]), str(r["minor"]), f"{100 * r['survival']:.0f}\\%", str(r["major"]),
                 words(r["work"])] for r in sel]
        tab = grid_table([r"nursery, \ words", r"minor collections", r"survive one", r"major", r"work, \ words"],
                         rows, widths=[2.6, 2.8, 2.2, 1.6, 2.4], row_h=0.48, font_size=20).next_to(boxes, DOWN,
                                                                                               buff=0.5)
        g = next(r for r in tr["rows"] if r["collector"] == "generational")
        c = tr["rows"][0]
        res = label(rf"in the same memory as chapter 7's table: \ {words(g['work'])} words of work against "
                    rf"Cheney's {words(c['work'])}, \ and a shorter longest pause", font_size=20,
                    color=COST).next_to(tab, DOWN, buff=0.35)
        pts = label(r"collect the nursery often and cheaply; \ the old space, \ rarely", font_size=22,
                    color=HEAD).to_edge(DOWN, buff=0.35)
        with self.voiceover(
            "So keep the young apart. <bookmark mark='a'/> New objects are allocated in a small nursery. When it "
            "fills, a minor collection copies the few survivors out, into an old space, and the whole nursery is "
            "free again. The old space is collected, by a major collection, only when it fills. <bookmark "
            "mark='b'/> Our generational collector, on the Job, with nurseries of several sizes. A tiny nursery "
            "of a thousand words collects three hundred and sixty times, and seventy percent of its objects "
            "survive, because they were simply not given time to die. At thirty-two thousand words, only one in "
            "ten survives. <bookmark mark='c'/> In the same memory as chapter seven's comparison, the generational "
            "collector does two thirds of the copying collector's work, with a shorter longest pause. <bookmark "
            "mark='d'/> Collect the young often and cheaply; the old, rarely. Every production collector, in the "
            "JVM, in V8, in .NET, in OCaml and in GHC, is built this way."
        ) as vo:
            self.play(FadeIn(head), FadeIn(boxes))
            vo.wait_until("a")
            self.play(Create(prom), FadeIn(pl))
            vo.wait_until("b")
            self.play(FadeIn(tab))
            vo.wait_until("c")
            self.play(FadeIn(res))
            vo.wait_until("d")
            self.play(FadeIn(pts))
        self.wait(0.3)
        self.clear_scene()

    def barrier(self):
        d = load("gen")
        head = label(r"The catch: \ old objects that point at young ones", font_size=34).to_edge(UP, buff=0.3)
        old = VGroup(Rectangle(width=1.6, height=0.8, color=DATA, stroke_width=2.5).set_fill(DATA, 0.12),
                     mono("old", 18, DATA))
        yng = VGroup(Rectangle(width=1.6, height=0.8, color=YES, stroke_width=2.5).set_fill(YES, 0.12),
                     mono("young", 18, YES))
        for b in (old, yng):
            b[1].move_to(b[0])
        VGroup(old, yng).arrange(RIGHT, buff=4.2).next_to(head, DOWN, buff=1.1)
        ar = Arrow(old.get_right(), yng.get_left(), buff=0.05, color=NO, stroke_width=3, tip_length=0.16)
        store = mono("old.field = young", 18, NO).next_to(ar, UP, buff=0.2)
        pts = VGroup(
            label(r"a minor collection scans only the roots and the nursery: \ this pointer would be missed",
                  font_size=21, color=GREY_A),
            label(r"a \textbf{write barrier}: \ a few instructions on every pointer store, \ recording such "
                  r"fields in a \textbf{remembered set}", font_size=21, color=GREY_A),
            label(r"HotSpot and V8 mark ``cards'' of the old space as dirty, \ and scan only those", font_size=21,
                  color=GREY_A),
            label(rf"in the $\lambda$-core: \ {d['rows'][0]['barrier_hits']} barrier hits. \ An object is never "
                  r"changed after it is made, \ so an old object cannot point at a younger one", font_size=21,
                  color=YES),
            label(r"pure functional languages get generations almost for free \ (Haskell's lazy updates are "
                  r"the exception)", font_size=20, color=HEAD),
        ).arrange(DOWN, buff=0.16).to_edge(DOWN, buff=0.4)
        with self.voiceover(
            "There is a catch. <bookmark mark='a'/> A minor collection looks only at the roots and the nursery. "
            "If the program stores a pointer to a young object into an old one, that pointer is invisible, and "
            "the young object would be freed while still in use. <bookmark mark='b'/> So every pointer store runs "
            "a write barrier: a few extra instructions that record old-to-young pointers in a remembered set, "
            "which the minor collection treats as more roots. HotSpot and V8 divide the old space into cards and "
            "mark a card dirty when it is written. <bookmark mark='c'/> Our generational collector counts how "
            "many times the barrier was needed on the Job: zero. In the lambda core an object is never modified "
            "after it is built, so it can only point at objects older than itself. <bookmark mark='d'/> That is "
            "one reason functional languages love generational collection: they get it almost for free. "
            "Haskell, whose lazy values are overwritten when they are evaluated, is the exception that proves the "
            "rule."
        ) as vo:
            self.play(FadeIn(head), FadeIn(old), FadeIn(yng))
            vo.wait_until("a")
            self.play(GrowArrow(ar), FadeIn(store), FadeIn(pts[0]))
            vo.wait_until("b")
            self.play(FadeIn(pts[1:3]))
            vo.wait_until("c")
            self.play(FadeIn(pts[3]))
            vo.wait_until("d")
            self.play(FadeIn(pts[4]))
        self.wait(0.3)
        self.clear_scene()

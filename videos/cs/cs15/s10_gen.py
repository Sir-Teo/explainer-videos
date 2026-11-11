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
        head = label('Sampling ages, not measuring death', font_size=34).to_edge(UP, buff=.3)
        sv = d["survival"]
        def age(a):
            return str(a) if a < 1000 else str(a//1000)+"k"
        ch = bar_chart([100*r["fraction"] for r in sv], [age(r["age"]) for r in sv],
                       [YES]+[DATA]*(len(sv)-1), height=2.1, bar_w=.43, gap=.22,
                       fmt_=lambda v: str(round(v,1))+chr(92)+'%', font_size=14).move_to(LEFT*3.3+UP*.5)
        xl = label('last-observed-live age; later words allocated', font_size=17, color=GREY_B).next_to(ch, DOWN, buff=.2)
        yl = label('fraction with observed age above threshold', font_size=18, color=GREY_B).next_to(ch, UP, buff=.2)
        obs=d['observations']
        side = VGroup(
            VGroup(label('never observed at a collection',font_size=20,color=YES),
                   mono(f"{100*obs['never_observed_at_collection']/d['objects']:.1f}%",23,YES)).arrange(DOWN,buff=.1),
            label('zero recorded age can still mean live',font_size=21,color=HEAD),
            VGroup(label('reachable at end: end-censored',font_size=20,color=DATA),
                   mono(str(obs['reachable_at_end']),22,DATA)).arrange(DOWN,buff=.1),
            label('generational hypothesis: test each workload',font_size=19,color=GREY_A),
        ).arrange(DOWN,buff=.22).move_to(RIGHT*3.6+UP*.4)
        axis=Arrow(LEFT*5.5,RIGHT*5.5,buff=0,color=GREY_B,stroke_width=2)
        birth=Dot(LEFT*4.4,color=DATA);end=Dot(RIGHT*4.3,color=YES)
        tl=VGroup(axis,birth,end,
            label('allocate three list cells',font_size=18,color=DATA).next_to(birth,UP,buff=.15),
            label('no collections in this run',font_size=18,color=GREY_A).next_to(axis,UP,buff=.2),
            label('result still reachable',font_size=18,color=YES).next_to(end,UP,buff=.15),
            label('all three recorded ages = 0',font_size=19,color=HEAD).next_to(axis,DOWN,buff=.2)
        ).move_to(DOWN*2.6)
        tl.add(label('separate run: [1;2;3]', font_size=18, color=GREY_A).move_to(DOWN*1.7))
        with self.voiceover(
            (
            "Can allocation ages guide collection? <bookmark mark='a'/> We record when each object is allocated "
            "and the last collection that observes it live. The histogram reports lower bounds on observed live "
            "age, measured in later words allocated. It does not record exact death times. <bookmark mark='b'/> "
            "Never observed at a collection does not mean dead: our three-cell result stays live at the end of a "
            "run with no collections, yet all three recorded ages are zero. The timeline shows this sampling gap. "
            "<bookmark mark='c'/> Objects reachable when measurement ends are end-censored. The displayed counts "
            "distinguish those cases. <bookmark mark='d'/> Many workloads do produce abundant short-lived "
            "objects, motivating generations. Treat that as an empirical hypothesis to test, not a universal law "
            "proved by this histogram."
        )
        ) as vo:
            self.play(FadeIn(head), FadeIn(yl), FadeIn(xl))
            vo.wait_until("a")
            self.play(FadeIn(ch.names), FadeIn(ch[0]))
            vo.wait_until("b")
            self.play(LaggedStart(*[GrowFromEdge(b, DOWN) for b in ch.bars], lag_ratio=0.1), FadeIn(ch.vals),
                      FadeIn(side[:2]), FadeIn(tl))
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
        tab = grid_table([r"nursery, \ words", r"minor collections", 'promoted words / used words', r"major", r"work, \ words"],
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
            (
            "Keep new objects in a nursery. <bookmark mark='a'/> A minor collection copies its reachable objects "
            "into old space. When old space may not fit another nursery, our full collection copies both regions "
            "together. It already empties the nursery, so there is no second, zero-work minor event. <bookmark "
            "mark='b'/> The table compares nursery sizes. Its percentage is promoted words divided by actual "
            "nursery words consumed in minor cycles, not a fraction of objects. <bookmark mark='c'/> The "
            "comparison below uses the same total reserved memory: nursery plus two old semispaces versus two "
            "Cheney semispaces. Work and pause columns count model words, not milliseconds. <bookmark mark='d'/> "
            "Generations are common, but not universal. Go's current collector, for example, is explicitly "
            "non-generational. Choose and measure the policy for the workload."
        )
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
            label('immutability removes this mutation barrier in our model; collection still costs work', font_size=20, color=HEAD),
        ).arrange(DOWN, buff=0.16).to_edge(DOWN, buff=0.4)
        with self.voiceover(
            (
            "A young-only collection needs to know about older references into the nursery. <bookmark mark='a'/> "
            "If an old object stores a young pointer, scanning only roots and nursery objects would miss that "
            "edge. <bookmark mark='b'/> A write barrier records relevant stores in a remembered set or card "
            "table, which the minor collector scans as additional roots. Exact barriers vary by runtime. "
            "<bookmark mark='c'/> In our immutable core, fully initialized objects point only to values that "
            "already existed. Under this allocation and promotion model there are no old-to-young mutation edges, "
            "and measured barrier hits are zero. <bookmark mark='d'/> That removes this particular barrier "
            "requirement. Lazy updates, mutable fields and runtime bookkeeping can reintroduce it; immutability "
            "does not make every part of collection free."
        )
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

from __future__ import annotations

from explainer.cs import *  # noqa: F403
from videos.cs.cs15.common import (BG, CODE, COST, CTRL, DATA, FUNC, HEAD, LAM, NO, PART, YES, grid_table, load,
                                   mono, words)

# a small heap: (name, words, live), in address order; pointers among the live objects
HEAP = [("A", 3, True), ("B", 3, False), ("C", 4, True), ("D", 2, False), ("E", 3, False), ("F", 3, True),
        ("G", 2, False), ("H", 4, True), ("I", 3, False)]
PTRS = [("A", "F"), ("C", "H"), ("B", "D")]
ROOTS = ["A", "C"]
U = 0.4


def heap_row(y=0.6):
    x = -len_words() * U / 2
    out = {}
    for name, n, live in HEAP:
        r = Rectangle(width=n * U, height=0.75, stroke_color=GREY_B, stroke_width=1.8, fill_color=BG, fill_opacity=1)
        r.move_to([x + n * U / 2, y, 0])
        t = mono(name, 18, WHITE).move_to(r)
        out[name] = VGroup(r, t)
        x += n * U
    return out


def len_words():
    return sum(n for _, n, _ in HEAP)


class Tracing(VoiceoverScene):
    def construct(self):
        self.card()
        self.marksweep()
        self.compact()
        self.compare()

    def card(self):
        card = chapter_card(7, r"Tracing: \ mark--sweep and mark--compact", r"Can we find the live objects instead?",
                            lit=(1960,), extra=((1960, r"McCarthy: \ mark and sweep"),), part=PART)
        with self.voiceover("Chapter seven. Tracing: mark–sweep and mark–compact."):
            self.play(FadeIn(card[0], shift=UP * 0.2), FadeIn(card[1]), FadeIn(card[2]))
        self.play(FadeOut(card))

    def marksweep(self):
        head = label(r"Mark, \ then sweep", font_size=34).to_edge(UP, buff=0.3)
        objs = heap_row()
        row = VGroup(*objs.values())
        roots = VGroup(*[Arrow(objs[r][0].get_top() + UP * 0.9, objs[r][0].get_top(), buff=0.05, color=CTRL,
                               stroke_width=2.5, tip_length=0.14) for r in ROOTS])
        rl = label(r"roots", font_size=19, color=CTRL).next_to(roots, UP, buff=0.05)
        arcs = VGroup(*[CurvedArrow(objs[a][0].get_bottom() + DOWN * 0.02, objs[b][0].get_bottom() + DOWN * 0.02,
                                    angle=0.7, color=GREY_B, stroke_width=2, tip_length=0.12) for a, b in PTRS])
        addr = label(r"the heap, \ in address order", font_size=18, color=GREY_B).next_to(row, UP, buff=1.4).align_to(
            row, LEFT)
        sweep = Arrow(UP * 0.4, DOWN * 0.4, color=HEAD, stroke_width=4, tip_length=0.2).next_to(row, UP, buff=0.1)
        sweep.align_to(row, LEFT)
        pts = VGroup(
            label(r"\textbf{mark}: \ from the roots, \ follow every pointer, \ set a bit in each object reached",
                  font_size=21, color=YES),
            label(r"\textbf{sweep}: \ walk the whole heap; \ every unmarked object joins a free list", font_size=21,
                  color=NO),
            label(r"marking costs the live data; \ sweeping costs the \textit{whole heap}", font_size=21,
                  color=HEAD),
        ).arrange(DOWN, buff=0.14).to_edge(DOWN, buff=0.5)
        with self.voiceover(
            "Reference counting watches every pointer all the time. The other approach, which McCarthy used in "
            "the first LISP, does nothing until memory runs out, and then looks. <bookmark mark='a'/> Here is a "
            "heap, in address order, with two roots pointing in. <bookmark mark='b'/> Mark: start from the roots and "
            "follow every pointer, setting a mark bit in each object reached. A reaches F, C reaches H. B points at "
            "D, but nothing reaches B, so neither is marked. <bookmark mark='c'/> Sweep: walk the whole heap from "
            "one end to the other. Every object without a mark is garbage; its space goes onto a free list for "
            "future allocations. <bookmark mark='d'/> Notice the costs. Marking touches only the live objects. "
            "Sweeping touches every object, live or dead."
        ) as vo:
            self.play(FadeIn(head), FadeIn(row), FadeIn(addr))
            vo.wait_until("a")
            self.play(Create(roots), FadeIn(rl), Create(arcs))
            vo.wait_until("b")
            for wave in (["A", "C"], ["F", "H"]):
                self.play(*[objs[n][0].animate.set_fill(YES, 0.45) for n in wave], run_time=0.8)
            self.play(FadeIn(pts[0]))
            vo.wait_until("c")
            self.play(FadeIn(sweep))
            for name, n, live in HEAP:
                tgt = objs[name][0]
                anims = [sweep.animate.move_to([tgt.get_center()[0], sweep.get_center()[1], 0])]
                if not live:
                    anims.append(tgt.animate.set_stroke(NO, 1.5).set_fill(NO, 0.12))
                    anims.append(objs[name][1].animate.set_opacity(0.3))
                self.play(*anims, run_time=0.35)
            self.play(FadeOut(arcs[2]), FadeIn(pts[1]))
            vo.wait_until("d")
            self.play(FadeIn(pts[2]))
        self.wait(0.3)
        self.clear_scene()

    def compact(self):
        head = label(r"Fragmentation, \ and compaction", font_size=34).to_edge(UP, buff=0.3)
        objs = heap_row(y=1.3)
        for name, n, live in HEAP:
            if live:
                objs[name][0].set_fill(YES, 0.45)
            else:
                objs[name][0].set_stroke(NO, 1.5).set_fill(NO, 0.12)
                objs[name][1].set_opacity(0.3)
        row = VGroup(*objs.values())
        free = sum(n for _, n, l in HEAP if not l)
        biggest = max(n for _, n, l in HEAP if not l)
        req = VGroup(Rectangle(width=5 * U, height=0.75, color=HEAD, stroke_width=2).set_fill(HEAD, 0.15),
                     label("new: 5 words", font_size=16, color=HEAD))
        req[1].move_to(req[0])
        req.next_to(row, DOWN, buff=0.6)
        fail = label(rf"{free} words free, \ but the largest hole is {biggest}: \ no room", font_size=22,
                     color=NO).next_to(req, DOWN, buff=0.25)
        # the compacted heap
        x = row.get_left()[0]
        targets = {}
        for name, n, live in HEAP:
            if live:
                targets[name] = x + n * U / 2
                x += n * U
        top = x
        pts = VGroup(
            label(r"\textbf{mark--compact}: \ slide every live object down, \ in order, \ and fix every pointer",
                  font_size=21, color=YES),
            label(r"then allocation is a pointer bump again: \ no holes, \ no free lists", font_size=21,
                  color=GREY_A),
            label(r"the price: \ several passes over the heap \ (Lisp 2's three)", font_size=21, color=NO),
        ).arrange(DOWN, buff=0.14).to_edge(DOWN, buff=0.4)
        with self.voiceover(
            "Sweeping has a second problem. <bookmark mark='a'/> After a sweep, the free space is scattered in "
            "holes between the live objects. <bookmark mark='b'/> Ask for five words: there are thirteen free, "
            "but no single hole bigger than three. The allocation fails, with memory to spare. This is "
            "fragmentation, the same problem Part 11's allocators fought. <bookmark mark='c'/> A tracing collector "
            "has an advantage those allocators never had: it knows every pointer, so it can move objects. "
            "Mark–compact slides the live objects down to one end, keeping their order, and rewrites every pointer "
            "to them. <bookmark mark='d'/> Now the free space is one block, and allocating is just bumping a "
            "pointer. The price is extra passes over the heap: the classic Lisp 2 algorithm takes three."
        ) as vo:
            self.play(FadeIn(head), FadeIn(row))
            vo.wait_until("a")
            self.play(*[Indicate(objs[n][0], color=NO) for n, _, l in HEAP if not l])
            vo.wait_until("b")
            self.play(FadeIn(req))
            self.play(FadeIn(fail))
            vo.wait_until("c")
            self.play(FadeOut(req), FadeOut(fail),
                      *[FadeOut(objs[n]) for n, _, l in HEAP if not l])
            self.play(*[objs[n].animate.move_to([targets[n], objs[n].get_center()[1], 0]) for n in targets],
                      run_time=1.6)
            bump = Arrow(UP * 0.4, DOWN * 0.4, color=HEAD, stroke_width=4, tip_length=0.2).move_to(
                [top, row.get_top()[1] + 0.45, 0])
            bl = label(r"next free", font_size=18, color=HEAD).next_to(bump, UP, buff=0.05)
            self.play(FadeIn(pts[0]), FadeIn(bump), FadeIn(bl))
            vo.wait_until("d")
            self.play(FadeIn(pts[1:]))
        self.wait(0.3)
        self.clear_scene()

    def compare(self):
        d = load("tracing")
        head = label(r"Four collectors, \ one Job", font_size=34).to_edge(UP, buff=0.3)
        rows = []
        for r in d["rows"]:
            rows.append([r["collector"], str(r["collections"]), words(r["work"]), words(r["max_pause"]),
                         words(r["free_blocks"]) if r["free_blocks"] else r"---"])
        tab = grid_table([r"collector", r"collections", r"work, \ words", r"longest pause, \ words",
                          r"holes, \ worst"], rows, widths=[3.6, 2.2, 2.4, 3.0, 2.2], row_h=0.52, font_size=20, mono_cols=(),
                         colors=[[DATA, WHITE, WHITE, WHITE, WHITE], [NO, WHITE, WHITE, WHITE, NO],
                                 [FUNC, WHITE, WHITE, WHITE, WHITE], [YES, WHITE, YES, YES, WHITE]]).scale_to_fit_width(13.0).next_to(
            head, DOWN, buff=0.6)
        cap = label(rf"the Job on Part 7's chapter, \ in a heap of {words(d['heap_words'])} words each; \ work: \ "
                    r"words copied, \ marked, \ swept or slid", font_size=19, color=GREY_B).next_to(tab, DOWN,
                                                                                                 buff=0.3)
        pts = VGroup(
            label('nonmoving tracing can accommodate conservative roots; policies differ', font_size=21,
                  color=GREY_A),
            label(r"its holes: \ tens of thousands of them, \ in a heap whose live data fits in a fifth of it",
                  font_size=21, color=NO),
            label(r"the copying and generational rows: \ chapters 8 and 9", font_size=21, color=HEAD),
        ).arrange(DOWN, buff=0.14).to_edge(DOWN, buff=0.4)
        with self.voiceover(
            (
            "Run the same Job under four collectors with equal reserved heap capacity. <bookmark mark='a'/> The "
            "table counts words of marking, scanning or copying using each toy collector's stated work model. "
            "These operations do not necessarily have equal native time. <bookmark mark='b'/> Mark-sweep leaves "
            "objects in place and can fragment free space. Compacting and copying move reachable objects and must "
            "update references. <bookmark mark='c'/> The generational layout reserves its nursery plus two old "
            "semispaces; Cheney reserves two equal semispaces. The longest work event is a model pause, not a "
            "measured millisecond bound. This comparison explains mechanisms on one workload, rather than "
            "crowning a universally best collector."
        )
        ) as vo:
            self.play(FadeIn(head), FadeIn(tab), FadeIn(cap))
            vo.wait_until("a")
            self.play(Indicate(VGroup(*tab.cells[2]), color=HEAD), FadeIn(pts[0]))
            vo.wait_until("b")
            self.play(Indicate(tab.cells[2][4], color=NO), FadeIn(pts[1]))
            vo.wait_until("c")
            self.play(Indicate(VGroup(*tab.cells[3]), color=HEAD), FadeIn(pts[2]))
        self.wait(0.3)
        self.clear_scene()

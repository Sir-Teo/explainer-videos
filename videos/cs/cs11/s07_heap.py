from __future__ import annotations

import numpy as np

from explainer.cs import *  # noqa: F403
from videos.cs.cs11.common import (BG, CODE, CTRL, DATA, FUNC, HEAD, NO, PART, YES, bar_chart, code, load, region)


class Heap(VoiceoverScene):
    def construct(self):
        self.card()
        self.why()
        self.freelist()
        self.trace()

    def card(self):
        card = chapter_card(6, r"The heap", r"Where does memory come from when you don't know how much you need?",
                            lit=(1965, 1968), extra=((1965, r"Knowlton: \ the buddy system"), (1968, r"Knuth: \ "
                                                                                                      r"boundary tags")),
                            part=PART)
        with self.voiceover("Chapter six. The heap."):
            self.play(FadeIn(card[0], shift=UP * 0.2), FadeIn(card[1]), FadeIn(card[2]))
        self.play(FadeOut(card))

    def why(self):
        head = label(r"\texttt{malloc} and \texttt{free}", font_size=34).to_edge(UP, buff=0.35)
        pts = VGroup(
            label(r"the stack is perfect for data that dies when the function returns", font_size=22, color=GREY_A),
            label(r"but the Job's table outlives every call that adds to it, \ and its size is unknown in advance",
                  font_size=22, color=GREY_A),
            label(r"\texttt{p = malloc(n)}: \ $n$ bytes, \ somewhere, \ until \ \texttt{free(p)}", font_size=24,
                  color=YES),
            label("online, nonmoving allocation: place requests without knowing future lifetimes", font_size=22, color=HEAD),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.3).next_to(head, DOWN, buff=0.45)
        # lifetimes: stack frames nest inside calls; heap blocks outlive the call that made them
        x0, x1 = -5.2, 5.6
        axis = Arrow([x0, -3.35, 0], [x1 + 0.4, -3.35, 0], buff=0, color=GREY_C, stroke_width=2,
                     max_tip_length_to_length_ratio=0.03)
        tl = label(r"time", font_size=16, color=GREY_B).next_to(axis, DOWN, buff=0.08).align_to(axis, RIGHT)
        mainbar = Rectangle(width=x1 - x0, height=0.28, stroke_width=0, fill_color=GREY_C, fill_opacity=0.5).move_to(
            [(x0 + x1) / 2, -0.75, 0])
        mt = label(r"\texttt{main}'s frame", font_size=15, color=WHITE).move_to(mainbar)
        calls, blocks = VGroup(), VGroup()
        for k, xs in enumerate((-4.4, -1.8, 0.8, 3.2)):
            calls.add(Rectangle(width=1.3, height=0.28, stroke_width=0, fill_color=CTRL, fill_opacity=0.6).move_to(
                [xs + 0.65, -1.15, 0]))
            b = Rectangle(width=x1 - (xs + 0.4), height=0.22, stroke_width=0, fill_color=YES,
                          fill_opacity=0.6).move_to([(xs + 0.4 + x1) / 2, -1.65 - 0.36 * k, 0])
            blocks.add(b)
        ct = label(r"\texttt{lookup}: \ adds a word, \ returns", font_size=15, color=CTRL).next_to(calls[0], LEFT,
                                                                                                 buff=0.1)
        ct.align_to([x0 - 1.6, 0, 0], LEFT).set_y(calls[0].get_y())
        bt = label(r"its node: \ lives on", font_size=15, color=YES).set_y(blocks[0].get_y()).align_to(
            [x0 - 1.6, 0, 0], LEFT)
        st = label(r"stack", font_size=17, color=GREY_B).next_to(VGroup(mainbar, calls), LEFT, buff=0.2).align_to(
            [x0 - 1.6, 0, 0], LEFT).set_y(-0.75)
        life = VGroup(axis, tl, mainbar, mt, calls, ct, st)
        with self.voiceover(
            (
            "The stack naturally serves data whose lifetime follows a call. <bookmark mark='a'/> Many objects "
            "have different lifetimes. <bookmark mark='b'/> The Job's word table survives the functions that add "
            "entries, and its eventual size depends on input. <bookmark mark='c'/> Dynamic allocation requests "
            "storage whose lifetime lasts until it is released. In C, malloc may fail and return null; a "
            "successful allocation does not initialize its bytes. After free, aliases no longer authorize access "
            "to that object. <bookmark mark='d'/> Our allocator handles requests online, without future "
            "knowledge. With ordinary raw pointers it cannot transparently relocate a live block: existing "
            "pointers would still name its old location. Moving collectors and handle-based systems use extra "
            "machinery to update or redirect references."
        )
        ) as vo:
            self.play(FadeIn(head), FadeIn(pts[0], shift=RIGHT * 0.1), FadeIn(life))
            vo.wait_until("a")
            self.play(LaggedStart(*[GrowFromEdge(b, LEFT) for b in blocks], lag_ratio=0.3), FadeIn(bt),
                      run_time=2.0)
            for mk, p in zip("bcd", pts[1:]):
                vo.wait_until(mk)
                self.play(FadeIn(p, shift=RIGHT * 0.1))
        self.wait(0.3)
        self.clear_scene()

    def freelist(self):
        head = label(r"A free list, \ boundary tags, \ coalescing", font_size=34).to_edge(UP, buff=0.3)
        W = 11.0
        blocks = [("A", 2, True), ("", 1.5, False), ("B", 1.0, True), ("C", 2.0, True), ("", 2.5, False),
                  ("D", 2.0, True)]
        x = -W / 2
        heap = VGroup()
        for name, w, used in blocks:
            c = DATA if used else GREY_E
            r = Rectangle(width=w, height=0.8, stroke_color=GREY_B, stroke_width=1.5, fill_color=c,
                          fill_opacity=0.45 if used else 0.2).move_to([x + w / 2, 0.9, 0])
            tag = Rectangle(width=0.14, height=0.8, stroke_width=0, fill_color=HEAD, fill_opacity=0.8).move_to(
                r.get_left() + RIGHT * 0.07)
            t = label(name if used else r"free", font_size=20, color=WHITE if used else GREY_B).move_to(r)
            heap.add(VGroup(r, tag, t))
            x += w
        tagl = label(r"each block begins with a header: \ its size, \ and whether it is in use", font_size=19,
                     color=HEAD).next_to(heap, UP, buff=0.25)
        flink = VGroup(CurvedArrow(heap[1][0].get_bottom() + DOWN * 0.05, heap[4][0].get_bottom() + DOWN * 0.05,
                                   angle=0.6, color=YES))
        fl = label(r"the free blocks, \ linked into a list", font_size=19, color=YES).next_to(flink, DOWN, buff=0.1)
        steps = VGroup(
            label(r"\texttt{malloc(n)}: \ walk the free list, \ take a big enough block, \ split off the rest",
                  font_size=21, color=GREY_A),
            label(r"\texttt{free(C)}: \ its neighbours are free too \ $\to$ \ merge them into one block", font_size=21,
                  color=GREY_A),
            label(r"Knuth's \textit{boundary tags} \ (1968): \ a copy of the size at each block's end \\ lets free "
                  r"find the block before it in one step", font_size=21, color=HEAD),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.25).to_edge(DOWN, buff=0.35)
        merged = Rectangle(width=2.0 + 2.5, height=0.8, stroke_color=YES, stroke_width=2.5, fill_color=GREY_E,
                           fill_opacity=0.25).move_to(VGroup(heap[3][0], heap[4][0]))
        ml = label(r"C and its free neighbour: \ one free block", font_size=19, color=YES).move_to(merged)
        with self.voiceover("This diagram explains a classic free-list design. <bookmark mark='a'/> Divide storage into blocks with metadata recording size and allocation state. <bookmark mark='b'/> Link the free blocks into a searchable structure. <bookmark mark='c'/> To allocate, find a sufficiently large hole and split it if the remainder can form a useful free block. The request must first account for metadata and alignment. <bookmark mark='d'/> To free, coalesce adjacent free blocks. This reduces separated holes but cannot combine holes across a live object. <bookmark mark='e'/> Boundary tags record information at block boundaries so a neighbor can be found efficiently. The Python simulator represents those relationships with dictionaries and ordered lists: its eight-byte-header accounting does not charge a literal footer or reproduce native execution time.") as vo:
            self.play(FadeIn(head), run_time=0.5)
            self.play(FadeIn(heap), FadeIn(tagl), run_time=0.6)
            vo.wait_until('a')
            vo.wait_until('b')
            self.play(Create(flink), FadeIn(fl))
            vo.wait_until('c')
            self.play(FadeIn(steps[0]))
            vo.wait_until('d')
            self.play(FadeIn(steps[1]), Indicate(heap[3], color=NO))
            self.play(FadeOut(heap[3]), FadeOut(heap[4]), FadeIn(merged), FadeIn(ml))
            vo.wait_until('e')
            self.play(FadeIn(steps[2]))
        self.wait(0.3)
        self.clear_scene()

    def trace(self):
        h = load("heap")
        head = label(r"A real program's allocations", font_size=34).to_edge(UP, buff=0.3)
        prog = label(r"Perl, \ counting the words of \textit{Pride and Prejudice}: \ every \texttt{malloc} and "
                     r"\texttt{free}, \ recorded", font_size=21, color=GREY_A).next_to(head, DOWN, buff=0.2)
        how = note(r"recorded by our own \texttt{malloc}, \ slipped in front of the C library's with "
                   r"\texttt{LD\_PRELOAD} \ (chapter 11)", font_size=17).next_to(prog, DOWN, buff=0.12)
        hist = {int(k): v for k, v in h["hist"].items()}
        keys = [k for k in sorted(hist) if k <= 4096]
        names = [rf"$\le${k}" for k in keys]
        vals = [hist[k] for k in keys]
        ch = bar_chart(vals, names, [DATA] * len(vals), height=2.6, bar_w=0.32, gap=0.12, log=True,
                       fmt_=lambda v: f"{v:,}", font_size=13).to_edge(LEFT, buff=0.6).shift(DOWN * 0.9)
        cl = label(r"requests by size \ (bytes, \ log scale)", font_size=17, color=GREY_B).next_to(ch, UP, buff=0.15)
        s = h["series"]
        mx = max(v for _, v in s)
        ax = Axes(x_range=[0, s[-1][0], s[-1][0] / 4], y_range=[0, mx * 1.1, mx / 2], x_length=4.6, y_length=2.6,
                  tips=False, axis_config={"color": GREY_C, "font_size": 14}).to_edge(RIGHT, buff=0.6).shift(DOWN * 0.9)
        live = VMobject(color=YES, stroke_width=3).set_points_as_corners([ax.c2p(x, y) for x, y in s])
        al = label(rf"bytes live over time: \ peak {mx / 1e6:.2f} MB", font_size=17, color=YES).next_to(ax, UP,
                                                                                                    buff=0.15)
        tot = label(rf"{h['allocs']:,} allocations, \ {h['frees']:,} frees", font_size=21, color=HEAD).to_edge(
            DOWN, buff=0.25)
        with self.voiceover(f"To compare allocators honestly we need real requests, not made-up ones. <bookmark mark='a'/> So we recorded a real program: Perl, counting the words of Pride and Prejudice, which builds a hash table much like the one Part 17 will build. We wrote our own malloc that logs every request and then calls the real one, and slipped it in front of the C library, a trick chapter eleven explains. <bookmark mark='b'/> Over a hundred and forty thousand allocations, and most of them tiny: sixteen bytes or less, the size of a short word and its bookkeeping. <bookmark mark='c'/> And the live data climbs as the table fills, to about two megabytes. <bookmark mark='d'/> Now we can replay this exact sequence through allocators of our own.") as vo:
            self.play(FadeIn(head), run_time=0.5)
            self.play(FadeIn(prog), FadeIn(how), run_time=0.6)
            self.play(FadeIn(ch[0]), FadeIn(ch.names), FadeIn(cl), *[GrowFromEdge(b, DOWN) for b in ch.bars], FadeIn(ch.vals), run_time=0.6)
            vo.wait_until('a')
            vo.wait_until('b')
            self.play(Indicate(VGroup(*ch.bars), color=HEAD), run_time=0.6)
            vo.wait_until('c')
            self.play(Create(ax), FadeIn(al), Create(live), run_time=2)
            vo.wait_until('d')
            self.play(FadeIn(tot))
        self.wait(0.3)
        self.clear_scene()

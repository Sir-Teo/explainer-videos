from __future__ import annotations

from explainer.cs import *  # noqa: F403
from videos.cs.cs15.common import (BG, CODE, COST, CTRL, DATA, FUNC, HEAD, LAM, NO, PART, YES, cell_obj, load,
                                   mono, words)


def _fields(f):
    return ["p" if isinstance(x, str) and x not in ("f",) else (None if x is None else x) for x in f]


class Copying(VoiceoverScene):
    def construct(self):
        self.card()
        self.cheney()
        self.cost()

    def card(self):
        card = chapter_card(8, r"Cheney's copying collector, \ and what it costs", r"Can we touch only the living?",
                            lit=(1970,), extra=((1970, r"Cheney's copying collector"),), part=PART)
        with self.voiceover("Chapter eight. Cheney's copying collector, and what it costs."):
            self.play(FadeIn(card[0], shift=UP * 0.2), FadeIn(card[1]), FadeIn(card[2]))
        self.play(FadeOut(card))

    def cheney(self):
        tr = load("tracing")["trace"]
        objs = tr["objects"]
        head = label(r"Two semispaces, \ two pointers \ (Cheney, \ 1970)", font_size=34).to_edge(UP, buff=0.3)
        W = 0.4

        def make(name):
            kind, f = objs[name]
            fs = [("p" if isinstance(x, str) and x in objs else ("·" if x is None else x)) for x in f]
            fs = [None if x == "·" else x for x in fs]
            o = cell_obj(kind, fs, w=W, h=0.42, font_size=13)
            o.name = mono(name, 14, GREY_B).next_to(o, UP, buff=0.06)
            return VGroup(o, o.name)
        frm = {n: make(n) for n in tr["from_order"]}
        frow = VGroup(*[frm[n] for n in tr["from_order"]]).arrange(RIGHT, buff=0.22).move_to(UP * 1.5)
        fl = label(r"from-space", font_size=20, color=GREY_B).next_to(frow, LEFT, buff=0.3)
        if fl.get_left()[0] < -7:
            VGroup(frow, fl).shift(RIGHT * (-6.9 - fl.get_left()[0]))
        root_ar = VGroup(*[Arrow(frm[r][0].get_top() + UP * 0.75, frm[r][0].get_top() + UP * 0.32, buff=0,
                                 color=CTRL, stroke_width=2.5, tip_length=0.12) for r in tr["roots"]])
        rl = label(r"roots", font_size=17, color=CTRL).next_to(root_ar[0], LEFT, buff=0.1)
        arcs = VGroup()
        for n in tr["from_order"]:
            for k, x in enumerate(objs[n][1]):
                if isinstance(x, str) and x in objs:
                    a = frm[n][0].dots[k].get_center()
                    b = frm[x][0].get_bottom()
                    arcs.add(CurvedArrow(a + DOWN * 0.05, b + DOWN * 0.02, angle=0.9 if b[0] > a[0] else -0.9,
                                         color=GREY_D, stroke_width=1.6, tip_length=0.1))
        # to-space slots
        to_y = -0.9
        to_objs = {}
        xs = frow.get_left()[0]
        tl = label(r"to-space", font_size=20, color=GREY_B).move_to([fl.get_center()[0], to_y, 0])
        base = Line([xs, to_y - 0.35, 0], [frow.get_right()[0], to_y - 0.35, 0], color=GREY_D, stroke_width=1.5)
        cur = xs

        def place(name):
            nonlocal cur
            o = make(name)
            o[0].move_to([cur + o[0].width / 2, to_y, 0])
            o[1].next_to(o[0], UP, buff=0.06)
            cur += o[0].width + 0.22
            to_objs[name] = o
            return o

        def ptr_mark(text, color):
            ar = Arrow(DOWN * 0.45, UP * 0.05, buff=0, color=color, stroke_width=3, tip_length=0.14)
            return VGroup(ar, label(text, font_size=17, color=color).next_to(ar, DOWN, buff=0.04))
        scan = ptr_mark(r"scan", CTRL)
        free = ptr_mark(r"free", YES)

        def at(m, x):
            return m.animate.move_to([x, to_y - 0.95, 0])
        scan.move_to([xs, to_y - 0.95, 0])
        free.move_to([xs, to_y - 0.95, 0])
        pts = VGroup(
            label(r"copy each root's object to to-space; \ leave a \textbf{forwarding address} behind",
                  font_size=20, color=GREY_A),
            label(r"then scan to-space left to right: \ copy what each field points at, \ unless already copied",
                  font_size=20, color=GREY_A),
            label(r"when \textit{scan} meets \textit{free}, \ everything live has been copied: \ swap the halves",
                  font_size=20, color=YES),
        ).arrange(DOWN, buff=0.12).to_edge(DOWN, buff=0.3)
        with self.voiceover(
            "In 1970 C. J. Cheney found a collector that never looks at garbage at all. <bookmark mark='a'/> Split "
            "memory into two halves. The program allocates in one, from-space. Here a pair p holds a list of three "
            "cells; the roots point at p and at the middle cell; and three other objects are dead. <bookmark "
            "mark='b'/> To collect, copy each root's object into the empty half, to-space, and leave behind, in the "
            "old copy, a forwarding address: the new location. <bookmark mark='c'/> Now two pointers do all the "
            "work. Free marks the end of to-space. Scan walks through to-space, object by object. For every field "
            "that points into from-space, copy the target to free, unless it has already been forwarded, and "
            "update the field. <bookmark mark='d'/> When scan catches up with free, every live object has been "
            "copied, and nothing else has. The garbage was never touched. The halves swap roles, and the program "
            "continues in a heap that is perfectly compacted. Breadth-first, with no stack and no recursion: two "
            "pointers."
        ) as vo:
            self.play(FadeIn(head))
            vo.wait_until("a")
            self.play(FadeIn(frow), FadeIn(fl), Create(arcs), Create(root_ar), FadeIn(rl))
            vo.wait_until("b")
            self.play(FadeIn(tl), Create(base), FadeIn(scan), FadeIn(free), FadeIn(pts[0]))
            ev = tr["events"]
            k = 0
            # the roots
            while ev[k][0] in ("copy", "root"):
                e = ev[k]
                if e[0] == "copy":
                    o = place(e[1])
                    self.play(TransformFromCopy(frm[e[1]], o), frm[e[1]][0].animate.set_opacity(0.35), at(free, cur),
                              run_time=0.8)
                k += 1
            vo.wait_until("c")
            self.play(FadeIn(pts[1]))
            while ev[k][0] != "done":
                e = ev[k]
                if e[0] == "scan":
                    o = to_objs[e[1]]
                    self.play(at(scan, o[0].get_left()[0] + 0.05), Indicate(o[0], color=CTRL, scale_factor=1.05),
                              run_time=0.6)
                elif e[0] == "copy":
                    o = place(e[1])
                    self.play(TransformFromCopy(frm[e[1]], o), frm[e[1]][0].animate.set_opacity(0.35), at(free, cur),
                              run_time=0.8)
                k += 1
            self.play(at(scan, cur), run_time=0.6)
            vo.wait_until("d")
            self.play(FadeIn(pts[2]), *[frm[n].animate.set_opacity(0.15) for n in tr["dead"]])
        self.wait(0.3)
        self.clear_scene()

    def cost(self):
        d = load("cost")
        head = label(r"The cost: \ live data, \ not garbage", font_size=34).to_edge(UP, buff=0.3)
        rows = [r for r in d["rows"] if not r.get("oom") and r["collections"]]
        xmax = 400000
        ymax = max(r["work"] for r in rows) * 1.15
        ax = Axes(x_range=[0, xmax, 100000], y_range=[0, ymax, ymax / 4], x_length=7.6, y_length=4.0,
                  axis_config={"color": GREY_D, "include_numbers": False, "include_ticks": True}).move_to(
            LEFT * 2.6 + DOWN * 0.4)
        meas = VMobject(color=YES, stroke_width=3).set_points_as_corners(
            [ax.c2p(r["semispace"], r["work"]) for r in rows])
        dots = VGroup(*[Dot(ax.c2p(r["semispace"], r["work"]), radius=0.06, color=YES) for r in rows])
        model = VMobject(color=HEAD, stroke_width=2.5).set_points_smoothly(
            [ax.c2p(r["semispace"], r["model"]) for r in rows])
        model = DashedVMobject(model, num_dashes=40)
        xl = label(r"semispace size, \ words", font_size=18, color=GREY_B).next_to(ax, DOWN, buff=0.3)
        yl = label(r"words copied, \ in all", font_size=18, color=GREY_B).next_to(ax, UP, buff=0.1).align_to(ax, LEFT)
        ticks = VGroup(*[label(f"{v // 1000}k", font_size=15, color=GREY_B).next_to(ax.c2p(v, 0), DOWN, buff=0.1)
                         for v in (100000, 200000, 300000, 400000)])
        live = rows[0]["mean_live"]
        side = VGroup(
            label(r"each collection copies the live data, \ $L$", font_size=21, color=GREY_A),
            label(r"and buys $S - L$ words of allocation", font_size=21, color=GREY_A),
            MathTex(r"\text{work per word allocated} \;\approx\; \frac{L}{S - L}", font_size=32, color=HEAD),
            label(rf"measured: \ the Job, \ $L \approx$ {words(round(live, -2))} words", font_size=20, color=YES),
            label(r"dashed: \ the formula, \ with each run's mean $L$", font_size=19, color=HEAD),
            label(r"twice the memory, \ far less than half the work: \ memory buys time", font_size=21, color=COST),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.2).to_edge(RIGHT, buff=0.35)
        if side.width > 5.4:
            side.scale_to_fit_width(5.4)
        with self.voiceover(
            "What does copying cost? <bookmark mark='a'/> Each collection copies the live data, call it L words, "
            "and leaves the rest of the semispace, S minus L, free for the program to fill. So the work per word "
            "allocated is about L over S minus L. Garbage costs nothing at all. <bookmark mark='b'/> We ran the "
            "Job with semispaces from thirty-six thousand words up to almost four hundred thousand, and measured "
            "the words copied. The curve falls steeply: near the live data, the collector runs constantly; with "
            "room to spare, hardly at all. <bookmark mark='c'/> The dashed line is the formula, using each run's "
            "average live data. It follows the measurement. <bookmark mark='d'/> This is the central trade of "
            "garbage collection: memory for time. Give a copying collector more memory and it does less work, "
            "without limit, until it never needs to run."
        ) as vo:
            self.play(FadeIn(head), Create(ax), FadeIn(xl), FadeIn(yl), FadeIn(ticks))
            vo.wait_until("a")
            self.play(FadeIn(side[:3]))
            vo.wait_until("b")
            self.play(Create(meas), FadeIn(dots), FadeIn(side[3]), run_time=2)
            vo.wait_until("c")
            self.play(Create(model), FadeIn(side[4]))
            vo.wait_until("d")
            self.play(FadeIn(side[5]))
        self.wait(0.3)
        self.clear_scene()

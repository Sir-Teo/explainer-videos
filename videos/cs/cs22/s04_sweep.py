from __future__ import annotations

from explainer.cs import *  # noqa: F403
from videos.cs.cs22.common import (CTRL, DATA, HEAD, LAM, NO, PART, YES, fit, grid_table, load, mono, words)

COLS = [DATA, YES, LAM, HEAD, CTRL, "#e07b9a", "#7fd1d1"]


class Sweep(VoiceoverScene):
    def construct(self):
        self.card()
        self.animate_sweep()
        self.measured()

    def card(self):
        card = chapter_card(3, r"The sweep line", r"Which of $n$ segments cross, \ without testing every pair?",
                            lit=(1979,), extra=((1979, r"Bentley--Ottmann"),), part=PART)
        with self.voiceover("Chapter three. The sweep line."):
            self.play(FadeIn(card[0], shift=UP * 0.2), FadeIn(card[1]), FadeIn(card[2]))
        self.play(FadeOut(card))

    def animate_sweep(self):
        d = load("sweep")
        segs = [tuple(map(tuple, s)) for s in d["segs"]]
        allp = [p for s in segs for p in s]
        f, _ = fit(allp, center=LEFT * 2.3 + DOWN * 0.3, w=8.6, h=4.8)
        head = label(r"Bentley and Ottmann: \ sweep a vertical line", font_size=32).to_edge(UP, buff=0.3)
        S = VGroup(*[VGroup(Line(f(a), f(b), color=COLS[i], stroke_width=3),
                            mono(str(i), 16, COLS[i]).next_to(f(a), LEFT, buff=0.08)) for i, (a, b) in enumerate(segs)])
        y0, y1 = f((0, -0.4))[1], f((0, 6.4))[1]
        xmin = min(p[0] for p in allp) - 0.4
        sweep = Line([f((xmin, 0))[0], y0, 0], [f((xmin, 0))[0], y1, 0], color=HEAD, stroke_width=2.5)
        stat_head = label(r"status, \ top to bottom", font_size=20, color=GREY_A).move_to(RIGHT * 4.9 + UP * 2.4)
        ev_lab = label(r"the next event", font_size=20, color=GREY_D).move_to(RIGHT * 4.9 + DOWN * 2.7)

        def status_mob(st):
            g = VGroup(*[VGroup(RoundedRectangle(width=0.9, height=0.42, corner_radius=0.08, stroke_color=COLS[i],
                                                 stroke_width=2), mono(str(i), 18, COLS[i])) for i in st[::-1]])
            for b in g:
                b[1].move_to(b[0])
            g.arrange(DOWN, buff=0.1)
            if not len(g):
                return VGroup(VectorizedPoint(stat_head.get_bottom() + DOWN * 0.4))
            return g.next_to(stat_head, DOWN, buff=0.25)
        stat = status_mob([])
        found = {(a, b): p for a, b, p in d["found"]}
        marks = {}
        side = VGroup(
            label(r"events: \ endpoints, \ and crossings once predicted", font_size=21, color=WHITE),
            label(r"the \textbf{status}: \ the segments the line meets, \ in order", font_size=21, color=LAM),
            label(r"test only segments that become \textbf{neighbours} in the status", font_size=21, color=YES),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.2).to_edge(DOWN, buff=0.25).to_edge(LEFT, buff=0.5)
        kind_col = {"left end": DATA, "right end": GREY_B, "crossing": NO}
        with self.voiceover(
            "Given n line segments, which pairs cross? Testing every pair takes n squared tests, even when almost "
            "nothing crosses. <bookmark mark='a'/> Jon Bentley and Thomas Ottmann, in 1979, swept a vertical line "
            "across the plane from left to right. It stops only at events: the endpoints of segments, and "
            "crossings, once they have been predicted. <bookmark mark='b'/> Along the way it keeps the status: the "
            "segments the line currently meets, ordered from top to bottom. <bookmark mark='c'/> The key "
            "observation is that two segments can only cross after they become neighbours in that order, so we "
            "only ever test neighbours: when a segment arrives, against the two beside it; when one leaves, the two "
            "it separated; and at a crossing, the two that swap places meet new neighbours. <bookmark mark='d'/> "
            "Watch the line move. Each crossing is found by a test made when its two segments first became adjacent, "
            "and at the crossing they trade places in the status. <bookmark mark='e'/> With a balanced tree for the "
            "status and a heap for the events, the cost is n plus k, times log n, for k crossings."
        ) as vo:
            self.play(FadeIn(head), LaggedStart(*[Create(s) for s in S], lag_ratio=0.15), run_time=2.0)
            vo.wait_until("a")
            self.play(Create(sweep), FadeIn(side[0]), FadeIn(stat_head))
            vo.wait_until("b")
            self.play(FadeIn(side[1]))
            vo.wait_until("c")
            self.play(FadeIn(side[2]))
            vo.wait_until("d")
            for e in d["log"]:
                x = f((e["x"], 0))[0]
                new = status_mob(e["status"])
                lab = label(rf"{e['kind']}" + (rf" \ {e['seg']}" if e["kind"] != "crossing" else
                                               rf" \ {e['seg']} $\times$ {e['other']}"),
                            font_size=21, color=kind_col[e["kind"]]).move_to(ev_lab)
                anims = [sweep.animate.set_x(x), Transform(stat, new), Transform(ev_lab, lab)]
                self.play(*anims, run_time=0.4)
                newly = [k for k in found if k not in marks and found[k][0] <= e["x"] + 1e-9]
                for k in newly:
                    marks[k] = Dot(f(found[k]), radius=0.09, color=NO)
                    self.play(FadeIn(marks[k], scale=1.6), run_time=0.15)
            vo.wait_until("e")
            self.play(sweep.animate.set_x(f((max(p[0] for p in allp) + 0.4, 0))[0]), run_time=0.8)
        self.wait(0.3)
        self.clear_scene()

    def measured(self):
        d = load("sweep")
        head = label(r"Short random segments in the unit square", font_size=32).to_edge(UP, buff=0.35)
        rows = [[words(r["n"]), words(r["k"]), words(r["events"]), words(r["tests"]), words(r["pairs"]),
                 f"{r['seconds'] * 1000:.0f} ms", r"yes" if r["ok"] else (r"---" if r["ok"] is None else r"NO")]
                for r in d["rows"]]
        tab = grid_table([r"segments $n$", r"crossings $k$", r"events", r"pair tests", r"all pairs", r"time",
                          r"same as brute force"], rows, widths=[1.9, 1.9, 1.5, 1.7, 1.9, 1.3, 2.6], row_h=0.5,
                         font_size=21, mono_cols=(), colors=[[WHITE, HEAD, DATA, YES, NO, GREY_A, YES]] * len(rows))
        tab.next_to(head, DOWN, buff=0.5).set_x(0)
        notes = VGroup(
            label(r"events $= 2n + k$; \ tests $\approx 2 \times$ events, \ against $n^2/2$ for brute force",
                  font_size=22, color=WHITE),
            label('balanced status: $O((n+k)\\log n)$; \\ our measured status is a plain list', font_size=22,
                  color=LAM),
            label(r"the sweep is a paradigm: \ turn a 2D problem into a sequence of 1D ones \ (Fortune's Voronoi "
                  r"sweep, \ chapter 5)", font_size=22, color=HEAD),
            label(r"in practice: \ map overlay in GIS, \ VLSI design-rule checks, \ Boolean operations on polygons "
                  r"in CAD", font_size=21, color=GREY_A),
        ).arrange(DOWN, buff=0.28).next_to(tab, DOWN, buff=0.45)
        with self.voiceover(
            "We ran our sweep on short random segments, from a hundred to three thousand. Every output pair was independently checked against all pairs after timing. <bookmark mark='a'/> On these general-position inputs, each endpoint and crossing supplies an event; neighbour tests are far fewer than all pairs. These are counts of executed tests, not a bound on total runtime. <bookmark mark='b'/> The textbook balanced-tree algorithm takes n plus k times log n. Our teaching implementation uses a plain list with linear updates, so its measured runtime does not inherit that bound. Chazelle and Edelsbrunner's 1992 algorithm achieves n log n plus k in its comparison model. <bookmark mark='c'/> The broader idea is a sweep: turn a two-dimensional question into a sequence of one-dimensional ones. Fortune's sweep will do that for Voronoi diagrams. <bookmark mark='d'/> Related sweeps support map overlay, chip design checks and polygon operations; robust production versions also need explicit degeneracy handling."
        ) as vo:
            self.play(FadeIn(head), FadeIn(VGroup(*tab.cells[0])), FadeIn(tab.rule),
                      LaggedStart(*[FadeIn(VGroup(*r)) for r in tab.cells[1:]], lag_ratio=0.3))
            for mk, nt in zip("abcd", notes):
                vo.wait_until(mk)
                self.play(FadeIn(nt))
        self.wait(0.3)
        self.clear_scene()

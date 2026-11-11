from __future__ import annotations

from explainer.cs import *  # noqa: F403
from videos.cs.cs22.common import (CTRL, DATA, HEAD, LAM, NO, PART, YES, dots, fit, grid_table, load, mono, words)


class Hulls(VoiceoverScene):
    def construct(self):
        self.card()
        self.graham()
        self.measured()
        self.lower_bound()
        self.chan()

    def card(self):
        card = chapter_card(2, r"Convex hulls", r"What is the tightest fence around a set of points?",
                            lit=(1972, 1996), extra=((1972, r"Graham's scan"), (1996, r"Chan's algorithm")), part=PART)
        with self.voiceover("Chapter two. Convex hulls."):
            self.play(FadeIn(card[0], shift=UP * 0.2), FadeIn(card[1]), FadeIn(card[2]))
        self.play(FadeOut(card))

    def graham(self):
        d = load("hulls")
        P = [tuple(p) for p in d["small"]]
        f, _ = fit(P, center=LEFT * 2.6 + DOWN * 0.35, w=7.2, h=5.6)
        head = label(r"Graham's scan", font_size=34).to_edge(UP, buff=0.3)
        pts = dots(P, f, color=GREY_A, r=0.06)
        o = tuple(d["origin"])
        od = Dot(f(o), radius=0.09, color=HEAD)
        steps = d["graham_steps"]
        side = VGroup(
            label(r"start at the lowest point", font_size=22, color=HEAD),
            label(r"sort the others by angle around it", font_size=22, color=WHITE),
            label(r"walk in that order, \ keeping a stack: \\ pop while the last two and the new point \\ turn "
                  r"\textbf{clockwise}", font_size=22, color=LAM),
            label(r"each point is pushed once and popped at most once: \\ $O(n)$ after an $O(n \log n)$ sort",
                  font_size=22, color=YES),
            label(r"Graham (1972), \ at Bell Labs, \ for a plotter's \\ 10,000 points", font_size=20, color=GREY_A),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.32).to_edge(RIGHT, buff=0.45)
        if side.width > 5.6:
            side.width = 5.6
            side.to_edge(RIGHT, buff=0.45)
        rays = VGroup(*[DashedLine(f(o), f(tuple(s["p"])), color=GREY_D, stroke_width=1, dash_length=0.06)
                        for s in steps])

        def chain(st):
            pts_ = [f(tuple(p)) for p in st]
            if len(pts_) < 2:
                return VMobject()
            return VMobject(color=LAM, stroke_width=3).set_points_as_corners(pts_)
        cur = chain([o])
        hull = Polygon(*[f(tuple(p)) for p in d["small_hull"]], color=YES, stroke_width=3.5)
        with self.voiceover(
            "The convex hull of a set of points is the smallest convex polygon that contains them all: stretch a "
            "rubber band around nails and let go. <bookmark mark='a'/> Ronald Graham's scan, from 1972, starts at "
            "the lowest point, <bookmark mark='b'/> sorts the others by the angle they make with it, <bookmark "
            "mark='c'/> and walks through them in that order, keeping the hull so far on a stack. Each new point "
            "is pushed; but first, while the last two points on the stack and the new one turn clockwise, the last "
            "point cannot be on the hull, and is popped. <bookmark mark='d'/> Every point is pushed once and "
            "popped at most once, so after sorting the walk is linear. <bookmark mark='e'/> Graham needed it at "
            "Bell Labs, for a plotter drawing ten thousand points."
        ) as vo:
            self.play(FadeIn(head), FadeIn(pts))
            vo.wait_until("a")
            self.play(FadeIn(od), FadeIn(side[0]))
            vo.wait_until("b")
            self.play(LaggedStart(*[Create(r) for r in rays], lag_ratio=0.05), FadeIn(side[1]), run_time=2.0)
            vo.wait_until("c")
            self.play(FadeIn(side[2]), FadeOut(rays))
            self.add(cur)
            for s in steps:
                new = chain([o] + [tuple(p) for p in s["stack"][1:]])
                anims = [Transform(cur, new)]
                if s["popped"]:
                    anims += [Flash(f(tuple(q)), color=NO, flash_radius=0.18, line_length=0.12) for q in s["popped"]]
                self.play(*anims, run_time=0.32)
            vo.wait_until("d")
            self.play(FadeIn(side[3]), FadeIn(hull))
            vo.wait_until("e")
            self.play(FadeIn(side[4]))
        self.wait(0.3)
        self.clear_scene()

    def measured(self):
        d = load("hulls")
        head = label(r"Five hull algorithms, \ counting their work", font_size=32).to_edge(UP, buff=0.35)
        rows = []
        for r in d["rows"]:
            if r["n"] != 10000:
                continue
            rows.append([rf"{r['dist']}", words(r["h"]),
                         words(r["jarvis"]) if r["jarvis"] is not None else r"---",
                         words(r["graham"] + r["graham_cmp"]), words(r["monotone"] + r["monotone_cmp"]),
                         words(r["quickhull"]), words(r["chan"] + r["chan_cmp"])])
        tab = grid_table([r"10,000 points in a", r"$h$", r"Jarvis $nh$", r"Graham", r"monotone chain",
                          r"quickhull", r"Chan"], rows, widths=[2.6, 1.2, 2.0, 1.7, 2.1, 1.7, 1.7], row_h=0.5,
                         font_size=21, mono_cols=(), colors=[[WHITE, GREY_A, NO, DATA, YES, LAM, HEAD]] * len(rows))
        tab.next_to(head, DOWN, buff=0.45).set_x(0)
        notes = VGroup(
            label('orientation/determinant evaluations + sort-comparator calls; \\\\ nested evaluations count in both; \\\\ dash = unmeasured', font_size=20, color=GREY_A),
            label(r"Jarvis (1973), \ gift wrapping: \ $h$ rounds of $n$ tests: \ fine for a square, \ hopeless on a "
                  r"circle", font_size=21, color=NO),
            label(r"Graham and Andrew's monotone chain \ (1979): \ the sort dominates, \ $\approx n \log_2 n$",
                  font_size=21, color=YES),
            label(r"quickhull: \ like quicksort, \ fast on random points, \ quadratic in the worst case",
                  font_size=21, color=LAM),
            label('Chan (1996): \\ output-sensitive $O(n\\log h)$ theory; \\ compare these particular implementations', font_size=21, color=HEAD),
        ).arrange(DOWN, buff=0.24).next_to(tab, DOWN, buff=0.4)
        with self.voiceover(
            "These counters compare five teaching implementations on seeded point sets. <bookmark mark='a'/> The square and disk have small hulls. The rounded circle has many hull vertices, but rounding means some generated points are not extreme. The table reports the actual h. <bookmark mark='b'/> Jarvis wraps one vertex per round and checks the points again. The largest circle run is left unmeasured, shown by a dash; it is not replaced with an invented count. <bookmark mark='c'/> Graham and Andrew's monotone chain sort before scanning. Here we add orientation or determinant evaluations and sorting-comparator calls, including a determinant used inside a comparison in both named counters. This is a chosen work metric, not elapsed CPU time. <bookmark mark='d'/> Quickhull counts its farthest-point determinants too and divides around farthest points; its worst case is quadratic even when some random cases are cheap. <bookmark mark='e'/> Chan's bound depends on output size. Our groups use sorting hulls and binary tangents, and the measured constants belong to this implementation and these inputs. No universal library winner follows from this table."
        ) as vo:
            self.play(FadeIn(head), FadeIn(VGroup(*tab.cells[0])), FadeIn(tab.rule), FadeIn(notes[0]))
            vo.wait_until("a")
            self.play(LaggedStart(*[FadeIn(VGroup(*r[:2])) for r in tab.cells[1:]], lag_ratio=0.3))
            for mk, cols, nt in zip("bcde", ((2,), (3, 4), (5,), (6,)), notes[1:]):
                vo.wait_until(mk)
                self.play(*[FadeIn(tab.cells[r][c]) for r in range(1, len(tab.cells)) for c in cols], FadeIn(nt))
        self.wait(0.3)
        self.clear_scene()

    def lower_bound(self):
        d = load("hulls")
        xs = d["sort_xs"]
        head = label(r"Why $n \log n$ is unavoidable", font_size=34).to_edge(UP, buff=0.35)
        sx, sy = 0.08, 0.0021
        base = LEFT * 3.2 + DOWN * 2.6

        def P(x, y):
            return base + np.array([x * sx, y * sy, 0])
        par = ParametricFunction(lambda t: P(t, t * t), t_range=[-42, 42], color=GREY_D, stroke_width=1.5)
        axis = Line(P(-45, 0), P(45, 0), color=GREY_B, stroke_width=1.5)
        nums = VGroup(*[VGroup(Dot(P(x, 0), radius=0.06, color=DATA), mono(str(x), 15, DATA).next_to(P(x, 0), DOWN,
                                                                                                    buff=0.12))
                        for x in xs])
        lifted = VGroup(*[Dot(P(x, x * x), radius=0.07, color=HEAD) for x in xs])
        drops = VGroup(*[DashedLine(P(x, 0), P(x, x * x), color=GREY_D, stroke_width=1, dash_length=0.06) for x in xs])
        hull = d["sort_hull"]
        hpoly = Polygon(*[P(*p) for p in hull], color=YES, stroke_width=2.5)
        order = VGroup(*[mono(str(k + 1), 15, YES).next_to(P(*p), UP + LEFT * 0.3, buff=0.08)
                         for k, p in enumerate(hull)])
        side = VGroup(
            label(r"to sort $x_1, \dots, x_n$: \\ lift each to $(x_i, x_i^2)$", font_size=23, color=WHITE),
            label(r"every lifted point is on the hull \\ (the parabola is convex)", font_size=23, color=HEAD),
            label(r"reading the hull counter-clockwise \\ from the leftmost point lists them in order", font_size=23,
                  color=YES),
            label(r"so a hull faster than $n \log n$ \\ would sort faster than $n \log n$: \\ impossible for "
                  r"comparisons \ (Part 16), \\ and for algebraic decision trees \\ (Ben-Or, 1983)", font_size=22,
                  color=NO),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.3).to_edge(RIGHT, buff=0.4).shift(UP * 0.6)
        if side.width > 6.3:
            side.width = 6.3
            side.to_edge(RIGHT, buff=0.4)
        with self.voiceover(
            "Could a cleverer algorithm avoid the n log n? No, and the proof is a reduction. <bookmark mark='a'/> "
            "Suppose you want to sort some numbers. Lift each number x to the point x, x squared. <bookmark "
            "mark='b'/> All the lifted points lie on a parabola, which is convex, so every one of them is a vertex "
            "of the hull. <bookmark mark='c'/> Walk around the hull from the leftmost point and you meet them in "
            "sorted order. <bookmark mark='d'/> So any hull algorithm is also a sorting algorithm, with linear "
            "extra work. Part 16 proved that sorting by comparisons needs n log n; Michael Ben-Or extended the "
            "bound in 1983 to algorithms that compute with arithmetic and test signs, which is what hull "
            "algorithms do."
        ) as vo:
            self.play(FadeIn(head), Create(axis), FadeIn(nums))
            vo.wait_until("a")
            self.play(Create(par), FadeIn(side[0]))
            self.play(LaggedStart(*[Create(x) for x in drops], lag_ratio=0.1),
                      LaggedStart(*[FadeIn(x) for x in lifted], lag_ratio=0.1), run_time=2.0)
            vo.wait_until("b")
            self.play(FadeIn(side[1]), Create(hpoly))
            vo.wait_until("c")
            self.play(FadeIn(side[2]), LaggedStart(*[FadeIn(x) for x in order], lag_ratio=0.25), run_time=2.0)
            vo.wait_until("d")
            self.play(FadeIn(side[3]))
        self.wait(0.3)
        self.clear_scene()

    def chan(self):
        head = label(r"Output-sensitive: \ $O(n \log h)$", font_size=34).to_edge(UP, buff=0.35)
        lines = VGroup(
            label(r"but $n \log n$ is the price when $h \approx n$; \ when the hull is small, \ can we pay less?",
                  font_size=22, color=WHITE),
            label('Chan (1996): \\ groups of $m$; \\ each sorted hull costs $O(m\\log m)$', font_size=22, color=DATA),
            label(r"then wrap the whole set like Jarvis, \ finding the next vertex in each group's hull by \textbf{binary "
                  r"search} for its tangent", font_size=22, color=LAM),
            label(r"$h$ rounds of $\frac{n}{m} \log m$: \ with $m = h$, \ $O(n \log h)$ in all", font_size=22,
                  color=YES),
            label(r"$h$ is unknown: \ guess $m = 2^{2^t}$ for $t = 1, 2, \dots$ \ and give up after $m$ rounds; \ the "
                  r"failed guesses cost a geometric series", font_size=22, color=HEAD),
            label('Kirkpatrick--Seidel (1986): \\ planar $O(n\\log h)$; \\\\ Chan (1996) gives output-sensitive algorithms in both 2D and 3D', font_size=20,
                  color=GREY_A),
        ).arrange(DOWN, buff=0.32).next_to(head, DOWN, buff=0.45)
        with self.voiceover(
            "There is a loophole. <bookmark mark='a'/> The lower bound needs every point on the hull. When the hull has only h vertices, can we pay n log h? <bookmark mark='b'/> Timothy Chan's algorithm splits the points into groups of m and finds each group's hull with a sorting method; our instrument uses the monotone chain. <bookmark mark='c'/> Then it wraps the whole set like Jarvis: to find the next vertex, it asks each small hull for its tangent from the current point, which a binary search answers in log m steps. <bookmark mark='d'/> If m equals h, that is h rounds of n over m times log m, and n log h in all. <bookmark mark='e'/> We don't know h, so Chan guesses: m equal to four, then sixteen, then two hundred and fifty-six, squaring each time, and abandons a guess after m rounds. The failed guesses form a geometric series and cost nothing extra in order. <bookmark mark='f'/> Kirkpatrick and Seidel reached n log h first, in 1986, under the title The ultimate planar convex hull algorithm. Chan's 1996 paper also gives an output-sensitive algorithm in three dimensions; the general n log n construction is not the only bound."
        ) as vo:
            self.play(FadeIn(head))
            for mk, ln in zip("abcdef", lines):
                vo.wait_until(mk)
                self.play(FadeIn(ln, shift=UP * 0.1))
        self.wait(0.3)
        self.clear_scene()

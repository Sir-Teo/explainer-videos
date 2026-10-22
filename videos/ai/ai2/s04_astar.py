from __future__ import annotations

import numpy as np

from explainer.ai import *  # noqa: F403
from videos.ai.ai2.common import (COLORS, FAIL, FCOL, GCOST, HEUR, HIST, PART, PATH, cell_center, frontier_rgb,
                                  grid_frame, image_from_rgb, live_image, load, path_line)


def clipped(points, box) -> VMobject:
    """A closed curve drawn only where it lies inside ``box`` (x0, x1, y0, y1)."""
    x0, x1, y0, y1 = box
    m = VMobject()
    run = []
    for p in list(points) + [points[0]]:
        if x0 <= p[0] <= x1 and y0 <= p[1] <= y1:
            run.append(p)
        else:
            if len(run) > 1:
                m.start_new_path(run[0])
                m.add_points_as_corners(run[1:])
            run = []
    if len(run) > 1:
        m.start_new_path(run[0])
        m.add_points_as_corners(run[1:])
    return m


class AStar(VoiceoverScene):
    def construct(self):
        self.card()
        self.idea()
        self.race()
        self.optimal()
        self.consistent()
        self.batch()

    def card(self):
        card = chapter_card(3, r"A*", r"Can a search know where it is going?", lit=(1968,), part=PART)
        with self.voiceover("Chapter three. A star."):
            self.play(FadeIn(card[0], shift=UP * 0.2), FadeIn(card[1]))
        self.play(FadeOut(card))

    # ------------------------------------------------------------------
    def idea(self):
        f = cmath(r"f(n)", r"=", r"g(n)", r"+", r"h(n)", font_size=60).move_to(UP * 1.6)
        f[0].set_color(FCOL)
        f[2].set_color(GCOST)
        f[4].set_color(HEUR)
        bg = brace_note(f[2], r"cost so far: \ known", color=GCOST, font_size=24)
        bh = brace_note(f[4], r"estimate of the cost to go", color=HEUR, font_size=24)
        bg[1].align_to(bg[0], RIGHT)
        bh[1].align_to(bh[0], LEFT)
        hc = history_card(1968, r"Peter Hart, Nils Nilsson \& Bertram Raphael, \ SRI", r"for Shakey, the first mobile "
                          r"robot that planned its own moves: \ expand the frontier state with the smallest $f$",
                          width=6.4, color=HIST).move_to(DOWN * 2.0)
        ex = label(r"on a map: \ $h$ = the straight-line distance to the goal", font_size=26, color=HEUR)
        ex.next_to(hc, UP, buff=0.3)
        # Shakey's problem, from the first word: a route across a map with walls
        d = load("grid")
        free = np.asarray(d["free"]).astype(bool)
        H, W = free.shape
        mp = image_from_rgb(frontier_rgb(free, np.asarray(d["dijkstra_order"]), 0), width=3.3)
        mp.move_to([0, 0.95, 0])
        sr, sc = d["start"]
        gr, gc = d["goal"]
        prob = Group(mp, grid_frame(mp), Dot(cell_center(mp, (H, W), sr, sc), radius=0.08, color=WHITE),
                      Star(n=5, outer_radius=0.13, color=PATH, fill_opacity=1).move_to(cell_center(mp, (H, W), gr, gc)))
        prob.add(label(r"start", font_size=20, color=GREY_A).next_to(prob[2], DOWN, buff=0.1),
                 label(r"goal", font_size=20, color=PATH).next_to(prob[3], DOWN, buff=0.1),
                 label(r"find a short route, \\ quickly", font_size=24, color=GREY_A).next_to(mp, RIGHT, buff=0.4))
        with self.voiceover(
            "In 1968 Peter Hart, Nils Nilsson and Bertram Raphael, at the Stanford Research Institute, needed Shakey, the "
            "first mobile robot to plan its own moves, to find paths quickly. <bookmark mark='a'/> Their algorithm, A star, "
            "orders the frontier by f equals g plus h. <bookmark mark='b'/> g is the cost so far, as in Dijkstra's algorithm. "
            "<bookmark mark='c'/> h is a guess at the cost still to go: a heuristic. <bookmark mark='d'/> On a map, the "
            "straight-line distance to the goal."
        ) as vo:
            self.play(FadeIn(hc, shift=UP * 0.2), FadeIn(prob))
            vo.wait_until("a")
            self.play(FadeOut(prob), run_time=0.5)
            self.play(Write(f))
            vo.wait_until("b")
            self.play(FadeIn(bg))
            vo.wait_until("c")
            self.play(FadeIn(bh))
            vo.wait_until("d")
            self.play(FadeIn(ex))
        self.wait(0.3)
        self.clear_scene()

    # ------------------------------------------------------------------
    def race(self):
        d = load("grid")
        free = np.asarray(d["free"]).astype(bool)
        H, W = free.shape
        od, oa = np.asarray(d["dijkstra_order"]), np.asarray(d["astar_order"])
        nd, na = int(d["dijkstra_n"]), int(d["astar_n"])
        width = 5.3
        cl, cr = np.array([-3.5, -0.45, 0]), np.array([3.5, -0.45, 0])
        t = ValueTracker(0)  # progress, 0 to 1 of each search

        A = live_image(lambda: frontier_rgb(free, od, t.get_value() * nd, band=220.0), width, cl)
        B = live_image(lambda: frontier_rgb(free, oa, t.get_value() * na, band=30.0), width, cr)
        frames = VGroup(grid_frame(A), grid_frame(B))
        sr, sc = d["start"]
        gr, gc = d["goal"]
        marks = VGroup()
        for img in (A, B):
            marks.add(Dot(cell_center(img, (H, W), sr, sc), radius=0.09, color=WHITE),
                      Star(n=5, outer_radius=0.14, color=PATH, fill_opacity=1).move_to(cell_center(img, (H, W), gr, gc)))
        hl = label(r"Dijkstra: \ smallest $g$", font_size=26, color=GCOST).next_to(A, UP, buff=0.2)
        hr = label(r"A*: \ smallest $g + h$", font_size=26, color=FCOL).next_to(B, UP, buff=0.2)
        cnt = VGroup(label(rf"${nd:,}$ cells".replace(",", "{,}"), font_size=24, color=GCOST).next_to(A, DOWN, buff=0.15),
                     label(rf"${na:,}$ cells, \ the same path".replace(",", "{,}"), font_size=24, color=FCOL)
                     .next_to(B, DOWN, buff=0.15))
        paths = VGroup(path_line(A, (H, W), d["dijkstra_path"]), path_line(B, (H, W), d["astar_path"]))
        # the circle and the ellipse every expanded cell must lie in
        C = float(d["dijkstra_cost"])
        k = width / W

        def P(img, r, c):
            return cell_center(img, (H, W), r, c)

        box_a = (A.get_left()[0], A.get_right()[0], A.get_bottom()[1], A.get_top()[1])
        box_b = (B.get_left()[0], B.get_right()[0], B.get_bottom()[1], B.get_top()[1])
        th = np.linspace(0, TAU, 400)
        circ = [P(A, sr, sc) + C * k * np.array([np.cos(a), np.sin(a), 0]) for a in th]
        circle = clipped(circ, box_a).set_stroke(GCOST, 3)
        a_ = C / 2
        f_ = np.hypot(gr - sr, gc - sc) / 2
        b_ = np.sqrt(max(a_ ** 2 - f_ ** 2, 0))
        mid = (P(B, sr, sc) + P(B, gr, gc)) / 2
        ell = [mid + k * np.array([a_ * np.cos(a), b_ * np.sin(a), 0]) for a in th]
        ellipse = clipped(ell, box_b).set_stroke(FCOL, 3)
        cap = VGroup(label(rf"circle: \ distance from start $\le C^* = {C:.1f}$", font_size=19, color=GCOST),
                     label(r"ellipse: \ distance from start $+$ distance to goal $\le C^*$", font_size=19, color=FCOL))
        for c, m in zip(cap, cnt):
            c.next_to(m, DOWN, buff=0.1)
            c.set_x(min(max(c.get_x(), -6.95 + c.width / 2), 6.95 - c.width / 2))
        inside = (100 * d["dijkstra_inside"], 100 * d["astar_inside"])
        with self.voiceover(
            "Here are the two searches on the same map. <bookmark mark='a'/> Dijkstra spreads in every direction; A star's "
            "frontier leans toward the goal, flows around the wall, and stops. <bookmark mark='b'/> Both find the same "
            f"shortest path, of length {C:.1f}. Dijkstra expanded {nd:,} cells; A star, {na:,}. <bookmark mark='c'/> Their "
            "shapes are no accident. Call the optimal cost C star. Dijkstra only expands cells closer than C star to the start, "
            "and no path beats a straight line, so they lie in a circle of radius C star. A star only expands cells whose g plus "
            "h is below C star, so they lie in an ellipse with the start and the goal as its foci. <bookmark mark='d'/> We "
            f"checked every expanded cell: {inside[0]:.0f} percent inside the circle, {inside[1]:.0f} percent inside the ellipse."
        ) as vo:
            self.add(A, B)
            self.play(Create(frames), FadeIn(marks), FadeIn(hl), FadeIn(hr))
            vo.wait_until("a")
            self.play(t.animate.set_value(1.0), run_time=7.0, rate_func=linear)
            vo.wait_until("b")
            self.play(Create(paths[0]), Create(paths[1]), FadeIn(cnt))
            vo.wait_until("c")
            self.play(Create(circle), run_time=1.5)
            self.play(Create(ellipse), FadeIn(cap), run_time=1.5)
            vo.wait_until("d")
            self.play(Indicate(cap, color=WHITE, scale_factor=1.03))
        A.clear_updaters()
        B.clear_updaters()
        self.wait(0.3)
        self.clear_scene()

    # ------------------------------------------------------------------
    def optimal(self):
        dc = definition_card(r"admissible", r"$h$ never overestimates: \ $h(n) \le h^*(n)$, \ the true cost from $n$ "
                             r"to the nearest goal", width=6.0, font_size=23, color=HEUR).to_corner(UL, buff=0.35)
        th = theorem_card(r"A* is optimal", r"with an admissible $h$, \ the first goal A* removes from the frontier "
                          r"is a cheapest one", who=r"Hart, Nilsson \& Raphael (1968)", width=6.0, color=PATH,
                          font_size=23).to_corner(UR, buff=0.35)
        rows = [
            cmath(r"f(n)", r"=", r"g(n) + h(n)", font_size=40),
            cmath(r"f(n)", r"\le", r"g(n) + h^*(n)", font_size=40),
            cmath(r"f(n)", r"=", r"C^*", font_size=40),
            cmath(r"f(n)", r"<", r"g(G_2) = f(G_2)", font_size=40),
        ]
        whys = [why(r"$n$: a frontier state on an optimal path"), why(r"admissible"),
                why(r"$n$ lies on an optimal path"), why(r"$G_2$ a worse goal, \ $h(G_2) = 0$")]
        for r in rows:
            r[0].set_color(FCOL)
        step = ladder(self, rows, whys, keep=4, top=0.6, x=-1.6)
        # left: a straight-line guess never longer than the true route
        p0, p1 = np.array([-5.6, 0.0, 0]), np.array([-1.8, 0.0, 0])
        adm = VGroup(Dot(p0, color=WHITE), Star(n=5, outer_radius=0.14, color=PATH, fill_opacity=1).move_to(p1),
                     DashedLine(p0, p1, color=HEUR, stroke_width=3),
                     ArcBetweenPoints(p0, p1, angle=1.6, color=PATH, stroke_width=3),
                     MathTex("n", font_size=28).next_to(p0, LEFT, buff=0.12))
        adm.add(label(r"$h(n)$: \ the guess", font_size=22, color=HEUR).next_to(adm[2], UP, buff=0.12),
                label(r"$h^*(n)$: \ the true cost", font_size=22, color=PATH).next_to(adm[3], DOWN, buff=0.1))
        # right: a worse goal on the frontier, and n on an optimal path
        s0, nn, g1, g2 = (np.array(v + [0]) for v in ([1.2, -0.6], [3.2, 0.3], [5.8, 0.3], [4.6, -1.9]))
        opt = VGroup(Line(s0, nn, color=PATH, stroke_width=4), DashedLine(nn, g1, color=PATH, stroke_width=3),
                     DashedLine(s0, g2, color=FAIL, stroke_width=3), Dot(s0, color=WHITE), Dot(nn, color=FCOL),
                     Star(n=5, outer_radius=0.14, color=PATH, fill_opacity=1).move_to(g1),
                     Star(n=5, outer_radius=0.14, color=FAIL, fill_opacity=1).move_to(g2))
        opt.add(MathTex("n", font_size=28, color=FCOL).next_to(nn, UP, buff=0.1),
                label(r"optimal goal: \ cost $C^*$", font_size=20, color=PATH).next_to(g1, UP, buff=0.12),
                label(r"$G_2$: \ cost $> C^*$", font_size=20, color=FAIL).next_to(g2, RIGHT, buff=0.12),
                label(r"start", font_size=20, color=GREY_A).next_to(s0, DOWN, buff=0.1))
        opt.add(label(r"schematic", font_size=18, color=GREY_B).next_to(opt, DOWN, buff=0.2))
        concl = label(r"so $n$ comes off the frontier before $G_2$ ever does", font_size=28, color=PATH)
        concl.to_edge(DOWN, buff=0.45)
        with self.voiceover(
            "Why is A star's path the shortest? <bookmark mark='a'/> Call h admissible if it never overestimates: h of n is at "
            "most h star of n, the true cost to a goal. <bookmark mark='b'/> Then A star is optimal. Suppose a worse goal, G "
            "two, sits on the frontier. Some state n on an optimal path is on the frontier too. <bookmark mark='c'/> Its f is g "
            "plus h, <bookmark mark='d'/> at most g plus h star, because h is admissible, <bookmark mark='e'/> which is exactly C "
            "star, because n lies on an optimal path. <bookmark mark='f'/> G two costs more than C star, and its h is zero. So "
            "n always comes off the frontier first, and the optimal goal before G two."
        ) as vo:
            vo.wait_until("a")
            self.play(FadeIn(dc, shift=UP * 0.2), FadeIn(adm))
            vo.wait_until("b")
            self.play(FadeIn(th, shift=UP * 0.2), FadeIn(opt))
            for i, mk in enumerate("cdef"):
                vo.wait_until(mk)
                if i == 0:
                    self.play(FadeOut(adm), FadeOut(opt), run_time=0.6)
                step(i)
            self.play(FadeIn(concl))
        self.wait(0.3)
        self.clear_scene()

    # ------------------------------------------------------------------
    def consistent(self):
        dc = definition_card(r"consistent", r"$h(n) \le c(n, n') + h(n')$ \ for every step $n \to n'$, \ and $h = 0$ at "
                             r"goals: \ a triangle inequality", width=6.2, font_size=23, color=HEUR)
        dc.to_corner(UL, buff=0.35)
        tri = VGroup()
        pn, pn2, pg = np.array([2.6, 1.2, 0]), np.array([4.6, 2.6, 0]), np.array([6.2, 0.6, 0])
        tri.add(Line(pn, pn2, color=GCOST, stroke_width=4), DashedLine(pn2, pg, color=HEUR),
                DashedLine(pn, pg, color=HEUR))
        tri.add(Dot(pn, color=WHITE), Dot(pn2, color=WHITE), Star(n=5, outer_radius=0.14, color=PATH,
                                                                   fill_opacity=1).move_to(pg))
        tri.add(MathTex("n", font_size=30).next_to(pn, DOWN, buff=0.1), MathTex("n'", font_size=30).next_to(pn2, UP,
                                                                                                         buff=0.1),
                MathTex(r"c(n, n')", font_size=26, color=GCOST).next_to(Line(pn, pn2), LEFT, buff=0.05),
                MathTex(r"h(n')", font_size=26, color=HEUR).next_to(Line(pn2, pg).get_center(), UR, buff=0.05),
                MathTex(r"h(n)", font_size=26, color=HEUR).next_to(Line(pn, pg).get_center(), DOWN, buff=0.1))
        rows = [
            cmath(r"f(n')", r"=", r"g(n) + c(n, n') + h(n')", font_size=38),
            cmath(r"f(n')", r"\ge", r"g(n) + h(n)", font_size=38),
            cmath(r"f(n')", r"\ge", r"f(n)", font_size=38),
        ]
        whys = [why(r"$g(n') = g(n) + c(n, n')$ along the path"), why(r"consistent"), why(r"$f$ never decreases")]
        for r in rows:
            r[0].set_color(FCOL)
        step = ladder(self, rows, whys, keep=3, top=0.3, x=-1.8)
        concl = label(r"states come off the frontier in order of $f$: \\ the first time a state is expanded, its $g$ is "
                      r"already the best; \ it never has to be reopened", font_size=24, color=PATH)
        concl.to_edge(DOWN, buff=0.3)
        with self.voiceover(
            "On graphs A star wants a little more. <bookmark mark='a'/> Call h consistent if, for every step from n to n prime, "
            "h of n is at most the step's cost plus h of n prime: a triangle inequality, which the straight-line distance obeys. "
            "<bookmark mark='b'/> Then f never decreases along a path. f of n prime is g of n, plus the step, plus h of n prime; "
            "<bookmark mark='c'/> by consistency, at least g of n plus h of n: <bookmark mark='d'/> f of n. "
            "<bookmark mark='e'/> So states come off the frontier in order of f, and the first time A star expands a state, it "
            "has its best path."
        ) as vo:
            vo.wait_until("a")
            self.play(FadeIn(dc, shift=UP * 0.2), FadeIn(tri))
            for i, mk in enumerate("bcd"):
                vo.wait_until(mk)
                step(i)
            vo.wait_until("e")
            self.play(FadeIn(concl))
        self.wait(0.3)
        self.clear_scene()

    # ------------------------------------------------------------------
    def batch(self):
        d = load("grid")
        names = [(r"Dijkstra", "dijkstra", GCOST), (r"A*", "astar", FCOL), (r"weighted A*, \ $h \times 2$", "wastar", HEUR),
                 (r"greedy: \ $h$ only", "greedy", FAIL)]
        med = [float(np.median(d[f"batch_{k}_n"])) for _, k, _ in names]
        dc = np.asarray(d["batch_dijkstra_cost"])
        excess = [float(np.mean(np.asarray(d[f"batch_{k}_cost"]) / dc) - 1) for _, k, _ in names]
        worst = [float(np.max(np.asarray(d[f"batch_{k}_cost"]) / dc) - 1) for _, k, _ in names]
        n_maps = len(dc)
        g = axes([0, 4], [0, np.log10(max(med)) + 0.6], x_length=5.6, y_length=3.6,
                 ylabel=r"cells expanded \ (median, log scale)", yticks=[1, 2, 3],
                 yfmt=lambda v: rf"10^{{{int(v)}}}", center=[-3.2, -0.2, 0])
        bars = VGroup()
        for i, ((nm, k, col), m) in enumerate(zip(names, med)):
            h = g.ax.c2p(0, np.log10(m))[1] - g.ax.c2p(0, 0)[1]
            r = Rectangle(width=0.8, height=h, stroke_width=0, fill_color=col, fill_opacity=0.9)
            r.move_to(g.ax.c2p(i + 0.5, 0), aligned_edge=DOWN)
            v = MathTex(f"{m:,.0f}".replace(",", "{,}"), font_size=24, color=col).next_to(r, UP, buff=0.08)
            bars.add(VGroup(r, v))
        short = [r"Dijkstra", r"A*", r"weighted \\ A*", r"greedy"]
        xl = VGroup(*[label(sh, font_size=18, color=col).next_to(g.ax.c2p(i + 0.5, 0), DOWN, buff=0.15)
                      for i, (sh, (_, _, col)) in enumerate(zip(short, names))])
        for i, m in enumerate(xl):
            if m.width > 1.35:
                m.width = 1.35
        rows = VGroup(*[label(rf"{nm}: \ paths {100 * e:.0f}\% longer on average, \ at worst {100 * w:.0f}\%",
                              font_size=22, color=col) for (nm, _, col), e, w in zip(names, excess, worst)])
        rows.arrange(DOWN, buff=0.28, aligned_edge=LEFT).move_to([3.4, 0.4, 0])
        if rows.width > 6.4:
            rows.width = 6.4
        rows.set_x(6.9 - rows.width / 2)
        bound = label(r"weighted A* is never more than $\times 2$ off: \ $2h$ overestimates by at most a factor of $2$",
                      font_size=20, color=GREY_A).next_to(rows, DOWN, buff=0.35)
        if bound.width > 6.4:
            bound.width = 6.4
        tag = note(rf"computed: \ ${n_maps}$ random maps, \ $48 \times 80$ cells").to_corner(DR, buff=0.2)
        ratio = 100 * d["batch_ratio_median"]
        with self.voiceover(
            f"One map proves little, so we ran {n_maps} random ones. <bookmark mark='a'/> On the median map, Dijkstra expands "
            f"{med[0]:,.0f} cells and A star {med[1]:,.0f}: about {ratio:.0f} percent of the work, for the same optimal paths. "
            "<bookmark mark='b'/> Weight h by two, and weighted A star expands a median of "
            f"{med[2]:,.0f}, with paths {100 * excess[2]:.0f} percent longer on average, never more than twice the optimum. "
            f"<bookmark mark='c'/> Greedy search ignores g altogether: {med[3]:,.0f} cells, but paths {100 * excess[3]:.0f} "
            "percent longer, with no guarantee. Speed against optimality."
        ) as vo:
            self.play(FadeIn(g), FadeIn(tag))
            vo.wait_until("a")
            self.play(*[GrowFromEdge(b[0], DOWN) for b in bars[:2]], *[FadeIn(b[1]) for b in bars[:2]],
                      FadeIn(xl[:2]), FadeIn(rows[:2]))
            vo.wait_until("b")
            self.play(GrowFromEdge(bars[2][0], DOWN), FadeIn(bars[2][1]), FadeIn(xl[2]), FadeIn(rows[2]), FadeIn(bound))
            vo.wait_until("c")
            self.play(GrowFromEdge(bars[3][0], DOWN), FadeIn(bars[3][1]), FadeIn(xl[3]), FadeIn(rows[3]))
        self.wait(0.3)
        self.clear_scene()

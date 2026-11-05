from __future__ import annotations

import numpy as np

from explainer.cs import *  # noqa: F403
from videos.cs.cs18.common import (BG, CODE, COST, CTRL, DATA, FUNC, HEAD, LAM, NO, PART, YES, bar_chart, grid_table,
                                   load, mono, words)


class AStar(VoiceoverScene):
    def construct(self):
        self.card()
        self.goal()
        self.landmarks()
        self.hierarchy()
        self.measured()

    def card(self):
        card = chapter_card(9, r"How a map answers in microseconds", r"Why search where the destination isn't?",
                            lit=(1968,), extra=((1968, r"Hart, \ Nilsson and Raphael: \ A*"),
                                                (2008, r"contraction hierarchies")), part=PART)
        with self.voiceover("Chapter nine. How a map answers in microseconds."):
            self.play(FadeIn(card[0], shift=UP * 0.2), FadeIn(card[1]), FadeIn(card[2]))
        self.play(FadeOut(card))

    def _city(self, d, k=1.0, oy=-0.4):
        pos = {tuple(map(int, kk.split(","))): v for kk, v in d["pos"].items()}
        xs = [p[0] for p in pos.values()]
        ys = [p[1] for p in pos.values()]
        sc = k * min(6.0 / (max(xs) - min(xs)), 4.6 / (max(ys) - min(ys)))
        cx, cy = (max(xs) + min(xs)) / 2, (max(ys) + min(ys)) / 2
        return pos, (lambda p, ox: np.array([(p[0] - cx) * sc + ox, (p[1] - cy) * sc + oy, 0]))

    def _panel(self, d, pos, at, ox, pts, col, text, oy, w, h, s, t, r=0.024):
        g = VGroup(*[Dot(at(pos[tuple(u)], ox), radius=r, color=col) for u in pts])
        frame = Rectangle(width=w, height=h, stroke_color=GREY_D, stroke_width=1).move_to([ox, oy, 0])
        sd = Dot(at(pos[tuple(s)], ox), radius=0.08, color=WHITE)
        td = Dot(at(pos[tuple(t)], ox), radius=0.08, color=NO)
        lab = label(text, font_size=19, color=col).next_to(frame, UP, buff=0.1)
        return VGroup(frame, g, sd, td, lab)

    def goal(self):
        d = load("astar")
        head = label(r"A*: \ head for the goal \ (Hart, \ Nilsson and Raphael, \ 1968)", font_size=32).to_edge(
            UP, buff=0.3)
        pos, at = self._city(d)
        sets = VGroup()
        for name, ox, col in (("dijkstra", -3.4, DATA), ("astar", 3.4, YES)):
            pts = d["pics"][name]
            g = VGroup(*[Dot(at(pos[tuple(u)], ox), radius=0.03, color=col) for u in pts])
            frame = Rectangle(width=6.3, height=4.9, stroke_color=GREY_D, stroke_width=1).move_to([ox, -0.4, 0])
            s = Dot(at(pos[tuple(d["s"])], ox), radius=0.09, color=WHITE)
            t = Dot(at(pos[tuple(d["t"])], ox), radius=0.09, color=NO)
            lab = label(rf"{'Dijkstra' if name == 'dijkstra' else 'A*'}: \ {words(len(pts))} vertices reached",
                        font_size=20, color=col).next_to(frame, UP, buff=0.12)
            sets.add(VGroup(frame, g, s, t, lab))
        formula = MathTex(r"\text{priority} = d(v) + h(v), \qquad h(v) \le \text{true distance from } v "
                          r"\text{ to } t", font_size=28, color=HEAD).to_edge(DOWN, buff=0.35)
        with self.voiceover(
            "To find one route, Dijkstra explores in every direction, including away from the destination. "
            "<bookmark mark='a'/> On the left, one query across our city: the dots are every intersection it "
            "reached. <bookmark mark='b'/> Peter Hart, Nils Nilsson and Bertram Raphael's A star, from 1968, adds "
            "to each vertex's priority an estimate of the distance still to go. If the estimate never "
            "overestimates, the answer is still exact. <bookmark mark='c'/> Here the estimate is the straight-line "
            "distance at the speed of the fastest road, and the search, on the right, stays in a narrow band "
            "between the two points. AI, Built's second part used the same algorithm for planning."
        ) as vo:
            self.play(FadeIn(head))
            vo.wait_until("a")
            self.play(FadeIn(sets[0]))
            vo.wait_until("b")
            self.play(FadeIn(formula))
            vo.wait_until("c")
            self.play(FadeIn(sets[1]))
        self.wait(0.3)
        self.clear_scene()

    def landmarks(self):
        d = load("astar")
        P = d["pics"]
        head = label(r"Better estimates: \ landmarks \ (Goldberg and Harrelson, \ 2005)", font_size=32).to_edge(
            UP, buff=0.3)
        pos, at = self._city(d, k=0.74, oy=0.55)
        a_ = self._panel(d, pos, at, -3.3, P["astar2"], YES, rf"A*, \ straight line: \ {words(len(P['astar2']))} "
                         r"reached", 0.55, 4.8, 3.7, P["s2"], P["t2"])
        b_ = self._panel(d, pos, at, 3.3, P["alt2"], LAM, rf"landmarks: \ {words(len(P['alt2']))} reached", 0.55,
                         4.8, 3.7, P["s2"], P["t2"])
        marks = VGroup(*[Square(side_length=0.2, color=HEAD, fill_color=HEAD, fill_opacity=1).move_to(
            at(pos[c], 3.3)) for c in ((0, 0), (79, 0), (0, 59), (79, 59))])
        steps = VGroup(
            label(r"precompute exact distances from a few \textbf{landmarks} $L$ \ (here the four corners) \ to "
                  r"every vertex", font_size=20, color=GREY_A),
            MathTex(r"d(v, t) \ \ge\ d(L, t) - d(L, v) \qquad \text{(the triangle inequality)}", font_size=30,
                    color=YES),
            label(r"take the best over the landmarks: \ an estimate that knows the roads, \ not just the straight "
                  r"line", font_size=20, color=GREY_A),
            label(r"memory: \ a few numbers per vertex; \ the A* search is otherwise unchanged", font_size=20,
                  color=HEAD),
        ).arrange(DOWN, buff=0.16).to_edge(DOWN, buff=0.3)
        with self.voiceover(
            "A straight line is a weak estimate in a city where the fast roads bend. On this diagonal trip, A star "
            "with the straight-line estimate still wanders over most of the city. <bookmark mark='a'/> Andrew "
            "Goldberg and Chris Harrelson's idea: pick a few landmarks, here the four corners of the map, and "
            "precompute the exact distance from each landmark to every vertex. <bookmark mark='b'/> The triangle "
            "inequality then gives a lower bound on the distance from any vertex to the target: the landmark's "
            "distance to the target, minus its distance to the vertex. <bookmark mark='c'/> Taking the best bound "
            "over all landmarks gives an estimate shaped by the real roads, and the same search now reaches a "
            "fifth as many intersections. <bookmark mark='d'/> It costs a few numbers per vertex, and the search "
            "itself is plain A star."
        ) as vo:
            self.play(FadeIn(head), FadeIn(a_))
            vo.wait_until("a")
            self.play(FadeIn(steps[0]), FadeIn(marks), FadeIn(b_[0]))
            vo.wait_until("b")
            self.play(FadeIn(steps[1]))
            vo.wait_until("c")
            self.play(FadeIn(b_[1:]), FadeIn(steps[2]))
            vo.wait_until("d")
            self.play(FadeIn(steps[3]))
        self.wait(0.3)
        self.clear_scene()

    def hierarchy(self):
        d = load("astar")
        P = d["pics"]
        head = label(r"Contraction hierarchies \ (Geisberger et al., \ 2008)", font_size=32).to_edge(UP, buff=0.3)
        # a toy contraction: v lies on the only shortest path from u to w
        u, v, w = np.array([-5.6, 0.9, 0]), np.array([-4.2, 1.9, 0]), np.array([-2.8, 0.9, 0])
        x = np.array([-4.2, -0.2, 0])
        toy = VGroup(Line(u, v, color=GREY_B), Line(v, w, color=GREY_B), Line(u, x, color=GREY_B),
                     Line(x, w, color=GREY_B))
        tl = VGroup(mono("1", 15, HEAD).move_to((u + v) / 2 + UL * 0.2), mono("2", 15, HEAD).move_to((v + w) / 2 + UR * 0.2),
                    mono("3", 15, HEAD).move_to((u + x) / 2 + DL * 0.2), mono("4", 15, HEAD).move_to((x + w) / 2 + DR * 0.2))
        dots = VGroup(*[VGroup(Dot(p, radius=0.11, color=DATA), mono(n, 15, WHITE).next_to(p, UP if n == "v" else
                      (LEFT if n == "u" else (RIGHT if n == "w" else DOWN)), buff=0.08)) for p, n in
                        ((u, "u"), (v, "v"), (w, "w"), (x, "x"))])
        sc = DashedLine(u, w, color=YES, stroke_width=3)
        scl = mono("3", 15, YES).next_to(sc, UP, buff=0.05)
        cap = label(r"contract $v$: \ no other path from $u$ to $w$ is as short, \\ so add a shortcut of length 3",
                    font_size=19, color=GREY_A).next_to(VGroup(toy, dots), DOWN, buff=0.35).to_edge(LEFT, buff=0.5)
        pos, at = self._city(d, k=0.74, oy=0.4)
        city = VGroup(*[Dot(at(p, 3.0), radius=0.012, color=GREY_D) for p in pos.values()])
        up_s = VGroup(*[Dot(at(pos[tuple(q)], 3.0), radius=0.05, color=YES) for q in P["ch_s"]])
        up_t = VGroup(*[Dot(at(pos[tuple(q)], 3.0), radius=0.05, color=LAM) for q in P["ch_t"]])
        sd = Dot(at(pos[tuple(P["s2"])], 3.0), radius=0.08, color=WHITE)
        td = Dot(at(pos[tuple(P["t2"])], 3.0), radius=0.08, color=NO)
        clab = label(rf"the same trip: \ {len(P['ch_s']) + len(P['ch_t'])} vertices settled, \ by two upward "
                     r"searches", font_size=19, color=YES).next_to(city, UP, buff=0.12)
        steps = VGroup(
            label(r"order the vertices from least to most important \ (side streets first, \ junctions of major "
                  r"roads last)", font_size=19, color=GREY_A),
            label(r"query: \ search \textbf{upward} only, \ from both ends; \ they meet near the top", font_size=19,
                  color=YES),
            label(r"exact: \ every shortest path climbs and then descends in the order, \ with shortcuts standing "
                  r"in for the vertices removed", font_size=19, color=GREY_A),
            label(r"on continental road networks: \ a few hundred vertices per query, \ instead of millions",
                  font_size=20, color=HEAD),
        ).arrange(DOWN, buff=0.14).to_edge(DOWN, buff=0.3)
        with self.voiceover(
            "The method behind most route planners precomputes even more. <bookmark mark='a'/> Rank the "
            "intersections by importance: quiet side streets first, junctions of major roads last. <bookmark "
            "mark='b'/> Then remove them one at a time in that order. Whenever removing a vertex would destroy the "
            "only shortest path between two of its neighbours, add a shortcut edge between them with the same "
            "length. Here v is removed, and the road through it from u to w survives as a shortcut of length "
            "three. <bookmark mark='c'/> A query searches only upward in the ranking, from both ends at once, and "
            "the two searches meet near the top. On the diagonal trip they settle about a hundred intersections, "
            "scattered, because the upward edges jump across the city. <bookmark mark='d'/> It is exact, because "
            "every shortest path can be written as a climb followed by a descent, with shortcuts standing in for "
            "the vertices removed along the way. <bookmark mark='e'/> On the road network of a continent, a query "
            "settles a few hundred vertices instead of millions."
        ) as vo:
            self.play(FadeIn(head), Create(toy), FadeIn(tl), FadeIn(dots), FadeIn(city))
            vo.wait_until("a")
            self.play(FadeIn(steps[0]))
            vo.wait_until("b")
            self.play(Create(sc), FadeIn(scl), FadeIn(cap))
            self.play(dots[1].animate.set_opacity(0.2), toy[0].animate.set_opacity(0.2),
                      toy[1].animate.set_opacity(0.2), tl[:2].animate.set_opacity(0.2))
            vo.wait_until("c")
            self.play(FadeIn(sd), FadeIn(td), FadeIn(clab), FadeIn(steps[1]))
            self.play(LaggedStart(*[FadeIn(q) for q in up_s], lag_ratio=0.04),
                      LaggedStart(*[FadeIn(q) for q in up_t], lag_ratio=0.08), run_time=2.5)
            vo.wait_until("d")
            self.play(FadeIn(steps[2]))
            vo.wait_until("e")
            self.play(FadeIn(steps[3]))
        self.wait(0.3)
        self.clear_scene()

    def measured(self):
        d = load("astar")
        a = d["avg"]
        head = label(rf"Forty queries on a city of {words(d['n'])} intersections", font_size=32).to_edge(UP, buff=0.3)
        names = [r"Dijkstra", r"bidirectional", r"A*", r"landmarks", r"contraction"]
        keys = ["dijkstra", "bidirectional", "astar", "alt", "ch"]
        vals = [a[k] for k in keys]
        ch = bar_chart(vals, names, [GREY_A, DATA, YES, LAM, HEAD], height=3.6, bar_w=1.0, gap=0.9,
                       fmt_=lambda v: f"{v:,.0f}", font_size=20)
        ch.scale_to_fit_width(7.4).to_edge(LEFT, buff=0.6).set_y(-0.7)
        yl = label(r"vertices settled per query, \ average", font_size=18, color=GREY_B).next_to(ch, UP, buff=0.2)
        side = VGroup(
            label(rf"contraction: \ {d['ch_build_s']:.1f} s of preprocessing, \\ {words(d['shortcuts'])} shortcuts",
                  font_size=22, color=HEAD),
            label(rf"{a['dijkstra'] / a['ch']:.0f}$\times$ fewer vertices than Dijkstra, \\ every answer identical",
                  font_size=22, color=YES),
            label(r"the gain grows with the network: \\ a hierarchy pays most \\ where there are highways",
                  font_size=21, color=GREY_A),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.35).to_edge(RIGHT, buff=0.4)
        if side.width > 5.0:
            side.scale_to_fit_width(5.0).to_edge(RIGHT, buff=0.4)
        with self.voiceover(
            "Here are all of them on forty random queries across a city of four thousand eight hundred "
            "intersections. <bookmark mark='a'/> Plain Dijkstra settles two and a half thousand vertices per query. "
            "Searching from both ends halves that. A star, with the straight-line estimate, needs a quarter. "
            "Landmarks need under a tenth. <bookmark mark='b'/> And the contraction hierarchy, after a short "
            "preprocessing step, settles about a hundred, more than twenty times fewer than Dijkstra, with every "
            "answer identical. <bookmark mark='c'/> The advantage grows with the size of the network, which is how "
            "a phone can answer a cross-country query in a millisecond."
        ) as vo:
            self.play(FadeIn(head), FadeIn(ch[0]), FadeIn(ch.names), FadeIn(yl))
            vo.wait_until("a")
            self.play(LaggedStart(*[GrowFromEdge(b, DOWN) for b in ch.bars[:4]], lag_ratio=0.3),
                      FadeIn(ch.vals[:4]), run_time=2.5)
            vo.wait_until("b")
            self.play(GrowFromEdge(ch.bars[4], DOWN), FadeIn(ch.vals[4]), FadeIn(side[:2]))
            vo.wait_until("c")
            self.play(FadeIn(side[2]))
        self.wait(0.3)
        self.clear_scene()

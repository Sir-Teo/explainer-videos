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
        card = chapter_card(9, "Exact routes with less search", r"Why search where the destination isn't?",
                            lit=(1968,), extra=((1968, r"Hart, \ Nilsson and Raphael: \ A*"),
                                                (2008, r"contraction hierarchies")), part=PART)
        with self.voiceover("Chapter nine. Exact routes with less search."):
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
            lab = label(f"{('Dijkstra' if name == 'dijkstra' else 'A*')}: \\ {words(len(pts))} vertices expanded",
                        font_size=20, color=col).next_to(frame, UP, buff=0.12)
            sets.add(VGroup(frame, g, s, t, lab))
        formula = MathTex("\\text{priority} = d(v) + h(v), \\qquad h(v) \\le \\text{true distance from } v \\text{ to } t,\\quad h(t)=0", font_size=28, color=HEAD).to_edge(DOWN, buff=0.35)
        with self.voiceover(
            "A point-to-point search can use its destination. <bookmark mark='a'/> The left panel shows "
            "intersections actually expanded by Dijkstra on this query, not every vertex merely "
            "discovered. White is the source and red the target. <bookmark mark='b'/> A star prioritizes "
            "distance so far plus a lower bound on the remaining distance. With nonnegative edges, an "
            "admissible estimate, zero at the goal, and reopening when an improved path reaches a "
            "previously expanded vertex, the answer is exact. <bookmark mark='c'/> Our straight-line "
            "bound uses the cheapest cost per unit distance, zero point three five. It is also consistent"
            " on every city edge, so this experiment needs no reopening. The right panel shows its actual"
            " expansions."
        ) as vo:
            self.play(FadeIn(head), FadeIn(sets[0]))
            vo.wait_until("a")
            self.play(Indicate(sets[0], color=DATA, scale_factor=1.02), run_time=.7)
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
        a_ = self._panel(d, pos, at, -3.3, P["astar2"], YES, f"A*, \\ straight line: \\ {words(len(P['astar2']))} expanded", 0.55, 4.8, 3.7, P["s2"], P["t2"])
        b_ = self._panel(d, pos, at, 3.3, P["alt2"], LAM, f"landmarks: \\ {words(len(P['alt2']))} expanded", 0.55,
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
            "Road structure can give a stronger estimate than a straight line. <bookmark mark='a'/> "
            "Precompute distances to and from four landmarks once, and reuse those tables across queries."
            " On this undirected city the two directions agree. <bookmark mark='b'/> The triangle "
            "inequality bounds distance from v to the target below by distance from a landmark to the "
            "target minus distance from that landmark to v; the reverse-direction difference gives "
            "another bound. <bookmark mark='c'/> Take the largest valid bound over landmarks. The two "
            "panels show actual expansions for the same diagonal query, with both final distances checked"
            " equal. <bookmark mark='d'/> Tables cost order landmarks times vertices in storage. "
            "Preprocessing cost and expanded-vertex count are different measurements; neither is a "
            "query-latency benchmark."
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
            label("order by shortcut difference and contracted neighbours; \\ not a supplied road-importance label", font_size=19, color=GREY_A),
            label(r"query: \ search \textbf{upward} only, \ from both ends; \ they meet near the top", font_size=19,
                  color=YES),
            label("exact: \\ some shortest route has an upward-then-downward representation \\ through shortcuts", font_size=19, color=GREY_A),
            label("bounded witness search may add extra shortcuts; \\ graph and ordering affect performance",
                  font_size=20, color=HEAD),
        ).arrange(DOWN, buff=0.14).to_edge(DOWN, buff=0.3)
        with self.voiceover(
            "Contraction hierarchies precompute shortcut edges. <bookmark mark='a'/> Choose a vertex "
            "order; our implementation uses a heuristic based on added shortcuts and contracted "
            "neighbours, not a supplied road-importance label. <bookmark mark='b'/> When contracting v, "
            "preserve a path between each pair of remaining neighbours. If no equally short witness "
            "avoiding v is found, add a shortcut. Here length one plus two becomes a shortcut of three, "
            "while the alternative costs seven. <bookmark mark='c'/> The query searches upward in the "
            "order from both endpoints. The dots show those two expansion sets on the same diagonal trip."
            " <bookmark mark='d'/> Shortcuts ensure that some shortest route has an equivalent "
            "upward-then-downward representation; not every original shortest path literally has that "
            "shape. <bookmark mark='e'/> A bounded witness search can add extra shortcuts without losing "
            "correctness. Performance depends on the graph, ordering and implementation."
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
            label("one fixed synthetic city; \\\\ query latency and scaling \\\\ are unmeasured",
                  font_size=21, color=GREY_A),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.35).to_edge(RIGHT, buff=0.4)
        if side.width > 5.0:
            side.scale_to_fit_width(5.0).to_edge(RIGHT, buff=0.4)
        with self.voiceover(
            "These are forty fixed queries on one synthetic city of four thousand eight hundred "
            "intersections. <bookmark mark='a'/> The bars count actual expanded vertices, averaged over "
            "queries. Bidirectional searches count both sides; they may count an intersection twice. "
            "<bookmark mark='b'/> We independently check every reported route distance against the plain "
            "Dijkstra result. Landmark tables are reused, and hierarchy preprocessing is recorded "
            "separately as one observed build. <bookmark mark='c'/> Fewer expansions explain a possible "
            "source of savings, but do not measure response time. This experiment makes no claim about "
            "phone latency or how the ratio scales to a continental network."
        ) as vo:
            self.play(FadeIn(head), FadeIn(ch[0]), FadeIn(ch.names), FadeIn(yl), FadeIn(ch.bars[:4]), FadeIn(ch.vals[:4]))
            vo.wait_until("a")
            self.play(Indicate(ch.bars[:4], color=DATA, scale_factor=1.02), run_time=.7)
            vo.wait_until("b")
            self.play(GrowFromEdge(ch.bars[4], DOWN), FadeIn(ch.vals[4]), FadeIn(side[:2]))
            vo.wait_until("c")
            self.play(FadeIn(side[2]))
        self.wait(0.3)
        self.clear_scene()

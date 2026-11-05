from __future__ import annotations

import numpy as np

from explainer.cs import *  # noqa: F403
from videos.cs.cs18.common import (BG, CODE, COST, CTRL, DATA, FUNC, HEAD, LAM, NO, PART, YES, draw_graph, load,
                                   mono, words)


class Bfs(VoiceoverScene):
    def construct(self):
        self.card()
        self.maze()
        self.why()
        self.bipartite()

    def card(self):
        card = chapter_card(2, r"Breadth-first search", r"What is everything one step away, \ then two?", lit=(1959,),
                            extra=((1945, r"Zuse"), (1959, r"Moore: \ the shortest path through a maze")), part=PART)
        with self.voiceover("Chapter two. Breadth-first search."):
            self.play(FadeIn(card[0], shift=UP * 0.2), FadeIn(card[1]), FadeIn(card[2]))
        self.play(FadeOut(card))

    def maze(self):
        d = load("bfs")
        w, h = d["w"], d["h"]
        S = 0.42
        head = label(r"A maze, \ explored in layers", font_size=34).to_edge(UP, buff=0.3)
        origin = np.array([-(w - 1) * S / 2, (h - 1) * S / 2 - 0.35, 0])

        def at(x, y):
            return origin + np.array([x * S, -y * S, 0])
        cells = {}
        for key, dist in d["dist"].items():
            x, y = map(int, key.split(","))
            cells[(x, y)] = (Square(side_length=S * 0.92, stroke_width=0, fill_color=DATA, fill_opacity=0.0).move_to(
                at(x, y)), dist)
        walls = VGroup()
        for x0, y0, x1, y1 in d["walls"]:
            walls.add(Line(at(x0, y0), at(x1, y1), color=GREY_B, stroke_width=2))
        border = Rectangle(width=w * S, height=h * S, stroke_color=GREY_B, stroke_width=2).move_to(
            (at(0, 0) + at(w - 1, h - 1)) / 2)
        maxd = max(v for _, v in cells.values())
        groups = [VGroup() for _ in range(maxd + 1)]
        for sq, dist in cells.values():
            groups[dist].add(sq)
        path = d["path"]
        pl = VMobject(color=HEAD, stroke_width=4).set_points_as_corners([at(x, y) for x, y in path])
        start = Dot(at(0, 0), color=YES, radius=0.1)
        goal = Dot(at(w - 1, h - 1), color=NO, radius=0.1)
        note_ = label(rf"{d['layers']} layers; \ the exit is {len(path) - 1} steps away, \ and no path is shorter",
                      font_size=21, color=HEAD).to_edge(DOWN, buff=0.3)
        with self.voiceover(
            "Breadth-first search explores a graph the way a flood fills a maze. <bookmark mark='a'/> Start at one "
            "vertex. Visit all its neighbours, then all of their unvisited neighbours, layer by layer, using a "
            "first-in, first-out queue so that nearer vertices are always handled first. <bookmark mark='b'/> The "
            "colour here is the layer: the number of steps from the entrance. <bookmark mark='c'/> When the flood "
            "reaches the exit, following the recorded parents back gives a path, and it is a shortest one. Edward "
            "Moore described exactly this in 1959, for finding the shortest path through a maze."
        ) as vo:
            self.play(FadeIn(head), Create(border), FadeIn(walls), FadeIn(start), FadeIn(goal))
            vo.wait_until("a")
            batches = [groups[i:i + 4] for i in range(0, len(groups), 4)]
            for k, b in enumerate(batches):
                col = interpolate_color(ManimColor(DATA), ManimColor(LAM), k / max(len(batches) - 1, 1))
                self.play(*[sq.animate.set_fill(col, 0.75) for g in b for sq in g], run_time=0.22)
                if k == len(batches) // 3:
                    vo.wait_until("b")
            vo.wait_until("c")
            self.play(Create(pl), run_time=2)
            self.play(FadeIn(note_))
        self.wait(0.3)
        self.clear_scene()

    def why(self):
        head = label(r"Why the layers are distances", font_size=34).to_edge(UP, buff=0.3)
        steps = VGroup(
            label(r"\textbf{claim}: \ BFS removes vertices from the queue in order of their distance from $s$",
                  font_size=23, color=GREY_A),
            label(r"the queue always holds layer $k$, \ then some of layer $k + 1$, \ and nothing else", font_size=22,
                  color=GREY_A),
            label(r"so a vertex first reached from layer $k$ is at distance exactly $k + 1$: \\ any shorter path "
                  r"would have reached it from an earlier layer", font_size=22, color=YES),
            MathTex(r"\text{time } O(V + E): \ \text{each vertex enters the queue once, \ each edge is looked at twice}",
                    font_size=30, color=HEAD),
            label(r"unweighted shortest paths, \ the six degrees of a social network, \ and Cheney's "
                  r"copying collector \ (Part 15)", font_size=20, color=GREY_B),
        ).arrange(DOWN, buff=0.26).next_to(head, DOWN, buff=0.45)

        def cell(k1, x):
            col = DATA if k1 == 0 else LAM
            return VGroup(Square(side_length=0.62, color=col, fill_color=col, fill_opacity=0.35, stroke_width=2),
                          label(r"$k$" if k1 == 0 else r"$k{+}1$", font_size=19, color=WHITE)).move_to([x, -2.55, 0])
        xs = [-2.4 + 0.72 * i for i in range(8)]
        q = VGroup(*[cell(k1, x) for k1, x in zip((0, 0, 0, 1, 1), xs)])
        outl = label(r"leaves here", font_size=18, color=GREY_B).next_to(q, LEFT, buff=0.7)
        inl = label(r"joins here", font_size=18, color=GREY_B).move_to([xs[7] + 0.9, -2.55, 0])
        qcap = label(r"the queue", font_size=18, color=GREY_B).next_to(q, UP, buff=0.15).align_to(q, LEFT)
        with self.voiceover(
            "Why is the first path found a shortest one? <bookmark mark='a'/> Because the queue releases vertices "
            "in order of distance. <bookmark mark='b'/> By induction, at every moment the queue holds some vertices "
            "of layer k, followed by some of layer k plus one. <bookmark mark='c'/> A vertex first discovered while "
            "handling layer k is at distance k plus one: if a shorter path existed, its last step would come from "
            "an earlier layer, which would have discovered it sooner. <bookmark mark='d'/> Every vertex enters the "
            "queue once and every edge is examined from both ends, so the time is linear in the size of the graph. "
            "<bookmark mark='e'/> The same search measures degrees of separation in social networks, and it is how "
            "Cheney's copying collector walked the heap in Part 15."
        ) as vo:
            self.play(FadeIn(head))
            vo.wait_until("a")
            self.play(FadeIn(steps[0]))
            vo.wait_until("b")
            self.play(FadeIn(steps[1]), FadeIn(q), FadeIn(outl), FadeIn(inl), FadeIn(qcap))
            vo.wait_until("c")
            self.play(FadeIn(steps[2]))
            for _ in range(2):              # dequeue a k, enqueue its new neighbours at k + 1
                first = q[0]
                self.play(first.animate.shift(LEFT * 0.9).set_opacity(0), run_time=0.5)
                q.remove(first)
                self.play(q.animate.shift(LEFT * 0.72), run_time=0.4)
                new = cell(1, q[-1].get_center()[0] + 0.72)
                q.add(new)
                self.play(FadeIn(new, shift=LEFT * 0.3), run_time=0.4)
            vo.wait_until("d")
            self.play(FadeIn(steps[3]))
            vo.wait_until("e")
            self.play(FadeIn(steps[4]))
        self.wait(0.3)
        self.clear_scene()

    def bipartite(self):
        d = load("bfs")
        head = label(r"Two colours, \ or an odd cycle", font_size=34).to_edge(UP, buff=0.3)
        g1, n1, e1 = draw_graph({0: (-5.0, 0.8), 1: (-3.4, 1.6), 2: (-1.8, 0.8), 3: (-1.8, -0.8), 4: (-3.4, -1.6),
                                 5: (-5.0, -0.8)}, [(0, 1), (1, 2), (2, 3), (3, 4), (4, 5), (5, 0), (1, 4)])
        g2, n2, e2 = draw_graph({0: (2.2, 1.2), 1: (4.4, 1.2), 2: (3.3, -0.8)}, [(0, 1), (1, 2), (2, 0)])
        cols1 = {0: YES, 1: CTRL, 2: YES, 3: CTRL, 4: YES, 5: CTRL}
        pts = VGroup(
            label(r"colour each BFS layer alternately: \ every edge joins two colours \ $\iff$ \ \textbf{bipartite}",
                  font_size=22, color=GREY_A),
            label(r"an edge inside one layer closes an \textbf{odd cycle}, \ the proof that no 2-colouring exists",
                  font_size=22, color=NO),
            label(rf"the maze: \ bipartite \ ({'yes' if d['maze_bipartite'] else 'no'}), \ like every grid", font_size=21,
                  color=GREY_B),
            label(r"used for scheduling into two shifts, \ for checking that a matching problem is two-sided "
                  r"\ (chapter 12)", font_size=20, color=GREY_B),
        ).arrange(DOWN, buff=0.18).to_edge(DOWN, buff=0.4)
        with self.voiceover(
            "Breadth-first layers answer a second question for free. <bookmark mark='a'/> Colour the layers "
            "alternately. If every edge then joins two different colours, the graph is bipartite: its vertices "
            "split into two sides with edges only between them. <bookmark mark='b'/> If some edge joins two "
            "vertices of the same layer, the two paths from the start to them, plus that edge, form a cycle of odd "
            "length, and an odd cycle can never be two-coloured. So the search either finds the colouring or "
            "proves it impossible. <bookmark mark='c'/> Our maze, like every grid, is bipartite. <bookmark "
            "mark='d'/> Two-colouring schedules things into two shifts, and chapter twelve's matching problems "
            "need it."
        ) as vo:
            self.play(FadeIn(head), FadeIn(g1), FadeIn(g2))
            vo.wait_until("a")
            self.play(*[n1[k][0].animate.set_fill(c, 0.6) for k, c in cols1.items()], FadeIn(pts[0]))
            vo.wait_until("b")
            self.play(n2[0][0].animate.set_fill(YES, 0.6), n2[1][0].animate.set_fill(CTRL, 0.6),
                      n2[2][0].animate.set_fill(YES, 0.6), e2[(2, 0)].animate.set_color(NO).set_stroke(width=5),
                      FadeIn(pts[1]))
            vo.wait_until("c")
            self.play(FadeIn(pts[2]))
            vo.wait_until("d")
            self.play(FadeIn(pts[3]))
        self.wait(0.3)
        self.clear_scene()

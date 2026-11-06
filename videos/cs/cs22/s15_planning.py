from __future__ import annotations

from explainer.cs import *  # noqa: F403
from explainer.cs.algo import geometry as G
from videos.cs.cs22.common import (CTRL, DATA, HEAD, LAM, NO, PART, YES, fit, load, mono, words)


class Planning(VoiceoverScene):
    def construct(self):
        self.card()
        self.cspace()
        self.sampling()
        self.beyond()

    def card(self):
        card = chapter_card(14, r"Moving a robot", r"How does a robot find a way between obstacles?", lit=(1979, 1998),
                            extra=((1979, r"Lozano-P\'erez and Wesley"), (1998, r"RRTs")), part=PART)
        with self.voiceover("Chapter fourteen. Moving a robot."):
            self.play(FadeIn(card[0], shift=UP * 0.2), FadeIn(card[1]), FadeIn(card[2]))
        self.play(FadeOut(card))

    def cspace(self):
        d = load("planning")
        robot = [tuple(p) for p in d["robot"]]
        obs = [[tuple(p) for p in o] for o in d["obs"]]
        cs = [[tuple(p) for p in c] for c in d["cspace"]]
        start, goal = tuple(d["start"]), tuple(d["goal"])
        allp = [p for c in cs for p in c] + [start, goal, (goal[0] + 1.2, goal[1] + 1.0)]
        f, s = fit(allp, center=LEFT * 2.0 + DOWN * 0.4, w=9.4, h=5.4)
        head = label(r"Configuration space", font_size=34).to_edge(UP, buff=0.3)
        O = VGroup(*[Polygon(*[f(p) for p in o], color=GREY_B, stroke_width=2).set_fill(GREY_C, 0.5) for o in obs])
        C = VGroup(*[Polygon(*[f(p) for p in c], color=NO, stroke_width=1.8).set_fill(NO, 0.18) for c in cs])

        def robot_at(x, color=HEAD, op=0.7):
            return Polygon(*[f((x[0] + r[0], x[1] + r[1])) for r in robot], color=color, stroke_width=2).set_fill(
                color, op)
        R = robot_at(start)
        ref = Dot(f(start), radius=0.06, color=WHITE)
        gdot = Star(n=5, outer_radius=0.15, inner_radius=0.07, color=YES, fill_opacity=1).move_to(f(goal))
        # the robot sliding around one obstacle traces its grown copy
        o0 = cs[0]
        trace = VGroup(*[robot_at(p, color=LAM, op=0.12) for p in o0])
        V = [start, goal] + [p for c in cs for p in c]
        vis = VGroup()
        for i in range(len(V)):
            for j in range(i + 1, len(V)):
                if not any(G._seg_hits_poly(V[i], V[j], P) for P in cs):
                    vis.add(Line(f(V[i]), f(V[j]), color=GREY_D, stroke_width=0.8))
        path = [tuple(p) for p in d["path"]]
        route = VMobject(color=YES, stroke_width=4).set_points_as_corners([f(p) for p in path])
        side = VGroup(
            label(r"a triangle that can only slide", font_size=21, color=HEAD),
            label(r"grow each obstacle by the robot: \\ obstacle $\oplus\, (-$robot$)$, \ a Minkowski sum", font_size=21,
                  color=NO),
            label(r"now the robot is a \textbf{point}: \\ its reference corner", font_size=21, color=WHITE),
            label(rf"shortest paths bend only at corners: \\ the \textbf{{visibility graph}}, \ {d['edges']} edges",
                  font_size=21, color=GREY_A),
            label(rf"Dijkstra \ (Part 18): \ length {d['length']:.2f}", font_size=21, color=YES),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.3).to_edge(RIGHT, buff=0.35)
        if side.width > 4.4:
            side.width = 4.4
            side.to_edge(RIGHT, buff=0.35)
        with self.voiceover(
            "A robot must get from here to the star without touching the obstacles. Make it a triangle that can "
            "slide but not turn. <bookmark mark='a'/> The trick, due to Tomás Lozano-Pérez and Michael Wesley in "
            "1979, is to change what moves. Slide the robot around an obstacle, touching it, and its reference "
            "corner traces a bigger shape: the obstacle grown by the robot, a Minkowski sum. <bookmark mark='b'/> Do "
            "that for every obstacle. <bookmark mark='c'/> Now the robot is a single point, its reference corner, "
            "and it must avoid the grown obstacles. That is configuration space. <bookmark mark='d'/> A shortest "
            "path around polygons bends only at their corners, so join every pair of corners that can see each "
            "other: the visibility graph. <bookmark mark='e'/> Dijkstra's algorithm from Part 18 finds the shortest "
            "route through it, and the real triangle follows it, brushing the obstacles at every bend."
        ) as vo:
            self.play(FadeIn(head), FadeIn(O), FadeIn(R), FadeIn(ref), FadeIn(gdot), FadeIn(side[0]))
            vo.wait_until("a")
            self.play(LaggedStart(*[FadeIn(t) for t in trace], lag_ratio=0.3), run_time=2.5)
            self.play(FadeIn(C[0]), FadeOut(trace))
            vo.wait_until("b")
            self.play(FadeIn(side[1]), LaggedStart(*[FadeIn(c) for c in C[1:]], lag_ratio=0.3))
            vo.wait_until("c")
            self.play(FadeIn(side[2]), R.animate.set_fill(opacity=0.15).set_stroke(opacity=0.3), Indicate(ref))
            vo.wait_until("d")
            self.play(FadeIn(side[3]), LaggedStart(*[Create(v) for v in vis], lag_ratio=0.01), run_time=2.5)
            vo.wait_until("e")
            self.play(FadeIn(side[4]), Create(route), run_time=2.0)
            self.play(R.animate.set_fill(opacity=0.7).set_stroke(opacity=1.0))
            for a, b in zip(path, path[1:]):
                self.play(R.animate.shift(f(b) - f(a)), ref.animate.move_to(f(b)), run_time=1.0)
        self.wait(0.3)
        self.clear_scene()

    def sampling(self):
        d = load("planning")
        cs = [[tuple(p) for p in c] for c in d["cspace"]]
        start, goal = tuple(d["start"]), tuple(d["goal"])
        allp = [p for c in cs for p in c] + [start, goal, (goal[0] + 1.2, goal[1] + 1.0)]
        f, s = fit(allp, center=LEFT * 2.0 + DOWN * 0.4, w=9.4, h=5.4)
        head = label(r"Sampling: \ a rapidly-exploring random tree", font_size=32).to_edge(UP, buff=0.3)
        C = VGroup(*[Polygon(*[f(p) for p in c], color=NO, stroke_width=1.8).set_fill(NO, 0.18) for c in cs])
        sd = Dot(f(start), radius=0.08, color=HEAD)
        gd = Star(n=5, outer_radius=0.15, inner_radius=0.07, color=YES, fill_opacity=1).move_to(f(goal))
        nodes = [tuple(p) for p in d["rrt_nodes"]]
        par = d["rrt_parent"]
        edges = VGroup(*[Line(f(nodes[par[i]]), f(nodes[i]), color=LAM, stroke_width=1.4)
                         for i in range(1, len(nodes))])
        rp = VMobject(color=HEAD, stroke_width=3.5).set_points_as_corners([f(tuple(p)) for p in d["rrt_path"]])
        best = VMobject(color=YES, stroke_width=3).set_points_as_corners([f(tuple(p)) for p in d["path"]])
        rl = sum(np.hypot(b[0] - a[0], b[1] - a[1]) for a, b in zip(d["rrt_path"], d["rrt_path"][1:]))
        side = VGroup(
            label(r"sample a random point; \\ step from the nearest tree node towards it; \\ keep the step if it "
                  r"is free", font_size=21, color=LAM),
            label(rf"this tree: \\ {len(nodes)} nodes, \\ a path of {rl:.1f}", font_size=21, color=HEAD),
            label(rf"the visibility graph's optimum: \\ {d['length']:.2f}", font_size=21, color=YES),
            label(rf"over {len(d['rrt_runs'])} seeds: \\ all found a path, \\ {d['rrt_mean_ratio']:.2f}"
                  rf"$\times$ the optimum on average", font_size=21, color=WHITE),
            label(r"no corners needed: \\ it works in any dimension, \\ with only a collision test", font_size=21,
                  color=GREY_A),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.3).to_edge(RIGHT, buff=0.35)
        if side.width > 4.4:
            side.width = 4.4
            side.to_edge(RIGHT, buff=0.35)
        with self.voiceover(
            "The visibility graph needs the corners of every obstacle, and in higher dimensions there is no such "
            "thing to list. <bookmark mark='a'/> Steven LaValle's rapidly-exploring random tree needs only a "
            "collision test. Throw a random point into the space, find the nearest node of the tree, take a short "
            "step towards the random point, and keep the step if it hits nothing. <bookmark mark='b'/> The tree "
            "spreads into the empty space, because big unexplored regions attract the most samples, and after a "
            "hundred and thirty-seven nodes it reaches the goal. <bookmark mark='c'/> Its path is not the shortest; "
            "the green one is. <bookmark mark='d'/> Over twenty runs every tree found a way, about thirty percent "
            "longer than the optimum. Later variants, like RRT star, keep rewiring the tree and converge to the "
            "shortest path. <bookmark mark='e'/> That trade, a little length for no geometry at all, is what makes "
            "sampling the standard in robotics."
        ) as vo:
            self.play(FadeIn(head), FadeIn(C), FadeIn(sd), FadeIn(gd))
            vo.wait_until("a")
            self.play(FadeIn(side[0]))
            vo.wait_until("b")
            self.play(LaggedStart(*[Create(e) for e in edges], lag_ratio=0.04), run_time=6.0)
            self.play(FadeIn(side[1]), Create(rp), run_time=1.5)
            vo.wait_until("c")
            self.play(FadeIn(side[2]), Create(best), run_time=1.5)
            vo.wait_until("d")
            self.play(FadeIn(side[3]))
            vo.wait_until("e")
            self.play(FadeIn(side[4]))
        self.wait(0.3)
        self.clear_scene()

    def beyond(self):
        head = label(r"When the robot can turn", font_size=34).to_edge(UP, buff=0.35)
        lines = VGroup(
            label(r"rotation adds a dimension: \ configuration space is $(x, y, \theta)$; \ an arm with $k$ joints has "
                  r"$k$", font_size=22, color=WHITE),
            label(r"Reif (1979): \ the ``piano mover's problem'' with many parts is PSPACE-hard", font_size=22,
                  color=NO),
            label(r"Canny (1988): \ exact planning in time singly exponential in the dimension", font_size=22,
                  color=LAM),
            label(r"in practice, \ sample: \ probabilistic roadmaps \ (Kavraki et al., 1996) \ and random trees, \ "
                  r"in planners like OMPL and MoveIt", font_size=22, color=YES),
            label(r"the same geometry: \ collision tests \ (GJK), \ meshes for simulation, \ bounding-volume "
                  r"hierarchies for ray tracing \ (Part 51)", font_size=22, color=HEAD),
        ).arrange(DOWN, buff=0.34).next_to(head, DOWN, buff=0.55)
        with self.voiceover(
            "Real robots turn. <bookmark mark='a'/> Rotation adds a dimension: the configuration space of a rigid "
            "body in the plane is three-dimensional, and an arm with seven joints lives in seven. <bookmark "
            "mark='b'/> John Reif showed in 1979 that the general piano mover's problem, many parts moving together, "
            "is PSPACE-hard. <bookmark mark='c'/> John Canny found an exact algorithm singly exponential in the "
            "dimension, which is about the best one can hope for. <bookmark mark='d'/> In practice, planners sample, "
            "with probabilistic roadmaps and random trees like the one we just grew, and they plan for factory arms "
            "and self-driving cars. <bookmark mark='e'/> The "
            "same primitives test collisions in games, build meshes for simulation, and organize scenes for ray "
            "tracing, which Part 51 builds."
        ) as vo:
            self.play(FadeIn(head))
            for mk, ln in zip("abcde", lines):
                vo.wait_until(mk)
                self.play(FadeIn(ln, shift=UP * 0.1))
        self.wait(0.3)
        self.clear_scene()

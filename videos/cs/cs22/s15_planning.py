from __future__ import annotations

from explainer.cs import *  # noqa: F403
from explainer.cs.algo import geometry as G
from videos.cs.cs22.common import (CTRL, DATA, HEAD, LAM, NO, PART, YES, fit, load, mono, words)


class Planning(VoiceoverScene):
    def construct(self):
        self.card()
        self.cspace()
        self.collision()
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
            "Our triangular robot slides without turning. This model permits contact with obstacle boundaries and forbids interior overlap. <bookmark mark='a'/> Replace each convex obstacle by its Minkowski sum with the reflected robot. <bookmark mark='b'/> The triangle's reference point can then represent the entire translated robot. <bookmark mark='c'/> Its forbidden region is the interior of these configuration obstacles. The example uses disjoint convex obstacles. <bookmark mark='d'/> A shortest route can bend at their vertices, so join mutually visible vertices with collision-free segments. Overlapping obstacles would require the vertices of their union, including new boundary intersections, which this simple builder does not construct. <bookmark mark='e'/> Dijkstra finds the shortest path in this visibility graph. Every path edge is checked independently; the animated triangle follows the resulting route with boundary contact allowed."
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
        allp = [p for c in cs for p in c] + [start, goal, (goal[0] + 1.2, goal[1] + 1.0)] + [tuple(p) for p in d['rrt_nodes']]
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
            label('general method: \\\\ sampling, distance metric and collision tests; \\\\ no explicit corner list', font_size=21,
                  color=GREY_A),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.3).to_edge(RIGHT, buff=0.35)
        if side.width > 4.4:
            side.width = 4.4
            side.to_edge(RIGHT, buff=0.35)
        with self.voiceover(
            "Explicit visibility graphs become difficult in large configuration spaces. <bookmark mark='a'/> An RRT samples a point, finds the nearest tree node, and accepts a short collision-free step toward the sample. Our nearest-node search is a linear scan. <bookmark mark='b'/> This seeded tree reaches the goal after the displayed number of nodes. All parent edges, including branches off the final path, pass independent segment checks. <bookmark mark='c'/> Its path is longer than the visibility optimum in green. <bookmark mark='d'/> All twenty tested seeds find a path in this scene, with the displayed mean length ratio. This finite result is not a guarantee for every environment. RRT star has asymptotic optimality under its sampling, clearance and connection assumptions. <bookmark mark='e'/> Sampling avoids explicitly constructing every obstacle boundary, but still depends on the geometry of collision checking and the chosen configuration metric."
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
            label('Canny (1988), \\ semi-algebraic descriptions: \\\\ singly exponential in dimension, \\ with input-size and degree factors', font_size=22,
                  color=LAM),
            label(r"in practice, \ sample: \ probabilistic roadmaps \ (Kavraki et al., 1996) \ and random trees, \ "
                  r"in planners like OMPL and MoveIt", font_size=22, color=YES),
            label(r"the same geometry: \ collision tests \ (GJK), \ meshes for simulation, \ bounding-volume "
                  r"hierarchies for ray tracing \ (Part 51)", font_size=22, color=HEAD),
        ).arrange(DOWN, buff=0.34).next_to(head, DOWN, buff=0.55)
        with self.voiceover(
            "This panel considers broader motion-planning models. <bookmark mark='a'/> A planar rigid body that can translate and rotate has configuration coordinates x, y and theta. A robot arm adds joint coordinates. <bookmark mark='b'/> Reif's 1979 hardness result concerns general motion planning with multiple moving parts in the input; it does not make this fixed translating-triangle example PSPACE-hard. <bookmark mark='c'/> For semi-algebraic input descriptions, Canny's 1988 roadmap method has singly exponential dependence on configuration dimension, with further dependence on description size and polynomial degrees. This is a theoretical algorithm overview, beyond the simple planner we executed. <bookmark mark='d'/> Sampling planners choose a configuration metric, a sampling rule and a collision oracle. Their completeness or optimality guarantees require the corresponding clearance and connection assumptions. <bookmark mark='e'/> Collision predicates, simulation meshes and bounding-volume hierarchies connect these ideas to other applications; the later graphics part develops the ray-tracing example."
        ) as vo:
            self.play(FadeIn(head), FadeIn(lines[0]))
            for mk, ln in zip("abcde", lines):
                vo.wait_until(mk)
                if ln is not lines[0]:
                    self.play(FadeIn(ln, shift=UP * 0.1))
        self.wait(0.3)
        self.clear_scene()


    def collision(self):
        a,b=(-100.,-100.),(100.,100.)
        square=[(0.,0.),(1.,0.),(1.,1.),(0.,1.)]
        assert G._seg_hits_poly(a,b,square)
        head=label('Check the complete segment, including corner crossings',font_size=31).to_edge(UP,buff=.35)
        timeline=Line(LEFT*5.3+UP*2.,RIGHT*5.3+UP*2.,color=GREY_A,stroke_width=3)
        probes=VGroup(*[Dot(LEFT*5.3+RIGHT*(10.6*t)+UP*2.,radius=.07,color=WHITE)for t in (.25,.5,.75)])
        ticklabels=VGroup(*[MathTex(f't={t}',font_size=23).next_to(dot,UP,buff=.15)for t,dot in zip((.25,.5,.75),probes)])
        interval=Line(UP*2.,RIGHT*.053+UP*2.,color=NO,stroke_width=14)
        P=np.array([-4.4,-2.1,0]);Q=P+RIGHT*2.4;R=Q+UP*2.4;S=P+UP*2.4
        box=Polygon(P,Q,R,S,color=DATA,stroke_width=3).set_fill(DATA,.15)
        segment=Line(P-UR*.65,R+UR*.65,color=HEAD,stroke_width=3)
        interior=Line(P,R,color=NO,stroke_width=7)
        entry=Dot(P,radius=.09,color=WHITE);exit=Dot(R,radius=.09,color=WHITE)
        zoom=label('zoom near the two corner crossings',font_size=20,color=GREY_A).next_to(box,DOWN,buff=.85)
        notes=VGroup(
            MathTex(r'a=(-100,-100),\quad b=(100,100)',font_size=29,color=WHITE),
            MathTex(r'P=[0,1]^2,\quad (x,y)=(-100+200t,-100+200t)',font_size=27,color=DATA),
            label(r'strict interior: $ .5<t<.505 $',font_size=28,color=NO),
            label('all three probes miss the strict interior',font_size=23,color=HEAD),
            label('convex half-plane clipping tests the whole interval',font_size=23,color=YES),
            label('boundary contact is allowed in this planner',font_size=21,color=GREY_A),
        ).arrange(DOWN,buff=.32).move_to(RIGHT*2.25+DOWN*.45)
        if notes.width>6.5:notes.width=6.5
        notes.set_x(2.75)
        with self.voiceover("Collision checking must test a complete motion segment. <bookmark mark='a'/> Consider the diagonal from minus one hundred to one hundred against the unit square. Probes at one quarter, one half and three quarters all miss the strict interior: the middle probe lands exactly on a corner. <bookmark mark='b'/> Yet the segment crosses the obstacle between parameters one half and point five zero five. The enlarged view shows the two corner crossings and the interior between them. <bookmark mark='c'/> Our convex half-plane clipping checks the full parameter interval. This planner allows contact with obstacle boundaries; its path and tree edges are independently checked against exact rational interval calculations.") as vo:
            self.play(FadeIn(head),Create(timeline),FadeIn(notes[:2]))
            vo.wait_until('a');self.play(FadeIn(probes),FadeIn(ticklabels),FadeIn(notes[3]))
            vo.wait_until('b');self.play(Create(box),Create(segment),Create(interior),FadeIn(entry),FadeIn(exit),FadeIn(zoom),Create(interval),FadeIn(notes[2]))
            vo.wait_until('c');self.play(FadeIn(notes[4:]))
        self.wait(.3);self.clear_scene()

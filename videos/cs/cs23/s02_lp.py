from __future__ import annotations

from explainer.cs import *  # noqa: F403
from videos.cs.cs23.common import (CTRL, DATA, HEAD, LAM, NO, PART, YES, View3, grid_table, load, mono, words)


class LinearPrograms(VoiceoverScene):
    def construct(self):
        self.card()
        self.history()
        self.modelling()
        self.polytope()

    def card(self):
        card = chapter_card(1, r"Linear programs", r"What does it mean to choose the best point?", lit=(1939, 1947),
                            extra=((1939, r"Kantorovich"), (1947, r"Dantzig")), part=PART)
        with self.voiceover("Chapter one. Linear programs."):
            self.play(FadeIn(card[0], shift=UP * 0.2), FadeIn(card[1]), FadeIn(card[2]))
        self.play(FadeOut(card))

    def history(self):
        head = label(r"Maximize a linear function over linear constraints", font_size=32).to_edge(UP, buff=0.35)
        lp = MathTex(r"\max\ 5x_1 + 4x_2 + 3x_3", r"\\ \text{s.t.}\quad 2x_1 + 3x_2 + x_3 \le 5",
                     r"\\ 4x_1 + x_2 + 2x_3 \le 11", r"\\ 3x_1 + 4x_2 + 2x_3 \le 8", r"\\ x_1, x_2, x_3 \ge 0",
                     font_size=34, color=WHITE).next_to(head, DOWN, buff=0.4).to_edge(LEFT, buff=0.9)
        std = MathTex(r"\max\ c^{\mathsf T} x \quad \text{s.t.} \quad A x \le b,\ \ x \ge 0", font_size=36,
                      color=LAM)
        side = VGroup(
            label(r"three products, \ three scarce resources: \\ Chv\'atal's first example", font_size=22,
                  color=GREY_A),
            std,
            label(r"Kantorovich (1939): \ planning a plywood trust \\ in Leningrad", font_size=22, color=DATA),
            label(r"Dantzig (1947): \ scheduling for the US Air Force; \\ the word ``programming'' meant ``planning''",
                  font_size=22, color=HEAD),
            label(r"Kantorovich and Koopmans: \ Nobel prize in economics, \ 1975", font_size=22, color=GREY_A),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.32).to_edge(RIGHT, buff=0.5).shift(DOWN * 0.3)
        with self.voiceover(
            "A linear program asks for the largest value of a linear function, subject to linear inequalities. "
            "<bookmark mark='a'/> Here is a small one, the first example in Vašek Chvátal's textbook: three products "
            "with profits five, four and three, made from three scarce resources, with the amounts each product "
            "needs on the left and the supply on the right. <bookmark mark='b'/> In matrix form: maximize c "
            "transpose x subject to A x at most b, with x non-negative. <bookmark mark='c'/> Leonid Kantorovich "
            "formulated such problems in 1939 to plan a plywood trust in Leningrad. <bookmark mark='d'/> George "
            "Dantzig met them in 1947, scheduling for the US Air Force, when programming still meant planning. "
            "<bookmark mark='e'/> Kantorovich and Tjalling Koopmans shared the 1975 Nobel prize in economics for "
            "this work; Dantzig, famously, did not."
        ) as vo:
            self.play(FadeIn(head))
            vo.wait_until("a")
            self.play(FadeIn(lp), FadeIn(side[0]))
            for mk, s_ in zip("bcde", side[1:]):
                vo.wait_until(mk)
                self.play(FadeIn(s_))
        self.wait(0.3)
        self.clear_scene()

    def modelling(self):
        t = load("lp")["transport"]
        head = label(r"Modelling: \ Kantorovich's kind of problem", font_size=32).to_edge(UP, buff=0.35)
        P = [np.array([-5.7, 1.5 - 1.9 * i, 0]) for i in range(2)]
        Q = [np.array([-2.6, 2.0 - 1.35 * j, 0]) for j in range(3)]
        plants = VGroup(*[VGroup(Circle(radius=0.34, color=DATA), label(rf"{'AB'[i]}", font_size=24, color=DATA))
                          for i in range(2)])
        stores = VGroup(*[VGroup(Square(side_length=0.58, color=HEAD), label(rf"{j + 1}", font_size=24, color=HEAD))
                          for j in range(3)])
        for g, p in zip(plants, P):
            g.move_to(p)
        for g, q in zip(stores, Q):
            g.move_to(q)
        slab = VGroup(*[label(rf"makes \\ {t['supply'][i]}", font_size=18, color=DATA).next_to(plants[i], LEFT, buff=0.12)
                        for i in range(2)])
        dlab = VGroup(*[label(rf"needs {t['demand'][j]}", font_size=18, color=HEAD).next_to(stores[j], RIGHT, buff=0.12)
                        for j in range(3)])
        roads, flows, amts = VGroup(), VGroup(), VGroup()
        for i in range(2):
            for j in range(3):
                roads.add(Line(P[i], Q[j], buff=0.38, color=GREY_D, stroke_width=1.5))
                x = t["ship"][i][j]
                if x > 0:
                    fl = Line(P[i], Q[j], buff=0.38, color=YES, stroke_width=1.5 + x / 3)
                    flows.add(fl)
                    amts.add(label(rf"{x:.0f}", font_size=19, color=YES).move_to(fl.point_from_proportion(0.8) + 0.2 * UP))
        ctab = grid_table([r"cost per unit", r"store 1", r"store 2", r"store 3"],
                          [[rf"plant {'AB'[i]}"] + [rf"\${c}" for c in t["cost"][i]] for i in range(2)],
                          widths=[1.6, 0.9, 0.9, 0.9], row_h=0.36, font_size=18, mono_cols=(),
                          colors=[[DATA, GREY_A, GREY_A, GREY_A]] * 2)
        ctab.next_to(VGroup(plants, stores, slab, dlab), DOWN, buff=0.45).align_to(slab, LEFT)
        side = VGroup(
            label(r"one variable per road: \\ $x_{ij}$ units from plant $i$ to store $j$", font_size=21, color=WHITE),
            MathTex(r"\min \sum_{ij} c_{ij} x_{ij}", font_size=30, color=LAM),
            MathTex(r"\text{s.t.} \ \ \sum_j x_{ij} \le s_i,\ \ \sum_i x_{ij} = d_j,\ \ x \ge 0", font_size=28,
                    color=LAM),
            label(rf"each store from its cheapest plant: \ \${t['naive']}, \\ but plant B can't make 50", font_size=21,
                  color=NO),
            label(rf"the optimum: \ \${t['total']:.0f}, \\ store 3 split between both plants", font_size=21, color=YES),
            label(r"the tricks: \ $=$ is two $\le$; \ a free $x$ is $x^+ - x^-$; \\ $\min \max_k \ell_k(x)$ becomes "
                  r"$\min t$ with $\ell_k(x) \le t$; \\ $|x| \le t$ is two inequalities", font_size=20, color=GREY_A),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.28).to_edge(RIGHT, buff=0.4).shift(DOWN * 0.2)
        room = 7.0 - (dlab.get_right()[0] + 0.4)
        if side.width > room:
            side.width = room
            side.to_edge(RIGHT, buff=0.4).shift(DOWN * 0.2)
        with self.voiceover(
            "Most of the work of linear programming is modelling: deciding what the variables are. <bookmark "
            "mark='a'/> Here is the kind of problem Kantorovich, and independently Frank Hitchcock in 1941, studied. "
            "Two plants make thirty and forty units; three stores need twenty, twenty-five and twenty-five; each road "
            "has a cost per unit shipped. <bookmark mark='b'/> Use one variable per road, the amount sent along it. "
            "<bookmark mark='c'/> Minimize the total cost, subject to each plant's capacity and each store's demand. "
            "<bookmark mark='d'/> Serving every store from its cheapest plant would cost three hundred and fifty-five "
            "dollars, but it asks plant B for fifty units, and B makes forty. <bookmark mark='e'/> The optimum costs "
            "three hundred and sixty-five: store three is split between the two plants, and ten units travel the "
            "more expensive road. <bookmark mark='f'/> A handful of tricks bring far more problems into this form. "
            "An equation is two inequalities. A variable that may be negative is the difference of two that may not. "
            "To minimize the largest of several linear costs, add a variable t, require each cost to be at most t, and "
            "minimize t. Absolute values work the same way. That is why so much of operations research is linear "
            "programming."
        ) as vo:
            self.play(FadeIn(head))
            vo.wait_until("a")
            self.play(FadeIn(plants), FadeIn(stores), FadeIn(slab), FadeIn(dlab), LaggedStart(
                *[Create(r) for r in roads], lag_ratio=0.1), FadeIn(ctab))
            vo.wait_until("b")
            self.play(FadeIn(side[0]))
            vo.wait_until("c")
            self.play(FadeIn(side[1]), FadeIn(side[2]))
            vo.wait_until("d")
            self.play(FadeIn(side[3]))
            vo.wait_until("e")
            self.play(FadeIn(side[4]), LaggedStart(*[Create(f) for f in flows], lag_ratio=0.2), FadeIn(amts))
            vo.wait_until("f")
            self.play(FadeIn(side[5]))
        self.wait(0.3)
        self.clear_scene()

    def polytope(self):
        d = load("lp")
        head = label(r"The feasible region is a polytope", font_size=34).to_edge(UP, buff=0.3)
        view = View3(origin=LEFT * 2.6 + DOWN * 0.9, scale=1.15, th=-0.75, ph=0.42, center=(1.2, 1.0, 1.0))
        V, F = d["vertices"], d["faces"]
        poly = always_redraw(lambda: view.polytope(V, F, color=DATA, opacity=0.22))
        ax = always_redraw(lambda: view.axes(3.2))
        lev = ValueTracker(0.0)
        c = np.array(d["c"], float)
        cn = c / np.linalg.norm(c)

        def plane():
            v = lev.get_value()
            # a square patch of the plane c.x = v, centred on its closest point to the region's centre
            p0 = cn * v / np.linalg.norm(c)
            u1 = np.cross(cn, [0, 0, 1.0])
            u1 /= np.linalg.norm(u1)
            u2 = np.cross(cn, u1)
            pts = [p0 + 1.8 * (a * u1 + b * u2) + np.array([1.0, 0.6, 0.8]) - cn * np.dot(cn, [1.0, 0.6, 0.8])
                   for a, b in ((-1, -1), (1, -1), (1, 1), (-1, 1))]
            return Polygon(*[view.p(p) for p in pts], stroke_color=HEAD, stroke_width=1.5).set_fill(HEAD, 0.12)
        pl = always_redraw(plane)
        opt = always_redraw(lambda: Dot(view.p(d["opt"]), radius=0.1, color=HEAD))
        vdots = always_redraw(lambda: VGroup(*[Dot(view.p(v), radius=0.05, color=WHITE) for v in V]))
        side = VGroup(
            label(r"each inequality is a half-space; \\ together, \ a convex \textbf{polytope}", font_size=22,
                  color=DATA),
            label(rf"this one has {len(V)} vertices", font_size=22, color=WHITE),
            label(r"the objective's level sets are parallel planes, \\ $5x_1 + 4x_2 + 3x_3 = v$", font_size=22,
                  color=HEAD),
            label(rf"push the plane until it last touches: \\ a \textbf{{vertex}}, \ $x = (2, 0, 1)$, \ value "
                  rf"{d['opt_value']:.0f}", font_size=22, color=YES),
            label(r"a linear function on a polytope is maximized at a vertex: \\ finitely many places to look",
                  font_size=21, color=GREY_A),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.3).to_edge(RIGHT, buff=0.4)
        if side.width > 6.2:
            side.width = 6.2
            side.to_edge(RIGHT, buff=0.4)
        with self.voiceover(
            "Each inequality cuts space in half, and the points satisfying all of them form a convex polytope. "
            "<bookmark mark='a'/> For our three products it is this solid in three dimensions, with the axes as "
            "three of its walls. <bookmark mark='b'/> It has six corners. <bookmark mark='c'/> The objective's level "
            "sets, the points with the same profit, are parallel planes. <bookmark mark='d'/> Push the plane in the "
            "direction of more profit until it is about to leave the polytope. The last point it touches is a "
            "corner: two units of the first product and one of the third, for a profit of thirteen. <bookmark "
            "mark='e'/> That is always so: a linear function on a polytope reaches its maximum at a vertex, so "
            "there are only finitely many places to look. The difficulty is that a polytope in many dimensions can "
            "have astronomically many vertices."
        ) as vo:
            self.play(FadeIn(head))
            self.add(ax, poly, vdots)
            vo.wait_until("a")
            self.play(FadeIn(side[0]), view.th.animate.set_value(-0.25), run_time=3.0)
            vo.wait_until("b")
            self.play(FadeIn(side[1]), view.th.animate.set_value(-0.9), run_time=3.0)
            vo.wait_until("c")
            self.add(pl)
            self.play(FadeIn(side[2]), lev.animate.set_value(6.0), run_time=2.0)
            vo.wait_until("d")
            self.play(lev.animate.set_value(13.0), run_time=3.0)
            self.add(opt)
            self.play(FadeIn(side[3]), Flash(opt.get_center(), color=HEAD))
            vo.wait_until("e")
            self.play(FadeIn(side[4]), view.th.animate.set_value(-1.2), run_time=2.5)
        for m in (poly, ax, pl, opt, vdots):
            m.clear_updaters()
        self.wait(0.3)
        self.clear_scene()

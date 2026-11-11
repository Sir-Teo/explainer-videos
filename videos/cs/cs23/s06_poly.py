from __future__ import annotations

from explainer.cs import *  # noqa: F403
from videos.cs.cs23.common import (CTRL, DATA, HEAD, LAM, NO, PART, YES, grid_table, load, mono, words)


def ellipse_mob(c, P, T, color, width=2.0):
    w, U = np.linalg.eigh(np.array(P))
    pts = []
    for t in np.linspace(0, TAU, 73):
        v = U @ (np.sqrt(np.maximum(w, 1e-12)) * np.array([math.cos(t), math.sin(t)]))
        pts.append(T(np.array(c) + v))
    return VMobject(color=color, stroke_width=width).set_points_as_corners(pts)


class PolyTime(VoiceoverScene):
    def construct(self):
        self.card()
        self.ellipsoid()
        self.interior()

    def card(self):
        card = chapter_card(5, r"Polynomial time: \ ellipsoids and the central path", r"Can an LP be solved in "
                            r"polynomial time?", lit=(1979, 1984), extra=((1979, r"Khachiyan"), (1984, r"Karmarkar")),
                            part=PART)
        with self.voiceover("Chapter five. Polynomial time: ellipsoids and the central path."):
            self.play(FadeIn(card[0], shift=UP * 0.2), FadeIn(card[1]), FadeIn(card[2]))
        self.play(FadeOut(card))

    def ellipsoid(self):
        d = load("ellipsoid")
        A, b = np.array(d["A"]), np.array(d["b"])
        sc = 0.42
        O0 = np.array([-3.2, -0.4, 0])

        def T(p):
            return O0 + np.array([p[0] * sc, p[1] * sc, 0])
        head = label(r"Khachiyan's ellipsoid method", font_size=34).to_edge(UP, buff=0.3)
        # the feasible region: intersect the half-planes over a box
        reg = [(-7, -7), (7, -7), (7, 7), (-7, 7)]
        for a, bb in zip(A, b):
            out = []
            for k in range(len(reg)):
                p, q = np.array(reg[k]), np.array(reg[(k + 1) % len(reg)])
                fp, fq = a @ p - bb, a @ q - bb
                if fp <= 0:
                    out.append(tuple(p))
                if fp * fq < 0:
                    t = fp / (fp - fq)
                    out.append(tuple(p + t * (q - p)))
            reg = out
        region = Polygon(*[T(p) for p in reg], color=YES, stroke_width=2).set_fill(YES, 0.35)
        tr = d["trail"]
        E = ellipse_mob(tr[0]["c"], tr[0]["P"], T, LAM)
        cdot = Dot(T(tr[0]["c"]), radius=0.06, color=HEAD)
        side = VGroup(
            label(r"is $\{x : Ax \le b\}$ empty? \ start with a ball known to contain it", font_size=21,
                  color=WHITE),
            label(r"is the centre feasible? \ if not, \ a violated constraint cuts the ellipsoid in half", font_size=21,
                  color=NO),
            label(r"replace the half by the smallest ellipsoid containing it", font_size=21, color=LAM),
            MathTex(r"\mathrm{vol}(E_{k+1}) \le e^{-1/(2(n+1))}\ \mathrm{vol}(E_k)", font_size=30, color=HEAD),
            label(rf"here: \ {d['steps']} cuts to a feasible centre", font_size=21, color=YES),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.28).to_edge(RIGHT, buff=0.35)
        if side.width > 6.4:
            side.width = 6.4
            side.to_edge(RIGHT, buff=0.35)
        with self.voiceover(
            (
            "Khachiyan's 1979 result gives polynomial bit complexity for rational linear programming. <bookmark "
            "mark='a'/> This illustration starts with a radius-six ball whose enclosure of the target region is "
            "checked separately. <bookmark mark='b'/> If its centre violates a constraint, that constraint gives "
            "a central separating cut containing the feasible region. <bookmark mark='c'/> Replace the retained "
            "half with an enclosing ellipsoid and repeat. <bookmark mark='d'/> In exact arithmetic its volume "
            'contracts by at least the displayed factor. A full complexity argument also needs input encoding '
            'and radius or lower-dimensional feasibility treatment; small volume alone does not prove an '
            "arbitrary region empty. <bookmark mark='e'/> Our floating run finds a feasible point after nine "
            'cuts. Exhausting its numerical cut budget would mean no point found, not a general infeasibility '
            'certificate.'
        )
        ) as vo:
            self.play(FadeIn(head), FadeIn(region))
            vo.wait_until("a")
            self.play(FadeIn(side[0]), Create(E), FadeIn(cdot))
            vo.wait_until("b")
            self.play(FadeIn(side[1]))
            vo.wait_until("c")
            self.play(FadeIn(side[2]))
            volume_shown = False
            for k in range(1, len(tr)):
                if k == 3:
                    vo.wait_until("d")
                    self.play(FadeIn(side[3]))
                    volume_shown = True
                c0 = np.array(tr[k - 1]["c"])
                P0 = np.array(tr[k - 1]["P"])
                viol = A @ c0 - b
                j = int(np.argmax(viol))
                a = A[j]
                nrm = np.array([-a[1], a[0]]) / np.linalg.norm(a)
                cut = Line(T(c0 - 8 * nrm), T(c0 + 8 * nrm), color=NO, stroke_width=1.6)
                cut = cut.get_subcurve(0.3, 0.7)
                newE = ellipse_mob(tr[k]["c"], tr[k]["P"], T, LAM)
                self.play(Create(cut), run_time=0.4)
                self.play(Transform(E, newE), cdot.animate.move_to(T(tr[k]["c"])), FadeOut(cut), run_time=0.7)
                del P0
            if not volume_shown:
                vo.wait_until("d")
                self.play(FadeIn(side[3]))
            vo.wait_until("e")
            self.play(FadeIn(side[4]), Flash(cdot.get_center(), color=YES))
        self.wait(0.3)
        self.clear_scene()
        rows = [[f"{r['width']:g}", str(r["steps"])] for r in d["rows"]]
        tab = grid_table([r"region's width", r"ellipsoid steps"], rows, widths=[2.6, 2.6], row_h=0.42, font_size=21,
                         mono_cols=(), colors=[[WHITE, LAM]] * len(rows))
        head2 = label(r"Polynomial, \ but slow", font_size=34).to_edge(UP, buff=0.35)
        tab.next_to(head2, DOWN, buff=0.4).to_edge(LEFT, buff=1.0)
        notes = VGroup(
            label('these fixed 2D regions: \\ widths and actual cut counts; \\\\ no universal fitted iteration law', font_size=21,
                  color=WHITE),
            label('rational LP: \\ polynomial bit complexity; \\\\ coefficient encoding and radius assumptions matter',
                  font_size=21, color=HEAD),
            label('primarily a theoretical LP tool; \\\\ a finite numerical budget is not an infeasibility proof', font_size=21, color=NO),
            label('separation $\\equiv$ optimization: \\\\ suitable convex-set representation, \\ bounds and accuracy; \\\\ efficient separation oracle', font_size=21, color=YES),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.3).next_to(tab, RIGHT, buff=0.6).align_to(tab, UP)
        room = 7.0 - (tab.get_right()[0] + 0.5)
        if notes.width > room:
            notes.width = room
            notes.next_to(tab, RIGHT, buff=0.5).align_to(tab, UP)
        with self.voiceover(
            (
            "How many cuts do these examples take? <bookmark mark='a'/> As this fixed two-dimensional region "
            'becomes thinner, the recorded counts rise. This finite table is not a fitted universal iteration '
            "law. <bookmark mark='b'/> Polynomial bit complexity for rational LP depends on dimension and "
            'coefficient encoding; exact-arithmetic work and floating iteration counts are different '
            "measurements. <bookmark mark='c'/> Ellipsoids are primarily a theoretical tool for LP rather than "
            "the usual production solver. <bookmark mark='d'/> Their lasting result is the "
            'separation-optimization equivalence for appropriately represented, bounded convex sets with the '
            'required radius and accuracy information. Exponentially many constraints can be handled when a '
            'polynomial-time separation oracle and these representation assumptions are available.'
        )
        ) as vo:
            self.play(FadeIn(head2), FadeIn(VGroup(*tab.cells[0])), FadeIn(tab.rule),
                      LaggedStart(*[FadeIn(VGroup(*r)) for r in tab.cells[1:]], lag_ratio=0.2))
            for mk, n_ in zip("abcd", notes):
                vo.wait_until(mk)
                self.play(FadeIn(n_))
        self.wait(0.3)
        self.clear_scene()

    def interior(self):
        d = load("interior")
        A, b = np.array(d["A"]), np.array(d["b"])
        sc = 0.62
        O0 = np.array([-5.2, -2.6, 0])

        def T(p):
            return O0 + np.array([p[0] * sc, p[1] * sc, 0])
        reg = [(-1, -1), (6, -1), (6, 6), (-1, 6)]
        for a, bb in zip(A, b):
            out = []
            for k in range(len(reg)):
                p, q = np.array(reg[k]), np.array(reg[(k + 1) % len(reg)])
                fp, fq = a @ p - bb, a @ q - bb
                if fp <= 0:
                    out.append(tuple(p))
                if fp * fq < 0:
                    t = fp / (fp - fq)
                    out.append(tuple(p + t * (q - p)))
            reg = out
        head = label(r"Interior points: \ follow the central path", font_size=32).to_edge(UP, buff=0.3)
        region = Polygon(*[T(p) for p in reg], color=DATA, stroke_width=2).set_fill(DATA, 0.18)
        # barrier contours at t = 0 (the analytic centre's level sets)
        xs = np.linspace(0.02, 4.0, 90)
        pts = [p["x"] for p in d["path"]]
        path = VMobject(color=HEAD, stroke_width=3.5).set_points_smoothly([T(p) for p in pts])
        ds = VGroup(*[Dot(T(p), radius=0.045, color=HEAD) for p in pts[::3]])
        opt = Dot(T(d["opt"]), radius=0.09, color=YES)
        cvec = Arrow(T((0.4, 0.4)), T((1.2, 1.2)), buff=0, color=YES, stroke_width=3)
        del xs
        side = VGroup(
            label(r"Karmarkar (1984): \ stay \textbf{inside}, \ away from the walls", font_size=21, color=WHITE),
            MathTex(r"x^\star(t) = \arg\min_x\ -t\,c^{\mathsf T}x - \sum_i \log(b_i - a_i^{\mathsf T}x)", font_size=28,
                    color=LAM),
            label(r"the log barrier keeps $x$ inside; \ as $t \to \infty$, \ $x^\star(t)$ slides to the optimum",
                  font_size=21, color=HEAD),
            label(rf"each $t$: \ Newton steps ({d['total_newton']} total); \\ ideal central gap $m/t$; \ returned points use residual-corrected certificates", font_size=21,
                  color=WHITE),
            label('short-step theory: \\ $O(\\sqrt m\\log(1/\\varepsilon))$ with centrality control; \\\\ this teaching schedule has its own finite Newton counts',
                  font_size=21, color=YES),
            label('log barrier and Newton solves; \\\\ strict feasibility and convergence checks required',
                  font_size=20, color=GREY_A),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.28).to_edge(RIGHT, buff=0.35)
        if side.width > 6.4:
            side.width = 6.4
            side.to_edge(RIGHT, buff=0.35)
        with self.voiceover(
            (
            "Karmarkar's 1984 breakthrough made interior-point methods central to practical optimization. This "
            "illustration is a log-barrier Newton path follower. <bookmark mark='a'/> Begin strictly inside all "
            "the inequalities. <bookmark mark='b'/> Minimize minus t times the objective minus the sum of log "
            "slacks. The negative logarithms repel the boundary. <bookmark mark='c'/> Under the usual existence "
            'and nondegeneracy conditions, central points approach an optimal face as t grows; this example has '
            "the unique optimum two, three. <bookmark mark='d'/> The ideal central point has duality gap m over "
            't. Our approximate Newton points instead carry independently checked rational gap upper bounds, '
            "including stationarity residuals. <bookmark mark='e'/> The familiar square-root-m iteration theorem "
            'requires a specified short-step method and centrality control. Our one hundred twenty-seven Newton '
            "steps do not establish that theorem or a size-independent practical count. <bookmark mark='f'/> "
            'Strict feasibility, line-search convergence and the cost of linear solves all matter.'
        )
        ) as vo:
            self.play(FadeIn(head), FadeIn(region), GrowArrow(cvec))
            vo.wait_until("a")
            self.play(FadeIn(side[0]))
            vo.wait_until("b")
            self.play(FadeIn(side[1]))
            vo.wait_until("c")
            self.play(FadeIn(side[2]), Create(path), run_time=3.0)
            self.play(FadeIn(opt, scale=1.6))
            vo.wait_until("d")
            self.play(FadeIn(side[3]), LaggedStart(*[FadeIn(x, scale=1.5) for x in ds], lag_ratio=0.1))
            vo.wait_until("e")
            self.play(FadeIn(side[4]))
            vo.wait_until("f")
            self.play(FadeIn(side[5]))
        self.wait(0.3)
        self.clear_scene()

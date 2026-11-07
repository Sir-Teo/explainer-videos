from __future__ import annotations

import numpy as np

from videos.stats.stats21.common import *  # noqa: F403


class Hook(VoiceoverScene):
    def construct(self):
        self.dantzig()
        self.bakery()
        self.walk()
        self.stigler()
        self.argmin()
        self.objectives()

    def dantzig(self):
        tl = timeline(lit=(1939, 1947)).to_edge(UP, buff=0.35)
        a = history_card(1939, r"George Dantzig, \ a graduate student at Berkeley",
                         r"arrives late to Jerzy Neyman's class, \ copies two problems from the board as homework, \ and hands in "
                         r"the solutions days later, \ apologizing that they were harder than usual. \ They were open problems.",
                         color=PATH, width=11.0, font_size=23).move_to([0, 1.2, 0])
        rows = fit_rows(VGroup(
            label(r"one solution published in 1940; \ both contributed to his 1946 thesis", font_size=24),
            label(r"the other, \ with Abraham Wald (1951): \ the Neyman--Pearson lemma, \ generalized", font_size=24, color=NEWT),
            label(r"1947: \ the simplex method, \ for planning the US Air Force", font_size=24, color=PATH),
        ), 12.0, 0.35, [0, -1.7, 0])
        with self.voiceover(
            "The master's stage begins with a story statisticians like to tell. <bookmark mark='a'/> In 1939 George "
            "Dantzig, a graduate student at Berkeley, arrived late to a class of Jerzy Neyman's. Two problems were on"
            " the board, and he copied them down as homework. A few days later he handed in solutions, apologizing "
            "that they had taken longer than usual. They were two famous unsolved problems in statistics. <bookmark "
            "mark='b'/> The two solutions formed the basis of his 1946 doctoral thesis. <bookmark mark='c'/> The "
            "other, published with Abraham Wald in 1951, generalized the Neyman–Pearson lemma, and its mathematics "
            "turned out to be the duality of linear programming. <bookmark mark='d'/> By then Dantzig had invented "
            "the simplex method, in 1947, to plan the logistics of the United States Air Force."
        ) as vo:
            self.play(FadeIn(tl))
            vo.wait_until("a")
            self.play(FadeIn(a, shift=UP * 0.2))
            for k, m_ in enumerate("bcd"):
                vo.wait_until(m_)
                self.play(FadeIn(rows[k], shift=RIGHT * 0.2))
        self.clear_scene()

    def lp_axes(self):
        A = axes([0, 10], [0, 9], x_length=6.4, y_length=5.4, xlabel=r"trays of loaves, \ $x_1$", ylabel=r"trays of cakes, \ $x_2$",
                 xticks=[0, 2, 4, 6, 8, 10], yticks=[0, 2, 4, 6, 8], center=[-2.8, 0.1, 0])
        return A

    def bakery(self):
        d = load("bakery")
        A = self.lp_axes()
        ax = A.ax
        cols = [BLUE, RED, TEAL]
        names = [r"flour: \ $x_1 + 2x_2 \le 14$", r"oven: \ $3x_1 + 2x_2 \le 24$", r"staff: \ $x_1 + x_2 \le 9$"]
        lines = VGroup()
        for (a1, a2), b, c in zip(d["A"], d["b"], cols):
            pts = []
            for x1 in (0, 10):
                x2 = (b - a1 * x1) / a2
                pts.append((x1, x2))
            # clip to the axes box
            (x0, y0), (x1_, y1_) = pts
            lines.add(Line(ax.c2p(*self.clip(x0, y0, x1_, y1_)[0]), ax.c2p(*self.clip(x0, y0, x1_, y1_)[1]), color=c, stroke_width=2.5))
        poly = Polygon(*[ax.c2p(*v) for v in d["verts"]], stroke_width=0, fill_color=PATH, fill_opacity=0.18)
        rows = fit_rows(VGroup(
            label(r"the World's bakery: \ loaves earn 3, \ cakes earn 4 per tray", font_size=22),
            *[label(t, font_size=22, color=c) for t, c in zip(names, cols)],
            label(r"shaded: \ every feasible plan", font_size=22, color=PATH),
            label(r"maximize \ $3x_1 + 4x_2$", font_size=26, color=TRUE),
        ), 5.0, 0.35, [3.9, 0.2, 0])
        with self.voiceover(
            "<bookmark mark='a'/> A linear program in two dimensions shows the idea. The World's bakery bakes trays of loaves "
            "and trays of cakes, and makes three on a tray of loaves and four on a tray of cakes. <bookmark mark='b'/> But "
            "flour is limited: a tray of cakes takes two sacks, a tray of loaves one, and there are fourteen sacks. "
            "<bookmark mark='c'/> The oven has twenty-four hours, and loaves take longer. <bookmark mark='d'/> And there are "
            "nine shifts of staff. <bookmark mark='e'/> Each constraint is a half-plane; together they leave a polygon of "
            "feasible plans. <bookmark mark='f'/> The question: which plan makes the most money?"
        ) as vo:
            self.play(FadeIn(A))
            vo.wait_until("a")
            self.play(FadeIn(rows[0]))
            for k, m_ in enumerate("bcd"):
                vo.wait_until(m_)
                self.play(Create(lines[k]), FadeIn(rows[k + 1]))
            vo.wait_until("e")
            self.play(FadeIn(poly), FadeIn(rows[4]))
            vo.wait_until("f")
            self.play(FadeIn(rows[5]))
        self.wait(0.5)
        self.keep = (A, lines, poly, rows)

    @staticmethod
    def clip(x0, y0, x1, y1, xmax=10.0, ymax=9.0):
        pts = []
        for t in np.linspace(0, 1, 2001):
            x, y = x0 + t * (x1 - x0), y0 + t * (y1 - y0)
            if 0 <= x <= xmax and 0 <= y <= ymax:
                pts.append((x, y))
        return pts[0], pts[-1]

    def walk(self):
        d = load("bakery")
        A, lines, poly, old = self.keep
        ax = A.ax
        self.play(FadeOut(old))
        path = np.asarray(d["path"])
        vals = [float(np.dot(d["c"], v)) for v in path]
        iso = VGroup()
        for v in (0, 28, 32):
            # the profit line 3x1 + 4x2 = v
            p0, p1 = self.clip(0, v / 4, 10, (v - 30) / 4) if v > 0 else ((0, 0), (0.01, 0))
            iso.add(DashedLine(ax.c2p(*p0), ax.c2p(*p1), color=TRUE, stroke_width=2))
        dots = VGroup(*[Dot(ax.c2p(*v), radius=0.1, color=PATH) for v in path])
        steps = VGroup(*[Arrow(ax.c2p(*a), ax.c2p(*b), buff=0.08, color=PATH, stroke_width=4) for a, b in zip(path, path[1:])])
        dual = d["dual"]
        rows = fit_rows(VGroup(
            label(r"the simplex method: \ moves between basic feasible solutions, \ nondecreasing profit", font_size=22, color=PATH),
            label(rf"$(0, 0)$: \ {vals[0]:.0f} \ $\to$ \ $(0, 7)$: \ {vals[1]:.0f} \ $\to$ \ $(4, 5)$: \ {vals[2]:.0f}", font_size=22),
            label(r"no uphill neighbour: \ optimal", font_size=22, color=HIT),
            label(rf"shadow prices: \ flour {dual[0]:.0f}, \ oven {dual[1]:.0f}, \ staff {dual[2]:.0f}", font_size=22, color=NEWT),
            label(r"the dual problem prices the constraints: \ chapter three", font_size=20, color=GREY_A),
        ), 5.0, 0.4, [3.9, 0.2, 0])
        with self.voiceover(
            "<bookmark mark='a'/> The profit is a straight line's worth of plans at each level, so at least one optimal plan is "
            "at a corner of this bounded feasible polygon. Dantzig's simplex method moves between basic feasible solutions "
            "without decreasing profit; degenerate pivots can leave it unchanged. <bookmark mark='b'/> Start at the "
            "empty plan, profit zero. The cakes earn more, so bake cakes until flour runs out: seven trays, profit "
            "twenty-eight. Then trade cakes for loaves along the flour line until the staff run out: four trays of "
            "loaves and five of cakes, thirty-two. <bookmark mark='c'/> No neighbouring corner is higher, so this is "
            "the optimum. <bookmark mark='d'/> The method also gives shadow prices: for sufficiently small resource "
            "changes within the same optimal regime, an extra sack of flour is worth one, a staff shift two, and an "
            "oven hour nothing because the oven is slack. <bookmark mark='e'/> Those prices solve a second linear "
            "program, the dual, which is where Dantzig's homework comes back."
        ) as vo:
            self.play(FadeIn(rows[0]), FadeIn(dots[0], scale=1.5), Create(iso[0]))
            vo.wait_until("a")
            vo.wait_until("b")
            for k in range(len(steps)):
                self.play(GrowArrow(steps[k]), FadeIn(dots[k + 1], scale=1.5), Create(iso[k + 1]), run_time=1.5)
            self.play(FadeIn(rows[1]))
            for k, m_ in enumerate("cde"):
                vo.wait_until(m_)
                self.play(FadeIn(rows[k + 2]))
        self.clear_scene()

    def stigler(self):
        hc = history_card(1945, r"George Stigler: \ the cost of subsistence",
                          r"the cheapest diet meeting nine nutritional needs, \ from 77 foods at 1939 prices: \ by clever "
                          r"guessing, \ \$39.93 a year",
                          color=PATH, width=11.0, font_size=23).move_to([0, 1.6, 0])
        rows = fit_rows(VGroup(
            label(r"1947: \ Jack Laderman solves it exactly by the simplex method", font_size=24),
            label(r"9 constraints, \ 77 unknowns: \ about 120 person-days on desk calculators", font_size=24, color=GREY_A),
            label(r"the optimum: \ \$39.69 a year, \ 24 cents better than Stigler's guess", font_size=24, color=HIT),
            label(r"today: \ large sparse programs, \ with problem-dependent runtime", font_size=24, color=PATH),
        ), 12.0, 0.35, [0, -1.4, 0])
        with self.voiceover(
            "<bookmark mark='a'/> The first big test of the method was a famous puzzle. In 1945 the economist George "
            "Stigler asked for the cheapest diet that meets nine nutritional requirements, choosing among "
            "seventy-seven foods at 1939 prices. By clever trial and error he found one costing thirty-nine dollars "
            "and ninety-three cents a year. <bookmark mark='b'/> In 1947 Jack Laderman solved it exactly with "
            "Dantzig's new simplex method: nine constraints, seventy-seven unknowns, and about a hundred and twenty "
            "person-days of work on desk calculators. <bookmark mark='c'/> The true optimum was thirty-nine "
            "sixty-nine: Stigler had been within twenty-four cents. <bookmark mark='d'/> Modern solvers handle much "
            "larger sparse programs, though runtime depends on structure, conditioning and hardware."
        ) as vo:
            vo.wait_until("a")
            self.play(FadeIn(hc, shift=UP * 0.2))
            for k, m_ in enumerate("bcd"):
                vo.wait_until(m_)
                self.play(FadeIn(rows[k], shift=RIGHT * 0.2))
        self.clear_scene()

    def argmin(self):
        rows = [
            cmath(r"\bar x", r"=", r"\arg\min_\theta \textstyle\sum_i (x_i - \theta)^2", font_size=30),
            cmath(r"\text{median}", r"=", r"\arg\min_\theta \textstyle\sum_i |x_i - \theta|", font_size=30),
            cmath(r"\hat\theta_{\text{MLE}}", r"=", r"\arg\max_\theta \textstyle\sum_i \log f(x_i; \theta)", font_size=30),
            cmath(r"\hat\beta_{\text{lasso}}", r"=", r"\arg\min_\beta \tfrac{1}{2n}\|y - X\beta\|^2 + \lambda \|\beta\|_1", font_size=30),
            cmath(r"\text{this part}", r":", r"\text{how the arg min is found, \ and what its geometry says}", font_size=26),
        ]
        rows[4][2].set_color(PATH)
        whys = [why(r"a closed form"), why(r"a linear program: \ chapter four"), why(r"Newton, \ usually: \ chapter five"),
                why(r"coordinate descent, \ proximal steps"), why(r"algorithms and their guarantees")]
        intro = label('Statistical estimators are defined by optimization problems', font_size=36).move_to([0, 3.35, 0])
        if intro.width > 12.5:
            intro.width = 12.5
        with self.voiceover(
            "Why does a statistician need this? Because almost every estimator is the solution of an optimization problem. "
            "<bookmark mark='a'/> The mean minimizes squared distances, in closed form. <bookmark mark='b'/> The median "
            "minimizes absolute distances, a linear program. <bookmark mark='c'/> Maximum likelihood maximizes a log "
            "likelihood, usually with no formula at all. <bookmark mark='d'/> The lasso minimizes a penalized loss that isn't "
            "even differentiable. <bookmark mark='e'/> This part is about how those optima are found, how fast, and what the "
            "shape of the problem tells us about the estimator."
        ) as vo:
            self.play(FadeIn(intro))
            step = ladder(self, rows, whys, keep=5, top=2.8, x=-0.4, buff=0.62, edge=6.9)
            for k, m_ in enumerate("abcde"):
                vo.wait_until(m_)
                step(k, transform=False)
        self.clear_scene()

    def objectives(self):
        head = VGroup(label(r"Part 21", font_size=34, color=GREY_B), label(r"Optimization for Statistics", font_size=56),
                      label(r"Stage III: \ the master's", font_size=28, color=PATH)).arrange(DOWN, buff=0.25)
        obj = objectives_card([
            r"convexity; \ Lagrange multipliers and the KKT conditions",
            r"duality, \ and the Neyman--Pearson lemma as a linear program",
            r"linear programs: \ least absolute deviations and quantile regression",
            r"Newton and Fisher scoring; \ MM; \ coordinate descent; \ proximal methods; \ ADMM",
            r"stochastic gradient and Polyak--Ruppert averaging; \ optimization and inference",
        ], color=PATH, font_size=26)
        prereq = note(r"prerequisites: \ Parts 4, \ 9 and 19").to_corner(DL, buff=0.3)
        built = note(r"built: \ \texttt{statkit.optim}; \ the landscape").to_corner(DR, buff=0.3)
        with self.voiceover(
            "<bookmark mark='a'/> Part twenty-one: optimization for statistics. <bookmark mark='b'/> We'll meet convexity and "
            "Lagrange multipliers; duality, with the Neyman–Pearson lemma as a linear program; least absolute deviations and "
            "quantile regression; Newton's method, MM algorithms, coordinate descent, proximal methods and ADMM; stochastic "
            "gradient with averaging; and finally what an optimizer's output tells us about uncertainty."
        ) as vo:
            vo.wait_until("a")
            self.play(FadeIn(head, shift=UP * 0.2))
            vo.wait_until("b")
            self.play(FadeOut(head), FadeIn(obj, shift=UP * 0.2), FadeIn(prereq), FadeIn(built))
        self.wait(1.0)
        self.clear_scene()

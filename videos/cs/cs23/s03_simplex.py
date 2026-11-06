from __future__ import annotations

from explainer.cs import *  # noqa: F403
from videos.cs.cs23.common import (CTRL, DATA, HEAD, LAM, NO, PART, YES, View3, grid_table, load, mono, words)

VARS = ["x_1", "x_2", "x_3", "s_1", "s_2", "s_3"]


def frac_tex(s):
    if "/" in s:
        a, b = s.split("/")
        neg = a.startswith("-")
        a = a.lstrip("-")
        return ("-" if neg else "") + rf"\tfrac{{{a}}}{{{b}}}"
    return s


class Simplex(VoiceoverScene):
    def construct(self):
        self.card()
        self.walk()
        self.tableau()
        self.rules()

    def card(self):
        card = chapter_card(2, r"The simplex method", r"How do you walk to the best corner?", lit=(1947,),
                            extra=((1947, r"Dantzig's simplex"),), part=PART)
        with self.voiceover("Chapter two. The simplex method."):
            self.play(FadeIn(card[0], shift=UP * 0.2), FadeIn(card[1]), FadeIn(card[2]))
        self.play(FadeOut(card))

    def walk(self):
        d = load("lp")
        s = load("simplex")
        head = label(r"Walk along edges, \ uphill", font_size=34).to_edge(UP, buff=0.3)
        view = View3(origin=LEFT * 2.6 + DOWN * 0.9, scale=1.15, th=-0.75, ph=0.42, center=(1.2, 1.0, 1.0))
        V, F = d["vertices"], d["faces"]
        poly = always_redraw(lambda: view.polytope(V, F, color=DATA, opacity=0.2))
        ax = always_redraw(lambda: view.axes(3.2))
        path = s["dantzig"]["path"]
        vals = [sum(c * x for c, x in zip(d["c"], p)) for p in path]
        here = ValueTracker(0.0)

        def walker():
            t = here.get_value()
            k = min(int(t), len(path) - 2)
            f = t - k
            a, b = np.array(path[k]), np.array(path[k + 1])
            return Dot(view.p(*(a + (b - a) * f)), radius=0.11, color=HEAD)
        w = always_redraw(walker)
        trail = always_redraw(lambda: VGroup(*[Line(view.p(path[i]), view.p(path[i + 1]), color=HEAD, stroke_width=4)
                                               for i in range(min(int(here.get_value()), len(path) - 1))]))
        side = VGroup(
            label(r"start at a vertex: \ the origin, \ make nothing", font_size=22, color=WHITE),
            label(r"at each vertex, \ look along its edges: \\ is any of them uphill?", font_size=22, color=LAM),
            label(rf"move along it to the next vertex: \\ profit {vals[0]:.0f} $\to$ {vals[1]:.1f} $\to$ {vals[2]:.0f}",
                  font_size=22, color=HEAD),
            label(r"no uphill edge left: \ \textbf{optimal}, \\ because the region is convex", font_size=22, color=YES),
            label(rf"{s['dantzig']['pivots']} pivots, \ each a little Gaussian elimination", font_size=21, color=GREY_A),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.32).to_edge(RIGHT, buff=0.4)
        if side.width > 6.0:
            side.width = 6.0
            side.to_edge(RIGHT, buff=0.4)
        with self.voiceover(
            "Dantzig's simplex method walks from corner to corner. <bookmark mark='a'/> Start at a vertex; the "
            "origin, making nothing at all, is one. <bookmark mark='b'/> From the current vertex, look along the edges "
            "that leave it. Is any of them uphill, increasing the profit? <bookmark mark='c'/> If so, move along it "
            "until you hit the next vertex. Here the walk goes from zero profit to twelve and a half, making only "
            "the first product, and then to thirteen. <bookmark mark='d'/> When no edge goes uphill, you are done. "
            "That is the subtle part: a local check proves a global optimum, because in a convex region a vertex "
            "with no improving edge cannot be beaten anywhere. <bookmark mark='e'/> Here it took two moves."
        ) as vo:
            self.play(FadeIn(head))
            self.add(ax, poly, trail, w)
            vo.wait_until("a")
            self.play(FadeIn(side[0]))
            vo.wait_until("b")
            self.play(FadeIn(side[1]), view.th.animate.set_value(-0.45), run_time=2.0)
            vo.wait_until("c")
            self.play(FadeIn(side[2]))
            self.play(here.animate.set_value(1.0), run_time=2.0)
            self.play(here.animate.set_value(1.999), run_time=2.0)
            vo.wait_until("d")
            self.play(FadeIn(side[3]), Flash(view.p(path[-1]), color=YES))
            vo.wait_until("e")
            self.play(FadeIn(side[4]), view.th.animate.set_value(-0.95), run_time=2.5)
        for m in (poly, ax, w, trail):
            m.clear_updaters()
        self.wait(0.3)
        self.clear_scene()

    def tableau(self):
        s = load("simplex")
        tabs = s["tableaux"]
        head = label(r"The algebra: \ pivoting a tableau", font_size=34).to_edge(UP, buff=0.3)

        def table(t):
            hdr = [r"basis"] + [f"${v}$" for v in VARS] + [r"rhs"]
            rows = []
            for i, row in enumerate(t["T"]):
                rows.append([f"${VARS[t['basis'][i]]}$"] + [f"${frac_tex(v)}$" for v in row])
            rows.append([r"$z$"] + [f"${frac_tex(v)}$" for v in t["z"]])
            cols = []
            for i in range(len(rows)):
                cc = [YES] + [WHITE] * 6 + [HEAD]
                cols.append(cc)
            g = grid_table(hdr, rows, widths=[1.2] + [0.95] * 6 + [1.1], row_h=0.5, font_size=22, mono_cols=(),
                           colors=cols)
            return g
        tbs = [table(t).next_to(head, DOWN, buff=0.45).set_x(0) for t in tabs]
        notes = VGroup(
            label(r"slack variables turn $\le$ into $=$; \ the slacks form the first basis \ (the origin)",
                  font_size=21, color=WHITE),
            label(r"entering: \ a negative entry in the bottom row \ (an uphill edge; \ Dantzig picks the most "
                  r"negative)", font_size=21, color=LAM),
            label(r"leaving: \ the \textbf{ratio test}, \ the first constraint to become tight along that edge",
                  font_size=21, color=HEAD),
            label(r"a pivot is Gaussian elimination on one column: \ $O(mn)$ arithmetic", font_size=21, color=GREY_A),
            label(r"bottom row all $\ge 0$: \ optimal, \ $z = 13$; \ the slack columns hold the dual \ (chapter 3)",
                  font_size=21, color=YES),
        ).arrange(DOWN, buff=0.18).to_edge(DOWN, buff=0.3)

        def mark(i):
            t = tabs[i]
            if t["enter"] is None:
                return VGroup()
            tb = tbs[i]
            col = VGroup(*[tb.cells[r][1 + t["enter"]] for r in range(len(tb.cells))])
            row = VGroup(*tb.cells[1 + t["leave_row"]])
            return VGroup(SurroundingRectangle(col, color=LAM, buff=0.05),
                          SurroundingRectangle(row, color=HEAD, buff=0.05))
        with self.voiceover(
            "In algebra, the walk is a sequence of pivots. <bookmark mark='a'/> Add a slack variable to each "
            "inequality, the unused amount of each resource, and the constraints become equations. The slacks "
            "themselves form the first basis: the origin, where all resources are unused. <bookmark mark='b'/> "
            "The bottom row holds the objective. A negative entry means increasing that variable raises the profit; "
            "Dantzig's rule picks the most negative, here the first product. <bookmark mark='c'/> How far can it "
            "rise? The ratio test divides each right-hand side by the column's entry and takes the smallest: the "
            "first resource runs out first, at two and a half. <bookmark mark='d'/> The pivot is one step of "
            "Gaussian elimination, making that column a unit vector. <bookmark mark='e'/> One more pivot brings in "
            "the third product, and now the bottom row has no negative entries. The profit is thirteen, and the "
            "numbers under the slack columns, one, zero and one, are the prices of the resources, which the next "
            "chapter shows are a proof."
        ) as vo:
            self.play(FadeIn(head), FadeIn(tbs[0]))
            vo.wait_until("a")
            self.play(FadeIn(notes[0]))
            vo.wait_until("b")
            m0 = mark(0)
            self.play(FadeIn(notes[1]), Create(m0[0]))
            vo.wait_until("c")
            self.play(FadeIn(notes[2]), Create(m0[1]))
            vo.wait_until("d")
            self.play(FadeIn(notes[3]), FadeOut(m0), ReplacementTransform(tbs[0], tbs[1]))
            m1 = mark(1)
            self.play(Create(m1))
            vo.wait_until("e")
            self.play(FadeOut(m1), ReplacementTransform(tbs[1], tbs[2]))
            self.play(FadeIn(notes[4]), Indicate(VGroup(*tbs[2].cells[-1][4:7]), color=YES))
        self.wait(0.3)
        self.clear_scene()

    def rules(self):
        s = load("simplex")
        head = label(r"Choosing the edge", font_size=34).to_edge(UP, buff=0.35)
        lines = VGroup(
            label(r"Dantzig's rule: \ the steepest coefficient", font_size=22, color=WHITE),
            label(r"degenerate vertices \ (more than $n$ tight constraints) \ allow pivots that go nowhere, \ and "
                  r"\textbf{cycling} forever", font_size=22, color=NO),
            label(rf"Bland's rule \ (1977): \ always the smallest index; \ provably never cycles \ "
                  rf"({s['bland']['pivots']} pivots here too)", font_size=22, color=YES),
            label(r"real solvers: \ steepest edge, \ the revised simplex with LU factorizations, \ the dual simplex",
                  font_size=22, color=LAM),
            label(r"one of the ``top ten algorithms of the 20th century'' \ (Dongarra and Sullivan, 2000)",
                  font_size=21, color=GREY_A),
        ).arrange(DOWN, buff=0.34).next_to(head, DOWN, buff=0.55)
        with self.voiceover(
            "Which edge should the walk take? <bookmark mark='a'/> Dantzig's rule takes the steepest coefficient. "
            "<bookmark mark='b'/> At degenerate vertices, where more constraints are tight than the dimension needs, "
            "a pivot can change the basis without moving, and with an unlucky rule the method can cycle through the "
            "same bases forever. <bookmark mark='c'/> Robert Bland's rule, from 1977, always picks the smallest "
            "eligible index, and provably never cycles. <bookmark mark='d'/> Production solvers use smarter rules, "
            "like steepest edge, and keep the tableau implicit, as an LU factorization of the basis, updated after "
            "each pivot. <bookmark mark='e'/> The simplex method was named one of the ten most important algorithms of "
            "the twentieth century. Whether some pivot rule always finishes in polynomially many steps is still "
            "unknown, and chapter four shows why that question is subtle."
        ) as vo:
            self.play(FadeIn(head))
            for mk, ln in zip("abcde", lines):
                vo.wait_until(mk)
                self.play(FadeIn(ln, shift=UP * 0.1))
        self.wait(0.3)
        self.clear_scene()

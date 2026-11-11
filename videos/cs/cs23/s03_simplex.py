from __future__ import annotations

from explainer.cs import *  # noqa: F403
from explainer.cs.algo import optim as O
from fractions import Fraction
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
        self.budget()
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
            label('nonnegative reduced costs certify optimality; \\\\ feasible incumbent alone is insufficient', font_size=22, color=YES),
            label(rf"{s['dantzig']['pivots']} pivots, \ each a little Gaussian elimination", font_size=21, color=GREY_A),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.32).to_edge(RIGHT, buff=0.4)
        if side.width > 6.0:
            side.width = 6.0
            side.to_edge(RIGHT, buff=0.4)
        with self.voiceover(
            (
            "Dantzig's simplex method walks from vertex to vertex. <bookmark mark='a'/> Our implementation "
            'begins at the origin, a feasible slack basis because every right-hand side is nonnegative. Finding '
            'an initial feasible basis for arbitrary data needs a separate Phase One, which this teaching code '
            "does not implement. <bookmark mark='b'/> Inspect the reduced costs for a feasible improving pivot. "
            "<bookmark mark='c'/> Move until a constraint blocks further travel. Here the objective goes from "
            "zero to twelve and a half, then thirteen. <bookmark mark='d'/> Nonnegative reduced costs certify "
            'global optimality for this maximization tableau. Degenerate bases can require zero-length pivots; '
            "merely seeing no immediate positive movement is insufficient. <bookmark mark='e'/> This example "
            'reaches an exact primal and dual certificate after two pivots.'
        )
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
            label(r"one pivot updates the full tableau: \ $O(m(n+m))$ arithmetic, including slacks", font_size=21, color=GREY_A),
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
            label('Dantzig: \\ largest improving reduced-cost coefficient', font_size=22, color=WHITE),
            label(r"degenerate vertices \ (more than $n$ tight constraints) \ allow pivots that go nowhere, \ and "
                  r"\textbf{cycling} forever", font_size=22, color=NO),
            label(rf"Bland's rule \ (1977): \ always the smallest index; \ provably never cycles \ "
                  rf"({s['bland']['pivots']} pivots here too)", font_size=22, color=YES),
            label('full teaching tableau: \\ $O(m(n+m))$ arithmetic per pivot; \\\\ revised simplex maintains basis factors',
                  font_size=22, color=LAM),
            label(r"one of the ``top ten algorithms of the 20th century'' \ (Dongarra and Sullivan, 2000)",
                  font_size=21, color=GREY_A),
        ).arrange(DOWN, buff=0.34).next_to(head, DOWN, buff=0.55)
        with self.voiceover(
            (
            "Which pivot should the walk take? <bookmark mark='a'/> Dantzig chooses the largest improving "
            "reduced-cost coefficient; this is not a normalized geometric slope. <bookmark mark='b'/> At a "
            'degenerate vertex a pivot can change the basis without moving, and unsuitable choices can cycle. '
            "<bookmark mark='c'/> Bland's smallest eligible index rule prevents cycling in exact arithmetic. "
            "<bookmark mark='d'/> Our full tableau updates all m times n plus m entries at each pivot. "
            'Production revised simplex maintains basis factorizations. Its normalized steepest-edge rules '
            'differ from our selector called greatest improvement, which tests the whole gain of each candidate '
            "pivot. <bookmark mark='e'/> A small number of pivots in one example gives no polynomial worst-case "
            'guarantee; the next chapters examine that distinction.'
        )
        ) as vo:
            self.play(FadeIn(head))
            for mk, ln in zip("abcde", lines):
                vo.wait_until(mk)
                self.play(FadeIn(ln, shift=UP * 0.1))
        self.wait(0.3)
        self.clear_scene()


    def budget(self):
        stopped = O.simplex([1], [[1]], [1], exact=True, max_pivots=0)
        solved = O.simplex([1], [[1]], [1], exact=True, max_pivots=1)
        assert stopped['status'] == 'iteration_limit' and stopped['x_exact'] == [0]
        assert stopped['value_exact'] == 0 and stopped['duals_exact'] == [0]
        assert solved['status'] == 'optimal' and solved['value_exact'] == 1
        head = label('A feasible incumbent still needs an optimality certificate',font_size=31).to_edge(UP,buff=.35)
        line = NumberLine(x_range=[0,1,.25],length=4,include_numbers=True,font_size=25).move_to(LEFT*3.7+DOWN*.3)
        start = Dot(line.n2p(0),radius=.11,color=NO)
        end = Dot(line.n2p(1),radius=.11,color=YES)
        names = VGroup(label('feasible: x = 0',font_size=22,color=NO).next_to(start,UP,buff=.35),
                       label('optimal: x = 1',font_size=22,color=YES).next_to(end,DOWN,buff=.35))
        rows = VGroup(
            MathTex(r'\max x\quad\hbox{subject to }0\le x\le1',font_size=32,color=WHITE),
            label('zero pivot budget: iteration limit; incumbent value 0',font_size=23,color=NO),
            MathTex(r'y=0:\quad y\not\ge1',font_size=36,color=NO),
            label('the returned dual does not cover the objective',font_size=22,color=NO),
            MathTex(r'x=1,\ y=1:\quad c^Tx=b^Ty=1',font_size=33,color=YES),
            label('one pivot: feasible pair and equal objectives certify 1',font_size=22,color=YES),
        ).arrange(DOWN,buff=.33).move_to(RIGHT*2.5)
        if rows.width>7.3:rows.width=7.3;rows.set_x(2.5)
        with self.voiceover("Here is an executed stopping-status example. Maximize x between zero and one. <bookmark mark='a'/> With a zero pivot budget our code returns the feasible origin and reports iteration limit, not optimal. The incumbent earns zero, while the true optimum is one. <bookmark mark='b'/> Its zero dual multiplier does not cover the objective coefficient one. A feasible primal answer alone cannot certify optimality. <bookmark mark='c'/> Allow one pivot. The returned primal x and dual y both equal one; both are feasible, and their equal objectives certify the optimum. The budget status and the certificate now agree.") as vo:
            self.play(FadeIn(head),Create(line),FadeIn(start),FadeIn(names[0]),FadeIn(rows[0]))
            vo.wait_until('a');self.play(FadeIn(rows[1]))
            vo.wait_until('b');self.play(FadeIn(rows[2]),FadeIn(rows[3]))
            vo.wait_until('c');self.play(FadeIn(end),FadeIn(names[1]),FadeIn(rows[4]),FadeIn(rows[5]))
        self.wait(.3);self.clear_scene()

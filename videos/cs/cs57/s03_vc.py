from __future__ import annotations

import math

from explainer.cs import *  # noqa: F403
from videos.cs.cs57.common import BG, DATA, HEAD, KERN, LAM, NO, PART, YES, grid_table, load


def lab_color(v):
    return YES if v > 0 else NO


def panel(points, labels, w, h, lo=(-0.35, -0.3), hi=(2.35, 2.1), seg=None):
    """A small frame with labelled points (data coordinates) and, if given, a separating segment."""
    frame = RoundedRectangle(width=w, height=h, corner_radius=0.1, stroke_color=GREY_D, stroke_width=1.2,
                             fill_color=BG, fill_opacity=1)
    sx = (w - 0.2) / (hi[0] - lo[0])
    sy = (h - 0.2) / (hi[1] - lo[1])
    s = min(sx, sy)
    cx, cy = (lo[0] + hi[0]) / 2, (lo[1] + hi[1]) / 2

    def at(x, y):
        return frame.get_center() + np.array([(x - cx) * s, (y - cy) * s, 0])
    g = VGroup(frame)
    if seg is not None:
        g.add(Line(at(*seg[0]), at(*seg[1]), color=HEAD, stroke_width=3))
    g.add(VGroup(*[Dot(at(*p), radius=0.09, color=lab_color(v)) for p, v in zip(points, labels)]))
    g.at = at
    return g


def separator(P, labels):
    """A segment that separates the odd point of three from the other two (or lies beside all three)."""
    P = np.array(P)
    lab = np.array(labels)
    if abs(lab.sum()) == 3:
        x = P[:, 0].min() - 0.25
        return (x, P[:, 1].min() - 0.15), (x, P[:, 1].max() + 0.15)
    odd = int(np.flatnonzero(lab == (1 if lab.sum() < 0 else -1))[0])
    q, r = [P[i] for i in range(3) if i != odd]
    a, b = (P[odd] + q) / 2, (P[odd] + r) / 2
    u = b - a
    return tuple(a - 0.45 * u), tuple(b + 0.45 * u)


def stacked(rows, whys, buff=0.2):
    pairs = VGroup()
    for r, w in zip(rows, whys):
        w.next_to(r, DOWN, buff=0.08, aligned_edge=LEFT)
        pairs.add(VGroup(r, w))
    pairs.arrange(DOWN, aligned_edge=LEFT, buff=buff)
    return pairs


class Vc(VoiceoverScene):
    def construct(self):
        self.card()
        self.shatter()
        self.four()
        self.growth()
        self.sauer()
        self.bound()
        self.fundamental()

    def card(self):
        card = chapter_card(2, r"VC dimension", r"How do you count an infinite class?", lit=(1971, 1989),
                            extra=((1971, r"Vapnik and Chervonenkis: \ uniform convergence"),
                                   (1989, r"Blumer et al.: \ learnability and the VC dimension")), part=PART)
        with self.voiceover("Chapter two. The VC dimension."):
            self.play(FadeIn(card[0], shift=UP * 0.2), FadeIn(card[1]), FadeIn(card[2]))
        self.play(FadeOut(card))

    def shatter(self):
        s = load("shatter")["three"]
        P = s["points"]
        head = label(r"Shattering: \ three points, \ eight labellings", font_size=36).to_edge(UP, buff=0.3)
        panels = VGroup(*[panel(P, r["labels"], 2.95, 2.1, seg=separator(P, r["labels"])) for r in s["labelings"]])
        panels.arrange_in_grid(rows=2, cols=4, buff=(0.2, 0.2)).next_to(head, DOWN, buff=0.35)
        defs = VGroup(
            wrapped_label(r"a class $\mathcal H$ \textbf{shatters} a set of $m$ points if it realizes all $2^m$ of "
                          r"its labellings", 12.4, font_size=21, color=WHITE),
            wrapped_label(r"the \textbf{VC dimension} of $\mathcal H$ is the size of the largest set it shatters "
                          r"\ (Vapnik and Chervonenkis, \ 1971)", 12.4, font_size=21, color=HEAD),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.15).next_to(panels, DOWN, buff=0.3)
        src = note(rf"each labelling checked by a linear program: \ {s['separable_count']} of "
                   rf"{len(s['labelings'])} separable", font_size=16).to_edge(DOWN, buff=0.2)
        with self.voiceover(
            "In 1971 Vladimir Vapnik and Alexey Chervonenkis measured an infinite class not by its size but"
            " by how many ways it can label points. <bookmark mark='a'/> Take three points in the plane, "
            "not on a line, and colour each green or red: there are eight ways. <bookmark mark='b'/> For "
            "every one of them a line puts the greens on one side and the reds on the other; our instrument"
            " checked each with a linear program. <bookmark mark='c'/> A class that realizes every "
            "labelling of a set is said to shatter it, <bookmark mark='d'/> and the VC dimension is the "
            "size of the largest set the class shatters. For half-planes it is at least three."
        ) as vo:
            self.play(FadeIn(head))
            vo.wait_until("a")
            self.play(FadeIn(panels[0][0]), FadeIn(panels[0][-1]))
            vo.wait_until("b")
            self.play(Create(panels[0][1]))
            self.play(LaggedStart(*[FadeIn(p) for p in panels[1:]], lag_ratio=0.25), run_time=3.0)
            self.play(FadeIn(src))
            vo.wait_until("c")
            self.play(FadeIn(defs[0]))
            vo.wait_until("d")
            self.play(FadeIn(defs[1]))
        self.wait(0.4)
        self.clear_scene()

    def four(self):
        sh = load("shatter")
        sq, tr = sh["square"], sh["triangle with a point inside"]
        head = label(r"No four points are shattered", font_size=36).to_edge(UP, buff=0.3)
        bad_sq = next(r["labels"] for r in sq["labelings"] if not r["separable"])
        bad_tr = next(r["labels"] for r in tr["labelings"] if not r["separable"])
        A = panel(sq["points"], bad_sq, 3.3, 3.0, lo=(-0.3, -0.3), hi=(2.3, 2.3))
        B = panel(tr["points"], bad_tr, 3.3, 3.0, lo=(-0.3, -0.3), hi=(3.3, 2.8))
        VGroup(A, B).arrange(RIGHT, buff=0.35).next_to(head, DOWN, buff=0.5).to_edge(LEFT, buff=0.4)
        # the two diagonals of the square, each joining points of one colour
        pa = sq["points"]
        same = [(i, j) for i in range(4) for j in range(i + 1, 4) if bad_sq[i] == bad_sq[j]]
        diags = VGroup(*[Line(A.at(*pa[i]), A.at(*pa[j]), color=lab_color(bad_sq[i]), stroke_width=3)
                         for i, j in same])
        cross = Dot(A.at(1.0, 1.0), radius=0.07, color=HEAD)
        pb = tr["points"]
        outer = [i for i in range(4) if bad_tr[i] != bad_tr[3]] if bad_tr[3] != bad_tr[0] else [0, 1, 2]
        tri = Polygon(*[B.at(*pb[i]) for i in outer], stroke_color=lab_color(bad_tr[outer[0]]), stroke_width=2.5,
                      fill_color=lab_color(bad_tr[outer[0]]), fill_opacity=0.18)
        ca = label(rf"convex position: \ {sq['separable_count']} of 16 separable", font_size=17,
                   color=GREY_A).next_to(A, DOWN, buff=0.12)
        cb = label(rf"one point inside: \ {tr['separable_count']} of 16 separable", font_size=17,
                   color=GREY_A).next_to(B, DOWN, buff=0.12)
        W = 5.5
        side = VGroup(
            wrapped_label(r"a half-plane is convex: \ holding both green points, \ it holds the segment between "
                          r"them; \ the other side, \ also convex, \ holds the red segment; \ the segments cross, \ "
                          r"so no line separates them", W, font_size=19, color=WHITE),
            wrapped_label(r"any four points fall into one of these two cases: \ \textbf{Radon} \ (1921): \ any "
                          r"$d + 2$ points in $\mathbb R^d$ split into two groups whose convex hulls meet", W,
                          font_size=19, color=LAM),
            wrapped_label(r"so half-spaces in $\mathbb R^d$ have VC dimension exactly $d + 1$: \ \textbf{3} for "
                          r"half-planes; \ axis-aligned rectangles have \textbf{4}", W, font_size=19, color=HEAD),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.35).next_to(B, RIGHT, buff=0.4)
        foot = wrapped_label(r"a dimension is an \textit{upper} bound only when \textit{no} set of size $d + 1$ is "
                             r"shattered; \ a lower bound needs just \textit{one} shattered set of size $d$", 12.4,
                             font_size=19, color=GREY_A).to_edge(DOWN, buff=0.35)
        with self.voiceover(
            "Can half-planes shatter four points? <bookmark mark='a'/> At the corners of a square, fourteen"
            " of the sixteen labellings are separable, but not the two that colour opposite corners alike. "
            "<bookmark mark='b'/> A half-plane holding both green points holds the segment between them; "
            "the other side holds the red segment; the diagonals cross, so no line works. "
            "<bookmark mark='c'/> If one point lies inside the triangle of the others, colour it apart, and"
            " the same argument applies. <bookmark mark='d'/> Every four points fall into one of these "
            "cases: Radon's theorem of 1921, which in d dimensions splits any d plus two points. "
            "<bookmark mark='e'/> So half-planes have VC dimension three, half-spaces in d dimensions d "
            "plus one, and rectangles four. <bookmark mark='f'/> A lower bound needs one shattered set; an "
            "upper bound must defeat every set."
        ) as vo:
            self.play(FadeIn(head))
            vo.wait_until("a")
            self.play(FadeIn(A), FadeIn(ca))
            vo.wait_until("b")
            self.play(Create(diags), FadeIn(side[0]))
            self.play(FadeIn(cross, scale=2))
            vo.wait_until("c")
            self.add(B[0])
            self.play(FadeIn(B), FadeIn(cb))
            self.play(FadeIn(tri))
            self.bring_to_front(B[-1])
            vo.wait_until("d")
            self.play(FadeIn(side[1]))
            vo.wait_until("e")
            self.play(FadeIn(side[2]))
            vo.wait_until("f")
            self.play(FadeIn(foot))
        self.wait(0.4)
        self.clear_scene()

    def growth(self):
        rows = [r for r in load("growth")["rows"] if r["m"] <= 10]     # larger m: the formula, not a count
        head = label(r"The growth function", font_size=36).to_edge(UP, buff=0.3)
        ax = CornerAxes(x_range=[0, 11, 1], y_range=[0, 10.5, 1], x_length=6.6, y_length=4.7, tips=False,
                        axis_config={"color": GREY_D, "include_numbers": False, "include_ticks": False})
        ax.next_to(head, DOWN, buff=0.45).to_edge(LEFT, buff=1.2)
        xt = VGroup(*[label(f"{v}", font_size=16, color=GREY_B).next_to(ax.c2p(v, 0), DOWN, buff=0.1)
                      for v in (1, 4, 7, 10)])
        yt = VGroup(*[label(f"{2 ** v:,}", font_size=16, color=GREY_B).next_to(ax.c2p(0, v), LEFT, buff=0.1)
                      for v in (0, 4, 8, 10)])
        xl = label(r"points $m$", font_size=17, color=GREY_A).next_to(ax, DOWN, buff=0.45)
        yl = label(r"labellings \ (log scale)", font_size=17, color=GREY_A).next_to(ax, UP, buff=0.08).align_to(
            ax, LEFT)

        def curve(key, color):
            pts = [ax.c2p(r["m"], math.log2(r[key])) for r in rows]
            return VGroup(VMobject(color=color, stroke_width=3).set_points_as_corners(pts),
                          VGroup(*[Dot(p, radius=0.05, color=color) for p in pts]))
        c_all, c_s, c_r = curve("all", GREY_B), curve("sauer", HEAD), curve("realized", YES)
        last = rows[-1]
        W = 5.0
        side = VGroup(
            MathTex(r"\Pi_{\mathcal H}(m) = \max_{|S| = m} \big|\{\, h|_S : h \in \mathcal H \,\}\big|", font_size=30),
            wrapped_label(rf"all labellings, \ $2^m$: \ {last['all']:,} at $m = {last['m']}$", W, font_size=19,
                          color=GREY_B),
            wrapped_label(rf"half-planes, \ counted: \ {last['realized']} \ $= m^2 - m + 2$, \ the exact count for "
                          r"points in general position", W, font_size=19, color=YES),
            wrapped_label(rf"Sauer--Shelah's bound with $d = 3$, \ $\sum_{{i \le 3}} \binom{{m}}{{i}}$: \ "
                          rf"{last['sauer']}", W, font_size=19, color=HEAD),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.35).next_to(ax, RIGHT, buff=0.6).shift(UP * 0.2)
        src = note(r"random points; \ each labelling checked by a linear program; \ best of three point sets",
                   font_size=16).to_edge(DOWN, buff=0.3)
        with self.voiceover(
            "Behind the VC dimension is a function. <bookmark mark='a'/> The growth function counts, for "
            "each m, the most labellings the class produces on any m points. <bookmark mark='b'/> A class "
            "that shattered everything would follow two to the m, the grey line: a thousand and twenty-four"
            " at ten points. <bookmark mark='c'/> Half-planes, counted labelling by labelling, follow it up"
            " to three points, the VC dimension, and then fall away, to ninety-two, which is m squared "
            "minus m plus two. <bookmark mark='d'/> The yellow curve is the bound we are about to prove "
            "from the VC dimension alone. Past the VC dimension, growth is only polynomial."
        ) as vo:
            self.play(FadeIn(head), Create(ax), FadeIn(xt), FadeIn(yt), FadeIn(xl), FadeIn(yl), FadeIn(src))
            vo.wait_until("a")
            self.play(Write(side[0]))
            vo.wait_until("b")
            self.play(Create(c_all[0]), FadeIn(c_all[1]), FadeIn(side[1]), run_time=1.5)
            vo.wait_until("c")
            self.play(Create(c_r[0]), FadeIn(c_r[1]), FadeIn(side[2]), run_time=1.5)
            vo.wait_until("d")
            self.play(Create(c_s[0]), FadeIn(c_s[1]), FadeIn(side[3]), run_time=1.5)
        self.wait(0.4)
        self.clear_scene()

    def sauer(self):
        sq = load("shatter")["square"]
        labs = [tuple(r["labels"]) for r in sq["labelings"] if r["separable"]]
        heads = sorted({lab[:3] for lab in labs}, reverse=True)
        tails = {h: [lab[3] for lab in labs if lab[:3] == h] for h in heads}
        n1 = len(heads)
        n2 = sum(1 for h in heads if len(tails[h]) == 2)
        head = label(r"Sauer--Shelah: \ polynomial, \ not exponential", font_size=36).to_edge(UP, buff=0.3)
        # the table: one row per pattern on x1..x3, then the labels x4 takes with it
        rh, dx = 0.4, 0.34
        table = VGroup()
        boxes = VGroup()
        for k, h in enumerate(heads):
            y = -k * rh
            row = VGroup(*[Dot([i * dx, y, 0], radius=0.08, color=lab_color(v)) for i, v in enumerate(h)])
            t = VGroup(*[Dot([3 * dx + 0.45 + j * dx, y, 0], radius=0.08, color=lab_color(v))
                         for j, v in enumerate(sorted(tails[h], reverse=True))])
            table.add(VGroup(row, t))
            if len(tails[h]) == 2:
                boxes.add(SurroundingRectangle(t, color=LAM, buff=0.07, corner_radius=0.08, stroke_width=2))
        hdr = VGroup(label(r"$x_1\,x_2\,x_3$", font_size=17, color=GREY_A).move_to([dx, rh, 0]),
                     label(r"$x_4$", font_size=17, color=GREY_A).move_to([3 * dx + 0.45 + dx / 2, rh, 0]))
        vline = Line([3 * dx + 0.2, rh * 0.6, 0], [3 * dx + 0.2, -(n1 - 0.4) * rh, 0], color=GREY_D)
        tab = VGroup(hdr, vline, table, boxes)
        tab.next_to(head, DOWN, buff=0.5).to_edge(LEFT, buff=0.6)
        counts = VGroup(
            label(rf"$|\mathcal H_S| = {len(labs)}$", font_size=20, color=WHITE),
            label(rf"$|\mathcal H_1| = {n1}$ \ (rows)", font_size=20, color=DATA),
            label(rf"$|\mathcal H_2| = {n2}$ \ (boxed)", font_size=20, color=LAM),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.15).next_to(tab, DOWN, buff=0.3).align_to(tab, LEFT)
        src = note(r"half-planes on the square's corners", font_size=16).next_to(counts, DOWN, buff=0.15).align_to(
            tab, LEFT)
        stmt = MathTex(r"\mathrm{VC}(\mathcal H) = d \ \Longrightarrow\ \Pi_{\mathcal H}(m) \le \Phi_d(m) = "
                       r"\sum_{i=0}^{d}\binom{m}{i}", font_size=32, color=HEAD)
        fs = 28
        rows = [
            MathTex(r"|\mathcal H_S|", r"=", r"|\mathcal H_1|", r"+", r"|\mathcal H_2|", font_size=fs),
            MathTex(r"|\mathcal H_S|", r"\le", r"\Phi_d(m-1)", r"+", r"\Phi_{d-1}(m-1)", font_size=fs),
            MathTex(r"|\mathcal H_S|", r"\le", r"\sum_{i \le d}", r"\Big[\binom{m-1}{i} + \binom{m-1}{i-1}\Big]",
                    font_size=fs),
            MathTex(r"|\mathcal H_S|", r"\le", r"\sum_{i \le d}", r"\binom{m}{i}", r"\le",
                    r"\Big(\frac{em}{d}\Big)^d", font_size=fs),
        ]
        rows[0][2].set_color(DATA)
        rows[0][4].set_color(LAM)
        rows[3][5].set_color(YES)
        whys = [
            label(rf"each labelling is a row, \ or the second entry of a boxed row: \ ${len(labs)} = {n1} + {n2}$",
                  font_size=17, color=GREY_B),
            label(r"induction: \ $\mathcal H_1$ shatters at most $d$ points; \ if $\mathcal H_2$ shattered $T$, "
                  r"$\mathcal H$ would shatter $T \cup \{x_m\}$, \ so at most $d - 1$", font_size=17, color=GREY_B),
            label(r"write both as sums, \ shifting the second index", font_size=17, color=GREY_B),
            label(r"Pascal's rule; \ and for $m \ge d$, \ a polynomial of degree $d$", font_size=17, color=GREY_B),
        ]
        col = stacked(rows, whys, buff=0.26)
        right = VGroup(stmt, col).arrange(DOWN, aligned_edge=LEFT, buff=0.45).next_to(tab, RIGHT, buff=1.0)
        right.align_to(tab, UP)
        if right.get_right()[0] > 6.85:
            right.shift(LEFT * (right.get_right()[0] - 6.85))
        with self.voiceover(
            "Norbert Sauer and Saharon Shelah proved independently, in 1972, why. <bookmark mark='a'/> If "
            "the VC dimension is d, the growth function is at most the number of subsets of size at most d."
            " <bookmark mark='b'/> Here are the fourteen labellings of the square's corners, grouped by the"
            " first three points. The rows form H one; the boxed rows, which occur with both labels of the "
            "last point, form H two. Fourteen is eight plus six. <bookmark mark='c'/> Induct. H one "
            "shatters at most d points; H two at most d minus one, or the class would shatter that set plus"
            " the last point. <bookmark mark='d'/> Write both bounds as sums, <bookmark mark='e'/> and "
            "Pascal's rule adds them into the sum for m: for m at least d, at most e m over d, to the d. A "
            "polynomial."
        ) as vo:
            self.play(FadeIn(head))
            vo.wait_until("a")
            self.play(Write(stmt))
            vo.wait_until("b")
            self.play(FadeIn(hdr), Create(vline), LaggedStart(*[FadeIn(r) for r in table], lag_ratio=0.15),
                      run_time=2)
            self.play(Create(boxes), FadeIn(counts), FadeIn(src))
            self.play(Write(col[0][0]), FadeIn(col[0][1]))
            vo.wait_until("c")
            self.play(TransformMatchingTex(rows[0].copy(), rows[1]), FadeIn(col[1][1]))
            vo.wait_until("d")
            self.play(TransformMatchingTex(rows[1].copy(), rows[2]), FadeIn(col[2][1]))
            vo.wait_until("e")
            self.play(TransformMatchingTex(rows[2].copy(), rows[3]), FadeIn(col[3][1]))
        self.wait(0.4)
        self.clear_scene()

    def bound(self):
        r = load("rect")
        rr, delta = r["rows"], r["delta"]
        d = 4                                              # axis-aligned rectangles
        head = label(r"From the growth function to a bound", font_size=36).to_edge(UP, buff=0.3)
        defs = VGroup(
            label(r"$B$: \ some $h$ consistent with $S$ has $L_D(h) > \epsilon$", font_size=18, color=GREY_A),
            label(r"$B'$: \ some $h$ consistent with $S$ errs on $\ge \epsilon m/2$ points of a \textit{ghost} "
                  r"sample $S'$", font_size=18, color=GREY_A),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.1)
        fs = 26
        rows = [
            MathTex(r"\Pr[B]", r"\le", r"2\,\Pr[B']", font_size=fs),
            MathTex(r"\Pr[B]", r"\le", r"2\,", r"\Pi_{\mathcal H}(2m)", r"\,2^{-\epsilon m/2}", font_size=fs),
            MathTex(r"\epsilon", r"\le", r"\frac{2}{m}\Big(", r"\log_2 \Pi_{\mathcal H}(2m)",
                    r"+ \log_2\frac{2}{\delta}\Big)", font_size=fs),
            MathTex(r"\epsilon", r"\le", r"\frac{2}{m}\Big(", r"d\log_2\frac{2em}{d}", r"+ \log_2\frac{2}{\delta}"
                    r"\Big)", font_size=fs),
        ]
        rows[1][3].set_color(YES)
        rows[2][3].set_color(YES)
        rows[3][3].set_color(HEAD)
        whys = [
            label(r"if $B$, \ $S'$ catches $\ge \epsilon m/2$ errors with probability $\ge \tfrac12$ \ "
                  r"(Chebyshev, \ $m \ge 8/\epsilon$)", font_size=17, color=GREY_B),
            label(r"on $S \cup S'$, \ $\mathcal H$ has at most $\Pi_{\mathcal H}(2m)$ behaviours; \ a random "
                  r"swap puts all $k$ errors in $S'$ w.p.\ $\le 2^{-k}$", font_size=17, color=GREY_B),
            label(r"set the right side to $\delta$, \ solve for $\epsilon$", font_size=17, color=GREY_B),
            label(r"Sauer--Shelah: \ $\Pi_{\mathcal H}(2m) \le (2em/d)^d$", font_size=17, color=HEAD),
        ]
        col = stacked(rows, whys, buff=0.24)
        left = VGroup(defs, col).arrange(DOWN, aligned_edge=LEFT, buff=0.35).next_to(head, DOWN, buff=0.35)
        left.to_edge(LEFT, buff=0.35)
        if left.width > 6.9:
            left.scale_to_fit_width(6.9).to_edge(LEFT, buff=0.35)
        # the plot: the same curves as Chapter 1, with the general VC bound for d = 4
        ax = CornerAxes(x_range=[1, 3.4, 1], y_range=[-3, 0, 1], x_length=5.0, y_length=3.9, tips=False,
                        axis_config={"color": GREY_D, "include_numbers": False, "include_ticks": False})
        ax.move_to([4.15, 0.55, 0])
        xt = VGroup(*[label(f"{v:,}", font_size=16, color=GREY_B).next_to(ax.c2p(math.log10(v), -3), DOWN, buff=0.1)
                      for v in (10, 100, 1000)])
        yt = VGroup(*[label(f"{v:g}", font_size=16, color=GREY_B).next_to(ax.c2p(1, math.log10(v)), LEFT, buff=0.1)
                      for v in (0.001, 0.01, 0.1, 1)])
        xl = label(r"examples $m$", font_size=17, color=GREY_A).next_to(ax, DOWN, buff=0.4)

        def vc(m):
            return min(1.0, 2 / m * (d * math.log2(2 * math.e * m / d) + math.log2(2 / delta)))

        def line(vals, color, dashed=False):
            pts = [ax.c2p(math.log10(q["m"]), max(-3, min(0, math.log10(v)))) for q, v in zip(rr, vals)]
            v = VMobject(color=color, stroke_width=3).set_points_as_corners(pts)
            return DashedVMobject(v, num_dashes=36) if dashed else v
        c_p = line([q["p95"] for q in rr], DATA)
        c_r = line([q["rect_bound"] for q in rr], KERN, dashed=True)
        c_v = line([vc(q["m"]) for q in rr], HEAD)
        legend = VGroup(
            label(r"measured, \ 95th percentile", font_size=17, color=DATA),
            label(r"rectangle bound \ (Chapter 1)", font_size=17, color=KERN),
            label(r"VC bound, \ $d = 4$", font_size=17, color=HEAD),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.1).next_to(xl, DOWN, buff=0.2).align_to(ax, LEFT)
        big = rr[-1]
        ratio = vc(big["m"]) / big["p95"]
        note_ = wrapped_label(rf"at $m = {big['m']:,}$: \ VC bound {vc(big['m']):.3f}, \ measured {big['p95']:.4f}: "
                              rf"\ {ratio:.0f}$\times$ loose, \ knowing only $d$", 5.6, font_size=18,
                              color=WHITE).next_to(legend, DOWN, buff=0.2).align_to(ax, LEFT)
        with self.voiceover(
            "The growth function can now replace the class size, through a ghost sample. "
            "<bookmark mark='a'/> Draw m more points. If a consistent hypothesis has true error above "
            "epsilon, with probability at least a half it errs on epsilon m over two ghost points. So the "
            "bad event costs at most twice an event about two m points. <bookmark mark='b'/> On those, the "
            "class has at most the growth function of two m behaviours, and a random swap between the "
            "halves hides all k mistakes of one in the ghost half with probability at most two to the minus"
            " k. <bookmark mark='c'/> Set this to delta and solve, <bookmark mark='d'/> and Sauer and "
            "Shelah turn the growth function into d times a logarithm. <bookmark mark='e'/> For rectangles "
            "d is four: the bound is valid, but an order of magnitude above our measurement. It knows only "
            "the VC dimension."
        ) as vo:
            self.play(FadeIn(head), FadeIn(defs))
            vo.wait_until("a")
            self.play(Write(col[0][0]), FadeIn(col[0][1]))
            vo.wait_until("b")
            self.play(TransformMatchingTex(rows[0].copy(), rows[1]), FadeIn(col[1][1]))
            vo.wait_until("c")
            self.play(TransformMatchingTex(rows[1].copy(), rows[2]), FadeIn(col[2][1]))
            vo.wait_until("d")
            self.play(TransformMatchingTex(rows[2].copy(), rows[3]), FadeIn(col[3][1]))
            vo.wait_until("e")
            self.play(Create(ax), FadeIn(xt), FadeIn(yt), FadeIn(xl))
            self.play(Create(c_p), FadeIn(legend[0]))
            self.play(Create(c_r), FadeIn(legend[1]))
            self.play(Create(c_v), FadeIn(legend[2]), FadeIn(note_))
        self.wait(0.4)
        self.clear_scene()

    def fundamental(self):
        head = label(r"The fundamental theorem of PAC learning", font_size=36).to_edge(UP, buff=0.3)
        stmt = wrapped_label(r"for binary classification these are equivalent: \ $\mathcal H$ has \textbf{finite VC "
                             r"dimension}; \ uniform convergence holds; \ every ERM learner PAC-learns $\mathcal H$; "
                             r"\ $\mathcal H$ is agnostically PAC learnable", 12.4, font_size=21, color=WHITE)
        stmt.next_to(head, DOWN, buff=0.35)
        tab = grid_table([r"examples needed", r"realizable", r"agnostic"], [
            [r"enough", r"$O\!\left(\dfrac{d \log(1/\epsilon) + \log(1/\delta)}{\epsilon}\right)$",
             r"$O\!\left(\dfrac{d + \log(1/\delta)}{\epsilon^2}\right)$"],
            [r"necessary", r"$\Omega\!\left(\dfrac{d + \log(1/\delta)}{\epsilon}\right)$",
             r"$\Omega\!\left(\dfrac{d + \log(1/\delta)}{\epsilon^2}\right)$"],
        ], widths=[2.1, 3.5, 2.9], row_h=1.15, font_size=22, mono_cols=())
        tab.next_to(stmt, DOWN, buff=0.6).to_edge(LEFT, buff=0.45)
        tsrc = note(r"Shalev-Shwartz and Ben-David, \ Theorem 6.8; \ Blumer et al. \ (1989)", font_size=16).next_to(
            tab, DOWN, buff=0.25).align_to(tab, LEFT)
        # the lower bound: a shattered set of 2m points, half of them seen
        n = 12
        dots = VGroup(*[Dot(radius=0.12, color=GREY_B) for _ in range(n)]).arrange_in_grid(rows=2, cols=6,
                                                                                         buff=(0.42, 0.55))
        W = 4.3
        dl = wrapped_label(r"a shattered set of $2m$ points; \ the learner sees $m$", W, font_size=18,
                           color=GREY_A)
        labs = [1, -1, -1, 1, 1, -1, 1, 1, -1, 1, -1, -1]
        nfl = wrapped_label(r"every labelling of the unseen half is still possible, \ so some target makes the "
                            r"learner's error at least $1/8$ with probability at least $1/7$ \ (\textit{no free "
                            r"lunch}); \ infinite VC dimension: \ no $m$ is enough", W, font_size=19, color=NO)
        ill = note(r"illustrative", font_size=16)
        right = VGroup(dl, dots, ill, nfl).arrange(DOWN, aligned_edge=LEFT, buff=0.3)
        right.next_to(tab, RIGHT, buff=0.5).align_to(tab, UP)
        if right.get_right()[0] > 6.85:
            right.shift(LEFT * (right.get_right()[0] - 6.85))
        seen = VGroup(*[dots[i].copy().set_color(lab_color(labs[i])) for i in range(0, n, 2)])
        qs = VGroup(*[label(r"?", font_size=20, color=HEAD).next_to(dots[i], UP, buff=0.06) for i in range(1, n, 2)])
        with self.voiceover(
            "Together these give the fundamental theorem of PAC learning, made explicit by Blumer, "
            "Ehrenfeucht, Haussler and Warmuth in 1989. <bookmark mark='a'/> For binary classification, "
            "four things are equivalent: finite VC dimension, uniform convergence, learnability by any "
            "sample-error minimizer, and agnostic learnability. <bookmark mark='b'/> The examples needed "
            "are pinned down: about d over epsilon when a perfect hypothesis exists, d over epsilon squared"
            " when none does. <bookmark mark='c'/> The converse is the no free lunch argument: if the class"
            " shatters two m points, a learner that has seen m of them knows nothing about the rest. "
            "<bookmark mark='d'/> Some target forces error at least an eighth with probability at least a "
            "seventh. With infinite VC dimension, no amount of data is enough."
        ) as vo:
            self.play(FadeIn(head))
            vo.wait_until("a")
            self.play(FadeIn(stmt))
            vo.wait_until("b")
            self.play(FadeIn(tab), FadeIn(tsrc))
            vo.wait_until("c")
            self.play(FadeIn(dots), FadeIn(dl), FadeIn(ill))
            self.play(LaggedStart(*[FadeIn(s_, scale=1.5) for s_ in seen], lag_ratio=0.2), FadeIn(qs))
            vo.wait_until("d")
            self.play(FadeIn(nfl))
        self.wait(0.4)
        self.clear_scene()


_ = (DATA, KERN, BG)

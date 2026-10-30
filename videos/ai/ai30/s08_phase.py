from __future__ import annotations

import numpy as np

from explainer.ai import *  # noqa: F403
from videos.ai.ai30.common import FEATURE_COLORS, PART, load

PH = [GREY_D, C.TRUE_P, C.BITS]  # feature 2 dropped; feature 2 given the dimension; both, in superposition
F1, F2 = FEATURE_COLORS[0], FEATURE_COLORS[3]


def phase_grid(M, cell, colors):
    g = VGroup()
    n, m = M.shape  # rows: density (bottom: sparse), columns: importance
    for i in range(n):
        for j in range(m):
            g.add(Square(cell, stroke_width=0.5, stroke_color="#0B0F17", fill_color=colors[int(M[i, j])],
                         fill_opacity=0.9).move_to([j * cell, i * cell, 0]))
    return g


class Phase(VoiceoverScene):
    def construct(self):
        self.card()
        self.options()
        self.diagram()
        self.highdim()

    def card(self):
        card = chapter_card(7, r"The phase diagram", r"When does a network pack features together?", part=PART)
        with self.voiceover("Chapter seven. The phase diagram."):
            self.play(FadeIn(card[0], shift=UP * 0.2), FadeIn(card[1]))
        self.play(FadeOut(card))

    # ------------------------------------------------------------------
    def line_pic(self, w1, w2, title, color):
        ln = NumberLine(x_range=[-1.2, 1.2, 1.2], length=3.2, color=GREY_C, include_ticks=True, tick_size=0.05)
        a1 = Arrow(ln.n2p(0), ln.n2p(w1), buff=0, color=F1, stroke_width=6, max_tip_length_to_length_ratio=0.3) if abs(w1) > 0.05 else Dot(ln.n2p(0), color=F1)
        a2 = Arrow(ln.n2p(0) + DOWN * 0.18, ln.n2p(w2) + DOWN * 0.18, buff=0, color=F2, stroke_width=6,
                   max_tip_length_to_length_ratio=0.3) if abs(w2) > 0.05 else Dot(ln.n2p(0) + DOWN * 0.18, color=F2)
        t = label(title, font_size=20, color=GREY_A if color is PH[0] else color).next_to(ln, UP, buff=0.35)
        box = SurroundingRectangle(VGroup(ln, a1, a2, t), buff=0.2, color=GREY_B if color is PH[0] else color,
                                   corner_radius=0.1, stroke_width=2)
        return VGroup(box, ln, a1, a2, t)

    def options(self):
        colors = {r"w": C.BITS, r"x": C.TRUE_P}
        f = cmath(r"\hat x = \operatorname{ReLU}(", r"w", r"\, ", r"w", r"^{\top}", r"x", r" + b), \qquad ", r"w",
                  r" \in \mathbb{R}^{1 \times 2}", colors=colors, font_size=36).to_edge(UP, buff=0.4)
        sub = label(r"two features, \ one number in the middle; \ feature $2$ matters $r$ times as much; \ each is "
                    r"on a fraction $\rho$ of the time", font_size=22, color=GREY_A).next_to(f, DOWN, buff=0.25)
        pics = VGroup(self.line_pic(1, 0, r"drop feature $2$", PH[0]),
                      self.line_pic(0, 1, r"feature $2$ takes the dimension", PH[1]),
                      self.line_pic(1, -1, r"share it: \ opposite directions", PH[2])).arrange(RIGHT, buff=0.5).move_to(DOWN * 0.7)
        why_ = label(r"sharing works only if the two are rarely on together: \\ the ReLU and a negative bias cut off "
                     r"the other's shadow", font_size=22, color=GREY_A).to_edge(DOWN, buff=0.9)
        for p_ in pics:
            p_.set_opacity(0.2)
        cite_ = cite(r"Elhage et al., \textit{Toy Models of Superposition} (2022), \ \S 4", corner=DR)
        with self.voiceover(
            "Chapter six showed superposition happen. Elhage and colleagues asked when it happens, and drew the "
            "answer as a phase diagram. <bookmark mark='a'/> The smallest case: two features, squeezed through a "
            "single number. Feature two matters r times as much as feature one, and each is on a fraction rho of the "
            "time. <bookmark mark='b'/> The network has three choices. Drop feature two. <bookmark mark='c'/> Give "
            "feature two the dimension and drop feature one. <bookmark mark='d'/> Or share: point the two features "
            "in opposite directions, and let the ReLU, with a negative bias, cut off each one's shadow on the other. "
            "Sharing only pays when they are rarely on at the same time."
        ) as vo:
            self.play(Write(f), FadeIn(cite_), FadeIn(pics))
            vo.wait_until("a")
            self.play(FadeIn(sub))
            vo.wait_until("b")
            self.play(pics[0].animate.set_opacity(1))
            vo.wait_until("c")
            self.play(pics[1].animate.set_opacity(1))
            vo.wait_until("d")
            self.play(pics[2].animate.set_opacity(1), FadeIn(why_))
        self.wait(0.3)
        self.clear_scene()

    # ------------------------------------------------------------------
    def diagram(self):
        p = load("phase")
        emp, th = np.asarray(p["emp"]), np.asarray(p["theory"])
        dens, rel = np.asarray(p["dens"]), np.asarray(p["rel"])
        cell = 0.26
        ge = phase_grid(emp, cell, PH).move_to([-3.1, -0.45, 0])
        gt = phase_grid(th, cell, PH).move_to([3.0, -0.45, 0])

        def frame(g, title):
            t = label(title, font_size=22, color=WHITE).next_to(g, UP, buff=0.2)
            xl = label(r"$r$: \ how much feature $2$ matters \ ($0.1$ to $10$)", font_size=17, color=GREY_B)
            xl.next_to(g, DOWN, buff=0.15)
            yl = label(r"density $\rho$ \\ ($0.01$ to $1$)", font_size=17, color=GREY_B).next_to(g, LEFT, buff=0.15)
            return VGroup(t, xl, yl)

        fe = frame(ge, rf"trained: \ ${len(dens) * len(rel)}$ cells, \ best of ${int(p['seeds'])}$ seeds")
        ft = frame(gt, r"theory: \ the cheapest of the three")
        lg = VGroup(*[VGroup(Square(0.22, fill_color=c_, fill_opacity=0.9, stroke_width=0), label(t, font_size=18, color=GREY_A))
                      .arrange(RIGHT, buff=0.12) for c_, t in zip(PH, (r"feature $2$ dropped", r"feature $2$ takes the dimension",
                                                                         r"superposition"))]).arrange(RIGHT, buff=0.5)
        lg.to_edge(UP, buff=0.3)
        # one cell's run, replayed: its two weights as training goes
        tr = np.asarray(p["traj"])
        i0, j0 = int(p["mid"][0]), int(p["mid"][1])
        mark = Square(cell, color=WHITE, stroke_width=3).move_to(ge[i0 * len(rel) + j0])
        S = float(tr[-1, 0])
        lim = float(np.abs(tr[:, 1:]).max()) * 1.1
        gi = axes([0, S], [-lim, lim], x_length=4.6, y_length=2.6, xlabel=r"training steps", ylabel=r"the two weights",
                  xticks=[0, S], yticks=[-1, 0, 1], center=[3.0, -0.6, 0])
        w1 = curve(gi.ax, tr[:, 0], tr[:, 1], F1, 3)
        w2 = curve(gi.ax, tr[:, 0], tr[:, 2], F2, 3)
        it = label(rf"the marked cell: \ $\rho = {dens[i0]:.2f}$, \ $r = {rel[j0]:.1f}$", font_size=18, color=WHITE)
        it.next_to(gi, UP, buff=0.15)
        link = DashedLine(mark.get_right(), gi.get_left(), color=GREY_C, dash_length=0.06)
        agree = float(p["agree"])
        cellsay = ["the second weight shrinking to zero", "the first weight shrinking to zero",
                   "the two weights settling into opposite signs"][int(emp[i0, j0])]
        n_sup = int((emp == 2).sum())
        sparse_row = emp[0]
        dense_row = emp[-1]
        with self.voiceover(
            f"We trained the little model on a grid of {len(dens)} densities by {len(rel)} importances, four seeds "
            "a cell, and kept the best. <bookmark mark='a'/> Each cell is coloured by what the trained network did "
            f"with feature two; here is one cell's training, {cellsay}. "
            f"<bookmark mark='b'/> When features are dense, at the top, the network shares in "
            f"{int((dense_row == 2).sum())} of the top row's {len(rel)} cells: one feature gets the dimension, the "
            "other is dropped. <bookmark mark='c'/> When features are sparse, at the bottom, sharing "
            f"wins across {int((sparse_row == 2).sum())} of {len(rel)} cells. <bookmark mark='d'/> On the right, the "
            "same map from theory: for every cell, the expected loss of each of the three choices, and the "
            f"cheapest. They agree on {100 * agree:.0f} percent of the cells, and the misses sit on the boundaries, "
            "where two choices cost almost the same. Superposition is a phase the network enters when features are "
            "sparse enough."
        ) as vo:
            blank = ge.copy().set_fill(GREY_D, opacity=0.25)
            self.play(FadeIn(lg), FadeIn(fe), FadeIn(blank))
            vo.wait_until("a")
            self.play(LaggedStart(*[FadeIn(c) for c in ge], lag_ratio=0.004), run_time=3)
            self.play(Create(mark), Create(link), FadeIn(gi), FadeIn(it))
            self.play(Create(w1), Create(w2), run_time=2.5)
            vo.wait_until("b")
            self.play(FadeOut(VGroup(gi, w1, w2, it, link)))
            self.play(Indicate(VGroup(*ge[-len(rel):]), color=WHITE, scale_factor=1.03))
            vo.wait_until("c")
            self.play(Indicate(VGroup(*ge[:len(rel)]), color=WHITE, scale_factor=1.03))
            vo.wait_until("d")
            self.play(FadeIn(ft), LaggedStart(*[FadeIn(c) for c in gt], lag_ratio=0.004), run_time=3)
        self.wait(0.3)
        self.clear_scene()
    # ------------------------------------------------------------------
    def highdim(self):
        s = load("superposition")
        dims = [int(d) for d in s["dims"]]
        e = np.asarray(s["cos_edges"])
        top = max(float(np.max(s[f"cos_hist{d}"])) for d in dims)
        ax = Axes(x_range=[-1, 1, 0.5], y_range=[0, top * 1.05, top], x_length=8.0, y_length=3.6, tips=False,
                  axis_config={"stroke_color": GREY_C, "include_ticks": True, "tick_size": 0.05}).move_to([-1.4, -0.5, 0])
        xt = VGroup(*[MathTex(t, font_size=24, color=GREY_B).next_to(ax.c2p(v, 0), DOWN, buff=0.12)
                      for t, v in ((r"-1", -1), (r"0", 0), (r"1", 1))])
        xn = label(r"the cosine between two random directions \ ($0$: perpendicular)", font_size=22, color=GREY_A)
        xn.next_to(xt, DOWN, buff=0.12)
        w = (e[1] - e[0]) * ax.x_length / 2

        def hist(d):
            h = np.asarray(s[f"cos_hist{d}"])
            return VGroup(*[Rectangle(width=w * 0.9, height=max(v / top * ax.y_length / 1.05, 0.005), stroke_width=0, fill_color=C.TRUE_P,
                                      fill_opacity=0.85).move_to(ax.c2p((e[i] + e[i + 1]) / 2, 0), aligned_edge=DOWN)
                            for i, v in enumerate(h)])

        def dl(d):
            return label(rf"in ${d}$ dimensions: \ spread $\approx {float(s[f'cos_std{d}']):.3f}$", font_size=28,
                         color=C.TRUE_P).move_to([4.3, 1.4, 0])

        f = cmath(r"\text{spread} \approx \frac{1}{\sqrt{d}}", font_size=40).move_to([4.3, -0.2, 0])
        note_ = label(r"room for exponentially many \\ almost-perpendicular directions: \\ Part 3's random projections",
                      font_size=22, color=GREY_A).next_to(f, DOWN, buff=0.4)
        cite_ = cite(r"W.~B.~Johnson \& J.~Lindenstrauss (1984)", corner=DR)
        h = hist(dims[0])
        lab = dl(dims[0])
        with self.voiceover(
            "In two dimensions, five features are a crowd. But real models have hundreds or thousands of dimensions, and there, "
            "space is roomier than intuition says. <bookmark mark='a'/> Pick two random directions and measure the "
            "angle between them. In two dimensions, anything goes. <bookmark mark='b'/> In sixteen, they're "
            "usually close to perpendicular; in a hundred and twenty-eight, very close; <bookmark mark='c'/> in a "
            "thousand and twenty-four, the cosine is within a few hundredths of zero. The spread shrinks like one "
            "over root d, so the number of almost-perpendicular directions grows exponentially with the dimension. "
            "That's part three's random projections again, and it's why models can store far more features than they "
            "have numbers, as long as each feature is rare."
        ) as vo:
            self.play(Create(ax), FadeIn(xt), FadeIn(xn))
            vo.wait_until("a")
            self.play(LaggedStart(*[GrowFromEdge(r_, DOWN) for r_ in h], lag_ratio=0.01), FadeIn(lab), run_time=1.5)
            vo.wait_until("b")
            for d in dims[1:3]:
                self.play(Transform(h, hist(d)), Transform(lab, dl(d)), run_time=1.5)
                self.wait(0.4)
            vo.wait_until("c")
            self.play(Transform(h, hist(dims[3])), Transform(lab, dl(dims[3])), run_time=1.5)
            self.play(Write(f), FadeIn(note_), FadeIn(cite_))
        self.wait(0.3)
        self.clear_scene()


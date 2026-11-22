from __future__ import annotations

from explainer.cs import *  # noqa: F403
from videos.cs.cs52.common import BG, DATA, HEAD, KERN, LAM, NO, PART, YES, grid_table, load


def tile(title, body, col, w=4.2, h=3.0):
    frame = RoundedRectangle(width=w, height=h, corner_radius=0.15, stroke_color=col, stroke_width=2, fill_color=BG,
                             fill_opacity=1)
    t = label(title, font_size=22, color=col)
    b = wrapped_label(body, w - 0.4, font_size=18, color=GREY_A)
    VGroup(t, b).arrange(DOWN, buff=0.3).move_to(frame)
    return VGroup(frame, t, b)


class Frontier(WatchScene):
    def construct(self):
        self.card()
        self.randomized()
        self.precision()

    def card(self):
        self.chapter(15, r"Frontier: \ randomized and low-precision numerics", r"Can randomness and fewer bits make linear algebra faster, \ and still right?", lit=(2006, 2011), extra=((2006, r"Sankar, \ Spielman and Teng: \ smoothed elimination"),
                                                     (2011, r"Halko, \ Martinsson and Tropp")), part=PART, said="Chapter fifteen, the frontier. Can randomness, and fewer bits, make linear algebra "
                            "faster and still right?")

    def randomized(self):
        self.ask(r"Multiply a big matrix by a thin random one. \\ The product captures...", [r"random noise",
                 r"the matrix's dominant range"], 1,
                 say="Multiply a huge matrix by a thin random matrix. What does the product capture?",
                 reveal="The matrix's dominant directions, with high probability.")
        r = load("rsvd")
        head = label(r"A random sketch finds the important directions", font_size=36).to_edge(UP, buff=0.3)
        # the pipeline: A (tall) times a thin random matrix, orthonormalize, small SVD
        def mat(w, h, col, name):
            rect = Rectangle(width=w, height=h, stroke_color=col, stroke_width=2, fill_color=col, fill_opacity=0.15)
            return VGroup(rect, label(name, font_size=22, color=col).move_to(rect))
        A = mat(1.6, 2.6, DATA, r"$A$")
        Om = mat(0.45, 1.6, KERN, r"$\Omega$")
        Y = mat(0.45, 2.6, HEAD, r"$Y$")
        Q = mat(0.45, 2.6, YES, r"$Q$")
        B = mat(1.6, 0.45, LAM, r"$Q^{\mathsf T}\!A$")
        times = MathTex(r"\times", font_size=36)
        eq = MathTex(r"=", font_size=36)
        arr = MathTex(r"\to", font_size=36)
        arr2 = MathTex(r"\to", font_size=36)
        VGroup(A, times, Om, eq, Y, arr, Q, arr2, B).arrange(RIGHT, buff=0.3).next_to(head, DOWN, buff=0.5)
        caps = VGroup(label(rf"{r['m']:,} $\times$ {r['n']:,}", font_size=16, color=GREY_B).next_to(A, DOWN, buff=0.1),
                      label(r"random", font_size=16, color=GREY_B).next_to(Om, DOWN, buff=0.1),
                      label(r"orthonormalize", font_size=16, color=GREY_B).next_to(Q, DOWN, buff=0.1),
                      label(r"small SVD", font_size=16, color=GREY_B).next_to(B, DOWN, buff=0.1))
        rows = []
        for x in r["rows"]:
            if x["oversample"] in (0, 10):
                rows.append([rf"{x['oversample']}", rf"{x['power']}", rf"{x['ratio']:.2f}",
                             rf"{x['seconds']:.2f} s"])
        tab = grid_table([r"extra columns", r"power steps", r"error $\div$ best possible", r"time"], rows,
                         widths=[2.4, 2.2, 3.4, 1.8], row_h=0.38, font_size=17, mono_cols=())
        tab.to_edge(DOWN, buff=0.35)
        best = min(r["rows"], key=lambda x: x["ratio"])
        with self.voiceover(
            "The first frontier is randomness. <bookmark mark='a'/> To approximate a large matrix by one of rank "
            f"{r['k']}, multiply it by a thin random matrix. The product's columns are random mixtures of the matrix's "
            "own columns, and with high probability they span almost exactly its most important directions. "
            "<bookmark mark='b'/> Orthonormalize them, project, and take the SVD of a small matrix. Nathan Halko, "
            "Per-Gunnar Martinsson and Joel Tropp analysed this in 2011. <bookmark mark='c'/> On our "
            f"{r['m']:,} by {r['n']:,} matrix, a few extra random columns and one or two power steps bring the error "
            f"to within {max(1, round(100 * (best['ratio'] - 1)))} percent of the best any rank-{r['k']} matrix can do, in a "
            f"fraction of the {r['full_seconds']:.1f} seconds a full SVD takes."
        ) as vo:
            self.play(FadeIn(head))
            vo.wait_until("a")
            self.play(FadeIn(A), FadeIn(times), FadeIn(Om), FadeIn(caps[0]), FadeIn(caps[1]))
            self.play(FadeIn(eq), GrowFromEdge(Y, LEFT))
            vo.wait_until("b")
            self.play(FadeIn(arr), FadeIn(Q), FadeIn(caps[2]))
            self.play(FadeIn(arr2), FadeIn(B), FadeIn(caps[3]))
            vo.wait_until("c")
            self.play(FadeIn(tab.rule), FadeIn(VGroup(*tab.cells[0])),
                      LaggedStart(*[FadeIn(VGroup(*c)) for c in tab.cells[1:]], lag_ratio=0.2))
        self.wait(0.4)
        self.clear_scene()

    def precision(self):
        rows = load("refine")["rows"]
        head = label(r"Fewer bits, \ then a correction", font_size=36).to_edge(UP, buff=0.3)
        ax = Axes(x_range=[0, 6, 1], y_range=[-16, 2, 2], x_length=7.2, y_length=4.2,
                  axis_config={"color": GREY_D, "include_numbers": False})
        ax.next_to(head, DOWN, buff=0.5).shift(LEFT * 2.2)
        yt = VGroup(*[label(rf"$10^{{{v}}}$", font_size=16, color=GREY_B).next_to(ax.c2p(0, v), LEFT, buff=0.1)
                      for v in (-16, -12, -8, -4, 0)])
        xt = VGroup(*[label(rf"{v}", font_size=16, color=GREY_B).next_to(ax.c2p(v, -16), DOWN, buff=0.1)
                      for v in range(7)])
        xl = label(r"refinement steps", font_size=17, color=GREY_A).next_to(ax, DOWN, buff=0.45)
        yl = label(r"error", font_size=17, color=GREY_A).next_to(ax, LEFT, buff=0.6).shift(UP * 1.6)
        import math
        cols = (YES, HEAD, NO)
        lines, keys = VGroup(), VGroup()
        for r, c in zip(rows, cols):
            pts = [ax.c2p(i, max(-16, min(2, math.log10(max(e, 1e-17))))) for i, e in enumerate(r["errors"])]
            lines.add(VMobject(color=c, stroke_width=3).set_points_as_corners(pts))
            keys.add(label(rf"$\kappa = 10^{{{round(math.log10(r['kappa']))}}}$", font_size=19, color=c))
        keys.arrange(DOWN, aligned_edge=LEFT, buff=0.2).next_to(ax, RIGHT, buff=0.4).shift(UP * 0.8)
        side = wrapped_label(r"factor in single precision \ (fast; \ on GPUs, \ half precision is faster still), \ "
                             r"compute the residual in double, \ solve for a correction with the cheap factors; \ "
                             r"it converges when $\kappa \cdot u_{\mathrm{low}} < 1$", 4.6, font_size=18,
                             color=GREY_A).next_to(keys, DOWN, buff=0.4).align_to(keys, LEFT)
        with self.voiceover(
            "The second frontier is precision. Graphics processors do arithmetic in sixteen bits many times faster "
            "than in sixty-four, because machine learning wants them to. Can numerical linear algebra use those "
            "bits without losing accuracy? <bookmark mark='a'/> Iterative refinement, an idea of Wilkinson's, says "
            "yes, sometimes. Factor the matrix cheaply in low precision, compute the residual in high precision, and "
            "solve for a correction using the cheap factors. <bookmark mark='b'/> For a well-conditioned matrix the "
            "error falls to double precision in two or three steps. <bookmark mark='c'/> For condition number ten to "
            "the eight, times single precision's epsilon of about ten to the minus seven, the product exceeds one, "
            "and refinement diverges. Since 2019 a benchmark built on this idea runs beside the classic Linpack "
            "ranking of supercomputers."
        ) as vo:
            self.play(FadeIn(head), Create(ax), FadeIn(yt), FadeIn(xt), FadeIn(xl), FadeIn(yl))
            vo.wait_until("a")
            self.play(FadeIn(side))
            vo.wait_until("b")
            self.play(Create(lines[0]), FadeIn(keys[0]), Create(lines[1]), FadeIn(keys[1]), run_time=2)
            vo.wait_until("c")
            self.play(Create(lines[2]), FadeIn(keys[2]), run_time=2)
        self.wait(0.4)
        self.clear_scene()




_ = (DATA, KERN, LAM, NO, YES)

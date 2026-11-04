from __future__ import annotations

import numpy as np

from videos.stats.stats5.common import *  # noqa: F403


class Hook(VoiceoverScene):
    def construct(self):
        self.galton()
        self.table()
        self.ellipses()
        self.mediocrity()
        self.objectives()

    def galton(self):
        tl = timeline(lit=(1886,)).to_edge(UP, buff=0.35)
        hc = history_card(1886, r"Francis Galton, \ ``Regression towards mediocrity in hereditary stature''",
                          r"\emph{Journal of the Anthropological Institute}: \ the heights of 928 adult children and their "
                          r"parents, \ 205 families", color=S.MUSEUM, width=6.8, font_size=24).move_to([-2.8, 0.6, 0])
        note_ = label(r"Galton also founded eugenics; \ the methods outlived the aims, \ which this series does not share",
                      font_size=22, color=GREY_B).to_edge(DOWN, buff=0.6)
        rec = label(r"to compare sexes he multiplied women's heights by $1.08$; \ the mid-parent is $(\text{father} + 1.08 "
                    r"\times \text{mother})/2$", font_size=22, color=GREY_A).move_to([0, -1.6, 0])
        if rec.width > 12.8:
            rec.width = 12.8
        with self.voiceover(
            "In the 1880s Francis Galton, Charles Darwin's half-cousin, collected the heights of families. "
            "<bookmark mark='a'/> He gathered records of two hundred and five families, nine hundred and twenty-eight "
            "adult children and their parents, and in 1886 published what he found, in a paper with a striking "
            "title: regression towards mediocrity in hereditary stature. <bookmark mark='b'/> To put men and women "
            "on one scale he multiplied every woman's height by one point oh eight, and summarized each pair of "
            "parents by their average, the mid-parent. <bookmark mark='c'/> Galton was also the founder of "
            "eugenics, the attempt to improve the human race by controlling who has children. The statistics he "
            "invented outlived those aims, which this series does not share; but the record should say both."
        ) as vo:
            self.play(FadeIn(tl))
            vo.wait_until("a")
            self.play(FadeIn(hc, shift=RIGHT * 0.2))
            vo.wait_until("b")
            self.play(FadeIn(rec))
            vo.wait_until("c")
            self.play(FadeIn(note_))
        self.clear_scene()

    def table(self):
        d = load("galton")
        P, C, T = np.asarray(d["P"]), np.asarray(d["C"]), np.asarray(d["T"])
        cw, ch = 0.62, 0.42
        grid = VGroup()
        for i, p in enumerate(P):
            for j, c in enumerate(C):
                v = int(T[i, j])
                sq = Rectangle(width=cw, height=ch, stroke_color=GREY_D, stroke_width=0.8,
                               fill_color=interpolate_color(ManimColor("#121722"), ManimColor(S.MUSEUM), min(1, v / 48)),
                               fill_opacity=1)
                sq.move_to([(j - len(C) / 2) * cw, (i - len(P) / 2) * ch, 0])
                cell = VGroup(sq)
                if v:
                    cell.add(MathTex(str(v), font_size=16, color=WHITE if v < 30 else BLACK).move_to(sq))
                grid.add(cell)
        grid.move_to([0.4, -0.5, 0])
        xl = VGroup(*[MathTex(f"{c:g}", font_size=16, color=GREY_B).move_to([grid.get_left()[0] + (j + 0.5) * cw,
                                                                             grid.get_bottom()[1] - 0.2, 0])
                      for j, c in enumerate(C)])
        yl = VGroup(*[MathTex(f"{p:g}", font_size=16, color=GREY_B).move_to([grid.get_left()[0] - 0.35,
                                                                             grid.get_bottom()[1] + (i + 0.5) * ch, 0])
                      for i, p in enumerate(P)])
        xt = label(r"child's height (inches)", font_size=22, color=GREY_A).next_to(xl, DOWN, buff=0.15)
        yt = label(r"mid-parent (inches)", font_size=22, color=GREY_A).rotate(PI / 2).next_to(yl, LEFT, buff=0.15)
        src = historical_tag(r"Galton (1886), Table I; \ HistData")
        with self.voiceover(
            "Here is Galton's table, exactly as he grouped it. <bookmark mark='a'/> Each row is a mid-parent height, "
            "in inches; each column a child's adult height; each cell the number of children. "
            "<bookmark mark='b'/> Tall parents, near the top, tend to have tall children, toward the right; short "
            "parents short children. But the counts are spread widely: a table of tendencies, not of rules. Galton "
            "stared at it for a long time before he saw its shape."
        ) as vo:
            self.play(FadeIn(src), FadeIn(xt), FadeIn(yt), FadeIn(xl), FadeIn(yl))
            vo.wait_until("a")
            self.play(LaggedStart(*[FadeIn(c) for c in grid], lag_ratio=0.004), run_time=3.0)
            vo.wait_until("b")
            self.play(Indicate(grid, color=S.ACCENT, scale_factor=1.01))
        self.grid_parts = (grid, xl, yl, xt, yt, src)

    def ellipses(self):
        d = load("galton")
        grid, xl, yl, xt, yt, src = self.grid_parts
        A = axes([60.5, 75.5], [62.5, 74.5], x_length=7.6, y_length=5.0, xlabel=r"child (inches)",
                 ylabel=r"mid-parent (inches)", xticks=[62, 66, 70, 74], yticks=[64, 68, 72], center=[-1.6, -0.3, 0])
        ax = A.ax
        # Galton's orientation: child across, mid-parent up
        Ts = np.asarray(d["Ts"])
        P, C = np.asarray(d["P"]), np.asarray(d["C"])
        Pm, Cm = (P[:-1] + P[1:]) / 2, (C[:-1] + C[1:]) / 2
        dots = VGroup()
        for i, p in enumerate(Pm):
            for j, c in enumerate(Cm):
                v = Ts[i, j]
                if v > 0:
                    dots.add(Dot(ax.c2p(c, p), radius=0.03 + 0.012 * np.sqrt(v), color=S.MUSEUM, fill_opacity=0.75))
        S_ = np.asarray(d["S"])
        cov = np.array([[S_[1, 1], S_[0, 1]], [S_[0, 1], S_[0, 0]]])
        ells = VGroup(*[ellipse_curve(ax, [d["my"], d["mx"]], cov, c, S.ACCENT, 2.5, 1.0 - 0.25 * k)
                        for k, c in enumerate((0.7, 1.4, 2.1))])
        cap = label(r"smoothed (Galton averaged each $2 \times 2$ block): \ the counts lie on ellipses", font_size=24,
                    color=S.ACCENT).to_edge(UP, buff=0.35)
        side = VGroup(label(r"nested: \ one centre, \ one shape", font_size=26, color=S.ACCENT),
                      label(r"the same ellipses as Part 4's spectral theorem", font_size=22, color=GREY_B))
        side.arrange(DOWN, aligned_edge=LEFT, buff=0.2).move_to([4.6, 0.2, 0])
        for s_ in side:
            if s_.width > 4.0:
                s_.width = 4.0
        with self.voiceover(
            "Galton smoothed the table, replacing each count by the average of a block of four, and then drew lines "
            "through cells with equal counts. <bookmark mark='a'/> What emerged were ellipses, all with the same "
            "centre and the same shape, nested inside one another. <bookmark mark='b'/> He took them to a mathematician, J. D. Hamilton "
            "Dickson, who confirmed that they're exactly what a bivariate normal law predicts. They're the ellipses of "
            "Part 4's spectral theorem, drawn by nature in a table of heights."
        ) as vo:
            self.play(FadeOut(VGroup(grid, xl, yl, xt, yt)), FadeIn(A))
            self.play(FadeIn(dots, lag_ratio=0.01), FadeIn(cap))
            vo.wait_until("a")
            self.play(LaggedStart(*[Create(e) for e in ells], lag_ratio=0.3), run_time=3.0)
            vo.wait_until("b")
            self.play(FadeIn(side))
        self.clear_scene()

    def mediocrity(self):
        d = load("galton")
        P = np.asarray(d["P"])
        rm = d["row_means"]
        A = axes([63, 74], [63, 74], x_length=5.2, y_length=5.2, xlabel=r"mid-parent (inches)",
                 ylabel=r"mean child (inches)", xticks=[64, 68, 72], yticks=[64, 68, 72], center=[-3.6, -0.4, 0])
        ax = A.ax
        diag = DashedLine(ax.c2p(63, 63), ax.c2p(74, 74), color=GREY_C, stroke_width=2)
        dl = label(r"children like their parents", font_size=20, color=GREY_B).next_to(ax.c2p(72, 73.5), LEFT, buff=0.1)
        pts = VGroup(*[Dot(ax.c2p(p, m), radius=0.08, color=S.MUSEUM) for p, m in zip(P, rm) if m is not None])
        b = d["b_yx"]
        line = Line(ax.c2p(63, d["my"] + b * (63 - d["mx"])), ax.c2p(74, d["my"] + b * (74 - d["mx"])), color=COND,
                    stroke_width=3)
        info = VGroup(MathTex(rf"\text{{slope}} = {b:.2f} \approx \tfrac23", font_size=34, color=COND),
                      label(r"each inch of parental deviation: \ two-thirds of an inch in the child", font_size=24),
                      label(r"tall parents' children: \ tall, \ but less so", font_size=24, color=GREY_A),
                      label(r"short parents' children: \ short, \ but less so", font_size=24, color=GREY_A),
                      label(r"``regression towards mediocrity''", font_size=28, color=S.ACCENT))
        info.arrange(DOWN, aligned_edge=LEFT, buff=0.25).move_to([2.9, 0.4, 0])
        src = historical_tag(r"Galton (1886); \ the mean child height in each mid-parent row", corner=DR)
        with self.voiceover(
            "Then Galton asked the question of this part. <bookmark mark='a'/> For each mid-parent height, what is the "
            "average height of the children? <bookmark mark='b'/> If children simply resembled their parents, the "
            "averages would lie on the diagonal. <bookmark mark='c'/> They don't. They lie on a flatter line, with "
            f"slope about {b:.2f}, which Galton called two thirds. <bookmark mark='d'/> Children of tall parents are "
            "tall, but less extreme than their parents; children of short parents are short, but less so. Galton "
            "called it regression towards mediocrity. He thought he'd discovered a law of heredity. In fact he'd "
            "discovered a fact about every ellipse, and by the end of this part we'll see why it must happen, and "
            "why it fools people still."
        ) as vo:
            self.play(FadeIn(A), FadeIn(src))
            vo.wait_until("a")
            self.play(LaggedStart(*[FadeIn(p, scale=1.5) for p in pts], lag_ratio=0.1))
            vo.wait_until("b")
            self.play(Create(diag), FadeIn(dl))
            vo.wait_until("c")
            self.play(Create(line), FadeIn(info[:2]))
            vo.wait_until("d")
            self.play(FadeIn(info[2:]))
        self.clear_scene()

    def objectives(self):
        head = VGroup(label(r"Part 5", font_size=34, color=GREY_B), label(r"Many Variables at Once", font_size=60))
        head.arrange(DOWN, buff=0.25)
        obj = objectives_card([
            r"joint, marginal and conditional distributions; \ uncorrelated is not independent",
            r"conditional expectation as the best predictor; \ Eve's law, \ $R^2$",
            r"the multivariate normal; \ conditioning it with a Schur complement; \ regression to the mean; \ three lines",
            r"change of variables; \ latent variables and mixtures; \ copulas and their tails",
            r"exchangeability and P\'olya's urn; \ measuring dependence; \ the Dirichlet on the simplex",
        ], color=S.ACCENT, font_size=26)
        prereq = note(r"prerequisites: \ Parts 3 and 4").to_corner(DL, buff=0.3)
        built = label(r"Built in this part: \ a Gaussian slicer, \ and a P\'olya urn machine", font_size=28, color=S.ACCENT)
        built.to_edge(DOWN, buff=0.8)
        with self.voiceover(
            "This part asks: what does knowing one thing tell you about another? <bookmark mark='a'/> Part five: many "
            "variables at once. <bookmark mark='b'/> Joint, marginal and conditional distributions; dependence; "
            "conditional expectation as the best possible prediction, and the law of total variance; the "
            "multivariate normal and its conditionals, which give birth to regression; regression to the mean; "
            "change of variables; latent variables; copulas; exchangeability; how to measure dependence; and the "
            "simplex. <bookmark mark='c'/> We'll build a Gaussian slicer, to cut a density and renormalize the slice, "
            "and a Pólya urn machine."
        ) as vo:
            vo.wait_until("a")
            self.play(FadeIn(head, shift=UP * 0.2))
            vo.wait_until("b")
            self.play(FadeOut(head), FadeIn(obj, shift=UP * 0.2), FadeIn(prereq))
            vo.wait_until("c")
            self.play(obj.animate.shift(UP * 0.4), FadeIn(built))
        self.wait(1.0)
        self.clear_scene()

from __future__ import annotations

from videos.psychology.psych32.common import *  # noqa: F403


class Factor(VoiceoverScene):
    def construct(self):
        self.card()
        self.model()
        self.tetrad()
        self.fit()
        self.test()

    def card(self):
        card = chapter_card(2, r"One factor, \ derived", r"What would a single common cause predict?",
                            lit={1904: r"Spearman", 1940: r"Lawley", 1967: r"J\"oreskog"}, part=PART,
                            scale=("group",), marr=("what",))
        with self.voiceover("Chapter two. One factor, derived."):
            self.play(FadeIn(card, shift=UP * 0.2))
        self.clear_scene()

    def model(self):
        d = load("spearman")
        head = heading(r"The model")
        g = Circle(radius=0.45, color=G, fill_color=G, fill_opacity=0.2, stroke_width=3).move_to([-3.3, 1.4, 0])
        gl = label(r"$g$", font_size=34, color=G).move_to(g)
        boxes = VGroup()
        arrows = VGroup()
        for i, nm in enumerate(d["names"]):
            b = VGroup(RoundedRectangle(corner_radius=0.08, width=1.5, height=0.5, color=WHITE, stroke_width=2),
                       label(nm, font_size=16))
            b[1].move_to(b[0])
            b.move_to([-6.0 + 1.1 * i * 1.0 + 0.0, -1.0, 0]).shift(RIGHT * 0.6 * i)
            boxes.add(b)
            a = Arrow(g.get_bottom(), b.get_top(), buff=0.08, color=G, stroke_width=3)
            arrows.add(VGroup(a, label(f"{d['loadings'][i]:.2f}", font_size=15, color=G).move_to(
                a.point_from_proportion(0.55) + LEFT * 0.25)))
        diagram = VGroup(g, gl, boxes, arrows)
        eqs = VGroup(
            label(r"$x_j = \lambda_j\, g + \sqrt{1 - \lambda_j^2}\; e_j$", font_size=30),
            label(r"$r_{jk} = \lambda_j \lambda_k \quad (j \neq k)$", font_size=30, color=G),
            label(r"$R = \lambda\lambda^{\top} + \Psi$", font_size=30, color=MODEL),
        ).arrange(DOWN, buff=0.35, aligned_edge=LEFT).move_to([3.6, 1.2, 0])
        rows = rows_of([
            (r"each score is a share of $g$ plus something specific to that test, \ with $g$ and the specifics "
             r"independent", WHITE),
            (r"then two tests correlate only through $g$: \ the product of their loadings", G),
            (r"the whole matrix is one column of loadings times itself, \ plus a diagonal of uniquenesses", MODEL),
        ], 12.4, 22, 0.32).move_to([0, -2.6, 0])
        with self.voiceover(
            "Write down what one common cause would mean. <bookmark mark='a'/> Each score is a share of g, a "
            "loading lambda times g, plus something specific to that test, and g and the specifics are independent. "
            "<bookmark mark='b'/> Then two tests correlate only through g, and their correlation is the product of "
            "their loadings. <bookmark mark='c'/> The whole correlation matrix is one column of loadings times "
            "itself, plus a diagonal of uniquenesses. Six tests have fifteen correlations; the model explains them "
            "with six numbers."
        ) as vo:
            self.play(FadeIn(head), FadeIn(diagram))
            vo.wait_until("a")
            self.play(FadeIn(eqs[0]), FadeIn(rows[0]))
            vo.wait_until("b")
            self.play(FadeIn(eqs[1]), FadeIn(rows[1]))
            vo.wait_until("c")
            self.play(FadeIn(eqs[2]), FadeIn(rows[2]))
        self.clear_scene()

    def tetrad(self):
        d = load("spearman")
        head = heading(r"Spearman's test: \ the tetrad difference")
        eq = VGroup(
            label(r"$r_{ab}\, r_{cd} - r_{ac}\, r_{bd} = \lambda_a\lambda_b\lambda_c\lambda_d - "
                  r"\lambda_a\lambda_c\lambda_b\lambda_d = 0$", font_size=32),
        ).move_to([0, 1.6, 0])
        A = axes([-0.2, 0.2], [0, 40], x_length=6.0, y_length=2.6, xticks=[-0.2, -0.1, 0, 0.1, 0.2], yticks=None,
                 xfmt=lambda v: f"{v:g}", xlabel=r"tetrad differences in Spearman's table", center=[-2.6, -1.4, 0],
                 font_size=15)
        tet = np.asarray(d["tetrads"])
        edges = np.linspace(-0.2, 0.2, 17)
        cnt, _ = np.histogram(tet, edges)
        hb = bars(A.ax, (edges[:-1] + edges[1:]) / 2, cnt, G, width=0.022)
        rows = rows_of([
            (r"if one factor causes all the correlations, \ every tetrad difference is zero", WHITE),
            (rf"in Spearman's table: \ {len(tet)} tetrads, \ mean absolute size {d['tetrad_mean_abs']:.3f}, \ "
             rf"small and scattered around zero", G),
            (r"a test of a theory with nothing but a table of correlations", MODEL),
        ], 5.2, 22, 0.36).move_to([3.9, -1.3, 0])
        tag = psyche_tag(r"\texttt{traits.tetrads}; \ data: Spearman (1904)")
        with self.voiceover(
            "That gives Spearman a test. <bookmark mark='a'/> Take any four tests, a, b, c and d. If one factor "
            "causes all the correlations, r a b times r c d minus r a c times r b d is a product of the same four "
            "loadings minus itself: zero. Every tetrad difference vanishes. <bookmark mark='b'/> In Spearman's "
            f"table there are {len(tet)} of them, and their mean absolute size is {d['tetrad_mean_abs']:.3f}, "
            "small, and scattered on both sides of zero. <bookmark mark='c'/> It's a test of "
            "a theory using nothing but a table of correlations."
        ) as vo:
            self.play(FadeIn(head), FadeIn(tag), FadeIn(eq))
            vo.wait_until("a")
            self.play(FadeIn(rows[0]))
            vo.wait_until("b")
            self.play(FadeIn(A), FadeIn(hb), FadeIn(rows[1]))
            vo.wait_until("c")
            self.play(FadeIn(rows[2]))
        self.clear_scene()

    def fit(self):
        d = load("spearman")
        head = heading(r"Fitting the loadings")
        names = d["names"]
        A = axes([-0.5, 5.5], [0, 1.0], x_length=6.0, y_length=3.6, xticks=None, yticks=[0, 0.5, 1.0],
                 yfmt=lambda v: f"{v:g}", ylabel=r"loading on $g$", center=[-2.8, -0.3, 0], font_size=15)
        b = bars(A.ax, range(6), d["loadings"], G, width=0.6)
        nm = VGroup(*[label(n[:5], font_size=15).next_to(A.ax.c2p(i, 0), DOWN, buff=0.15) for i, n in enumerate(names)])
        vals = VGroup(*[label(f"{v:.2f}", font_size=15, color=G).next_to(b[i], UP, buff=0.06)
                        for i, v in enumerate(d["loadings"])])
        rows = rows_of([
            (r"maximum likelihood: \ choose the loadings that make $\lambda\lambda^{\top} + \Psi$ closest to the "
             r"observed matrix \ (Lawley, \ J\"oreskog; \ \texttt{statkit.multi})", MODEL),
            (rf"Classics loads {d['loadings'][0]:.2f}, \ music {d['loadings'][5]:.2f}: \ the hierarchy, \ as "
             rf"numbers", G),
            (rf"the residual correlations, \ observed minus implied, \ average {d['rmsr']:.2f} in size", WHITE),
            (rf"one factor carries {pct(d['share'])} of all the variance in the six measures", GOOD),
        ], 5.4, 21, 0.36).move_to([3.7, -0.3, 0])
        tag = psyche_tag(r"\texttt{traits.one\_factor}; \ data: Spearman (1904)")
        with self.voiceover(
            "Now fit it. <bookmark mark='a'/> Maximum likelihood chooses the loadings that make lambda lambda "
            "transpose plus psi as close as possible to the observed matrix; that's Lawley's and Joreskog's method, "
            "in this series' statistics kit. <bookmark mark='b'/> Classics loads "
            f"{d['loadings'][0]:.2f}, music {d['loadings'][5]:.2f}: Spearman's hierarchy, as numbers. "
            "<bookmark mark='c'/> The residual correlations, observed minus implied, average "
            f"{d['rmsr']:.2f} in size. <bookmark mark='d'/> And one factor carries {spct(d['share'])} of all the "
            "variance in the six measures."
        ) as vo:
            self.play(FadeIn(head), FadeIn(tag), FadeIn(A), FadeIn(nm))
            vo.wait_until("a")
            self.play(FadeIn(rows[0]))
            vo.wait_until("b")
            self.play(FadeIn(b), FadeIn(vals), FadeIn(rows[1]))
            for m, r in zip("cd", rows[2:]):
                vo.wait_until(m)
                self.play(FadeIn(r, shift=RIGHT * 0.15))
        self.clear_scene()

    def test(self):
        d = load("holzinger")
        head = heading(r"Holzinger and Swineford: \ one factor is not enough")
        tbl = VGroup()
        hdr = VGroup(label(r"factors", font_size=22, color=GREY_B), label(r"$\chi^2$", font_size=22, color=GREY_B),
                     label(r"df", font_size=22, color=GREY_B), label(r"$p$", font_size=22, color=GREY_B))
        tbl.add(hdr)
        for k in range(3):
            p = d["p"][k]
            ptxt = rf"${p:.2f}$" if p >= 0.001 else r"$< 10^{-15}$" if p < 1e-15 else rf"${p:.0e}$"
            col = LOST if p < 0.01 else (G if p < 0.05 else GOOD)
            tbl.add(VGroup(label(f"{k + 1}", font_size=24), label(f"{d['chi2'][k]:.1f}", font_size=24, color=col),
                           label(f"{d['df'][k]:.0f}", font_size=24), label(ptxt, font_size=24, color=col)))
        for i, row in enumerate(tbl):
            for j, c in enumerate(row):
                c.move_to([-5.0 + 1.6 * j, 1.2 - 0.6 * i, 0])
        rows = rows_of([
            (r"the likelihood-ratio test asks whether the leftover correlations are more than sampling error, \ for "
             r"301 children", WHITE),
            (r"one factor: \ decisively rejected; \ two: \ rejected", LOST),
            (r"three: \ close to adequate: \ the visual, \ verbal and speeded blocks of chapter one", G),
            (r"Spearman's single factor fits his table; \ a broader battery needs more", YOU),
        ], 5.6, 22, 0.36).move_to([3.6, -0.2, 0])
        tag = psyche_tag(r"\texttt{statkit.multi.factor\_ml}; \ data: Holzinger \& Swineford (1939)")
        with self.voiceover(
            "Spearman's table is small. The real battery is a stronger test. <bookmark mark='a'/> The "
            "likelihood-ratio test asks whether the correlations a model leaves unexplained are more than sampling "
            "error would produce in three hundred and one children. <bookmark mark='b'/> One factor gives a "
            f"chi-squared of {d['chi2'][0]:.0f} on {d['df'][0]:.0f} degrees of freedom: decisively rejected. Two "
            f"factors are rejected too. <bookmark mark='c'/> Three factors give {d['chi2'][2]:.1f} on "
            f"{d['df'][2]:.0f}, close to adequate: the visual, verbal and speeded blocks of chapter one. "
            "<bookmark mark='d'/> Spearman's single factor fits his table. A broader battery needs more."
        ) as vo:
            self.play(FadeIn(head), FadeIn(tag), FadeIn(tbl[0]))
            vo.wait_until("a")
            self.play(FadeIn(rows[0]))
            vo.wait_until("b")
            self.play(FadeIn(tbl[1]), FadeIn(tbl[2]), FadeIn(rows[1]))
            vo.wait_until("c")
            self.play(FadeIn(tbl[3]), FadeIn(rows[2]))
            vo.wait_until("d")
            self.play(FadeIn(rows[3]))
        self.clear_scene()

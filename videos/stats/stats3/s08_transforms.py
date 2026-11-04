from __future__ import annotations

import numpy as np

from videos.stats.stats3.common import *  # noqa: F403


class Transforms(VoiceoverScene, TreeMixin):
    def construct(self):
        self.card()
        self.cdf_method()
        self.jacobian()
        self.box_muller()
        self.lognormal()
        self.tree_voiceover("Four arrows from transformations: <bookmark mark='t'/> minus the log of a uniform is "
                            "exponential; Box and Muller turn two uniforms into normals; e to a normal is log-normal; "
                            "and e to an exponential is a Pareto.", 7)

    def card(self):
        card = chapter_card(7, r"Transformations", r"If $X$ has a distribution, what does $g(X)$ have?", lit=(),
                            part=PART)
        with self.voiceover("Chapter seven. Transformations."):
            self.play(FadeIn(card[0], shift=UP * 0.2), FadeIn(card[1]))
        self.play(FadeOut(card))

    def cdf_method(self):
        d = load("transforms")
        u, e = np.asarray(d["u"]), np.asarray(d["e"])
        A = axes([0, 1], [0, 1.6], x_length=3.6, y_length=2.6, xlabel=r"$U$ uniform", xticks=[0, 1], center=[-4.6, -1.6, 0])
        A.ax.y_axis.set_opacity(0)
        ed = np.linspace(0, 1, 21)
        hu = hist_bars(A.ax, ed, np.histogram(u, ed)[0] / (len(u) * np.diff(ed)), color=SIM)
        B = axes([0, 6], [0, 1.1], x_length=4.4, y_length=2.6, xlabel=r"$Y = -\log U$", xticks=[0, 2, 4, 6],
                 center=[3.8, -1.6, 0])
        B.ax.y_axis.set_opacity(0)
        ed2 = np.linspace(0, 6, 31)
        he = hist_bars(B.ax, ed2, np.histogram(e, ed2)[0] / (len(e) * np.diff(ed2)), color=SIM)
        xs = np.linspace(0, 6, 200)
        ce = curve(B.ax, xs, np.exp(-xs), EXACT, 3)
        arrow = Arrow([-2.4, -1.6, 0], [1.2, -1.6, 0], color=GREY_B, stroke_width=3)
        al = MathTex(r"g(u) = -\log u", font_size=30).next_to(arrow, UP, buff=0.1)
        rows = [
            cmath(r"P(Y \le y)", r"=", r"P(-\log U \le y)", r"=", r"P(U \ge e^{-y})", r"=", r"1 - e^{-y}", font_size=34),
        ]
        rows[0][6].set_color(EXACT)
        rows[0].to_edge(UP, buff=0.6)
        wl = label(r"the CDF method: \ compute $P(g(X) \le y)$ \ from the law of $X$", font_size=24, color=GREY_B)
        wl.next_to(rows[0], DOWN, buff=0.25)
        inv = label(r"run backwards, \ it turns uniforms into anything: \ Part 7", font_size=22, color=GREY_A)
        inv.next_to(wl, DOWN, buff=0.2)
        with self.voiceover(
            "If X has a known distribution, what's the distribution of a function of X? <bookmark mark='a'/> "
            "Start with a uniform random number between zero and one, the kind every computer produces. "
            "<bookmark mark='b'/> Take minus its logarithm. <bookmark mark='c'/> The result is never negative, and "
            "it piles up near zero. <bookmark mark='d'/> The CDF method says exactly how. The chance that minus log "
            "U is at most y is the chance that U is at least e to the minus y, which is one minus e to the minus y: "
            "the exponential distribution, gold. <bookmark mark='e'/> Run this idea backwards and it lets a computer "
            "turn uniform random numbers into draws from any distribution at all, the subject of Part 7."
        ) as vo:
            vo.wait_until("a")
            self.play(FadeIn(A), FadeIn(hu))
            vo.wait_until("b")
            self.play(GrowArrow(arrow), FadeIn(al))
            vo.wait_until("c")
            self.play(FadeIn(B), FadeIn(he))
            vo.wait_until("d")
            self.play(Write(rows[0]), FadeIn(wl))
            self.play(Create(ce))
            vo.wait_until("e")
            self.play(FadeIn(inv))
        self.clear_scene()

    def jacobian(self):
        rows = [
            cmath(r"P(y \le Y \le y + dy)", r"=", r"P(x \le X \le x + dx)", font_size=34),
            cmath(r"f_Y(y)\, dy", r"=", r"f_X(x)\, |dx|", font_size=36),
            cmath(r"f_Y(y)", r"=", r"f_X\big(g^{-1}(y)\big) \left| \frac{d}{dy} g^{-1}(y) \right|", font_size=36),
            cmath(r"f_{\mathbf Y}(\mathbf y)", r"=", r"f_{\mathbf X}\big(g^{-1}(\mathbf y)\big)\, \big| \det J_{g^{-1}}(\mathbf y)\big|",
                  font_size=34),
        ]
        rows[2][0].set_color(EXACT)
        rows[3][0].set_color(EXACT)
        whys = [why(r"$g$ increasing: \ the same event"), why(r"probability is conserved"),
                why(r"the 1D change of variables"), why(r"in $\mathbb R^n$: \ the Jacobian determinant")]
        # a strip stretched by the map
        A = axes([0, 1], [0, 4], x_length=3.4, y_length=3.4, xticks=[0, 1], yticks=[0, 2, 4], center=[-4.6, -1.6, 0])
        ax = A.ax
        xs = np.linspace(0.02, 1, 200)
        g_ = curve(ax, xs, -np.log(xs), GREY_A, 2.5)
        strips = VGroup()
        for x0 in (0.1, 0.5, 0.85):
            dx = 0.05
            y0, y1 = -np.log(x0 + dx), -np.log(x0)
            strips.add(Rectangle(width=ax.c2p(dx, 0)[0] - ax.c2p(0, 0)[0], height=0.12, stroke_width=0, fill_color=SIM,
                                 fill_opacity=0.8).move_to(ax.c2p(x0 + dx / 2, 0) + UP * 0.06),
                       Rectangle(width=0.12, height=ax.c2p(0, y1)[1] - ax.c2p(0, y0)[1], stroke_width=0,
                                 fill_color=EXACT, fill_opacity=0.8).move_to(ax.c2p(0, (y0 + y1) / 2) + RIGHT * 0.06))
        cap = label(r"equal widths in $x$, \ unequal heights in $y$", font_size=20, color=GREY_B).next_to(A, DOWN,
                                                                                                    buff=0.15)
        with self.voiceover(
            "The general rule is about conserving probability. <bookmark mark='a'/> If g is increasing, Y lands in "
            "a tiny interval near y exactly when X lands in the matching interval near x. <bookmark mark='b'/> The "
            "two probabilities are equal, but the intervals have different widths, <bookmark mark='c'/> so the "
            "density of Y is the density of X at the matching point, times the stretch factor, the derivative of "
            "the inverse. Where the map stretches, the density thins; where it squeezes, the density piles up. "
            "<bookmark mark='d'/> In several dimensions the stretch factor is the absolute value of the Jacobian "
            "determinant: how much the map changes small areas, or volumes."
        ) as vo:
            self.play(FadeIn(A), Create(g_))
            step = ladder(self, rows, whys, keep=4, top=3.0, x=1.6, buff=0.5, edge=6.9)
            vo.wait_until("a")
            step(0, transform=False)
            self.play(FadeIn(strips), FadeIn(cap))
            vo.wait_until("b")
            step(1, transform=False)
            vo.wait_until("c")
            step(2, transform=False)
            vo.wait_until("d")
            step(3, transform=False)
        self.clear_scene()

    def box_muller(self):
        d = load("transforms")
        u1, u2 = np.asarray(d["u1"])[:1200], np.asarray(d["u2"])[:1200]
        z1, z2 = np.asarray(d["z1"])[:1200], np.asarray(d["z2"])[:1200]
        c0 = np.array([-2.4, -0.4, 0])
        sq_pts = [c0 + np.array([(a - 0.5) * 4.4, (b - 0.5) * 4.4, 0]) for a, b in zip(u1, u2)]
        n_pts = [c0 + 0.85 * np.array([a, b, 0]) for a, b in zip(z1, z2)]
        dots = VGroup(*[Dot(p, radius=0.025, color=SIM) for p in sq_pts])
        frame = Square(side_length=4.4, stroke_color=GREY_C, stroke_width=1.5).move_to(c0)
        hc = history_card(1958, r"George Box \& Mervin Muller", r"two independent uniforms $\to$ two independent "
                          r"normals", color=S.MUSEUM, width=5.0, font_size=22).move_to([4.3, 2.6, 0])
        f = VGroup(MathTex(r"R = \sqrt{-2 \log U_1}", font_size=32), MathTex(r"\Theta = 2\pi U_2", font_size=32),
                   MathTex(r"(Z_1, Z_2) = (R\cos\Theta,\ R\sin\Theta)", font_size=30, color=EXACT))
        f.arrange(DOWN, aligned_edge=LEFT, buff=0.22).move_to([4.2, 0.4, 0])
        why_ = label(r"$R^2/2$ is exponential, \ $\Theta$ uniform: \ Herschel's rotation invariance, built in",
                     font_size=22, color=GREY_B)
        if why_.width > 5.0:
            why_.width = 5.0
        why_.move_to([4.0, -1.3, 0])
        chk = MathTex(rf"\text{{mean }} {d['z_mean']:.3f},\ \text{{SD }} {d['z_sd']:.3f}", font_size=26, color=SIM)
        chk.move_to([4.2, -2.3, 0])
        with self.voiceover(
            "Here's a two-dimensional transformation that's in every statistics library. <bookmark mark='a'/> In "
            "1958 George Box and Mervin Muller showed how to turn two independent uniforms into two independent "
            "normals. <bookmark mark='b'/> Start with a cloud of points spread evenly over a square. "
            "<bookmark mark='c'/> Use the first coordinate to choose a radius, the square root of minus twice its "
            "log, and the second to choose an angle. <bookmark mark='d'/> Watch the square become a bell. "
            "<bookmark mark='e'/> Why does it work? Half the squared radius is minus log U one, which we just saw "
            "is exponential, and the angle is uniform; that's exactly the polar description of two independent "
            "normals, Herschel's rotation invariance built in. The Jacobian makes it precise, and the sample's mean "
            "and SD come out zero and one."
        ) as vo:
            vo.wait_until("a")
            self.play(FadeIn(hc))
            vo.wait_until("b")
            self.play(Create(frame), FadeIn(dots, lag_ratio=0.002))
            vo.wait_until("c")
            self.play(Write(f[0]), Write(f[1]))
            vo.wait_until("d")
            self.play(FadeOut(frame), *[dt.animate.move_to(p) for dt, p in zip(dots, n_pts)], run_time=3.5)
            self.play(Write(f[2]))
            vo.wait_until("e")
            self.play(FadeIn(why_), FadeIn(chk))
        self.clear_scene()

    def lognormal(self):
        d = load("transforms")
        prod = np.asarray(d["prod"])
        A = axes([0, 15], [0, 0.4], x_length=5.8, y_length=3.4, xlabel=r"product of 60 random factors",
                 xticks=[0, 5, 10, 15], center=[-3.4, -0.8, 0])
        A.ax.y_axis.set_opacity(0)
        ed = np.linspace(0, 15, 46)
        hp = hist_bars(A.ax, ed, np.histogram(prod, ed)[0] / (len(prod) * np.diff(ed)), color=SIM)
        B = axes([-3, 5], [0, 0.45], x_length=5.4, y_length=3.4, xlabel=r"its logarithm", xticks=[-2, 0, 2, 4],
                 center=[3.6, -0.8, 0])
        B.ax.y_axis.set_opacity(0)
        lp = np.log(prod)
        ed2 = np.linspace(-3, 5, 41)
        hl = hist_bars(B.ax, ed2, np.histogram(lp, ed2)[0] / (len(lp) * np.diff(ed2)), color=SIM)
        xs = np.linspace(-3, 5, 200)
        m, s = d["logp_mean"], d["logp_sd"]
        nc = curve(B.ax, xs, np.exp(-(xs - m) ** 2 / (2 * s * s)) / (s * np.sqrt(2 * np.pi)), EXACT, 3)
        sk = VGroup(MathTex(rf"\text{{skewness }} {d['prod_skew']:.1f}", font_size=26, color=GREY_A).next_to(A, UP, buff=0.2),
                    MathTex(rf"\text{{skewness }} {d['logp_skew']:.3f}", font_size=26, color=GREY_A).next_to(B, UP, buff=0.2))
        title = label(r"each factor uniform on $[0.8,\, 1.25]$: \ growth that compounds", font_size=26,
                      color=GREY_A).to_edge(UP, buff=0.4)
        take = label(r"sums $\to$ normal; \ products $\to$ log-normal: \ incomes, city sizes, particle sizes",
                     font_size=24, color=S.ACCENT).to_edge(DOWN, buff=0.35)
        with self.voiceover(
            "One last transformation, and it explains Part 1's incomes. <bookmark mark='a'/> Take sixty random "
            "factors, each between point eight and one point two five, and multiply them: growth that compounds, a "
            "year of good luck or bad luck at a time. <bookmark mark='b'/> The products are wildly skewed. "
            "<bookmark mark='c'/> But their logarithms are sums of sixty small random terms, and sums make bells: "
            "the logarithm is normal, skewness essentially zero. <bookmark mark='d'/> A variable whose logarithm is "
            "normal is called log-normal. Sums of many small effects give normals; products of many small effects "
            "give log-normals, which is why incomes, city sizes and particle sizes are skewed the way they are."
        ) as vo:
            vo.wait_until("a")
            self.play(FadeIn(title))
            vo.wait_until("b")
            self.play(FadeIn(A), FadeIn(hp), FadeIn(sk[0]))
            vo.wait_until("c")
            self.play(FadeIn(B), FadeIn(hl), Create(nc), FadeIn(sk[1]))
            vo.wait_until("d")
            self.play(FadeIn(take))
        self.clear_scene()

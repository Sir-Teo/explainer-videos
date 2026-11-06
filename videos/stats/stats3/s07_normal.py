from __future__ import annotations

import numpy as np

from videos.stats.stats3.common import *  # noqa: F403


class Normal(VoiceoverScene, TreeMixin):
    def construct(self):
        self.card()
        self.demoivre()
        self.gauss()
        self.herschel()
        self.integral()
        self.rule()
        self.tree_voiceover("Two arrows into the normal: <bookmark mark='t'/> de Moivre's, from the binomial with many "
                            "trials, and the Poisson with a large mean, which is a sum of many small Poissons.", 6)

    def card(self):
        card = chapter_card(6, r"The normal, three ways", r"One curve, reached from three directions", lit=(1733,),
                            part=PART)
        with self.voiceover("Chapter six. The normal, three ways."):
            self.play(FadeIn(card[0], shift=UP * 0.2), FadeIn(card[1]))
        self.play(FadeOut(card))

    def demoivre(self):
        d = load("normal")
        hc = history_card(1733, r"Abraham de Moivre", r"the binomial for large $n$, via Stirling's $n! \approx \sqrt{2\pi n}"
                          r"\,(n/e)^n$", color=S.MUSEUM, width=5.4, font_size=22).to_corner(UL, buff=0.3)
        A = axes([-4, 4], [0, 0.45], x_length=7.6, y_length=4.2, xlabel=r"$(k - n/2) / \sqrt{n/4}$",
                 xticks=[-3, -2, -1, 0, 1, 2, 3], yticks=[0, 0.2, 0.4], center=[-1.6, -0.9, 0])
        ax = A.ax
        xs = np.linspace(-4, 4, 300)
        bell = curve(ax, xs, np.exp(-xs ** 2 / 2) / np.sqrt(2 * np.pi), EXACT, 3)
        sets = []
        for b in d["binoms"]:
            n = b["n"]
            pmf = np.asarray(b["pmf"])
            k = np.arange(n + 1)
            z = (k - n / 2) / np.sqrt(n / 4)
            w = 1 / np.sqrt(n / 4)
            keep = np.abs(z) < 4
            bars = VGroup(*[Rectangle(width=(ax.c2p(w * 0.85, 0)[0] - ax.c2p(0, 0)[0]),
                                      height=max(ax.c2p(0, p / w)[1] - ax.c2p(0, 0)[1], 0.002), stroke_width=0,
                                      fill_color=DISC, fill_opacity=0.8).move_to(ax.c2p(zz, p / w / 2))
                            for zz, p in zip(z[keep], pmf[keep])])
            sets.append((n, bars))
        lab = [MathTex(rf"n = {n}", font_size=34, color=DISC).move_to([4.4, 1.6, 0]) for n, _ in sets]
        st = VGroup(*[MathTex(rf"n = {r[0]}:\ \ n!\ /\ \text{{Stirling}} = {r[3]:.4f}", font_size=24,
                              color=GREY_A) for r in d["stirling"][1:]]).arrange(DOWN, aligned_edge=LEFT, buff=0.15)
        st.move_to([4.5, -0.8, 0])
        f = MathTex(r"\frac{1}{\sqrt{2\pi}} e^{-z^2/2}", font_size=36, color=EXACT).move_to([4.4, 0.4, 0])
        intro = label('The bell as a binomial limit', font_size=36)
        with self.voiceover(
            "The bell curve was found first as an approximation. <bookmark mark='a'/> In 1733 Abraham de Moivre, a "
            "French Protestant exile living in London and making his living as a consultant to gamblers, wanted "
            "binomial probabilities for large numbers of tosses, where the factorials are hopeless. "
            "<bookmark mark='b'/> Rescale the binomial so it's centred and has unit spread. For ten tosses, a "
            "lumpy histogram; <bookmark mark='c'/> for fifty, smoother; <bookmark mark='d'/> for two hundred, a "
            "smooth curve. <bookmark mark='e'/> De Moivre found the limit, one over root two pi, times e to the "
            "minus z squared over two, using the approximation to n factorial that we now call Stirling's formula. "
            "It's already accurate for small n. This is the first central limit theorem, proved in general in "
            "Part 6."
        ) as vo:
            self.play(FadeIn(intro))
            vo.wait_until("a")
            self.play(FadeOut(intro), run_time=0.25)
            self.play(FadeIn(hc))
            vo.wait_until("b")
            self.play(FadeIn(A), FadeIn(sets[0][1]), FadeIn(lab[0]))
            cur, cl = sets[0][1], lab[0]
            for k, m in zip((1, 2), "cd"):
                vo.wait_until(m)
                self.play(Transform(cur, sets[k][1]), Transform(cl, lab[k]), run_time=1.4)
            vo.wait_until("e")
            self.play(Create(bell), Write(f))
            self.play(FadeIn(st))
        self.clear_scene()

    def gauss(self):
        hc = history_card(1809, r"Carl Friedrich Gauss, \ \emph{Theoria motus}", r"which error law makes the "
                          r"\emph{average} of the measurements the most probable value? \ Only one: the normal",
                          color=S.MUSEUM, width=6.0, font_size=23).move_to([-3.4, 1.6, 0])
        rows = [
            cmath(r"\sum_i g'(x_i - \hat\mu) = 0", r"\ \text{ whenever }\ ", r"\sum_i (x_i - \hat\mu) = 0", font_size=32),
            cmath(r"g'(u)", r"=", r"-c\, u", font_size=36),
            cmath(r"f(u)", r"\propto", r"e^{-c u^2 / 2}", font_size=38),
        ]
        rows[2][2].set_color(EXACT)
        whys = [why(r"the mean maximizes the likelihood, \ for every data set"), why(r"so $g'$ is linear"),
                why(r"integrate $g = \log f$")]
        side = label(r"Laplace (1810) then linked it to sums: \ Part 6", font_size=22, color=GREY_B).to_edge(DOWN, buff=0.4)
        intro = label('Which error law favors the mean?', font_size=36)
        with self.voiceover(
            "The second way came from astronomy. <bookmark mark='a'/> In 1809 Carl Friedrich Gauss asked: if we "
            "average repeated measurements of a star's position, for which law of errors is the average the most "
            "probable value? <bookmark mark='b'/> Write the error density as f, and its logarithm as g. The average "
            "maximizes the likelihood for every possible data set exactly when the derivative of g balances "
            "whenever the deviations balance. <bookmark mark='c'/> That forces g prime to be linear, "
            "<bookmark mark='d'/> and integrating gives e to the minus c u squared over two: the same curve. This characterizes a smooth positive error density under independent, identically distributed errors. It "
            "does not establish those assumptions for real measurements, but it bound the normal to least squares, "
            "and Laplace soon connected both to sums of many small errors."
        ) as vo:
            self.play(FadeIn(intro))
            vo.wait_until("a")
            self.play(FadeOut(intro), run_time=0.25)
            self.play(FadeIn(hc, shift=RIGHT * 0.2))
            step = ladder(self, rows, whys, keep=3, top=0.1, x=0.4, buff=0.5, edge=6.9)
            vo.wait_until("b")
            step(0, transform=False)
            vo.wait_until("c")
            step(1, transform=False)
            vo.wait_until("d")
            step(2, transform=False)
            self.play(FadeIn(side))
        self.clear_scene()

    def herschel(self):
        d = load("normal")
        xy = np.asarray(d["xy"])
        c0 = np.array([-3.4, -0.3, 0])
        sc = 0.95
        cloud = VGroup(*[Dot(c0 + sc * np.array([x, y, 0]), radius=0.025, color=SIM) for x, y in xy])
        axes_ = VGroup(Line(c0 + LEFT * 3.2, c0 + RIGHT * 3.2, color=GREY_D), Line(c0 + DOWN * 3.2, c0 + UP * 3.2,
                                                                                    color=GREY_D))
        rot = ValueTracker(0.0)
        circle = Circle(radius=2.0 * sc, stroke_color=EXACT, stroke_width=2).move_to(c0)
        hc = history_card(1850, r"John Herschel (1850); \ James Clerk Maxwell (1860)", r"errors in two directions "
                          r"that are independent, \ with a law that does not depend on the direction", color=S.MUSEUM,
                          width=5.8, font_size=22).move_to([3.7, 2.4, 0])
        rows = VGroup(
            MathTex(r"f(x)\, f(y)", r"=", r"\phi(x^2 + y^2)", font_size=34),
            MathTex(r"\Rightarrow\ \ f(x)", r"\propto", r"e^{-c x^2}", font_size=36),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.35).move_to([3.8, 0.0, 0])
        rows[1][2].set_color(EXACT)
        wl = label(r"independence $\times$ rotation invariance: \ only the normal", font_size=22, color=GREY_B)
        wl.next_to(rows, DOWN, buff=0.3)
        maxw = label(r"Maxwell's molecular speeds come from this argument", font_size=22, color=GREY_B)
        maxw.next_to(wl, DOWN, buff=0.2)
        tag = note(r"simulated: 1,500 pairs of independent normals").to_corner(DL, buff=0.3)
        with self.voiceover(
            "The third way is the most beautiful. <bookmark mark='a'/> Throw darts at a target, or think of the "
            "velocity of a gas molecule. Suppose the errors in the two directions are independent, and their joint "
            "law looks the same in every direction: it doesn't care how you turn the axes. We assume a nondegenerate, regular density. "
            "<bookmark mark='b'/> Here's a cloud of independent normal pairs; turn it, and nothing changes. "
            "<bookmark mark='c'/> Independence says the joint density is f of x times f of y; rotation invariance "
            "says it depends only on the distance from the centre, x squared plus y squared. <bookmark mark='d'/> "
            "A product that's a function of a sum of squares: the only solutions are exponentials of x squared. "
            "John Herschel gave this argument in 1850, and James Clerk Maxwell used it ten years later to derive "
            "the distribution of molecular velocities."
        ) as vo:
            self.play(FadeIn(axes_), FadeIn(cloud, lag_ratio=0.002), FadeIn(tag))
            vo.wait_until("a")
            self.play(FadeIn(hc))
            vo.wait_until("b")
            self.play(Rotate(cloud, angle=PI / 2, about_point=c0), Create(circle), run_time=3.0)
            vo.wait_until("c")
            self.play(Write(rows[0]))
            vo.wait_until("d")
            self.play(Write(rows[1]), FadeIn(wl), FadeIn(maxw))
        _ = rot
        self.clear_scene()

    def rule(self):
        d = load("normal")
        A = axes([-4, 4], [0, 0.45], x_length=8.0, y_length=3.8, xlabel=r"standard deviations from the mean",
                 xticks=[-3, -2, -1, 0, 1, 2, 3], center=[-2.0, -0.6, 0])
        A.ax.y_axis.set_opacity(0)
        ax = A.ax
        xs = np.linspace(-4, 4, 300)
        pdf = np.exp(-xs ** 2 / 2) / np.sqrt(2 * np.pi)
        bell = curve(ax, xs, pdf, EXACT, 3)
        bands = VGroup()
        for k, op in ((3, 0.18), (2, 0.28), (1, 0.42)):
            m = np.abs(xs) <= k
            bands.add(band(ax, xs[m], np.zeros(m.sum()), pdf[m], S.ACCENT, opacity=op))
        rows = VGroup(*[MathTex(rf"\pm {k}\sigma:\ \ {100 * r:.1f}\%", r"\quad", rf"\text{{World men: }} {100 * w:.1f}\%",
                                font_size=30) for k, r, w in zip((1, 2, 3), d["rule"], d["within"])])
        rows.arrange(DOWN, aligned_edge=LEFT, buff=0.3).move_to([4.4, 1.6, 0])
        for r in rows:
            r[0].set_color(EXACT)
            r[2].set_color(SIM)
        info = MathTex(rf"{fmt_int(d['n_men'])} \text{{ men: }} \mu = {d['men_mu']:.1f},\ \sigma = {d['men_sd']:.2f}",
                       font_size=24, color=S.WORLD).move_to([4.4, 0.0, 0])
        caveat = label(r"the rule describes the normal; \ the World's incomes break it badly", font_size=22,
                       color=GREY_B)
        if caveat.width > 5.2:
            caveat.width = 5.2
        caveat.move_to([3.9, -1.0, 0])
        tag = simulated_tag()
        with self.voiceover(
            "With the constant in hand, the normal gives the most quoted numbers in statistics. "
            "<bookmark mark='a'/> Within one standard deviation of the mean lies sixty-eight point three percent of "
            "the probability; <bookmark mark='b'/> within two, ninety-five point four; <bookmark mark='c'/> within "
            "three, ninety-nine point seven. <bookmark mark='d'/> The World's men's heights are close to normal by "
            f"construction, and their actual fractions match to a tenth of a percent: {100 * d['within'][0]:.1f}, "
            f"{100 * d['within'][1]:.1f} and {100 * d['within'][2]:.1f}. But the rule is a fact about the normal, "
            "not about data: for the World's incomes it fails badly, as Part 1's heavy tails would predict."
        ) as vo:
            self.play(FadeIn(A), Create(bell), FadeIn(tag))
            for k, m in enumerate("abc"):
                vo.wait_until(m)
                self.play(FadeIn(bands[2 - k]), FadeIn(rows[k][0]))
            vo.wait_until("d")
            self.play(FadeIn(info), *[FadeIn(r[2]) for r in rows], FadeIn(caveat))
        self.clear_scene()

    def integral(self):
        rows = [
            cmath(r"I", r"=", r"\int_{-\infty}^{\infty} e^{-x^2/2}\, dx", font_size=36),
            cmath(r"I^2", r"=", r"\iint e^{-(x^2 + y^2)/2}\, dx\, dy", font_size=36),
            cmath(r"I^2", r"=", r"\int_0^{2\pi}\!\! \int_0^\infty e^{-r^2/2}\, r\, dr\, d\theta", font_size=36),
            cmath(r"I^2", r"=", r"2\pi \cdot \Big[-e^{-r^2/2}\Big]_0^\infty", r"=", r"2\pi", font_size=36),
            cmath(r"I", r"=", r"\sqrt{2\pi}", font_size=42),
        ]
        rows[4][2].set_color(EXACT)
        whys = [why(r"why $\sqrt{2\pi}$?"), why(r"two independent copies"), why(r"polar coordinates: \ $dx\,dy = r\,dr\,"
                                                                              r"d\theta$"),
                why(r"the $r$ makes it integrable"), why(r"so $\frac{1}{\sqrt{2\pi}} e^{-x^2/2}$ integrates to $1$")]
        rings = VGroup(*[Circle(radius=r, stroke_color=EXACT, stroke_width=1.5, stroke_opacity=0.9 - 0.15 * k)
                         for k, r in enumerate((0.4, 0.8, 1.2, 1.6, 2.0))]).move_to([-4.6, -1.2, 0])
        rl = label(r"the volume, in rings", font_size=22, color=GREY_B).next_to(rings, DOWN, buff=0.15)
        intro = label('The Gaussian integral', font_size=36)
        with self.voiceover(
            "One loose end: where does the root two pi come from? <bookmark mark='a'/> Call the integral of e to "
            "the minus x squared over two I. It has no formula in elementary functions. <bookmark mark='b'/> But I "
            "squared is the same integral in two variables, over the whole plane: the volume under the "
            "two-dimensional bell. <bookmark mark='c'/> Herschel's rotation invariance suggests polar coordinates. "
            "The area of a thin ring is r d r d theta, <bookmark mark='d'/> and that extra r makes the integral "
            "easy: two pi. <bookmark mark='e'/> So I is root two pi, and the normal density, with its constant, "
            "integrates to one. It's Poisson's trick, and it's one of the great one-line proofs in mathematics."
        ) as vo:
            self.play(FadeIn(intro))
            step = ladder(self, rows, whys, keep=5, top=3.2, x=0.8, buff=0.45, edge=6.9)
            for k, m in enumerate("abcde"):
                vo.wait_until(m)
                if k == 0:
                    self.play(FadeOut(intro), run_time=0.25)
                step(k, transform=k > 0)
                if m == "c":
                    self.play(Create(rings), FadeIn(rl))
        self.clear_scene()

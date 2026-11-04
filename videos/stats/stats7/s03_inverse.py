from __future__ import annotations

import numpy as np

from videos.stats.stats7.common import *  # noqa: F403


class Inverse(VoiceoverScene):
    def construct(self):
        self.card()
        self.proof()
        self.picture()
        self.histogram()
        self.discrete()
        self.empirical()
        self.limits()

    def card(self):
        card = chapter_card(2, r"The inverse CDF", r"Any distribution from one uniform", part=PART)
        with self.voiceover("Chapter two. The inverse CDF."):
            self.play(FadeIn(card[0], shift=UP * 0.2), FadeIn(card[1]))
        self.play(FadeOut(card))

    def proof(self):
        rows = [
            cmath(r"X = F^{-1}(U)", r",\quad", r"U \sim \mathrm{Uniform}(0, 1)", font_size=36),
            cmath(r"P(X \le x)", r"=", r"P\big(F^{-1}(U) \le x\big)", r"=", r"P\big(U \le F(x)\big)", r"=", r"F(x)", font_size=34),
            cmath(r"F^{-1}(u)", r"=", r"\inf\{x : F(x) \ge u\}", font_size=34),
        ]
        rows[1][6].set_color(EXACT)
        whys = [why(r"Part 3's probability integral transform, \ run backwards"),
                why(r"$F$ is increasing, \ so $F^{-1}(u) \le x \iff u \le F(x)$; \ and $P(U \le t) = t$"),
                why(r"the generalized inverse: \ it works for jumps and flat stretches too")]
        with self.voiceover(
            "With a good source of uniform numbers, how do we get any other distribution? The first answer is "
            "Part 3's probability integral transform, run backwards. <bookmark mark='a'/> Take a uniform U and "
            "apply the inverse of the CDF you want. <bookmark mark='b'/> The chance that the result is at most x is "
            "the chance that U is at most F of x, because F is increasing. And for a uniform, that chance is just F "
            "of x. So X has CDF F, exactly. <bookmark mark='c'/> For CDFs with jumps or flat stretches, use the "
            "generalized inverse: the smallest x at which F reaches u. The proof is the same."
        ) as vo:
            step = ladder(self, rows, whys, keep=3, top=2.6, x=-0.6, buff=0.95, edge=6.9)
            for k, m in enumerate("abc"):
                vo.wait_until(m)
                step(k, transform=False)
        self.clear_scene()

    def picture(self):
        d = load("inverse")
        u, x = np.asarray(d["u"]), np.asarray(d["x"])
        A = axes([0, 5], [0, 1.05], x_length=7.6, y_length=4.6, xlabel=r"$x$", ylabel=r"$F(x) = 1 - e^{-x}$", xticks=[0, 1, 2, 3, 4, 5],
                 yticks=[0, 0.5, 1], center=[-1.8, -0.4, 0])
        ax = A.ax
        xs = np.linspace(0, 5, 200)
        F = curve(ax, xs, 1 - np.exp(-xs), EXACT, 3.5)
        inv = MathTex(r"F^{-1}(u) = -\log(1 - u)", font_size=32, color=EXACT).move_to([4.6, 2.2, 0])
        darts = []
        for k in range(10):
            uu, xx = float(u[k]), float(min(x[k], 5))
            h = Line(ax.c2p(0, uu), ax.c2p(xx, uu), color=GOOD, stroke_width=2)
            v = Line(ax.c2p(xx, uu), ax.c2p(xx, 0), color=GOOD, stroke_width=2)
            du = Dot(ax.c2p(0, uu), radius=0.06, color=GOOD)
            dx = Dot(ax.c2p(xx, 0), radius=0.06, color=S.POST)
            darts.append((du, h, v, dx))
        rows = fit_rows(VGroup(label(r"a uniform $u$ on the vertical axis", font_size=24, color=GOOD),
                               label(r"across to the curve, \ down to $x$", font_size=24),
                               label(r"steep parts of $F$ \ (high density) \ catch many $u$'s", font_size=24, color=S.POST)),
                        4.6, 0.25, [4.6, 0.6, 0])
        with self.voiceover(
            "Here it is for the exponential distribution, whose CDF is one minus e to the minus x. "
            "<bookmark mark='a'/> Its inverse is minus the log of one minus u. <bookmark mark='b'/> Draw a uniform u "
            "and mark it on the vertical axis. Go across to the curve and down: that's the draw. "
            "<bookmark mark='c'/> Ten draws. Where the curve is steep, which is where the density is high, a band "
            "of u's maps to a narrow band of x's, so draws pile up there. Where it's flat, in the tail, the same "
            "band of u's spreads out across a wide range of x."
        ) as vo:
            self.play(FadeIn(A), Create(F))
            vo.wait_until("a")
            self.play(FadeIn(inv))
            vo.wait_until("b")
            du, h, v, dx = darts[0]
            self.play(FadeIn(du), FadeIn(rows[0]))
            self.play(Create(h), FadeIn(rows[1]))
            self.play(Create(v), FadeIn(dx))
            vo.wait_until("c")
            for du, h, v, dx in darts[1:]:
                self.play(FadeIn(du), Create(h), Create(v), FadeIn(dx), run_time=0.5)
            self.play(FadeIn(rows[2]))
        self.clear_scene()

    def histogram(self):
        d = load("inverse")
        ed = np.asarray(d["edges"])
        A = axes([0, 6], [0, 1.05], x_length=7.4, y_length=4.2, xlabel=r"$x = -\log(1 - U)$", xticks=[0, 2, 4, 6], yticks=[0, 0.5, 1],
                 center=[-1.8, -0.5, 0])
        h = hist_bars(A.ax, ed, np.asarray(d["hist"]), color=GOOD, opacity=0.75)
        xs = np.linspace(0, 6, 200)
        cv = curve(A.ax, xs, np.exp(-xs), EXACT, 3)
        rows = fit_rows(VGroup(label(r"4,000 draws, \ each from one PCG32 uniform", font_size=24, color=GOOD),
                               label(r"gold: \ the density $e^{-x}$", font_size=24, color=EXACT),
                               label(r"one uniform in, \ one draw out: \ the cheapest possible sampler", font_size=24, color=GREY_A)),
                        4.8, 0.3, [4.4, 0.8, 0])
        with self.voiceover(
            "<bookmark mark='a'/> Four thousand draws this way, each using a single uniform from our PCG generator. "
            "<bookmark mark='b'/> The histogram follows the exponential density exactly. <bookmark mark='c'/> One "
            "uniform in, one draw out: when the inverse CDF has a formula, nothing is cheaper. The same trick turns "
            "uniforms into Cauchys, with the tangent function; into Paretos, with a power; into Weibulls and "
            "logistics."
        ) as vo:
            self.play(FadeIn(A))
            vo.wait_until("a")
            self.play(FadeIn(h, lag_ratio=0.03), FadeIn(rows[0]))
            vo.wait_until("b")
            self.play(Create(cv), FadeIn(rows[1]))
            vo.wait_until("c")
            self.play(FadeIn(rows[2]))
        self.clear_scene()

    def discrete(self):
        d = load("inverse")
        pmf, cdf, freq = np.asarray(d["pmf"]), np.asarray(d["cdf"]), np.asarray(d["freq"])
        x0, x1, y = -5.5, 5.5, 1.3
        segs = VGroup()
        cols = [S.EST, S.LIK, S.POST, S.PRIOR, S.ACCENT]
        lo = 0.0
        for k, (p, c) in enumerate(zip(pmf, cols)):
            a, b = x0 + lo * (x1 - x0), x0 + (lo + p) * (x1 - x0)
            segs.add(VGroup(Rectangle(width=b - a, height=0.6, stroke_color=BLACK, stroke_width=2, fill_color=c, fill_opacity=0.75)
                            .move_to([(a + b) / 2, y, 0]), MathTex(rf"X = {k}", font_size=24).move_to([(a + b) / 2, y, 0])))
            lo += p
        ticks = VGroup(*[MathTex(f"{v:.2f}".rstrip("0").rstrip("."), font_size=20, color=GREY_B).next_to([x0 + v * (x1 - x0), y - 0.3, 0], DOWN,
                                                                                                buff=0.1) for v in [0, *cdf]])
        lab = label(r"the unit interval, \ cut at the CDF: \ $0.1,\ 0.35,\ 0.65,\ 0.85,\ 1$", font_size=24).next_to(segs, UP, buff=0.4)
        A = axes([-0.6, 4.6], [0, 0.35], x_length=6.0, y_length=2.6, xticks=[0, 1, 2, 3, 4], yticks=[0, 0.1, 0.2, 0.3],
                 center=[-2.6, -2.0, 0])
        b1 = bars(A.ax, np.arange(5) - 0.18, pmf, EXACT, width=0.34)
        b2 = bars(A.ax, np.arange(5) + 0.18, freq, GOOD, width=0.34)
        leg = legend([(EXACT, r"$P(X = k)$"), (GOOD, r"2,000 draws")], font_size=22).move_to([2.6, -1.6, 0])
        cost = label(r"cost: \ a search through the CDF, \ up to $k$ steps per draw", font_size=22, color=GREY_A).move_to([3.4, -2.6, 0])
        with self.voiceover(
            "Inversion works for discrete laws too. <bookmark mark='a'/> Lay the probabilities end to end along the "
            "unit interval: a tenth for zero, a quarter for one, and so on. The cut points are the CDF. "
            "<bookmark mark='b'/> Draw a uniform and see which piece it lands in. <bookmark mark='c'/> Two thousand "
            "draws reproduce the probabilities. <bookmark mark='d'/> The only cost is the search for the right "
            "piece, which for a law with many values can take many steps. Chapter four's alias method removes it."
        ) as vo:
            vo.wait_until("a")
            self.play(LaggedStart(*[FadeIn(s_) for s_ in segs], lag_ratio=0.2), FadeIn(ticks), FadeIn(lab))
            vo.wait_until("b")
            g = np.random.Generator(np.random.PCG64(4))
            for uu in g.random(6):
                arrow = Arrow([x0 + uu * (x1 - x0), y + 1.0, 0], [x0 + uu * (x1 - x0), y + 0.32, 0], buff=0, color=WHITE,
                              stroke_width=3, max_tip_length_to_length_ratio=0.3)
                self.play(GrowArrow(arrow), run_time=0.35)
                self.play(FadeOut(arrow), run_time=0.2)
            vo.wait_until("c")
            self.play(FadeIn(A), FadeIn(b1), FadeIn(b2), FadeIn(leg))
            vo.wait_until("d")
            self.play(FadeIn(cost))
        self.clear_scene()

    def limits(self):
        rows = fit_rows(VGroup(
            label(r"inversion needs $F^{-1}$ in a usable form", font_size=28),
            MathTex(r"\text{normal: } \Phi^{-1}(u) \text{ has no closed form}", font_size=30, color=BAD),
            label(r"it can be computed (Wichura's algorithm AS 241, 1988, to 16 digits), \ but slowly", font_size=24, color=GREY_A),
            MathTex(r"\text{gamma, beta: } F \text{ itself has no closed form}", font_size=30, color=BAD),
            label(r"so: \ samplers that never invert anything \ (chapters 3 and 4)", font_size=26, color=S.ACCENT),
        ), 12.4, 0.35, [0, 0.3, 0])
        with self.voiceover(
            "Inversion has one requirement: an inverse CDF you can compute. <bookmark mark='a'/> The normal's "
            "inverse CDF has no closed form. It can be computed to sixteen digits, with a rational approximation "
            "like Michael Wichura's algorithm of 1988, but every draw then costs a careful numerical evaluation. "
            "<bookmark mark='b'/> For the gamma and the beta, even the CDF itself has no formula. "
            "<bookmark mark='c'/> So we need samplers that never invert anything. The next two chapters build them."
        ) as vo:
            self.play(FadeIn(rows[0]))
            vo.wait_until("a")
            self.play(FadeIn(rows[1:3]))
            vo.wait_until("b")
            self.play(FadeIn(rows[3]))
            vo.wait_until("c")
            self.play(FadeIn(rows[4]))
        self.clear_scene()

    def empirical(self):
        data = np.array([3.1, 4.7, 5.2, 6.0, 8.4])
        A = axes([2, 9.5], [0, 1.05], x_length=7.0, y_length=4.2, xlabel=r"$x$", ylabel=r"$\hat F_n(x)$", xticks=[3, 5, 7, 9],
                 yticks=[0, 0.2, 0.4, 0.6, 0.8, 1], center=[-2.4, -0.4, 0])
        ax = A.ax
        steps = VGroup()
        for i, v in enumerate(data):
            nxt_ = data[i + 1] if i + 1 < len(data) else 9.5
            steps.add(Line(ax.c2p(v, (i + 1) / 5), ax.c2p(nxt_, (i + 1) / 5), color=GOOD, stroke_width=3))
        steps.add(Line(ax.c2p(2, 0), ax.c2p(data[0], 0), color=GOOD, stroke_width=3))
        dots = VGroup(*[Dot(ax.c2p(v, 0), radius=0.07, color=WHITE) for v in data])
        g = np.random.Generator(np.random.PCG64(16))
        us = g.random(5)
        picks = np.searchsorted(np.arange(1, 6) / 5, us, side="left")
        arrows = VGroup(*[VGroup(DashedLine(ax.c2p(2, u), ax.c2p(data[k], u), color=S.POST, stroke_width=1.5),
                                 DashedLine(ax.c2p(data[k], u), ax.c2p(data[k], 0), color=S.POST, stroke_width=1.5))
                          for u, k in zip(us, picks)])
        rows = fit_rows(VGroup(
            label(r"invert the \emph{empirical} CDF of a sample", font_size=24),
            label(r"each $u$ lands on one observation, \ each with chance $1/n$", font_size=24),
            label(r"= drawing from the data \emph{with replacement}", font_size=24, color=S.POST),
            MathTex(r"\text{resample: } " + ",\\ ".join(f"{data[k]:.1f}" for k in picks), font_size=26, color=S.POST),
            label(r"the bootstrap (Efron 1979): \ Part 16", font_size=24, color=S.ACCENT),
        ), 5.0, 0.28, [4.3, 0.4, 0])
        with self.voiceover(
            "Inversion has one more use, and it's a famous one. <bookmark mark='a'/> Take a sample of five numbers and "
            "its empirical CDF from Part 1: a staircase climbing a fifth at each observation. <bookmark mark='b'/> "
            "Invert it. A uniform u lands on one step, and so picks one observation, each with chance one fifth. "
            "<bookmark mark='c'/> Five uniforms give five picks, with repeats: a sample drawn from the data with "
            "replacement. That's a resample, and simulating many of them is Bradley Efron's bootstrap of 1979, which "
            "Part 16 builds into a way of computing standard errors for almost anything."
        ) as vo:
            self.play(FadeIn(A), FadeIn(dots))
            vo.wait_until("a")
            self.play(Create(steps), FadeIn(rows[0]))
            vo.wait_until("b")
            self.play(Create(arrows[0]), FadeIn(rows[1]))
            vo.wait_until("c")
            self.play(LaggedStart(*[Create(a) for a in arrows[1:]], lag_ratio=0.3), FadeIn(rows[2:]))
        self.clear_scene()

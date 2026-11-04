from __future__ import annotations

import numpy as np

from videos.stats.stats7.common import *  # noqa: F403


class MonteCarlo(VoiceoverScene):
    def construct(self):
        self.card()
        self.darts()
        self.rate()
        self.dimension()
        self.quasi()
        self.buffon()
        self.lazzarini()

    def card(self):
        card = chapter_card(5, r"Monte Carlo integration", r"Integrals as averages", lit=(1777,), part=PART)
        with self.voiceover("Chapter five. Monte Carlo integration."):
            self.play(FadeIn(card[0], shift=UP * 0.2), FadeIn(card[1]))
        self.play(FadeOut(card))

    def darts(self):
        d = load("montecarlo")
        x, y, ins = np.asarray(d["x"]), np.asarray(d["y"]), np.asarray(d["inside"]).astype(bool)
        A = axes([0, 1], [0, 1], x_length=4.6, y_length=4.6, xticks=[0, 1], yticks=[0, 1], center=[-4.0, -0.4, 0])
        ax = A.ax
        arc = ParametricFunction(lambda t: ax.c2p(np.cos(t), np.sin(t)), t_range=[0, PI / 2], color=EXACT, stroke_width=3)
        dots = VGroup(*[Dot(ax.c2p(a, b), radius=0.02, color=ACC if i else REJ, fill_opacity=0.8) for a, b, i in zip(x, y, ins)])
        n = np.asarray(d["est_n"], float)
        est = np.asarray(d["est"])
        B = axes([1, 4000], [2.8, 3.5], x_length=5.6, y_length=3.6, xlabel=r"darts", ylabel=r"$4 \times$ share inside",
                 xticks=[1000, 2000, 3000, 4000], yticks=[2.8, 3.0, 3.2, 3.4], center=[2.9, -0.6, 0])
        pi_l = DashedLine(B.ax.c2p(1, np.pi), B.ax.c2p(4000, np.pi), color=EXACT, stroke_width=2)
        sd = 4 * np.sqrt(np.pi / 4 * (1 - np.pi / 4))
        nn = np.linspace(20, 4000, 200)
        hi = curve(B.ax, nn, np.minimum(np.pi + 2 * sd / np.sqrt(nn), 3.5), GREY_B, 1.5)
        lo = curve(B.ax, nn, np.maximum(np.pi - 2 * sd / np.sqrt(nn), 2.8), GREY_B, 1.5)
        path = polyline(B.ax, n[n >= 20], np.clip(est[n >= 20], 2.8, 3.5), GOOD, 2.5)
        f = MathTex(r"\pi = 4\,P(U_1^2 + U_2^2 \le 1) = 4\int\!\!\int \mathbf 1\{u_1^2 + u_2^2 \le 1\}\,du_1 du_2", font_size=28)
        f.to_edge(UP, buff=0.4)
        res = MathTex(rf"4{{,}}000 \text{{ darts: }} {est[-1]:.3f}", font_size=28, color=GOOD).next_to(B, UP, buff=0.1).align_to(B, RIGHT)
        with self.voiceover(
            "Every expectation is an integral, and every integral is an expectation. That's the whole idea of Monte "
            "Carlo, the name Stanislaw Ulam, John von Neumann and Nicholas Metropolis used at Los Alamos, after the casino. "
            "<bookmark mark='a'/> Pi is four times the chance that a uniform point in the unit square lands inside "
            "the quarter circle. <bookmark mark='b'/> So throw darts and count. <bookmark mark='c'/> The running "
            "estimate wanders, then settles, inside the funnel of two standard errors from Part 6. After four "
            "thousand darts it's three point one six: two correct digits. To get a third you need a hundred times "
            "as many."
        ) as vo:
            self.play(FadeIn(A), Create(arc))
            vo.wait_until("a")
            self.play(FadeIn(f))
            vo.wait_until("b")
            self.play(LaggedStart(*[FadeIn(p) for p in dots], lag_ratio=0.002), run_time=3.0)
            vo.wait_until("c")
            self.play(FadeIn(B), Create(pi_l), Create(hi), Create(lo))
            self.play(Create(path), run_time=3.0)
            self.play(FadeIn(res))
        self.clear_scene()

    def rate(self):
        rows = [
            cmath(r"I = \int g(\mathbf x)\, f(\mathbf x)\, d\mathbf x", r"=", r"E\,g(\mathbf X)", r",\quad \mathbf X \sim f", font_size=32),
            cmath(r"\hat I_n", r"=", r"\frac1n \sum_{i=1}^n g(\mathbf X_i)", font_size=32),
            cmath(r"\mathrm{sd}(\hat I_n)", r"=", r"\frac{\sigma_g}{\sqrt n}", r",\qquad", r"\hat\sigma_g \text{ from the same draws}",
                  font_size=32),
        ]
        rows[2][2].set_color(S.ACCENT)
        whys = [why(r"an integral, \ read as an expectation"), why(r"the weak law: \ consistent (Part 6)"),
                why(r"the CLT gives the error bar, \ and the dimension of $\mathbf x$ appears nowhere")]
        with self.voiceover(
            "In general: <bookmark mark='a'/> an integral of g against a density f is the expectation of g of X, "
            "with X drawn from f. <bookmark mark='b'/> Estimate it by averaging g over n draws; Part 6's weak law "
            "makes the average converge. <bookmark mark='c'/> And the central limit theorem gives the error: sigma "
            "over root n, where sigma, estimated from the same draws, is the spread of g. Look at what's missing "
            "from that formula: the dimension. The error falls like one over root n whether x has one coordinate "
            "or a thousand."
        ) as vo:
            step = ladder(self, rows, whys, keep=3, top=2.6, x=-0.6, buff=0.95, edge=6.9)
            for k, m in enumerate("abc"):
                vo.wait_until(m)
                step(k, transform=False)
        self.clear_scene()

    def dimension(self):
        d = load("montecarlo")
        b = d["ball"]
        ds = np.asarray(b["d"])
        mc = np.log10(np.maximum(np.asarray(b["mc_err"]), 1e-5))
        gr = np.log10(np.maximum(np.asarray(b["grid_err"]), 1e-5))
        A = axes([0.5, 10.5], [-5, 0], x_length=7.0, y_length=4.4, xlabel=r"dimension $d$",
                 ylabel=r"relative error, \ volume of the $d$-ball (log scale)", xticks=[1, 2, 4, 6, 8, 10],
                 yticks=[-5, -4, -3, -2, -1, 0], yfmt=lambda v: f"10^{{{int(v)}}}", center=[-2.2, -0.4, 0])
        ax = A.ax
        l1 = VGroup(polyline(ax, ds[1:], mc[1:], GOOD, 3), *[Dot(ax.c2p(a, v), radius=0.06, color=GOOD) for a, v in zip(ds[1:], mc[1:])])
        l2 = VGroup(polyline(ax, ds[1:], gr[1:], BAD, 3), *[Dot(ax.c2p(a, v), radius=0.06, color=BAD) for a, v in zip(ds[1:], gr[1:])])
        leg = legend([(BAD, r"a grid of $10^6$ points"), (GOOD, r"$10^6$ random points")], font_size=22).move_to([4.3, 1.8, 0])
        rows = fit_rows(VGroup(
            label(r"a grid of $N$ points has $N^{1/d}$ per side: \ in 10 dimensions, \ 4", font_size=24),
            label(r"Monte Carlo's error: \ $\sigma/\sqrt N$, \ in any dimension", font_size=24, color=GOOD),
            label(r"why Bayesian computation, physics and finance simulate", font_size=22, color=GREY_A),
        ), 5.0, 0.3, [4.3, -0.6, 0])
        with self.voiceover(
            "Here's why that matters. <bookmark mark='a'/> Estimate the volume of a ball in d dimensions with a "
            "budget of a million points. A grid in d dimensions has only the d-th root of a million points per "
            "side: a thousand in two dimensions, but ten in six and four in ten. Its error explodes. "
            "<bookmark mark='b'/> A million random points do far better: their error grows a little with d, because "
            "the ball becomes a smaller and smaller target inside the cube, but the rate stays one over root N. "
            "<bookmark mark='c'/> In one dimension, the grid wins easily. In ten, it isn't close. That's why "
            "high-dimensional integrals, in Bayesian statistics, physics and finance, are done by simulation."
        ) as vo:
            self.play(FadeIn(A))
            vo.wait_until("a")
            self.play(Create(l2), FadeIn(leg[0]), FadeIn(rows[0]))
            vo.wait_until("b")
            self.play(Create(l1), FadeIn(leg[1]), FadeIn(rows[1]))
            vo.wait_until("c")
            self.play(FadeIn(rows[2]))
        self.clear_scene()

    def buffon(self):
        g = np.random.Generator(np.random.PCG64(1777))
        t, l = 1.0, 5 / 6
        sc = 1.1
        lines = VGroup(*[Line([-6.0, (k - 2) * sc * t - 0.4, 0], [1.0, (k - 2) * sc * t - 0.4, 0], color=GREY_C, stroke_width=2)
                         for k in range(5)])
        needles = VGroup()
        for _ in range(60):
            cx, cy, th = g.uniform(-5.5, 0.5), g.uniform(-2.4 - 0.4, 2.0 - 0.4), g.uniform(0, PI)
            dx, dy = 0.5 * l * sc * np.cos(th), 0.5 * l * sc * np.sin(th)
            y1, y2 = cy - dy, cy + dy
            k1, k2 = np.floor((y1 + 0.4) / (sc * t)), np.floor((y2 + 0.4) / (sc * t))
            needles.add(Line([cx - dx, y1, 0], [cx + dx, y2, 0], color=ACC if k1 != k2 else GREY_A, stroke_width=3))
        hc = history_card(1777, r"Georges-Louis Leclerc, \ Comte de Buffon", r"\emph{Essai d'arithm\'etique morale}: \ drop a "
                          r"needle on ruled floorboards; \ how often does it cross a line?", color=S.MUSEUM, width=5.2,
                          font_size=20).move_to([4.4, 2.0, 0])
        rows = fit_rows(VGroup(
            MathTex(r"P(\text{cross}) = \frac{2\ell}{\pi t}", font_size=34, color=EXACT),
            label(r"needle $\ell$, \ lines $t$ apart \ ($\ell \le t$)", font_size=22, color=GREY_A),
            MathTex(r"\hat\pi = \frac{2\ell\, n}{t \cdot \text{crossings}}", font_size=32),
        ), 4.6, 0.3, [4.4, -0.8, 0])
        with self.voiceover(
            "The oldest Monte Carlo experiment is two centuries older than the name. <bookmark mark='a'/> In 1777 "
            "Georges-Louis Leclerc, Comte de Buffon, asked: drop a needle on a floor of parallel boards; how often "
            "does it cross a line? <bookmark mark='b'/> If the needle is no longer than the spacing, the chance is "
            "two times its length over pi times the spacing. Pi appears because the needle's angle is uniform. "
            "<bookmark mark='c'/> So counting crossings estimates pi. In the nineteenth century, people actually "
            "did it, by hand, thousands of times."
        ) as vo:
            self.play(FadeIn(lines))
            vo.wait_until("a")
            self.play(FadeIn(hc), LaggedStart(*[FadeIn(nd) for nd in needles], lag_ratio=0.05), run_time=3.0)
            vo.wait_until("b")
            self.play(FadeIn(rows[:2]))
            vo.wait_until("c")
            self.play(FadeIn(rows[2]))
        self.clear_scene()

    def lazzarini(self):
        d = load("montecarlo")
        rows = fit_rows(VGroup(
            label(r"Mario Lazzarini (1901): \ $\ell = \tfrac56 t$, \ $n = 3{,}408$ throws, \ $1{,}808$ crossings", font_size=26),
            MathTex(r"\hat\pi = \frac{2 \cdot \tfrac56 \cdot 3408}{1808} = \frac{355}{113} = 3.1415929\ldots", font_size=32, color=BAD),
            label(r"correct to six decimal places", font_size=24, color=BAD),
            MathTex(rf"\text{{but the standard error of 3,408 throws is }} {d['buffon_sd']:.3f}", font_size=28, color=GOOD),
            label(r"$355/113$ is a famous approximation, \ and with $\ell = \tfrac56 t$ it needs $n$ a multiple of 213: \ $3{,}408 = 16 \times 213$", font_size=22,
                  color=GREY_A),
            label(r"the lesson: \ a simulation is only as honest as its stopping rule, \ and its error bar", font_size=26,
                  color=S.ACCENT),
        ), 12.6, 0.3, [0, 0.2, 0])
        with self.voiceover(
            "And one of them is a cautionary tale. <bookmark mark='a'/> In 1901 the Italian mathematician Mario "
            "Lazzarini reported three thousand four hundred and eight throws of a needle five sixths as long as the "
            "spacing, with one thousand eight hundred and eight crossings. <bookmark mark='b'/> That gives three "
            "hundred and fifty-five over a hundred and thirteen: pi correct to six decimal places. "
            "<bookmark mark='c'/> Too correct. The standard error of an experiment that size is about point oh five: "
            "you'd expect the second decimal place to be wrong. <bookmark mark='d'/> Three fifty-five over one "
            "thirteen is a famous fraction for pi, and with that needle it can only come out when the number of throws is a multiple of two hundred and thirteen. Three thousand four hundred and eight is sixteen times two hundred and thirteen. Historians suspect he stopped, or chose his count, when the answer looked best. "
            "<bookmark mark='e'/> The lesson for every simulation in this course: report the error bar, and decide "
            "in advance when to stop."
        ) as vo:
            vo.wait_until("a")
            self.play(FadeIn(rows[0]))
            vo.wait_until("b")
            self.play(FadeIn(rows[1:3]))
            vo.wait_until("c")
            self.play(FadeIn(rows[3]))
            vo.wait_until("d")
            self.play(FadeIn(rows[4]))
            vo.wait_until("e")
            self.play(FadeIn(rows[5]))
        self.clear_scene()

    def quasi(self):
        def vdc(i, b):
            x, f = 0.0, 1.0 / b
            while i:
                i, r = divmod(i, b)
                x += r * f
                f /= b
            return x
        n = 400
        H = np.array([[vdc(i, 2), vdc(i, 3)] for i in range(1, n + 1)])
        R = np.random.Generator(np.random.PCG64(1967)).random((n, 2))
        A = axes([0, 1], [0, 1], x_length=3.7, y_length=3.7, xticks=[0, 1], yticks=[0, 1], center=[-4.9, -0.2, 0])
        B = axes([0, 1], [0, 1], x_length=3.7, y_length=3.7, xticks=[0, 1], yticks=[0, 1], center=[-0.8, -0.2, 0])
        pr = VGroup(*[Dot(A.ax.c2p(a, b), radius=0.03, color=GOOD) for a, b in R])
        ph = VGroup(*[Dot(B.ax.c2p(a, b), radius=0.03, color=S.ACCENT) for a, b in H])
        t1 = label(r"400 random points: \ clumps and gaps", font_size=22, color=GOOD).next_to(A, UP, buff=0.15)
        t2 = label(r"400 Halton points (bases 2, 3)", font_size=22, color=S.ACCENT).next_to(B, UP, buff=0.15)
        rows = fit_rows(VGroup(
            label(r"quasi-Monte Carlo:", font_size=24),
            label(r"points spread deliberately evenly", font_size=24),
            MathTex(r"\text{error} \approx \frac{(\log n)^d}{n} \ \text{vs}\ \frac{\sigma}{\sqrt n}", font_size=26, color=S.ACCENT),
            label(r"Halton (1960), \ Sobol' (1967)", font_size=20, color=GREY_A),
            label(r"wins for smooth integrands, \ moderate $d$", font_size=22, color=GREY_A),
            label(r"randomized to get error bars", font_size=22, color=GREY_A),
        ), 4.6, 0.26, [4.2, -0.2, 0])
        with self.voiceover(
            "Random points have a flaw for integration: by chance, they clump and leave gaps. "
            "<bookmark mark='a'/> Here are four hundred random points in the square. <bookmark mark='b'/> And four "
            "hundred points of the Halton sequence, which writes the index in base two and in base three and reverses "
            "the digits: they fill the square deliberately evenly. <bookmark mark='c'/> Integrating with such "
            "low-discrepancy points, quasi-Monte Carlo, can make the error fall almost like one over n instead of one "
            "over root n, for smooth integrands in moderate dimension. The price is that the error bar must be "
            "recovered by randomizing the points, as finance practitioners do every day."
        ) as vo:
            vo.wait_until("a")
            self.play(FadeIn(A), FadeIn(t1), FadeIn(pr, lag_ratio=0.003))
            vo.wait_until("b")
            self.play(FadeIn(B), FadeIn(t2), FadeIn(ph, lag_ratio=0.003))
            vo.wait_until("c")
            self.play(FadeIn(rows))
        self.clear_scene()

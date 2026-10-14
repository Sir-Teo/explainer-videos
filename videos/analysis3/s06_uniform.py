from __future__ import annotations

import math

import numpy as np

from explainer.analysis import *  # noqa: F403
from videos.analysis3.common import load, plain_axes, polyline


class Uniform(VoiceoverScene):
    def construct(self):
        self.card()
        self.game()
        self.dashboard()
        self.cauchy()
        self.mtest()

    # ------------------------------------------------------------------
    def card(self):
        card = chapter_card(5, r"Uniform convergence", r"When does a sequence of functions converge all at once?",
                            lit=(), part=3)
        with self.voiceover(
            "Chapter five. The swaps in the opening failed because the functions converged at each point, but at "
            "different speeds at different points. The cure is to ask for one speed everywhere."
        ):
            self.play(FadeIn(card[0], shift=UP * 0.2), FadeIn(card[1]))
        self.play(FadeOut(card))

    # ------------------------------------------------------------------
    def game(self):
        dfn = VGroup(
            MathTex(r"\text{pointwise:}", r"\quad \forall x\ \forall \varepsilon\ \exists N", r":\ n \ge N \Rightarrow "
                    r"|f_n(x) - f(x)| < \varepsilon", font_size=32),
            MathTex(r"\text{uniform:}", r"\quad \forall \varepsilon\ \exists N\ \forall x", r":\ n \ge N \Rightarrow "
                    r"|f_n(x) - f(x)| < \varepsilon", font_size=32),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.25)
        head = label(r"Pointwise or uniform: \ when is $N$ chosen?", font_size=34).to_edge(UP, buff=0.3)
        dfn.next_to(head, DOWN, buff=0.3)
        dfn[0][1].set_color(C.DELTA)
        dfn[1][1].set_color(C.EPS)
        ref = note(r"Rudin 7.7: \ $N$ is chosen before $x$").next_to(dfn, DOWN, buff=0.1).align_to(dfn, RIGHT)
        eps = 0.1
        N_ok = math.ceil(math.log(eps) / math.log(0.9))
        assert 0.9**N_ok < eps <= 0.9 ** (N_ok - 1)
        x = np.linspace(0, 1, 800)
        ax1 = plain_axes([0, 1, 0.25], [-0.15, 1.05, 0.5], 5.6, 3.7).move_to([-3.4, -1.15, 0])
        ax2 = plain_axes([0, 1, 0.25], [-0.15, 1.05, 0.5], 5.6, 3.7).move_to([3.4, -1.15, 0])
        n1, n2 = ValueTracker(1.0), ValueTracker(1.0)
        band1 = Rectangle(width=ax1.c2p(0.9, 0)[0] - ax1.c2p(0, 0)[0], height=ax1.c2p(0, eps)[1] - ax1.c2p(0, -eps)[1],
                          stroke_width=0, fill_color=C.EPS, fill_opacity=0.2).move_to(ax1.c2p(0.45, 0))
        band2 = Rectangle(width=ax2.c2p(1, 0)[0] - ax2.c2p(0, 0)[0], height=ax2.c2p(0, eps)[1] - ax2.c2p(0, -eps)[1],
                          stroke_width=0, fill_color=C.EPS, fill_opacity=0.2).move_to(ax2.c2p(0.5, 0))
        x1 = x[x <= 0.9]
        g1 = always_redraw(lambda: polyline(ax1, x1, x1 ** n1.get_value(), color=C.FUNC, stroke_width=3.5))
        x2 = x[x < 1]
        g2 = always_redraw(lambda: polyline(ax2, x2, x2 ** n2.get_value(), color=C.FUNC, stroke_width=3.5))
        t1 = MathTex(r"x^n \text{ on } [0, 0.9]", font_size=30).next_to(ax1, UP, buff=0.1)
        t2 = MathTex(r"x^n \text{ on } [0, 1)", font_size=30).next_to(ax2, UP, buff=0.1)
        lab1 = always_redraw(lambda: MathTex(rf"n = {round(n1.get_value())}:\ \sup = 0.9^n = {0.9 ** round(n1.get_value()):.3f}",
                                             font_size=26, color=C.EPS).next_to(ax1, DOWN, buff=0.15))
        lab2 = always_redraw(lambda: MathTex(rf"n = {round(n2.get_value())}:\ \sup = 1", font_size=26,
                                             color=C.PATHOLOGY).next_to(ax2, DOWN, buff=0.15))
        with self.voiceover(
            "Put the two definitions side by side as games. <bookmark mark='p'/> Pointwise convergence: for each x and "
            "each epsilon there's an N, and N may depend on x. <bookmark mark='u'/> Uniform convergence: for each "
            "epsilon, one N that works for every x at once. Only the order of the quantifiers changed. "
            "<bookmark mark='a'/> Picture it as a band of half-width epsilon around the limit: uniform convergence "
            "means that from some N on, the entire graph lies inside the band. <bookmark mark='b'/> On the interval "
            "from zero to 0.9, x to the n does this: its largest value is 0.9 to the n, and with epsilon a tenth, N "
            f"equal to {N_ok} works everywhere. <bookmark mark='c'/> On the interval from zero up to, but not including, "
            "one, it never does: for every n, the graph climbs to near one before the end, outside any band."
        ) as vo:
            self.play(FadeIn(head), Create(ax1), Create(ax2), FadeIn(t1), FadeIn(t2), Create(g1), Create(g2), FadeIn(lab1),
                      FadeIn(lab2))
            vo.wait_until("p")
            self.play(FadeIn(dfn[0]))
            self.play(n1.animate.set_value(4), n2.animate.set_value(4), run_time=2.5, rate_func=linear)
            vo.wait_until("u")
            self.play(FadeIn(dfn[1]), FadeIn(ref))
            vo.wait_until("a")
            self.play(FadeIn(band1), FadeIn(band2))
            vo.wait_until("b")
            self.play(n1.animate.set_value(N_ok), run_time=3.0, rate_func=linear)
            vo.wait_until("c")
            self.play(n2.animate.set_value(60), run_time=3.0, rate_func=linear)
        for m in (g1, g2, lab1, lab2):
            m.clear_updaters()
        self.wait(0.3)
        self.clear_scene()

    # ------------------------------------------------------------------
    def dashboard(self):
        ax = plain_axes([0, 1, 0.25], [-0.1, 1.1, 0.5], 6.6, 4.6).move_to([-3.0, -0.5, 0])
        dash = Dashboard(ax, lambda n, x: x**n, lambda x: np.where(x >= 1, 1.0, 0.0), n=1.0, x0=0.8,
                         lenses=("point", "sup", "L1", "L2"), sup_domain=(0, 0.999999),
                         exact={"sup": lambda n: 1.0, "L1": lambda n: 1 / (n + 1), "L2": lambda n: 1 / math.sqrt(2 * n + 1)})
        g = dash.graph()
        tube = dash.tube(opacity=0.11)
        area = dash.area()
        probe = dash.probe()
        lim = VGroup(Line(ax.c2p(0, 0), ax.c2p(0.985, 0), color=WHITE, stroke_width=3),
                     Circle(radius=0.06, color=WHITE, stroke_width=2.5).set_fill(BACKGROUND, 1).move_to(ax.c2p(1, 0)),
                     Dot(ax.c2p(1, 1), radius=0.07, color=WHITE))
        panel = dash.panel(font_size=26, width=4.8).move_to([3.9, -0.4, 0])
        head = label(r"The convergence dashboard: \ one sequence, four lenses", font_size=34).to_edge(UP, buff=0.3)
        nl = always_redraw(lambda: MathTex(rf"f_n = x^n,\ \ n = {round(dash.n.get_value())}", font_size=30,
                                           color=C.FUNC).next_to(ax, UP, buff=0.1))
        verdict = label(r"uniform convergence is the strictest lens", font_size=26, color=C.EPS).next_to(panel, DOWN, buff=0.4)
        with self.voiceover(
            "From now on we'll watch sequences of functions through several lenses at once, on a dashboard. "
            "<bookmark mark='a'/> Here is x to the n again. The pointwise lens is a probe at one point, here 0.8: the "
            "distance there goes to zero. <bookmark mark='b'/> The uniform lens is the band: its half-width is the "
            "largest distance from the limit, and for x to the n it stays at one forever. <bookmark mark='c'/> Two "
            "more lenses measure the gap on average: the area between the graph and its limit, and the square root "
            "of the integral of the squared gap, which we'll call energy. Both go to zero. <bookmark mark='d'/> So "
            "this sequence converges in three senses but not uniformly. Uniform convergence is the most demanding, "
            "and this chapter shows it's the one that makes the swaps legal."
        ) as vo:
            self.play(FadeIn(head), Create(ax), FadeIn(lim), Create(g), FadeIn(nl))
            vo.wait_until("a")
            self.play(FadeIn(probe), FadeIn(panel[0]))
            self.play(dash.n.animate.set_value(12), run_time=2.5, rate_func=linear)
            vo.wait_until("b")
            self.play(FadeIn(tube), FadeIn(panel[1]))
            self.play(dash.n.animate.set_value(25), run_time=2.0, rate_func=linear)
            vo.wait_until("c")
            self.play(FadeIn(area), FadeIn(panel[2]), FadeIn(panel[3]))
            self.play(dash.n.animate.set_value(60), run_time=3.0, rate_func=linear)
            vo.wait_until("d")
            self.play(*dash.light({"point": True, "sup": False, "L1": True, "L2": True}))
            self.play(FadeIn(verdict))
        dash.freeze()
        for m in (g, tube, area, probe, nl):
            m.clear_updaters()
        self.wait(0.3)
        self.clear_scene()

    # ------------------------------------------------------------------
    def cauchy(self):
        d = load("mtest")
        x, S, Ns = d["x"], d["S"], d["Ns"]
        eps = 0.06
        idx = {int(N): i for i, N in enumerate(Ns)}
        pairs = [(1, 2), (3, 10), (10, 20), (20, 50)]
        gaps = [float(np.abs(S[idx[n]] - S[idx[m]]).max()) for m, n in pairs]
        assert gaps[0] > eps and gaps[1] > eps and gaps[2] < eps and gaps[3] < eps
        head = VGroup(label(r"\textbf{Rudin 7.8} \ (Cauchy criterion) \ $f_n$ converges uniformly $\iff$", font_size=30),
                      MathTex(r"\forall \varepsilon\ \exists N:\ m, n \ge N \Rightarrow |f_n(x) - f_m(x)| < \varepsilon "
                              r"\ \text{ for all } x", font_size=32)).arrange(DOWN, buff=0.15).to_edge(UP, buff=0.3)
        ax = plain_axes([0, 2 * np.pi, np.pi / 2], [-1.4, 1.4, 0.5], 6.4, 3.0).move_to([-3.3, 0.0, 0])
        bx = plain_axes([0, 2 * np.pi, np.pi / 2], [0, 0.3, 0.1], 6.4, 1.5).move_to([-3.3, -2.55, 0])
        tl = MathTex(r"f_n = \sum_{k \le n} \frac{\sin kx}{k^2}", font_size=26, color=GREY_A).next_to(ax, UP, buff=0.05)
        tl.align_to(ax, RIGHT)
        # right of the plot: the first pair's arches reach 0.25 across the whole width
        bl = MathTex(r"|f_n - f_m|", font_size=24, color=C.DIST).next_to(bx.c2p(2 * np.pi, 0.25), RIGHT, buff=0.25)
        el = DashedLine(bx.c2p(0, eps), bx.c2p(2 * np.pi, eps), color=C.EPS, stroke_width=2)
        el_l = MathTex(r"\varepsilon = 0.06", font_size=22, color=C.EPS).next_to(el, RIGHT, buff=0.08)

        def frame(k):
            m, n = pairs[k]
            fm, fn = S[idx[m]], S[idx[n]]
            pts = ([ax.c2p(a, b) for a, b in zip(x[::10], fm[::10] + eps)] +
                   [ax.c2p(a, b) for a, b in zip(x[::-10], fm[::-10] - eps)])
            band = Polygon(*pts, stroke_width=0, fill_color=C.EPS, fill_opacity=0.22)
            gm = polyline(ax, x, fm, color=C.SEQ, stroke_width=3)
            gn = polyline(ax, x, fn, color=C.APPROX, stroke_width=2.5)
            dif = np.abs(fn - fm)
            j = int(np.argmax(dif))
            dg = polyline(bx, x, dif, color=C.DIST, stroke_width=2.5)
            dd = Dot(bx.c2p(x[j], dif[j]), radius=0.06, color=C.PATHOLOGY if gaps[k] > eps else C.CONNECTED_SET)
            return VGroup(band, gm, gn, dg, dd)

        ptab = VGroup(MathTex(r"m,\ n", r"\sup|f_n - f_m|", r"\text{vs } \varepsilon = 0.06", font_size=26, color=GREY_A))
        for k, (m, n) in enumerate(pairs):
            ok = gaps[k] < eps
            ptab.add(MathTex(rf"{m},\ {n}", rf"{gaps[k]:.3f}", r"< \varepsilon" if ok else r"> \varepsilon", font_size=28,
                             color=C.CONNECTED_SET if ok else C.PATHOLOGY))
        ptab.arrange(DOWN, aligned_edge=LEFT, buff=0.24).move_to([3.75, 0.2, 0])
        regrid(ptab, gap=0.45)

        side = VGroup(
            label(r"($\Leftarrow$) \ for each $x$, \ $f_n(x)$ is a Cauchy", font_size=24),
            label(r"sequence of numbers: \ call its limit $f(x)$;", font_size=24),
            label(r"let $m \to \infty$: \ $|f_n(x) - f(x)| \le \varepsilon$ for all $x$", font_size=24, color=C.EPS),
            label(r"\textbf{Rudin 7.9} \ $f_n \to f$ uniformly $\iff$", font_size=26),
            MathTex(r"\sup_x |f_n(x) - f(x)| \to 0", font_size=30, color=C.EPS),
            MathTex(r"\|f\| = \sup_x |f(x)|", font_size=34, color=C.DIST),
            label(r"the \textbf{sup norm}: \ one number for the size of a function", font_size=24, color=GREY_A),
        )
        side.arrange(DOWN, aligned_edge=LEFT, buff=0.16).move_to([3.75, -0.85, 0])
        side[3].shift(DOWN * 0.2)
        side[4].shift(DOWN * 0.2)
        side[5].shift(DOWN * 0.4)
        side[6].shift(DOWN * 0.4)
        with self.voiceover(
            "As with sequences of numbers, we can test uniform convergence without knowing the limit. "
            "<bookmark mark='a'/> A sequence of functions converges uniformly exactly when it's uniformly Cauchy: one "
            "N for which any two later functions are within epsilon of each other at every point. Here are partial "
            "sums of sine k x over k squared, and epsilon is 0.06. The first and second, or the third and tenth, are "
            "still too far apart somewhere; from the tenth on, every pair stays inside the band. "
            "<bookmark mark='b'/> The proof: at each x the values form a Cauchy sequence of numbers, so they converge "
            "to something we call f of x; then letting m go to infinity in the inequality gives uniform convergence to "
            "f. <bookmark mark='c'/> Everything is measured by one number, the largest gap, the height of the dot "
            "below. That suggests giving functions a size: the sup norm."
        ) as vo:
            cur = frame(0)
            self.play(FadeIn(head), Create(ax), Create(bx), FadeIn(tl), FadeIn(bl), Create(el), FadeIn(el_l), FadeIn(cur))
            vo.wait_until("a")
            self.play(FadeIn(ptab[0]), FadeIn(ptab[1]))
            for k in range(1, len(pairs)):
                nxt = frame(k)
                self.play(*[ReplacementTransform(a_, b_) for a_, b_ in zip(cur, nxt)], FadeIn(ptab[k + 1]), run_time=1.4)
                self.wait(0.6)
                cur = nxt
            vo.wait_until("b")
            self.play(FadeOut(ptab), run_time=0.6)
            self.play(LaggedStart(*[FadeIn(r_) for r_ in side[:3]], lag_ratio=0.5), run_time=2.0)
            vo.wait_until("c")
            self.play(Indicate(cur[4], scale_factor=1.8, color=C.DIST))
            self.play(FadeIn(side[3]), FadeIn(side[4]))
            self.play(FadeIn(side[5]), FadeIn(side[6]))
        self.wait(0.3)
        self.clear_scene()

    # ------------------------------------------------------------------
    def mtest(self):
        d = load("mtest")
        x, S, Ns, err, tail = d["x"], d["S"], d["Ns"], d["err"], d["tail"]
        ref = S[-1]
        ax = plain_axes([0, 2 * np.pi, np.pi / 2], [-1.6, 1.6, 0.5], 8.0, 4.8).move_to([-2.4, -0.8, 0])
        lim = polyline(ax, x, ref, color=WHITE, stroke_width=2).set_stroke(opacity=0.6)
        terms = VGroup()
        for n, col in zip((1, 2, 3), [interpolate_color(ManimColor(C.APPROX), ManimColor(WHITE), a_) for a_ in (0.0, 0.35, 0.65)]):
            terms.add(VGroup(polyline(ax, x, np.sin(n * x) / n**2, color=col, stroke_width=2.5),
                             DashedLine(ax.c2p(0, 1 / n**2), ax.c2p(2 * np.pi, 1 / n**2), color=col, stroke_width=1.5),
                             DashedLine(ax.c2p(0, -1 / n**2), ax.c2p(2 * np.pi, -1 / n**2), color=col,
                                        stroke_width=1.5),
                             MathTex(rf"\pm\tfrac{{1}}{{{n * n}}}" if n > 1 else r"\pm 1", font_size=24, color=col).next_to(
                                 ax.c2p(2 * np.pi, (-1) ** (n + 1) / n**2), RIGHT, buff=0.1)))  # alternate sides
        head = VGroup(label(r"\textbf{Rudin 7.10} \ (Weierstrass M-test) \ $|f_n| \le M_n$ and $\sum M_n < \infty$ "
                            r"$\Rightarrow$ $\sum f_n$ converges uniformly", font_size=28),
                      MathTex(r"\sum_{n=1}^{\infty} \frac{\sin nx}{n^2}: \qquad M_n = \frac{1}{n^2}", font_size=34,
                              color=C.APPROX)).arrange(DOWN, buff=0.15).to_edge(UP, buff=0.25)
        if head[0].width > 13.0:
            head[0].width = 13.0
        idx = {1: 0, 2: 1, 3: 2, 5: 3, 10: 4, 20: 5}
        shown = [1, 2, 5, 10, 20]

        def frame(N):
            i = idx[N]
            k = int(np.nonzero(Ns == N)[0][0])
            r = float(tail[k])
            top, bot = ref + r, ref - r
            pts = [ax.c2p(a, b) for a, b in zip(x[::10], top[::10])] + [ax.c2p(a, b) for a, b in zip(x[::-10], bot[::-10])]
            band = Polygon(*pts, stroke_width=0, fill_color=C.EPS, fill_opacity=0.18)
            cur = polyline(ax, x, S[i], color=C.APPROX, stroke_width=3.5)
            return VGroup(band, cur)

        mtab = VGroup(MathTex(r"N", r"\sup |s - s_N|", r"\le \sum_{n > N} \tfrac{1}{n^2}", font_size=26, color=GREY_A))
        for N in shown:
            k = int(np.nonzero(Ns == N)[0][0])
            mtab.add(MathTex(rf"{N}", rf"{err[k]:.4f}", rf"{tail[k]:.4f}", font_size=28))
        mtab.arrange(DOWN, aligned_edge=LEFT, buff=0.22).move_to([4.35, -0.6, 0])
        regrid(mtab, gap=0.4)
        mtab[0][2].set_color(C.EPS)

        assert np.all(err <= tail)
        with self.voiceover(
            "The most useful test for uniform convergence of a series is Weierstrass's M-test. <bookmark mark='a'/> If "
            "each term is bounded by a number M n, and the M n have a finite sum, the series converges uniformly. "
            "<bookmark mark='b'/> Here: sine of n x over n squared, bounded by one over n squared. "
            "<bookmark mark='c'/> After N terms, the rest of the series is at most the tail of the M n, so every "
            "partial sum lies in a band around the limit of that half-width, at every x at once, and the bands shrink "
            "to nothing. The numbers on screen are the actual largest gaps, each under its bound."
        ) as vo:
            self.play(FadeIn(head[0]), Create(ax), LaggedStart(*[Create(t_) for t_ in terms], lag_ratio=0.4), run_time=2.5)
            vo.wait_until("a")
            self.play(*[ShowPassingFlash(VGroup(t_[1], t_[2]).copy().set_stroke(width=4), time_width=0.6) for t_ in terms],
                      run_time=1.2)
            vo.wait_until("b")
            self.play(FadeIn(head[1]), FadeOut(terms))
            self.play(Create(lim))
            cur = frame(shown[0])
            self.play(FadeIn(cur), FadeIn(mtab[0]), FadeIn(mtab[1].set_color(C.APPROX)))
            vo.wait_until("c")
            for j, N in enumerate(shown[1:], start=1):
                nxt = frame(N)
                self.play(ReplacementTransform(cur[0], nxt[0]), ReplacementTransform(cur[1], nxt[1]),
                          mtab[j].animate.set_color(WHITE), FadeIn(mtab[j + 1].set_color(C.APPROX)), run_time=1.3)
                cur = nxt
        self.wait(0.4)
        self.clear_scene()

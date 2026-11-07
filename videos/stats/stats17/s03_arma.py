from __future__ import annotations

import numpy as np

from explainer.stats.kit import ts as T
from videos.stats.stats17.common import *  # noqa: F403


class Arma(VoiceoverScene):
    def construct(self):
        self.card()
        self.ar1()
        self.gallery()
        self.explode()
        self.roots()
        self.triangle()
        self.ma_invert()
        self.wold()

    def card(self):
        card = chapter_card(2, r"AR, \ MA, \ ARMA", r"Building memory out of shocks", part=PART)
        with self.voiceover("Chapter two. Autoregressive and moving-average models."):
            self.play(FadeIn(card[0], shift=UP * 0.2), FadeIn(card[1]))
        self.play(FadeOut(card))

    def ar1(self):
        rows = [
            cmath(r"X_t", r"=", r"\phi X_{t-1} + e_t", font_size=34),
            cmath(r"\ ", r"=", r"e_t + \phi e_{t-1} + \phi^2 e_{t-2} + \cdots", font_size=34),
            cmath(r"\mathrm{Var}(X_t)", r"=", r"\frac{\sigma^2}{1 - \phi^2},\ \ \rho(h) = \phi^{|h|}", font_size=32),
            cmath(r"\text{needs}", r":", r"|\phi| < 1", font_size=34),
        ]
        rows[3][2].set_color(OBS)
        whys = [why(r"an autoregression of order 1"), why(r"substitute again and again: \ an MA($\infty$)"),
                why(r"a geometric series; \ the memory fades geometrically"), why(r"or the old shocks never fade")]
        intro = label('Autoregression carries past shocks into the present', font_size=36).move_to([0, 3.2, 0])
        if intro.width > 12.5:
            intro.width = 12.5
        with self.voiceover(
            "<bookmark mark='a'/> The autoregression of order one: this period's value is phi times the last, plus a fresh "
            "shock. <bookmark mark='b'/> Substitute for the last value, and again, and again: the series is a weighted sum of "
            "all the past shocks, with weights one, phi, phi squared. Every observation carries a fading memory of every shock "
            "before it. <bookmark mark='c'/> The variance is a geometric series, sigma squared over one minus phi squared, and "
            "the autocorrelation at lag h is phi to the h: memory decays geometrically. <bookmark mark='d'/> All of this needs "
            "phi between minus one and one, so that old shocks fade. Otherwise the sum doesn't converge."
        ) as vo:
            self.play(FadeIn(intro))
            step = ladder(self, rows, whys, keep=4, top=2.6, x=-0.4, buff=0.7, edge=6.9)
            for k, m_ in enumerate("abcd"):
                vo.wait_until(m_)
                step(k, transform=False)
        self.clear_scene()

    def gallery(self):
        d = load("arma")
        specs = [("ar_pos", r"AR(1), \ $\phi = 0.9$", SERIES), ("ar_neg", r"AR(1), \ $\phi = -0.9$", S.ALT),
                 ("ma", r"MA(1), \ $\theta = 0.8$", RES), ("arma", r"ARMA(1,1), \ $\phi = 0.7,\ \theta = 0.5$", OBS)]
        panels = VGroup()
        for k, (key, nm, col) in enumerate(specs):
            cx = -3.5 if k % 2 == 0 else 3.5
            cy = 1.55 if k < 2 else -1.75
            x = np.asarray(d[key]["x"])
            A = axes([0, 150], [x.min(), x.max()], x_length=5.8, y_length=1.1, center=[cx, cy + 0.75, 0])
            B = axes([0, 13], [-1, 1], x_length=5.8, y_length=1.2, center=[cx, cy - 0.65, 0], yticks=[-1, 0, 1], font_size=14)
            ln = series_line(A.ax, np.arange(150), x, col, 1.6)
            cg = Correlogram(B.ax, np.asarray(d[key]["acf"])[:13], theory=None, color=col, width=0.55)
            nm_ = label(nm, font_size=20, color=col).next_to(A, UP, buff=0.05)
            panels.add(VGroup(A, ln, B, cg, nm_))
        intro = label('Different memories leave different autocorrelation patterns', font_size=36)
        with self.voiceover(
            "A gallery, each with a simulated path and its theoretical autocorrelations. <bookmark mark='a'/> Phi equal to "
            "point nine: long, slow swells, and correlations that fade slowly. <bookmark mark='b'/> Phi equal to minus point "
            "nine: the series flips sign almost every step, and the correlations alternate. <bookmark mark='c'/> A moving "
            "average of order one, the current shock plus point eight of the previous one. Its memory is exactly one step "
            "long: the autocorrelation at lag one is theta over one plus theta squared, point four nine, and every later lag "
            "is zero. <bookmark mark='d'/> And a mixture, an ARMA of order one and one: an autoregressive decay that starts "
            "from a lag-one value set by the moving-average part. Different memories, different fingerprints in the "
            "autocorrelation function."
        ) as vo:
            self.play(FadeIn(intro))
            for k, m_ in enumerate("abcd"):
                vo.wait_until(m_)
                if k == 0:
                    self.play(FadeOut(intro), run_time=0.25)
                p = panels[k]
                self.play(FadeIn(p[0]), FadeIn(p[4]), Create(p[1]), FadeIn(p[2]), run_time=1.2)
                self.play(LaggedStart(*[GrowFromEdge(b_, DOWN) for b_ in p[3].bars], lag_ratio=0.05), FadeIn(p[3].zero))
        self.clear_scene()

    def explode(self):
        g = np.random.Generator(np.random.PCG64(11))
        n = 60
        e = g.normal(size=n)
        paths = {}
        for phi in (0.5, 1.0, 1.08):
            x = np.zeros(n)
            for t in range(1, n):
                x[t] = phi * x[t - 1] + e[t]
            paths[phi] = x
        A = axes([0, 60], [-12, 40], x_length=8.4, y_length=4.4, xlabel=r"time", ylabel=r"$X_t$", xticks=[0, 20, 40, 60],
                 yticks=[0, 20, 40], center=[-1.6, 0.2, 0])
        ax = A.ax
        cols = {0.5: SERIES, 1.0: OBS, 1.08: RES}
        lines = {p: series_line(ax, np.arange(n), x, cols[p], 3) for p, x in paths.items()}
        rows = fit_rows(VGroup(
            label(r"the same shocks, \ three values of $\phi$", font_size=22),
            label(r"$\phi = 0.5$: \ stationary, \ hugs zero", font_size=22, color=SERIES),
            label(r"$\phi = 1$: \ a random walk, \ wanders", font_size=22, color=OBS),
            label(r"$\phi = 1.08$: \ explodes", font_size=22, color=RES),
        ), 3.8, 0.4, [5.0, 0.4, 0])
        with self.voiceover(
            "<bookmark mark='a'/> Feed the same sixty shocks into three autoregressions. <bookmark mark='b'/> With phi equal to "
            "a half, the series hugs zero: each shock is half forgotten by the next step. <bookmark mark='c'/> With phi equal "
            "to one, nothing is forgotten: the random walk, which has no mean reversion, and whose variance grows without "
            "limit. Part 38 will test for this unit root. <bookmark mark='d'/> With phi just above one, each step amplifies the "
            "last, and the series explodes. Only the first converges from this zero start to a causal stationary law."
        ) as vo:
            self.play(FadeIn(A))
            vo.wait_until("a")
            self.play(FadeIn(rows[0]))
            for k, (m_, p) in enumerate(zip("bcd", (0.5, 1.0, 1.08))):
                vo.wait_until(m_)
                self.play(Create(lines[p]), FadeIn(rows[k + 1]), run_time=1.6)
        self.clear_scene()

    def roots(self):
        d = load("sunspot")
        rp = RootPlane([], center=[-3.4, 0.2, 0], scale=1.35, extent=2.2)
        steps = [([2.0], r"AR(1), \ $\phi = 0.5$: \ root $1/\phi = 2$"), ([1 / 0.9], r"$\phi = 0.9$: \ root 1.11, \ near the circle"),
                 ([1.0], r"$\phi = 1$: \ on the circle, \ a unit root"), (d["roots"], r"Yule's sunspot AR(2): \ $1.03 \pm 0.69i$")]
        rows = [
            cmath(r"\phi(z)", r"=", r"1 - \phi_1 z - \cdots - \phi_p z^p", font_size=30),
            cmath(r"\text{causal stationary}", r"\iff", r"\text{every root of } \phi(z) \text{ has } |z| > 1", font_size=28),
        ]
        g = VGroup(*rows).arrange(DOWN, aligned_edge=LEFT, buff=0.35).move_to([3.4, 2.4, 0])
        for r_ in g:
            if r_.width > 6.2:
                r_.width = 6.2
        notes = VGroup(*[label(t, font_size=22, color=GREY_A) for _, t in steps]).arrange(DOWN, aligned_edge=LEFT, buff=0.32)
        notes.move_to([3.4, -0.6, 0])
        for nt in notes:
            if nt.width > 6.4:
                nt.width = 6.4
        mod = MathTex(rf"|z| = {d['modulus']:.2f} > 1", font_size=28, color=HIT).move_to([3.4, -2.6, 0])
        with self.voiceover(
            "There's a single test for all autoregressions. <bookmark mark='a'/> Write the coefficients as a polynomial, one "
            "minus phi one z, minus phi two z squared, and so on. <bookmark mark='b'/> A causal stationary AR solution, driven by innovations orthogonal to its past, exists exactly when "
            "every root of that polynomial lies outside the unit circle in the complex plane. <bookmark mark='c'/> For an "
            "AR one with phi a half, the root is at two: comfortably outside. <bookmark mark='d'/> Phi of point nine puts it at "
            "one point one one, close to the edge: long memory. <bookmark mark='e'/> Phi of one puts it on the circle: the "
            "unit root of the random walk. <bookmark mark='f'/> Yule's sunspot model has a pair of complex roots, one point oh "
            "three plus or minus point six nine i, <bookmark mark='g'/> of modulus one point two four: outside, so stationary. "
            "Complex roots mean oscillation, and that's chapter three."
        ) as vo:
            self.play(FadeIn(rp))
            vo.wait_until("a")
            self.play(FadeIn(g[0]))
            vo.wait_until("b")
            self.play(FadeIn(g[1]))
            cur = VGroup()
            for k, m_ in enumerate("cdef"):
                vo.wait_until(m_)
                new = rp.mark(steps[k][0], radius=0.11)
                self.play(FadeOut(cur), FadeIn(new, scale=1.6), FadeIn(notes[k]))
                cur = new
            vo.wait_until("g")
            self.play(FadeIn(mod), Indicate(cur, color=HIT))
        self.clear_scene()

    def triangle(self):
        d = load("sunspot")
        A = axes([-2.2, 2.2], [-1.2, 1.2], x_length=6.4, y_length=4.4, xlabel=r"$\phi_1$", ylabel=r"$\phi_2$", xticks=[-2, -1, 0, 1, 2],
                 yticks=[-1, 0, 1], center=[-2.6, 0.1, 0])
        ax = A.ax
        tri = Polygon(ax.c2p(-2, -1), ax.c2p(2, -1), ax.c2p(0, 1), stroke_color=GREY_A, stroke_width=2.5, fill_color=SERIES,
                      fill_opacity=0.15)
        xs = np.linspace(-2, 2, 100)
        par = polyline(ax, xs, -xs ** 2 / 4, OBS, 2.5)
        cplx = Polygon(*[ax.c2p(a, -a ** 2 / 4) for a in xs], ax.c2p(2, -1), ax.c2p(-2, -1), stroke_width=0, fill_color=OBS,
                       fill_opacity=0.18)
        yule = Dot(ax.c2p(*d["ols"]), radius=0.1, color=RES)
        yl = MathTex(r"\text{Yule}", font_size=22, color=RES).next_to(yule, RIGHT, buff=0.1)
        rows = fit_rows(VGroup(
            label(r"AR(2) is stationary inside the triangle", font_size=22),
            MathTex(r"\phi_1 + \phi_2 < 1,\ \ \phi_2 - \phi_1 < 1,\ \ |\phi_2| < 1", font_size=26),
            label(r"below the parabola $\phi_1^2 + 4\phi_2 < 0$: \ complex roots, \ oscillation", font_size=22, color=OBS),
            MathTex(rf"\text{{Yule's sunspots}}: ({d['ols'][0]:.2f},\ {d['ols'][1]:.2f})", font_size=26, color=RES),
        ), 5.0, 0.4, [4.0, 0.2, 0])
        with self.voiceover(
            "<bookmark mark='a'/> For the AR two, the roots condition draws a picture in the plane of the two coefficients. "
            "The model is stationary inside a triangle, <bookmark mark='b'/> bounded by three lines. <bookmark mark='c'/> "
            "Below the parabola, phi one squared plus four phi two less than zero, the roots are complex, and the series "
            "oscillates. <bookmark mark='d'/> Yule's sunspot fit sits here: inside the triangle, below the parabola, a damped "
            "oscillation kept alive by its shocks."
        ) as vo:
            self.play(FadeIn(A))
            vo.wait_until("a")
            self.play(DrawBorderThenFill(tri), FadeIn(rows[0]))
            vo.wait_until("b")
            self.play(FadeIn(rows[1]))
            vo.wait_until("c")
            self.play(Create(par), FadeIn(cplx), FadeIn(rows[2]))
            vo.wait_until("d")
            self.play(FadeIn(yule, scale=1.8), FadeIn(yl), FadeIn(rows[3]))
        self.clear_scene()

    def ma_invert(self):
        rows = [
            cmath(r"X_t", r"=", r"e_t + \theta e_{t-1}", font_size=34),
            cmath(r"\rho(1)", r"=", r"\frac{\theta}{1 + \theta^2}\ \ \text{the same for } \theta \text{ and } 1/\theta", font_size=30),
            cmath(r"|\theta| < 1", r":", r"e_t = X_t - \theta X_{t-1} + \theta^2 X_{t-2} - \cdots", font_size=30),
            cmath(r"\text{invertible}", r"\iff", r"\text{the roots of } 1 + \theta_1 z + \cdots \text{ lie outside the circle}", font_size=28),
        ]
        rows[3][2].set_color(OBS)
        whys = [why(r"a moving average of order 1"), why(r"$\theta = 0.5$ and $\theta = 2$: \ identical ACFs"),
                why(r"the shocks can be recovered from the past"), why(r"the convention that makes MA models identifiable")]
        intro = label('Invertibility recovers innovations from observed history', font_size=36)
        with self.voiceover(
            "Moving averages have a subtlety of their own. <bookmark mark='a'/> An MA one is the current shock plus theta "
            "times the last. <bookmark mark='b'/> Its lag-one autocorrelation is theta over one plus theta squared, and that's "
            "the same for theta and one over theta: point five and two give identical autocorrelations, so autocorrelations alone cannot distinguish them. For Gaussian shocks their full laws agree after rescaling the innovation variance. <bookmark mark='c'/> With theta inside the unit interval, the shocks can be rebuilt from the "
            "observed past, a convergent sum. <bookmark mark='d'/> That's invertibility, and the rule is the mirror of "
            "stationarity: the moving-average polynomial's roots must lie outside the unit circle. By convention we always "
            "choose the invertible version."
        ) as vo:
            self.play(FadeIn(intro))
            step = ladder(self, rows, whys, keep=4, top=2.6, x=-0.4, buff=0.7, edge=6.9)
            for k, m_ in enumerate("abcd"):
                vo.wait_until(m_)
                step(k, transform=False)
                if k == 0:
                    self.play(FadeOut(intro), run_time=0.25)
        self.clear_scene()

    def wold(self):
        psi = T.psi_weights([0.7], [0.5], 12)
        rows = [
            cmath(r"\text{ARMA}(p, q)", r":", r"\phi(B) X_t = \theta(B) e_t", font_size=32),
            cmath(r"X_t", r"=", r"\sum_{j \ge 0} \psi_j e_{t-j},\ \ \psi(z) = \theta(z)/\phi(z)", font_size=32),
            cmath(r"\text{ARMA(1,1)}", r":", rf"\psi = 1,\ {psi[1]:.2f},\ {psi[2]:.2f},\ {psi[3]:.3f}, \ldots", font_size=30),
            cmath(r"\text{Wold (1938)}", r":", r"\text{every stationary series} = \text{deterministic} + \text{MA}(\infty)", font_size=28),
        ]
        rows[3][2].set_color(OBS)
        whys = [why(r"$B$: \ the backshift, \ $BX_t = X_{t-1}$"), why(r"divide the polynomials"),
                why(r"$\phi = 0.7$, \ $\theta = 0.5$"), why(r"ARMA: \ a few parameters for a long memory")]
        with self.voiceover(
            "<bookmark mark='a'/> In general an ARMA of orders p and q combines both: a polynomial in the backshift operator on "
            "the series, and another on the shocks. <bookmark mark='b'/> For a causal stable model, the centred series is an infinite moving "
            "average of shocks, with weights psi from dividing one polynomial by the other. <bookmark mark='c'/> For the "
            "ARMA one-one of the gallery: one, one point two, point eight four, point five eight eight, decaying. "
            "<bookmark mark='d'/> Herman Wold proved in 1938 that every finite-variance weakly stationary series can be written as a linearly deterministic "
            "part, predictable from its infinite past, plus an infinite moving average of uncorrelated innovations. The deterministic part need not be a nonrandom path. ARMA models are a way of approximating that infinite list of "
            "weights with a handful of parameters."
        ) as vo:
            step = ladder(self, rows, whys, keep=4, top=2.6, x=-0.4, buff=0.7, edge=6.9)
            for k, m_ in enumerate("abcd"):
                vo.wait_until(m_)
                step(k, transform=False)
        self.clear_scene()

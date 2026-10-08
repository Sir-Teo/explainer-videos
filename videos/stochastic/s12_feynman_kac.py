from __future__ import annotations

import numpy as np

from explainer import *  # noqa: F403
from explainer.fluids import colormaps as cm
from videos.stochastic.common import boxed, label, load, mtex, note, num, polyline
from videos.stochastic.compute import disk_g

HEAT_MID = "#B0587C"


def heat_rgba(F: np.ndarray) -> np.ndarray:
    """Temperature field (NaN outside the domain) -> RGBA, cold blue through magenta to hot amber."""
    rgb = cm.sequential(np.nan_to_num(F, nan=0.0), 0.0, 1.0, low=C.COLD, high=C.HOT, mid=HEAT_MID)
    a = np.where(np.isfinite(F), 1.0, 0.0)[..., None]
    return cm.to_uint8(np.concatenate([rgb, a], axis=2))


def heat_color(v: float) -> ManimColor:
    rgb = cm.sequential(np.array([v]), 0.0, 1.0, low=C.COLD, high=C.HOT, mid=HEAT_MID)[0]
    return rgb_to_color(rgb)


class FeynmanKac(VoiceoverScene):
    def construct(self):
        self.question()
        self.ruin()
        self.backward()
        self.disk()
        self.field()

    # ------------------------------------------------------------------
    def question(self):
        fwd = label(r"Fokker--Planck: \ where will the particles \emph{be}?", font_size=34, color=C.PDF)
        bwd = label(r"Backward: \ starting from $x$, what will a payoff be worth \emph{on average}?", font_size=34,
                    color=C.GAINS)
        u = MathTex(r"u(t, x)", r"=", r"\mathbb E\big[\,g(X_T)\;\big|\;X_t = x\,\big]", font_size=46)
        u[0].set_color(C.GAINS)
        VGroup(fwd, bwd, u).arrange(DOWN, buff=0.6).move_to(UP * 0.3)
        with self.voiceover(
            "Fokker–Planck runs forward in time: given where the particles start, where will they be? "
            "<bookmark mark='b'/> Now turn the question around. Start a particle at x. Some payoff g depends on where "
            "it ends up at time T. <bookmark mark='u'/> What is that payoff worth on average? Call the answer u of t and x."
        ) as vo:
            self.play(FadeIn(fwd))
            vo.wait_until("b")
            self.play(FadeIn(bwd))
            vo.wait_until("u")
            self.play(Write(u))
        self.wait(0.3)
        self.clear_scene()

    # ------------------------------------------------------------------
    def ruin(self):
        e = load("exit")
        trace, tau, hit = e["trace"], e["tau"], e["hit_top"]
        dt = float(e["dt"][0])
        p_top, m_tau, x0, th_tau = (float(v) for v in e["stats"])
        T = 0.6
        ax = Axes(x_range=[0, T, 0.1], y_range=[0, 1, 0.5], x_length=9.0, y_length=4.4, tips=False,
                  axis_config={"stroke_color": GREY_D, "include_ticks": False}).to_edge(LEFT, buff=1.5).shift(DOWN * 0.4)
        top = Line(ax.c2p(0, 1), ax.c2p(T, 1), color=C.HOT, stroke_width=6)
        bot = Line(ax.c2p(0, 0), ax.c2p(T, 0), color=C.COLD, stroke_width=6)
        tl = label(r"win: $g = 1$", font_size=26, color=C.HOT).next_to(top, UP, buff=0.1).align_to(top, LEFT)
        bl = label(r"lose: $g = 0$", font_size=26, color=C.COLD).next_to(bot, DOWN, buff=0.1).align_to(bot, LEFT)
        start = Dot(ax.c2p(0, x0), radius=0.07, color=WHITE)
        sl = MathTex(rf"x = {x0:g}", font_size=28).next_to(start, LEFT, buff=0.1)
        paths = VGroup()
        for i in range(trace.shape[1]):
            n_i = min(len(trace), int(np.ceil(tau[i] / dt)) + 1)
            ts = np.arange(n_i) * dt
            keep = ts <= T
            if keep.sum() < 2:
                continue
            col = C.HOT if hit[i] else C.COLD
            paths.add(polyline(ax, ts[keep], trace[:n_i, i][keep], color=col, stroke_width=1.6).set_stroke(opacity=0.75))
        stats = VGroup(
            MathTex(r"P(\text{hit } 1 \text{ first})", r"=", num(p_top, 3), font_size=32),
            MathTex(r"\text{theory: } u(x) = x", r"=", num(x0, 3), font_size=28, color=GREY_A),
            MathTex(r"\mathbb E[\text{time to exit}]", r"=", num(m_tau, 3), font_size=32),
            MathTex(r"\text{theory: } x(1 - x)", r"=", num(th_tau, 3), font_size=28, color=GREY_A),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.2).to_edge(RIGHT, buff=0.4).shift(UP * 0.6)
        stats[0][2].set_color(C.HOT)
        sim = note(r"4{,}000 simulated paths, 40 shown").to_corner(DR, buff=0.3)
        title = label(r"Gambler's ruin, in continuous time", font_size=34).to_edge(UP, buff=0.4)
        assert round(p_top, 3) == 0.295 and round(m_tau, 3) == 0.203

        with self.voiceover(
            "Here's the simplest case: <bookmark mark='a'/> a Brownian gambler starts with fortune point three, and plays "
            "until reaching one, a win, or zero, ruin. <bookmark mark='p'/> Each path is colored by how it ended. "
            "<bookmark mark='s'/> Out of four thousand simulated gamblers, 29.5 percent reach the top first, and the game "
            "lasts 0.203 time units on average."
        ) as vo:
            self.play(FadeIn(title))
            vo.wait_until("a")
            self.play(Create(ax), Create(top), Create(bot), FadeIn(tl), FadeIn(bl), FadeIn(start), FadeIn(sl))
            vo.wait_until("p")
            self.play(LaggedStart(*[Create(p) for p in paths], lag_ratio=0.05), FadeIn(sim), run_time=3)
            vo.wait_until("s")
            self.play(FadeIn(stats[0]), FadeIn(stats[2]))
        with self.voiceover(
            "Both numbers have exact answers, and here's where they come from. <bookmark mark='m'/> Let u of x be the "
            "chance of winning from x. Your chance, re-evaluated as the game goes on, is a fair game: it's a martingale. "
            "So by Itô's lemma, its drift, one half u double prime, must be zero. <bookmark mark='l'/> u is a straight line, "
            "zero at zero and one at one: u of x equals x. Point three. <bookmark mark='t'/> The same argument for the "
            "expected time gives one half u double prime equals minus one, and the answer x times one minus x: 0.21."
        ) as vo:
            vo.wait_until("m")
            mart = MathTex(r"\tfrac12\,u''(x) = 0", font_size=34, color=C.QV).next_to(stats, DOWN, buff=0.45).align_to(stats, LEFT)
            self.play(Write(mart))
            vo.wait_until("l")
            self.play(FadeIn(stats[1]))
            vo.wait_until("t")
            self.play(FadeIn(stats[3]))
        self.wait(0.4)
        self.clear_scene()

    # ------------------------------------------------------------------
    def backward(self):
        l1 = MathTex(r"M_s", r"=", r"u(s, X_s)", r"=", r"\mathbb E\big[g(X_T)\mid \text{everything known at } s\big]",
                     font_size=36)
        l1[2].set_color(C.GAINS)
        n1 = label(r"your forecast, updated as you learn: \ a martingale", font_size=24, color=GREY_B)
        l2 = MathTex(r"dM", r"=", r"\Big(u_t + \mu\,u_x + \tfrac12\sigma^2 u_{xx}\Big)", r"\,ds", r"+",
                     r"\sigma\,u_x\,dW", font_size=38)
        l2[2].set_color(C.DRIFT)
        l2[5].set_color(C.BROWNIAN)
        n2 = label(r"It\^o's lemma", font_size=24, color=GREY_B)
        l3 = MathTex(r"u_t + \mu\,u_x + \tfrac12\sigma^2 u_{xx}", r"=", r"0", r",\qquad u(T, x) = g(x)", font_size=44)
        l3[0].set_color(C.DRIFT)
        l3b = boxed(l3, color=C.GAINS, buff=0.25)
        n3 = label(r"a martingale has no drift: \ Kolmogorov's backward equation", font_size=26, color=C.GAINS)
        col = VGroup(VGroup(l1, n1).arrange(DOWN, buff=0.1), VGroup(l2, n2).arrange(DOWN, buff=0.1),
                     VGroup(l3b, n3).arrange(DOWN, buff=0.12)).arrange(DOWN, buff=0.5).to_edge(UP, buff=0.4)
        fk = MathTex(r"u(t, x)", r"=", r"\mathbb E\Big[e^{-r(T - t)}\, g(X_T)\;\Big|\;X_t = x\Big]", r"\quad\text{solves}\quad",
                     r"u_t + \mu u_x + \tfrac12\sigma^2 u_{xx} - r\,u = 0", font_size=32)
        fk[0].set_color(C.GAINS)
        fk.next_to(col, DOWN, buff=0.45)
        fkn = label(r"the Feynman--Kac formula (Kac, 1949)", font_size=26, color=GREY_A).next_to(fk, DOWN, buff=0.15)

        with self.voiceover(
            "The same argument works for any payoff. <bookmark mark='a'/> Your best forecast of the payoff, given "
            "everything you know at time s, is u of s and X s. As information arrives, the forecast gets updated, but it "
            "can't be expected to drift: if you expected it to rise, you'd have raised it already. It's a martingale. "
            "<bookmark mark='b'/> Itô's lemma splits its change into a drift term and a noise term. <bookmark mark='c'/> "
            "A martingale has no drift, so the drift term must vanish, everywhere."
        ) as vo:
            vo.wait_until("a")
            self.play(Write(l1), FadeIn(n1))
            vo.wait_until("b")
            self.play(Write(l2), FadeIn(n2))
            vo.wait_until("c")
            self.play(Indicate(l2[2], color=C.DRIFT))
        with self.voiceover(
            "That's a partial differential equation for u, <bookmark mark='k'/> Kolmogorov's backward equation, solved "
            "backward from the payoff at the final time. <bookmark mark='f'/> Add a discount rate, and you get the "
            "Feynman–Kac formula: averages over random paths solve partial differential equations. Mark Kac found it in "
            "1949, inspired by Feynman's path integrals in quantum mechanics."
        ) as vo:
            vo.wait_until("k")
            self.play(Write(l3), Create(l3b[0]), FadeIn(n3))
            vo.wait_until("f")
            self.play(FadeIn(fk), FadeIn(fkn))
        self.wait(0.4)
        self.clear_scene()

    # ------------------------------------------------------------------
    def disk_frame(self, center, R):
        """The rim: g = 1 where sin(3 theta) > 0 (three hot arcs), 0 elsewhere (three cold arcs)."""
        assert disk_g(np.array([np.pi / 6]))[0] == 1 and disk_g(np.array([np.pi / 2]))[0] == 0
        return VGroup(*[Arc(radius=R, start_angle=k * PI / 3, angle=PI / 3, arc_center=center, stroke_width=7,
                            color=C.HOT if k % 2 == 0 else C.COLD) for k in range(6)])

    def disk(self):
        d = load("disk")
        P, lens, ends, z0 = d["paths"], d["lens"], d["ends"], d["z0"]
        run, exact0 = d["run"], float(d["exact0"][0])
        R = 2.7
        center = np.array([-3.3, -0.5, 0])
        inside = Circle(radius=R, stroke_width=0, fill_color="#141B24", fill_opacity=1).move_to(center)
        rim = self.disk_frame(center, R)
        eq = MathTex(r"\Delta u = 0", r"\ \text{inside},\qquad", r"u = g", r"\ \text{on the rim}", font_size=36)
        eq[0].set_color(C.PDF)
        eq.to_edge(UP, buff=0.35).shift(RIGHT * 2.6)
        eqn = label(r"steady temperature: Laplace's equation", font_size=26, color=GREY_A).next_to(eq, DOWN, buff=0.12)
        p0 = center + R * np.array([z0[0], z0[1], 0])
        dot = Dot(p0, radius=0.08, color=WHITE)

        with self.voiceover(
            "In two dimensions, this idea solves a classic problem of physics. <bookmark mark='r'/> Heat the rim of a metal "
            "disk: three hot arcs, three cold ones. Wait for the temperature inside to settle. <bookmark mark='l'/> The "
            "steady temperature solves Laplace's equation: zero curvature, on average, in every direction. "
            "<bookmark mark='q'/> What's the temperature at this point?"
        ) as vo:
            vo.wait_until("r")
            self.play(FadeIn(inside), Create(rim), run_time=1.5)
            vo.wait_until("l")
            self.play(Write(eq), FadeIn(eqn))
            vo.wait_until("q")
            self.play(FadeIn(dot, scale=2))

        walkers = []
        for i in range(len(lens)):
            pts = P[i, : lens[i]]
            hot = disk_g(np.array([ends[i]]))[0] > 0.5
            col = C.HOT if hot else C.COLD
            m = VMobject(stroke_color=col, stroke_width=1.4, stroke_opacity=0.8)
            m.set_points_as_corners([center + R * np.array([x, y, 0]) for x, y in pts])
            hit = Dot(center + R * np.array([np.cos(ends[i]), np.sin(ends[i]), 0]), radius=0.07, color=col)
            walkers.append((m, hit, hot))
        count = ValueTracker(0)
        hots = ValueTracker(0)
        avg = DecimalNumber(0, num_decimal_places=3, font_size=36, color=C.GAINS)
        avg.add_updater(lambda m: m.set_value(hots.get_value() / max(count.get_value(), 1)))
        nn = Integer(0, font_size=32)
        nn.add_updater(lambda m: m.set_value(int(count.get_value())))
        panel = VGroup(
            VGroup(label(r"walkers:", font_size=30), nn).arrange(RIGHT, buff=0.15),
            VGroup(label(r"average rim temperature:", font_size=30), avg).arrange(RIGHT, buff=0.15),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.25).move_to([3.2, 0.9, 0])
        big = VGroup(
            MathTex(r"20{,}000 \text{ walkers: }", num(float(run.mean()), 4), font_size=32),
            MathTex(r"\text{exact: }", num(exact0, 4), font_size=32),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.2).next_to(panel, DOWN, buff=0.5).align_to(panel, LEFT)
        big[0][1].set_color(C.GAINS)
        why = label(r"in 2D, It\^o: \ $du(B_t) = \nabla u\cdot dB_t + \tfrac12\Delta u\,dt$\\"
                    r"so $\Delta u = 0$ \ $\Leftrightarrow$ \ $u(B_t)$ is a martingale", font_size=26, color=GREY_A)
        why.next_to(big, DOWN, buff=0.45).align_to(panel, LEFT)
        why.shift(LEFT * max(0, why.get_right()[0] - 6.9))
        assert abs(run.mean() - exact0) < 0.005

        with self.voiceover(
            "Brownian motion knows. <bookmark mark='w'/> Release a random walker from the point, let it wander until it "
            "hits the rim, and record the temperature where it lands. Do it again, and again. <bookmark mark='a'/> The "
            "average temperature they report converges to the temperature at the point."
        ) as vo:
            self.play(FadeIn(panel))
            vo.wait_until("w")
            for i, (m, hit, hot) in enumerate(walkers[:4]):
                self.play(Create(m), run_time=1.0, rate_func=linear)
                self.play(FadeIn(hit, scale=2), count.animate.set_value(i + 1), hots.animate.set_value(hots.get_value() + hot),
                          m.animate.set_stroke(opacity=0.25), run_time=0.4)
            vo.wait_until("a")
            rest = walkers[4:]
            for j in range(0, len(rest), 4):
                chunk = rest[j:j + 4]
                c0 = count.get_value()
                h0 = hots.get_value()
                self.play(*[Create(m) for m, _, _ in chunk], run_time=0.5, rate_func=linear)
                self.play(*[FadeIn(h) for _, h, _ in chunk], *[m.animate.set_stroke(opacity=0.18) for m, _, _ in chunk],
                          count.animate.set_value(c0 + len(chunk)), hots.animate.set_value(h0 + sum(h for _, _, h in chunk)),
                          run_time=0.25)
        with self.voiceover(
            "With twenty thousand walkers, the average is 0.533. <bookmark mark='e'/> The exact solution of Laplace's "
            "equation at that point: 0.534. <bookmark mark='y'/> The reason is Itô's lemma once more: for two-dimensional "
            "Brownian motion the drift term is one half the Laplacian, so a function with zero Laplacian, evaluated along "
            "the walk, is a fair game. Averaging where the walkers stop gives the value where they started."
        ) as vo:
            self.play(FadeIn(big[0]))
            vo.wait_until("e")
            self.play(FadeIn(big[1]))
            vo.wait_until("y")
            self.play(FadeIn(why))
        self.wait(0.3)
        for m in (avg, nn):
            m.clear_updaters()
        self.clear_scene()

    # ------------------------------------------------------------------
    def field(self):
        d = load("disk")
        R = 2.6
        cl, cr = np.array([-3.4, -0.45, 0]), np.array([3.4, -0.45, 0])

        def img(F, center):
            im = ImageMobject(heat_rgba(F))
            im.set_resampling_algorithm(RESAMPLING_ALGORITHMS["bilinear"])
            im.stretch_to_fit_width(2 * R).stretch_to_fit_height(2 * R).move_to(center)
            return im

        rims = VGroup(self.disk_frame(cl, R), self.disk_frame(cr, R))
        mcs = [img(d[f"mc{k}"], cl) for k in (1, 4, 16, 64, 256)]
        exact = img(d["exact"], cr)
        lab = [MathTex(rf"{k} \text{{ walker{'s' if k > 1 else ''} per pixel}}", font_size=32).next_to(rims[0], UP, buff=0.25)
               for k in (1, 4, 16, 64, 256)]
        el = label(r"exact solution of $\Delta u = 0$", font_size=32).next_to(rims[1], UP, buff=0.25)
        err = float(d["mc_err"][0])
        errl = label(rf"mean difference at 256 walkers: {err:.3f}", font_size=26, color=GREY_A).to_corner(DL, buff=0.3)
        kak = note(r"Kakutani (1944): harmonic functions are averages over Brownian paths").to_corner(DR, buff=0.3)
        with self.voiceover(
            "Now do that at every point of the disk at once. <bookmark mark='a'/> With one walker per pixel, each pixel "
            "is just hot or cold: pure noise. <bookmark mark='b'/> Four walkers. <bookmark mark='c'/> Sixteen. "
            "<bookmark mark='d'/> Sixty-four. <bookmark mark='e'/> Two hundred fifty-six. <bookmark mark='x'/> The noise "
            "melts into the smooth solution of Laplace's equation. Shizuo Kakutani discovered this connection in 1944: "
            "harmonic functions are averages over Brownian paths."
        ) as vo:
            self.play(Create(rims[0]), Create(rims[1]), run_time=1.2)
            vo.wait_until("a")
            self.add(mcs[0])
            self.play(FadeIn(mcs[0]), FadeIn(lab[0]))
            cur, curl = mcs[0], lab[0]
            for m, k_ in zip("bcde", range(1, 5)):
                vo.wait_until(m)
                self.play(FadeIn(mcs[k_]), FadeOut(cur), Transform(curl, lab[k_]), run_time=0.8)
                cur = mcs[k_]
            vo.wait_until("x")
            self.play(FadeIn(exact), FadeIn(el), FadeIn(errl), FadeIn(kak))
        with self.voiceover(
            "So there are two bridges between random paths and partial differential equations. Fokker–Planck pushes "
            "densities forward in time. Kolmogorov and Feynman–Kac pull averages backward. Both come straight out of Itô's "
            "lemma."
        ):
            pass
        self.wait(0.3)
        self.clear_scene()

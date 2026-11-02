from __future__ import annotations

import numpy as np

from explainer.quant import *  # noqa: F403
from videos.quant.quant8.common import ALT, KELLY, PART, UNDER, VALUE, illustration, load


class Bellman(VoiceoverScene, ThreeDScene):
    def construct(self):
        b = load("bellman")
        sw = load("bellman_sweep")
        self.card()
        self.recursion()
        self.lab(b, sw)
        self.replay(sw)
        self.policy(b)

    def card(self):
        c = chapter_card(2, r"Bellman's principle: solving backwards", r"How do you decide when tomorrow you decide "
                         r"again?", lit=(1957,), part=PART)
        with self.voiceover("Chapter two. Bellman's principle: solving a problem backwards."):
            self.play(FadeIn(c[0], shift=UP * 0.2), FadeIn(c[1]))
        self.play(FadeOut(c))

    def recursion(self):
        # a three-period tree, values flowing back from the end
        cols = []
        for n in range(4):
            cols.append([np.array([-5.6 + 1.25 * n, 0.55 * (2 * j - n) - 0.6, 0]) for j in range(n + 1)])
        edges = VGroup(*[Line(cols[n][j], cols[n + 1][j + k], color=GREY_D, stroke_width=1.5)
                         for n in range(3) for j in range(n + 1) for k in (0, 1)])
        nodes = [VGroup(*[Dot(p, radius=0.09, color=GREY_B) for p in col]) for col in cols]
        tags = VGroup(*[label(t, font_size=18, color=GREY_B).next_to(cols[n][0], DOWN, buff=0.35)
                        for n, t in enumerate((r"today", r"$n = 1$", r"$n = 2$", r"end: $u(W)$"))])
        rows = [cmath(r"V_n(w)", r"=", r"\max_{\pi}\ \mathbb{E}\Big[V_{n+1}\big(w\,(1 + r\Delta + \pi(R - r\Delta))\big)"
                      r"\Big]", font_size=30, colors={r"V_n(w)": VALUE}),
                cmath(r"V_{n+1}(w)", r"=", r"v_{n+1}\,\frac{w^{1-\gamma}}{1-\gamma}", font_size=30,
                      colors={r"V_{n+1}(w)": VALUE}),
                cmath(r"V_n(w)", r"=", r"v_{n+1}\, w^{1-\gamma}\ \max_{\pi}\ \mathbb{E}\Big[\frac{(1 + r\Delta + \pi(R - "
                      r"r\Delta))^{1-\gamma}}{1-\gamma}\Big]", font_size=30, colors={r"V_n(w)": VALUE}),
                cmath(r"\pi^*_n(w)", r"=", r"\pi^*\quad\text{the same at every } w \text{ and } n", font_size=30,
                      colors={r"\pi^*_n(w)": KELLY})]
        whys = [why(r"principle of optimality (Bellman 1957): whatever today's choice, act optimally from wherever it "
                    r"leads; so the value today is the best expected value tomorrow", font_size=21),
                why(r"guess: power utility at the end, so try a power at every step", font_size=21),
                why(r"substitute: wealth factors out of the maximum, because $(wG)^{1-\gamma} = w^{1-\gamma} "
                    r"G^{1-\gamma}$", font_size=21),
                why(r"so the best fraction is myopic: it ignores wealth and the horizon (Mossin 1968; Samuelson "
                    r"1969)", font_size=21)]
        for r_ in rows:
            r_.scale(0.95)
        step = ladder(self, rows, whys, keep=4, top=3.3, x=1.2, buff=0.45, edge=6.9)
        with self.voiceover(
            "Most decisions are made again tomorrow, with whatever today's choice led to. Bellman's principle of "
            "optimality, from 1957: an optimal plan stays optimal from wherever it has led. So start at the end, where the "
            "value is just utility, and work backwards. <bookmark mark='a'/> At each node, try every fraction, average the "
            "next value over what the stock might do, and keep the best. <bookmark mark='b'/> With power utility, guess that "
            "tomorrow's value is a power of wealth too. <bookmark mark='c'/> Wealth factors out of the maximum. "
            "<bookmark mark='d'/> So the best fraction is the same at every wealth and date: the investor is myopic, as "
            "Mossin and Samuelson proved in 1968 and 1969."
        ) as vo:
            self.play(Create(edges), *[FadeIn(nd) for nd in nodes], FadeIn(tags), run_time=1.5)
            step(0)
            vo.wait_until("a")
            for n in range(3, -1, -1):
                self.play(nodes[n].animate.set_color(VALUE), run_time=0.45)
            vo.wait_until("b")
            step(1)
            vo.wait_until("c")
            step(2)
            vo.wait_until("d")
            step(3)
            self.play(*[nd.animate.set_color(KELLY) for nd in nodes], run_time=0.6)
        self.wait(0.4)
        self.clear_scene()

    def lab(self, b, sw):
        card = lab_card(r"Merton by dynamic programming", [
            "def bellman_merton(mu, r, sigma, gamma, T, steps, floor, ...):",
            "    z, wq = hermegauss(15)                       # quadrature nodes",
            "    R = exp((mu - sigma**2/2)*dt + sigma*sqrt(dt)*z) - 1",
            "    for n in range(steps - 1, -1, -1):           # backwards",
            "        w = cgrid + pv[n]                        # wealth grid",
            "        gross = 1 + r*dt + pis*(R - r*dt)        # every pi, node",
            "        c_next = w * gross - pv[n + 1]",
            "        val = crra(exp(interp(log(c_next), lg, lce)), gamma)",
            "        ev = val @ wq                            # E[V_{n+1}]",
            "        k = argmax(ev, axis=1)                   # best pi",
            "        V_next, out_pi[n] = ev[:, k], pis[k]",
        ], source="explainer/quant/house/control.py", width=8.6, font_size=18).to_edge(UP, buff=0.3)
        m = sw["merton"]
        p0 = np.asarray(m["pi"])[0]
        f = b["floor"]
        gap = float(np.nanmax(np.abs(np.asarray(f["pi"]) - np.asarray(f["pi_closed"]))))
        with self.voiceover(
            "Lab one: the House's solver, for a stock with eight percent expected return and eighteen percent volatility, a "
            "bond at two, and gamma three over ten years. It steps backwards a month at a time, tries a hundred and "
            "fifty-one fractions at every wealth on its grid, and keeps the best. <bookmark mark='a'/> Run it. Without a "
            f"floor it chooses {100 * p0.min():.0f} to {100 * p0.max():.0f} percent across the grid: Merton's "
            f"{100 * sw['pi_merton']:.1f}, to the grid's step."
        ) as vo:
            self.play(FadeIn(card, shift=UP * 0.2))
            vo.wait_until("a")
            lab_run(self, card, ["bellman_merton(0.08, 0.02, 0.18, 3.0, T=10, steps=120)",
                                 f"pi at t=0: min {p0.min():.2f}  max {p0.max():.2f}   Merton {sw['pi_merton']:.4f}",
                                 f"with floor 0.6: largest gap to closed form {gap:.3f}"])
        self.wait(0.4)
        self.clear_scene()

    def replay(self, sw):
        f = sw["floor"]
        t, w = np.asarray(f["t"]), np.asarray(f["w"])
        P, EV = np.asarray(f["pi"]), np.asarray(f["ev"])
        pis = np.asarray(sw["pis"])
        ax = ThreeDAxes(x_range=[0.65, 3.0, 0.5], y_range=[0, 10, 2], z_range=[0, 0.8, 0.2], x_length=7.0,
                        y_length=5.0, z_length=3.2, tips=False,
                        axis_config={"stroke_color": GREY_C, "include_ticks": False, "stroke_width": 2})
        ax.shift(LEFT * 1.6 + DOWN * 0.6)

        def slab(k):
            k2 = min(k + 1, len(t) - 1)
            t_hi = t[k2] if k2 > k else 10.0
            return Surface(lambda u, v: ax.c2p(u, v, float(np.interp(u, w, P[k]) + (np.interp(u, w, P[k2]) - np.interp(
                u, w, P[k])) * (v - t[k]) / max(t_hi - t[k], 1e-9))), u_range=[0.65, 3.0], v_range=[t[k], t_hi],
                resolution=(24, 1), fill_opacity=0.85, stroke_width=0.4, stroke_color=GREY_D,
                checkerboard_colors=[interpolate_color(ManimColor(UNDER), ManimColor(VALUE), float(t[k] / 10))] * 2)

        plane = Surface(lambda u, v: ax.c2p(u, v, sw["pi_merton"]), u_range=[0.65, 3.0], v_range=[0, 10],
                        resolution=(2, 2), fill_color=KELLY, fill_opacity=0.15, stroke_width=0.6, stroke_color=KELLY)
        # the inset: E[V_{n+1}] against pi at wealth 1, scaled to [0, 1]; its peak is the decision
        ig = axes([0, 1.5], [0, 1.1], x_length=3.4, y_length=2.0, xlabel=r"fraction $\pi$ at wealth 1",
                  ylabel=r"$\mathbb{E}[V_{n+1}]$", xticks=[0, 0.5, 1, 1.5], xfmt=lambda u: f"{100 * u:.0f}\\%",
                  yticks=[], font_size=14).to_corner(UR, buff=0.45)

        def inset(k):
            e = EV[k]
            y = (e - e.min()) / max(e.max() - e.min(), 1e-12)
            j = int(np.argmax(e))
            return VGroup(curve(ig.ax, pis, y, VALUE, stroke_width=3), Dot(ig.ax.c2p(pis[j], 1.0), color=KELLY),
                          MathTex(rf"t = {t[k]:.1f}:\ \pi^* = {100 * pis[j]:.0f}\%", font_size=24, color=KELLY).next_to(
                              ig, DOWN, buff=0.15))

        hint = VGroup(label(r"wealth", font_size=20, color=UNDER), label(r"years (of 10)", font_size=20, color=GREY_A),
                      label(r"fraction in stocks", font_size=20, color=VALUE)).arrange(DOWN, aligned_edge=LEFT,
                                                                                      buff=0.1).to_corner(DL, buff=0.4)
        params = note(r"$\gamma = 3$; a floor of 0.6 at year 10; built backwards, half a year per slab", font_size=18
                      ).to_corner(DR, buff=0.3)
        self.set_camera_orientation(phi=64 * DEGREES, theta=-58 * DEGREES, zoom=0.85)
        cur = inset(len(t) - 1)
        self.add_fixed_in_frame_mobjects(ig, cur, hint, params)
        self.remove(ig, cur, hint, params)
        last = len(t) - 1
        with self.voiceover(
            "Now add a floor: the investor must end ten years with at least sixty cents of every starting dollar. The "
            "surface is the solver's decision at every wealth and date, built the way it is computed: backwards from year "
            "ten, slab by slab. <bookmark mark='a'/> The inset is the slab's choice at a wealth of one: next period's "
            "expected value against the fraction, a hump whose peak is the decision. It walks from "
            f"{100 * f['best_at_1'][last]:.0f} percent near the deadline to {100 * f['best_at_1'][0]:.0f} today. "
            "<bookmark mark='b'/> The faint plane is Merton without a floor; with it, the decision falls toward zero near "
            "the floor, more steeply as the deadline nears."
        ) as vo:
            self.play(Create(ax), FadeIn(ig), FadeIn(cur), FadeIn(hint), FadeIn(params), run_time=1.5)
            vo.wait_until("a")
            per = max(min((vo.remaining(6.0) - 4.0) / len(t), 0.6), 0.25)
            for k in range(last, -1, -1):
                new = inset(k)
                self.add_fixed_in_frame_mobjects(new)
                self.remove(new)
                self.play(Create(slab(k)), Transform(cur, new), run_time=per)
            vo.wait_until("b")
            self.play(FadeIn(plane))
            self.move_camera(theta=-35 * DEGREES, phi=60 * DEGREES, run_time=max(vo.remaining(1.0) - 0.5, 1.0))
        self.move_camera(phi=0, theta=-90 * DEGREES, added_anims=[FadeOut(Group(*self.mobjects))], run_time=1.5)
        self.clear_scene()

    def policy(self, b):
        f = b["floor"]
        t, w = np.asarray(f["t"]), np.asarray(f["w"])
        P, Q = np.asarray(f["pi"]), np.asarray(f["pi_closed"])
        g = axes([0.6, 3.0], [0, 0.8], x_length=7.4, y_length=4.4, xlabel=r"wealth", ylabel=r"fraction in stocks",
                 xticks=[0.6, 1, 1.5, 2, 2.5, 3], yticks=[0, 0.2, 0.4, 0.6, 0.8], yfmt=lambda u: f"{100 * u:.0f}\\%",
                 font_size=18).to_edge(LEFT, buff=0.7).shift(DOWN * 0.2)
        ax = g.ax
        merton = DashedLine(ax.c2p(0.6, b["pi_merton"]), ax.c2p(3.0, b["pi_merton"]), color=KELLY, stroke_width=3)
        ml = MathTex(rf"\text{{no floor: }}\pi^* = {100 * b['pi_merton']:.0f}\%", font_size=26, color=KELLY).next_to(
            ax.c2p(3.0, b["pi_merton"]), UP, buff=0.1).shift(LEFT * 1.3)
        cols = [UNDER, ALT, VALUE]
        picks = [0, len(t) // 2, len(t) - 1]
        dots, lines, labs = VGroup(), VGroup(), VGroup()
        for c_, k in zip(cols, picks):
            ok = w >= 0.62
            lines.add(curve(ax, w[ok], Q[k][ok], c_, stroke_width=3))
            dots.add(VGroup(*[Dot(ax.c2p(x, y), radius=0.04, color=WHITE) for x, y in zip(w[ok][::3], P[k][ok][::3])]))
            labs.add(label(rf"year {t[k]:.1f}", font_size=19, color=c_))
        labs.arrange(DOWN, aligned_edge=LEFT, buff=0.1).next_to(g, RIGHT, buff=0.2).align_to(g, DOWN).shift(UP * 0.6)
        side = VGroup(
            MathTex(r"\pi^*(t, w) = \frac{\mu - r}{\gamma\sigma^2}\cdot\frac{w - F e^{-r(T - t)}}{w}", font_size=30),
            wrapped_label(r"lines: the closed form (portfolio insurance: Merton's fraction of the cushion above the "
                          r"floor's present value); dots: the grid solver", 4.2, 20, GREY_A),
            label(rf"largest gap: {np.nanmax(np.abs(P - Q)):.3f}", font_size=22, color=GREY_B),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.25).to_corner(UR, buff=0.4)
        q = pause_card(r"As the deadline nears with wealth just above the floor, does the stock fraction rise or fall?",
                       width=5.0, font_size=21).to_corner(DR, buff=0.35)
        with self.voiceover(
            "Slice it at three dates. <bookmark mark='a'/> The solver invests Merton's fraction of the cushion, the wealth "
            "above what the floor costs today. Pause and predict: near the deadline, just above the floor, does the "
            "fraction rise or fall? <bookmark mark='b'/> It falls: the cushion shrinks, and so does the bet. "
            "<bookmark mark='c'/> The lines are the closed form, portfolio insurance; the dots, the solver, which never saw "
            f"it. They differ by at most {np.nanmax(np.abs(P - Q)):.3f}."
        ) as vo:
            self.play(FadeIn(g), Create(merton), FadeIn(ml))
            vo.wait_until("a")
            self.play(FadeIn(side[0]), FadeIn(q))
            vo.wait_until("b")
            self.play(FadeOut(q), LaggedStart(*[Create(l_) for l_ in lines], lag_ratio=0.4), FadeIn(labs), run_time=3)
            vo.wait_until("c")
            self.play(LaggedStart(*[FadeIn(d_) for d_ in dots], lag_ratio=0.3), FadeIn(side[1]), FadeIn(side[2]))
        self.wait(0.4)
        self.clear_scene()

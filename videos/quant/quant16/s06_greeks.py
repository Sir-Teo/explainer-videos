from __future__ import annotations

import numpy as np
from scipy.interpolate import RegularGridInterpolator

from explainer.quant import *  # noqa: F403
from videos.quant.quant16.common import BAD, DELTA, GOOD, OPT, PART, SPOT, fixed, illustration, load, predict


class Greeks(VoiceoverScene, ThreeDScene):
    def construct(self):
        g = load("greeks")
        b = load("bump_h")
        self.card()
        self.valley(b)
        self.proof()
        self.three(g)
        self.digital(g)

    def card(self):
        c = chapter_card(10, r"Greeks three ways", r"How do you differentiate a simulation?", lit=(1996,), part=PART)
        with self.voiceover("Chapter ten. Greeks, three ways."):
            self.play(FadeIn(c[0], shift=UP * 0.2), FadeIn(c[1]))
        self.play(FadeOut(c))

    def valley(self, b):
        hs, ns = np.log10(b["hs"]), np.log10(b["ns"])
        Zi = np.log10(np.asarray(b["indep"]))
        Zc = np.log10(np.asarray(b["crn"]))
        ax = ThreeDAxes(x_range=[-2, 1.5, 1], y_range=[3, 5, 1], z_range=[-2.5, 1.2, 1], x_length=6.5, y_length=4.5,
                        z_length=3.4, tips=False, axis_config={"stroke_color": GREY_C, "include_ticks": False,
                                                               "stroke_width": 2})
        ax.shift(DOWN * 0.5)

        def surf(Z, colors):
            f = RegularGridInterpolator((ns, hs), np.clip(Z, -2.5, 1.2))
            s = Surface(lambda u, v: ax.c2p(u, v, float(f((v, u)))), u_range=[hs[0], hs[-1]], v_range=[ns[0], ns[-1]],
                        resolution=(28, 12), fill_opacity=0.85, stroke_width=0.4, stroke_color="#0E1117",
                        checkerboard_colors=False)
            s.set_fill_by_value(axes=ax, colorscale=list(zip(colors, [-2.3, -1, 0.8])), axis=2)
            return s

        si = surf(Zi, [QC.GAIN, QC.DELTA, QC.LOSS])
        sc = surf(Zc, [QC.GAIN, QC.DELTA, QC.LOSS])
        hint = VGroup(label(r"across: the bump $h$ (log, $0.01$ to $30$)", font_size=21, color=GREY_A),
                      label(r"back: paths $n$ (log, $10^3$ to $10^5$)", font_size=21, color=GREY_A),
                      label(r"up: error of the bumped delta (log)", font_size=21, color=GREY_A)).arrange(
            DOWN, aligned_edge=LEFT, buff=0.1).to_corner(UL, buff=0.35)
        t_i = label(r"independent random numbers at $S_0 \pm h$", font_size=26, color=BAD).to_corner(UR, buff=0.4)
        t_c = label(r"common random numbers", font_size=26, color=GOOD).to_corner(UR, buff=0.4)
        k = 2
        nums_i = MathTex(rf"n = 10^4:\ \ h = 0.01 \to {b['indep'][k][0]:.1f},\ \ \text{{best}}\ {min(b['indep'][k]):.3f}",
                         font_size=26, color=BAD).to_corner(DR, buff=0.4)
        nums_c = MathTex(rf"n = 10^4:\ \ {b['crn'][k][0]:.4f}\ \text{{from}}\ h = 0.01\ \text{{to}}\ 3;\ \ "
                         rf"{b['crn'][k][-1]:.3f}\ \text{{at}}\ 30", font_size=26, color=GOOD).to_corner(DR, buff=0.4)
        self.set_camera_orientation(phi=65 * DEGREES, theta=-60 * DEGREES, zoom=0.85)
        fixed(self, hint, t_i, t_c, nums_i, nums_c)
        with self.voiceover(
            "The simplest Greek: bump the spot up and down by h, reprice, and take the difference. How big should h "
            "be? Here is the error of that delta, over thirty seeds, for every bump size and every number of paths. "
            "<bookmark mark='a'/> With fresh random numbers for the two prices, the surface is a valley. On the left "
            "wall, small bumps divide the noise by a tiny h and the error explodes; on the right wall, large bumps "
            "are biased. The floor slopes down as paths grow, and the best bump sits in between. "
            "<bookmark mark='b'/> Now use the same random numbers for both prices. The left wall collapses. The two "
            "prices' noise cancels, and the error is flat, for any small bump, until the bias of a huge one returns."
        ) as vo:
            self.play(Create(ax), FadeIn(hint), run_time=1.5)
            vo.wait_until("a")
            self.play(Create(si), FadeIn(t_i), FadeIn(nums_i), run_time=2)
            self.move_camera(theta=-30 * DEGREES, run_time=3)
            vo.wait_until("b")
            self.play(ReplacementTransform(si, sc), FadeOut(t_i), FadeIn(t_c), FadeOut(nums_i), FadeIn(nums_c), run_time=2.5)
            self.move_camera(theta=-80 * DEGREES, phi=70 * DEGREES, run_time=max(vo.remaining(0.5), 2))
        self.move_camera(phi=0, theta=-90 * DEGREES, added_anims=[FadeOut(VGroup(ax, sc)), FadeOut(hint), FadeOut(t_c),
                                                                  FadeOut(nums_c)], run_time=1.5)
        self.clear_scene()

    def proof(self):
        rows = [
            cmath(r"\frac{\hat V(\theta + h) - \hat V(\theta - h)}{2h}", r"-\ V'", r"= \frac{h^2}{6}V''' + "
                  r"\text{noise},\quad \operatorname{Var} = \frac{\operatorname{Var}(Y_+ - Y_-)}{4nh^2}", font_size=30),
            cmath(r"\Delta", r"=", r"\mathbb{E}\Big[e^{-rT}\,\mathbf{1}_{S_T > K}\,\frac{S_T}{S_0}\Big]", font_size=34,
                  colors={r"\Delta": GOOD}),
            cmath(r"\frac{\partial}{\partial\theta}\int f\,p_\theta", r"=", r"\mathbb{E}\big[f(X)\,\partial_\theta \log "
                  r"p_\theta(X)\big],\quad \partial_{S_0}\log p = \frac{Z}{S_0\sigma\sqrt T}", font_size=32,
                  colors={r"=": OPT}),
            cmath(r"\Delta", r"=", r"\mathbb{E}\Big[e^{-rT} f(S_T)\,\frac{W_T}{S_0\,\sigma\,T}\Big]", font_size=34,
                  colors={r"\Delta": QC.Q}),
        ]
        whys = [why(r"Taylor: bias $h^2$. Independent draws: $\operatorname{Var}(Y_+ - Y_-) = O(1)$, so the best $h \sim "
                    r"n^{-1/6}$ and error $\sim n^{-1/3}$; common numbers and a Lipschitz payoff: $O(h^2)$, error "
                    r"$n^{-1/2}$ for any small $h$"),
                why(r"pathwise: differentiate inside the expectation ($\partial S_T/\partial S_0 = S_T/S_0$; the payoff "
                    r"is Lipschitz, so dominated convergence allows it)"),
                why(r"likelihood ratio: differentiate the density, never the payoff (Broadie and Glasserman 1996); "
                    r"for $\sigma$: $\frac{Z^2 - 1}{\sigma} - Z\sqrt T$"),
                why(r"Malliavin weights (Fourni\'e, Lasry, Lebuchoux, Lions and Touzi 1999): integration by parts on "
                    r"Wiener space; works for path-dependent payoffs with no known density")]
        step = ladder(self, rows, whys, keep=4, top=2.9, x=-0.4, buff=0.6, edge=6.9)
        with self.voiceover(
            "The valley in symbols. A central bump has bias of order h squared, and with independent numbers a "
            "variance of order one over n h squared, so the best bump shrinks like n to the minus a sixth and the "
            "error only like n to the minus a third. Common numbers kill the h squared in the denominator. "
            "<bookmark mark='a'/> The second way skips the bump: differentiate the payoff along each path; for a call, "
            "delta is the discounted indicator times the stock's growth ratio. <bookmark mark='b'/> The third differentiates the "
            "density instead: the payoff times the derivative of the log density, the score. <bookmark mark='c'/> And "
            "Malliavin calculus, brought to finance by Fournié, Lasry, Lebuchoux, Lions and Touzi in 1999, finds such "
            "weights by integrating by parts on the space of paths, even when no density is known."
        ) as vo:
            for i, mk in enumerate("abc"):
                step(i)
                vo.wait_until(mk)
            step(3)
        self.wait(0.4)
        self.clear_scene()

    def three(self, g):
        ex = g["exact"]
        head = VGroup(label(r"", font_size=20), label(r"call: delta", font_size=21, color=GREY_A),
                      label(r"digital: delta", font_size=21, color=GREY_A))
        rows = [(r"bump and reprice", "bump", BAD), (r"pathwise", "pathwise", GOOD), (r"likelihood ratio", "likelihood ratio", OPT)]
        tab = VGroup(VGroup(VectorizedPoint(), head[1], head[2]))
        for name, key, col in rows:
            c = g["call"].get(key)
            d = g["digital"].get(key)
            cells = [label(name, font_size=22, color=col)]
            cells.append(MathTex(rf"{c['delta']:.4f} \pm {c['delta_se']:.4f}", font_size=26) if c else MathTex(r"-", font_size=26))
            cells.append(MathTex(rf"{d['delta']:.5f} \pm {d['delta_se']:.5f}", font_size=26) if d else
                         label(r"fails: the payoff jumps", font_size=19, color=BAD))
            tab.add(VGroup(*cells))
        tab.add(VGroup(label(r"exact", font_size=22, color=GREY_A), MathTex(f"{ex['call']['delta']:.4f}", font_size=26, color=GREY_A),
                       MathTex(f"{ex['digital']['delta']:.5f}", font_size=26, color=GREY_A)))
        xs = [-4.2, 0.2, 4.0]
        for i, row in enumerate(tab):
            for j, cell in enumerate(row):
                cell.move_to([xs[j], 2.3 - 0.75 * i, 0])
        ratio = g["digital"]["bump"]["delta_se"] / g["digital"]["likelihood ratio"]["delta_se"]
        foot = wrapped_label(rf"for the digital, the likelihood ratio's standard error is {ratio:.1f} times smaller than "
                             r"the bump's (bump $h = 1$, common numbers)", 11.6, 20, GREY_A).to_edge(DOWN, buff=0.9)
        src = illustration(r"200{,}000 paths; one-year at-the-money call and cash-or-nothing digital", corner=UR)
        with self.voiceover(
            "All three on two products, with two hundred thousand paths. For the call they agree with the exact "
            "delta; the bump with common numbers and the pathwise method are equally precise, and the likelihood "
            "ratio is noisier. <bookmark mark='a'/> For a digital, which pays one above the strike, the pathwise "
            "derivative is zero almost everywhere: it fails. The likelihood ratio never touches the payoff, and its "
            f"standard error is {ratio:.1f} times smaller than the bump's."
        ) as vo:
            self.play(FadeIn(tab[0]), FadeIn(tab[1]), FadeIn(tab[2]), FadeIn(tab[3]), FadeIn(tab[4]), FadeIn(src))
            vo.wait_until("a")
            self.play(FadeIn(foot))
        self.wait(0.4)
        self.clear_scene()

    def digital(self, g):
        ga = axes([70, 130], [-0.2, 1.3], x_length=5.0, y_length=3.0, xlabel=r"$S_T$", ylabel=r"digital payoff and its slope",
                  xticks=[80, 100, 120], yticks=[0, 1], font_size=14).to_edge(LEFT, buff=0.7).shift(UP * 0.6)
        ax = ga.ax
        step = VGroup(Line(ax.c2p(70, 0), ax.c2p(100, 0), stroke_color=OPT, stroke_width=4),
                      Line(ax.c2p(100, 1), ax.c2p(130, 1), stroke_color=OPT, stroke_width=4))
        slope = VGroup(Line(ax.c2p(70, 0.02), ax.c2p(130, 0.02), stroke_color=GOOD, stroke_width=3),
                       Arrow(ax.c2p(100, 0), ax.c2p(100, 1.25), buff=0, stroke_width=3, color=BAD, tip_length=0.15))
        cap1 = wrapped_label(r"pathwise sees the green slope: zero everywhere it exists. The red spike at the strike, "
                             r"a delta function, is exactly what it misses", 5.4, 18, GREY_A).next_to(ga, DOWN, buff=0.3)
        z = np.linspace(-3, 3, 200)
        gb = axes([-3, 3], [-1.2, 1.2], x_length=5.0, y_length=3.0, xlabel=r"the normal $Z$",
                  ylabel=r"likelihood-ratio weight $Z/(S_0\sigma\sqrt T)$, scaled", xticks=[-2, 0, 2], yticks=[-1, 0, 1],
                  font_size=14).to_edge(RIGHT, buff=0.7).shift(UP * 0.6)
        w = curve(gb.ax, z, z / 3, QC.Q, stroke_width=3)
        cap2 = wrapped_label(r"the likelihood ratio multiplies the payoff by this weight instead: no derivative of the "
                             r"payoff anywhere. Gamma of a call needs the same trick (pathwise once, then the ratio: "
                             r"problem 6)", 5.4, 18, GREY_A).next_to(gb, DOWN, buff=0.3)
        q = predict(r"Bump with $h = 0.0001$ and fresh random numbers. What do you get?", width=5.6,
                    font_size=21).to_edge(DOWN, buff=0.25)
        with self.voiceover(
            "Why pathwise fails for the digital, in one picture. The payoff is a step. Along any path its slope is "
            "zero, except at the strike, where it is infinite, and a simulation never lands exactly there. "
            "<bookmark mark='a'/> The likelihood ratio moves the derivative onto the density: each path's payoff is "
            "multiplied by a weight that is linear in its normal. Gamma of a call has the same problem, one level "
            "up, and the same cure. <bookmark mark='b'/> Pause and predict: a bump of one ten-thousandth with fresh "
            "random numbers. You get noise: the error grows like one over h, the left wall of the valley."
        ) as vo:
            self.play(FadeIn(ga), Create(step), FadeIn(slope), FadeIn(cap1))
            vo.wait_until("a")
            self.play(FadeIn(gb), Create(w), FadeIn(cap2))
            vo.wait_until("b")
            self.play(FadeIn(q))
        self.wait(0.5)
        self.clear_scene()

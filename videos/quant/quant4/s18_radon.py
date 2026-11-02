from __future__ import annotations

import numpy as np

from explainer.quant import *  # noqa: F403
from videos.quant.quant4.common import DRIFT, LOSS, MART, P_C, PART, Q_C, load


class Radon(VoiceoverScene, ThreeDScene):
    def construct(self):
        r = load("radon")
        k = load("kakutani")
        self.card()
        self.derive()
        self.city(r)
        self.kakutani(k)

    def card(self):
        c = chapter_card(13, r"Radon--Nikodym, and the singular infinite", r"When can one probability be rewritten as "
                         r"another?", part=PART)
        with self.voiceover("Chapter thirteen. Radon-Nikodym, and the singular infinite."):
            self.play(FadeIn(c[0], shift=UP * 0.2), FadeIn(c[1]))
        self.play(FadeOut(c))

    def derive(self):
        rows = [cmath(r"Q \ll P", r"\Rightarrow", r"\exists\, L \ge 0:\ Q(A) = \mathbb{E}_P[L\,\mathbf{1}_A]", font_size=38,
                      colors={r"\exists\, L \ge 0:\ Q(A) = \mathbb{E}_P[L\,\mathbf{1}_A]": MART}),
                cmath(r"Z_n(\omega)", r"=", r"\frac{Q(I_n(\omega))}{P(I_n(\omega))}, \quad "
                      r"\mathbb{E}_P[Z_{n+1} \mid \mathcal{F}_n] = Z_n", font_size=38),
                cmath(r"Z_n \ge 0", r"\Rightarrow", r"Z_n \to Z_\infty; \quad Q \ll P \Rightarrow \text{UI} \Rightarrow "
                      r"Z_\infty = \frac{dQ}{dP}", font_size=38, colors={r"Z_n \ge 0": MART}),
                cmath(r"P \sim Q", r":", r"\text{the same null sets; an arbitrage is defined by null sets alone}",
                      font_size=36),
                cmath(r"\prod_k \rho_k > 0 \Rightarrow P \sim Q,", r"\quad",
                      r"\prod_k \rho_k = 0 \Rightarrow P \perp Q, \quad \rho_k = \sqrt{p_k q_k} + \sqrt{(1-p_k)(1-q_k)}",
                      font_size=34, colors={r"\prod_k \rho_k > 0 \Rightarrow P \sim Q,": MART})]
        whys = [why(r"Radon (1913), Nikodym (1930): if $Q$ gives no weight to what $P$ calls impossible, $Q$ has a "
                    r"density with respect to $P$"),
                why(r"on the dyadic grid of chapter 1: a cell's two children carry the parent's $Q$-mass between them"),
                why(r"a nonnegative martingale converges (chapter 10); absolute continuity makes it uniformly integrable "
                    r"(Williams, ch.\ 14)"),
                why(r"equivalence: absolutely continuous both ways; ``$V_0 = 0$, $V_T \ge 0$ surely, $>0$ possibly'' "
                    r"is the same statement under every equivalent measure (Part 9)"),
                why(r"Kakutani (1948): infinite products of coins are either equivalent or mutually singular, "
                    r"nothing in between")]
        step = ladder(self, rows, whys, keep=4, top=2.9, x=-0.8, buff=0.68, edge=6.9)
        with self.voiceover(
            "When can one probability be written as another, reweighted? The Radon-Nikodym theorem: whenever Q gives "
            "no weight to anything P calls impossible, Q has a density with respect to P. <bookmark mark='a'/> "
            "Martingales prove it. On the dyadic cells of chapter one, take the ratio of Q's mass to P's. A cell's "
            "two children share the parent's Q-mass, so the ratio is a P-martingale. <bookmark mark='b'/> It is "
            "nonnegative, so it converges, by chapter ten; absolute continuity makes it uniformly integrable, and "
            "the limit is the density. <bookmark mark='c'/> Measures absolutely continuous both ways are "
            "equivalent: they share their impossible events, and an arbitrage is defined by impossible events alone, "
            "so equivalent measures agree on it. <bookmark mark='d'/> On infinite coin sequences there is a sharp "
            "dichotomy, Shizuo Kakutani's of 1948: equivalent or completely singular, as a product of affinities "
            "stays positive or not."
        ) as vo:
            step(0)
            vo.wait_until("a")
            step(1)
            vo.wait_until("b")
            step(2)
            vo.wait_until("c")
            step(3)
            vo.wait_until("d")
            step(4)
        self.wait(0.4)
        self.clear_scene()

    def city(self, r):
        ax = ThreeDAxes(x_range=[0, 1, 0.5], y_range=[0, 1, 0.5], z_range=[0, 2.2, 1], x_length=5.0, y_length=5.0,
                        z_length=3.0, axis_config={"stroke_color": GREY_C, "include_ticks": False, "include_tip": False})
        ax.shift(DOWN * 0.6 + LEFT * 1.0)
        L = r["levels"]
        cmap = [QC.SPOT, MART, QC.IDEA, Q_C]

        def bars(Z, zmax=2.2, color_by=True):
            Z = np.asarray(Z, float)
            k = Z.shape[0]
            grp = VGroup()
            for i in range(k):
                for j in range(k):
                    h = float(min(Z[i, j], zmax))
                    if h <= 1e-6:
                        continue
                    col = interpolate_color(ManimColor(QC.SPOT), ManimColor(Q_C), min(h / zmax, 1.0)) if color_by else LOSS
                    hz = h / zmax * ax.z_length
                    pr = Prism(dimensions=[ax.x_length / k * 0.92, ax.y_length / k * 0.92, hz],
                               fill_color=col, fill_opacity=0.85, stroke_width=0.3, stroke_color=BACKGROUND)
                    pr.move_to(ax.c2p((i + 0.5) / k, (j + 0.5) / k, 0) + OUT * hz / 2)
                    grp.add(pr)
            return grp

        cur = bars(L["1"])
        surf = Surface(lambda u, v: ax.c2p(u, v, (1 + 2 * u * v) / 1.5), u_range=[0, 1], v_range=[0, 1],
                       resolution=(16, 16), fill_opacity=0.75, checkerboard_colors=[Q_C, MART], stroke_width=0.3)
        head = label(r"$P$ uniform on the square; $Q$ with density $(1 + 2xy)/1.5$", font_size=24,
                     color=GREY_A).to_edge(UP, buff=0.3)
        side = VGroup(
            label(r"bar height $= Q(\text{cell}) / P(\text{cell})$", font_size=22, color=Q_C),
            MathTex(r"2 \times 2 \to 4 \times 4 \to \dots \to 16 \times 16", font_size=28),
            label(rf"each parent is the average of its four children (to {r['martingale_err']:.0e})", font_size=19,
                  color=GREY_B),
            label(r"singular $Q$ (all its mass on the diagonal): bars $2^n$ high on the diagonal, 0 elsewhere",
                  font_size=19, color=LOSS),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.2).to_corner(DR, buff=0.35)
        for s_ in side:
            if s_.width > 5.0:
                s_.scale_to_fit_width(5.0)
        for mob in (head, side):
            self.add_fixed_in_frame_mobjects(mob)
            self.remove(mob)
        self.set_camera_orientation(phi=62 * DEGREES, theta=-50 * DEGREES, zoom=0.85)
        with self.voiceover(
            "Watch the density appear. P spreads probability evenly over a square; Q leans toward the far corner. On "
            "a two by two grid, each bar's height is Q's mass in the cell divided by P's. <bookmark mark='a'/> Split "
            "every cell into four: four by four, eight by eight, sixteen by sixteen. Each bar becomes four, and the "
            "four average to their parent: that is the martingale. The city of bars smooths into a surface, the "
            "Radon-Nikodym derivative. <bookmark mark='b'/> Now try a Q that puts all its mass on the diagonal. P "
            "gives the diagonal zero area, so Q is not absolutely continuous. The bars along the diagonal double at "
            "every split, the rest fall to zero, and no surface ever forms. Q and P are singular: each lives where "
            "the other says nothing can happen."
        ) as vo:
            self.play(Create(ax), FadeIn(head), FadeIn(side[0]))
            self.play(FadeIn(cur))
            vo.wait_until("a")
            self.play(FadeIn(side[1]))
            for lev in ("2", "3", "4"):
                self.play(Transform(cur, bars(L[lev])), run_time=1.6)
            self.play(FadeIn(side[2]))
            self.begin_ambient_camera_rotation(rate=0.12)
            self.play(FadeOut(cur), FadeIn(surf), run_time=2)
            vo.wait_until("b")
            self.stop_ambient_camera_rotation()
            self.play(FadeOut(surf), FadeIn(side[3]))
            sing = None
            for n in range(1, 5):
                k = 2 ** n
                Z = np.zeros((k, k))
                np.fill_diagonal(Z, float(k))
                nb = bars(Z, zmax=16.0, color_by=False)
                if sing is None:
                    sing = nb
                    self.play(FadeIn(sing))
                else:
                    self.play(Transform(sing, nb), run_time=1.2)
        self.wait(0.4)
        self.clear_scene()
        self.set_camera_orientation(phi=0, theta=-90 * DEGREES, zoom=1.0)

    def kakutani(self, k):
        C, F = k["constant"], k["fading"]
        PC, PF = np.asarray(C["paths"], float), np.asarray(F["paths"], float)
        x = np.arange(PC.shape[1]) * 20
        g1 = axes([0, 10000], [-100, 5], x_length=5.6, y_length=3.6, xlabel=r"tosses of a fair coin",
                  ylabel=r"$\log_{10} L_n$, $Q$: heads 60\% every toss", xticks=[0, 5000, 10000], yticks=[-100, -50, 0],
                  font_size=15)
        g2 = axes([0, 10000], [-1.5, 1.5], x_length=5.6, y_length=3.6, xlabel=r"tosses of a fair coin",
                  ylabel=r"$\log_{10} L_n$, $Q$: heads $\tfrac12 + 0.2/k$", xticks=[0, 5000, 10000],
                  yticks=[-1, 0, 1], font_size=15)
        VGroup(g1, g2).arrange(RIGHT, buff=0.9).to_edge(UP, buff=0.8)
        tk = ValueTracker(0.0)
        f1 = VGroup(*[tracing(g1.ax, x, row, tk, LOSS, stroke_width=1.2) for row in PC[:30]])
        f2 = VGroup(*[tracing(g2.ax, x, np.clip(row, -1.5, 1.5), tk, MART, stroke_width=1.2) for row in PF[:30]])
        r1 = VGroup(MathTex(rf"\text{{median }} \log_{{10}} L_{{10{{,}}000}} = {C['median_log10']:.1f}", font_size=26,
                            color=LOSS),
                    MathTex(rf"\textstyle\prod \rho_k = 10^{{{C['log10_affinity_prod']:.1f}}} \to 0:\ P \perp Q",
                            font_size=26, color=LOSS)).arrange(DOWN, aligned_edge=LEFT, buff=0.12).next_to(g1, DOWN, buff=0.35)
        r2 = VGroup(MathTex(rf"\text{{mean }} L_{{10{{,}}000}} = {F['mean_L']:.3f};\ \text{{all }} {100 * F['frac_pos']:.0f}\% > 0",
                            font_size=26, color=MART),
                    MathTex(rf"\textstyle\prod \rho_k = {10 ** F['log10_affinity_prod']:.3f} > 0:\ P \sim Q", font_size=26,
                            color=MART)).arrange(DOWN, aligned_edge=LEFT, buff=0.12).next_to(g2, DOWN, buff=0.35)
        pred = desk_question(r"A fair coin and a 50.1\% coin, tossed forever: equivalent?",
                             r"No. Any fixed tilt is singular (the strong law tells them apart); only a tilt that "
                             r"fades fast enough, $\sum (q_k - \tfrac12)^2 < \infty$, keeps them equivalent.",
                             width=11.0, font_size=20).to_edge(DOWN, buff=0.25)
        with self.voiceover(
            "Kakutani's dichotomy, simulated. Under a fair coin, follow the likelihood ratio of a sixty-percent coin "
            "for ten thousand tosses. <bookmark mark='a'/> It collapses: the median ends near ten to the "
            f"{C['median_log10']:.0f}, as the relative entropy of point zero two a toss predicts. At every finite "
            "time the two coins are equivalent, but on the infinite sequence they are singular: the strong law of "
            "large numbers tells them apart with certainty. <bookmark mark='b'/> Now let the tilt fade: heads with "
            "probability one half plus point two over k on toss k. The squared tilts add up to something finite, the "
            "product of affinities stays positive, and the likelihood ratio settles to a positive limit, with mean "
            f"{F['mean_L']:.2f}. These two measures are equivalent forever. <bookmark mark='c'/> So is a fair coin "
            "equivalent to a fifty point one percent coin, tossed forever? No. This is why, in Part five, Girsanov "
            "changes the drift of Brownian motion only within a fixed horizon, and why no change of measure can "
            "change its volatility."
        ) as vo:
            self.play(FadeIn(g1), FadeIn(g2))
            self.add(f1, f2)
            vo.wait_until("a")
            self.play(tk.animate.set_value(float(len(x) - 1)), run_time=6, rate_func=linear)
            for m_ in (*f1, *f2):
                m_.clear_updaters()
            self.play(FadeIn(r1))
            vo.wait_until("b")
            self.play(FadeIn(r2), Indicate(g2, color=MART, scale_factor=1.02))
            vo.wait_until("c")
            self.play(FadeIn(pred, shift=UP * 0.2))
        self.wait(0.4)
        self.clear_scene()

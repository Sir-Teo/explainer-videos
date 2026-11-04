from __future__ import annotations

import numpy as np

from videos.stats.stats5.common import *  # noqa: F403

COP = {"gauss": (r"Gaussian", S.EST), "clayton": (r"Clayton", S.LIK), "gumbel": (r"Gumbel", S.POST)}


class Copulas(VoiceoverScene):
    def construct(self):
        self.card()
        self.sklar()
        self.three()
        self.recipe()
        self.crisis()

    def card(self):
        card = chapter_card(11, r"Copulas", r"Separating the margins from the dependence", lit=(), part=PART)
        with self.voiceover("Chapter eleven. Copulas."):
            self.play(FadeIn(card[0], shift=UP * 0.2), FadeIn(card[1]))
        self.play(FadeOut(card))

    def sklar(self):
        rows = [
            cmath(r"(U, V)", r"=", r"\big(F_X(X),\ F_Y(Y)\big)", font_size=34),
            cmath(r"C(u, v)", r"=", r"P(U \le u,\ V \le v)", font_size=34),
            cmath(r"F(x, y)", r"=", r"C\big(F_X(x),\ F_Y(y)\big)", font_size=38),
        ]
        rows[2][2].set_color(S.ACCENT)
        whys = [why(r"each margin uniform: \ the probability integral transform"), why(r"the copula: \ a joint law on the square"),
                why(r"Sklar (1959): \ every joint law splits this way")]
        rank = label(r"the copula keeps only the \emph{ranks}: \ Spearman and Kendall measure it (chapter 13)", font_size=24,
                     color=GREY_A).to_edge(DOWN, buff=0.7)
        with self.voiceover(
            "A joint distribution mixes two things: the shape of each variable on its own, and the way they move "
            "together. Copulas pull them apart. <bookmark mark='a'/> Pass each variable through its own CDF. Each "
            "becomes uniform: Part 3's probability integral transform. <bookmark mark='b'/> What's left is a joint "
            "distribution on the unit square, with uniform margins: the copula. <bookmark mark='c'/> Abe Sklar proved "
            "in 1959 that every joint distribution is its copula applied to its margins, so you can choose the "
            "margins and the dependence separately. <bookmark mark='d'/> The copula depends only on ranks, which is "
            "why the rank correlations of chapter thirteen are properties of it."
        ) as vo:
            step = ladder(self, rows, whys, keep=3, top=2.6, x=-0.6, buff=0.6, edge=6.9)
            for k, m in enumerate("abc"):
                vo.wait_until(m)
                step(k, transform=False)
            vo.wait_until("d")
            self.play(FadeIn(rank))
        self.clear_scene()

    def three(self):
        d = load("copulas")
        panels = VGroup()
        for k, key in enumerate(("gauss", "clayton", "gumbel")):
            nm, col = COP[key]
            c = d[key]
            uv = np.asarray(c["uv"])
            A = axes([0, 1], [0, 1], x_length=3.6, y_length=3.6, xticks=[0, 1], yticks=[0, 1], center=[-4.4 + 4.4 * k, 0.0, 0])
            ax = A.ax
            pts = scatter(ax, uv[:, 0], uv[:, 1], color=col, radius=0.016, opacity=0.6)
            lo = Square(side_length=ax.c2p(0.12, 0)[0] - ax.c2p(0, 0)[0], stroke_color=WHITE, stroke_width=1.5).move_to(ax.c2p(0.06, 0.06))
            hi = Square(side_length=ax.c2p(0.12, 0)[0] - ax.c2p(0, 0)[0], stroke_color=WHITE, stroke_width=1.5).move_to(ax.c2p(0.94, 0.94))
            t = label(nm, font_size=28, color=col).next_to(A, UP, buff=0.2)
            st = VGroup(MathTex(rf"\tau = {c['tau']:.2f}", font_size=24),
                        MathTex(rf"\text{{lower tail }} {c['lower']:.2f},\ \text{{upper }} {c['upper']:.2f}", font_size=22, color=GREY_A))
            st.arrange(DOWN, buff=0.12).next_to(A, DOWN, buff=0.25)
            panels.add(VGroup(A, pts, lo, hi, t, st))
        expl = label(r"tail number: \ $P(\text{both below } 5\%)\,/\,5\%$, \ the chance the second is extreme given the first is",
                     font_size=22, color=GREY_B).to_edge(DOWN, buff=0.35)
        if expl.width > 12.8:
            expl.width = 12.8
        tag = note(r"simulated: 4,000 draws each").to_corner(UR, buff=0.3)
        with self.voiceover(
            "Same strength of dependence, different shapes. <bookmark mark='a'/> Three copulas, each with a Kendall "
            "rank correlation of one half. The Gaussian copula is symmetric. <bookmark mark='b'/> The Clayton copula "
            "clusters tightly in the lower-left corner: when one variable is very low, the other almost always is too. "
            "<bookmark mark='c'/> The Gumbel copula does the same in the upper-right. <bookmark mark='d'/> Measure "
            "the tails directly: given that one variable is in its bottom five percent, how often is the other? For "
            f"the Gaussian about {d['gauss']['lower']:.2f}; for Clayton {d['clayton']['lower']:.2f}. And as the "
            "threshold goes further out, the Gaussian's tail dependence goes to zero, while Clayton's stays "
            "positive. The same correlation can hide very different behaviour in a crisis."
        ) as vo:
            self.play(FadeIn(tag))
            for k, m in enumerate("abc"):
                vo.wait_until(m)
                p = panels[k]
                self.play(FadeIn(p[0]), FadeIn(p[4]), FadeIn(p[1], lag_ratio=0.001), FadeIn(p[5][0]))
            vo.wait_until("d")
            self.play(*[FadeIn(p[2]) for p in panels], *[FadeIn(p[3]) for p in panels], *[FadeIn(p[5][1]) for p in panels],
                      FadeIn(expl))
        self.clear_scene()

    def crisis(self):
        hc = history_card(2000, r"David X. Li, \ ``On default correlation: \ a copula function approach''",
                          r"\emph{Journal of Fixed Income}: \ the Gaussian copula becomes the standard way to price bundles of "
                          r"mortgages and corporate debt", color=S.MUSEUM, width=8.4, font_size=24).move_to([0, 1.4, 0])
        rows = VGroup(label(r"one correlation number for every pair of borrowers", font_size=26),
                      label(r"and a copula with no tail dependence: \ joint defaults in a crash made to look vanishingly rare",
                            font_size=26, color=S.RESID),
                      label(r"in 2007--08, \ correlated defaults arrived together", font_size=26, color=GREY_A))
        rows.arrange(DOWN, aligned_edge=LEFT, buff=0.25).next_to(hc, DOWN, buff=0.45)
        for r in rows:
            if r.width > 12.6:
                r.width = 12.6
        cite = note(r"see D. MacKenzie \& T. Spears, ``The formula that killed Wall Street?'' (2014)").to_edge(DOWN, buff=0.35)
        with self.voiceover(
            "This mattered in the real world. <bookmark mark='a'/> In 2000 David Li showed how to price bundles of "
            "loans with a Gaussian copula, and it became the industry's standard tool for collateralized debt. "
            "<bookmark mark='b'/> It summarized the dependence between borrowers by a single correlation, and the "
            "Gaussian copula has no tail dependence, so simultaneous defaults in a crash looked extraordinarily "
            "unlikely. <bookmark mark='c'/> In the financial crisis of 2007 and 2008, defaults arrived together. "
            "Historians of finance argue about how much the formula itself was to blame, as against how it was used; "
            "but the mathematical lesson is plain. Correlation describes the middle of a distribution, and risk lives "
            "in the tails."
        ) as vo:
            vo.wait_until("a")
            self.play(FadeIn(hc, shift=UP * 0.2))
            vo.wait_until("b")
            self.play(FadeIn(rows[:2]))
            vo.wait_until("c")
            self.play(FadeIn(rows[2]), FadeIn(cite))
        self.clear_scene()

    def recipe(self):
        d = load("extras2")["copsim"]
        z, u, v = np.asarray(d["z"]), np.asarray(d["u"]), np.asarray(d["v"])
        specs = [(z, [-3.3, 3.3], [-3.3, 3.3], r"$\mathbf Z \sim N_2(0, R)$", rf"$r = {d['r_z']:.2f},\ \tau = {d['tau_z']:.2f}$"),
                 (u, [0, 1], [0, 1], r"$U_i = \Phi(Z_i)$", r"uniform margins: \ the copula"),
                 (v, [0, 4.5], [0, 4.5], r"$X_1 = F_1^{-1}(U_1),\ X_2 = F_2^{-1}(U_2)$",
                  rf"$r = {d['r_v']:.2f},\ \tau = {d['tau_v']:.2f}$")]
        panels = VGroup()
        for k, (P, xr, yr, t, s) in enumerate(specs):
            A = axes(xr, yr, x_length=3.3, y_length=3.3, center=[-4.4 + 4.4 * k, -0.2, 0])
            A.ax.x_axis.set_opacity(0.35)
            A.ax.y_axis.set_opacity(0.35)
            pts = scatter(A.ax, P[:, 0], P[:, 1], color=(SIM, S.ACCENT, S.POST)[k], radius=0.015, opacity=0.55, xr=xr, yr=yr)
            tt = label(t, font_size=22).next_to(A, UP, buff=0.15)
            ss = label(s, font_size=20, color=GREY_B).next_to(A, DOWN, buff=0.15)
            panels.add(VGroup(A, pts, tt, ss))
        arr = VGroup(*[Arrow([-2.4 + 4.4 * k, -0.2, 0], [-2.0 + 4.4 * k, -0.2, 0], buff=0, color=GREY_B) for k in range(2)])
        marg = label(r"margins chosen freely: \ exponential and lognormal", font_size=22, color=GREY_A).to_edge(DOWN, buff=0.75)
        take = label(r"Kendall's $\tau$ survives every step, \ to the last digit; \ Pearson's $r$ does not", font_size=24,
                     color=S.ACCENT).to_edge(DOWN, buff=0.3)
        tag = note(r"simulated: 1,500 pairs").to_corner(UR, buff=0.25)
        with self.voiceover(
            "Sklar's theorem is also a recipe for simulation. <bookmark mark='a'/> Draw pairs from a bivariate normal "
            "with correlation point seven. <bookmark mark='b'/> Pass each coordinate through the normal CDF. Now "
            "both margins are uniform, and what's left is the Gaussian copula: the dependence, stripped of the "
            "margins. <bookmark mark='c'/> Then push each uniform through the inverse CDF of any margin you like: "
            "here, an exponential and a lognormal. <bookmark mark='d'/> Kendall's tau is unchanged through every "
            "step, because each step is increasing in each coordinate. Pearson's correlation drifts. This recipe, "
            "Part 3's probability integral transform run backwards in two dimensions, is how risk models and simulation studies build joint "
            "distributions with realistic margins."
        ) as vo:
            self.play(FadeIn(tag))
            vo.wait_until("a")
            self.play(FadeIn(panels[0]))
            vo.wait_until("b")
            self.play(GrowArrow(arr[0]), FadeIn(panels[1]))
            vo.wait_until("c")
            self.play(GrowArrow(arr[1]), FadeIn(panels[2]), FadeIn(marg))
            vo.wait_until("d")
            self.play(FadeIn(take))
        self.clear_scene()

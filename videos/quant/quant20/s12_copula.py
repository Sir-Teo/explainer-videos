from __future__ import annotations

import numpy as np

from explainer.quant import *  # noqa: F403
from videos.quant.quant20.common import BAD, PART, RISKY, SAFE, ask, fit_right, illustration, load


class Copula(VoiceoverScene):
    def construct(self):
        c = load("copula")
        self.card()
        self.li()
        self.joint(load("joint"))
        self.clouds(c)
        self.ftd(load("ftd"))
        self.tails(c)

    def card(self):
        c = chapter_card(11, r"Copulas: defaults together", r"How likely are two companies to fail at once?", lit=(2000,),
                         part=PART)
        with self.voiceover("Chapter eleven. Copulas: how to make many defaults happen together."):
            self.play(FadeIn(c[0], shift=UP * 0.2), FadeIn(c[1]))
        self.play(FadeOut(c))

    def li(self):
        rows = [cmath(r"\mathbb{P}(\tau_1 \le t_1, \dots, \tau_n \le t_n)", r"=", r"C\big(F_1(t_1), \dots, F_n(t_n)\big)",
                      font_size=36, colors={r"\mathbb{P}(\tau_1 \le t_1, \dots, \tau_n \le t_n)": RISKY}),
                cmath(r"C_\rho^{\text{Gauss}}(u_1, \dots, u_n)", r"=", r"\Phi_\rho\big(N^{-1}(u_1), \dots, N^{-1}(u_n)\big)",
                      font_size=36, colors={r"C_\rho^{\text{Gauss}}(u_1, \dots, u_n)": BAD})]
        whys = [why(r"Sklar (1959): any joint distribution splits into its marginals, here each name's default curve "
                    r"from its CDS, and a copula $C$ that holds the dependence"),
                why(r"Li (2000): take the copula of correlated normals. Each name keeps its own CDS-implied default "
                    r"curve, and one correlation ties them: fast, and quoted by every desk by 2004")]
        step = ladder(self, rows, whys, keep=2, top=2.5, x=-0.6, buff=0.8, edge=6.9)
        with self.voiceover(
            "Single-name curves come from each company's swap. A basket needs to know how the names default together. "
            "Abe Sklar proved in 1959 that any joint distribution splits into its marginals and a copula, a function "
            "that holds only the dependence. <bookmark mark='a'/> In 2000 David Li, then at RiskMetrics, used the "
            "copula of correlated normal variables: each name keeps the default curve its own swaps imply, and one "
            "correlation ties them. It was fast and simple, and within a few years every desk quoted it. In 2009 a "
            "magazine called it the formula that killed Wall Street."
        ) as vo:
            step(0)
            vo.wait_until("a")
            step(1)
        self.wait(0.4)
        self.clear_scene()

    def joint(self, j):
        rh, dc = np.asarray(j["rhos"]), np.asarray(j["default_corr"])
        p12 = np.asarray(j["p12"]) * 1e4
        rows = [cmath(r"p_{12}", r"=", r"\Phi_\rho\big(N^{-1}(p_1), N^{-1}(p_2)\big)", font_size=38, colors={r"p_{12}": BAD}),
                cmath(r"\rho_{\text{default}}", r"=", r"\frac{p_{12} - p_1 p_2}{\sqrt{p_1(1 - p_1)\,p_2(1 - p_2)}}",
                      font_size=36, colors={r"\rho_{\text{default}}": BAD})]
        hdr = VGroup(*rows).arrange(DOWN, aligned_edge=LEFT, buff=0.25).to_edge(UP, buff=0.4).shift(LEFT * 2.0)
        g = axes([0, 0.9], [0, 0.6], x_length=6.4, y_length=3.6, xlabel=r"asset correlation $\rho$",
                 ylabel=r"default correlation", xticks=[0, 0.3, 0.6, 0.9], yticks=[0, 0.2, 0.4, 0.6], font_size=13
                 ).to_edge(LEFT, buff=0.6).shift(DOWN * 1.1)
        ax = g.ax
        line = curve(ax, rh, dc, BAD, stroke_width=3.5)
        diag = DashedLine(ax.c2p(0, 0), ax.c2p(0.6, 0.6), color=GREY_C, stroke_width=1.5)
        k = int(np.argmin(np.abs(rh - 0.3)))
        side = VGroup(
            MathTex(rf"\rho = 0.3:\ p_{{12}} = {p12[k]:.1f}\ \text{{bp}}\ \text{{vs}}\ {1e4 * j['pd'] ** 2:.0f}\ "
                    r"\text{bp if independent}", font_size=24),
            MathTex(rf"\rho_{{\text{{default}}}} = {dc[k]:.3f}", font_size=26, color=BAD),
            wrapped_label(r"two names with 2\% default probabilities: a sizeable asset correlation becomes a small "
                          r"default correlation, because defaults are rare. Small numbers, large consequences: the "
                          r"chance both default quadruples", 3.8, 17, GREY_A),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.3).to_edge(RIGHT, buff=0.3).shift(DOWN * 0.8)
        fit_right(side)
        with self.voiceover(
            "What does a copula correlation mean for defaults? Take two names, each with a two percent chance of "
            "default. The chance that both default is the bivariate normal at their two thresholds. "
            "<bookmark mark='a'/> An asset correlation of 0.3 gives a default correlation of only "
            f"{dc[k]:.2f}, because defaults are rare events. <bookmark mark='b'/> But the joint probability is "
            f"{p12[k]:.0f} basis points instead of the {1e4 * j['pd'] ** 2:.0f} it would be if they were independent. "
            "Small correlations of rare events hide large changes in the chance of disaster."
        ) as vo:
            self.play(FadeIn(hdr))
            vo.wait_until("a")
            self.play(FadeIn(g), Create(diag), Create(line), FadeIn(side[1]), run_time=2)
            vo.wait_until("b")
            self.play(FadeIn(side[0]), FadeIn(side[2]))
        self.wait(0.4)
        self.clear_scene()

    def clouds(self, c):
        pg, pt = np.asarray(c["pts"]["gauss"]), np.asarray(c["pts"]["t"])
        g1 = axes([0, 1], [0, 1], x_length=4.6, y_length=4.6, xlabel=r"$u_1$", ylabel=r"$u_2$", xticks=[0, 0.5, 1],
                  yticks=[0, 0.5, 1], font_size=13)
        g2 = axes([0, 1], [0, 1], x_length=4.6, y_length=4.6, xlabel=r"$u_1$", ylabel=r"$u_2$", xticks=[0, 0.5, 1],
                  yticks=[0, 0.5, 1], font_size=13)
        VGroup(g1, g2).arrange(RIGHT, buff=1.4).shift(DOWN * 0.5)
        d1 = VGroup(*[Dot(g1.ax.c2p(a, b), radius=0.018, color=SAFE).set_opacity(0.6) for a, b in pg[:1200]])
        d2 = VGroup(*[Dot(g2.ax.c2p(a, b), radius=0.018, color=BAD).set_opacity(0.6) for a, b in pt[:1200]])
        q = 0.05
        box1 = Rectangle(width=g1.ax.c2p(q, 0)[0] - g1.ax.c2p(0, 0)[0], height=g1.ax.c2p(0, q)[1] - g1.ax.c2p(0, 0)[1],
                         stroke_color=WHITE, stroke_width=2).move_to(g1.ax.c2p(q / 2, q / 2))
        box2 = box1.copy().move_to(g2.ax.c2p(q / 2, q / 2))
        n1 = int(np.sum((pg[:, 0] < q) & (pg[:, 1] < q)))
        n2 = int(np.sum((pt[:, 0] < q) & (pt[:, 1] < q)))
        t1 = label(rf"Gaussian copula, $\rho = {c['rho2']:g}$", font_size=21, color=SAFE).next_to(g1, UP, buff=0.15)
        t2 = label(rf"$t$ copula, $\rho = {c['rho2']:g}$, $\nu = {c['nu']}$", font_size=21, color=BAD).next_to(g2, UP, buff=0.15)
        c1 = MathTex(rf"\text{{both in worst 5\%}}: {n1}", font_size=22).next_to(g1, DOWN, buff=0.45)
        c2 = MathTex(rf"\text{{both in worst 5\%}}: {n2}", font_size=22).next_to(g2, DOWN, buff=0.45)
        with self.voiceover(
            "Draw fifteen hundred pairs from each copula, with the same correlation. Each dot is a pair of "
            "probabilities: how far into its own distribution each name has fallen. <bookmark mark='a'/> The "
            "Gaussian cloud thins out in the corners. <bookmark mark='b'/> The t copula, which mixes in one shared "
            "shock to everyone's volatility, keeps a dense corner: when one name is in its worst five percent, the "
            f"other often is too. {n2} pairs against {n1}. Same correlation, different crises."
        ) as vo:
            self.play(FadeIn(g1), FadeIn(g2), FadeIn(t1), FadeIn(t2))
            vo.wait_until("a")
            self.play(LaggedStart(*[FadeIn(d) for d in d1], lag_ratio=0.001, run_time=2.5), Create(box1), FadeIn(c1))
            vo.wait_until("b")
            self.play(LaggedStart(*[FadeIn(d) for d in d2], lag_ratio=0.001, run_time=2.5), Create(box2), FadeIn(c2))
        self.wait(0.4)
        self.clear_scene()

    def ftd(self, f):
        rh, v = np.asarray(f["rhos"]), np.asarray(f["ftd_bp"])
        rows = [cmath(r"\tau_i", r"=", r"Q_i^{-1}\big(N(X_i)\big),\quad X_i = \sqrt\rho\,M + \sqrt{1 - \rho}\,Z_i",
                      font_size=36, colors={r"\tau_i": RISKY})]
        hdr = rows[0].to_edge(UP, buff=0.5)
        g = axes([0, 1], [0, 550], x_length=6.8, y_length=3.8, xlabel=r"copula correlation $\rho$",
                 ylabel=r"first-to-default spread, bp", xticks=[0, 0.25, 0.5, 0.75, 1], yticks=[0, 100, 300, 500],
                 font_size=14).to_edge(LEFT, buff=0.6).shift(DOWN * 0.8)
        ax = g.ax
        line = VGroup(curve(ax, rh, v, BAD, stroke_width=3.5), *[Dot(ax.c2p(a, b), color=BAD) for a, b in zip(rh, v)])
        hi = DashedLine(ax.c2p(0, f["n"] * f["single_bp"]), ax.c2p(1, f["n"] * f["single_bp"]), color=GREY_B,
                        stroke_width=1.5)
        lo = DashedLine(ax.c2p(0, f["single_bp"]), ax.c2p(1, f["single_bp"]), color=GREY_B, stroke_width=1.5)
        side = VGroup(
            label(rf"{f['n']} names, each 100 bp, 5 years, recovery 40\%", font_size=18, color=GREY_A),
            MathTex(rf"\rho = 0:\ {v[0]:.0f}\ \text{{bp}} \approx 5 \times 100", font_size=26),
            MathTex(rf"\rho \to 1:\ {v[-1]:.0f}\ \text{{bp}} \to 100", font_size=26),
            wrapped_label(r"the protection pays on the first default in the basket: independent names give five chances, "
                          r"perfectly correlated ones only one. The basket's price is a price of correlation", 3.6, 17,
                          GREY_A),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.28).to_edge(RIGHT, buff=0.3).shift(DOWN * 0.6)
        fit_right(side)
        with self.voiceover(
            "Li's recipe makes default times: draw the correlated normals, map each through the name's own survival "
            "curve, and read off when it defaults. <bookmark mark='a'/> Use it on a basket of five names, each with a "
            "swap spread of one hundred, and price protection on the first default among them. With independent "
            f"names, it costs about {v[0]:.0f}, five chances of a default. <bookmark mark='b'/> As the correlation "
            "rises, the names tend to default together or not at all, and the price falls toward one name's spread. "
            "The basket trades the correlation, which no single-name swap reveals."
        ) as vo:
            self.play(FadeIn(hdr))
            vo.wait_until("a")
            self.play(FadeIn(g), Create(hi), Create(lo), FadeIn(side[0]), FadeIn(side[1]))
            vo.wait_until("b")
            self.play(Create(line), FadeIn(side[2]), FadeIn(side[3]), run_time=2)
        self.add(illustration(r"200{,}000 simulated baskets per correlation"))
        self.wait(0.4)
        self.clear_scene()

    def tails(self, c):
        Lg, Lt = np.asarray(c["losses_g"]) * 100, np.asarray(c["losses_t"]) * 100
        edges = np.linspace(0, 30, 61)
        hg = np.histogram(np.clip(Lg, 0, 29.99), edges)[0] / len(Lg)
        ht = np.histogram(np.clip(Lt, 0, 29.99), edges)[0] / len(Lt)
        g = axes([0, 30], [-4, 0], x_length=7.6, y_length=4.4, xlabel=r"pool loss in a year, \% of notional",
                 ylabel=r"$\log_{10}$ probability", xticks=[0, 5, 10, 15, 20, 25, 30], yticks=[-4, -3, -2, -1, 0],
                 font_size=14).to_edge(LEFT, buff=0.6).shift(DOWN * 0.3)
        ax = g.ax
        mid = 0.5 * (edges[1:] + edges[:-1])

        def line(h, col):
            ok = h > 0
            return curve(ax, mid[ok], np.log10(h[ok]), col, stroke_width=3)
        lg, lt = line(hg, SAFE), line(ht, BAD)
        side = VGroup(
            legend([(SAFE, r"Gaussian copula"), (BAD, r"$t$ copula, $\nu = 4$")], font_size=17),
            label(rf"{c['N']} names, PD {100 * c['pd']:.0f}\%, $\rho$ = 0.2, recovery {100 * c['R']:.0f}\%", font_size=18,
                  color=GREY_A),
            MathTex(rf"\mathbb{{P}}(\text{{loss}} > 15\%):\ {100 * c['tail']['gauss']:.2f}\%\ \text{{vs}}\ "
                    rf"{100 * c['tail']['t']:.2f}\%", font_size=24, color=BAD),
            wrapped_label(r"the copula decides the senior tranches' risk, and the Gaussian one says it is tiny", 3.6, 17,
                          GREY_A),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.28).to_edge(RIGHT, buff=0.3)
        fit_right(side)
        with self.voiceover(
            "Now a pool of a hundred and twenty-five names, the size of the standard index, each with a two percent "
            "default probability and the same correlation, under each copula. On a log scale, the chance of each "
            "level of loss in a year. <bookmark mark='a'/> Near the average they agree. <bookmark mark='b'/> In the "
            "tail they do not: the chance of losing more than fifteen percent of the pool is "
            f"{100 * c['tail']['gauss']:.2f} percent with the Gaussian copula and {100 * c['tail']['t']:.1f} with the "
            "t, more than ten times as large. That tail is exactly what a senior tranche insures."
        ) as vo:
            self.play(FadeIn(g), FadeIn(side[0]), FadeIn(side[1]))
            vo.wait_until("a")
            self.play(Create(lg), run_time=1.5)
            vo.wait_until("b")
            self.play(Create(lt), FadeIn(side[2]), FadeIn(side[3]), run_time=1.5)
        self.add(illustration(r"40{,}000 simulated years of each copula (the House's \texttt{copula\_defaults})"))
        q = ask(r"with a Gaussian copula, does correlating the names raise or lower the chance that none of them "
                r"defaults?")
        with self.voiceover("With a Gaussian copula, does raising the correlation make it more or less likely that no "
                            "name defaults at all?"):
            self.play(FadeIn(q))
        self.wait(0.5)
        self.clear_scene()

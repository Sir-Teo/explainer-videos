from __future__ import annotations

from videos.quant.quant20.common import lesson_cards

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
        self.feedback()

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
                why('Gaussian copulas were widely used for credit portfolios: marginal default curves and a chosen latent dependence structure. Single-name curves alone do not identify dependence; this example is homogeneous and one-factor')]
        step = ladder(self, rows, whys, keep=2, top=2.5, x=-0.6, buff=0.8, edge=6.9)
        with self.voiceover(
            "Single-name pricing curves specify marginal survival, not joint defaults. Sklar's theorem represents a joint distribution through marginals and a copula; uniqueness holds for continuous marginals, while atoms require care. <bookmark mark='a'/> David Li's two thousand paper applied copulas to default-time modeling. Correlated latent normals, transformed through each name's marginal curve, give a tractable Gaussian dependence model. Its latent correlation is not the correlation of binary default indicators. Broad adoption did not make one constant correlation a complete description of credit dependence, and a magazine headline is not a causal explanation of the financial crisis."
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
            wrapped_label('two names with 2\\% marginal PD in a Gaussian copula. Latent correlation and default correlation differ; their mapping depends on PD and the assumed joint law', 3.8, 17, GREY_A),
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
        d1 = VGroup(*[Dot(g1.ax.c2p(a, b), radius=0.018, color=SAFE).set_opacity(0.6) for a, b in pg])
        d2 = VGroup(*[Dot(g2.ax.c2p(a, b), radius=0.018, color=BAD).set_opacity(0.6) for a, b in pt])
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
            f"These fifteen hundred simulated pairs compare a Gaussian copula with a Student t copula at the same latent correlation, one half. The t illustration has three degrees of freedom and a shared random scale. <bookmark mark='a'/> The Gaussian copula has no asymptotic tail dependence when correlation is below one. <bookmark mark='b'/> The t copula retains tail dependence. In this fixed sample, {n2} t pairs and {n1} Gaussian pairs fall in the displayed joint corner. Those counts fluctuate with simulation. The later pool example uses different parameters: correlation point two and four degrees of freedom, which must not be confused with this cloud. Neither cloud is fitted to market joint-default data."
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
            wrapped_label('first-to-default protection: holding marginal curves, recovery and contract terms fixed, dependence changes this Monte Carlo price estimate. Marginal spreads do not identify basket dependence', 3.6, 17,
                          GREY_A),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.28).to_edge(RIGHT, buff=0.3).shift(DOWN * 0.6)
        fit_right(side)
        with self.voiceover(
            f"Draw correlated latent normals, map them to uniforms and invert the names' survival curves to obtain default times. <bookmark mark='a'/> This fixed-seed example prices first-to-default protection on five homogeneous names, each with a one hundred basis point continuous-premium credit-triangle input. With independence, the displayed basket estimate is {v[0]:.0f} basis points. <bookmark mark='b'/> As dependence approaches perfect comovement, the basket approaches one name's event risk. The calculation uses Monte Carlo, quarterly premiums without a full production accrual model, and different sample sizes for its two legs. Treat the numbers as approximate illustrations with sampling error. Dependence is an additional assumption beyond the marginal spreads, not a quantity identified by single-name quotes alone."
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
        support = 100 * (1 - c["R"])
        edges = np.linspace(0, support, int(round(support / 0.5)) + 1)
        assert all(np.isfinite(v).all() and (v >= 0).all() and (v <= support).all() for v in (Lg, Lt))
        ng, nt = np.histogram(Lg, edges)[0], np.histogram(Lt, edges)[0]
        assert ng.sum() == len(Lg) and nt.sum() == len(Lt)
        hg, ht = ng / len(Lg), nt / len(Lt)
        g = axes([0, support], [-5, 0], x_length=7.6, y_length=4.4, xlabel=r"pool loss in a year, \% of notional",
                 ylabel=r"$\log_{10}$ probability per 0.5\%-loss bin", xticks=np.arange(0, support + 1, 10), yticks=[-5, -4, -3, -2, -1, 0],
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
            wrapped_label('fixed marginal PD and recovery; empirical 0.5\\%-loss bins over full 0--60\\% support, with empty bins omitted. These finite-sample tails are conditional model estimates, not tranche prices or tail bounds', 3.6, 17,
                          GREY_A),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.28).to_edge(RIGHT, buff=0.3)
        fit_right(side)
        with self.voiceover(
            f"Now compare one hundred twenty-five homogeneous names, fixed forty percent recovery, two percent marginal default probability and latent correlation point two. The Student t version has four degrees of freedom. <bookmark mark='a'/> The means agree by construction, while the distribution shapes need not. <bookmark mark='b'/> In forty thousand scenarios the loss-above-fifteen-percent frequency is {100 * c['tail']['gauss']:.2f} percent for Gaussian dependence and {100 * c['tail']['t']:.2f} percent for Student t dependence. These are finite Monte Carlo estimates; rare tail counts need uncertainty. A heavier dependence tail in this example does not prove that every tranche under every t parameter is more risky. The event, recovery, horizon and dependence assumptions must all be stated."
        ) as vo:
            self.play(FadeIn(g), FadeIn(side[0]), FadeIn(side[1]))
            vo.wait_until("a")
            self.play(Create(lg), run_time=1.5)
            vo.wait_until("b")
            self.play(Create(lt), FadeIn(side[2]), FadeIn(side[3]), run_time=1.5)
        self.add(illustration(r"40{,}000 simulated years of each copula (the House's \texttt{copula\_defaults})"))
        self.wait(0.4)
        self.clear_scene()
        q = ask(r"with a Gaussian copula, does correlating the names raise or lower the chance that none of them "
                r"defaults?")
        with self.voiceover("With a Gaussian copula, does raising the correlation make it more or less likely that no "
                            "name defaults at all?"):
            self.play(FadeIn(q))
        self.wait(0.5)
        self.clear_scene()

    def feedback(self):
        title = wrapped_label('Answer: more joint survival can coexist with a worse tail', 12.4, 32, QC.IDEA).to_edge(UP, buff=.6)
        answer = wrapped_label('For the homogeneous Gaussian pool with fixed marginal PDs, increasing common correlation raises the probability of no defaults and also concentrates bad outcomes.', 11.8, 27, GREY_A).move_to(ORIGIN)
        with self.voiceover('In this homogeneous Gaussian pool with fixed marginal probabilities, stronger common correlation raises the probability that all names survive. It also clusters defaults into worse states. The unchanged mean therefore conceals a different distribution. This conclusion concerns the stated dependence ordering; it is not a rule that raising any arbitrary correlation statistic orders every possible credit distribution.') as vo:
            self.play(FadeIn(title), FadeIn(answer))
        self.wait(.5)
        self.clear_scene()

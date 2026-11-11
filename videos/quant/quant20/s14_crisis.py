from __future__ import annotations

from videos.quant.quant20.common import lesson_cards

import numpy as np

from explainer.quant import *  # noqa: F403
from videos.quant.quant20.common import BAD, EQT, MEZZ, PART, SENIOR, ask, fit_right, illustration, load


class Crisis(VoiceoverScene):
    def construct(self):
        j = load("cjs")
        self.card()
        self.catbond(j)
        self.reprice()
        self.ratings()
        self.squared()
        self.feedback()

    def card(self):
        c = chapter_card(13, r"2007--08: the senior tranches", r"How did AAA securities lose money?", lit=(2008,),
                         part=PART)
        with self.voiceover("Chapter thirteen. 2007 and 2008: how securities rated triple-A came to lose money."):
            self.play(FadeIn(c[0], shift=UP * 0.2), FadeIn(c[1]))
        self.play(FadeOut(c))

    def catbond(self, j):
        m = np.asarray(j["m"])
        from scipy.stats import norm
        pct = norm.cdf(m) * 100
        g = axes([-4, 2], [0, 1.05], x_length=7.6, y_length=4.4, xlabel=r"the economy $M$ (standard deviations)",
                 ylabel=r"tranche loss, fraction", xticks=[-4, -3, -2, -1, 0, 1, 2], yticks=[0, 0.5, 1.0], font_size=14
                 ).to_edge(LEFT, buff=0.6).shift(DOWN * 0.3)
        ax = g.ax
        cols = {"equity": EQT, "mezz": MEZZ, "senior": SENIOR}
        lines = VGroup(*[curve(ax, m, np.asarray(j[k]), c_, stroke_width=3.5) for k, c_ in cols.items()])
        ms = j["m_star"]
        star = DashedLine(ax.c2p(ms, 0), ax.c2p(ms, 1.05), color=WHITE, stroke_width=2)
        p = j["params"]
        side = VGroup(
            legend([(EQT, r"equity 0--3\%"), (MEZZ, r"mezzanine 3--7\%"), (SENIOR, r"senior 15--30\%")], font_size=17),
            MathTex(rf"\text{{senior loses only below the }} {100 * j['threshold_pct']:.2f}\text{{th percentile}}",
                    font_size=24),
            MathTex(rf"\text{{expected loss: }} {1e4 * j['el_senior']:.1f}\ \text{{bp, pool }} {1e4 * j['el_pool']:.0f}\ \text{{bp}}",
                    font_size=24),
            wrapped_label(rf"large pool, PD {100 * p['pd']:.0f}\%, $\rho$ = {p['rho']:g}, recovery "
                          rf"{100 * p['R']:.0f}\%. Coval, Jurek and Stafford (2009): a senior tranche is an 'economic "
                          r"catastrophe bond', paying off except in the economy's worst states, which is exactly when "
                          r"money is worth most. A pricing kernel is needed to compare its spread with a corporate bond of the same "
                          r"expected loss", 3.8, 16, GREY_A),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.25).to_edge(RIGHT, buff=0.3)
        fit_right(side)
        with self.voiceover(
            f"This is a stylized one-factor loss illustration, not a fitted mortgage deal. <bookmark mark='a'/> The equity tranche loses in relatively ordinary adverse states. <bookmark mark='b'/> The senior tranche starts losing only in the worst {100 * j['threshold_pct']:.2f} percent of factor states under the assumed normal distribution. Its model expected loss is {10000 * j['el_senior']:.1f} basis points of tranche notional over the specified horizon. A small event frequency is not a guarantee against loss. <bookmark mark='c'/> Coval, Jurek and Stafford explain how losses concentrated in high-marginal-value states can command a large price of risk. That conclusion needs a physical loss distribution and a pricing kernel or an equivalent risk-neutral specification. Expected loss or a rating alone does not determine a spread, and different rating methods do not all target the same statistic. This chart supplies no calibrated spread comparison with government or corporate bonds."
        ) as vo:
            self.play(FadeIn(g), FadeIn(side[0]))
            vo.wait_until("a")
            self.play(Create(lines[0]), Create(lines[1]), run_time=2)
            vo.wait_until("b")
            self.play(Create(lines[2]), Create(star), FadeIn(side[1]), FadeIn(side[2]), run_time=2)
            vo.wait_until("c")
            self.play(FadeIn(side[3]))
        self.wait(0.4)
        self.clear_scene()

    def reprice(self):
        from explainer.quant.house import credit as CR
        cases = [(0.02, 0.15, r"calm: PD 2\%, $\rho$ = 0.15"), (0.04, 0.15, r"PD doubles"), (0.02, 0.4, r"$\rho$ = 0.4"),
                 (0.04, 0.4, r"both")]
        vals = [CR.lhp_tranche_el(p_, r_, 0.4, 0.15, 0.30) * 1e4 for p_, r_, _ in cases]
        g = axes([0.4, 4.6], [-1, 2.5], x_length=6.4, y_length=4.2, xlabel=r"", ylabel=r"senior 15--30\%: expected loss, bp "
                 r"(log scale)", xticks=[], yticks=[], font_size=14).to_edge(LEFT, buff=0.9).shift(DOWN * 0.3)
        ax = g.ax
        ty = VGroup(*[MathTex(f"{10 ** e:g}", font_size=20).next_to(ax.c2p(0.4, e), LEFT, buff=0.12) for e in (-1, 0, 1, 2)])
        bars = VGroup()
        for i, (v_, (_, _, l_)) in enumerate(zip(vals, cases)):
            h = np.log10(max(v_, 0.1))
            b_ = Rectangle(width=0.7, height=max(ax.c2p(0, h)[1] - ax.c2p(0, -1)[1], 0.01), stroke_width=0,
                           fill_color=SENIOR if i == 0 else BAD, fill_opacity=0.8).move_to(
                [ax.c2p(i + 1, 0)[0], (ax.c2p(0, h)[1] + ax.c2p(0, -1)[1]) / 2, 0])
            bars.add(VGroup(b_, MathTex(f"{v_:.1f}" if v_ < 10 else f"{v_:.0f}", font_size=24).next_to(b_, UP, buff=0.1),
                            wrapped_label(l_, 1.5, 14, GREY_A).next_to(ax.c2p(i + 1, -1), DOWN, buff=0.15)))
        side = wrapped_label('fixed-model stress for the same large-pool tranche at 40\\% recovery: doubling PD and raising correlation together greatly increases expected loss. The multiplier is a model comparison, not a reconstruction of ratings or trading P\\&L', 3.8, 18, GREY_A).to_edge(RIGHT, buff=0.4)
        with self.voiceover(
            f"This is a controlled model stress, not an empirical reconstruction of two thousand seven. We change marginal default probability and Gaussian dependence separately, holding the stated recovery and tranche structure fixed. <bookmark mark='a'/> The displayed bars report how each change affects the senior expected loss in this particular model. <bookmark mark='b'/> Applying both changes gives a multiplier of {vals[3] / vals[0]:,.0f} relative to the initial value. That large ratio partly reflects a very small initial expected loss. The exercise illustrates nonlinear sensitivity; it does not estimate historical mortgage correlation or identify how much of a traded-price decline each parameter caused."
        ) as vo:
            self.play(FadeIn(g), FadeIn(ty), FadeIn(bars[0]))
            vo.wait_until("a")
            self.play(FadeIn(bars[1]), FadeIn(bars[2]))
            vo.wait_until("b")
            self.play(FadeIn(bars[3]), FadeIn(side))
        self.wait(0.4)
        self.clear_scene()

    def ratings(self):
        cc = crisis_card(r"FCIC report, 2011", r"A defined rating-agency and vintage denominator",
                         r"Moody's ultimately downgraded 83\% of its 2006 Aaa mortgage-backed-security tranches; "
                         r"downgrade is not default or full realized loss",
                         stats=[(r"83\%", r"Moody's 2006 Aaa MBS tranches")], width=7.8, font_size=23).shift(UP*.65)
        foot = wrapped_label(r"Ratings, underwriting, common shocks, funding and governance: the model stress "
                             r"illustrates a mechanism, not a complete empirical explanation.",12,23,GREY_A).to_edge(DOWN,buff=.7)
        with self.voiceover(
            "The Financial Crisis Inquiry Report states that Moody's ultimately downgraded eighty-three percent of its two thousand six Aaa mortgage-backed-security tranches. The denominator is that rating-agency and vintage group, not all triple-A debt, all CDOs or all securities. A downgrade is not the same as a default or a realized full loss. <bookmark mark='a'/> The record documents rating and model failures amid a national housing downturn. Our Gaussian illustrations help explain sensitivity to common shocks, but do not establish one estimated correlation as the sole cause. Underwriting, incentives, leverage, funding, recovery and model governance also matter."
        ) as vo:
            self.play(FadeIn(cc))
            vo.wait_until("a")
            self.play(FadeIn(foot))
        self.add(illustration(r"FCIC, \textit{The Financial Crisis Inquiry Report} (2011), p. 221 (Moody's 2006-vintage Aaa MBS tranches)"))
        self.wait(0.4)
        self.clear_scene()

    def squared(self):
        rows = [cmath(r"\text{CDO}^2", r"=", r"\text{tranches of a pool of mezzanine tranches}", font_size=38,
                      colors={r"\text{CDO}^2": BAD}),
                cmath(r"\mathrm{EL}_{A,D}", r"=", r"\frac{\mathbb{E}[\min((L-A)^+,D-A)]}{D-A}",
                      font_size=36, colors={r"\mathrm{EL}_{A,D}": BAD})]
        whys = [why('ABS CDOs re-tranched mezzanine mortgage exposures. Shared housing drivers and overlapping collateral can cluster losses; the constituent pieces need not fail in identical states'),
                why('re-tranching increases sensitivity to joint-tail assumptions that are hard to estimate from sparse crises. Dependence is one input alongside marginal risk, recovery, collateral and cash-flow structure')]
        step = ladder(self, rows, whys, keep=2, top=2.4, x=-0.6, buff=0.8, edge=6.9)
        with self.voiceover(
            "Resecuritization can pool mezzanine mortgage exposures and tranche their combined cash flows again. <bookmark mark='a'/> Shared collateral, common housing shocks and overlapping exposures can make their tail losses strongly dependent. Senior risk still depends on marginal credit quality, recovery, attachment, cash-flow structure and funding assumptions, as well as dependence. Sparse downturn observations do not identify that joint tail without substantial assumptions. The Gaussian examples illustrate concentration mechanisms; they are not an empirical reconstruction of CDO-squared losses or proof that one correlation number explains the crisis."
        ) as vo:
            step(0)
            vo.wait_until("a")
            step(1)
        q = ask(r"two bonds both lose 0.5\% a year on average: one in every bad year, one only in a depression. Which "
                r"should pay the higher spread, and why?")
        with self.voiceover("Two bonds both lose half a percent a year on average: one a little in every bad year, the "
                            "other only in a depression. Which should pay the higher spread?"):
            self.play(FadeIn(q))
        self.wait(0.5)
        self.clear_scene()

    def feedback(self):
        title = wrapped_label('Answer: expected loss alone does not fix the price', 12.4, 32, QC.IDEA).to_edge(UP, buff=.6)
        answer = wrapped_label('Equal physical expected loss can have different prices when losses coincide with different marginal values of wealth. State the pricing kernel and comparable contract terms.', 11.8, 27, GREY_A).move_to(ORIGIN)
        with self.voiceover('If the pricing kernel is especially high in a depression, a loss concentrated in that state has a larger risk-adjusted cost than an equal expected loss spread across less severe states. That is a conditional pricing argument, not a claim that physical expected loss alone fixes a spread. Align maturity, recovery, liquidity and contract terms before comparing two traded bonds.') as vo:
            self.play(FadeIn(title), FadeIn(answer))
        self.wait(.5)
        self.clear_scene()

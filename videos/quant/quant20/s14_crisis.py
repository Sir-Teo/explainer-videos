from __future__ import annotations

import numpy as np

from explainer.quant import *  # noqa: F403
from videos.quant.quant20.common import BAD, EQT, MEZZ, PART, SENIOR, ask, fit_right, illustration, load


class Crisis(VoiceoverScene):
    def construct(self):
        j = load("cjs")
        self.card()
        self.catbond(j)
        self.ratings()
        self.squared()

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
                          r"money is worth most. Its spread should be far wider than a corporate bond with the same "
                          r"expected loss", 3.8, 16, GREY_A),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.25).to_edge(RIGHT, buff=0.3)
        fit_right(side)
        with self.voiceover(
            "Each tranche's loss, as a function of the state of the economy. <bookmark mark='a'/> The equity tranche "
            "starts losing in ordinary bad years. <bookmark mark='b'/> The senior tranche loses nothing at all unless "
            f"the economy is in its worst {100 * j['threshold_pct']:.2f} percent of states: about one year in six "
            f"hundred. Its expected loss is tiny, {1e4 * j['el_senior']:.1f} basis points a year. "
            "<bookmark mark='c'/> Joshua Coval, Jakub Jurek and Erik Stafford pointed out in 2009 what that means: a "
            "senior tranche is a bet against economic catastrophe, which pays out exactly when everything else does "
            "badly. A rating that looks only at expected loss calls it as safe as a government bond; a price that "
            "accounts for when the loss arrives should make its spread much wider than a corporate bond's with the "
            "same rating."
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

    def ratings(self):
        cc = crisis_card(r"2006--2011", r"The triple-A mortgage securities",
                         r"from the conclusions of the Financial Crisis Inquiry Commission (January 2011): in 2006 alone, "
                         r"Moody's rated some 30 mortgage-related securities triple-A every working day, and 83\% of "
                         r"the mortgage securities rated triple-A that year were ultimately downgraded",
                         stats=[(r"83\%", r"of 2006's AAA mortgage securities, downgraded"),
                                (r"\sim 30", r"AAA ratings a working day, 2006 (Moody's)")],
                         width=8.6, font_size=21).move_to(UP * 0.4)
        foot = wrapped_label(r"the models behind the ratings used correlations estimated from years of rising house "
                             r"prices, in which mortgages across regions had rarely defaulted together: chapter 11's "
                             r"$\rho$, fitted to calm, applied to a national fall", 11.5, 19, GREY_A).to_edge(DOWN, buff=0.6)
        with self.voiceover(
            "The public record shows the scale. The Financial Crisis Inquiry Commission found that in 2006 alone "
            "Moody's rated about thirty mortgage-related securities triple-A every working day, and that eighty-three "
            "percent of the mortgage securities rated triple-A that year were ultimately downgraded. "
            "<bookmark mark='a'/> The models behind those ratings used correlations estimated from years of rising "
            "house prices, when mortgages in different regions rarely defaulted together. Chapter eleven's "
            "correlation, fitted to calm and applied to a national fall."
        ) as vo:
            self.play(FadeIn(cc))
            vo.wait_until("a")
            self.play(FadeIn(foot))
        self.add(illustration(r"FCIC, \textit{The Financial Crisis Inquiry Report} (2011), Conclusions"))
        self.wait(0.4)
        self.clear_scene()

    def squared(self):
        rows = [cmath(r"\text{CDO}^2", r"=", r"\text{tranches of a pool of mezzanine tranches}", font_size=38,
                      colors={r"\text{CDO}^2": BAD}),
                cmath(r"\frac{\partial\,\text{senior}}{\partial\rho}", r"\gg", r"\frac{\partial\,\text{senior of a "
                      r"loan pool}}{\partial\rho}", font_size=36, colors={r"\frac{\partial\,\text{senior}}{\partial\rho}": BAD})]
        whys = [why(r"ABS CDOs pooled the mezzanine tranches of mortgage securitisations, and tranched them again: "
                    r"each mezzanine piece is already a bet on a tail, so the new pool's names all fail in the same "
                    r"states"),
                why(r"re-tranching tail bets concentrates the dependence on the one assumption nobody could test: the "
                    r"correlation in a national housing fall")]
        step = ladder(self, rows, whys, keep=2, top=2.4, x=-0.6, buff=0.8, edge=6.9)
        with self.voiceover(
            "And then the tranches were tranched again. Mortgage securitizations produced mezzanine slices that were "
            "hard to sell, so they were pooled into new CDOs and sliced once more. <bookmark mark='a'/> But each "
            "mezzanine slice is already a bet on a tail; a pool of them is a pool of names that all fail in the same "
            "states. The senior tranche of such a pool depends almost entirely on one number, the correlation in a "
            "national housing downturn, which no historical data could pin down. Senior tranches like these were "
            "among the largest losses at the banks in 2007 and 2008."
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

from __future__ import annotations

from videos.economics.econ6.common import *  # noqa: F403


class Practice(VoiceoverScene):
    def construct(self):
        card(self, 12, r"In practice: \ price indices, poor households, taxes", r"Where does demand theory earn its "
             r"keep outside the classroom?", "Chapter twelve. In practice: price indices, poor households, taxes.",
             scale=("household", "nation"))
        self.cpi()
        self.poor()
        self.ramsey()

    def cpi(self):
        c = load("cpi")
        from explainer.ai.viz import axes

        years = list(c["years"])
        ax = axes([2000, 2025], [1.0, 1.85], x_length=6.4, y_length=4.6, xticks=[2000, 2005, 2010, 2015, 2020, 2025],
                  yticks=[1.0, 1.2, 1.4, 1.6, 1.8], xlabel=r"", ylabel=r"price level, \ 2000 = 1", font_size=17,
                  xfmt=lambda v: f"{v:.0f}", yfmt=lambda v: f"{v:.1f}", center=LEFT * 3.0 + DOWN * 0.35)
        a = ax.ax
        L = VMobject(stroke_color=E.ACCENT, stroke_width=4).set_points_as_corners(
            [a.c2p(y, v) for y, v in zip(years, c["laspeyres"])])
        T = VMobject(stroke_color=HICKS, stroke_width=4).set_points_as_corners(
            [a.c2p(y, v) for y, v in zip(years, c["tornqvist"])])
        lab = VGroup(label(rf"fixed 2000 basket \ ({c['laspeyres'][-1]:.2f})", font_size=19, color=E.ACCENT).next_to(
            L.get_end(), UP, buff=0.12).shift(LEFT * 0.9),
                     label(rf"chained T\"ornqvist \ ({c['tornqvist'][-1]:.2f})", font_size=19, color=HICKS).next_to(
                         T.get_end(), DOWN, buff=0.15).shift(LEFT * 0.9))
        m = c["methods"]
        side = VGroup(
            label(r"how the official CPI allows for substitution", font_size=25, color=E.ACCENT),
            label(rf"since {m['geometric_mean_since']}: \ geometric means \\ within each item stratum (apples with "
                  r"apples): \\ shares held fixed, \ as for Cobb--Douglas tastes", font_size=21),
            label(rf"since {m['chained_published']}: \ the chained CPI, \ a T\"ornqvist index \\ with this month's "
                  r"and last month's weights", font_size=21),
            label(rf"on fifteen kinds of American spending, \\ 2000--2025: \ the fixed basket runs "
                  rf"{100 * c['gap_per_year']:.2f} points \\ a year faster than the chained index", font_size=21,
                  color=HICKS),
            label(r"(substitution between broad groups only)", font_size=18, color=GREY_B),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.3).to_edge(RIGHT, buff=0.35)
        tag = data_tag(r"BLS, Handbook of Methods; BEA PCE by type of product (FRED), our computation", corner=DR,
                       font_size=12)
        with self.voiceover(
            "First, the price index itself. The theory of chapter nine changed how America measures inflation. "
            "<bookmark mark='a'/> Since January 1999, the Bureau of Labor Statistics has averaged prices within "
            "each narrow stratum, apples with apples, by a geometric mean, which is exactly right if shoppers keep "
            "the shares they spend on each variety fixed, as Cobb–Douglas tastes do. <bookmark mark='b'/> And since "
            "2002 it has published a chained CPI, a Törnqvist index whose weights are updated every month, which "
            "allows substitution between strata too. <bookmark mark='c'/> How much does it matter? On fifteen broad "
            "kinds of American spending from 2000 to 2025, a fixed 2000 basket rises nought point one eight points a "
            "year faster than the chained index: substitution bias from broad groups alone, a sizeable part of the "
            "Boskin Commission's nought point four."
        ) as vo:
            self.play(FadeIn(ax), FadeIn(tag), FadeIn(side[0]))
            self.play(Create(L), Create(T), FadeIn(lab), run_time=2.5)
            vo.wait_until("a")
            self.play(FadeIn(side[1]))
            vo.wait_until("b")
            self.play(FadeIn(side[2]))
            vo.wait_until("c")
            self.play(FadeIn(side[3]), FadeIn(side[4]), Indicate(lab, color=E.ACCENT))
        self.clear_scene()

    def poor(self):
        eq = MathTex(r"\frac{\Delta\,\text{welfare}}{m} \;\approx\; -\,(\text{share bought} - \text{share "
                     r"produced})\times\frac{\Delta p}{p}", font_size=40).to_edge(UP, buff=0.7)
        why = label(r"Roy's identity: \ at the margin, \ a price rise costs what you buy of the good", font_size=24,
                    color=GREY_A).next_to(eq, DOWN, buff=0.25)
        from explainer.ai.viz import axes

        ax = axes([0, 3], [-4, 4], x_length=6.0, y_length=3.6, xticks=None, yticks=[-4, -2, 0, 2, 4],
                  ylabel=r"\% of budget", font_size=17, yfmt=lambda v: f"{v:+.0f}" if v else "0",
                  center=LEFT * 2.6 + DOWN * 1.35)
        a = ax.ax
        hh = [(r"a city family: \\ buys 30\%, \ grows none", -3.0, GIFF),
              (r"a small farmer: \\ buys 30\%, \ grows 30\%", 0.0, GREY_B),
              (r"a rice farmer: \\ buys 20\%, \ grows 50\%", 3.0, PASS)]
        bars = VGroup(Line(a.c2p(0, 0), a.c2p(3, 0), color=GREY_B, stroke_width=1.5))
        for k, (n, v, col) in enumerate(hh):
            r = Polygon(a.c2p(k + 0.25, 0), a.c2p(k + 0.75, 0), a.c2p(k + 0.75, v), a.c2p(k + 0.25, v),
                        stroke_width=0, fill_color=col, fill_opacity=0.85) if v else Line(a.c2p(k + 0.25, 0),
                                                                                          a.c2p(k + 0.75, 0),
                                                                                          color=col, stroke_width=5)
            t = label(rf"{v:+.0f}\%", font_size=20, color=col).next_to(r, UP if v >= 0 else DOWN, buff=0.06)
            nm = label(n, font_size=16, color=GREY_A).move_to(a.c2p(k + 0.5, 3.4 if v < 0 else -3.4))
            bars.add(VGroup(r, t, nm))
        head2 = label(r"rice 10\% dearer:", font_size=24, color=COCO).next_to(ax, UP, buff=0.1)
        side = VGroup(
            label(r"Deaton (1989), \ rice in Thailand: \\ who gains and who loses \\ from a price change, \ read "
                  r"from \\ budget shares alone", font_size=22),
            label(r"Indonesia, 1997--98: \ the price of rice \\ rose almost 200\%, \ for households \\ spending "
                  r"nearly 30\% of budgets on it", font_size=22, color=GIFF),
            label(r"for changes that big, \\ substitution matters: \ chapter 8", font_size=20, color=GREY_A),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.35).to_edge(RIGHT, buff=0.4).shift(DOWN * 0.9)
        tag = illustrative_tag(r"illustrative households; Indonesia: Friedman and Levinsohn (2002), via Jensen and "
                               r"Miller", corner=DR, font_size=12)
        with self.voiceover(
            "Second, poor households. Development economists need to know who is hurt by a change in food prices, "
            "often with nothing but a household survey. <bookmark mark='a'/> Duality gives a first answer. To first "
            "order, a price rise costs a household its net purchases of the good: the share of its budget it "
            "spends on it, minus the share it earns by producing it. That's Roy's identity at work. "
            "<bookmark mark='b'/> If rice gets ten percent dearer, a city family spending thirty percent of its "
            "budget on rice loses about three percent; a farmer who grows what it eats is untouched; a farmer who "
            "sells rice gains. Angus Deaton mapped exactly this for rice in Thailand in 1989. "
            "<bookmark mark='c'/> It matters because the changes can be enormous. In Indonesia's financial crisis of "
            "1997 and 1998 the price of rice rose almost two hundred percent, for households that spent nearly "
            "thirty percent of their budgets on it. For changes that big, the first-order answer is not enough, "
            "and substitution, chapter eight's welfare measures, must come in."
        ) as vo:
            opener = label(r"who is hurt when food gets dearer?", font_size=38, color=COCO)
            self.play(FadeIn(tag), FadeIn(opener, shift=UP * 0.15), run_time=0.8)
            vo.wait_until("a")
            self.play(FadeOut(opener), Write(eq), FadeIn(why), run_time=2)
            vo.wait_until("b")
            self.play(FadeIn(ax), FadeIn(head2), LaggedStart(*[FadeIn(b_) for b_ in bars], lag_ratio=0.3),
                      FadeIn(side[0]), run_time=2.5)
            vo.wait_until("c")
            self.play(FadeIn(side[1]), FadeIn(side[2]))
        self.clear_scene()

    def ramsey(self):
        r = load("ramsey")
        rows = VGroup(
            label(r"raise \$10 from two goods, \ \$100 spent on each", font_size=27),
            label(rf"a staple, \ elasticity ${r['elasticity'][0]:.1f}$; \ a treat, \ elasticity "
                  rf"${r['elasticity'][1]:.1f}$", font_size=25, color=GREY_A),
            label(rf"the same tax on both, \ {100 * r['t_uniform'][0]:.0f}\%: \ deadweight loss "
                  rf"\${r['loss_uniform']:.2f}", font_size=26),
            label(rf"Ramsey: \ {100 * r['t'][0]:.0f}\% on the staple, \ {100 * r['t'][1]:.0f}\% on the treat: \ "
                  rf"\${r['loss']:.2f}", font_size=26, color=HICKS),
            label(r"tax each good in inverse proportion to its elasticity", font_size=26, color=HICKS),
            label(r"but staples are what the poor buy (Engel's law): \\ efficiency says tax them, \ equity says "
                  r"don't", font_size=26, color=GIFF),
            label(r"the trade-off of Part 41: \ optimal taxes, \ Diamond and Mirrlees, \ Atkinson and Stiglitz",
                  font_size=22, color=GREY_A),
        ).arrange(DOWN, buff=0.36).move_to(DOWN * 0.1)
        head = label(r"Frank Ramsey, 1927: \ the cheapest way to raise a tax", font_size=32,
                     color=E.ACCENT).to_edge(UP, buff=0.45)
        tag = agora_tag(r"computed: small-tax approximation, loss $\approx \tfrac12|\varepsilon| t^2\,px$",
                        corner=DR, font_size=13)
        with self.voiceover(
            "Third, taxes. <bookmark mark='a'/> In 1927 Frank Ramsey, a twenty-four-year-old Cambridge "
            "mathematician, asked how to raise a given revenue with the least deadweight loss. "
            "<bookmark mark='b'/> Suppose the government must raise ten dollars from two goods, with a hundred "
            "dollars spent on each: a staple with an elasticity of minus nought point three and a treat with minus "
            "one point two. <bookmark mark='c'/> The same five percent tax on both costs nineteen cents of "
            "deadweight loss. <bookmark mark='d'/> Eight percent on the staple and two on the treat raises the same "
            "money for twelve cents. Ramsey's rule: tax goods in inverse proportion to their elasticities, because "
            "a tax on a good people can't avoid distorts little. <bookmark mark='e'/> But this part has shown who "
            "can't avoid staples: the poor, who spend the largest share on them. Efficiency says tax the staple, "
            "equity says don't, and Part forty-one is about that trade-off."
        ) as vo:
            self.play(FadeIn(tag), FadeIn(head))
            vo.wait_until("a")
            self.play(Indicate(head, color=WHITE))
            vo.wait_until("b")
            self.play(FadeIn(rows[0]), FadeIn(rows[1]))
            vo.wait_until("c")
            self.play(FadeIn(rows[2]))
            vo.wait_until("d")
            self.play(FadeIn(rows[3]), FadeIn(rows[4]))
            vo.wait_until("e")
            self.play(FadeIn(rows[5]), FadeIn(rows[6]))
        self.clear_scene()

from __future__ import annotations

from videos.economics.econ22.common import *  # noqa: F403


class Keynes(VoiceoverScene):
    def construct(self):
        card(self, 2, r"Keynes's function and Kuznets's puzzle", r"Why do the rich save a larger share of income, \ "
             r"while nations save the same share as they grow rich?", "Chapter two. Keynes's function and Kuznets's "
             "puzzle.", lit={1936: r"Keynes", 1946: r"Kuznets", 1957: r"Friedman"}, scale=("household", "nation"),
             horizon=("a year", "a century"))
        self.law()
        self.puzzle()
        self.island()
        self.friedman()

    def law(self):
        k = load("kuznets")
        rows = VGroup(
            quote_card(r"men are disposed, as a rule and on the average, to increase their consumption as their "
                       r"income increases, but not by as much as the increase in their income", r"John Maynard "
                       r"Keynes, \emph{The General Theory}, 1936, ch.\ 8", width=11.4, font_size=24),
            MathTex(r"C = a + bY, \qquad 0 < b < 1, \quad a > 0", font_size=44, color=SPEND),
            label(r"so the average propensity $C/Y$ falls as income rises: \ the rich save a larger share",
                  font_size=24, color=GREY_A),
        ).arrange(DOWN, buff=0.5).move_to(UP * 0.1)
        del k
        with self.voiceover(
            "In 1936 John Maynard Keynes stated what he called a fundamental psychological law. "
            "<bookmark mark='a'/> Men are disposed, as a rule and on the average, to increase their consumption as "
            "their income increases, but not by as much as the increase in their income. <bookmark mark='b'/> "
            "Write it as a line: consumption equals a constant plus a fraction b of income, with b between zero and "
            "one. That fraction is the marginal propensity to consume. <bookmark mark='c'/> Because of the "
            "constant, the average propensity, consumption over income, falls as income rises. The rich save a "
            "larger share. And household surveys agreed: across families in any one year, saving rises with "
            "income."
        ) as vo:
            self.play(FadeIn(rows[0]))
            vo.wait_until("b")
            self.play(FadeIn(rows[1]))
            vo.wait_until("c")
            self.play(FadeIn(rows[2]))
        self.clear_scene()

    def puzzle(self):
        k = load("kuznets")
        ax = plane([1958, 2026], [0.75, 1.0], center=LEFT * 2.3 + DOWN * 0.35, x_length=7.4, y_length=4.8,
                   xticks=[1960, 1980, 2000, 2020], yticks=[0.75, 0.8, 0.85, 0.9, 0.95, 1.0],
                   ylabel=r"consumption $\div$ disposable income", xfmt=lambda v: f"{v:.0f}",
                   yfmt=lambda v: f"{v:.2f}", font_size=16)
        line_ = path(ax, k["years"], k["ratio"], color=SPEND, width=4, smooth=False)
        side = VGroup(
            label(r"Simon Kuznets, \ 1946: \ American data back to 1869", font_size=20, color=GREY_A),
            label(r"income rose many times over; \\ the share consumed hardly moved", font_size=20, color=WHITE),
            label(rf"since 1959: \ real disposable income \\ $\times{k['income_growth']:.1f}$; \ the ratio stayed "
                  rf"between \\ {k['ratio_min']:.2f} and {k['ratio_max']:.2f}", font_size=20, color=SPEND),
            label(r"Keynes's function predicts \\ a falling ratio", font_size=20, color=HOLD),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.35).to_edge(RIGHT, buff=0.3)
        tag = data_tag(rf"BEA via FRED: \ PCE, \ PCEPI, \ DSPIC96 \ (retrieved {data.fred('PCE')['retrieved']})",
                       corner=DR, font_size=12)
        with self.voiceover(
            "Then the puzzle. <bookmark mark='a'/> In 1946 Simon Kuznets assembled American national income back to "
            "1869. <bookmark mark='b'/> Income per head had risen several times over. The share of it consumed had "
            "hardly moved, decade after decade. <bookmark mark='c'/> The modern accounts say the same. Since 1959 "
            f"real disposable income has risen about {k['income_growth']:.1f} times, and consumption has stayed "
            f"between {say_num(k['ratio_min'], 2)} and {say_num(k['ratio_max'], 2)} of it. <bookmark mark='d'/> "
            "Keynes's function, fitted across families, says the ratio should fall as a country grows richer. "
            "It does not. Across households the rich save more; across time the nation saves the same share. "
            "Both are true. Why?"
        ) as vo:
            self.play(FadeIn(ax), FadeIn(tag))
            vo.wait_until("a")
            self.play(FadeIn(side[0]))
            vo.wait_until("b")
            self.play(FadeIn(side[1]))
            vo.wait_until("c")
            self.play(Create(line_), FadeIn(side[2]), run_time=2.5)
            vo.wait_until("d")
            self.play(FadeIn(side[3]))
        self.clear_scene()

    def island(self):
        k = load("kuznets")
        f = k["island"]
        T = k["truth"]
        ax = plane([0, 3.2], [0, 2.6], center=LEFT * 2.6 + DOWN * 0.35, x_length=6.4, y_length=5.0,
                   xticks=[0, 1, 2, 3], yticks=[0, 1, 2], xlabel=r"measured income this year",
                   ylabel=r"consumption", xfmt=lambda v: f"{v:g}", yfmt=lambda v: f"{v:g}", font_size=16)
        pts = VGroup(*[Dot(ax.ax.c2p(x, y), radius=0.025, color=SPEND).set_opacity(0.55)
                       for x, y in zip(f["sample_Y"], f["sample_C"]) if x < 3.2 and y < 2.6])
        fit = seg(ax, 0, f["intercept"], 3.2, f["intercept"] + 3.2 * f["slope"], color=WHITE, width=4)
        side = VGroup(
            label(rf"{commas(T['n'])} households \ (simulated)", font_size=21, color=GREY_A),
            label(rf"the fitted line: \ $C = {f['intercept']:.2f} + {f['slope']:.2f}\,Y$", font_size=22,
                  color=WHITE),
            label(r"Keynes's function, \ found again", font_size=21, color=WHITE),
            label(r"share consumed, \ by tenth of income:", font_size=20, color=GREY_A),
            label(rf"poorest tenth \ {f['apc_by_decile'][0]:.2f}, \ richest \ {f['apc_by_decile'][-1]:.2f}",
                  font_size=21, color=SAVE),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.3).to_edge(RIGHT, buff=0.5)
        tag = island_tag(corner=DR, font_size=14)
        with self.voiceover(
            "The Island can show you, because its households now number "
            f"{T['n']:,}, and we know their truth. <bookmark mark='a'/> Here is a survey of them in one year: "
            "each household's measured income, and what it consumed. <bookmark mark='b'/> Fit Keynes's line "
            f"through them: a constant of {f['intercept']:.2f} and a slope of {f['slope']:.2f}. "
            "<bookmark mark='c'/> And by tenths of income, the poorest tenth consumes "
            f"{f['apc_by_decile'][0]:.2f} times its income this year, more than it earns, and the richest "
            f"{f['apc_by_decile'][-1]:.2f}. The rich save more. Keynes's function, found again."
        ) as vo:
            self.play(FadeIn(ax), FadeIn(tag), FadeIn(side[0]))
            vo.wait_until("a")
            self.play(LaggedStart(*[FadeIn(d) for d in pts], lag_ratio=0.002), run_time=2.5)
            vo.wait_until("b")
            self.play(Create(fit), FadeIn(side[1]), FadeIn(side[2]))
            vo.wait_until("c")
            self.play(FadeIn(side[3]), FadeIn(side[4]))
        self.clear_scene()

    def friedman(self):
        k = load("kuznets")
        f = k["island"]
        T = k["truth"]
        rows = VGroup(
            label(r"the truth planted on the Island:", font_size=24, color=TRUTH_C),
            MathTex(r"C_i = 0.9\,Y^P_i, \qquad Y_i = Y^P_i \times \text{a transitory part}", font_size=40,
                    color=TRUTH_C),
            label(r"every household consumes nine tenths of its \emph{permanent} income", font_size=23,
                  color=GREY_A),
            label(r"a household with a good year looks rich and seems to save; \ a bad year, poor and seems to borrow",
                  font_size=22, color=SAVE),
            MathTex(r"\text{slope in logs} = \frac{\operatorname{var}(\ln Y^P)}{\operatorname{var}(\ln Y^P) + "
                    r"\operatorname{var}(\text{transitory})} = \frac{0.5^2}{0.5^2 + 0.3^2} = "
                    + f"{f['elasticity_theory']:.2f}", font_size=34),
            label(rf"measured: \ {f['elasticity']:.2f}; \ and over {T['years']} years of growth, \ "
                  rf"$C/Y$ stays at {f['apc_time'][0]:.2f}--{f['apc_time'][-1]:.2f}", font_size=22, color=SPEND),
        ).arrange(DOWN, buff=0.32)
        hc = history_card(1957, r"Milton Friedman", r"\emph{A Theory of the Consumption Function}", color=INCOME,
                          width=6.6, font_size=21)
        VGroup(hc, rows).arrange(DOWN, buff=0.4).move_to(DOWN * 0.1)
        tag = island_tag(corner=DR, font_size=14)
        with self.voiceover(
            "But we planted something else. <bookmark mark='a'/> Every household on the Island consumes nine tenths "
            "of its permanent income, the income it expects to earn on average. Its measured income this year adds "
            "a transitory part: a good harvest, a bad one. <bookmark mark='b'/> There is no Keynesian constant, and "
            "no rich household saves a larger share of its permanent income. <bookmark mark='c'/> A household with "
            "a good year looks rich in the survey and seems to save. One with a bad year looks poor and seems to "
            "borrow. Sorting by this year's income sorts by luck. <bookmark mark='d'/> That is Milton Friedman's "
            "answer to Kuznets, in 1957: an errors-in-variables problem, from Part 4. The slope in logs is the "
            "share of the variance of income that is permanent, here " + f"{f['elasticity_theory']:.2f}. "
            f"<bookmark mark='e'/> The survey gives {f['elasticity']:.2f}. And as everyone's permanent income grows "
            f"for {T['years']} years, the ratio of consumption to income stays at nine tenths, as Kuznets found."
        ) as vo:
            self.play(FadeIn(hc), FadeIn(tag), FadeIn(rows[0]), FadeIn(rows[1]))
            vo.wait_until("a")
            self.play(FadeIn(rows[2]))
            vo.wait_until("c")
            self.play(FadeIn(rows[3]))
            vo.wait_until("d")
            self.play(FadeIn(rows[4]))
            vo.wait_until("e")
            self.play(FadeIn(rows[5]))
        self.clear_scene()

from __future__ import annotations

from videos.economics.econ40.common import *  # noqa: F403

PROBLEMS = [
    r"Lorenz: \ five people earn 1, \ 2, \ 3, \ 4 and 10. \ Draw the Lorenz curve and find the Gini, \ the top 20\% "
    r"share and Atkinson's index with $\varepsilon = 1$.",
    r"Pareto: \ the top 1\% hold 20\% of income and the top 0.1\% hold 9\%. \ What is $\alpha$? \ What share do "
    r"the top 0.01\% hold?",
    r"Random growth: \ with $\nu = 0$, \ $\sigma = 0.1$ and $\delta = 0.02$, \ find $\zeta$. \ What happens to "
    r"$\zeta$ if careers last twice as long?",
    r"Wealth: \ with $r - g - c = 0.01$, \ $\sigma = 0.15$, \ $\delta = 0.02$, \ find the tail exponent. \ Is the "
    r"mean finite?",
    r"Kuznets: \ $\sigma_a = 0.4$, \ $\sigma_m = 0.7$, \ $\Delta = 1$. \ At what modern share is the variance of "
    r"log income largest?",
    r"Attenuation: \ $\sigma_{\mathrm{perm}} = 0.6$, \ $\sigma_{\mathrm{trans}} = 0.55$, \ $\beta = 0.45$. \ "
    r"What does one year of parents' income estimate? \ Five years?",
    r"Ranks: \ with a rank-rank slope of 0.34 and a mean rank of 50 at the 50th percentile, \ what is the expected "
    r"rank of a child from the 25th percentile? \ From the 75th?",
    r"$\bigstar$ \ Derive $\zeta$: \ substitute $f(y) = e^{-\zeta y}$ into the stationary Kolmogorov equation "
    r"above the entry point, \ and show that the positive root is the Pareto exponent of $x = e^y$.",
]


class Outro(VoiceoverScene):
    def construct(self):
        self.answer()
        self.recap()
        self.problems()
        self.references()
        self.next_part()

    def answer(self):
        q = wrapped_label(ASK, 12.0, 40, E.ACCENT).move_to(UP * 2.2)
        a = wrapped_label(r"Very unequal at the top, \ and more so since 1980, \ for income and still more for "
                          r"wealth; \ long tails come from compounding growth, \ and moved fast because a few grew "
                          r"fast; \ children escape less where inequality is high, \ less than their grandparents "
                          r"did, \ and much less in some places than others.", 11.6, 25, WHITE)
        a.next_to(q, DOWN, buff=0.5)
        F = load("film")
        mini = plane([1913, 2022], [5, 21], x_length=4.2, y_length=1.3)
        logo = path(mini, F["t"], F["v"], TOP, 2.4, smooth=False).next_to(a, DOWN, buff=0.35)
        with self.voiceover(
            "So: how unequal are incomes and wealth, why, and do children escape where they started? "
            "<bookmark mark='a'/> Very unequal at the top, and more so since 1980, for income and still more for "
            "wealth. The long tails come from growth that compounds, and they moved fast because a few incomes grew "
            "fast. And children escape less where inequality is high, less than their grandparents did, and much "
            "less in some places than in others, which is where policy has found its firmest footing."
        ) as vo:
            self.play(FadeIn(q, shift=UP * 0.2))
            vo.wait_until("a")
            self.play(FadeIn(a, shift=UP * 0.1), run_time=2)
            self.play(Create(logo), run_time=1.5)
        self.clear_scene()

    def recap(self):
        P, M, T, Pa, S, W, K, I_, G, C, Pl, Wo = (load(x) for x in (
            "parade", "measures", "top", "pareto", "speed", "wealth", "kuznets", "ige", "gatsby", "chetty", "places",
            "world"))
        items = [
            (rf"the parade: \ average height at minute {P['minute_mean']:.0f}; \ the top 0.01\% at "
             rf"{P['h_top001']:.0f} m", TOP),
            (rf"measures: \ the Island's Gini {M['m']['gini']['value']:.2f} $\pm$ {M['m']['gini']['se']:.2f}; \ "
             r"crossing curves need ethics", LORENZ),
            (rf"top shares: \ a U, \ {T['at']['1928']['top1']:.0f}\% $\to$ {T['at']['1970']['top1']:.0f}\% $\to$ "
             rf"{T['at']['2022']['top1']:.0f}\%; \ the after-tax rise disputed", LOSS),
            (rf"Pareto: \ $\alpha$ {Pa['a1970']:.1f} in 1970, \ {Pa['a2022']:.1f} in 2022; \ random growth gives the "
             r"tail", TOP),
            (rf"speed: \ pure random growth {S['hl_pure']:.0f} years, \ fast types {S['hl_types']:.0f}", TYPES),
            (rf"wealth: \ top 1\% {W['last']['top1']:.0f}\%; \ $\alpha$ {W['last']['alpha']:.2f}; \ $r - g$ fattens "
             r"the tail", WEALTH),
            (r"Kuznets: \ an inverted U from migration; \ the data drew a U \ (partly right)", MIDDLE),
            (rf"the elasticity: \ one year {I_['rows'][0]['ige']:.2f}, \ fifteen {I_['rows'][-1]['ige']:.2f}, \ truth "
             rf"{I_['beta']:.2f}", PARENT),
            (rf"Gatsby: \ unequal places, \ less mobility \ (correlation {G['corr_am']:.2f})", CHILD),
            (rf"ranks: \ slope {C['slope']:.2f}; \ bottom to top {100 * C['q5q1']:.1f}\%; \ out-earning parents "
             rf"{100 * C['absmob'][0]:.0f}\% $\to$ {100 * C['absmob'][-1]:.0f}\%", CHILD),
            (rf"places: \ {100 * Pl['pick_q'][0]:.1f}\% in Charlotte, \ {100 * Pl['pick_q'][5]:.1f}\% in San Jose; \ "
             r"moving young helps", GAIN),
            (rf"the world: \ between countries {Wo['all'][0]:.2f} $\to$ {Wo['all'][-1]:.2f}, \ thanks to China and "
             r"India", MIDDLE),
        ]
        rows = VGroup(*[label(rf"{n + 1}.\ \ {txt}", font_size=28, color=col) for n, (txt, col) in enumerate(items)])
        rows.arrange(DOWN, aligned_edge=LEFT, buff=0.2)
        head = label(r"Part 40, \ in twelve lines", font_size=42).to_edge(UP, buff=0.3)
        if rows.width > 13.2:
            rows.width = 13.2
        room = head.get_bottom()[1] - 0.35 + 3.75
        if rows.height > room:
            rows.scale_to_fit_height(room)
        rows.next_to(head, DOWN, buff=0.35)
        with self.voiceover(
            "Part forty in twelve lines. <bookmark mark='a'/> In Pen's parade, average height arrives only in the "
            "last third of the hour, and the giants come at the end. Every measure of inequality watches some part "
            "of the distribution, and when Lorenz curves cross, ranking societies takes a value judgement. America's "
            "top shares traced a U over the century, though how much the top pulled away after taxes and transfers "
            "is disputed. Top incomes follow Pareto's law, and random growth with turnover explains why; the tail "
            "fattened faster than pure random growth allows, which points to a few fast-growing incomes. Wealth is "
            "more concentrated still, and a point or two of r minus g fattens its tail. Kuznets's inverted U "
            "described the arithmetic of migration, not the century that followed. The intergenerational "
            "elasticity is understated by one year of income, and countries and places with more inequality have "
            "less mobility. A child's rank rises about a third of a percentile for each percentile of the parents', "
            "half of children now out-earn their parents, and where a child grows up matters, most when the child "
            "is young. Between countries, the world has become more equal, mostly through China and India."
        ) as vo:
            self.play(FadeIn(head))
            vo.wait_until("a")
            self.play(LaggedStart(*[FadeIn(r_, shift=RIGHT * 0.15) for r_ in rows], lag_ratio=0.8), run_time=44.0)
        self.clear_scene()

    def problems(self):
        ps = problem_set(PROBLEMS, font_size=19, width=13.0)
        with self.voiceover(
            "The problems. A Lorenz curve by hand; the Pareto exponent from two shares; the random growth exponent; "
            "the tail of wealth; Kuznets's peak; attenuation; ranks; and a starred derivation of the exponent from "
            "the Kolmogorov equation. Full solutions are in the part's notes."
        ):
            self.play(FadeIn(ps.head), FadeIn(ps.rows[0], shift=UP * 0.1), run_time=0.8)
            self.play(LaggedStart(*[FadeIn(r) for r in ps.rows[1:]], lag_ratio=0.4), run_time=6)
        self.wait(4)
        self.clear_scene()

    def references(self):
        rc = reference_card(
            [r"Anthony Atkinson, \emph{Inequality: What Can Be Done?} (2015)",
             r"Thomas Piketty, \emph{Capital in the Twenty-First Century} (2014)",
             r"Branko Milanovic, \emph{Global Inequality} (2016)",
             r"Frank Cowell, \emph{Measuring Inequality} (3rd edition, 2011)"],
            [r"Pareto (1896); \ Champernowne (1953); \ Kuznets (1955); \ Atkinson (1970); \ Pen (1971)",
             r"Solon (1992); \ Piketty and Saez (2003); \ Mazumder (2005); \ Gabaix (2009)",
             r"Corak (2013); \ Chetty, \ Hendren, \ Kline and Saez (2014); \ Rognlie (2015)",
             r"Krusell and Smith (2015); \ Gabaix, \ Lasry, \ Lions and Moll (2016); \ Lakner and Milanovic (2016)",
             r"Chetty et al.\ (2016, 2017); \ Chetty and Hendren (2018); \ Piketty, \ Saez and Zucman (2018)",
             r"Jakobsen et al.\ (2020); \ Black et al.\ (2020); \ Auten and Splinter (2024)"])
        with self.voiceover(
            "The reading: Anthony Atkinson's Inequality: What Can Be Done?; Piketty's Capital in the Twenty-First "
            "Century; Milanovic's Global Inequality; and Frank Cowell's Measuring Inequality for the measures. Then "
            "the papers, from Pareto to the measurement dispute."
        ):
            self.play(FadeIn(rc))
        self.wait(1.5)
        self.clear_scene()

    def next_part(self):
        hc = history_card(1974, r"Arthur Laffer", r"draws a curve on a napkin for two aides to President Ford: \ at "
                          r"a tax rate of zero the government collects nothing, \ and at a hundred percent also "
                          r"nothing", color=E.ACCENT, width=10.4, font_size=24)
        nxt = VGroup(label(r"Next: \ Part 41 \ $\cdot$ \ Act VIII, \ Work and the State", font_size=30, color=GREY_B),
                     label(r"Taxes", font_size=46),
                     label(r"who really pays a tax, \ and how high should the top rate be?", font_size=24,
                           color=E.ACCENT)).arrange(DOWN, buff=0.22)
        head = label(r"from the distribution \ to what a state can do about it", font_size=26,
                     color=GREY_A).to_edge(UP, buff=0.5)
        VGroup(hc, nxt).arrange(DOWN, buff=0.6).next_to(head, DOWN, buff=0.5)
        with self.voiceover(
            "This part measured the distribution. The next asks what taxes can do to it, and at what cost. "
            "<bookmark mark='a'/> In December 1974, in a Washington restaurant, the economist Arthur Laffer drew a "
            "curve on a napkin for two of President Ford's aides: at a tax rate of zero the government collects "
            "nothing, and at a hundred percent also nothing. The curve is correct. The question the napkin cannot "
            "answer is where its top is. <bookmark mark='b'/> Part forty-one: taxes. Who really pays a tax, and how "
            "high should the top rate be?"
        ) as vo:
            self.play(FadeIn(head))
            vo.wait_until("a")
            self.play(FadeIn(hc, shift=UP * 0.2))
            vo.wait_until("b")
            self.play(FadeIn(nxt, shift=UP * 0.2))
        self.wait(9.5)
        self.clear_scene()

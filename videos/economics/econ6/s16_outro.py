from __future__ import annotations

from videos.economics.econ6.common import *  # noqa: F403
from videos.economics.econ6.s01_hook import voucher_glyph

PROBLEMS = [
    r"Bo: \ $u = x^{0.6}y^{0.4}$, \ \$60, \ coconuts \$6; \ fish fall from \$10 to \$6. \ Find the bundles A, C, "
    r"\ Hicks's B and Slutsky's B$'$, \ and both splits into substitution and income effects.",
    r"A good takes 30\% of a budget, \ with compensated elasticity $-0.5$ and income elasticity $0.8$. \ Find its "
    r"price elasticity. \ How negative must the income elasticity be for demand to slope up?",
    r"Play it: \ \$21, \ 14{,}000 calories; \ coconuts 1{,}400 calories, \ fish 700 at \$2. \ Find the bundle at "
    r"coconut prices \$1.20 and \$1.50, \ and show the elasticity in the subsistence zone is $r/(1-r)$.",
    r"Derive the expenditure function and Hicksian demand for $u = x^{a}y^{1-a}$, \ and check Shephard's lemma and "
    r"Roy's identity.",
    r"Shares $w_i = \alpha_i + \sum_j \gamma_{ij}\log p_j$ with $\gamma_{12} = 0.08$, $\gamma_{21} = 0.02$. \ "
    r"Compensated income goes counter-clockwise round a square of side 0.2 in $(\log p_1, \log p_2)$. \ By how much does it change, "
    r"and in which direction?",
    r"2024: \ the poorest fifth spent \$5{,}498 on food (33.0\% of income), \ the middle fifth \$9{,}097 "
    r"(12.2\%). \ Find the incomes and the arc income elasticity of food.",
    r"Coconuts: \ $x = -4p + 0.1m + 6$, \ $m = 60$, \ $p = 1.20$. \ A 60-cent tax: \ find Marshall's loss, \ "
    r"Willig's approximation to CV, \ and Hausman's exact CV and deadweight loss.",
    r"$\bigstar$ \ Hamilton's method assumes the food Engel curve's shape is stable. \ Let tastes drift away from "
    r"food by 0.2 points of share a year. \ What does the method report, \ and how could you tell drift from CPI "
    r"bias?",
]


class Outro(VoiceoverScene):
    def construct(self):
        self.answer()
        self.recap()
        self.problems()
        self.references()
        self.next_part()

    def answer(self):
        q = wrapped_label(ASK, 12.0, 42, E.ACCENT).move_to(UP * 2.0)
        a = wrapped_label(r"Two things at once: \ the good becomes cheaper or dearer relative to everything else, \ and "
                          r"the buyer richer or poorer. \ The first always pushes demand the expected way; \ the "
                          r"second usually agrees, \ but for the poorest it can win. \ And the change in welfare is "
                          r"a change in the expenditure function: \ a number of dollars, \ different for every "
                          r"household.", 11.6, 30, WHITE)
        a.next_to(q, DOWN, buff=0.55)
        logo = voucher_glyph(0.6).next_to(a, DOWN, buff=0.45)
        with self.voiceover(
            "So: when a price changes, what happens to what people buy, and to how well off they are? "
            "<bookmark mark='a'/> Two things happen at once. The good becomes cheaper or dearer relative to "
            "everything else, and the buyer becomes richer or poorer. The first always pushes demand the expected "
            "way. The second usually agrees, but for households that live on one staple it can win, and demand "
            "slopes up. And how much better or worse off they are is a change in the expenditure function: a number "
            "of dollars, different for every household."
        ) as vo:
            self.play(FadeIn(q, shift=UP * 0.2))
            vo.wait_until("a")
            self.play(FadeIn(a, shift=UP * 0.1), run_time=2)
            self.play(Create(logo.body), Create(logo.perf), FadeIn(logo.stub))
        self.clear_scene()

    def recap(self):
        h = tables.JENSEN_MILLER_2008.data["hunan"]
        p, b, v, lp, e, hm, w, lv, j = (load(x) for x in ("playit", "bo", "vouchers", "loop", "engel", "hamilton",
                                                           "welfare", "living", "frontier"))
        items = [
            (rf"Hunan's vouchers: \ cheaper rice, \ less rice: \ {h['share_le_080'][0]:+.2f} for the poor but not "
             r"the poorest", GIFF),
            (rf"Play it: \ dearer coconuts, \ {p['before'][1]:.1f} $\to$ {p['after'][1]:.1f} coconuts", COCO),
            (r"demand is homogeneous of degree zero; \ elasticities add up", WHITE),
            (rf"Slutsky: \ Bo's +{b['C'][0] - b['A'][0]:.1f} fish = +{b['sub_hicks']:.2f} substitution "
             rf"+ {b['inc_hicks']:.2f} income", SUB),
            (r"$\varepsilon = \varepsilon^h - w\,\eta$: \ inferior, \ a big share, \ no room to substitute", INC),
            (rf"the Island's vouchers: \ all {signed(v['rows']['full'][0])}, \ 60--80\% {signed(v['rows']['share_060_080'][0])}"
             rf" \ (planted {v['planted_giffen']:+.2f})", GIFF),
            (r"duality: \ four functions; \ Roy, \ Shephard; \ $e$ concave in prices", HICKS),
            (rf"integrability: \ a symmetric Slutsky matrix, \ or a "
             rf"{abs(100 * (np.exp(lp['circular']['gap']) - 1)):.0f}\% money pump", E.ACCENT),
            (rf"Engel: \ food at home {100 * e['food_share'][0]:.0f}\% $\to$ {100 * e['food_share'][-1]:.1f}\%; \ "
             rf"Hamilton's drift: \ {100 * hm['per_year']:.2f}\% a year (planted 1\%)", IC),
            (rf"Bo's welfare: \ CV \${w['cv']:.2f} $<$ CS \${w['cs']:.2f} $<$ EV \${w['ev']:.2f}; \ "
             rf"deadweight loss {100 * w['taxes'][1]['dwl_error']:.0f}\% off", E.ACCENT),
            (rf"Laspeyres $\ge$ true $\ge$ Paasche; \ Cheerios' virtual price \${lv['cheerios']['virtual']:.2f}",
             HICKS),
            (rf"inflation: \ the poorest fifth {j['jaravel']['retail_gap'][0]:.2f} points a year above the richest",
             GIFF),
        ]
        rows = VGroup(*[label(rf"{i + 1}.\ \ {txt}", font_size=28, color=col) for i, (txt, col) in enumerate(items)])
        rows.arrange(DOWN, aligned_edge=LEFT, buff=0.2)
        head = label(r"Part 6, \ in twelve lines", font_size=42).to_edge(UP, buff=0.3)
        if rows.width > 13.2:
            rows.width = 13.2
        room = head.get_bottom()[1] - 0.35 + 3.75
        if rows.height > room:
            rows.scale_to_fit_height(room)
        rows.next_to(head, DOWN, buff=0.35)
        with self.voiceover(
            "Part six in twelve lines. <bookmark mark='a'/> Rice vouchers in Hunan made poor households eat less "
            "rice, and in Play it you bought more coconuts when they got dearer. Demand depends only on prices "
            "relative to income, and its elasticities add up. Slutsky split every price change into substitution "
            "and income, and the elasticity form gave the recipe for demand that slopes up. On the Island, Jensen "
            "and Miller's method found the planted Giffen households, and showed how an average can hide them. "
            "Duality gave four functions for one consumer, and integrability asked whether any consumer lies "
            "behind a demand system, or a money pump. Engel's law held across a century and across today's "
            "households, and its drift read the error in a price index. Welfare came in dollars, three ways, with a "
            "warning about deadweight losses. A fixed basket overstates the cost of living, and new goods are worth "
            "their virtual prices. And inflation itself depends on who you are."
        ) as vo:
            self.play(FadeIn(head))
            vo.wait_until("a")
            self.play(LaggedStart(*[FadeIn(r_, shift=RIGHT * 0.15) for r_ in rows], lag_ratio=0.8), run_time=40.0)
        self.clear_scene()

    def problems(self):
        ps = problem_set(PROBLEMS, font_size=20, width=13.0)
        with self.voiceover(
            "The problems. Bo's two decompositions, by hand; the Slutsky equation in elasticities, and how inferior "
            "a good must be to be Giffen; the Play-it household and its elasticity; the four functions of a "
            "Cobb–Douglas consumer; a money pump on a square; Engel's law from two numbers; a tax's exact and "
            "approximate costs; and a research problem, marked with a star, on telling a drifting Engel curve from "
            "a biased price index. Full solutions are in the part's notes."
        ):
            self.play(FadeIn(ps.head), FadeIn(ps.rows[0], shift=UP * 0.1), run_time=0.8)
            self.play(LaggedStart(*[FadeIn(r, shift=UP * 0.1) for r in ps.rows[1:]], lag_ratio=0.4), run_time=6)
        self.wait(4)
        self.clear_scene()

    def references(self):
        rc = reference_card(
            [r"Hal Varian, \emph{Intermediate Microeconomics}, chs.\ 6--10, 14",
             r"Andreu Mas-Colell, Michael Whinston and Jerry Green, \emph{Microeconomic Theory}, chs.\ 2--3",
             r"Angus Deaton and John Muellbauer, \emph{Economics and Consumer Behavior} (1980)",
             r"Walter Nicholson and Christopher Snyder, \emph{Microeconomic Theory}, chs.\ 5--6"],
            [r"Slutsky (1915); \ Hicks and Allen (1934), \emph{Economica}; \ Hicks, \emph{Value and Capital} (1939)",
             r"Jensen and Miller (2008), \emph{AER} 98(4); \ Stigler (1947); \ Rosen (1999), \emph{JPE}",
             r"Roy (1947); \ Shephard (1953); \ Hurwicz and Uzawa (1971); \ Konüs (1924); \ Hicks (1940)",
             r"Willig (1976), \emph{AER}; \ Hausman (1981), \emph{AER}; \ Hausman (1997), new goods",
             r"Stone (1954); \ Deaton and Muellbauer (1980), \emph{AER}; \ Gorman (1953); \ Houthakker (1957)",
             r"Hamilton (2001), \emph{AER}; \ Costa (2001), \emph{JPE}; \ Almås (2012), \emph{AER}; \ Deaton (1989)",
             r"Feenstra (1994); \ Jaravel (2019), \emph{QJE}; \ Redding and Weinstein (2020); \ Jaravel and Lashkari "
             r"(2024); \ Atkin et al.\ (2024)"])
        with self.voiceover(
            "The reading for this part: the demand chapters of Varian's intermediate textbook; chapters two and "
            "three of Mas-Colell, Whinston and Green for the graduate version; Deaton and Muellbauer's book on "
            "consumer behaviour, which is still the best account of demand systems; and Nicholson and Snyder. Then "
            "the papers, from Slutsky's to the scanner-data frontier."
        ):
            self.play(FadeIn(rc))
        self.wait(1.5)
        self.clear_scene()

    def next_part(self):
        hc = history_card(1738, r"Daniel Bernoulli, \ St Petersburg",
                          r"a coin game whose expected prize is infinite, \ which nobody would pay much to play: \ "
                          r"his answer is the first utility function", color=E.ACCENT, width=9.0,
                          font_size=26).move_to(UP * 0.6)
        lead = label(r"from prices today \ to time and risk", font_size=40, color=GREY_A)
        nxt = VGroup(label(r"Next: \ Part 7", font_size=30, color=GREY_B),
                     label(r"Time and Risk", font_size=56, color=WHITE),
                     label(r"how do people choose when the pay-off comes later, \ or may not come at all?",
                           font_size=26, color=GREY_A)).arrange(DOWN, buff=0.15).next_to(hc, DOWN, buff=0.6)
        with self.voiceover(
            "This part followed one price change through to what people buy and what they're worth. The next adds "
            "the two things every real choice has: time, and risk. <bookmark mark='a'/> In 1738 Daniel Bernoulli "
            "asked what you would pay to play a coin game whose expected prize is infinite. Almost nobody would pay "
            "much, and his explanation was the first utility function. <bookmark mark='b'/> Part seven: time and "
            "risk."
        ) as vo:
            self.play(FadeIn(lead))
            vo.wait_until("a")
            self.play(FadeOut(lead), FadeIn(hc, shift=UP * 0.2))
            vo.wait_until("b")
            self.play(FadeIn(nxt, shift=UP * 0.1))
        self.wait(3.0)
        self.play(*[FadeOut(m) for m in self.mobjects], run_time=1.5)

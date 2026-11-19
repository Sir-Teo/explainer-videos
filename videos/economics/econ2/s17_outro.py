from __future__ import annotations

from videos.economics.econ2.common import *  # noqa: F403

PROBLEMS = [
    r"A household's value of one more litre of water a day, with $q$ litres already, is $30\,e^{-q/28}$ dollars. \ "
    r"Show that the first 150 litres are worth about \$836 in all, \ while the 150th is worth about 14 cents. \ Which "
    r"of the two numbers does the price of water measure?",
    r"Ana's cups are worth \$4.00, \$2.50, \$1.20 and \$0.40; \ Bo's \$3.00, \$1.50 and \$0.60; \ Chidi's \$5.00 and "
    r"\$2.00. \ Draw the market's demand. \ How many cups are bought at \$1.00, \ and at \$2.25?",
    r"In Part 1's pit the band is \$2.20 to \$2.30. \ Which one card, changed, would narrow it to \$2.20 to \$2.25? \ "
    r"Which would raise it, \ and why can the keenest buyer's card rise as far as you like without moving it?",
    r"On the demand line $Q = 400\,(1 - p/6)$, \ find the elasticity at \$2, \$3 and \$4, \ and the price at which "
    r"buyers spend the most. \ Show that the answer is the price where the elasticity is $-1$.",
    r"With that demand and supply $Q = 400\,(p - 0.5)/4.5$, \ a tax of 40 cents a fish is levied on the fishers. \ "
    r"Find the price buyers pay, \ the price fishers keep, \ and the buyers' share of the tax; \ check it against "
    r"$\varepsilon_S/(\varepsilon_S + |\varepsilon_D|)$, \ and show the answer is the same if the buyers pay the tax.",
    r"On the same lines a cap holds the price at \$2.26. \ Find the shortage, \ the triangle, \ and the extra loss if "
    r"the fish go by lottery among everyone who wants one. \ Why can the lottery cost more than the triangle?",
    r"$\star$ \ Replace the pit's learning sellers with two Q-learning sellers who meet day after day. \ Under what "
    r"conditions does their price stay above the band, \ and what evidence would tell a court it was collusion?",
]


class Outro(VoiceoverScene):
    def construct(self):
        self.answer()
        self.recap()
        self.problems()
        self.references()
        self.next_part()

    def answer(self):
        q = label(ASK, font_size=56, color=E.ACCENT).move_to(UP * 1.6)
        a = wrapped_label(r"Both blades: \ what the last unit is worth to the last buyer, \ and what it costs the last "
                          r"seller. \ Traders who see only their own cards find it, \ if they learn from what they "
                          r"see.", 11.5, 34, WHITE).next_to(q, DOWN, buff=0.6)
        logo = scissors_logo(1.0).next_to(a, DOWN, buff=0.6)
        with self.voiceover(
            "So: what sets a price? <bookmark mark='a'/> Both blades. What the last unit is worth to the last "
            "buyer, and what it costs the last seller. Traders who see only their own cards find that price, as "
            "long as they learn from what they see."
        ) as vo:
            self.play(FadeIn(q, shift=UP * 0.2))
            vo.wait_until("a")
            self.play(FadeIn(a, shift=UP * 0.1), run_time=2)
            self.play(Create(logo.demand), Create(logo.supply), FadeIn(logo.price))
        self.clear_scene()

    def recap(self):
        pl, a, fr, t, c = (load(k) for k in ("playit", "asym", "frost", "tax", "controls"))
        el = dials.DIALS["elasticity_staples"].estimates
        items = [
            (r"a price measures the margin, \ not the whole: \ water's last litre is worth little", WATER),
            (r"demand is buyers' values added sideways; \ supply is sellers' costs", E.DEMAND),
            (r"four cards fix the band: \ the last ones in, \ and the first ones out", E.ACCENT),
            (rf"a lopsided market converged too, \ to {dollars(pl['zip']['price'])}: \ Smith's prediction, \ wrong",
             E.PRED),
            (rf"zero is not enough: \ random traders missed by up to "
             rf"{100 * max(abs(a[n]['zi_miss']) for n in a):.0f} cents", GREY_A),
            (rf"elasticity: \ petrol {el[0].value:.2f} within a year, \ {el[1].value:.2f} in the long run".replace(
                "-", "$-$"), E.SUPPLY),
            (rf"the frost: \ the world's crop {100 * fr['world_change']:.0f}\%, \ the price "
             rf"{fr['ratio_peak_june75']:.1f} times".replace("-", "$-$"), COFFEE),
            (r"surplus: \ the competitive quantity makes the most; \ the triangle is what is lost", E.CS),
            (rf"a tax: \ buyers paid {dollars(t['on_sellers']['paid'])} or {dollars(t['on_buyers']['paid'])}, \ "
             r"whoever remitted it", TAX),
            (rf"a cap: \ {100 * c['cap']['zip']['efficiency']:.0f}\% of the gains, \ not "
             rf"{100 * c['cap']['best_share']:.1f}\%: \ the goods went to the wrong people", CAP),
        ]
        rows = VGroup(*[label(rf"{i + 1}.\ \ {txt}", font_size=30, color=col) for i, (txt, col) in enumerate(items)])
        rows.arrange(DOWN, aligned_edge=LEFT, buff=0.26)
        head = label(r"Part 2, \ in ten lines", font_size=42).to_edge(UP, buff=0.3)
        if rows.width > 13.2:
            rows.width = 13.2
        room = head.get_bottom()[1] - 0.35 + 3.75
        if rows.height > room:
            rows.scale_to_fit_height(room)
        rows.next_to(head, DOWN, buff=0.35)
        with self.voiceover(
            "Part two in ten lines. <bookmark mark='a'/> A price measures the margin, not the whole, which is why "
            "water is cheap. Demand is buyers' values added up sideways, and supply is sellers' costs. Four cards fix "
            "the band: the last traders in and the first ones out. A lopsided market converged too, which made "
            "Smith's prediction wrong. But traders with no intelligence missed its price; the rules give the "
            "efficiency, and learning gives the price. Elasticity grows with time: for petrol, almost nothing "
            "within a year, a third in the long run. A frost cut the world's coffee crop by a sixth and multiplied "
            "the price more than fivefold. The competitive quantity makes the largest surplus, and whatever stops "
            "trade short of it loses a triangle. A tax falls on buyers and sellers the same way whoever hands it "
            "over. And a price cap loses more than the triangle, because the goods end up with the wrong people."
        ) as vo:
            self.play(FadeIn(head))
            vo.wait_until("a")
            self.play(LaggedStart(*[FadeIn(r, shift=RIGHT * 0.15) for r in rows], lag_ratio=0.8), run_time=34.0)
        self.clear_scene()

    def problems(self):
        ps = problem_set(PROBLEMS, font_size=21, width=13.0)
        with self.voiceover(
            "The problems. The arithmetic of water and diamonds; three coffee drinkers' demand; the cards that "
            "set the pit's band; elasticity and spending along a line; a tax on the Island's fish, remitted by "
            "either side; the cost of a price cap; and a research problem, marked with a star, on algorithms that "
            "learn to keep prices high. Full solutions are in the part's notes."
        ):
            self.play(FadeIn(ps.head))
            self.play(LaggedStart(*[FadeIn(r, shift=UP * 0.1) for r in ps.rows], lag_ratio=0.4), run_time=6)
        self.wait(4)
        self.clear_scene()

    def references(self):
        rc = reference_card(
            [r"Alfred Marshall, \emph{Principles of Economics} (1890), Book V",
             r"Adam Smith, \emph{The Wealth of Nations} (1776), Book I, ch. 4",
             r"Hal Varian, \emph{Intermediate Microeconomics}, chs 1, 15--16",
             r"N. Gregory Mankiw, \emph{Principles of Economics}, chs 4--8; \ Krugman and Wells, chs 3--5"],
            [r"Smith (1962), \emph{JPE} 70; \ Gode and Sunder (1993), \emph{JPE} 101; \ Cliff and Bruten (1997)",
             r"Dupuit (1844); \ Whately (1832), Lecture IX",
             r"Havranek, Irsova and Janda (2012); \ Chetty, Looney and Kroft (2009), \emph{AER} 99",
             r"Kopczuk, Marion, Muehlegger and Slemrod (2016); \ Diamond, McQuade and Qian (2019), \emph{AER} 109",
             r"Calvano, Calzolari, Denicol\`o and Pastorello (2020), \emph{AER} 110; \ Assad, Clark, Ershov and Xu "
             r"(2024), \emph{JPE} 132"])
        with self.voiceover(
            "The reading for this part: Marshall's fifth book, still clear after more than a century; Smith's "
            "fourth chapter, for the paradox; and the demand and supply chapters of any principles textbook. Then "
            "Vernon Smith's 1962 paper, Gode and Sunder's, and the papers on taxes and rent control. Each is "
            "short, and each changed how economists think about prices."
        ):
            self.play(FadeIn(rc))
        self.wait(1.5)
        self.clear_scene()

    def next_part(self):
        hc = history_card(1934, r"Simon Kuznets reports to the United States Senate",
                          r"the first estimates of the national income: \ how big is the economy, \ and how much did "
                          r"it shrink?", color=E.ACCENT, width=9.0, font_size=26).move_to(UP * 0.6)
        nxt = VGroup(label(r"Next: \ Part 3", font_size=30, color=GREY_B),
                     label(r"The Measure", font_size=56, color=WHITE),
                     label(r"GDP three ways, \ prices and indices, \ unemployment as a survey", font_size=26,
                           color=GREY_A)).arrange(DOWN, buff=0.15).next_to(hc, DOWN, buff=0.6)
        with self.voiceover(
            "This part's prices were for one good at a time. The next part asks how you add them all up. "
            "<bookmark mark='a'/> In 1934 Simon Kuznets handed the United States Senate the first official "
            "estimates of the country's national income, in the middle of the Depression, when nobody could say how "
            "much the economy had shrunk. <bookmark mark='b'/> Part three: the measure. What GDP counts and leaves "
            "out, how you compare prices across years, and how a country counts its unemployed."
        ) as vo:
            self.play(FadeIn(hc, shift=UP * 0.2))
            vo.wait_until("b")
            self.play(FadeIn(nxt, shift=UP * 0.1))
        self.wait(3.0)
        self.play(*[FadeOut(m) for m in self.mobjects], run_time=1.5)

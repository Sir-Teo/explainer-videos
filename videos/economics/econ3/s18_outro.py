from __future__ import annotations

from videos.economics.econ3.common import *  # noqa: F403

PROBLEMS = [
    r"An island has two firms. \ The farm sells \$100 of grain, \$30 of it to the bakery; \ it imports \$10 of "
    r"seed and pays \$50 in wages. \ The bakery sells \$120 of bread to households and pays \$40 in wages. \ Find GDP "
    r"by output, \ by spending and by income, \ and each firm's profit.",
    r"Show from $Y = C + I + G + X - M$ that national saving $Y - C - G$ equals $I + (X - M)$. \ The Island's "
    r"council now buys \$20 more coconuts, \ and the grove sells \$20 fewer abroad to supply them. \ What happens to "
    r"national saving, \ investment and the trade balance, \ and how much is the Island now borrowing?",
    r"Fish triples to \$6 while coconuts stay at \$1, \ and Bo still spends half of his \$100 on each. \ Find the "
    r"Laspeyres, Paasche and Fisher indexes, \ and the income that leaves him exactly as well off.",
    r"Over one storm and one calm, \ show that chained Laspeyres multiplies to $1.5 \times 0.75 = 1.125$, \ chained "
    r"Paasche to $0.889$, \ and chained Fisher to exactly 1.",
    r"The boatyard's regression gives $\log p = 0.756 + 1.56 \log L + 0.024 \cdot \text{this year}$. \ What is the "
    r"pure price change? \ This year's boats average 5.71 m, last year's 5.00 m: \ roughly what rise in the "
    r"average price does the regression imply?",
    r"On the Island, the two discouraged islanders start looking again, \ and find nothing. \ What happens to U-3, "
    r"\ U-4 \ and the participation rate? \ Which of them gives the better reading of the labour market?",
    r"Two industries with $A = \begin{pmatrix} 0.1 & 0.2 \\ 0.3 & 0.1 \end{pmatrix}$. \ Find $(I - A)^{-1}$ and "
    r"both output multipliers, \ and the extra output of each industry for \$10 more final demand for the second.",
    r"$\star$ \ Design a test of whether a country's official growth is inflated, \ using night lights. \ What could "
    r"make lights grow faster than output in an honest country?",
]


class Outro(VoiceoverScene):
    def construct(self):
        self.answer()
        self.recap()
        self.problems()
        self.references()
        self.next_part()

    def answer(self):
        q = label(ASK, font_size=54, color=E.ACCENT).move_to(UP * 1.8)
        a = wrapped_label(r"Add up what each producer adds, \ and check it against what is spent and what is "
                          r"earned. \ Divide by a price index whose basket you choose with care, \ compare countries at "
                          r"the same prices, \ and remember what the number leaves out.", 11.5, 33, WHITE)
        a.next_to(q, DOWN, buff=0.6)
        logo = meter_glyph(0.75, 0.72).next_to(a, DOWN, buff=0.6)
        with self.voiceover(
            "So: how do you put a number on an economy? <bookmark mark='a'/> Add up what each producer adds, and "
            "check it against what is spent and what is earned, since the three must agree. Divide by a price "
            "index whose basket you choose with care. Compare countries at the same prices. And remember, as "
            "Kuznets said in 1934, what the number leaves out."
        ) as vo:
            self.play(FadeIn(q, shift=UP * 0.2))
            vo.wait_until("a")
            self.play(FadeIn(a, shift=UP * 0.1), run_time=2)
            self.play(Create(logo.arc), FadeIn(logo.ticks), FadeIn(logo.hub), Create(logo.needle))
        self.clear_scene()

    def recap(self):
        k, acc, ix, h, c, w, u, r = (load(x) for x in ("kuznets", "accounts", "indices", "hedonic", "cpi", "world",
                                                       "unemployment", "revisions"))
        items = [
            (rf"1932: \ income produced fell {100 * k['fall_produced']:.0f}\%; \ interest held, \ wages fell", KUZ),
            (r"output, spending and income: \ the Island's \$740 three ways, \ and they must agree", E.ACCENT),
            (rf"the US, 2025: \ GDP {tn(acc['us']['GDP'])}; \ the discrepancy $-${abs(acc['us']['discrepancy']):.0f} "
             r"billion",
             E.FIRMS),
            (r"outside the boundary: \ the Island's unpaid work, \ 31\% of its GDP", UNPAID),
            (rf"Bo's basket: \ Laspeyres +50\%, \ Paasche +33\%, \ the truth +{100 * (ix['true'] - 1):.1f}\%", FISHER),
            (rf"a longer boat is not inflation: \ +{100 * h['naive']:.0f}\% on average, \ "
             rf"+{100 * h['pure']:.1f}\% for the same boat", E.FISH),
            (rf"the CPI: \ about 1 point a year too high in 1996; \ the chained index "
             rf"{100 * c['gap_chained']:.2f} lower a year since", PAAS),
            (rf"at purchasing power, \ China's economy is {w['CHN']['gdp_ppp'] / 1e12:.0f} trillion, \ not "
             rf"{w['CHN']['gdp_usd'] / 1e12:.0f}", E.WORLD),
            (rf"unemployment is a survey: \ U-3 {u['us']['U-3']:.1f}\%, \ U-6 {u['us']['U-6']:.1f}\%, \ and one "
             r"missing month", E.HOUSEHOLDS),
            (rf"revisions: \ 2008's last quarter, \ $-3.8\%$ at first, \ $-8.5\%$ today", E.MISS),
        ]
        rows = VGroup(*[label(rf"{i + 1}.\ \ {txt}", font_size=30, color=col) for i, (txt, col) in enumerate(items)])
        rows.arrange(DOWN, aligned_edge=LEFT, buff=0.26)
        head = label(r"Part 3, \ in ten lines", font_size=42).to_edge(UP, buff=0.3)
        if rows.width > 13.2:
            rows.width = 13.2
        room = head.get_bottom()[1] - 0.35 + 3.75
        if rows.height > room:
            rows.scale_to_fit_height(room)
        rows.next_to(head, DOWN, buff=0.35)
        with self.voiceover(
            "Part three in ten lines. <bookmark mark='a'/> In the Depression, America's income fell by half, and "
            "Kuznets's tables showed creditors still paid while wages collapsed. GDP can be added up three ways, "
            "by output, spending and income, and the three must agree. America's came to nearly thirty-one "
            "trillion dollars in 2025, with a discrepancy of forty-six billion between the ways. Outside the "
            "boundary lies work nobody pays for, almost a third of the Island's output. Whose basket you price "
            "decides how much prices rose: for Bo, Laspeyres said fifty percent and Paasche thirty-three, and the "
            "truth was forty-one. A longer boat is not inflation. The consumer price index ran about a point a "
            "year too high in 1996, and still runs high. At purchasing power, China's economy is twice as large as "
            "at market rates. Unemployment is a survey, with six answers and one missing month. And the first "
            "numbers are revised: the worst quarter of 2008 turned out more than twice as bad as first reported."
        ) as vo:
            self.play(FadeIn(head))
            vo.wait_until("a")
            self.play(LaggedStart(*[FadeIn(r, shift=RIGHT * 0.15) for r in rows], lag_ratio=0.8), run_time=34.0)
        self.clear_scene()

    def problems(self):
        ps = problem_set(PROBLEMS, font_size=20, width=13.0)
        with self.voiceover(
            "The problems. A two-firm island's accounts, three ways; the saving identity, and a council that buys "
            "what used to be exported; Bo's basket when fish triples; chain drift over one storm; the boatyard's regression; the "
            "discouraged islanders who start looking again; a two-industry Leontief inverse; and a research "
            "problem, marked with a star, on catching inflated growth from space. Full solutions are in the part's "
            "notes."
        ):
            self.play(FadeIn(ps.head))
            self.play(LaggedStart(*[FadeIn(r, shift=UP * 0.1) for r in ps.rows], lag_ratio=0.4), run_time=6)
        self.wait(4)
        self.clear_scene()

    def references(self):
        rc = reference_card(
            [r"Diane Coyle, \emph{GDP: A Brief but Affectionate History} (2014)",
             r"Fran\c{c}ois Lequiller and Derek Blades, \emph{Understanding National Accounts} (OECD, 2nd ed., 2014)",
             r"N. Gregory Mankiw, \emph{Macroeconomics}, ch.\ 2, \ ``The Data of Macroeconomics''",
             r"Wassily Leontief, \emph{Input-Output Economics} (2nd ed., 1986)"],
            [r"Kuznets et al., \emph{National Income, 1929--32} (1934); \ Petty, \emph{Verbum Sapienti} (1665)",
             r"Boskin et al.\ (1996); \ Lebow and Rudd (2003), \emph{JEL} 41; \ Moulton (2018), Brookings",
             r"Deaton and Heston (2010), \emph{AEJ: Macro} 2; \ Jones and Klenow (2016), \emph{AER} 106",
             r"Nordhaus and Tobin (1972); \ Piketty, Saez and Zucman (2018), \emph{QJE} 133",
             r"Corrado, Hulten and Sichel (2009); \ Henderson, Storeygard and Weil (2012), \emph{AER} 102; \ "
             r"Martinez (2022), \emph{JPE} 130"])
        with self.voiceover(
            "The reading for this part: Diane Coyle's short history of GDP, Lequiller and Blades on how the "
            "accounts are actually built, the data chapter of any intermediate macroeconomics textbook, and "
            "Leontief's own essays. Then the papers: Kuznets's report, the price-index audits, Deaton and Heston "
            "on purchasing power, Jones and Klenow on welfare, and the newer work on what the accounts miss."
        ):
            self.play(FadeIn(rc))
        self.wait(1.5)
        self.clear_scene()

    def next_part(self):
        hc = history_card(1927, r"Elmer Working, ``What Do Statistical `Demand Curves' Show?''",
                          r"prices plotted against quantities: \ a cloud that is neither demand nor supply", color=E.ACCENT,
                          width=9.0, font_size=26).move_to(UP * 0.6)
        nxt = VGroup(label(r"Next: \ Part 4", font_size=30, color=GREY_B),
                     label(r"The Evidence", font_size=56, color=WHITE),
                     label(r"when can data answer an economic question?", font_size=26, color=GREY_A)).arrange(
            DOWN, buff=0.15).next_to(hc, DOWN, buff=0.6)
        with self.voiceover(
            "Now we have numbers. The next part asks what they can tell us. <bookmark mark='a'/> In 1927 an "
            "agricultural economist, Elmer Working, plotted the prices and quantities of a market year after year, "
            "and asked a simple question: is the cloud of points the demand curve, or the supply curve? The answer "
            "is neither. <bookmark mark='b'/> Part four: the evidence. When data can answer an economic question, "
            "and how economists learned to find the experiments hidden in the world."
        ) as vo:
            self.play(FadeIn(hc, shift=UP * 0.2))
            vo.wait_until("b")
            self.play(FadeIn(nxt, shift=UP * 0.1))
        self.wait(3.0)
        self.play(*[FadeOut(m) for m in self.mobjects], run_time=1.5)

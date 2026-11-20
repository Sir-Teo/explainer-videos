from __future__ import annotations

from videos.economics.econ25.common import *  # noqa: F403

PROBLEMS = [
    r"Barter: \ with $n$ goods, \ show that a random meeting allows a trade with probability $1/(n-1)^2$ under barter "
    r"and $1/(n-1)$ with money; \ count the prices needed each way.",
    r"Kiyotaki--Wright: \ under the fundamental strategies, \ show that Bo holds salt exactly half the time in a "
    r"steady state.",
    r"The quantity equation: \ from $MV = PY$, \ derive $\pi = \mu + \Delta\ln V - g$; \ with M2 growing 6\%, "
    r"\ velocity steady and output 2.5\%, \ what inflation?",
    r"Cagan: \ show that steady-state seigniorage $\mu e^{-\alpha\mu}$ is largest at $\mu = 1/\alpha$, \ and find "
    r"its maximum.",
    r"Two steady states: \ show that a deficit $d$ financed by $\pi e^{-\alpha\pi} = d$ has two solutions if $d < "
    r"e^{-1}/\alpha$ and none if $d > e^{-1}/\alpha$.",
    r"Baumol--Tobin: \ derive $n^* = \sqrt{iY/2b}$ and $M^* = \sqrt{bY/2i}$, \ and the income and interest "
    r"elasticities.",
    r"T-accounts: \ Ana borrows 100 and withdraws 20 in cash. \ Write the three balance sheets. \ Does broad money "
    r"change? \ Base money?",
    r"$\bigstar$ \ Cash in advance: \ with utility $\ln c - a n$, \ $c = n$ and $Pc \le M$, \ derive $c = 1/(a(1 + "
    r"i))$ and show the welfare cost is zero only at $i = 0$.",
]


class Outro(VoiceoverScene):
    def construct(self):
        self.answer()
        self.recap()
        self.problems()
        self.references()
        self.next_part()

    def answer(self):
        q = wrapped_label(ASK, 12.0, 42, E.ACCENT).move_to(UP * 2.2)
        a = wrapped_label(r"Money is whatever people accept in order to pass it on: \ a social convention, \ and a "
                          r"kind of memory, \ that saves the double coincidence of barter. \ Today it is mostly bank "
                          r"deposits, \ created when banks lend. \ Too much of it raises prices one for one in the "
                          r"long run; \ printed to pay a government's bills, \ it becomes a tax that people flee, \ "
                          r"and only a believable change of fiscal regime, \ or another money, \ ends the flight.",
                          11.6, 27, WHITE)
        a.next_to(q, DOWN, buff=0.55)
        f = load("film")
        mini = plane([1959, 2027], [0, np.log10(120)], x_length=4.2, y_length=1.3)
        logo = VGroup(path(mini, f["t"], np.log10(f["base"]), CB, width=3, smooth=False),
                      path(mini, f["t"], np.log10(f["m2"]), BANK, width=3, smooth=False),
                      path(mini, f["t"], np.log10(f["cpi"]), PRICE, width=3, smooth=False))
        logo.next_to(a, DOWN, buff=0.4)
        with self.voiceover(
            "So: what is money, and what happens when there is too much of it? <bookmark mark='a'/> Money is "
            "whatever people accept in order to pass it on: a social convention, and a kind of memory, that saves "
            "them the double coincidence of barter. Today it is mostly bank deposits, created when banks lend. Too "
            "much of it raises prices one for one in the long run. Printed to pay a government's bills, it becomes "
            "a tax that people flee, and only a believable change of fiscal regime, or another money, ends the "
            "flight."
        ) as vo:
            self.play(FadeIn(q, shift=UP * 0.2))
            vo.wait_until("a")
            self.play(FadeIn(a, shift=UP * 0.1), run_time=2)
            self.play(Create(logo), run_time=1.5)
        self.clear_scene()

    def recap(self):
        k, w, L, d, b, ba, fi, c, bt = (load(x) for x in ("kw", "world", "laffer", "deficit", "baumol", "base",
                                                          "fisher", "cia", "barter"))
        k10 = bt["n"].index(10)
        items = [
            (r"Yap: \ a stone on the seabed, \ still money", MONEY),
            (rf"barter: \ 1 chance in {1 / bt['barter'][k10]:.0f} with ten goods; \ money as memory", COCO),
            (r"Play it: \ salt became the Island's money", SALT),
            (r"Kiyotaki and Wright: \ smoked fish became money too; \ fiat money rests on expectations", FISH),
            (r"from Lydia's coins to 15 August 1971", MONEY),
            (rf"the quantity theory: \ slope {w['slope']:.2f} across {w['n']} countries; \ year by year "
             rf"{w['annual_corr']:.2f}", MONEY),
            (r"hyperinflation: \ the inflation tax peaks at $1/\alpha$; \ Cagan's ceiling, \ wrong", PRICE),
            (r"four ends, \ Zimbabwe and Venezuela: \ a new fiscal regime or a new money", CB),
            (rf"money demand: \ the square-root rule; \ M1's semi-elasticity {b['semi_pre']:.3f}, \ then "
             rf"{b['semi_post']:.3f}", MONEY),
            (rf"banks create deposits by lending; \ M2 fell from {ba['mult_2007']:.1f} to {ba['mult_2014']:.1f} "
             r"times the base", BANK),
            (r"Fisher: \ $i \approx r + \pi^e$; \ neutrality and its limits", RATE),
            (rf"the Friedman rule; \ 10\% inflation costs {100 * c['at']['10']:.1f}\%; \ a dial; \ payments; \ "
             r"stablecoins", PRICE),
        ]
        rows = VGroup(*[label(rf"{n + 1}.\ \ {txt}", font_size=28, color=col) for n, (txt, col) in enumerate(items)])
        rows.arrange(DOWN, aligned_edge=LEFT, buff=0.2)
        head = label(r"Part 25, \ in twelve lines", font_size=42).to_edge(UP, buff=0.3)
        if rows.width > 13.2:
            rows.width = 13.2
        room = head.get_bottom()[1] - 0.35 + 3.75
        if rows.height > room:
            rows.scale_to_fit_height(room)
        rows.next_to(head, DOWN, buff=0.35)
        del k, L, d, fi
        with self.voiceover(
            "Part twenty-five in twelve lines. <bookmark mark='a'/> On Yap, a stone on the seabed was still money. "
            "Barter needs a double coincidence, and money works like a public memory. On the Island, salt became "
            "money without anyone deciding it, and smoked fish became money too; paper money rests on expectations "
            "alone. Money went from Lydia's coins to Nixon's closed window. Across countries, inflation tracks "
            "money growth almost one for one, though not year by year. The inflation tax has a Laffer curve, and "
            "governments in hyperinflation printed beyond its peak. Hyperinflations end with a believable fiscal "
            "regime or a different money. People hold less money when interest rates rise, though the measured "
            "relationship broke in the 1980s. Banks create deposits by lending, and the money multiplier collapsed "
            "after 2008. Interest rates carry expected inflation. And the Friedman rule, the cost of inflation, a "
            "dial, the payment systems, and the new private moneys."
        ) as vo:
            self.play(FadeIn(head))
            vo.wait_until("a")
            self.play(LaggedStart(*[FadeIn(r_, shift=RIGHT * 0.15) for r_ in rows], lag_ratio=0.8), run_time=46.0)
        self.clear_scene()

    def problems(self):
        ps = problem_set(PROBLEMS, font_size=20, width=13.0)
        with self.voiceover(
            "The problems. Barter's odds; why Bo holds salt half the time; the quantity equation in growth rates; "
            "Cagan's Laffer curve and its two steady states; Baumol and Tobin's square-root rule; balance sheets "
            "when a loan is drawn in cash; and a starred problem on the cash-in-advance economy. Full solutions are "
            "in the part's notes."
        ):
            self.play(FadeIn(ps.head), FadeIn(ps.rows[0], shift=UP * 0.1), run_time=0.8)
            self.play(LaggedStart(*[FadeIn(r) for r in ps.rows[1:]], lag_ratio=0.4), run_time=6)
        self.wait(4)
        self.clear_scene()

    def references(self):
        rc = reference_card(
            [r"Carl Walsh, \emph{Monetary Theory and Policy} (4th ed., 2017), \ chs.\ 1--4",
             r"Milton Friedman and Anna Schwartz, \emph{A Monetary History of the United States, 1867--1960} (1963)",
             r"Thomas Sargent, \emph{Rational Expectations and Inflation} (3rd ed., 2013)",
             r"Ricardo Lagos, Guillaume Rocheteau and Randall Wright, \ JEL 55(2) (2017): \ liquidity, \ a survey"],
            [r"Jevons (1875); \ Furness (1910); \ Friedman (1991); \ Kocherlakota (1998); \ Kiyotaki and Wright (1989)",
             r"Duffy and Ochs (1999); \ Fisher (1896, 1911); \ McCandless and Weber (1995); \ Cagan (1956)",
             r"Sargent (1982); \ Hanke and Krus (2012); \ Baumol (1952); \ Tobin (1956); \ Lucas and Nicolini (2015)",
             r"McLeay, Radia and Thomas (2014); \ Sidrauski (1967); \ Friedman (1969); \ Lucas (2000)",
             r"Ball (2001); \ Ireland (2009); \ Gorton and Zhang (2023)"])
        with self.voiceover(
            "The reading: Carl Walsh's Monetary Theory and Policy, whose first chapters this part follows; Friedman "
            "and Schwartz's Monetary History; Sargent's essays on inflation, including the four big inflations; and "
            "the survey of the new monetarist search models by Lagos, Rocheteau and Wright. Then the papers, from "
            "Jevons to the stablecoins."
        ):
            self.play(FadeIn(rc))
        self.wait(1.5)
        self.clear_scene()

    def next_part(self):
        hc = history_card(2023, r"Silicon Valley Bank", r"on Thursday 9 March its customers ask to withdraw 42 billion "
                          r"dollars, \ mostly from their phones; \ by the next morning the bank is closed",
                          color=E.ACCENT, width=10.4, font_size=24)
        nxt = VGroup(label(r"Next: \ Part 26 \ $\cdot$ \ Act VI, \ Money and the Cycle", font_size=30, color=GREY_B),
                     label(r"Banks and Runs", font_size=46),
                     label(r"why are banks fragile, \ and can they be made safe?", font_size=26,
                           color=E.ACCENT)).arrange(DOWN, buff=0.22)
        head = label(r"this part: \ what money is; \ next: \ the institutions that create most of it", font_size=26,
                     color=GREY_A).to_edge(UP, buff=0.5)
        VGroup(hc, nxt).arrange(DOWN, buff=0.6).next_to(head, DOWN, buff=0.5)
        with self.voiceover(
            "This part asked what money is. The next turns to the institutions that create most of it. "
            "<bookmark mark='a'/> On Thursday the ninth of March 2023, the customers of Silicon Valley Bank asked "
            "to withdraw forty-two billion dollars, mostly from their phones. By the next morning the bank had been "
            "closed. <bookmark mark='b'/> Part twenty-six: banks and runs. Why are banks fragile, and can they be "
            "made safe?"
        ) as vo:
            self.play(FadeIn(head))
            vo.wait_until("a")
            self.play(FadeIn(hc, shift=UP * 0.2))
            vo.wait_until("b")
            self.play(FadeIn(nxt, shift=UP * 0.2))
        self.wait(9.5)
        self.clear_scene()

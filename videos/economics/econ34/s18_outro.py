from __future__ import annotations

from videos.economics.econ34.common import *  # noqa: F403

PROBLEMS = [
    r"Accounts: \ national saving is 18\% of GDP and investment 22\%. \ Find the current account; \ then cut the "
    r"budget deficit by 2 points with private saving fixed.",
    r"Big Mac: \ it costs \$6.22 in America and 6.50 francs in Switzerland, \ at 0.80 francs per dollar. \ Find the "
    r"implied PPP rate and the franc's valuation.",
    r"Half-life: \ show that an AR(1) with coefficient $\rho$ has half-life $\ln 0.5/\ln\rho$; \ evaluate at "
    r"$\rho = 0.87$ a year and $0.98$ a month.",
    r"Parity: \ spot \$1.25 per pound, \ dollar rate 4\%, \ sterling rate 5\%. \ Find the one-year forward rate; \ "
    r"and the carry return if the pound then rises 3\%.",
    r"Mundell--Fleming: \ with $y = a y + g - b r + c e$, \ $m = k y - h r$ and $r = r^*$, \ derive the effects of "
    r"$g$ and $m$ under each regime.",
    r"Overshooting: \ derive the impact factor $1 + 1/(\lambda\theta)$; \ evaluate at $\lambda = 4$ with $\theta = "
    r"0.5$ and $\theta = 2$.",
    r"Krugman: \ reserves 40, \ credit 60 growing 2 a year, \ peg 100, \ $\alpha = 5$. \ When do reserves run out "
    r"unaided, \ and when does the attack come?",
    r"$\bigstar$ \ Obstfeld: \ with loss $(u + \gamma x)^2$ and cost $C$, \ find the band of $u$ with two "
    r"equilibria; \ show that it widens with $\gamma\delta$.",
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
        a = wrapped_label(r"Asset markets set it, \ through interest rates, \ expectations and the demand for safe "
                          r"assets, \ far more than trade does: \ parity returns only slowly, \ and no model beats "
                          r"the random walk month to month. \ And a country cannot have at once a fixed exchange "
                          r"rate, \ free movement of capital and its own monetary policy: \ it chooses two, \ and "
                          r"markets test the choice.", 11.6, 25, WHITE)
        a.next_to(q, DOWN, buff=0.5)
        F = load("film")
        mini = plane([1971, 2027], [1.0, 2.7], x_length=4.2, y_length=1.3)
        logo = path(mini, F["t"], F["v"], GBP, 2.4, smooth=False).next_to(a, DOWN, buff=0.35)
        with self.voiceover(
            "So: what sets the price of one money in terms of another, and what can a country not have at once? "
            "<bookmark mark='a'/> Asset markets set it, through interest rates, expectations and the world's demand "
            "for safe assets, far more than trade does. Prices pull it back toward parity, but only slowly, and "
            "month to month no model beats the random walk. And a country cannot have at once a fixed exchange "
            "rate, capital that moves freely and a monetary policy of its own. It chooses two, and markets test "
            "the choice."
        ) as vo:
            self.play(FadeIn(q, shift=UP * 0.2))
            vo.wait_until("a")
            self.play(FadeIn(a, shift=UP * 0.1), run_time=2)
            self.play(Create(logo), run_time=1.5)
        self.clear_scene()

    def recap(self):
        S, B, P, Q, U, M, MF_, D, C, EU, I, Dl = (load(x) for x in ("story", "bop", "playit", "ppp", "uip", "meese",
                                                                   "mf", "dornbusch", "crises", "euro",
                                                                   "imbalances", "dollar"))
        neg = sum(1 for v in U["fama"].values() if v["beta"] < 0)
        ratios = [M[h]["ratio"]["interest parity"] for h in ("h1", "h3", "h12")]
        gr = max(EU["GR"]["v"])
        K = C["krugman"]
        sw, ind = Q["pick"]["Switzerland"], Q["pick"]["India"]
        items = [
            (rf"1992: \ the pound $-{S['fall']:.0f}\%$ against the mark; \ Britain's rate {S['i_uk_aug92']:.1f}\% "
             rf"$\to$ {S['i_uk_feb93']:.1f}\%", GBP),
            (rf"accounts: \ US current account {B['ca_min']:.1f}\% (2006); \ net position "
             rf"{B['niip_first']:.0f}\% $\to$ {B['niip_last']:.0f}\% of GDP", USD),
            (rf"Play it: \ between {P['safe_below']:.1f} and {P['doomed_above']:.1f}, \ the peg falls if traders "
             r"expect it to", CRISIS),
            (rf"PPP: \ a Big Mac \${sw['price']:.2f} in Switzerland, \ \${ind['price']:.2f} in India; \ half-life "
             rf"{Q['full']['halflife']:.1f} years", PRICE),
            (rf"parity: \ Fama's slope negative for {neg} of {len(U['fama'])} currencies; \ carry "
             rf"{100 * U['carry']['mean']:.1f}\% a year", RATE),
            (rf"the random walk: \ RMSE ratios {min(ratios):.2f} to {max(ratios):.2f} at 1, \ 3 and 12 months", GREY_A),
            (rf"the trilemma: \ fiscal policy moves output {MF_['fixed']['fiscal']['y']:.0f} under a peg, \ "
             rf"{MF_['floating']['fiscal']['y']:.0f} under a float", DEM),
            (rf"overshooting: \ money $+10\%$, \ the currency $-{100 * D['jump']:.0f}\%$ at once", GBP),
            (rf"crises: \ the attack in year {K['T_attack']:.0f}, \ {K['T_exhaust'] - K['T_attack']:.0f} years before "
             r"reserves would have run out", CRISIS),
            (rf"the euro: \ one interest rate, \ then Greek ten-year yields {gr:.0f}\%", DEM),
            (rf"imbalances: \ China {I['chn2007']:+.1f}\% (2007), \ America {I['usa2006']:+.1f}\% (2006)", CNY),
            (rf"the dollar: \ pass-through {abs(Dl['pt']['impact']):.2f} at once, \ "
             rf"{abs(Dl['pt']['long_run']):.2f} after a year", USD),
        ]
        rows = VGroup(*[label(rf"{n + 1}.\ \ {txt}", font_size=28, color=col) for n, (txt, col) in enumerate(items)])
        rows.arrange(DOWN, aligned_edge=LEFT, buff=0.2)
        head = label(r"Part 34, \ in twelve lines", font_size=42).to_edge(UP, buff=0.3)
        if rows.width > 13.2:
            rows.width = 13.2
        room = head.get_bottom()[1] - 0.35 + 3.75
        if rows.height > room:
            rows.scale_to_fit_height(room)
        rows.next_to(head, DOWN, buff=0.35)
        with self.voiceover(
            "Part thirty-four in twelve lines. <bookmark mark='a'/> In 1992 Britain chose its own recovery over the "
            "mark, and rates fell by four points within months. The balance of payments says a deficit is investment "
            "above saving, and America's debts to the world have grown for forty years. A peg can fall because "
            "traders expect it to. Prices differ widely across countries and return to parity slowly. Currencies "
            "with high interest rates tend to rise, not fall, which pays the carry trade, until it crashes. No model "
            "beats the random walk. Under a peg fiscal policy works and money does not; under a float, the reverse. "
            "Sticky prices make exchange rates overshoot. Crises come before the reserves run out, because "
            "speculators see the end coming. The euro removed exchange rates and found what replaced them. The "
            "world's imbalances are a story of saving, not only of spending. And the dollar, in which the world "
            "prices its trade, makes exchange rates matter less to America than to everyone else."
        ) as vo:
            self.play(FadeIn(head))
            vo.wait_until("a")
            self.play(LaggedStart(*[FadeIn(r_, shift=RIGHT * 0.15) for r_ in rows], lag_ratio=0.8), run_time=40.0)
        self.clear_scene()

    def problems(self):
        ps = problem_set(PROBLEMS, font_size=19, width=13.0)
        with self.voiceover(
            "The problems. The current account as saving minus investment; the Big Mac's arithmetic; the half-life "
            "of a deviation; covered parity and the carry trade; the Mundell-Fleming algebra; Dornbusch's overshoot; "
            "the timing of a speculative attack; and a starred problem on self-fulfilling crises. Full solutions "
            "are in the part's notes."
        ):
            self.play(FadeIn(ps.head), FadeIn(ps.rows[0], shift=UP * 0.1), run_time=0.8)
            self.play(LaggedStart(*[FadeIn(r) for r in ps.rows[1:]], lag_ratio=0.4), run_time=6)
        self.wait(4)
        self.clear_scene()

    def references(self):
        rc = reference_card(
            [r"Paul Krugman, \ Maurice Obstfeld and Marc Melitz, \emph{International Economics} (12th ed., 2022), "
             r"Part 3",
             r"Maurice Obstfeld and Kenneth Rogoff, \emph{Foundations of International Macroeconomics} (1996)",
             r"Barry Eichengreen, \emph{Globalizing Capital} (3rd ed., 2019)",
             r"Martin Uribe and Stephanie Schmitt-Groh\'e, \emph{Open Economy Macroeconomics} (2017)"],
            [r"Mundell (1961, 1963); \ Fleming (1962); \ Dornbusch (1976); \ Balassa (1964); \ Samuelson (1964)",
             r"Krugman (1979); \ Obstfeld (1996); \ Calvo (1998); \ Meese and Rogoff (1983); \ Fama (1984)",
             r"Rogoff (1996); \ Lustig and Verdelhan (2007); \ Gourinchas and Rey (2007); \ Rey (2013)",
             r"Gopinath, \ Itskhoki and Rigobon (2010); \ Gopinath et al.\ (2020); \ Gabaix and Maggiori (2015)",
             r"Itskhoki and Mukhin (2021); \ Caballero, \ Farhi and Gourinchas (2017); \ Rossi (2013)"])
        with self.voiceover(
            "The reading: Krugman, Obstfeld and Melitz for the undergraduate course; Obstfeld and Rogoff's "
            "Foundations for the graduate one; Barry Eichengreen's history of the international monetary system; "
            "and Uribe and Schmitt-Grohe on open-economy business cycles. Then the papers, from Mundell to "
            "Itskhoki and Mukhin."
        ):
            self.play(FadeIn(rc))
        self.wait(1.5)
        self.clear_scene()

    def next_part(self):
        hc = history_card(1817, r"David Ricardo", r"England makes cloth with 100 men and wine with 120; \ Portugal "
                          r"needs 90 and 80, \ fewer for both. \ Yet both gain if England makes the cloth and "
                          r"Portugal the wine", color=E.ACCENT, width=10.4, font_size=24)
        nxt = VGroup(label(r"Next: \ Part 35 \ $\cdot$ \ Act VII, \ The World Economy", font_size=30, color=GREY_B),
                     label(r"Trade I: \ Comparative Advantage", font_size=46),
                     label(r"why do countries trade, \ and who wins and loses when they do?", font_size=26,
                           color=E.ACCENT)).arrange(DOWN, buff=0.22)
        head = label(r"from the price of money \ to the trade in goods", font_size=26,
                     color=GREY_A).to_edge(UP, buff=0.5)
        VGroup(hc, nxt).arrange(DOWN, buff=0.6).next_to(head, DOWN, buff=0.5)
        with self.voiceover(
            "This part was about money crossing borders. The next is about goods. <bookmark mark='a'/> In 1817 David "
            "Ricardo wrote down four numbers. England needs a hundred workers for a year to make a quantity of cloth "
            "and a hundred and twenty for a quantity of wine; Portugal needs ninety and eighty, fewer for both. Yet "
            "both countries gain if England makes the cloth and Portugal the wine. Paul Samuelson called it the one "
            "proposition in the social sciences that is both true and not trivial. <bookmark mark='b'/> Part "
            "thirty-five: comparative advantage. Why do countries trade, and who wins and loses when they do?"
        ) as vo:
            self.play(FadeIn(head))
            vo.wait_until("a")
            self.play(FadeIn(hc, shift=UP * 0.2))
            vo.wait_until("b")
            self.play(FadeIn(nxt, shift=UP * 0.2))
        self.wait(9.5)
        self.clear_scene()

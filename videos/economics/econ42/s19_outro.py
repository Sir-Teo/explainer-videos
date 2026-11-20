from __future__ import annotations

from videos.economics.econ42.common import *  # noqa: F403

PROBLEMS = [
    r"Pooling: \ each of 10,000 members claims with probability 5\%, \ independently. \ What is the standard deviation "
    r"of the claim per member, \ relative to its mean? \ Now let the chance be 3\% or 9\% (a recession one year in "
    r"seven): \ what is the floor?",
    r"Baily-Chetty: \ risk aversion 2, \ consumption falls 10\% on losing a job, \ $\varepsilon$ = 0.5, \ $e$ = 0.8. "
    r"\ Should benefits rise or fall? \ Use the exact left side and the approximation.",
    r"Liquidity: \ if 60\% of the response of durations to benefits is liquidity, \ what is the gain side of the "
    r"formula? \ What if it were 20\%?",
    r"RAND: \ spending is \$1,000 with 25\% coinsurance and \$700 with 95\%. \ Find the arc elasticity.",
    r"Oregon: \ the lottery raises coverage by 25 points \ and lowers the share screening positive for depression by "
    r"2.3 points. \ What is the effect of coverage? \ If the reduced form's standard error is 0.9 points, \ what is "
    r"the IV estimate's?",
    r"Pensions: \ a 12.4\% payroll tax, \ 2.3 workers per beneficiary. \ What benefit can it pay, \ as a share of the "
    r"wage? \ What tax keeps today's 33.5\%?",
    r"The EITC: \ with the 2025 schedule for three children, \ find the credit and the marginal rate at earnings of "
    r"\$10,000 and \$40,000.",
    r"$\bigstar$ \ Derive Baily's formula: \ from $W = e\,u(c_e) + (1-e)\,u(c_u) - \psi(e)$ and $(1-e)\,b = e\,\tau$, "
    r"\ show that $dW/db = 0$ gives $(u'(c_u) - u'(c_e))/u'(c_e) = \varepsilon_{1-e,b}/e$.",
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
        a = wrapped_label(r"What private markets cannot: \ risks that strike everyone at once, \ that adverse "
                          r"selection unravels, \ or that are settled before anyone can buy cover. \ How generously: "
                          r"\ until the last dollar is worth a dollar, \ which turns on two measurable numbers, \ how "
                          r"far consumption falls and how much behaviour changes.", 11.6, 25, WHITE)
        a.next_to(q, DOWN, buff=0.5)
        F = load("film")
        mini = plane([1967, 2027], [0, 1], x_length=4.2, y_length=1.3)
        v = np.log(np.array(F["v"]))
        v = (v - v.min()) / (v.max() - v.min())
        logo = path(mini, F["t"], v, UNEMP, 2.4, smooth=False).next_to(a, DOWN, buff=0.35)
        with self.voiceover(
            "So: what should the state insure, and how generously? <bookmark mark='a'/> What private markets cannot: "
            "risks that strike everyone at once, risks that adverse selection unravels, and risks that are settled "
            "before anyone can buy cover. How generously: until the last dollar is worth a dollar, which turns on "
            "two numbers that can be measured, how far consumption falls when the risk strikes, and how much "
            "behaviour changes when it is insured."
        ) as vo:
            self.play(FadeIn(q, shift=UP * 0.2))
            vo.wait_until("a")
            self.play(FadeIn(a, shift=UP * 0.1), run_time=2)
            self.play(Create(logo), run_time=1.5)
        self.clear_scene()

    def recap(self):
        P, B, W, H, L, Pe, D, M = (load(x) for x in ("pooling", "baily", "weekly", "health", "lottery",
                                                      "pensions", "defaults", "mvpf"))
        ms = tables.MADRIAN_SHEA_2001.data["participation"]
        before = ms["hired the year before, same tenure"]
        after = ms["auto-enrolled (3-15 months' tenure)"]
        items = [
            (r"the lottery: \ 90,000 names, \ 30,000 drawn, \ 10,000 places: \ an experiment by chance", LOTTO),
            (rf"pooling: \ recessions keep the spread above {100 * P['floor']:.0f}\%; \ the state can borrow", RISK),
            (rf"the game: \ the Island's best benefit, \ {100 * B['bstar']:.0f}\% of the wage", GAIN),
            (rf"the formula: \ gain = cost = {B['at']['gain']:.2f} at the optimum", THEORY),
            (rf"durations: \ elasticity {W['level']:.2f} on the Island, \ 0.4--0.8 measured", COST),
            (r"consumption: \ $-$7\% on losing a job, \ $-$12\% when benefits run out", SMOOTH),
            (rf"liquidity: \ {100 * B['split']['share']:.0f}\% on the Island, \ 60\% measured: \ benefits may be "
             r"too low", LIQ),
            (rf"health: \ RAND's 95\% plan spent 30\% less; \ the best plan pays {100 * H['cstar']:.0f}\%", HEALTH),
            (rf"Oregon: \ more care, \ less strain and depression; \ blood pressure: \ power "
             rf"{100 * L['summary']['systolic']['power']:.0f}\%", LOTTO),
            (rf"pensions and defaults: \ 5.1 $\to$ 2.3 workers; \ "
             rf"{100 * before:.0f}\% $\to$ {100 * after:.0f}\% by changing a form", PENSION),
            (r"disability, \ the EITC, \ basic income: \ examiners, \ tags and trials", UNEMP),
            (rf"one yardstick: \ MVPF; \ the best benefit scores 1, \ the EITC {M['points']['eitc']['mvpf']:.2f}",
             E.ACCENT),
        ]
        rows = VGroup(*[label(rf"{n + 1}.\ \ {txt}", font_size=28, color=col) for n, (txt, col) in enumerate(items)])
        rows.arrange(DOWN, aligned_edge=LEFT, buff=0.2)
        head = label(r"Part 42, \ in twelve lines", font_size=42).to_edge(UP, buff=0.3)
        if rows.width > 13.2:
            rows.width = 13.2
        room = head.get_bottom()[1] - 0.35 + 3.75
        if rows.height > room:
            rows.scale_to_fit_height(room)
        rows.next_to(head, DOWN, buff=0.35)
        with self.voiceover(
            "Part forty-two in twelve lines. <bookmark mark='a'/> Oregon's lottery made an experiment out of a "
            "shortage. Recessions put a floor under the risk any pool can remove, which is why the state, which can "
            "borrow, insures unemployment. The best benefit balances smoother consumption against longer "
            "unemployment, and Baily and Chetty's formula says where, in two measurable numbers. Benefits lengthen "
            "unemployment by four to eight tenths of a percent for each percent, and consumption falls about seven "
            "percent on losing a job and more when benefits run out. If much of the response is liquidity, benefits "
            "should be higher than the consumption drop alone suggests. Health insurance raises spending, by about "
            "thirty percent in RAND's experiment, and the best plan keeps a price on care while capping risk. Oregon "
            "found more care and less strain and depression, and could not detect small effects on blood pressure. "
            "Pay-as-you-go pensions face fewer workers per retiree, and defaults move saving more than subsidies. "
            "Examiners, tags and trials sharpen disability insurance, help for the working poor and the case for a "
            "basic income. And one yardstick, the value of a public dollar, compares them all."
        ) as vo:
            self.play(FadeIn(head))
            vo.wait_until("a")
            self.play(LaggedStart(*[FadeIn(r_, shift=RIGHT * 0.15) for r_ in rows], lag_ratio=0.8), run_time=44.0)
        self.clear_scene()

    def problems(self):
        ps = problem_set(PROBLEMS, font_size=19, width=13.0)
        with self.voiceover(
            "The problems. Pooling; Baily and Chetty's formula; liquidity; the RAND elasticity; the Oregon "
            "instrument; pension arithmetic; the earned income tax credit; and a starred derivation of the formula. "
            "Full solutions are in the part's notes."
        ):
            self.play(FadeIn(ps.head), FadeIn(ps.rows[0], shift=UP * 0.1), run_time=0.8)
            self.play(LaggedStart(*[FadeIn(r) for r in ps.rows[1:]], lag_ratio=0.4), run_time=6)
        self.wait(4)
        self.clear_scene()

    def references(self):
        rc = reference_card(
            [r"Jonathan Gruber, \emph{Public Finance and Public Policy}, \ chapters 12--17",
             r"Nicholas Barr, \emph{The Economics of the Welfare State} (6th edition, 2020)",
             r"Liran Einav and Amy Finkelstein, \emph{Risky Business} (2023)",
             r"Raj Chetty and Amy Finkelstein, \ `Social Insurance: \ Connecting Theory to Data', \ \emph{Handbook "
             r"of Public Economics} 5 (2013)"],
            [r"Arrow (1963); \ Pauly (1968); \ Zeckhauser (1970); \ Akerlof (1978); \ Baily (1978)",
             r"Robins (1985); \ Manning et al.\ (1987); \ Meyer (1990); \ Eissa and Liebman (1996); \ Gruber (1997)",
             r"Madrian and Shea (2001); \ Chetty (2006, \ 2008); \ Card, \ Chetty and Weber (2007)",
             r"Finkelstein et al.\ (2012); \ Schmieder, \ von Wachter and Bender (2012); \ Baicker et al.\ (2013)",
             r"Maestas, \ Mullen and Strand (2013); \ Chetty et al.\ (2014); \ Taubman et al.\ (2014)",
             r"Ganong and Noel (2019); \ Finkelstein, \ Hendren and Luttmer (2019); \ Hendren and Sprung-Keyser "
             r"(2020)"])
        with self.voiceover(
            "The reading: Gruber's textbook chapters on social insurance; Nicholas Barr's The Economics of the "
            "Welfare State; Einav and Finkelstein's Risky Business, on why insurance markets fail; and Chetty and "
            "Finkelstein's survey of social insurance. Then the papers, from Arrow to the value of public funds."
        ):
            self.play(FadeIn(rc))
        self.wait(1.5)
        self.clear_scene()

    def next_part(self):
        hc = history_card(1995, r"Berry, \ Levinsohn and Pakes", r"publish a way to estimate demand for hundreds of "
                          r"differentiated products, \ and with it market power, \ without seeing anyone's costs",
                          color=E.ACCENT, width=10.4, font_size=24)
        nxt = VGroup(label(r"Next: \ Part 43 \ $\cdot$ \ Act IX, \ The Fields", font_size=30, color=GREY_B),
                     label(r"Measuring Market Power", font_size=46),
                     label(r"how do you tell whether a market is competitive \ when you cannot see anyone's costs?",
                           font_size=24, color=E.ACCENT)).arrange(DOWN, buff=0.22)
        head = label(r"from the state's markets \ to the economist's fields", font_size=26, color=GREY_A).to_edge(
            UP, buff=0.5)
        VGroup(hc, nxt).arrange(DOWN, buff=0.6).next_to(head, DOWN, buff=0.5)
        with self.voiceover(
            "This part ends Act eight, on work and the state. The next act turns to the fields of economics, one "
            "by one, starting with industry. <bookmark mark='a'/> In 1995 Steven Berry, James Levinsohn and Ariel "
            "Pakes published a way to estimate the demand for hundreds of different products at once, cars in their "
            "case, and with it how much market power each seller has, without ever seeing a firm's costs. "
            "<bookmark mark='b'/> Part forty-three: measuring market power. How do you tell whether a market is "
            "competitive when you cannot see anyone's costs?"
        ) as vo:
            self.play(FadeIn(head))
            vo.wait_until("a")
            self.play(FadeIn(hc, shift=UP * 0.2))
            vo.wait_until("b")
            self.play(FadeIn(nxt, shift=UP * 0.2))
        self.wait(9.5)

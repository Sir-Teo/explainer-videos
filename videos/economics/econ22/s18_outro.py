from __future__ import annotations

from videos.economics.econ22.common import *  # noqa: F403

PROBLEMS = [
    r"Kuznets and Friedman: \ with $\ln C = \ln 0.9 + p$ and $\ln Y = p + t$, \ $p$ and $t$ independent, \ show "
    r"that the slope of $\ln C$ on $\ln Y$ is $\sigma_p^2 / (\sigma_p^2 + \sigma_t^2)$.",
    r"Permanent income: \ with $\beta(1+r) = 1$ and an infinite horizon, \ show that a windfall $w$ raises "
    r"consumption by $\frac{r}{1+r} w$ a year, \ and a permanent raise of $1$ by $1$.",
    r"Hall: \ derive $\mathbb{E}_t c_{t+1} = c_t$ from the Euler equation with quadratic utility, \ and say why "
    r"income growth at $t-1$ is a bad test variable with quarterly averages.",
    r"Working's effect: \ for a random walk averaged over $m$ points, \ show that successive changes of the "
    r"averages have correlation $(m^2-1)/(2(2m^2+1))$.",
    r"Campbell and Mankiw: \ with $\Delta c = \lambda \Delta y + (1-\lambda)\varepsilon$, \ show that OLS of $\Delta "
    r"c$ on $\Delta y$ is biased when $\operatorname{cov}(\Delta y, \varepsilon) > 0$, \ and that a lagged "
    r"instrument removes the bias.",
    r"Prudence: \ show that with $u'(c) = c^{-\gamma}$, \ a mean-preserving spread in $c_{t+1}$ raises "
    r"$\mathbb{E}\, u'(c_{t+1})$, \ and so raises saving.",
    r"Ricardian equivalence: \ a tax cut $T$ today is repaid as $T(1+r)^n$ in $n$ years; \ show the "
    r"household's lifetime budget is unchanged, \ and name two reasons it may still spend.",
    r"$\bigstar$ \ Diamond: \ with log utility and $f(k) = Ak^\alpha$, \ derive the steady state $k^*$, \ and show "
    r"that a pay-as-you-go pension raises steady-state welfare if and only if $R < 1 + n$.",
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
        a = wrapped_label(r"By looking ahead, \ but less than the theory says. \ A household that can borrow and "
                          r"save spreads a windfall over its life and spends only its interest; \ prudence keeps a "
                          r"buffer of cash, \ and below it spending follows income. \ Real households spend 10 to 40\% "
                          r"of a windfall within a quarter, \ most when cash is short, \ whatever they own; \ and "
                          r"across generations, \ saving depends on growth, \ pensions and bequests.", 11.6, 27, WHITE)
        a.next_to(q, DOWN, buff=0.55)
        r = load("rebate")
        mini = plane([2000.5, 2002.5], [97, 104.5], x_length=4.2, y_length=1.3)
        jun = r["dates"].index("2001-06-01")
        logo = VGroup(path(mini, r["t"], np.array(r["Y"]) / r["Y"][jun] * 100, INCOME, width=4, smooth=False),
                      path(mini, r["t"], np.array(r["CNS"]) / r["CNS"][jun] * 100, SPEND, width=4, smooth=False))
        logo.next_to(a, DOWN, buff=0.4)
        with self.voiceover(
            "So: how do households decide how much to spend today? <bookmark mark='a'/> By looking ahead, but less "
            "than the theory says. A household that can borrow and save spreads a windfall over its life and spends "
            "only the interest. Prudence keeps a buffer of cash, and below the buffer spending follows income. Real "
            "households spend ten to forty percent of a windfall within a quarter, most of all when they are short "
            "of cash, whatever they own. And across generations, how much a nation saves depends on its growth, its "
            "pensions and its bequests."
        ) as vo:
            self.play(FadeIn(q, shift=UP * 0.2))
            vo.wait_until("a")
            self.play(FadeIn(a, shift=UP * 0.1), run_time=2)
            self.play(Create(logo), run_time=1.5)
        self.clear_scene()

    def recap(self):
        k, h, m, ht, o, c = (load(x) for x in ("kuznets", "hall", "mpc", "htm", "olg", "china"))
        items = [
            (r"the 2001 rebates: \ timing set by a Social Security digit, \ an experiment no one designed", SAVE),
            (r"Play it: \ 20 to 40 cents of each dollar on nondurables within the quarter", SAVE),
            (rf"Keynes and Kuznets: \ the rich save more, \ nations do not; \ Friedman: \ slope "
             rf"{k['island']['elasticity']:.2f} from luck", SPEND),
            (r"permanent income: \ spend the interest on a windfall; \ the life cycle's hump of wealth", INCOME),
            (rf"Hall's random walk: \ rejected, \ $F = {h['F']:.1f}$ on sixty years of US quarters", HOLD),
            (rf"rule-of-thumb households: \ $\hat\lambda = {h['iv']:.2f}$, \ weakly identified; \ consumption too "
             r"smooth", GREY_A),
            (rf"the buffer stock: \ prudence bends $c(m)$; \ {m['mean_mpc']:.2f} of a month's windfall in a year",
             CASH),
            (r"the rebates, \ Alaska's dividend, \ and Hall: \ partly right", SAVE),
            (rf"the wealthy hand-to-mouth: \ spending follows liquid wealth \ (correlation "
             rf"{ht['corr_liquid']:+.2f})", HOUSE),
            (r"Ricardian equivalence: \ a benchmark that fails where cash is short", GREY_A),
            (rf"overlapping generations: \ a pension is a free lunch only if $R < 1 + n$", PENSION),
            (rf"China: \ household consumption {c['chn_2010']:.2f} of GDP in 2010; \ a dial on the propensity to spend",
             RISK),
        ]
        rows = VGroup(*[label(rf"{n + 1}.\ \ {txt}", font_size=28, color=col) for n, (txt, col) in enumerate(items)])
        rows.arrange(DOWN, aligned_edge=LEFT, buff=0.2)
        head = label(r"Part 22, \ in twelve lines", font_size=42).to_edge(UP, buff=0.3)
        if rows.width > 13.2:
            rows.width = 13.2
        room = head.get_bottom()[1] - 0.35 + 3.75
        if rows.height > room:
            rows.scale_to_fit_height(room)
        rows.next_to(head, DOWN, buff=0.35)
        del o
        with self.voiceover(
            "Part twenty-two in twelve lines. <bookmark mark='a'/> The 2001 rebates went out in an order set by a "
            "digit, an experiment no one designed, and households spent twenty to forty cents of each dollar on "
            "nondurables within the quarter. Keynes's function fits across households and fails across time, and "
            "Friedman's permanent income explains much of why. A forward-looking household spends only the interest "
            "on a windfall, and builds a hump of wealth for retirement. Hall's random walk is rejected on sixty years "
            "of American data: past income predicts spending. A large share of income goes to households who spend "
            "what they get, and consumption is smoother than the theory says. Prudence bends the consumption "
            "function and builds a buffer of cash. Hall's prediction was partly right. Spending follows liquid "
            "wealth, not net worth. Ricardian equivalence is a benchmark that fails where cash is short. A "
            "pay-as-you-go pension is a free lunch only in an inefficient economy. And China's households consumed "
            "about a third of output by 2010; and a dial records how much of a windfall people spend."
        ) as vo:
            self.play(FadeIn(head))
            vo.wait_until("a")
            self.play(LaggedStart(*[FadeIn(r_, shift=RIGHT * 0.15) for r_ in rows], lag_ratio=0.8), run_time=46.0)
        self.clear_scene()

    def problems(self):
        ps = problem_set(PROBLEMS, font_size=20, width=13.0)
        with self.voiceover(
            "The problems. Friedman's errors in variables; the permanent-income annuity; Hall's random walk and its "
            "test; Working's averaging; Campbell and Mankiw's instrument; prudence; Ricardian equivalence; and a "
            "starred problem on Diamond's economy and the pension. Full solutions are in the part's notes."
        ):
            self.play(FadeIn(ps.head), FadeIn(ps.rows[0], shift=UP * 0.1), run_time=0.8)
            self.play(LaggedStart(*[FadeIn(r) for r in ps.rows[1:]], lag_ratio=0.4), run_time=6)
        self.wait(4)
        self.clear_scene()

    def references(self):
        rc = reference_card(
            [r"Angus Deaton, \emph{Understanding Consumption} (1992)",
             r"David Romer, \emph{Advanced Macroeconomics} (5th ed., 2019), \ chs.\ 2 and 8",
             r"Lars Ljungqvist and Thomas Sargent, \emph{Recursive Macroeconomic Theory} (4th ed., 2018), \ chs.\ 17--18",
             r"Milton Friedman, \emph{A Theory of the Consumption Function} (1957)"],
            [r"Modigliani and Brumberg (1954); \ Hall (1978); \ Flavin (1981); \ Campbell and Mankiw (1989); \ "
             r"Working (1960)",
             r"Zeldes (1989); \ Kimball (1990); \ Deaton (1991); \ Carroll (1997, 2006)",
             r"Johnson, Parker and Souleles (2006); \ Parker et al.\ (2013, 2022); \ Hsieh (2003); \ Kueng (2018)",
             r"Kaplan, Violante and Weidner (2014); \ Kaplan and Violante (2014); \ Fagereng, Holm and Natvik (2021)",
             r"Jappelli and Pistaferri (2014); \ Fuster, Kaplan and Zafar (2021); \ Sahm, Shapiro and Slemrod (2012)",
             r"Barro (1974); \ Samuelson (1958); \ Diamond (1965); \ Abel, Mankiw, Summers and Zeckhauser (1989)",
             r"Dynan, Skinner and Zeldes (2004); \ Modigliani and Cao (2004); \ Chamon and Prasad (2010); \ Wei and "
             r"Zhang (2011); \ Ganong and Noel (2019)"])
        with self.voiceover(
            "The reading: Angus Deaton's Understanding Consumption, still the best short book on the subject; "
            "Romer's Advanced Macroeconomics for the graduate treatment; Ljungqvist and Sargent for the recursive "
            "methods; and Friedman's own book. Then the papers, from Modigliani and Brumberg to bank accounts."
        ):
            self.play(FadeIn(rc))
        self.wait(1.5)
        self.clear_scene()

    def next_part(self):
        hc = history_card(1985, r"Rajnish Mehra and Edward Prescott", r"the standard model says stocks should pay a "
                          r"fraction of a percent over bills; \ they paid about six", color=E.ACCENT, width=10.4,
                          font_size=24)
        nxt = VGroup(label(r"Next: \ Part 23 \ $\cdot$ \ Act V, \ The Long Run", font_size=30, color=GREY_B),
                     label(r"Capital and Asset Prices", font_size=46),
                     label(r"what is a claim on the future worth, \ and how does that decide what gets built?",
                           font_size=26, color=E.ACCENT)).arrange(DOWN, buff=0.22)
        head = label(r"this part: \ how households save; \ next: \ what their savings buy, \ and at what price",
                     font_size=26, color=GREY_A).to_edge(UP, buff=0.5)
        VGroup(hc, nxt).arrange(DOWN, buff=0.6).next_to(head, DOWN, buff=0.5)
        with self.voiceover(
            "This part asked how households save. The next asks what their savings buy, and at what price. "
            "<bookmark mark='a'/> In 1985 Rajnish Mehra and Edward Prescott fed a century of American consumption "
            "into the standard model and asked what stocks should have paid over safe bills. The model said a "
            "fraction of a percent. The record said about six. <bookmark mark='b'/> Part twenty-three: capital and "
            "asset prices. What is a claim on the future worth, and how does that decide what gets built?"
        ) as vo:
            self.play(FadeIn(head))
            vo.wait_until("a")
            self.play(FadeIn(hc, shift=UP * 0.2))
            vo.wait_until("b")
            self.play(FadeIn(nxt, shift=UP * 0.2))
        self.wait(9.5)
        self.clear_scene()

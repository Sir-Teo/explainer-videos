from __future__ import annotations

from videos.economics.econ41.common import *  # noqa: F403

PROBLEMS = [
    r"Laffer: \ revenue is $t(1 - t)^e$. \ Find the revenue-maximizing rate for $e$ = 0.5, \ and the revenue lost by "
    r"setting the rate 10 points above it.",
    r"Incidence: \ demand elasticity 0.5, \ supply elasticity 1. \ What share of a small tax do buyers bear? \ And if "
    r"supply were perfectly elastic?",
    r"The triangle: \ with the same elasticities, \ use Harberger's formula for the deadweight loss of a 10\% and a "
    r"30\% tax, \ per unit of spending.",
    r"Ramsey: \ two independent goods with elasticities 0.5 and 2. \ If the first is taxed at 20\%, \ what does "
    r"Ramsey's rule set for the second?",
    r"The top rate: \ $a$ = 1.5. \ Find the top rate for $e$ = 0.2 and 0.5, \ with $g$ = 0 and with $g$ = 0.3.",
    r"Bunching: \ a kink at 50 where the rate rises from 20\% to 40\%; \ the excess mass is 3.5 (thousand). \ What "
    r"elasticity does Saez's formula give?",
    r"Evasion: \ in Allingham and Sandmo's model with risk neutrality, \ when is it optimal to declare everything? "
    r"\ (audit probability $p$, \ fine $\theta$)",
    r"$\bigstar$ \ Derive the top rate: \ show that a small increase $d\tau$ yields $(1 - g)(z_m - \bar z)d\tau - "
    r"\tau e z_m d\tau/(1-\tau)$ per top earner, \ and solve for $\tau^{*}$.",
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
        a = wrapped_label(r"Whoever cannot escape it: \ workers bear much of a tax on mobile capital, \ and buyers "
                          r"bear taxes they do not see. \ The top rate that raises the most is $1/(1 + ae)$: \ about "
                          r"seventy percent if top incomes respond weakly, \ forty if they respond strongly, \ and how "
                          r"strongly depends partly on the tax law itself.", 11.6, 25, WHITE)
        a.next_to(q, DOWN, buff=0.5)
        F = load("film")
        mini = plane([1913, 2025], [0, 100], x_length=4.2, y_length=1.3)
        logo = path(mini, F["t"], F["v"], RATE, 2.4, smooth=False).next_to(a, DOWN, buff=0.35)
        with self.voiceover(
            "So: who really pays a tax, and how high should the top rate be? <bookmark mark='a'/> Whoever cannot "
            "escape it: workers bear much of a tax on mobile capital, and buyers bear the taxes they do not see. The "
            "top rate that raises the most is one over one plus a times e: about seventy percent if top incomes "
            "respond weakly, forty if they respond strongly; and how strongly they respond depends partly on the tax "
            "law itself."
        ) as vo:
            self.play(FadeIn(q, shift=UP * 0.2))
            vo.wait_until("a")
            self.play(FadeIn(a, shift=UP * 0.1), run_time=2)
            self.play(Create(logo), run_time=1.5)
        self.clear_scene()

    def recap(self):
        N, H, Tr, P, R, M, E_, B, Ev = (load(x) for x in ("napkin", "harberger", "triangle", "top", "ramsey",
                                                          "mirrlees", "eti", "bunching", "evasion"))
        O = H["open"]
        items = [
            (rf"the napkin: \ the top of the curve at {100 * N['peak'][0]:.0f}\% or {100 * N['peak'][1]:.0f}\%, \ "
             r"by the elasticity", REVENUE),
            (rf"incidence: \ workers bear none (closed) to {100 * O['worker_per_revenue']:.0f}\% of revenue (open); "
             r"\ Germany about half", WORKER),
            (rf"the triangle: \ loss {100 * Tr['at']['0.1']['dwl'] / Tr['at']['0.1']['revenue']:.1f}\% of revenue at "
             rf"10\%, \ {100 * Tr['at']['0.4']['dwl'] / Tr['at']['0.4']['revenue']:.1f}\% at 40\%", LOSS),
            (rf"the game: \ $a$ = {P['a']:.2f}, \ $e$ = 0.25 \ $\Rightarrow$ {100 * P['rates']['0.25']:.0f}\%", TOP),
            (rf"Ramsey: \ tax the inelastic; \ {R['total_uniform'] / R['total_ramsey']:.1f} times less loss", GOODS[0]),
            (r"Mirrlees: \ the government sees income, \ not ability", WORKER),
            (r"the top rate: \ $(1 - g)/(1 - g + ae)$, \ derived from one small reform", TOP),
            (rf"the schedule: \ a U, \ {100 * M['bottom']:.0f}\%, \ {100 * M['min']['Tp']:.0f}\%, \ "
             rf"{100 * M['top']:.0f}\%; \ the EITC at the bottom", RATE),
            (rf"the elasticity: \ about {E_['tra86']:.1f} in 1986, \ much of it relabelling; \ a policy choice",
             RATE),
            (rf"bunching: \ {B['e_hat']:.2f} against {B['e']:.2f} planted; \ only the self-employed bunch", WORKER),
            (r"salience, \ havens, \ capital: \ visibility, \ 36\% of profits shifted, \ Chamley-Judd revised",
             CAPITAL),
            (r"evasion: \ 0.3\% against 37\%: \ third-party reporting works", GAIN),
        ]
        rows = VGroup(*[label(rf"{n + 1}.\ \ {txt}", font_size=28, color=col) for n, (txt, col) in enumerate(items)])
        rows.arrange(DOWN, aligned_edge=LEFT, buff=0.2)
        head = label(r"Part 41, \ in twelve lines", font_size=42).to_edge(UP, buff=0.3)
        if rows.width > 13.2:
            rows.width = 13.2
        room = head.get_bottom()[1] - 0.35 + 3.75
        if rows.height > room:
            rows.scale_to_fit_height(room)
        rows.next_to(head, DOWN, buff=0.35)
        with self.voiceover(
            "Part forty-one in twelve lines. <bookmark mark='a'/> The Laffer curve is right, and where its top lies "
            "depends on the elasticity. A tax falls on whoever cannot escape it, so workers bear much of a tax on "
            "mobile capital. A tax's cost grows with the square of its rate. Three numbers set the top rate. "
            "Ramsey's rule taxes what people cannot avoid buying, though fairness and production efficiency qualify "
            "it. Mirrlees showed that the income tax is limited by what the government can see. One small reform "
            "derives the top rate, and the whole schedule is shaped like a U, with work subsidies at the bottom. "
            "The elasticity is measured from reforms and bunching, and much of it is relabelling that tax design can "
            "shut down. People ignore taxes they do not see; profits move to havens; the case against taxing capital "
            "has weakened. And third-party reporting, not fear of audits, is why most people pay."
        ) as vo:
            self.play(FadeIn(head))
            vo.wait_until("a")
            self.play(LaggedStart(*[FadeIn(r_, shift=RIGHT * 0.15) for r_ in rows], lag_ratio=0.8), run_time=44.0)
        self.clear_scene()

    def problems(self):
        ps = problem_set(PROBLEMS, font_size=19, width=13.0)
        with self.voiceover(
            "The problems. A Laffer curve; incidence; the triangle; Ramsey's rule; the top rate; bunching; evasion; "
            "and a starred derivation of the top rate. Full solutions are in the part's notes."
        ):
            self.play(FadeIn(ps.head), FadeIn(ps.rows[0], shift=UP * 0.1), run_time=0.8)
            self.play(LaggedStart(*[FadeIn(r) for r in ps.rows[1:]], lag_ratio=0.4), run_time=6)
        self.wait(4)
        self.clear_scene()

    def references(self):
        rc = reference_card(
            [r"Bernard Salani\'e, \emph{The Economics of Taxation} (2nd edition, 2011)",
             r"Joel Slemrod and Jon Bakija, \emph{Taxing Ourselves} (5th edition, 2017)",
             r"Peter Diamond and Emmanuel Saez, \ `The Case for a Progressive Tax', \ \emph{JEP} (2011)",
             r"Jonathan Gruber, \emph{Public Finance and Public Policy}, \ chapters 18--25"],
            [r"Ramsey (1927); \ Harberger (1962); \ Mirrlees (1971); \ Diamond and Mirrlees (1971)",
             r"Allingham and Sandmo (1972); \ Atkinson and Stiglitz (1976); \ Judd (1985); \ Chamley (1986)",
             r"Feldstein (1995); \ Diamond (1998); \ Saez (2001, \ 2002, \ 2010); \ Gruber and Saez (2002)",
             r"Chetty, \ Looney and Kroft (2009); \ Kleven et al.\ (2011); \ Saez, \ Slemrod and Giertz (2012)",
             r"Kleven and Waseem (2013); \ Kleven, \ Landais and Saez (2013); \ Zucman (2013)",
             r"Piketty, \ Saez and Stantcheva (2014); \ Fuest, \ Peichl and Siegloch (2018); \ Straub and Werning "
             r"(2020)"])
        with self.voiceover(
            "The reading: Bernard Salanie's The Economics of Taxation for the theory; Slemrod and Bakija's Taxing "
            "Ourselves for the practice; Diamond and Saez's case for a progressive tax; and Gruber's textbook "
            "chapters. Then the papers, from Ramsey to the global minimum tax."
        ):
            self.play(FadeIn(rc))
        self.wait(1.5)
        self.clear_scene()

    def next_part(self):
        hc = history_card(2008, r"Oregon", r"has money to add about 10,000 adults to Medicaid, \ and 90,000 people who "
                          r"want in: \ it holds a lottery", color=E.ACCENT, width=10.4, font_size=24)
        nxt = VGroup(label(r"Next: \ Part 42 \ $\cdot$ \ Act VIII, \ Work and the State", font_size=30, color=GREY_B),
                     label(r"Social Insurance", font_size=46),
                     label(r"what should the state insure, \ and how generously?", font_size=24,
                           color=E.ACCENT)).arrange(DOWN, buff=0.22)
        head = label(r"from what taxes take \ to what the state gives back", font_size=26, color=GREY_A).to_edge(
            UP, buff=0.5)
        VGroup(hc, nxt).arrange(DOWN, buff=0.6).next_to(head, DOWN, buff=0.5)
        with self.voiceover(
            "This part asked what taxes take, and from whom. The next asks what the state gives back. "
            "<bookmark mark='a'/> In 2008 the state of Oregon had money to add about ten thousand adults to Medicaid, "
            "and ninety thousand people who wanted in. It held a lottery, and for the first time in decades there was "
            "a randomized experiment on what health insurance does. <bookmark mark='b'/> Part forty-two: social "
            "insurance. What should the state insure, and how generously?"
        ) as vo:
            self.play(FadeIn(head))
            vo.wait_until("a")
            self.play(FadeIn(hc, shift=UP * 0.2))
            vo.wait_until("b")
            self.play(FadeIn(nxt, shift=UP * 0.2))
        self.wait(9.5)
        self.clear_scene()

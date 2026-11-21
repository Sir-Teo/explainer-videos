from __future__ import annotations

from videos.economics.econ52.common import *  # noqa: F403

PROBLEMS = [
    r"Gorman: \ three households spend $c_i = 5 + b_i m_i$ with $b = (0.9, 0.6, 0.3)$. \ A transfer of 10 goes from "
    r"the third to the first. \ By how much does total spending change? \ With equal slopes?",
    r"The supermartingale: \ with $\beta(1 + r) = 1$ and income risk, \ show that $u'(c_t)$ is a nonnegative "
    r"supermartingale, \ and explain why consumption cannot settle down.",
    r"Aiyagari's market: \ with $\alpha = 0.36$, \ $\delta = 0.08$, \ find capital per worker at $r = 4.17\%$ and at "
    r"$r = 2.12\%$. \ By what percentage does capital rise?",
    r"Huggett: \ explain why bonds held must sum to zero, \ and why the interest rate that clears the market falls "
    r"as the borrowing limit tightens.",
    r"Krusell and Smith: \ a rule $\log K' = 0.13 + 0.964 \log K$. \ Find its fixed point. \ What does $R^2$ miss "
    r"that Den Haan's test catches?",
    r"Werning's benchmark: \ with debt fixed and output set by demand, \ show that a balanced-budget increase in "
    r"purchases raises output one for one, \ whatever the MPCs.",
    r"Fake news: \ show that $\mathbf{J}_{t,s} = \mathbf{F}_{t,s} + \mathbf{J}_{t-1,s-1}$ when the economy is the "
    r"same at every date.",
    r"$\bigstar$ \ Hopenhayn: \ derive the stationary mass of firms $\mu = M\,(I - \mathbf{P}^{\top} X)^{-1}\nu$, "
    r"\ and show that a higher entry cost lowers the exit threshold.",
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
        a = wrapped_label(r"Whatever depends on who holds what: \ how much a nation saves and the interest rate it "
                          r"needs, \ the top of the wealth distribution, \ how a rate cut reaches spending, \ how "
                          r"large a multiplier is, \ who gains from inflation. \ For the path of capital, \ one "
                          r"household is nearly enough; \ for spending, \ it is not.", 11.6, 25, WHITE)
        a.next_to(q, DOWN, buff=0.5)
        people = crowd(26, 3, 9.0, 1.0, colors=(MANY, POOR, RICH)).next_to(a, DOWN, buff=0.5)
        with self.voiceover(
            "So: what does macroeconomics get wrong by treating a country as one household? <bookmark mark='a'/> "
            "Whatever depends on who holds what. How much a nation saves, and the interest rate it needs: "
            "households who cannot insure their risks save more, and push the rate below the rate of time "
            "preference. The top of the wealth distribution, which needs more than bad luck to explain. How a rate "
            "cut reaches spending, which is mostly through incomes when liquid wealth is scarce. How large a "
            "multiplier is, and who gains from inflation. For the path of capital, one household is nearly enough, "
            "as Krusell and Smith found. For spending, which is done disproportionately by those with little, it "
            "is not."
        ) as vo:
            self.play(FadeIn(q, shift=UP * 0.2))
            vo.wait_until("a")
            self.play(FadeIn(a, shift=UP * 0.1), run_time=2)
            self.play(LaggedStart(*[FadeIn(d, scale=0.5) for d in people], lag_ratio=0.02), run_time=12.0)
            self.play(Indicate(a, color=E.ACCENT, scale_factor=1.0), run_time=2.0)
        self.clear_scene()

    def recap(self):
        A, W, K, Hk, P, J, F, C = (load(x) for x in ("aiyagari", "wealth", "ks", "hank", "playit", "jacobian",
                                                     "firms", "continuous"))
        isl = next(r for r in Hk["rows"] if r["liquid"] == Hk["island"])
        one = next(r for r in Hk["rows"] if r["liquid"] == 1.0)
        win = max(P["rows"], key=lambda r: r["total"])
        fifth = (r"poorest", r"second", r"middle", r"fourth", r"richest")[win["group"]]
        items = [
            (r"Gorman: \ one household is exact only with straight, \ parallel Engel curves", REP),
            (r"incomplete markets: \ uninsured risk pushes the rate below time preference", MANY),
            (rf"Aiyagari: \ {100 * A['r']:.2f}\% against {100 * A['rho_time']:.2f}\%; \ "
             rf"{100 * (A['K'] / A['K_rep'] - 1):.0f}\% more capital", SUPPLY),
            (r"the Island: \ 100{,}000 households and the histogram agree", DIST),
            (rf"rates fall: \ the {fifth} fifth's spending rises most; \ the poorest's, \ through incomes",
             INDIRECT),
            (rf"the top: \ {W['data']['top1']:.0f}\% in the data, \ {W['models'][0]['top1']:.0f}\% in the model, "
             rf"\ more with lucky returns", DIST),
            (rf"Krusell and Smith: \ the mean is nearly enough, \ $R^2$ {K['r2'][1]:.5f}", RULE),
            (r"continuous time: \ one sparse matrix, \ and its transpose", THEORY),
            (rf"HANK: \ {100 * (1 - isl['share_impact']):.0f}\% of the first quarter through incomes", INDIRECT),
            (rf"fake news: \ {J['fake_seconds']:.2f} s against about {J['brute_seconds_all']:.0f} s", THEORY),
            (rf"policy: \ a deficit multiplier of {one['mult_deficit']:.2f} with little liquid wealth", POOR),
            (r"firms: \ entry barriers protect the unproductive; \ lumps vanish in the sum", FIRM),
        ]
        rows = VGroup(*[label(rf"{n + 1}.\ \ {txt}", font_size=28, color=col) for n, (txt, col) in enumerate(items)])
        rows.arrange(DOWN, aligned_edge=LEFT, buff=0.2)
        head = label(r"Part 52, \ in twelve lines", font_size=42).to_edge(UP, buff=0.3)
        if rows.width > 13.2:
            rows.width = 13.2
        room = head.get_bottom()[1] - 0.35 + 3.75
        if rows.height > room:
            rows.scale_to_fit_height(room)
        rows.next_to(head, DOWN, buff=0.35)
        del C, F
        with self.voiceover(
            "Part fifty-two in twelve lines. <bookmark mark='r1'/> One household stands for many only if everyone "
            "spends an extra dollar alike. <bookmark mark='r2'/> Risk that cannot be insured pushes the interest "
            "rate below the rate of time preference. <bookmark mark='r3'/> In Aiyagari's economy, that means more "
            "capital, built by precaution. <bookmark mark='r4'/> A simulated population and a moving histogram "
            "give the same answer. <bookmark mark='r5'/> When rates fall, the poorest respond through their "
            "incomes, not the rate. <bookmark mark='r6'/> The simple model misses the very rich; lucky returns can "
            "make them. <bookmark mark='r7'/> With aggregate shocks, the mean is nearly enough for capital. "
            "<bookmark mark='r8'/> In continuous time, the distribution comes from the transpose of one matrix. "
            "<bookmark mark='r9'/> In HANK, most of a rate cut's effect comes through incomes. <bookmark "
            "mark='r10'/> Sequence-space Jacobians solve such economies in a second. <bookmark mark='r11'/> "
            "Deficit-financed spending multiplies more when households cannot borrow. <bookmark mark='r12'/> And "
            "populations of firms enter, grow and exit, and their lumps mostly vanish in the sum."
        ) as vo:
            self.play(FadeIn(head))
            for i, r_ in enumerate(rows):
                vo.wait_until(f"r{i + 1}")
                self.play(FadeIn(r_, shift=RIGHT * 0.15), run_time=0.8)
            self.play(Indicate(rows, color=WHITE, scale_factor=1.0), run_time=2.0)
        self.clear_scene()

    def problems(self):
        ps = problem_set(PROBLEMS, font_size=19, width=13.0)
        with self.voiceover(
            "The problems. Gorman's condition with numbers; why marginal utility is a supermartingale; Aiyagari's "
            "extra capital; why Huggett's rate falls as the limit tightens; the fixed point of a Krusell and Smith "
            "rule; the balanced-budget multiplier; the fake-news recursion; and a starred problem on Hopenhayn's "
            "stationary industry. Full solutions are in the part's notes."
        ):
            self.play(FadeIn(ps.head), FadeIn(ps.rows[0], shift=UP * 0.1), run_time=0.8)
            self.play(LaggedStart(*[FadeIn(r) for r in ps.rows[1:]], lag_ratio=0.4), run_time=6)
        self.wait(4)
        self.clear_scene()

    def references(self):
        rc = reference_card(
            [r"Lars Ljungqvist and Thomas Sargent, \emph{Recursive Macroeconomic Theory}, \ chapters 17 and 18",
             r"Greg Kaplan, \ `Heterogeneous agent macroeconomics', \ lecture notes, \ and Benjamin Moll's notes on "
             r"continuous time",
             r"Per Krusell and Anthony Smith, \ `Quantitative macroeconomic models with heterogeneous agents' "
             r"(2006)",
             r"Adrien Auclert and coauthors, \ the sequence-space Jacobian toolkit and its documentation"],
            [r"Gorman (1953); \ Bewley (1977); \ Kirman (1992); \ Hopenhayn (1992); \ Huggett (1993); \ "
             r"Aiyagari (1994)",
             r"Krusell and Smith (1998); \ Doepke and Schneider (2006); \ Khan and Thomas (2008); \ Den Haan (2010)",
             r"Young (2010); \ Benhabib, Bisin and Zhu (2011, 2015); \ Kaplan and Violante (2014); \ Werning (2015)",
             r"McKay, Nakamura and Steinsson (2016); \ Kaplan, Moll and Violante (2018)",
             r"Auclert, Bardóczy, Rognlie and Straub (2021); \ Fagereng, Holm and Natvik (2021); \ Achdou et al. "
             r"(2022)"])
        with self.voiceover(
            "The reading: Ljungqvist and Sargent's chapters on incomplete markets; lecture notes by Greg Kaplan "
            "and by Benjamin Moll; Krusell and Smith's own survey; and the documentation of the sequence-space "
            "Jacobian toolkit. Then the papers, from Gorman to the fake news."
        ):
            self.play(FadeIn(rc))
        self.wait(1.5)
        self.clear_scene()

    def next_part(self):
        hc = history_card(2011, r"Emir Kamenica and Matthew Gentzkow", r"a prosecutor who cannot lie, \ but chooses "
                          r"which investigation to run, \ and a judge who follows the evidence", color=E.ACCENT,
                          width=10.4, font_size=24)
        nxt = VGroup(label(r"Next: \ Part 53 \ $\cdot$ \ Act X, \ The Graduate Core", font_size=30, color=GREY_B),
                     label(r"Information and Persuasion", font_size=46),
                     label(r"how does someone who controls only what others learn get them to do what she wants?",
                           font_size=22, color=E.ACCENT)).arrange(DOWN, buff=0.22)
        head = label(r"from what people have \ to what people know", font_size=26, color=GREY_A).to_edge(UP,
                                                                                                         buff=0.5)
        steps = VGroup(*[VGroup(RoundedRectangle(width=2.9, height=0.9, corner_radius=0.12, stroke_color=c_,
                                                 stroke_width=2.0), label(t_, font_size=18, color=c_))
                         for t_, c_ in ((r"types and beliefs", DIST), (r"signals", RULE),
                                        (r"cheap talk", MANY), (r"persuasion", INDIRECT))])
        for s_ in steps:
            s_[1].move_to(s_[0])
        steps.arrange(RIGHT, buff=0.3)
        VGroup(hc, steps, nxt).arrange(DOWN, buff=0.45).next_to(head, DOWN, buff=0.4)
        with self.voiceover(
            "Next time, the households differ not in what they have but in what they know. <bookmark mark='a'/> A "
            "prosecutor cannot lie to the judge, but she chooses which investigation to run, and the judge follows "
            "the evidence. <bookmark mark='b'/> Part fifty-three builds the games of incomplete information: types "
            "and beliefs, signals, cheap talk, <bookmark mark='c'/> and the design of information itself, Emir "
            "Kamenica and Matthew Gentzkow's theory of Bayesian persuasion."
        ) as vo:
            self.play(FadeIn(head))
            vo.wait_until("a")
            self.play(FadeIn(hc, shift=UP * 0.1))
            vo.wait_until("b")
            self.play(LaggedStart(*[FadeIn(s_) for s_ in steps], lag_ratio=0.4), run_time=2.0)
            vo.wait_until("c")
            self.play(FadeIn(nxt, shift=UP * 0.1))
        self.wait(9.5)

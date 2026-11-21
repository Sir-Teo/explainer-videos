from __future__ import annotations

from videos.economics.econ55.common import *  # noqa: F403

PROBLEMS = [
    r"Counting: \ with $n$ variables, \ how many restrictions does a structural VAR need beyond $\Sigma = BB'$? \ "
    r"How many does the recursive ordering supply?",
    r"Timing: \ in a VAR of output, \ prices and the rate, \ which zeros does ordering the rate last impose, \ and "
    r"what must the bank not know for them to hold?",
    r"The long run: \ with $C(1) = (I - A_1 - \dots - A_p)^{-1}$, \ show that only the first shock moves the first "
    r"variable's level for ever if $C(1)B$ is lower triangular.",
    r"An instrument: \ if $z_t = \lambda \varepsilon^m_t + \eta_t$ with $\eta$ independent of every shock, \ show "
    r"that $\mathrm{Cov}(u_t, z_t) \propto b_m$.",
    r"Heteroskedasticity: \ if only $\varepsilon^m$'s variance changes, \ show that $\Sigma_1 - \Sigma_0$ has rank "
    r"one, \ and find $b_m$ from it.",
    r"Local projections: \ in a VAR(1), \ show that the population projection coefficient at horizon $h$ equals "
    r"$A^h b$.",
    r"Weak identification: \ a posterior is 90\% as wide as its prior. \ What should a referee ask for?",
    r"$\bigstar$ \ The missing intercept: \ in $y_{rt} = m_\ell (g_{rt} - \bar g_t) + m_a \bar g_t + u_t + "
    r"e_{rt}$, \ show that year effects remove $m_a$ and leave $m_\ell$.",
]


class Outro(VoiceoverScene):
    def construct(self):
        self.answer()
        self.recap()
        self.problems()
        self.references()
        self.next_part()

    def answer(self):
        q = wrapped_label(ASK, 12.0, 40, E.ACCENT).move_to(UP * 2.4)
        a = wrapped_label(r"Only by adding an assumption the data cannot supply, \ about timing, \ the long run, \ "
                          r"signs, \ an outside instrument or a change in variance, \ and then by testing it where "
                          r"the truth is known, \ against instruments built from the bank's own records and from "
                          r"markets, \ and against regions that saw different policies. \ The sign and timing of "
                          r"policy's effects survive every credible method; \ their size still depends on the "
                          r"assumption.", 11.6, 25, WHITE)
        a.next_to(q, DOWN, buff=0.5)
        F = load("film")
        mini = plane([F["t"][0], F["t"][-1]], [0, 1], x_length=4.2, y_length=1.3)
        v = np.array(F["spread"])
        v = (v - v.min()) / (v.max() - v.min())
        logo = path(mini, F["t"], v, RATE, 2.0, smooth=False).next_to(a, DOWN, buff=0.4)
        with self.voiceover(
            "So: with one history and no control group, how can anyone say what a policy did? <bookmark mark='a'/> "
            "Only by adding an assumption the data cannot supply, about timing, the long run, signs, an outside "
            "instrument or a change in variance, and then by testing it: where the truth is known, as on the "
            "Island; against instruments built from the bank's own records and from markets; and against regions "
            "that saw different policies. What survives every credible method is the sign and the timing of "
            "policy's effects. Their size still depends on the assumption, and an honest answer says which one."
        ) as vo:
            self.play(FadeIn(q, shift=UP * 0.2))
            vo.wait_until("a")
            self.play(FadeIn(a, shift=UP * 0.1), run_time=2)
            self.play(Create(logo), run_time=12.0, rate_func=linear)
            self.play(Indicate(a, color=E.ACCENT, scale_factor=1.0), run_time=2.0)
        self.clear_scene()

    def recap(self):
        P, M, L, D, W, G, I = (load(x) for x in ("puzzle", "schemes_mc", "lpvar", "dsge", "dsge_weak", "regions",
                                                  "irfmatch"))
        weak = [n for n in W["names"] if W["params"][n]["ratio"] > 0.5]
        items = [
            (rf"the price puzzle: \ prices up for {P['months_above_zero']} months; \ commodity prices undo it", INFL),
            (r"a VAR alone: \ six numbers known, \ nine needed", DATA),
            (r"Play it: \ you knew a tightening by its signs", MONEY),
            (r"timing wrong on the Island; \ instrument and variance right", METHOD["proxy"]),
            (r"the long run finds supply; \ signs give a set, \ shaped by its prior", METHOD["long_run"]),
            (rf"projections: \ unbiased but noisier \ ({L['methods']['lp']['sd'][-1]:.2f} against "
             rf"{L['methods']['var1']['sd'][-1]:.2f})", METHOD["lp"]),
            (r"narrative and clean surprises cure the puzzle", METHOD["narrative"]),
            (r"a DSGE model: \ every posterior far narrower than its prior", EST),
            (rf"drop the rate: \ {len(weak)} of {len(W['names'])} posteriors are mostly prior", MODEL),
            (rf"regions: \ {G['b_fe']:.1f} relative, \ {G['b_nat']:.1f} national: \ the missing intercept", DEMAND),
            (rf"matching: \ $\sigma$ {I['estimate']['sigma']:.2f}, \ $\kappa$ uncertain", THEORY),
            (r"sign and timing agree; \ size depends on the assumption", E.ACCENT),
        ]
        rows = VGroup(*[label(rf"{n + 1}.\ \ {txt}", font_size=28, color=col) for n, (txt, col) in enumerate(items)])
        rows.arrange(DOWN, aligned_edge=LEFT, buff=0.2)
        head = label(r"Part 55, \ in twelve lines", font_size=42).to_edge(UP, buff=0.3)
        if rows.width > 13.2:
            rows.width = 13.2
        room = head.get_bottom()[1] - 0.35 + 3.75
        if rows.height > room:
            rows.scale_to_fit_height(room)
        rows.next_to(head, DOWN, buff=0.35)
        del M, D
        with self.voiceover(
            "Part fifty-five in twelve lines. <bookmark mark='r1'/> On American data, a recursive autoregression "
            "says prices rise after a hike, until commodity prices are added. <bookmark mark='r2'/> A vector "
            "autoregression alone knows six numbers and needs nine. <bookmark mark='r3'/> You recognized a "
            "tightening by its signs, which is an assumption. <bookmark mark='r4'/> On the Island, timing is wrong; "
            "an outside instrument and a change in variance are right. <bookmark mark='r5'/> The long run finds "
            "supply shocks; signs give a set whose shape depends on how it was drawn. <bookmark mark='r6'/> Local "
            "projections trade bias for noise. <bookmark mark='r7'/> Narrative and clean market surprises cure the "
            "price puzzle. <bookmark mark='r8'/> A whole model can be estimated with the Kalman filter and "
            "Metropolis-Hastings. <bookmark mark='r9'/> Without the right data, its posteriors are mostly its "
            "priors. <bookmark mark='r10'/> Regions identify relative effects, and the national one goes missing. "
            "<bookmark mark='r11'/> Matching responses estimates a model from what a shock does. <bookmark "
            "mark='r12'/> And the sign and timing of policy's effects agree across methods, while their size "
            "depends on the assumption."
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
            "The problems. Count the missing restrictions; read the zeros of a recursive ordering; the long-run "
            "restriction; why an instrument traces out a column; why a change in variance does; local projections "
            "in a simple autoregression; what to ask of a weak posterior; and a starred problem on the missing "
            "intercept. Full solutions are in the part's notes."
        ):
            self.play(FadeIn(ps.head), FadeIn(ps.rows[0], shift=UP * 0.1), run_time=0.8)
            self.play(LaggedStart(*[FadeIn(r) for r in ps.rows[1:]], lag_ratio=0.4), run_time=6)
        self.wait(4)
        self.clear_scene()

    def references(self):
        rc = reference_card(
            [r"Lutz Kilian and Helmut L\"utkepohl, \emph{Structural Vector Autoregressive Analysis} (2017)",
             r"James Hamilton, \emph{Time Series Analysis} (1994), \ chapters 11 to 13",
             r"Valerie Ramey, \ `Macroeconomic shocks and their propagation', \emph{Handbook of Macroeconomics} "
             r"(2016)",
             r"Emi Nakamura and J\'on Steinsson, \ `Identification in macroeconomics', \emph{JEP} (2018)"],
            [r"Sims (1980, 1992); \ Blanchard and Quah (1989); \ Kuttner (2001); \ Rigobon (2003)",
             r"Romer and Romer (2004); \ Jord\`a (2005); \ Uhlig (2005); \ Christiano, Eichenbaum and Evans (2005)",
             r"An and Schorfheide (2007); \ Smets and Wouters (2007); \ Canova and Sala (2009)",
             r"Stock and Watson (2012, 2018); \ Mertens and Ravn (2013); \ Nakamura and Steinsson (2014, 2018)",
             r"Gertler and Karadi (2015); \ Goldsmith-Pinkham, Sorkin and Swift (2020); \ Plagborg-M{\o}ller and "
             r"Wolf (2021)"])
        with self.voiceover(
            "The reading: Kilian and Lütkepohl's book on structural autoregressions; Hamilton's chapters on vector "
            "autoregressions; Valerie Ramey's survey of shocks; and Nakamura and Steinsson on identification in "
            "macroeconomics. Then the papers, from Sims to the projections."
        ):
            self.play(FadeIn(rc))
        self.wait(1.5)
        self.clear_scene()

    def next_part(self):
        hc = history_card(2026, r"the night before the first-year examinations",
                          r"twelve problems of the kind every PhD programme sets: \ four in micro, \ four in macro, \ "
                          r"four in econometrics", color=E.ACCENT, width=10.4, font_size=23)
        nxt = VGroup(label(r"Next: \ Part 56 \ $\cdot$ \ Act X, \ The Graduate Core", font_size=30, color=GREY_B),
                     label(r"The Core Exam", font_size=46),
                     label(r"can you do it with the book closed?", font_size=24, color=E.ACCENT)).arrange(DOWN,
                                                                                                         buff=0.22)
        head = label(r"from methods to mastery", font_size=26, color=GREY_A).to_edge(UP, buff=0.5)
        steps = VGroup(*[VGroup(RoundedRectangle(width=2.9, height=0.9, corner_radius=0.12, stroke_color=c_,
                                                 stroke_width=2.0), label(t_, font_size=18, color=c_))
                         for t_, c_ in ((r"micro", DATA), (r"macro", EST), (r"econometrics", MODEL),
                                        (r"how graders read", GAIN))])
        for s_ in steps:
            s_[1].move_to(s_[0])
        steps.arrange(RIGHT, buff=0.3)
        VGroup(hc, steps, nxt).arrange(DOWN, buff=0.45).next_to(head, DOWN, buff=0.4)
        with self.voiceover(
            "Next time, the end of the graduate core. <bookmark mark='a'/> It is the night before the first-year "
            "examinations: twelve problems of the kind every doctoral programme sets, <bookmark mark='b'/> four "
            "each in micro, macro and econometrics, solved the way a grader wants to see them, <bookmark "
            "mark='c'/> with the mistakes that cost marks. Part fifty-six: the core exam."
        ) as vo:
            self.play(FadeIn(head))
            vo.wait_until("a")
            self.play(FadeIn(hc, shift=UP * 0.1))
            vo.wait_until("b")
            self.play(LaggedStart(*[FadeIn(s_) for s_ in steps], lag_ratio=0.4), run_time=2.0)
            vo.wait_until("c")
            self.play(FadeIn(nxt, shift=UP * 0.1))
        self.wait(9.5)

from __future__ import annotations

from videos.economics.econ56.common import *  # noqa: F403

PROBLEMS = [
    r"Question 1 again: \ for which values of $\alpha$ does the consumer buy exactly 20 units?",
    r"Question 3 with $n$ bidders: \ show that the best reserve is $\tfrac12$ for every $n$, \ and find the revenue "
    r"with and without it for $n = 3$.",
    r"Question 5 again, \ but the revenue pays for useless government spending instead of a rebate: \ what changes "
    r"in the steady state?",
    r"Question 9: \ suppose storms also keep shoppers at home. \ What does the Wald estimator estimate now?",
    r"Question 11 without unit N: \ compute the two-way fixed-effects coefficient, \ and explain its sign.",
    r"$\bigstar$ \ Question 8: \ what happens to $r^*$ as the variance of income shocks goes to zero? \ Why?",
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
        a = wrapped_label(r"Yes, \ if you can do four things without being told: \ say who chooses what, \ given "
                          r"what; \ find the condition that pins the answer down, \ whether a first-order condition, "
                          r"\ a Bellman equation, \ market clearing or a moment; \ solve it with a reason for every "
                          r"step; \ and check the answer against a special case, \ its units and its signs. \ The "
                          r"twelve questions used no more than that.", 11.6, 26, WHITE)
        a.next_to(q, DOWN, buff=0.5)
        papers = VGroup(*[RoundedRectangle(width=0.9, height=1.2, corner_radius=0.05, stroke_color=c_,
                                           stroke_width=2.5, fill_color=PAPER, fill_opacity=1)
                          for c_ in (MICRO, MACRO, METRICS)]).arrange(RIGHT, buff=0.3).next_to(a, DOWN, buff=0.5)
        ticks = VGroup(*[label(r"\checkmark", font_size=34, color=GAIN).move_to(p_) for p_ in papers])
        with self.voiceover(
            "So: can you do it with the book closed? <bookmark mark='a'/> Yes, if you can do four things without "
            "being told: say who chooses what, given what; find the condition that pins the answer down, whether "
            "it is a first-order condition, a Bellman equation, market clearing or a moment; solve it with a "
            "reason for every step; and check the answer against a special case, its units and its signs. The "
            "twelve questions needed nothing more, and nothing less."
        ) as vo:
            self.play(FadeIn(q, shift=UP * 0.2))
            vo.wait_until("a")
            self.play(FadeIn(a, shift=UP * 0.1), run_time=2)
            self.play(LaggedStart(*[FadeIn(p_) for p_ in papers], lag_ratio=0.3), run_time=1.5)
            self.play(LaggedStart(*[FadeIn(t_, scale=1.3) for t_ in ticks], lag_ratio=0.4), run_time=2.0)
        self.clear_scene()

    def recap(self):
        L = {k: load(k) for k in ("micro1", "micro2", "micro3", "micro4", "macro1", "macro2", "macro3", "macro4",
                                  "metrics1", "metrics2", "metrics3", "metrics4")}
        items = [
            (rf"a kink: \ check every segment; \ income effect on $x - \bar x$: \ "
             rf"$dx/dp_2 = {L['micro1']['total']:.0f}$", MICRO),
            (rf"an externality: \ tax the source at the marginal harm, \ {L['micro2']['tax']:.1f}", MICRO),
            (rf"a reserve: \ $\beta(r) = r$; \ revenue {L['micro3']['rev']:.3f}, \ no sale a quarter of the time",
             MICRO),
            (rf"screening: \ no distortion at the top; \ $q_L = {L['micro4']['q_l']:.1f}$", MICRO),
            (rf"a capital tax: \ $c$ jumps up, \ $k$ falls to {L['macro1']['k_new']:.2f}", MACRO),
            (rf"expiring benefits: \ solve exhaustion first; \ $w^*$ falls to {L['macro2']['res'][0]:.3f}", MACRO),
            (rf"discretion: \ a bias of {L['macro3']['pi_bar']:.1f} point that buys almost no output", MACRO),
            (rf"precaution: \ $r^* = {100 * L['macro4']['r']:.2f}\% < \rho = {100 * L['macro4']['rho']:.2f}\%$",
             MACRO),
            (rf"demand: \ storms trace it out; \ Wald ${say_tex(L['metrics1']['wald'])}$, \ OLS "
             rf"${say_tex(L['metrics1']['ols'])}$", METRICS),
            (rf"GMM: \ {L['metrics2']['m']} moments, \ 2 parameters, \ $J$ on {L['metrics2']['df']} degrees of "
             r"freedom", METRICS),
            (rf"staggered timing: \ TWFE {L['metrics3']['twfe']:.1f} against an effect of "
             rf"{L['metrics3']['att']:.2f}", METRICS),
            (r"the long run: \ one zero in $C(1)B$, \ and a Cholesky factor", METRICS),
        ]
        rows = VGroup(*[label(rf"{n + 1}.\ \ {txt}", font_size=27, color=col) for n, (txt, col) in enumerate(items)])
        rows.arrange(DOWN, aligned_edge=LEFT, buff=0.2)
        head = label(r"Part 56, \ in twelve lines", font_size=42).to_edge(UP, buff=0.3)
        if rows.width > 13.2:
            rows.width = 13.2
        room = head.get_bottom()[1] - 0.35 + 3.75
        if rows.height > room:
            rows.scale_to_fit_height(room)
        rows.next_to(head, DOWN, buff=0.35)
        with self.voiceover(
            "Part fifty-six in twelve lines. <bookmark mark='r1'/> A kinked budget: check every segment, and put "
            "the income effect only on the units bought at the margin. <bookmark mark='r2'/> An externality: tax "
            "the source at the marginal harm. <bookmark mark='r3'/> An auction with a reserve: the type at the "
            "reserve bids the reserve, and sometimes nothing sells. <bookmark mark='r4'/> Screening: no distortion "
            "at the top. <bookmark mark='r5'/> A capital tax: consumption jumps, capital falls. <bookmark "
            "mark='r6'/> Benefits that run out: solve the end first. <bookmark mark='r7'/> Discretion: a bias "
            "that buys nothing. <bookmark mark='r8'/> Precaution: the interest rate sits below the rate of time "
            "preference. <bookmark mark='r9'/> Demand: a supply shifter traces it out. <bookmark mark='r10'/> "
            "GMM: count the moments, weight them, test the spares. <bookmark mark='r11'/> Staggered timing: "
            "compare only with the untreated. <bookmark mark='r12'/> And the long run: one zero, and a Cholesky "
            "factor."
        ) as vo:
            self.play(FadeIn(head))
            for i, r_ in enumerate(rows):
                vo.wait_until(f"r{i + 1}")
                self.play(FadeIn(r_, shift=RIGHT * 0.15), run_time=0.8)
            self.play(Indicate(rows, color=WHITE, scale_factor=1.0), run_time=2.0)
        self.clear_scene()

    def problems(self):
        ps = problem_set(PROBLEMS, font_size=21, width=13.0)
        with self.voiceover(
            "The problems: variations on tonight's questions. The range of tastes that lands at the kink; the "
            "reserve with any number of bidders; the capital tax when the revenue is wasted; storms that also "
            "keep shoppers at home; the staggered design without its never-treated unit; and a starred problem "
            "on what happens to the interest rate as income risk disappears. Full solutions are in the part's "
            "notes."
        ):
            self.play(FadeIn(ps.head), FadeIn(ps.rows[0], shift=UP * 0.1), run_time=0.8)
            self.play(LaggedStart(*[FadeIn(r) for r in ps.rows[1:]], lag_ratio=0.4), run_time=6)
        self.wait(4)
        self.clear_scene()

    def references(self):
        rc = reference_card(
            [r"Andreu Mas-Colell, \ Michael Whinston and Jerry Green, \emph{Microeconomic Theory} (1995)",
             r"David Kreps, \emph{A Course in Microeconomic Theory} (1990)",
             r"Lars Ljungqvist and Thomas Sargent, \emph{Recursive Macroeconomic Theory} (2000; \ 4th ed. 2018)",
             r"David Romer, \emph{Advanced Macroeconomics} (1996; \ 5th ed. 2019)",
             r"Jordi Gal\'i, \emph{Monetary Policy, Inflation, and the Business Cycle} (2008; \ 2nd ed. 2015)",
             r"Fumio Hayashi, \emph{Econometrics} (2000)"],
            [r"Mussa and Rosen (1978); \ Myerson (1981); \ Riley and Samuelson (1981); \ Hansen (1982)",
             r"Burtless and Hausman (1978); \ Chamley (1986); \ Blanchard and Quah (1989); \ Katz and Meyer (1990)",
             r"Aiyagari (1994); \ Clarida, \ Gal\'i and Gertler (1999); \ Chamberlain and Wilson (2000)",
             r"Card, \ Chetty and Weber (2007); \ Goodman-Bacon (2021); \ Callaway and Sant'Anna (2021); \ "
             r"Borusyak, \ Jaravel and Spiess (2024)"])
        with self.voiceover(
            "The reading: the core's textbooks. Mas-Colell, Whinston and Green, and Kreps, for micro; Ljungqvist "
            "and Sargent, Romer, and Galí for macro; Hayashi for econometrics. Then the papers behind each "
            "question. And the best preparation of all: past examinations, which many departments publish, worked "
            "against the clock."
        ):
            self.play(FadeIn(rc))
        self.wait(1.5)
        self.clear_scene()

    def next_part(self):
        hc = history_card(1966, r"Paul Samuelson, \ in \emph{Newsweek}",
                          r"`Wall Street indexes predicted nine out of the last five recessions'", color=E.ACCENT,
                          width=10.4, font_size=23)
        nxt = VGroup(label(r"Next: \ Part 57 \ $\cdot$ \ Act XI, \ Economics at Work", font_size=30, color=GREY_B),
                     label(r"Reading the Economy in Real Time", font_size=46),
                     label(r"what is the economy doing right now?", font_size=24, color=E.ACCENT)).arrange(DOWN,
                                                                                                         buff=0.22)
        head = label(r"from the exam room to the job", font_size=26, color=GREY_A).to_edge(UP, buff=0.5)
        steps_ = VGroup(*[VGroup(RoundedRectangle(width=2.9, height=0.9, corner_radius=0.12, stroke_color=c_,
                                                  stroke_width=2.0), label(t_, font_size=18, color=c_))
                          for t_, c_ in ((r"how a number is made", MICRO), (r"nowcasting", MACRO),
                                         (r"scoring forecasts", METRICS), (r"new data", GAIN))])
        for s_ in steps_:
            s_[1].move_to(s_[0])
        steps_.arrange(RIGHT, buff=0.3)
        VGroup(hc, steps_, nxt).arrange(DOWN, buff=0.45).next_to(head, DOWN, buff=0.4)
        with self.voiceover(
            "Next time, the graduate core is behind us, and economics goes to work. <bookmark mark='a'/> In 1966 "
            "Paul Samuelson joked that the stock market had predicted nine of the last five recessions. "
            "<bookmark mark='b'/> Economists, it turns out, err the other way. How are the numbers made, how do "
            "forecasters read them as they arrive, and how good are their guesses? <bookmark mark='c'/> Part "
            "fifty-seven: reading the economy in real time."
        ) as vo:
            self.play(FadeIn(head))
            vo.wait_until("a")
            self.play(FadeIn(hc, shift=UP * 0.1))
            vo.wait_until("b")
            self.play(LaggedStart(*[FadeIn(s_) for s_ in steps_], lag_ratio=0.4), run_time=2.0)
            vo.wait_until("c")
            self.play(FadeIn(nxt, shift=UP * 0.1))
        self.wait(9.5)

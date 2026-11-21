from __future__ import annotations

from videos.economics.econ50.common import *  # noqa: F403

PROBLEMS = [
    r"The credits: \ a single parent of two, \ one under six, \ with no other income. \ Find the old credit and the "
    r"allowance at earnings of 0, \ 10,000 and 30,000 \ (the old credit: \ 2,000 a child, \ refundable up to 1,400 a "
    r"child at 15\% of earnings above 2,500; \ tax 10\% above 18,800), \ and the gain at each.",
    r"The reward for work: \ at 20,000 the parent pays 120 in tax and receives 5,879 of EITC. \ Find what working "
    r"adds under each system, \ the percentage fall, \ and the fall in the share working if the participation "
    r"elasticity is 0.44 and 85\% worked.",
    r"Deep poverty: \ the line for three is $24{,}000\sqrt{3/4}$. \ Show that the parent working at 15,000 is above "
    r"it under the old credit, \ and that stopping work under the allowance leaves the family below half of it.",
    r"The MVPF: \ families would pay 108.9 million; \ the net cost is 109.2 million. \ Find the MVPF if children "
    r"later repay nothing, \ a quarter or half of 108.9 million, \ and divide each by a cost of funds of 1.33.",
    r"The cost of funds: \ show that a dollar of net revenue from a top rate $\tau$ costs top earners "
    r"$(1-\tau)/(1-\tau-\tau a e)$. \ With $\tau = 0.4$ and $a = 1.5$, \ find it for $e = 0.25$, \ and the $e$ at "
    r"which it is 2.",
    r"The second design: \ the old credit plus 1,600 for the young child and 1,000 for the older, \ unconditional. "
    r"\ For the parent of problem 2, \ find the payment at 0 and at 20,000, \ and what working adds.",
    r"The tornado: \ poverty ranges 10.1--13.5 for the elasticity, \ 11.6--12.5 for the income effect, \ "
    r"11.6--12.3 for take-up. \ Which study would you fund first, \ and what would it have to find to change the "
    r"advice?",
    r"$\bigstar$ \ The envelope theorem: \ a parent chooses work $h \in \{0, 1\}$ to maximize $u(y(h) + T) - "
    r"\theta h$. \ Show that the value of a small allowance $dT$ is $u'\,dT$ whether or not the parent switches, "
    r"\ so that what families would pay equals the payment at unchanged behaviour.",
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
        a = wrapped_label(r"The decision first, \ every number with its range, \ the evidence with its limits, \ "
                          r"the judgment named as the minister's. \ Here: \ about a fifth fewer poor children for "
                          r"about 1,500 dollars a child, \ few parents leaving work unless they respond far more than "
                          r"they have so far, \ and a case that rests on what the children repay later and on the "
                          r"weight given to their incomes.".replace("1,500", "1{,}500"), 11.6, 25, WHITE)
        a.next_to(q, DOWN, buff=0.5)
        F = load("film")
        mini = plane([1989, 2024], [0, 1], x_length=4.2, y_length=1.3)
        v = np.array(F["v"])
        v = (v - v.min()) / (v.max() - v.min())
        logo = path(mini, F["t"], v, POOR, 2.4, smooth=False).next_to(a, DOWN, buff=0.35)
        with self.voiceover(
            "So: a minister asks whether to pay a child allowance. What do you write? <bookmark mark='a'/> The "
            "decision first. Every number with its range. The evidence with its limits, and the judgment named as "
            "the minister's own. Here: about a fifth fewer poor children on the Island, for about fifteen hundred "
            "dollars a child a year; few parents leaving work, unless they respond far more than the evidence so "
            "far suggests; a second design that gives up a little of the poverty reduction to keep the reward for "
            "work and save a quarter of the cost; and a case that rests, in the end, on what the children repay "
            "later and on how much a society chooses to value their incomes."
        ) as vo:
            self.play(FadeIn(q, shift=UP * 0.2))
            vo.wait_until("a")
            self.play(FadeIn(a, shift=UP * 0.1), run_time=2)
            self.play(Create(logo), run_time=16.0, rate_func=linear)
            self.play(Indicate(a, color=E.ACCENT, scale_factor=1.0), run_time=2.0)
        self.clear_scene()

    def recap(self):
        I, S, Fn, B, O, Ec = (load(x) for x in ("island", "schedules", "fan", "budget", "options", "economy"))
        T = tables.CTC_2021.data
        A = tables.ALLOWANCE_50.data
        F50 = tables.FRONTIER50.data
        items = [
            (rf"2021: \ monthly payments for six months; \ child poverty (SPM) {T['spm_2020']} $\to$ "
             rf"{T['spm_2021']} $\to$ {T['spm_2022']}\%", SPM),
            (r"the question: \ the policy, \ the people, \ the outcomes, \ the comparison, \ the horizon", GREY_A),
            (rf"one family: \ +\${S['at0_new']:,.0f} at no earnings; \ the reward for work "
             rf"{100 * (S['gain_work_new_20k'] / S['gain_work_old_20k'] - 1):.0f}\% at 20k".replace(",", "{,}")
             .replace("-", "{-}"), CHILD),
            (r"the dials: \ participation 0.25 \ (0--0.5); \ the elasticity of taxable income; \ the MVPF", WORK),
            (r"the margins: \ take-up misses the poorest; \ monthly timing; \ labels and conditions", HOLD),
            (rf"the budget: \ \${I['per_child']:,.0f} a child, \ about {100 * Ec['share_gdp']:.2f}\% of GDP "
             rf"scaled; \ a surtax costs {Ec['mcpf'][0]:.2f}--{Ec['mcpf'][2]:.2f} a dollar".replace(",", "{,}"),
             BUDGET),
            (rf"the evidence: \ no fall in work in 2021 or Canada; \ a model says {A['exit_share']}\%; \ the long "
             r"run is old", EVIDENCE),
            (rf"the Island: \ {100 * I['old']['child_poverty']:.1f}\% $\to$ {100 * I['new']['child_poverty']:.1f}\% "
             rf"\ (static {100 * I['static_child_poverty']:.1f}\%); \ deep poverty rises above "
             rf"{Fn['deep_cross']:.2f}", NEW),
            (rf"the value: \ {B['rows'][0]['mvpf']:.2f} per dollar, \ {B['rows'][6]['mvpf']:.2f} if half is "
             r"repaid; \ below one with a surtax and nothing repaid", BUDGET),
            (rf"who gains: \ the poorest tenth +\${load('deciles')['mean_gain'][0]:,.0f}; \ the judgment is the "
             r"minister's".replace(",", "{,}"), CHILD),
            (rf"the second design: \ {100 * O['hybrid'][0]['poverty']:.1f}\% poor, \ a quarter cheaper, \ safe if "
             r"parents respond more", WORK),
            (rf"the frontier: \ no gains by age four in a trial of {F50['mothers']:,} mothers; \ the long run "
             r"unknown".replace(",", "{,}"), HOLD),
        ]
        rows = VGroup(*[label(rf"{n + 1}.\ \ {txt}", font_size=28, color=col) for n, (txt, col) in enumerate(items)])
        rows.arrange(DOWN, aligned_edge=LEFT, buff=0.2)
        head = label(r"Part 50, \ in twelve lines", font_size=42).to_edge(UP, buff=0.3)
        if rows.width > 13.2:
            rows.width = 13.2
        room = head.get_bottom()[1] - 0.35 + 3.75
        if rows.height > room:
            rows.scale_to_fit_height(room)
        rows.next_to(head, DOWN, buff=0.35)
        with self.voiceover(
            "Part fifty in twelve lines. <bookmark mark='r1'/> In 2021 America paid most families a monthly sum "
            "for each child, and child poverty on the measure that counts credits fell to a record low, then rose "
            "when the payments stopped. <bookmark mark='r2'/> A question becomes answerable when it names the "
            "policy, the people, the outcomes, the comparison and the horizon. <bookmark mark='r3'/> For one "
            "family the allowance adds most at the bottom, and cuts the reward for starting work by about a tenth. "
            "<bookmark mark='r4'/> Three dials matter most: participation, the elasticity of taxable income, and "
            "the value of public funds. <bookmark mark='r5'/> Take-up, timing and labels move the answer too. "
            "<bookmark mark='r6'/> The cost is about fifteen hundred dollars a child, and raising it from top "
            "incomes costs more than a dollar a dollar. <bookmark mark='r7'/> The evidence finds no fall in work, "
            "but only for a temporary payment or another country. <bookmark mark='r8'/> On the Island child "
            "poverty falls by about a fifth, and deep poverty rises if parents respond strongly. <bookmark "
            "mark='r9'/> A dollar delivers about a dollar of value, more if children repay later. <bookmark "
            "mark='r10'/> The poorest gain most, and the weight on their gain is a judgment. <bookmark mark='r11'/> "
            "A second design trades a little poverty reduction for safety and a lower cost. <bookmark mark='r12'/> "
            "And the long run is still unknown."
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
            "The problems. The credits at three levels of earnings; the reward for work and the share who stop; "
            "deep poverty by hand; the MVPF and the cost of funds; the second design; reading a tornado chart; and "
            "a starred problem on why what families would pay equals the payment itself. Full solutions are in "
            "the part's notes."
        ):
            self.play(FadeIn(ps.head), FadeIn(ps.rows[0], shift=UP * 0.1), run_time=0.8)
            self.play(LaggedStart(*[FadeIn(r) for r in ps.rows[1:]], lag_ratio=0.4), run_time=6)
        self.wait(4)
        self.clear_scene()

    def references(self):
        rc = reference_card(
            [r"Jonathan Gruber, \emph{Public Finance and Public Policy}, \ the chapters on cost-benefit analysis and "
             r"on welfare programmes",
             r"Anthony Boardman, David Greenberg, Aidan Vining and David Weimer, \emph{Cost-Benefit Analysis: "
             r"Concepts and Practice}",
             r"Joshua Angrist and J\"orn-Steffen Pischke, \emph{Mastering 'Metrics} (2015)",
             r"Eugene Bardach and Eric Patashnik, \emph{A Practical Guide for Policy Analysis}"],
            [r"Orcutt (1957); \ Saez (2001); \ Chetty, Guren, Manoli and Weber (2011); \ Milligan (2005)",
             r"Milligan and Stabile (2011); \ Aizer, Eli, Ferrie and Lleras-Muney (2016)",
             r"Hendren and Sprung-Keyser (2020); \ Corinth, Meyer, Stadnicki and Wu (2021)",
             r"Ananat, Glasner, Hamilton and Parolin (2022); \ Baker, Messacar and Stabile (2023)",
             r"Noble, Magnuson, Duncan, Gennetian et al. (2025); \ Egger et al. (2022)"])
        with self.voiceover(
            "The reading: Gruber's public finance textbook for cost-benefit analysis and welfare programmes; "
            "Boardman and his co-authors on cost-benefit practice; Angrist and Pischke's Mastering Metrics for the "
            "designs; and Bardach and Patashnik's practical guide to writing policy analysis. Then the papers this "
            "memo rests on."
        ):
            self.play(FadeIn(rc))
        self.wait(1.5)
        self.clear_scene()

    def next_part(self):
        hc = history_card(r"the 1950s", r"Richard Bellman at RAND", r"names his method for multistage decisions "
                          r"`dynamic programming': \ a name, \ he later wrote, \ that no one could object to",
                          color=E.ACCENT, width=10.4, font_size=24)
        nxt = VGroup(label(r"Next: \ Part 51 \ $\cdot$ \ Act X, \ The Graduate Core", font_size=30, color=GREY_B),
                     label(r"Computing Economies", font_size=46),
                     label(r"how is an economy with no formula solved, \ and how do you know the answer is right?",
                           font_size=24, color=E.ACCENT)).arrange(DOWN, buff=0.22)
        head = label(r"from the memo \ to the graduate toolkit", font_size=26, color=GREY_A).to_edge(UP, buff=0.5)
        steps = VGroup(*[VGroup(RoundedRectangle(width=2.9, height=0.9, corner_radius=0.12, stroke_color=c_,
                                                 stroke_width=2.0), label(t_, font_size=18, color=c_))
                         for t_, c_ in ((r"the Bellman equation", THEORY), (r"value iteration", NEW),
                                        (r"endogenous grids", CHILD), (r"accuracy checks", E.ACCENT))])
        for s_ in steps:
            s_[1].move_to(s_[0])
        steps.arrange(RIGHT, buff=0.3)
        VGroup(hc, steps, nxt).arrange(DOWN, buff=0.45).next_to(head, DOWN, buff=0.4)
        with self.voiceover(
            "That completes Act nine, the fields, and the course's first capstone. Next comes the graduate core. "
            "<bookmark mark='a'/> In the early 1950s at RAND, Richard Bellman needed a name for his work on "
            "decisions made in stages, a name, he later wrote, that not even a hostile official could object to. "
            "He chose dynamic programming. <bookmark mark='b'/> Part fifty-one solves economies that have no "
            "formula: the Bellman equation, value and policy iteration, endogenous grids, <bookmark mark='c'/> "
            "and the checks that tell you whether a computed answer is right."
        ) as vo:
            self.play(FadeIn(head))
            vo.wait_until("a")
            self.play(FadeIn(hc, shift=UP * 0.1))
            vo.wait_until("b")
            self.play(LaggedStart(*[FadeIn(s_) for s_ in steps], lag_ratio=0.4), run_time=2.0)
            vo.wait_until("c")
            self.play(FadeIn(nxt, shift=UP * 0.1))
        self.wait(9.5)

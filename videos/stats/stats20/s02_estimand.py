from __future__ import annotations

from videos.stats.stats20.common import *  # noqa: F403


def doc_card(title, lines, color, width=9.6, font_size=21):
    """A plain 'document': a titled sheet with numbered lines."""
    head = label(title, font_size=font_size + 6, color=color)
    rows = VGroup(*[label(rf"{i + 1}.\ \ {t}", font_size=font_size) for i, t in enumerate(lines)])
    for r in rows:
        if r.width > width - 0.6:
            r.width = width - 0.6
    rows.arrange(DOWN, aligned_edge=LEFT, buff=0.22)
    body = VGroup(head, rows).arrange(DOWN, aligned_edge=LEFT, buff=0.35)
    sheet = RoundedRectangle(width=width, height=body.height + 0.7, corner_radius=0.12, stroke_color=color, stroke_width=2,
                             fill_color="#11161d", fill_opacity=1)
    body.move_to(sheet)
    return VGroup(sheet, body)


class Estimand(VoiceoverScene):
    def construct(self):
        self.card()
        self.five_parts()
        self.two_questions()
        self.usual()
        self.plan()
        self.why_plan()

    def card(self):
        card = chapter_card(1, r"From question to estimand", r"What, exactly, for whom?", part=PART)
        with self.voiceover("Chapter one. From a question to an estimand."):
            self.play(FadeIn(card[0], shift=UP * 0.2), FadeIn(card[1]))
        self.play(FadeOut(card))

    def five_parts(self):
        d = load("design")
        rows = [
            cmath(r"\text{population}", r":", rf"\text{{US adults 20+, \ living at home, \ 2017--18: \ {d['pop'] / 1e6:.0f} million}}", font_size=26),
            cmath(r"\text{outcome}", r":", r"\text{systolic pressure, \ mm Hg}", font_size=28),
            cmath(r"\text{exposure}", r":", r"\text{usual sodium intake, \ g per day}", font_size=28),
            cmath(r"\text{contrast}", r":", r"\text{mean pressure, \ per 1 g/day more}", font_size=28),
            cmath(r"\text{holding fixed}", r":", r"\text{age, \ sex, \ BMI, \ energy intake}", font_size=28),
        ]
        rows[2][2].set_color(SALT)
        rows[1][2].set_color(BP)
        whys = [why(r"civilian, \ not in institutions: \ the sampling frame"), why(r"the average of readings 2 and 3"),
                why(r"not yesterday's: \ chapter eight"), why(r"a slope, \ not a single person's response"),
                why(r"so that like is compared with like")]
        intro = label('Define the target before choosing the estimator', font_size=36)
        if intro.width > 12.5:
            intro.width = 12.5
        with self.voiceover(
            "A question in words isn't yet something a computer can estimate. An estimand pins it down, in five parts. "
            "<bookmark mark='a'/> The population: American adults aged twenty and over, living at home rather than in prisons, "
            "nursing homes or the military, in 2017 and 2018. That's about two hundred and thirty-six million people, and it's "
            "what NHANES samples. <bookmark mark='b'/> The outcome: systolic blood pressure, the higher of the two numbers. "
            "<bookmark mark='c'/> The exposure: usual daily sodium intake, the long-run average, which is what could plausibly "
            "affect blood pressure. <bookmark mark='d'/> The contrast: how much higher mean pressure is per extra gram a day. "
            "<bookmark mark='e'/> And what is held fixed: age, sex, body mass index and total energy intake, so that people "
            "are compared with others like them."
        ) as vo:
            self.play(FadeIn(intro))
            step = ladder(self, rows, whys, keep=5, top=2.8, x=-0.8, buff=0.62, edge=6.9)
            for k, m_ in enumerate("abcde"):
                vo.wait_until(m_)
                step(k, transform=False)
                if k == 0:
                    self.play(FadeOut(intro), run_time=0.25)
        self.clear_scene()

    def two_questions(self):
        left = VGroup(label(r"descriptive", font_size=30, color=DES),
                      label(r"among adults alike in age, \ sex, \ BMI and energy,", font_size=22),
                      label(r"how much higher is mean pressure", font_size=22),
                      label(r"in those who eat a gram more?", font_size=22),
                      label(r"a survey can estimate this", font_size=22, color=HIT)).arrange(DOWN, buff=0.22)
        right = VGroup(label(r"causal", font_size=30, color=TRUE),
                       label(r"if every adult ate a gram less,", font_size=22),
                       label(r"how much would mean pressure fall?", font_size=22),
                       label(r"what the guideline needs", font_size=22, color=GREY_A),
                       label(r"needs more than a survey: \ chapter nine", font_size=22, color=RES)).arrange(DOWN, buff=0.22)
        VGroup(left, right).arrange(RIGHT, buff=1.2).move_to([0, 0.2, 0])
        line = Line([0, 2.2, 0], [0, -1.6, 0], color=GREY_D)
        foot = label(r"same words, \ ``depends on'', \ two different estimands", font_size=24, color=OBS).to_edge(DOWN, buff=0.6)
        with self.voiceover(
            "The phrase depends on hides two different questions. <bookmark mark='a'/> The descriptive one: among "
            "adults alike in age, sex, size and energy intake, how much higher is mean blood pressure in those who "
            "eat a gram more sodium? That's a fact about the population as it is, and a good survey can estimate it. "
            "<bookmark mark='b'/> The causal one: if every adult ate a gram less, how much would mean pressure fall? "
            "That's what a guideline needs, and it's a question about a world that hasn't happened. <bookmark "
            "mark='c'/> A descriptive slope becomes causal only with adequate confounding control, a well-defined "
            "intervention and a suitable model. We'll estimate the first, and argue about the second in chapter nine."
        ) as vo:
            vo.wait_until("a")
            self.play(FadeIn(left, shift=RIGHT * 0.2), Create(line))
            vo.wait_until("b")
            self.play(FadeIn(right, shift=LEFT * 0.2))
            vo.wait_until("c")
            self.play(FadeIn(foot))
        self.clear_scene()

    def usual(self):
        d = load("meas")
        rows = [
            cmath(r"\text{the estimand}", r":", r"\text{usual intake, \ a long-run average}", font_size=28),
            cmath(r"\text{the data}", r":", r"\text{yesterday's intake, \ from memory}", font_size=28),
            cmath(r"\text{two days, \ same people}", r":", rf"r = {d['reliability']:.2f}", font_size=30),
            cmath(r"\text{so}", r":", r"\text{a noisy measurement of the exposure}", font_size=28),
        ]
        rows[3][2].set_color(RES)
        whys = [why(r"what a body responds to"), why(r"a 24-hour recall interview"),
                why(rf"{d['n2']:,} adults with two reliable recalls"), why(r"Part 12's errors in $x$: \ the slope shrinks")]
        intro = label('Usual intake and a recalled day are different exposures', font_size=36)
        if intro.width > 12.5:
            intro.width = 12.5
        with self.voiceover(
            "Notice a gap already. <bookmark mark='a'/> The estimand is about usual intake, a long-run average. "
            "<bookmark mark='b'/> The data record one day, yesterday, reconstructed from memory in an interview. "
            "<bookmark mark='c'/> People eat very differently from day to day: for the two thousand six hundred and "
            "fifty-nine adults with two reliable recalls, the correlation between their first and second day is only "
            "point three two. <bookmark mark='d'/> So the exposure is measured with a great deal of noise, and Part "
            "12 taught us what noise in x does to a slope: under a classical additive-error model it attenuates the "
            "slope; correlated recall errors and noisy covariates can behave differently. Write that down now; "
            "chapter eight measures how much."
        ) as vo:
            self.play(FadeIn(intro))
            step = ladder(self, rows, whys, keep=4, top=2.6, x=-0.6, buff=0.72, edge=6.9)
            for k, m_ in enumerate("abcd"):
                vo.wait_until(m_)
                step(k, transform=False)
                if k == 0:
                    self.play(FadeOut(intro), run_time=0.25)
        self.clear_scene()

    def plan(self):
        card = doc_card(r"Illustrative analysis plan, \ presented before the results", [
            r"sample: \ adults 20+, \ not pregnant, \ not taking blood-pressure medicine",
            r"outcome: \ mean of systolic readings 2 and 3 (the first if only one)",
            r"exposure: \ day-1 sodium, \ g; \ reliable recalls; \ energy 500--5,000 kcal",
            r"model: \ weighted least squares on sodium, \ age, \ sex, \ BMI, \ energy",
            r"weights: \ the day-1 dietary weights; \ SEs: \ design-based, \ $t$ with 15 df",
            r"secondary: \ medicine users in, \ splines, \ two-day means, \ unweighted",
            r"reported whatever it shows; \ deviations from the plan flagged as such",
        ], SALT, width=11.4, font_size=21).move_to([0, 0, 0])
        with self.voiceover(
            "<bookmark mark='a'/> Before fitting anything, we write down the plan. The sample: adults over twenty, "
            "not pregnant, and not taking blood-pressure medicine, because treatment changes pressure; this exclusion"
            " also changes the target population and can introduce selection bias. The outcome: the mean of the "
            "second and third readings. The exposure: sodium on the first recall day, for reliable recalls with "
            "plausible energy totals. The model: weighted least squares on sodium, age, sex, BMI and energy. The "
            "weights and standard errors follow the survey's design. Secondary analyses are listed in advance. "
            "<bookmark mark='b'/> And the last line matters most: the primary result is reported whatever it shows, "
            "and anything we change later is labelled as a change."
        ) as vo:
            vo.wait_until("a")
            self.play(FadeIn(card[0]), FadeIn(card[1][0]),
                      LaggedStart(*[FadeIn(r, shift=RIGHT * 0.15) for r in card[1][1][:6]], lag_ratio=0.5), run_time=12.0)
            vo.wait_until("b")
            self.play(FadeIn(card[1][1][6], shift=RIGHT * 0.15), Indicate(card[1][1][6], color=OBS))
        self.wait(1.0)
        self.clear_scene()

    def why_plan(self):
        d = load("spec")
        rows = fit_rows(VGroup(
            label(r"each line of the plan is a fork in the garden of paths (Part 10)", font_size=24),
            label(rf"six reasonable binary choices: \ $2^6 = {len(d['runs'])}$ analyses", font_size=24, color=OBS),
            label(r"selection after seeing results can inflate false positives", font_size=24, color=RES),
            label(r"choose first, \ then show all 64: \ chapter eight", font_size=24, color=HIT),
            label(r"many trial journals require prospective registration; \ surveys can register too", font_size=22, color=GREY_A),
        ), 12.4, 0.5, [0, 0, 0])
        with self.voiceover(
            "<bookmark mark='a'/> Why so formal? Because each line is a fork in Part 10's garden of paths. <bookmark "
            "mark='b'/> Medicine users in or out, energy in the model or not, weights or not, a spline for age, which"
            " readings, one recall day or two: six reasonable choices, sixty-four analyses. <bookmark mark='c'/> "
            "Choosing after seeing results can inflate false positives, even without deliberate cherry-picking. It "
            "does not guarantee that these sixty-four choices can produce any desired answer. <bookmark mark='d'/> So"
            " we choose first, and in chapter eight we'll show all sixty-four anyway. <bookmark mark='e'/> "
            "Prospective registration is required by many trial journals and regulators, with rules depending on the "
            "trial. A survey analysis can also register its plan. Our displayed teaching plan is not evidence of "
            "registration."
        ) as vo:
            for k, m_ in enumerate("abcde"):
                vo.wait_until(m_)
                self.play(FadeIn(rows[k], shift=RIGHT * 0.2))
        self.clear_scene()

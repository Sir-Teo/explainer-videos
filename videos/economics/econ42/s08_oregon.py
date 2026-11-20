from __future__ import annotations

from videos.economics.econ42.common import *  # noqa: F403


class Oregon(VoiceoverScene):
    def construct(self):
        card(self, 7, r"Oregon's lottery", r"What did insurance do to health, to money and to peace of mind?",
             "Chapter seven. Oregon's lottery.", lit={2012: r"Finkelstein et al.", 2013: r"Baicker et al.",
                                                     2014: r"Taubman et al."},
             scale=("person", "household"), horizon=("a year",))
        self.design()
        self.results()
        self.power()
        self.value()

    def design(self):
        L = load("lottery")
        S = L["shown"]
        bars = VGroup()
        for k, (nm, v, col) in enumerate(((r"names drawn", S["cover_won"], LOTTO),
                                          (r"not drawn", S["cover_lost"], GREY_B))):
            x = -4.2 + 2.2 * k
            h = v * 5.0
            r = Rectangle(width=1.5, height=h, stroke_width=0, fill_color=col, fill_opacity=0.85).move_to(
                np.array([x, -2.5 + h / 2, 0]))
            bars.add(VGroup(r, label(nm, font_size=19, color=WHITE).next_to(r, DOWN, buff=0.15),
                            label(rf"{100 * v:.0f}\%", font_size=24, color=col).next_to(r, UP, buff=0.12)))
        head_b = label(r"insured, \ the Island's lottery", font_size=20, color=GREY_A).next_to(bars, UP, buff=0.8)
        eq = VGroup(
            MathTex(r"\text{effect of coverage} = \frac{\bar y_{\text{drawn}} - \bar y_{\text{not}}}"
                    r"{\bar d_{\text{drawn}} - \bar d_{\text{not}}}", font_size=34),
            label(rf"first stage: \ {100 * L['first_stage']:.0f} points \ (Oregon: \ about "
                  rf"{L['oregon']['first_stage']})", font_size=20, color=LOTTO),
            label(r"everyone drawn is compared with \\ everyone not drawn, \ insured or not", font_size=19,
                  color=GREY_A),
            label(r"so the comparison is fair, \\ and the gap is scaled up by \\ the first stage", font_size=19,
                  color=E.ACCENT),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.35).move_to(RIGHT * 2.6 + UP * 0.2)
        tag = island_tag(corner=DR, font_size=14)
        with self.voiceover(
            "How do you learn from a lottery when not every winner takes up the prize? Many people drawn never "
            "applied, or did not qualify, and some who were not drawn found coverage elsewhere. "
            "<bookmark mark='a'/> On the Island's version of Oregon, "
            f"{say_pct(S['cover_won'], 0)} of those drawn ended up insured, against {say_pct(S['cover_lost'], 0)} "
            "of the rest. <bookmark mark='b'/> The difference, about a quarter, is the first stage, close to "
            "Oregon's twenty-five points. <bookmark mark='c'/> The trick is to compare everyone drawn with everyone "
            "not drawn, whether or not they were insured, because only that comparison is guaranteed fair. "
            "<bookmark mark='d'/> Then divide the gap in outcomes by the gap in coverage. If insurance moves an "
            "outcome by some amount, a lottery that raises coverage by a quarter moves it by a quarter as much; "
            "dividing by the first stage scales it back up. This is the Wald estimator of Part four, an instrument "
            "made by chance."
        ) as vo:
            self.play(FadeIn(tag), FadeIn(head_b), *[FadeIn(b_[1]) for b_ in bars],
                      *[GrowFromEdge(b_[0], DOWN) for b_ in bars], run_time=1.5)
            vo.wait_until("a")
            self.play(*[FadeIn(b_[2]) for b_ in bars])
            vo.wait_until("b")
            self.play(FadeIn(eq[1]))
            vo.wait_until("c")
            self.play(FadeIn(eq[2]))
            vo.wait_until("d")
            self.play(Write(eq[0]), FadeIn(eq[3]))
        self.clear_scene()

    def results(self):
        O = tables.OREGON_2008.data
        cards = point_cards([
            (r"more care", rf"outpatient visits \\ $+${O['outpatient']}\%, \ prescriptions \\ $+${O['drugs']}\%; "
                           rf"\\ emergency visits \\ $+${O['ed_pct']}\%", HEALTH),
            (r"less financial strain", r"catastrophic medical \\ bills, \ above 30\% \\ of income: \\ virtually "
                                       r"eliminated", GAIN),
            (r"less depression", rf"{abs(O['depression']):.1f} points less, \\ from {O['depression_base']}\% \\ "
                                 rf"(95\%: \ {abs(O['depression_hi']):.1f} to \\ {abs(O['depression_lo']):.1f})",
             UNEMP),
            (r"blood pressure", r"no statistically \\ significant change \\ in two years, \ nor \\ in cholesterol \\ "
                                r"or blood sugar", HOLD),
        ], width=12.8, cols=4, font_size=19).move_to(DOWN * 0.1)
        head = label(r"what Oregon found", font_size=28, color=E.ACCENT).to_edge(UP, buff=0.6)
        tag = published_tag(tables.OREGON_2008.tag, corner=DR, font_size=10)
        with self.voiceover(
            "Here is what Oregon found, in papers led by Amy Finkelstein and Katherine Baicker. "
            "<bookmark mark='a'/> Insurance raised the use of care: outpatient visits by about thirty-five percent, "
            "prescriptions by about fifteen. Emergency visits rose too, by about forty percent, against the hope "
            "that coverage would move people from the emergency room to the doctor's office. "
            "<bookmark mark='b'/> It removed financial strain: medical bills above thirty percent of a household's "
            "income were virtually eliminated. <bookmark mark='c'/> It reduced depression, by about nine "
            "percentage points from thirty, a large effect. <bookmark mark='d'/> But in two years it produced no "
            "statistically significant change in measured blood pressure, cholesterol, or blood sugar."
        ) as vo:
            self.play(FadeIn(head), FadeIn(tag))
            for mk, c in zip("abcd", cards.cards):
                vo.wait_until(mk)
                self.play(FadeIn(c, shift=UP * 0.1))
        self.clear_scene()

    def power(self):
        L = load("lottery")
        Sy = L["summary"]["systolic"]
        Sd = L["summary"]["depression"]
        d = np.array(Sy["draws"])
        ax = plane([-6, 4], [0, 1], center=LEFT * 1.6 + DOWN * 0.2, x_length=8.6, y_length=3.8,
                   xticks=[-6, -4, -2, 0, 2, 4], yticks=[], xlabel=r"estimated effect on systolic blood pressure, "
                                                                   r"\ mmHg", xfmt=lambda v: f"{v:.0f}", font_size=14)
        rng = np.random.default_rng(1)
        ys = 0.08 + 0.84 * rng.random(len(d))
        sig = np.abs(d) > 1.96 * Sy["se"]
        dots_ = VGroup(*[dot(ax, float(x), float(y), LOSS if s else GREY_B, 0.045) for x, y, s in zip(d, ys, sig)])
        zero = vline(ax, 0, 0, 1, WHITE)
        truth = vline(ax, Sy["true"], 0, 1, GAIN)
        tl = label(rf"the truth: \ {Sy['true']:g}", font_size=16, color=GAIN).next_to(ax.ax.c2p(Sy["true"], 1.0),
                                                                                    UP, buff=0.08)
        side = VGroup(
            label(rf"{L['runs']} lotteries on \\ the Island, \ each \\ with 12,000 measured", font_size=17,
                  color=GREY_A),
            label(rf"red: \ significant: \\ only {100 * Sy['power']:.0f}\% of runs", font_size=18, color=LOSS),
            label(rf"smallest effect \\ reliably found: \\ about {Sy['mde']:.1f} mmHg", font_size=18,
                  color=E.ACCENT),
            label(rf"depression, \ same runs: \\ found {100 * Sd['power']:.0f}\% of the time", font_size=18,
                  color=UNEMP),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.32).to_edge(RIGHT, buff=0.35)
        tag = island_tag(corner=DR, font_size=14)
        with self.voiceover(
            "Does that mean insurance does nothing for blood pressure? Not necessarily, and the Island shows why. "
            "<bookmark mark='a'/> Plant a true effect of one point of blood pressure, run the lottery two hundred "
            "times with twelve thousand people measured each time, and estimate the effect each time. "
            "<bookmark mark='b'/> Because only a quarter of those drawn gained coverage, each estimate is noisy: "
            f"it is statistically significant in only {say_pct(Sy['power'], 0)} of the runs. "
            f"<bookmark mark='c'/> The smallest effect this design would reliably detect is about {Sy['mde']:.1f} "
            "points; anything smaller would usually go unseen. <bookmark mark='d'/> The same runs detect the "
            "planted effect on depression "
            f"{say_pct(Sd['power'], 0)} of the time. No detectable effect is not the same as no effect: the "
            "experiment could rule out large effects, not small ones."
        ) as vo:
            self.play(FadeIn(ax), FadeIn(tag), Create(zero), FadeIn(side[0]), run_time=1.0)
            vo.wait_until("a")
            self.play(Create(truth), FadeIn(tl))
            self.play(LaggedStart(*[FadeIn(x) for x in dots_], lag_ratio=0.01), run_time=4.0)
            vo.wait_until("b")
            self.play(FadeIn(side[1]))
            vo.wait_until("c")
            self.play(FadeIn(side[2]))
            vo.wait_until("d")
            self.play(FadeIn(side[3]))
        self.clear_scene()

    def value(self):
        M = tables.MVPF_2020.data
        cards = point_cards([
            (r"what recipients value", rf"\${M['medicaid_lo']} to \${M['medicaid_hi']} \\ per dollar of the \\ "
                                       r"cost of their care", UNEMP),
            (r"where the money goes", rf"about {100 * M['external']:.0f} cents of \\ each government dollar \\ "
                                      r"goes, \ in effect, \ to those \\ who paid for the \\ uninsured's care",
             HOLD),
            (r"who paid before", r"hospitals, \ other \\ patients and \\ taxpayers, \ through \\ unpaid bills", RISK),
            (r"so Medicaid", r"is also insurance \\ for those who \\ would have paid", GAIN),
        ], width=12.8, cols=4, font_size=19).move_to(DOWN * 0.1)
        head = label(r"what is Medicaid worth to those it covers?", font_size=28, color=E.ACCENT).to_edge(UP,
                                                                                                    buff=0.6)
        tag = published_tag(r"Finkelstein, \ Hendren and Luttmer, \ \emph{JPE} (2019)", corner=DR, font_size=11)
        with self.voiceover(
            "One more question: what is Medicaid worth to the people it covers? Amy Finkelstein, Nathaniel Hendren "
            "and Erzo Luttmer used Oregon's results to estimate it. <bookmark mark='a'/> Recipients would pay "
            "between fifty cents and a dollar twenty for each dollar their care costs. <bookmark mark='b'/> The "
            "reason it is not more is that the uninsured already received much of their care without paying for "
            "it, and about sixty cents of each government dollar is, in effect, a transfer to those who had been "
            "paying for that care. "
            "<bookmark mark='c'/> Before, hospitals, other patients and taxpayers bore that cost through unpaid "
            "bills. <bookmark mark='d'/> So Medicaid is partly insurance for them: a transfer to the people who "
            "would otherwise have paid. Who benefits from a programme is not always who receives it."
        ) as vo:
            self.play(FadeIn(head), FadeIn(tag))
            for mk, c in zip("abcd", cards.cards):
                vo.wait_until(mk)
                self.play(FadeIn(c, shift=UP * 0.1))
        self.clear_scene()

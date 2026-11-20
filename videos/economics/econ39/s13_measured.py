from __future__ import annotations

from videos.economics.econ39.common import *  # noqa: F403


class Measured(VoiceoverScene):
    def construct(self):
        card(self, 11, r"Discrimination measured", r"How can anyone see discrimination in the data?",
             "Chapter eleven. Discrimination measured.",
             lit={2000: r"Goldin and Rouse", 2004: r"Bertrand and Mullainathan", 2017: r"Quillian et al."},
             scale=("firm", "market"), horizon=("a year",))
        self.resumes()
        self.experiments()
        self.oaxaca()

    def resumes(self):
        R = load("resume")
        groups = [("Boston", R["boston"]), ("Chicago", R["chicago"]), ("women's names", R["female"]),
                  ("men's names", R["male"]), (r"higher-quality \\ r\'esum\'es", R["high"]),
                  (r"lower-quality \\ r\'esum\'es", R["low"])]
        bars = VGroup()
        for k, (nm, g) in enumerate(groups):
            x = -5.4 + 2.05 * k
            hw, hb = g["white"] * 28, g["black"] * 28
            bw = Rectangle(width=0.6, height=hw, stroke_width=0, fill_color=WHITE_N, fill_opacity=0.9).move_to(
                np.array([x - 0.33, -2.2 + hw / 2, 0]))
            bb = Rectangle(width=0.6, height=hb, stroke_width=0, fill_color=BLACK_N, fill_opacity=0.9).move_to(
                np.array([x + 0.33, -2.2 + hb / 2, 0]))
            bars.add(VGroup(bw, bb, label(f"{100 * g['white']:.1f}", font_size=15, color=WHITE_N).next_to(bw, UP,
                                                                                                    buff=0.06),
                            label(f"{100 * g['black']:.1f}", font_size=15, color=BLACK_N).next_to(bb, UP, buff=0.06),
                            label(nm, font_size=15, color=GREY_A).move_to(np.array([x, -2.65, 0]))))
        head = label(r"call-back rates, \ \%: \ White-sounding \ (gold) \ and African-American-sounding names "
                     r"\ (violet)", font_size=20, color=E.ACCENT).to_edge(UP, buff=0.45)
        gain_w = R["high"]["white"] - R["low"]["white"]
        gain_b = R["high"]["black"] - R["low"]["black"]
        foot = label(rf"a better r\'esum\'e adds {100 * gain_w:.1f} points for White names, \ "
                     rf"{100 * gain_b:.1f} for African-American names", font_size=19, color=WHITE).next_to(head, DOWN,
                                                                                                   buff=0.3)
        tag = data_tag(r"Bertrand and Mullainathan (2004), \ via openintro; \ recomputed", corner=DR, font_size=12)
        with self.voiceover(
            "Return to the résumés, the cleanest kind of evidence: the employer sees everything about the candidate "
            "except a randomly assigned name, so any difference in call-backs is caused by the name. "
            "<bookmark mark='a'/> The gap appears in both cities, <bookmark mark='b'/> for women's names and men's "
            "names alike. <bookmark mark='c'/> And the researchers made some résumés stronger than others: more "
            "experience, honours, skills. A better résumé raised call-backs by "
            f"{100 * gain_w:.1f} percentage points for White names, but only {100 * gain_b:.1f} for African-American "
            "names. Investing in a stronger résumé paid less for the group discriminated against, Arrow's mechanism "
            "in the data."
        ) as vo:
            self.play(FadeIn(head), FadeIn(tag), LaggedStart(*[FadeIn(b_, shift=UP * 0.1) for b_ in bars[:2]],
                                                             lag_ratio=0.3), run_time=1.5)
            vo.wait_until("a")
            self.play(Indicate(bars[0], color=WHITE), Indicate(bars[1], color=WHITE))
            vo.wait_until("b")
            self.play(LaggedStart(*[FadeIn(b_, shift=UP * 0.1) for b_ in bars[2:4]], lag_ratio=0.3))
            vo.wait_until("c")
            self.play(LaggedStart(*[FadeIn(b_, shift=UP * 0.1) for b_ in bars[4:]], lag_ratio=0.3), FadeIn(foot))
        self.clear_scene()

    def experiments(self):
        D = tables.DISCRIMINATION.data
        cards = point_cards([
            (r"audits", r"trained pairs of \\ applicants, \ matched \\ but for race or sex: \\ realistic, \ but the "
                        r"\\ actors know the aim", GREY_B),
            (r"correspondence", r"written applications \\ only: \ clean, \\ but only the first step", WHITE_N),
            (rf"{D['meta_studies']} studies since {D['meta_since']}",
             rf"White applicants: \ {D['meta_black']}\% more \\ call-backs than \\ African Americans; \\ "
             r"no change over time", BLACK_N),
            (r"blind auditions", r"orchestras that hid \\ the player behind a \\ screen advanced \\ and hired "
                                 r"more women", WOMEN),
        ], width=12.8, cols=4, font_size=18).move_to(DOWN * 0.1)
        head = label(r"field experiments", font_size=28, color=E.ACCENT).to_edge(UP, buff=0.6)
        foot = label(r"Goldin and Rouse: \ some estimates are imprecise, \ as they note", font_size=17,
                     color=GREY_A).to_edge(DOWN, buff=0.6)
        tag = published_tag(tables.DISCRIMINATION.tag, corner=DR, font_size=11)
        with self.voiceover(
            "There are two kinds of field experiment. <bookmark mark='a'/> In an audit study, trained pairs of "
            "applicants, alike except in race or sex, apply in person: realistic, but the actors know what is being "
            "tested. <bookmark mark='b'/> In a correspondence study, like the résumés, only paper is sent: cleaner, "
            "but it sees only the first step of hiring. <bookmark mark='c'/> In 2017 Lincoln Quillian, Devah Pager "
            f"and colleagues combined the American field experiments run since {D['meta_since']}: White applicants "
            f"received on average {D['meta_black']} percent more call-backs than African Americans, with no decline "
            "over twenty-five years. <bookmark mark='d'/> And when American orchestras began auditioning players "
            "behind a screen, Claudia Goldin and Cecilia Rouse found that women became more likely to advance and "
            "be hired, though, as they note, some of their estimates are imprecise."
        ) as vo:
            self.play(FadeIn(head), FadeIn(tag))
            for mk, c in zip("abcd", cards.cards):
                vo.wait_until(mk)
                self.play(FadeIn(c, shift=UP * 0.1))
            self.play(FadeIn(foot))
        self.clear_scene()

    def oaxaca(self):
        O = load("oaxaca")
        g78, g85 = O["78"], O["85"]
        eq = MathTex(r"\bar y_m - \bar y_f = \underbrace{(\bar x_m - \bar x_f)\hat\beta_f}_{\text{explained}} + "
                     r"\underbrace{\bar x_m(\hat\beta_m - \hat\beta_f)}_{\text{unexplained}}", font_size=32).to_edge(
            UP, buff=0.45)
        rows = VGroup()
        for k, (yr, g) in enumerate((("1978", g78), ("1985", g85))):
            y = 0.4 - 1.4 * k
            e, u = g["explained"], g["unexplained"]
            be = Rectangle(width=max(abs(e) * 12, 0.02), height=0.6, stroke_width=0, fill_color=GREY_B,
                           fill_opacity=0.9).move_to(np.array([-2.0 + e * 6, y, 0]))
            bu = Rectangle(width=u * 12, height=0.6, stroke_width=0, fill_color=WOMEN, fill_opacity=0.9).move_to(
                np.array([-2.0 + max(e, 0) * 12 + u * 6, y, 0]))
            rows.add(VGroup(label(yr, font_size=22, color=WHITE).next_to(np.array([-2.1, y, 0]), LEFT, buff=0.2), be,
                            bu, label(rf"gap {g['gap']:.2f}: \ explained {g['explained']:+.2f}, \ unexplained "
                                      rf"{g['unexplained']:.2f}", font_size=17, color=WHITE).next_to(np.array(
                                          [-2.0, y - 0.5, 0]), DOWN, buff=0.05, aligned_edge=LEFT)))
        side = VGroup(
            label(r"controls: \ schooling, \ experience, \\ union, \ race, \ marriage, \ region", font_size=16,
                  color=GREY_A),
            label(r"`unexplained' is not \\ `discrimination': \\ omitted skills and hours \\ inflate it; \ "
                  r"controls \\ shaped by discrimination \\ (occupation) shrink it", font_size=17, color=E.ACCENT),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.4).to_edge(RIGHT, buff=0.35).shift(DOWN * 0.4)
        tag = data_tag(r"Current Population Survey, \ 1978 and 1985, \ via Wooldridge's data", corner=DR,
                       font_size=12)
        with self.voiceover(
            "Most data are not experiments. The standard tool for them is the Oaxaca-Blinder decomposition, from "
            "1973: split a pay gap into a part explained by differences in measured characteristics and a part "
            "that remains. <bookmark mark='a'/> In a 1978 sample from the Current Population Survey, men's log "
            f"wages exceeded women's by {g78['gap']:.2f}; schooling, experience, union membership and the rest "
            f"explain only {g78['explained']:.2f} of it. <bookmark mark='b'/> By 1985 the gap was {g85['gap']:.2f}, "
            "and the measured characteristics explain none of it. <bookmark mark='c'/> But the unexplained part is "
            "not a measure of discrimination. It also contains everything not measured: actual rather than "
            "potential experience, hours, the field of study. And some controls, such as occupation, may themselves "
            "be shaped by discrimination, so adding them hides it. A decomposition describes; only a design like the "
            "résumés can say what causes what."
        ) as vo:
            self.play(Write(eq), FadeIn(tag), FadeIn(side[0]), run_time=1.5)
            vo.wait_until("a")
            self.play(FadeIn(rows[0], shift=RIGHT * 0.1))
            vo.wait_until("b")
            self.play(FadeIn(rows[1], shift=RIGHT * 0.1))
            vo.wait_until("c")
            self.play(FadeIn(side[1]))
        self.clear_scene()

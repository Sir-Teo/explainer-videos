from __future__ import annotations

from videos.economics.econ38.common import *  # noqa: F403


class Returns(VoiceoverScene):
    def construct(self):
        card(self, 10, r"The return to schooling",
             r"Does school make people earn more, \ or do earners stay in school?",
             "Chapter ten. The return to schooling.",
             lit={1991: r"Angrist and Krueger", 1995: r"Card", 2006: r"Oreopoulos"}, scale=("person",),
             horizon=("a decade",))
        self.ability()
        self.distance()
        self.designs()

    def ability(self):
        R = load("returns")
        rows = VGroup(
            label(r"the 1980 survey, \ 935 men", font_size=22, color=GREY_A),
            VGroup(label(r"least squares", font_size=22, color=SCHOOL),
                   label(f"{R['w2_ols']:.3f}", font_size=26, color=SCHOOL)).arrange(RIGHT, buff=0.6),
            VGroup(label(r"add IQ", font_size=22, color=ABILITY),
                   label(f"{R['w2_iq']:.3f}", font_size=26, color=ABILITY)).arrange(RIGHT, buff=0.6),
        ).arrange(DOWN, buff=0.45).move_to(LEFT * 3.4 + UP * 0.3)
        eq = MathTex(r"\hat\rho_{\text{OLS}} = \rho + "
                     r"\frac{\operatorname{Cov}(S, \text{ability})}{\operatorname{Var}(S)}"
                     r"\,\beta_{\text{ability}}", font_size=32).move_to(RIGHT * 2.8 + UP * 1.6)
        side = VGroup(
            label(rf"each year of school: \\ IQ {R['iq_per_year']:.1f} points higher", font_size=19, color=ABILITY),
            label(r"some of the regression's \\ return is ability: \\ the bias is positive", font_size=19, color=WHITE),
            label(r"but IQ is not all of ability, \\ and some of it is schooling", font_size=17, color=GREY_A),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.35).move_to(RIGHT * 3.0 + DOWN * 1.0)
        tag = data_tag(r"the 1980 National Longitudinal Survey, \ via Wooldridge's data", corner=DR, font_size=12)
        bh = label(r"ability bias", font_size=30, color=ABILITY).next_to(eq, UP, buff=0.35)
        with self.voiceover(
            "The worry has a name: ability bias. If abler people both stay longer in school and earn more, the "
            "regression credits school with what ability did. <bookmark mark='a'/> Among 935 men in a 1980 survey, "
            f"least squares gives {R['w2_ols']:.3f} a year. <bookmark mark='b'/> Add their IQ scores and it falls to "
            f"{R['w2_iq']:.3f}: each extra year of school goes with an IQ about {R['iq_per_year']:.1f} points "
            "higher. <bookmark mark='c'/> The formula says the bias is positive. <bookmark mark='d'/> But a test score "
            "is a poor measure of ability, and school itself raises test scores, so controls cannot settle it. The "
            "field turned to natural experiments."
        ) as vo:
            self.play(FadeIn(bh), FadeIn(tag))
            self.play(Write(eq), run_time=1.5)
            vo.wait_until("a")
            self.play(FadeIn(rows[0]), FadeIn(rows[1]))
            vo.wait_until("b")
            self.play(FadeIn(rows[2]), FadeIn(side[0]))
            vo.wait_until("c")
            self.play(Indicate(eq, color=ABILITY, scale_factor=1.05), FadeIn(side[1]))
            vo.wait_until("d")
            self.play(FadeIn(side[2]))
        self.clear_scene()

    def distance(self):
        R = load("returns")
        steps = flow_chain([(r"a four-year college \\ nearby when 14", E.ACCENT), (r"more schooling", SCHOOL),
                            (r"higher wages", WAGE)],
                           notes=[rf"{100 * R['share_near']:.0f}\% of the men", rf"{R['educ_near']:.1f} vs "
                                  rf"{R['educ_far']:.1f} years", rf"log wage {R['lwage_near']:.2f} vs "
                                  rf"{R['lwage_far']:.2f}"], box_w=3.2, font_size=20, note_size=17).move_to(UP * 1.5)
        bars = VGroup()
        for k, (nm, v, s, col) in enumerate(((r"least squares", R["ols"], R["ols_se"], SCHOOL),
                                             (r"college nearby, \ as an instrument", R["iv"], R["iv_se"], E.ACCENT))):
            y = -0.6 - 1.0 * k
            r = Rectangle(width=v * 30, height=0.45, stroke_width=0, fill_color=col, fill_opacity=0.85).move_to(
                np.array([-1.0 + v * 15, y, 0]))
            ci = Line(np.array([-1.0 + (v - 1.96 * s) * 30, y, 0]), np.array([-1.0 + (v + 1.96 * s) * 30, y, 0]),
                      color=WHITE, stroke_width=2)
            bars.add(VGroup(label(nm, font_size=18, color=col).next_to(r, LEFT, buff=0.2).align_to(
                np.array([-1.1, 0, 0]), RIGHT), r, ci, label(f"{v:.3f}", font_size=18, color=WHITE).next_to(
                r, UP, buff=0.05).shift(RIGHT * (v * 15 - 0.3))))
        foot = label(rf"first-stage F {R['F']:.0f}: \ a usable but not strong instrument", font_size=18,
                     color=GREY_A).to_edge(DOWN, buff=0.4)
        tag = data_tag(r"Card (1995), \ via Wooldridge's data; \ recomputed", corner=DR, font_size=12)
        with self.voiceover(
            "In 1995 David Card used geography. <bookmark mark='a'/> Young men who grew up near a four-year college "
            "were more likely to go, <bookmark mark='b'/> getting almost a year more school, <bookmark mark='c'/> "
            "and earned more. If living near a college matters for wages only through schooling, it is an "
            "instrument. <bookmark mark='d'/> With Card's controls, least squares gives "
            f"{R['ols']:.3f}; the instrument gives {R['iv']:.3f}, with a standard error of {R['iv_se']:.3f}. "
            "Recomputed here from his data, the published numbers come back. <bookmark mark='e'/> The instrumental "
            "estimate is larger, not smaller, than least squares, the opposite of what ability bias predicts."
        ) as vo:
            self.play(FadeIn(tag), FadeIn(steps.boxes[0]), FadeIn(steps.notes[0]))
            vo.wait_until("b")
            self.play(GrowArrow(steps.arrows[0]), FadeIn(steps.boxes[1]), FadeIn(steps.notes[1]))
            vo.wait_until("c")
            self.play(GrowArrow(steps.arrows[1]), FadeIn(steps.boxes[2]), FadeIn(steps.notes[2]))
            vo.wait_until("d")
            self.play(LaggedStart(*[FadeIn(b_) for b_ in bars], lag_ratio=0.5), run_time=2.0)
            vo.wait_until("e")
            self.play(FadeIn(foot))
        self.clear_scene()

    def designs(self):
        A, O = tables.AK_1991.data, tables.OREOPOULOS_2006.data
        cards = point_cards([
            (r"quarter of birth", rf"compulsory schooling \\ kept up to {A['dropouts']}\% of \\ would-be dropouts "
                                  r"\\ in school", SCHOOL),
            (r"weak instruments", r"random 'quarters' \\ give the same answer: \\ the instrument \\ barely moves "
                                  r"school", LOSS),
            (r"Britain, \ 1947", rf"the leaving age \\ from {O['from']} to {O['to']}: \\ almost half stayed on; \\ "
                                 r"large returns", WAGE),
            (r"the pattern", r"the instruments \\ give 6 to 15\%, \\ at or above \\ least squares", E.ACCENT),
        ], width=12.8, cols=4, font_size=19).move_to(DOWN * 0.1)
        head = label(r"more natural experiments", font_size=28, color=E.ACCENT).to_edge(UP, buff=0.6)
        tag = published_tag(tables.AK_1991.tag + r"; \ " + tables.OREOPOULOS_2006.tag, corner=DR, font_size=11)
        with self.voiceover(
            "Other designs agree. <bookmark mark='a'/> Joshua Angrist and Alan Krueger noticed in 1991 that children "
            "born early in the year reach the school-leaving age with less schooling, and that compulsory schooling "
            f"kept up to {A['dropouts']} percent of would-be dropouts in school; their instrumental estimates were "
            "close to least squares. <bookmark mark='b'/> John Bound, David Jaeger and Regina Baker then showed that "
            "quarter of birth moves schooling so little that random numbers, used as instruments, gave similar "
            "answers: the lesson of weak instruments, now taught in every course. <bookmark mark='c'/> Philip "
            f"Oreopoulos used Britain's rise in the school-leaving age from {O['from']} to {O['to']} in 1947, which "
            "kept almost half of fourteen-year-olds in school a year longer, and found large returns. "
            "<bookmark mark='d'/> Across designs, a year of school is worth roughly six to fifteen percent, and the "
            "natural experiments sit at or above least squares."
        ) as vo:
            self.play(FadeIn(head), FadeIn(tag))
            for mk, c in zip("abcd", cards.cards):
                vo.wait_until(mk)
                self.play(FadeIn(c, shift=UP * 0.1))
        self.clear_scene()

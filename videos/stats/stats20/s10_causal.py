from __future__ import annotations

import numpy as np

from videos.stats.stats20.common import *  # noqa: F403

NODES = {
    "usual": ((-2.2, 0.0), r"current usual sodium", SALT),
    "prior": ((0.0, -0.9), r"earlier pressure", GREY_A),
    "sbp": ((2.6, 0.0), r"current pressure", BP),
    "age": ((0.2, 2.3), r"age, \ sex", GREY_A),
    "energy": ((-4.8, 1.8), r"energy", GREY_A),
    "bmi": ((-1.2, 2.3), r"BMI", GREY_A),
    "recall": ((-4.6, -1.6), r"one day's recall", SALT),
    "told": ((0.2, -2.3), r"told it's high", RES),
    "meds": ((3.6, -2.0), r"medicine", RES),
    "other": ((5.0, 2.0), r"unmeasured: \ activity, \ alcohol, \ income", GREY_B),
}


def node(key):
    (x, y), t, c = NODES[key]
    lab = label(t, font_size=20, color=c)
    box = RoundedRectangle(width=lab.width + 0.4, height=0.6, corner_radius=0.12, stroke_color=c, stroke_width=2,
                           fill_color="#11161d", fill_opacity=1)
    return VGroup(box, lab.move_to(box)).move_to([x, y, 0])


def arrow(a, b, color=GREY_B, dashed=False):
    s, e = a.get_center(), b.get_center()
    d = (e - s) / np.linalg.norm(e - s)
    p0 = a[0].get_boundary_point(d) if hasattr(a[0], "get_boundary_point") else s
    p1 = b[0].get_boundary_point(-d) if hasattr(b[0], "get_boundary_point") else e
    cls = DashedLine if dashed else Line
    ln = cls(p0, p1, color=color, stroke_width=2.5)
    ln.add_tip(tip_length=0.18)
    return ln


class CausalOrNot(VoiceoverScene):
    def construct(self):
        self.card()
        self.dag()
        self.reverse()
        self.trials()
        self.hierarchy()
        self.can_say()

    def card(self):
        card = chapter_card(9, r"Causal or not?", r"What a survey can, \ and cannot, \ say", lit=(1988,), part=PART)
        with self.voiceover("Chapter nine. Causal, or not?"):
            self.play(FadeIn(card[0], shift=UP * 0.2), FadeIn(card[1]))
        self.play(FadeOut(card))

    def dag(self):
        n = {k: node(k) for k in NODES}
        main = arrow(n["usual"], n["sbp"], SALT)
        q = label(r"?", font_size=36, color=SALT).next_to(main, UP, buff=0.1)
        conf = VGroup(arrow(n["age"], n["usual"]), arrow(n["age"], n["sbp"]), arrow(n["energy"], n["usual"]),
                      arrow(n["bmi"], n["sbp"]), arrow(n["bmi"], n["usual"]))
        meas = arrow(n["usual"], n["recall"], SALT, dashed=True)
        rev = VGroup(arrow(n["prior"], n["told"], RES), arrow(n["prior"], n["sbp"], GREY_B), arrow(n["told"], n["usual"], RES), arrow(n["told"], n["meds"], RES),
                     arrow(n["meds"], n["sbp"], RES))
        unm = VGroup(arrow(n["other"], n["sbp"], GREY_B, dashed=True), arrow(n["other"], n["usual"], GREY_B, dashed=True))
        with self.voiceover(
            "To see what the survey can and can't say about cause, draw the causal story, as Part 35 will do "
            "formally. <bookmark mark='a'/> The arrow we care about runs from usual sodium to blood pressure. "
            "<bookmark mark='b'/> Age and sex affect both; energy intake drives sodium; body size affects both. These"
            " are the confounders the model adjusted for. <bookmark mark='c'/> We never see usual sodium, only one "
            "day's recall of it, the dashed arrow of chapter eight. <bookmark mark='d'/> Time order matters: earlier "
            "high pressure can lead to diagnosis, which can change current sodium and treatment; both can affect "
            "current pressure. We separate earlier and current pressure so the diagram is acyclic. The primary "
            "analysis removed the medicated, but not everyone who changed their diet. <bookmark mark='e'/> And things"
            " we didn't measure, such as physical activity, alcohol and income, may affect both diet and pressure."
        ) as vo:
            vo.wait_until("a")
            self.play(FadeIn(n["usual"]), FadeIn(n["sbp"]), Create(main), FadeIn(q))
            vo.wait_until("b")
            self.play(FadeIn(n["age"]), FadeIn(n["energy"]), FadeIn(n["bmi"]), LaggedStart(*[Create(a) for a in conf], lag_ratio=0.2))
            vo.wait_until("c")
            self.play(FadeIn(n["recall"]), Create(meas))
            vo.wait_until("d")
            self.play(FadeIn(n["prior"]), FadeIn(n["told"]), FadeIn(n["meds"]), LaggedStart(*[Create(a) for a in rev], lag_ratio=0.3), run_time=2.0)
            vo.wait_until("e")
            self.play(FadeIn(n["other"]), LaggedStart(*[Create(a) for a in unm], lag_ratio=0.3))
        self.wait(1.5)
        self.clear_scene()

    def reverse(self):
        d = load("reverse")
        rows = [
            cmath(r"\text{ever told pressure is high}", r":", rf"{100 * d['told_share']:.0f}\%\ \text{{of adults}}", font_size=28),
            cmath(r"\text{sodium: \ told vs not}", r":", rf"{d['na_told']:.2f}\ \text{{vs}}\ {d['na_not']:.2f}\ \text{{g}}", font_size=28),
            cmath(r"\text{per 1,000 kcal}", r":", rf"{d['dens_told']:.2f}\ \text{{vs}}\ {d['dens_not']:.2f}\ \text{{g}}", font_size=28),
            cmath(r"\text{their age}", r":", rf"{d['age_told']:.0f}\ \text{{vs}}\ {d['age_not']:.0f}", font_size=28),
        ]
        rows[2][2].set_color(OBS)
        whys = [why(r"including those on medicine"), why(r"a little less salt"), why(r"but no less salty a diet"),
                why(r"older people eat less of everything")]
        intro = label('A cross-sectional comparison cannot establish time order', font_size=36)
        if intro.width > 12.5:
            intro.width = 12.5
        with self.voiceover(
            "Is the backwards loop real here? <bookmark mark='a'/> A third of adults say a doctor has told them their"
            " pressure is high. <bookmark mark='b'/> They do eat a little less sodium, three point four zero grams "
            "against three point five five. <bookmark mark='c'/> But per thousand kilocalories, their diet is no less"
            " salty: one point six six against one point six four. <bookmark mark='d'/> They're older, by fourteen "
            "years, and older people eat less of everything. So in NHANES, at least, there's little sign that "
            "diagnosis changed the saltiness of diets. This aggregate cross-sectional comparison cannot rule out diet"
            " changes after diagnosis; age, treatment, reporting and selection may conceal them."
        ) as vo:
            self.play(FadeIn(intro))
            step = ladder(self, rows, whys, keep=4, top=2.6, x=-0.6, buff=0.75, edge=6.9)
            for k, m_ in enumerate("abcd"):
                vo.wait_until(m_)
                step(k, transform=False)
                if k == 0:
                    self.play(FadeOut(intro), run_time=0.25)
        self.clear_scene()

    def trials(self):
        a = history_card(2001, r"DASH-Sodium: \ Sacks et al., \ \emph{NEJM}",
                         r"412 adults fed set diets with 50, \ 100 or 150 mmol of sodium a day, \ for 30 days each, in random order: "
                         r"high to low lowered systolic pressure by 6.7 mm Hg on a typical American diet",
                         color=HIT, width=11.6, font_size=22).move_to([0, 1.6, 0])
        b = history_card(2013, r"He, \ Li \& MacGregor: \ a meta-analysis, \ \emph{BMJ}",
                         r"34 randomized trials of salt reduction for 4 weeks or more: \ 4.4 g a day less salt "
                         r"(1.75 g of sodium) lowered systolic pressure by 4.2 mm Hg",
                         color=HIT, width=11.6, font_size=22).move_to([0, -0.9, 0])
        foot = label(r"about 2.4 to 2.9 mm Hg per g of sodium; \ randomization balances baseline confounders in expectation", font_size=24,
                     color=OBS).to_edge(DOWN, buff=0.5)
        with self.voiceover(
            "<bookmark mark='a'/> Now the trials. In DASH-Sodium, published in 2001, four hundred and twelve adults "
            "ate diets prepared for them, at three levels of sodium, each for a month, in random order. On a typical "
            "American diet, going from high sodium to low lowered systolic pressure by six point seven millimetres. "
            "<bookmark mark='b'/> In 2013 Feng He, Jiafu Li and Graham MacGregor pooled thirty-four randomized trials"
            " of at least four weeks: four point four grams a day less salt, one point seven five of sodium, lowered "
            "pressure by four point two. <bookmark mark='c'/> That's two and a half to three millimetres per gram of "
            "sodium. And because the diets were assigned at random, baseline confounders are balanced in expectation,"
            " though finite-sample imbalance, adherence and measurement remain considerations. DASH controlled the "
            "supplied food; the meta-analysis also included free-living trials, many using urinary sodium to assess "
            "intake."
        ) as vo:
            vo.wait_until("a")
            self.play(FadeIn(a, shift=UP * 0.2))
            vo.wait_until("b")
            self.play(FadeIn(b, shift=UP * 0.2))
            vo.wait_until("c")
            self.play(FadeIn(foot))
        self.wait(1.0)
        self.clear_scene()

    def hierarchy(self):
        rows = [
            cmath(r"\text{randomized trials}", r":", r"\text{the causal effect of a diet change, \ for a month}", font_size=26),
            cmath(r"\text{the survey}", r":", r"\text{a descriptive slope, \ in the free-living population}", font_size=26),
            cmath(r"\text{the trials' limits}", r":", r"\text{short, \ selected volunteers, \ blood pressure not strokes}", font_size=26),
            cmath(r"\text{the survey's limits}", r":", r"\text{one day's diet, \ confounding, \ no time order}", font_size=26),
        ]
        rows[0][2].set_color(HIT)
        rows[1][2].set_color(DES)
        whys = [why(r"internal validity"), why(r"external validity: \ the population we care about"),
                why(r"do they generalize?"), why(r"can it see an effect at all?")]
        intro = label('Trials and surveys can answer different questions', font_size=36)
        if intro.width > 12.5:
            intro.width = 12.5
        with self.voiceover(
            "<bookmark mark='a'/> The two kinds of evidence answer different questions. A trial tells us the causal effect of "
            "changing the diet, for the people in it, over a month or so. <bookmark mark='b'/> The survey describes the whole "
            "population as it lives. <bookmark mark='c'/> Trials have limits: they're short, their volunteers aren't typical, "
            "and they measure blood pressure rather than strokes. <bookmark mark='d'/> And this survey has the limits we've "
            "found: a single day's diet, possible confounding, and no time order, since diet and pressure were measured "
            "together. Each has to be read with the other's strengths in mind."
        ) as vo:
            self.play(FadeIn(intro))
            step = ladder(self, rows, whys, keep=4, top=2.6, x=-0.6, buff=0.75, edge=6.9)
            for k, m_ in enumerate("abcd"):
                vo.wait_until(m_)
                step(k, transform=False)
                if k == 0:
                    self.play(FadeOut(intro), run_time=0.25)
        self.clear_scene()

    def can_say(self):
        rows = fit_rows(VGroup(
            label(r"we can say: \ in 2017--18, \ among untreated adults, \ yesterday's sodium barely predicts pressure", font_size=22, color=DES),
            label(r"we can say: \ one day's recall is too noisy to detect an effect of the trials' size", font_size=22, color=SALT),
            label(r"we cannot say: \ ``salt does not raise blood pressure''", font_size=24, color=RES),
            label(r"the guideline rests on the trials; \ this survey neither supports nor undermines it", font_size=22, color=OBS),
            label(r"designs that can answer causal questions from observational data: \ Parts 35--37", font_size=20, color=GREY_A),
        ), 12.4, 0.5, [0, 0, 0])
        intro = label('Report the descriptive association within its causal limits', font_size=36)
        if intro.width > 12.5:
            intro.width = 12.5
        with self.voiceover(
            "<bookmark mark='a'/> The report can describe the adjusted recall-day association in this analytic "
            "sample, with survey weights and explicit exclusions. Extending it to all eligible adults needs "
            "assumptions about nonresponse and missing measurements. <bookmark mark='b'/> The repeat recalls reveal "
            "measurement concerns; quantitative attenuation or correction needs an adequate error model, especially "
            "with noisy energy. <bookmark mark='c'/> A non-significant descriptive slope does not show that changing "
            "sodium has no causal effect. <bookmark mark='d'/> It also does not formally test a guideline supported "
            "by trials in different populations and interventions. <bookmark mark='e'/> Observational causal designs "
            "and their assumptions return in Parts thirty-five to thirty-seven."
        ) as vo:
            self.play(FadeIn(intro))
            for k, m_ in enumerate("abcde"):
                vo.wait_until(m_)
                if k == 0:
                    self.play(FadeOut(intro), run_time=0.25)
                self.play(FadeIn(rows[k], shift=RIGHT * 0.2))
        self.clear_scene()

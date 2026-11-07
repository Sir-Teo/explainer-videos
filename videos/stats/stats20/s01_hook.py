from __future__ import annotations

import numpy as np

from videos.stats.stats20.common import *  # noqa: F403

STAGES = [r"question", r"estimand", r"design", r"cleaning", r"exploration", r"model", r"checks", r"uncertainty",
          r"sensitivity", r"causal?", r"the World", r"report", r"reproducible"]


class Hook(VoiceoverScene):
    def construct(self):
        self.question()
        self.nhanes()
        self.cloud()
        self.plan()
        self.objectives()

    def question(self):
        tl = timeline(lit=(1971, 1988)).to_edge(UP, buff=0.35)
        d = load("explore")
        rows = fit_rows(VGroup(
            label(r"the US guideline: \ under 2,300 mg of sodium a day", font_size=26, color=SALT),
            label(rf"untreated adults in our analytic sample: \ mean \ {1000 * d['mean_na']:,.0f} mg", font_size=26, color=SALT),
            label(rf"{100 * d['share_over_2300']:.0f}\% of adults are over the guideline on a given day", font_size=24, color=GREY_A),
            label(r"the question: \ how does blood pressure depend on salt?", font_size=30, color=BP),
            label(r"and how much can a survey tell us about it?", font_size=26, color=OBS),
        ), 12.4, 0.45, [0, -0.6, 0])
        intro = label('An observational analysis of sodium and blood pressure', font_size=36).move_to([0, 1.9, 0])
        if intro.width > 12.5:
            intro.width = 12.5
        with self.voiceover(
            "This is the last part of the bachelor's degree, and it introduces no new method. Instead we take one "
            "question all the way through, the way a working statistician would. <bookmark mark='a'/> The question is"
            " about salt. American dietary guidelines say adults should eat less than two thousand three hundred "
            "milligrams of sodium a day. <bookmark mark='b'/> In our weighted analytic sample, untreated adults "
            "average about three and a half thousand. <bookmark mark='c'/> On any given day, three in four are over "
            "the guideline. <bookmark mark='d'/> The reason for the guideline is blood pressure: salt is thought to "
            "raise it, and high pressure causes strokes and heart attacks. So, how does blood pressure depend on "
            "salt? <bookmark mark='e'/> And how much can a national survey tell us about that?"
        ) as vo:
            self.play(FadeIn(intro))
            self.play(FadeIn(tl))
            for k, m_ in enumerate("abcde"):
                vo.wait_until(m_)
                self.play(FadeIn(rows[k], shift=RIGHT * 0.2))
        self.clear_scene()

    def nhanes(self):
        hc = history_card(1971, r"NHANES, \ the National Health and Nutrition Examination Survey",
                          r"run by the CDC's National Center for Health Statistics; \ a national sample interviewed at home, \ then "
                          r"examined in mobile centres: \ blood pressure, \ height and weight, \ blood tests, \ and what they ate",
                          color=NH, width=11.0, font_size=24).move_to([0, 1.5, 0])
        rows = fit_rows(VGroup(
            label(r"2017--2018 cycle: \ 9,254 people interviewed, \ 8,704 examined", font_size=24),
            label(r"blood pressure: \ three readings, \ by a trained examiner", font_size=24, color=BP),
            label(r"diet: \ two 24-hour recalls, \ every food and drink of the day before", font_size=24, color=SALT),
            label(r"public domain: \ anyone can download it, \ and anyone can check us", font_size=24, color=HIT),
        ), 12.0, 0.35, [0, -1.6, 0])
        with self.voiceover(
            "<bookmark mark='a'/> Our data come from NHANES, the National Health and Nutrition Examination Survey. "
            "Its ancestor began in 1959, and since 1971 it has combined a home interview with a physical examination "
            "in a mobile centre that travels the country. <bookmark mark='b'/> We use the 2017 to 2018 cycle: nine "
            "thousand two hundred and fifty-four people interviewed, eight thousand seven hundred and four examined. "
            "<bookmark mark='c'/> The protocol called for three blood-pressure readings by a trained examiner, though"
            " some participants have fewer. <bookmark mark='d'/> And each was asked to recall everything they had "
            "eaten and drunk the day before, from which sodium is computed; most were asked again, by telephone, "
            "three to ten days later. <bookmark mark='e'/> The files are public: anyone can download them from the "
            "CDC, and anyone can check every number in this part."
        ) as vo:
            vo.wait_until("a")
            self.play(FadeIn(hc, shift=UP * 0.2))
            for k, m_ in enumerate("bcde"):
                vo.wait_until(m_)
                self.play(FadeIn(rows[k], shift=RIGHT * 0.2))
        self.clear_scene()

    def cloud(self):
        d = load("hook")
        A = axes([0, 9], [80, 200], x_length=8.4, y_length=4.6, xlabel=r"sodium yesterday, \ g", ylabel=r"systolic pressure, \ mm Hg",
                 xticks=[0, 2, 4, 6, 8], yticks=[80, 120, 160, 200], center=[-1.5, 0.2, 0])
        ax = A.ax
        na, y = np.asarray(d["na"]), np.asarray(d["sbp"])
        m = (na < 9) & (y < 200) & (y > 80)
        dots = VGroup(*[Dot(ax.c2p(a, b), radius=0.035, color=NH, fill_opacity=0.65) for a, b in zip(na[m], y[m])])
        line = Line(ax.c2p(0, d["intercept"]), ax.c2p(9, d["intercept"] + 9 * d["slope"]), color=BP, stroke_width=4)
        guide = DashedLine(ax.c2p(2.3, 80), ax.c2p(2.3, 200), color=SALT, stroke_width=2)
        rows = fit_rows(VGroup(
            label(rf"{d['n']:,} adults not on BP medicine \ (700 shown)", font_size=22),
            label(r"dashed: \ the 2,300 mg guideline", font_size=22, color=SALT),
            MathTex(rf"\text{{crude slope}}: {d['slope']:+.2f}\ \text{{mm Hg per g}}", font_size=28, color=BP),
            label(r"the trials: \ about 2--3 mm Hg per g", font_size=22, color=HIT),
            label(r"why the difference? \ that is this part", font_size=22, color=OBS),
        ), 3.45, 0.4, [5.1, 0.2, 0])
        with self.voiceover(
            "<bookmark mark='a'/> Here is a first look: three thousand and seventy-one adults not taking blood-pressure medicine, "
            "seven hundred of them shown, with their systolic pressure against the sodium they ate the day before. "
            "<bookmark mark='b'/> The dashed line is the guideline. <bookmark mark='c'/> A straight line through the cloud "
            "slopes very slightly down: minus point one four millimetres of mercury per gram. More salt, a hair lower pressure. "
            "<bookmark mark='d'/> Yet randomized trials, in which people were assigned diets with different amounts of salt, "
            "find that each gram of sodium raises pressure by two to three millimetres. <bookmark mark='e'/> Is the survey "
            "wrong, or the trials, or the question? Finding out is the whole of this part."
        ) as vo:
            self.add(nh_tag(corner=DR))
            self.play(FadeIn(A))
            vo.wait_until("a")
            self.play(LaggedStart(*[FadeIn(x) for x in dots], lag_ratio=0.002), FadeIn(rows[0]), run_time=2.5)
            vo.wait_until("b")
            self.play(Create(guide), FadeIn(rows[1]))
            vo.wait_until("c")
            self.play(Create(line), FadeIn(rows[2]))
            vo.wait_until("d")
            self.play(FadeIn(rows[3]))
            vo.wait_until("e")
            self.play(FadeIn(rows[4]))
        self.clear_scene()

    def plan(self):
        boxes = VGroup()
        for i, s in enumerate(STAGES):
            r = RoundedRectangle(width=1.85, height=0.7, corner_radius=0.1, stroke_color=SALT if i == 0 else GREY_B,
                                 stroke_width=2, fill_color=SALT, fill_opacity=0.1 if i else 0.3)
            boxes.add(VGroup(r, label(s, font_size=18).move_to(r)))
        top = VGroup(*boxes[:7]).arrange(RIGHT, buff=0.12)
        bot = VGroup(*boxes[7:]).arrange(RIGHT, buff=0.12)
        grid = VGroup(top, bot).arrange(DOWN, buff=0.5).move_to([0, 0.8, 0])
        rows = fit_rows(VGroup(
            label(r"every decision made on screen, \ and logged", font_size=24),
            label(r"an illustrative plan, \ presented before the results", font_size=24, color=OBS),
            label(r"the same code run on the World, \ where the answer is known", font_size=24, color=WLD),
        ), 12.0, 0.35, [0, -2.2, 0])
        intro = label('An analysis connects the question to a reproducible report', font_size=36)
        if intro.width > 12.5:
            intro.width = 12.5
        with self.voiceover(
            "<bookmark mark='a'/> We'll go through every stage an analysis really has, in order: from the question, "
            "through what exactly we're estimating, the survey's design, cleaning, exploration, a model and its "
            "checks, uncertainty and sensitivity, the causal question, a check on the World, the report, and "
            "reproducibility. <bookmark mark='b'/> Every decision will be made on screen and written into a log. "
            "<bookmark mark='c'/> We present an illustrative analysis plan before showing the result. This is a "
            "teaching sequence, not a claim of time-stamped preregistration. <bookmark mark='d'/> And then the "
            "identical code will run on the World, where we built the effect of salt ourselves and know the answer."
        ) as vo:
            self.play(FadeIn(intro))
            vo.wait_until("a")
            self.play(FadeOut(intro), run_time=0.25)
            self.play(LaggedStart(*[FadeIn(b, shift=UP * 0.1) for b in boxes], lag_ratio=0.15), run_time=4.0)
            for k, m_ in enumerate("bcd"):
                vo.wait_until(m_)
                self.play(FadeIn(rows[k], shift=RIGHT * 0.2))
        self.clear_scene()

    def objectives(self):
        head = VGroup(label(r"Part 20", font_size=34, color=GREY_B), label(r"The Analysis", font_size=60),
                      label(r"the bachelor's capstone", font_size=28, color=SALT)).arrange(DOWN, buff=0.25)
        obj = objectives_card([
            r"from a question to an estimand, \ for a stated population",
            r"a complex survey: \ strata, \ PSUs and weights; \ cleaning with a decision log",
            r"exploration, \ a pre-specified model, \ and its checks",
            r"design-based uncertainty, \ sensitivity, \ and measurement error",
            r"what a survey cannot say; \ the World and a trial; \ the report and its reproducibility",
        ], color=SALT, font_size=26)
        prereq = note(r"prerequisites: \ Parts 1--19").to_corner(DL, buff=0.3)
        built = note(r"built: \ the capstone pipeline, \ \texttt{statkit.capstone}, \ the World's health block").to_corner(DR, buff=0.3)
        with self.voiceover(
            "<bookmark mark='a'/> Part twenty: the analysis. <bookmark mark='b'/> We'll turn a question into an estimand; "
            "handle a complex survey's strata, clusters and weights; clean the data with a log of every decision; explore; fit "
            "a model we wrote down in advance, and check it; get its uncertainty right; test how sensitive the answer is; face "
            "measurement error; ask what a survey can and cannot say about cause; check everything on the World and against a "
            "trial; and write the report, so that anyone can reproduce it."
        ) as vo:
            vo.wait_until("a")
            self.play(FadeIn(head, shift=UP * 0.2))
            vo.wait_until("b")
            self.play(FadeOut(head), FadeIn(obj, shift=UP * 0.2), FadeIn(prereq), FadeIn(built))
        self.wait(1.0)
        self.clear_scene()

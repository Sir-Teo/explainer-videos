from __future__ import annotations

from videos.psychology.psych31.common import *  # noqa: F403


class Designs(VoiceoverScene):
    def construct(self):
        self.card()
        self.world()
        self.cross()
        self.longitudinal()
        self.sequential()
        self.debate()

    def card(self):
        card = chapter_card(2, r"Three designs, \ three answers", r"When does ability start to decline?",
                            lit={1956: r"Seattle Longitudinal Study", 2009: r"Salthouse"}, part=PART,
                            scale=("person", "group"), marr=("what",))
        with self.voiceover("Chapter two. Three designs, three answers."):
            self.play(FadeIn(card, shift=UP * 0.2))
        self.clear_scene()

    def _axes(self, center=(-3.1, -0.4, 0)):
        return axes([20, 90], [-2.8, 0.7], x_length=6.5, y_length=5.0, xticks=[20, 40, 60, 80],
                    yticks=[-2, -1, 0], xfmt=lambda v: f"{v:.0f}", yfmt=lambda v: f"{v:g}", xlabel=r"age",
                    ylabel=r"score \ (SD, \ from age 20)", center=list(center), font_size=16)

    def world(self):
        d = load("designs")
        head = heading(r"A world where the truth is known")
        A = self._axes()
        truth = curve(A.ax, d["grid"], d["truth"], TRUE, stroke_width=6)
        rows = rows_of([
            (r"Psyche's population: \ 40{,}000 people born from 1900 to 1990, \ tested from 1956 on", WHITE),
            (r"the true ageing curve: \ flat to 55, \ then falling, \ faster with age", TRUE),
            (rf"and a cohort drift: \ each later year of birth scores {d['gain']:.2f} SD higher, \ about three IQ "
             r"points a decade", COHORT),
            (r"no period effect at all, \ so we can see what each design does with the other two clocks", PERIOD),
        ], 5.4, 22, 0.36).move_to([3.7, -0.2, 0])
        tag = simulated_tag(r"simulated: \texttt{lifespan.ability\_world}")
        with self.voiceover(
            "To see what each design does, Psyche builds a world where the truth is known. "
            "<bookmark mark='a'/> Forty thousand people, born between 1900 and 1990, tested from 1956 on. "
            "<bookmark mark='b'/> The true ageing curve, in green, is flat until fifty-five, then falls, faster and "
            "faster. <bookmark mark='c'/> On top of it there's a cohort drift: each later year of birth scores two "
            "hundredths of a standard deviation higher, about three IQ points a decade, roughly the size of the "
            "Flynn effect we'll meet in chapter twelve. <bookmark mark='d'/> And there's no period effect at all, so "
            "we can watch what each design does with the other two clocks."
        ) as vo:
            self.play(FadeIn(head), FadeIn(A), FadeIn(tag))
            vo.wait_until("a")
            self.play(FadeIn(rows[0]))
            vo.wait_until("b")
            self.play(Create(truth), FadeIn(rows[1]))
            for m, r in zip("cd", rows[2:]):
                vo.wait_until(m)
                self.play(FadeIn(r, shift=RIGHT * 0.15))
        self.clear_scene()

    def cross(self):
        d = load("designs")
        head = heading(r"Cross-sectional: \ many ages, \ one year")
        A = self._axes()
        truth = curve(A.ax, d["grid"], d["truth"], TRUE, stroke_width=4)
        pts = scatter(A.ax, d["cs_age"], d["cs_mean"], PERIOD, radius=0.08)
        line = curve(A.ax, d["cs_age"], d["cs_mean"], PERIOD, stroke_width=3)
        i50 = list(d["cs_age"]).index(50.0)
        rows = rows_of([
            (r"test 300 people at each age, \ all in 1990", PERIOD),
            (rf"the 20-year-olds were born in 1970, \ the 70-year-olds in 1920: \ age and cohort move together",
             COHORT),
            (rf"so the curve falls from the twenties: \ {d['cs_mean'][i50]:.2f} SD by 50, \ where the truth is flat",
             LOST),
            (r"a cross-section measures differences between generations, \ and calls them ageing", WHITE),
        ], 5.4, 22, 0.36).move_to([3.7, -0.2, 0])
        tag = simulated_tag(r"simulated: \texttt{lifespan.cross\_sectional}")
        with self.voiceover(
            "The first design is the quickest. <bookmark mark='a'/> Test three hundred people at each age, all in "
            "the same year, 1990. <bookmark mark='b'/> But the twenty-year-olds were born in 1970 and the "
            "seventy-year-olds in 1920, so age and cohort move together. <bookmark mark='c'/> The curve falls from "
            f"the twenties: by fifty it's down {abs(d['cs_mean'][i50]):.2f} of a standard deviation, where the true "
            "curve hasn't moved. <bookmark mark='d'/> A cross-section measures differences between generations, "
            "and calls them ageing."
        ) as vo:
            self.play(FadeIn(head), FadeIn(A), FadeIn(truth), FadeIn(tag))
            vo.wait_until("a")
            self.play(FadeIn(rows[0]), LaggedStart(*[FadeIn(p_) for p_ in pts], lag_ratio=0.1))
            vo.wait_until("b")
            self.play(FadeIn(rows[1]))
            vo.wait_until("c")
            self.play(Create(line), FadeIn(rows[2]))
            vo.wait_until("d")
            self.play(FadeIn(rows[3]))
        self.clear_scene()

    def longitudinal(self):
        d = load("designs")
        head = heading(r"Longitudinal: \ one cohort, \ many years")
        A = self._axes()
        truth = curve(A.ax, d["grid"], d["truth"], TRUE, stroke_width=4)
        kept = curve(A.ax, d["lo_age"], d["lo_kept"], AGE, stroke_width=4)
        kd = scatter(A.ax, d["lo_age"], d["lo_kept"], AGE, radius=0.08)
        every = DashedVMobject(curve(A.ax, d["lo_age"], d["lo_every"], GREY_B, stroke_width=3), num_dashes=30)
        n0, n1 = int(d["lo_n"][0]), int(d["lo_n"][-1])
        rows = rows_of([
            (r"follow people born around 1930, \ every seven years from 1956", AGE),
            (r"each retest adds practice: \ they have seen the test before", PERIOD),
            (rf"and people leave, \ the lowest scorers most often: \ {num(n0)} at the start, \ {num(n1)} at the "
             rf"end", LOST),
            (r"the survivors improve into their fifties, \ and the late decline looks milder than it is", AGE),
            (r"dashed: \ everyone, \ without practice: \ the truth, \ up to noise", GREY_B),
        ], 5.4, 22, 0.34).move_to([3.7, -0.2, 0])
        tag = simulated_tag(r"simulated: \texttt{lifespan.longitudinal}")
        with self.voiceover(
            "The second design follows the same people. <bookmark mark='a'/> Take everyone born around 1930 and "
            "test them every seven years from 1956, as the Seattle study did. Cohort is now fixed, but each test "
            "is also a later year. <bookmark mark='b'/> And two things go wrong. Each retest adds practice: people "
            "have seen the test before. <bookmark mark='c'/> And people leave, the lowest scorers most often, from "
            f"{n0:,} at the start to {n1:,} at the end. <bookmark mark='d'/> So the survivors seem to improve into "
            "their fifties, and the late decline looks milder than it is. <bookmark mark='e'/> The dashed line is "
            "what the same tests would show for everyone, without practice. It follows the truth."
        ) as vo:
            self.play(FadeIn(head), FadeIn(A), FadeIn(truth), FadeIn(tag))
            vo.wait_until("a")
            self.play(FadeIn(rows[0]))
            vo.wait_until("b")
            self.play(FadeIn(rows[1]))
            vo.wait_until("c")
            self.play(FadeIn(rows[2]), LaggedStart(*[FadeIn(p_) for p_ in kd], lag_ratio=0.15))
            vo.wait_until("d")
            self.play(Create(kept), FadeIn(rows[3]))
            vo.wait_until("e")
            self.play(Create(every), FadeIn(rows[4]))
        self.clear_scene()

    def sequential(self):
        d = load("designs")
        head = heading(r"Cohort-sequential: \ several cohorts, \ followed")
        A = self._axes()
        truth = curve(A.ax, d["grid"], d["truth"], TRUE, stroke_width=4)
        est = scatter(A.ax, d["cq_age"], d["cq_curve"], COHORT, radius=0.09)
        line = curve(A.ax, d["cq_age"], d["cq_curve"], COHORT, stroke_width=3)
        rows = rows_of([
            (r"seven cohorts, \ born 1900 to 1960, \ each followed for up to nine waves", COHORT),
            (r"regress the scores on age bands and year of birth, \ assuming no period effect", PERIOD),
            (rf"the ageing curve comes back, \ and the cohort drift: \ {d['cq_gain']:.3f} SD a year against a true "
             rf"{d['gain']:.3f}", TRUE),
            (r"Schaie's design in Seattle: \ the assumption does the work, \ and here it happens to be true", YOU),
        ], 5.4, 22, 0.36).move_to([3.7, -0.2, 0])
        tag = simulated_tag(r"simulated: \texttt{lifespan.cohort\_sequential}")
        with self.voiceover(
            "The third design combines the first two. <bookmark mark='a'/> Follow several cohorts, born from 1900 "
            "to 1960, each for up to nine waves. Now the same age is seen in different cohorts, and the same cohort "
            "at different ages. <bookmark mark='b'/> Regress the scores on age bands and year of birth, assuming no "
            "period effect. <bookmark mark='c'/> The ageing curve comes back, and so does the cohort drift: "
            f"{d['cq_gain']:.3f} of a standard deviation a year, against a true {d['gain']:.2f}. "
            "<bookmark mark='d'/> This is Warner Schaie's design in the Seattle Longitudinal Study, begun in 1956. "
            "The assumption does the work, and in Psyche's world it happens to be true."
        ) as vo:
            self.play(FadeIn(head), FadeIn(A), FadeIn(truth), FadeIn(tag))
            vo.wait_until("a")
            self.play(FadeIn(rows[0]))
            vo.wait_until("b")
            self.play(FadeIn(rows[1]))
            vo.wait_until("c")
            self.play(LaggedStart(*[FadeIn(p_) for p_ in est], lag_ratio=0.1), Create(line), FadeIn(rows[2]))
            vo.wait_until("d")
            self.play(FadeIn(rows[3]))
        self.clear_scene()

    def debate(self):
        head = heading(r"The real argument")
        left = VGroup(label(r"K. Warner Schaie", font_size=28, color=AGE),
                      wrapped_label(r"most abilities peak in early midlife, \ hold until the late fifties or "
                                    r"sixties, \ then decline, \ faster by the late seventies", 5.6, 22, WHITE),
                      wrapped_label(r"the cross-sectional decline from the twenties is mostly cohort differences",
                                    5.6, 22, COHORT)).arrange(DOWN, buff=0.3, aligned_edge=LEFT)
        right = VGroup(label(r"Timothy Salthouse", font_size=28, color=PERIOD),
                       wrapped_label(r"2009: \ about 2{,}000 healthy adults aged 18 to 60: \ reasoning and speed "
                                     r"begin to decline in the late twenties; \ vocabulary rises until 60", 5.6, 22,
                                     WHITE),
                       wrapped_label(r"longitudinal studies hide early decline under retest gains", 5.6, 22, LOST))
        right.arrange(DOWN, buff=0.3, aligned_edge=LEFT)
        VGroup(left, right).arrange(RIGHT, buff=0.9, aligned_edge=UP).move_to([0, 0.5, 0])
        foot = wrapped_label(r"each side's answer rests on an assumption about practice, \ drop-out or cohorts: \ "
                             r"the argument is about the assumptions", 12.0, 24, YOU).to_edge(DOWN, buff=0.6)
        tag = published_tag(r"Schaie (2005); \ Salthouse (2009)")
        with self.voiceover(
            "With real people, the truth isn't known, and this is a live argument. <bookmark mark='a'/> Warner "
            "Schaie's summary of the Seattle study is that most abilities peak in early midlife, hold until the late "
            "fifties or sixties, then decline, faster by the late seventies, and that the cross-sectional decline "
            "from the twenties is mostly differences between cohorts. <bookmark mark='b'/> Timothy Salthouse, "
            "testing about two thousand healthy adults aged eighteen to sixty, found reasoning and speed beginning to "
            "decline in the late twenties, with vocabulary rising until sixty, and argued that longitudinal studies "
            "hide early decline under retest gains. Schaie called that the cross-sectional fallacy. "
            "<bookmark mark='c'/> Each answer rests on an assumption about practice, drop-out or cohorts. The "
            "argument is really about the assumptions, and the simulation shows how each one bends the curve."
        ) as vo:
            self.play(FadeIn(head), FadeIn(tag))
            vo.wait_until("a")
            self.play(FadeIn(left, shift=RIGHT * 0.15))
            vo.wait_until("b")
            self.play(FadeIn(right, shift=LEFT * 0.15))
            vo.wait_until("c")
            self.play(FadeIn(foot))
        self.clear_scene()

from __future__ import annotations

from videos.psychology.psych56.common import *  # noqa: F403


class Numbers(VoiceoverScene):
    def construct(self):
        card_section(self, 12, r"Numbers in court", r"Can a standard error decide a life?", scale=("society",))
        self.hall()
        self.flynn()

    def hall(self):
        d = load("iq")
        head = heading(r"\emph{Hall v. Florida}, \ 2014")
        A = axes([60, 82], [0, 1], x_length=6.0, y_length=1.6, xticks=[60, 65, 70, 75, 80], yticks=None,
                 xfmt=lambda v: f"{v:.0f}", xlabel=r"IQ", center=[-3.0, 1.0, 0], font_size=12)
        band = Rectangle(width=abs(A.ax.c2p(d["hi"], 0)[0] - A.ax.c2p(d["lo"], 0)[0]), height=0.5, color=MODEL,
                         fill_opacity=0.35, stroke_width=0).move_to(A.ax.c2p((d["lo"] + d["hi"]) / 2, 0.5))
        dot = Dot(A.ax.c2p(71, 0.5), radius=0.09, color=PERSON)
        cut = DashedLine(A.ax.c2p(70, 0), A.ax.c2p(70, 1), color=AUTH)
        rows = rows_of([
            (r"2002: \ the US Supreme Court ruled that people with intellectual disability may not be executed; \ "
             r"states set the tests", WHITE),
            (r"Florida treated an IQ score above 70 as conclusive: \ a man scoring 71 could not show disability", AUTH),
            (rf"Part 3's standard error: \ with reliability 0.97, \ the SEM is {d['sem']:.1f} points; \ a 95\% interval "
             rf"for 71 runs from {d['lo']:.0f} to {d['hi']:.0f}", MODEL),
            (r"in 2014 the Court held that a state must consider the standard error, \ and other evidence, \ when a "
             r"score is near the line: \ psychometrics became constitutional law", GOOD),
        ], 12.4, 20, 0.32).move_to([0, -1.8, 0])
        tag = psyche_tag(r"\texttt{work.score\_interval}")
        with self.voiceover(
            "Can a standard error decide a life? <bookmark mark='a'/> In 2002 the US Supreme Court ruled that people "
            "with intellectual disability may not be executed, and left the states to set the tests. "
            "<bookmark mark='b'/> Florida treated an IQ score above seventy as conclusive, so a man scoring "
            "seventy-one couldn't show disability. <bookmark mark='c'/> Part 3's standard error says otherwise. With "
            "a reliability of zero point nine seven, the standard error is about two and a half points, and a "
            "ninety-five percent interval for seventy-one runs from sixty-six to seventy-six. <bookmark mark='d'/> In "
            "2014 the Court held that a state must consider the standard error, and other evidence, when a score is "
            "near the line. Psychometrics became constitutional law."
        ) as vo:
            self.play(FadeIn(head), FadeIn(tag), FadeIn(A), Create(cut))
            vo.wait_until("a")
            self.play(FadeIn(rows[0]))
            vo.wait_until("b")
            self.play(FadeIn(rows[1]), FadeIn(dot, scale=1.5))
            vo.wait_until("c")
            self.play(FadeIn(rows[2]), FadeIn(band))
            vo.wait_until("d")
            self.play(FadeIn(rows[3]))
        self.clear_scene()

    def flynn(self):
        rows_section(self, r"The Flynn effect in capital cases", [
            (r"Part 32's Flynn effect: \ scores on a test rise over the years after its norms were set, \ about 0.3 "
             r"points a year for many tests in the twentieth century", WHITE),
            (r"a person tested on old norms scores higher than on new ones: \ a 72 on a test normed 15 years earlier "
             r"is roughly a 67.5 on current norms", MODEL),
            (r"courts have split over whether to adjust: \ the arithmetic is simple; \ whether the average trend "
             r"applies to one person is not (Part 47)", AUTH),
            (r"the general lesson: \ a score in court is an estimate with an error and a date, \ not a fact about a "
             r"person", YOU),
        ], "There's a second number in these cases. <bookmark mark='a'/> Part 32's Flynn effect: scores on a test rise "
           "over the years after its norms were set, by about a third of a point a year for many tests in the "
           "twentieth century. <bookmark mark='b'/> So a person tested on old norms scores higher than on new ones. "
           "A seventy-two on a test normed fifteen years earlier is roughly sixty-seven and a half on current norms. "
           "<bookmark mark='c'/> Courts have split over whether to adjust. The arithmetic is simple. Whether an "
           "average trend applies to one person isn't, which is Part 47's question. <bookmark mark='d'/> The general "
           "lesson: a score in court is an estimate, with an error and a date, not a fact about a person.")

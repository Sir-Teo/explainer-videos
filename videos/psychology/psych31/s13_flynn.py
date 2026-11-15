from __future__ import annotations

from videos.psychology.psych31.common import *  # noqa: F403


class Flynn(VoiceoverScene):
    def construct(self):
        self.card()
        self.rise()
        self.norms()
        self.reversal()

    def card(self):
        card = chapter_card(12, r"Cohorts change", r"What if the generations themselves move?",
                            lit={1984: r"Flynn", 2015: r"Pietschnig \& Voracek", 2018: r"Bratsberg \& Rogeberg"},
                            part=PART, scale=("group", "society"), marr=("what",))
        with self.voiceover("Chapter twelve. Cohorts change."):
            self.play(FadeIn(card, shift=UP * 0.2))
        self.clear_scene()

    def rise(self):
        head = heading(r"The Flynn effect")
        A = axes([1910, 2010], [70, 110], x_length=6.2, y_length=4.2, xticks=[1910, 1940, 1970, 2000],
                 yticks=[70, 80, 90, 100, 110], xfmt=lambda v: f"{v:.0f}", yfmt=lambda v: f"{v:.0f}",
                 xlabel=r"year of testing", ylabel=r"IQ on today's norms", center=[-3.0, -0.4, 0], font_size=16)
        yrs = np.linspace(1910, 2010, 101)
        line = curve(A.ax, yrs, 100 - 2.8 * (2010 - yrs) / 10, COHORT, stroke_width=5)
        sh = label(r"the average rate, \ 2.8 points a decade, \ drawn as a line", font_size=16, color=GREY_B)
        sh.next_to(A, DOWN, buff=0.1)
        rows = rows_of([
            (r"James Flynn, \ 1984 and 1987: \ raw scores on IQ tests rose, \ generation after generation, \ in "
             r"every country with the data", WHITE),
            (r"Jakob Pietschnig and Martin Voracek, \ 2015: \ 271 samples, \ about four million people, \ 31 "
             r"countries, \ 1909 to 2013: \ about 2.8 points a decade", COHORT),
            (r"larger for reasoning with new problems than for knowledge: \ too fast for genes", AGE),
            (r"the candidates: \ nutrition and health, \ more and different schooling, \ smaller families, \ a "
             r"world full of abstraction", YOU),
        ], 5.6, 21, 0.36).move_to([3.6, -0.2, 0])
        tag = published_tag(r"Pietschnig \& Voracek (2015)")
        with self.voiceover(
            "The cohort clock isn't only a nuisance. Sometimes it's the finding. <bookmark mark='a'/> In the 1980s, "
            "James Flynn showed that raw scores on IQ tests had risen, generation after generation, in every "
            "country with the data. <bookmark mark='b'/> In 2015, Jakob Pietschnig and Martin Voracek pooled two "
            "hundred and seventy-one samples, about four million people in thirty-one countries, tested from 1909 to "
            "2013: on average, about 2.8 points a decade. On today's norms, the average person of 1910 would score "
            "around seventy-two. <bookmark mark='c'/> The rise was larger for reasoning with new problems than for "
            "knowledge, and far too fast for genes. <bookmark mark='d'/> The candidate causes are nutrition and "
            "health, more and different schooling, smaller families, and a world full of abstraction."
        ) as vo:
            self.play(FadeIn(head), FadeIn(A), FadeIn(tag), FadeIn(sh))
            vo.wait_until("a")
            self.play(FadeIn(rows[0]))
            vo.wait_until("b")
            self.play(Create(line), FadeIn(rows[1]))
            for m, r in zip("cd", rows[2:]):
                vo.wait_until(m)
                self.play(FadeIn(r, shift=RIGHT * 0.15))
        self.clear_scene()

    def norms(self):
        d = load("flynn")
        head = heading(r"Old norms inflate scores")
        A = axes([0, 30], [99, 110], x_length=5.8, y_length=3.8, xticks=[0, 10, 20, 30], yticks=[100, 105, 110],
                 xfmt=lambda v: f"{v:.0f}", yfmt=lambda v: f"{v:.0f}", xlabel=r"years since the test was normed",
                 ylabel=r"average score", center=[-3.0, -0.4, 0], font_size=16)
        c = curve(A.ax, d["years"], d["score"], PERIOD, stroke_width=5)
        dot = Dot(A.ax.c2p(15, d["at15"]), radius=0.09, color=WHITE)
        rows = rows_of([
            (r"an IQ is a rank against a norming sample; \ if scores drift up 3 points a decade, \ the average "
             r"person scored on 15-year-old norms gets about 104.5", WHITE),
            (r"a person's score depends on which edition of the test was used, \ and when", PERIOD),
            (r"in the United States, \ since \emph{Atkins v. Virginia}, \ 2002, \ barred executing people with "
             r"intellectual disability, \ courts have argued over correcting scores near the cutoff for outdated "
             r"norms", LOST),
            (r"a cohort effect, \ deciding a life", YOU),
        ], 5.6, 21, 0.36).move_to([3.6, -0.2, 0])
        tag = psyche_tag(r"\texttt{lifespan.flynn\_norms}")
        with self.voiceover(
            "The drift has a practical consequence. <bookmark mark='a'/> An IQ is a rank against a norming sample. "
            "If scores drift up three points a decade, the average person scored against fifteen-year-old norms "
            "gets about a hundred and four and a half. <bookmark mark='b'/> So a person's score depends on which "
            "edition of the test was used, and when. <bookmark mark='c'/> In the United States, since the Supreme "
            "Court barred executing people with intellectual disability in Atkins versus Virginia in 2002, courts "
            "have argued over whether to correct scores near the cutoff for outdated norms. "
            "<bookmark mark='d'/> It's a cohort effect, deciding a life."
        ) as vo:
            self.play(FadeIn(head), FadeIn(A), FadeIn(tag))
            vo.wait_until("a")
            self.play(Create(c), FadeIn(dot), FadeIn(rows[0]))
            for m, r in zip("bcd", rows[1:]):
                vo.wait_until(m)
                self.play(FadeIn(r, shift=RIGHT * 0.15))
        self.clear_scene()

    def reversal(self):
        head = heading(r"And then it reversed")
        rows = rows_of([
            (r"in Norway, \ Denmark and other countries of northern and western Europe, \ scores of men born from "
             r"the mid-1970s began to fall", WHITE),
            (r"Bernt Bratsberg and Ole Rogeberg, \ 2018: \ 736{,}808 Norwegian conscripts' scores, \ compared "
             r"between brothers in the same families", COHORT),
            (r"the decline appears within families: \ younger brothers score lower than their older brothers did "
             r"at the same age", LOST),
            (r"so not a change in who has children, \ or who arrives: \ something in the environment changed, \ for "
             r"everyone", AGE),
            (r"the same design idea as birth order: \ compare within families, \ and the family's genes and home "
             r"are held fixed", YOU),
        ], 12.4, 24, 0.4).move_to([0, -0.3, 0])
        tag = published_tag(r"Bratsberg \& Rogeberg (2018)")
        with self.voiceover(
            "And then the rise stopped. <bookmark mark='a'/> In Norway, Denmark and other countries of northern and "
            "western Europe, the scores of men born from the mid-1970s began to fall. Some read that as a change "
            "in who was having children. <bookmark mark='b'/> In 2018, Bernt Bratsberg and Ole Rogeberg used the "
            "scores of seven hundred and thirty-six thousand Norwegian conscripts, and compared brothers in the same "
            "families. <bookmark mark='c'/> The decline appears within families: younger brothers score lower than "
            "their older brothers did at the same age. <bookmark mark='d'/> So it isn't a change in who has children "
            "or who arrives. Something in the environment changed, for everyone. <bookmark mark='e'/> It's the same "
            "design idea as the birth-order studies: compare within families, and the family's genes and home are "
            "held fixed. Part 32 takes intelligence up properly."
        ) as vo:
            self.play(FadeIn(head), FadeIn(tag))
            for m, r in zip("abcde", rows):
                vo.wait_until(m)
                self.play(FadeIn(r, shift=RIGHT * 0.15))
        self.clear_scene()

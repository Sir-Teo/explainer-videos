from __future__ import annotations

from videos.psychology.psych54.common import *  # noqa: F403


class Tutoring(VoiceoverScene):
    def construct(self):
        card_section(self, 8, r"Tutoring", r"How big is the tutoring effect, \ really?", scale=("person", "society"))
        self.sizes()
        self.systems()

    def sizes(self):
        head = heading(r"Two sigma, \ measured again")
        A = axes([0.3, 4.7], [0, 2.2], x_length=5.6, y_length=3.0, xticks=None, yticks=[0, 0.5, 1.0, 1.5, 2.0],
                 yfmt=lambda v: f"{v:.1f}", ylabel=r"effect size (SD)", center=[-3.3, 0.3, 0], font_size=12)
        vals = [2.0, 0.79, 0.76, 0.37]
        cols = [GREY_B, PERSON, MODEL, GOOD]
        b = bars(A.ax, [1, 2, 3, 4], vals, cols, width=0.6)
        names = VGroup(*[label(s, font_size=12, color=GREY_A).next_to(A.ax.c2p(i + 1, 0), DOWN, buff=0.12)
                         for i, s in enumerate([r"Bloom, \ 1984", r"human tutors", r"step-based ITS", r"school "
                                                                                                   r"programmes"])])
        rows = rows_of([
            (r"Bloom's figure came from a few short studies with tests aligned to the lessons", GREY_B),
            (r"VanLehn, \ 2011: \ human tutoring about 0.79; \ computer tutors that respond to each step of a "
             r"solution about 0.76", MODEL),
            (r"Nickow, \ Oreopoulos and Quan's 2020 review of randomized trials of school tutoring: \ about 0.37 on "
             r"average, \ largest for teacher and paraprofessional tutors in school hours", GOOD),
            (r"still among the largest effects in education; \ ``replicated, \ smaller'' in the Ledger", YOU),
        ], 6.0, 19, 0.36).move_to([3.4, -0.1, 0])
        tag = published_tag(r"VanLehn (2011); \ Nickow et al.\ (2020)")
        with self.voiceover(
            "How big is the tutoring effect, really? <bookmark mark='a'/> Bloom's two sigma came from a few short "
            "studies, with tests aligned to the lessons. <bookmark mark='b'/> Kurt VanLehn's 2011 review found human "
            "tutoring at about zero point eight, and computer tutors that respond to each step of a solution at "
            "almost the same. <bookmark mark='c'/> A 2020 review of randomized trials of school tutoring, by Andre "
            "Nickow, Philip Oreopoulos and Vincent Quan, found about zero point four on average, largest for teachers "
            "and paraprofessionals tutoring in school hours. <bookmark mark='d'/> That's still among the largest "
            "effects in education. The Ledger says: replicated, smaller."
        ) as vo:
            self.play(FadeIn(head), FadeIn(tag), FadeIn(A), FadeIn(names))
            for i, m in enumerate("abcd"):
                vo.wait_until(m)
                self.play(FadeIn(rows[i]), FadeIn(b[i]))
        self.clear_scene()

    def systems(self):
        chips_section(self, r"How a tutoring system models the learner", [
            (r"the inner loop", r"feedback and hints on each step of a problem, \ as a good human tutor gives", MODEL),
            (r"the outer loop", r"choosing the next problem: \ Part 45's knowledge tracing estimates each skill's "
                                r"mastery", PERSON),
            (r"mastery learning", r"move on when the estimate passes about 0.95, \ not when the time runs out", GOOD),
            (r"what it cannot do", r"motivate, \ notice confusion in a face, \ or build a relationship; \ much of a "
                                   r"human tutor's effect may live there", AUTH),
        ], "How does a tutoring system model the learner? <bookmark mark='a'/> The inner loop gives feedback and hints "
           "on each step of a problem, as a good human tutor does. <bookmark mark='b'/> The outer loop chooses the "
           "next problem, with Part 45's knowledge tracing estimating each skill's mastery. <bookmark mark='c'/> "
           "Mastery learning moves on when the estimate passes about zero point nine five, not when the time runs "
           "out. <bookmark mark='d'/> What it can't do is motivate, notice confusion in a face, or build a "
           "relationship, and much of a human tutor's effect may live there.")

from __future__ import annotations

from videos.psychology.psych54.common import *  # noqa: F403


class Myths(VoiceoverScene):
    def construct(self):
        card_section(self, 7, r"Myths", r"Do people learn best in their own style?", scale=("person", "society"))
        self.styles()
        self.others()

    def styles(self):
        head = heading(r"What a test of learning styles needs")
        A = axes([0.3, 2.7], [0, 1.0], x_length=4.0, y_length=3.0, xticks=None, yticks=None, center=[-4.0, 0.2, 0],
                 font_size=12)
        cross = VGroup(Line(A.ax.c2p(0.7, 0.3), A.ax.c2p(2.3, 0.8), color=PERSON, stroke_width=4),
                       Line(A.ax.c2p(0.7, 0.8), A.ax.c2p(2.3, 0.3), color=MODEL, stroke_width=4))
        lab = VGroup(label(r"taught visually", font_size=13, color=GREY_A).next_to(A.ax.c2p(0.7, 0), DOWN, buff=0.12),
                     label(r"taught verbally", font_size=13, color=GREY_A).next_to(A.ax.c2p(2.3, 0), DOWN, buff=0.12))
        key = VGroup(label(r"``visual learners''", font_size=13, color=MODEL),
                     label(r"``verbal learners''", font_size=13, color=PERSON)).arrange(RIGHT, buff=0.3)
        key.next_to(A, UP, buff=0.2)
        rows = rows_of([
            (r"the meshing hypothesis: \ teaching matched to a learner's preferred style improves learning", WHITE),
            (r"Pashler, \ McDaniel, \ Rohrer and Bjork, \ 2008: \ the test needs this crossover: \ each style learning "
             r"best from its own method", MODEL),
            (r"of the few studies with that design, \ almost none found it; \ several found the opposite pattern or "
             r"none", AUTH),
            (r"people do have preferences; \ teaching to them does not help. \ The content decides the mode: \ maps "
             r"are visual, \ poems are heard", YOU),
        ], 7.2, 19, 0.36).move_to([2.9, -0.1, 0])
        tag = published_tag(r"Pashler et al.\ (2008)")
        with self.voiceover(
            "Do people learn best in their own style? <bookmark mark='a'/> The meshing hypothesis says that teaching "
            "matched to a learner's preferred style improves learning. <bookmark mark='b'/> In 2008 Harold Pashler, "
            "Mark McDaniel, Doug Rohrer and Robert Bjork set out what a test needs: this crossover, with each style "
            "learning best from its own method. <bookmark mark='c'/> Of the few studies with that design, almost none "
            "found it, and several found the opposite pattern, or none. <bookmark mark='d'/> People do have "
            "preferences. Teaching to them doesn't help. The content decides the mode: maps are visual, and poems are "
            "heard."
        ) as vo:
            self.play(FadeIn(head), FadeIn(tag), FadeIn(A), FadeIn(lab))
            vo.wait_until("a")
            self.play(FadeIn(rows[0]))
            vo.wait_until("b")
            self.play(FadeIn(rows[1]), Create(cross), FadeIn(key))
            for m, r in zip("cd", rows[2:]):
                vo.wait_until(m)
                self.play(FadeIn(r, shift=RIGHT * 0.15))
        self.clear_scene()

    def others(self):
        chips_section(self, r"Other myths, \ tested", [
            (r"left and right brains", r"people are not ``left-brained'' or ``right-brained'' learners; \ both "
                                       r"hemispheres work on almost everything (Part 7)", AUTH),
            (r"ten percent of the brain", r"imaging shows nearly all of it active over a day (Part 8)", AUTH),
            (r"laptop notes", r"one study found longhand notes beat laptops on conceptual questions; \ a "
                              r"preregistered replication found no reliable difference: \ contested", PERSON),
            (r"why myths last", r"they flatter learners and teachers, \ and nobody runs the crossover test", MODEL),
        ], "Other myths fare no better. <bookmark mark='a'/> People aren't left-brained or right-brained learners. "
           "Both hemispheres work on almost everything, as Part 7 showed. <bookmark mark='b'/> Nor do we use ten "
           "percent of the brain. Imaging shows nearly all of it active over a day. <bookmark mark='c'/> Laptop "
           "notes are a closer case. One study found longhand notes beat laptops on conceptual questions, and a "
           "preregistered replication found no reliable difference. The Ledger calls it contested. "
           "<bookmark mark='d'/> Myths last because they flatter learners and teachers, and nobody runs the "
           "crossover test.", tag=published_tag(r"Mueller \& Oppenheimer (2014)"))

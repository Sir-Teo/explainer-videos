from __future__ import annotations

from videos.psychology.psych53.common import *  # noqa: F403


class Interviews(VoiceoverScene):
    def construct(self):
        card_section(self, 6, r"The interview", r"Why does a conversation feel so informative?")
        self.noise()
        self.structure()
        self.worked()

    def noise(self):
        d = load("interviews")
        head = heading(r"Noise that feels like signal")
        A = axes([0.3, 5.7], [0, 0.55], x_length=5.6, y_length=3.0, xticks=None, yticks=[0, 0.25, 0.5],
                 yfmt=lambda v: f"{v:.2f}", ylabel=r"validity", center=[-3.3, 0.3, 0], font_size=12)
        keys = ["unstructured", "test", "holistic", "structured", "mechanical"]
        cols = [AUTH, MODEL, PERSON, GOOD, GOOD]
        vals = [d[k] for k in keys]
        b = bars(A.ax, [1, 2, 3, 4, 5], vals, cols, width=0.6)
        names = VGroup(*[label(s, font_size=12, color=GREY_A).next_to(A.ax.c2p(i + 1, 0), DOWN, buff=0.12)
                         for i, s in enumerate([r"unstructured", r"test", r"test + gut", r"structured",
                                                r"test + structured"])])
        nums = VGroup(*[label(f"{v:.2f}", font_size=13, color=c).next_to(A.ax.c2p(i + 1, v), UP, buff=0.08)
                        for i, (v, c) in enumerate(zip(vals, cols))])
        rows = rows_of([
            (r"an unstructured interview sees something real, \ buried in first impressions, \ rapport and the "
             r"interviewer's own tastes", AUTH),
            (r"a recruiter who weighs that impression heavily against a test does slightly worse than the test alone",
             PERSON),
            (r"Dana, \ Dawes and Peterson, \ 2013: \ interviewers formed confident impressions even from interviews "
             r"whose answers were random, \ and preferred them to no interview", MODEL),
            (r"the same information combined by a fixed rule predicts best: \ Part 39's actuarial prediction, \ at "
             r"work", GOOD),
        ], 6.0, 19, 0.34).move_to([3.4, -0.1, 0])
        tag = psyche_tag(r"\texttt{work.interviews}, \ 20{,}000 simulated candidates")
        with self.voiceover(
            "Why does a conversation feel so informative? <bookmark mark='a'/> In Psyche's model, an unstructured "
            "interview sees something real, buried in first impressions, rapport, and the interviewer's own tastes. "
            "Its validity is about zero point one eight. <bookmark mark='b'/> A recruiter who weighs that impression "
            "heavily against a test does slightly worse than the test alone. <bookmark mark='c'/> Jason Dana, Robyn "
            "Dawes and Nathanial Peterson found in 2013 that interviewers formed confident impressions even from "
            "interviews whose answers were random, and preferred having them to having no interview. "
            "<bookmark mark='d'/> The same information combined by a fixed rule predicts best. That's Part 39's "
            "actuarial prediction, at work."
        ) as vo:
            self.play(FadeIn(head), FadeIn(tag), FadeIn(A), FadeIn(names))
            vo.wait_until("a")
            self.play(FadeIn(rows[0]), FadeIn(b[0]), FadeIn(nums[0]), FadeIn(b[1]), FadeIn(nums[1]))
            vo.wait_until("b")
            self.play(FadeIn(rows[1]), FadeIn(b[2]), FadeIn(nums[2]))
            vo.wait_until("c")
            self.play(FadeIn(rows[2]))
            vo.wait_until("d")
            self.play(FadeIn(rows[3]), FadeIn(b[3]), FadeIn(nums[3]), FadeIn(b[4]), FadeIn(nums[4]))
        self.clear_scene()

    def structure(self):
        chips_section(self, r"Structure, \ as the fix", [
            (r"job analysis", r"ask about what the job actually needs, \ from a study of the job", MODEL),
            (r"same questions", r"every candidate gets the same questions, \ in the same order: \ past behaviour "
                                r"(``tell me about a time...'') or situations", PERSON),
            (r"anchored scales", r"rate each answer against written examples of poor, \ fair and good answers", GOOD),
            (r"several raters, \ combined by rule", r"independent ratings, \ averaged, \ before anyone discusses the "
                                                   r"candidate", SYMP),
        ], "Structure is the fix, and it's well understood. <bookmark mark='a'/> Base the questions on a job "
           "analysis, on what the job actually needs. <bookmark mark='b'/> Give every candidate the same questions in "
           "the same order, about past behaviour or about situations they might face. <bookmark mark='c'/> Rate each "
           "answer against written examples of poor, fair and good answers. <bookmark mark='d'/> And use several "
           "independent raters, averaged by rule, before anyone discusses the candidate. Scott Highhouse called the "
           "resistance to all this a stubborn reliance on intuition.", chip_w=4.2, text_w=8.0)

    def worked(self):
        rows_section(self, r"One structured question, \ worked", [
            (r"for a ward nurse: \ ``tell me about a time you noticed a patient getting worse before the monitors "
             r"did''", WHITE),
            (r"anchors written in advance: \ 1, \ waited to be told; \ 3, \ noticed and reported; \ 5, \ "
             r"noticed, \ acted, \ escalated, \ and checked the result", MODEL),
            (r"two interviewers score alone, \ then average; \ a gap of more than a point is discussed against the "
             r"anchors, \ not against impressions", PERSON),
            (r"candidates tend to judge interviews fairer when the questions are visibly about the job", GOOD),
            (r"the cost is an afternoon of writing per role; \ the gain is the largest improvement in validity an "
             r"interview can buy", YOU),
        ], "Here's one structured question, worked. <bookmark mark='a'/> For a ward nurse: tell me about a time you "
           "noticed a patient getting worse before the monitors did. <bookmark mark='b'/> The anchors are written in "
           "advance. One: waited to be told. Three: noticed and reported. Five: noticed, acted, escalated, and checked "
           "the result. <bookmark mark='c'/> Two interviewers score alone, then average, and a gap of more than a "
           "point is discussed against the anchors, not against impressions. <bookmark mark='d'/> Candidates tend to "
           "judge interviews fairer when the questions are visibly about the job. <bookmark mark='e'/> The cost is an "
           "afternoon of writing per role. The gain is the largest improvement in validity an interview can buy.")

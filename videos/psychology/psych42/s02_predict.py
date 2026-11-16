from __future__ import annotations

from videos.psychology.psych42.common import *  # noqa: F403

QUESTIONS = [
    (r"1", r"Smith and Glass, \ 1977, \ pooled 375 studies of psychotherapy. \ The average effect size?", PERSON),
    (r"2", r"Of the antidepressant trials the US regulator had, \ about half were positive. \ What share of the "
           r"published ones were?", MODEL),
    (r"3", r"The correlation between the client-therapist alliance and outcome, \ across nearly 300 studies?", SYMP),
    (r"4", r"By how many sessions have half of clients improved?", GOOD),
]


class Predict(VoiceoverScene):
    def construct(self):
        self.card()
        self.graphs()
        self.quiz()

    def card(self):
        card = chapter_card(1, r"On you: \ two graphs, \ and four numbers", r"Which graph shows therapy working?",
                            lit=(), part=PART, scale=("person",), marr=("what",))
        with self.voiceover("Chapter one. On you: two graphs, and four numbers."):
            self.play(FadeIn(card, shift=UP * 0.2))
        self.clear_scene()

    def graphs(self):
        d = load("arms")
        stage = demo_stage(13.2, 6.0, center=[0, -0.3, 0])
        panels = VGroup()
        for k, (title, lines) in enumerate((
                (r"A: \ clients before and after therapy", ((d["active_pre"], d["active_post"], PERSON),)),
                (r"B: \ therapy, \ and people who waited", ((d["active_pre"], d["active_post"], PERSON),
                                                          (d["waitlist_pre"], d["waitlist_post"], GREY_B))))):
            A = axes([-0.3, 1.3], [10, 26], x_length=4.2, y_length=3.0, xticks=None, yticks=[10, 15, 20, 25],
                     yfmt=lambda v: f"{v:.0f}", ylabel=r"symptoms", font_size=12)
            seg = VGroup()
            for a, b, c in lines:
                seg.add(Line(A.ax.c2p(0, a), A.ax.c2p(1, b), color=c, stroke_width=4),
                        Dot(A.ax.c2p(0, a), color=c), Dot(A.ax.c2p(1, b), color=c))
            ticks = VGroup(label(r"start", font_size=12, color=GREY_B).next_to(A.ax.c2p(0, 10), DOWN, buff=0.12),
                           label(r"end", font_size=12, color=GREY_B).next_to(A.ax.c2p(1, 10), DOWN, buff=0.12))
            t = label(title, font_size=17, color=WHITE).next_to(A, UP, buff=0.15)
            panels.add(VGroup(A, seg, ticks, t))
        panels.arrange(RIGHT, buff=1.4).move_to([0, 0.0, 0])
        ask = wrapped_label(r"which graph shows that the therapy worked?", 10.0, 22, YOU).move_to([0, -2.7, 0])
        ans = wrapped_label(r"only B: \ A would look the same if therapy did nothing, \ since people enrol at their "
                            r"worst and improve anyway", 11.0, 20, GOOD).move_to([0, -2.7, 0])
        with self.voiceover(
            "First, two graphs. <bookmark mark='a'/> In graph A, clients start therapy with high symptom scores and "
            "end much lower. <bookmark mark='b'/> In graph B, the same clients, and a group who waited for the same "
            "time. Both improve; the clients in therapy improve more. <bookmark mark='c'/> Which graph shows that the "
            "therapy worked? <bookmark mark='d'/> Only B. Graph A would look just the same if therapy did nothing, "
            "because people come for help at their worst, and improve anyway. The waiting group shows how much."
        ) as vo:
            self.play(FadeIn(stage))
            vo.wait_until("a")
            self.play(FadeIn(panels[0]))
            vo.wait_until("b")
            self.play(FadeIn(panels[1]))
            vo.wait_until("c")
            self.play(FadeIn(ask))
            vo.wait_until("d")
            self.play(FadeOut(ask), FadeIn(ans))
        self.wait(1.0)
        self.clear_scene()

    def quiz(self):
        stage = demo_stage(13.2, 6.0, center=[0, -0.3, 0])
        rows = VGroup()
        for n, q, c in QUESTIONS:
            rows.add(VGroup(label(n, font_size=34, color=c), wrapped_label(q, 9.4, 22, WHITE),
                            label(r"\underline{\hspace{1.2cm}}", font_size=26, color=YOU)).arrange(RIGHT, buff=0.35))
        rows.arrange(DOWN, aligned_edge=LEFT, buff=0.4).move_to([0, -0.3, 0])
        with self.voiceover(
            "Now four numbers to write down before the part answers them. <bookmark mark='a'/> One: Smith and Glass "
            "pooled three hundred and seventy-five studies of psychotherapy. What was the average effect size? "
            "<bookmark mark='b'/> Two: of the antidepressant trials the American regulator held, about half were "
            "positive. What share of the published ones were? <bookmark mark='c'/> Three: across nearly three "
            "hundred studies, what's the correlation between the client-therapist alliance and outcome? "
            "<bookmark mark='d'/> And four: by how many sessions have half of clients improved? Pause here, and "
            "write them down."
        ) as vo:
            self.play(FadeIn(stage))
            for m, r in zip("abcd", rows):
                vo.wait_until(m)
                self.play(FadeIn(r, shift=RIGHT * 0.15))
        self.wait(4.0)
        self.clear_scene()

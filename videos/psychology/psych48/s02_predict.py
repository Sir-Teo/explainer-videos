from __future__ import annotations

from videos.psychology.psych48.common import *  # noqa: F403

QUESTIONS = [
    (r"1", r"A learner's true learning rate is 0.4. \ From 200 choices, \ how close will a fit come, \ typically?",
     PERSON),
    (r"2", r"Data from a learner who also tends to repeat choices. \ How often does model comparison pick the right "
           r"model?", MODEL),
    (r"3", r"Each of 60 people improves exponentially. \ What curve fits their average best?", AUTH),
    (r"4", r"Thirty people, \ 60 trials each: \ by how much does fitting them as a population cut the error in each "
           r"person's learning rate?", GOOD),
]


class Predict(VoiceoverScene):
    def construct(self):
        self.card()
        self.bandit()
        self.quiz()

    def card(self):
        card = chapter_card(1, r"On you: \ your learning rate, \ and four numbers", r"How much should you trust a "
                            r"fitted parameter?", lit=(), part=PART, scale=("person",), marr=("what",))
        with self.voiceover("Chapter one. On you: your learning rate, and four numbers."):
            self.play(FadeIn(card, shift=UP * 0.2))
        self.clear_scene()

    def bandit(self):
        d = load("example")
        stage = demo_stage(13.2, 6.0, center=[0, -0.3, 0])
        n = len(d["choices"])
        A = axes([0, n], [-0.2, 1.2], x_length=8.6, y_length=2.2, xticks=[0, 50, 100, 150, 200], yticks=[0, 1],
                 xfmt=lambda v: f"{v:.0f}", yfmt=lambda v: [r"left", r"right"][int(v)], xlabel=r"trial",
                 center=[-1.6, 0.9, 0], font_size=12)
        marks = VGroup(*[Dot(A.ax.c2p(t, d["choices"][t]), radius=0.03, color=GOOD if d["rewards"][t] else AUTH)
                         for t in range(n)])
        rev = DashedLine(A.ax.c2p(100, -0.2), A.ax.c2p(100, 1.2), color=YOU, stroke_width=2)
        rv_l = label(r"the arms swap", font_size=13, color=YOU).next_to(A.ax.c2p(100, 1.2), UP, buff=0.05)
        rows = rows_of([
            (r"Part 17's bandit, \ played by Psyche: \ two arms, \ one pays 70\% of the time, \ and halfway through "
             r"they swap", WHITE),
            (rf"the Q-learner's fit: \ learning rate {d['q_params'][0]:.2f}, \ inverse temperature "
             rf"{d['q_params'][1]:.1f}; \ the truth was 0.3 and 5", MODEL),
            (r"on the site: \ play it yourself, \ see your own learning rate fitted, \ and beside it how well that "
             r"rate can be recovered from 200 choices", YOU),
        ], 11.6, 19, 0.3).move_to([0, -1.7, 0])
        with self.voiceover(
            "First, Part 17's bandit again. <bookmark mark='a'/> Psyche plays two arms; one pays seventy percent of "
            "the time, and halfway through they swap. Each dot is a choice, green when it paid. "
            "<bookmark mark='b'/> Fit the Q-learner, and the learning rate comes out at about zero point four, with "
            "an inverse temperature near five. The truth was zero point three and five. <bookmark mark='c'/> On the "
            "course site you can play it yourself, see your own learning rate fitted, and beside it how well a rate "
            "like yours can be recovered from two hundred choices."
        ) as vo:
            self.play(FadeIn(stage), FadeIn(A), FadeIn(rev), FadeIn(rv_l))
            vo.wait_until("a")
            self.play(FadeIn(rows[0]), LaggedStart(*[FadeIn(m) for m in marks], lag_ratio=0.01), run_time=2.5)
            vo.wait_until("b")
            self.play(FadeIn(rows[1]))
            vo.wait_until("c")
            self.play(FadeIn(rows[2]))
        self.wait(1.0)
        self.clear_scene()

    def quiz(self):
        stage = demo_stage(13.2, 6.0, center=[0, -0.3, 0])
        rows = VGroup()
        for n, q, c in QUESTIONS:
            rows.add(VGroup(label(n, font_size=34, color=c), wrapped_label(q, 9.4, 21, WHITE),
                            label(r"\underline{\hspace{1.2cm}}", font_size=26, color=YOU)).arrange(RIGHT, buff=0.35))
        rows.arrange(DOWN, aligned_edge=LEFT, buff=0.38).move_to([0, -0.3, 0])
        with self.voiceover(
            "Now four numbers. <bookmark mark='a'/> One: a learner's true learning rate is zero point four. From two "
            "hundred choices, how close will a fit come, typically? <bookmark mark='b'/> Two: data from a learner who "
            "also tends to repeat choices. How often does model comparison pick the right model? "
            "<bookmark mark='c'/> Three: each of sixty people improves exponentially with practice. What curve fits "
            "their average best? <bookmark mark='d'/> And four: thirty people, sixty trials each. By how much does "
            "fitting them as a population cut the error in each person's learning rate? Pause here, and write them "
            "down."
        ) as vo:
            self.play(FadeIn(stage))
            for m, r in zip("abcd", rows):
                vo.wait_until(m)
                self.play(FadeIn(r, shift=RIGHT * 0.15))
        self.wait(1.0)
        self.clear_scene()

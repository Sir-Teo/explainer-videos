from __future__ import annotations

from videos.psychology.psych47.common import *  # noqa: F403

QUESTIONS = [
    (r"1", r"Thirty people, \ twenty words, \ no effect, \ analysed by participants only: \ the false-positive rate?",
     AUTH),
    (r"2", r"In the cloud you just saw, \ when one person's x rises, \ does their y rise or fall?", PERSON),
    (r"3", r"Two traits correlate 0.6 across people. \ What share of people show about that correlation within "
           r"themselves, \ over time?", MODEL),
    (r"4", r"A person's true day-to-day inertia is 0.4. \ Estimated from 20 days, \ on average it comes out as?", GOOD),
]


class Predict(VoiceoverScene):
    def construct(self):
        self.card()
        self.cloud()
        self.quiz()

    def card(self):
        card = chapter_card(1, r"On you: \ one cloud, \ and four numbers", r"Which way does it go for one person?",
                            lit=(), part=PART, scale=("person",), marr=("what",))
        with self.voiceover("Chapter one. On you: one cloud, and four numbers."):
            self.play(FadeIn(card, shift=UP * 0.2))
        self.clear_scene()

    def cloud(self):
        d = load("simpson")
        stage = demo_stage(13.2, 6.0, center=[0, -0.3, 0])
        A = axes([-6, 6], [-7, 7], x_length=6.0, y_length=4.4, xticks=[-4, 0, 4], yticks=[-5, 0, 5],
                 xfmt=lambda v: f"{v:g}", yfmt=lambda v: f"{v:g}", xlabel=r"x", ylabel=r"y", center=[-2.4, -0.4, 0],
                 font_size=13)
        dots = scatter(A.ax, d["x"], d["y"], GREY_A, radius=0.05)
        xx = np.linspace(-6, 6, 50)
        fit = curve_in(A.ax, xx, d["pooled"] * xx + (d["y"].mean() - d["pooled"] * d["x"].mean()), AUTH, stroke_width=3)
        rows = rows_of([
            (r"each dot is one occasion for one person; \ twelve people, \ fifteen occasions each", WHITE),
            (rf"across everyone, \ y falls as x rises: \ slope {d['pooled']:.1f}", AUTH),
            (r"now guess: \ for one person, \ on a day when their x is higher than usual, \ is their y higher or "
             r"lower?", YOU),
            (r"on the site: \ the same cloud, \ coloured by person", MODEL),
        ], 4.0, 18, 0.34).move_to([4.2, -0.3, 0])
        with self.voiceover(
            "First, a cloud of points. <bookmark mark='a'/> Each dot is one occasion for one person: twelve people, "
            "fifteen occasions each. <bookmark mark='b'/> Across everyone, y falls as x rises. <bookmark mark='c'/> Now "
            "guess. For one person, on a day when their x is higher than usual, is their y higher or lower? "
            "<bookmark mark='d'/> On the course site you can see the same cloud, coloured by person."
        ) as vo:
            self.play(FadeIn(stage), FadeIn(A), FadeIn(dots))
            vo.wait_until("a")
            self.play(FadeIn(rows[0]))
            vo.wait_until("b")
            self.play(FadeIn(rows[1]), Create(fit))
            vo.wait_until("c")
            self.play(FadeIn(rows[2]))
            vo.wait_until("d")
            self.play(FadeIn(rows[3]))
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
            "Now four numbers. <bookmark mark='a'/> One: thirty people, twenty words, no effect, analysed by "
            "participants only. What's the false-positive rate? <bookmark mark='b'/> Two: in the cloud you just saw, "
            "when one person's x rises, does their y rise or fall? <bookmark mark='c'/> Three: two traits correlate "
            "zero point six across people. What share of people show about that correlation within themselves, over "
            "time? <bookmark mark='d'/> And four: a person's true day-to-day inertia is zero point four. Estimated "
            "from twenty days, what does it come out as, on average? Pause here, and write them down."
        ) as vo:
            self.play(FadeIn(stage))
            for m, r in zip("abcd", rows):
                vo.wait_until(m)
                self.play(FadeIn(r, shift=RIGHT * 0.15))
        self.wait(1.0)
        self.clear_scene()

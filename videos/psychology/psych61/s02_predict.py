from __future__ import annotations

from videos.psychology.psych61.common import *  # noqa: F403

CHOICES = [
    r"text or call", r"one reminder or three", r"named sender or not", r"a deadline or none",
    r"framed as gain or loss", r"sent morning or evening", r"short or long", r"online or in person",
    r"students or adults", r"one country or another",
]

QUESTIONS = [
    (r"1", r"160 teams, \ thousands of variables, \ predicting a child's school grades: \ the best held-out "
           r"$R^2$?", PERSON),
    (r"2", r"One effect, \ 40 labs, \ no true difference between labs. \ How far apart are the labs' estimates?",
     MODEL),
    (r"3", r"A million self-selected volunteers. \ Does the bias shrink with the interval?", AUTH),
    (r"4", r"Labs copied in proportion to their publications, \ for 200 generations: \ the share of published "
           r"positives that are false?", GOOD),
]


class Predict(VoiceoverScene):
    def construct(self):
        card_section(self, 1, r"On you: \ a space of experiments, \ and four numbers", r"Which experiment would you "
                     r"run?")
        self.space()
        self.quiz()

    def space(self):
        d = load("space")
        head = heading(r"Ten design choices, \ 1,024 experiments")
        chips = VGroup(*[label(rf"{i + 1}.\ {c}", font_size=17, color=WHITE) for i, c in enumerate(CHOICES)])
        chips.arrange(DOWN, aligned_edge=LEFT, buff=0.16).move_to([-4.5, -0.3, 0])
        eff = np.asarray(d["effects"])
        A = axes([-1.2, 1.6], [0, 140], x_length=6.0, y_length=3.0, xticks=[-1, 0, 0.5, 1], yticks=None,
                 xfmt=lambda v: f"{v:g}", xlabel=r"true effect (SD units) of a reminder in each cell",
                 center=[2.4, 0.3, 0], font_size=12)
        hist, edges = np.histogram(eff, bins=28, range=(-1.2, 1.6))
        bs = bars(A.ax, 0.5 * (edges[1:] + edges[:-1]), hist, MODEL, width=0.09)
        zero = DashedLine(A.ax.c2p(0, 0), A.ax.c2p(0, 140), color=GREY_B, stroke_width=1.5)
        foot = wrapped_label(rf"one cell, \ one study: \ the same question, \ a different answer; \ "
                             rf"{100 * d['share_negative']:.0f}\% of cells go the other way", 6.2, 19, YOU)
        foot.next_to(A, DOWN, buff=0.35)
        with self.voiceover(
            "First, an experiment on you. You're testing whether a reminder raises attendance at appointments, "
            "Part 55's question. <bookmark mark='a'/> You must make ten design choices: text or call, one reminder or "
            "three, a named sender or not, and so on. Each choice has two options, so there are a thousand and "
            "twenty-four possible experiments. Pick one in your head, as a standard study does. "
            "<bookmark mark='b'/> Now here's the true effect in every one of those experiments, in a world Psyche "
            "built. <bookmark mark='c'/> One cell, one study: the same question, a different answer. More than a "
            "quarter of the cells go the other way. Which one did you pick?"
        ) as vo:
            self.play(FadeIn(head))
            vo.wait_until("a")
            self.play(LaggedStart(*[FadeIn(c, shift=RIGHT * 0.1) for c in chips], lag_ratio=0.3), run_time=4.0)
            vo.wait_until("b")
            self.play(FadeIn(A), Create(zero), LaggedStart(*[GrowFromEdge(b, DOWN) for b in bs], lag_ratio=0.03))
            vo.wait_until("c")
            self.play(FadeIn(foot))
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
            "Now four numbers. <bookmark mark='a'/> One: a hundred and sixty teams with thousands of variables predict "
            "a child's school grades. What's the best held-out R squared? <bookmark mark='b'/> Two: one effect is run "
            "in forty labs, with no true difference between them. How far apart are the labs' estimates? "
            "<bookmark mark='c'/> Three: a million self-selected volunteers. Does the bias shrink along with the "
            "interval? <bookmark mark='d'/> And four: labs are copied in proportion to their publications for two "
            "hundred generations. What share of the published positive results are false? Pause here, and write "
            "them down."
        ) as vo:
            self.play(FadeIn(stage))
            for m, r in zip("abcd", rows):
                vo.wait_until(m)
                self.play(FadeIn(r, shift=RIGHT * 0.15))
        self.wait(1.0)
        self.clear_scene()

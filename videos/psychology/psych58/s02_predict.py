from __future__ import annotations

from videos.psychology.psych58.common import *  # noqa: F403

QUESTIONS = [
    (r"1", r"After staring at lines tilted 20 degrees clockwise, \ a vertical line looks tilted which way, \ and by "
           r"about how much?", PERSON),
    (r"2", r"Vertical and horizontal are the commonest orientations in the world. \ Is a line near vertical seen "
           r"pulled toward vertical, \ or pushed away?", MODEL),
    (r"3", r"A neuron has 20 response levels for contrast. \ Which contrasts should get the most levels?", AUTH),
    (r"4", r"You decide by drawing samples from your beliefs, \ and each sample costs time. \ The best number of "
           r"samples?", GOOD),
]


def grating(center, radius: float = 1.3, angle: float = 0.0, spacing: float = 0.2, width: float = 7.0) -> VGroup:
    """Parallel lines filling a circle; ``angle`` in degrees, clockwise from vertical."""
    a = np.deg2rad(angle)
    d = np.array([np.sin(a), np.cos(a), 0.0])
    n = np.array([np.cos(a), -np.sin(a), 0.0])
    c = np.asarray(center, float)
    out = VGroup()
    t = -radius + spacing / 2
    while t < radius:
        h = np.sqrt(max(radius ** 2 - t ** 2, 0.0))
        out.add(Line(c + t * n - h * d, c + t * n + h * d, color=WHITE, stroke_width=width))
        t += spacing
    out.add(Circle(radius=radius, color=GREY_B, stroke_width=2).move_to(c))
    return out


class Predict(VoiceoverScene):
    def construct(self):
        card_section(self, 1, r"On you: \ an after-effect, \ and four numbers", r"Can a code that adapts fool you?")
        self.tilt()
        self.quiz()

    def tilt(self):
        top, bot = [0, 1.75, 0], [0, -1.75, 0]
        adapt = VGroup(grating(top, angle=15), grating(bot, angle=-15))
        test = VGroup(grating(top, angle=0), grating(bot, angle=0))
        bar = Rectangle(width=0.9, height=0.08, fill_color=YOU, fill_opacity=1, stroke_width=0).move_to([0, 0, 0])
        note = wrapped_label(r"look at the yellow bar; \ let your eyes drift slowly along it", 3.6, 20, YOU)
        note.move_to([-4.8, 0, 0])
        later = wrapped_label(r"now: \ are these lines vertical?", 3.6, 22, WHITE).move_to([4.8, 0, 0])
        with self.voiceover(
            "First, an experiment on you. <bookmark mark='a'/> Look at the small yellow bar between the two circles, "
            "and let your eyes drift slowly from one end of it to the other. Keep looking. The top lines lean one "
            "way, the bottom lines the other. Stay on the bar for the next half minute. Your orientation-tuned "
            "neurons are adapting, turning down their gain for the orientations they've been shown. Keep your eyes "
            "on the bar. It's the same mechanism that makes a waterfall's rocks seem to rise when you look away. "
            "<bookmark mark='b'/> Now. Are these lines vertical?"
        ) as vo:
            self.play(FadeIn(bar))
            vo.wait_until("a")
            self.play(FadeIn(adapt), FadeIn(note))
            vo.wait_until("b")
            self.remove(adapt)
            self.add(test)
            self.play(FadeIn(later), run_time=0.3)
        self.wait(4.0)
        explain = rows_of([
            (r"they are; \ most people see the top tilted to the left and the bottom to the right, \ away from what "
             r"they adapted to", WHITE),
            (r"the tilt after-effect: \ adapted units respond less, \ and a readout that assumes they did not is "
             r"pushed away", MODEL),
            (r"chapter 4 predicts its size from an efficient code", GOOD),
        ], 3.8, 18, 0.3).move_to([4.6, -0.2, 0])
        with self.voiceover(
            "They are vertical. <bookmark mark='a'/> Most people see the top lines tilted to the left and the bottom "
            "lines to the right, away from what they adapted to. <bookmark mark='b'/> It's the tilt after-effect. "
            "The adapted units respond less, and a readout that assumes they didn't is pushed away from the adapter. "
            "<bookmark mark='c'/> Chapter four predicts its size from an efficient code."
        ) as vo:
            self.play(FadeOut(later), FadeOut(note))
            for m, r in zip("abc", explain):
                vo.wait_until(m)
                self.play(FadeIn(r, shift=RIGHT * 0.15))
        self.clear_scene()

    def quiz(self):
        stage = demo_stage(13.2, 6.0, center=[0, -0.3, 0])
        rows = VGroup()
        for n, q, c in QUESTIONS:
            rows.add(VGroup(label(n, font_size=34, color=c), wrapped_label(q, 9.4, 21, WHITE),
                            label(r"\underline{\hspace{1.2cm}}", font_size=26, color=YOU)).arrange(RIGHT, buff=0.35))
        rows.arrange(DOWN, aligned_edge=LEFT, buff=0.38).move_to([0, -0.3, 0])
        with self.voiceover(
            "Now four numbers. <bookmark mark='a'/> One: after staring at lines tilted twenty degrees clockwise, a "
            "vertical line looks tilted which way, and by about how much? <bookmark mark='b'/> Two: vertical and "
            "horizontal are the commonest orientations in the world. Is a line near vertical seen pulled toward "
            "vertical, or pushed away? <bookmark mark='c'/> Three: a neuron has twenty response levels for contrast. "
            "Which contrasts should get the most levels? <bookmark mark='d'/> And four: you decide by drawing samples "
            "from your beliefs, and each sample costs time. What's the best number of samples? Pause here, and write "
            "them down."
        ) as vo:
            self.play(FadeIn(stage))
            for m, r in zip("abcd", rows):
                vo.wait_until(m)
                self.play(FadeIn(r, shift=RIGHT * 0.15))
        self.wait(1.0)
        self.clear_scene()

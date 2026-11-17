from __future__ import annotations

from videos.psychology.psych41.common import *  # noqa: F403

QUESTIONS = [
    (r"1", r"In twin studies, \ what share of the variation in risk for schizophrenia is put down to genes?", PERSON),
    (r"2", r"Of US soldiers addicted to heroin in Vietnam, \ what share were addicted again within a year of coming "
           r"home?", MODEL),
    (r"3", r"A Danish study of vaccination and autism: \ how many children did it follow?", SYMP),
    (r"4", r"In the largest ADHD trial, \ medication beat behavioural treatment at 14 months. \ How much of that "
           r"advantage was left at three years?", GOOD),
]


def shaded_disc(light_up: bool, radius: float = 0.36) -> Circle:
    """A disc shaded light-to-dark: lit from above it reads as a bump, from below as a dent."""
    top, bottom = ("#F2F2F2", "#202020") if light_up else ("#202020", "#F2F2F2")
    disc = Circle(radius=radius, stroke_width=0).set_fill([bottom, top], opacity=1)
    disc.set_sheen_direction(UP)
    return disc


class Predict(VoiceoverScene):
    def construct(self):
        self.card()
        self.shading()
        self.quiz()

    def card(self):
        card = chapter_card(1, r"On you: \ bumps, \ dents, \ and four numbers", r"Which way is the light?", lit=(),
                            part=PART, scale=("person",), marr=("what",))
        with self.voiceover("Chapter one. On you: bumps, dents, and four numbers."):
            self.play(FadeIn(card, shift=UP * 0.2))
        self.clear_scene()

    def shading(self):
        stage = demo_stage(13.2, 6.0, center=[0, -0.3, 0])
        rng = np.random.default_rng(41)
        ups = rng.random(24) < 0.5
        discs = VGroup(*[shaded_disc(bool(u)) for u in ups]).arrange_in_grid(4, 6, buff=0.35).move_to([0, -0.4, 0])
        ask = wrapped_label(r"which discs bulge toward you, \ and which are dents?", 10.0, 22, GREY_A).move_to(
            [0, -2.75, 0])
        bumps = VGroup(*[SurroundingRectangle(d, color=GOOD, buff=0.06) for d, u in zip(discs, ups) if u])
        note = wrapped_label(r"lit from above: \ bumps; \ lit from below: \ dents; \ turn the page upside down and "
                             r"they swap", 11.0, 20, YOU).move_to([0, 2.15, 0])
        with self.voiceover(
            "First, try this. <bookmark mark='a'/> Some of these discs look like bumps, bulging toward you, and some "
            "like dents. Which are which? <bookmark mark='b'/> The bumps are the discs lit from above. The dents are "
            "the same discs, upside down. Nothing on the screen says which way the light comes from. "
            "<bookmark mark='c'/> Your visual system assumes it: a prior that light comes from above, learned from a "
            "world lit by the sun. Turn your head, or the screen, upside down, and the bumps and dents swap. It's the "
            "hollow mask's lesson in miniature. What you see is evidence weighed against expectation."
        ) as vo:
            self.play(FadeIn(stage))
            vo.wait_until("a")
            self.play(FadeIn(discs), FadeIn(ask))
            vo.wait_until("b")
            self.play(LaggedStart(*[Create(b) for b in bumps], lag_ratio=0.1), run_time=2.0)
            vo.wait_until("c")
            self.play(FadeIn(note))
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
            "Now four numbers to write down before the part answers them. <bookmark mark='a'/> One: in twin "
            "studies, what share of the variation in risk for schizophrenia is put down to genes? "
            "<bookmark mark='b'/> Two: of American soldiers addicted to heroin in Vietnam, what share were addicted "
            "again within a year of coming home? <bookmark mark='c'/> Three: a Danish study of vaccination and "
            "autism. How many children did it follow? <bookmark mark='d'/> And four: in the largest trial for ADHD, "
            "medication beat behavioural treatment at fourteen months. How much of that advantage was left at three "
            "years? Pause here, and write them down."
        ) as vo:
            self.play(FadeIn(stage))
            for m, r in zip("abcd", rows):
                vo.wait_until(m)
                self.play(FadeIn(r, shift=RIGHT * 0.15))
        self.wait(4.0)
        self.clear_scene()

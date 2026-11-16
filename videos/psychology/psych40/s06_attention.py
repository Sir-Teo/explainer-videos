from __future__ import annotations

from videos.psychology.psych40.common import *  # noqa: F403


class Attention(VoiceoverScene):
    def construct(self):
        self.card()
        self.bias()

    def card(self):
        card = chapter_card(5, r"Attention to threat", r"Can a reaction-time task find, \ or fix, \ anxiety?",
                            lit={2015: r"Cristea et al."}, part=PART, scale=("person",), marr=("what",))
        with self.voiceover("Chapter five. Attention to threat."):
            self.play(FadeIn(card, shift=UP * 0.2))
        self.clear_scene()

    def bias(self):
        head = heading(r"A bias, \ a measure and a treatment")
        A = axes([-3, 3], [-3, 3], x_length=3.6, y_length=3.0, xticks=None, yticks=None,
                 xlabel=r"bias score, \ session 1", ylabel=r"session 2", center=[-4.0, -0.1, 0], font_size=13)
        rng = np.random.default_rng(40)
        x = rng.normal(size=80)
        y = 0.15 * x + np.sqrt(1 - 0.15 ** 2) * rng.normal(size=80)
        pts = scatter(A.ax, x, y, SYMP, radius=0.045)
        note = label(r"schematic: \ test-retest $r \approx 0.15$", font_size=13, color=GREY_B).next_to(A, DOWN,
                                                                                                  buff=0.3)
        rows = rows_of([
            (r"in the dot-probe task, \ anxious groups on average find the dot faster where a threat word was: \ "
             r"attention is drawn to threat", WHITE),
            (r"but a person's bias score barely correlates with their own score a week later: \ the measure is too "
             r"unreliable to diagnose anyone (Part 3)", AUTH),
            (r"attention-bias modification tried to train the bias away, \ by putting the dot where the neutral "
             r"word was", PERSON),
            (r"Cristea, \ Kok and Cuijpers, \ 2015: \ in a meta-analysis, \ the small effects on anxiety disappeared "
             r"after correcting for bias in the literature", MODEL),
            (r"a group difference is not an individual measure, \ and a mechanism is not yet a treatment", YOU),
        ], 7.4, 19, 0.34).move_to([2.6, -0.2, 0])
        tag = published_tag(r"Cristea, \ Kok \& Cuijpers (2015)")
        with self.voiceover(
            "Back to the dot-probe trial. <bookmark mark='a'/> Anxious groups, on average, find the dot faster where "
            "a threat word was. Their attention is drawn to threat. <bookmark mark='b'/> But one person's bias score "
            "barely correlates with their own score a week later. As Part 3 showed, a measure that unreliable can't "
            "diagnose anyone. <bookmark mark='c'/> Attention-bias modification tried to train the bias away, by "
            "always putting the dot where the neutral word was. <bookmark mark='d'/> In 2015 Ioana Cristea and "
            "colleagues meta-analysed the trials. The small effects on anxiety disappeared after correcting for bias "
            "in the literature. <bookmark mark='e'/> A group difference isn't an individual measure, and a mechanism "
            "isn't yet a treatment."
        ) as vo:
            self.play(FadeIn(head), FadeIn(tag))
            vo.wait_until("a")
            self.play(FadeIn(rows[0]))
            vo.wait_until("b")
            self.play(FadeIn(rows[1]), FadeIn(A), FadeIn(pts), FadeIn(note))
            for m, r in zip("cde", rows[2:]):
                vo.wait_until(m)
                self.play(FadeIn(r, shift=RIGHT * 0.15))
        self.clear_scene()

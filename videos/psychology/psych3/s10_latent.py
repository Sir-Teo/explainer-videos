from __future__ import annotations

import numpy as np

from videos.psychology.psych3.common import *  # noqa: F403

SYMPTOMS = [r"poor sleep", r"fatigue", r"poor concentration", r"low mood", r"loss of interest", r"worry"]
NET, CAUSE = "#7EC8F5", "#F2C14E"


def boxed(text, color=OBS, font_size=22):
    t = label(text, font_size=font_size, color=WHITE)
    return VGroup(SurroundingRectangle(t, color=color, buff=0.13, stroke_width=2, corner_radius=0.08), t)


class Latent(VoiceoverScene):
    def construct(self):
        self.card()
        self.pictures()
        self.same()

    def card(self):
        card = chapter_card(9, r"What is a construct?", r"A hidden cause, or a name for a pattern?", lit=(),
                            part=PART, scale=("person",), marr=("what", "how"))
        with self.voiceover(
            "Chapter nine. What is a construct?"
        ):
            self.play(FadeIn(card, shift=UP * 0.2))
        self.clear_scene()

    def pictures(self):
        head = heading(r"Six things that go together: \ two stories about why")
        # left: one hidden cause, with the six items round it
        l_title = label(r"one hidden cause", font_size=32, color=CAUSE).move_to([-3.6, 2.45, 0])
        l_ring = [np.array([-3.6 + 2.5 * np.cos(a), -0.35 + 1.75 * np.sin(a), 0]) for a in
                  np.pi / 2 - np.arange(6) * np.pi / 3]
        l_items = VGroup(*[boxed(s_, font_size=21).move_to(pos) for s_, pos in zip(SYMPTOMS, l_ring)])
        cause = VGroup(DashedVMobject(Ellipse(width=2.2, height=0.85, color=CAUSE, stroke_width=3), num_dashes=28),
                       label(r"depression", font_size=26, color=CAUSE)).move_to([-3.6, -0.35, 0])
        l_arrows = VGroup(*[Arrow(cause.get_center(), it.get_center(), color=CAUSE, stroke_width=3, buff=0.62,
                                  max_tip_length_to_length_ratio=0.2) for it in l_items])
        l_cap = wrapped_label(r"the symptoms go together because they share a cause; \ the cause is what a score "
                              r"estimates", 5.6, 24, GREY_A).move_to([-3.6, -2.95, 0])
        # right: a network
        r_title = label(r"they cause one another", font_size=32, color=NET).move_to([3.6, 2.45, 0])
        ring = [np.array([3.6 + 2.5 * np.cos(a), -0.35 + 1.75 * np.sin(a), 0]) for a in
                np.pi / 2 - np.arange(6) * np.pi / 3]
        r_items = VGroup(*[boxed(s_, color=NET, font_size=21).move_to(pos) for s_, pos in zip(SYMPTOMS, ring)])
        r_arrows = VGroup()
        for i in range(6):
            a, b = r_items[i], r_items[(i + 1) % 6]
            r_arrows.add(Arrow(a.get_center(), b.get_center(), color=NET, stroke_width=3, buff=0.5,
                               max_tip_length_to_length_ratio=0.15))
        for i, j in ((0, 3), (1, 4), (2, 5)):
            r_arrows.add(DoubleArrow(r_items[i].get_center(), r_items[j].get_center(), color=NET, stroke_width=2,
                                     buff=0.8, stroke_opacity=0.45, max_tip_length_to_length_ratio=0.06))
        r_cap = wrapped_label(r"no hidden cause; \ ``depression'' is the name of the tangle", 5.6, 24, GREY_A)
        r_cap.move_to([3.6, -2.95, 0])
        divider = DashedLine([0, 2.7, 0], [0, -3.3, 0], color=GREY_D, stroke_width=2)
        tag = note(r"schematic").to_corner(UR, buff=0.2)
        with self.voiceover(
            "All through this part we've spoken as if a score estimates something inside the person: a true "
            "score, a trait, a construct. It's time to ask what kind of thing that is, and there are two serious "
            "answers. <bookmark mark='a'/> Take six complaints that tend to arrive together: poor sleep, fatigue, "
            "poor concentration, low mood, loss of interest, worry. <bookmark mark='b'/> The first story says "
            "they go together because they have a common cause. There's a condition, depression, that you can't "
            "see directly, and it produces all six, the way an infection produces a fever and a cough. On this "
            "story the questionnaire's total estimates how much of the hidden thing you have. This is the "
            "picture behind everything in this part: the true score, alpha, the factor analysis we reach in "
            "Part 32. <bookmark mark='c'/> The second story has no hidden thing. You sleep badly, so you're "
            "tired. You're tired, so you can't concentrate. You fall behind, and your mood drops, and you lie "
            "awake worrying about it. The complaints cause one another. Depression is just the name for the "
            "tangle when it gets going."
        ) as vo:
            self.play(FadeIn(head), FadeIn(tag))
            vo.wait_until("a")
            self.play(LaggedStart(*[FadeIn(it) for it in l_items], lag_ratio=0.25), run_time=3.5)
            vo.wait_until("b")
            self.play(FadeIn(l_title), FadeIn(cause), LaggedStart(*[GrowArrow(a) for a in l_arrows], lag_ratio=0.1),
                      run_time=2.5)
            self.play(FadeIn(l_cap))
            vo.wait_until("c")
            self.play(Create(divider), FadeIn(r_title), FadeIn(r_items))
            self.play(LaggedStart(*[GrowArrow(a) for a in r_arrows[:6]], lag_ratio=0.5), run_time=9.0)
            self.play(FadeIn(r_arrows[6:]), FadeIn(r_cap))
        self.clear_scene()

    def same(self):
        d = load("latent")
        head = heading(r"The two stories, and the correlations each implies")
        left = heatmap(d["factor"], cell=0.7, font_size=21, diagonal=False).move_to([-4.45, 0.05, 0])
        right = heatmap(d["network"], cell=0.7, font_size=21, diagonal=False).move_to([0.75, 0.05, 0])
        l_cap = VGroup(label(r"one hidden cause", font_size=28, color=CAUSE),
                       label(rf"each item loads {r2(d['loading'])} on it", font_size=22, color=GREY_A))
        l_cap.arrange(DOWN, buff=0.08).next_to(left, UP, buff=0.2)
        r_cap = VGroup(label(r"they cause one another", font_size=28, color=NET),
                       label(rf"each pushes each other one with weight {d['b']:.2f}", font_size=22, color=GREY_A))
        r_cap.arrange(DOWN, buff=0.08).next_to(right, UP, buff=0.2)
        eq = label(r"$=$", font_size=64, color=WHITE).move_to([-1.85, 0.05, 0])
        same = VGroup(label(r"largest difference", font_size=24, color=GREY_A),
                      label(rf"{d['largest_difference']:.2f}", font_size=56, color=P.ACCENT)).arrange(DOWN, buff=0.1)
        same.move_to([5.1, 1.2, 0])
        tell = VGroup(
            label(r"what can tell them apart", font_size=26, color=WHITE),
            wrapped_label(r"change one item, and see whether the others move", 3.3, 24, GREY_A),
            wrapped_label(r"follow the same people through time", 3.3, 24, GREY_A),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.15).move_to([5.15, -0.9, 0])
        end = label(r"A table of correlations at one moment cannot say which story is true.", font_size=30,
                    color=P.ACCENT).to_edge(DOWN, buff=0.6)
        tag = psyche_tag(r"computed: two models of six variables")
        with self.voiceover(
            "You'd think data could decide between them. So build both, and compute what each implies. "
            "<bookmark mark='a'/> Six items driven by one hidden cause give this table of correlations. "
            "<bookmark mark='b'/> Six items with no common cause at all, each nudging every other one, give "
            "this table. <bookmark mark='c'/> They're the same table, to as many decimal places as you like. "
            "For this pair of models, a set of correlations measured at one moment can't tell you which story "
            "you're in. That's a result about the limits of a method, and it's why the argument between these "
            "two pictures is still alive. <bookmark mark='d'/> What does distinguish them is what distinguishes "
            "causes anywhere. Intervene: improve someone's sleep, and see whether their mood follows. In the "
            "first story it shouldn't, because sleep was only a symptom. In the second it should. Or follow "
            "people through time, and see what changes first. The hidden-cause picture returns in Part 32, the "
            "network picture in Part 39, and the two are set against each other properly in Part 44. For now, "
            "keep one thing: a score can be reliable, and useful, and still leave open what it's a score of."
        ) as vo:
            self.play(FadeIn(head), FadeIn(tag))
            vo.wait_until("a")
            self.play(FadeIn(l_cap), FadeIn(left, lag_ratio=0.02), run_time=2.0)
            vo.wait_until("b")
            self.play(FadeIn(r_cap), FadeIn(right, lag_ratio=0.02), run_time=2.0)
            vo.wait_until("c")
            self.play(FadeIn(eq, scale=1.4), FadeIn(same))
            self.play(FadeIn(end, shift=UP * 0.15))
            vo.wait_until("d")
            self.play(LaggedStart(*[FadeIn(t, shift=UP * 0.1) for t in tell], lag_ratio=0.6), run_time=4.0)
        self.clear_scene()

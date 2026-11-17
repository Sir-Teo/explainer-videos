from __future__ import annotations

import numpy as np

from videos.psychology.psych1.common import *  # noqa: F403


def theatre(height: float) -> VGroup:
    """A head with a screen inside and a little person watching it: the explanation that explains nothing.
    ``.person`` is the watcher, ``.screen`` the screen, ``.head`` the outline."""
    head = head_outline(height)
    c = head.inside
    screen = Rectangle(width=0.2 * height, height=0.14 * height, stroke_color=WHITE, stroke_width=2,
                       fill_color="#1D2A1F", fill_opacity=1).move_to(c + np.array([0.15 * height, 0.02 * height, 0]))
    tree = VGroup(Triangle(stroke_width=0, fill_color="#5BD18B", fill_opacity=1).scale(0.035 * height),
                  Rectangle(width=0.012 * height, height=0.03 * height, stroke_width=0, fill_color="#B08968",
                            fill_opacity=1))
    tree.arrange(DOWN, buff=0).move_to(screen)
    person = little_person(0.2 * height, color=GREY_A).move_to(c + np.array([-0.14 * height, -0.03 * height, 0]))
    eye = Dot(np.array([0.33 * height, 0.1 * height, 0]), radius=0.018 * height, color=WHITE)
    ray = DashedLine(eye.get_center(), screen.get_right(), color=GREY_B, stroke_width=2)
    g = VGroup(head, eye, ray, screen, tree, person)
    g.head, g.screen, g.person, g.eye = head, VGroup(screen, tree), person, VGroup(eye, ray)
    return g


class Homunculus(VoiceoverScene):
    def construct(self):
        self.card()
        self.little_man()
        self.discharge()

    def card(self):
        card = chapter_card(10, r"The little person in the head", r"What does it take for an explanation of the "
                            r"mind to explain anything?", lit=(), part=PART, scale=("mind",), marr=("how",))
        with self.voiceover(
            "Chapter ten. The little person in the head."
        ):
            self.play(FadeIn(card, shift=UP * 0.2))
        self.clear_scene()

    # ------------------------------------------------------------------
    def little_man(self):
        big = theatre(6.6).move_to([-3.4, 0, 0])
        outside = VGroup(Triangle(stroke_width=0, fill_color="#5BD18B", fill_opacity=1).scale(0.5),
                         Rectangle(width=0.16, height=0.4, stroke_width=0, fill_color="#B08968", fill_opacity=1))
        outside.arrange(DOWN, buff=0).move_to([1.2, 0.6, 0])
        sight = DashedLine(outside.get_left(), big.eye[0].get_center(), color=GREY_B, stroke_width=2)
        # the regress: a smaller theatre in the watcher's head, and a smaller one in that
        mid = theatre(6.6 * 0.24)
        mid.shift(big.person.head.get_center() - mid.head.get_center())
        small = theatre(6.6 * 0.24 * 0.24)
        small.shift(mid.person.head.get_center() - small.head.get_center())
        name = VGroup(label(r"\emph{homunculus}", font_size=44, color=P.ACCENT),
                      label(r"Latin: \ a little person", font_size=28, color=GREY_A)).arrange(DOWN, buff=0.1)
        name.move_to([3.9, 2.6, 0])
        ask = label(r"And how does \emph{it} see?", font_size=36, color=WHITE).move_to([3.9, 1.3, 0])
        phrases = VGroup()
        for t in (r"``The brain decides.''", r"``Attention selects.''", r"``Memory retrieves the right fact.''"):
            phrases.add(VGroup(little_person(0.42, color=P.ACCENT), label(t, font_size=32, color=WHITE))
                        .arrange(RIGHT, buff=0.25))
        phrases.arrange(DOWN, aligned_edge=LEFT, buff=0.35).move_to([3.9, -1.5, 0])
        with self.voiceover(
            "There's one way to fail at all three levels at once, and it's the most natural explanation there "
            "is. How do you see a tree? Well, the eye sends a picture to the brain, and then something in there "
            "looks at it. <bookmark mark='a'/> A little person, sitting in the head, watching a screen. In "
            "Latin: a homunculus. <bookmark mark='b'/> The trouble is plain as soon as it's drawn. How does the "
            "little person see? There would have to be a smaller one inside its head, and a smaller one inside "
            "that. Nothing has been explained. The whole problem has just been moved one step in. "
            "<bookmark mark='c'/> Nobody proposes this in so many words. It slips in through phrases. The brain "
            "decides. Attention selects. Memory retrieves the right fact. Each of those hides somebody clever, "
            "doing the work."
        ) as vo:
            self.play(FadeIn(big.head), FadeIn(outside))
            self.play(Create(sight), FadeIn(big.eye))
            self.play(FadeIn(big.screen))
            vo.wait_until("a")
            self.play(FadeIn(big.person, shift=UP * 0.2), FadeIn(name))
            vo.wait_until("b")
            self.play(FadeIn(ask))
            self.play(FadeIn(mid, scale=0.5))
            self.play(FadeIn(small, scale=0.5))
            vo.wait_until("c")
            self.play(FadeOut(ask), LaggedStart(*[FadeIn(p_, shift=LEFT * 0.2) for p_ in phrases], lag_ratio=0.5),
                      run_time=4.5)
        self.clear_scene()

    def discharge(self):
        pos = [-3.5, 0, 0]
        whole = homunculus_map(whole=True, height=7.5).move_to(pos)
        comm = homunculus_map(done=(), height=7.5, font_size=17).move_to(pos)
        done = homunculus_map(done=("reacts",), height=7.5, font_size=17).move_to(pos)
        rule = quote_card(r"A homunculus is a problem only if it is as clever as the person it is meant to explain. "
                          r"Replace it with a committee of simpler ones, and those with simpler ones still, until "
                          r"each can be replaced by a machine.", r"after Daniel Dennett, \emph{Brainstorms} (1978)",
                          width=6.2, font_size=27, color=P.ACCENT).move_to([3.75, 1.3, 0])
        donders = VGroup(label(r"Donders, 1868: \ one reactor becomes three", font_size=28, color=WHITE),
                         VGroup(*[label(t, font_size=28, color=c) for t, c in ((r"sense", SENSE),
                                                                               (r"tell apart", DISC),
                                                                               (r"choose", CHOOSE))])
                         .arrange(RIGHT, buff=0.5)).arrange(DOWN, buff=0.2).move_to([3.75, -1.6, 0])
        legend_ = VGroup(
            VGroup(little_person(0.4, color=P.PERSON), label(r"not yet explained", font_size=26, color=GREY_A))
            .arrange(RIGHT, buff=0.2),
            VGroup(gear(0.19), label(r"built: \ a mechanism that runs", font_size=26,
                                     color=P.MECH)).arrange(RIGHT, buff=0.2),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.25).move_to([3.6, -1.9, 0])
        title = VGroup(label(r"The map of the series", font_size=40, color=WHITE),
                       label(r"twenty things a mind does", font_size=30, color=GREY_A)).arrange(DOWN, buff=0.15)
        title.move_to([3.6, 1.6, 0])
        last = wrapped_label(r"What is still a person in Part 62 is the list of what psychology has not explained.",
                             6.0, 30, WHITE).move_to([3.6, 1.4, 0])
        tokens = VGroup(*[VGroup(comm.token[k], comm.name[k]) for k, _, _ in FACULTIES])
        with self.voiceover(
            "The philosopher Daniel Dennett gave the rule for doing it properly. A homunculus is only a problem "
            "if it's as clever as the person it's supposed to explain. <bookmark mark='a'/> So replace the one "
            "clever person with a committee of specialists, each of which does less. One that only detects. One "
            "that only compares. One that only remembers. <bookmark mark='b'/> Then replace each of those with "
            "simpler ones still. When the members are so simple that a machine could do the job, a gear, a "
            "switch, a line of arithmetic, the homunculus has been discharged, and something has been "
            "explained. <bookmark mark='c'/> Donders took the first step in 1868. One reactor became three: "
            "something that senses, something that tells apart, something that chooses. Each does less than the "
            "whole. <bookmark mark='d'/> This is the map of the series. Twenty things a mind does, each still "
            "drawn as a little person. Every part takes one of them, and replaces it with a mechanism that runs. "
            "<bookmark mark='e'/> Today we've made a start on the first: reacting. <bookmark mark='f'/> And "
            "whatever is still a person at the end, in Part 62, is the honest list of what psychology has not "
            "explained."
        ) as vo:
            self.play(FadeIn(whole), FadeIn(rule, shift=LEFT * 0.2))
            vo.wait_until("a")
            self.play(FadeOut(whole.person), LaggedStart(*[FadeIn(t, scale=0.5) for t in tokens], lag_ratio=0.08),
                      run_time=3.5)
            vo.wait_until("c")
            self.play(FadeIn(donders, shift=UP * 0.15))
            self.play(Indicate(tokens[0], color=WHITE, scale_factor=1.25))
            vo.wait_until("d")
            self.play(FadeOut(donders), FadeOut(rule), FadeIn(legend_), FadeIn(title))
            self.play(LaggedStart(*[Indicate(t, color=WHITE, scale_factor=1.12) for t in tokens], lag_ratio=0.06),
                      run_time=3.0)
            vo.wait_until("e")
            self.play(ReplacementTransform(comm.token["reacts"], done.token["reacts"]),
                      ReplacementTransform(comm.name["reacts"], done.name["reacts"]))
            self.play(Circumscribe(VGroup(done.token["reacts"], done.name["reacts"]), color=P.MECH, buff=0.08))
            vo.wait_until("f")
            self.play(FadeOut(title), FadeIn(last, shift=UP * 0.15))
            self.play(Indicate(VGroup(comm.token["aware"], comm.name["aware"]), color=WHITE, scale_factor=1.25))
        self.clear_scene()

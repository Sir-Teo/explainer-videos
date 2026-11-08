from __future__ import annotations

from videos.philosophy.philosophy31.common import *  # noqa: F403


class Bat(VoiceoverScene):
    def construct(self):
        card = chapter_card(1, r"What it is like", r"Can an objective science capture a point of view?", lit=(1974,),
                            part=PART)
        with self.voiceover("Chapter one. What it is like."):
            self.play(FadeIn(card[0], shift=UP * 0.2), FadeIn(card[1]))
        self.play(FadeOut(card))
        self.sonar()
        self.viewpoint()
        self.access()

    def sonar(self):
        hc = history_card(1974, r"Thomas Nagel", r"`What Is It Like to Be a Bat?', \ \textit{Philosophical Review}",
                          width=6.4, color=HIST).to_corner(UL, buff=0.3)
        bat = VGroup(Polygon([-0.5, 0, 0], [-0.15, 0.12, 0], [0, 0.35, 0], [0.15, 0.12, 0], [0.5, 0, 0],
                             [0.15, -0.05, 0], [0, -0.15, 0], [-0.15, -0.05, 0], color=FEEL, fill_opacity=0.6)
                     ).scale(1.3).move_to([-4.2, 0.0, 0])
        moth = Dot([3.0, 0.3, 0], radius=0.12, color=SIG)
        waves = VGroup(*[Arc(radius=0.5 + 0.62 * k, start_angle=-0.22, angle=0.44, color=FEEL, stroke_width=3
                             ).shift(bat.get_center()) for k in range(11)])
        echoes = VGroup(*[Arc(radius=0.3 + 0.5 * k, start_angle=PI - 0.28, angle=0.56, color=SIG, stroke_width=2
                              ).shift(moth.get_center()) for k in range(7)])
        rows = stack([(r"bats see by sound: \ shrieks, \ and the echoes that come back", GREY_A),
                      (r"a sense we lack, \ precise enough to catch a moth in flight", FEEL),
                      (r"we can learn every fact about the mechanism \dots", PHYS),
                      (r"\dots and still not know what it is like \textit{for the bat}", GOAL)], font_size=21,
                     aligned_edge=LEFT, buff=0.25).to_edge(DOWN, buff=0.4)
        with self.voiceover(
            "Nagel chose bats because they are mammals, close enough to us that few doubt they have experience, "
            "yet strange. <bookmark mark='a'/>A bat finds its way by sound: it shrieks, and reads the world from the "
            "echoes. <bookmark mark='b'/>It is a sense we lack, fine enough to catch a moth in flight. "
            "<bookmark mark='c'/>We can learn every fact about the mechanism: the frequencies, the neurons, the "
            "timing of the echoes. <bookmark mark='d'/>And still, Nagel argued, we would not know what it is like "
            "for the bat. Imagining ourselves hanging upside down with webbing on our arms tells us what it would be "
            "like for us to behave like a bat, not what it is like for a bat to be a bat."
        ) as vo:
            self.play(FadeIn(hc), FadeIn(bat), FadeIn(moth))
            vo.wait_until("a")
            self.play(LaggedStart(*[Create(w) for w in waves], lag_ratio=0.15), run_time=2.5)
            self.play(LaggedStart(*[Create(e) for e in echoes], lag_ratio=0.15), FadeIn(rows[0]), run_time=2.5)
            vo.wait_until("b")
            self.play(FadeIn(rows[1]), moth.animate.shift(LEFT * 0.6 + UP * 0.3))
            vo.wait_until("c")
            self.play(FadeIn(rows[2]))
            vo.wait_until("d")
            self.play(FadeIn(rows[3]), Indicate(bat, color=FEEL))
        self.clear_scene()

    def viewpoint(self):
        head = label(r"The view from nowhere, \ and the view from somewhere", font_size=30, color=CONN).to_edge(
            UP, buff=0.3)
        ax = NumberLine(x_range=[0, 3, 1], length=9.0, include_numbers=False, color=GREY_B).move_to([0, 0.4, 0])
        steps = [r"how it seems to me", r"how it is for humans", r"how it is for any perceiver",
                 r"how it is, \ from no point of view", r"\textit{physics}"]
        ticks = VGroup()
        for k, s in enumerate(steps[:4]):
            ticks.add(VGroup(Dot(ax.n2p(k), radius=0.08, color=PHYS if k else FEEL),
                             wrapped_label(s, 2.2, 18, PHYS if k else FEEL).next_to(ax.n2p(k), UP, buff=0.25)))
        arrow = Arrow(ax.n2p(0) + DOWN * 0.5, ax.n2p(3) + DOWN * 0.5, buff=0, color=PHYS)
        al = label(r"objectivity: \ leave each point of view behind", font_size=18, color=PHYS).next_to(arrow, DOWN,
                                                                                                       buff=0.12)
        rows = stack([(r"the method that made physics objective is to drop the perceiver's perspective", GREY_A),
                      (r"experience is the perspective: \ dropping it drops the very thing to be explained", FEEL),
                      (r"Nagel: \ not that physicalism is false, \ but that we cannot yet see how it could be true",
                       GOAL)], font_size=21, buff=0.25).to_edge(DOWN, buff=0.4)
        with self.voiceover(
            "Nagel's deeper point was about objectivity. <bookmark mark='a'/>Science becomes objective by stepping "
            "back from any one point of view: from how things seem to me, to how they are for humans, to how they "
            "would be for any perceiver, to how they are from no point of view at all. That is how we got physics. "
            "<bookmark mark='b'/>For most things, each step loses nothing that matters. "
            "<bookmark mark='c'/>But experience is the point of view. Stepping back from it does not get closer to "
            "it; it leaves it behind. <bookmark mark='d'/>Nagel did not conclude that physicalism is false. He "
            "concluded that we do not yet have the concepts to understand how it could be true, as a pre-Socratic "
            "philosopher could not have understood that matter is energy."
        ) as vo:
            self.play(FadeIn(head))
            vo.wait_until("a")
            self.play(Create(ax), LaggedStart(*[FadeIn(t) for t in ticks], lag_ratio=0.4), run_time=3)
            self.play(GrowArrow(arrow), FadeIn(al))
            vo.wait_until("b")
            self.play(FadeIn(rows[0]))
            vo.wait_until("c")
            self.play(FadeIn(rows[1]), Indicate(ticks[0], color=FEEL))
            vo.wait_until("d")
            self.play(FadeIn(rows[2]))
        self.clear_scene()

    def access(self):
        hc = history_card(1995, r"Ned Block", r"`On a Confusion about a Function of Consciousness'", width=6.4,
                          color=HIST).to_corner(UL, buff=0.3)
        left = VGroup(RoundedRectangle(width=5.2, height=2.6, corner_radius=0.2, color=FEEL, fill_opacity=0.08),
                      VGroup(label(r"phenomenal consciousness", font_size=24, color=FEEL),
                             wrapped_label(r"what it is like: \ the redness of red, \ the hurt of pain", 4.6, 18,
                                           GREY_A)).arrange(DOWN, buff=0.2)).move_to([-3.2, 0.0, 0])
        right = VGroup(RoundedRectangle(width=5.2, height=2.6, corner_radius=0.2, color=FUNC, fill_opacity=0.08),
                       VGroup(label(r"access consciousness", font_size=24, color=FUNC),
                              wrapped_label(r"available for reasoning, \ report and the control of action", 4.6, 18,
                                            GREY_A)).arrange(DOWN, buff=0.2)).move_to([3.2, 0.0, 0])
        rows = stack([(r"defined by a function: \ science knows how to study it", FUNC),
                      (r"possible dissociations: \ blindsight \ (access without phenomenality?) \ and overflow \ "
                       r"(more seen than can be reported?)", GREY_A),
                      (r"the question of this part: \ is phenomenal consciousness anything over and above access?",
                       GOAL)], font_size=20, buff=0.22, width=12.6).to_edge(DOWN, buff=0.4)
        with self.voiceover(
            "In 1995 Ned Block drew a distinction that runs through the rest of this part. "
            "<bookmark mark='a'/>Phenomenal consciousness is what it is like: the redness of red, the hurt of pain. "
            "<bookmark mark='b'/>Access consciousness is a matter of function: a state is access conscious when its "
            "content is available for reasoning, for report, and for the control of action. "
            "<bookmark mark='c'/>Access is defined by what it does, so science knows how to study it. "
            "<bookmark mark='d'/>Block argued that the two can come apart: perhaps in blindsight, which chapter "
            "nine simulates, and perhaps in overflow, when we seem to see more than we can report. "
            "<bookmark mark='e'/>Whether phenomenal consciousness is anything over and above access is the question "
            "of this part, and the next chapter gives it its name."
        ) as vo:
            self.play(FadeIn(hc))
            vo.wait_until("a")
            self.play(FadeIn(left))
            vo.wait_until("b")
            self.play(FadeIn(right))
            vo.wait_until("c")
            self.play(FadeIn(rows[0]))
            vo.wait_until("d")
            self.play(FadeIn(rows[1]))
            vo.wait_until("e")
            self.play(FadeIn(rows[2]))
        self.clear_scene()

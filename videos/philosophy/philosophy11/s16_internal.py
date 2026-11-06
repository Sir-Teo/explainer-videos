from __future__ import annotations

from videos.philosophy.philosophy11.common import *  # noqa: F403


def head_icon(color=WHITE, s=1.0) -> VGroup:
    skull = Circle(radius=0.55 * s, stroke_color=color, stroke_width=3)
    neck = Line(skull.get_bottom(), skull.get_bottom() + DOWN * 0.35 * s, color=color, stroke_width=3)
    thought = VGroup(*[Circle(radius=r * s, stroke_color=color, stroke_width=2).move_to(
        skull.get_center() + np.array([0.75, 0.75, 0]) * s + np.array([dx, dy, 0]) * s)
        for r, dx, dy in ((0.06, -0.15, -0.15), (0.1, 0.0, 0.0), (0.3, 0.35, 0.35))])
    return VGroup(skull, neck, thought)


class Internal(VoiceoverScene):
    def construct(self):
        card = chapter_card(15, r"Inside or outside the head", r"Must you be able to see your own reasons?",
                            lit=(1979,), part=PART)
        with self.voiceover("Chapter fifteen. Inside or outside the head."):
            self.play(FadeIn(card[0], shift=UP * 0.2), FadeIn(card[1]))
        self.play(FadeOut(card))
        self.divide()
        self.demon()

    def divide(self):
        head = label(r"Two pictures of justification", font_size=32, color=CONN).to_edge(UP, buff=0.4)
        a = VGroup(label(r"internalism", font_size=28, color=BEL),
                   label(r"what justifies a belief", font_size=22),
                   label(r"is accessible to the believer by reflection", font_size=22),
                   label(r"Descartes, \ Chisholm, \ BonJour;", font_size=20, color=GREY_B),
                   label(r"mentalism: \ Conee and Feldman (2001)", font_size=20, color=GREY_B)).arrange(DOWN,
                                                                                                    buff=0.15)
        b = VGroup(label(r"externalism", font_size=28, color=JUST),
                   label(r"what justifies a belief", font_size=22),
                   label(r"may lie outside: \ reliability, \ causal history", font_size=22),
                   label(r"Goldman, \ Nozick, \ Sosa, \ Williamson;", font_size=20, color=GREY_B),
                   label(r"animals and infants can know", font_size=20, color=GREY_B)).arrange(DOWN, buff=0.15)
        cols = VGroup(a, b).arrange(RIGHT, buff=1.6, aligned_edge=UP).move_to([0, 0.6, 0])
        hd = [label(r"case", font_size=21, color=P.CLAIM), label(r"internalist", font_size=21, color=P.CLAIM),
              label(r"externalist", font_size=21, color=P.CLAIM)]
        rows = [[label(r"Norman the clairvoyant", font_size=20), label(r"unjustified", font_size=20, color=BAD),
                 label(r"justified", font_size=20, color=OK)],
                [label(r"the chicken sexer", font_size=20), label(r"no knowledge", font_size=20, color=BAD),
                 label(r"knows", font_size=20, color=OK)],
                [label(r"the demon's victim", font_size=20), label(r"justified", font_size=20, color=OK),
                 label(r"unjustified", font_size=20, color=BAD)]]
        grid = ValueGrid(hd, rows, col_w=[4.2, 2.6, 2.6], cell_h=0.46, font_size=20).to_edge(DOWN, buff=0.4)
        with self.voiceover(
            "Behind many of these disputes lies one division. <bookmark mark='a'/>Internalists hold that whatever "
            "justifies a belief must be accessible to the believer, by reflection: her experiences, her reasons, "
            "what she could cite if asked. Descartes was an internalist, and so were Chisholm and BonJour; Earl Conee "
            "and Richard Feldman's version, mentalism, says that justification depends only on the believer's mental "
            "states. <bookmark mark='b'/>Externalists hold that what justifies may lie outside the believer's view: "
            "the reliability of the process, the causal history of the belief. That is why, for them, animals and "
            "infants can know. <bookmark mark='c'/>The two sides sort the cases in opposite ways. BonJour's "
            "clairvoyant, reliable without reasons. The professional chicken sexers who can tell male chicks from "
            "female with high accuracy, while unable to say how. And a third case, which the internalist uses in "
            "return."
        ) as vo:
            self.play(FadeIn(head))
            vo.wait_until("a")
            self.play(FadeIn(a))
            vo.wait_until("b")
            self.play(FadeIn(b))
            vo.wait_until("c")
            self.play(FadeIn(grid.head), FadeIn(grid.rule), FadeIn(grid.rows_bg),
                      LaggedStart(*[FadeIn(VGroup(*grid.cell[r])) for r in range(3)], lag_ratio=0.6), run_time=5)
        self.clear_scene()

    def demon(self):
        head = label(r"The new evil demon problem", font_size=32, color=CONN).to_edge(UP, buff=0.35)
        who = label(r"Lehrer and Cohen (1983); \ Cohen (1984)", font_size=21, color=GREY_B).next_to(head, DOWN,
                                                                                                  buff=0.15)
        you = head_icon(BEL).move_to([-3.6, 0.7, 0])
        twin = head_icon(LUCK).move_to([3.6, 0.7, 0])
        demon = VGroup(Triangle(color=BAD, fill_opacity=0.3).scale(0.25).shift(LEFT * 0.18),
                       Triangle(color=BAD, fill_opacity=0.3).scale(0.25).shift(RIGHT * 0.18)).next_to(twin, UR,
                                                                                                   buff=0.1)
        yl = VGroup(label(r"you", font_size=24, color=BEL),
                    label(r"your perception is reliable", font_size=20, color=GREY_A)).arrange(DOWN, buff=0.1).next_to(
            you, DOWN, buff=0.3)
        tl = VGroup(label(r"your twin, \ deceived by a demon", font_size=24, color=LUCK),
                    label(r"the same experiences, \ the same reasoning", font_size=20, color=GREY_A),
                    label(r"her perception: \ always wrong", font_size=20, color=BAD)).arrange(DOWN, buff=0.1).next_to(
            twin, DOWN, buff=0.3)
        eq = MathTex(r"=", font_size=60, color=GREY_B).move_to([0, 0.7, 0])
        rows = VGroup(label(r"is she as justified as you? \ surely: \ she reasons as carefully as you do",
                            font_size=23, color=GOAL),
                      label(r"reliabilism says no: \ her processes are unreliable", font_size=23, color=BAD),
                      label(r"replies: \ reliability in \textit{our} world (Goldman); \ justification vs.\ blamelessness"
                            r" (Williamson)", font_size=21, color=GREY_A)).arrange(DOWN, buff=0.18).to_edge(DOWN,
                                                                                                   buff=0.4)
        with self.voiceover(
            "The internalist's counterexample is the new evil demon problem, from Keith Lehrer and Stewart Cohen. "
            "<bookmark mark='a'/>Take yourself, with your reliable perception. <bookmark mark='b'/>Now imagine a twin, "
            "deceived from birth by Descartes's demon. She has exactly your experiences, and reasons from them "
            "exactly as carefully as you do. But her perception is always wrong. <bookmark mark='c'/>Is she as "
            "justified as you are? It seems she is: she does everything right. <bookmark mark='d'/>Yet simple "
            "reliabilism says her beliefs are unjustified, since the processes that produce them are unreliable in "
            "her world. <bookmark mark='e'/>Externalists have replies. Goldman proposed measuring reliability in "
            "our world, not hers. Williamson distinguishes being justified from being blameless: the twin is "
            "blameless, but her beliefs are not justified, since they are not knowledge. The quarrel continues."
        ) as vo:
            self.play(FadeIn(head), FadeIn(who))
            vo.wait_until("a")
            self.play(FadeIn(you), FadeIn(yl))
            vo.wait_until("b")
            self.play(FadeIn(twin), FadeIn(demon), FadeIn(tl), FadeIn(eq))
            for mk, r in zip("cde", rows):
                vo.wait_until(mk)
                self.play(FadeIn(r))
        self.clear_scene()

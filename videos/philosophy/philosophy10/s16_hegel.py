from __future__ import annotations

from videos.philosophy.philosophy10.common import *  # noqa: F403


class Hegel(VoiceoverScene):
    def construct(self):
        card = chapter_card(15, r"Hegel, \ briefly and honestly", r"Can contradiction drive thought forward?",
                            lit=(1807,), part=PART)
        with self.voiceover("Chapter fifteen. Hegel, briefly and honestly."):
            self.play(FadeIn(card[0], shift=UP * 0.2), FadeIn(card[1]))
        self.play(FadeOut(card))
        self.dialectic()
        self.formal()

    def dialectic(self):
        hc = history_card(1807, r"G.\ W.\ F.\ Hegel", r"\textit{Phenomenology of Spirit}; \ \textit{Science of Logic} "
                          r"(1812--16)", width=6.0, color=HIST).to_corner(UL, buff=0.35)
        steps = VGroup(label(r"being", font_size=30, color=REASON), label(r"nothing", font_size=30, color=SENSE),
                       label(r"becoming", font_size=30, color=KANT)).arrange(RIGHT, buff=1.6).move_to([0, 0.9, 0])
        arrs = VGroup(Arrow(steps[0].get_right(), steps[1].get_left(), buff=0.2, color=GREY_B),
                      Arrow(steps[1].get_right(), steps[2].get_left(), buff=0.2, color=GREY_B))
        rows = VGroup(
            label(r"pure being, \ with no further determination, \ turns out to be nothing", font_size=22,
                  color=GREY_A),
            label(r"their unity, \ the passing of each into the other, \ is becoming", font_size=22, color=GREY_A),
            label(r"each concept, \ thought through, \ shows its own limits: \ \textit{determinate negation}",
                  font_size=24, color=GOAL),
            label(r"`thesis, antithesis, synthesis' \ is Fichte's language, \ not Hegel's", font_size=22,
                  color=BAD)).arrange(DOWN, buff=0.3).move_to([0, -1.4, 0])
        with self.voiceover(
            "Kant's antinomies showed reason contradicting itself. Hegel made that into a method. "
            "<bookmark mark='a'/>His Science of Logic begins with the emptiest concept there is: pure being, with "
            "no further determination. <bookmark mark='b'/>Thought through, it turns out to have no content at all; "
            "it is nothing. <bookmark mark='c'/>And the passing of each into the other is becoming. "
            "<bookmark mark='d'/>The engine is what Hegel called determinate negation: each concept, thought through, "
            "reveals its own limits, and the limit points to a richer concept. <bookmark mark='e'/>One correction is "
            "owed. The formula thesis, antithesis, synthesis is not Hegel's. It comes from Fichte, and was attached "
            "to Hegel by later expositors."
        ) as vo:
            self.play(FadeIn(hc))
            vo.wait_until("a")
            self.play(FadeIn(steps[0]))
            vo.wait_until("b")
            self.play(GrowArrow(arrs[0]), FadeIn(steps[1]), FadeIn(rows[0]))
            vo.wait_until("c")
            self.play(GrowArrow(arrs[1]), FadeIn(steps[2]), FadeIn(rows[1]))
            vo.wait_until("d")
            self.play(FadeIn(rows[2]))
            vo.wait_until("e")
            self.play(FadeIn(rows[3]))
        self.clear_scene()

    def formal(self):
        head = label(r"Can the dialectic be formalized?", font_size=32, color=CONN).to_edge(UP, buff=0.45)
        rows = rows_at([
            (r"as paraconsistent logic", r"some contradictions are true \ (Priest; \ Part 5)"),
            (r"as category theory", r"Lawvere: \ adjoint pairs as `unity of opposites'"),
            (r"as a process", r"each stage revises the last, \ like a learning system"),
        ], x_left=-6.2, x_right=-2.2, y0=1.5, dy=0.9, font_size=25, left_color=KANT)
        verdict = VGroup(label(r"each captures something; \ none is accepted as \textit{the} reading", font_size=24,
                               color=GOAL),
                         label(r"the honest summary: \ Hegel's logic is not a formal logic, \ and claims not to be",
                               font_size=24, color=GREY_A),
                         label(r"his influence runs through history and society: \ Marx; \ Parts 29 and 38",
                               font_size=22, color=GREY_B)).arrange(DOWN, buff=0.25).to_edge(DOWN, buff=0.6)
        with self.voiceover(
            "A series built on formal reasoning has to ask: can the dialectic be formalized? <bookmark mark='a'/>"
            "Some read it as a paraconsistent logic, in which some contradictions are true, the view of Part 5. "
            "<bookmark mark='b'/>William Lawvere, a founder of category theory, read Hegel's unities of opposites as "
            "adjoint pairs of functors. <bookmark mark='c'/>Others read the dialectic as a process of revision, each "
            "stage correcting the last, rather like a learning system. <bookmark mark='d'/>Each reading captures "
            "something, and none is accepted as the reading. <bookmark mark='e'/>The honest summary is that Hegel's "
            "logic is not a formal logic, and does not claim to be one. <bookmark mark='f'/>Its influence runs "
            "instead through philosophy of history and society, through Marx, and into Parts 29 and 38."
        ) as vo:
            self.play(FadeIn(head))
            for mk, r in zip("abc", rows):
                vo.wait_until(mk)
                self.play(FadeIn(r, shift=RIGHT * 0.1))
            for mk, r in zip("def", verdict):
                vo.wait_until(mk)
                self.play(FadeIn(r))
        self.clear_scene()

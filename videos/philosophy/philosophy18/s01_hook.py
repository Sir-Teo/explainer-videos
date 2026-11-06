from __future__ import annotations

from videos.philosophy.philosophy18.common import *  # noqa: F403


class Hook(VoiceoverScene):
    def construct(self):
        self.title()
        self.electron()
        self.objectives()

    def title(self):
        t = part_title(PART)
        q = quote_card(r"The positive argument for realism is that it is the only philosophy that doesn't make the "
                       r"success of science a miracle.", r"Hilary Putnam", r"\textit{Mathematics, Matter and Method} "
                       r"\ (1975)", width=10.4, font_size=25).next_to(t, DOWN, buff=0.5)
        with self.voiceover(
            "Part 17 built a mathematics of causes, and found that data alone often leave the causal structure "
            "open. This part asks the same question of science as a whole. Does evidence fix theory, and do our "
            "best theories tell us what the world is really like? <bookmark mark='a'/>Hilary Putnam put the case "
            "for yes in one sentence: realism is the only philosophy that does not make the success of science a "
            "miracle. <bookmark mark='b'/>This part tests that sentence."
        ) as vo:
            self.play(FadeIn(t, shift=UP * 0.2))
            vo.wait_until("a")
            self.play(FadeIn(q))
            vo.wait_until("b")
            self.play(Indicate(q, color=GOAL, scale_factor=1.03))
        self.clear_scene()

    def electron(self):
        head = label(r"Is the electron real?", font_size=30, color=CONN).to_edge(UP, buff=0.35)
        tube = VGroup(RoundedRectangle(width=6.0, height=1.6, corner_radius=0.8, color=GREY_B, stroke_width=3),
                      Line([-2.6, -0.5, 0], [-2.6, 0.5, 0], color=DATA, stroke_width=5),
                      Line([2.7, -0.7, 0], [2.7, 0.7, 0], color=THEORY, stroke_width=6)).move_to([-2.6, 1.0, 0])
        p0 = tube[1].get_center()
        p3 = tube[2].get_center() + UP * 0.5
        beam = CubicBezier(p0, p0 + RIGHT * 1.6, p0 + RIGHT * 2.6 + UP * 0.05, p3, color=THEORY, stroke_width=3)
        plates = VGroup(Line([-1.2, 0.35, 0], [0.4, 0.35, 0], color=REAL, stroke_width=4),
                        Line([-1.2, -0.35, 0], [0.4, -0.35, 0], color=REAL, stroke_width=4)).shift(UP * 1.0 + LEFT * 2.6)
        cap = label(r"Thomson \ (1897): \ a beam bends between charged plates", font_size=19, color=GREY_A).next_to(
            tube, DOWN, buff=0.25)
        rows = stack([
            (r"no one has seen an electron; \ we see glows, \ tracks and meter readings", WHITE),
            (r"yet we compute its magnetic moment to twelve digits, \ and build transistors with it", THEORY),
            (r"realist: \ electrons exist, \ and the theory is approximately true of them", REAL),
            (r"anti-realist: \ the theory is a superb instrument; \ its unobservables need not be believed", ANTI),
            (r"and history: \ the aether, \ caloric and phlogiston were once just as well confirmed", BAD),
        ], font_size=21, aligned_edge=LEFT, width=7.0).move_to([3.0, -1.6, 0])
        with self.voiceover(
            "Take the electron. <bookmark mark='a'/>In 1897 J. J. Thomson watched a glowing beam bend between "
            "charged plates, and inferred a particle two thousand times lighter than hydrogen. "
            "<bookmark mark='b'/>No one has ever seen an electron. We see glows, tracks in cloud chambers, and "
            "meter readings. <bookmark mark='c'/>Yet physics predicts the electron's magnetic moment to about twelve "
            "significant figures, and industry builds billions of transistors on its behaviour. "
            "<bookmark mark='d'/>The realist says electrons exist, and our theory is approximately true of them. "
            "<bookmark mark='e'/>The anti-realist says the theory is a superb instrument for prediction, and its "
            "unobservable entities need not be believed. <bookmark mark='f'/>And history weighs in: the aether, "
            "caloric and phlogiston were once just as well confirmed, and are gone."
        ) as vo:
            self.play(FadeIn(head))
            vo.wait_until("a")
            self.play(Create(tube), FadeIn(plates), FadeIn(cap))
            self.play(Create(beam), run_time=1.5)
            for mk, r in zip("bcdef", rows):
                vo.wait_until(mk)
                self.play(FadeIn(r))
        self.clear_scene()

    def objectives(self):
        card = objectives_card([
            r"verificationism and its collapse; \ Hempel's laws, \ the flagpole, \ unification and mechanism",
            r"Kuhn's revolutions \ (a toy cascade); \ Lakatos, \ Feyerabend, \ Laudan",
            r"underdetermination \ (two Newtonian worlds); \ Duhem and Quine",
            r"no miracles, \ the base rate, \ and the pessimistic meta-induction \ (the Wall)",
            r"structural realism \ (Fresnel to Maxwell); \ constructive empiricism",
            r"reduction; \ emergence and universality: \ the Ising model, \ renormalized on screen",
            r"models and idealization; \ demarcation; \ values; \ AI scientists",
        ], font_size=24)
        with self.voiceover(
            "The plan. <bookmark mark='a'/>First, what makes a statement scientific, and what makes it explain: the "
            "Vienna Circle, Hempel's laws, and their successors. <bookmark mark='b'/>Then how science changes: Kuhn's "
            "revolutions, with a toy model of one, and his critics. <bookmark mark='c'/>Underdetermination: why "
            "evidence never quite fixes theory. <bookmark mark='d'/>The great debate over realism: the no-miracles "
            "argument, its base rate, and the history of failed theories, this part's brick in the Wall. "
            "<bookmark mark='e'/>Two middle ways: structural realism and constructive empiricism. "
            "<bookmark mark='f'/>Reduction and emergence, with the Ising model coarse-grained on screen. "
            "<bookmark mark='g'/>And models, demarcation, values, and machines that do science."
        ) as vo:
            self.play(FadeIn(card.head))
            for mk, i in zip("abcdefg", range(7)):
                vo.wait_until(mk)
                self.play(FadeIn(card.rows[i], shift=RIGHT * 0.2))
        self.clear_scene()

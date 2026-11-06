from __future__ import annotations

from videos.philosophy.philosophy8.common import *  # noqa: F403


class Hook(VoiceoverScene):
    def construct(self):
        self.title()
        self.liar()
        self.preview()
        self.objectives()

    def title(self):
        t = part_title(PART)
        q = quote_card(r"This sentence is not true.", r"the liar", r"after Eubulides of Miletus, \ 4th century BCE",
                       width=8.0, font_size=34).next_to(t, DOWN, buff=0.7)
        with self.voiceover(
            "Part 8 is about one sentence. <bookmark mark='a'/>This sentence is not true. "
            "<bookmark mark='b'/>It has been argued over for two thousand four hundred years, and it is still "
            "argued over today."
        ) as vo:
            self.play(FadeIn(t, shift=UP * 0.2))
            vo.wait_until("a")
            self.play(FadeIn(q))
            vo.wait_until("b")
            self.play(Indicate(q, color=SELF, scale_factor=1.03))
        self.clear_scene()

    def liar(self):
        s = label(r"$L$: \ `$L$ is not true'", font_size=40, color=SELF).move_to([0, 2.0, 0])
        left = VGroup(label(r"if $L$ is true", font_size=28, color=OK),
                      label(r"then what it says is so:", font_size=24, color=GREY_A),
                      label(r"$L$ is not true", font_size=28, color=BAD)).arrange(DOWN, buff=0.2)
        right = VGroup(label(r"if $L$ is not true", font_size=28, color=BAD),
                       label(r"then what it says is so:", font_size=24, color=GREY_A),
                       label(r"so $L$ is true", font_size=28, color=OK)).arrange(DOWN, buff=0.2)
        cols = VGroup(left, right).arrange(RIGHT, buff=2.4).move_to([0, -0.2, 0])
        arrows = VGroup(CurvedArrow(left.get_bottom() + DOWN * 0.15, right.get_bottom() + DOWN * 0.15, angle=0.8,
                                    color=GREY_B),
                        CurvedArrow(right.get_top() + UP * 0.15, left.get_top() + UP * 0.15, angle=0.8,
                                    color=GREY_B))
        why = label(r"and it uses nothing but the word `true' \ and ordinary logic", font_size=26,
                    color=GOAL).to_edge(DOWN, buff=0.5)
        with self.voiceover(
            "Call the sentence L. <bookmark mark='a'/>If L is true, then what it says is so, and it says that L is "
            "not true. <bookmark mark='b'/>If L is not true, then what it says is so after all, which makes it "
            "true. <bookmark mark='c'/>Each answer turns into the other. <bookmark mark='d'/>And the argument uses "
            "nothing but the word 'true' and the most ordinary logic. That is why it matters: Part 7 showed that the "
            "same structure, with 'provable' in place of 'true', is Gödel's theorem, and with 'true' it is "
            "Tarski's."
        ) as vo:
            self.play(FadeIn(s))
            vo.wait_until("a")
            self.play(FadeIn(left, shift=RIGHT * 0.1))
            vo.wait_until("b")
            self.play(FadeIn(right, shift=LEFT * 0.1))
            vo.wait_until("c")
            self.play(Create(arrows[0]), Create(arrows[1]))
            vo.wait_until("d")
            self.play(FadeIn(why))
        self.clear_scene()

    def preview(self):
        opts = VGroup(*[VGroup(label(a, font_size=30, color=c), label(b, font_size=22, color=GREY_A)).arrange(
            DOWN, buff=0.15) for a, b, c in (
            (r"a gap", r"the liar is neither true nor false \ (Kripke, Field)", "#5A6372"),
            (r"a glut", r"the liar is both \ (Priest)", GLUT),
            (r"a hierarchy", r"no language holds its own truth \ (Tarski)", GOAL),
            (r"a restriction", r"keep classical logic, \ give up some T-sentences \ (KF, Maudlin)", OK))]).arrange_in_grid(
            rows=2, cols=2, buff=(1.2, 0.6)).move_to([0, 0.3, 0])
        head = label(r"Four ways out, \ each with a price", font_size=32, color=CONN).to_edge(UP, buff=0.6)
        brick = label(r"this part's brick in the Wall: \ the liar, \ and revenge against every consistent answer",
                      font_size=26, color=P.WALL).to_edge(DOWN, buff=0.8)
        with self.voiceover(
            "There are four classical ways out, and the part builds each one. <bookmark mark='a'/>A gap: the liar "
            "is neither true nor false. A glut: it is both. A hierarchy: no language can contain its own truth "
            "predicate. Or a restriction: keep classical logic and give up some instances of the schema that "
            "defines truth. <bookmark mark='b'/>Each has a price, and each, as we will see, faces a stronger liar "
            "built against it. That is this part's brick in the Wall."
        ) as vo:
            self.play(FadeIn(head))
            vo.wait_until("a")
            self.play(LaggedStart(*[FadeIn(o, shift=UP * 0.1) for o in opts], lag_ratio=0.5), run_time=5)
            vo.wait_until("b")
            self.play(FadeIn(brick))
        self.clear_scene()

    def objectives(self):
        card = objectives_card([
            r"Eubulides, \ the Mohists, \ the medieval \textit{insolubilia}",
            r"Tarski's T-schema and the hierarchy of languages",
            r"a family of paradoxes: \ Grelling, Richard, Berry; \ Priest's inclosure schema",
            r"Kripke's fixed points, \ built: \ grounded and paradoxical sentences; \ revenge",
            r"revision theory; \ Curry; \ Yablo's staircase; \ dialetheism",
            r"the Price List; \ axiomatic theories of truth; \ what truth is",
            r"the surprise exam, \ the knower, \ and Moore's paradox",
        ], font_size=25)
        with self.voiceover(
            "So: <bookmark mark='a'/>first the liar's history, in Greece, in China and in the medieval schools. "
            "<bookmark mark='b'/>Then Tarski's analysis, and his hierarchy. <bookmark mark='c'/>Then the liar's "
            "relatives, and a pattern that unites them. <bookmark mark='d'/>Then Kripke's theory of truth, built and "
            "run by the Reasoner, and the revenge it invites. <bookmark mark='e'/>Then three more ways of thinking "
            "about paradox: revision, Curry's paradox, Yablo's infinite staircase, and the view that some "
            "contradictions are true. <bookmark mark='f'/>Then the Price List, the formal theories of truth, and "
            "the old question of what truth is. <bookmark mark='g'/>And last, paradoxes of knowledge and belief."
        ) as vo:
            self.play(FadeIn(card.head))
            for mk, i in zip("abcdefg", range(7)):
                vo.wait_until(mk)
                self.play(FadeIn(card.rows[i], shift=RIGHT * 0.2))
        self.clear_scene()

from __future__ import annotations

from videos.philosophy.philosophy8.common import *  # noqa: F403


class Yablo(VoiceoverScene):
    def construct(self):
        card = chapter_card(10, r"Yablo's staircase", r"Is self-reference needed for paradox?", lit=(1993,),
                            part=PART)
        with self.voiceover("Chapter ten. Yablo's staircase."):
            self.play(FadeIn(card[0], shift=UP * 0.2), FadeIn(card[1]))
        self.play(FadeOut(card))
        self.stairs()
        self.finite()
        self.debate()

    def stairs(self):
        hc = history_card(1993, r"Stephen Yablo", r"`Paradox without self-reference'", width=5.6, color=HIST).to_corner(
            UL, buff=0.35)
        steps = VGroup()
        for k in range(7):
            x, y = -5.0 + 1.55 * k, -2.6 + 0.62 * k
            st = Rectangle(width=1.5, height=0.36, stroke_color=GLUT, stroke_width=2, fill_color=GLUT,
                           fill_opacity=0.12).move_to([x, y, 0])
            t = label(rf"$Y_{{{k + 1}}}$: \ all later ones are untrue", font_size=16, color=WHITE).next_to(st, UP,
                                                                                                    buff=0.06)
            steps.add(VGroup(st, t))
        dots = MathTex(r"\cdots", font_size=40, color=GLUT).next_to(steps[-1], UR, buff=0.1)
        arg = VGroup(label(r"if any $Y_n$ were true, \ every later $Y$ is untrue:", font_size=22),
                     label(r"then $Y_{n+1}$ is true, \ since every $Y$ after it is untrue: \ contradiction",
                           font_size=22, color=BAD),
                     label(r"so every $Y_n$ is untrue: \ but then $Y_1$ is true", font_size=22, color=BAD)).arrange(
            DOWN, aligned_edge=LEFT, buff=0.15).next_to(hc, DOWN, buff=0.4).align_to(hc, LEFT)
        with self.voiceover(
            "Every paradox so far had a sentence that talks about itself. In 1993 Stephen Yablo asked whether that "
            "is essential. <bookmark mark='a'/>Imagine an infinite staircase of sentences. Each one says: every "
            "sentence after me is untrue. None mentions itself, and none mentions anything earlier. "
            "<bookmark mark='b'/>Suppose some sentence on the staircase were true. Then every later one is untrue. "
            "In particular the next is untrue; but everything after the next is untrue too, which is just what the "
            "next one says, so it is true. Contradiction. <bookmark mark='c'/>So every sentence is untrue. But then "
            "the first sentence is right about all the others, and it is true. A paradox, apparently with no "
            "self-reference."
        ) as vo:
            self.play(FadeIn(hc))
            vo.wait_until("a")
            self.play(LaggedStart(*[FadeIn(s, shift=UP * 0.1) for s in steps], lag_ratio=0.3), FadeIn(dots),
                      run_time=4)
            vo.wait_until("b")
            self.play(FadeIn(arg[0]), FadeIn(arg[1]))
            vo.wait_until("c")
            self.play(FadeIn(arg[2]))
        self.clear_scene()

    def finite(self):
        d = load("yablo")
        head = label(r"Cut the staircase off, \ and the paradox goes", font_size=32, color=CONN).to_edge(UP, buff=0.45)
        rows = VGroup()
        for n in range(1, 9):
            sol = d["solutions"][str(n)]
            assert len(sol) == 1 and sol[0] == [f"Y{n}"]
            chips = VGroup(*[value_chip("t" if k == n else "f", 20) for k in range(1, n + 1)]).arrange(RIGHT, buff=0.08)
            rows.add(VGroup(label(rf"{n} sentence{'s' if n > 1 else ''}:", font_size=22, color=GREY_A), chips).arrange(
                RIGHT, buff=0.3))
        rows.arrange(DOWN, aligned_edge=LEFT, buff=0.14).move_to([0, 0.55, 0])
        note = VGroup(label(r"for each finite staircase, \ the Reasoner finds exactly one consistent assignment:",
                            font_size=22),
                      label(r"the last sentence true \ (vacuously), \ every other false", font_size=22, color=OK),
                      label(r"the paradox needs the \textit{infinite} staircase: \ like $\omega$-inconsistency in "
                            r"Part 7", font_size=22, color=GOAL)).arrange(DOWN, buff=0.14).to_edge(DOWN, buff=0.3)
        with self.voiceover(
            "The Reasoner can only build finite staircases, and that is instructive. <bookmark mark='a'/>With one "
            "sentence, two, up to eight, it checks every assignment of true and false against the schema. Each time "
            "there is exactly one consistent assignment: the last sentence is true, vacuously, since nothing comes "
            "after it, and every other one is false. <bookmark mark='b'/>No finite staircase is paradoxical. The "
            "paradox lives only in the infinite one, where there is no last step. In arithmetic, Jeffrey Ketland "
            "showed, Yablo's sequence is not contradictory but omega-inconsistent, the property we met in Gödel's "
            "first theorem."
        ) as vo:
            self.play(FadeIn(head))
            vo.wait_until("a")
            self.play(LaggedStart(*[FadeIn(r, shift=RIGHT * 0.1) for r in rows], lag_ratio=0.25), run_time=4)
            self.play(FadeIn(note[0]), FadeIn(note[1]))
            vo.wait_until("b")
            self.play(FadeIn(note[2]))
        self.clear_scene()

    def debate(self):
        head = label(r"Is there self-reference after all?", font_size=32, color=CONN).to_edge(UP, buff=0.5)
        rows = VGroup(
            VGroup(label(r"Priest (1997):", font_size=26, color=GOAL),
                   label(r"to define the staircase you need a predicate that refers to itself: \ the circle is hidden "
                         r"in the definition", font_size=22, color=GREY_A)).arrange(DOWN, aligned_edge=LEFT, buff=0.1),
            VGroup(label(r"Sorensen; \ Cook (2014):", font_size=26, color=GOAL),
                   label(r"with infinitary sentences, \ or the right notion of reference, \ none is needed", font_size=22,
                         color=GREY_A)).arrange(DOWN, aligned_edge=LEFT, buff=0.1),
            VGroup(label(r"either way:", font_size=26, color=OK),
                   label(r"paradox comes from \textit{ungroundedness}, \ a chain of reference with no foot, \ of "
                         r"which a loop is one case", font_size=22, color=GREY_A)).arrange(DOWN, aligned_edge=LEFT,
                                                                                         buff=0.1)).arrange(
            DOWN, aligned_edge=LEFT, buff=0.45).move_to([0, -0.2, 0])
        with self.voiceover(
            "Is the staircase really free of self-reference? <bookmark mark='a'/>Graham Priest argued in 1997 that "
            "it is not: to describe the whole staircase in a finite language, you need a predicate that is "
            "satisfied by numbers in virtue of its own extension, a circle hidden in the definition. "
            "<bookmark mark='b'/>Roy Sorensen and Roy Cook replied that with infinitely long sentences, or a "
            "careful notion of reference, no circle is needed. <bookmark mark='c'/>Either way, the lesson matches "
            "Kripke's: what makes trouble is ungroundedness, a chain of 'is true' that never reaches the facts. A "
            "loop is one way to have no foundation; an endless staircase is another."
        ) as vo:
            self.play(FadeIn(head))
            for mk, r in zip("abc", rows):
                vo.wait_until(mk)
                self.play(FadeIn(r, shift=RIGHT * 0.1))
        self.clear_scene()

from __future__ import annotations

from videos.philosophy.philosophy31.common import *  # noqa: F403


class Gap(VoiceoverScene):
    def construct(self):
        card = chapter_card(5, r"The explanatory gap", r"If experience is physical, \ why can't we see why?",
                            lit=(1983,), part=PART)
        with self.voiceover("Chapter five. The explanatory gap."):
            self.play(FadeIn(card[0], shift=UP * 0.2), FadeIn(card[1]))
        self.play(FadeOut(card))
        self.levine()
        self.concepts()
        self.master()

    def levine(self):
        hc = history_card(1983, r"Joseph Levine", r"`Materialism and Qualia: \ The Explanatory Gap'", width=6.4,
                          color=HIST).to_corner(UL, buff=0.3)
        left = VGroup(label(r"heat \ $=$ \ mean molecular kinetic energy", font_size=22, color=PHYS),
                      label(r"the role of heat, \ fully played by molecular motion", font_size=18, color=GREY_A),
                      label(r"no further question", font_size=20, color=OK)).arrange(DOWN, buff=0.25).move_to(
            [-3.3, 0.0, 0])
        right = VGroup(label(r"pain \ $=$ \ C-fibre firing", font_size=22, color=FEEL),
                       label(r"the role of pain, \ perhaps played by C-fibres", font_size=18, color=GREY_A),
                       label(r"but why does \textit{that} feel like \textit{this}?", font_size=20, color=BAD)).arrange(
            DOWN, buff=0.25).move_to([3.3, 0.0, 0])
        line = DashedLine([0, 1.4, 0], [0, -1.4, 0], color=GREY_D)
        foot = label(r"Levine: \ a gap in explanation, \ whatever the metaphysics", font_size=21,
                     color=GOAL).to_edge(DOWN, buff=0.6)
        with self.voiceover(
            "In 1983 Joseph Levine separated the epistemic problem from the metaphysical one. "
            "<bookmark mark='a'/>Heat is the mean kinetic energy of molecules. Once we see that molecular motion "
            "plays every role that heat plays, raising thermometers and cooking food, there is no further question "
            "why molecular motion is heat. <bookmark mark='b'/>Pain is, let us say, C-fibre firing. Even if C-fibre "
            "firing plays every role of pain, a question remains: why does that firing feel like this, rather than "
            "like something else, or like nothing? <bookmark mark='c'/>Levine did not claim that physicalism is "
            "false. He claimed that it leaves an explanatory gap, even if it is true."
        ) as vo:
            self.play(FadeIn(hc))
            vo.wait_until("a")
            self.play(FadeIn(left), Create(line))
            vo.wait_until("b")
            self.play(FadeIn(right))
            vo.wait_until("c")
            self.play(FadeIn(foot))
        self.clear_scene()

    def concepts(self):
        head = label(r"The phenomenal concept strategy", font_size=30, color=CONN).to_edge(UP, buff=0.35)
        state = VGroup(Circle(radius=0.6, color=PHYS, fill_opacity=0.15), label(r"$P$", font_size=30, color=PHYS)
                       ).move_to([0, -0.3, 0])
        c1 = label(r"`C-fibre firing' \ (a physical concept)", font_size=19, color=PHYS).move_to([-4.0, 1.4, 0])
        c2 = label(r"`this feeling' \ (a phenomenal concept)", font_size=19, color=FEEL).move_to([4.0, 1.4, 0])
        a1 = Arrow(c1.get_bottom(), state.get_left() + UP * 0.2, color=PHYS, buff=0.15)
        a2 = Arrow(c2.get_bottom(), state.get_right() + UP * 0.2, color=FEEL, buff=0.15)
        rows = stack([(r"two concepts, \ one state: \ no a priori link between the concepts", GREY_A),
                      (r"phenomenal concepts refer directly, \ by quotation or recognition: \ Loar \ (1990), \ "
                       r"Papineau \ (2002), \ Balog", FEEL),
                      (r"so the gap is in our concepts, \ not in the world", GOAL)], font_size=20,
                     buff=0.22).to_edge(DOWN, buff=0.4)
        with self.voiceover(
            "Most physicalists now answer with what is called the phenomenal concept strategy. "
            "<bookmark mark='a'/>We have two kinds of concept for one and the same state: a physical concept, C-fibre "
            "firing, from the textbooks, <bookmark mark='b'/>and a phenomenal concept, this feeling, which we apply "
            "from the inside by recognizing the state when we have it. <bookmark mark='c'/>The two concepts have no "
            "a priori link, so no amount of reasoning from the one gets you to the other. That explains why zombies "
            "seem conceivable and why Mary seems to learn something. <bookmark mark='d'/>Brian Loar and David "
            "Papineau argue that phenomenal concepts refer directly, almost by quoting the experience itself. "
            "<bookmark mark='e'/>So the gap is in our concepts, not in the world: a type-B physicalism."
        ) as vo:
            self.play(FadeIn(head), FadeIn(state))
            vo.wait_until("a")
            self.play(FadeIn(c1), GrowArrow(a1))
            vo.wait_until("b")
            self.play(FadeIn(c2), GrowArrow(a2))
            vo.wait_until("c")
            self.play(FadeIn(rows[0]))
            vo.wait_until("d")
            self.play(FadeIn(rows[1]))
            vo.wait_until("e")
            self.play(FadeIn(rows[2]))
        self.clear_scene()

    def master(self):
        hc = history_card(2007, r"David Chalmers", r"`Phenomenal Concepts and the Explanatory Gap'", width=6.2,
                          color=HIST).to_corner(UL, buff=0.3)
        rows = [(r"the thesis", r"phenomenal concepts have some feature $C$ that explains the gap", GREY_A),
                (r"horn 1", r"if a zombie could lack $C$, \ $C$ is not physically explicable: \ the gap reappears "
                            r"one level up", BAD),
                (r"horn 2", r"if a zombie shares $C$, \ $C$ cannot explain our epistemic situation, \ which the "
                            r"zombie does not share", BAD),
                (r"replies", r"deny that a zombie's situation differs \ (Papineau, \ Balog); \ the debate goes on",
                 GOAL)]
        g = rows_table(rows, top=1.4, gap=0.5)
        with self.voiceover(
            "Chalmers replied in 2007 with a dilemma, sometimes called the master argument. "
            "<bookmark mark='a'/>Suppose phenomenal concepts have some feature C that explains the gap. "
            "<bookmark mark='b'/>Is a zombie conceivable that lacks C? If so, C is not itself physically explained: "
            "the gap has just moved up a level. <bookmark mark='c'/>If not, the zombie shares C. But the zombie is "
            "not in our epistemic situation: it has no experience to be ignorant about. So C cannot explain our "
            "situation either. <bookmark mark='d'/>Defenders reply that the zombie's situation is not as different "
            "as Chalmers says. On both sides the arguments are precise, and neither has carried the field."
        ) as vo:
            self.play(FadeIn(hc))
            for mk, r in zip("abcd", g):
                vo.wait_until(mk)
                self.play(FadeIn(r))
        self.clear_scene()

from __future__ import annotations

from videos.philosophy.philosophy12.common import *  # noqa: F403


class Hintikka(VoiceoverScene):
    def construct(self):
        card = chapter_card(1, r"Knowledge as a box", r"What does it mean to know, in a logic?", lit=(1962,),
                            part=PART)
        with self.voiceover("Chapter one. Knowledge as a box."):
            self.play(FadeIn(card[0], shift=UP * 0.2), FadeIn(card[1]))
        self.play(FadeOut(card))
        self.box()
        self.axioms()
        self.belief()
        self.critics()

    def box(self):
        hc = history_card(1962, r"Jaakko Hintikka", r"\textit{Knowledge and Belief}", width=5.0,
                          color=HIST).to_corner(UL, buff=0.35)
        worlds = [("r", "w"), ("r", "c"), ("s", "w"), ("s", "c")]
        labels = {("r", "w"): r"\text{rain, warm}", ("r", "c"): r"\text{rain, cold}",
                  ("s", "w"): r"\text{sun, warm}", ("s", "c"): r"\text{sun, cold}"}
        pos = {("r", "w"): [-1.6, 0.9, 0], ("r", "c"): [1.6, 0.9, 0], ("s", "w"): [-1.6, -0.9, 0],
               ("s", "c"): [1.6, -0.9, 0]}
        g = AgentGraph(worlds, {"a": [(("r", "w"), ("r", "c")), (("s", "w"), ("s", "c"))]}, pos, labels,
                       radius=0.75, font_size=20, center=[-2.6, -0.4, 0])
        act = SurroundingRectangle(g.world[("r", "w")], color=COMMON, buff=0.08, corner_radius=0.3)
        al = label(r"actual", font_size=20, color=COMMON).next_to(act, UP, buff=0.08)
        rows = VGroup(
            label(r"Ann looks out of the window: \ she sees rain, \ not the temperature", font_size=22),
            label(r"her blue line: \ worlds she cannot tell apart", font_size=22, color=AG["a"]),
            MathTex(r"K_a\,\text{rain}\ \ \text{true: rain in every world she can't rule out}", font_size=26,
                    color=OK),
            MathTex(r"K_a\,\text{warm}\ \ \text{false: a cold world is still open}", font_size=26, color=BAD),
            label(r"$K_a\,\varphi$ \ = \ $\varphi$ in every world compatible with what $a$ knows: \ a box, \ "
                  r"$\Box_a\varphi$", font_size=23, color=GOAL)).arrange(DOWN, aligned_edge=LEFT, buff=0.25)
        for r in rows:
            if r.width > 6.6:
                r.width = 6.6
        rows.arrange(DOWN, aligned_edge=LEFT, buff=0.25).move_to([3.4, -0.4, 0])
        with self.voiceover(
            "The logic of knowledge begins with a short book by Jaakko Hintikka, in 1962. <bookmark mark='a'/>Its "
            "idea is the possible-worlds semantics of Part 4. Four ways the day could be: rain or sun, warm or "
            "cold. In fact it is raining and warm. <bookmark mark='b'/>Ann looks out of the window. She sees the "
            "rain, but not the temperature. <bookmark mark='c'/>So she cannot tell the warm rainy world from the cold "
            "rainy one; a line joins them. <bookmark mark='d'/>Ann knows it is raining: rain holds in every world she "
            "cannot rule out. <bookmark mark='e'/>She does not know it is warm: a cold world is still open. "
            "<bookmark mark='f'/>To know phi is for phi to hold in every world compatible with what one knows. "
            "Knowledge is a box."
        ) as vo:
            self.play(FadeIn(hc))
            vo.wait_until("a")
            self.play(FadeIn(g.discs), Create(act), FadeIn(al))
            vo.wait_until("b")
            self.play(FadeIn(rows[0]))
            vo.wait_until("c")
            self.play(Create(g.edges), FadeIn(rows[1]))
            vo.wait_until("d")
            self.play(FadeIn(rows[2]))
            vo.wait_until("e")
            self.play(FadeIn(rows[3]))
            vo.wait_until("f")
            self.play(FadeIn(rows[4]))
        self.clear_scene()

    def axioms(self):
        head = label(r"The axioms of knowledge, \ and their frames", font_size=32, color=CONN).to_edge(UP, buff=0.35)
        hd = [label(r"axiom", font_size=22, color=P.CLAIM), label(r"formula", font_size=22, color=P.CLAIM),
              label(r"says", font_size=22, color=P.CLAIM), label(r"frame", font_size=22, color=P.CLAIM)]
        rows = [[label(r"K", font_size=22), MathTex(r"K(p \rightarrow q) \rightarrow (Kp \rightarrow Kq)",
                                                    font_size=26),
                 label(r"knowledge is closed under implication", font_size=20), label(r"every frame", font_size=20)],
                [label(r"T", font_size=22), MathTex(r"Kp \rightarrow p", font_size=26),
                 label(r"what is known is true", font_size=20), label(r"reflexive", font_size=20)],
                [label(r"4", font_size=22), MathTex(r"Kp \rightarrow KKp", font_size=26),
                 label(r"you know what you know", font_size=20), label(r"transitive", font_size=20)],
                [label(r"5", font_size=22), MathTex(r"\lnot Kp \rightarrow K\lnot Kp", font_size=26),
                 label(r"you know what you don't know", font_size=20), label(r"euclidean", font_size=20)]]
        grid = ValueGrid(hd, rows, col_w=[1.2, 4.6, 4.6, 2.2], cell_h=0.62, font_size=22).move_to([0, 0.3, 0])
        foot = VGroup(label(r"all four: \ S5, \ where the relation is an equivalence: \ a partition of the worlds",
                            font_size=24, color=GOAL),
                      label(r"each agent's knowledge \ = \ which cell of her partition she is in \ (Part 4's "
                            r"correspondence theory)", font_size=21, color=GREY_A)).arrange(DOWN, buff=0.15).to_edge(
            DOWN, buff=0.5)
        with self.voiceover(
            "Which laws does knowledge obey? <bookmark mark='a'/>Each axiom corresponds, as we proved in Part 4, to "
            "a property of the relation between worlds. K: if you know p implies q, and know p, you know q. It holds "
            "on every frame. <bookmark mark='b'/>T: what is known is true. Reflexive frames: the actual world is "
            "always among those you cannot rule out. <bookmark mark='c'/>Four: if you know, you know that you know. "
            "Transitive frames. <bookmark mark='d'/>Five: if you don't know, you know that you don't. Euclidean "
            "frames. <bookmark mark='e'/>All four together give the system S5, whose relation is an equivalence. "
            "Then each agent's knowledge is a partition of the worlds into cells, and what she knows is which cell "
            "she is in. This is the standard model in economics and computer science."
        ) as vo:
            self.play(FadeIn(head), FadeIn(grid.head), FadeIn(grid.rule), FadeIn(grid.rows_bg))
            for mk, r in zip("abcd", range(4)):
                vo.wait_until(mk)
                self.play(FadeIn(VGroup(*grid.cell[r])))
            vo.wait_until("e")
            self.play(FadeIn(foot))
        self.clear_scene()

    def belief(self):
        head = label(r"Belief: \ KD45", font_size=32, color=CONN).to_edge(UP, buff=0.4)
        rows = VGroup(
            label(r"belief can be false: \ drop T", font_size=24),
            label(r"keep consistency instead: \ D, \ $B\varphi \rightarrow \lnot B\lnot\varphi$ \ (serial frames)",
                  font_size=24, color=GREY_A),
            label(r"keep both introspections: \ 4 and 5", font_size=24, color=GREY_A),
            label(r"Moore's paradox: \ `it's raining, \ but I don't believe it' \ can be true", font_size=24,
                  color=GOAL),
            label(r"yet in KD45 \ $B(p \land \lnot Bp)$ \ is inconsistent: \ it can never be believed", font_size=24,
                  color=BAD),
            label(r"and knowledge and belief together: \ Stalnaker (2006) \ derives `believing is believing you "
                  r"know'", font_size=21, color=GREY_B)).arrange(DOWN, buff=0.3).move_to([0, -0.4, 0])
        with self.voiceover(
            "Belief obeys different laws. <bookmark mark='a'/>A belief can be false, so the axiom T goes. "
            "<bookmark mark='b'/>In its place, consistency: if you believe phi, you do not believe its negation. "
            "That is the axiom D, true on frames where every world sees at least one world. "
            "<bookmark mark='c'/>The introspection axioms, four and five, are usually kept. The result is the "
            "system KD45. <bookmark mark='d'/>G. E. Moore noticed a paradox here. The sentence 'it's raining, but I "
            "don't believe it' can perfectly well be true. <bookmark mark='e'/>Yet nobody can consistently believe "
            "it: in KD45, believing it would mean believing that it rains, and, by introspection, believing that one "
            "does not believe it. <bookmark mark='f'/>Robert Stalnaker, combining the two logics in 2006, showed "
            "that on natural assumptions, to believe something is to believe that you know it."
        ) as vo:
            self.play(FadeIn(head))
            for mk, r in zip("abcdef", rows):
                vo.wait_until(mk)
                self.play(FadeIn(r, shift=UP * 0.1))
        self.clear_scene()

    def critics(self):
        head = label(r"Two objections", font_size=32, color=CONN).to_edge(UP, buff=0.4)
        a = VGroup(label(r"negative introspection is too strong", font_size=25, color=BAD),
                   label(r"you believe you know where your keys are;", font_size=21),
                   label(r"they were moved: \ you don't know, \ and you don't know that you don't", font_size=21),
                   label(r"and KK fails under margins for error \ (Part 11)", font_size=21, color=GREY_A)).arrange(
            DOWN, buff=0.15)
        b = VGroup(label(r"logical omniscience", font_size=25, color=BAD),
                   label(r"axiom K makes knowledge closed under consequence:", font_size=21),
                   label(r"know the axioms of arithmetic, \ and you know whether Goldbach is true", font_size=21),
                   label(r"repairs: \ awareness (Fagin and Halpern 1988), \ impossible worlds, \ bounded "
                         r"resources", font_size=20, color=GREY_A)).arrange(DOWN, buff=0.15)
        for g in (a, b):
            for m in g:
                if m.width > 6.4:
                    m.width = 6.4
            g.arrange(DOWN, buff=0.15)
        cols = VGroup(a, b).arrange(DOWN, buff=0.7).move_to([0, -0.2, 0])
        foot = label(r"S5 is an idealization: \ the knowledge of a perfect reasoner with perfect access to herself",
                     font_size=24, color=GOAL).to_edge(DOWN, buff=0.4)
        with self.voiceover(
            "S5 is an idealization, and philosophers have pressed on both ends of it. <bookmark mark='a'/>Negative "
            "introspection is too strong. You believe you know where your keys are; someone moved them. You do not "
            "know where they are, and you do not know that you do not know. And Part 11 showed that even positive "
            "introspection fails when knowledge has margins for error. <bookmark mark='b'/>The other problem is "
            "logical omniscience. By axiom K, knowledge is closed under logical consequence, so anyone who knew the "
            "axioms of arithmetic would know whether Goldbach's conjecture is true. Repairs include models of "
            "awareness, impossible worlds, and reasoners with bounded resources. <bookmark mark='c'/>So S5 describes "
            "a perfect reasoner with perfect access to herself. Its power is that it lets us reason exactly about "
            "many such reasoners at once, which is where we go next."
        ) as vo:
            self.play(FadeIn(head))
            vo.wait_until("a")
            self.play(FadeIn(a))
            vo.wait_until("b")
            self.play(FadeIn(b))
            vo.wait_until("c")
            self.play(FadeIn(foot))
        self.clear_scene()

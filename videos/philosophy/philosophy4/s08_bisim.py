from __future__ import annotations

from videos.philosophy.philosophy4.common import *  # noqa: F403

SIX = {0: (-2.4, 0.0, 0), 1: (0.0, 1.9, 0), 2: (0.0, 0.0, 0), 5: (0.0, -1.9, 0), 3: (2.4, 1.9, 0),
       4: (2.4, 0.0, 0)}


class Bisim(VoiceoverScene):
    def construct(self):
        card = chapter_card(7, r"What modal logic cannot see", r"When do two models look the same from inside?",
                            lit=(1976,), part=PART)
        with self.voiceover("Chapter seven. What modal logic cannot see."):
            self.play(FadeIn(card[0], shift=UP * 0.2), FadeIn(card[1]))
        self.play(FadeOut(card))
        self.definition()
        self.minimize()
        self.loop()
        self.benthem()

    def definition(self):
        defn = definition_card(r"bisimulation $Z$", r"a relation between the worlds of two models such that, whenever "
                               r"$w Z w'$: \ the same atoms are true at $w$ and $w'$; \ every move from $w$ is matched "
                               r"by a move from $w'$ to a $Z$-related world \ (forth), \ and vice versa \ (back)",
                               width=9.0, font_size=24, color=GOAL).to_edge(UP, buff=0.5)
        thm = theorem_card(r"Invariance", r"bisimilar worlds satisfy exactly the same modal formulas", width=7.0,
                           font_size=24).move_to([0, -0.8, 0])
        why = label(r"proof: \ induction on formulas; \ the $\Box$ case uses forth and back", font_size=24,
                    color=GREY_A).to_edge(DOWN, buff=0.6)
        with self.voiceover(
            "A modal formula looks at the world from inside: from here, it can only follow arrows. When do two "
            "worlds look the same from inside? <bookmark mark='a'/>When there is a bisimulation between them: a "
            "relation that matches worlds with the same atoms, such that every move on one side can be matched by a "
            "move on the other, to matched worlds, in both directions. <bookmark mark='b'/>The basic theorem: "
            "bisimilar worlds satisfy exactly the same modal formulas. <bookmark mark='c'/>The proof is an "
            "induction on formulas; the box case uses the back and forth conditions."
        ) as vo:
            vo.wait_until("a")
            self.play(FadeIn(defn))
            vo.wait_until("b")
            self.play(FadeIn(thm, shift=UP * 0.2))
            vo.wait_until("c")
            self.play(FadeIn(why))
        self.clear_scene()

    def minimize(self):
        d = load("bisim")
        V = {"p": set(d["p"])}
        g = WorldGraph(d["worlds"], [tuple(x) for x in d["R"]], V, pos=SIX, center=[-3.0, -0.3, 0], scale_pos=0.85)
        cols = [P.CLAIM, P.AGENT, GOAL, OK]
        rings = VGroup(*[Circle(radius=0.42, color=c, stroke_width=5).move_to(g.world[w][0]) for b, c in
                         zip(d["blocks"], cols) for w in b])
        qpos = {0: (-1.4, 0.0, 0), 1: (0.4, 1.0, 0), 2: (1.8, 1.0, 0), 3: (0.4, -1.0, 0)}
        Q = WorldGraph(list(range(len(d["blocks"]))), [tuple(x) for x in d["quotient_R"]],
                       {"p": set(d["quotient_p"])}, pos=qpos, center=[4.0, -0.3, 0], scale_pos=1.0,
                       names={i: rf"[{','.join(map(str, b))}]" for i, b in enumerate(d["blocks"])}, font_size=22)
        for i, c in enumerate(cols):
            Q.world[i][0].set_stroke(c, width=4)
        arr = Arrow([-0.2, -0.3, 0], [1.9, -0.3, 0], color=GREY_B)
        al = label(r"quotient", font_size=22, color=GREY_A).next_to(arr, UP, buff=0.1)
        cap = label(rf"{len(d['worlds'])} worlds, \ {len(d['blocks'])} kinds: \ the smallest model that no modal "
                    r"formula can tell apart", font_size=24, color=GOAL).to_edge(DOWN, buff=0.5)
        with self.voiceover(
            "Bisimulation also compresses. <bookmark mark='a'/>Here is a model with six worlds. <bookmark mark='b'/>"
            "The Reasoner computes the largest bisimulation of the model with itself, by repeatedly removing pairs "
            "that break the back-and-forth conditions. Worlds one and two are bisimilar: both have p, and both lead "
            "to a dead end without p. Worlds three and four are bisimilar too. <bookmark mark='c'/>Merge each class "
            "into one world. <bookmark mark='d'/>The result has four worlds, and no modal formula can tell it from "
            "the original. Process algebra and model checkers use exactly this to shrink systems before checking "
            "them."
        ) as vo:
            vo.wait_until("a")
            self.play(FadeIn(g))
            vo.wait_until("b")
            self.play(LaggedStart(*[Create(r) for r in rings], lag_ratio=0.15))
            vo.wait_until("c")
            self.play(GrowArrow(arr), FadeIn(al), FadeIn(Q))
            vo.wait_until("d")
            self.play(FadeIn(cap))
        self.clear_scene()

    def loop(self):
        d = load("bisim")
        L = WorldGraph([0], {(0, 0)}, {"p": {0}}, pos={0: (0, 0, 0)}, center=[-3.4, -0.5, 0])
        C = WorldGraph([0, 1, 2], {(0, 1), (1, 2), (2, 0)}, {"p": {0, 1, 2}}, center=[2.8, -0.5, 0], scale_pos=0.7)
        lines = VGroup(*[DashedLine(L.world[0][0].get_center(), C.world[v][0].get_center(), color=GOAL,
                                    stroke_width=2) for _, v in d["loop_cycle"]])
        cap = VGroup(label(r"one world that sees itself \ $\sim$ \ three worlds in a cycle", font_size=26, color=GOAL),
                     label(r"so no modal formula says `this world sees itself', \ or counts the worlds of a cycle",
                           font_size=24, color=BAD)).arrange(DOWN, buff=0.2).to_edge(DOWN, buff=0.5)
        with self.voiceover(
            "Bisimulation also shows what modal logic cannot say. <bookmark mark='a'/>On the left, one world that "
            "sees itself. On the right, three worlds in a cycle, all with p. <bookmark mark='b'/>Match the single "
            "world with each of the three: every move is matched, back and forth. They are bisimilar. "
            "<bookmark mark='c'/>So no modal formula can say 'this world sees itself', since that is true on the left "
            "and false on the right, and none can count the length of a cycle."
        ) as vo:
            vo.wait_until("a")
            self.play(FadeIn(L), FadeIn(C))
            vo.wait_until("b")
            self.play(LaggedStart(*[Create(x) for x in lines], lag_ratio=0.3))
            vo.wait_until("c")
            self.play(FadeIn(cap))
        self.clear_scene()

    def benthem(self):
        st = VGroup(MathTex(r"\mathrm{ST}_x(\Box p)", r"\;=\;", r"\forall y\, (R(x, y) \to P(y))", font_size=40),
                    MathTex(r"\mathrm{ST}_x(\Diamond p)", r"\;=\;", r"\exists y\, (R(x, y) \land P(y))",
                            font_size=40)).arrange(DOWN, buff=0.3).move_to([0, 1.6, 0])
        for r in st:
            r[0].set_color(GOAL)
        sl = label(r"the standard translation: \ modal logic inside the first-order logic of Part 3", font_size=24,
                   color=GREY_A).next_to(st, DOWN, buff=0.3)
        thm = theorem_card(r"van Benthem's theorem (1976)", r"a first-order formula $\varphi(x)$ is equivalent to "
                           r"the translation of a modal formula \ iff \ $\varphi$ is invariant under bisimulation",
                           width=9.6, font_size=24).move_to([0, -1.0, 0])
        moral = label(r"modal logic is exactly the bisimulation-invariant part of first-order logic", font_size=26,
                      color=OK).to_edge(DOWN, buff=0.5)
        with self.voiceover(
            "How does modal logic sit inside the first-order logic of Part 3? <bookmark mark='a'/>Translate it: "
            "necessarily p at x becomes 'for every y, if x sees y, then y has P'; possibly p, 'there is a y that x "
            "sees, with P'. <bookmark mark='b'/>Every modal formula becomes a first-order formula with one free "
            "variable. <bookmark mark='c'/>In 1976 Johan van Benthem proved which ones: a first-order formula comes "
            "from a modal formula exactly when bisimulation cannot change its truth value. <bookmark mark='d'/>Modal "
            "logic is the bisimulation-invariant part of first-order logic, a characterization in the spirit of "
            "Lindström's theorem."
        ) as vo:
            vo.wait_until("a")
            self.play(FadeIn(st))
            vo.wait_until("b")
            self.play(FadeIn(sl))
            vo.wait_until("c")
            self.play(FadeIn(thm, shift=UP * 0.2))
            vo.wait_until("d")
            self.play(FadeIn(moral))
        self.clear_scene()

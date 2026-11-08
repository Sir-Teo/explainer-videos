from __future__ import annotations

from videos.philosophy.philosophy4.common import *  # noqa: F403

TRI = {0: (-1.6, -1.0, 0), 1: (1.6, -1.0, 0), 2: (0.0, 1.5, 0)}


class Corr(VoiceoverScene):
    def construct(self):
        card = chapter_card(4, r"Axioms and frames", r"Which shapes of arrows make which axioms true?", lit=(1959,),
                            part=PART)
        with self.voiceover("Chapter four. Axioms and frames."):
            self.play(FadeIn(card[0], shift=UP * 0.2), FadeIn(card[1]))
        self.play(FadeOut(card))
        self.validity()
        self.proof_T()
        self.proof_4()
        self.morph()
        self.table()
        self.meaning()

    def validity(self):
        defn = definition_card(r"valid on a frame", r"true at every world, \ under every way of choosing where the "
                               r"atoms are true", width=7.2, font_size=24, color=GOAL).to_edge(UP, buff=0.5)
        q = MathTex(r"\Box p \to p", r"\ \text{ valid on } (W, R) \iff \ ?", font_size=44).move_to([0, 0.2, 0])
        q[0].set_color(GOAL)
        why = label(r"validity on a frame quantifies over every valuation: \ a statement about $R$ alone", font_size=24,
                    color=GREY_A).to_edge(DOWN, buff=0.8)
        with self.voiceover(
            "Truth in a model depends on where p happens to be true. To study the axioms we need something "
            "sturdier. <bookmark mark='a'/>A formula is valid on a frame when it is true at every world under every "
            "possible choice of where the atoms are true. <bookmark mark='b'/>Then a question with a clean answer "
            "becomes possible: on which frames is 'if necessarily p, then p' valid? <bookmark mark='c'/>Because we "
            "quantify over every valuation, the answer can only depend on the arrows."
        ) as vo:
            self.play(FadeIn(defn))
            vo.wait_until("a")
            vo.wait_until("b")
            self.play(Write(q))
            vo.wait_until("c")
            self.play(FadeIn(why))
        self.clear_scene()

    def proof_T(self):
        thm = theorem_card(r"T and reflexivity", r"$\Box p \to p$ is valid on a frame \ $\iff$ \ every world sees "
                           r"itself", width=7.4, font_size=24).to_edge(UP, buff=0.4)
        a = VGroup(label(r"$\Leftarrow$ \ if $wRw$ and $\Box p$ holds at $w$, \ then $p$ holds at every world $w$ "
                         r"sees, \ including $w$", font_size=24),
                   label(r"$\Rightarrow$ \ if some $w$ does not see itself, \ make $p$ true everywhere except at $w$:",
                         font_size=24)).arrange(DOWN, aligned_edge=LEFT, buff=0.3).next_to(thm, DOWN, buff=0.45)
        g = WorldGraph([0, 1, 2], {(0, 1), (0, 2), (1, 1), (2, 2)}, {"p": {1, 2}}, pos=TRI, center=[-0.5, -1.6, 0],
                       scale_pos=0.7, names={0: "w", 1: "v_1", 2: "v_2"})
        res = VGroup(MathTex(r"w \models \Box p", font_size=32, color=OK),
                     MathTex(r"w \not\models p", font_size=32, color=BAD)).arrange(DOWN, buff=0.2).next_to(
            g, RIGHT, buff=0.9)
        with self.voiceover(
            "Here is the theorem, and its proof, which fits on one screen. <bookmark mark='a'/>Suppose every world "
            "sees itself. If necessarily p is true at w, then p is true at every world w sees, and w is one of them. "
            "So p is true at w. <bookmark mark='b'/>Conversely, suppose some world w does not see itself. Make p true "
            "everywhere except at w. <bookmark mark='c'/>Then at w, necessarily p is true, since every world w sees "
            "has p, and p is false. The axiom fails. So T is valid on exactly the reflexive frames."
        ) as vo:
            self.play(FadeIn(thm))
            vo.wait_until("a")
            self.play(FadeIn(a[0]))
            vo.wait_until("b")
            self.play(FadeIn(a[1]))
            self.play(FadeIn(g))
            vo.wait_until("c")
            self.play(FadeIn(res))
        self.clear_scene()

    def proof_4(self):
        thm = theorem_card(r"4 and transitivity", r"$\Box p \to \Box\Box p$ is valid on a frame \ $\iff$ \ "
                           r"$uRv$ and $vRw$ always give $uRw$", width=7.6, font_size=24).to_edge(UP, buff=0.4)
        pos = {0: (-2.0, -0.4, 0), 1: (0.0, 1.0, 0), 2: (2.0, -0.4, 0)}
        g = WorldGraph([0, 1, 2], {(0, 1), (1, 2)}, {"p": {1}}, pos=pos, center=[-2.6, -0.9, 0], scale_pos=0.8,
                       names={0: "u", 1: "v", 2: "w"})
        txt = VGroup(label(r"if not: \ $uRv$, $vRw$, \ but not $uRw$", font_size=24),
                     label(r"make $p$ true exactly at the worlds $u$ sees: \ here, $v$", font_size=24),
                     label(r"$\Box p$ holds at $u$; \ $\Box\Box p$ fails, \ since $v$ sees $w$ and $w$ lacks $p$",
                           font_size=24, color=BAD),
                     label(r"and if $R$ is transitive, \ whatever $u$ reaches in two steps it reaches in one",
                           font_size=24, color=OK)).arrange(DOWN, aligned_edge=LEFT, buff=0.25).move_to([3.0, -0.9, 0])
        with self.voiceover(
            "The same recipe proves the match for axiom four. <bookmark mark='a'/>Suppose the frame is not "
            "transitive: u sees v, v sees w, but u does not see w. <bookmark mark='b'/>Make p true exactly at the "
            "worlds u sees, here just v. <bookmark mark='c'/>Then necessarily p holds at u, but necessarily "
            "necessarily p fails, because v sees w, where p is false. <bookmark mark='d'/>Conversely, if the arrows "
            "are transitive, any world u reaches in two steps it reaches in one, so whatever is necessary at u is "
            "necessarily necessary. Every proof in this chapter has this shape: a valuation tailored to the frame "
            "refutes the axiom wherever the condition fails."
        ) as vo:
            self.play(FadeIn(thm))
            vo.wait_until("a")
            self.play(FadeIn(g.discs), Create(g.arrows), FadeIn(txt[0]))
            vo.wait_until("b")
            self.play(FadeIn(txt[1]))
            vo.wait_until("c")
            self.play(FadeIn(txt[2]), Indicate(g.world[2][0], color=BAD))
            vo.wait_until("d")
            self.play(FadeIn(txt[3]))
        self.clear_scene()

    def morph(self):
        base = {(0, 1), (1, 2)}
        stages = [("none", base, r"a frame: \ no axiom beyond K"),
                  ("T", base | {(0, 0), (1, 1), (2, 2)}, r"+ reflexive: \ T"),
                  ("4", base | {(0, 0), (1, 1), (2, 2), (0, 2)}, r"+ transitive: \ S4"),
                  ("5", {(i, j) for i in range(3) for j in range(3)}, r"+ symmetric: \ S5, \ every world sees every "
                                                                       r"world")]
        cap = None
        g = None
        with self.voiceover(
            "Watch a frame change as axioms are imposed. <bookmark mark='a'/>Three worlds, each seeing the next. "
            "Only K holds. <bookmark mark='b'/>Demand T, and every world must see itself. <bookmark mark='c'/>Demand "
            "four as well, and the arrows must be transitive: world zero must see world two. That is S4. "
            "<bookmark mark='d'/>Demand five too, and the frame becomes an equivalence relation: here, every world "
            "sees every world. That is S5, Leibniz's picture, where possible means possible from anywhere."
        ) as vo:
            for mk, (nm, R, txt) in zip("abcd", stages):
                if mk != 'a':
                    vo.wait_until(mk)
                g2 = WorldGraph([0, 1, 2], R, {}, pos=TRI, center=[0, -0.3, 0], scale_pos=1.0)
                c2 = label(txt, font_size=28, color=GOAL).to_edge(DOWN, buff=0.6)
                if g is None:
                    self.play(FadeIn(g2), FadeIn(c2))
                else:
                    new = [a for k, a in g2.arrow.items() if k not in g.arrow]
                    self.play(FadeTransform(cap, c2), *[Create(a) for a in new])
                    self.remove(g, *new)
                    self.add(g2)
                g, cap = g2, c2
        self.clear_scene()

    def table(self):
        d = load("corr")
        names = {"T": r"reflexive", "D": r"serial: \ every world sees one", "B": r"symmetric", "4": r"transitive",
                 "5": r"Euclidean"}
        forms = {"T": "[]p -> p", "D": "[]p -> <>p", "B": "p -> []<>p", "4": "[]p -> [][]p", "5": "<>p -> []<>p"}
        hd = [label(t, font_size=22, color=P.CLAIM) for t in (r"axiom", r"frame condition", r"3 worlds",
                                                              r"4 worlds", r"agree")]
        rows = []
        for ax in ["T", "D", "B", "4", "5"]:
            r3, r4 = d[ax]
            rows.append([mf(forms[ax], font_size=26), label(names[ax], font_size=22),
                         MathTex(f"{r3['valid']}" + r"/512", font_size=24),
                         MathTex(f"{r4['valid']:,}".replace(",", "{,}") + r"/65{,}536", font_size=24),
                         label(r"every frame \ $\checkmark$", font_size=22, color=OK)])
        grid = ValueGrid(hd, rows, col_w=[2.6, 3.6, 1.5, 2.4, 2.4], cell_h=0.56, font_size=22).move_to([0, 0.4, 0])
        cap = label(r"for each frame: \ is the axiom valid? \ does the condition hold? \ always the same answer",
                    font_size=24, color=GREY_A).to_edge(DOWN, buff=0.6)
        with self.voiceover(
            "The same holds for the others, each with its own proof. <bookmark mark='a'/>D, necessarily p implies "
            "possibly p, matches seriality: every world sees at least one world. B matches symmetry, four matches "
            "transitivity, and five matches the Euclidean property: two worlds visible from one see each other. "
            "<bookmark mark='b'/>The Reasoner checked every pairing exhaustively, on all five hundred and twelve "
            "frames with three worlds and all sixty-five thousand five hundred and thirty-six with four. "
            "<bookmark mark='c'/>On every single frame, the axiom is valid exactly when the condition holds. Proof "
            "and brute force agree."
        ) as vo:
            self.play(FadeIn(grid.head), FadeIn(grid.rows_bg), FadeIn(grid.rule))
            vo.wait_until("a")
            self.play(LaggedStart(*[FadeIn(VGroup(grid.cell[r][0], grid.cell[r][1])) for r in range(5)],
                                  lag_ratio=0.3), run_time=3)
            vo.wait_until("b")
            self.play(LaggedStart(*[FadeIn(VGroup(grid.cell[r][2], grid.cell[r][3])) for r in range(5)],
                                  lag_ratio=0.2))
            vo.wait_until("c")
            self.play(LaggedStart(*[FadeIn(grid.cell[r][4]) for r in range(5)], lag_ratio=0.2), FadeIn(cap))
        self.clear_scene()

    def meaning(self):
        head = label(r"So the axioms are claims about the arrows", font_size=32, color=CONN).to_edge(UP, buff=0.5)
        rows = VGroup(
            VGroup(label(r"knowledge:", font_size=26, color=GOAL),
                   label(r"T, \ `what is known is true': \ the actual world is never ruled out", font_size=24)),
            VGroup(label(r"positive introspection:", font_size=26, color=GOAL),
                   label(r"4, \ `if you know, you know that you know' \ (contested: Part 11)", font_size=24)),
            VGroup(label(r"obligation:", font_size=26, color=GOAL),
                   label(r"D but not T: \ duties can be broken, \ but they are never jointly impossible",
                         font_size=24)),
            VGroup(label(r"time:", font_size=26, color=GOAL),
                   label(r"4 but not T: \ later than later is later; \ now is not later than now", font_size=24)))
        for r in rows:
            r.arrange(RIGHT, buff=0.4)
        rows.arrange(DOWN, aligned_edge=LEFT, buff=0.4).next_to(head, DOWN, buff=0.6)
        with self.voiceover(
            "This turns arguments about axioms into arguments about arrows. <bookmark mark='a'/>For knowledge, T "
            "says what is known is true: the actual world is never ruled out. <bookmark mark='b'/>Four says that if "
            "you know something, you know that you know it, which Timothy Williamson has argued against, in Part 11. "
            "<bookmark mark='c'/>For obligation we want D but not T: duties can be broken, but they can always be "
            "met together. <bookmark mark='d'/>And for time, four but not T: a moment later than a later moment is "
            "later, but now is not later than now."
        ) as vo:
            self.play(FadeIn(head))
            for mk, r in zip("abcd", rows):
                vo.wait_until(mk)
                self.play(FadeIn(r, shift=RIGHT * 0.2))
        self.clear_scene()

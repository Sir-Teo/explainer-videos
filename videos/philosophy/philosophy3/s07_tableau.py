from __future__ import annotations

from videos.philosophy.philosophy3.common import *  # noqa: F403

BARBARA = {"lines": [("forall x (M(x) -> P(x))", r"premise", False), ("forall x (S(x) -> M(x))", r"premise", False),
                     ("~forall x (S(x) -> P(x))", r"denied conclusion", False),
                     ("~(S(a) -> P(a))", r"$\delta$: new name $a$", False), ("S(a)", r"$\alpha$", False),
                     ("~P(a)", r"$\alpha$", False), ("M(a) -> P(a)", r"$\gamma$: line 1 at $a$", False)],
           "kids": [{"lines": [("~M(a)", r"$\beta$", False), ("S(a) -> M(a)", r"$\gamma$: line 2", False)],
                     "kids": [{"lines": [("~S(a)", r"$\beta$", True)]}, {"lines": [("M(a)", r"$\beta$", True)]}]},
                    {"lines": [("P(a)", r"$\beta$", True)]}]}

OPEN = {"lines": [("exists x (S(x) & P(x))", r"premise", False), ("exists x (P(x) & M(x))", r"premise", False),
                  ("~exists x (S(x) & M(x))", r"denied conclusion", False), ("S(a) & P(a)", r"$\delta$: $a$", False),
                  ("P(b) & M(b)", r"$\delta$: $b$", False), ("~(S(a) & M(a))", r"$\gamma$: $a$", False)],
        "kids": [{"lines": [("~S(a)", r"$\beta$", True)]},
                 {"lines": [("~M(a)", r"$\beta$", False), ("~(S(b) & M(b))", r"$\gamma$: $b$", False)],
                  "kids": [{"lines": [("~S(b)", r"open", False)]}, {"lines": [("~M(b)", r"$\beta$", True)]}]}]}


class Tableau(VoiceoverScene):
    def construct(self):
        card = chapter_card(6, r"Trees that find countermodels", r"Can a machine search for a counterexample?",
                            lit=(1955,), part=PART)
        with self.voiceover("Chapter six. Trees that find countermodels."):
            self.play(FadeIn(card[0], shift=UP * 0.2), FadeIn(card[1]))
        self.play(FadeOut(card))
        self.idea()
        self.rules()
        self.barbara()
        self.open_branch()
        self.forever()

    def idea(self):
        hcs = VGroup(history_card(1955, r"Evert Beth; \ Jaakko Hintikka", r"semantic tableaux; model sets",
                                  width=5.2, color=HIST),
                     history_card(1968, r"Raymond Smullyan", r"\textit{First-Order Logic}: the tree method, "
                                  r"unified", width=5.2, color=HIST)).arrange(RIGHT, buff=0.5).to_edge(UP, buff=0.4)
        steps = VGroup(
            label(r"1. \ to test $\Gamma \models \varphi$, \ try to build a world where $\Gamma$ is true and "
                  r"$\varphi$ false", font_size=26),
            label(r"2. \ break each formula into what it demands; \ split at every `or'", font_size=26),
            label(r"3. \ a branch that contains $A$ and $\lnot A$ is impossible: \ close it \ $\times$",
                  font_size=26, color=BAD),
            label(r"4. \ every branch closed: \ no such world, \ \textbf{valid}", font_size=26, color=OK),
            label(r"5. \ a finished open branch: \ a recipe for a countermodel", font_size=26, color=GOAL)).arrange(
            DOWN, aligned_edge=LEFT, buff=0.25).next_to(hcs, DOWN, buff=0.5)
        with self.voiceover(
            "In 1955 Evert Beth and Jaakko Hintikka, independently, turned the definition of validity into a search. "
            "Raymond Smullyan's book of 1968 gave the method its cleanest form. <bookmark mark='a'/>To test whether "
            "a conclusion follows, try to build a world where the premises are true and the conclusion false. "
            "<bookmark mark='b'/>Break each formula into what it demands of the world, and wherever there is an "
            "'or', split the search in two. <bookmark mark='c'/>A branch that demands both A and not A cannot "
            "describe any world: close it. <bookmark mark='d'/>If every branch closes, no counterexample exists, "
            "and the argument is valid. <bookmark mark='e'/>And if a branch is finished and still open, it is a "
            "recipe for a countermodel."
        ) as vo:
            self.play(LaggedStart(*[FadeIn(h, shift=DOWN * 0.2) for h in hcs], lag_ratio=0.3))
            for mk, st in zip("abcde", steps):
                vo.wait_until(mk)
                self.play(FadeIn(st, shift=RIGHT * 0.2))
        self.clear_scene()

    def rules(self):
        def box(name, color, top, rows, note_):
            t = VGroup(MathTex(top, font_size=32), *[MathTex(r, font_size=30, color=color) for r in rows])
            t.arrange(DOWN, buff=0.15)
            head = label(name, font_size=26, color=color)
            nt = label(note_, font_size=20, color=GREY_A)
            g = VGroup(head, t, nt).arrange(DOWN, buff=0.2)
            frame = SurroundingRectangle(g, color=color, buff=0.2, corner_radius=0.12, stroke_width=2)
            return VGroup(frame, g)

        boxes = VGroup(
            box(r"$\alpha$: \ both", P.CLAIM, r"A \land B", [r"A", r"B"], r"also $\lnot(A \lor B)$, $\lnot(A \to B)$"),
            box(r"$\beta$: \ split", P.AGENT, r"A \lor B", [r"A \ \mid \ B"], r"also $A \to B$, $\lnot(A \land B)$"),
            box(r"$\gamma$: \ every name", QUANT, r"\forall x\, \varphi(x)", [r"\varphi(a),\ \varphi(b),\ \dots"],
                r"also $\lnot \exists x\, \varphi$; \ may be used again"),
            box(r"$\delta$: \ a new name", GOAL, r"\exists x\, \varphi(x)", [r"\varphi(c),\ c \text{ new}"],
                r"also $\lnot \forall x\, \varphi$; \ once")).arrange(RIGHT, buff=0.3)
        if boxes.width > 13.4:
            boxes.width = 13.4
        boxes.move_to([0, 0.4, 0])
        foot = label(r"Smullyan's four kinds of formula: \ every rule is one of these", font_size=24,
                     color=GREY_A).to_edge(DOWN, buff=0.6)
        with self.voiceover(
            "Smullyan noticed that every rule is one of four kinds. <bookmark mark='a'/>Alpha formulas, like A and B, "
            "demand two things at once: write both on the branch. <bookmark mark='b'/>Beta formulas, like A or B, "
            "demand one of two: split. <bookmark mark='c'/>Gamma formulas, like 'for all x', demand something of "
            "every object: instantiate with any name on the branch, as often as needed. <bookmark mark='d'/>Delta "
            "formulas, like 'there exists an x', demand a witness: give it a brand-new name, exactly the condition "
            "of the last chapter."
        ) as vo:
            self.play(FadeIn(foot))
            for mk, b in zip("abcd", boxes):
                vo.wait_until(mk)
                self.play(FadeIn(b, shift=UP * 0.2))
        self.clear_scene()

    def barbara(self):
        d = load("tableaux")["barbara"]
        tree = tableau_tree(BARBARA, top=3.35, col_w=3.4, line_h=0.47, font_size=26, x_center=-1.0)
        side = VGroup(label(r"Barbara:", font_size=26, color=GOAL),
                      label(r"all $M$ are $P$; \ all $S$ are $M$;", font_size=24),
                      label(r"so all $S$ are $P$", font_size=24)).arrange(DOWN, aligned_edge=LEFT, buff=0.12)
        side.to_corner(UR, buff=0.5)
        res = wrapped_label(rf"the Reasoner: \ {len(d['steps'])} steps, \ {d['branches']} branches, \ all closed \ "
                            r"$\checkmark$", 3.0, font_size=24, color=OK).next_to(side, DOWN, buff=0.5).align_to(side, LEFT)
        s = tree.steps
        with self.voiceover(
            "Here is Barbara, run as a tree. <bookmark mark='a'/>The two premises, and the denial of the conclusion: "
            "not everything that is S is P. <bookmark mark='b'/>A delta rule: so some object, call it a, is S and "
            "not P. <bookmark mark='c'/>Apply the first premise to a: if a is M, a is P. That is a beta formula, "
            "so the tree splits. <bookmark mark='d'/>On the right, a is P, but we already have not P: closed. "
            "<bookmark mark='e'/>On the left, a is not M. Apply the second premise to a: if a is S, a is M. Split "
            "again. <bookmark mark='f'/>a is not S: closed, since a is S. a is M: closed, since a is not M. "
            "<bookmark mark='g'/>Every branch is closed, so there is no world where the premises hold and the "
            "conclusion fails. Barbara is valid."
        ) as vo:
            self.play(FadeIn(side))
            self.play(LaggedStart(*[FadeIn(p) for p in s[:3]], lag_ratio=0.3))
            vo.wait_until("b")
            self.play(LaggedStart(*[FadeIn(p) for p in s[3:6]], lag_ratio=0.3))
            vo.wait_until("c")
            self.play(FadeIn(s[6]))
            self.play(Create(s[7]))
            # depth-first: left segment, its split and leaves, then the right leaf
            left_a, left_b, split2, leaf1, leaf2, right = s[8], s[9], s[10], s[11], s[12], s[13]
            vo.wait_until("d")
            self.play(FadeIn(right))
            vo.wait_until("e")
            self.play(FadeIn(left_a), FadeIn(left_b))
            self.play(Create(split2))
            vo.wait_until("f")
            self.play(FadeIn(leaf1))
            self.play(FadeIn(leaf2))
            vo.wait_until("g")
            self.play(FadeIn(res))
        self.clear_scene()

    def open_branch(self):
        d = load("tableaux")["open"]
        cm = d["countermodel"]
        tree = tableau_tree(OPEN, top=3.35, col_w=3.3, line_h=0.47, font_size=26, x_center=-1.4)
        side = VGroup(label(r"some $S$ are $P$; \ some $P$ are $M$;", font_size=24),
                      label(r"so some $S$ are $M$?", font_size=24, color=GOAL)).arrange(DOWN, aligned_edge=LEFT,
                                                                                    buff=0.12).to_corner(UR, buff=0.5)
        s = tree.steps
        leaf_open = s[-2]
        ring = SurroundingRectangle(leaf_open, color=GOAL, buff=0.12, corner_radius=0.1)
        names = {"a0": "a", "a1": "b"}
        rows = []
        for el in cm["domain"]:
            has = [k for k, v in sorted(cm["preds"].items()) if [el] in v]
            rows.append(rf"${names[el]}$: \ " + ", ".join(rf"${k}$" for k in has))
        model = VGroup(label(r"read off the open branch:", font_size=24, color=GOAL),
                       *[label(r_, font_size=26, color=OBJ) for r_ in rows]).arrange(DOWN, aligned_edge=LEFT,
                                                                                    buff=0.15)
        model.next_to(side, DOWN, buff=0.6).align_to(side, LEFT)
        check = label(r"in this world both premises are true \\ and the conclusion is false", font_size=22,
                      color=GREY_A).next_to(model, DOWN, buff=0.3).align_to(model, LEFT)
        assert not d["closed"]
        with self.voiceover(
            "Now an invalid argument. Some S are P, some P are M, so some S are M. <bookmark mark='a'/>Premises, and "
            "the denied conclusion: nothing is both S and M. <bookmark mark='b'/>Two delta rules give two new names: "
            "a is S and P; b is P and M. <bookmark mark='c'/>The denied conclusion is a gamma formula, so apply it "
            "to a: a is not both S and M. Split. Not S closes against S of a. <bookmark mark='d'/>On the other "
            "side, a is not M. Apply the gamma formula again, to b, and split. Not M of b closes. "
            "<bookmark mark='e'/>But b is not S stays open, and nothing is left to do. <bookmark mark='f'/>So read "
            "the world off the branch: a is S and P; b is P and M. In that world both premises are true and the "
            "conclusion is false. The tree did not just say 'invalid'. It built the counterexample."
        ) as vo:
            self.play(FadeIn(side))
            self.play(LaggedStart(*[FadeIn(p) for p in s[:2]], lag_ratio=0.3))
            vo.wait_until("a")
            self.play(FadeIn(s[2]))
            vo.wait_until("b")
            self.play(FadeIn(s[3]), FadeIn(s[4]))
            vo.wait_until("c")
            self.play(FadeIn(s[5]))
            self.play(Create(s[6]))
            self.play(FadeIn(s[7]))
            vo.wait_until("d")
            self.play(FadeIn(s[8]), FadeIn(s[9]))
            self.play(Create(s[10]))
            self.play(FadeIn(s[12]))
            vo.wait_until("e")
            self.play(FadeIn(s[11]), Create(ring))
            vo.wait_until("f")
            self.play(FadeIn(model))
            self.play(FadeIn(check))
        self.clear_scene()

    def forever(self):
        sw = load("tableaux")["swap"]
        st = sw["tableau_steps"]
        news = [r for r in st if r[0].startswith("new")]
        head = VGroup(fm(sw["premise"], font_size=34),
                      MathTex(r"\not\models", font_size=34, color=BAD),
                      fm(sw["conclusion"], font_size=34)).arrange(RIGHT, buff=0.3).to_edge(UP, buff=0.4)
        k = len(news) + 1
        dots = VGroup(*[VGroup(Dot(radius=0.11, color=OBJ), MathTex(rf"a_{{{i}}}", font_size=28, color=OBJ))
                        for i in range(k)])
        for d_ in dots:
            d_[1].next_to(d_[0], DOWN, buff=0.12)
        dots.arrange(RIGHT, buff=1.15).move_to([0, 0.6, 0])
        arrows = VGroup(*[Arrow(dots[i][0].get_center(), dots[i + 1][0].get_center(), buff=0.15, color=REL,
                                stroke_width=3) for i in range(k - 1)])
        more = MathTex(r"\cdots", font_size=40, color=GREY_B).next_to(dots, RIGHT, buff=0.4)
        cap = label(r"each new person must love someone: \ $\gamma$ gives a new demand, \ $\delta$ a new name, "
                    r"\ forever", font_size=24, color=GREY_A).next_to(dots, DOWN, buff=0.7)
        gave = label(rf"the Reasoner's tableau gives up after {len(st)} steps: \ still open, \ never finished",
                     font_size=24, color=BAD).next_to(cap, DOWN, buff=0.3)
        loop = relation_graph(["Ann", "Bo"], [tuple(p) for p in sw["countermodel"]], radius=0.9,
                              center=[0, -2.6, 0])
        loop_l = label(r"a smarter search: \ let $a_1$ love $a_0$ \ (2 people)", font_size=24, color=OK).next_to(
            loop, RIGHT, buff=0.5)
        with self.voiceover(
            "Sometimes the tree never finishes. <bookmark mark='a'/>Test the bad argument of the last chapter: "
            "everyone loves someone, so someone is loved by everyone. <bookmark mark='b'/>The tree introduces a "
            "person, a zero, who must love someone: a new name, a one. But a one must love someone too: a two. And "
            "so on. <bookmark mark='c'/>Each new person brings a new demand, and the demand brings a new person. "
            f"The Reasoner stops after {len(st)} steps with the branch still open and unfinished. "
            "<bookmark mark='d'/>A smarter search would try letting a one love a zero, and find the two-person "
            "countermodel at once. <bookmark mark='e'/>But there is no general rule for when to stop growing a tree "
            "and look for a loop, and Chapter ten will show why there never can be."
        ) as vo:
            self.play(FadeIn(head))
            vo.wait_until("b")
            self.play(FadeIn(dots[0]))
            for i in range(k - 1):
                self.play(GrowArrow(arrows[i]), FadeIn(dots[i + 1]), run_time=0.6)
            self.play(FadeIn(more))
            vo.wait_until("c")
            self.play(FadeIn(cap))
            self.play(FadeIn(gave))
            vo.wait_until("d")
            self.play(FadeIn(loop), FadeIn(loop_l))
            vo.wait_until("e")
            self.play(Indicate(more, color=BAD))
        self.clear_scene()

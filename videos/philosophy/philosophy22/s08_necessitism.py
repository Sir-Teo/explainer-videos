from __future__ import annotations

from videos.philosophy.philosophy22.common import *  # noqa: F403


class Necessitism(VoiceoverScene):
    def construct(self):
        card = chapter_card(7, r"Necessitism and contingentism",
                            r"Could there have been something that there isn't?", lit=(1946, 2013), part=PART)
        with self.voiceover("Chapter seven. Necessitism and contingentism."):
            self.play(FadeIn(card[0], shift=UP * 0.2), FadeIn(card[1]))
        self.play(FadeOut(card))
        self.formula()
        self.child()
        self.williamson()
        self.logic()

    def formula(self):
        hc = history_card(1946, r"Ruth Barcan", r"`A Functional Calculus of First Order Based on Strict "
                                               r"Implication'", width=8.6, color=HIST).to_corner(UL, buff=0.3)
        bf = MathTex(r"\Diamond\, \exists x\, Fx \;\to\; \exists x\, \Diamond\, Fx", font_size=44, color=ABS)
        bf2 = MathTex(r"\forall x\, \Box\, Fx \;\to\; \Box\, \forall x\, Fx", font_size=36, color=ABS)
        g = VGroup(bf, bf2).arrange(DOWN, buff=0.35).move_to([0, 0.6, 0])
        gl = label(r"the Barcan formula, \ and its equivalent with boxes", font_size=19, color=GREY_A).next_to(
            g, DOWN, buff=0.2)
        rows = stack([(r"if there could have been an F, \ then there is something that could have been an F", WHITE),
                      (r"it holds when every world has the same domain; \ it fails when domains vary \ (Kripke, "
                       r"\ 1963)", CPT),
                      (r"so the logic depends on a metaphysical question: \ could there have been other things?",
                       GOAL)], font_size=21, aligned_edge=LEFT, width=12.0).to_edge(DOWN, buff=0.4)
        with self.voiceover(
            "In 1946 Ruth Barcan published the first systems of quantified modal logic, and with them a formula "
            "that now bears her name. <bookmark mark='a'/>If possibly there is an F, then there is something that "
            "possibly is an F. Equivalently, if everything is necessarily F, then necessarily everything is F. "
            "<bookmark mark='b'/>In words: if there could have been an F, there is something which could have been "
            "an F. <bookmark mark='c'/>In Kripke's semantics the formula holds when every world has the same domain "
            "of objects, and fails when domains can vary from world to world. <bookmark mark='d'/>So which logic is "
            "right depends on a metaphysical question: could there have been things other than the things there "
            "are?"
        ) as vo:
            self.play(FadeIn(hc))
            vo.wait_until("a")
            self.play(Write(bf), Write(bf2), FadeIn(gl))
            for mk, r in zip("bcd", rows):
                vo.wait_until(mk)
                self.play(FadeIn(r))
        self.clear_scene()

    def child(self):
        d = load("barcan")
        head = label(r"Wittgenstein's possible child", font_size=30, color=CONN).to_edge(UP, buff=0.3)
        titles = [(r"contingentist", WORLD), (r"necessitist", NAME)]
        groups = VGroup()
        for k, (t, col) in enumerate(titles):
            x = -3.6 + 7.2 * k
            tt = label(t, font_size=24, color=col).move_to([x, 2.5, 0])
            a = island([x - 1.65, 0.9, 0], w=3.1, h=1.7, seed=150 + 2 * k, color=NAME, name=r"actual",
                       font_size=18)
            u = island([x + 1.65, 0.9, 0], w=3.1, h=1.7, seed=151 + 2 * k, color=WORLD, name=r"$u$", font_size=18)
            wa = person([x - 1.65 - (0.65 if k == 1 else 0.0), 0.95, 0], color=DESC, name=r"Wittgenstein",
                        font_size=16)
            wu = person([x + 1.0, 0.95, 0], color=DESC, name=r"Wittgenstein", font_size=16)
            bu = person([x + 2.3, 0.95, 0], color=CPT, name=r"$b$, \ a child", font_size=16)
            grp = VGroup(tt, a, u, wa, wu, bu)
            if k == 1:
                ghost = VGroup(Circle(radius=0.16, color=CPT, stroke_width=2.5).move_to([x - 1.0, 0.95, 0]),
                               label(r"$b$, \ not concrete", font_size=16, color=CPT).move_to([x - 1.0, 0.62, 0]))
                grp.add(ghost)
            groups.add(grp)
        hd = [r"\text{formula}", r"\text{contingentist}", r"\text{necessitist}"]
        rows = []
        for r in d["rows"]:
            rows.append([MathTex(r["formula"].replace("Barcan: ", "").strip("$"), font_size=22),
                         tf(r["contingentist"]), tf(r["necessitist"])])
        grid = ValueGrid(hd, rows, col_w=[6.4, 2.4, 2.4], cell_h=0.5, font_size=19).move_to([0, -1.75, 0])
        with self.voiceover(
            "Take an example. Ludwig Wittgenstein had no children, but he might have had one. <bookmark mark='a'/>"
            "The contingentist model: at the actual world there is Wittgenstein; at world u there is Wittgenstein and "
            "a child, b, who does not exist at the actual world at all. <bookmark mark='b'/>The necessitist model: "
            "the same domain everywhere. At the actual world b exists too, but only as a merely possible object: "
            "not concrete, not a person, not anyone's child. At u, b is concrete, and a child. "
            "<bookmark mark='c'/>The Reasoner evaluates three formulas at the actual world. The Barcan formula: "
            "possibly there is a child, so there is something that could have been a child. False for the "
            "contingentist, true for the necessitist. <bookmark mark='d'/>Necessarily everything is necessarily "
            "something: false for the contingentist, since b exists at u but not at the actual world; true for "
            "the necessitist. <bookmark mark='e'/>And there is something not concrete that could have been "
            "concrete: the necessitist's b."
        ) as vo:
            self.play(FadeIn(head))
            vo.wait_until("a")
            self.play(FadeIn(groups[0]))
            vo.wait_until("b")
            self.play(FadeIn(groups[1]))
            vo.wait_until("c")
            self.play(FadeIn(grid.head), Create(grid.rule), *[FadeIn(grid.cell[0][c]) for c in range(3)])
            for mk, r in zip("de", (1, 2)):
                vo.wait_until(mk)
                self.play(*[FadeIn(grid.cell[r][c]) for c in range(3)])
        self.clear_scene()

    def williamson(self):
        hc = history_card(2013, r"Timothy Williamson", r"\textit{Modal Logic as Metaphysics}", width=6.6,
                          color=HIST).to_corner(UL, buff=0.3)
        f = MathTex(r"\Box\, \forall x\, \Box\, \exists y\,(y = x)", font_size=44, color=NAME).move_to([2.6, 2.4, 0])
        fl = label(r"necessitism: \ necessarily, \ everything is necessarily something", font_size=19,
                   color=NAME).next_to(f, DOWN, buff=0.15)
        rows = [
            (r"the claim", r"whatever there could have been, \ there is; \ only being concrete is contingent", NAME),
            (r"the payoff", r"the simplest modal logic: \ S5, \ the Barcan formula and its converse, \ classical "
                            r"quantifiers", OK),
            (r"the cost", r"there is something that could have been Wittgenstein's child, \ and is in fact "
                          r"nothing concrete", BAD),
            (r"the reframing", r"not `do merely possible things exist?' \ but `is it contingent what there is?'",
             GOAL),
            (r"the method", r"choose the metaphysics by the strength and simplicity of the logic it allows: \ "
                            r"abduction, \ as in science", CPT),
        ]
        g = rows_table(rows, top=0.9, gap=0.42, width=8.8, x_text=-2.6, label_size=21)
        with self.voiceover(
            "Timothy Williamson defended necessitism in a book of 2013. <bookmark mark='a'/>Necessarily, everything "
            "is necessarily something. <bookmark mark='b'/>Whatever there could have been, there is. What is "
            "contingent is only whether a thing is concrete: a person, a planet, a child. <bookmark mark='c'/>The "
            "payoff is logic. Necessitism allows the simplest and strongest quantified modal logic: S5 with the "
            "Barcan formula, its converse, and the ordinary rules for quantifiers. <bookmark mark='d'/>The cost is "
            "ontological. There is something that could have been Wittgenstein's child, though in fact it is "
            "nothing concrete at all. <bookmark mark='e'/>Williamson reframed the old debate. The question is not "
            "whether merely possible things exist, but whether it is contingent what there is. "
            "<bookmark mark='f'/>And he argued for a method: choose the metaphysics by the strength and simplicity of "
            "the logic it supports, as scientists choose theories by abduction."
        ) as vo:
            self.play(FadeIn(hc))
            vo.wait_until("a")
            self.play(Write(f), FadeIn(fl))
            for mk, r in zip("bcdef", g):
                vo.wait_until(mk)
                self.play(FadeIn(r))
        self.clear_scene()

    def logic(self):
        head = label(r"Why the logic forces the question", font_size=30, color=CONN).to_edge(UP, buff=0.35)
        steps = VGroup(
            MathTex(r"1.\quad \forall x\, \Box Fx \to \Box Fx", font_size=28),
            MathTex(r"2.\quad \Diamond \forall x\, \Box Fx \to \Diamond \Box Fx", font_size=28),
            MathTex(r"3.\quad \Diamond \Box Fx \to Fx \qquad (\text{S5})", font_size=28),
            MathTex(r"4.\quad \Diamond \forall x\, \Box Fx \to \forall x\, Fx", font_size=28),
            MathTex(r"5.\quad \forall x\, \Box Fx \to \Box \forall x\, Fx", font_size=28, color=OK)).arrange(
            DOWN, aligned_edge=LEFT, buff=0.22).move_to([-3.2, 0.2, 0])
        why = VGroup(*[label(t, font_size=17, color=GREY_A) for t in (
            r"instantiate the quantifier", r"possibility distributes over a conditional", r"S5's B axiom, contraposed",
            r"chain 2 and 3; \ generalize on $x$", r"necessitate and use S5: \ the Barcan formula")])
        for w_, st in zip(why, steps):
            w_.next_to(st, RIGHT, buff=0.35)
        rows = stack([(r"Prior \ (1956): \ in quantified S5, \ the Barcan formula is a theorem", NAME),
                      (r"to escape it, \ the contingentist must change the logic: \ a free logic for quantifiers, "
                       r"\ or a weaker modal logic", BAD),
                      (r"Kripke's 1963 semantics blocks the proof: \ open formulas may not be necessitated", CPT)],
                     font_size=20, aligned_edge=LEFT, width=12.2).to_edge(DOWN, buff=0.4)
        with self.voiceover(
            "Why can't we simply choose varying domains? Because of a proof. <bookmark mark='a'/>Arthur Prior showed "
            "in 1956 that in quantified S5 with the standard quantifier rules, the Barcan formula is a theorem. The "
            "steps are on screen: instantiate, take possibilities, use S5's characteristic axiom, chain, generalize, "
            "and necessitate. <bookmark mark='b'/>So a contingentist must change something in the logic: use a free "
            "logic, in which quantifier instantiation needs an existence premise, or give up some of S5. "
            "<bookmark mark='c'/>Kripke's 1963 semantics blocks the proof by not allowing formulas with free "
            "variables to be necessitated, generalizing first. The metaphysics of what there could have been is "
            "written into the rules of inference."
        ) as vo:
            self.play(FadeIn(head))
            vo.wait_until("a")
            self.play(FadeIn(rows[0]))
            self.play(LaggedStart(*[AnimationGroup(Write(s_), FadeIn(w_)) for s_, w_ in zip(steps, why)],
                                  lag_ratio=0.45), run_time=5)
            for mk, r in zip("bc", rows[1:]):
                vo.wait_until(mk)
                self.play(FadeIn(r))
        self.clear_scene()

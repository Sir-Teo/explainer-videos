from __future__ import annotations

from videos.philosophy.philosophy7.common import *  # noqa: F403


class Arith(VoiceoverScene):
    def construct(self):
        card = chapter_card(2, r"Arithmetic, axiom by axiom", r"How little do you need to compute?", lit=(1889,),
                            part=PART)
        with self.voiceover("Chapter two. Arithmetic, axiom by axiom."):
            self.play(FadeIn(card[0], shift=UP * 0.2), FadeIn(card[1]))
        self.play(FadeOut(card))
        self.axioms()
        self.compute()
        self.induction()
        self.models()

    def axioms(self):
        head = label(r"Robinson's $Q$ \ (1950): \ seven axioms", font_size=32, color=CONN).to_edge(UP, buff=0.45)
        lang = label(r"the language: \ $0$, \ successor $\mathsf{S}$, \ $+$, \ $\times$; \ so $3$ is written "
                     r"$\mathsf{S}\mathsf{S}\mathsf{S}0$", font_size=26, color=GREY_A).next_to(head, DOWN, buff=0.35)
        rows = VGroup()
        notes = {"Q1": r"0 is no one's successor", "Q2": r"different numbers have different successors",
                 "Q3": r"every other number is a successor", "Q4": r"adding zero", "Q5": r"adding a successor",
                 "Q6": r"times zero", "Q7": r"times a successor"}
        for k, (tex, _) in A.Q_AXIOMS.items():
            rows.add(VGroup(label(k, font_size=24, color=NUM), MathTex(tex, font_size=32),
                            label(notes[k], font_size=22, color=GREY_B)))
        for i, r in enumerate(rows):
            y = 1.4 - 0.62 * i
            r[0].move_to([-5.6, y, 0])
            r[1].move_to([-4.9 + r[1].width / 2, y, 0])
            r[2].move_to([1.2 + r[2].width / 2, y, 0])
        with self.voiceover(
            "To say anything about arithmetic, we need a formal system for it. Here is the weakest one that will "
            "do, from Raphael Robinson in 1950. <bookmark mark='a'/>Its language has zero, a successor symbol S "
            "for plus one, addition and multiplication. Three is S S S zero. <bookmark mark='b'/>Three axioms say "
            "how successor behaves: zero is not a successor, different numbers have different successors, and every "
            "other number is a successor. <bookmark mark='c'/>And four are the school definitions of addition and "
            "multiplication, by recursion on the second argument."
        ) as vo:
            self.play(FadeIn(head))
            vo.wait_until("a")
            self.play(FadeIn(lang))
            vo.wait_until("b")
            self.play(LaggedStart(*[FadeIn(r) for r in rows[:3]], lag_ratio=0.3))
            vo.wait_until("c")
            self.play(LaggedStart(*[FadeIn(r) for r in rows[3:]], lag_ratio=0.3))
        self.clear_scene()

    def compute(self):
        d = load("q")
        head = label(r"$Q$ computes: \ every step is an axiom", font_size=32, color=CONN).to_edge(UP, buff=0.45)

        def chain(steps, x0, y0, dy=0.62, fs=32):
            g = VGroup()
            for i, (t, ax) in enumerate(steps):
                eq = MathTex(("" if i == 0 else "= ") + t, font_size=fs)
                eq.move_to([x0 + eq.width / 2 + (0 if i == 0 else 0.0), y0 - i * dy, 0])
                row = VGroup(eq)
                if ax:
                    row.add(label(ax, font_size=20, color=NUM).next_to(eq, RIGHT, buff=0.3))
                g.add(row)
            return g

        add = chain(d["add"], -6.3, 1.9)
        mul = chain(d["mul"], 0.4, 2.0, dy=0.46, fs=26)
        lab1 = label(r"$2 + 2 = 4$", font_size=28, color=GOAL).next_to(add, DOWN, buff=0.4).align_to(add, LEFT)
        lab2 = label(rf"$2 \times 2 = 4$: \ {len(d['mul']) - 1} steps", font_size=28, color=GOAL).next_to(
            mul, DOWN, buff=0.3).align_to(mul, LEFT)
        moral = label(r"$Q$ proves every true equation between numerals, \ and every false one false",
                      font_size=24, color=OK).to_edge(DOWN, buff=0.35)
        with self.voiceover(
            "Watch Q compute. <bookmark mark='a'/>Two plus two: S S zero plus S S zero. Axiom five moves a successor "
            "outside, twice. Axiom four removes plus zero. What is left is S S S S zero: four. "
            "<bookmark mark='b'/>Two times two takes nine steps: axiom seven unpacks the multiplication into "
            "additions, axiom six removes times zero, and the additions run as before. <bookmark mark='c'/>In this "
            "way Q proves every true equation between numerals, and refutes every false one. That will matter: "
            "Gödel's argument needs only that the system can check computations."
        ) as vo:
            self.play(FadeIn(head))
            vo.wait_until("a")
            self.play(LaggedStart(*[FadeIn(r, shift=DOWN * 0.1) for r in add], lag_ratio=0.5), run_time=3)
            self.play(FadeIn(lab1))
            vo.wait_until("b")
            self.play(LaggedStart(*[FadeIn(r, shift=DOWN * 0.1) for r in mul], lag_ratio=0.3), run_time=4)
            self.play(FadeIn(lab2))
            vo.wait_until("c")
            self.play(FadeIn(moral))
        self.clear_scene()

    def induction(self):
        hc = history_card(1889, r"Giuseppe Peano \ (after Dedekind, 1888)", r"\textit{Arithmetices principia}",
                          width=6.2, color=HIST).to_corner(UL, buff=0.35)
        ind = MathTex(r"\varphi(0) \ \land\ \forall x\,\bigl(\varphi(x) \to \varphi(\mathsf{S}x)\bigr) \ \to\ "
                      r"\forall x\,\varphi(x)", font_size=40, color=GOAL).move_to([0, 1.0, 0])
        cap = label(r"the induction schema: \ one axiom for every formula $\varphi$", font_size=26).next_to(
            ind, DOWN, buff=0.35)
        pa = label(r"$Q$ + induction = \textbf{Peano arithmetic}, \ PA", font_size=30, color=CONN).next_to(
            cap, DOWN, buff=0.6)
        gap = VGroup(label(r"$Q$ cannot prove \ $\forall x\,(0 + x = x)$", font_size=26, color=BAD),
                     label(r"(a model of $Q$ with two extra `numbers' makes it false)", font_size=22,
                           color=GREY_A)).arrange(DOWN, buff=0.15)
        pa2 = label(r"PA proves it, by induction on $x$", font_size=26, color=OK)
        both = VGroup(gap, pa2).arrange(DOWN, buff=0.35).to_edge(DOWN, buff=0.6)
        with self.voiceover(
            "Q can compute, but it cannot generalize. <bookmark mark='a'/>It cannot even prove that zero plus x is "
            "x for every x: there is a model of Q with two extra objects in which that fails. "
            "<bookmark mark='b'/>The missing ingredient is induction, from Dedekind in 1888 and Giuseppe Peano in "
            "1889: if a property holds of zero, and passes from each number to the next, it holds of all. "
            "<bookmark mark='c'/>As a first-order schema, one axiom for each formula, added to Q, it gives Peano "
            "arithmetic, PA, in which almost all of number theory can be carried out. "
            "<bookmark mark='d'/>Gödel's theorems will apply to Q and to PA alike, and to every consistent system "
            "that extends them."
        ) as vo:
            vo.wait_until("a")
            self.play(FadeIn(gap[0]), FadeIn(gap[1]))
            vo.wait_until("b")
            self.play(FadeIn(hc), Write(ind))
            vo.wait_until("c")
            self.play(FadeIn(cap), FadeIn(pa), FadeIn(pa2))
            vo.wait_until("d")
            self.play(Indicate(pa, color=GOAL, scale_factor=1.03))
        self.clear_scene()

    def models(self):
        head = label(r"PA does not pin down the numbers", font_size=32, color=CONN).to_edge(UP, buff=0.45)
        std = VGroup(*[Dot([-6.0 + 0.42 * i, 1.2, 0], radius=0.06, color=TAPE) for i in range(9)])
        stdl = VGroup(*[MathTex(str(i), font_size=20, color=GREY_B).next_to(std[i], DOWN, buff=0.12)
                        for i in range(0, 9, 2)])
        dots = MathTex(r"\cdots", font_size=30, color=TAPE).next_to(std, RIGHT, buff=0.15)
        blocks = VGroup()
        for k, x in enumerate((-0.6, 1.6, 3.4, 5.0)):
            blk = VGroup(*[Dot([x + 0.22 * (j - 3), 1.2, 0], radius=0.05, color=SELF) for j in range(7)])
            blocks.add(VGroup(MathTex(r"\cdots", font_size=22, color=SELF).next_to(blk, LEFT, buff=0.06), blk,
                              MathTex(r"\cdots", font_size=22, color=SELF).next_to(blk, RIGHT, buff=0.06)))
        bl = label(r"each block a copy of the integers, \ $\dots, c-1, c, c+1, \dots$; \ the blocks ordered like the "
                   r"rationals", font_size=22, color=SELF).move_to([2.2, 0.4, 0])
        nl = label(r"$\mathbb{N}$", font_size=26, color=TAPE).move_to([-4.3, 1.9, 0])
        rows = VGroup(label(r"by compactness \ (Part 3): \ PA has models with `numbers' after every numeral",
                            font_size=24),
                      label(r"Skolem (1934): \ every countable nonstandard model looks like this", font_size=24),
                      label(r"Tennenbaum (1959): \ in none of them can $+$ or $\times$ be computed", font_size=24,
                            color=GOAL),
                      label(r"so `PA does not prove $\varphi$' \ can mean: \ $\varphi$ fails in some strange model",
                            font_size=24, color=BAD)).arrange(DOWN, aligned_edge=LEFT, buff=0.25).to_edge(DOWN, buff=0.5)
        with self.voiceover(
            "Even with induction, PA cannot say exactly which things are numbers. <bookmark mark='a'/>By the "
            "compactness theorem of Part 3, PA has models with extra elements, bigger than every numeral. "
            "<bookmark mark='b'/>Thoralf Skolem built the first in 1934. Every countable one looks like this: the "
            "true natural numbers first, and then, after all of them, block upon block of nonstandard numbers, each "
            "block a copy of the integers, the blocks themselves ordered like the rationals, densely and without "
            "end. <bookmark mark='c'/>Stanley Tennenbaum proved in 1959 that in none of these can addition or "
            "multiplication be computed: the strange models are not just strange, they are beyond any machine. "
            "<bookmark mark='d'/>This matters for what follows. When PA fails to prove a sentence, there is a model "
            "in which it is false, and that model may be one of these."
        ) as vo:
            self.play(FadeIn(head))
            vo.wait_until("a")
            self.play(LaggedStart(*[FadeIn(d_) for d_ in std], lag_ratio=0.1), FadeIn(stdl), FadeIn(dots), FadeIn(nl),
                      FadeIn(rows[0]))
            vo.wait_until("b")
            self.play(LaggedStart(*[FadeIn(b) for b in blocks], lag_ratio=0.3), FadeIn(bl), FadeIn(rows[1]),
                      run_time=3)
            vo.wait_until("c")
            self.play(FadeIn(rows[2]))
            vo.wait_until("d")
            self.play(FadeIn(rows[3]))
        self.clear_scene()

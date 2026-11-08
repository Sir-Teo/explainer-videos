from __future__ import annotations

from videos.philosophy.philosophy9.common import *  # noqa: F403


class Theorem(VoiceoverScene):
    def construct(self):
        card = chapter_card(3, r"Frege's theorem", r"Did Frege succeed after all?", lit=(1983,), part=PART)
        with self.voiceover("Chapter three. Frege's theorem."):
            self.play(FadeIn(card[0], shift=UP * 0.2), FadeIn(card[1]))
        self.play(FadeOut(card))
        self.revival()
        self.ladder()
        self.steps()
        self.infinity()

    def revival(self):
        hcs = VGroup(history_card(1983, r"Crispin Wright", r"\textit{Frege's Conception of Numbers as Objects}",
                                  width=5.6, color=HIST),
                     history_card(1987, r"George Boolos", r"`The consistency of Frege's \textit{Foundations of "
                                  r"Arithmetic}'", width=5.6, color=HIST)).arrange(RIGHT, buff=0.4).to_edge(UP, buff=0.4)
        eq = MathTex(r"\underbrace{\text{Hume's principle}}_{\#F = \#G \iff F \approx G} \;+\; "
                     r"\text{second-order logic} \;\vdash\; \text{the Peano axioms}", font_size=36,
                     color=NUM).move_to([0, 0.3, 0])
        notes = VGroup(label(r"Frege's own proofs, \ in the \textit{Grundlagen} and \textit{Grundgesetze}, \ used Basic "
                             r"Law V only to derive Hume's principle", font_size=24, color=GREY_A),
                       label(r"so drop Basic Law V, \ keep Hume's principle as the axiom", font_size=26, color=OK),
                       label(r"Boolos: \ consistent if second-order arithmetic is \ (the bad axiom is gone)",
                             font_size=24, color=GREY_A)).arrange(DOWN, buff=0.25).to_edge(DOWN, buff=0.6)
        with self.voiceover(
            "In 1983 Crispin Wright noticed something that Charles Parsons had glimpsed in 1965. "
            "<bookmark mark='a'/>Frege's own derivations of arithmetic used Basic Law Five for one thing only: to "
            "prove Hume's principle. After that, everything followed from Hume's principle alone. "
            "<bookmark mark='b'/>So drop the inconsistent law, and take Hume's principle as the axiom. "
            "<bookmark mark='c'/>With second-order logic, it yields all the Peano axioms of arithmetic. "
            "<bookmark mark='d'/>And George Boolos proved in 1987 that the system is consistent if second-order "
            "arithmetic is. The result is now called Frege's theorem: Frege had proved it, without knowing it was "
            "what mattered."
        ) as vo:
            self.play(FadeIn(hcs))
            vo.wait_until("a")
            self.play(FadeIn(notes[0]))
            vo.wait_until("b")
            self.play(FadeIn(notes[1]))
            vo.wait_until("c")
            self.play(Write(eq), run_time=2)
            vo.wait_until("d")
            self.play(FadeIn(notes[2]))
        self.clear_scene()

    def ladder(self):
        head = label(r"Numbers that count themselves", font_size=32, color=CONN).to_edge(UP, buff=0.45)
        defs = [r"0 = \#[x : x \neq x]", r"1 = \#[x : x = 0]", r"2 = \#[x : x = 0 \vee x = 1]",
                r"3 = \#[x : x = 0 \vee x = 1 \vee x = 2]", r"n + 1 = \#[x : x \le n]"]
        rows = VGroup()
        for i, dtex in enumerate(defs):
            m = MathTex(dtex, font_size=34, color=NUM if i < 4 else GOAL)
            if i < 4:
                box = VGroup(*[MathTex(str(j), font_size=26, color=WHITE) for j in range(i)])
                box.arrange(RIGHT, buff=0.25) if i else None
                frame = (SurroundingRectangle(box, buff=0.12, corner_radius=0.08, stroke_color=NUM, stroke_width=2)
                         if i else Square(side_length=0.42, stroke_color=NUM, stroke_width=2))
                pic = VGroup(frame, box) if i else VGroup(frame)
                gl = label(rf"the number of the numbers before {i}" if i else r"nothing is not itself", font_size=21,
                           color=GREY_A)
                row = VGroup(m, pic, gl)
            else:
                row = VGroup(m, VectorizedPoint(), label(r"Frege: \ each number counts the ones before it",
                                                         font_size=22, color=GOAL))
            rows.add(row)
        for i, r in enumerate(rows):
            y = 1.7 - 0.85 * i
            r[0].move_to([-6.2, y, 0], aligned_edge=LEFT)
            r[1].move_to([0.9, y, 0])
            r[2].move_to([2.2, y, 0], aligned_edge=LEFT)
        moral = label(r"no apples, \ no stones: \ the only objects needed are the numbers already built", font_size=24,
                      color=OK).to_edge(DOWN, buff=0.45)
        with self.voiceover(
            "How does Hume's principle give infinitely many numbers from nothing? <bookmark mark='a'/>Zero is the "
            "number of things not identical with themselves. There are none, so zero exists. <bookmark mark='b'/>"
            "One is the number of things identical with zero, and there is exactly one: zero itself. "
            "<bookmark mark='c'/>Two is the number of things that are zero or one. <bookmark mark='d'/>Three counts "
            "zero, one and two. <bookmark mark='e'/>In general, n plus one is the number of numbers up to n. Each "
            "number counts the ones before it. <bookmark mark='f'/>No apples or stones are needed: the only objects "
            "used are the numbers already built. That is why Frege thought arithmetic could be pure logic."
        ) as vo:
            self.play(FadeIn(head))
            for mk, r in zip("abcde", rows):
                vo.wait_until(mk)
                self.play(FadeIn(r, shift=RIGHT * 0.1))
            vo.wait_until("f")
            self.play(FadeIn(moral))
        self.clear_scene()

    def steps(self):
        head = label(r"Frege's theorem, \ the key steps", font_size=32, color=CONN).to_edge(UP, buff=0.4)
        rows = [(r"P(m, n) \iff \exists F\, \exists x\, (Fx \wedge n = \#F \wedge m = \#[y : Fy \wedge y \neq x])",
                 r"$n$ comes right after $m$: \ take one object away"),
                (r"\mathbb{N}(n) \iff \forall X\,(X0 \wedge \forall m\,\forall k\,(Xm \wedge P(m, k) \to Xk) \to Xn)",
                 r"the natural numbers: \ Frege's ancestral \ (\textit{Begriffsschrift}, 1879)"),
                (r"\lnot\, \exists m\; P(m, 0)", r"nothing comes before $0$: \ $\#F = 0$ makes $F$ empty"),
                (r"P(m, n) \wedge P(m', n) \to m = m'", r"$P$ is one-one: \ by Hume's principle"),
                (r"\mathbb{N}(n) \to P\big(n,\ \#[x : \mathbb{N}(x) \wedge x \le n]\big)",
                 r"every number has a successor: \ the hard step, \ Grundlagen \S 82--83")]
        tab = VGroup()
        for i, (f, why) in enumerate(rows):
            y = 1.7 - 0.95 * i
            tab.add(VGroup(MathTex(f, font_size=28, color=WHITE).move_to([-6.4, y, 0], aligned_edge=LEFT),
                           label(why, font_size=20, color=GREY_A).move_to([-6.4, y - 0.38, 0], aligned_edge=LEFT)))
        foot = label(r"and induction comes free with $\mathbb{N}$: \ the Peano axioms, \ from Hume's principle and logic",
                     font_size=24, color=OK).to_edge(DOWN, buff=0.35)
        with self.voiceover(
            "Here are the key steps. <bookmark mark='a'/>First, n comes right after m when n is the number of some "
            "concept F, and m is the number of what is left when one object is taken away from F. "
            "<bookmark mark='b'/>Second, the natural numbers are the things reachable from zero by such steps. "
            "Frege defined this with the ancestral, an idea from his Begriffsschrift of 1879, whose notation we met "
            "in Part 3: n is a natural number if it has every property that zero has and that passes along each "
            "step. "
            "<bookmark mark='c'/>Then the axioms fall out. Nothing comes right before zero, since a concept with "
            "number zero has no object to take away. <bookmark mark='d'/>The relation is one to one, by Hume's "
            "principle. <bookmark mark='e'/>And every natural number has a successor: the hard step, which Frege "
            "proved in sections 82 and 83. The successor of n is the number of natural numbers up to n. "
            "<bookmark mark='f'/>Induction comes free with the definition of the natural numbers. All of Peano "
            "arithmetic, from one principle about counting, and logic."
        ) as vo:
            self.play(FadeIn(head))
            for mk, r in zip("abcde", tab):
                vo.wait_until(mk)
                self.play(FadeIn(r, shift=RIGHT * 0.1))
            vo.wait_until("f")
            self.play(FadeIn(foot))
        self.clear_scene()

    def infinity(self):
        d = load("demands")["rows"]
        hm = load("hpmodel")
        head = label(r"Hume's principle forces infinitely many objects", font_size=32, color=CONN).to_edge(UP,
                                                                                                         buff=0.45)
        hd = [label(r"objects in the world", font_size=22, color=P.CLAIM),
              label(r"different sizes of concept", font_size=22, color=P.CLAIM),
              label(r"numbers needed, \ each an object", font_size=22, color=P.CLAIM),
              label(r"possible?", font_size=22, color=P.CLAIM)]
        rows = [[MathTex(str(r["n"]), font_size=28), MathTex(rf"0, \dots, {r['n']}", font_size=26),
                 MathTex(str(r["HP"]), font_size=28, color=NUM), label(r"no", font_size=24, color=BAD)] for r in d]
        grid = ValueGrid(hd, rows, col_w=[2.8, 3.4, 3.6, 1.8], cell_h=0.5, font_size=24).move_to([0, 0.35, 0])
        assert all(r["HP"] == r["n"] + 1 for r in d) and hm["ok"]
        model = VGroup(label(r"a model with infinitely many objects: \ the numbers $0, 1, 2, \dots$", font_size=24),
                       MathTex(r"\#F = \begin{cases} 0 & F \text{ infinite} \\ |F| + 1 & F \text{ finite} \end{cases}",
                               font_size=34, color=NUM),
                       label(rf"the Reasoner checks it on all {hm['checked']} finite concepts on seven objects, \ and "
                             r"every pair", font_size=21, color=OK)).arrange(DOWN, buff=0.18).to_edge(DOWN, buff=0.3)
        with self.voiceover(
            "There is a surprise inside the theorem. <bookmark mark='a'/>Suppose the world had only five objects. "
            "Concepts can have zero, one, two, three, four or five members: six different sizes. Hume's principle "
            "gives each size a number, and each number must itself be one of the objects. Six numbers will not fit "
            "in a world of five. The Reasoner tries every world size up to five, and the same thing happens every "
            "time: Hume's principle has no finite model. <bookmark mark='b'/>It needs infinitely many objects, and "
            "with infinitely many it works. Take the numbers zero, one, two and so on, and let the number of an "
            "infinite concept be zero, and of a finite concept its size plus one. The Reasoner checks every pair "
            "of finite concepts on seven objects. So a principle meant to be logic proves that the world contains "
            "infinitely many things. Is that logic?"
        ) as vo:
            self.play(FadeIn(head))
            vo.wait_until("a")
            self.play(FadeIn(grid.head), FadeIn(grid.rows_bg), FadeIn(grid.rule),
                      LaggedStart(*[FadeIn(VGroup(*grid.cell[r])) for r in range(len(rows))], lag_ratio=0.4),
                      run_time=5)
            vo.wait_until("b")
            self.play(FadeIn(model))
        self.clear_scene()

from __future__ import annotations

from videos.philosophy.philosophy9.common import *  # noqa: F403


class Univalence(VoiceoverScene):
    def construct(self):
        card = chapter_card(13, r"Equal and equivalent", r"What if isomorphic structures are identical?", lit=(2013,),
                            part=PART)
        with self.voiceover("Chapter thirteen. Equal and equivalent."):
            self.play(FadeIn(card[0], shift=UP * 0.2), FadeIn(card[1]))
        self.play(FadeOut(card))
        self.paths()
        self.circle()
        self.axiom()
        self.structuralism()

    def paths(self):
        head = label(r"A proof of $a = b$ \ is a path from $a$ to $b$", font_size=32, color=CONN).to_edge(UP, buff=0.4)
        blob = Ellipse(width=5.2, height=3.4, stroke_color=GREY_C, stroke_width=2, fill_color=ABSTRACT,
                       fill_opacity=0.08).move_to([-4.0, -0.3, 0])
        a, b = np.array([-5.9, -0.4, 0]), np.array([-2.2, -0.2, 0])
        da, db = Dot(a, color=NUM), Dot(b, color=NUM)
        la, lb = MathTex("a", font_size=30, color=NUM).next_to(da, LEFT), MathTex("b", font_size=30, color=NUM).next_to(
            db, RIGHT)
        p = ArcBetweenPoints(a, b, angle=-0.9, color=PROOF, stroke_width=3)
        q = ArcBetweenPoints(a, b, angle=0.9, color=OK, stroke_width=3)
        lp = MathTex("p", font_size=28, color=PROOF).move_to([-4.05, 0.95, 0])
        lq = MathTex("q", font_size=28, color=OK).move_to([-4.05, -1.6, 0])
        hom = VGroup(*[ArcBetweenPoints(a, b, angle=t, color=GOAL, stroke_width=1.2, stroke_opacity=0.6)
                       for t in np.linspace(-0.7, 0.7, 7)])
        rows = VGroup(
            label(r"Martin-Löf (1972): \ a type of proofs \ $a = b$", font_size=22),
            label(r"Hofmann \& Streicher (1994): \ two proofs of $a = b$ \ can differ", font_size=22),
            VGroup(label(r"Awodey \& Warren; \ Voevodsky \ (2006--09):", font_size=22, color=PROOF),
                   label(r"proofs of equality behave like \textit{paths} in a space", font_size=22,
                         color=PROOF)).arrange(DOWN, aligned_edge=LEFT, buff=0.08),
            VGroup(label(r"a proof that two paths are equal \ is a \textit{homotopy}:", font_size=22, color=GOAL),
                   label(r"a deformation of one into the other", font_size=22, color=GOAL)).arrange(
                DOWN, aligned_edge=LEFT, buff=0.08)).arrange(DOWN, aligned_edge=LEFT, buff=0.28)
        for r in rows:
            if r.width > 6.4:
                r.width = 6.4
        rows.arrange(DOWN, aligned_edge=LEFT, buff=0.28).move_to([3.0, -0.3, 0])
        with self.voiceover(
            "The newest foundation for mathematics grew out of the proofs-as-programs idea. <bookmark mark='a'/>"
            "In Martin-Löf's type theory, for any two things a and b there is a type of proofs that a equals b. "
            "<bookmark mark='b'/>Martin Hofmann and Thomas Streicher showed, in 1994, that two such proofs need not "
            "be the same. <bookmark mark='c'/>Then Steve Awodey and Michael Warren, and independently Vladimir "
            "Voevodsky, saw why: proofs of equality behave like paths in a space. A proof that a equals b is a path "
            "from a to b, and there may be many. <bookmark mark='d'/>A proof that two paths are equal is a "
            "deformation of one into the other, what topologists call a homotopy. The result is called homotopy type "
            "theory."
        ) as vo:
            self.play(FadeIn(head), FadeIn(blob), FadeIn(da), FadeIn(db), FadeIn(la), FadeIn(lb))
            vo.wait_until("a")
            self.play(FadeIn(rows[0]))
            vo.wait_until("b")
            self.play(FadeIn(rows[1]))
            vo.wait_until("c")
            self.play(Create(p), Create(q), FadeIn(lp), FadeIn(lq), FadeIn(rows[2]))
            vo.wait_until("d")
            self.play(LaggedStart(*[Create(h) for h in hom], lag_ratio=0.15), FadeIn(rows[3]), run_time=2.5)
        self.clear_scene()

    def circle(self):
        d = load("winding")
        head = label(r"The circle, \ and its loops", font_size=32, color=CONN).to_edge(UP, buff=0.4)
        centres = [np.array([-4.8 + 3.2 * k, 0.2, 0]) for k in range(4)]
        groups = VGroup()
        for (n, w), c in zip(d["loops"], centres):
            base = Circle(radius=1.0, color=GREY_C, stroke_width=2).move_to(c)
            pt = Dot(c + RIGHT * 1.0, radius=0.07, color=WHITE)
            loop = circle_loop(n, radius=1.0, center=c, color=PROOF if n >= 0 else ABSTRACT)
            lab = MathTex(rf"\text{{winds }} {w}", font_size=28, color=NUM).next_to(base, DOWN, buff=0.55)
            groups.add(VGroup(base, pt, loop, lab))
        assert [w for _, w in d["loops"]] == [0, 1, 2, -1]
        rows = VGroup(
            label(r"the circle as a type: \ one point, \ one loop", font_size=24, color=PROOF),
            label(r"the Reasoner counts each loop's turns; \ loops compose by adding turns", font_size=22,
                  color=GREY_A),
            label(r"the loops of the circle are the integers: \ proved \textit{inside} the theory \ (Licata \& "
                  r"Shulman, 2013)", font_size=24, color=OK)).arrange(DOWN, buff=0.2).to_edge(DOWN, buff=0.4)
        with self.voiceover(
            "This lets a foundation talk about shapes directly. <bookmark mark='a'/>The circle becomes a type with "
            "one point and one loop from the point to itself. <bookmark mark='b'/>Paths can stay put and come back, "
            "go round once, twice, or the other way. The Reasoner counts the turns of each: zero, one, two, minus "
            "one. Following one loop by another adds the turns. <bookmark mark='c'/>That the loops of the circle, "
            "up to deformation, are exactly the integers is a classical theorem of topology. In 2013 Daniel Licata "
            "and Michael Shulman proved it inside homotopy type theory, as a theorem about types, checked by "
            "computer."
        ) as vo:
            self.play(FadeIn(head))
            vo.wait_until("a")
            self.play(FadeIn(rows[0]), FadeIn(VGroup(*[VGroup(g[0], g[1]) for g in groups])))
            vo.wait_until("b")
            self.play(LaggedStart(*[Create(g[2]) for g in groups], lag_ratio=0.5), run_time=5)
            self.play(LaggedStart(*[FadeIn(g[3]) for g in groups], lag_ratio=0.2), FadeIn(rows[1]))
            vo.wait_until("c")
            self.play(FadeIn(rows[2]))
        self.clear_scene()

    def axiom(self):
        d = load("transport")
        hc = history_card(2013, r"The Univalent Foundations Program", r"\textit{Homotopy Type Theory}, \ written in a "
                          r"year at the IAS", width=5.8, color=HIST).to_corner(UL, buff=0.35)
        ua = MathTex(r"(A = B) \;\simeq\; (A \simeq B)", font_size=52, color=NUM).move_to([0, 1.3, 0])
        gl = label(r"Voevodsky's univalence axiom: \ to identify two types \ is to give an equivalence between them",
                   font_size=24, color=GREY_A).next_to(ua, DOWN, buff=0.3)
        tr = VGroup(
            label(r"transport: \ whatever is proved of $A$ \ holds of every $B$ equivalent to it", font_size=24,
                  color=PROOF),
            label(r"the Reasoner: \ `even', \ defined by recursion on strokes, \ carried to binary numerals,",
                  font_size=22, color=GREY_A),
            label(rf"is `the last bit is 0' \ (checked for all {d['checked']} numbers below {d['checked']})",
                  font_size=22, color=OK)).arrange(DOWN, buff=0.2).next_to(gl, DOWN, buff=0.5)
        assert d["even_is_last_bit_zero"]
        with self.voiceover(
            "In 2009 Voevodsky proposed a new axiom. <bookmark mark='a'/>The univalence axiom says that the type of "
            "identifications between two types is equivalent to the type of equivalences between them. In words: to "
            "identify two structures is to give an equivalence between them, and every equivalence counts. "
            "<bookmark mark='b'/>Its consequence is transport: whatever is proved about one structure holds of "
            "every structure equivalent to it, automatically. The Reasoner shows the idea in a small case. Define "
            "'even' by recursion on stroke numerals: zero is even, and one more than an even number is not. Carry "
            "it across the equivalence to binary numerals, and it becomes a different computation, the last bit is "
            "zero, with the same answers everywhere it is checked. <bookmark mark='c'/>The theory was written up "
            "in a single collaborative book during a special year at the Institute for Advanced Study in Princeton, "
            "published in 2013."
        ) as vo:
            self.play(Write(ua), FadeIn(gl), run_time=2)
            vo.wait_until("a")
            vo.wait_until("b")
            self.play(LaggedStart(*[FadeIn(r) for r in tr], lag_ratio=0.6), run_time=5)
            vo.wait_until("c")
            self.play(FadeIn(hc))
        self.clear_scene()

    def structuralism(self):
        head = label(r"Structuralism, \ built into the foundation", font_size=32, color=CONN).to_edge(UP, buff=0.45)
        rows = VGroup(
            label(r"Zermelo's and von Neumann's numbers are equivalent, \ so in univalent foundations they are "
                  r"\textit{equal}", font_size=24, color=NUM),
            label(r"junk questions like `is $1 \in 3$?' \ cannot even be asked: \ every statement transports", font_size=24,
                  color=OK),
            label(r"and $i$ versus $-i$? \ the type $\mathbb{C} = \mathbb{C}$ \ (over $\mathbb{R}$) \ has two elements:", font_size=24),
            label(r"the identity, \ and conjugation: \ two ways of identifying $\mathbb{C}$ with itself", font_size=24,
                  color=ABSTRACT),
            label(r"the puzzle becomes a fact about paths, \ not a contradiction", font_size=24, color=GOAL),
            label(r"in practice: \ Lean's Mathlib does not assume univalence; \ cubical type theory (2015--) makes it "
                  r"compute", font_size=21, color=GREY_B)).arrange(DOWN, buff=0.32).move_to([0, -0.4, 0])
        with self.voiceover(
            "This builds structuralism into the foundation. <bookmark mark='a'/>Zermelo's numbers and von Neumann's "
            "are equivalent structures, so in univalent foundations they are equal, and Benacerraf's identification "
            "problem cannot arise. <bookmark mark='b'/>The junk questions cannot even be asked, because every "
            "statement must transport along equivalences. <bookmark mark='c'/>And the puzzle of i and minus i? The "
            "type of identifications of the complex numbers with themselves, as an extension of the real numbers, has "
            "exactly two elements. "
            "<bookmark mark='d'/>One is the identity, another is conjugation, which swaps i and minus i. "
            "<bookmark mark='e'/>So the puzzle becomes a fact about paths: there are two different ways of "
            "identifying the structure with itself, and that is all the difference between i and minus i amounts "
            "to. <bookmark mark='f'/>In practice, Lean's large library of mathematics does not assume univalence, "
            "while cubical type theory, developed since 2015, is designed to make it compute."
        ) as vo:
            self.play(FadeIn(head))
            for mk, r in zip("abcdef", rows):
                vo.wait_until(mk)
                self.play(FadeIn(r, shift=UP * 0.1))
        self.clear_scene()

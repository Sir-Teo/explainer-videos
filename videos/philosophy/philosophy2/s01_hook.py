from __future__ import annotations

import numpy as np

from videos.philosophy.philosophy2.common import *  # noqa: F403


def speech(who: str, text: str, color) -> VGroup:
    head = VGroup(Circle(radius=0.42, stroke_color=color, stroke_width=3, fill_color=color, fill_opacity=0.15),
                  MathTex(who, font_size=40, color=color))
    head[1].move_to(head[0])
    t = label(text, font_size=26)
    bubble = RoundedRectangle(width=t.width + 0.5, height=t.height + 0.36, corner_radius=0.16, stroke_color=color,
                              stroke_width=2, fill_color="#0B0F17", fill_opacity=0.95)
    t.move_to(bubble)
    b = VGroup(bubble, t).next_to(head, RIGHT, buff=0.35)
    tail = Polygon(bubble.get_left() + UP * 0.1, bubble.get_left() + DOWN * 0.12, head.get_right() + RIGHT * 0.05,
                   stroke_width=0, fill_color=color, fill_opacity=0.6)
    return VGroup(head, tail, b)


class Hook(VoiceoverScene):
    def construct(self):
        self.title()
        self.puzzle()
        self.triples()
        self.objectives()
        self.devices()

    def title(self):
        t = part_title(PART)
        q = quote_card(r"If controversies were to arise, there would be no more need of disputation between two "
                       r"philosophers than between two accountants. For it would suffice to take their pencils in "
                       r"their hands, to sit down to their slates, and to say to each other: let us calculate.",
                       r"Leibniz, around 1685", r"trans. Russell, \textit{A Critical Exposition of the Philosophy of "
                       r"Leibniz} (1900)", width=11.0, font_size=28)
        with self.voiceover(
            "In Part 1 we met Leibniz's dream: that one day, when two philosophers disagree, they will not argue. "
            "<bookmark mark='a'/>They will take up their pencils, sit down at their slates, and say to each other: "
            "let us calculate. <bookmark mark='b'/>This part builds the first piece of that calculator: the logic of "
            "and, or, not, and if. It is the one corner of philosophy where the dream comes true, at a price we will "
            "measure."
        ) as vo:
            self.play(FadeIn(t, shift=UP * 0.2), run_time=1.5)
            vo.wait_until("a")
            self.play(t.animate.scale(0.55).to_edge(UP, buff=0.35), FadeIn(q, shift=UP * 0.2))
            vo.wait_until("b")
            self.play(Indicate(q[1][0], color=P.CONCL, scale_factor=1.03))
        self.clear_scene()

    def puzzle(self):
        d = load("knights")
        A = speech("A", r"All of us are knaves.", P.CLAIM).move_to([-3.2, 2.4, 0])
        B = speech("B", r"Exactly one of us is a knight.", P.AGENT).move_to([-2.4, 1.0, 0])
        C = VGroup(Circle(radius=0.42, stroke_color=GREY_B, stroke_width=3, fill_color=GREY_B, fill_opacity=0.15),
                   MathTex("C", font_size=40, color=GREY_B))
        C[1].move_to(C[0])
        C.move_to([-5.6, -0.25, 0])
        rules = VGroup(label(r"knights: only truths", font_size=24, color=OK),
                       label(r"knaves: only lies", font_size=24, color=BAD)).arrange(DOWN, aligned_edge=LEFT,
                                                                                     buff=0.15)
        rules.to_corner(UR, buff=0.5)
        cite_ = cite(r"Raymond Smullyan, \textit{What Is the Name of This Book?} (1978)")
        eq1 = MathTex(r"a", r"\leftrightarrow", r"(\lnot a \land \lnot b \land \lnot c)", font_size=40)
        eq2 = MathTex(r"b", r"\leftrightarrow", r"\text{exactly one of } a, b, c", font_size=40)
        for e in (eq1, eq2):
            e[0].set_color(ATOM)
        eqs = VGroup(eq1, eq2).arrange(DOWN, aligned_edge=LEFT, buff=0.3).move_to([2.6, -0.6, 0])
        key = label(r"$a$: A is a knight", font_size=24, color=ATOM).next_to(eqs, UP, buff=0.35).align_to(eqs, LEFT)
        rows = [[r["v"]["a"], r["v"]["b"], r["v"]["c"], r["s1"], r["s2"]] for r in d["rows"]]
        grid = ValueGrid([r"a", r"b", r"c", r"\text{A's claim fits}", r"\text{B's claim fits}"], rows, font_size=24,
                         cell_h=0.46).scale(1.15).move_to([2.6, -0.2, 0])
        sol = d["solution"]
        k = next(i for i, r in enumerate(d["rows"]) if r["v"] == sol)
        strikes = VGroup(*[grid.strike(i) for i, r in enumerate(d["rows"]) if not (r["s1"] and r["s2"])])
        verdict = label(r"A: knave \quad B: knight \quad C: knave", font_size=30, color=OK)
        verdict.next_to(grid, DOWN, buff=0.35)
        assert sol == {"a": False, "b": True, "c": False}
        with self.voiceover(
            "Here is a dispute to settle. On an island, everyone is either a knight, who only tells the truth, or a "
            "knave, who only lies. <bookmark mark='a'/>You meet three islanders. A says: all of us are knaves. "
            "<bookmark mark='b'/>B says: exactly one of us is a knight. <bookmark mark='c'/>C says nothing. Who is "
            "what? The puzzle is Raymond Smullyan's. You can reason it out, and you might reason it out wrongly."
        ) as vo:
            self.play(FadeIn(rules), FadeIn(cite_), FadeIn(A[0]), FadeIn(B[0]), FadeIn(C))
            vo.wait_until("a")
            self.play(FadeIn(A[1:], shift=RIGHT * 0.2))
            vo.wait_until("b")
            self.play(FadeIn(B[1:], shift=RIGHT * 0.2))
            vo.wait_until("c")
            self.play(Indicate(C, color=GREY_A))
        with self.voiceover(
            "Or you can calculate. Write a for the sentence 'A is a knight'. <bookmark mark='a'/>Then what A says is "
            "true exactly when A is a knight: a, if and only if not a and not b and not c. <bookmark mark='b'/>The "
            "same for B. Two equations, in three unknowns that can each be only true or false."
        ) as vo:
            self.play(FadeIn(key))
            vo.wait_until("a")
            self.play(Write(eq1))
            vo.wait_until("b")
            self.play(Write(eq2))
        with self.voiceover(
            "So there are only eight possibilities. <bookmark mark='a'/>Check each one against both equations, "
            "<bookmark mark='b'/>and strike out every row where somebody's words don't fit what they are. "
            "<bookmark mark='c'/>One row survives. A and C are knaves; B is a knight. No cleverness: a table, filled in "
            "the same way by anyone, or anything."
        ) as vo:
            self.play(FadeOut(eqs), FadeOut(key), VGroup(A, B, C).animate.scale(0.75).to_edge(LEFT, buff=0.4))
            self.play(FadeIn(grid.head), FadeIn(grid.rule), FadeIn(grid.rows_bg))
            vo.wait_until("a")
            self.play(LaggedStart(*[FadeIn(grid.row(i), shift=LEFT * 0.1) for i in range(8)], lag_ratio=0.12),
                      run_time=2.0)
            vo.wait_until("b")
            self.play(LaggedStart(*[Create(s) for s in strikes], lag_ratio=0.15), run_time=1.6)
            vo.wait_until("c")
            self.play(Create(grid.row_box(k)), FadeIn(verdict, shift=UP * 0.15))
        self.clear_scene()

    def triples(self):
        d = load("pythag")
        n, colour = d["n"], d["colour"]
        side = 20
        cell = 0.27
        cells = VGroup()
        for i in range(n):
            r, c = divmod(i, side)
            sq = Square(cell * 0.92, stroke_width=0, fill_color=P.CLAIM if colour[i] else P.AGENT, fill_opacity=0.85)
            sq.move_to([(c - (side - 1) / 2) * cell, ((n // side - 1) / 2 - r) * cell, 0])
            cells.add(sq)
        cells.move_to([-3.0, -0.2, 0])
        nums = VGroup()
        show_trip = [(3, 4, 5), (5, 12, 13), (20, 21, 29), (119, 120, 169)]
        trip_boxes = VGroup()
        for t in show_trip:
            assert list(t) in [list(x) for x in d["triples"]]
            for x in t:
                trip_boxes.add(SurroundingRectangle(cells[x - 1], buff=0.02, color=WHITE, stroke_width=2.5))
        legend_ = VGroup(*[label(rf"${a}^2+{b}^2={c}^2$", font_size=22) for a, b, c in show_trip]).arrange(
            DOWN, aligned_edge=LEFT, buff=0.15).next_to(cells, RIGHT, buff=0.4).align_to(cells, UP)
        info = label(rf"{len(d['triples'])} triples up to {n}; \ none one colour", font_size=24, color=OK)
        info.next_to(cells, DOWN, buff=0.25)
        tag = computed_tag(r"computed: our solver, Chapter 11").to_corner(DL, buff=0.25)
        hc = history_card(2016, r"Heule, Kullmann \& Marek", r"1 to 7,824 can be split; 1 to 7,825 cannot. "
                          r"The certificate: 200 terabytes, checked by a second program.", width=5.2, color=HIST)
        hc.to_corner(DR, buff=0.4)
        with self.voiceover(
            "Now make the puzzle enormous. Colour the whole numbers from one to n, each blue or orange, so that no "
            "Pythagorean triple, like three, four, five, is all one colour. <bookmark mark='a'/>Here are the first "
            f"{n}, coloured by the solver we will build in this part. <bookmark mark='b'/>Three, four, five; five, twelve, "
            "thirteen; twenty, twenty-one, twenty-nine: <bookmark mark='c'/>"
            f"every one of the {len(d['triples'])} triples below {n} uses both colours."
        ) as vo:
            self.play(LaggedStart(*[FadeIn(c) for c in cells], lag_ratio=0.004), run_time=2.5)
            self.play(FadeIn(tag))
            vo.wait_until("a")
            self.play(Indicate(cells, scale_factor=1.02, color=WHITE))
            vo.wait_until("b")
            self.play(LaggedStart(*[Create(b) for b in trip_boxes], lag_ratio=0.15), FadeIn(legend_), run_time=2.0)
            vo.wait_until("c")
            self.play(FadeIn(info))
        with self.voiceover(
            "How far can you go? <bookmark mark='a'/>In 2016 Marijn Heule, Oliver Kullmann and Victor Marek settled "
            "it: the numbers up to 7,824 can be split this way, and up to 7,825 they cannot. No person found that "
            "proof. A program did, and the certificate it wrote out runs to two hundred terabytes, far too long for "
            "anyone to read. It was checked by a second, much simpler program. That is Leibniz's slate, at a scale he "
            "never imagined."
        ) as vo:
            vo.wait_until("a")
            self.play(FadeOut(legend_), FadeIn(hc, shift=LEFT * 0.2))
        self.clear_scene()

    def objectives(self):
        card = objectives_card([
            r"Boole's algebra; formulas as trees; the sixteen connectives, and why one is enough",
            r"truth tables: validity, satisfiability and consequence, decided by calculation",
            r"normal forms, and Tseitin's encoding",
            r"natural deduction, with proofs a machine can check",
            r"soundness and completeness: proof and truth agree",
            r"resolution, DPLL and clause learning: the solvers inside industry",
            r"the price of calculation, and Socrates' method, run as SAT",
        ], font_size=27)
        with self.voiceover(
            "So this part is about the logic of whole sentences, propositional logic, and about what it means to "
            "calculate with it. <bookmark mark='a'/>We begin with Boole's algebra of thought, formulas as trees, and the "
            "sixteen ways two sentences can combine. <bookmark mark='b'/>Then truth tables, and what validity is. "
            "<bookmark mark='c'/>Natural deduction, with proofs a machine can check; then soundness and completeness, the "
            "two theorems that say proof and truth agree. <bookmark mark='d'/>Then the solvers: resolution, search, and "
            "clause learning; what they cost; and what they do for industry and for philosophy."
        ) as vo:
            self.play(FadeIn(card.head), FadeIn(card.rows[0], shift=RIGHT * 0.2))
            for mk, idx in (("b", [1, 2]), ("c", [3, 4]), ("d", [5, 6])):
                vo.wait_until(mk)
                self.play(LaggedStart(*[FadeIn(card.rows[i], shift=RIGHT * 0.2) for i in idx], lag_ratio=0.3))
        self.clear_scene()

    def devices(self):
        w = wall(upto=1, current=None).move_to([0, -0.2, 0])
        q = w.brick[2]
        qm = label(r"?", font_size=34, color=P.CONCL).move_to(q[0])
        head = label(r"The Wall", font_size=40, color=P.WALL).to_edge(UP, buff=0.35)
        d = load("evil")
        pl = PriceList([(c["key"], c["text"]) for c in d["claims"]], mus=d["mus"], center=[0, -0.4, 0])
        head2 = label(r"The Price List", font_size=40, color=P.PRICE).to_edge(UP, buff=0.35)
        with self.voiceover(
            "Two of the series' devices begin here. <bookmark mark='a'/>The first is the Wall. Every part adds a brick: "
            "the theorem that marks where calculation stops. Part 1 laid Zeno's. <bookmark mark='b'/>This part's brick "
            "will not say that we can't calculate. It will say what calculating costs."
        ) as vo:
            self.play(FadeIn(head), LaggedStart(*[FadeIn(b) for b in w], lag_ratio=0.02), run_time=2.0)
            vo.wait_until("a")
            self.play(Indicate(w.brick[1], color=P.WALL))
            vo.wait_until("b")
            self.play(q[0].animate.set_stroke(P.CONCL, width=3), FadeIn(qm))
        self.clear_scene()
        with self.voiceover(
            "The second is the Price List. When Socrates showed someone that their beliefs contradicted each other, he "
            "left them stuck, in what the Greeks called aporia: no way through. <bookmark mark='a'/>We will build a "
            "machine that lists every way out of a contradiction, exactly, and use it on one of the oldest arguments "
            "there is: the problem of evil."
        ) as vo:
            self.play(FadeIn(head2), LaggedStart(*[FadeIn(c, scale=0.9) for c in pl.cards], lag_ratio=0.15))
            vo.wait_until("a")
            self.play(Create(pl.conflict), run_time=1.5)
        self.clear_scene()

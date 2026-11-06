from __future__ import annotations

from videos.philosophy.philosophy7.common import *  # noqa: F403


class Numbering(VoiceoverScene):
    def construct(self):
        card = chapter_card(5, r"Gödel numbering", r"Can a formula be a number?", lit=(1931,), part=PART)
        with self.voiceover("Chapter five. Gödel numbering."):
            self.play(FadeIn(card[0], shift=UP * 0.2), FadeIn(card[1]))
        self.play(FadeOut(card))
        self.table()
        self.encode()
        self.decode()
        self.prov()

    def table(self):
        d = load("numbering")
        head = label(r"Every symbol gets a number", font_size=32, color=CONN).to_edge(UP, buff=0.45)
        cells = VGroup()
        for i, (s, c) in enumerate(d["table"]):
            tex = A.TEX.get(s, s)
            sym = MathTex(tex, font_size=36)
            num = MathTex(str(c), font_size=28, color=NUM)
            box = RoundedRectangle(width=1.0, height=1.25, corner_radius=0.08, stroke_color=GREY_C, stroke_width=1.2,
                                   fill_color="#151A24", fill_opacity=1)
            sym.move_to(box.get_center() + UP * 0.22)
            num.move_to(box.get_center() + DOWN * 0.3)
            cells.add(VGroup(box, sym, num))
        top = VGroup(*cells[:9]).arrange(RIGHT, buff=0.15)
        bot = VGroup(*cells[9:]).arrange(RIGHT, buff=0.15)
        grid = VGroup(top, bot).arrange(DOWN, buff=0.3).move_to([0, 0.4, 0])
        note = label(r"logical and arithmetical symbols get odd numbers; \ variables $x, y, z, \dots$ get even ones",
                     font_size=24, color=GREY_A).to_edge(DOWN, buff=0.9)
        with self.voiceover(
            "Gödel's second idea was to turn syntax into arithmetic. <bookmark mark='a'/>Give every symbol a "
            "number: odd numbers for the logical and arithmetical symbols, not, and, or, implies, the quantifiers, "
            "equals, brackets, zero, successor, plus, times; even numbers for the variables. "
            "<bookmark mark='b'/>The particular numbers do not matter. What matters is that the coding is "
            "mechanical, both ways."
        ) as vo:
            self.play(FadeIn(head))
            vo.wait_until("a")
            self.play(LaggedStart(*[FadeIn(c, shift=UP * 0.1) for c in cells], lag_ratio=0.08), run_time=3)
            vo.wait_until("b")
            self.play(FadeIn(note))
        self.clear_scene()

    def encode(self):
        d = load("numbering")
        head = label(r"A formula becomes a number", font_size=32, color=CONN).to_edge(UP, buff=0.45)
        f = MathTex(r"0", r"=", r"0", font_size=72).move_to([0, 2.0, 0])
        codes = VGroup(*[MathTex(str(c), font_size=34, color=NUM).next_to(f[i], DOWN, buff=0.45)
                         for i, c in enumerate(d["f1_codes"])])
        ps = [2, 3, 5]
        powers = VGroup(*[MathTex(rf"{p}^{{{c}}}", font_size=44, color=GOAL) for p, c in zip(ps, d["f1_codes"])])
        prod = VGroup(powers[0], MathTex(r"\cdot", font_size=44), powers[1], MathTex(r"\cdot", font_size=44),
                      powers[2]).arrange(RIGHT, buff=0.2).move_to([0, -0.3, 0])
        val = MathTex(r"= " + gnum_tex(d["g1"]), font_size=40, color=NUM).next_to(prod, DOWN, buff=0.4)
        rule = label(r"the $k$-th symbol's code becomes the exponent of the $k$-th prime", font_size=26,
                     color=GREY_A).to_edge(DOWN, buff=0.9)
        big = label(rf"$\forall x\,(x + 0 = x)$: \ a number of {d['g2_digits']} digits", font_size=26,
                    color=GREY_A).next_to(rule, DOWN, buff=0.25)
        with self.voiceover(
            "Now code a whole formula. <bookmark mark='a'/>Take zero equals zero. Its symbols have codes twenty-one, "
            "fifteen, twenty-one. <bookmark mark='b'/>Make each code the exponent of a prime, in order: two to the "
            "twenty-one, times three to the fifteen, times five to the twenty-one. <bookmark mark='c'/>The product "
            "is a single number, about fourteen billion billion billion. <bookmark mark='d'/>Every formula gets a "
            "number this way. The law that x plus zero is x gets one with a hundred and fifteen digits."
        ) as vo:
            self.play(FadeIn(head), FadeIn(f))
            vo.wait_until("a")
            self.play(LaggedStart(*[FadeIn(c, shift=DOWN * 0.1) for c in codes], lag_ratio=0.3))
            vo.wait_until("b")
            self.play(*[TransformFromCopy(c, p_) for c, p_ in zip(codes, powers)], FadeIn(prod[1]), FadeIn(prod[3]),
                      run_time=1.5)
            self.play(FadeIn(rule))
            vo.wait_until("c")
            self.play(Write(val))
            vo.wait_until("d")
            self.play(FadeIn(big))
        self.clear_scene()

    def decode(self):
        d = load("numbering")
        head = label(r"And back again: \ the Reasoner factors", font_size=32, color=CONN).to_edge(UP, buff=0.45)
        n = MathTex(r"2^{11} \cdot 3^{2} \cdot 5^{17} \cdot 7^{2} \cdot 11^{25} \cdot 13^{21} \cdot 17^{15} "
                    r"\cdot 19^{2} \cdot 23^{19}", font_size=38, color=NUM).move_to([0, 1.6, 0])
        arrow = Arrow([0, 1.0, 0], [0, 0.2, 0], color=GREY_B, buff=0)
        syms = A.tokens(d["f2"])
        out = VGroup(*[VGroup(MathTex(str(A.CODE[s]), font_size=26, color=NUM),
                              MathTex(A.TEX.get(s, s), font_size=40)).arrange(DOWN, buff=0.2) for s in syms]).arrange(
            RIGHT, buff=0.35).move_to([0, -0.6, 0])
        res = MathTex(r"\forall x\,(x + 0 = x)", font_size=48, color=GOAL).move_to([0, -2.0, 0])
        proofs = label(rf"a proof is a list of formulas: \ code it as $2^{{g_1}} \cdot 3^{{g_2}} \cdots$; \ the "
                       rf"two-line proof `$0 = 0$, \ $\mathsf{{S}}0 = \mathsf{{S}}0$' \ gets a number with about "
                       rf"$10^{{{int(d['proof_digits_log10'])}}}$ digits", font_size=23,
                       color=GREY_A).to_edge(DOWN, buff=0.35)
        assert d["decoded"] == d["f2"]
        with self.voiceover(
            "Decoding is just factoring. <bookmark mark='a'/>Given a number, the Reasoner divides out two, three, "
            "five, and so on, and reads off the exponents. <bookmark mark='b'/>Eleven, two, seventeen, two, "
            "twenty-five: for all x, open bracket, x plus, and so on. <bookmark mark='c'/>Out comes the formula: "
            "for all x, x plus zero equals x. <bookmark mark='d'/>A proof is a list of formulas, so it too gets a "
            "number, with the formulas' numbers as exponents. These numbers are absurdly large. A two-line proof "
            "gets a number with about ten to the sixty-eight digits: written one digit to an atom, it would use "
            "up the atoms of a hundred billion suns. Nobody computes them. What "
            "matters is that the relations between them are arithmetic."
        ) as vo:
            self.play(FadeIn(head), FadeIn(n))
            vo.wait_until("a")
            self.play(GrowArrow(arrow))
            vo.wait_until("b")
            self.play(LaggedStart(*[FadeIn(o, shift=DOWN * 0.1) for o in out], lag_ratio=0.15), run_time=3)
            vo.wait_until("c")
            self.play(FadeIn(res))
            vo.wait_until("d")
            self.play(FadeIn(proofs))
        self.clear_scene()

    def prov(self):
        head = label(r"Syntax becomes arithmetic", font_size=32, color=CONN).to_edge(UP, buff=0.45)
        rows = [(r"`$n$ codes a formula'", r"$\mathrm{Form}(n)$", r"primitive recursive"),
                (r"`$m$ codes a proof of the formula coded by $n$'", r"$\mathrm{Prf}(m, n)$", r"primitive recursive"),
                (r"`the formula coded by $n$ is provable'", r"$\mathrm{Prov}(n) := \exists m\,\mathrm{Prf}(m, n)$",
                 r"$\Sigma_1$")]
        tab = VGroup()
        for i, (a, b, c) in enumerate(rows):
            y = 1.3 - 1.0 * i
            la = label(a, font_size=26)
            lb = label(b, font_size=28, color=PROV)
            lc = label(c, font_size=22, color=GREY_B)
            la.move_to([-6.3 + la.width / 2, y, 0])
            lb.move_to([0.6 + lb.width / 2, y, 0])
            lc.move_to([0.6 + lc.width / 2, y - 0.42, 0])
            tab.add(VGroup(la, lb, lc))
        corner = label(r"$\ulcorner \varphi \urcorner$: \ the numeral for $\varphi$'s Gödel number", font_size=26,
                       color=NUM).to_edge(DOWN, buff=1.1)
        moral = label(r"arithmetic can now talk about its own formulas and proofs", font_size=28,
                      color=GOAL).next_to(corner, DOWN, buff=0.3)
        with self.voiceover(
            "And so syntax becomes arithmetic. <bookmark mark='a'/>Being the code of a formula is a primitive "
            "recursive property of numbers: you can check it by factoring and looking. "
            "<bookmark mark='b'/>So is being the code of a proof of a given formula: check that each line is an "
            "axiom or follows by a rule. <bookmark mark='c'/>And provability, there exists a proof, is a sigma "
            "one formula, Prov of n. <bookmark mark='d'/>Write corner quotes around a formula for the numeral of "
            "its Gödel number. <bookmark mark='e'/>Arithmetic, which was supposed to be about numbers, can now talk "
            "about its own formulas and proofs. That is the opening Gödel needed."
        ) as vo:
            self.play(FadeIn(head))
            for mk, r in zip("abc", tab):
                vo.wait_until(mk)
                self.play(FadeIn(r, shift=RIGHT * 0.1))
            vo.wait_until("d")
            self.play(FadeIn(corner))
            vo.wait_until("e")
            self.play(FadeIn(moral))
        self.clear_scene()

from __future__ import annotations

from videos.philosophy.philosophy7.common import *  # noqa: F403


class Berry(VoiceoverScene):
    def construct(self):
        card = chapter_card(13, r"Berry's paradox, \ made exact", r"What is the smallest number you cannot name?",
                            lit=(1974,), part=PART)
        with self.voiceover("Chapter thirteen. Berry's paradox, made exact."):
            self.play(FadeIn(card[0], shift=UP * 0.2), FadeIn(card[1]))
        self.play(FadeOut(card))
        self.paradox()
        self.toy()
        self.chaitin()
        self.omega()

    def paradox(self):
        hc = history_card(1906, r"Bertrand Russell, \ crediting G. G. Berry, \ an Oxford librarian",
                          r"`the least integer not nameable in fewer than nineteen syllables'", width=7.6,
                          color=HIST).to_corner(UL, buff=0.35)
        p = label(r"`the smallest number not definable in under sixty letters'", font_size=30, color=SELF).move_to(
            [0, 0.6, 0])
        rows = VGroup(label(r"finitely many phrases have under sixty letters, \ so some numbers escape them all",
                            font_size=24),
                      label(r"so there is a smallest such number", font_size=24),
                      label(r"but the phrase above defines it, \ in under sixty letters", font_size=24, color=BAD)
                      ).arrange(DOWN, buff=0.25).next_to(p, DOWN, buff=0.5)
        with self.voiceover(
            "In 1906 Bertrand Russell published a paradox he credited to G. G. Berry, a librarian at the Bodleian in "
            "Oxford. <bookmark mark='a'/>Consider the smallest number not definable in under sixty letters. "
            "<bookmark mark='b'/>Only finitely many phrases have under sixty letters, so only finitely many numbers "
            "are defined by them, and some numbers escape. There is a smallest. <bookmark mark='c'/>But the phrase "
            "we just used defines it, and has under sixty letters. Contradiction. The trouble is the word "
            "'definable', applied to the language it is used in."
        ) as vo:
            self.play(FadeIn(hc))
            vo.wait_until("a")
            self.play(FadeIn(p))
            for mk, r in zip("bc", (VGroup(rows[0], rows[1]), rows[2])):
                vo.wait_until(mk)
                self.play(FadeIn(r))
        self.clear_scene()

    def toy(self):
        d = load("berry")
        head = label(r"A toy language: \ digits 1--9, \ and $+$, $\times$, $\hat{}$ \ in postfix", font_size=30,
                     color=CONN).to_edge(UP, buff=0.35)
        cols = {1: "#2E3A4D", 3: TAPE, 5: PROV, 7: NUM, 9: BAD}
        grid = VGroup()
        for n, L in d["grid"]:
            i = n - 1
            r, c = divmod(i, 25)
            sq = Square(side_length=0.3, stroke_width=0.5, stroke_color="#0B0F17", fill_color=cols.get(L, BAD),
                        fill_opacity=0.9 if L > 1 else 0.6).move_to([-6.4 + c * 0.32, 2.2 - r * 0.32, 0])
            grid.add(sq)
        key = VGroup(*[VGroup(Square(side_length=0.26, fill_color=cols[L], fill_opacity=0.9, stroke_width=0),
                              label(t, font_size=20, color=GREY_A)).arrange(RIGHT, buff=0.15)
                       for L, t in ((1, r"one symbol"), (3, r"three"), (5, r"five"), (7, r"seven"),
                                    (9, r"more than seven"))]).arrange(DOWN, aligned_edge=LEFT, buff=0.15)
        key.next_to([2.0, 1.5, 0], RIGHT, buff=0)
        grid_lab = label(r"the numbers 1 to 300, \ by the length of their shortest name", font_size=20,
                         color=GREY_B).next_to(grid, DOWN, buff=0.15)
        names = VGroup()
        for n in ("100", "729", "1000"):
            L, ex = d["names"][n]
            names.add(label(rf"${n}$: \ ${ex}$ \ ({L} symbols)", font_size=22))
        names.arrange(DOWN, aligned_edge=LEFT, buff=0.15).next_to(key, DOWN, buff=0.4).align_to(key, LEFT)
        b = d["berry"]
        berry = VGroup(label(r"the least number with no name of", font_size=22, color=GOAL),
                       label(rf"3 symbols: \ {b['3']}; \ \ 5: \ {b['5']}; \ \ 7: \ {b['7']}", font_size=24,
                             color=GOAL)).arrange(
            DOWN, aligned_edge=LEFT, buff=0.12).next_to(names, DOWN, buff=0.35).align_to(key, LEFT)
        mark = VGroup(*[SurroundingRectangle(grid[n - 1], buff=0.02, color=WHITE, stroke_width=2.5)
                        for n in (int(b["5"]), int(b["7"])) if n <= 300])
        moral = label(r"no paradox: \ `the least number with no short name' \ is said in our language, \ not the toy's",
                      font_size=22, color=OK).to_edge(DOWN, buff=0.3)
        with self.voiceover(
            "The Reasoner can make the paradox precise for a toy language. <bookmark mark='a'/>Its names are "
            "expressions built from the digits one to nine with plus, times and power, written in postfix, so no "
            "brackets are needed. The Reasoner finds the shortest name of every number. Here are the numbers up to "
            "three hundred, coloured by the length of their shortest name. <bookmark mark='b'/>A hundred needs five "
            "symbols: four times five squared. Seven hundred and twenty-nine needs only three: three to the sixth. "
            "A thousand is eight times five cubed. <bookmark mark='c'/>The least number with no name of three "
            "symbols is nineteen. With five symbols, ninety-two; with seven, two hundred and thirty-nine. "
            "<bookmark mark='d'/>There is no paradox here, because the phrase 'the least number with no name of "
            "seven symbols' is not an expression of the toy language. It is said in ours. The paradox returns only "
            "when a language tries to talk about definability in itself, which is exactly what arithmetic, with "
            "Gödel's coding, can almost do."
        ) as vo:
            self.play(FadeIn(head))
            vo.wait_until("a")
            self.play(LaggedStart(*[FadeIn(s) for s in grid], lag_ratio=0.004), FadeIn(key), FadeIn(grid_lab),
                      run_time=3)
            vo.wait_until("b")
            self.play(LaggedStart(*[FadeIn(n_) for n_ in names], lag_ratio=0.4))
            vo.wait_until("c")
            self.play(FadeIn(berry), *[Create(m) for m in mark])
            vo.wait_until("d")
            self.play(FadeIn(moral))
        self.clear_scene()

    def chaitin(self):
        hc = history_card(1974, r"Gregory Chaitin", r"`Information-theoretic limitations of formal systems'",
                          width=6.6, color=HIST).to_corner(UL, buff=0.35)
        dc = definition_card(r"Kolmogorov complexity", r"$K(x)$: \ the length of the shortest program that prints "
                             r"$x$ \ (Kolmogorov 1965; Solomonoff; Chaitin)", width=10.0, font_size=25,
                             color=P.CLAIM).move_to([0, 1.1, 0])
        thm = theorem_card(r"Chaitin's incompleteness theorem", r"for a consistent theory $T$ there is a constant "
                           r"$L$ such that $T$ proves \ $K(x) > L$ \ for no $x$ at all, \ though almost every $x$ "
                           r"satisfies it", width=10.0, font_size=25).next_to(dc, DOWN, buff=0.35)
        proof = label(r"proof, Berry's way: \ a program could search $T$'s proofs for an $x$ with $K(x) > L$ and print "
                      r"it; \ that program is shorter than $L$", font_size=22, color=GREY_A).to_edge(DOWN, buff=0.4)
        with self.voiceover(
            "Gregory Chaitin made Berry's paradox into a theorem in 1974. <bookmark mark='a'/>The Kolmogorov "
            "complexity of a string is the length of the shortest program that prints it. A random string has "
            "complexity about its own length: there is no shorter description. <bookmark mark='b'/>Chaitin's "
            "theorem: for any consistent theory, there is a number L such that the theory cannot prove, of any "
            "particular string, that its complexity exceeds L, even though all but finitely many strings do. "
            "<bookmark mark='c'/>The proof is Berry's. If the theory could prove such facts, a short program could "
            "search through its proofs for a string of complexity above L, and print it. But that program has "
            "length less than L, so it would be a short description of a string with no short description."
        ) as vo:
            self.play(FadeIn(hc))
            vo.wait_until("a")
            self.play(FadeIn(dc))
            vo.wait_until("b")
            self.play(FadeIn(thm))
            vo.wait_until("c")
            self.play(FadeIn(proof))
        self.clear_scene()

    def omega(self):
        head = label(r"Chaitin's $\Omega$ \ (1975)", font_size=32, color=CONN).to_edge(UP, buff=0.5)
        om = MathTex(r"\Omega \;=\; \sum_{p \text{ halts}} 2^{-|p|}", font_size=56, color=SELF).move_to([0, 1.3, 0])
        rows = VGroup(label(r"the probability that a random program halts \ (for a prefix-free language)",
                            font_size=26),
                      label(r"its first $n$ bits would settle the halting of every program of length $\le n$",
                            font_size=26, color=GOAL),
                      label(r"so a theory can determine only finitely many of its bits: \ mathematical facts "
                            r"that are true for no reason", font_size=26, color=BAD)).arrange(
            DOWN, buff=0.3).next_to(om, DOWN, buff=0.6)
        caveat = label(r"a caution: \ `true for no reason' means no reason \textit{within} the theory \ (Franzén)",
                       font_size=22, color=GREY_A).to_edge(DOWN, buff=0.35)
        with self.voiceover(
            "Chaitin went on to define a single number that packs in the whole halting problem. "
            "<bookmark mark='a'/>Omega is the probability that a randomly chosen program halts. "
            "<bookmark mark='b'/>Knowing its first n bits would let you decide the halting of every program up to "
            "length n. <bookmark mark='c'/>So any theory can determine only finitely many of its bits. Chaitin "
            "described the rest as mathematical facts that are true for no reason. <bookmark mark='d'/>A caution "
            "from Torkel Franzén: they are true for no reason that the theory can supply, which is the same lesson "
            "as Gödel's, in the language of information."
        ) as vo:
            self.play(FadeIn(head))
            vo.wait_until("a")
            self.play(Write(om), FadeIn(rows[0]))
            vo.wait_until("b")
            self.play(FadeIn(rows[1]))
            vo.wait_until("c")
            self.play(FadeIn(rows[2]))
            vo.wait_until("d")
            self.play(FadeIn(caveat))
        self.clear_scene()

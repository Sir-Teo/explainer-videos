from __future__ import annotations

from fractions import Fraction

from videos.philosophy.philosophy9.common import *  # noqa: F403


class Brouwer(VoiceoverScene):
    def construct(self):
        card = chapter_card(6, r"Mathematics as construction", r"Can a mathematical fact outrun every proof?",
                            lit=(1907,), part=PART)
        with self.voiceover("Chapter six. Mathematics as construction."):
            self.play(FadeIn(card[0], shift=UP * 0.2), FadeIn(card[1]))
        self.play(FadeOut(card))
        self.mind()
        self.pi()
        self.weak()
        self.continuity()

    def mind(self):
        hc = history_card(1907, r"L.\ E.\ J.\ Brouwer", r"\textit{On the Foundations of Mathematics}, \ his thesis",
                          width=5.6, color=HIST).to_corner(UL, buff=0.35)
        rows = VGroup(
            label(r"mathematics is an activity of the mind, \ prior to language and to logic", font_size=26,
                  color=PROOF),
            label(r"its root: \ the intuition of time, \ one moment falling apart into two", font_size=24,
                  color=GREY_A),
            label(r"a statement is true when we have constructed a proof of it \ (the BHK reading, Part 5)",
                  font_size=24, color=GREY_A),
            label(r"so excluded middle, \ $A \vee \lnot A$, \ would need a way to decide every question",
                  font_size=24, color=GOAL)).arrange(DOWN, buff=0.35).move_to([0, -0.4, 0])
        with self.voiceover(
            "The fourth answer came from the Dutch topologist L. E. J. Brouwer. <bookmark mark='a'/>In his thesis "
            "of 1907 he held that mathematics is an activity of the mind, prior to language, and prior to logic, "
            "which only records its regularities. <bookmark mark='b'/>Its root is our intuition of time: one moment "
            "falling apart into two, and the two-ness repeated without end. <bookmark mark='c'/>A mathematical "
            "statement is true when we have constructed a proof of it. Part 5 met the logic of this view, the BHK "
            "reading of the connectives. <bookmark mark='d'/>On it, 'A or not A' would require a method for "
            "deciding every question, so it is not a law. This chapter shows what that does to mathematics."
        ) as vo:
            self.play(FadeIn(hc))
            for mk, r in zip("abcd", rows):
                vo.wait_until(mk)
                self.play(FadeIn(r, shift=UP * 0.1))
        self.clear_scene()

    def pi(self):
        d = load("pi")
        digits = d["digits"]
        head = label(r"The Reasoner computes $\pi$", font_size=32, color=CONN).to_edge(UP, buff=0.35)
        per, nrows = 60, 9
        start = 721
        block = code_block([digits[start + r * per: start + (r + 1) * per] for r in range(nrows)], font_size=17,
                           color=GREY_B, buff=0.08).move_to([0, 1.0, 0])
        pos = d["six9"]
        rr, cc = divmod(pos - start, per)
        hl = SurroundingRectangle(VGroup(*block[rr][cc:cc + 6]), buff=0.04, color=NUM, stroke_width=2.5)
        tag = label(rf"six 9s, \ from decimal place {pos}: \ the `Feynman point'", font_size=22, color=NUM).next_to(
            block, DOWN, buff=0.25)
        gl = label(rf"Gibbons's spigot: \ {len(digits):,} digits, \ one at a time, \ in exact integer arithmetic".replace(
            ",", "{,}"), font_size=20, color=GREY_B).next_to(head, DOWN, buff=0.15)
        q = VGroup(
            label(r"Brouwer (1908): \ does $0123456789$ occur in $\pi$? \ nobody knew", font_size=24, color=GOAL),
            label(r"the Reasoner: \ not in the first 3,000 digits".replace(",", "{,}"), font_size=22, color=GREY_A),
            label(r"found in 1997 \ (Kanada's team), \ more than seventeen billion digits in", font_size=22,
                  color=GREY_A),
            VGroup(label(r"so use a question still open: \ Goldbach's conjecture", font_size=21, color=OK),
                   label(rf"checked here to 100,000 \ (hardest: {d['goldbach']['hardest'][0]:,} needs the prime "
                         rf"{d['goldbach']['hardest'][1]}); \ by others to $4 \times 10^{{18}}$".replace(",", "{,}"),
                         font_size=20, color=OK)).arrange(DOWN, buff=0.08)).arrange(
            DOWN, buff=0.18).to_edge(DOWN, buff=0.3)
        assert d["brouwer"] is None and pos == 762 and d["goldbach"]["counterexample"] is None
        with self.voiceover(
            "Brouwer's favourite examples used the digits of pi. <bookmark mark='a'/>The Reasoner computes them "
            "with an unbounded spigot, one digit at a time in exact integer arithmetic. Here are the digits from "
            "the seven hundred and twenty-first place on. <bookmark mark='b'/>At place 762 there are six nines in a "
            "row, the stretch nicknamed the Feynman point. <bookmark mark='c'/>Brouwer asked whether the block zero, "
            "one, two, up to nine ever occurs in pi. In his day nobody knew. <bookmark mark='d'/>It is not in the "
            "first three thousand digits. <bookmark mark='e'/>In 1997 Yasumasa Kanada's team found it, more than "
            "seventeen billion digits in, so Brouwer's question has been answered. <bookmark mark='f'/>The method "
            "does not depend on the example. Use any question still open, such as Goldbach's conjecture, that every "
            "even number above two is a sum of two primes. The Reasoner checks it up to a hundred thousand; others "
            "have checked it to four billion billion. Nobody has proved it."
        ) as vo:
            self.play(FadeIn(head), FadeIn(gl))
            vo.wait_until("a")
            self.play(LaggedStart(*[FadeIn(r) for r in block], lag_ratio=0.15), run_time=2.5)
            vo.wait_until("b")
            self.play(Create(hl), FadeIn(tag))
            for mk, r in zip("cdef", q):
                vo.wait_until(mk)
                self.play(FadeIn(r))
        self.clear_scene()

    def weak(self):
        head = label(r"Brouwer's real number", font_size=32, color=CONN).to_edge(UP, buff=0.4)
        df = MathTex(r"r_n = \begin{cases} (-\tfrac{1}{2})^k & \text{if the first counterexample to Goldbach is the "
                     r"}k\text{-th even number, } k \le n \\ (-\tfrac{1}{2})^n & \text{if there is none up to the "
                     r"}n\text{-th} \end{cases}", font_size=30, color=WHITE).move_to([0, 1.9, 0])
        nl = NumberLine(x_range=[-0.6, 0.6, 0.2], length=11, color=GREY_C, include_numbers=True,
                        decimal_number_config={"num_decimal_places": 1}, font_size=22).move_to([0, 0.0, 0])
        vals = [Fraction(-1, 2) ** n for n in range(1, 8)]
        dots = VGroup(*[Dot(nl.n2p(float(v)), radius=0.07, color=NUM) for v in vals])
        labs = VGroup(*[MathTex(rf"r_{n + 1}", font_size=24, color=NUM).next_to(dt, UP if n % 2 else DOWN, buff=0.15)
                        for n, dt in enumerate(dots[:4])])
        facts = VGroup(
            label(r"every $r_n$ is computable, \ and they converge: \ $r$ is a perfectly good real number", font_size=23,
                  color=OK),
            label(r"if Goldbach is true, \ $r = 0$; \ if it fails first at an even $k$, \ $r > 0$; \ at an odd $k$, "
                  r"\ $r < 0$", font_size=23, color=GREY_A),
            label(r"so we cannot assert \ $r < 0 \;\vee\; r = 0 \;\vee\; r > 0$: \ trichotomy is not a constructive "
                  r"law", font_size=24, color=GOAL),
            label(r"a \textit{weak counterexample}: \ not a disproof, \ but a law that would solve open problems for "
                  r"free", font_size=22, color=GREY_B)).arrange(DOWN, buff=0.2).to_edge(DOWN, buff=0.35)
        with self.voiceover(
            "From an open question, Brouwer built a real number. <bookmark mark='a'/>Its n-th approximation is minus "
            "one half to the power n, unless a counterexample to Goldbach has turned up among the first n even "
            "numbers; then it freezes at minus one half to the power where the first counterexample appeared. "
            "<bookmark mark='b'/>The approximations hop from side to side of zero, closer each time. "
            "<bookmark mark='c'/>Every one is computable, and they converge, so r is a perfectly good real number. "
            "<bookmark mark='d'/>If Goldbach's conjecture is true, r is zero. If it fails first at an even place, r "
            "is positive; at an odd place, negative. <bookmark mark='e'/>So nobody can assert that r is negative, "
            "zero, or positive. Classically, one of the three holds. Constructively, saying which would settle "
            "Goldbach's conjecture. <bookmark mark='f'/>This is a weak counterexample: not a disproof of the law, but "
            "a demonstration that the law would solve open problems for free."
        ) as vo:
            self.play(FadeIn(head))
            vo.wait_until("a")
            self.play(FadeIn(df))
            vo.wait_until("b")
            self.play(Create(nl), run_time=1)
            self.play(LaggedStart(*[FadeIn(dt, scale=1.4) for dt in dots], lag_ratio=0.35), FadeIn(labs),
                      run_time=3)
            for mk, r in zip("cdef", facts):
                vo.wait_until(mk)
                self.play(FadeIn(r))
        self.clear_scene()

    def continuity(self):
        head = label(r"Every function is continuous", font_size=32, color=CONN).to_edge(UP, buff=0.4)
        ax = Axes(x_range=[-2, 2, 1], y_range=[-1.5, 1.5, 1], x_length=6, y_length=3.2, tips=False,
                  axis_config={"color": GREY_C, "stroke_width": 2}).move_to([-3.2, 0.2, 0])
        neg = ax.plot(lambda x: -1, x_range=[-2, -0.02], color=NUM, stroke_width=4)
        pos = ax.plot(lambda x: 1, x_range=[0.02, 2], color=NUM, stroke_width=4)
        hole = VGroup(Circle(radius=0.07, color=NUM).move_to(ax.c2p(0, -1)), Dot(ax.c2p(0, 1), radius=0.07,
                                                                                   color=NUM))
        fl = label(r"$f(x) = -1$ for $x < 0$, \ $1$ for $x \ge 0$", font_size=22, color=NUM).next_to(ax, DOWN,
                                                                                                 buff=0.2)
        band = Rectangle(width=ax.c2p(0.3, 0)[0] - ax.c2p(-0.3, 0)[0], height=3.2, stroke_width=0, fill_color=GOAL,
                         fill_opacity=0.15).move_to(ax.c2p(0, 0))
        steps = VGroup(label(r"to compute $f(x)$, \ use finitely many digits of $x$", font_size=22),
                       label(r"$x = 0.000\dots$ \ so far: \ the interval still straddles $0$", font_size=22,
                             color=GOAL),
                       label(r"no finite stage settles the output: \ $f$ is not a total function", font_size=22,
                             color=BAD)).arrange(DOWN, aligned_edge=LEFT, buff=0.25).move_to([3.3, 0.6, 0])
        rows = VGroup(
            label(r"Brouwer (1924): \ every total function on the reals is continuous \ (choice sequences: reals "
                  r"never finished, \ only ever growing)", font_size=22, color=PROOF),
            label(r"computer science agrees: \ every computable function on the reals is continuous", font_size=22,
                  color=OK),
            label(r"Bishop (1967): \ constructive analysis, \ no anti-classical axioms: \ every proof carries an "
                  r"algorithm", font_size=22, color=GREY_A)).arrange(DOWN, buff=0.2).to_edge(DOWN, buff=0.3)
        with self.voiceover(
            "Brouwer went further. <bookmark mark='a'/>Take the function that is minus one for negative numbers and "
            "one from zero on. Classically, a fine function with a jump. <bookmark mark='b'/>But a real number, for "
            "Brouwer, is never finished: we only ever have finitely many of its digits. To compute the value at x, "
            "we must decide on the basis of finitely many digits. <bookmark mark='c'/>If the digits so far are all "
            "zeros, the number could still turn out negative or positive. <bookmark mark='d'/>No finite stage "
            "settles the output, so the jump function is not a total function at all. <bookmark mark='e'/>Brouwer "
            "proved, in 1924, that every total function on the reals is continuous, using his choice sequences: "
            "reals that grow by free choices, never finished. <bookmark mark='f'/>Computer science now agrees in its "
            "own terms: every computable function on the reals is continuous. <bookmark mark='g'/>And in 1967 Errett "
            "Bishop showed that most of analysis can be done constructively without Brouwer's stranger axioms. Every "
            "theorem stays classically true, and every proof carries an algorithm."
        ) as vo:
            self.play(FadeIn(head), Create(ax))
            vo.wait_until("a")
            self.play(Create(neg), Create(pos), FadeIn(hole), FadeIn(fl))
            vo.wait_until("b")
            self.play(FadeIn(steps[0]))
            vo.wait_until("c")
            self.play(FadeIn(band), FadeIn(steps[1]))
            self.play(band.animate.stretch(0.35, 0), run_time=1.5)
            vo.wait_until("d")
            self.play(FadeIn(steps[2]))
            for mk, r in zip("efg", rows):
                vo.wait_until(mk)
                self.play(FadeIn(r))
        self.clear_scene()

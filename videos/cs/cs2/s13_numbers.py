from __future__ import annotations

import numpy as np

from explainer.cs import *  # noqa: F403
from videos.cs.cs2.common import CLOCK, CODE, COST, CTRL, DATA, FUNC, HEAD, HIST, NO, PART, YES, live_int, load


class Clock(VGroup):
    """A modular clock: m marks around a circle and a hand pointing at x mod m (driven by ``.x``, a tracker)."""

    def __init__(self, m: int, radius=1.0, color=CLOCK, target=None, font_size=24):
        super().__init__()
        self.m = m
        self.ring = Circle(radius, stroke_color=GREY_C, stroke_width=2.5)
        self.add(self.ring)
        self.marks = VGroup()
        for k in range(m):
            a = PI / 2 - 2 * PI * k / m
            p = radius * np.array([np.cos(a), np.sin(a), 0])
            col = YES if target == k else GREY_A
            self.marks.add(MathTex(str(k), font_size=font_size, color=col).move_to(p * 1.25))
        self.add(self.marks)
        self.x = ValueTracker(0)
        self.hand = always_redraw(lambda: Line(self.ring.get_center(), self.ring.get_center() + 0.85 * radius * np.array(
            [np.cos(PI / 2 - 2 * PI * self.x.get_value() / m), np.sin(PI / 2 - 2 * PI * self.x.get_value() / m), 0]),
            color=color, stroke_width=5))
        self.add(self.hand)
        self.title = MathTex(rf"\bmod {m}", font_size=30, color=color).next_to(self.ring, DOWN, buff=0.55)
        self.add(self.title)


class Numbers(VoiceoverScene):
    def construct(self):
        self.card()
        self.bezout()
        self.clocks()
        self.inverse()
        self.crt()
        self.unique()

    def card(self):
        card = chapter_card(12, r"Numbers", r"What can you do with remainders?", part=PART)
        with self.voiceover("Chapter twelve. Numbers."):
            self.play(FadeIn(card[0], shift=UP * 0.2), FadeIn(card[1]), FadeIn(card[2]))
        self.play(FadeOut(card))

    # ------------------------------------------------------------------
    def bezout(self):
        d = load("numbers")
        head = label(r"Euclid, \ keeping track", font_size=38).to_edge(UP, buff=0.35)
        inv = MathTex(r"r = 1071\, s + 462\, t", font_size=40, color=YES).next_to(head, DOWN, buff=0.35)
        il = note(r"the invariant every row keeps", font_size=22).next_to(inv, DOWN, buff=0.1)
        hdr = VGroup(*[MathTex(t, font_size=32, color=GREY_B) for t in ("r", "s", "t", "q")])
        rows = [hdr]
        for r in d["bezout"]:
            rows.append(VGroup(MathTex(str(r["r"]), font_size=34, color=DATA), MathTex(str(r["s"]), font_size=34,
                                                                                     color=CTRL),
                               MathTex(str(r["t"]), font_size=34, color=CTRL),
                               MathTex("" if r["q"] is None else str(r["q"]), font_size=30, color=GREY_B)))
        tab = VGroup(*rows)
        for i, r in enumerate(tab):
            for j, m in enumerate(r):
                m.move_to([-4.6 + j * 1.5, 0.9 - i * 0.62, 0])
        rule = note(r"each row $=$ the row two above $- \ q \times$ the row above", font_size=22).next_to(tab, DOWN,
                                                                                                  buff=0.3)
        res = MathTex(r"21 = -3 \cdot 1071 + 7 \cdot 462", font_size=42, color=HEAD).move_to(RIGHT * 3.2 + UP * 0.6)
        thm = theorem_card(r"B\'ezout", r"$\gcd(a, b) = a s + b t$ for some integers $s, t$; \ and the numbers $a s + b t$ "
                           r"are exactly the multiples of $\gcd(a, b)$.", width=6.0, font_size=22).next_to(res, DOWN,
                                                                                                        buff=0.4)
        jug = note(r"the jugs: \ $4 = 3 \cdot 3 - 1 \cdot 5$: \ fill the 3 three times, \ empty the 5 once",
                   font_size=22).to_edge(DOWN, buff=0.35).shift(RIGHT * 2.4)
        with self.voiceover(
            "Euclid's algorithm from Part 1 can do more than find the greatest common divisor. Run it on a table, and "
            "keep track of how each remainder is made. <bookmark mark='a'/> Every row holds a number r, and two "
            "integers s and t with r equal to s times 1071 plus t times 462. The first two rows are trivial. "
            "<bookmark mark='b'/> Each new row is the row two above, minus the quotient times the row above, so the "
            "invariant survives every step. <bookmark mark='c'/> At the end, twenty-one equals minus three times 1071 "
            "plus seven times 462. <bookmark mark='d'/> This is Bézout's identity: the gcd is always a combination of "
            "the two numbers, and the combinations are exactly its multiples. It is the converse the jugs were missing: "
            "four equals three threes minus one five."
        ) as vo:
            self.play(FadeIn(head))
            vo.wait_until("a")
            self.play(Write(inv), FadeIn(il), FadeIn(tab[0]), FadeIn(tab[1]), FadeIn(tab[2]))
            vo.wait_until("b")
            for r in tab[3:]:
                self.play(FadeIn(r, shift=DOWN * 0.1), run_time=0.8)
            self.play(FadeIn(rule))
            vo.wait_until("c")
            self.play(Write(res))
            vo.wait_until("d")
            self.play(FadeIn(thm), FadeIn(jug))
        self.wait(0.3)
        self.clear_scene()

    # ------------------------------------------------------------------
    def clocks(self):
        head = label(r"Arithmetic on a clock", font_size=38).to_edge(UP, buff=0.35)
        c = Clock(10, radius=1.6).move_to(LEFT * 3.4 + DOWN * 0.3)
        defn = MathTex(r"a \equiv b \pmod m \iff m \mid a - b", font_size=38, color=CLOCK).move_to(RIGHT * 2.8 + UP * 1.8)
        rules = note(r"sums and products can be reduced at any moment: \\ the answer's remainder does not change",
                     font_size=22).next_to(defn, DOWN, buff=0.2)
        pw = VGroup(*[MathTex(rf"7^{{{k}}} \equiv {pow(7, k, 10)}", font_size=34, color=DATA) for k in range(1, 6)])
        pw.arrange(DOWN, aligned_edge=LEFT, buff=0.18).move_to(RIGHT * 1.6 + DOWN * 0.7)
        cyc = MathTex(r"7^{100} = (7^4)^{25} \equiv 1^{25} = 1", font_size=36, color=YES).move_to(RIGHT * 4.6 + DOWN * 0.7)
        cl = note(r"so $7^{100}$ ends in the digit 1", font_size=22).next_to(cyc, DOWN, buff=0.2)
        with self.voiceover(
            "Remainders have an arithmetic of their own. <bookmark mark='a'/> Two numbers are congruent modulo m when "
            "they leave the same remainder, that is, when m divides their difference. On a clock with ten marks, "
            "fourteen and four are the same place. You can add and multiply and reduce at any moment; the remainder "
            "comes out the same. <bookmark mark='b'/> What is the last digit of seven to the hundredth power? Work "
            "modulo ten. Seven, nine, three, one, and then it repeats: the hand comes home every four steps. "
            "<bookmark mark='c'/> A hundred is twenty-five fours, so seven to the hundred is congruent to one. The "
            "number has eighty-five digits, and we know the last one without computing any of the others."
        ) as vo:
            self.play(FadeIn(head), FadeIn(c))
            vo.wait_until("a")
            self.play(Write(defn), FadeIn(rules))
            self.play(c.x.animate.set_value(14), run_time=1.6)
            vo.wait_until("b")
            self.play(c.x.animate.set_value(0), run_time=0.6)
            val = 1
            for k in range(1, 6):
                val = val * 7 % 10
                self.play(c.x.animate.set_value(val), FadeIn(pw[k - 1]), run_time=0.8)
            vo.wait_until("c")
            self.play(Write(cyc), FadeIn(cl))
        self.wait(0.3)
        self.clear_scene()

    # ------------------------------------------------------------------
    def inverse(self):
        head = label(r"Division by remainders", font_size=38).to_edge(UP, buff=0.35)
        q = label(r"solve \ $3x \equiv 1 \pmod{10}$", font_size=32, color=DATA).next_to(head, DOWN, buff=0.4)
        rows = VGroup(*[MathTex(rf"3 \cdot {x} = {3 * x} \equiv {3 * x % 10}", font_size=32,
                                color=YES if 3 * x % 10 == 1 else GREY_A) for x in range(10)])
        rows.arrange_in_grid(rows=2, cols=5, buff=(0.5, 0.3)).next_to(q, DOWN, buff=0.45)
        ok = label(r"$x = 7$: \ $3$ has an inverse modulo $10$", font_size=28, color=YES).next_to(rows, DOWN, buff=0.4)
        no = label(r"but $2x \equiv 1 \pmod{10}$ has no solution: \ $2x$ is always even", font_size=28,
                   color=NO).next_to(ok, DOWN, buff=0.3)
        rule = label(r"$a$ has an inverse mod $m$ \ exactly when $\gcd(a, m) = 1$: \ Bezout gives $as + mt = 1$",
                     font_size=28, color=HEAD).next_to(no, DOWN, buff=0.45)
        with self.voiceover(
            "Can you divide? <bookmark mark='a'/> Solving three x congruent to one, modulo ten, means finding a number "
            "that undoes multiplication by three. Try them all: x equals seven works, because twenty-one ends in one. "
            "<bookmark mark='b'/> But two x congruent to one has no solution at all: two x is always even, and so is "
            "anything congruent to it modulo ten. <bookmark mark='c'/> The rule is Bézout again. a has an inverse "
            "modulo m exactly when a and m share no factor: then a s plus m t equals one, and s is the inverse. The "
            "extended Euclidean algorithm finds it in a few steps even for numbers hundreds of digits long, which is "
            "exactly what RSA, in Part 30, needs."
        ) as vo:
            self.play(FadeIn(head))
            vo.wait_until("a")
            self.play(FadeIn(q), LaggedStart(*[FadeIn(r) for r in rows], lag_ratio=0.1))
            self.play(FadeIn(ok))
            vo.wait_until("b")
            self.play(FadeIn(no))
            vo.wait_until("c")
            self.play(FadeIn(rule))
        self.wait(0.3)
        self.clear_scene()

    # ------------------------------------------------------------------
    def crt(self):
        d = load("numbers")
        head = label(r"Sunzi's remainder problem", font_size=38).to_edge(UP, buff=0.3)
        hc = history_card(r"c.\,400", r"\textit{Sunzi Suanjing}", r"a number leaves 2 when divided by 3, \ 3 by 5, \ "
                          r"2 by 7. \ What is it?", width=5.4, font_size=22).to_corner(UL, buff=0.35).shift(DOWN * 0.6)
        clocks = VGroup(*[Clock(m, radius=0.9, target=r, font_size=20) for m, r in zip(d["mods"], d["res"])]).arrange(
            RIGHT, buff=0.9).move_to(RIGHT * 2.6 + UP * 0.4)
        x = live_int(0, 54, HEAD)
        xl = VGroup(MathTex("x =", font_size=48, color=GREY_A), x).arrange(RIGHT, buff=0.25).next_to(clocks, DOWN,
                                                                                                buff=0.6)
        x.add_updater(lambda m: m.next_to(xl[0], RIGHT, buff=0.25))
        build = MathTex(r"x = " + " + ".join(rf"{t['r']}\cdot{t['Mi']}\cdot{t['inv']}" for t in d["terms"]) +
                        rf" = {sum(t['term'] for t in d['terms'])} \equiv {d['solution']} \pmod{{{d['M']}}}",
                        font_size=32, color=CTRL).to_edge(DOWN, buff=1.0)
        bl = note(r"each term is right for one clock and $0$ on the others; \ $M_i$ is the product of the other "
                  r"moduli, \ times its inverse", font_size=21).next_to(build, DOWN, buff=0.15)
        thm = theorem_card(r"Chinese remainder theorem", r"If $m_1, \dots, m_k$ share no factors, \ the remainders "
                           r"modulo each determine $x$ modulo $m_1 \cdots m_k$, \ uniquely.", width=5.6,
                           font_size=21).next_to(hc, DOWN, buff=0.35).align_to(hc, LEFT)
        with self.voiceover(
            "A puzzle from a Chinese mathematics book of about the year four hundred, the Sunzi Suanjing. "
            "<bookmark mark='a'/> There is a number that leaves remainder two when divided by three, three when divided "
            "by five, and two when divided by seven. What is it? <bookmark mark='b'/> Three clocks, one hand each, all "
            "driven by the same x. Count up, and watch for the moment all three hands point at their targets. "
            "<bookmark mark='c'/> Twenty-three. And the pattern repeats only every three times five times seven, a "
            "hundred and five. <bookmark mark='d'/> There is a construction, not just a search: for each clock, a term "
            "that is right on that clock and zero on the other two, built from an inverse. Add them up. "
            "<bookmark mark='e'/> This is the Chinese remainder theorem. It lets a computer work with a huge number "
            "through its small remainders, in parallel, which Part 30 uses to make RSA four times faster."
        ) as vo:
            self.play(FadeIn(head))
            vo.wait_until("a")
            self.play(FadeIn(hc))
            vo.wait_until("b")
            self.play(FadeIn(clocks), FadeIn(xl))
            for k in range(1, d["solution"] + 1):
                anims = [c.x.animate.set_value(k) for c in clocks] + [x.tracker.animate.set_value(k)]
                self.play(*anims, run_time=0.32 if k < d["solution"] - 2 else 0.7)
            vo.wait_until("c")
            self.play(*[Indicate(c.hand, color=YES) for c in clocks], x.animate.set_color(YES))
            vo.wait_until("d")
            self.play(Write(build), FadeIn(bl))
            vo.wait_until("e")
            self.play(FadeIn(thm))
        self.wait(0.3)
        self.clear_scene()

    # ------------------------------------------------------------------
    def unique(self):
        head = label(r"The fundamental theorem of arithmetic", font_size=38).to_edge(UP, buff=0.35)
        stmt = label(r"every $n \ge 2$ is a product of primes \ in exactly one way \ (up to order)", font_size=30,
                     color=DATA).next_to(head, DOWN, buff=0.4)
        ex = MathTex(r"360 = 2^3 \cdot 3^2 \cdot 5", font_size=44, color=YES).next_to(stmt, DOWN, buff=0.45)
        steps = VGroup(*[label(t, font_size=27, color=c) for t, c in (
            (r"existence: \ chapter 3, \ by strong induction", GREY_A),
            (r"uniqueness needs Euclid's lemma: \ if $p \mid ab$, \ then $p \mid a$ or $p \mid b$", CTRL),
            (r"proof: \ if $p \nmid a$, \ Bezout gives $ps + at = 1$; \ multiply by $b$: \ $p \mid psb + abt = b$",
             HEAD),
        )]).arrange(DOWN, aligned_edge=LEFT, buff=0.32).next_to(ex, DOWN, buff=0.55)
        warn = note(r"it fails in other number systems: \ in $\mathbb{Z}[\sqrt{-5}]$, \ $6 = 2 \cdot 3 = "
                    r"(1 + \sqrt{-5})(1 - \sqrt{-5})$", font_size=22).to_edge(DOWN, buff=0.35)
        with self.voiceover(
            "One last theorem, which most people learn without ever seeing why it is true. <bookmark mark='a'/> Every "
            "number from two up is a product of primes, in exactly one way, apart from the order. Three hundred and "
            "sixty is two cubed, times three squared, times five, and nothing else. <bookmark mark='b'/> That a "
            "factorization exists, chapter three proved by strong induction. That it is unique needs a lemma of "
            "Euclid's: if a prime divides a product, it divides one of the factors. <bookmark mark='c'/> And that lemma "
            "falls out of Bézout. If p does not divide a, then p s plus a t equals one for some s and t; multiply by b, "
            "and p divides both terms on the left, so it divides b. <bookmark mark='d'/> It is not a triviality: in "
            "other number systems it fails, and six factors in two different ways. Unique factorization is why the "
            "hardness of factoring, the thing RSA bets on, is even a well-posed question."
        ) as vo:
            self.play(FadeIn(head))
            vo.wait_until("a")
            self.play(FadeIn(stmt), Write(ex))
            vo.wait_until("b")
            self.play(FadeIn(steps[0]), FadeIn(steps[1]))
            vo.wait_until("c")
            self.play(FadeIn(steps[2]))
            vo.wait_until("d")
            self.play(FadeIn(warn))
        self.wait(0.3)
        self.clear_scene()

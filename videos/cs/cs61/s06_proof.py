from __future__ import annotations

from explainer.cs import *  # noqa: F403
from videos.cs.cs2.compute import load as load2
from videos.cs.cs54.compute import load as load54
from videos.cs.cs61.common import BG, DATA, HEAD, KERN, LAM, NO, PART, YES, code_block, load

_ONES = ("zero one two three four five six seven eight nine ten eleven twelve thirteen fourteen fifteen sixteen "
         "seventeen eighteen nineteen").split()
_TENS = "_ _ twenty thirty forty fifty sixty seventy eighty ninety".split()


def say(n) -> str:
    """A whole number as a speaker says it (British: 'one hundred and ten')."""
    n = int(round(n))
    if n < 20:
        return _ONES[n]
    if n < 100:
        return _TENS[n // 10] + ("" if n % 10 == 0 else "-" + _ONES[n % 10])
    if n < 1000:
        return _ONES[n // 100] + " hundred" + ("" if n % 100 == 0 else " and " + say(n % 100))
    if n < 1_000_000:
        return say(n // 1000) + " thousand" + ("" if n % 1000 == 0 else
                                               (" and " if n % 1000 < 100 else " ") + say(n % 1000))
    return say(n // 1_000_000) + " million" + ("" if n % 1_000_000 == 0 else " " + say(n % 1_000_000))


def box(text: str, color, size=19, w=None, h=0.6, fill=0.12):
    """A rounded box with a Tex caption."""
    t = label(text, font_size=size, color=WHITE)
    r = RoundedRectangle(width=w or t.width + 0.35, height=h, corner_radius=0.1, stroke_color=color,
                         stroke_width=1.8, fill_color=color, fill_opacity=fill)
    if t.width > r.width - 0.15:
        t.width = r.width - 0.15
    t.move_to(r)
    return VGroup(r, t)


def omega(n: int) -> int:
    """The number of prime factors of n, counted with repetition (12 = 2 x 2 x 3 has three)."""
    c, p = 0, 2
    while p * p <= n:
        while n % p == 0:
            n //= p
            c += 1
        p += 1
    return c + (n > 1)


G = load("goldbach")
C = load("collatz")
RAMSEY = load2("ramsey")
LCF = load54("lcf")["size"]
# the primes up to the hardest Goldbach case's smallest partner: which prime it was
_PR = [p for p in range(2, G["worst_p"] + 1) if all(p % q for q in range(2, int(p ** 0.5) + 1))]
WORST_RANK = len(_PR)
# Lander and Parkin (1966), and Frye's fourth powers (1988), checked here with exact integers
LP = (27, 84, 110, 133)
LP_SUM = sum(a ** 5 for a in LP)
assert LP_SUM == 144 ** 5
FRYE = (95800, 217519, 414560)
assert sum(a ** 4 for a in FRYE) == 422481 ** 4
# Liouville's lambda and its running sum, for the first twenty numbers
LAMBDA = {n: (-1) ** omega(n) for n in range(1, 21)}
LSUM = {n: sum(LAMBDA[k] for k in range(1, n + 1)) for n in range(1, 21)}
# the Collatz path of 7, up to the first value below 7
PATH7 = [7]
while PATH7[-1] >= 7:
    x = PATH7[-1]
    PATH7.append(x // 2 if x % 2 == 0 else 3 * x + 1)


class Proof(VoiceoverScene):
    def construct(self):
        self.card()
        self.life()
        self.search()
        self.induction()
        self.euler()
        self.polya()
        self.trust()

    def card(self):
        card = chapter_card(5, r"Proof as research", r"How does a conjecture become a theorem?", lit=(1958, 2014),
                            extra=((1958, r"Haselgrove: \ P\'olya refuted"), (1966, r"Lander and Parkin"),
                                   (1976, r"four colours, \ by computer"), (2014, r"Flyspeck")), part=PART)
        with self.voiceover("Chapter five. Proof as research."):
            self.play(FadeIn(card[0], shift=UP * 0.2), FadeIn(card[1]), FadeIn(card[2]))
        self.play(FadeOut(card))

    # ------------------------------------------------------------------
    def life(self):
        head = label(r"The life of a conjecture", font_size=36).to_edge(UP, buff=0.3)
        xs = (-3.05, -0.25, 2.55, 5.35)
        heads = VGroup(box(r"conjecture", HEAD, w=2.5), box(r"evidence", DATA, w=2.5),
                       box(r"refuted, \ or proved", YES, w=2.5), box(r"proof checked", KERN, w=2.5))
        for h, x in zip(heads, xs):
            h.move_to([x, 2.25, 0])
        arrows = VGroup(*[Arrow(heads[i].get_right(), heads[i + 1].get_left(), buff=0.04, color=GREY_B,
                                stroke_width=2, max_tip_length_to_length_ratio=0.4) for i in range(3)])
        rows_txt = [
            (r"Goldbach", [(r"1742, \ in letters with Euler", WHITE),
                           (r"every even number to $4 \times 10^{18}$ \ (2014)", WHITE),
                           (r"?", GREY_B), (r"", WHITE)]),
            (r"Euler's powers", [(r"1769: \ $k$-th powers need $k$ terms", WHITE),
                                 (r"a search by computer", WHITE),
                                 (r"1966: \ a counterexample", NO), (r"anyone can redo the sum", WHITE)]),
            (r"four colours", [(r"1852: \ Guthrie", WHITE), (r"failed proofs \ (Kempe, \ 1879)", WHITE),
                               (r"1976: \ Appel and Haken, \ by computer", YES),
                               (r"2005: \ Gonthier, \ in Coq", KERN)]),
        ]
        rows = VGroup()
        for i, (name, cells) in enumerate(rows_txt):
            y = 1.0 - 1.35 * i
            nm = label(name, font_size=21, color=HEAD).move_to([-6.85, y, 0], aligned_edge=LEFT)
            cs = VGroup()
            for (t, c), x in zip(cells, xs):
                if not t:
                    cs.add(VectorizedPoint([x, y, 0]))
                    continue
                m = label(t, font_size=34, color=c) if t == "?" else wrapped_label(t, 2.5, font_size=18, color=c)
                cs.add(m.move_to([x, y, 0]))
            rows.add(VGroup(nm, cs))
        rules = VGroup(*[Line([-6.85, 1.0 - 1.35 * i - 0.67, 0], [6.7, 1.0 - 1.35 * i - 0.67, 0], color=GREY_D,
                              stroke_width=1) for i in range(2)])
        foot = wrapped_label(r"evidence alone never moves a conjecture out of the second column: \ only a "
                             r"counterexample or a proof does", 12.4, font_size=21, color=WHITE).to_edge(DOWN,
                                                                                                         buff=0.35)
        with self.voiceover(
            "A conjecture is a statement someone believes and nobody has proved. <bookmark mark='a'/> In letters "
            "in 1742, Christian Goldbach and Leonhard Euler arrived at this one: every even number above two is a "
            "sum of two primes. <bookmark mark='b'/> Then comes evidence: by 2014 it had been checked for every even number up "
            "to four times ten to the eighteenth, and it is still a conjecture. <bookmark mark='c'/> It can leave "
            "that state in only two ways. A counterexample refutes it, as a computer search refuted a conjecture of "
            "Euler's in 1966. <bookmark mark='d'/> Or a proof makes it a theorem, as for the four colours in 1976, "
            "in Part 18. <bookmark mark='e'/> And then the proof itself is checked: in 2005, by a proof assistant."
        ) as vo:
            self.play(FadeIn(head), FadeIn(heads[0]), FadeIn(VGroup(*[r[0] for r in rows])))
            vo.wait_until("a")
            self.play(FadeIn(rows[0][1][0]), FadeIn(rows[1][1][0]), FadeIn(rows[2][1][0]), Create(rules))
            vo.wait_until("b")
            self.play(GrowArrow(arrows[0]), FadeIn(heads[1]))
            self.play(LaggedStart(*[FadeIn(r[1][1]) for r in rows], lag_ratio=0.3))
            vo.wait_until("c")
            self.play(GrowArrow(arrows[1]), FadeIn(heads[2]), FadeIn(rows[0][1][2]))
            self.play(FadeIn(rows[1][1][2], shift=RIGHT * 0.2), FadeIn(rows[1][1][3]))
            vo.wait_until("d")
            self.play(FadeIn(rows[2][1][2], shift=RIGHT * 0.2))
            vo.wait_until("e")
            self.play(GrowArrow(arrows[2]), FadeIn(heads[3]), FadeIn(rows[2][1][3], shift=RIGHT * 0.2))
            self.play(FadeIn(foot))
        self.wait(0.4)
        self.clear_scene()

    # ------------------------------------------------------------------
    def search(self):
        head = label(r"What a computer search proves", font_size=36).to_edge(UP, buff=0.3)
        code = code_block([
            "sieve = primes up to N",
            "left = every even n, 4 .. N",
            "for p in primes:",
            "    ok = sieve[left - p]",
            "    need[left[ok]] = p",
            "    left = left[~ok]",
            "assert left is empty",
        ], size=17)
        frame = SurroundingRectangle(code, buff=0.25, color=GREY_D, stroke_width=1.5, corner_radius=0.08)
        src = note(r"explainer/cs/research/method.py, \ simplified", font_size=16).next_to(frame, DOWN, buff=0.12)
        left = VGroup(frame, code, src).to_edge(LEFT, buff=0.5).shift(UP * 0.7)
        lim = f"{G['limit']:,}".replace(",", "{,}")
        cols = {r"4 \le n \le " + lim: YES, r"n \ge 4": NO}
        r0 = cmath(r"\forall\, n \text{ even},\ ", r"4 \le n \le " + lim, r":\ n = p + q", colors=cols,
                   font_size=32)
        r1 = cmath(r"\forall\, n \text{ even},\ ", r"n \ge 4", r":\ n = p + q", colors=cols, font_size=32)
        w0 = label(r"a theorem: \ finitely many cases, \ every one checked", font_size=19, color=YES)
        w1 = label(r"Goldbach's conjecture: \ no search can reach it", font_size=19, color=NO)
        right = VGroup(r0, w0, r1, w1).arrange(DOWN, aligned_edge=LEFT, buff=0.22)
        right.next_to(left, RIGHT, buff=0.6).align_to(left, UP)
        r1.shift(DOWN * 0.35)
        w1.shift(DOWN * 0.35)
        worst = f"{G['worst']:,}"
        margin = VGroup(
            wrapped_label(rf"the hardest case below {G['limit']:,}: \ {worst} $= {G['worst_p']} + "
                          rf"{G['worst'] - G['worst_p']:,}$".replace(",", "{,}"), 6.4, font_size=20, color=HEAD),
            wrapped_label(rf"{G['worst_p']} is only the {WORST_RANK}th prime: \ a counterexample would need every "
                          r"prime below $n/2$, \ tens of thousands of them, \ to fail", 6.4, font_size=19,
                          color=GREY_A),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.18).next_to(right, DOWN, buff=0.5).align_to(right, LEFT)
        foot = wrapped_label(r"a search proves a finite statement exactly; \ about the infinite one it gives only "
                             r"evidence, \ and a counterexample if it is lucky", 12.4, font_size=21,
                             color=WHITE).to_edge(DOWN, buff=0.35)
        with self.voiceover(
            "What does a search prove? <bookmark mark='a'/> Here is our Goldbach check, simplified: sieve the "
            "primes, then for each prime in turn strike out the even numbers it completes. At the end, nothing is "
            "left. <bookmark mark='b'/> That run proves a theorem: every even number from four to two million is a "
            "sum of two primes. Finitely many cases, every one checked. <bookmark mark='c'/> Change one symbol, to "
            "any size at all, and it is Goldbach's conjecture, which no search can reach. <bookmark mark='d'/> What "
            f"the search gives is a feel for the margin. The hardest case below two million, {say(G['worst'])}, "
            f"needs only {say(G['worst_p'])}, the {say(WORST_RANK)}th prime; a counterexample would need every "
            "prime below half of n to fail."
        ) as vo:
            self.play(FadeIn(head), FadeIn(frame), FadeIn(src))
            vo.wait_until("a")
            self.play(LaggedStart(*[FadeIn(c, shift=RIGHT * 0.1) for c in code], lag_ratio=0.25), run_time=2.5)
            vo.wait_until("b")
            self.play(Write(r0), FadeIn(w0))
            vo.wait_until("c")
            self.play(TransformMatchingTex(r0.copy(), r1), FadeIn(w1))
            vo.wait_until("d")
            self.play(FadeIn(margin[0]))
            self.play(FadeIn(margin[1]))
            self.play(FadeIn(foot))
        self.wait(0.4)
        self.clear_scene()

    # ------------------------------------------------------------------
    def induction(self):
        head = label(r"Searching smarter: \ induction, \ by computer", font_size=36).to_edge(UP, buff=0.3)
        chips = VGroup()
        for i, v in enumerate(PATH7):
            c = YES if i == len(PATH7) - 1 else (HEAD if i == 0 else DATA)
            t = label(str(v), font_size=22, color=c)
            r = RoundedRectangle(width=max(0.7, t.width + 0.25), height=0.55, corner_radius=0.08, stroke_color=c,
                                 stroke_width=1.6, fill_color=c, fill_opacity=0.1)
            chips.add(VGroup(r, t.move_to(r)))
        chips.arrange(RIGHT, buff=0.32).next_to(head, DOWN, buff=0.55)
        steps = VGroup(*[Arrow(chips[i].get_right(), chips[i + 1].get_left(), buff=0.02, color=GREY_C,
                               stroke_width=1.6, max_tip_length_to_length_ratio=0.5) for i in range(len(chips) - 1)])
        below = label(r"below 7: \ already checked", font_size=18, color=YES).next_to(chips[-1], DOWN, buff=0.15)
        below.align_to(chips[-1], RIGHT)
        rule = label(r"halve an even number; \ treble an odd one and add one", font_size=19,
                     color=GREY_A).next_to(chips, DOWN, buff=0.15).align_to(chips, LEFT)
        code = code_block([
            "for n in range(1, N):",
            "    x = n",
            "    while x >= n and x != 1:",
            "        x = x//2 if x%2 == 0 else 3*x+1",
            "    # now x < n: done before",
        ], size=16)
        frame = SurroundingRectangle(code, buff=0.22, color=GREY_D, stroke_width=1.5, corner_radius=0.08)
        lc = VGroup(frame, code).to_edge(LEFT, buff=0.5).shift(DOWN * 0.95)
        src = note(r"method.py, \ collatz, \ simplified", font_size=16).next_to(frame, DOWN, buff=0.1).align_to(
            frame, LEFT)
        cols = {r"P(m)": DATA, r"P(n)": YES}
        rows = VGroup(
            cmath(r"P(m)", r"\ \text{for every } m < n", colors=cols, font_size=30),
            cmath(r"\text{the path from } n \text{ reaches some } m < n", colors=cols, font_size=30),
            cmath(r"\Rightarrow\ ", r"P(n)", colors=cols, font_size=30),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.42)
        rows.next_to(lc, RIGHT, buff=0.5).align_to(lc, UP).shift(DOWN * 0.05)
        whys = VGroup(label(r"strong induction \ (Part 2)", font_size=17, color=GREY_B),
                      label(r"the loop's job: \ follow the path until it drops", font_size=17, color=GREY_B),
                      label(r"$P(n)$: \ the path from $n$ reaches 1", font_size=17, color=GREY_B))
        for w, r in zip(whys, rows):
            w.next_to(r, DOWN, buff=0.08).align_to(r, LEFT)
        lim = say(C["limit"])
        res = wrapped_label(rf"every start below {C['limit']:,} reaches 1: \ a theorem; \ for every start, \ the "
                            r"step is the open problem", 12.4, font_size=21, color=WHITE).to_edge(DOWN, buff=0.3)
        with self.voiceover(
            "Our Collatz check is cleverer than it looks. <bookmark mark='a'/> Halve an even number, treble an odd "
            "one and add one. From seven the path climbs to fifty-two, then falls to five. <bookmark mark='b'/> "
            "There the program stops, because every start below seven already reaches one. <bookmark mark='c'/> "
            "That is strong induction, from Part 2: assume the claim for every smaller start; <bookmark mark='d'/> "
            "show that the path from n drops below n; <bookmark mark='e'/> then it holds for n. The computer proves "
            f"that step for each n below {lim}, so every start below {lim} reaches one. <bookmark mark='f'/> "
            "Proving the step for every n is the whole Collatz problem."
        ) as vo:
            self.play(FadeIn(head))
            vo.wait_until("a")
            self.play(FadeIn(rule), FadeIn(chips[0]))
            self.play(LaggedStart(*[AnimationGroup(GrowArrow(a), FadeIn(c)) for a, c in zip(steps, chips[1:])],
                                  lag_ratio=0.5), run_time=3.5)
            vo.wait_until("b")
            self.play(Indicate(chips[-1], color=YES), FadeIn(below))
            self.play(FadeIn(lc), FadeIn(src))
            vo.wait_until("c")
            self.play(Write(rows[0]), FadeIn(whys[0]))
            vo.wait_until("d")
            self.play(FadeIn(rows[1]), FadeIn(whys[1]))
            vo.wait_until("e")
            self.play(FadeIn(rows[2]), FadeIn(whys[2]))
            vo.wait_until("f")
            self.play(FadeIn(res))
        self.wait(0.4)
        self.clear_scene()

    # ------------------------------------------------------------------
    def euler(self):
        head = label(r"A conjecture refuted by search", font_size=36).to_edge(UP, buff=0.3)
        cols = {r"m \ge k": NO}
        stmt = cmath(r"a_1^k + a_2^k + \cdots + a_m^k = b^k \quad (m \ge 2)", r"\ \Rightarrow\ ", r"m \ge k", colors=cols,
                     font_size=34)
        stmt.next_to(head, DOWN, buff=0.35)
        sw = label(r"Euler \ (1769): \ to make a $k$-th power from $k$-th powers, \ you need at least $k$ of them",
                   font_size=19, color=GREY_A).next_to(stmt, DOWN, buff=0.15)
        five = cmath(r"a^5 + b^5 + c^5 + d^5", r"\ \neq\ ", r"e^5 \ ?", font_size=34, color=WHITE)
        found = cmath(r"27^5 + 84^5 + 110^5 + 133^5", r"\ =\ ", r"144^5", font_size=34, color=WHITE)
        found[0].set_color(DATA)
        found[2].set_color(YES)
        five.next_to(sw, DOWN, buff=0.35).set_x(-2.6)
        found.move_to(five)

        def big(v):
            return f"{v:,}".replace(",", "{,}")
        terms = VGroup(*[MathTex(rf"{a}^5", r"=", big(a ** 5), font_size=30, color=DATA) for a in LP])
        total = MathTex(r"\text{sum}", r"=", big(LP_SUM), font_size=30, color=WHITE)
        last = MathTex(r"144^5", r"=", big(144 ** 5), font_size=30, color=YES)
        col = VGroup(*terms, total, last).arrange(DOWN, buff=0.18)
        for m in col:
            m.shift((0 - m[1].get_center()[0]) * RIGHT)
        col.next_to(found, DOWN, buff=0.35).set_x(-2.6)
        for m in col:
            m.shift((col[0][1].get_center()[0] - m[1].get_center()[0]) * RIGHT)
        bar = Line(total.get_left() + UP * 0.25 + LEFT * 0.1, total.get_right() + UP * 0.25 + RIGHT * 0.1,
                   color=GREY_B, stroke_width=1.5)
        side = VGroup(
            wrapped_label(r"Lander and Parkin \ (1966): \ found by a direct search on a computer; \ their published "
                          r"note is only a few lines long", 4.6, font_size=19, color=WHITE),
            wrapped_label(r"fourth powers fell in 1988: \ Elkies found a counterexample, \ and showed there are "
                          r"infinitely many; \ Frye's search found the smallest:", 4.6, font_size=19, color=GREY_A),
            MathTex(r"95800^4 + 217519^4 + 414560^4", r"= 422481^4", font_size=24, color=HEAD).arrange(
                DOWN, aligned_edge=RIGHT, buff=0.08),
            note(r"both identities checked here, \ in exact integers", font_size=17),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.3).to_edge(RIGHT, buff=0.4).shift(DOWN * 0.7)
        with self.voiceover(
            "Search shines when a conjecture is false. <bookmark mark='a'/> In 1769 Euler conjectured that it takes "
            "at least k k-th powers to add up to a k-th power: three cubes, four fourth powers, five fifth powers. "
            "<bookmark mark='b'/> So four fifth powers should never sum to a fifth power. <bookmark mark='c'/> In "
            "1966 Leon Lander and Thomas Parkin searched by computer and found four that do. <bookmark mark='d'/> "
            "Check it: twenty-seven, eighty-four, one hundred and ten and one hundred and thirty-three, each to "
            "the fifth. <bookmark mark='e'/> The sum is exactly one hundred and forty-four to the fifth. Their note "
            "is a few lines long; it needed nothing else. <bookmark mark='f'/> Fourth powers fell in 1988: Noam "
            "Elkies found a counterexample, and Roger Frye's search found the smallest."
        ) as vo:
            self.play(FadeIn(head))
            vo.wait_until("a")
            self.play(Write(stmt), FadeIn(sw))
            vo.wait_until("b")
            self.play(FadeIn(five))
            vo.wait_until("c")
            self.play(ReplacementTransform(five, found), run_time=1.5)
            self.play(FadeIn(side[0]))
            vo.wait_until("d")
            self.play(LaggedStart(*[FadeIn(t, shift=DOWN * 0.15) for t in terms], lag_ratio=0.5), run_time=3)
            vo.wait_until("e")
            self.play(Create(bar), FadeIn(total))
            self.play(FadeIn(last), Indicate(found[2], color=YES))
            vo.wait_until("f")
            self.play(FadeIn(side[1]), FadeIn(side[2]), FadeIn(side[3]))
        self.wait(0.4)
        self.clear_scene()

    # ------------------------------------------------------------------
    def polya(self):
        head = label(r"When the evidence misleads", font_size=36).to_edge(UP, buff=0.3)
        cols = {r"\Omega(n)": DATA}
        lam = cmath(r"\lambda(n) = (-1)^{", r"\Omega(n)", r"}", colors=cols, font_size=32)
        lsum = cmath(r"L(n) = \sum_{k \le n} \lambda(k)", r"\ \le\ 0 \quad (n \ge 2)\ ?", font_size=32)
        lsum[1].set_color(NO)
        top = VGroup(lam, lsum).arrange(RIGHT, buff=1.0).next_to(head, DOWN, buff=0.25)
        lw = label(r"$\Omega(n)$: \ prime factors, \ counted with repeats: \ $12 = 2 \cdot 2 \cdot 3$ has three",
                   font_size=18, color=GREY_B).next_to(top, DOWN, buff=0.12)
        ns = list(range(2, 21))
        tiles = VGroup()
        for n in ns:
            c = DATA if LAMBDA[n] < 0 else KERN
            r = Square(side_length=0.56, stroke_color=c, stroke_width=1.6, fill_color=c, fill_opacity=0.18)
            t = label(str(n), font_size=20, color=WHITE).move_to(r)
            s = label("$-1$" if LAMBDA[n] < 0 else "$+1$", font_size=17, color=c).next_to(r, DOWN, buff=0.08)
            tiles.add(VGroup(r, t, s))
        tiles.arrange(RIGHT, buff=0.1).next_to(lw, DOWN, buff=0.25)
        key = VGroup(label(r"odd count: \ $-1$", font_size=17, color=DATA),
                     label(r"even count: \ $+1$", font_size=17, color=KERN)).arrange(RIGHT, buff=0.5)
        y0 = tiles.get_bottom()[1] - 0.6
        sc = 0.36
        ypos = lambda v: y0 + sc * v  # noqa: E731
        zero = DashedLine([tiles.get_left()[0], ypos(0), 0], [tiles.get_right()[0], ypos(0), 0], color=NO,
                          stroke_width=1.8)
        zl = label(r"0", font_size=17, color=NO).next_to(zero, LEFT, buff=0.1)
        pts = [[tiles[i].get_x(), ypos(LSUM[n]), 0] for i, n in enumerate(ns)]
        stair = VMobject(color=HEAD, stroke_width=2.5).set_points_as_corners(
            [p for a, b in zip(pts, pts[1:] + [[pts[-1][0] + 0.3, pts[-1][1], 0]]) for p in (a, [b[0], a[1], 0])])
        dots = VGroup(*[Dot(p, radius=0.05, color=HEAD) for p in pts])
        touch = VGroup(*[Circle(radius=0.11, color=NO, stroke_width=2).move_to(pts[i])
                         for i, n in enumerate(ns) if LSUM[n] == 0])
        ll = label(r"$L(n)$", font_size=19, color=HEAD).next_to(pts[-1], DOWN, buff=0.15)
        key.next_to(VGroup(zero, stair), DOWN, buff=0.15).align_to(tiles, LEFT)
        facts = wrapped_label(r"P\'olya conjectured it; \ Haselgrove \ (1958) \ proved it false without finding "
                              r"where; \ Tanaka \ (1980): \ the first failure is at $n = 906{,}150{,}257$", 12.4,
                              font_size=20, color=WHITE).to_edge(DOWN, buff=0.3)
        with self.voiceover(
            "Sometimes the small cases lie. <bookmark mark='a'/> Give every number a sign: minus one if it has an "
            "odd number of prime factors, counted with repeats, plus one if even. Twelve is two times two times "
            "three: minus one. <bookmark mark='b'/> Primes get minus one; four, two times two, gets plus one. "
            "<bookmark mark='c'/> Keep a running total. It touches zero at two, four, six, ten and sixteen, and "
            "never rises above. <bookmark mark='d'/> George Pólya conjectured that it never does. "
            "<bookmark mark='e'/> In 1958 Brian Haselgrove proved it false without finding where, and in 1980 "
            "Minoru Tanaka found the first failure, near nine hundred and six million. A search to two million "
            "would have confirmed the conjecture more than four hundred times over."
        ) as vo:
            self.play(FadeIn(head))
            vo.wait_until("a")
            self.play(Write(lam), FadeIn(lw))
            vo.wait_until("b")
            self.play(LaggedStart(*[FadeIn(t, shift=DOWN * 0.1) for t in tiles], lag_ratio=0.12), FadeIn(key),
                      run_time=3)
            vo.wait_until("c")
            self.play(Create(zero), FadeIn(zl))
            self.play(Create(stair), FadeIn(dots), FadeIn(ll), run_time=2.5)
            self.play(LaggedStart(*[Create(t) for t in touch], lag_ratio=0.2))
            vo.wait_until("d")
            self.play(FadeIn(lsum))
            vo.wait_until("e")
            self.play(FadeIn(facts))
        self.wait(0.4)
        self.clear_scene()

    # ------------------------------------------------------------------
    def trust(self):
        head = label(r"What a proof asks you to trust", font_size=36).to_edge(UP, buff=0.3)
        tiers = [
            (r"a reader checks \\ every step", HEAD,
             r"Part 2: \ among six people, \ three are friends or three are strangers, \ by the pigeonhole "
             r"principle, \ in two lines", r"the argument, \ and its readers", 4.2),
            (r"a program checks \\ every case", DATA,
             rf"Part 2 again: \ all $2^{{15}} = 32{{,}}768$ colourings, \ {RAMSEY['good6']} escape; \ four "
             r"colours \ (1976); \ Kepler \ (Hales, \ 1998); \ Pythagorean triples, \ a 200-terabyte proof \ "
             r"(2016, \ Part 26)", r"the program, \ its compiler, \ the machine", 3.0),
            (r"a kernel checks \\ every inference", KERN,
             rf"four colours in Coq \ (2005); \ Kepler, \ Flyspeck \ (2014); \ Part 54's kernel: \ "
             rf"{LCF['kernel_lines']} lines, \ {len(LCF['rules'])} rules", rf"the kernel: \ "
             rf"{LCF['kernel_lines']} lines in Part 54", 0.9),
        ]
        rows = VGroup()
        for t, c, ex, tr, wbar in tiers:
            nm = Tex(r"\begin{tabular}{@{}l@{}}" + t + r"\end{tabular}", font_size=22, color=c)
            exl = wrapped_label(ex, 5.2, font_size=18, color=GREY_A)
            bar = Rectangle(width=wbar, height=0.36, stroke_width=0, fill_color=c, fill_opacity=0.7)
            trl = wrapped_label(tr, 4.2, font_size=18, color=WHITE)
            rows.add(VGroup(nm, exl, bar, trl))
        for i, r in enumerate(rows):
            y = 1.55 - 1.55 * i
            r[0].move_to([-6.8, y, 0], aligned_edge=LEFT)
            r[1].move_to([-4.0, y, 0], aligned_edge=LEFT)
            r[2].move_to([1.75, y + 0.25, 0], aligned_edge=LEFT)
            r[3].next_to(r[2], DOWN, buff=0.1).align_to(r[2], LEFT)
        tl = label(r"what you must trust", font_size=20, color=GREY_B).move_to([1.75, 2.45, 0], aligned_edge=LEFT)
        rules = VGroup(*[Line([-6.8, 1.55 - 1.55 * i - 0.78, 0], [6.7, 1.55 - 1.55 * i - 0.78, 0], color=GREY_D,
                              stroke_width=1) for i in range(2)])
        foot = wrapped_label(r"a theorem is only as sure as the least reliable thing you have to trust: \ proof "
                             r"assistants make that thing small", 12.4, font_size=21, color=YES).to_edge(DOWN,
                                                                                                        buff=0.35)
        with self.voiceover(
            "Each way of checking a proof asks you to trust something different. <bookmark mark='a'/> Part 2 "
            "proved that among six people, three are friends or three are strangers, in two lines, by "
            "pigeonholes. You trust the argument and its readers. <bookmark mark='b'/> Part 2 also checked all "
            "thirty-two thousand seven hundred and sixty-eight colourings by brute force. The four colour theorem, "
            "Thomas Hales's 1998 proof of Kepler's conjecture, and Part 26's two-hundred-terabyte proof work this "
            "way: you trust a program, its compiler and the machine. <bookmark mark='c'/> A proof assistant checks "
            f"every inference, and you trust only its kernel, {say(LCF['kernel_lines'])} lines in Part 54. Four "
            "colours were checked this way in 2005, and Kepler by Hales's Flyspeck project in 2014. "
            "<bookmark mark='d'/> A theorem is only as sure as the least reliable thing you trust."
        ) as vo:
            self.play(FadeIn(head), FadeIn(tl))
            for mk, r, i in zip("abc", rows, range(3)):
                vo.wait_until(mk)
                anims = [FadeIn(r[0], shift=RIGHT * 0.15), FadeIn(r[1]), GrowFromEdge(r[2], LEFT), FadeIn(r[3])]
                if i:
                    anims.append(Create(rules[i - 1]))
                self.play(*anims, run_time=1.5)
            vo.wait_until("d")
            self.play(FadeIn(foot))
        self.wait(0.4)
        self.clear_scene()


_ = (BG, KERN, LAM)

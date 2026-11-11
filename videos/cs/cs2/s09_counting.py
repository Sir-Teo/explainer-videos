from __future__ import annotations

import math

import numpy as np

from explainer.cs import *  # noqa: F403
from videos.cs.cs2.common import COST, CTRL, DATA, FUNC, HEAD, INF, NO, PART, YES, fmt, load


class Counting(VoiceoverScene):
    def construct(self):
        self.card()
        self.rules()
        self.choose()
        self.pascal()
        self.sierpinski()
        self.identities()
        self.stars()

    def card(self):
        card = chapter_card(8, r"Counting", r"How many ways are there?", part=PART)
        with self.voiceover("Chapter eight. Counting."):
            self.play(FadeIn(card[0], shift=UP * 0.2), FadeIn(card[1]), FadeIn(card[2]))
        self.play(FadeOut(card))

    # ------------------------------------------------------------------
    def rules(self):
        head = label(r"The product rule", font_size=38).to_edge(UP, buff=0.35)
        root = Dot(LEFT * 5.2 + DOWN * 0.3, color=GREY_A)
        firsts = VGroup(*[Dot(LEFT * 3.0 + UP * (1.6 - 1.6 * i) + DOWN * 0.3, color=DATA) for i in range(3)])
        e1 = VGroup(*[Line(root.get_center(), f.get_center(), color=GREY_C) for f in firsts])
        seconds, e2, leaves = VGroup(), VGroup(), VGroup()
        for i, f in enumerate(firsts):
            for j in range(4):
                p = f.get_center() + RIGHT * 2.0 + UP * (0.6 - 0.4 * j)
                d_ = Dot(p, color=CTRL, radius=0.07)
                seconds.add(d_)
                e2.add(Line(f.get_center(), p, color=GREY_D))
        l1 = label(r"3 choices", font_size=26, color=DATA).next_to(firsts, UP, buff=0.3)
        l2 = label(r"then 4 each", font_size=26, color=CTRL).next_to(seconds, UP, buff=0.15)
        tot = MathTex(r"3 \times 4 = 12", font_size=44, color=YES).next_to(seconds, RIGHT, buff=0.8)
        pw = VGroup(label(r"an 8-character password from $62$ symbols:", font_size=28, color=GREY_A),
                    MathTex(r"62^8 = 218{,}340{,}105{,}584{,}896", font_size=38, color=COST),
                    note(r"at $10^{10}$ guesses a second: \ about $6$ hours", font_size=24)).arrange(
            DOWN, buff=0.2).to_edge(DOWN, buff=0.4).shift(RIGHT * 2.6)
        sumr = label(r"sum rule: \ choices from \textit{separate} lists add", font_size=26, color=GREY_B).next_to(
            head, DOWN, buff=0.25)
        with self.voiceover(
            "Counting is the raw material of every bound in this series: how many inputs, states, keys, paths. Two rules "
            "do most of the work. <bookmark mark='a'/> If you choose from one list or from a separate one, the counts "
            "add. <bookmark mark='b'/> If you make one choice and then another, and the second has the same number of "
            "options whatever the first was, the counts multiply. Three, then four: twelve outcomes, the leaves of this "
            "tree. <bookmark mark='c'/> The product rule is why passwords work. Eight characters, each one of sixty-two "
            "letters and digits: sixty-two to the eighth, about two hundred trillion. And why short ones do not: at ten "
            "billion guesses a second, all of them take about six hours."
        ) as vo:
            self.play(FadeIn(head))
            vo.wait_until("a")
            self.play(FadeIn(sumr))
            vo.wait_until("b")
            self.play(FadeIn(root), Create(e1), FadeIn(firsts), FadeIn(l1))
            self.play(Create(e2), FadeIn(seconds), FadeIn(l2), run_time=1.4)
            self.play(Write(tot))
            vo.wait_until("c")
            self.play(FadeIn(pw, lag_ratio=0.3))
        self.wait(0.3)
        self.clear_scene()

    # ------------------------------------------------------------------
    def choose(self):
        head = label(r"Order, \ and forgetting it", font_size=38).to_edge(UP, buff=0.35)
        letters = "ABCD"
        cols = {"A": DATA, "B": CTRL, "C": FUNC, "D": HEAD}

        def chip(s):
            return VGroup(*[VGroup(RoundedRectangle(width=0.5, height=0.5, corner_radius=0.08, stroke_width=1.5,
                                                    stroke_color=cols[c], fill_color="#121722", fill_opacity=1),
                                   Text(c, font="DejaVu Sans Mono", font_size=24, color=cols[c])) for c in s]).arrange(
                RIGHT, buff=0.06)

        ordered = [a + b for a in letters for b in letters if a != b]
        og = VGroup(*[chip(s) for s in ordered]).arrange_in_grid(rows=4, cols=3, buff=(0.45, 0.3))
        og.move_to(LEFT * 3.4 + DOWN * 0.3)
        ol = MathTex(r"4 \times 3 = 12 \text{ ordered}", font_size=34, color=GREY_A).next_to(og, UP, buff=0.35)
        pairs = sorted({"".join(sorted(s)) for s in ordered})
        ug = VGroup(*[chip(s) for s in pairs]).arrange_in_grid(rows=3, cols=2, buff=(0.5, 0.45))
        ug.move_to(RIGHT * 1.6 + DOWN * 0.3)
        ul = MathTex(r"12 / 2! = 6 \text{ sets}", font_size=34, color=YES).next_to(ug, UP, buff=0.35)
        fs = VGroup(MathTex(r"n! = n (n - 1) \cdots 1", font_size=34, color=GREY_A),
                    MathTex(r"\binom{n}{k} = \frac{n!}{k!\,(n - k)!}", font_size=44, color=YES)).arrange(
            DOWN, buff=0.45).move_to(RIGHT * 5.0 + DOWN * 0.2)
        with self.voiceover(
            "Arrangements next. <bookmark mark='a'/> Line up n different things: n choices for the first place, n minus "
            "one for the second, and so on. n factorial. <bookmark mark='b'/> Choose two of four letters, in order: four "
            "times three, twelve. <bookmark mark='c'/> But if the order does not matter, each set of two was counted "
            "twice, once in each order. Divide by two factorial: six. <bookmark mark='d'/> In general, choosing k of n "
            "things, ignoring order, is n factorial over k factorial times n minus k factorial: n choose k. Counting "
            "too much and then dividing out a known overcount is one of the most useful tricks there is."
        ) as vo:
            self.play(FadeIn(head))
            vo.wait_until("a")
            self.play(FadeIn(fs[0]))
            vo.wait_until("b")
            self.play(FadeIn(ol), LaggedStart(*[FadeIn(c) for c in og], lag_ratio=0.06))
            vo.wait_until("c")
            copies = [c.copy() for c in og]
            self.play(*[cp.animate.move_to(ug[pairs.index("".join(sorted(s)))]) for s, cp in zip(ordered, copies)],
                      FadeIn(ul), run_time=2.0)
            self.add(ug)
            self.remove(*copies)
            vo.wait_until("d")
            self.play(FadeIn(fs[1]))
        self.wait(0.3)
        self.clear_scene()

    # ------------------------------------------------------------------
    def pascal(self):
        d = load("pascal")
        rows = d["rows"][:9]
        head = label(r"Pascal's triangle", font_size=38).to_edge(UP, buff=0.3)
        tri = VGroup()
        for n, r in enumerate(rows):
            row = VGroup(*[MathTex(str(v), font_size=30, color=YES if v == max(r) and n == 8 else WHITE)
                           for v in r])
            for k, m in enumerate(row):
                m.move_to([(k - n / 2) * 0.78, 2.4 - n * 0.6, 0])
            tri.add(row)
        tri.shift(LEFT * 2.2)
        rule = MathTex(r"\binom{n}{k} = \binom{n-1}{k-1} + \binom{n-1}{k}", font_size=40, color=CTRL).move_to(
            RIGHT * 3.6 + UP * 1.5)
        why = label(r"choose $k$ of $n$ people: \\ either Ann is in \ (choose $k - 1$ more) \\ or she is not \ "
                    r"(choose all $k$ from the rest)", font_size=26, color=GREY_A).next_to(rule, DOWN, buff=0.35)
        binom = MathTex(r"(x + y)^n = \sum_{k} \binom{n}{k} x^k y^{n - k}", font_size=40, color=FUNC).next_to(
            why, DOWN, buff=0.5)
        bw = note(r"pick $x$ from $k$ of the $n$ factors", font_size=22).next_to(binom, DOWN, buff=0.15)
        with self.voiceover(
            "The numbers n choose k fit into a triangle. <bookmark mark='a'/> Each entry is the sum of the two above it. "
            "<bookmark mark='b'/> Why? A counting argument, with no algebra. To choose k people from n, either Ann is "
            "chosen, and you pick k minus one more from the others, or she is not, and you pick all k from the others. "
            "Those two cases are separate, so they add. A proof that counts the same set two ways is called a bijective, "
            "or combinatorial, proof. <bookmark mark='c'/> The same numbers expand powers. Multiply out x plus y, n "
            "times: each term picks x from some of the factors and y from the rest, and there are n choose k ways to "
            "pick x from k of them."
        ) as vo:
            self.play(FadeIn(head))
            vo.wait_until("a")
            self.play(FadeIn(tri[0]), FadeIn(tri[1]))
            for n in range(2, len(rows)):
                anims = [FadeIn(tri[n][0]), FadeIn(tri[n][-1])]
                for k in range(1, n):
                    anims.append(TransformFromCopy(VGroup(tri[n - 1][k - 1], tri[n - 1][k]), tri[n][k]))
                self.play(*anims, run_time=0.6)
            vo.wait_until("b")
            self.play(FadeIn(rule), FadeIn(why))
            vo.wait_until("c")
            self.play(FadeIn(binom), FadeIn(bw))
        self.wait(0.3)
        self.clear_scene()

    # ------------------------------------------------------------------
    def sierpinski(self):
        d = load("pascal")
        m = np.asarray(d["mod2"])
        head = label(r"Pascal's triangle, \ odd entries lit", font_size=38).to_edge(UP, buff=0.3)
        small = VGroup()
        for n in range(16):
            for k in range(n + 1):
                odd = math.comb(n, k) % 2 == 1
                small.add(Square(0.2, stroke_width=0, fill_color=HEAD if odd else "#1B2130", fill_opacity=1).move_to(
                    [(k - n / 2) * 0.22 - 3.6, 1.6 - n * 0.2, 0]))
        big = bitmap(m, ["#0E131C", C.CS_HEAD], width=5.8, height=5.8 * m.shape[0] / m.shape[1] * 2.0)
        big.move_to(RIGHT * 3.0 + DOWN * 0.45)
        l1 = note(r"16 rows", font_size=22).next_to(small, DOWN, buff=0.2)
        l2 = note(r"128 rows \ (computed)", font_size=22).next_to(big, DOWN, buff=0.15)
        luc = VGroup(label(r"$\binom{n}{k}$ is odd \ exactly when \\ every binary 1 of $k$ is a 1 of $n$",
                           font_size=25, color=YES),
                     label(r"so row $n$ has $2^{\#\text{1s in } n}$ odd entries", font_size=23, color=GREY_A)).arrange(
            DOWN, buff=0.2).move_to(LEFT * 3.6 + DOWN * 2.7)
        with self.voiceover(
            "Colour each entry by whether it is odd. <bookmark mark='a'/> Sixteen rows show a pattern of triangles "
            "inside triangles. <bookmark mark='b'/> A hundred and twenty-eight rows, computed, and it is Sierpiński's "
            "triangle, a fractal, made of nothing but additions. <bookmark mark='c'/> There is an exact rule behind it, "
            "Lucas's theorem: n choose k is odd exactly when every binary one of k is also a one of n. So the number of "
            "odd entries in row n is two to the number of ones in n's binary form. Binary keeps turning up uninvited; "
            "from Part 3 on, it is all we have."
        ) as vo:
            self.play(FadeIn(head))
            vo.wait_until("a")
            self.play(LaggedStart(*[FadeIn(s_) for s_ in small], lag_ratio=0.004), FadeIn(l1), run_time=2.0)
            vo.wait_until("b")
            self.play(FadeIn(big), FadeIn(l2))
            vo.wait_until("c")
            self.play(FadeIn(luc, lag_ratio=0.3))
        self.wait(0.3)
        self.clear_scene()

    # ------------------------------------------------------------------
    def identities(self):
        d = load("pascal")
        v = d["vandermonde"]
        head = label(r"Proof by counting twice", font_size=38).to_edge(UP, buff=0.35)
        q = label(r"choose a committee of $3$ \ from $5$ engineers and $4$ designers", font_size=30, color=GREY_A)
        q.next_to(head, DOWN, buff=0.4)
        eng = VGroup(*[Circle(0.22, stroke_width=0, fill_color=DATA, fill_opacity=0.9) for _ in range(5)]).arrange(
            RIGHT, buff=0.18)
        des = VGroup(*[Circle(0.22, stroke_width=0, fill_color=CTRL, fill_opacity=0.9) for _ in range(4)]).arrange(
            RIGHT, buff=0.18)
        people = VGroup(eng, des).arrange(RIGHT, buff=0.6).next_to(q, DOWN, buff=0.4)
        one = MathTex(r"\text{ignore the jobs: } \binom{9}{3} = " + str(v[1]), font_size=36, color=YES)
        two = MathTex(r"\text{by how many engineers: } " + " + ".join(
            rf"\binom{{5}}{{{k}}}\binom{{4}}{{{3 - k}}}" for k in range(4)), font_size=34, color=CTRL)
        two_v = MathTex(" + ".join(str(x) for x in v[0]) + rf" = {sum(v[0])}", font_size=36, color=CTRL)
        VGroup(one, two, two_v).arrange(DOWN, buff=0.35).next_to(people, DOWN, buff=0.5)
        gen = MathTex(r"\binom{m + n}{r} = \sum_k \binom{m}{k}\binom{n}{r - k}", font_size=40, color=HEAD).to_edge(
            DOWN, buff=0.45)
        gl = note(r"Vandermonde's identity", font_size=22).next_to(gen, UP, buff=0.12)
        with self.voiceover(
            "Counting the same set in two ways proves identities that would be tedious by algebra. "
            "<bookmark mark='a'/> Choose a committee of three from five engineers and four designers. "
            "<bookmark mark='b'/> Ignoring jobs, it is nine choose three: eighty-four. <bookmark mark='c'/> Or split by "
            "how many engineers it has, zero to three, and choose each part separately: four, plus thirty, plus forty, "
            "plus ten. Eighty-four again, as it must be. <bookmark mark='d'/> In general this is Vandermonde's identity, "
            "and the argument proves it for every m, n and r at once."
        ) as vo:
            self.play(FadeIn(head))
            vo.wait_until("a")
            self.play(FadeIn(q), FadeIn(people, lag_ratio=0.1))
            vo.wait_until("b")
            self.play(FadeIn(one))
            vo.wait_until("c")
            self.play(FadeIn(two))
            self.play(FadeIn(two_v))
            vo.wait_until("d")
            self.play(FadeIn(gl), FadeIn(gen))
        self.wait(0.3)
        self.clear_scene()

    # ------------------------------------------------------------------
    def stars(self):
        head = label(r"Stars and bars", font_size=38).to_edge(UP, buff=0.35)
        q = label(r"$10$ identical cookies \ shared among $4$ children: \ how many ways?", font_size=30,
                  color=GREY_A).next_to(head, DOWN, buff=0.4)
        seqs = ["***|**||*****", "|****|***|***", "**********|||"]
        rows = VGroup()
        for sq in seqs:
            r = VGroup()
            for ch in sq:
                if ch == "*":
                    r.add(Star(5, outer_radius=0.2, stroke_width=0, fill_color=HEAD, fill_opacity=1))
                else:
                    r.add(Line(UP * 0.3, DOWN * 0.3, color=CTRL, stroke_width=5))
            r.arrange(RIGHT, buff=0.16)
            counts = [len(p) for p in sq.split("|")]
            tag = MathTex(r"(" + ", ".join(map(str, counts)) + ")", font_size=32, color=DATA).next_to(r, RIGHT, buff=0.6)
            rows.add(VGroup(r, tag))
        rows.arrange(DOWN, buff=0.5, aligned_edge=LEFT).next_to(q, DOWN, buff=0.5)
        ans = MathTex(r"\binom{10 + 3}{3} = \binom{13}{3} = 286", font_size=44, color=YES).next_to(rows, DOWN, buff=0.6)
        expl = note(r"13 positions; \ choose which 3 hold the bars", font_size=24).next_to(ans, DOWN, buff=0.2)
        with self.voiceover(
            "One more bijection, because it is so neat. Share ten identical cookies among four children: how many ways? "
            "<bookmark mark='a'/> Write the cookies as stars, and put three bars between them to mark where one child's "
            "share ends and the next begins. Three, two, none, five. <bookmark mark='b'/> Every sharing is a row of "
            "thirteen symbols with exactly three bars, and every such row is a sharing. <bookmark mark='c'/> So count "
            "the rows instead: choose which three of the thirteen positions hold bars. Thirteen choose three, two "
            "hundred and eighty-six. Turning one counting problem into another that is easier is what a bijection is "
            "for."
        ) as vo:
            self.play(FadeIn(head), FadeIn(q))
            vo.wait_until("a")
            self.play(FadeIn(rows[0], lag_ratio=0.05))
            vo.wait_until("b")
            self.play(FadeIn(rows[1], lag_ratio=0.05), FadeIn(rows[2], lag_ratio=0.05))
            vo.wait_until("c")
            self.play(Write(ans), FadeIn(expl))
        self.wait(0.3)
        self.clear_scene()

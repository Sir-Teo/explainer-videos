from __future__ import annotations

import numpy as np

from explainer.cs import *  # noqa: F403
from videos.cs.cs2.common import CODE, COST, CTRL, DATA, HEAD, HIST, LIMIT, NO, PART, YES, fmt, load


def odd_dots(n_pairs: int, color, r=0.15, gap=0.46) -> VGroup:
    """2 n + 1 dots: n columns of two, and one left over on top."""
    g = VGroup()
    for k in range(n_pairs):
        g.add(Dot([k * gap, 0, 0], radius=r, color=color), Dot([k * gap, -gap, 0], radius=r, color=color))
    g.extra = Dot([n_pairs * gap, 0, 0], radius=r, color=HEAD)
    g.add(g.extra)
    return g


class Proofs(VoiceoverScene):
    def construct(self):
        self.card()
        self.direct()
        self.contrapositive()
        self.sqrt2()
        self.primes()
        self.cases()
        self.nonconstructive()

    def card(self):
        card = chapter_card(2, r"Ways to prove", r"What counts as a proof?", part=PART)
        with self.voiceover("Chapter two. Ways to prove."):
            self.play(FadeIn(card[0], shift=UP * 0.2), FadeIn(card[1]), FadeIn(card[2]))
        self.play(FadeOut(card))

    # ------------------------------------------------------------------
    def direct(self):
        head = label(r"Direct proof: \ the sum of two odd numbers is even", font_size=36).to_edge(UP, buff=0.4)
        a = odd_dots(3, DATA).move_to(LEFT * 3.6 + UP * 0.6)
        b = odd_dots(4, CTRL).move_to(RIGHT * 0.2 + UP * 0.6)
        la = MathTex(r"7 = 2 \cdot 3 + 1", font_size=34, color=DATA).next_to(a, DOWN, buff=0.4)
        lb = MathTex(r"9 = 2 \cdot 4 + 1", font_size=34, color=CTRL).next_to(b, DOWN, buff=0.4)
        alg = MathTex(r"(2a + 1) + (2b + 1)", r"= 2a + 2b + 2", r"= 2(a + b + 1)", font_size=42).to_edge(DOWN, buff=1.2)
        alg[2].set_color(YES)
        defn = note(r"odd: \ $n = 2k + 1$ \ for some integer $k$; \ \ even: \ $n = 2k$", font_size=24).to_edge(
            DOWN, buff=0.4)
        with self.voiceover(
            "A proof is an argument that leaves no case out. The simplest kind is direct: start from what you are "
            "given, and walk to what you want. <bookmark mark='a'/> Claim: the sum of two odd numbers is even. An odd "
            "number is pairs, plus one left over. <bookmark mark='b'/> Put two of them together, and the two leftovers "
            "make one more pair. <bookmark mark='c'/> In symbols, with the definitions written out: two a plus one, plus "
            "two b plus one, is two times a plus b plus one, which is even. Notice that the proof starts by writing "
            "down exactly what odd means. Most proofs that go wrong go wrong there."
        ) as vo:
            self.play(FadeIn(head))
            vo.wait_until("a")
            self.play(FadeIn(a), FadeIn(b), FadeIn(la), FadeIn(lb))
            vo.wait_until("b")
            self.play(FadeOut(la), FadeOut(lb), run_time=0.4)
            tgt = b.extra.get_center() + DOWN * 0.46
            self.play(a.extra.animate.move_to(tgt).set_color(YES), b.extra.animate.set_color(YES),
                      run_time=1.0)
            vo.wait_until("c")
            self.play(Write(alg), FadeIn(defn))
        self.wait(0.3)
        self.clear_scene()

    # ------------------------------------------------------------------
    def contrapositive(self):
        head = label(r"By contrapositive", font_size=38).to_edge(UP, buff=0.4)
        claim = label(r"if $n^2$ is even, \ then $n$ is even", font_size=34, color=DATA).next_to(head, DOWN, buff=0.5)
        hard = note(r"directly: \ from ``$n^2 = 2k$'' \ nothing obvious follows about $n$", font_size=24).next_to(
            claim, DOWN, buff=0.25)
        flip = label(r"equivalently: \ if $n$ is odd, \ then $n^2$ is odd", font_size=34, color=YES).next_to(
            hard, DOWN, buff=0.6)
        alg = MathTex(r"n = 2k + 1 \ \Rightarrow\ n^2 = 4k^2 + 4k + 1 = 2(2k^2 + 2k) + 1", font_size=40).next_to(
            flip, DOWN, buff=0.5)
        with self.voiceover(
            "Sometimes the direct road is blocked. <bookmark mark='a'/> Claim: if n squared is even, then n is even. "
            "Starting from n squared equals two k gives you nothing to hold. <bookmark mark='b'/> So prove the "
            "contrapositive, which chapter one showed says exactly the same thing: if n is odd, then n squared is odd. "
            "<bookmark mark='c'/> Now it is one line. Two k plus one, squared, is two times something, plus one. Odd."
        ) as vo:
            self.play(FadeIn(head))
            vo.wait_until("a")
            self.play(FadeIn(claim), FadeIn(hard))
            vo.wait_until("b")
            self.play(FadeIn(flip, shift=DOWN * 0.15))
            vo.wait_until("c")
            self.play(Write(alg))
        self.wait(0.3)
        self.clear_scene()

    # ------------------------------------------------------------------
    def sqrt2(self):
        head = label(r"By contradiction: \ $\sqrt 2$ is not a fraction", font_size=38).to_edge(UP, buff=0.35)
        steps = VGroup(*[MathTex(t, font_size=34, color=c) for t, c in (
            (r"\text{suppose } \sqrt 2 = p / q \text{ in lowest terms}", GREY_A),
            (r"p^2 = 2 q^2", DATA),
        )]).arrange(DOWN, aligned_edge=LEFT, buff=0.3).to_corner(UL, buff=0.5).shift(DOWN * 0.8)
        # Tennenbaum's picture: a square of side p holds two squares of side q (same total area)
        s = 3.6
        p_len, q_len = s, s / np.sqrt(2)
        o = np.array([1.2, -2.8, 0])
        big = Square(p_len, stroke_color=WHITE, stroke_width=2.5, fill_color=DATA, fill_opacity=0.15).move_to(
            o + np.array([p_len / 2, p_len / 2, 0]))
        q1 = Square(q_len, stroke_width=0, fill_color=CTRL, fill_opacity=0.45).move_to(
            o + np.array([q_len / 2, q_len / 2, 0]))
        q2 = Square(q_len, stroke_width=0, fill_color=CTRL, fill_opacity=0.45).move_to(
            o + np.array([p_len - q_len / 2, p_len - q_len / 2, 0]))
        ov = 2 * q_len - p_len
        mid = Square(ov, stroke_color=NO, stroke_width=3, fill_color=NO, fill_opacity=0.5).move_to(
            o + np.array([p_len / 2, p_len / 2, 0]))
        u = p_len - q_len
        c1 = Square(u, stroke_color=YES, stroke_width=3, fill_opacity=0).move_to(o + np.array([u / 2, p_len - u / 2, 0]))
        c2 = Square(u, stroke_color=YES, stroke_width=3, fill_opacity=0).move_to(o + np.array([p_len - u / 2, u / 2, 0]))
        lp = MathTex("p", font_size=34).next_to(big, DOWN, buff=0.12)
        lq = MathTex("q", font_size=30, color=CTRL).next_to(q1, LEFT, buff=0.12)
        expl = VGroup(*[label(t, font_size=27, color=c) for t, c in (
            (r"the overlap \ (red) \ must equal \\ the two uncovered corners \ (green)", GREY_A),
            (r"$(2q - p)^2 = 2 (p - q)^2$: \\ a smaller pair, \ also whole numbers", YES),
            (r"so no smallest pair, \\ so no pair at all", NO),
        )]).arrange(DOWN, aligned_edge=LEFT, buff=0.38).next_to(steps, DOWN, buff=0.5).align_to(steps, LEFT)
        alt = note(r"the parity proof: \ $p^2$ even $\Rightarrow$ $p$ even $\Rightarrow$ $q^2 = 2 r^2$ $\Rightarrow$ "
                   r"$q$ even: \ not lowest terms", font_size=21).to_edge(DOWN, buff=0.2).to_edge(LEFT, buff=0.4)
        tag = note(r"picture: \ Stanley Tennenbaum", font_size=20).next_to(big, UP, buff=0.12)
        with self.voiceover(
            "Proof by contradiction assumes the opposite of what you want, and derives something impossible. The "
            "classic: the square root of two is not a fraction. <bookmark mark='a'/> Suppose it were p over q, in "
            "lowest terms. Squaring, p squared is two q squared. <bookmark mark='b'/> Here is that equation as a "
            "picture. A square of side p has the same area as two squares of side q. <bookmark mark='c'/> Put the two "
            "smaller squares in opposite corners of the big one. They overlap in the middle, and they leave two corners "
            "uncovered. Since the areas match, the overlap has exactly the combined area of the two uncovered corners. "
            "<bookmark mark='d'/> But that is the same equation again, with smaller whole numbers: a square equal to "
            "two smaller squares. <bookmark mark='e'/> Repeat, and the numbers shrink forever, which whole numbers "
            "cannot do. So there was no p and q to begin with. The usual proof uses parity, the hook's tool, in the "
            "same way: it shows p and q are both even, so the fraction was not in lowest terms."
        ) as vo:
            self.play(FadeIn(head))
            vo.wait_until("a")
            self.play(FadeIn(steps, lag_ratio=0.4))
            vo.wait_until("b")
            self.play(DrawBorderThenFill(big), FadeIn(lp), FadeIn(tag))
            vo.wait_until("c")
            self.play(FadeIn(q1, shift=UP * 0.3 + RIGHT * 0.3), FadeIn(lq))
            self.play(FadeIn(q2, shift=DOWN * 0.3 + LEFT * 0.3))
            self.play(FadeIn(mid), Create(c1), Create(c2), FadeIn(expl[0]))
            vo.wait_until("d")
            self.play(FadeIn(expl[1]))
            self.play(Indicate(mid, color=NO), Indicate(VGroup(c1, c2), color=YES))
            vo.wait_until("e")
            self.play(FadeIn(expl[2]), FadeIn(alt))
        self.wait(0.3)
        self.clear_scene()

    # ------------------------------------------------------------------
    def primes(self):
        d = load("numbers")
        head = label(r"Euclid: \ there are infinitely many primes", font_size=38).to_edge(UP, buff=0.4)
        steps = VGroup(*[label(t, font_size=30, color=c) for t, c in (
            (r"suppose the primes were only $p_1, p_2, \dots, p_k$", GREY_A),
            (r"let $N = p_1 p_2 \cdots p_k + 1$", DATA),
            (r"each $p_i$ leaves remainder $1$ when it divides $N$", CTRL),
            (r"but $N > 1$ has a prime factor: \ not on the list", NO),
        )]).arrange(DOWN, aligned_edge=LEFT, buff=0.32).next_to(head, DOWN, buff=0.5).to_edge(LEFT, buff=0.7)
        rows = VGroup()
        for e in d["euclid_numbers"]:
            prod = r" \cdot ".join(str(p) for p in e["primes"])
            fac = r" \cdot ".join(str(f) for f in e["factors"])
            col = YES if len(e["factors"]) == 1 else HEAD
            rows.add(MathTex(rf"{prod} + 1 = {fmt(e['value'])}" + ("" if len(e["factors"]) == 1 else rf" = {fac}"),
                             font_size=30, color=col))
        rows.arrange(DOWN, aligned_edge=LEFT, buff=0.16).next_to(steps, DOWN, buff=0.5).align_to(steps, LEFT)
        warn = label(r"$N$ need not be prime: \ its factors are new primes", font_size=26, color=HEAD).next_to(
            rows, RIGHT, buff=0.5).align_to(rows, DOWN)
        tag = note(r"\textit{Elements}, Book IX, Proposition 20; \ computed", font_size=20).to_corner(DR, buff=0.25)
        with self.voiceover(
            "Another contradiction, perhaps the oldest proof still taught. Euclid: there are infinitely many primes. "
            "<bookmark mark='a'/> Suppose there were only finitely many. <bookmark mark='b'/> Multiply them all together "
            "and add one. <bookmark mark='c'/> Every prime on the list leaves remainder one when it divides that "
            "number, so none of them divides it. <bookmark mark='d'/> But every number bigger than one has some prime "
            "factor. That factor is a prime not on the list. Contradiction. <bookmark mark='e'/> A common misreading is "
            "that the new number is itself prime. Computing them: two plus one, three; up to two times three times "
            "five times seven times eleven, plus one: all prime. But the next one, thirty thousand and thirty-one, is "
            "fifty-nine times five hundred and nine: two new primes, exactly as the proof promised. The one after "
            "that is a product of three."
        ) as vo:
            self.play(FadeIn(head))
            for mk, s_ in zip("abcd", steps):
                vo.wait_until(mk)
                self.play(FadeIn(s_, shift=RIGHT * 0.15))
            vo.wait_until("e")
            self.play(LaggedStart(*[FadeIn(r) for r in rows], lag_ratio=0.3), run_time=2.4)
            self.play(FadeIn(warn), FadeIn(tag))
        self.wait(0.3)
        self.clear_scene()

    # ------------------------------------------------------------------
    def cases(self):
        head = label(r"By cases: \ $n^2 + n$ is always even", font_size=38).to_edge(UP, buff=0.4)
        fact = MathTex(r"n^2 + n = n\,(n + 1)", font_size=44).next_to(head, DOWN, buff=0.5)
        left = VGroup(label(r"$n$ even", font_size=30, color=DATA),
                      MathTex(r"n = 2k:\quad n(n+1) = 2\,k(n+1)", font_size=34)).arrange(DOWN, buff=0.25)
        right = VGroup(label(r"$n$ odd", font_size=30, color=CTRL),
                       MathTex(r"n + 1 = 2k:\quad n(n+1) = 2\,nk", font_size=34)).arrange(DOWN, buff=0.25)
        VGroup(left, right).arrange(RIGHT, buff=1.4).next_to(fact, DOWN, buff=0.8)
        both = label(r"every integer is one or the other: \ even, \ in every case", font_size=30, color=YES).next_to(
            VGroup(left, right), DOWN, buff=0.7)
        with self.voiceover(
            "Proof by cases splits the world into pieces that together cover everything, and proves the claim in each. "
            "<bookmark mark='a'/> Claim: n squared plus n is always even. It is n times n plus one. <bookmark mark='b'/> "
            "If n is even, the first factor is even. If n is odd, the second is. <bookmark mark='c'/> Every integer is "
            "one or the other, so the claim holds for all of them. The danger in this method is a missing case. A "
            "compiler's exhaustiveness check, which Part 14 builds, is a machine that looks for exactly that mistake."
        ) as vo:
            self.play(FadeIn(head))
            vo.wait_until("a")
            self.play(Write(fact))
            vo.wait_until("b")
            self.play(FadeIn(left, shift=UP * 0.15), FadeIn(right, shift=UP * 0.15))
            vo.wait_until("c")
            self.play(FadeIn(both))
        self.wait(0.3)
        self.clear_scene()

    # ------------------------------------------------------------------
    def nonconstructive(self):
        head = label(r"A proof that does not say which", font_size=38).to_edge(UP, buff=0.4)
        claim = label(r"there are irrational $a, b$ \ with $a^b$ rational", font_size=32, color=DATA).next_to(
            head, DOWN, buff=0.45)
        x = MathTex(r"x = \sqrt2^{\sqrt2}", font_size=44, color=HEAD).next_to(claim, DOWN, buff=0.5)
        c1 = VGroup(label(r"if $x$ is rational:", font_size=28, color=GREY_A),
                    MathTex(r"a = b = \sqrt 2", font_size=36, color=YES)).arrange(DOWN, buff=0.2)
        c2 = VGroup(label(r"if $x$ is irrational:", font_size=28, color=GREY_A),
                    MathTex(r"x^{\sqrt2} = \sqrt2^{\sqrt2 \cdot \sqrt2} = \sqrt2^{\,2} = 2", font_size=36,
                            color=YES)).arrange(DOWN, buff=0.2)
        VGroup(c1, c2).arrange(RIGHT, buff=1.4).next_to(x, DOWN, buff=0.6)
        which = label(r"either way the claim holds, \ and the proof never says which", font_size=28,
                      color=HEAD).next_to(VGroup(c1, c2), DOWN, buff=0.55)
        later = note(r"(the second: \ $x$ is irrational, \ by the Gelfond--Schneider theorem, 1934)", font_size=22)
        later.next_to(which, DOWN, buff=0.2)
        cs = label(r"a constructive proof is an algorithm \ (Part 14)", font_size=28, color=CODE).to_edge(DOWN, buff=0.4)
        with self.voiceover(
            "One more kind, and it matters for computer science. <bookmark mark='a'/> Claim: there are irrational "
            "numbers a and b with a to the b rational. <bookmark mark='b'/> Look at root two to the power root two. "
            "<bookmark mark='c'/> If it is rational, we are done, with a and b both root two. If it is irrational, raise "
            "it to the power root two: the exponents multiply to two, and the answer is two, which is rational. "
            "<bookmark mark='d'/> Either way the claim is true, and the proof never tells us which case we are in. "
            "It took another theorem, in 1934, to settle that it is the second. <bookmark mark='e'/> A proof like this "
            "is non-constructive: it proves something exists without producing it. A constructive proof hands you the "
            "object, and so it is, in effect, a program. In Part 14 that observation becomes exact: proofs are programs, "
            "and the propositions they prove are types."
        ) as vo:
            self.play(FadeIn(head))
            vo.wait_until("a")
            self.play(FadeIn(claim))
            vo.wait_until("b")
            self.play(Write(x))
            vo.wait_until("c")
            self.play(FadeIn(c1, shift=UP * 0.15))
            self.play(FadeIn(c2, shift=UP * 0.15))
            vo.wait_until("d")
            self.play(FadeIn(which), FadeIn(later))
            vo.wait_until("e")
            self.play(FadeIn(cs))
        self.wait(0.3)
        self.clear_scene()

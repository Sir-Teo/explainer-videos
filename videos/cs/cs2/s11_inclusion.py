from __future__ import annotations

import math

import numpy as np

from explainer.cs import *  # noqa: F403
from videos.cs.cs2.common import COST, CTRL, DATA, FUNC, HEAD, INF, NO, PART, YES, fmt, load


class Inclusion(VoiceoverScene):
    def construct(self):
        self.card()
        self.venn()
        self.hats()
        self.limit()
        self.phi()

    def card(self):
        card = chapter_card(10, r"Inclusion and exclusion", r"How do you count a union without counting twice?",
                            part=PART)
        with self.voiceover("Chapter ten. Inclusion and exclusion."):
            self.play(FadeIn(card[0], shift=UP * 0.2), FadeIn(card[1]), FadeIn(card[2]))
        self.play(FadeOut(card))

    # ------------------------------------------------------------------
    def venn(self):
        head = label(r"Counting a union", font_size=38).to_edge(UP, buff=0.35)
        r = 1.45
        cA = Circle(r, stroke_color=DATA, stroke_width=3, fill_color=DATA, fill_opacity=0.18).move_to(
            LEFT * 3.6 + UP * 0.55)
        cB = Circle(r, stroke_color=CTRL, stroke_width=3, fill_color=CTRL, fill_opacity=0.18).move_to(
            LEFT * 1.9 + UP * 0.55)
        cC = Circle(r, stroke_color=FUNC, stroke_width=3, fill_color=FUNC, fill_opacity=0.18).move_to(
            LEFT * 2.75 + DOWN * 0.9)
        la = MathTex(r"A: 2 \mid x", font_size=28, color=DATA).next_to(cA, UL, buff=-0.25)
        lb = MathTex(r"B: 3 \mid x", font_size=28, color=CTRL).next_to(cB, UR, buff=-0.25)
        lc = MathTex(r"C: 5 \mid x", font_size=28, color=FUNC).next_to(cC, DOWN, buff=0.1)
        two = MathTex(r"|A \cup B| = |A| + |B| - |A \cap B|", font_size=36).move_to(RIGHT * 3.3 + UP * 1.9)
        three = MathTex(r"|A \cup B \cup C| = |A| + |B| + |C|", r"- |A\cap B| - |A \cap C| - |B \cap C|",
                        r"+ |A \cap B \cap C|", font_size=32).arrange(DOWN, aligned_edge=LEFT, buff=0.15)
        three.next_to(two, DOWN, buff=0.5)
        three[0].set_color(YES)
        three[1].set_color(NO)
        three[2].set_color(YES)
        num = MathTex(r"50 + 33 + 20 - 16 - 10 - 6 + 3 = 74", font_size=36, color=HEAD).next_to(three, DOWN, buff=0.5)
        q = label(r"how many of $1, \dots, 100$ \\ are divisible by $2$, $3$ or $5$?", font_size=26, color=GREY_A)
        q.next_to(num, DOWN, buff=0.35)
        chk = note(r"checked by listing: \ 74", font_size=22).next_to(q, DOWN, buff=0.15)
        with self.voiceover(
            "To count the elements in either of two sets, add their sizes. But the elements in both were counted "
            "twice, so subtract the overlap once. <bookmark mark='a'/> With three sets, add the three sizes, subtract "
            "the three pairwise overlaps, and then the very middle, which was added three times and subtracted three "
            "times, must be added back. <bookmark mark='b'/> Example: how many numbers from one to a hundred are "
            "divisible by two, three or five? Fifty, plus thirty-three, plus twenty; minus sixteen, ten and six for "
            "the multiples of six, ten and fifteen; plus three for the multiples of thirty. Seventy-four. "
            "<bookmark mark='c'/> The pattern continues for any number of sets, with alternating signs: inclusion, "
            "exclusion, inclusion."
        ) as vo:
            self.play(FadeIn(head), DrawBorderThenFill(cA), DrawBorderThenFill(cB), FadeIn(la), FadeIn(lb))
            self.play(Write(two))
            vo.wait_until("a")
            self.play(DrawBorderThenFill(cC), FadeIn(lc), FadeIn(three, lag_ratio=0.3))
            vo.wait_until("b")
            self.play(FadeIn(q), Write(num))
            self.play(FadeIn(chk))
        self.wait(0.3)
        self.clear_scene()

    # ------------------------------------------------------------------
    def hats(self):
        d = load("derange")
        head = label(r"The hat-check problem", font_size=38).to_edge(UP, buff=0.35)
        q = label(r"$n$ hats are handed back at random: \ what is the chance that \textit{nobody} gets their own?",
                  font_size=28, color=GREY_A).next_to(head, DOWN, buff=0.35)
        f = MathTex(r"D_n = \sum_{k=0}^{n} (-1)^k \binom{n}{k} (n - k)!", font_size=40, color=CTRL).next_to(
            q, DOWN, buff=0.45)
        expl = note(r"$\binom{n}{k}(n-k)!$: \ orders in which a chosen $k$ people \textit{do} get their own hats",
                    font_size=22).next_to(f, DOWN, buff=0.15)
        t = d["terms4"]
        four = MathTex(rf"D_4 = {t[0]} - {t[1]} + {t[2]} - {t[3]} + {t[4]} = {d['D'][4]}", font_size=40,
                       color=HEAD).next_to(expl, DOWN, buff=0.45)
        perms = [p for p in __import__("itertools").permutations(range(4)) if all(p[i] != i for i in range(4))]
        chips = VGroup(*[Text("".join("ABCD"[i] for i in p), font="DejaVu Sans Mono", font_size=24, color=YES)
                         for p in perms]).arrange_in_grid(rows=1, buff=0.35).next_to(four, DOWN, buff=0.4)
        cl = note(r"the 9 ways for 4 people: \ person $i$ gets hat \texttt{ABCD}$[\,\cdot\,]$, never their own",
                  font_size=22).next_to(chips, DOWN, buff=0.15)
        with self.voiceover(
            "Now a classic that inclusion-exclusion answers exactly. <bookmark mark='a'/> n people check their hats, "
            "and the hats are handed back at random. What is the chance that nobody gets their own? An arrangement with "
            "no fixed points is called a derangement. <bookmark mark='b'/> Count the bad orders instead, with "
            "inclusion-exclusion over the people who do get their own hat. Fix any k people: the other hats can go "
            "anywhere, n minus k factorial ways. Alternate the signs over k, and what remains is the derangements. "
            "<bookmark mark='c'/> For four people: twenty-four, minus twenty-four, plus twelve, minus four, plus one. "
            "Nine. <bookmark mark='d'/> Here they are, listed, checked by brute force."
        ) as vo:
            self.play(FadeIn(head))
            vo.wait_until("a")
            self.play(FadeIn(q))
            vo.wait_until("b")
            self.play(Write(f), FadeIn(expl))
            vo.wait_until("c")
            self.play(Write(four))
            vo.wait_until("d")
            self.play(LaggedStart(*[FadeIn(c) for c in chips], lag_ratio=0.1), FadeIn(cl))
        self.wait(0.3)
        self.clear_scene()

    # ------------------------------------------------------------------
    def limit(self):
        d = load("derange")
        ratio = d["ratio"]
        head = label(r"The chance tends to $1/e$", font_size=38).to_edge(UP, buff=0.35)
        ax = Axes(x_range=[0, 12, 1], y_range=[0, 1, 0.25], x_length=6.4, y_length=4.0, tips=False,
                  axis_config={"color": GREY_C, "font_size": 20},
                  x_axis_config={"numbers_to_include": list(range(1, 13))},
                  y_axis_config={"numbers_to_include": [0.25, 0.5, 0.75, 1.0]}).move_to(LEFT * 2.8 + DOWN * 0.4)
        e_line = DashedLine(ax.c2p(0, d["e_inv"]), ax.c2p(12, d["e_inv"]), color=HEAD, stroke_width=2)
        el = MathTex(r"1/e = 0.3679\ldots", font_size=28, color=HEAD).next_to(ax.c2p(8, d["e_inv"]), UP, buff=0.2)
        pts = [ax.c2p(n, ratio[n]) for n in range(1, 13)]
        path = VMobject(color=CTRL, stroke_width=3).set_points_as_corners(pts)
        dots = VGroup(*[Dot(p, radius=0.06, color=CTRL) for p in pts])
        xl = note(r"$n$ people", font_size=22).next_to(ax, DOWN, buff=0.15)
        yl = note(r"$D_n / n!$", font_size=22).next_to(ax, LEFT, buff=0.1).shift(UP * 1.8)
        sims = d["sims"]
        rows = VGroup(*[label(rf"$n = {s['n']}$: \ nobody $= {s['none']:.3f}$, \ mean fixed $= {s['mean']:.3f}$",
                              font_size=24, color=GREY_A) for s in sims]).arrange(DOWN, aligned_edge=LEFT, buff=0.22)
        rows.move_to(RIGHT * 3.6 + UP * 0.9)
        rl = note(rf"simulated: \ ${fmt(sims[0]['trials'])}$ shuffles each \ (${fmt(sims[-1]['trials'])}$ for "
                  rf"$n = {sims[-1]['n']}$)", font_size=20).next_to(rows, UP, buff=0.2)
        series = MathTex(r"\frac{D_n}{n!} = 1 - 1 + \frac{1}{2!} - \frac{1}{3!} + \cdots \to e^{-1}", font_size=32,
                         color=CTRL).move_to(RIGHT * 3.7 + DOWN * 0.9)
        bon = note(r"stopping after any term over- or under-shoots, \\ alternately \ (Bonferroni)", font_size=22).next_to(
            series, DOWN, buff=0.25)
        with self.voiceover(
            "Divide by n factorial to get the probability. <bookmark mark='a'/> One person: zero. Two: one half. Three: "
            "one third. Then it settles almost at once, at thirty-six point eight percent, and stays there: with ten "
            "people or ten thousand, the chance that nobody gets their own hat is the same. <bookmark mark='b'/> The "
            "formula is the series for e to the minus one, cut off after n terms. <bookmark mark='c'/> And a simulation "
            "agrees: shuffle a hundred thousand times, and about thirty-six point eight percent of shuffles have no "
            "fixed point, for ten people, for a deck of fifty-two, or for a thousand; with three it is exactly one "
            "third. <bookmark mark='d'/> Notice also that stopping "
            "the alternating sum early always overshoots or undershoots, by turns. Those Bonferroni bounds are how "
            "inclusion-exclusion is used when the full sum is too big to compute."
        ) as vo:
            self.play(FadeIn(head), Create(ax), FadeIn(xl), FadeIn(yl))
            vo.wait_until("a")
            self.play(Create(path), LaggedStart(*[FadeIn(dd) for dd in dots], lag_ratio=0.1), run_time=2.0)
            self.play(Create(e_line), FadeIn(el))
            vo.wait_until("b")
            self.play(Write(series))
            vo.wait_until("c")
            self.play(FadeIn(rl), LaggedStart(*[FadeIn(r) for r in rows], lag_ratio=0.3))
            vo.wait_until("d")
            self.play(FadeIn(bon))
        self.wait(0.3)
        self.clear_scene()

    # ------------------------------------------------------------------
    def phi(self):
        d = load("derange")
        phis = d["phi"]
        head = label(r"Euler's $\varphi$: \ the numbers that share no factor with $n$", font_size=36).to_edge(UP,
                                                                                                      buff=0.35)
        f = MathTex(r"\varphi(n) = n \prod_{p \mid n} \left(1 - \frac1p\right)", font_size=40, color=FUNC).next_to(
            head, DOWN, buff=0.35)
        ex = MathTex(r"\varphi(60) = 60 \cdot \tfrac12 \cdot \tfrac23 \cdot \tfrac45 = 16", font_size=36,
                     color=HEAD).next_to(f, DOWN, buff=0.3)
        ax = Axes(x_range=[0, 61, 10], y_range=[0, 60, 20], x_length=10.5, y_length=3.0, tips=False,
                  axis_config={"color": GREY_C, "font_size": 18},
                  x_axis_config={"numbers_to_include": list(range(10, 61, 10))},
                  y_axis_config={"numbers_to_include": [20, 40, 60]}).to_edge(DOWN, buff=0.7)
        bars = VGroup()
        for n, v in enumerate(phis, 1):
            prime = v == n - 1
            bars.add(Rectangle(width=ax.x_length / 61 * 0.75, height=max(ax.y_length * v / 60, 0.01), stroke_width=0,
                               fill_color=YES if prime else (HEAD if n == 60 else DATA),
                               fill_opacity=0.9).move_to(ax.c2p(n, 0), aligned_edge=DOWN))
        xl = note(r"$\varphi(n)$ for $n \le 60$, \ computed by inclusion--exclusion over the prime factors \ "
                  r"(green: \ primes, \ $\varphi(p) = p - 1$)", font_size=20).next_to(ax, DOWN, buff=0.12)
        rsa = label(r"Part 30: \ RSA works because $a^{\varphi(n)} \equiv 1 \pmod n$", font_size=26,
                    color=CTRL).next_to(ex, DOWN, buff=0.3)
        with self.voiceover(
            "Inclusion-exclusion also counts the numbers that share no factor with n. Remove the multiples of each "
            "prime that divides n, add back what was removed twice, and so on. <bookmark mark='a'/> The result factors "
            "into a product: n times one minus one over p, for each prime p dividing n. This is Euler's phi function. "
            "<bookmark mark='b'/> For sixty: sixty, times a half, times two thirds, times four fifths: sixteen. "
            "<bookmark mark='c'/> Here it is for every n up to sixty. The primes stand tallest, one less than "
            "themselves; numbers with many small factors sit low. <bookmark mark='d'/> Phi is the hidden engine of RSA "
            "encryption, which Part 30 builds."
        ) as vo:
            self.play(FadeIn(head))
            vo.wait_until("a")
            self.play(Write(f))
            vo.wait_until("b")
            self.play(Write(ex))
            vo.wait_until("c")
            self.play(Create(ax), LaggedStart(*[GrowFromEdge(b, DOWN) for b in bars], lag_ratio=0.02), FadeIn(xl),
                      run_time=2.6)
            vo.wait_until("d")
            self.play(FadeIn(rsa))
        self.wait(0.3)
        self.clear_scene()

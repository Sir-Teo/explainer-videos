from __future__ import annotations

import numpy as np

from explainer.cs import *  # noqa: F403
from videos.cs.cs16.common import (CODE, COST, CTRL, DATA, FUNC, HEAD, LAM, NO, PART, YES, grid_table, load, mono)


def level_bars(levels, color, W=3.2, H=0.24, gap=0.06, maxv=None):
    """Each level's total cost as a horizontal bar: the geometry of the three cases."""
    mx = maxv or max(levels)
    g = VGroup()
    for k, v in enumerate(levels):
        w = max(W * v / mx, 0.03)
        g.add(Rectangle(width=w, height=H, stroke_width=0, fill_color=color, fill_opacity=0.85).move_to(
            [w / 2, -k * (H + gap), 0]))
    return g


class Master(VoiceoverScene):
    def construct(self):
        self.card()
        self.theorem()
        self.geometry()
        self.proof()
        self.examples()

    def card(self):
        card = chapter_card(5, r"The master theorem", r"Can one rule solve every divide-and-conquer?", lit=(1980,),
                            extra=((1980, r"Bentley, Haken and Saxe"),), part=PART)
        with self.voiceover("Chapter five. The master theorem."):
            self.play(FadeIn(card[0], shift=UP * 0.2), FadeIn(card[1]), FadeIn(card[2]))
        self.play(FadeOut(card))

    def theorem(self):
        head = label(r"$T(n) = a\,T(n/b) + f(n)$", font_size=36).to_edge(UP, buff=0.3)
        crit = MathTex(r"\text{compare } f(n) \text{ with } n^{\log_b a} \text{, the number of leaves}",
                       font_size=30, color=GREY_A).next_to(head, DOWN, buff=0.45)
        cases = VGroup(
            VGroup(label(r"\textbf{1.} \ $f(n) = O(n^{\log_b a - \varepsilon})$", font_size=24, color=NO),
                   MathTex(r"T(n) = \Theta(n^{\log_b a})", font_size=28, color=NO),
                   label(r"the leaves dominate", font_size=20, color=GREY_B)).arrange(DOWN, buff=0.1),
            VGroup(label(r"\textbf{2.} \ $f(n) = \Theta(n^{\log_b a})$", font_size=24, color=YES),
                   MathTex(r"T(n) = \Theta(n^{\log_b a} \log n)", font_size=28, color=YES),
                   label(r"every level the same", font_size=20, color=GREY_B)).arrange(DOWN, buff=0.1),
            VGroup(label(r"\textbf{3.} \ $f(n) = \Omega(n^{\log_b a + \varepsilon})$", font_size=24, color=CTRL),
                   MathTex(r"T(n) = \Theta(f(n))", font_size=28, color=CTRL),
                   label(r"the root dominates \ (if $a f(n/b) \le c f(n)$, $c < 1$)", font_size=20,
                         color=GREY_B)).arrange(DOWN, buff=0.1),
        ).arrange(RIGHT, buff=0.6).next_to(crit, DOWN, buff=0.6)
        if cases.width > 13.2:
            cases.scale_to_fit_width(13.2)
        note = label(r"$a\ge1$, $b>1$; positive constant base, nonnegative toll; case 3 needs the shown regularity", font_size=19,
                     color=GREY_B).to_edge(DOWN, buff=0.5)
        with self.voiceover(
            "Most divide-and-conquer algorithms split a problem of size n into a pieces of size n over b, and spend "
            "f of n splitting and combining. <bookmark mark='a'/> The recursion tree has n to the log base b of a "
            "leaves, and everything depends on how f compares with that number. <bookmark mark='b'/> If f grows "
            "polynomially slower, the leaves dominate and T is Theta of the number of leaves. <bookmark mark='c'/> "
            "If f matches it, every level costs the same, and T picks up a log factor: that was merge sort. "
            "<bookmark mark='d'/> If f grows polynomially faster, and shrinks geometrically down the tree, the root "
            "dominates and T is just Theta of f. Bentley, Haken and Saxe gave the general form in 1980."
        ) as vo:
            self.play(FadeIn(head))
            vo.wait_until("a")
            self.play(FadeIn(crit))
            for mk, c in zip("bcd", cases):
                vo.wait_until(mk)
                self.play(FadeIn(c, shift=UP * 0.1))
            self.play(FadeIn(note))
        self.wait(0.3)
        self.clear_scene()

    def geometry(self):
        d = load("master")
        head = label(r"The three shapes", font_size=34).to_edge(UP, buff=0.3)
        pick = {c["name"]: c for c in d["cases"]}
        trio = [("Karatsuba", NO, r"$3T(n/2) + n$: \ levels grow by $3/2$"),
                ("merge sort", YES, r"$2T(n/2) + n$: \ levels equal"),
                ("a heavy combine", CTRL, r"$2T(n/2) + n^2$: \ levels shrink by $1/2$")]
        cols = VGroup()
        for name, col, cap in trio:
            lv = pick[name]["levels"][:9]
            bars = level_bars(lv, col)
            t = label(cap, font_size=19, color=col)
            s = MathTex(pick[name]["sol"], font_size=26, color=col)
            cols.add(VGroup(t, bars, s).arrange(DOWN, buff=0.3))
        cols.arrange(RIGHT, buff=0.7, aligned_edge=UP).next_to(head, DOWN, buff=0.5)
        if cols.width > 13:
            cols.scale_to_fit_width(13)
        note = label(r"first nine levels shown, root at top; total work per level, $n=1024$", font_size=19,
                     color=GREY_B).to_edge(DOWN, buff=0.45)
        with self.voiceover(
            "Here are the three cases as pictures. Each bar is the total work of one level of the recursion tree, "
            "root at the top. <bookmark mark='a'/> Karatsuba's multiplication, three half-size products and linear "
            "work: each level costs one and a half times the one above. The sum is dominated by the bottom, the "
            "leaves, and the answer is n to the log base two of three, about n to the one point five eight. "
            "<bookmark mark='b'/> Merge sort: every level the same, so the sum is a level times the number of "
            "levels. <bookmark mark='c'/> And a combine step that costs n squared: each level is half the one "
            "above, a geometric series, so the root's n squared is the whole answer, up to a factor of two."
        ) as vo:
            self.play(FadeIn(head), FadeIn(note), FadeIn(cols[0]))
            vo.wait_until("a")
            self.play(Indicate(cols[0], color=NO))
            for mk, c in zip("bc", cols[1:]):
                vo.wait_until(mk)
                self.play(FadeIn(c[0]), LaggedStart(*[GrowFromEdge(b, LEFT) for b in c[1]], lag_ratio=0.1),
                          FadeIn(c[2]), run_time=2)
        self.wait(0.3)
        self.clear_scene()

    def proof(self):
        head = label(r"Why the three cases", font_size=34).to_edge(UP, buff=0.3)
        steps = VGroup(
            MathTex(r"n=b^h:\quad T(n)=a^hT(1)+\sum_{j=0}^{h-1}a^j f\!\left(\frac n{b^j}\right)", font_size=36),
            label(r"level $j$ has $a^j$ subproblems of size $n/b^j$", font_size=21, color=GREY_B),
            label(r"if $f(n) = n^c$, \ level $j$ costs $n^c \left(a / b^c\right)^j$: \ a geometric series with "
                  r"ratio $r = a / b^c$", font_size=22, color=GREY_A),
            VGroup(label(r"$r > 1$: \ the last term wins, \ the leaves", font_size=22, color=NO),
                   label(r"$r = 1$: \ $\log_b n$ equal terms", font_size=22, color=YES),
                   label(r"$r < 1$: \ the first term wins, \ the root", font_size=22, color=CTRL)).arrange(
                DOWN, aligned_edge=LEFT, buff=0.12),
            label(r"$r > 1 \iff c < \log_b a$: \ the theorem's comparison, \ in disguise", font_size=22,
                  color=HEAD),
        ).arrange(DOWN, buff=0.25).next_to(head, DOWN, buff=0.45)
        with self.voiceover(
            (
            "The geometry comes from a geometric series. <bookmark mark='a'/> Let n equal b to the h and retain "
            "the leaf term explicitly. Internal level j costs a to the j times f of n over b to the j; the leaves "
            "cost a to the h times the base cost. <bookmark mark='b'/> If f is n to the c, consecutive internal "
            "levels have ratio a over b to the c. <bookmark mark='c'/> A ratio above one favors the bottom, one "
            "gives equal levels, and a ratio below one favors the root. With positive constant base cost, the "
            "leaves have the same asymptotic scale as the bottom. <bookmark mark='d'/> The ratio exceeds one "
            "exactly when c is less than log base b of a. The theorem formalizes this picture, with its stated "
            "regularity conditions."
        )
        ) as vo:
            self.play(FadeIn(head))
            vo.wait_until("a")
            self.play(Write(steps[0]), FadeIn(steps[1]))
            vo.wait_until("b")
            self.play(FadeIn(steps[2]))
            vo.wait_until("c")
            self.play(FadeIn(steps[3]))
            vo.wait_until("d")
            self.play(FadeIn(steps[4]))
        self.wait(0.3)
        self.clear_scene()

    def examples(self):
        d = load("master")
        head = label(r"Five recurrences, \ one rule", font_size=34).to_edge(UP, buff=0.3)
        rows = [[c["name"], f"${c['rec']}$", str(c["case"]), f"${c['sol']}$"] for c in d["cases"]]
        tab = grid_table([r"algorithm", r"recurrence", r"case", r"solution"], rows, widths=[2.6, 4.0, 1.2, 4.0],
                         row_h=0.55, font_size=20, mono_cols=()).next_to(head, DOWN, buff=0.45)
        exponents = MathTex(rf"\log_2 3\approx{math.log2(3):.3f},\quad\log_2 7\approx{math.log2(7):.3f}",
                            font_size=23, color=GREY_B).next_to(tab, DOWN, buff=0.22)
        ab = d["akra_bazzi"]
        akra = VGroup(
            label(r"uneven splits: \ Akra--Bazzi \ (1998)", font_size=22, color=LAM),
            MathTex(r"T(n)=T(\lfloor n/3\rfloor)+T(n-\lfloor n/3\rfloor)+n", font_size=28),
            label(rf"$T(n)=n$ for $n\le2$; \ computed $T(n)/(n\lg n)$ \ = {ab[2]['ratio']:.3f}, \ {ab[4]['ratio']:.3f}, \ "
                  rf"{ab[5]['ratio']:.3f} \ at $10^3, 10^5, 10^6$: \ settling to a constant", font_size=20,
                  color=GREY_A),
        ).arrange(DOWN, buff=0.15).next_to(exponents, DOWN, buff=0.35)
        with self.voiceover(
            (
            "The table shows the standard three cases. <bookmark mark='a'/> Binary search and merge sort have "
            "matching per-level work. Karatsuba and Strassen are leaf dominated; a quadratic combine with two "
            "half-size calls is root dominated. <bookmark mark='b'/> For unequal splits, Akra and Bazzi provide a "
            "broader method. Our numeric illustration now has explicit integer semantics: for n at most two, T "
            "equals n; otherwise split into floor of n over three and the complementary size, and add n. These "
            "actual subproblem sizes are memoized separately. The displayed ratio to n log n is a finite "
            "numerical check of this example, alongside the asymptotic theorem."
        )
        ) as vo:
            self.play(FadeIn(head))
            vo.wait_until("a")
            self.play(FadeIn(tab), FadeIn(exponents))
            vo.wait_until("b")
            self.play(FadeIn(akra))
        self.wait(0.3)
        self.clear_scene()

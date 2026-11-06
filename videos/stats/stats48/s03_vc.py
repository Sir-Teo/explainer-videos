from __future__ import annotations

import numpy as np

from videos.stats.stats48.common import *  # noqa: F403


def point_panel(pts, labels, width=2.2, color_in=None, color_out=None):
    """Points in a small square, filled if labelled 1."""
    p = np.asarray(pts, float)
    p = (p - p.mean(axis=0)) / (np.ptp(p, axis=0).max() + 1e-9) * width
    box = Square(side_length=width * 1.5, stroke_color=GREY_D, stroke_width=1.5)
    dots = VGroup(*[Dot(np.array([x, y, 0.0]), radius=0.09, color=(color_in or CLASSC) if lab else (color_out or GREY_C))
                    for (x, y), lab in zip(p, labels)])
    return VGroup(box, dots)


class VC(VoiceoverScene):
    def construct(self):
        self.card()
        self.shatter()
        self.pictures()
        self.table()
        self.chart()
        self.covering()

    def card(self):
        card = chapter_card(2, r"VC classes", r"Counting the patterns a class can draw", lit=(1971,), part=PART)
        with self.voiceover("Chapter two. VC classes: counting the patterns a class can draw."):
            self.play(FadeIn(card[0], shift=UP * 0.2), FadeIn(card[1]))
        self.play(FadeOut(card))

    def shatter(self):
        rows = [
            cmath(r"\Pi_{\mathcal C}(n)", r"=", r"\max_{x_1, \dots, x_n} \#\{C \cap \{x_1, \dots, x_n\} : C \in \mathcal C\}", font_size=32),
            cmath(r"\mathcal C \text{ shatters } \{x_1..x_n\}", r":", r"\text{all } 2^n \text{ subsets are picked out}", font_size=32),
            cmath(r"\mathrm{VC}(\mathcal C)", r"=", r"\text{the largest } n \text{ that can be shattered}", font_size=34),
            cmath(r"\text{half-lines } 1, \ \text{intervals } 2", r",", r"\text{half-planes } 3, \ \text{rectangles } 4, \ \text{half-spaces in } \mathbb R^d: \ d + 1", font_size=28),
        ]
        rows[2][-1].set_color(CLASSC)
        whys = [why(r"the growth function"), why(r"every labelling possible"), why(r"Vapnik \& Chervonenkis (1971)"), why(r"examples")]
        with self.voiceover(
            "<bookmark mark='a'/> For a class of sets, count how many different subsets of n points it can pick out, and "
            "take the most over all configurations of the points. That is the growth function. <bookmark mark='b'/> If the "
            "class picks out all two to the n subsets, it shatters the points. <bookmark mark='c'/> The VC dimension, after "
            "Vladimir Vapnik and Alexey Chervonenkis in 1971, is the largest number of points the class can shatter. "
            "<bookmark mark='d'/> Half-lines have VC dimension one, intervals two, half-planes three, axis-parallel rectangles "
            "four, and half-spaces in d dimensions d plus one."
        ) as vo:
            step = ladder(self, rows, whys, keep=4, top=2.6, x=-0.9, buff=0.85, edge=6.9)
            for k, m_ in enumerate("abcd"):
                vo.wait_until(m_)
                step(k, transform=False)
        self.clear_scene()

    def pictures(self):
        d = load("vc")
        three = np.array([[0, 0], [1, 0], [0.4, 0.9]], float)
        labs3 = [[0, 0, 0], [1, 0, 0], [0, 1, 0], [0, 0, 1], [1, 1, 0], [1, 0, 1], [0, 1, 1], [1, 1, 1]]
        p3 = VGroup(*[point_panel(three, l, width=0.9) for l in labs3]).arrange_in_grid(2, 4, buff=0.25).scale(0.9).move_to([-3.3, 0.6, 0])
        four = np.array([[0, 0], [1, 0], [1, 1], [0, 1]], float)
        xor = point_panel(four, [1, 0, 1, 0], width=1.4).move_to([3.4, 0.9, 0])
        cross = VGroup(Line([2.4, 1.9, 0], [4.4, -0.1, 0], color=BADC, stroke_width=4), Line([2.4, -0.1, 0], [4.4, 1.9, 0], color=BADC, stroke_width=4))
        t3 = label(rf"3 points: \ all 8 labellings by half-planes \ ({d['three_hp']} counted)", font_size=24, color=GOODC).next_to(p3, DOWN, buff=0.3)
        t4 = label(rf"4 points: \ the diagonals cannot be split \ ({d['four_hp']} of 16)", font_size=24, color=BADC).next_to(xor, DOWN, buff=0.55)
        note_ = label(r"Radon: \ any 4 points in the plane split into two parts whose hulls meet", font_size=24, color=GREY_A).move_to([0, -2.6, 0])
        with self.voiceover(
            f"<bookmark mark='a'/> Here is why half-planes have dimension three. Three points in general position: every one "
            f"of the eight labellings, from none to all, is cut out by some half-plane. The brute-force count agrees: "
            f"{d['three_hp']}. <bookmark mark='b'/> But no four points can be shattered. For a square, the labelling that "
            f"takes opposite corners cannot be separated by a line, and brute force finds only {d['four_hp']} of the "
            f"sixteen patterns. <bookmark mark='c'/> In general Radon's theorem says any four points in the plane split into "
            f"two groups whose convex hulls intersect, and no half-plane can contain one group and miss the other."
        ) as vo:
            vo.wait_until("a")
            self.play(LaggedStart(*[FadeIn(m) for m in p3], lag_ratio=0.15), FadeIn(t3), run_time=2.5)
            vo.wait_until("b")
            self.play(FadeIn(xor), Create(cross), FadeIn(t4))
            vo.wait_until("c")
            self.play(FadeIn(note_))
        self.clear_scene()

    def table(self):
        d = load("vc")
        rows = [[r"$n$", r"half-lines", r"intervals", r"half-planes", r"rectangles$^*$", r"$\sum_{i \le 4}\binom ni$", r"$2^n$"]]
        for r in d["rows"]:
            if r["n"] in (2, 3, 4, 5, 6, 8, 10):
                rows.append([str(r["n"]), str(r["halflines"]), str(r["intervals"]), str(r["halfplanes"]), str(r["rect"]), str(r["ss4"]), f"{r['all']:,}"])
        tab = table_rows(rows, font_size=26, col_buff=0.55, row_buff=0.3, colors=[GREY_B] + [None] * 7)
        if tab.width > 12.6:
            tab.width = 12.6
        tab.move_to([0, 0.7, 0])
        foot = label(r"brute-force counts: \ $^*$the most over six random configurations; \ the half-plane count is $n(n-1)+2$", font_size=22, color=GREY_A).move_to([0, -2.3, 0])
        foot2 = label(r"Sauer--Shelah: \ dimension $V$ $\Rightarrow$ $\Pi(n) \le \sum_{i \le V}\binom ni \le (en/V)^V$: \ polynomial", font_size=24, color=GOODC).next_to(foot, DOWN, buff=0.2)
        with self.voiceover(
            "<bookmark mark='a'/> Counting by brute force on points in the plane: half-lines pick out n plus one subsets, "
            "intervals n times n plus one over two plus one, and half-planes n times n minus one plus two, Thomas Cover's "
            "count. Rectangles, on random points, pick out more, but still far fewer than all subsets in the last column. "
            "<bookmark mark='b'/> The pattern is a theorem, proved independently by Norbert Sauer and Saharon Shelah in 1972: "
            "once a class fails to shatter some number of points V plus one, its growth function is at most the sum of the "
            "binomial coefficients up to V, a polynomial of degree V. There is no middle ground between polynomial and "
            "exponential growth."
        ) as vo:
            vo.wait_until("a")
            self.play(FadeIn(tab), FadeIn(foot))
            vo.wait_until("b")
            self.play(FadeIn(foot2))
        self.clear_scene()

    def chart(self):
        d = load("vc")
        n = np.array([r["n"] for r in d["rows"]], float)
        A = axes([1, 10], [0, 10.5], x_length=7.4, y_length=4.4, xlabel=r"$n$", ylabel=r"$\log_2 \Pi(n)$",
                 xticks=[2, 4, 6, 8, 10], yticks=[0, 2, 4, 6, 8, 10], center=[-2.5, 0.2, 0])
        ax = A.ax

        def line(key, c):
            v = np.log2([r[key] for r in d["rows"]])
            return VGroup(polyline(ax, n, v, c, 4), *[Dot(ax.c2p(a, b), radius=0.07, color=c) for a, b in zip(n, v)])

        call, chl, chp, crect = line("all", BADC), line("halflines", EMPC), line("halfplanes", CLASSC), line("rect", S.ALT)
        side = fit_rows(VGroup(
            label(r"red: \ all subsets, \ $n$ bits", font_size=22, color=BADC),
            label(r"blue: \ half-lines, \ $\log_2(n+1)$", font_size=22, color=EMPC),
            label(r"gold: \ half-planes, \ $\approx 2\log_2 n$", font_size=22, color=CLASSC),
            label(r"teal: \ rectangles, \ $\approx 4\log_2 n$", font_size=22, color=S.ALT),
            label(r"a VC class: \ logarithmic in bits, \ forever", font_size=22, color=GOODC),
        ), 4.6, 0.42, [4.45, 0.4, 0])
        with self.voiceover(
            "<bookmark mark='a'/> On a log scale the difference is stark. Measured in bits, the set of all subsets grows "
            "linearly, one bit per point. <bookmark mark='b'/> Half-lines grow like log n, <bookmark mark='c'/> half-planes "
            "like two log n, <bookmark mark='d'/> and rectangles like four log n, each hugging the diagonal until its VC "
            "dimension and peeling away after. <bookmark mark='e'/> Plugged into chapter one's bound, logarithmic growth gives "
            "a uniform law of large numbers at rate root of V log n over n. The VC dimension is the complexity that counts."
        ) as vo:
            self.play(FadeIn(A), FadeIn(exact_tag(r"exact: \ brute-force counts")))
            for k, (m_, c) in enumerate(zip("abcde", [call, chl, chp, crect, None])):
                vo.wait_until(m_)
                anims = [FadeIn(side[k])]
                if c is not None:
                    anims.insert(0, Create(c))
                self.play(*anims)
        self.clear_scene()

    def covering(self):
        rows = fit_rows(VGroup(
            label(r"Haussler (1995): \ a VC class of dimension $V$ has $N(\varepsilon, L_2(Q)) \le K\,(1/\varepsilon)^{2V}$ \ for every $Q$", font_size=26),
            label(r"so: \ VC $\Rightarrow$ Glivenko--Cantelli, \ for every $P$, \ uniformly", font_size=26, color=GOODC),
            label(r"VC-subgraph functions: \ linear combinations of $d$ functions, \ monotone functions of them", font_size=26, color=CLASSC),
            label(r"but $\{x \mapsto \mathbf 1\{\sin(\omega x) > 0\} : \omega > 0\}$ has infinite VC dimension, \ with one parameter", font_size=26, color=BADC),
            label(r"dimension is not the number of parameters", font_size=26, color=GREY_A),
        ), 12.4, 0.55, [0, 0, 0])
        with self.voiceover(
            "<bookmark mark='a'/> VC classes are small in a stronger sense too. David Haussler showed that a class of "
            "dimension V can be covered by about one over epsilon to the two V balls of radius epsilon in L two of any "
            "probability measure. <bookmark mark='b'/> So a VC class is Glivenko–Cantelli for every underlying "
            "distribution at once. <bookmark mark='c'/> The idea extends to functions through their subgraphs: finite "
            "dimensional vector spaces of functions, and monotone transformations of them, are VC. <bookmark mark='d'/> "
            "But beware counting parameters. The class of indicators of sine of omega x being positive has one parameter "
            "and infinite VC dimension: with a high enough frequency it can realise any labelling of suitably placed points. "
            "<bookmark mark='e'/> Complexity is about what a class can do, not how it is written down."
        ) as vo:
            for k, m_ in enumerate("abcde"):
                vo.wait_until(m_)
                self.play(FadeIn(rows[k], shift=RIGHT * 0.2))
        self.clear_scene()

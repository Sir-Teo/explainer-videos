from __future__ import annotations

import math

import numpy as np

from explainer.ai import *  # noqa: F403
from videos.ai.ai8.common import BOUND, HIST, MEAS, NEG, POS, TEST, card_body, chapter, curve, load


def find_line(P, s):
    """A separating line (w, b) for the labels s, or None."""
    for th in np.linspace(0, 2 * math.pi, 720, endpoint=False):
        w = np.array([math.cos(th), math.sin(th)])
        pr = P @ w
        pos, neg = pr[s > 0], pr[s < 0]
        if len(pos) == 0:
            return w, -(pr.max() + 0.6)
        if len(neg) == 0:
            return w, -(pr.min() - 0.6)
        if pos.min() > neg.max() + 0.05:
            return w, -0.5 * (pos.min() + neg.max())
    return None


def clip(a, b, c, h):
    pts = []
    for t in np.linspace(0, 1, 400):
        p = a + t * (b - a)
        if abs(p[0] - c[0]) <= h and abs(p[1] - c[1]) <= h:
            pts.append(p)
    return (pts[0], pts[-1]) if pts else (c, c)


def panel(P, s, center=ORIGIN, size=0.55, radius=0.09):
    box = Square(2 * size + 0.6, stroke_color=GREY_D, stroke_width=1.5).move_to(center)
    c = np.asarray(center, float)
    dots = VGroup(*[Dot(c + size * np.array([*p, 0]) * 0.8, radius=radius, color=POS if v > 0 else NEG)
                    for p, v in zip(P, s)])
    fl = find_line(P, s)
    if fl is None:
        return VGroup(box, dots, Cross(box, stroke_color=C.SURPRISE, stroke_width=4).scale(0.35))
    w, b = fl
    d = np.array([-w[1], w[0]])
    p0 = -b * w
    a_ = c + size * 0.8 * np.array([*(p0 - 3 * d), 0])
    b_ = c + size * 0.8 * np.array([*(p0 + 3 * d), 0])
    line = Line(a_, b_, color=C.BITS, stroke_width=3)
    line.put_start_and_end_on(*clip(a_, b_, c, 0.5 * box.width))
    return VGroup(box, dots, line)


class VC(VoiceoverScene):
    def construct(self):
        chapter(self, 4, r"Shattering and the VC bound", r"How do you count infinitely many lines?",
                "Chapter four. Shattering, and the VC bound.", lit=(1995,))
        self.shatter()
        self.growth()
        self.bound()

    # ------------------------------------------------------------------
    def shatter(self):
        s = load("shatter")
        P3, P4 = np.asarray(s["P3"]), np.asarray(s["P4"])
        L3, L4 = np.asarray(s["labs3"]), np.asarray(s["labs4"])
        p3 = VGroup(*[panel(P3, L3[k], [-5.6 + 1.6 * (k % 4), 1.7 - 2.0 * (k // 4), 0]) for k in range(8)])
        p3.move_to([-3.3, 0.6, 0])
        bad = [k for k in range(16) if not s["ok4"][k]]
        good = [k for k in range(16) if s["ok4"][k]][:2]
        p4 = VGroup(*[panel(P4, L4[k]) for k in good + bad]).arrange_in_grid(rows=2, cols=2, buff=0.25)
        p4.move_to([3.6, 0.6, 0])
        t3 = label(r"$3$ points: \ all $8$ labellings, \ a line for each", font_size=26).next_to(p3, UP, buff=0.3)
        t4 = label(r"$4$ points: \ no line for these two", font_size=26).next_to(p4, UP, buff=0.3)
        dfn = definition_card(r"shattering; \ the VC dimension",
                              r"a family \textit{shatters} $n$ points if it realizes all $2^n$ labellings of them. \ "
                              r"Its VC dimension $d$ is the largest $n$ it can shatter: \ $3$ for lines in the plane, "
                              r"\ $k + 1$ for linear rules on $k$ numbers.", width=11.5, font_size=21)
        dfn.to_edge(DOWN, buff=0.25)
        with self.voiceover(
            "A family of rules with infinitely many members can still be weak. Take lines in the plane, and three "
            "points. <bookmark mark='a'/> Colour the points any of the eight possible ways, and some line separates "
            "the colours every time. <bookmark mark='b'/> With four points, it fails: no line splits these two "
            "labellings, the crossing pattern of XOR. <bookmark mark='c'/> A family shatters a set of points if it "
            "can produce every labelling of them, and the largest set it can shatter is its VC dimension, after "
            "Vapnik and Chervonenkis: three for lines in the plane, and in general one more than the number of "
            "inputs a linear rule with a bias reads."
        ) as vo:
            self.play(FadeIn(t3))
            vo.wait_until("a")
            self.play(LaggedStart(*[FadeIn(p) for p in p3], lag_ratio=0.15), run_time=2.5)
            vo.wait_until("b")
            self.play(FadeIn(t4), LaggedStart(*[FadeIn(p) for p in p4], lag_ratio=0.2), run_time=1.5)
            vo.wait_until("c")
            self.play(FadeIn(dfn, shift=UP * 0.2))
        self.wait(0.3)
        self.clear_scene()

    # ------------------------------------------------------------------
    def growth(self):
        g = load("growth")
        ns = np.asarray(g["ns"])
        half, inter, s3, p2 = (np.asarray(g[k], float) for k in ("half", "interval", "sauer3", "pow2"))
        P5, L5 = np.asarray(g["P5"]), np.asarray(g["labs5"])
        n5 = int(g["n5"])
        # the 5-point labellings that half-planes realize, as small panels
        pans = VGroup(*[panel(P5 * 0.75, np.array([1 if (int(m) >> i) & 1 else -1 for i in range(5)]), size=0.32,
                              radius=0.05) for m in L5])
        pans.arrange_in_grid(rows=3, buff=0.1).scale_to_fit_width(6.2).move_to([-3.4, 1.7, 0])
        pcap = label(rf"$5$ points: \ half-planes give ${n5}$ of the $32$ labellings", font_size=24, color=GREY_A)
        pcap.next_to(pans, DOWN, buff=0.15)
        G = axes([0, 16], [0, 16], x_length=6.0, y_length=4.6, xticks=[0, 4, 8, 12, 16], yticks=[0, 4, 8, 12, 16],
                 yfmt=lambda v: f"2^{{{int(v)}}}", xlabel=r"$n$ points", ylabel=r"labellings realized \ (log scale)",
                 center=(3.6, -0.5, 0))
        ax = G.ax
        c2 = curve(ax, ns, np.log2(p2), GREY_B, 3)
        cs = curve(ax, ns, np.log2(s3), BOUND, 3.5)
        ch = VGroup(curve(ax, ns, np.log2(half), MEAS, 4),
                    *[Dot(ax.c2p(n, math.log2(h)), radius=0.045, color=MEAS) for n, h in zip(ns, half)])
        ci = curve(ax, ns, np.log2(inter), TEST, 3)
        key = legend([(GREY_B, r"all $2^n$"), (BOUND, r"Sauer--Shelah, $d = 3$"),
                      (MEAS, r"half-planes, \ counted"), (TEST, r"intervals on a line, \ counted")], font_size=19)
        key.next_to(ax.c2p(0, 16), DR, buff=0.15)
        thm = theorem_card(r"the Sauer--Shelah lemma",
                           card_body(r"VC dimension $d$, \ $n \ge d \ge 1$:",
                                     r"\Pi_{\mathcal H}(n) \le \sum_{i=0}^{d} \binom{n}{i} \le \big(\tfrac{en}{d}\big)^d",
                                     width=5.4, font_size=21), who=r"N.~Sauer; \ S.~Shelah "
                           r"(1972); \ Vapnik \& Chervonenkis (1971)", width=6.2, font_size=21)
        thm.to_corner(DL, buff=0.3)
        nN = int(ns[-1])
        with self.voiceover(
            "What matters is not how many rules a family has, but how many different labellings it can produce on "
            "the points in front of it: the growth function. <bookmark mark='a'/> For five points, half-planes "
            f"produce {n5} of the thirty-two. <bookmark mark='b'/> Count it for every n by sweeping a line around: "
            f"for points in general position, half-planes realize n squared minus n plus two labellings, {int(half[-1])} on {nN} points, out "
            f"of {int(p2[-1]):,}. <bookmark mark='c'/> The Sauer–Shelah lemma says this always happens: once a "
            "family cannot shatter any set of size d plus one, its growth is bounded by a polynomial of degree d, rather than "
            "continuing as two to the n. <bookmark mark='d'/> Intervals on a line, VC dimension two, meet their bound "
            "exactly. Polynomial instead of exponential is what lets an infinite family be learned."
        ) as vo:
            self.play(FadeIn(G), Create(c2), FadeIn(key[0]))
            self.play(LaggedStart(*[FadeIn(p) for p in pans], lag_ratio=0.05), run_time=2.0)
            vo.wait_until("a")
            self.play(FadeIn(pcap), Indicate(pans, color=C.BITS, scale_factor=1.02))
            vo.wait_until("b")
            self.play(Create(ch), FadeIn(key[2]), run_time=2.0)
            vo.wait_until("c")
            self.play(FadeOut(pans), FadeOut(pcap), FadeIn(thm, shift=UP * 0.2), Create(cs), FadeIn(key[1]))
            vo.wait_until("d")
            self.play(Create(ci), FadeIn(key[3]))
        self.wait(0.3)
        self.clear_scene()

    # ------------------------------------------------------------------
    def bound(self):
        g = load("growth")
        col = {r"\Pi_{\mathcal H}(2n)": MEAS}
        rows = [
            cmath(r"P\big(\sup_h |R - \hat R| > \varepsilon\big)", r"\le",
                  r"2\,P\big(\sup_h |\hat R' - \hat R| > \tfrac{\varepsilon}{2}\big)", font_size=30),
            cmath(r"P\big(\sup_h |R - \hat R| > \varepsilon\big)", r"\le",
                  r"2\,\Pi_{\mathcal H}(2n) \cdot 2 e^{-n\varepsilon^2/8}", colors=col, font_size=30),
            cmath(r"P\big(\sup_h |R - \hat R| > \varepsilon\big)", r"\le", r"4\,(2en/d)^d\, e^{-n\varepsilon^2/8}",
                  font_size=30),
            cmath(r"R(h)", r"\le", r"\hat R(h) + \sqrt{\dfrac{8\,[d\,(\ln(2n/d) + 1) + \ln(4/\delta)]}{n}}", font_size=32,
                  colors={r"\hat R(h) + \sqrt{\dfrac{8\,[d\,(\ln(2n/d) + 1) + \ln(4/\delta)]}{n}}": BOUND}),
        ]
        whys = [why(r"a ghost sample $S'$: \ symmetrization, \ $n\varepsilon^2 \ge 2$"),
                why(r"on $2n$ points, \ only $\Pi(2n)$ labellings: \ union bound, \ Hoeffding"),
                why(r"Sauer--Shelah, \ $1 \le d \le n$"),
                why(r"solve for $\varepsilon$, \ uniformly with probability $1-\delta$")]
        step = ladder(self, rows, whys, keep=4, top=3.2, x=-1.8, buff=0.42, edge=6.9)
        nums = VGroup(
            label(rf"lines in the plane, \ $n = 448$: \ gap $\le {g['lines_plane']:.2f}$", font_size=24, color=MEAS),
            label(rf"linear on $70$ word rates \ ($d = 71$), \ $n = 448$: \ gap $\le {g['lines_pages']:.2f}$",
                  font_size=24, color=BOUND),
            label(rf"for a gap of $0.1$: \ $n \approx {fmt_int(g['n10'])}$ pages", font_size=24, color=BOUND),
            label(rf"a network with ${fmt_int(load('random')['n_params'])}$ weights: \ $d > n$, \ the bound says "
                  r"nothing", font_size=24, color=C.SURPRISE),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.16).to_corner(DL, buff=0.35)
        hist = history_card(1971, r"V.~Vapnik \& A.~Chervonenkis", r"uniform convergence of frequencies to "
                            r"probabilities (announced 1968); \ Vapnik's support vector machines followed in 1995",
                            width=5.0, font_size=18, color=HIST).to_corner(DR, buff=0.3)
        with self.voiceover(
            "That count buys a bound for IID binary classification, with 95 percent confidence here. The proof in four steps. <bookmark mark='a'/> First, compare the training "
            "sample with a second, imaginary one of the same size, a ghost sample: if training and true error are "
            "far apart, the two samples' errors probably are too. <bookmark mark='b'/> On the two samples together, "
            "the family acts as at most the growth function of two n rules, a finite number, so the union bound "
            "and Hoeffding apply. <bookmark mark='c'/> Sauer–Shelah makes that number a polynomial. "
            "<bookmark mark='d'/> Solve for epsilon: the gap shrinks like the square root of d log n over n. "
            f"<bookmark mark='e'/> For lines in the plane on 448 pages, the gap is at most {g['lines_plane']:.2f}. For a "
            f"linear rule on all seventy word rates, {g['lines_pages']:.2f}: hardly a guarantee; it would take about "
            f"{int(g['n10']):,} pages to get it down to a tenth. And for the network of chapter nine, with three "
            "hundred thousand weights for 448 pages, it says nothing at all. That network generalizes anyway."
        ) as vo:
            step(0)
            self.play(FadeIn(hist, shift=UP * 0.2))
            vo.wait_until("a")
            self.play(Indicate(rows[0][2], color=WHITE, scale_factor=1.03))
            vo.wait_until("b")
            step(1)
            vo.wait_until("c")
            step(2)
            vo.wait_until("d")
            step(3)
            vo.wait_until("e")
            self.play(LaggedStart(*[FadeIn(r_, shift=UP * 0.1) for r_ in nums], lag_ratio=0.5), run_time=3.0)
        self.wait(0.3)
        self.clear_scene()

from __future__ import annotations

import numpy as np

from videos.stats.stats2.common import *  # noqa: F403

SUM_COLORS = {s: interpolate_color(ManimColor("#5DADEC"), ManimColor("#F28FB8"), (s - 2) / 10) for s in range(2, 13)}


def staircase(ax, xs, F, color, stroke_width=3, x_lo=None, x_hi=None):
    """A CDF of a discrete variable: flat steps with jumps at xs (values), F the cumulative sums."""
    pts = []
    x_lo = bounds(ax)[0] if x_lo is None else x_lo
    x_hi = bounds(ax)[1] if x_hi is None else x_hi
    prev = 0.0
    cur = x_lo
    segs = VGroup()
    for x, f in zip(xs, F):
        segs.add(Line(ax.c2p(cur, prev), ax.c2p(x, prev), color=color, stroke_width=stroke_width))
        segs.add(DashedLine(ax.c2p(x, prev), ax.c2p(x, f), color=color, stroke_width=1.5, stroke_opacity=0.5))
        segs.add(Dot(ax.c2p(x, f), radius=0.05, color=color))
        prev, cur = f, x
    segs.add(Line(ax.c2p(cur, prev), ax.c2p(x_hi, prev), color=color, stroke_width=stroke_width))
    _ = pts
    return segs


class Variables(VoiceoverScene):
    def construct(self):
        self.card()
        self.function()
        self.cdf()
        self.kinds()
        self.cantor()

    def card(self):
        card = chapter_card(10, r"Random variables", r"Numbers that depend on chance, and their distributions",
                            lit=(1933,), part=PART)
        with self.voiceover("Chapter ten. Random variables."):
            self.play(FadeIn(card[0], shift=UP * 0.2), FadeIn(card[1]))
        self.play(FadeOut(card))

    def function(self):
        d = load("variables")
        grid = outcome_grid(size=0.6, buff=0.06, show_dice=False).move_to([-4.0, 0.2, 0])
        dice_hdr = VGroup(*[die_face(i, 0.32).next_to(grid.cell[(i, 1)], UP, buff=0.12) for i in range(1, 7)])
        dice_side = VGroup(*[die_face(j, 0.32).next_to(grid.cell[(1, j)], LEFT, buff=0.12) for j in range(1, 7)])
        nums = VGroup()
        for (i, j), c in grid.cell.items():
            nums.add(MathTex(str(i + j), font_size=26, color=SUM_COLORS[i + j]).move_to(c))
        om = MathTex(r"\Omega", font_size=36, color=GREY_A).next_to(grid, DOWN, buff=0.25)
        dfn = definition_card(r"Random variable", r"a function $X : \Omega \to \mathbb{R}$, \ a number for every "
                              r"outcome. \ Its \emph{distribution}: \ $P(X = x) = P(\{\omega : X(\omega) = x\})$",
                              color=EXACT, width=6.0, font_size=23).move_to([3.4, 2.3, 0])
        A = axes([1.5, 12.5], [0, 6.6], x_length=5.6, y_length=3.0, xticks=list(range(2, 13)), center=[3.4, -0.5, 0])
        A.ax.y_axis.set_opacity(0)
        ax = A.ax
        cell_w = (ax.c2p(1, 0)[0] - ax.c2p(0, 0)[0]) * 0.8
        cell_h = (ax.c2p(0, 1)[1] - ax.c2p(0, 0)[1]) * 0.92
        height = {s: 0 for s in range(2, 13)}
        targets = []
        for (i, j), c in grid.cell.items():
            s = i + j
            targets.append(Square(side_length=1, stroke_color=GREY_D, stroke_width=1, fill_color=SUM_COLORS[s],
                                  fill_opacity=0.85).stretch_to_fit_width(cell_w).stretch_to_fit_height(cell_h)
                           .move_to(ax.c2p(s, height[s] + 0.5)))
            height[s] += 1
        pmf = label(r"$P(X = x)$: \ counts over $36$", font_size=24, color=GREY_A).next_to(A, DOWN, buff=0.05)
        code = code_block(["two = die * die", "X = two.map(sum)        # the push-forward"], font_size=20)
        code.next_to(A, DOWN, buff=0.35)
        with self.voiceover(
            "So far we've asked about events. Most statistical questions are about numbers. <bookmark mark='a'/> "
            "Here are the thirty-six outcomes of two dice again. <bookmark mark='b'/> Write in each cell the sum of "
            "the two dice. That assignment, a number for every outcome, is a random variable. The name is "
            "unfortunate: it's neither random nor a variable. It's a function on the outcomes, and the randomness "
            "lives in which outcome happens. <bookmark mark='c'/> What we usually care about is its distribution: "
            "for each value, the probability of the set of outcomes that produce it. <bookmark mark='d'/> Watch "
            "the outcomes sort themselves by their value. One way to make two, six ways to make seven, one way to "
            "make twelve. <bookmark mark='e'/> The thirty-six cells have become the familiar triangle. The engine "
            "calls this map: it carries the probability from the outcomes to the values, and statisticians call the "
            "result the push-forward of P."
        ) as vo:
            vo.wait_until("a")
            self.play(LaggedStart(*[FadeIn(c) for c in grid], lag_ratio=0.01), FadeIn(dice_hdr), FadeIn(dice_side),
                      FadeIn(om))
            vo.wait_until("b")
            self.play(LaggedStart(*[FadeIn(n_, scale=0.6) for n_ in nums], lag_ratio=0.02), run_time=2.0)
            vo.wait_until("c")
            self.play(FadeIn(dfn, shift=LEFT * 0.2))
            vo.wait_until("d")
            self.play(FadeIn(A))
            movers = VGroup(*[VGroup(c[0].copy(), n_.copy()) for c, n_ in zip(grid, nums)])
            self.play(LaggedStart(*[Transform(m, VGroup(t, VectorizedPoint(t.get_center())))
                                    for m, t in zip(movers, targets)], lag_ratio=0.03), run_time=4.0)
            vo.wait_until("e")
            self.play(FadeIn(code, shift=UP * 0.2))
        _ = d
        self.clear_scene()

    def cdf(self):
        d = load("variables")
        pmf = np.asarray(d["pmf"])
        F = np.cumsum(pmf)
        A = axes([1, 13], [0, 1.05], x_length=8.8, y_length=4.4, xlabel=r"$x$", ylabel=r"$F(x) = P(X \le x)$",
                 xticks=list(range(2, 13)), yticks=[0, 0.5, 1], center=[-1.4, -0.3, 0])
        ax = A.ax
        st = staircase(ax, list(range(2, 13)), F, EXACT)
        props = VGroup(
            label(r"non-decreasing", font_size=26),
            label(r"from $0$ to $1$", font_size=26),
            label(r"right-continuous: \ each jump lands on its dot", font_size=26),
            label(r"jump at $x$ \ $=$ \ $P(X = x)$", font_size=26, color=EXACT),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.3).move_to([4.7, 0.6, 0])
        for p in props:
            if p.width > 4.6:
                p.width = 4.6
        jump = Brace(Line(ax.c2p(7, F[4]), ax.c2p(7, F[5])), RIGHT, color=S.ACCENT, buff=0.05)
        jl = MathTex(r"\tfrac{6}{36}", font_size=28, color=S.ACCENT).next_to(jump, RIGHT, buff=0.08)
        back = label(r"Part 1's ECDF and quantiles: \ the same object, for data", font_size=24, color=GREY_B)
        back.to_edge(DOWN, buff=0.3)
        with self.voiceover(
            "One function describes any distribution, of any kind: the cumulative distribution function. "
            "<bookmark mark='a'/> F of x is the probability that X is at most x. For the sum of two dice it's a "
            "staircase, climbing from zero to one, with a jump at each possible value. <bookmark mark='b'/> The "
            "height of each jump is the probability of that value: six thirty-sixths at seven. <bookmark mark='c'/> "
            "Every CDF has the same three properties: it never decreases, it goes from zero to one, and it's "
            "continuous from the right, so at each jump the function takes the upper value. And every function with "
            "those properties is the CDF of some random variable. <bookmark mark='d'/> If this looks familiar, it "
            "should: Part 1's empirical distribution function is exactly this, for the data."
        ) as vo:
            self.play(FadeIn(A))
            vo.wait_until("a")
            self.play(LaggedStart(*[FadeIn(m) for m in st], lag_ratio=0.03), run_time=3.0)
            vo.wait_until("b")
            self.play(FadeIn(jump), FadeIn(jl), FadeIn(props[3]))
            vo.wait_until("c")
            self.play(LaggedStart(*[FadeIn(p, shift=RIGHT * 0.2) for p in props[:3]], lag_ratio=0.4))
            vo.wait_until("d")
            self.play(FadeIn(back))
        self.clear_scene()

    def kinds(self):
        panels = VGroup()
        specs = [(r"discrete", r"a die: \ jumps only", S.EST), (r"continuous", r"a waiting time: \ a density, \ "
                                                                              r"$F' = f$", S.LIK),
                 (r"mixed", r"a day's rain: \ $P(0) = 0.6$, \ then smooth", S.POST)]
        for k, (name, sub, col) in enumerate(specs):
            A = axes([0, 6], [0, 1.05], x_length=3.6, y_length=2.6, yticks=[0, 1], center=[-4.6 + 4.6 * k, -0.2, 0])
            ax = A.ax
            if k == 0:
                g = staircase(ax, [1, 2, 3, 4, 5, 6], [i / 6 for i in range(1, 7)], col, stroke_width=3, x_lo=0, x_hi=6)
            elif k == 1:
                xs = np.linspace(0, 6, 120)
                g = curve(ax, xs, 1 - np.exp(-xs / 1.3), col, 3)
            else:
                xs = np.linspace(0, 6, 120)
                g = VGroup(Line(ax.c2p(0, 0), ax.c2p(0, 0.6), color=col, stroke_width=1.5, stroke_opacity=0.5),
                           Dot(ax.c2p(0, 0.6), radius=0.06, color=col),
                           curve(ax, xs, 0.6 + 0.4 * (1 - np.exp(-xs / 1.1)), col, 3))
            t = label(name, font_size=30, color=col).next_to(A, UP, buff=0.2)
            s_ = label(sub, font_size=22, color=GREY_A).next_to(A, DOWN, buff=0.2)
            panels.add(VGroup(A, g, t, s_))
        tag = note(r"illustrative").to_corner(DR, buff=0.3)
        with self.voiceover(
            "CDFs come in kinds. <bookmark mark='a'/> A discrete variable, like a die, has a CDF that only jumps. "
            "<bookmark mark='b'/> A continuous one, like the time until the next bus arrives, has a smooth CDF with "
            "no jumps at all: each single value has probability zero, and probability is spread with a density, "
            "the CDF's slope. <bookmark mark='c'/> And some are mixed. The rainfall on a given day is exactly zero "
            "with probability, say, sixty percent, a jump at zero, and otherwise it's spread smoothly over positive "
            "amounts. <bookmark mark='d'/> Discrete, continuous and mixed: is that every kind? Surprisingly, no."
        ) as vo:
            self.play(FadeIn(tag))
            for k, m in enumerate("abc"):
                vo.wait_until(m)
                self.play(FadeIn(panels[k][0]), FadeIn(panels[k][2]), FadeIn(panels[k][3]), Create(panels[k][1]))
            vo.wait_until("d")
            self.play(*[p.animate.fade(0.65) for p in panels])
        self.clear_scene()

    def cantor(self):
        d = load("variables")
        xs = np.asarray(d["xs"])
        levels = np.asarray(d["levels"])
        A = axes([0, 1], [0, 1.02], x_length=7.4, y_length=5.0, xlabel=r"$x$", ylabel=r"$F(x)$", xticks=[0, 1 / 3, 2 / 3, 1],
                 yticks=[0, 0.5, 1], xfmt=lambda v: {0: "0", 1: "1"}.get(v, r"\tfrac13" if v < 0.5 else r"\tfrac23"),
                 center=[-2.4, -0.1, 0])
        ax = A.ax
        cur = curve(ax, xs, levels[0], EXACT, 3)
        # the Cantor set's intervals at each level, under the axis
        def cset(L):
            ivs = [(0.0, 1.0)]
            for _ in range(L):
                ivs = [iv for a, b in ivs for iv in ((a, a + (b - a) / 3), (b - (b - a) / 3, b))]
            return VGroup(*[Line(ax.c2p(a, 0) + DOWN * 0.18, ax.c2p(b, 0) + DOWN * 0.18, color=S.ACCENT,
                                 stroke_width=5) for a, b in ivs])
        cs = cset(0)
        lev = MathTex(r"\text{level } 0", font_size=28, color=GREY_A).move_to([3.6, 2.8, 0])
        defn = MathTex(r"X = \sum_{k \ge 1} \frac{2 b_k}{3^k}", r",\quad b_k \text{ fair coin flips}", font_size=32)
        defn.move_to([3.9, 1.7, 0])
        props = VGroup(
            label(r"no jumps: \ $P(X = x) = 0$ for every $x$", font_size=24),
            label(r"no density: \ $F' = 0$ off a set of length $0$", font_size=24),
            label(r"all the mass on the Cantor set", font_size=24, color=S.ACCENT),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.25).move_to([3.9, 0.1, 0])
        cs_ = np.asarray(d["cantor"])
        ecdf_x = cs_[::40]
        ecdf = VGroup(*[Dot(ax.c2p(x, (k * 40 + 1) / len(cs_)), radius=0.025, color=SIM) for k, x in enumerate(ecdf_x)])
        chk = VGroup(MathTex(rf"E X = \tfrac12 \quad \text{{simulated }} {d['cantor_mean']:.4f}", font_size=26, color=SIM),
                     MathTex(rf"\mathrm{{Var}}\, X = \tfrac18 \quad \text{{simulated }} {d['cantor_var']:.4f}",
                             font_size=26, color=SIM)).arrange(DOWN, aligned_edge=LEFT, buff=0.15).move_to([3.9, -1.7, 0])
        leb = label(r"every distribution $=$ discrete $+$ continuous $+$ singular parts \ (Lebesgue; \ Part 43)",
                    font_size=24, color=GREY_B).to_edge(DOWN, buff=0.3)
        tag = note(r"computed: 20,000 draws, 30 ternary digits each").to_corner(UR, buff=0.25)
        with self.voiceover(
            "Here's a fourth kind, and it's strange. <bookmark mark='a'/> Build a number between zero and one in "
            "base three, digit by digit, flipping a fair coin for each digit: zero or two, never one. "
            "<bookmark mark='b'/> Its distribution function starts out as a straight line, <bookmark mark='c'/> "
            "but at each stage the middle third of every remaining interval is removed, because a digit one is "
            "impossible, and the CDF goes flat there. <bookmark mark='d'/> In the limit you get the devil's "
            "staircase, Cantor's function. It's continuous, so the variable takes no single value with positive "
            "probability. But it's flat almost everywhere, so there's no density either: all the probability lives "
            "on the Cantor set, a dust of points with total length zero. <bookmark mark='e'/> Twenty thousand draws "
            "from the coin-flip recipe fall right on the staircase, with mean a half and variance an eighth, as the "
            "theory predicts. <bookmark mark='f'/> Distributions like this are called singular, and Lebesgue showed "
            "that every distribution is a mixture of a discrete part, a continuous part and a singular part. Part "
            "43 proves it. For the rest of Stage One, discrete and continuous will be enough, and Part 3 names the "
            "shapes that keep appearing."
        ) as vo:
            self.play(FadeIn(A), FadeIn(tag))
            vo.wait_until("a")
            self.play(Write(defn))
            vo.wait_until("b")
            self.play(Create(cur), FadeIn(cs), FadeIn(lev))
            vo.wait_until("c")
            for L in range(1, 6):
                self.play(Transform(cur, curve(ax, xs, levels[L], EXACT, 3)), Transform(cs, cset(L)),
                          Transform(lev, MathTex(rf"\text{{level }} {L}", font_size=28, color=GREY_A).move_to(lev)),
                          run_time=1.2)
            vo.wait_until("d")
            self.play(Transform(cur, curve(ax, xs, np.asarray(d["staircase"]), EXACT, 3)),
                      Transform(lev, MathTex(r"\text{the limit}", font_size=28, color=EXACT).move_to(lev)))
            self.play(LaggedStart(*[FadeIn(p, shift=RIGHT * 0.2) for p in props], lag_ratio=0.5), run_time=3.0)
            vo.wait_until("e")
            self.play(FadeIn(ecdf, lag_ratio=0.01), run_time=2.0)
            self.play(FadeIn(chk))
            vo.wait_until("f")
            self.play(FadeIn(leb))
        self.clear_scene()

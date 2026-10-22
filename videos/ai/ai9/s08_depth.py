from __future__ import annotations

import numpy as np

from explainer.ai import *  # noqa: F403
from videos.ai.ai9.common import HINGE, NEURON, PART, load, patch_image, rgb_of

CORNERS = ("#2E6FB0", "#3FB8AF", "#F28C5B", "#B39DDB")  # the folded square's four corners


def motif(Q):
    """An asymmetric picture on [-1, 1]^2 (an F), so that every mirror image is visible."""
    x, y = Q[..., 0], Q[..., 1]
    bar = (x > -0.62) & (x < -0.32) & (y > -0.75) & (y < 0.75)
    top = (x > -0.62) & (x < 0.55) & (y > 0.45) & (y < 0.75)
    mid = (x > -0.62) & (x < 0.25) & (y > -0.1) & (y < 0.18)
    return bar | top | mid


def fold_picture_rgb(Q) -> np.ndarray:
    u, v = (Q[..., 0] + 1) / 2, (Q[..., 1] + 1) / 2
    c = [rgb_of(k) for k in CORNERS]
    rgb = ((1 - u) * (1 - v))[..., None] * c[0] + (u * (1 - v))[..., None] * c[1] + (u * v)[..., None] * c[2] + \
          ((1 - u) * v)[..., None] * c[3]
    rgb = 0.55 * rgb + 0.45 * rgb_of("#0B0F17")
    rgb[motif(Q)] = rgb_of(C.BITS)
    return rgb


def fold_picture(Q, side) -> ImageMobject:
    """Colour each input point by where the folds send it: a smooth blend of the four corners of the folded square,
    with the F on top. Each linear piece of the network shows one whole (mirrored) copy."""
    rgb = fold_picture_rgb(Q)
    img = ImageMobject((np.concatenate([rgb, np.ones(Q.shape[:2] + (1,))], -1)[::-1] * 255).astype(np.uint8))
    img.set_resampling_algorithm(RESAMPLING_ALGORITHMS["bilinear"])
    return img.stretch_to_fit_width(side).stretch_to_fit_height(side)


class Depth(VoiceoverScene):
    def construct(self):
        self.card()
        self.folding()
        self.foldplane()
        self.counting()
        self.random_nets()

    def card(self):
        card = chapter_card(7, r"What depth adds", r"Why stack layers at all?", part=PART)
        with self.voiceover("Chapter seven. What depth adds."):
            self.play(FadeIn(card[0], shift=UP * 0.2), FadeIn(card[1]))
        self.play(FadeOut(card))

    # ------------------------------------------------------------------
    def folding(self):
        s = load("sawtooth")
        xs = np.asarray(s["xs"])
        ax = Axes(x_range=[0, 1, 0.5], y_range=[0, 1, 0.5], x_length=6.2, y_length=3.6, tips=False,
                  axis_config={"stroke_color": GREY_C, "include_ticks": False}).move_to([-2.9, -0.4, 0])
        ident = curve(ax, xs, xs, GREY_B, 3)
        teeth = [curve(ax, xs, np.asarray(s[f"tent{k}"]), HINGE, 4) for k in range(1, 6)]
        colors = {r"t(x)": HINGE}
        f = cmath(r"t(x)", "=", r"2\max(0, x) - 4\max(0,\, x - \tfrac12)", colors=colors, font_size=34)
        f.to_edge(UP, buff=0.4).shift(LEFT * 2.6)
        fl = label(r"one layer of $2$ units: \ a tent", font_size=26, color=GREY_A).next_to(f, DOWN, buff=0.15)
        kv = Integer(1, font_size=40, color=HINGE)
        kl = VGroup(label(r"layers:", font_size=30), kv).arrange(RIGHT, buff=0.2).move_to([0, 2.0, 0]).align_to([1.6, 0, 0], LEFT)
        pv = Integer(2, font_size=40, color=C.BITS)
        pl = VGroup(label(r"straight pieces:", font_size=30), pv).arrange(RIGHT, buff=0.2).next_to(kl, DOWN, buff=0.3)
        pl.align_to(kl, LEFT)
        rule = label(r"$k$ layers, \ $2k$ units: \ $2^k$ pieces; \\ one layer of $m$ units: \ at most $m + 1$",
                     font_size=26, color=C.BITS).next_to(pl, DOWN, buff=0.45).align_to(kl, LEFT)
        th = theorem_card(r"Depth separation", r"for every $k$, a network with $O(k^3)$ layers of $O(1)$ units computes "
                          r"a function that networks with $O(k)$ layers can only approximate with $\Omega(2^k)$ units",
                          who=r"M.~Telgarsky (2016)", width=5.6, font_size=20, color=HINGE).to_corner(DR, buff=0.25)
        with self.voiceover(
            "If one layer can do anything, why stack them? Here's the answer in one picture. Two units make a tent: "
            "up from zero to one, and back down. <bookmark mark='a'/> Feed the tent into another tent, and the line "
            "is folded twice: four pieces. <bookmark mark='b'/> Three layers, eight pieces. Five layers, thirty-two. "
            "Each layer doubles the pieces, while one wide layer gets only one more piece per unit. "
            "<bookmark mark='c'/> Matus Telgarsky turned this into a theorem in 2016: some functions that a deep, "
            "narrow network computes exactly need exponentially many units if the network is shallow."
        ) as vo:
            self.play(Create(ax), Create(ident), Write(f), FadeIn(fl))
            self.play(Transform(ident, teeth[0]), FadeIn(kl), FadeIn(pl))
            vo.wait_until("a")
            self.play(Transform(ident, teeth[1]), ChangeDecimalToValue(kv, 2), ChangeDecimalToValue(pv, 4))
            vo.wait_until("b")
            for k in (3, 4, 5):
                self.play(Transform(ident, teeth[k - 1]), ChangeDecimalToValue(kv, k), ChangeDecimalToValue(pv, 2 ** k),
                          run_time=1.0)
            self.play(FadeIn(rule))
            vo.wait_until("c")
            self.play(FadeIn(th, shift=UP * 0.2))
        self.wait(0.3)
        self.clear_scene()

    # ------------------------------------------------------------------
    def foldplane(self):
        d = load("fold")
        side = 4.6
        c = np.array([-3.4, -0.3, 0])
        K = int(d["n_folds"])
        pics = [fold_picture(np.asarray(d[f"fold{k}"]), side).move_to(c) for k in range(K + 1)]
        frame_ = Square(side, stroke_color=GREY_C, stroke_width=2).move_to(c)
        kv = Integer(0, font_size=36, color=HINGE)
        kl = VGroup(label(r"fold layers:", font_size=28), kv).arrange(RIGHT, buff=0.2)
        cv = Integer(1, font_size=36, color=C.BITS)
        cl = VGroup(label(r"linear pieces:", font_size=28), cv).arrange(RIGHT, buff=0.2)
        VGroup(kl, cl).arrange(DOWN, aligned_edge=LEFT, buff=0.25).move_to([3.0, 2.2, 0])
        lay = cmath(r"t \ \mapsto\ 2|t| - 1 \ = \ 2\max(0, t) + 2\max(0, -t) - 1", font_size=28).move_to([3.0, 0.8, 0])
        layl = label(r"one ReLU layer: \ fold the square in half, \ stretch it back", font_size=22, color=GREY_A)
        layl.next_to(lay, DOWN, buff=0.15)
        expl = label(r"every piece of the input \\ lands on the whole square, \\ mirrored", font_size=24, color=GREY_A)
        expl.move_to([3.0, -1.4, 0])
        tag = note(r"computed exactly: \ alternate folds along $x$ and $y$").to_corner(DR, buff=0.2)
        # the first fold, acted out: the left half of the picture, as a sheet of small squares, flips onto the right half
        n_ = 32
        q = (np.arange(n_) + 0.5) / n_ * 2 - 1
        Qg = np.stack(np.meshgrid(q, q), -1)
        cols_ = np.asarray(fold_picture_rgb(Qg))
        cell = side / n_
        left = VGroup(*[Square(cell, stroke_width=0, fill_color=ManimColor(cols_[i, j]), fill_opacity=1)
                        .move_to(c + np.array([(j + 0.5) * cell - side / 2, (i + 0.5) * cell - side / 2, 0]))
                        for i in range(n_) for j in range(n_ // 2)])
        with self.voiceover(
            "In two dimensions the same trick folds the plane. Here's a square with a picture on it: an F, so you can "
            "tell its mirror images apart. <bookmark mark='a'/> A ReLU layer can compute two times the absolute value "
            "of x, minus one: that folds the square in half along the middle, and stretches the half back to full "
            "size. <bookmark mark='b'/> Now colour each point of the input by where it lands: two mirrored copies of "
            "the picture. <bookmark mark='c'/> Fold again, along the other direction: four. Then eight, sixteen, "
            "thirty-two. <bookmark mark='d'/> Each layer doubles the number of linear pieces, and whatever the rest "
            "of the network draws on the folded square is drawn in every piece at once, mirrored. A deep network can "
            "reuse what it has built."
        ) as vo:
            self.play(FadeIn(pics[0]), Create(frame_), FadeIn(kl), FadeIn(cl), FadeIn(tag))
            vo.wait_until("a")
            self.play(Write(lay), FadeIn(layl))
            half = Rectangle(width=side / 2, height=side, stroke_width=0, fill_color=BACKGROUND, fill_opacity=1)
            half.move_to(c + LEFT * side / 4)
            crease = DashedLine(c + UP * side / 2, c + DOWN * side / 2, color=WHITE, stroke_width=2)
            self.add(half, left)
            self.play(Create(crease))
            self.play(Rotate(left, PI, axis=UP, about_point=c), run_time=1.6)
            vo.wait_until("b")
            self.play(FadeOut(left), FadeOut(half), FadeOut(crease), FadeOut(pics[0]), FadeIn(pics[1]),
                      ChangeDecimalToValue(kv, 1), ChangeDecimalToValue(cv, d["cells"][1]))
            vo.wait_until("c")
            self.play(FadeIn(expl))
            cur = pics[1]
            for k in range(2, K + 1):
                self.play(FadeOut(cur), FadeIn(pics[k]), ChangeDecimalToValue(kv, k), ChangeDecimalToValue(cv, d["cells"][k]),
                          run_time=1.1)
                cur = pics[k]
            vo.wait_until("d")
            self.play(Indicate(cv, color=C.BITS))
        self.wait(0.3)
        self.clear_scene()

    # ------------------------------------------------------------------
    def counting(self):
        d = load("fold")
        ol = np.asarray(d["one_layer"])  # n, counted, formula
        g = np.random.default_rng(3)  # a drawing of six lines (illustrative)
        c, side = np.array([-3.6, -0.3, 0]), 4.6
        sq = Square(side, stroke_color=GREY_D, stroke_width=1.5).move_to(c)
        lines = VGroup()
        h = side / 2
        for _ in range(6):
            a = g.uniform(0, np.pi)
            p0 = g.uniform(-0.9, 0.9, 2)
            dv = np.array([np.cos(a), np.sin(a)])
            ts = []
            for k in range(2):  # where the line crosses the square's edges
                if abs(dv[k]) > 1e-9:
                    ts += [(-h - p0[k]) / dv[k], (h - p0[k]) / dv[k]]
            ts = sorted(t for t in ts if np.all(np.abs(p0 + t * dv) <= h + 1e-9))
            a_, b_ = p0 + ts[0] * dv, p0 + ts[-1] * dv
            lines.add(Line(c + np.r_[a_, 0], c + np.r_[b_, 0], color=NEURON, stroke_width=2.5))
        tag = note(r"illustrative lines").next_to(sq, DOWN, buff=0.15)
        f = cmath(r"\text{pieces}", r"\le", r"1 + n + \tbinom{n}{2}", font_size=38).move_to([3.0, 2.5, 0])
        fl = label(r"one layer of $n$ ReLUs in the plane: \ $n$ lines", font_size=24, color=GREY_A).next_to(f, DOWN, buff=0.2)
        tab = VGroup()
        for n, cnt, form in ol:
            tab.add(VGroup(MathTex(rf"n = {n}", font_size=28), MathTex(rf"{cnt}", font_size=28, color=C.BITS),
                           MathTex(rf"{form}", font_size=28, color=GREY_A)))
        hd = VGroup(label(r"", font_size=22), label(r"counted", font_size=22, color=C.BITS),
                    label(r"formula", font_size=22, color=GREY_A))
        tab = VGroup(hd, *tab)
        for i, r_ in enumerate(tab):
            for j, m_ in enumerate(r_):
                m_.move_to([1.6 + 1.6 * j, 1.0 - 0.42 * i, 0])
        deep = label(r"deep networks can have exponentially many \\ in the depth \ (Mont\'ufar et al.\ 2014)",
                     font_size=24, color=HINGE).move_to([3.0, -2.6, 0])
        with self.voiceover(
            "Let's count pieces properly. Each unit of a first layer is a line in the plane: on one side it's off, on "
            "the other it's on. <bookmark mark='a'/> n lines in general position cut the plane into at most one, plus "
            "n, plus n choose two pieces, the classic count that Thomas Zaslavsky made general for hyperplanes in "
            "1975. <bookmark mark='b'/> Count them directly for random lines, and they match. Growth like n "
            "squared, in the plane; like n to the d in d dimensions. <bookmark mark='c'/> Deep networks can do far "
            "better: Guido Montufar and colleagues showed in 2014 that the maximum grows exponentially with depth, "
            "as the folds suggest."
        ) as vo:
            self.play(Create(sq), FadeIn(tag))
            self.play(LaggedStart(*[Create(ln) for ln in lines], lag_ratio=0.3), run_time=2.0)
            vo.wait_until("a")
            self.play(Write(f), FadeIn(fl))
            vo.wait_until("b")
            self.play(LaggedStart(*[FadeIn(r_) for r_ in tab], lag_ratio=0.2), run_time=2.0)
            vo.wait_until("c")
            self.play(FadeIn(deep))
        self.wait(0.3)
        self.clear_scene()

    # ------------------------------------------------------------------
    def random_nets(self):
        s = load("sawtooth")
        sp = load("spiral")
        depths, counts = [int(d) for d in s["depths"]], np.asarray(s["counts"])
        tiles = Group()
        for d, cnt in zip(depths, counts):
            img = patch_image(s[f"map{d}"], 2.3, 2.3, seed=d)
            cap = label(rf"${d}$ layer{'s' if d > 1 else ''} of ${48 // d}$", font_size=22, color=NEURON)
            num = label(rf"$\approx {cnt:.0f}$ pieces", font_size=22, color=WHITE)
            tiles.add(Group(img, VGroup(cap, num).arrange(DOWN, buff=0.06).next_to(img, DOWN, buff=0.12)))
        tiles.arrange(RIGHT, buff=0.3).move_to(UP * 0.4)
        head = label(r"$48$ ReLU units in the plane, \ randomly initialized, \ arranged in $1$ to $6$ layers", font_size=28)
        head.to_edge(UP, buff=0.4)
        keep = [int(k) for k in sp["keep"]]
        n0, n1 = int(sp[f"nreg{keep[0]}"]), int(sp[f"nreg{keep[-1]}"])
        note_ = label(rf"the spiral network of the opening: \ ${n0:,}$ pieces at the start, \ ${n1:,}$ after training"
                      .replace(",", "{,}"), font_size=26, color=C.BITS).to_edge(DOWN, buff=0.85)
        cite_ = cite(r"B.~Hanin \& D.~Rolnick, \textit{Deep ReLU Networks Have Surprisingly Few Activation Patterns} (2019)",
                     corner=DR)
        trend = "barely changes, and even falls" if counts[-1] < counts[0] * 1.2 else "grows only slowly"
        change = ("training rearranged the pieces far more than it multiplied them" if n1 < 3 * n0 else
                  "training multiplied them")
        with self.voiceover(
            "But that's what depth can do, with weights chosen by hand. What does a random network do? Here are "
            "forty-eight units cutting the plane, arranged in one layer, then two, three, four and six. "
            f"<bookmark mark='a'/> The number of pieces {trend}. Boris Hanin and David Rolnick proved in 2019 that, at "
            "initialization, typical networks have about as many pieces as their number of units to the power of "
            "the input dimension, nothing like the maximum, and found the same through training. <bookmark mark='b'/> Our spiral "
            f"network started with {n0:,} pieces and ended with {n1:,}: {change}. Depth helps in subtler ways, by "
            "making useful functions easy for training to reach."
        ) as vo:
            self.play(FadeIn(head))
            self.play(LaggedStart(*[FadeIn(t, shift=UP * 0.1) for t in tiles], lag_ratio=0.25), run_time=2.5)
            vo.wait_until("a")
            self.play(FadeIn(cite_))
            vo.wait_until("b")
            self.play(FadeIn(note_))
        self.wait(0.3)
        self.clear_scene()
